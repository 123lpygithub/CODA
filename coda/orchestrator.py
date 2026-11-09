from __future__ import annotations

import json
import hashlib
import math
from copy import deepcopy
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict, dataclass, field, replace
from datetime import datetime, timezone
from typing import Any, Callable
from uuid import uuid4

from adapters.base import ArtifactRecord
from coda.agents.common import build_evidence_item, ground_context_packet
from coda.calibration import calculate_risk_score
from coda.contracts import (
    ArbitrationInput,
    ArbitrationOutput,
    CoderAgentInput,
    CoderAgentOutput,
    ContextAgentInput,
    ContextPacket,
    ComparisonInput,
    ComparisonOutput,
    CodebookChangePacket,
    EvidencePacket,
    HumanReviewInput,
    HumanReviewOutput,
    ProvisionalCode,
    ReviewRoutingDecision,
    ValidationInput,
    ValidationSignal,
    ValidationOutput,
)
from coda.state import (
    ArtifactBatchState,
    CodeState,
    CodebookChangeState,
    ContextRequestState,
    RetrospectiveRecodingTask,
    RunState,
    UnresolvedCaseState,
)
from coda.semantic_retrieval import rank_semantic_impacts
from coda.stage_checkpoints import StageCheckpointStore

ContextAgent = Callable[[ContextAgentInput], ContextPacket]
CoderAgent = Callable[[CoderAgentInput], CoderAgentOutput]
ComparisonAgent = Callable[[ComparisonInput], ComparisonOutput]
ArbitrationAgent = ComparisonAgent
ValidationAgent = Callable[[ValidationInput], ValidationOutput]
HumanReviewAgent = Callable[[HumanReviewInput], HumanReviewOutput]


@dataclass(frozen=True)
class ArtifactRunResult:
    """Complete no-model pipeline output for one artifact."""

    artifact_id: str
    context_packet: ContextPacket
    coder_outputs: list[CoderAgentOutput]
    arbitration_output: ArbitrationOutput
    validation_output: ValidationOutput
    evidence_packet: EvidencePacket
    human_review_output: HumanReviewOutput


@dataclass(frozen=True)
class PreparedArtifactReview:
    """Agent-side result for one artifact, waiting for a human decision.

    Web clients share this boundary: agents prepare an evidence packet,
    then a human supplies ``HumanReviewOutput`` in a separate operation.
    """

    artifact: ArtifactRecord
    batch: ArtifactBatchState
    context_packet: ContextPacket
    coder_outputs: list[CoderAgentOutput]
    arbitration_output: ArbitrationOutput
    validation_output: ValidationOutput
    evidence_packet: EvidencePacket
    codebook_version: int
    review_origin: str = "current"
    retrospective_task_id: str | None = None

    @property
    def artifact_id(self) -> str:
        return self.artifact.artifact_id


@dataclass(frozen=True)
class BatchRunResult:
    """Pipeline outputs for one coding batch."""

    batch_id: str
    batch_index: int
    artifact_results: list[ArtifactRunResult] = field(default_factory=list)


class CODAOrchestrator:
    """Wire CODA components together without embedding any model logic."""

    def __init__(
        self,
        *,
        context_agent: ContextAgent,
        coder_agents: list[tuple[str, CoderAgent]],
        validation_agent: ValidationAgent,
        human_review_agent: HumanReviewAgent,
        comparison_agent: ComparisonAgent | None = None,
        arbitration_agent: ArbitrationAgent | None = None,
        failure_policy: str = "raise",
    ) -> None:
        if len(coder_agents) < 2:
            msg = "CODAOrchestrator requires at least two independent coder agents."
            raise ValueError(msg)
        self._context_agent = context_agent
        self._coder_agents = list(coder_agents)
        if comparison_agent is not None and arbitration_agent is not None:
            raise ValueError(
                "Provide comparison_agent or the legacy arbitration_agent, not both."
            )
        selected_comparison_agent = comparison_agent or arbitration_agent
        if selected_comparison_agent is None:
            raise ValueError("CODAOrchestrator requires a comparison agent.")
        self._comparison_agent = selected_comparison_agent
        self._validation_agent = validation_agent
        self._human_review_agent = human_review_agent
        if failure_policy not in {"raise", "route_to_r6"}:
            raise ValueError(
                "failure_policy must be either 'raise' or 'route_to_r6'."
            )
        self._failure_policy = failure_policy
        self._output_language = "en"

    def _historical_materials(self, run_state: RunState) -> dict[str, Any]:
        loader = getattr(self, "artifact_loader", None)
        cache = run_state.metadata.get("case_materials", {})
        materials = {}
        # Loading is cached per immutable run. Selection of the relevant subset
        # remains with Comparison/Validation, keeping the coder inputs blind.
        for record in run_state.history.coding_records:
            if record.artifact_id in materials:
                continue
            material = cache.get(record.artifact_id)
            if material is not None and "content" in material:
                materials[record.artifact_id] = material
            elif loader is not None:
                artifact = loader(record.artifact_id)
                if artifact is not None:
                    materials[record.artifact_id] = {
                        "status": "available", "content": artifact.content,
                        "raw_fields": artifact.raw_fields,
                        "source_refs": [asdict(ref) for ref in artifact.source_refs],
                    }
        return materials

    def set_execution_trace_sink(self, sink: Callable[[dict[str, Any]], None]) -> None:
        self.trace_sink = sink
        for agent in [self._context_agent, *(agent for _, agent in self._coder_agents),
                      self._comparison_agent, self._validation_agent]:
            if hasattr(agent, "trace_sink"):
                agent.trace_sink = sink

    def set_output_language(self, language: str) -> None:
        """Set the response language for every LLM stage in this pipeline."""

        self._output_language = language
        agents = [
            self._context_agent,
            *(coder for _, coder in self._coder_agents),
            self._comparison_agent,
            self._validation_agent,
        ]
        for agent in agents:
            setter = getattr(agent, "set_output_language", None)
            if setter is not None:
                setter(language)

    def stage_cache_key(
        self,
        run_state: RunState,
        artifact: ArtifactRecord,
        *,
        review_origin: str = "current",
        retrospective_task_id: str | None = None,
    ) -> str:
        """Fingerprint every input that can change a stage output."""

        def agent_fingerprint(name: str, agent: Any) -> dict[str, Any]:
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

        payload = {
            "artifact_id": artifact.artifact_id,
            "artifact_sha256": hashlib.sha256(
                artifact.content.encode("utf-8")
            ).hexdigest(),
            "codebook_version": run_state.codebook.version,
            "language": self._output_language,
            "research_question": asdict(run_state.research_question),
            "analysis_protocol": asdict(run_state.analysis_protocol),
            # Resolved context is an actual model input.  Include it in the
            # checkpoint fingerprint so a later context resolution cannot
            # accidentally reuse an earlier Context/Coder/Comparison result.
            "additional_context": self._additional_context_for_artifact(
                run_state,
                artifact.artifact_id,
            ),
            "review_origin": review_origin,
            "retrospective_task_id": retrospective_task_id,
            "case_review_history": [asdict(row) for row in run_state.history.coding_records
                                    if row.artifact_id == artifact.artifact_id],
            "agents": [
                agent_fingerprint("context", self._context_agent),
                *(
                    agent_fingerprint(coder_id, coder)
                    for coder_id, coder in self._coder_agents
                ),
                agent_fingerprint("comparison", self._comparison_agent),
                agent_fingerprint("validation", self._validation_agent),
            ],
        }
        return hashlib.sha256(
            json.dumps(payload, ensure_ascii=False, sort_keys=True, default=str).encode(
                "utf-8"
            )
        ).hexdigest()

    def prepare_bootstrap_context(
        self,
        run_state: RunState,
        artifact: ArtifactRecord,
    ) -> ContextPacket:
        """Expose only the evidence-card stage for the separate bootstrap flow."""

        return self._context_agent(
            ContextAgentInput(
                artifact=artifact,
                research_question=run_state.research_question,
                analysis_protocol=run_state.analysis_protocol,
                additional_context=self._additional_context_for_artifact(
                    run_state,
                    artifact.artifact_id,
                ),
            )
        )

    def prepare_context(self, agent_input: ContextAgentInput) -> ContextPacket:
        """Run the context stage from an already assembled agent input.

        Bootstrap prepares evidence cards before the regular per-artifact loop,
        so it needs the same context callable with the normal agent signature.
        Keeping this adapter public avoids coupling bootstrap to a private
        orchestrator field or accidentally binding the two-argument helper.
        """

        return self._context_agent(agent_input)

    def run_current_batch(self, run_state: RunState) -> BatchRunResult:
        """Execute the fixed CODA pipeline for the current coding batch."""

        batch = run_state.current_batch()
        if batch is None:
            msg = "RunState has no remaining coding batch."
            raise IndexError(msg)

        run_state.status = "in_progress"
        artifact_results = [self._run_one_artifact(run_state, batch, artifact) for artifact in batch.artifacts]
        run_state.advance_to_next_batch()
        if run_state.has_remaining_coding_batches():
            run_state.status = "in_progress"
        else:
            run_state.status = "completed"
        return BatchRunResult(
            batch_id=batch.batch_id,
            batch_index=batch.batch_index,
            artifact_results=artifact_results,
        )

    def run_all_batches(self, run_state: RunState) -> list[BatchRunResult]:
        """Run the no-model skeleton until every coding batch is processed."""

        results: list[BatchRunResult] = []
        while run_state.has_remaining_coding_batches():
            results.append(self.run_current_batch(run_state))
        return results

    def run_one_artifact(
        self,
        run_state: RunState,
        *,
        artifact: ArtifactRecord,
        batch: ArtifactBatchState | None = None,
        stage_checkpoint_store: StageCheckpointStore | None = None,
    ) -> ArtifactRunResult:
        """Execute the full CODA pipeline for one artifact without advancing batches."""

        active_batch = batch or run_state.current_batch()
        if active_batch is None:
            msg = "RunState has no current batch."
            raise IndexError(msg)
        if not active_batch.contains(artifact.artifact_id):
            msg = (
                f"Artifact {artifact.artifact_id} does not belong to batch "
                f"{active_batch.batch_id}."
            )
            raise ValueError(msg)
        prepared_review = self.prepare_one_artifact(
            run_state,
            artifact=artifact,
            batch=active_batch,
            stage_checkpoint_store=stage_checkpoint_store,
        )
        human_review_output = self._human_review_agent(
            self.human_review_input(run_state, prepared_review)
        )
        result = self.submit_prepared_review(
            run_state,
            prepared_review=prepared_review,
            human_review_output=human_review_output,
        )
        if stage_checkpoint_store is not None:
            stage_checkpoint_store.clear()
        return result

    def prepare_one_artifact(
        self,
        run_state: RunState,
        *,
        artifact: ArtifactRecord,
        batch: ArtifactBatchState | None = None,
        allow_reviewed: bool = False,
        review_origin: str = "current",
        retrospective_task_id: str | None = None,
        stage_checkpoint_store: StageCheckpointStore | None = None,
        stage_callback: Callable[[str], None] | None = None,
        defer_validation: bool = False,
        comparison_task: str | None = None,
        prior_comparison: dict[str, Any] | None = None,
    ) -> PreparedArtifactReview:
        """Run model stages through validation, stopping before human review."""

        active_batch = batch or run_state.current_batch()
        if active_batch is None:
            msg = "RunState has no current batch."
            raise IndexError(msg)
        if not active_batch.contains(artifact.artifact_id):
            msg = (
                f"Artifact {artifact.artifact_id} does not belong to batch "
                f"{active_batch.batch_id}."
            )
            raise ValueError(msg)
        if not allow_reviewed and artifact.artifact_id in set(run_state.history.reviewed_artifact_ids()):
            msg = f"Artifact {artifact.artifact_id} has already been human-reviewed."
            raise ValueError(msg)

        run_state.status = "in_progress"
        context_packet = (
            stage_checkpoint_store.get("context", ContextPacket)
            if stage_checkpoint_store is not None
            else None
        )
        if context_packet is None:
            try:
                context_packet = self._context_agent(
                    ContextAgentInput(
                        artifact=artifact,
                        research_question=run_state.research_question,
                        analysis_protocol=run_state.analysis_protocol,
                        additional_context=self._additional_context_for_artifact(
                            run_state,
                            artifact.artifact_id,
                        ),
                    )
                )
            except Exception as error:
                if self._failure_policy == "raise":
                    raise
                context_packet = self._failed_context_packet(artifact, error)
            context_packet = ground_context_packet(artifact, context_packet)
            if stage_checkpoint_store is not None:
                stage_checkpoint_store.put("context", context_packet)
            if stage_callback is not None:
                stage_callback("context")
        coder_outputs = (
            stage_checkpoint_store.get("coders", list[CoderAgentOutput])
            if stage_checkpoint_store is not None
            else None
        )
        if coder_outputs is None:
            if stage_checkpoint_store is not None:
                # Proxy-backed providers may be unstable under concurrent long
                # requests. Persist each independent coder as soon as it
                # succeeds so a retry resumes only the missing model call.
                coder_outputs = []
                for coder_id, coder in self._coder_agents:
                    coder_stage = f"coder/{coder_id}"
                    output = stage_checkpoint_store.get(
                        coder_stage,
                        CoderAgentOutput,
                    )
                    if output is None:
                        try:
                            output = coder(
                                CoderAgentInput(
                                    artifact=artifact,
                                    research_question=run_state.research_question,
                                    context_packet=context_packet,
                                    coder_id=coder_id,
                                    analysis_protocol=run_state.analysis_protocol,
                                )
                            )
                        except Exception as error:
                            if self._failure_policy == "raise":
                                raise
                            output = self._failed_coder_output(artifact, coder_id, error)
                        stage_checkpoint_store.put(coder_stage, output)
                    coder_outputs.append(output)
            else:
                with ThreadPoolExecutor(max_workers=2, thread_name_prefix="coda-coder") as executor:
                    futures = [
                        executor.submit(
                            coder,
                            CoderAgentInput(
                                artifact=artifact,
                                research_question=run_state.research_question,
                                context_packet=context_packet,
                                coder_id=coder_id,
                                analysis_protocol=run_state.analysis_protocol,
                            ),
                        )
                        for coder_id, coder in self._coder_agents
                    ]
                    coder_outputs = []
                    for (coder_id, _), future in zip(self._coder_agents, futures):
                        try:
                            coder_outputs.append(future.result())
                        except Exception as error:
                            if self._failure_policy == "raise":
                                raise
                            coder_outputs.append(self._failed_coder_output(artifact, coder_id, error))
            if stage_checkpoint_store is not None:
                stage_checkpoint_store.put("coders", coder_outputs)
            if stage_callback is not None:
                stage_callback("coders")
        arbitration_output = (
            stage_checkpoint_store.get("comparison", ComparisonOutput)
            if stage_checkpoint_store is not None
            else None
        )
        if arbitration_output is None:
            try:
                arbitration_output = self._comparison_agent(
                    ComparisonInput(
                        artifact=artifact,
                        research_question=run_state.research_question,
                        context_packet=context_packet,
                        coder_outputs=coder_outputs,
                        codebook=run_state.codebook,
                        history=run_state.history,
                        analysis_protocol=run_state.analysis_protocol,
                        historical_materials=self._historical_materials(run_state),
                        task=comparison_task or ("retrospective_reassessment" if review_origin == "retrospective" else "case_comparison"),
                        prior_comparison=prior_comparison or {},
                        defer_refinement=defer_validation,
                    )
                )
            except Exception as error:
                if self._failure_policy == "raise":
                    raise
                arbitration_output = self._failed_comparison_output(artifact, error)
            if stage_checkpoint_store is not None:
                stage_checkpoint_store.put("comparison", arbitration_output)
            if stage_callback is not None:
                stage_callback("comparison")
        run_state.metadata.setdefault("case_materials", {})[artifact.artifact_id] = {
            "status": "available", "content": artifact.content,
            "raw_fields": artifact.raw_fields,
            "source_refs": [asdict(ref) for ref in artifact.source_refs],
            "context_packet": asdict(context_packet),
        }
        if defer_validation:
            # Batch preparation gathers independent case proposals against one
            # immutable snapshot. No validation/routing/sampling occurs before
            # Comparison has reconciled the whole batch.
            validation = ValidationOutput(artifact_id=artifact.artifact_id)
            return PreparedArtifactReview(
                artifact=artifact, batch=active_batch, context_packet=context_packet,
                coder_outputs=coder_outputs, arbitration_output=arbitration_output,
                validation_output=validation,
                evidence_packet=self._build_evidence_packet(
                    artifact=artifact, run_state=run_state, context_packet=context_packet,
                    coder_outputs=coder_outputs, arbitration_output=arbitration_output,
                    validation_output=validation),
                codebook_version=run_state.codebook.version,
            )
        validation_output = (
            stage_checkpoint_store.get("validation", ValidationOutput)
            if stage_checkpoint_store is not None
            else None
        )
        if validation_output is None:
            try:
                validation_output = self._validation_agent(
                    ValidationInput(
                        artifact=artifact,
                        research_question=run_state.research_question,
                        context_packet=context_packet,
                        coder_outputs=coder_outputs,
                        comparison_output=arbitration_output,
                        arbitration_output=arbitration_output,
                        codebook=run_state.codebook,
                        history=run_state.history,
                        analysis_protocol=run_state.analysis_protocol,
                        historical_materials=self._historical_materials(run_state),
                        validation_scope="iterative_decision",
                    )
                )
            except Exception as error:
                if self._failure_policy == "raise":
                    raise
                validation_output = self._failed_validation_output(artifact, error)
            if stage_checkpoint_store is not None:
                stage_checkpoint_store.put("validation", validation_output)
            if stage_callback is not None:
                stage_callback("validation")
        evidence_packet = self._build_evidence_packet(
            artifact=artifact,
            run_state=run_state,
            context_packet=context_packet,
            coder_outputs=coder_outputs,
            arbitration_output=arbitration_output,
            validation_output=validation_output,
        )
        routing_decision = self._route_review(
            run_state=run_state,
            artifact_id=artifact.artifact_id,
            batch=active_batch,
            context_packet=context_packet,
            coder_outputs=coder_outputs,
            arbitration_output=arbitration_output,
            validation_output=validation_output,
            sampling_stream=(
                "retrospective" if review_origin == "retrospective" else "current"
            ),
        )
        evidence_packet = replace(
            evidence_packet,
            routing_decision=routing_decision,
        )
        run_state.status = (
            "awaiting_human_review"
            if routing_decision.route == "human_review"
            else "in_progress"
        )
        return PreparedArtifactReview(
            artifact=artifact,
            batch=active_batch,
            context_packet=context_packet,
            coder_outputs=coder_outputs,
            arbitration_output=arbitration_output,
            validation_output=validation_output,
            evidence_packet=evidence_packet,
            codebook_version=run_state.codebook.version,
            review_origin=review_origin,
            retrospective_task_id=retrospective_task_id,
        )

    @staticmethod
    def _failure_metadata(agent: str, error: Exception) -> dict[str, Any]:
        return {
            "agent_failure": True,
            "failed_agent": agent,
            "error_type": type(error).__name__,
            "error_message": str(error)[:500],
        }

    @classmethod
    def _failed_context_packet(
        cls, artifact: ArtifactRecord, error: Exception
    ) -> ContextPacket:
        message = (
            f"The Context Agent could not produce a usable packet: "
            f"{type(error).__name__}: {str(error)[:500]}"
        )
        return ContextPacket(
            artifact_id=artifact.artifact_id,
            context_brief=message,
            context_brief_zh=(
                "上下文智能体未能生成可用的证据包："
                f"{type(error).__name__}: {str(error)[:500]}"
            ),
            source_refs=list(artifact.source_refs),
            missing_context_warnings=[message],
            missing_context_warnings_zh=[message],
            model_metadata=cls._failure_metadata("context_agent", error),
        )

    @classmethod
    def _failed_coder_output(
        cls, artifact: ArtifactRecord, coder_id: str, error: Exception
    ) -> CoderAgentOutput:
        message = (
            f"{coder_id} did not return a usable coding output: "
            f"{type(error).__name__}: {str(error)[:500]}"
        )
        return CoderAgentOutput(
            artifact_id=artifact.artifact_id,
            coder_id=coder_id,
            insufficient_context=True,
            overall_uncertainty=message,
            overall_uncertainty_zh=message,
            notes=[message],
            notes_zh=[message],
            model_metadata=cls._failure_metadata(coder_id, error),
        )

    @classmethod
    def _failed_comparison_output(
        cls, artifact: ArtifactRecord, error: Exception
    ) -> ComparisonOutput:
        message = (
            f"Comparison Agent did not return a usable output: "
            f"{type(error).__name__}: {str(error)[:500]}"
        )
        return ComparisonOutput(
            artifact_id=artifact.artifact_id,
            agreement_summary="",
            disagreement_summary=message,
            agreement_summary_zh="",
            disagreement_summary_zh=message,
            model_metadata=cls._failure_metadata("comparison_agent", error),
        )

    @classmethod
    def _failed_validation_output(
        cls, artifact: ArtifactRecord, error: Exception
    ) -> ValidationOutput:
        message = (
            f"Validation Agent did not return a usable output: "
            f"{type(error).__name__}: {str(error)[:500]}"
        )
        return ValidationOutput(
            artifact_id=artifact.artifact_id,
            signals=[
                ValidationSignal(
                    signal="human_review_required",
                    issue_scope="assignment",
                    summary=message,
                    summary_zh=message,
                )
            ],
            human_review_required=True,
            review_criteria=["R6"],
            review_questions=[
                "The agent output is unusable. Should the system retry with the same evidence, request context, or leave this case unresolved?"
            ],
            review_questions_zh=[
                "智能体输出不可用。应使用相同证据重试、请求补充上下文，还是将此案例保留为未解决？"
            ],
            summary=message,
            summary_zh=message,
            notes=[message],
            notes_zh=[message],
            model_metadata=cls._failure_metadata("validation_agent", error),
        )

    @staticmethod
    def _additional_context_for_artifact(
        run_state: RunState,
        artifact_id: str,
    ) -> list[str]:
        return [
            item
            for request in run_state.history.context_requests
            if request.scope == "artifact"
            and request.artifact_id == artifact_id
            and request.status == "resolved"
            for item in request.supplied_context
        ]

    def prepare_retrospective_artifact(
        self,
        run_state: RunState,
        *,
        artifact: ArtifactRecord,
        batch: ArtifactBatchState,
        task_id: str,
        stage_checkpoint_store: StageCheckpointStore | None = None,
    ) -> PreparedArtifactReview:
        """Re-run the agent pipeline against a historical artifact and new codebook."""

        ordinary_status = run_state.status
        try:
            return self.prepare_one_artifact(
                run_state,
                artifact=artifact,
                batch=batch,
                allow_reviewed=True,
                review_origin="retrospective",
                retrospective_task_id=task_id,
                stage_checkpoint_store=stage_checkpoint_store,
            )
        finally:
            run_state.status = ordinary_status

    def human_review_input(
        self,
        run_state: RunState,
        prepared_review: PreparedArtifactReview,
    ) -> HumanReviewInput:
        """Build the exact material a human reviewer should receive."""

        return HumanReviewInput(
            artifact=prepared_review.artifact,
            research_question=run_state.research_question,
            evidence_packet=prepared_review.evidence_packet,
            codebook=run_state.codebook,
            history=run_state.history,
            analysis_protocol=run_state.analysis_protocol,
        )

    def validate_final_record(
        self,
        run_state: RunState,
        artifact: ArtifactRecord,
        *,
        corpus_audit: dict[str, Any],
        validation_scope: str = "final_audit",
    ) -> ValidationOutput:
        """Audit a stored decision against final definitions without recoding it."""

        record = run_state.history.latest_record_for_artifact(artifact.artifact_id)
        if record is None and validation_scope != "initial_codebook":
            return self._failed_validation_output(
                artifact, ValueError("Final audit has no coding record for this case.")
            )
        source_evidence = [build_evidence_item(
            artifact,
            field_name="content",
            excerpt=artifact.content,
            rationale="Full original case for audit; this is not a confirmed supporting excerpt.",
        )] if artifact.content else []
        context = ContextPacket(
            artifact_id=artifact.artifact_id,
            context_brief="Audit the stored decision against the full original case and final codebook.",
            evidence_items=source_evidence,
            source_refs=list(artifact.source_refs),
        )
        assigned = []
        for code_id in (record.final_code_ids if record else [code.code_id for code in run_state.codebook.active_codes()]):
            code = run_state.codebook.get_code(code_id)
            if code is not None:
                assigned.append(ProvisionalCode(
                    code_name=code.name,
                    short_definition=code.definition,
                    inclusion_criteria=list(code.inclusion_criteria),
                    exclusion_criteria=list(code.exclusion_criteria),
                    supporting_evidence=source_evidence,
                    relationship_to_codebook="reuse_existing_code",
                    linked_code_ids=[code_id],
                ))
        try:
            return self._validation_agent(ValidationInput(
                artifact=artifact,
                research_question=run_state.research_question,
                context_packet=context,
                coder_outputs=[],
                codebook=run_state.codebook,
                history=run_state.history,
                comparison_output=ComparisonOutput(
                    artifact_id=artifact.artifact_id,
                    agreement_summary=record.rationale if record else "Validate initial candidate definitions against the source.",
                    disagreement_summary="Stored coding record, not a new comparison proposal.",
                    recommended_codes=assigned,
                ),
                analysis_protocol=run_state.analysis_protocol,
                validation_scope=validation_scope,
                corpus_audit={**corpus_audit, "recorded_assignment": asdict(record) if record else None},
                historical_materials=self._historical_materials(run_state),
            ))
        except Exception as error:
            if self._failure_policy == "raise":
                raise
            return self._failed_validation_output(artifact, error)

    def automatic_review_if_safe(
        self,
        run_state: RunState,
        prepared_review: PreparedArtifactReview,
    ) -> HumanReviewOutput | None:
        """Translate a transparent routing result into an automatic decision."""

        routing = prepared_review.evidence_packet.routing_decision
        if routing is None:
            raise RuntimeError("Prepared review is missing its authoritative routing decision.")
        if routing.route == "human_review":
            return None
        if routing.route == "unresolved":
            return HumanReviewOutput(
                artifact_id=prepared_review.artifact_id,
                decision="mark_uncertain",
                pre_read_memo="Automatic workflow preserved this case as unresolved.",
                rationale="; ".join(routing.reasons + routing.risk_signals),
                metadata={
                    "review_origin": "automatic_unresolved",
                    "human_reviewed": False,
                    "routing_decision": asdict(routing),
                },
            )

        blockers = self._automatic_acceptance_blockers(
            run_state=run_state,
            context_packet=prepared_review.context_packet,
            coder_outputs=prepared_review.coder_outputs,
            arbitration_output=prepared_review.arbitration_output,
            validation_output=prepared_review.validation_output,
        )
        if blockers:
            raise RuntimeError(
                "Routing selected automatic_accept despite blocker(s): "
                + ", ".join(blockers)
            )

        validation = prepared_review.validation_output
        arbitration = prepared_review.arbitration_output
        active_by_id = {
            code.code_id: code for code in run_state.codebook.active_codes()
        }
        active_by_name = {
            " ".join(code.name.split()).casefold(): code
            for code in active_by_id.values()
        }

        recommended_ids: set[str] = set()
        new_codes: list[CodeState] = []
        new_changes: list[CodebookChangeState] = []
        structural_results: dict[str, list[tuple[str, str]]] = {}
        for candidate in arbitration.recommended_codes:
            if candidate.relationship_to_codebook in {
                "refine_existing_code", "merge_existing_codes", "split_existing_code", "add_parent_code",
            }:
                targets = candidate.proposed_codebook_target_ids or candidate.linked_code_ids
                action = candidate.proposed_codebook_action
                if action == "refine" and len(targets) == 1:
                    code = replace(
                        active_by_id[targets[0]],
                        name=candidate.code_name, definition=candidate.short_definition,
                        metadata=dict(active_by_id[targets[0]].metadata),
                    )
                else:
                    digest = hashlib.sha256(
                        f"{prepared_review.artifact_id}:{action}:{candidate.code_name}".encode("utf-8")
                    ).hexdigest()[:10]
                    code = CodeState(
                        code_id=f"code-{digest}", name=candidate.code_name,
                        definition=candidate.short_definition,
                        representative_artifact_ids=[prepared_review.artifact_id],
                    )
                code.metadata.update({
                    "origin": "automatically_accepted",
                    "name_zh": candidate.code_name_zh,
                    "definition_zh": candidate.short_definition_zh,
                    "inclusion_criteria_zh": candidate.inclusion_criteria_zh,
                    "exclusion_criteria_zh": candidate.exclusion_criteria_zh,
                })
                code = replace(code, inclusion_criteria=candidate.inclusion_criteria,
                               exclusion_criteria=candidate.exclusion_criteria)
                new_codes.append(code)
                structural_results.setdefault(action, []).append((candidate.code_name, code.code_id))
                continue
            if candidate.relationship_to_codebook not in {
                "reuse_existing_code",
                "new_code",
            }:
                raise RuntimeError("Automatic assignment received a structural relationship.")
            if not candidate.supporting_evidence:
                raise RuntimeError("Automatic assignment received ungrounded evidence.")
            if candidate.relationship_to_codebook == "new_code":
                digest = hashlib.sha256(
                    f"{prepared_review.artifact_id}:{candidate.code_name}".encode("utf-8")
                ).hexdigest()[:10]
                code = CodeState(
                    code_id=f"code-{digest}",
                    name=candidate.code_name,
                    definition=candidate.short_definition,
                    inclusion_criteria=list(candidate.inclusion_criteria),
                    exclusion_criteria=list(candidate.exclusion_criteria),
                    representative_artifact_ids=[prepared_review.artifact_id],
                    notes=[candidate.alternative_interpretation]
                    if candidate.alternative_interpretation
                    else [],
                    metadata={
                        "origin": "automatically_accepted",
                        "observed_phenomenon": candidate.observed_phenomenon,
                        "observed_phenomenon_zh": candidate.observed_phenomenon_zh,
                        "name_zh": candidate.code_name_zh,
                        "definition_zh": candidate.short_definition_zh,
                        "inclusion_criteria_zh": candidate.inclusion_criteria_zh,
                        "exclusion_criteria_zh": candidate.exclusion_criteria_zh,
                    },
                )
                new_codes.append(code)
                new_changes.append(
                    CodebookChangeState(
                        change_id=f"auto-change-{digest}",
                        action="add",
                        round_index=len(run_state.history.coding_records),
                        summary=f"Add evidence-supported code: {candidate.code_name}",
                        rationale=candidate.short_definition,
                        resulting_code_ids=[code.code_id],
                        artifact_ids=[prepared_review.artifact_id],
                        decided_by="automatic",
                        metadata={"routing": "automatic_accept"},
                    )
                )
                recommended_ids.add(code.code_id)
                continue
            linked = set(candidate.linked_code_ids)
            if linked:
                if not linked <= set(active_by_id):
                    raise RuntimeError("Automatic assignment references an unknown code id.")
                recommended_ids.update(linked)
            else:
                code = active_by_name.get(
                    " ".join(candidate.code_name.split()).casefold()
                )
                if code is None:
                    raise RuntimeError("Automatic assignment could not map an existing code.")
                recommended_ids.add(code.code_id)
        existing_recommended_ids = recommended_ids.intersection(active_by_id)

        final_codes = [
            active_by_id[code_id] for code_id in sorted(existing_recommended_ids)
        ] + new_codes
        for proposal in arbitration.possible_codebook_changes:
            results = structural_results.get(proposal.action, [])
            if not results:
                continue
            proposed_names = proposal.metadata.get("resulting_code_names", [])
            names = {" ".join(str(name).split()).casefold() for name in proposed_names}
            result_ids = [
                code_id for name, code_id in results
                if " ".join(name.split()).casefold() in names
            ]
            if not result_ids:
                raise RuntimeError("Automatic structural change has no matching resulting definition.")
            new_changes.append(replace(
                proposal,
                resulting_code_ids=result_ids,
                decided_by="automatic",
                metadata={**proposal.metadata, "routing": "automatic_accept"},
            ))
        confirmed_evidence = list({
            (item.field_name, item.excerpt, item.locator): item
            for candidate in arbitration.recommended_codes
            for item in candidate.supporting_evidence
        }.values())
        evidence_summary = [
            f"{item.field_name}: {item.excerpt}" for item in confirmed_evidence
        ]
        return HumanReviewOutput(
            artifact_id=prepared_review.artifact_id,
            decision="accept",
            pre_read_memo=(
                "Automatic gate: two blind coders produced grounded readings and the "
                "Comparison Agent mapped them without a review trigger."
            ),
            final_codes=final_codes,
            rationale=(
                "Automatically accepted under the frozen review policy because the "
                "independent readings were stable, the comparison found no substantive "
                "disagreement, and validation returned only valid signals."
            ),
            evidence_summary=evidence_summary,
            confirmed_evidence=confirmed_evidence,
            codebook_changes=new_changes,
            metadata={
                "review_origin": "automatic_policy",
                "processing_origin": "automatic_policy",
                "human_reviewed": False,
                "gate": "transparent_routing_and_valid_validation",
                "confidence_level": "high",
                "confidence_rationale": (
                    "Both blind coders produced stable evidence-grounded readings, and "
                    "the Comparison and Validation stages found no frozen review trigger."
                ),
            },
        )

    def submit_prepared_review(
        self,
        run_state: RunState,
        *,
        prepared_review: PreparedArtifactReview,
        human_review_output: HumanReviewOutput,
    ) -> ArtifactRunResult:
        """Apply one human decision to a previously prepared evidence packet."""

        if human_review_output.artifact_id != prepared_review.artifact_id:
            msg = "Human review artifact_id does not match the prepared review."
            raise ValueError(msg)
        if prepared_review.codebook_version != run_state.codebook.version:
            raise ValueError(
                "The codebook changed after this evidence packet was prepared. "
                "Prepare the review again before submitting a decision."
            )
        if (
            prepared_review.review_origin == "current"
            and prepared_review.batch is not run_state.current_batch()
        ):
            msg = "Prepared review does not belong to the current coding batch."
            raise ValueError(msg)
        if (
            prepared_review.review_origin == "current"
            and prepared_review.artifact_id in set(run_state.history.reviewed_artifact_ids())
        ):
            msg = f"Artifact {prepared_review.artifact_id} has already been human-reviewed."
            raise ValueError(msg)
        self._validate_human_review_output(human_review_output)
        # Representative artifacts are system-maintained provenance, not a
        # field that a reviewer may edit in the submitted code payload.
        existing_by_id = {code.code_id: code for code in run_state.codebook.codes}
        managed_final_codes = [
            replace(
                code,
                representative_artifact_ids=(
                    list(dict.fromkeys([
                        *existing_by_id[code.code_id].representative_artifact_ids,
                        prepared_review.artifact_id,
                    ]))
                    if code.code_id in existing_by_id
                    else [prepared_review.artifact_id]
                ),
            )
            for code in human_review_output.final_codes
        ]
        human_review_output = replace(
            human_review_output,
            final_codes=managed_final_codes,
        )

        candidate_evidence = prepared_review.context_packet.evidence_items
        confirmed_evidence = human_review_output.confirmed_evidence
        candidate_keys = {
            (item.field_name, item.excerpt.strip()) for item in candidate_evidence
        }
        confirmed_keys = {
            (item.field_name, item.excerpt.strip()) for item in confirmed_evidence
        }
        human_assessed = human_review_output.metadata.get("human_reviewed", True) is True
        evidence_audit = {
            "status": "assessed" if human_assessed else "not_human_assessed",
            "agent_candidate_count": len(candidate_keys),
            "human_confirmed_candidate_count": len(candidate_keys & confirmed_keys),
            "human_added_count": len(confirmed_keys - candidate_keys),
            "agent_candidates_not_confirmed_count": len(candidate_keys - confirmed_keys),
            "omission_claimed": False,
        }
        human_review_output = replace(
            human_review_output,
            metadata={
                **human_review_output.metadata,
                "evidence_unit_audit": evidence_audit,
                "routing_decision": (
                    asdict(prepared_review.evidence_packet.routing_decision)
                    if prepared_review.evidence_packet.routing_decision is not None
                    else None
                ),
            },
        )

        validation_output = prepared_review.validation_output
        definition_changed = any(
            code.code_id not in existing_by_id or replace(code, representative_artifact_ids=[])
            != replace(existing_by_id[code.code_id], representative_artifact_ids=[])
            for code in human_review_output.final_codes
        )
        if human_review_output.decision == "revise" or (
                human_assessed and human_review_output.decision == "accept"
                and (definition_changed or human_review_output.codebook_changes)):
            # Apply on an isolated state first: neither versions nor accepted
            # assignments may leak from a failed candidate validation.
            candidate = deepcopy(run_state)
            candidate.metadata["candidate_validation_only"] = True
            self._apply_human_review(
                run_state=candidate, batch=prepared_review.batch,
                human_review_output=human_review_output,
                validation_output=validation_output,
                comparison_output=prepared_review.arbitration_output,
                review_origin=prepared_review.review_origin,
                retrospective_task_id=prepared_review.retrospective_task_id,
            )
            proposal = replace(
                prepared_review.arbitration_output,
                recommended_codes=[ProvisionalCode(
                    code_name=code.name, short_definition=code.definition,
                    supporting_evidence=human_review_output.confirmed_evidence,
                    relationship_to_codebook="reuse_existing_code",
                    linked_code_ids=[code.code_id],
                    inclusion_criteria=code.inclusion_criteria,
                    exclusion_criteria=code.exclusion_criteria,
                ) for code in human_review_output.final_codes],
                possible_codebook_changes=human_review_output.codebook_changes,
                preserved_alternatives=[], disagreements=[],
            )
            validation_output = self._validation_agent(ValidationInput(
                artifact=prepared_review.artifact,
                research_question=candidate.research_question,
                context_packet=prepared_review.context_packet,
                coder_outputs=prepared_review.coder_outputs,
                codebook=candidate.codebook, history=run_state.history,
                comparison_output=proposal,
                analysis_protocol=candidate.analysis_protocol,
                validation_scope="iterative_decision",
                historical_materials=self._historical_materials(run_state),
                corpus_audit={"human_revision": True,
                              "reviewer_rationale": human_review_output.rationale},
            ))
            try:
                self.require_supported_revision(validation_output)
            except ValueError:
                attempts = run_state.metadata.setdefault("human_revision_failures", {}).setdefault(
                    prepared_review.artifact_id, [])
                attempts.append({"validation_output": asdict(validation_output),
                                 "candidate": asdict(human_review_output),
                                 "base_version": run_state.codebook.version})
                if len(attempts) < run_state.review_policy.automatic_reassessment_limit:
                    raise
                human_review_output = replace(
                    human_review_output, decision="mark_uncertain", final_codes=[],
                    codebook_changes=[],
                    rationale="Human revision remained unsupported at the frozen work limit. " + human_review_output.rationale,
                    metadata={**human_review_output.metadata, "work_limit_exhausted": True,
                              "revision_attempts": len(attempts)},
                )

        if human_review_output.decision == "reject":
            attempts = sum(
                record.artifact_id == prepared_review.artifact_id
                and record.decision == "reject"
                for record in run_state.history.coding_records
            ) + 1
            if attempts >= run_state.review_policy.automatic_reassessment_limit:
                human_review_output = replace(
                    human_review_output, decision="mark_uncertain",
                    metadata={**human_review_output.metadata,
                              "rejected_proposal": True,
                              "work_limit_exhausted": True,
                              "revision_attempts": attempts},
                )

        self._apply_human_review(
            run_state=run_state,
            batch=prepared_review.batch,
            human_review_output=human_review_output,
            validation_output=validation_output,
            comparison_output=prepared_review.arbitration_output,
            review_origin=prepared_review.review_origin,
            retrospective_task_id=prepared_review.retrospective_task_id,
        )
        reopened = run_state.metadata.get("reopened_context_artifact_ids", [])
        if isinstance(reopened, list) and prepared_review.artifact_id in reopened:
            run_state.metadata["reopened_context_artifact_ids"] = [
                item for item in reopened if item != prepared_review.artifact_id
            ]
        return ArtifactRunResult(
            artifact_id=prepared_review.artifact_id,
            context_packet=prepared_review.context_packet,
            coder_outputs=prepared_review.coder_outputs,
            arbitration_output=prepared_review.arbitration_output,
            validation_output=validation_output,
            evidence_packet=replace(prepared_review.evidence_packet, validation_output=validation_output),
            human_review_output=human_review_output,
        )

    @staticmethod
    def require_supported_revision(output: ValidationOutput) -> None:
        """A human-approved structural change alone is not a new rejection.

        Evidence/format/boundary problems must be repaired or explicitly left
        unresolved, rather than committing a candidate with stale validation.
        """
        if any(signal.signal not in {"valid", "human_review_required"}
               for signal in output.signals) or any(
            criterion in {"R1", "R2", "R3", "R6"}
            for criterion in output.review_criteria
        ) or (output.human_review_required and not output.review_criteria):
            raise ValueError(
                "Revised decision remains pending: " +
                (output.summary or "validation identified unresolved evidence or boundary problems.")
            )

    def _validate_human_review_output(
        self,
        human_review_output: HumanReviewOutput,
    ) -> None:
        """Keep persisted terminal review records internally consistent.

        The web API performs the same validation before a request reaches this
        layer. Keeping it here also protects non-Web callers.
        """

        if human_review_output.decision in {
            "reject",
            "mark_uncertain",
            "request_additional_context",
        }:
            if human_review_output.final_codes or human_review_output.codebook_changes:
                msg = (
                    "Reject, mark_uncertain, and request_additional_context cannot include final codes or "
                    "codebook changes."
                )
                raise ValueError(msg)
        if human_review_output.final_codes and not human_review_output.evidence_summary:
            msg = "Every final code requires at least one human-confirmed evidence summary."
            raise ValueError(msg)

    def _run_one_artifact(
        self,
        run_state: RunState,
        batch: ArtifactBatchState,
        artifact: ArtifactRecord,
    ) -> ArtifactRunResult:
        prepared_review = self.prepare_one_artifact(
            run_state,
            artifact=artifact,
            batch=batch,
        )
        human_review_output = self._human_review_agent(
            self.human_review_input(run_state, prepared_review)
        )
        return self.submit_prepared_review(
            run_state,
            prepared_review=prepared_review,
            human_review_output=human_review_output,
        )

    def _build_evidence_packet(
        self,
        *,
        artifact,
        run_state: RunState,
        context_packet: ContextPacket,
        coder_outputs: list[CoderAgentOutput],
        arbitration_output: ArbitrationOutput,
        validation_output: ValidationOutput,
    ) -> EvidencePacket:
        candidate_definitions: list[str] = []
        candidate_definitions_zh: list[str] = []
        alternative_interpretations: list[str] = []
        alternative_interpretations_zh: list[str] = []
        for coder_output in coder_outputs:
            for provisional_code in coder_output.provisional_codes:
                candidate_definitions.append(provisional_code.short_definition)
                candidate_definitions_zh.append(
                    provisional_code.short_definition_zh
                    or provisional_code.short_definition
                )
                if provisional_code.alternative_interpretation:
                    alternative_interpretations.append(
                        provisional_code.alternative_interpretation
                    )
                if provisional_code.alternative_interpretation:
                    alternative_interpretations_zh.append(
                        provisional_code.alternative_interpretation_zh
                        or provisional_code.alternative_interpretation
                    )
        for provisional_code in arbitration_output.preserved_alternatives:
            if provisional_code.alternative_interpretation:
                alternative_interpretations.append(
                    provisional_code.alternative_interpretation
                )
            if provisional_code.alternative_interpretation:
                alternative_interpretations_zh.append(
                    provisional_code.alternative_interpretation_zh
                    or provisional_code.alternative_interpretation
                )

        change_packets = self._build_codebook_change_packets(
            run_state=run_state,
            artifact_id=artifact.artifact_id,
            arbitration_output=arbitration_output,
            validation_output=validation_output,
        )
        return EvidencePacket(
            artifact_id=artifact.artifact_id,
            original_artifact=artifact,
            research_question=run_state.research_question,
            context_packet=context_packet,
            coder_outputs=coder_outputs,
            candidate_definitions=candidate_definitions,
            candidate_definitions_zh=candidate_definitions_zh,
            alternative_interpretations=alternative_interpretations,
            alternative_interpretations_zh=alternative_interpretations_zh,
            comparison_output=arbitration_output,
            arbitration_output=arbitration_output,
            validation_output=validation_output,
            proposed_codebook_changes=list(arbitration_output.possible_codebook_changes),
            codebook_change_packets=change_packets,
            comparison_findings=list(arbitration_output.comparison_findings),
            analytic_memos=list(arbitration_output.analytic_memos),
            model_metadata={
                "evidence_unit_quality": {
                    "candidate_span_count": len(context_packet.evidence_items),
                    "grounded_locator_count": sum(
                        1
                        for item in context_packet.evidence_items
                        if item.locator is not None
                    ),
                    "all_candidates_located": bool(context_packet.evidence_items)
                    and all(
                        item.locator is not None
                        for item in context_packet.evidence_items
                    ),
                    "audit_method": "human_confirmation_when_routed",
                }
            },
        )

    def _build_codebook_change_packets(
        self,
        *,
        run_state: RunState,
        artifact_id: str,
        arbitration_output: ArbitrationOutput,
        validation_output: ValidationOutput,
    ) -> list[CodebookChangePacket]:
        """Build one deduplicated category-level packet per proposed change."""

        active_by_id = {
            code.code_id: code for code in run_state.codebook.active_codes()
        }
        boundary_artifact_ids = list(
            dict.fromkeys(
                compared_id
                for finding in arbitration_output.comparison_findings
                if finding.finding in {"boundary_case", "partial_overlap"}
                for compared_id in [
                    finding.current_artifact_id,
                    *finding.compared_artifact_ids,
                ]
                if compared_id
            )
        )
        validation_warnings = list(
            dict.fromkeys(
                signal.summary
                for signal in validation_output.signals
                if signal.signal != "valid" and signal.summary
            )
        )
        packets: list[CodebookChangePacket] = []
        seen_change_signatures: set[tuple[str, tuple[str, ...], tuple[str, ...]]] = set()
        for change in arbitration_output.possible_codebook_changes:
            if change.action == "no_change":
                continue
            resulting_names = change.metadata.get("resulting_code_names", [])
            if not isinstance(resulting_names, list):
                resulting_names = []
            normalized_results = {
                " ".join(str(name).split()).casefold()
                for name in resulting_names
                if str(name).strip()
            }
            if not normalized_results:
                normalized_results.add(" ".join(change.summary.split()).casefold())
            signature = (
                change.action,
                tuple(sorted(set(change.target_code_ids))),
                tuple(sorted(normalized_results)),
            )
            if signature in seen_change_signatures:
                continue
            seen_change_signatures.add(signature)
            before_codes = [
                active_by_id[code_id]
                for code_id in change.target_code_ids
                if code_id in active_by_id
            ]
            related_candidates = [
                candidate
                for candidate in [
                    *arbitration_output.recommended_codes,
                    *arbitration_output.preserved_alternatives,
                ]
                if candidate.proposed_codebook_action == change.action
                and set(candidate.proposed_codebook_target_ids)
                == set(change.target_code_ids)
                and " ".join(candidate.code_name.split()).casefold()
                in normalized_results
            ]
            proposed_codes = [
                CodeState(
                    code_id=f"proposed-{change.change_id}-{index}",
                    name=candidate.code_name,
                    definition=candidate.short_definition,
                    inclusion_criteria=list(candidate.inclusion_criteria),
                    exclusion_criteria=list(candidate.exclusion_criteria),
                    representative_artifact_ids=[artifact_id],
                    notes=[candidate.alternative_interpretation]
                    if candidate.alternative_interpretation
                    else [],
                    metadata={
                        "provisional": True,
                        "name_zh": candidate.code_name_zh,
                        "definition_zh": candidate.short_definition_zh,
                        "inclusion_criteria_zh": candidate.inclusion_criteria_zh,
                        "exclusion_criteria_zh": candidate.exclusion_criteria_zh,
                        "observed_phenomenon": candidate.observed_phenomenon,
                        "observed_phenomenon_zh": candidate.observed_phenomenon_zh,
                        "relationship_to_codebook": candidate.relationship_to_codebook,
                    },
                )
                for index, candidate in enumerate(related_candidates, start=1)
            ]
            affected = change.metadata.get("affected_historical_artifact_ids", [])
            if not isinstance(affected, list):
                affected = []
            packets.append(
                CodebookChangePacket(
                    change_id=change.change_id,
                    action=change.action,
                    summary=change.summary,
                    summary_zh=change.summary_zh,
                    rationale=change.rationale,
                    rationale_zh=change.rationale_zh,
                    before_codes=before_codes,
                    proposed_codes=proposed_codes,
                    supporting_artifact_ids=list(
                        dict.fromkeys([artifact_id, *change.artifact_ids])
                    ),
                    boundary_artifact_ids=boundary_artifact_ids,
                    affected_artifact_ids=list(
                        dict.fromkeys(str(item) for item in affected)
                    ),
                    validation_warnings=validation_warnings,
                )
            )
        return packets

    def _route_review(
        self,
        *,
        run_state: RunState,
        artifact_id: str,
        batch: ArtifactBatchState,
        context_packet: ContextPacket,
        coder_outputs: list[CoderAgentOutput],
        arbitration_output: ArbitrationOutput,
        validation_output: ValidationOutput,
        sampling_stream: str = "current",
    ) -> ReviewRoutingDecision:
        """Apply the run's frozen review policy using observable risk signals."""

        setting = run_state.review_policy.setting
        reasons: list[str] = []
        weighted_risks: dict[str, int] = {}

        def add_risk(name: str, weight: int) -> None:
            configured_weight = run_state.review_policy.risk_weights.get(name, weight)
            weighted_risks[name] = max(configured_weight, weighted_risks.get(name, 0))

        validation_signal_names = {
            signal.signal for signal in validation_output.signals
        }
        review_criteria = self._review_criteria(
            run_state=run_state,
            coder_outputs=coder_outputs,
            arbitration_output=arbitration_output,
            validation_output=validation_output,
        )
        material_context_gap = any(
            output.insufficient_context for output in coder_outputs
        ) or "context_missing" in validation_signal_names
        if material_context_gap:
            add_risk("missing_context", 3)
            if "R2" not in review_criteria:
                review_criteria.append("R2")
        boundary_disagreement_types = {
            "granularity_disagreement",
            "codebook_boundary_disagreement",
        }
        substantive_disagreements = [
            disagreement
            for disagreement in arbitration_output.disagreements
            if disagreement.disagreement_type
            not in {"output_format_inconsistency", *boundary_disagreement_types}
        ]
        boundary_disagreements = [
            disagreement
            for disagreement in arbitration_output.disagreements
            if disagreement.disagreement_type in boundary_disagreement_types
        ]
        if substantive_disagreements:
            add_risk("substantive_coder_disagreement", 3)
        boundary_risk = bool(
            boundary_disagreements or arbitration_output.preserved_alternatives
        ) or any(
            finding.finding in {"boundary_case", "partial_overlap"}
            for finding in arbitration_output.comparison_findings
        ) or bool(
            validation_signal_names.intersection({"category_overlap", "boundary_unclear"})
        )
        if boundary_risk:
            add_risk("new_or_ambiguous_boundary", 3)
        if validation_signal_names.intersection(
            {"evidence_insufficient", "unsupported_inference", "use_case_mismatch"}
        ):
            add_risk("validation_warning", 3)
        structural_changes = [
            change
            for change in arbitration_output.possible_codebook_changes
            if change.action in {"refine", "merge", "split", "rename", "add_parent"}
        ]
        if structural_changes:
            add_risk("structural_codebook_change", 3)
        if any(
            candidate.relationship_to_codebook == "new_code"
            for candidate in arbitration_output.recommended_codes
        ) and not self._safe_local_new_code(
            context_packet=context_packet,
            coder_outputs=coder_outputs,
            arbitration_output=arbitration_output,
            validation_output=validation_output,
        ):
            add_risk("new_code_proposal", 3)
        affected_ids: set[str] = set()
        for change in structural_changes:
            affected_ids.update(
                self._derived_affected_artifact_ids(run_state, change)
            )
        if len(affected_ids) >= run_state.review_policy.high_impact_case_threshold:
            add_risk("high_impact_codebook_revision", 3)

        if arbitration_output.prior_human_conflicts:
            add_risk("conflict_with_prior_human_boundary", 3)

        if "R6" in review_criteria:
            add_risk("unusable_agent_output", 3)

        hard_blockers = self._automatic_acceptance_blockers(
            run_state=run_state,
            context_packet=context_packet,
            coder_outputs=coder_outputs,
            arbitration_output=arbitration_output,
            validation_output=validation_output,
        )
        for blocker in hard_blockers:
            add_risk(blocker, 2)

        # These fields remain readable for old checkpoints, but they cannot
        # suppress a paper-defined R1-R6 route. Selective Review is governed
        # by observable criteria, not by a tunable confidence/risk threshold.

        # The evidence-unit audit is an evidence quality metric, not a second
        # review policy.  Older checkpoints may still carry this field, but it
        # must not silently increase the human-review rate.
        evidence_audit = False
        criterion_triggered = bool(review_criteria) or bool(hard_blockers)

        # Single-artifact runs use criterion-triggered review only. Multi-case
        # runs retain their frozen sampling windows, including a one-case tail
        # batch or a retrospective task represented by a one-case container.
        random_audit = False
        if setting == "selective" and not criterion_triggered and not hard_blockers:
            random_audit = self._selective_audit_membership(
                run_state,
                artifact_id=artifact_id,
                stream=sampling_stream,
            )

        risk_score = calculate_risk_score(
            weighted_risks,
            run_state.review_policy.risk_aggregation,
        )
        risks = list(weighted_risks)
        review_questions, review_questions_zh = self._review_questions(
            review_criteria, validation_output,
        )
        if setting == "full":
            route = "human_review"
            review_origin = "full_policy"
            reasons.append("Full Review requires human review for every artifact.")
        elif setting == "selective" and criterion_triggered:
            route = "human_review"
            review_origin = "risk_criterion"
            reasons.append(
                "Selective Review was triggered by one or more applicable R1-R6 criteria."
            )
        elif setting == "selective" and random_audit:
            route = "human_review"
            review_origin = "random_audit"
            reasons.append(
                "Selective Review sampled this otherwise unflagged decision under the fixed 10% audit rule."
            )
        elif setting == "automatic" and (criterion_triggered or risks) and not (
            set(review_criteria) == {"R4"}
            and not hard_blockers
            and "valid" in validation_signal_names
            and all(signal.signal in {"valid", "human_review_required"} for signal in validation_output.signals)
            and not arbitration_output.prior_human_conflicts
        ):
            route = "unresolved"
            review_origin = "automatic_unresolved"
            reasons.append(
                "Automatic setting preserves risky cases as unresolved instead of claiming human acceptance."
            )
        else:
            route = "automatic_accept"
            review_origin = "automatic_policy"
            reasons.append(
                "Automatic accepted a validated category change under R4 without human approval."
                if setting == "automatic" and review_criteria == ["R4"]
                else "No configured review trigger was observed."
            )

        return ReviewRoutingDecision(
            artifact_id=artifact_id,
            setting=setting,
            route=route,
            reasons=reasons,
            risk_signals=list(dict.fromkeys(risks)),
            random_audit=random_audit,
            evidence_audit=evidence_audit,
            review_origin=review_origin,
            risk_score=risk_score,
            signal_details={
                "weights": weighted_risks,
                "aggregation": run_state.review_policy.risk_aggregation,
                "threshold": None,
                "threshold_status": "ignored; routing uses R1-R6 criteria",
                "criterion_triggered": criterion_triggered,
                "calibration_version": run_state.review_policy.calibration_version,
                "evidence_candidate_count": len(context_packet.evidence_items),
                "evidence_locator_count": sum(
                    1 for item in context_packet.evidence_items if item.locator is not None
                ),
                "evidence_audit_rate": run_state.review_policy.evidence_audit_rate,
                "random_audit_rate": run_state.review_policy.random_audit_rate,
                "effective_random_audit_rate": (
                    run_state.review_policy.random_audit_rate
                    if self._selective_sampling_enabled(run_state) else 0.0
                ),
                "random_audit_status": (
                    "enabled_for_multi_artifact_run" if self._selective_sampling_enabled(run_state)
                    else "disabled_for_single_artifact_batches"
                ),
                "batch_id": batch.batch_id,
                "batch_size": batch.size,
                "sampling_manifest": run_state.metadata.get(
                    "review_sampling_manifest", {}
                ),
                "substantive_disagreement_count": len(substantive_disagreements),
                "boundary_disagreement_count": len(boundary_disagreements),
                "format_only_disagreement_count": (
                    len(arbitration_output.disagreements)
                    - len(substantive_disagreements)
                    - len(boundary_disagreements)
                ),
                "derived_affected_artifact_ids": sorted(affected_ids),
                "prior_human_conflicts": arbitration_output.prior_human_conflicts,
                "hard_blockers": hard_blockers,
                "validation_recommended_review": validation_output.human_review_required,
                "review_criteria": review_criteria,
                "review_questions": review_questions,
                "review_questions_zh": review_questions_zh,
                "safe_local_new_code": self._safe_local_new_code(
                    context_packet=context_packet,
                    coder_outputs=coder_outputs,
                    arbitration_output=arbitration_output,
                    validation_output=validation_output,
                ),
            },
        )

    @staticmethod
    def _selective_sampling_enabled(run_state: RunState) -> bool:
        """Use configured batch size, not a final short batch or task wrapper.

        Legacy checkpoints predate the explicit protocol: inspect their stored
        iterative batches without migrating them or redrawing saved samples.
        """
        configured = run_state.metadata.get("iterative_batch_protocol", {}).get("batch_size")
        if configured is not None:
            return int(configured) > 1
        return any(batch.size > 1 for batch in run_state.coding_batches)

    @staticmethod
    def _selective_audit_membership(
        run_state: RunState,
        *,
        artifact_id: str,
        stream: str = "current",
    ) -> bool:
        """Sample one eligible decision from each complete ten-decision window.

        This is intentionally separate from the execution micro-batch. A
        decision is counted only after R1-R6 and deterministic blockers show it
        is otherwise unflagged. The random rank is fixed by the run seed and
        window index, so retries and restarts cannot redraw the sample.
        """

        if (not CODAOrchestrator._selective_sampling_enabled(run_state)
                or run_state.review_policy.random_audit_rate <= 0):
            return False
        manifest = run_state.metadata.get("review_sampling_manifest")
        if not isinstance(manifest, dict):
            return False
        # Checkpoints created before the cumulative-window protocol used a
        # population-level sample. Preserve their frozen membership on resume;
        # new runs never enter this compatibility branch.
        if "sampling_window_size" not in manifest and isinstance(
            manifest.get("blocks"), list
        ):
            return artifact_id in {
                str(item) for item in manifest.get("sampled_artifact_ids", [])
            }
        streams = manifest.setdefault("streams", {})
        state = streams.setdefault(
            stream,
            {
                "eligible_decision_count": 0,
                "decisions": {},
                "completed_windows": [],
                "sampled_artifact_ids": [],
            },
        )
        if not isinstance(state, dict):
            return False
        decisions = state.setdefault("decisions", {})
        existing = decisions.get(artifact_id)
        if isinstance(existing, dict):
            return bool(existing.get("sampled", False))

        window_size = int(manifest.get("sampling_window_size", 10) or 10)
        eligible_count = int(state.get("eligible_decision_count", 0)) + 1
        window_index = (eligible_count - 1) // window_size
        rank_in_window = (eligible_count - 1) % window_size + 1
        seed = int(manifest.get("seed", run_state.review_policy.random_seed))
        digest = hashlib.sha256(
            f"{seed}:{run_state.dataset_metadata.dataset_name}:{stream}:window-{window_index}".encode(
                "utf-8"
            )
        ).hexdigest()
        selected_rank = int(digest[:16], 16) % window_size + 1
        sampled = rank_in_window == selected_rank
        decisions[artifact_id] = {
            "eligible_index": eligible_count,
            "window_index": window_index,
            "rank_in_window": rank_in_window,
            "selected_rank": selected_rank,
            "sampled": sampled,
        }
        state["eligible_decision_count"] = eligible_count
        if sampled:
            state.setdefault("sampled_artifact_ids", []).append(artifact_id)
        all_sampled = {
            str(item)
            for stream_state in streams.values()
            if isinstance(stream_state, dict)
            for item in stream_state.get("sampled_artifact_ids", [])
        }
        manifest["sampled_artifact_ids"] = sorted(all_sampled)
        manifest["sample_size"] = len(all_sampled)
        if rank_in_window == window_size:
            state.setdefault("completed_windows", []).append(
                {
                    "window_index": window_index,
                    "eligible_artifact_ids": [
                        item_id
                        for item_id, item in decisions.items()
                        if isinstance(item, dict)
                        and item.get("window_index") == window_index
                    ],
                    "selected_rank": selected_rank,
                    "sampled_artifact_id": next((item_id for item_id, item in decisions.items()
                        if isinstance(item, dict) and item.get("window_index") == window_index
                        and item.get("sampled")), None),
                }
            )
        return sampled

    @staticmethod
    def _derived_affected_artifact_ids(
        run_state: RunState,
        change: CodebookChangeState,
    ) -> set[str]:
        target_ids = set(change.target_code_ids)
        affected = {
            record.artifact_id
            for record in run_state.history.coding_records
            if target_ids.intersection(record.final_code_ids)
        }
        for code_id in target_ids:
            code = run_state.codebook.get_code(code_id)
            if code is not None:
                affected.update(code.representative_artifact_ids)
        explicit = change.metadata.get("affected_historical_artifact_ids", [])
        if isinstance(explicit, list):
            affected.update(str(item) for item in explicit)
        return affected

    @staticmethod
    def _review_criteria(
        *,
        run_state: RunState,
        coder_outputs: list[CoderAgentOutput],
        arbitration_output: ArbitrationOutput,
        validation_output: ValidationOutput,
    ) -> list[str]:
        """Derive the six pre-specified review criteria from observable records."""

        signals = {signal.signal for signal in validation_output.signals}
        criteria: set[str] = set(validation_output.review_criteria)
        # A validation response that explicitly requests human review without
        # naming a structural reason is itself unusable for the paper-defined
        # routing contract.  Do not let this malformed response fall through
        # to automatic acceptance; route it as R6 so the researcher can decide
        # whether to repair the proposal, provide context, or leave it open.
        if validation_output.human_review_required and not criteria:
            criteria.add("R6")
        if (
            validation_output.model_metadata.get("agent_failure")
            or any(
                output.model_metadata.get("agent_failure")
                for output in coder_outputs
            )
            or arbitration_output.model_metadata.get("agent_failure")
        ):
            criteria.add("R6")
        # R1 is only an unresolved, incompatible interpretation. Comparison
        # may preserve a difference for provenance while resolving it in the
        # recommended assignment; that alone is not a review trigger.
        if any(
            disagreement.disagreement_type
            in {"evidence_disagreement", "semantic_disagreement"}
            and not arbitration_output.recommended_codes
            and bool(arbitration_output.preserved_alternatives)
            for disagreement in arbitration_output.disagreements
        ):
            criteria.add("R1")
        if signals.intersection({"evidence_insufficient", "unsupported_inference", "context_missing"}):
            criteria.add("R2")
        if signals.intersection({"category_overlap", "boundary_unclear"}) or any(
            finding.finding in {"partial_overlap", "boundary_case"}
            and (
                finding.resolution_status == "unresolved"
                or finding.resolution_status is None and not finding.implication.lower().startswith(
                    ("resolved", "complementary", "permitted"))
            )
            for finding in arbitration_output.comparison_findings
        ):
            criteria.add("R3")
        accepted_code_ids = {
            code_id
            for record in run_state.history.coding_records
            for code_id in record.final_code_ids
        }
        if any(
            change.action in {"merge", "split"}
            or (
                change.action == "refine"
                and bool(accepted_code_ids.intersection(change.target_code_ids))
            )
            or (
                change.action == "add_parent"
                and change.metadata.get("changes_existing_meaning", False) is True
                and bool(change.target_code_ids)
                and bool(accepted_code_ids.intersection(change.target_code_ids))
            )
            for change in arbitration_output.possible_codebook_changes
        ):
            criteria.add("R4")
        if arbitration_output.prior_human_conflicts:
            criteria.add("R5")
        if (
            len(coder_outputs) < 2
            or any(
                not output.provisional_codes and not output.insufficient_context
                for output in coder_outputs
            )
            or any(
                not candidate.supporting_evidence
                for output in coder_outputs
                for candidate in output.provisional_codes
            )
            or not arbitration_output.recommended_codes
            and not arbitration_output.preserved_alternatives
            and not criteria.intersection({"R2", "R3"})
            and not any(output.insufficient_context for output in coder_outputs)
        ):
            criteria.add("R6")
        if any(
            candidate.relationship_to_codebook != "uncertain"
            or candidate.linked_code_ids
            or candidate.proposed_codebook_target_ids
            or candidate.proposed_codebook_action != "no_change"
            or not candidate.supporting_evidence
            for output in coder_outputs
            for candidate in output.provisional_codes
        ):
            # Coders are codebook-blind. A mapping, target, codebook action,
            # or ungrounded proposal makes the response unusable rather than
            # an ordinary disagreement.
            criteria.add("R6")
        return [criterion for criterion in ("R1", "R2", "R3", "R4", "R5", "R6") if criterion in criteria]

    @staticmethod
    def _review_questions(
        criteria: list[str],
        validation_output: ValidationOutput,
    ) -> tuple[list[str], list[str]]:
        """Return one actionable bilingual question for every routed criterion."""

        default_questions = {
            "R1": (
                "Which coder interpretation is supported by the cited evidence, and why can the alternatives not both be retained?",
                "引用的证据支持哪一种编码者解释？为什么不能同时保留其他解释？",
            ),
            "R2": (
                "What missing or conflicting evidence must be checked before accepting this assignment or change?",
                "在接受这次归类或修改前，还需要核对哪些缺失或相互冲突的证据？",
            ),
            "R3": (
                "Do the competing categories describe the same interpretation, and where should their boundary be drawn?",
                "这些竞争类别是否表达同一种解释？它们的边界应当如何划分？",
            ),
            "R4": (
                "Should this established category change, and what earlier assignments are affected by the proposed change?",
                "这个已有类别是否应当修改？该修改会影响哪些此前的归类？",
            ),
            "R5": (
                "How should this proposal be reconciled with the earlier human decision or approved category condition?",
                "这项提议应如何与此前的人类决定或已批准的类别条件保持一致？",
            ),
            "R6": (
                "Is the agent output usable as written, or should it be repaired, supplemented with context, or left unresolved?",
                "当前 Agent 输出是否可以直接使用？还是应当修复、补充上下文，或保留为未解决？",
            ),
        }
        supplied_by_criterion = {
            criterion: (
                validation_output.review_questions[index],
                validation_output.review_questions_zh[index],
            )
            for index, criterion in enumerate(validation_output.review_criteria)
            if index < len(validation_output.review_questions)
            and index < len(validation_output.review_questions_zh)
        }
        english: list[str] = []
        chinese: list[str] = []
        for criterion in criteria:
            supplied = supplied_by_criterion.get(criterion)
            question = supplied or default_questions[criterion]
            english.append(question[0])
            chinese.append(question[1])
        return english, chinese

    @staticmethod
    def _automatic_acceptance_blockers(
        *,
        run_state: RunState,
        context_packet: ContextPacket,
        coder_outputs: list[CoderAgentOutput],
        arbitration_output: ArbitrationOutput,
        validation_output: ValidationOutput,
    ) -> list[str]:
        """Return deterministic blockers used by routing and materialization alike."""

        blockers: list[str] = []
        validation_signal_names = {
            signal.signal for signal in validation_output.signals
        }
        if (
            (
                any(output.insufficient_context for output in coder_outputs)
                or "context_missing" in validation_signal_names
            )
        ):
            blockers.append("missing_context")
        if any(
            signal.signal
            in {"evidence_insufficient", "unsupported_inference", "use_case_mismatch"}
            for signal in validation_output.signals
        ):
            blockers.append("validation_warning")
        if "R6" in CODAOrchestrator._review_criteria(
            run_state=run_state,
            coder_outputs=coder_outputs,
            arbitration_output=arbitration_output,
            validation_output=validation_output,
        ):
            blockers.append("unusable_agent_output")
        if run_state.review_policy.setting != "automatic" and any(
            change.action in {"refine", "merge", "split", "add_parent"}
            for change in arbitration_output.possible_codebook_changes
        ):
            blockers.append("structural_codebook_change")

        for output in coder_outputs:
            for candidate in output.provisional_codes:
                if candidate.relationship_to_codebook != "uncertain":
                    blockers.append("non_blind_coder_mapping")
                if candidate.linked_code_ids or candidate.proposed_codebook_target_ids:
                    blockers.append("non_blind_coder_mapping")
                if candidate.proposed_codebook_action != "no_change":
                    blockers.append("non_blind_coder_mapping")
                if not candidate.supporting_evidence:
                    blockers.append("ungrounded_coder_output")
            if not output.provisional_codes and not output.insufficient_context:
                blockers.append("empty_coder_output")

        if len(coder_outputs) < 2:
            blockers.append("insufficient_independent_coders")

        active_ids = {code.code_id for code in run_state.codebook.active_codes()}
        recommended_existing_ids: set[str] = set()
        new_candidate_names: set[str] = set()
        for candidate in arbitration_output.recommended_codes:
            structural = {
                "refine_existing_code": "refine", "merge_existing_codes": "merge",
                "split_existing_code": "split", "add_parent_code": "add_parent",
            }
            if run_state.review_policy.setting == "automatic" and candidate.relationship_to_codebook in structural:
                targets = candidate.proposed_codebook_target_ids or candidate.linked_code_ids
                action = structural[candidate.relationship_to_codebook]
                if (
                    candidate.proposed_codebook_action != action
                    or not targets or not set(targets) <= active_ids
                    or not any(
                        change.action == action and set(change.target_code_ids) == set(targets)
                        for change in arbitration_output.possible_codebook_changes
                    )
                ):
                    blockers.append("unresolvable_comparison_mapping")
                if not candidate.supporting_evidence:
                    blockers.append("ungrounded_recommendation")
                continue
            if candidate.relationship_to_codebook not in {"reuse_existing_code", "new_code"}:
                blockers.append("unresolvable_comparison_mapping")
                continue
            if not candidate.supporting_evidence:
                blockers.append("ungrounded_recommendation")
            if candidate.relationship_to_codebook == "reuse_existing_code":
                if not candidate.linked_code_ids or not set(candidate.linked_code_ids) <= active_ids:
                    blockers.append("unresolvable_comparison_mapping")
                recommended_existing_ids.update(candidate.linked_code_ids)
            elif candidate.relationship_to_codebook == "new_code":
                normalized_name = " ".join(candidate.code_name.split()).casefold()
                if not normalized_name or normalized_name in new_candidate_names:
                    blockers.append("duplicate_new_code_candidate")
                new_candidate_names.add(normalized_name)

        # Comparison, rather than either blind coder, is the sole authority for
        # mapping candidates to existing codes or proposing a local new code.
        if any(
            candidate.relationship_to_codebook == "uncertain"
            for candidate in arbitration_output.recommended_codes
        ):
            blockers.append("unresolvable_comparison_mapping")

        if not arbitration_output.recommended_codes and not arbitration_output.preserved_alternatives:
            blockers.append("empty_comparison_recommendation")

        return list(dict.fromkeys(blockers))

    @staticmethod
    def _safe_local_new_code(
        *,
        context_packet: ContextPacket,
        coder_outputs: list[CoderAgentOutput],
        arbitration_output: ArbitrationOutput,
        validation_output: ValidationOutput,
    ) -> bool:
        """Return whether a new category is narrow and grounded enough for auto-add.

        This exception applies only to a local ``add``. Meaning-changing operations
        such as refine, merge, split, rename, and add-parent always remain review
        triggers because they can invalidate prior assignments.
        """

        new_candidates = [
            candidate
            for candidate in arbitration_output.recommended_codes
            if candidate.relationship_to_codebook == "new_code"
        ]
        if not new_candidates or len(coder_outputs) < 2:
            return False
        normalized_new_names = [
            " ".join(candidate.code_name.split()).casefold()
            for candidate in new_candidates
        ]
        if (
            any(not name for name in normalized_new_names)
            or len(normalized_new_names) != len(set(normalized_new_names))
        ):
            return False
        if any(
            signal.signal
            in {
                "evidence_insufficient",
                "unsupported_inference",
                "use_case_mismatch",
                "category_overlap",
                "boundary_unclear",
            }
            for signal in validation_output.signals
        ):
            return False
        if any(
            output.insufficient_context
            or not output.provisional_codes
            for output in coder_outputs
        ):
            return False
        if arbitration_output.preserved_alternatives:
            return False
        if any(
            disagreement.disagreement_type != "output_format_inconsistency"
            for disagreement in arbitration_output.disagreements
        ):
            return False
        if any(not candidate.supporting_evidence for candidate in new_candidates):
            return False
        if any(
            candidate.relationship_to_codebook
            not in {"reuse_existing_code", "new_code"}
            for candidate in arbitration_output.recommended_codes
        ):
            return False
        return all(
            change.action in {"add", "no_change"}
            for change in arbitration_output.possible_codebook_changes
        )

    def _apply_human_review(
        self,
        *,
        run_state: RunState,
        batch: ArtifactBatchState,
        human_review_output: HumanReviewOutput,
        validation_output: ValidationOutput,
        comparison_output: ComparisonOutput | None = None,
        review_origin: str = "current",
        retrospective_task_id: str | None = None,
    ) -> None:
        human_review_output = self._apply_experiment_variant(
            run_state,
            human_review_output,
            review_origin=review_origin,
        )
        suppressed_change_details = human_review_output.metadata.get(
            "suppressed_codebook_change_details"
        )
        if isinstance(suppressed_change_details, dict):
            suppression = {
                "event": "codebook_refinement_suppressed",
                "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                "experiment_variant": human_review_output.metadata.get(
                    "experiment_variant"
                ),
                "artifact_id": human_review_output.artifact_id,
                "details": dict(suppressed_change_details),
            }
            suppression_events = run_state.metadata.setdefault(
                "codebook_suppression_events", []
            )
            if isinstance(suppression_events, list):
                suppression_events.append(dict(suppression))
            events = run_state.metadata.setdefault("events", [])
            if isinstance(events, list):
                events.append(dict(suppression))
        coding_round = len(run_state.history.coding_records)
        changes = [
            replace(change, round_index=coding_round)
            for change in self._resolve_codebook_changes(
                existing_codes=run_state.codebook.codes,
                human_review_output=human_review_output,
            )
        ]
        codebook_version_before = run_state.codebook.version
        previous_record = run_state.history.latest_record_for_artifact(
            human_review_output.artifact_id
        )

        next_codes = self._merge_final_codes(
            run_state.codebook.codes,
            human_review_output.final_codes,
        )
        applied_changes: list[CodebookChangeState] = []
        for change in changes:
            next_codes = self._apply_codebook_change(next_codes, change)
            run_state.history.append_revision(change)
            if change.action != "no_change":
                applied_changes.append(change)
        if applied_changes:
            run_state.codebook = replace(
                run_state.codebook,
                version=codebook_version_before + 1,
                codes=next_codes,
                revisions=[
                    *run_state.codebook.revisions,
                    *applied_changes,
                ],
            )
        else:
            run_state.codebook = run_state.codebook.with_codes(next_codes)

        record_id = f"record-{uuid4().hex[:12]}"
        coding_record = human_review_output.to_coding_record(
            dataset_name=run_state.dataset_metadata.dataset_name,
            batch_index=batch.batch_index,
            codebook_version_before=codebook_version_before,
            codebook_version_after=run_state.codebook.version,
            record_id=record_id,
            validation_output=validation_output,
        )
        # Retrospective coding is a distinct provenance class even when the
        # frozen routing policy accepts it automatically. Preserve the routing
        # mechanism separately instead of letting it hide the record origin.
        if review_origin != "current":
            coding_record.metadata["review_origin"] = review_origin
        else:
            coding_record.metadata.setdefault("review_origin", review_origin)
        coding_record.metadata.setdefault("retrospective_task_id", retrospective_task_id)
        suppressed_variant_details = human_review_output.metadata.get(
            "suppressed_codebook_change_details"
        )
        if isinstance(suppressed_variant_details, dict):
            coding_record.metadata["suppressed_codebook_change_details"] = dict(
                suppressed_variant_details
            )
        if review_origin == "retrospective":
            coding_record.metadata["supersedes_record_id"] = (
                previous_record.record_id if previous_record is not None else None
            )
        run_state.history.append_record(coding_record)
        if human_review_output.decision in {"accept", "revise"}:
            for unresolved in run_state.history.unresolved_cases:
                if unresolved.artifact_id == human_review_output.artifact_id and unresolved.status == "open":
                    unresolved.status = "resolved"
                    unresolved.resolution = human_review_output.rationale
                    unresolved.metadata["resolved_by_record_id"] = coding_record.record_id
        if human_review_output.decision in {
            "mark_uncertain",
            "request_additional_context",
        }:
            run_state.history.append_unresolved(
                UnresolvedCaseState(
                    unresolved_id=f"unresolved-{uuid4().hex[:12]}",
                    artifact_id=human_review_output.artifact_id,
                    reason=human_review_output.rationale,
                    source=(
                        "automatic"
                        if not human_review_output.metadata.get("human_reviewed", True)
                        else "human_review"
                    ),
                    created_at_codebook_version=run_state.codebook.version,
                    related_code_ids=[
                        code.code_id for code in human_review_output.final_codes
                    ],
                    requested_context=(
                        list(human_review_output.notes)
                        if human_review_output.decision == "request_additional_context"
                        else []
                    ),
                    metadata={
                        "record_id": coding_record.record_id,
                        "review_origin": review_origin,
                        **(
                            {
                                "experiment_variant": human_review_output.metadata.get(
                                    "experiment_variant"
                                ),
                                "suppressed_codebook_change_details": dict(
                                    suppressed_variant_details
                                ),
                            }
                            if isinstance(suppressed_variant_details, dict)
                            else {}
                        ),
                    },
                )
            )
            if human_review_output.decision == "request_additional_context":
                requested_items = [
                    item.strip() for item in human_review_output.notes if item.strip()
                ] or [human_review_output.rationale]
                run_state.history.append_context_request(
                    ContextRequestState(
                        request_id=f"context-request-{uuid4().hex[:12]}",
                        scope="artifact",
                        artifact_id=human_review_output.artifact_id,
                        reason=human_review_output.rationale,
                        requested_items=requested_items,
                        created_at_codebook_version=run_state.codebook.version,
                        metadata={
                            "record_id": coding_record.record_id,
                            "review_origin": review_origin,
                            "retrospective_task_id": retrospective_task_id,
                        },
                    )
                )
        for memo in (comparison_output.analytic_memos if comparison_output else []):
            run_state.history.append_analytic_memo(asdict(memo))
        for change in applied_changes:
            if run_state.metadata.get("candidate_validation_only"):
                continue
            self._enqueue_retrospective_tasks(
                run_state=run_state,
                change=change,
                from_codebook_version=codebook_version_before,
                source_artifact_id=human_review_output.artifact_id,
            )

        if review_origin == "retrospective" and retrospective_task_id:
            task = run_state.history.retrospective_task(retrospective_task_id)
            if task is not None:
                task.attempt_count += 1
                task.status = (
                    "awaiting_human" if human_review_output.decision == "request_additional_context"
                    else "pending" if human_review_output.decision == "reject"
                    else "completed"
                )

    @staticmethod
    def _apply_experiment_variant(
        run_state: RunState,
        human_review_output: HumanReviewOutput,
        *,
        review_origin: str,
    ) -> HumanReviewOutput:
        """Apply pre-registered ablation constraints after initialization."""

        protocol = run_state.metadata.get("experiment_protocol", {})
        if not isinstance(protocol, dict):
            return human_review_output
        if protocol.get("variant") != "freeze_after_initialization":
            return human_review_output
        bootstrap = run_state.metadata.get("bootstrap", {})
        if not isinstance(bootstrap, dict) or bootstrap.get("status") != "completed":
            return human_review_output
        bootstrap_ids = {str(item) for item in bootstrap.get("artifact_ids", [])}
        if review_origin == "bootstrap_provisional" or human_review_output.artifact_id in bootstrap_ids:
            return human_review_output

        existing_by_id = {
            code.code_id: code for code in run_state.codebook.active_codes()
        }
        has_new_code = any(code.code_id not in existing_by_id for code in human_review_output.final_codes)
        has_changed_definition = any(
            code.code_id in existing_by_id
            and replace(code, representative_artifact_ids=[])
            != replace(existing_by_id[code.code_id], representative_artifact_ids=[])
            for code in human_review_output.final_codes
        )
        has_change_operation = any(
            change.action != "no_change"
            for change in human_review_output.codebook_changes
        )
        if not (has_new_code or has_changed_definition or has_change_operation):
            return human_review_output

        preserved_codes = [
            existing_by_id[code.code_id]
            for code in human_review_output.final_codes
            if code.code_id in existing_by_id
        ]
        metadata = dict(human_review_output.metadata)
        metadata["experiment_variant"] = "freeze_after_initialization"
        metadata["suppressed_codebook_change"] = True
        metadata["suppressed_change_count"] = len(human_review_output.codebook_changes)
        metadata["suppressed_codebook_change_details"] = {
            "reason": "codebook_frozen_after_initialization",
            "new_code_ids": sorted(
                code.code_id
                for code in human_review_output.final_codes
                if code.code_id not in existing_by_id
            ),
            "changed_code_ids": sorted(
                code.code_id
                for code in human_review_output.final_codes
                if code.code_id in existing_by_id
                and replace(code, representative_artifact_ids=[])
                != replace(
                    existing_by_id[code.code_id],
                    representative_artifact_ids=[],
                )
            ),
            "proposed_changes": [
                asdict(change) for change in human_review_output.codebook_changes
            ],
            "suppressed_final_code_ids": [
                code.code_id for code in human_review_output.final_codes
            ],
        }
        return replace(
            human_review_output,
            decision="mark_uncertain",
            final_codes=preserved_codes,
            codebook_changes=[],
            request_additional_context=False,
            rationale=(
                human_review_output.rationale
                + " Codebook refinement is disabled in the freeze-after-initialization ablation; "
                "the proposed change remains unresolved."
            ),
            metadata=metadata,
        )

    def _enqueue_retrospective_tasks(
        self,
        *,
        run_state: RunState,
        change: CodebookChangeState,
        from_codebook_version: int,
        source_artifact_id: str,
    ) -> list[RetrospectiveRecodingTask]:
        """Create append-only tasks for historical records affected by a change."""

        protocol = run_state.metadata.get("experiment_protocol", {})

        target_ids = set(change.target_code_ids)
        explicit_ids = change.metadata.get("affected_historical_artifact_ids", [])
        if not isinstance(explicit_ids, list):
            explicit_ids = []

        bootstrap = run_state.metadata.get("bootstrap", {})
        bootstrap_ids = {
            str(artifact_id)
            for artifact_id in (
                bootstrap.get("artifact_ids", [])
                if isinstance(bootstrap, dict)
                else []
            )
        }
        historical_ids = set(run_state.history.reviewed_artifact_ids()) | bootstrap_ids
        affected: set[str] = {
            str(artifact_id)
            for artifact_id in [*explicit_ids, *change.artifact_ids]
            if str(artifact_id) in historical_ids
        }
        latest_records = [
            run_state.history.latest_record_for_artifact(artifact_id)
            for artifact_id in run_state.history.reviewed_artifact_ids()
        ]
        # Adding a category can also affect earlier cases that were previously
        # left unresolved or described with a broader neighboring code. Treat
        # it as a substantive change for candidate historical screening; the
        # later Comparison/Validation stages still decide whether recoding is
        # actually warranted.
        substantive_actions = {"add", "refine", "merge", "split", "add_parent"}
        semantic_matches = {}
        if change.action in substantive_actions:
            for code_id in target_ids:
                code = run_state.codebook.get_code(code_id)
                if code is not None:
                    affected.update(code.representative_artifact_ids)
        if change.action in {"refine", "split"}:
            affected.update(
                record.artifact_id
                for record in latest_records
                if record is not None and target_ids.intersection(record.final_code_ids)
            )
        elif change.action == "merge":
            affected.update(
                record.artifact_id
                for record in latest_records
                if record is not None and target_ids.intersection(record.final_code_ids)
            )
        elif change.action == "add_parent":
            # Children retain their labels, but their interpretation may now
            # include a hierarchy that was not available at first coding.
            affected.update(
                record.artifact_id
                for record in latest_records
                if record is not None and target_ids.intersection(record.final_code_ids)
            )

        if change.action in substantive_actions:
            adjacent_code_ids = {
                code.code_id
                for code in run_state.codebook.codes
                if code.parent_code_id in target_ids
                or code.code_id in {
                    parent_id
                    for target_id in target_ids
                    for parent_id in [
                        (
                            run_state.codebook.get_code(target_id).parent_code_id
                            if run_state.codebook.get_code(target_id) is not None
                            else None
                        )
                    ]
                    if parent_id
                }
            }
            affected.update(
                record.artifact_id
                for record in latest_records
                if record is not None
                and adjacent_code_ids.intersection(record.final_code_ids)
            )
            for code_id in adjacent_code_ids:
                code = run_state.codebook.get_code(code_id)
                if code is not None:
                    affected.update(code.representative_artifact_ids)
            for memo in run_state.history.analytic_memos:
                memo_code_ids = memo.get("code_ids", [])
                memo_artifact_ids = memo.get("artifact_ids", [])
                if (
                    isinstance(memo_code_ids, list)
                    and isinstance(memo_artifact_ids, list)
                    and (target_ids | adjacent_code_ids).intersection(
                        str(item) for item in memo_code_ids
                    )
                ):
                    affected.update(str(item) for item in memo_artifact_ids)
            affected.update(
                item.artifact_id for item in run_state.history.open_unresolved_cases()
            )

            query_parts = [change.summary, change.rationale]
            for code_id in target_ids | set(change.resulting_code_ids):
                code = run_state.codebook.get_code(code_id)
                if code is not None:
                    query_parts.extend(
                        [
                            code.name,
                            code.definition,
                            *code.inclusion_criteria,
                            *code.exclusion_criteria,
                        ]
                    )
            # Build one auditable retrieval document per historical artifact.
            # The lexical retriever only proposes candidates; it does not make
            # a semantic recoding decision. Include stored coding records,
            # analytic memos, and unresolved-case reasons so an added category
            # can find earlier material that was not assigned a code.
            documents: dict[str, list[str]] = {}
            for record in latest_records:
                if record is None or record.artifact_id == source_artifact_id:
                    continue
                documents.setdefault(record.artifact_id, []).extend(
                    [record.rationale, *record.evidence_summary, *record.final_code_names]
                )
            for artifact_id, material in self._historical_materials(run_state).items():
                if artifact_id != source_artifact_id:
                    documents.setdefault(artifact_id, []).extend([
                        str(material.get("content", "")),
                        str(material.get("context_packet", {}).get("context_brief", "")),
                    ])
            for memo in run_state.history.analytic_memos:
                memo_artifact_ids = memo.get("artifact_ids", [])
                if not isinstance(memo_artifact_ids, list):
                    continue
                memo_text = " ".join(
                    str(item)
                    for item in (
                        memo.get("summary", ""),
                        memo.get("summary_zh", ""),
                        memo.get("rationale", ""),
                    )
                    if item
                )
                for artifact_id in memo_artifact_ids:
                    if str(artifact_id) != source_artifact_id and memo_text:
                        documents.setdefault(str(artifact_id), []).append(memo_text)
            for unresolved in run_state.history.unresolved_cases:
                if unresolved.artifact_id == source_artifact_id:
                    continue
                documents.setdefault(unresolved.artifact_id, []).extend(
                    [unresolved.reason, *unresolved.requested_context]
                )
            retrieval_documents = {
                artifact_id: " ".join(parts)
                for artifact_id, parts in documents.items()
                if artifact_id in historical_ids and any(parts)
            }
            for match in rank_semantic_impacts(
                " ".join(query_parts),
                retrieval_documents,
                top_k=run_state.review_policy.retrospective_semantic_top_k,
                minimum_score=run_state.review_policy.retrospective_semantic_min_score,
            ):
                affected.add(match.document_id)
                semantic_matches[match.document_id] = {
                    "score": round(match.score, 6),
                    "shared_terms": list(match.shared_terms),
                    "retriever": "local_idf_lexical_v1",
                }

            # Lexical recall alone cannot screen a newly introduced concept.
            # Inspect every historical summary/record, independently of top-k;
            # original evidence is examined before any reassignment is accepted.
            if change.action == "add":
                materials = self._historical_materials(run_state)
                screen = getattr(self._comparison_agent, "screen_historical_impacts", None)
                candidates = sorted(historical_ids - {source_artifact_id})
                screenings = run_state.metadata.setdefault("historical_impact_screenings", {})
                for offset in range(0, len(candidates), 16):
                    ids = candidates[offset:offset + 16]
                    screen_key = f"{change.change_id}:{offset}"
                    if screen_key not in screenings:
                        cases = {key: {
                            "summary": materials.get(key, {}).get("context_packet", {}).get("context_brief"),
                            "coding_record": asdict(record) if (record := run_state.history.latest_record_for_artifact(key)) else None,
                        } for key in ids}
                        try:
                            if screen is None:
                                raise ValueError("Comparison implementation has no semantic screening method.")
                            screenings[screen_key] = screen(change=change, codebook=run_state.codebook, cases=cases)
                        except Exception as error:
                            # Incomplete screening must widen recall, not silently
                            # exclude cases or undo an already accepted decision.
                            screenings[screen_key] = {"affected_cases": [], "unchecked_cases": [
                                {"artifact_id": key, "reason": f"Screening unavailable: {type(error).__name__}: {error}"}
                                for key in ids]}
                    result = screenings[screen_key]
                    affected.update(row["artifact_id"] for field in ("affected_cases", "unchecked_cases")
                                    for row in result[field])

            outside = sorted(
                historical_ids
                - affected
                - {source_artifact_id}
            )
            if outside:
                audit_index = int(
                    hashlib.sha256(change.change_id.encode("utf-8")).hexdigest(), 16
                ) % len(outside)
                affected.add(outside[audit_index])

        affected.discard(source_artifact_id)
        retrospective_disabled = (
            isinstance(protocol, dict)
            and protocol.get("variant") == "without_retrospective_recoding"
        )
        if retrospective_disabled:
            affected_ids = sorted(affected)
            suppression = {
                "event": "retrospective_recoding_suppressed",
                "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                "experiment_variant": "without_retrospective_recoding",
                "change_id": change.change_id,
                "change_action": change.action,
                "source_artifact_id": source_artifact_id,
                "affected_artifact_count": len(affected_ids),
                "affected_artifact_ids": affected_ids,
            }
            change.metadata.update(
                {
                    "retrospective_recoding_suppressed": True,
                    "suppressed_affected_artifact_count": len(affected_ids),
                    "suppressed_affected_artifact_ids": affected_ids,
                }
            )
            suppression_events = run_state.metadata.setdefault(
                "retrospective_suppression_events", []
            )
            if isinstance(suppression_events, list):
                suppression_events.append(dict(suppression))
            events = run_state.metadata.setdefault("events", [])
            if isinstance(events, list):
                events.append(dict(suppression))
            return []
        existing_keys = {
            (task.artifact_id, task.trigger_change_id)
            for task in run_state.history.retrospective_tasks
        }
        created: list[RetrospectiveRecodingTask] = []
        for artifact_id in sorted(affected):
            key = (artifact_id, change.change_id)
            if key in existing_keys:
                continue
            previous = run_state.history.latest_record_for_artifact(artifact_id)
            task = RetrospectiveRecodingTask(
                task_id=f"retro-{uuid4().hex[:12]}",
                artifact_id=artifact_id,
                trigger_change_id=change.change_id,
                from_codebook_version=from_codebook_version,
                target_codebook_version=run_state.codebook.version,
                reason=(
                    f"Reconsider artifact {artifact_id} after {change.action} change "
                    f"{change.change_id}: {change.summary}"
                ),
                metadata={
                    "change_action": change.action,
                    "target_code_ids": list(change.target_code_ids),
                    "resulting_code_ids": list(change.resulting_code_ids),
                    "previous_record_id": previous.record_id if previous else None,
                    "source_artifact_id": source_artifact_id,
                    "requires_evidence_rejudgment": change.action != "rename",
                    "impact_scope": "direct_adjacent_boundary_semantic_unresolved_plus_audit",
                    "semantic_retrieval": semantic_matches.get(artifact_id),
                },
            )
            run_state.history.append_retrospective_task(task)
            created.append(task)
        return created

    def enqueue_retrospective_tasks(
        self,
        *,
        run_state: RunState,
        change: CodebookChangeState,
        from_codebook_version: int,
        source_artifact_id: str,
    ) -> list[RetrospectiveRecodingTask]:
        """Expose version-propagation work to stage-level human reviews."""

        return self._enqueue_retrospective_tasks(
            run_state=run_state,
            change=change,
            from_codebook_version=from_codebook_version,
            source_artifact_id=source_artifact_id,
        )

    def _resolve_codebook_changes(
        self,
        *,
        existing_codes: list[CodeState],
        human_review_output: HumanReviewOutput,
    ) -> list[CodebookChangeState]:
        """Validate and normalize a human-approved structural change plan.

        A ``CodebookChangeState`` is not merely a note. Its target and result
        IDs define a reproducible edit to the current codebook. Final codes
        carry the complete definitions of any resulting codes.
        """

        final_by_id = {code.code_id: code for code in human_review_output.final_codes}
        if len(final_by_id) != len(human_review_output.final_codes):
            msg = "Final code ids must be unique within one human review."
            raise ValueError(msg)

        existing_by_id = {code.code_id: code for code in existing_codes}
        final_by_name = {code.name.casefold(): code.code_id for code in human_review_output.final_codes}
        existing_by_name = {code.name.casefold(): code.code_id for code in existing_codes}
        resolved_changes: list[CodebookChangeState] = []
        structural_result_ids: set[str] = set()
        structural_target_ids: set[str] = set()

        for change in human_review_output.codebook_changes:
            target_ids = self._unique_ids(change.target_code_ids)
            result_ids = self._resolve_result_ids(
                change,
                final_by_name=final_by_name,
                existing_by_name=existing_by_name,
            )
            resolved = replace(
                change,
                target_code_ids=target_ids,
                resulting_code_ids=result_ids,
            )
            self._validate_change_shape(
                change=resolved,
                existing_by_id=existing_by_id,
                final_by_id=final_by_id,
            )
            if resolved.action != "no_change":
                structural_result_ids.update(resolved.resulting_code_ids)
                structural_target_ids.update(resolved.target_code_ids)
            resolved_changes.append(resolved)

        for final_code in human_review_output.final_codes:
            existing = existing_by_id.get(final_code.code_id)
            if existing is None and final_code.code_id not in structural_result_ids:
                msg = (
                    f"New final code {final_code.code_id} requires an explicit Add, "
                    "Merge, or Split codebook change."
                )
                raise ValueError(msg)
            if (
                existing is not None
                and self._structural_code_signature(existing)
                != self._structural_code_signature(final_code)
                and final_code.code_id not in structural_result_ids | structural_target_ids
            ):
                msg = (
                    f"Structural edit to existing code {final_code.code_id} requires an "
                    "explicit Refine, Rename, Merge, or Split codebook change."
                )
                raise ValueError(msg)
        return resolved_changes

    def _resolve_result_ids(
        self,
        change: CodebookChangeState,
        *,
        final_by_name: dict[str, str],
        existing_by_name: dict[str, str],
    ) -> list[str]:
        result_ids = self._unique_ids(change.resulting_code_ids)
        result_names = change.metadata.get("resulting_code_names", [])
        if not isinstance(result_names, list):
            msg = "Codebook change metadata.resulting_code_names must be a list when present."
            raise ValueError(msg)
        for name in result_names:
            if not isinstance(name, str):
                msg = "Codebook change result names must be strings."
                raise ValueError(msg)
            resolved_id = final_by_name.get(name.casefold()) or existing_by_name.get(name.casefold())
            if resolved_id is None:
                msg = f"Cannot resolve resulting code name {name!r} to a final or existing code."
                raise ValueError(msg)
            if resolved_id not in result_ids:
                result_ids.append(resolved_id)
        return result_ids

    def _validate_change_shape(
        self,
        *,
        change: CodebookChangeState,
        existing_by_id: dict[str, CodeState],
        final_by_id: dict[str, CodeState],
    ) -> None:
        targets = set(change.target_code_ids)
        results = set(change.resulting_code_ids)
        unknown_targets = targets - set(existing_by_id)
        if unknown_targets:
            msg = f"Codebook change references unknown target code ids: {sorted(unknown_targets)}."
            raise ValueError(msg)

        if change.action == "no_change":
            if targets or results:
                msg = "No change cannot name target or resulting code ids."
                raise ValueError(msg)
            return
        if not change.rationale.strip():
            msg = f"Codebook change {change.action} requires a rationale."
            raise ValueError(msg)
        if change.action == "add":
            if targets or not results:
                msg = "Add requires no targets and at least one resulting code id."
                raise ValueError(msg)
            if results & set(existing_by_id):
                msg = "Add cannot reuse an existing code id. Use Refine, Rename, Merge, or Split."
                raise ValueError(msg)
            self._require_final_definitions(results, final_by_id, action="Add")
            return
        if change.action == "add_parent":
            if len(targets) < 2 or len(results) != 1:
                msg = "Add parent requires at least two child targets and exactly one new parent code."
                raise ValueError(msg)
            inactive_targets = sorted(
                target_id
                for target_id in targets
                if existing_by_id[target_id].status != "active"
            )
            if inactive_targets:
                msg = (
                    "Add parent can only attach active child codes; inactive targets: "
                    f"{inactive_targets}."
                )
                raise ValueError(msg)
            result_id = next(iter(results))
            if result_id in existing_by_id:
                msg = "Add parent requires a new parent code id. Use Refine or Rename for an existing code."
                raise ValueError(msg)
            self._require_final_definitions(results, final_by_id, action="Add parent")
            return
        if change.action in {"refine", "rename"}:
            if len(targets) != 1:
                msg = f"{change.action.title()} requires exactly one existing target code."
                raise ValueError(msg)
            if results and results != targets:
                msg = f"{change.action.title()} keeps the same code id; omit results or repeat its target id."
                raise ValueError(msg)
            target_id = next(iter(targets))
            if target_id not in final_by_id:
                msg = f"{change.action.title()} requires the updated target code definition in final_codes."
                raise ValueError(msg)
            return
        if change.action == "retire":
            if len(targets) != 1 or (results and results != targets):
                msg = "Retire requires exactly one existing target code and keeps its id."
                raise ValueError(msg)
            target_id = next(iter(targets))
            if target_id not in final_by_id:
                msg = "Retire requires the retired code definition in final_codes."
                raise ValueError(msg)
            if final_by_id[target_id].status != "retired":
                msg = "Retire requires the resulting code status to be 'retired'."
                raise ValueError(msg)
            return
        if change.action == "merge":
            if len(targets) < 2 or len(results) != 1:
                msg = "Merge requires at least two targets and exactly one resulting code id."
                raise ValueError(msg)
            result_id = next(iter(results))
            if result_id not in existing_by_id:
                self._require_final_definitions(results, final_by_id, action="Merge")
            return
        if change.action == "split":
            if len(targets) != 1 or len(results) < 2 or results & targets:
                msg = "Split requires one target and at least two distinct resulting code ids."
                raise ValueError(msg)
            self._require_final_definitions(results, final_by_id, action="Split")
            return
        msg = f"Unsupported codebook change action: {change.action}."
        raise ValueError(msg)

    def _require_final_definitions(
        self,
        code_ids: set[str],
        final_by_id: dict[str, CodeState],
        *,
        action: str,
    ) -> None:
        missing = code_ids - set(final_by_id)
        if missing:
            msg = f"{action} requires final code definitions for: {sorted(missing)}."
            raise ValueError(msg)

    def _apply_codebook_change(
        self,
        codes: list[CodeState],
        change: CodebookChangeState,
    ) -> list[CodeState]:
        """Apply statuses implied by merge/split while preserving code order."""

        by_id = {code.code_id: code for code in codes}
        if change.action == "merge":
            result_id = change.resulting_code_ids[0]
            for target_id in change.target_code_ids:
                if target_id != result_id:
                    target = by_id[target_id]
                    by_id[target_id] = replace(
                        target,
                        status="merged",
                        metadata={**target.metadata, "merged_into": result_id},
                    )
            result = by_id[result_id]
            by_id[result_id] = replace(result, status="active")
        elif change.action == "split":
            target_id = change.target_code_ids[0]
            target = by_id[target_id]
            by_id[target_id] = replace(
                target,
                status="split",
                metadata={**target.metadata, "split_into": list(change.resulting_code_ids)},
            )
            for result_id in change.resulting_code_ids:
                by_id[result_id] = replace(by_id[result_id], status="active")
        elif change.action == "add":
            for result_id in change.resulting_code_ids:
                by_id[result_id] = replace(by_id[result_id], status="active")
        elif change.action == "retire":
            target_id = change.target_code_ids[0]
            by_id[target_id] = replace(by_id[target_id], status="retired")
        elif change.action == "add_parent":
            parent_id = change.resulting_code_ids[0]
            for target_id in change.target_code_ids:
                by_id[target_id] = replace(by_id[target_id], parent_code_id=parent_id)
            by_id[parent_id] = replace(by_id[parent_id], status="active")
        return [by_id[code.code_id] for code in codes]

    def _unique_ids(self, code_ids: list[str]) -> list[str]:
        seen: set[str] = set()
        unique: list[str] = []
        for code_id in code_ids:
            if not code_id or code_id in seen:
                continue
            seen.add(code_id)
            unique.append(code_id)
        return unique

    def _merge_final_codes(
        self,
        existing_codes: list[CodeState],
        final_codes: list[CodeState],
    ) -> list[CodeState]:
        by_id = {code.code_id: code for code in existing_codes}
        changed = False
        for code in final_codes:
            if by_id.get(code.code_id) != code:
                by_id[code.code_id] = code
                changed = True
        if not changed:
            return list(existing_codes)
        existing_order = [code.code_id for code in existing_codes]
        new_order = [code.code_id for code in final_codes if code.code_id not in existing_order]
        ordered_ids = existing_order + new_order
        return [by_id[code_id] for code_id in ordered_ids]

    def _codebook_structure_changed(
        self,
        existing_codes: list[CodeState],
        next_codes: list[CodeState],
    ) -> bool:
        if len(existing_codes) != len(next_codes):
            return True
        for existing_code, next_code in zip(existing_codes, next_codes):
            if existing_code.code_id != next_code.code_id:
                return True
            if self._structural_code_signature(existing_code) != self._structural_code_signature(
                next_code
            ):
                return True
        return False

    def _structural_code_signature(self, code: CodeState) -> tuple[object, ...]:
        return (
            code.code_id,
            code.name,
            code.definition,
            tuple(code.inclusion_criteria),
            tuple(code.exclusion_criteria),
            code.parent_code_id,
            code.status,
            tuple(code.notes),
            json.dumps(code.metadata, ensure_ascii=False, sort_keys=True, default=str),
        )
