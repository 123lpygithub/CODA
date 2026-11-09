"""LLM bootstrap for CODA's initial, explicitly provisional codebook.

This module is deliberately separate from the human-review orchestration.  Its
output is a starting point for open coding, not a set of completed coding
records or a hidden reference taxonomy.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Callable

from adapters.base import ArtifactRecord
from coda.agents.base import BaseLLMAgent, AgentPromptSpec, AgentRefusalError, AgentExecutionError
from coda.agents.coder_agent import build_initial_open_coder
from coda.agents.common import ground_context_packet
from coda.agents.induction_agent import InductionLLMAgent
from coda.bootstrap_checkpoints import BootstrapCheckpointStore
from coda.prompts import read_prompt_file
from coda.contracts import (
    ComparisonOutput,
    CoderAgentInput,
    CoderAgentOutput,
    ContextAgentInput,
    ContextPacket,
    InductionAgentInput,
    InductionAgentOutput,
    InitialCodingCase,
    ProvisionalCode,
    ValidationInput,
    ValidationIssueScope,
    ValidationOutput,
)
from coda.llm import (
    ChatBackend,
    LLMMessage,
    LLMModelConfig,
    LLMRequestCancelledError,
)
from coda.parsing import extract_json_object
from coda.state import CodeState, CodebookState, HistoryState, RunState

ContextAgent = Callable[[ContextAgentInput], ContextPacket]
InitialCoder = Callable[[CoderAgentInput], CoderAgentOutput]
InductionAgent = Callable[[InductionAgentInput], InductionAgentOutput]
ValidationAgent = Callable[[ValidationInput], ValidationOutput]
ProgressCallback = Callable[[dict[str, Any]], None]
CancelCallback = Callable[[], bool]


class BootstrapCancelledError(RuntimeError):
    """Raised after persisting completed stages when bootstrap is paused."""


@dataclass(frozen=True)
class BootstrapConfig:
    """Protocol parameters that must be fixed before starting a run."""

    enabled: bool = True
    fraction: float = 0.20
    # Keep small, researcher-selected runs proportional to the protocol.  A
    # fixed floor of 20 made a 20-artifact smoke run sample 19 artifacts after
    # the ``total - 1`` safeguard, instead of the intended 20% (4 artifacts).
    minimum_size: int = 1
    maximum_size: int = 150
    random_seed: int = 20260907
    batch_size: int = 12
    sampler: str = "group_aware_diversity"
    stratification_enabled: bool = True
    stratification_fields: tuple[str, ...] = (
        "repo_name",
        "year",
        "source_kind",
    )
    validation_reinduction_rounds: int = 1
    fixed_artifact_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not 0.0 < self.fraction < 1.0:
            raise ValueError("Bootstrap fraction must be between 0 and 1.")
        if self.minimum_size < 1 or self.maximum_size < self.minimum_size:
            raise ValueError("Bootstrap sample bounds are invalid.")
        if self.batch_size < 1:
            raise ValueError("Bootstrap batch_size must be positive.")
        if self.validation_reinduction_rounds < 0:
            raise ValueError("validation_reinduction_rounds cannot be negative.")
        if self.stratification_enabled and not self.stratification_fields:
            raise ValueError("stratification_fields cannot be empty when stratification is enabled.")

    @classmethod
    def from_env(cls) -> BootstrapConfig:
        """Build the frozen sampling protocol from optional environment settings."""

        stratification = os.getenv("CODA_BOOTSTRAP_STRATIFICATION", "true")
        fields = tuple(
            field_name.strip()
            for field_name in os.getenv(
                "CODA_BOOTSTRAP_STRATIFICATION_FIELDS",
                "repo_name,year,source_kind",
            ).split(",")
            if field_name.strip()
        )
        return cls(
            fraction=float(os.getenv("CODA_BOOTSTRAP_FRACTION", "0.20")),
            minimum_size=int(os.getenv("CODA_BOOTSTRAP_MINIMUM_SIZE", "1")),
            maximum_size=int(os.getenv("CODA_BOOTSTRAP_MAXIMUM_SIZE", "150")),
            random_seed=int(os.getenv("CODA_BOOTSTRAP_RANDOM_SEED", "20260907")),
            batch_size=int(os.getenv("CODA_BOOTSTRAP_BATCH_SIZE", "12")),
            stratification_enabled=stratification.strip().lower()
            not in {"0", "false", "no", "off"},
            stratification_fields=fields,
        )


@dataclass(frozen=True)
class BootstrapAssignment:
    artifact_id: str
    code_ids: list[str]
    evidence_summary: list[str]
    status: str = "bootstrap_provisional"


@dataclass(frozen=True)
class BootstrapResult:
    codebook: CodebookState
    artifact_ids: list[str]
    group_ids: dict[str, str]
    assignments: list[BootstrapAssignment] = field(default_factory=list)
    context_packets: list[dict[str, Any]] = field(default_factory=list)
    initial_codings: list[InitialCodingCase] = field(default_factory=list)
    change_log: list[dict[str, Any]] = field(default_factory=list)
    analytic_memos: list[dict[str, Any]] = field(default_factory=list)
    draft_codebooks: list[dict[str, Any]] = field(default_factory=list)
    supporting_model_calls: list[dict[str, Any]] = field(default_factory=list)
    audit_warnings: list[str] = field(default_factory=list)
    audit_warnings_zh: list[str] = field(default_factory=list)
    validation_outputs: list[ValidationOutput] = field(default_factory=list)
    protocol: dict[str, Any] = field(default_factory=dict)
    progress: dict[str, Any] = field(default_factory=dict)
    status: str = "completed"
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def artifact_group_id(artifact: ArtifactRecord) -> str:
    """Return a visible grouping key without accessing reference annotations."""

    for key in ("thread_id", "discussion_id", "base_issue_url", "issue_url", "repo_name"):
        value = artifact.metadata.get(key)
        if value is None:
            value = artifact.raw_fields.get(key)
        if isinstance(value, str) and value.strip():
            return f"{key}:{value.strip()}"
    return f"artifact:{artifact.artifact_id}"


def _terms(artifact: ArtifactRecord) -> set[str]:
    return set(re.findall(r"[a-z0-9_]{3,}", artifact.content.lower()))


def _artifact_stratum_value(artifact: ArtifactRecord, field_name: str) -> str | None:
    if field_name == "source_kind":
        return artifact.source_refs[0].kind if artifact.source_refs else None
    value = artifact.metadata.get(field_name)
    if value is None:
        value = artifact.raw_fields.get(field_name)
    if value is None and field_name == "year":
        for candidate in ("created_at", "date", "timestamp", "published_at"):
            raw_value = artifact.metadata.get(candidate, artifact.raw_fields.get(candidate))
            match = re.search(r"\b(19|20)\d{2}\b", str(raw_value or ""))
            if match:
                value = match.group(0)
                break
    text = str(value).strip() if value is not None else ""
    return text or None


def _group_strata(
    artifacts: list[ArtifactRecord],
    fields: tuple[str, ...],
) -> set[str]:
    return {
        f"{field_name}:{value}"
        for artifact in artifacts
        for field_name in fields
        if (value := _artifact_stratum_value(artifact, field_name)) is not None
    }


def _sample_size(total: int, config: BootstrapConfig) -> int:
    if total < 2:
        return 0
    desired = min(max(math.ceil(config.fraction * total), config.minimum_size), config.maximum_size)
    # Small smoke runs must retain at least one artifact for actual human review.
    return min(desired, total - 1)


def bootstrap_sample_size(total: int, config: BootstrapConfig | None = None) -> int:
    """Return the number of artifacts the fixed bootstrap will inspect."""

    return _sample_size(total, config or BootstrapConfig())


def select_bootstrap_artifacts(
    artifacts: list[ArtifactRecord],
    config: BootstrapConfig,
) -> tuple[list[ArtifactRecord], dict[str, str]]:
    """Select visible-text-diverse groups while keeping every group intact."""

    target = _sample_size(len(artifacts), config)
    group_ids = {artifact.artifact_id: artifact_group_id(artifact) for artifact in artifacts}
    if config.fixed_artifact_ids:
        by_id = {artifact.artifact_id: artifact for artifact in artifacts}
        if len(set(config.fixed_artifact_ids)) != len(config.fixed_artifact_ids) or set(config.fixed_artifact_ids) - set(by_id):
            raise ValueError("Fixed initialization IDs must be unique members of the run corpus.")
        return [by_id[key] for key in config.fixed_artifact_ids], group_ids
    if target == 0:
        return [], group_ids

    groups: dict[str, list[ArtifactRecord]] = {}
    for artifact in artifacts:
        groups.setdefault(group_ids[artifact.artifact_id], []).append(artifact)

    # Greedy MMR-like selection: prioritise groups whose visible vocabulary adds
    # the most new material, with deterministic ID tie-breaking.
    selected: list[ArtifactRecord] = []
    selected_terms: set[str] = set()
    selected_strata: set[str] = set()
    remaining = sorted(
        groups.items(),
        key=lambda item: hashlib.sha256(
            f"{config.random_seed}:{item[0]}".encode("utf-8")
        ).hexdigest(),
    )
    while remaining:
        candidates = [item for item in remaining if len(selected) + len(item[1]) <= target]
        if not candidates:
            break

        def score(item: tuple[str, list[ArtifactRecord]]) -> tuple[float, float, float, str]:
            vocabulary = set().union(*(_terms(artifact) for artifact in item[1]))
            novelty = len(vocabulary - selected_terms) / max(1, len(vocabulary))
            strata = (
                _group_strata(item[1], config.stratification_fields)
                if config.stratification_enabled
                else set()
            )
            stratum_gain = float(len(strata - selected_strata))
            tie_break = hashlib.sha256(
                f"{config.random_seed}:{item[0]}".encode("utf-8")
            ).hexdigest()
            # Cover unseen strata first, then maximise visible-text diversity.
            return (stratum_gain, novelty, -float(len(item[1])), tie_break)

        best = max(candidates, key=score)
        selected.extend(best[1])
        selected_terms.update(*(_terms(artifact) for artifact in best[1]))
        selected_strata.update(_group_strata(best[1], config.stratification_fields))
        remaining.remove(best)
    return selected, group_ids


class EvidenceFirstBootstrap:
    """Independently code evidence, induce categories, and audit provisional B1."""

    def __init__(
        self,
        *,
        model_config: LLMModelConfig,
        backend: ChatBackend,
        context_agent: ContextAgent,
        initial_coder_agents: list[tuple[str, InitialCoder]] | None = None,
        induction_agent: InductionAgent | None = None,
        validation_agent: ValidationAgent | None = None,
        config: BootstrapConfig | None = None,
    ) -> None:
        self._model_config = model_config
        self._backend = backend
        self._context_agent = context_agent
        self._initial_coder_agents = initial_coder_agents or [
            (
                "initial-coder-a",
                build_initial_open_coder(model_config=model_config, backend=backend),
            ),
            (
                "initial-coder-b",
                build_initial_open_coder(model_config=model_config, backend=backend),
            ),
        ]
        if len(self._initial_coder_agents) != 2:
            raise ValueError("Bootstrap requires exactly two independent initial coders.")
        if len({coder_id for coder_id, _ in self._initial_coder_agents}) != 2:
            raise ValueError("Bootstrap initial coder ids must be distinct.")
        self._induction_agent = induction_agent or InductionLLMAgent(
            model_config=model_config,
            backend=backend,
        )
        self._validation_agent = validation_agent
        self.config = config or BootstrapConfig()
        self._supporting_model_calls: list[dict[str, Any]] = []
        self._output_language = "en"

    def set_output_language(self, language: str) -> None:
        """Set the preferred explanation language for every bootstrap model."""

        if language not in {"en", "zh"}:
            raise ValueError("Output language must be 'en' or 'zh'.")
        self._output_language = language
        for _, coder in self._initial_coder_agents:
            setter = getattr(coder, "set_output_language", None)
            if setter is not None:
                setter(language)
        for agent in (self._induction_agent, self._validation_agent):
            setter = getattr(agent, "set_output_language", None)
            if setter is not None:
                setter(language)

    @property
    def initial_coder_models(self) -> dict[str, str]:
        """Return the configured model for each initial coder, when inspectable."""

        models: dict[str, str] = {}
        for coder_id, coder in self._initial_coder_agents:
            model_config = getattr(coder, "model_config", None)
            models[coder_id] = str(getattr(model_config, "model", "custom-callable"))
        return models

    @staticmethod
    def _agent_fingerprint(name: str, agent: Any) -> dict[str, Any]:
        bound_owner = getattr(agent, "__self__", None)
        if bound_owner is not None and hasattr(bound_owner, "_context_agent"):
            agent = getattr(bound_owner, "_context_agent")
        prompt = getattr(agent, "_prompt_spec", None)
        model_config = getattr(agent, "_model_config", None)
        return {
            "name": name,
            "callable": (
                f"{agent.__class__.__module__}.{agent.__class__.__qualname__}"
                if not hasattr(agent, "__qualname__")
                else f"{agent.__module__}.{agent.__qualname__}"
            ),
            "model": asdict(model_config) if model_config is not None else None,
            "system_prompt": getattr(prompt, "system_prompt", None),
            "user_prompt_template": getattr(prompt, "user_prompt_template", None),
        }

    def _resume_cache_key(
        self,
        run_state: RunState,
        selected: list[ArtifactRecord],
        protocol: dict[str, Any],
    ) -> str:
        payload = {
            "format_version": 1,
            "language": self._output_language,
            "research_question": asdict(run_state.research_question),
            "analysis_protocol": asdict(run_state.analysis_protocol),
            "initial_revision_feedback": run_state.metadata.get("initial_revision_feedback", []),
            "protocol": protocol,
            "artifacts": [asdict(artifact) for artifact in selected],
            # Assignment and compatibility-audit calls are implemented by this
            # bootstrap object rather than a role-specific Agent instance.
            "bootstrap_supporting_model": asdict(self._model_config),
            "bootstrap_supporting_prompt_contract_version": 4,
            "induction_assignment_system_prompt": read_prompt_file(
                "induction_assignment_system_prompt.txt"
            ),
            "agents": [
                self._agent_fingerprint("context", self._context_agent),
                *(
                    self._agent_fingerprint(coder_id, coder)
                    for coder_id, coder in self._initial_coder_agents
                ),
                self._agent_fingerprint("induction", self._induction_agent),
                self._agent_fingerprint("validation", self._validation_agent)
                if self._validation_agent is not None
                else None,
            ],
        }
        return hashlib.sha256(
            json.dumps(payload, ensure_ascii=False, sort_keys=True, default=str).encode(
                "utf-8"
            )
        ).hexdigest()

    def run(
        self,
        run_state: RunState,
        artifacts: list[ArtifactRecord],
        *,
        progress_callback: ProgressCallback | None = None,
        checkpoint_dir: str | Path | None = None,
        cancel_requested: CancelCallback | None = None,
    ) -> BootstrapResult:
        self._supporting_model_calls = []
        induction_config = getattr(self._induction_agent, "model_config", None)
        protocol = {
            **asdict(self.config),
            "population_size": len(artifacts),
            "workflow": "independent_initial_coding_then_induction",
            "initial_coder_models": self.initial_coder_models,
            "induction_model": str(getattr(induction_config, "model", "custom-callable")),
        }
        if not self.config.enabled:
            progress = self._progress(
                status="disabled",
                phase="disabled",
                processed_artifacts=0,
                total_artifacts=0,
                overall_completed=0,
                overall_total=0,
            )
            self._notify(progress_callback, progress)
            return BootstrapResult(
                codebook=CodebookState.empty(run_state.dataset_metadata.dataset_name),
                artifact_ids=[],
                group_ids={artifact.artifact_id: artifact_group_id(artifact) for artifact in artifacts},
                status="disabled",
                audit_warnings=["Bootstrap was disabled by the run protocol."],
                audit_warnings_zh=["初始化已被本次运行协议禁用。"],
                protocol=protocol,
                progress=progress,
            )
        selected, group_ids = select_bootstrap_artifacts(artifacts, self.config)
        self._assignment_materials = {artifact.artifact_id: {
            "content": artifact.content, "raw_fields": artifact.raw_fields,
            "source_refs": [asdict(ref) for ref in artifact.source_refs],
        } for artifact in selected}
        if not selected:
            progress = self._progress(
                status="skipped",
                phase="skipped",
                processed_artifacts=0,
                total_artifacts=0,
                overall_completed=0,
                overall_total=0,
            )
            self._notify(progress_callback, progress)
            return BootstrapResult(
                codebook=CodebookState.empty(run_state.dataset_metadata.dataset_name),
                artifact_ids=[],
                group_ids=group_ids,
                status="skipped",
                audit_warnings=["Bootstrap skipped because this run has fewer than two artifacts."],
                audit_warnings_zh=["由于本次运行少于两个分析材料，已跳过初始化。"],
                protocol=protocol,
                progress=progress,
            )
        total = len(selected)
        checkpoint_store = (
            BootstrapCheckpointStore(
                checkpoint_dir,
                cache_key=self._resume_cache_key(run_state, selected, protocol),
            )
            if checkpoint_dir is not None
            else None
        )
        if checkpoint_store is not None:
            checkpoint_store.put(
                "manifest",
                {
                    "format": "coda-bootstrap-checkpoints",
                    "format_version": 1,
                    "artifact_ids": [artifact.artifact_id for artifact in selected],
                    "language": self._output_language,
                    "protocol": protocol,
                },
            )
        # Reserve progress for the validation-driven refinement pass. Without
        # these stages, initial validation reached 100% before re-induction,
        # reassignment, and revalidation had actually finished.
        stage_total = 8 if self.config.validation_reinduction_rounds > 0 else 5
        overall_total = total * stage_total
        last_progress = self._progress(
            status="running",
            phase="evidence",
            processed_artifacts=0,
            total_artifacts=total,
            overall_completed=0,
            overall_total=overall_total,
        )
        self._notify(progress_callback, last_progress)
        self._configure_backend_cancellation(cancel_requested)

        def check_cancelled() -> None:
            if cancel_requested is not None and cancel_requested():
                raise BootstrapCancelledError("Bootstrap initialization was cancelled.")

        def report(
            *,
            phase: str,
            processed_artifacts: int,
            overall_completed: int,
            current_artifact_id: str | None = None,
        ) -> None:
            nonlocal last_progress
            last_progress = self._progress(
                status="running",
                phase=phase,
                processed_artifacts=processed_artifacts,
                total_artifacts=total,
                overall_completed=overall_completed,
                overall_total=overall_total,
                current_artifact_id=current_artifact_id,
            )
            self._notify(progress_callback, last_progress)

        try:
            packets: list[ContextPacket] = []
            for index, artifact in enumerate(selected, 1):
                check_cancelled()
                checkpoint_stage = f"context/{artifact.artifact_id}"
                packet = (
                    checkpoint_store.get(checkpoint_stage, ContextPacket)
                    if checkpoint_store is not None
                    else None
                )
                if packet is None:
                    packet = ground_context_packet(
                        artifact,
                        self._context_agent(
                            ContextAgentInput(
                                artifact=artifact,
                                research_question=run_state.research_question,
                                analysis_protocol=run_state.analysis_protocol,
                            ),
                        ),
                    )
                    if checkpoint_store is not None:
                        checkpoint_store.put(checkpoint_stage, packet)
                packets.append(packet)
                report(
                    phase="evidence",
                    processed_artifacts=index,
                    overall_completed=index,
                    current_artifact_id=artifact.artifact_id,
                )
            report(
                phase="initial_coding",
                processed_artifacts=0,
                overall_completed=total,
            )
            initial_codings = self._run_initial_coding(
                run_state,
                selected,
                packets,
                checkpoint_store=checkpoint_store,
                cancel_requested=cancel_requested,
                progress_callback=lambda processed, artifact_id: report(
                    phase="initial_coding",
                    processed_artifacts=processed,
                    overall_completed=total + processed,
                    current_artifact_id=artifact_id,
                ),
            )
            report(
                phase="induction",
                processed_artifacts=0,
                overall_completed=total * 2,
            )
            codes, change_log, draft_codebooks, analytic_memos = self._induce_codes(
                run_state,
                packets,
                initial_codings,
                checkpoint_store=checkpoint_store,
                checkpoint_prefix="induction/initial",
                cancel_requested=cancel_requested,
                validation_feedback=[{"source": "initial_human_rejection", "summary": item}
                                     for item in run_state.metadata.get("initial_revision_feedback", [])],
                progress_callback=lambda processed: report(
                    phase="induction",
                    processed_artifacts=processed,
                    overall_completed=total * 2 + processed,
                ),
            )
            report(
                phase="assignment",
                processed_artifacts=0,
                overall_completed=total * 3,
            )
            assignments = self._label_artifacts(
                codes,
                packets,
                checkpoint_store=checkpoint_store,
                checkpoint_prefix="assignment/initial",
                analysis_protocol=asdict(run_state.analysis_protocol),
                research_question=run_state.research_question.question_text,
                cancel_requested=cancel_requested,
                progress_callback=lambda processed: report(
                    phase="assignment",
                    processed_artifacts=processed,
                    overall_completed=total * 3 + processed,
                ),
            )
            report(
                phase="validation",
                processed_artifacts=0,
                overall_completed=total * 4,
            )
            validation_outputs: list[ValidationOutput] = []
            self._grouping_memos = list(analytic_memos)
            if self._validation_agent is not None:
                validation_outputs = self._validate_bootstrap(
                    run_state=run_state,
                    artifacts=selected,
                    packets=packets,
                    initial_codings=initial_codings,
                    codes=codes,
                    assignments=assignments,
                    checkpoint_store=checkpoint_store,
                    checkpoint_prefix="validation/initial",
                    cancel_requested=cancel_requested,
                    progress_callback=lambda processed: report(
                        phase="validation",
                        processed_artifacts=processed,
                        overall_completed=total * 4 + processed,
                    ),
                )
                initial_warnings = self._validation_warnings(validation_outputs)
                initial_warnings_zh = self._validation_warnings_zh(validation_outputs)
                warnings = list(initial_warnings)
                warnings_zh = list(initial_warnings_zh)
                codebook_feedback = self._validation_feedback(
                    validation_outputs,
                    scopes={"codebook"},
                )
                assignment_feedback = self._validation_feedback(
                    validation_outputs,
                    scopes={"assignment", "evidence"},
                )
                correction_feedback: list[dict[str, Any]] = []
                correction_prefix = ""
                if codebook_feedback and self.config.validation_reinduction_rounds > 0:
                    report(
                        phase="reinduction",
                        processed_artifacts=0,
                        overall_completed=total * 5,
                    )
                    revised_codes, revised_changes, revised_drafts, revised_memos = self._induce_codes(
                        run_state,
                        packets,
                        initial_codings,
                        checkpoint_store=checkpoint_store,
                        checkpoint_prefix="induction/reinduced",
                        cancel_requested=cancel_requested,
                        validation_feedback=codebook_feedback,
                        progress_callback=lambda processed: report(
                            phase="reinduction",
                            processed_artifacts=processed,
                            overall_completed=total * 5 + processed,
                        ),
                    )
                    codes = revised_codes
                    change_log.extend(revised_changes)
                    draft_codebooks.extend(revised_drafts)
                    analytic_memos.extend(revised_memos)
                    correction_feedback = [*codebook_feedback, *assignment_feedback]
                    correction_prefix = "reinduced"
                elif assignment_feedback and self.config.validation_reinduction_rounds > 0:
                    correction_feedback = assignment_feedback
                    correction_prefix = "corrected"

                if correction_feedback:
                    self._grouping_memos = list(analytic_memos)
                    report(
                        phase="reassignment",
                        processed_artifacts=0,
                        overall_completed=total * 6,
                    )
                    assignments = self._label_artifacts(
                        codes,
                        packets,
                        checkpoint_store=checkpoint_store,
                        checkpoint_prefix=f"assignment/{correction_prefix}",
                        analysis_protocol=asdict(run_state.analysis_protocol),
                        research_question=run_state.research_question.question_text,
                        cancel_requested=cancel_requested,
                        validation_feedback=correction_feedback,
                        progress_callback=lambda processed: report(
                            phase="reassignment",
                            processed_artifacts=processed,
                            overall_completed=total * 6 + processed,
                        ),
                    )
                    report(
                        phase="revalidation",
                        processed_artifacts=0,
                        overall_completed=total * 7,
                    )
                    validation_outputs = self._validate_bootstrap(
                        run_state=run_state,
                        artifacts=selected,
                        packets=packets,
                        initial_codings=initial_codings,
                        codes=codes,
                        assignments=assignments,
                        checkpoint_store=checkpoint_store,
                        checkpoint_prefix=f"validation/{correction_prefix}",
                        cancel_requested=cancel_requested,
                        progress_callback=lambda processed: report(
                            phase="revalidation",
                            processed_artifacts=processed,
                            overall_completed=total * 7 + processed,
                        ),
                    )
                    warnings = list(
                        dict.fromkeys(
                            [*initial_warnings, *self._validation_warnings(validation_outputs)]
                        )
                    )
                    warnings_zh = list(
                        dict.fromkeys(
                            [
                                *initial_warnings_zh,
                                *self._validation_warnings_zh(validation_outputs),
                            ]
                        )
                    )
            else:
                # Compatibility path for injected test/bootstrap implementations.
                # The production web workflow always supplies the standard validator.
                warnings, warnings_zh = self._audit_codes(codes, packets)
                report(
                    phase="audit",
                    processed_artifacts=total,
                    overall_completed=total * 5,
                )
            for code in codes:
                code.metadata["audit_warnings"] = list(warnings)
                code.metadata["audit_warnings_zh"] = list(warnings_zh)
            codebook = CodebookState(
                dataset_name=run_state.dataset_metadata.dataset_name,
                version=1,
                codes=codes,
                notes=[
                    "LLM bootstrap B1: induced from two independent initial coders; not human-reviewed.",
                    "Human review may add, refine, merge, split, rename, or retire any B1 code.",
                ],
            )
            completed_progress = self._progress(
                status="completed",
                phase="completed",
                processed_artifacts=total,
                total_artifacts=total,
                overall_completed=overall_total,
                overall_total=overall_total,
            )
            self._notify(progress_callback, completed_progress)
            return BootstrapResult(
                codebook=codebook,
                artifact_ids=[artifact.artifact_id for artifact in selected],
                group_ids=group_ids,
                assignments=assignments,
                context_packets=[asdict(packet) for packet in packets],
                initial_codings=initial_codings,
                change_log=change_log,
                analytic_memos=analytic_memos,
                draft_codebooks=draft_codebooks,
                supporting_model_calls=list(self._supporting_model_calls),
                audit_warnings=warnings,
                audit_warnings_zh=warnings_zh,
                validation_outputs=validation_outputs,
                protocol=protocol,
                progress=completed_progress,
            )
        except (BootstrapCancelledError, LLMRequestCancelledError) as error:
            raise BootstrapCancelledError("Bootstrap initialization was cancelled.") from error
        except AgentExecutionError as error:
            # Semantic output failure is different from a transport failure.
            # BaseLLMAgent has already used its one allowed format repair;
            # make the affected initial decisions explicitly reviewable as R6.
            reason = f"Initialization output is unusable: {type(error).__name__}: {error}"
            outputs = [ValidationOutput(
                artifact_id=item.artifact_id, human_review_required=True,
                review_criteria=["R6"], summary=reason,
                review_questions=["Repair the initial proposal, supply context, or leave this case unresolved?"],
            ) for item in selected]
            return BootstrapResult(
                codebook=CodebookState.empty(run_state.dataset_metadata.dataset_name),
                artifact_ids=[item.artifact_id for item in selected], group_ids=group_ids,
                assignments=[BootstrapAssignment(item.artifact_id, [], [reason], "unresolved_R6") for item in selected],
                context_packets=[asdict(packet) for packet in packets],
                initial_codings=list(locals().get("initial_codings", [])),
                supporting_model_calls=list(self._supporting_model_calls),
                validation_outputs=outputs, audit_warnings=[reason],
                protocol=protocol, status="completed",
                progress=self._progress(status="completed", phase="completed", processed_artifacts=total,
                    total_artifacts=total, overall_completed=overall_total, overall_total=overall_total),
            )
        except Exception as error:  # A bad automatic draft must never block human-led coding.
            failed_progress = dict(last_progress)
            failed_progress.update(
                {
                    "status": "failed",
                    "phase": "failed",
                    "error": f"{type(error).__name__}: {error}",
                }
            )
            self._notify(progress_callback, failed_progress)
            return BootstrapResult(
                codebook=CodebookState.empty(
                    run_state.dataset_metadata.dataset_name,
                    notes=["LLM bootstrap failed; the run starts with an empty codebook."],
                ),
                artifact_ids=[artifact.artifact_id for artifact in selected],
                group_ids=group_ids,
                status="failed",
                error=f"{type(error).__name__}: {error}",
                audit_warnings=["Bootstrap output was discarded and no automatic codes were used."],
                audit_warnings_zh=["初始化结果已丢弃，未使用自动生成的编码。"],
                protocol=protocol,
                progress=failed_progress,
            )
        finally:
            self._configure_backend_cancellation(None)

    def _run_initial_coding(
        self,
        run_state: RunState,
        artifacts: list[ArtifactRecord],
        packets: list[ContextPacket],
        checkpoint_store: BootstrapCheckpointStore | None = None,
        progress_callback: Callable[[int, str], None] | None = None,
        cancel_requested: CancelCallback | None = None,
    ) -> list[InitialCodingCase]:
        """Run both coders against identical evidence with no shared codebook or history."""

        artifact_by_id = {artifact.artifact_id: artifact for artifact in artifacts}
        cases: list[InitialCodingCase] = []
        for index, packet in enumerate(packets, 1):
            self._check_cancelled(cancel_requested)
            artifact = artifact_by_id[packet.artifact_id]
            outputs_by_id: dict[str, CoderAgentOutput] = {}
            missing: list[tuple[str, InitialCoder]] = []
            for coder_id, coder in self._initial_coder_agents:
                stage = f"initial-coding/{artifact.artifact_id}/{coder_id}"
                cached = (
                    checkpoint_store.get(stage, CoderAgentOutput)
                    if checkpoint_store is not None
                    else None
                )
                if cached is None:
                    missing.append((coder_id, coder))
                else:
                    outputs_by_id[coder_id] = cached
            if missing:
                errors: list[Exception] = []
                with ThreadPoolExecutor(
                    max_workers=len(missing),
                    thread_name_prefix="coda-bootstrap-coder",
                ) as executor:
                    futures = {
                        executor.submit(
                            coder,
                            CoderAgentInput(
                                artifact=artifact,
                                research_question=run_state.research_question,
                                context_packet=packet,
                                coder_id=coder_id,
                                analysis_protocol=run_state.analysis_protocol,
                            ),
                        ): coder_id
                        for coder_id, coder in missing
                    }
                    for future in as_completed(futures):
                        coder_id = futures[future]
                        try:
                            output = future.result()
                        except Exception as error:  # Preserve successful peer output.
                            errors.append(error)
                            continue
                        outputs_by_id[coder_id] = output
                        if checkpoint_store is not None:
                            checkpoint_store.put(
                                f"initial-coding/{artifact.artifact_id}/{coder_id}",
                                output,
                            )
                if errors:
                    raise errors[0]
            outputs = [
                outputs_by_id[coder_id]
                for coder_id, _coder in self._initial_coder_agents
            ]
            cases.append(
                InitialCodingCase(
                    artifact_id=artifact.artifact_id,
                    context_packet=packet,
                    coder_outputs=outputs,
                    original_material={"content": artifact.content, "raw_fields": artifact.raw_fields,
                                       "source_refs": [asdict(ref) for ref in artifact.source_refs]},
                )
            )
            if progress_callback is not None:
                progress_callback(index, artifact.artifact_id)
        return cases

    def _induce_codes(
        self,
        run_state: RunState,
        packets: list[ContextPacket],
        initial_codings: list[InitialCodingCase],
        checkpoint_store: BootstrapCheckpointStore | None = None,
        checkpoint_prefix: str = "induction",
        progress_callback: Callable[[int], None] | None = None,
        validation_feedback: list[dict[str, Any]] | None = None,
        cancel_requested: CancelCallback | None = None,
    ) -> tuple[
        list[CodeState],
        list[dict[str, Any]],
        list[dict[str, Any]],
        list[dict[str, Any]],
    ]:
        draft: list[CodeState] = []
        changes: list[dict[str, Any]] = []
        drafts: list[dict[str, Any]] = []
        analytic_memos: list[dict[str, Any]] = []
        processed = 0
        coding_by_artifact = {case.artifact_id: case for case in initial_codings}
        allowed_artifact_ids = [packet.artifact_id for packet in packets]
        for index in range(0, len(packets), self.config.batch_size):
            self._check_cancelled(cancel_requested)
            batch = packets[index : index + self.config.batch_size]
            batch_index = index // self.config.batch_size
            stage = f"{checkpoint_prefix}/batch-{batch_index:04d}"
            output = (
                checkpoint_store.get(stage, InductionAgentOutput)
                if checkpoint_store is not None
                else None
            )
            if output is None:
                output = self._induction_agent(
                    InductionAgentInput(
                        research_question=run_state.research_question,
                        cases=[coding_by_artifact[packet.artifact_id] for packet in batch],
                        existing_draft_codes=draft,
                        allowed_artifact_ids=allowed_artifact_ids,
                        batch_index=batch_index,
                        analysis_protocol=run_state.analysis_protocol,
                        validation_feedback=list(validation_feedback or []),
                        induction_stage=(
                            "global_consolidation"
                            if len(packets) <= self.config.batch_size
                            else "incremental_batch"
                        ),
                    )
                )
                if checkpoint_store is not None:
                    checkpoint_store.put(stage, output)
            draft = output.codes
            changes.extend(output.change_log)
            analytic_memos.extend(output.analytic_memos)
            processed += len(batch)
            if progress_callback is not None:
                progress_callback(processed)
            drafts.append(
                {
                    "stage": "incremental_batch",
                    "batch_index": batch_index,
                    "artifact_ids": [packet.artifact_id for packet in batch],
                    "codes": [asdict(code) for code in draft],
                    "change_log": output.change_log,
                    "analytic_memos": output.analytic_memos,
                    "model_metadata": output.model_metadata,
                }
            )
        batch_count = math.ceil(len(packets) / self.config.batch_size)
        if batch_count > 1:
            self._check_cancelled(cancel_requested)
            # Incremental drafts keep each request bounded, but a final pass must
            # see every evidence-grounded provisional code. Otherwise evidence
            # from early batches is reduced to the previous draft's labels and
            # definitions, which weakens constant comparison.
            stage = f"{checkpoint_prefix}/global-consolidation"
            output = (
                checkpoint_store.get(stage, InductionAgentOutput)
                if checkpoint_store is not None
                else None
            )
            if output is None:
                output = self._induction_agent(
                    InductionAgentInput(
                        research_question=run_state.research_question,
                        cases=list(initial_codings),
                        existing_draft_codes=draft,
                        allowed_artifact_ids=allowed_artifact_ids,
                        batch_index=batch_count,
                        analysis_protocol=run_state.analysis_protocol,
                        validation_feedback=list(validation_feedback or []),
                        induction_stage="global_consolidation",
                    )
                )
                if checkpoint_store is not None:
                    checkpoint_store.put(stage, output)
            draft = output.codes
            changes.extend(output.change_log)
            analytic_memos.extend(output.analytic_memos)
            drafts.append(
                {
                    "stage": "global_consolidation",
                    "batch_index": batch_count,
                    "artifact_ids": list(allowed_artifact_ids),
                    "codes": [asdict(code) for code in draft],
                    "change_log": output.change_log,
                    "analytic_memos": output.analytic_memos,
                    "model_metadata": output.model_metadata,
                }
            )
        if not draft:
            raise ValueError("Induction Agent returned no usable codes.")
        evidence_by_artifact = {
            packet.artifact_id: [asdict(item) for item in packet.evidence_items]
            for packet in packets
        }
        for code in draft:
            code.metadata["supporting_evidence"] = {
                artifact_id: evidence_by_artifact[artifact_id]
                for artifact_id in code.representative_artifact_ids
            }
        return draft, changes, drafts, analytic_memos

    def _validate_bootstrap(
        self,
        *,
        run_state: RunState,
        artifacts: list[ArtifactRecord],
        packets: list[ContextPacket],
        initial_codings: list[InitialCodingCase],
        codes: list[CodeState],
        assignments: list[BootstrapAssignment],
        checkpoint_store: BootstrapCheckpointStore | None = None,
        checkpoint_prefix: str = "validation",
        progress_callback: Callable[[int], None] | None = None,
        cancel_requested: CancelCallback | None = None,
    ) -> list[ValidationOutput]:
        """Apply the ordinary Validation Agent to every bootstrap assignment."""

        if self._validation_agent is None:
            return []
        artifact_by_id = {artifact.artifact_id: artifact for artifact in artifacts}
        packet_by_id = {packet.artifact_id: packet for packet in packets}
        coding_by_id = {case.artifact_id: case for case in initial_codings}
        code_by_id = {code.code_id: code for code in codes}
        bootstrap_codebook = CodebookState(
            dataset_name=run_state.dataset_metadata.dataset_name,
            version=1,
            codes=codes,
            notes=["Provisional bootstrap draft under validation."],
        )
        outputs: list[ValidationOutput] = []
        for index, assignment in enumerate(assignments, 1):
            self._check_cancelled(cancel_requested)
            stage = f"{checkpoint_prefix}/{assignment.artifact_id}"
            cached = (
                checkpoint_store.get(stage, ValidationOutput)
                if checkpoint_store is not None
                else None
            )
            if cached is not None:
                outputs.append(cached)
                if progress_callback is not None:
                    progress_callback(index)
                continue
            packet = packet_by_id[assignment.artifact_id]
            if assignment.status.startswith("unresolved_R"):
                criterion = assignment.status.rsplit("_", 1)[-1]
                output = ValidationOutput(
                    artifact_id=assignment.artifact_id,
                    human_review_required=True, review_criteria=[criterion],
                    summary="; ".join(assignment.evidence_summary),
                    review_questions=["Can the missing evidence or unusable initial proposal be resolved?"],
                )
                outputs.append(output)
                if checkpoint_store is not None:
                    checkpoint_store.put(stage, output)
                if progress_callback is not None:
                    progress_callback(index)
                continue
            recommended_codes = [
                ProvisionalCode(
                    code_name=code_by_id[code_id].name,
                    code_name_zh=str(code_by_id[code_id].metadata.get("name_zh", "")),
                    short_definition=code_by_id[code_id].definition,
                    inclusion_criteria=list(code_by_id[code_id].inclusion_criteria),
                    exclusion_criteria=list(code_by_id[code_id].exclusion_criteria),
                    short_definition_zh=str(
                        code_by_id[code_id].metadata.get("definition_zh", "")
                    ),
                    observed_phenomenon="; ".join(assignment.evidence_summary),
                    observed_phenomenon_zh="; ".join(assignment.evidence_summary),
                    supporting_evidence=list(packet.evidence_items),
                    relationship_to_codebook="reuse_existing_code",
                    linked_code_ids=[code_id],
                    proposed_codebook_action="no_change",
                )
                for code_id in assignment.code_ids
            ]
            comparison = ComparisonOutput(
                artifact_id=assignment.artifact_id,
                agreement_summary="Bootstrap assignment against the induced draft.",
                disagreement_summary="",
                recommended_codes=recommended_codes,
            )
            output = self._validation_agent(
                ValidationInput(
                    artifact=artifact_by_id[assignment.artifact_id],
                    research_question=run_state.research_question,
                    context_packet=packet,
                    coder_outputs=coding_by_id[assignment.artifact_id].coder_outputs,
                    arbitration_output=comparison,
                    codebook=bootstrap_codebook,
                    history=HistoryState(),
                    analysis_protocol=run_state.analysis_protocol,
                    validation_scope="initial_codebook",
                    corpus_audit={"grouping_memos": list(getattr(self, "_grouping_memos", []))},
                )
            )
            outputs.append(output)
            if checkpoint_store is not None:
                checkpoint_store.put(stage, output)
            if progress_callback is not None:
                progress_callback(index)
        return outputs

    @staticmethod
    def _validation_warnings(outputs: list[ValidationOutput]) -> list[str]:
        return list(
            dict.fromkeys(
                signal.summary
                for output in outputs
                for signal in output.signals
                if signal.signal != "valid" and signal.summary
            )
        )

    @staticmethod
    def _validation_warnings_zh(outputs: list[ValidationOutput]) -> list[str]:
        return list(
            dict.fromkeys(
                signal.summary_zh or signal.summary
                for output in outputs
                for signal in output.signals
                if signal.signal != "valid" and (signal.summary_zh or signal.summary)
            )
        )

    @staticmethod
    def _validation_feedback(
        outputs: list[ValidationOutput],
        *,
        scopes: set[ValidationIssueScope],
    ) -> list[dict[str, Any]]:
        corrective_signals = {
            "evidence_insufficient",
            "unsupported_inference",
            "use_case_mismatch",
            "category_overlap",
            "boundary_unclear",
        }
        return [
            {
                "artifact_id": output.artifact_id,
                "signal": signal.signal,
                "issue_scope": EvidenceFirstBootstrap._effective_validation_scope(signal),
                "summary": signal.summary,
                "related_code_names": signal.related_code_names,
            }
            for output in outputs
            for signal in output.signals
            if signal.signal in corrective_signals
            and EvidenceFirstBootstrap._effective_validation_scope(signal) in scopes
        ]

    @staticmethod
    def _effective_validation_scope(signal: Any) -> ValidationIssueScope:
        """Infer scope for checkpoints created before ValidationSignal.issue_scope."""

        if signal.issue_scope != "none" or signal.signal == "valid":
            return signal.issue_scope
        return {
            "evidence_insufficient": "evidence",
            "unsupported_inference": "evidence",
            "use_case_mismatch": "codebook",
            "category_overlap": "assignment",
            "boundary_unclear": "assignment",
            "context_missing": "context",
            "human_review_required": "assignment",
        }.get(signal.signal, "none")

    def _audit_codes(
        self,
        codes: list[CodeState],
        packets: list[ContextPacket],
    ) -> tuple[list[str], list[str]]:
        payload = self._invoke_json(
            system=(
                "Audit this provisional open-coding codebook. Do not change it and do not invent "
                "taxonomy structure. Identify only evidence gaps, duplicate boundaries, overly broad "
                "definitions, or evidence cards left without a plausible code."
            ),
            user=json.dumps(
                {
                    "codes": [self._code_to_prompt(code) for code in codes],
                    "evidence_cards": [self._context_to_dict(packet) for packet in packets],
                "required_json": {
                    "warnings": ["specific warning"],
                    "warnings_zh": ["同一警告的中文翻译"],
                },
                },
                ensure_ascii=False,
            ),
        )
        warnings = payload.get("warnings", [])
        if not isinstance(warnings, list):
            raise ValueError("Bootstrap auditor warnings must be a list.")
        warnings_zh = payload.get("warnings_zh", warnings)
        if not isinstance(warnings_zh, list):
            raise ValueError("Bootstrap auditor Chinese warnings must be a list.")
        return (
            [str(warning).strip() for warning in warnings if str(warning).strip()],
            [str(warning).strip() for warning in warnings_zh if str(warning).strip()],
        )

    def _label_artifacts(
        self,
        codes: list[CodeState],
        packets: list[ContextPacket],
        checkpoint_store: BootstrapCheckpointStore | None = None,
        checkpoint_prefix: str = "assignment",
        progress_callback: Callable[[int], None] | None = None,
        cancel_requested: CancelCallback | None = None,
        validation_feedback: list[dict[str, Any]] | None = None,
        analysis_protocol: dict[str, Any] | None = None,
        research_question: str = "",
    ) -> list[BootstrapAssignment]:
        valid_artifacts = {packet.artifact_id for packet in packets}
        valid_codes = {code.code_id for code in codes}
        assignments: list[BootstrapAssignment] = []
        processed = 0
        # One large output can exceed the model's JSON token budget. Label in
        # the same fixed mini-batches used by generation while retaining the
        # complete provisional B1 codebook as the assignment vocabulary.
        for index in range(0, len(packets), self.config.batch_size):
            self._check_cancelled(cancel_requested)
            batch = packets[index : index + self.config.batch_size]
            batch_index = index // self.config.batch_size
            stage = f"{checkpoint_prefix}/batch-{batch_index:04d}"
            cached = (
                checkpoint_store.get(stage, list[BootstrapAssignment])
                if checkpoint_store is not None
                else None
            )
            if cached is None:
                try:
                    payload = self._invoke_json(
                        system=read_prompt_file("induction_assignment_system_prompt.txt"),
                    user=json.dumps(
                        {
                            "research_question": research_question,
                            "analysis_protocol": analysis_protocol or {},
                            "codes": [self._code_to_prompt(code) for code in codes],
                            "evidence_cards": [self._context_to_dict(packet) for packet in batch],
                            "original_materials": {packet.artifact_id: getattr(self, "_assignment_materials", {}).get(
                                packet.artifact_id, {"status": "unavailable"}) for packet in batch},
                            "validation_feedback": [
                                item
                                for item in (validation_feedback or [])
                                if item.get("artifact_id")
                                in {packet.artifact_id for packet in batch}
                            ],
                            "required_json": {
                                "assignments": [
                                    {"artifact_id": "id", "code_ids": ["code-id"],
                                     "evidence_summary": ["grounded reason"],
                                     "status": "bootstrap_provisional"}
                                ]
                            },
                        },
                        ensure_ascii=False,
                    ),
                )
                except (AgentExecutionError, ValueError, TypeError, KeyError) as error:
                    cached = [BootstrapAssignment(
                        packet.artifact_id, [],
                        [f"Unusable initialization assignment after format repair: {error}"],
                        status="unresolved_R6",
                    ) for packet in batch]
                    if checkpoint_store is not None:
                        checkpoint_store.put(stage, cached)
                    assignments.extend(cached)
                    processed += len(batch)
                    if progress_callback is not None:
                        progress_callback(processed)
                    continue
                valid_artifacts_in_batch = {packet.artifact_id for packet in batch}
                rows = payload.get("assignments", [])
                if not isinstance(rows, list):
                    raise ValueError("Bootstrap labeler assignments must be a list.")
                cached = []
                for row in rows:
                    if not isinstance(row, dict):
                        raise ValueError("Bootstrap assignment must be an object.")
                    artifact_id = str(row.get("artifact_id", "")).strip()
                    code_ids = [str(code_id).strip() for code_id in row.get("code_ids", [])]
                    evidence = [str(item).strip() for item in row.get("evidence_summary", [])]
                    status = str(row.get("status", "bootstrap_provisional"))
                    if artifact_id not in valid_artifacts_in_batch or not evidence or (
                        not code_ids and status not in {"unresolved_R2", "unresolved_R3"}
                    ):
                        raise ValueError("Bootstrap assignment is incomplete.")
                    if any(code_id not in valid_codes for code_id in code_ids):
                        raise ValueError("Bootstrap assignment references an unknown code.")
                    cached.append(
                        BootstrapAssignment(
                            artifact_id,
                            self._leaf_most_code_ids(code_ids, codes),
                            evidence,
                            status=status,
                        )
                    )
                if checkpoint_store is not None:
                    checkpoint_store.put(stage, cached)
            assignments.extend(
                BootstrapAssignment(
                    assignment.artifact_id,
                    self._leaf_most_code_ids(assignment.code_ids, codes),
                    assignment.evidence_summary,
                    assignment.status,
                )
                for assignment in cached
            )
            processed += len(batch)
            if progress_callback is not None:
                progress_callback(processed)
        if {assignment.artifact_id for assignment in assignments} != valid_artifacts:
            raise ValueError("Bootstrap labeler must assign every bootstrap artifact.")
        return assignments

    @staticmethod
    def _leaf_most_code_ids(
        code_ids: list[str],
        codes: list[CodeState],
    ) -> list[str]:
        """Drop an assigned ancestor whenever one of its descendants is selected."""

        parent_by_id = {code.code_id: code.parent_code_id for code in codes}
        selected = set(code_ids)

        def has_selected_descendant(code_id: str) -> bool:
            for candidate in selected - {code_id}:
                visited: set[str] = set()
                parent = parent_by_id.get(candidate)
                while parent is not None and parent not in visited:
                    if parent == code_id:
                        return True
                    visited.add(parent)
                    parent = parent_by_id.get(parent)
            return False

        return list(
            dict.fromkeys(
                code_id for code_id in code_ids if not has_selected_descendant(code_id)
            )
        )

    @staticmethod
    def _check_cancelled(cancel_requested: CancelCallback | None) -> None:
        if cancel_requested is not None and cancel_requested():
            raise BootstrapCancelledError("Bootstrap initialization was cancelled.")

    def _configure_backend_cancellation(
        self,
        cancel_requested: CancelCallback | None,
    ) -> None:
        """Apply cancellation to every backend used by bootstrap Agents."""

        agents: list[Any] = [
            self._context_agent,
            *(coder for _coder_id, coder in self._initial_coder_agents),
            self._induction_agent,
            self._validation_agent,
        ]
        backends: list[Any] = [self._backend]
        for agent in agents:
            if agent is None:
                continue
            owner = getattr(agent, "__self__", None)
            if owner is not None and hasattr(owner, "_context_agent"):
                agent = getattr(owner, "_context_agent")
            backend = getattr(agent, "_backend", None)
            if backend is not None:
                backends.append(backend)
        seen: set[int] = set()
        for backend in backends:
            if id(backend) in seen:
                continue
            seen.add(id(backend))
            setter = getattr(backend, "set_cancel_requested", None)
            if setter is not None:
                setter(cancel_requested)

    @staticmethod
    def _progress(
        *,
        status: str,
        phase: str,
        processed_artifacts: int,
        total_artifacts: int,
        overall_completed: int,
        overall_total: int,
        current_artifact_id: str | None = None,
    ) -> dict[str, Any]:
        stage_numbers = {
            "evidence": 1,
            "initial_coding": 2,
            "induction": 3,
            "assignment": 4,
            "validation": 5,
            "reinduction": 6,
            "reassignment": 7,
            "revalidation": 8,
            "completed": 8,
        }
        percent = (
            round(100 * overall_completed / overall_total)
            if overall_total > 0
            else (100 if status in {"completed", "skipped", "disabled"} else 0)
        )
        return {
            "status": status,
            "phase": phase,
            "processed_artifacts": processed_artifacts,
            "total_artifacts": total_artifacts,
            "overall_completed": overall_completed,
            "overall_total": overall_total,
            # Retain weighted counters for compatibility, but expose the
            # human-readable stage position separately. These counters are
            # stage tasks, not completed artifacts.
            "stage_index": stage_numbers.get(phase, 0),
            "stage_total": 8,
            "percent": max(0, min(100, percent)),
            "current_artifact_id": current_artifact_id,
        }

    @staticmethod
    def _notify(
        callback: ProgressCallback | None,
        progress: dict[str, Any],
    ) -> None:
        if callback is not None:
            callback(dict(progress))

    def set_execution_trace_sink(self, sink) -> None:
        self.trace_sink = sink
        for agent in [self._induction_agent, self._validation_agent,
                      self._context_agent, *(item for _, item in self._initial_coder_agents)]:
            if hasattr(agent, "trace_sink"):
                agent.trace_sink = sink

    def _invoke_json(self, *, system: str, user: str) -> dict[str, Any]:
        language_instruction = (
            "\n\n请使用中文回答中文 *_zh 字段，同时生成语义一致的英文 canonical 字段。"
            if self._output_language == "zh"
            else "\n\nAnswer in English in canonical fields and provide semantically equivalent Chinese *_zh fields."
        )
        contract_instruction = (
            " JSON 字段名必须严格保持，证据摘录、artifact id、code id 和原始代码保持原文；"
            "只返回一个 JSON object，不要 markdown。"
        )
        agent = BaseLLMAgent(
            prompt_spec=AgentPromptSpec(
                name="induction_assignment_or_audit",
                system_prompt=system + language_instruction + contract_instruction,
                user_prompt_template="{request}",
            ), model_config=self._model_config, backend=self._backend,
        )
        # Preserve machine-readable JSON user bodies for this task.
        agent.build_messages = lambda *, user_prompt: [
            LLMMessage(role="system", content=agent._prompt_spec.system_prompt),
            LLMMessage(role="user", content=user_prompt),
        ]
        agent.trace_sink = getattr(self, "trace_sink", None)
        def parse(payload, response):
            if "assignments" in json.loads(user).get("required_json", {}):
                request = json.loads(user)
                expected = {row["artifact_id"] for row in request["evidence_cards"]}
                rows = payload.get("assignments")
                if not isinstance(rows, list):
                    raise ValueError("Assignments must be a list.")
                ids = [row.get("artifact_id") for row in rows if isinstance(row, dict)]
                if len(ids) != len(rows) or len(ids) != len(set(ids)) or set(ids) != expected:
                    raise ValueError("Each requested case requires exactly one assignment, with no foreign cases.")
                valid_codes = {row["code_id"] for row in request["codes"]}
                for row in rows:
                    if not isinstance(row.get("code_ids"), list) or (
                        not row["code_ids"] and row.get("status") not in {"unresolved_R2", "unresolved_R3"}
                    ) or not isinstance(row.get("evidence_summary"), list) or not row["evidence_summary"]:
                        raise ValueError("Assignment is incomplete.")
                    if set(row["code_ids"]) - valid_codes:
                        raise ValueError("Assignment references an unknown code.")
            return payload
        try:
            payload = agent.invoke_validated_json_object(parse, request=user)
        finally:
            for trace in agent.execution_log:
                self._supporting_model_calls.append({**trace, **trace.get("config", {}), "call_kind": "bootstrap_supporting_call"})
        return payload

    @staticmethod
    def _code_to_prompt(code: CodeState) -> dict[str, Any]:
        return {
            "code_id": code.code_id,
            "name": code.name,
            "definition": code.definition,
            "inclusion_criteria": code.inclusion_criteria,
            "exclusion_criteria": code.exclusion_criteria,
            "inclusion_criteria_zh": code.metadata.get("inclusion_criteria_zh", []),
            "exclusion_criteria_zh": code.metadata.get("exclusion_criteria_zh", []),
            "representative_artifact_ids": code.representative_artifact_ids,
        }

    @staticmethod
    def _context_to_dict(packet: ContextPacket) -> dict[str, Any]:
        return {
            "artifact_id": packet.artifact_id,
            "context_brief": packet.context_brief,
            "evidence_items": [
                asdict(item) for item in packet.evidence_items
            ],
            "missing_context_warnings": packet.missing_context_warnings,
        }
