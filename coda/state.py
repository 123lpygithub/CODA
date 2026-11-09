from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import Any, Literal
from uuid import uuid4

from adapters.base import ArtifactRecord, DatasetMetadata

HumanDecision = Literal[
    "accept",
    "revise",
    "reject",
    "mark_uncertain",
    "request_additional_context",
]

CodebookAction = Literal[
    "add",
    "add_parent",
    "refine",
    "merge",
    "split",
    "rename",
    "retire",
    "no_change",
]
CodeStatus = Literal["active", "merged", "split", "retired"]
CounterexampleStatus = Literal[
    "not_assessed",
    "no_observed_counterexample",
    "observed_counterexample",
]
SplitName = Literal["coding_pool", "held_out_pool"]
RunStatus = Literal[
    "not_started",
    "awaiting_initial_review",
    "in_progress",
    "awaiting_human_review",
    "awaiting_context",
    "awaiting_next_artifact",
    "awaiting_final_review",
    "stabilized",
    "completed_with_unresolved",
    "resource_limited",
    "completed",
]
ReviewSetting = Literal["automatic", "selective", "full"]
ExperimentVariant = Literal[
    "standard",
    "freeze_after_initialization",
    "without_retrospective_recoding",
]
StageReviewKind = Literal["initial", "triggered", "final"]
StageReviewDecision = Literal[
    "accept",
    "revise",
    "reject",
    "request_additional_context",
    "mark_unresolved",
]
UnresolvedStatus = Literal["open", "resolved"]
RetrospectiveTaskStatus = Literal[
    "pending",
    "prepared",
    "awaiting_human",
    "completed",
    "cancelled",
]
ContextRequestStatus = Literal["pending", "resolved", "cancelled"]


@dataclass
class ResearchQuestionState:
    """Runtime representation of Q in I_t = <Q, D_t, B_t, H_t>."""

    dataset_name: str
    question_text: str
    analysis_scope: str
    use_case: str
    artifact_unit: str
    sensitizing_concepts: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    @classmethod
    def from_dataset_metadata(
        cls,
        metadata: DatasetMetadata,
        *,
        analysis_scope: str | None = None,
        sensitizing_concepts: list[str] | None = None,
        notes: list[str] | None = None,
    ) -> ResearchQuestionState:
        return cls(
            dataset_name=metadata.dataset_name,
            question_text=metadata.research_question,
            analysis_scope=analysis_scope or metadata.data_description,
            use_case=metadata.use_case,
            artifact_unit=metadata.artifact_unit,
            sensitizing_concepts=list(sensitizing_concepts or []),
            notes=list(notes or []),
        )


@dataclass
class AnalysisProtocolState:
    """Pre-registered analytical constraints supplied to every CODA stage."""

    artifact_unit: str
    evidence_unit: str = "A traceable span from an artifact"
    allow_cross_span_evidence: bool = True
    allow_multiple_codes: bool = True
    allow_unit_adjustment: bool = True
    predefined_codebook_allowed: bool = False
    held_out_may_update_codebook: bool = False
    notes: list[str] = field(default_factory=list)


@dataclass
class ReviewPolicyState:
    """Frozen, transparent routing policy for one experimental setting."""

    setting: ReviewSetting = "full"
    initial_review_required: bool = True
    final_review_required: bool = True
    # TSE27-CODA S2 requires a deterministic 10% audit of decisions that did
    # not already trigger R1-R6.  The name is kept for checkpoint compatibility.
    random_audit_rate: float = 0.10
    random_seed: int = 20260907
    # Evidence auditing is retained as an audit metric for older runs, but it
    # is not an additional human-review trigger in the paper protocol.
    evidence_audit_rate: float = 0.0
    evidence_audit_seed: int = 20260908
    review_budget_minutes: int | None = None
    high_impact_case_threshold: int = 5
    # Deprecated compatibility field.  Review routing must never depend on a
    # confidence/risk score threshold; R1-R6 are criterion-based.
    selective_review_score_threshold: int = 3
    risk_aggregation: Literal["sum", "max"] = "sum"
    risk_weights: dict[str, int] = field(
        default_factory=lambda: {
            "missing_context": 3,
            "substantive_coder_disagreement": 3,
            "new_or_ambiguous_boundary": 3,
            "new_code_proposal": 3,
            "structural_codebook_change": 3,
            "validation_warning": 3,
            "high_impact_codebook_revision": 3,
            "conflict_with_prior_human_boundary": 3,
        }
    )
    calibration_version: str = "selective-review-v2"
    retrospective_semantic_top_k: int = 5
    retrospective_semantic_min_score: float = 0.08
    automatic_reassessment_limit: int = 2
    # Deprecated compatibility fields. R1-R6 routing no longer consults these
    # switches, but old checkpoints remain readable.
    require_review_for_disagreement: bool = True
    require_review_for_missing_context: bool = True
    require_review_for_boundary_change: bool = True
    stabilization_window_size: int = 10
    stabilization_required_consecutive_batches: int = 2
    frozen: bool = True
    notes: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not 0.0 <= self.random_audit_rate <= 1.0:
            raise ValueError("random_audit_rate must be between 0 and 1.")
        if not 0.0 <= self.evidence_audit_rate <= 1.0:
            raise ValueError("evidence_audit_rate must be between 0 and 1.")
        if self.review_budget_minutes is not None and self.review_budget_minutes <= 0:
            raise ValueError("review_budget_minutes must be positive when provided.")
        if self.high_impact_case_threshold < 1:
            raise ValueError("high_impact_case_threshold must be positive.")
        if self.selective_review_score_threshold < 1:
            raise ValueError("selective_review_score_threshold must be positive.")
        if self.risk_aggregation not in {"sum", "max"}:
            raise ValueError("risk_aggregation must be 'sum' or 'max'.")
        if any(weight < 0 for weight in self.risk_weights.values()):
            raise ValueError("risk_weights cannot contain negative values.")
        if self.retrospective_semantic_top_k < 0:
            raise ValueError("retrospective_semantic_top_k cannot be negative.")
        if self.automatic_reassessment_limit < 1:
            raise ValueError("automatic_reassessment_limit must be positive.")
        if not 0.0 <= self.retrospective_semantic_min_score <= 1.0:
            raise ValueError("retrospective_semantic_min_score must be between 0 and 1.")
        if self.stabilization_window_size < 1:
            raise ValueError("stabilization_window_size must be positive.")
        if self.stabilization_required_consecutive_batches < 1:
            raise ValueError(
                "stabilization_required_consecutive_batches must be positive."
            )
        if self.setting == "automatic":
            self.initial_review_required = False
            self.final_review_required = False
            self.random_audit_rate = 0.0
            self.evidence_audit_rate = 0.0
        elif self.setting == "full":
            self.initial_review_required = True
            self.final_review_required = True


@dataclass
class UnresolvedCaseState:
    """One explicit item in U_t rather than an implicit note or empty coding."""

    unresolved_id: str
    artifact_id: str
    reason: str
    source: str
    created_at_codebook_version: int
    status: UnresolvedStatus = "open"
    related_code_ids: list[str] = field(default_factory=list)
    requested_context: list[str] = field(default_factory=list)
    resolution: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class StageReviewState:
    """Initial, triggered, or final human review with auditable provenance."""

    review_id: str
    kind: StageReviewKind
    decision: StageReviewDecision
    rationale: str
    codebook_version_before: int
    codebook_version_after: int
    reviewer_id: str = "researcher"
    duration_seconds: float | None = None
    artifact_ids: list[str] = field(default_factory=list)
    change_ids: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class StabilizationCheckState:
    """Operational coding-stability audit; it is not theoretical saturation."""

    check_id: str
    codebook_version: int
    processed_artifacts: int
    remaining_artifacts: int
    open_unresolved_count: int
    pending_retrospective_count: int
    recent_new_code_count: int
    recent_substantive_revision_count: int
    window_size: int
    stable: bool
    consecutive_stable_batches: int = 0
    cross_source_audit_status: str = "not_run"
    cross_source_audit_artifact_ids: list[str] = field(default_factory=list)
    reasons: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class ArtifactBatchState:
    """Runtime representation of D_t for one coding round."""

    batch_id: str
    dataset_name: str
    batch_index: int
    split_name: SplitName
    artifacts: list[ArtifactRecord]
    group_ids: dict[str, str] = field(default_factory=dict)
    sampling_note: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.batch_index < 0:
            msg = "batch_index must be non-negative."
            raise ValueError(msg)
        if not self.artifacts:
            msg = "ArtifactBatchState must contain at least one artifact."
            raise ValueError(msg)
        duplicate_ids = len(self.artifact_ids) != len(set(self.artifact_ids))
        if duplicate_ids:
            msg = f"Duplicate artifact ids found in batch {self.batch_id}."
            raise ValueError(msg)

    @property
    def artifact_ids(self) -> list[str]:
        return [artifact.artifact_id for artifact in self.artifacts]

    @property
    def size(self) -> int:
        return len(self.artifacts)

    def contains(self, artifact_id: str) -> bool:
        return artifact_id in set(self.artifact_ids)


@dataclass
class CodeState:
    """One code definition inside the current codebook."""

    code_id: str
    name: str
    definition: str
    inclusion_criteria: list[str] = field(default_factory=list)
    exclusion_criteria: list[str] = field(default_factory=list)
    representative_artifact_ids: list[str] = field(default_factory=list)
    boundary_artifact_ids: list[str] = field(default_factory=list)
    counterexample_status: CounterexampleStatus = "not_assessed"
    hypothetical_examples: list[str] = field(default_factory=list)
    parent_code_id: str | None = None
    status: CodeStatus = "active"
    notes: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class CodebookChangeState:
    """One human-approved codebook change recorded in history."""

    change_id: str
    action: CodebookAction
    round_index: int
    summary: str
    summary_zh: str = ""
    rationale: str = ""
    rationale_zh: str = ""
    target_code_ids: list[str] = field(default_factory=list)
    resulting_code_ids: list[str] = field(default_factory=list)
    artifact_ids: list[str] = field(default_factory=list)
    decided_by: str = "human"
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.round_index < 0:
            msg = "round_index must be non-negative."
            raise ValueError(msg)


@dataclass
class CodebookState:
    """Runtime representation of B_t."""

    dataset_name: str
    version: int
    codes: list[CodeState] = field(default_factory=list)
    sensitizing_concepts: list[str] = field(default_factory=list)
    revisions: list[CodebookChangeState] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.version < 0:
            msg = "Codebook version must be non-negative."
            raise ValueError(msg)
        code_ids = [code.code_id for code in self.codes]
        if len(code_ids) != len(set(code_ids)):
            msg = "CodeState.code_id values must be unique inside a codebook."
            raise ValueError(msg)

    @classmethod
    def empty(
        cls,
        dataset_name: str,
        *,
        sensitizing_concepts: list[str] | None = None,
        notes: list[str] | None = None,
    ) -> CodebookState:
        return cls(
            dataset_name=dataset_name,
            version=0,
            codes=[],
            sensitizing_concepts=list(sensitizing_concepts or []),
            revisions=[],
            notes=list(notes or []),
        )

    def active_codes(self) -> list[CodeState]:
        return [code for code in self.codes if code.status == "active"]

    def get_code(self, code_id: str) -> CodeState | None:
        for code in self.codes:
            if code.code_id == code_id:
                return code
        return None

    def with_codes(
        self,
        codes: list[CodeState],
    ) -> CodebookState:
        """Replace runtime code entries without treating it as a new version."""

        return replace(self, codes=list(codes))

    def next_version(
        self,
        *,
        codes: list[CodeState] | None = None,
        new_revision: CodebookChangeState | None = None,
        notes: list[str] | None = None,
    ) -> CodebookState:
        revisions = list(self.revisions)
        if new_revision is not None:
            revisions.append(new_revision)
        return replace(
            self,
            version=self.version + 1,
            codes=list(codes if codes is not None else self.codes),
            revisions=revisions,
            notes=list(notes if notes is not None else self.notes),
        )


@dataclass
class CodingRecordState:
    """One human-reviewed artifact-level coding record."""

    record_id: str
    artifact_id: str
    dataset_name: str
    batch_index: int
    codebook_version: int
    decision: HumanDecision
    codebook_version_before: int | None = None
    codebook_version_after: int | None = None
    pre_read_memo: str = ""
    final_code_ids: list[str] = field(default_factory=list)
    final_code_names: list[str] = field(default_factory=list)
    rationale: str = ""
    evidence_summary: list[str] = field(default_factory=list)
    preserved_alternatives: list[str] = field(default_factory=list)
    validation_signals: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.batch_index < 0:
            msg = "batch_index must be non-negative."
            raise ValueError(msg)
        if self.codebook_version < 0:
            msg = "codebook_version must be non-negative."
            raise ValueError(msg)
        if self.codebook_version_before is None:
            self.codebook_version_before = self.codebook_version
        if self.codebook_version_after is None:
            self.codebook_version_after = self.codebook_version
        if self.codebook_version_before < 0 or self.codebook_version_after < 0:
            raise ValueError("Coding record codebook versions must be non-negative.")


@dataclass
class ContextRequestState:
    """Actionable request for material that was missing during review."""

    request_id: str
    scope: Literal["artifact", "initial", "final"]
    reason: str
    requested_items: list[str]
    created_at_codebook_version: int
    artifact_id: str | None = None
    status: ContextRequestStatus = "pending"
    resolution: str = ""
    supplied_context: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class RetrospectiveRecodingTask:
    """A versioned request to reconsider an already coded artifact.

    Retrospective work is append-only: the original CodingRecordState remains
    intact and the later record carries the task id and version transition.
    """

    task_id: str
    artifact_id: str
    trigger_change_id: str
    from_codebook_version: int
    target_codebook_version: int
    status: RetrospectiveTaskStatus = "pending"
    reason: str = ""
    attempt_count: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.from_codebook_version < 0 or self.target_codebook_version < 0:
            msg = "Retrospective task codebook versions must be non-negative."
            raise ValueError(msg)
        if self.target_codebook_version < self.from_codebook_version:
            msg = "Retrospective task target version cannot precede its source version."
            raise ValueError(msg)
        if self.attempt_count < 0:
            msg = "Retrospective task attempt_count must be non-negative."
            raise ValueError(msg)


@dataclass
class HistoryState:
    """Runtime representation of H_t."""

    coding_records: list[CodingRecordState] = field(default_factory=list)
    codebook_revisions: list[CodebookChangeState] = field(default_factory=list)
    analytic_memos: list[dict[str, Any]] = field(default_factory=list)
    retrospective_tasks: list[RetrospectiveRecodingTask] = field(default_factory=list)
    unresolved_cases: list[UnresolvedCaseState] = field(default_factory=list)
    stage_reviews: list[StageReviewState] = field(default_factory=list)
    stabilization_checks: list[StabilizationCheckState] = field(default_factory=list)
    context_requests: list[ContextRequestState] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    def reviewed_artifact_ids(self) -> list[str]:
        latest = {record.artifact_id: record for record in self.coding_records}
        # A rejected proposal is a request to reconsider this case. Its audit
        # record must not make the controller silently skip the case.
        return [artifact_id for artifact_id, record in latest.items()
                if record.decision != "reject"]

    def latest_record_for_artifact(self, artifact_id: str) -> CodingRecordState | None:
        for record in reversed(self.coding_records):
            if record.artifact_id == artifact_id:
                return record
        return None

    def append_record(self, record: CodingRecordState) -> None:
        self.coding_records.append(record)

    def append_revision(self, revision: CodebookChangeState) -> None:
        self.codebook_revisions.append(revision)

    def append_analytic_memo(self, memo: dict[str, Any]) -> dict[str, Any]:
        stored = dict(memo)
        stored.setdefault("memo_id", f"memo-{uuid4().hex[:12]}")
        stored.setdefault("status", "open")
        stored.setdefault(
            "status_history",
            [{"status": stored["status"], "source": "created"}],
        )
        self.analytic_memos.append(stored)
        return stored

    def analytic_memo(self, memo_id: str) -> dict[str, Any] | None:
        for memo in self.analytic_memos:
            if memo.get("memo_id") == memo_id:
                return memo
        return None

    def append_retrospective_task(self, task: RetrospectiveRecodingTask) -> None:
        self.retrospective_tasks.append(task)

    def pending_retrospective_tasks(self) -> list[RetrospectiveRecodingTask]:
        return [
            task
            for task in self.retrospective_tasks
            if task.status in {"pending", "prepared", "awaiting_human"}
        ]

    def retrospective_task(self, task_id: str) -> RetrospectiveRecodingTask | None:
        for task in self.retrospective_tasks:
            if task.task_id == task_id:
                return task
        return None

    def append_unresolved(self, item: UnresolvedCaseState) -> None:
        self.unresolved_cases.append(item)

    def open_unresolved_cases(self) -> list[UnresolvedCaseState]:
        return [item for item in self.unresolved_cases if item.status == "open"]

    def append_stage_review(self, review: StageReviewState) -> None:
        self.stage_reviews.append(review)

    def latest_stage_review(self, kind: StageReviewKind) -> StageReviewState | None:
        for review in reversed(self.stage_reviews):
            if review.kind == kind:
                return review
        return None

    def append_stabilization_check(self, check: StabilizationCheckState) -> None:
        self.stabilization_checks.append(check)

    def append_context_request(self, request: ContextRequestState) -> None:
        self.context_requests.append(request)

    def pending_context_requests(self) -> list[ContextRequestState]:
        return [item for item in self.context_requests if item.status == "pending"]


@dataclass
class RunState:
    """Top-level runtime object that carries the evolving CODA state."""

    run_id: str
    dataset_metadata: DatasetMetadata
    research_question: ResearchQuestionState
    codebook: CodebookState
    history: HistoryState
    coding_batches: list[ArtifactBatchState]
    held_out_batches: list[ArtifactBatchState] = field(default_factory=list)
    analysis_protocol: AnalysisProtocolState | None = None
    review_policy: ReviewPolicyState = field(default_factory=ReviewPolicyState)
    current_batch_index: int = 0
    status: RunStatus = "not_started"
    notes: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        dataset_name = self.dataset_metadata.dataset_name
        if self.analysis_protocol is None:
            self.analysis_protocol = AnalysisProtocolState(
                artifact_unit=self.dataset_metadata.artifact_unit
            )
        if self.research_question.dataset_name != dataset_name:
            msg = "ResearchQuestionState dataset_name must match DatasetMetadata."
            raise ValueError(msg)
        if self.codebook.dataset_name != dataset_name:
            msg = "CodebookState dataset_name must match DatasetMetadata."
            raise ValueError(msg)
        if self.current_batch_index < 0:
            msg = "current_batch_index must be non-negative."
            raise ValueError(msg)
        if self.current_batch_index > len(self.coding_batches):
            msg = "current_batch_index cannot exceed the number of coding batches."
            raise ValueError(msg)

        for batch in self.coding_batches:
            if batch.dataset_name != dataset_name:
                msg = f"Coding batch {batch.batch_id} belongs to the wrong dataset."
                raise ValueError(msg)
            if batch.split_name != "coding_pool":
                msg = f"Coding batch {batch.batch_id} must use split_name='coding_pool'."
                raise ValueError(msg)

        for batch in self.held_out_batches:
            if batch.dataset_name != dataset_name:
                msg = f"Held-out batch {batch.batch_id} belongs to the wrong dataset."
                raise ValueError(msg)
            if batch.split_name != "held_out_pool":
                msg = f"Held-out batch {batch.batch_id} must use split_name='held_out_pool'."
                raise ValueError(msg)

    @classmethod
    def initialize(
        cls,
        dataset_metadata: DatasetMetadata,
        *,
        coding_batches: list[ArtifactBatchState],
        held_out_batches: list[ArtifactBatchState] | None = None,
        sensitizing_concepts: list[str] | None = None,
        run_id: str | None = None,
        notes: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
        analysis_protocol: AnalysisProtocolState | None = None,
        review_policy: ReviewPolicyState | None = None,
    ) -> RunState:
        dataset_name = dataset_metadata.dataset_name
        return cls(
            run_id=run_id or f"run-{uuid4().hex[:12]}",
            dataset_metadata=dataset_metadata,
            research_question=ResearchQuestionState.from_dataset_metadata(
                dataset_metadata,
                sensitizing_concepts=sensitizing_concepts,
            ),
            codebook=CodebookState.empty(
                dataset_name,
                sensitizing_concepts=sensitizing_concepts,
            ),
            history=HistoryState(),
            coding_batches=list(coding_batches),
            held_out_batches=list(held_out_batches or []),
            analysis_protocol=analysis_protocol or AnalysisProtocolState(
                artifact_unit=dataset_metadata.artifact_unit
            ),
            review_policy=review_policy or ReviewPolicyState(),
            current_batch_index=0,
            status="not_started",
            notes=list(notes or []),
            metadata=dict(metadata or {}),
        )

    @property
    def total_coding_artifacts(self) -> int:
        return sum(batch.size for batch in self.coding_batches)

    @property
    def total_held_out_artifacts(self) -> int:
        return sum(batch.size for batch in self.held_out_batches)

    def current_batch(self) -> ArtifactBatchState | None:
        if self.current_batch_index >= len(self.coding_batches):
            return None
        return self.coding_batches[self.current_batch_index]

    def current_input(
        self,
    ) -> tuple[ResearchQuestionState, ArtifactBatchState, CodebookState, HistoryState] | None:
        batch = self.current_batch()
        if batch is None:
            return None
        return (self.research_question, batch, self.codebook, self.history)

    def has_remaining_coding_batches(self) -> bool:
        return self.current_batch() is not None

    def advance_to_next_batch(self) -> None:
        if self.current_batch_index >= len(self.coding_batches):
            msg = "No remaining coding batch to advance to."
            raise IndexError(msg)
        self.current_batch_index += 1
