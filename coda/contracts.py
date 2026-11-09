from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

from adapters.base import ArtifactRecord, SourceRef, TextLocator
from coda.state import (
    AnalysisProtocolState,
    CodeState,
    CodebookAction,
    CodebookChangeState,
    CodebookState,
    CodingRecordState,
    HistoryState,
    HumanDecision,
    ResearchQuestionState,
)

CodebookRelationship = Literal[
    "reuse_existing_code",
    "new_code",
    "add_parent_code",
    "refine_existing_code",
    "merge_existing_codes",
    "split_existing_code",
    "uncertain",
]

ConfidenceLevel = Literal["high", "medium", "low"]

HumanReviewMode = Literal[
    "automatic",
    "selective",
    "full",
]

DisagreementType = Literal[
    "evidence_disagreement",
    "semantic_disagreement",
    "granularity_disagreement",
    "codebook_boundary_disagreement",
    "missing_context_disagreement",
    "output_format_inconsistency",
]

ComparisonType = Literal[
    "case_to_case",
    "case_to_code",
    "code_to_code",
]

ComparisonFindingType = Literal[
    "same_phenomenon",
    "distinct_phenomenon",
    "partial_overlap",
    "granularity_difference",
    "boundary_case",
    "insufficient_evidence",
]

AnalyticMemoType = Literal[
    "comparison",
    "category_boundary",
    "alternative_interpretation",
    "change_rationale",
    "unresolved_question",
]

ValidationSignalName = Literal[
    "valid",
    "evidence_insufficient",
    "unsupported_inference",
    "use_case_mismatch",
    "category_overlap",
    "boundary_unclear",
    "context_missing",
    "human_review_required",
]

ReviewCriterion = Literal["R1", "R2", "R3", "R4", "R5", "R6"]

ValidationIssueScope = Literal[
    "none",
    "evidence",
    "assignment",
    "codebook",
    "context",
]


@dataclass(frozen=True)
class EvidenceItem:
    """One grounded evidence snippet linked back to the original artifact."""

    field_name: str
    excerpt: str
    locator: TextLocator | None = None
    source_ref: SourceRef | None = None
    rationale: str = ""
    rationale_zh: str = ""
    claim_type: Literal["reported", "observed", "inferred"] = "reported"
    revision: str | None = None


@dataclass(frozen=True)
class HistoricalExample:
    """One prior reviewed example surfaced during arbitration or validation."""

    artifact_id: str
    code_ids: list[str] = field(default_factory=list)
    code_names: list[str] = field(default_factory=list)
    note: str = ""
    human_reviewed: bool = False
    review_origin: str = "agent_generated"


@dataclass(frozen=True)
class ContextAgentInput:
    """Inputs required by the Context Agent for one artifact."""

    artifact: ArtifactRecord
    research_question: ResearchQuestionState
    analysis_protocol: AnalysisProtocolState | None = None
    additional_context: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class ContextPacket:
    """Structured context prepared for downstream coders."""

    artifact_id: str
    context_brief: str
    context_brief_zh: str = ""
    evidence_items: list[EvidenceItem] = field(default_factory=list)
    missing_context_warnings: list[str] = field(default_factory=list)
    missing_context_warnings_zh: list[str] = field(default_factory=list)
    distracting_information: list[str] = field(default_factory=list)
    distracting_information_zh: list[str] = field(default_factory=list)
    source_refs: list[SourceRef] = field(default_factory=list)
    model_metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ProvisionalCode:
    """One candidate code proposed by a coder."""

    code_name: str
    short_definition: str
    code_name_zh: str = ""
    short_definition_zh: str = ""
    observed_phenomenon: str = ""
    observed_phenomenon_zh: str = ""
    supporting_evidence: list[EvidenceItem] = field(default_factory=list)
    relationship_to_codebook: CodebookRelationship = "uncertain"
    linked_code_ids: list[str] = field(default_factory=list)
    alternative_interpretation: str = ""
    alternative_interpretation_zh: str = ""
    uncertainty_note: str = ""
    uncertainty_note_zh: str = ""
    proposed_codebook_action: CodebookAction = "no_change"
    proposed_codebook_target_ids: list[str] = field(default_factory=list)
    inclusion_criteria: list[str] = field(default_factory=list)
    exclusion_criteria: list[str] = field(default_factory=list)
    inclusion_criteria_zh: list[str] = field(default_factory=list)
    exclusion_criteria_zh: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class CoderAgentInput:
    """Codebook-blind inputs required by one independent coder agent."""

    artifact: ArtifactRecord
    research_question: ResearchQuestionState
    context_packet: ContextPacket
    coder_id: str
    analysis_protocol: AnalysisProtocolState | None = None


@dataclass(frozen=True)
class CoderAgentOutput:
    """Structured output of one independent coder agent."""

    artifact_id: str
    coder_id: str
    provisional_codes: list[ProvisionalCode] = field(default_factory=list)
    insufficient_context: bool = False
    overall_uncertainty: str = ""
    overall_uncertainty_zh: str = ""
    confidence_level: ConfidenceLevel = "low"
    confidence_rationale: str = ""
    confidence_rationale_zh: str = ""
    confidence_factors: dict[str, str] = field(default_factory=dict)
    notes: list[str] = field(default_factory=list)
    notes_zh: list[str] = field(default_factory=list)
    model_metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class InitialCodingCase:
    """Two or more independent, codebook-free readings of one bootstrap case."""

    artifact_id: str
    context_packet: ContextPacket
    coder_outputs: list[CoderAgentOutput] = field(default_factory=list)
    original_material: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.context_packet.artifact_id != self.artifact_id:
            raise ValueError("InitialCodingCase context packet belongs to another artifact.")
        if len(self.coder_outputs) < 2:
            raise ValueError("InitialCodingCase requires at least two independent coder outputs.")
        if any(output.artifact_id != self.artifact_id for output in self.coder_outputs):
            raise ValueError("InitialCodingCase coder output belongs to another artifact.")


@dataclass(frozen=True)
class InductionAgentInput:
    """Evidence-grounded initial codes to consolidate into a provisional codebook."""

    research_question: ResearchQuestionState
    cases: list[InitialCodingCase]
    existing_draft_codes: list[CodeState] = field(default_factory=list)
    allowed_artifact_ids: list[str] = field(default_factory=list)
    batch_index: int = 0
    analysis_protocol: AnalysisProtocolState | None = None
    validation_feedback: list[dict[str, Any]] = field(default_factory=list)
    induction_stage: Literal["incremental_batch", "global_consolidation"] = "incremental_batch"


@dataclass(frozen=True)
class InductionAgentOutput:
    """One complete provisional codebook draft and its induction audit trail."""

    codes: list[CodeState]
    change_log: list[dict[str, Any]] = field(default_factory=list)
    analytic_memos: list[dict[str, Any]] = field(default_factory=list)
    model_metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class DisagreementRecord:
    """One preserved disagreement identified during arbitration."""

    disagreement_type: DisagreementType
    summary: str
    summary_zh: str = ""
    coder_ids: list[str] = field(default_factory=list)
    affected_code_names: list[str] = field(default_factory=list)
    evidence_items: list[EvidenceItem] = field(default_factory=list)


@dataclass(frozen=True)
class ComparisonFinding:
    """One explicit result of constant comparison between cases or codes."""

    comparison_id: str
    comparison_type: ComparisonType
    finding: ComparisonFindingType
    summary: str
    summary_zh: str = ""
    current_artifact_id: str = ""
    compared_artifact_ids: list[str] = field(default_factory=list)
    compared_code_ids: list[str] = field(default_factory=list)
    evidence_items: list[EvidenceItem] = field(default_factory=list)
    implication: str = ""
    implication_zh: str = ""
    resolution_status: Literal["unresolved", "resolved", "complementary", "permitted"] | None = None


@dataclass(frozen=True)
class AnalyticMemo:
    """A traceable analytical note retained across coding iterations."""

    memo_id: str
    memo_type: AnalyticMemoType
    summary: str
    summary_zh: str = ""
    artifact_ids: list[str] = field(default_factory=list)
    code_ids: list[str] = field(default_factory=list)
    status: Literal["open", "resolved"] = "open"


@dataclass(frozen=True)
class ComparisonInput:
    """Inputs required by the Comparison Agent."""

    artifact: ArtifactRecord
    research_question: ResearchQuestionState
    context_packet: ContextPacket
    coder_outputs: list[CoderAgentOutput]
    codebook: CodebookState
    history: HistoryState
    analysis_protocol: AnalysisProtocolState | None = None
    historical_materials: dict[str, Any] = field(default_factory=dict)
    task: Literal["case_comparison", "codebook_refinement", "retrospective_reassessment", "batch_recheck"] = "case_comparison"
    prior_comparison: dict[str, Any] = field(default_factory=dict)
    defer_refinement: bool = False

    def __post_init__(self) -> None:
        if not self.coder_outputs:
            msg = "ComparisonInput requires at least one coder output."
            raise ValueError(msg)


@dataclass(frozen=True)
class ComparisonOutput:
    """Constant-comparison result produced for the current artifact."""

    artifact_id: str
    agreement_summary: str
    disagreement_summary: str
    agreement_summary_zh: str = ""
    disagreement_summary_zh: str = ""
    recommended_codes: list[ProvisionalCode] = field(default_factory=list)
    preserved_alternatives: list[ProvisionalCode] = field(default_factory=list)
    disagreements: list[DisagreementRecord] = field(default_factory=list)
    relevant_historical_examples: list[HistoricalExample] = field(default_factory=list)
    possible_codebook_changes: list[CodebookChangeState] = field(default_factory=list)
    comparison_findings: list[ComparisonFinding] = field(default_factory=list)
    analytic_memos: list[AnalyticMemo] = field(default_factory=list)
    prior_human_conflicts: list[dict[str, Any]] = field(default_factory=list)
    model_metadata: dict[str, Any] = field(default_factory=dict)


# Persisted traces and external clients still use the original names. These
# aliases preserve that interface while the method is expressed as comparison.
ArbitrationInput = ComparisonInput
ArbitrationOutput = ComparisonOutput


@dataclass(frozen=True)
class ValidationSignal:
    """One structured warning or confirmation emitted by validation."""

    signal: ValidationSignalName
    summary: str
    issue_scope: ValidationIssueScope = "none"
    summary_zh: str = ""
    related_code_names: list[str] = field(default_factory=list)
    evidence_items: list[EvidenceItem] = field(default_factory=list)


@dataclass(frozen=True)
class ValidationInput:
    """Inputs required by the Validation Agent."""

    artifact: ArtifactRecord
    research_question: ResearchQuestionState
    context_packet: ContextPacket
    coder_outputs: list[CoderAgentOutput]
    codebook: CodebookState
    history: HistoryState
    comparison_output: ComparisonOutput | None = None
    arbitration_output: ArbitrationOutput | None = None
    analysis_protocol: AnalysisProtocolState | None = None
    validation_scope: Literal["proposal", "initial_codebook", "iterative_decision", "final_audit"] = "proposal"
    corpus_audit: dict[str, Any] = field(default_factory=dict)
    historical_materials: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        output = self.comparison_output or self.arbitration_output
        if output is None:
            raise ValueError("ValidationInput requires comparison_output.")
        object.__setattr__(self, "comparison_output", output)
        object.__setattr__(self, "arbitration_output", output)


@dataclass(frozen=True)
class ValidationOutput:
    """Structured validation result for the current artifact."""

    artifact_id: str
    signals: list[ValidationSignal] = field(default_factory=list)
    human_review_required: bool = False
    summary: str = ""
    summary_zh: str = ""
    confidence_level: ConfidenceLevel = "low"
    confidence_rationale: str = ""
    confidence_rationale_zh: str = ""
    confidence_factors: dict[str, str] = field(default_factory=dict)
    review_criteria: list[ReviewCriterion] = field(default_factory=list)
    review_questions: list[str] = field(default_factory=list)
    review_questions_zh: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)
    notes_zh: list[str] = field(default_factory=list)
    model_metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class CodebookChangePacket:
    """Category-level review material kept separate from a case assignment."""

    change_id: str
    action: CodebookAction
    summary: str
    summary_zh: str = ""
    rationale: str = ""
    rationale_zh: str = ""
    before_codes: list[CodeState] = field(default_factory=list)
    proposed_codes: list[CodeState] = field(default_factory=list)
    supporting_artifact_ids: list[str] = field(default_factory=list)
    boundary_artifact_ids: list[str] = field(default_factory=list)
    affected_artifact_ids: list[str] = field(default_factory=list)
    validation_warnings: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class ReviewRoutingDecision:
    """Transparent rule result used by Automatic, Selective, and Full settings."""

    artifact_id: str
    setting: str
    route: Literal["automatic_accept", "human_review", "unresolved"]
    reasons: list[str] = field(default_factory=list)
    risk_signals: list[str] = field(default_factory=list)
    random_audit: bool = False
    evidence_audit: bool = False
    review_origin: str = "none"
    risk_score: int = 0
    signal_details: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class EvidencePacket:
    """Human-facing packet that consolidates all agent-side analysis."""

    artifact_id: str
    original_artifact: ArtifactRecord
    research_question: ResearchQuestionState
    context_packet: ContextPacket
    coder_outputs: list[CoderAgentOutput]
    candidate_definitions: list[str] = field(default_factory=list)
    candidate_definitions_zh: list[str] = field(default_factory=list)
    alternative_interpretations: list[str] = field(default_factory=list)
    alternative_interpretations_zh: list[str] = field(default_factory=list)
    comparison_output: ComparisonOutput | None = None
    arbitration_output: ArbitrationOutput | None = None
    validation_output: ValidationOutput | None = None
    proposed_codebook_changes: list[CodebookChangeState] = field(default_factory=list)
    codebook_change_packets: list[CodebookChangePacket] = field(default_factory=list)
    comparison_findings: list[ComparisonFinding] = field(default_factory=list)
    analytic_memos: list[AnalyticMemo] = field(default_factory=list)
    model_metadata: dict[str, Any] = field(default_factory=dict)
    routing_decision: ReviewRoutingDecision | None = None

    def __post_init__(self) -> None:
        output = self.comparison_output or self.arbitration_output
        object.__setattr__(self, "comparison_output", output)
        object.__setattr__(self, "arbitration_output", output)


@dataclass(frozen=True)
class HumanReviewInput:
    """Inputs presented to the human reviewer."""

    artifact: ArtifactRecord
    research_question: ResearchQuestionState
    evidence_packet: EvidencePacket
    codebook: CodebookState
    history: HistoryState
    analysis_protocol: AnalysisProtocolState | None = None


@dataclass(frozen=True)
class HumanReviewOutput:
    """Final human decision for the current artifact and codebook."""

    artifact_id: str
    decision: HumanDecision
    pre_read_memo: str = ""
    final_codes: list[CodeState] = field(default_factory=list)
    rationale: str = ""
    evidence_summary: list[str] = field(default_factory=list)
    confirmed_evidence: list[EvidenceItem] = field(default_factory=list)
    preserved_alternatives: list[str] = field(default_factory=list)
    codebook_changes: list[CodebookChangeState] = field(default_factory=list)
    request_additional_context: bool = False
    notes: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_coding_record(
        self,
        *,
        dataset_name: str,
        batch_index: int,
        codebook_version_before: int,
        codebook_version_after: int,
        record_id: str,
        validation_output: ValidationOutput | None = None,
    ) -> CodingRecordState:
        return CodingRecordState(
            record_id=record_id,
            artifact_id=self.artifact_id,
            dataset_name=dataset_name,
            batch_index=batch_index,
            codebook_version=codebook_version_after,
            codebook_version_before=codebook_version_before,
            codebook_version_after=codebook_version_after,
            decision=self.decision,
            pre_read_memo=self.pre_read_memo,
            final_code_ids=[code.code_id for code in self.final_codes],
            final_code_names=[code.name for code in self.final_codes],
            rationale=self.rationale,
            evidence_summary=list(self.evidence_summary),
            preserved_alternatives=list(self.preserved_alternatives),
            validation_signals=(
                [signal.signal for signal in validation_output.signals]
                if validation_output is not None
                else []
            ),
            notes=list(self.notes),
            metadata={
                **dict(self.metadata),
                "confirmed_evidence": [
                    {
                        "field_name": item.field_name,
                        "excerpt": item.excerpt,
                        "locator": (
                            {
                                "start": item.locator.start,
                                "end": item.locator.end,
                            }
                            if item.locator is not None
                            else None
                        ),
                        "rationale": item.rationale,
                        "rationale_zh": item.rationale_zh,
                        "claim_type": item.claim_type,
                        "revision": item.revision,
                    }
                    for item in self.confirmed_evidence
                ],
            },
        )
