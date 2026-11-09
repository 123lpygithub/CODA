"""Stateful service layer shared by the FastAPI app and its tests.

The service intentionally contains no HTTP concepts. It supports resumable
single-case reviews and shared-snapshot multi-case comparison batches while
the API layer only translates requests and responses.
"""

from __future__ import annotations

import hashlib
import json
import inspect
import math
import os
import shutil
from copy import deepcopy
from datetime import datetime, timezone
from dataclasses import asdict, replace
from pathlib import Path
from threading import Event, RLock
from typing import Callable

from adapters import (
    Defects4CodeLLMSemanticAdapter,
    Defects4CodeLLMSyntacticAdapter,
    MLSATD23ShadesAdapter,
    PersonalDataProtectionGitHubAdapter,
)
from adapters.base import ArtifactRecord, DatasetAdapter
from coda.agents import (
    ComparisonLLMAgent,
    ContextLLMAgent,
    InductionLLMAgent,
    ValidationLLMAgent,
    build_initial_open_coder,
    build_open_coder,
)
from coda.completion import completion_issues, decision_fingerprint
from coda.batching import prepare_batch_case
from coda.agents.common import build_evidence_item
from coda.contracts import EvidenceItem, HumanReviewOutput
from coda.bootstrap import (
    BootstrapCancelledError,
    BootstrapConfig,
    BootstrapResult,
    EvidenceFirstBootstrap,
    bootstrap_sample_size,
)
from coda.full_runner import (
    FullRunPaths,
    advance_completed_batches,
    pending_artifacts_for_batch,
    persist_artifact_completion,
    persist_final_codebook,
)
from coda.llm import LLMModelConfig, load_chat_backend, web_model_configurations
from coda.manifest import build_run_manifest, write_run_manifest
from coda.orchestrator import CODAOrchestrator, PreparedArtifactReview
from coda.evaluation import EvaluationError, export_held_out_materials
from coda.persistence import (
    append_jsonl,
    load_run_state_checkpoint,
    persist_codebook_snapshot,
    save_run_state_checkpoint,
    serialize_codebook_state,
    serialize_run_state_checkpoint,
)
from coda.state import (
    ArtifactBatchState,
    CodeState,
    CodebookChangeState,
    CodebookState,
    CodingRecordState,
    ReviewPolicyState,
    ContextRequestState,
    RetrospectiveRecodingTask,
    RunState,
    StabilizationCheckState,
    StageReviewState,
    UnresolvedCaseState,
    ExperimentVariant,
)
from coda.stage_checkpoints import StageCheckpointStore
from coda.study import load_study_manifest, select_study_artifacts, study_binding
from coda.splitting import (
    default_held_out_size,
    deterministic_held_out_split,
    split_group_id,
)
from uuid import uuid4

AdapterFactory = Callable[[], DatasetAdapter]
OrchestratorFactory = Callable[[], CODAOrchestrator]
BootstrapFactory = Callable[[CODAOrchestrator], EvidenceFirstBootstrap]


class WebWorkflowError(RuntimeError):
    """Raised when an operation violates the explicit review workflow."""


class WebRunNotFoundError(WebWorkflowError):
    """Raised when a requested persisted run does not exist."""


_ADAPTER_FACTORIES: dict[str, AdapterFactory] = {
    "ml_satd_23_shades": MLSATD23ShadesAdapter,
    "personal_data_protection_github": PersonalDataProtectionGitHubAdapter,
    "llm_code_error_semantic": Defects4CodeLLMSemanticAdapter,
}

_SPLIT_FAMILIES = {
    "llm_code_error_semantic": "llm_code_error",
    "llm_code_error_syntactic": "llm_code_error",
}


def _unavailable_cli_reviewer(_: object) -> HumanReviewOutput:
    raise RuntimeError("Web runs must submit human review through the web service.")


def build_default_web_orchestrator() -> CODAOrchestrator:
    """Build the real LLM pipeline used by the local web workbench."""

    configs = web_model_configurations()
    stage_config = configs["context_comparison_iterative_validation"]
    coder_a_config = configs["coder_a"]
    coder_b_config = configs["coder_b"]
    backend = load_chat_backend(stage_config)
    return CODAOrchestrator(
        context_agent=ContextLLMAgent(model_config=stage_config, backend=backend),
        coder_agents=[
            (
                "coder-a",
                build_open_coder(model_config=coder_a_config, backend=backend),
            ),
            (
                "coder-b",
                build_open_coder(model_config=coder_b_config, backend=backend),
            ),
        ],
        comparison_agent=ComparisonLLMAgent(
            model_config=stage_config,
            backend=backend,
        ),
        validation_agent=ValidationLLMAgent(
            model_config=stage_config,
            backend=backend,
        ),
        human_review_agent=_unavailable_cli_reviewer,
        # A web run must keep the evidence packet boundary alive when an
        # individual provider response is unusable, so the case can enter
        # the explicit R6 review path instead of losing the run.
        failure_policy="route_to_r6",
    )


def build_default_web_bootstrap(orchestrator: CODAOrchestrator) -> EvidenceFirstBootstrap:
    """Build codebook-free initial coders followed by category induction."""

    configs = web_model_configurations()
    induction_config = configs["induction_and_bootstrap_validation"]
    initial_coder_a_config = configs["coder_a"]
    initial_coder_b_config = configs["coder_b"]
    backend = load_chat_backend(induction_config)
    return EvidenceFirstBootstrap(
        model_config=induction_config,
        backend=backend,
        context_agent=orchestrator.prepare_context,
        initial_coder_agents=[
            (
                "initial-coder-a",
                build_initial_open_coder(
                    model_config=initial_coder_a_config,
                    backend=backend,
                ),
            ),
            (
                "initial-coder-b",
                build_initial_open_coder(
                    model_config=initial_coder_b_config,
                    backend=backend,
                ),
            ),
        ],
        induction_agent=InductionLLMAgent(
            model_config=induction_config,
            backend=backend,
        ),
        validation_agent=ValidationLLMAgent(
            model_config=induction_config,
            backend=backend,
        ),
        config=BootstrapConfig.from_env(),
    )


class CodaWebService:
    """Run lifecycle for a single-process local CODA web server."""

    def __init__(
        self,
        *,
        runs_root: str | Path = "runs/web",
        adapter_factories: dict[str, AdapterFactory] | None = None,
        orchestrator_factory: OrchestratorFactory | None = None,
        bootstrap_factory: BootstrapFactory | None = None,
    ) -> None:
        self._runs_root = Path(runs_root)
        self._adapter_factories = dict(adapter_factories or _ADAPTER_FACTORIES)
        self._orchestrator_factory = orchestrator_factory or build_default_web_orchestrator
        self._bootstrap_factory = bootstrap_factory or build_default_web_bootstrap
        self._active_states: dict[str, RunState] = {}
        self._prepared_reviews: dict[str, PreparedArtifactReview] = {}
        self._prepared_retrospective_reviews: dict[
            tuple[str, str], PreparedArtifactReview
        ] = {}
        self._orchestrators: dict[str, CODAOrchestrator] = {}
        self._output_languages: dict[str, str] = {}
        self._state_lock = RLock()
        self._initializing_runs: set[str] = set()
        self._initialization_cancel_events: dict[str, Event] = {}
        self._processing_runs: set[str] = set()
        self._backend_instance_id = uuid4().hex

    def runtime_info(self) -> dict[str, object]:
        configs = web_model_configurations()
        config = configs["context_comparison_iterative_validation"]
        return {
            "backend_instance_id": self._backend_instance_id,
            "api_key_available": all(value.api_key_available() for value in configs.values()),
            "provider": config.provider,
            "base_url": config.resolved_base_url(),
            "timeout_seconds": config.timeout_seconds,
            "retry_timeouts_forever": config.retry_timeouts_forever,
            "coder_models": [configs["coder_a"].model, configs["coder_b"].model],
            "roles": {role: {
                "provider": value.provider, "model": value.model,
                "base_url": value.resolved_base_url(),
                "api_key_env": value.resolved_api_key_env(),
                "api_key_available": value.api_key_available(),
            } for role, value in configs.items()},
        }

    def execution_status(self, run_id: str) -> dict[str, object]:
        with self._state_lock:
            state = self._load_run_state(run_id)
            events = state.metadata.get("events", [])
            return {
                "run": self.run_summary(run_id),
                "backend_instance_id": self._backend_instance_id,
                "initialization_active": run_id in self._initializing_runs,
                "processing_active": run_id in self._processing_runs,
                "observed_at_utc": datetime.now(timezone.utc).isoformat(),
                "last_event": events[-1] if events else None,
            }

    @staticmethod
    def _record_event(run_state: RunState, event: str, **details: object) -> None:
        """Append a UTC lifecycle event to the persisted run audit trail."""

        events = run_state.metadata.setdefault("events", [])
        if not isinstance(events, list):
            events = []
            run_state.metadata["events"] = events
        events.append(
            {
                "event": event,
                "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                **details,
            }
        )

    def available_datasets(self) -> list[dict[str, object]]:
        """Return dataset choices without exposing their hidden labels."""

        datasets: list[dict[str, object]] = []
        for dataset_name, factory in sorted(self._adapter_factories.items()):
            adapter = factory()
            metadata = adapter.load_dataset_metadata()
            solution_view = isinstance(adapter, (Defects4CodeLLMSemanticAdapter, Defects4CodeLLMSyntacticAdapter))
            datasets.append(
                {
                    "dataset_name": dataset_name,
                    "display_name": metadata.display_name,
                    "target_record_count": len(list(adapter.iter_solution_artifacts())) if solution_view else metadata.target_record_count,
                    "artifact_unit": "One distinct generated solution, grouped by task, model and incorrect code." if solution_view else metadata.artifact_unit,
                    "task_family": metadata.task_family,
                    "data_available": metadata.data_available,
                    "availability_message": metadata.availability_message,
                }
            )
        return datasets

    def create_run(
        self,
        *,
        dataset_name: str,
        artifact_limit: int | None = None,
        review_mode: str = "automatic",
        review_budget_minutes: int | None = None,
        experiment_variant: ExperimentVariant = "standard",
        held_out_enabled: bool = False,
        held_out_size: int | None = None,
        study_manifest_path: str | None = None,
        study_phase: str | None = None,
        participant_id: str | None = None,
        replicate_index: int | None = None,
        comparison_block_id: str | None = None,
        iterative_batch_size: int = 1,
    ) -> dict[str, object]:
        if type(iterative_batch_size) is not int or iterative_batch_size < 1:
            raise WebWorkflowError("iterative_batch_size must be a positive integer.")
        if participant_id is not None and not participant_id.strip():
            raise WebWorkflowError("participant_id must not be blank.")
        if replicate_index is not None and (type(replicate_index) is not int or replicate_index not in {1, 2}):
            raise WebWorkflowError("replicate_index must be 1 or 2.")
        if review_mode == "automatic" and participant_id is not None:
            raise WebWorkflowError("Automatic runs have no human reviewer participant.")
        if review_mode not in {"automatic", "selective", "full"}:
            raise WebWorkflowError(
                "review_mode must be 'automatic', 'selective', or 'full'."
            )
        if experiment_variant not in {
            "standard",
            "freeze_after_initialization",
            "without_retrospective_recoding",
        }:
            raise WebWorkflowError("Invalid experiment_variant.")
        adapter = self._adapter_for(dataset_name)
        metadata = adapter.load_dataset_metadata()
        artifacts = list(adapter.iter_artifacts())
        study_manifest = None
        binding = None
        if (study_manifest_path is None) != (study_phase is None):
            raise WebWorkflowError("Provide both study_manifest_path and study_phase.")
        if study_manifest_path is None and isinstance(adapter, (Defects4CodeLLMSemanticAdapter, Defects4CodeLLMSyntacticAdapter)):
            artifacts = list(adapter.iter_solution_artifacts())
        if study_manifest_path is not None:
            if held_out_enabled:
                raise WebWorkflowError(
                    "A matched study run uses its entire frozen phase corpus; "
                    "reserve supplementary held-out material in a separate run."
                )
            study_manifest = load_study_manifest(study_manifest_path)
            artifacts = select_study_artifacts(study_manifest, dataset_name, artifacts, str(study_phase))
            binding = study_binding(study_manifest, dataset_name, str(study_phase))
            if artifact_limit is not None and artifact_limit != len(artifacts):
                raise WebWorkflowError("artifact_limit cannot change the frozen study phase corpus.")
        elif artifact_limit is not None:
            if artifact_limit <= 0:
                raise WebWorkflowError("artifact_limit must be a positive integer.")
            split_family = self._split_family(dataset_name)
            artifacts = sorted(
                artifacts,
                key=lambda artifact: hashlib.sha256(
                    f"20260907:{split_family}:{artifact.artifact_id}".encode("utf-8")
                ).hexdigest(),
            )[:artifact_limit]
        if not artifacts:
            raise WebWorkflowError(f"Dataset {dataset_name} has no artifacts to run.")

        # Task creation deliberately performs no model work. The researcher
        # explicitly starts the fixed bootstrap in a separate, persisted step.
        # Held-out is an explicit evaluation-only partition. It is never
        # included in the bootstrap or iterative coding queue.
        if held_out_enabled:
            requested_held_out_size = (
                default_held_out_size(len(artifacts))
                if held_out_size is None
                else held_out_size
            )
            if requested_held_out_size < 1:
                raise WebWorkflowError(
                    "Held-out evaluation requires at least three selected artifacts."
                )
            try:
                coding_artifacts, held_out_artifacts, group_ids = (
                    deterministic_held_out_split(
                        artifacts,
                        dataset_name=dataset_name,
                        split_family=self._split_family(dataset_name),
                        held_out_target=requested_held_out_size,
                    )
                )
            except ValueError as error:
                raise WebWorkflowError(str(error)) from error
        else:
            coding_artifacts = artifacts
            held_out_artifacts = []
            group_ids = {
                artifact.artifact_id: split_group_id(dataset_name, artifact)
                for artifact in artifacts
            }
        coding_batch = ArtifactBatchState(
            batch_id=f"batch-{dataset_name}-0",
            dataset_name=dataset_name,
            batch_index=0,
            split_name="coding_pool",
            artifacts=coding_artifacts,
            group_ids={artifact.artifact_id: group_ids[artifact.artifact_id] for artifact in coding_artifacts},
            sampling_note="Deterministic, group-preserving codebook-construction pool.",
        )
        run_state = RunState.initialize(
            metadata,
            coding_batches=[coding_batch],
            held_out_batches=(
                [
                    ArtifactBatchState(
                        batch_id=f"held-out-{dataset_name}-0",
                        dataset_name=dataset_name,
                        batch_index=0,
                        split_name="held_out_pool",
                        artifacts=held_out_artifacts,
                        group_ids={
                            artifact.artifact_id: group_ids[artifact.artifact_id]
                            for artifact in held_out_artifacts
                        },
                        sampling_note=(
                            "Held-out evaluation pool; isolated from codebook construction "
                            "and iterative coding."
                        ),
                        metadata={"evaluation_only": True},
                    )
                ]
                if held_out_artifacts
                else []
            ),
        )
        run_state.review_policy = ReviewPolicyState(
            setting=review_mode,  # type: ignore[arg-type]
            review_budget_minutes=review_budget_minutes,
        )
        run_state.metadata["bootstrap"] = self._pending_bootstrap_metadata(len(coding_artifacts))
        run_state.metadata["review_mode"] = review_mode
        run_state.metadata["iterative_batch_protocol"] = {
            "batch_size": iterative_batch_size,
            "initial_comparison": "shared_snapshot",
            "reconciliation": "comparison_before_validation",
            "commit_policy": "accepted_decisions_with_stale_proposal_recheck",
        }
        run_state.metadata["study_execution"] = {
            "participant_id": participant_id.strip() if participant_id else None,
            "replicate_index": replicate_index,
            "comparison_block_id": comparison_block_id,
        }
        # Interactive workbench runs are created with Selective as a provisional
        # setting and choose coverage at Initial Review. Explicit Automatic API
        # runs retain their protocol-assigned routing and do not expose a selector.
        run_state.metadata["review_setting_user_selectable"] = review_mode != "automatic" and binding is None
        if binding is not None:
            run_state.metadata["study_materials"] = binding
        run_state.metadata["experiment_protocol"] = {
            "variant": experiment_variant,
            "codebook_refinement_enabled": experiment_variant != "freeze_after_initialization",
            "retrospective_recoding_enabled": experiment_variant != "without_retrospective_recoding",
            "held_out_enabled": bool(held_out_artifacts),
            "held_out_protocol": (
                "frozen_codebook_application_after_final_review"
                if held_out_artifacts
                else "disabled"
            ),
        }
        run_state.metadata["selected_artifact_ids"] = [
            artifact.artifact_id for artifact in coding_artifacts
        ]
        run_state.metadata["all_selected_artifact_ids"] = [artifact.artifact_id for artifact in artifacts]
        run_state.metadata["held_out_artifact_ids"] = [
            artifact.artifact_id for artifact in held_out_artifacts
        ]
        run_state.metadata["split_protocol"] = {
            "seed": 20260907,
            "split_family": self._split_family(dataset_name),
            "group_preserving": True,
            "coding_pool_size": len(coding_artifacts),
            "held_out_size": len(held_out_artifacts),
            "held_out_enabled": bool(held_out_artifacts),
            "held_out_target": (
                requested_held_out_size if held_out_artifacts else 0
            ),
            "held_out_selection_note": (
                "Whole source groups are assigned deterministically; the realized "
                "count may be below the requested target."
                if held_out_artifacts
                else "No held-out pool was requested."
            ),
            "experiment_variant": experiment_variant,
        }
        run_state.metadata["batch_commit_policy"] = "one_artifact_snapshot_then_commit"
        run_state.metadata["review_sampling_protocol"] = {
            "setting": review_mode,
            "criterion_rule": "Any applicable R1-R6 criterion routes to review.",
            "unflagged_audit_rate": run_state.review_policy.random_audit_rate,
            "effective_unflagged_audit_rate": (
                run_state.review_policy.random_audit_rate if iterative_batch_size > 1 else 0.0
            ),
            "single_artifact_batches_skip_random_audit": True,
            "random_seed": run_state.review_policy.random_seed,
            "sampling_block_size": 10,
            "selection_rule": (
                "one deterministic random position per cumulative window of ten "
                "eligible unflagged case decisions; current and retrospective streams "
                "are separate; incomplete tail windows are not rounded up"
            ),
            "confidence_used_as_threshold": False,
        }
        run_state.metadata["output_language"] = "en"
        run_state.metadata["events"] = []
        self._record_event(
            run_state,
            "run_created",
            artifact_count=len(artifacts),
            coding_pool_count=len(coding_artifacts),
            held_out_count=len(held_out_artifacts),
            review_setting=review_mode,
            experiment_variant=experiment_variant,
        )
        paths = self._paths_for(run_state.run_id)
        if study_manifest is not None:
            self._write_json(paths.run_dir / "study_manifest.json", study_manifest)
        self._write_json(
            paths.run_dir / "split_manifest.json",
            {
                "dataset_name": dataset_name,
                "seed": 20260907,
                "split_family": self._split_family(dataset_name),
                "protocol": (
                    "coding_pool_plus_held_out_evaluation"
                    if held_out_artifacts
                    else "single_coding_pool"
                ),
                "assignments": [
                    {
                        "artifact_id": artifact.artifact_id,
                        "split_name": "coding_pool",
                        "group_id": group_ids[artifact.artifact_id],
                    }
                    for artifact in coding_artifacts
                ]
                + [
                    {
                        "artifact_id": artifact.artifact_id,
                        "split_name": "held_out_pool",
                        "group_id": group_ids[artifact.artifact_id],
                    }
                    for artifact in held_out_artifacts
                ],
            },
        )
        model_configurations = {
            role: asdict(config) for role, config in web_model_configurations().items()
        }
        write_run_manifest(
            paths.run_manifest_path,
            build_run_manifest(
                run_state,
                coding_artifacts,
                held_out_artifacts=held_out_artifacts,
                project_root=Path(__file__).resolve().parents[2],
                bootstrap_config=BootstrapConfig.from_env(),
                model_configurations=model_configurations,
            ),
        )
        save_run_state_checkpoint(run_state, paths.checkpoint_path)
        persist_codebook_snapshot(run_state, paths.codebook_snapshot_dir)
        with self._state_lock:
            self._active_states[run_state.run_id] = run_state
            self._output_languages[run_state.run_id] = "en"
        return self.run_summary(run_state.run_id)

    @staticmethod
    def _split_family(dataset_name: str) -> str:
        """Return the shared split identity for alternate views of one corpus."""

        return _SPLIT_FAMILIES.get(dataset_name, dataset_name)

    def process_automatic(
        self,
        run_id: str,
        *,
        language: str = "en",
        max_artifacts: int | None = None,
    ) -> dict[str, object]:
        """Serialize automatic processing requests for one run.

        A single researcher can still use multiple browser tabs, refreshes, or
        repeated clicks. Only one request may own the run's LLM execution
        queue at a time; otherwise two requests could process the same pending
        artifact and append conflicting records.
        """

        with self._state_lock:
            if run_id in self._processing_runs:
                raise WebWorkflowError(
                    "This run is already processing an artifact. Wait for the current request to finish."
                )
            self._processing_runs.add(run_id)
        try:
            return self._process_automatic_impl(
                run_id,
                language=language,
                max_artifacts=max_artifacts,
            )
        finally:
            with self._state_lock:
                self._processing_runs.discard(run_id)

    def _process_automatic_impl(
        self,
        run_id: str,
        *,
        language: str = "en",
        max_artifacts: int | None = None,
    ) -> dict[str, object]:
        """Run automatic passes until review is required or a request limit is reached."""

        if max_artifacts is not None and max_artifacts < 1:
            raise ValueError("max_artifacts must be positive when provided.")

        run_state = self._load_run_state(run_id)
        if run_state.review_policy.setting == "full":
            raise WebWorkflowError(
                "Automatic processing is available only for Automatic or Selective runs."
            )
        if self._bootstrap_is_pending(run_state):
            raise WebWorkflowError("Initialize this task before automatic processing.")
        if run_state.status == "awaiting_initial_review":
            raise WebWorkflowError("Complete the initial codebook review before automatic processing.")
        if run_state.status == "awaiting_final_review":
            raise WebWorkflowError("This run is waiting for final review.")
        if run_state.status == "awaiting_context":
            raise WebWorkflowError(
                "Resolve or cancel the pending context request before automatic processing."
            )
        if run_state.status == "awaiting_human_review":
            raise WebWorkflowError(
                "The current artifact is waiting for human review. Submit it before automatic processing."
            )
        if run_state.status in {
            "completed", "stabilized", "completed_with_unresolved", "resource_limited"
        }:
            raise WebWorkflowError("This run has no remaining artifacts to process.")
        if language not in {"en", "zh"}:
            raise WebWorkflowError("language must be 'en' or 'zh'.")

        processed = 0
        automatic_ids: list[str] = []
        orchestrator = self._orchestrator_for(run_id)
        orchestrator.set_output_language(language)
        self._output_languages[run_id] = language
        run_state.metadata["output_language"] = language
        self._record_event(run_state, "iterative_started")
        save_run_state_checkpoint(run_state, self._paths_for(run_id).checkpoint_path)

        while True:
            if run_state.status == "awaiting_next_artifact":
                advance_completed_batches(run_state)
                if run_state.status == "completed":
                    self._finish_iterative_coding(run_state)
                    break
                run_state.status = "in_progress"
            batch = run_state.current_batch()
            if batch is None:
                run_state.status = "completed"
                self._finish_iterative_coding(run_state)
                break
            pending = pending_artifacts_for_batch(batch, run_state)
            if not pending:
                advance_completed_batches(run_state)
                continue
            artifact = pending[0]
            self._record_event(
                run_state,
                "artifact_processing_started",
                artifact_id=artifact.artifact_id,
            )
            save_run_state_checkpoint(run_state, self._paths_for(run_id).checkpoint_path)
            stage_store = self._stage_store(
                run_id,
                orchestrator,
                run_state,
                artifact,
            )
            prepared = self._prepare_iterative_case(run_state, orchestrator, batch, artifact,
                                                   stage_store=stage_store)
            # Persist the sampling decision before applying the result so a
            # restart cannot count the same eligible decision twice.
            save_run_state_checkpoint(run_state, self._paths_for(run_id).checkpoint_path)
            automatic_output = orchestrator.automatic_review_if_safe(run_state, prepared)
            if automatic_output is None:
                if self._review_budget_exhausted(run_state):
                    automatic_output = self._budget_exhausted_output(prepared)
                else:
                    self._prepared_reviews[run_id] = prepared
                    run_state.metadata["awaiting_human_review"] = {
                        "artifact_id": prepared.artifact_id,
                        "codebook_version": prepared.codebook_version,
                        "routing_decision": asdict(
                            prepared.evidence_packet.routing_decision
                        )
                        if prepared.evidence_packet.routing_decision is not None
                        else None,
                    }
                    self._record_event(
                        run_state,
                        "artifact_waiting_for_human_review",
                        artifact_id=prepared.artifact_id,
                        risk_signals=(
                            list(prepared.evidence_packet.routing_decision.risk_signals)
                            if prepared.evidence_packet.routing_decision is not None
                            else []
                        ),
                    )
                    self._record_event(
                        run_state,
                        "iterative_paused",
                        status="awaiting_human_review",
                        artifact_id=prepared.artifact_id,
                    )
                    # The in-memory packet can be reconstructed from stage
                    # checkpoints after a restart, but the waiting state and
                    # routing provenance must survive the request boundary.
                    save_run_state_checkpoint(
                        run_state, self._paths_for(run_id).checkpoint_path
                    )
                    persist_codebook_snapshot(
                        run_state, self._paths_for(run_id).codebook_snapshot_dir
                    )
                    return {
                        "run": self.run_summary(run_id),
                        "current": self.current_artifact(run_id),
                        "auto_processed": processed,
                        "auto_processed_artifact_ids": automatic_ids,
                        "stopped_for_human": True,
                    }
            result = orchestrator.submit_prepared_review(
                run_state,
                prepared_review=prepared,
                human_review_output=automatic_output,
            )
            run_state.status = "awaiting_next_artifact"
            self._update_batch_progress(run_state)
            persist_artifact_completion(
                run_state=run_state,
                batch=batch,
                result=result,
                paths=self._paths_for(run_id),
            )
            self._record_stabilization_check(run_state)
            processed += 1
            automatic_ids.append(artifact.artifact_id)
            self._prepared_reviews.pop(run_id, None)
            run_state.metadata.pop("awaiting_human_review", None)
            stage_store.clear()
            self._record_event(
                run_state,
                "artifact_processing_finished",
                artifact_id=artifact.artifact_id,
                decision=result.human_review_output.decision,
                human_reviewed=False,
            )
            if max_artifacts is not None and processed >= max_artifacts:
                break

        save_run_state_checkpoint(run_state, self._paths_for(run_id).checkpoint_path)
        self._record_event(run_state, "iterative_finished", status=run_state.status)
        save_run_state_checkpoint(run_state, self._paths_for(run_id).checkpoint_path)
        return {
            "run": self.run_summary(run_id),
            "current": self.current_artifact(run_id),
            "auto_processed": processed,
            "auto_processed_artifact_ids": automatic_ids,
            "stopped_for_human": False,
        }

    def initialize_run(
        self, run_id: str, *, language: str = "en",
    ) -> dict[str, object]:
        """Generate provisional B1 from empty B0 after explicit researcher action."""

        if language not in {"en", "zh"}:
            raise WebWorkflowError("language must be 'en' or 'zh'.")

        with self._state_lock:
            run_state = self._load_run_state(run_id)
            bootstrap_metadata = dict(run_state.metadata.get("bootstrap", {}))
            bootstrap_status = str(bootstrap_metadata.get("status", "not_run"))
            if run_id in self._initializing_runs:
                raise WebWorkflowError("This task is already initializing. Please wait for it to finish.")
            if bootstrap_status in {"running", "cancelling"}:
                bootstrap_status = "interrupted"
                bootstrap_metadata = self._interrupted_bootstrap_metadata(bootstrap_metadata)
                run_state.metadata["bootstrap"] = bootstrap_metadata
            if bootstrap_status not in {"not_run", "failed", "cancelled", "interrupted"}:
                raise WebWorkflowError("This task has already completed its initialization step.")
            if run_state.history.coding_records or run_id in self._prepared_reviews:
                raise WebWorkflowError("Initialization must finish before any artifact review begins.")

            batch = run_state.current_batch()
            if batch is None:
                raise WebWorkflowError("This task has no artifacts available for initialization.")
            artifacts = list(batch.artifacts)
            if not artifacts:
                raise WebWorkflowError("This task has no artifacts available for initialization.")

            orchestrator = self._orchestrator_for(run_id)
            orchestrator.set_output_language(language)
            bootstrap = self._bootstrap_factory(orchestrator)
            self._bind_agent_protocol(run_state, "bootstrap", [
                ("induction", getattr(bootstrap, "_induction_agent", None)),
                ("validation", getattr(bootstrap, "_validation_agent", None)),
                *getattr(bootstrap, "_initial_coder_agents", []),
            ])
            fixed_initial_ids = run_state.metadata.get("sensitivity_protocol", {}).get("initialization_artifact_ids", [])
            if fixed_initial_ids and hasattr(bootstrap, "config"):
                bootstrap.config = replace(bootstrap.config, fixed_artifact_ids=tuple(fixed_initial_ids))
            sink = getattr(orchestrator, "trace_sink", None)
            if sink is not None and hasattr(bootstrap, "set_execution_trace_sink"):
                bootstrap.set_execution_trace_sink(sink)
            set_bootstrap_language = getattr(bootstrap, "set_output_language", None)
            if set_bootstrap_language is not None:
                set_bootstrap_language(language)
            paths = self._paths_for(run_id)
            cancel_event = Event()
            self._initializing_runs.add(run_id)
            self._initialization_cancel_events[run_id] = cancel_event
            self._output_languages[run_id] = language
            run_state.metadata["output_language"] = language
            run_state.metadata["bootstrap"] = self._running_bootstrap_metadata(
                bootstrap_metadata,
                population_size=len(artifacts),
            )
            self._record_event(run_state, "bootstrap_started", artifact_count=len(artifacts))
            save_run_state_checkpoint(run_state, paths.checkpoint_path)

        def progress_callback(progress: dict[str, object]) -> None:
            self._persist_bootstrap_progress(
                run_state,
                paths,
                progress,
                population_size=len(artifacts),
            )

        try:
            try:
                bootstrap_result = self._run_bootstrap(
                    bootstrap,
                    run_state,
                    artifacts,
                    progress_callback=progress_callback,
                    checkpoint_dir=paths.bootstrap_checkpoint_dir,
                    cancel_requested=cancel_event.is_set,
                )
                if cancel_event.is_set():
                    raise BootstrapCancelledError("Bootstrap initialization was cancelled.")
            except BootstrapCancelledError:
                with self._state_lock:
                    run_state.status = "not_started"
                    run_state.metadata["bootstrap"] = self._cancelled_bootstrap_metadata(
                        dict(run_state.metadata.get("bootstrap", {}))
                    )
                    self._record_event(run_state, "bootstrap_cancelled")
                    save_run_state_checkpoint(run_state, paths.checkpoint_path)
                    return self.run_summary(run_id)
            except Exception as error:
                # Keep the run recoverable if a custom Bootstrap implementation
                # raises before it can return its normal failed result.
                progress = self._failed_progress(
                    run_state,
                    error,
                    population_size=len(artifacts),
                )
                progress_callback(progress)
                bootstrap_result = BootstrapResult(
                    codebook=CodebookState.empty(
                        run_state.dataset_metadata.dataset_name,
                        notes=["LLM bootstrap failed; the run starts with an empty codebook."],
                    ),
                    artifact_ids=[],
                    group_ids={artifact.artifact_id: artifact.artifact_id for artifact in artifacts},
                    audit_warnings=["Bootstrap output was discarded and no automatic codes were used."],
                    audit_warnings_zh=["初始化结果已丢弃，未使用自动生成的编码。"],
                    protocol={"population_size": len(artifacts)},
                    progress=progress,
                    status="failed",
                    error=f"{type(error).__name__}: {error}",
                )

            with self._state_lock:
                bootstrap_ids = set(bootstrap_result.artifact_ids)
                # Failed drafts are discarded and every selected artifact remains in the
                # human queue. A successful B1 removes only the sampled artifacts.
                if bootstrap_result.status == "completed":
                    remaining_artifacts = [
                        artifact
                        for artifact in artifacts
                        if artifact.artifact_id not in bootstrap_ids
                    ]
                    self._set_iterative_micro_batches(
                        run_state,
                        remaining_artifacts,
                        group_ids=bootstrap_result.group_ids,
                    )
                    run_state.codebook = bootstrap_result.codebook
                    self._register_bootstrap_state(run_state, bootstrap_result)
                    for artifact in artifacts:
                        if artifact.artifact_id in bootstrap_ids:
                            material = run_state.metadata.setdefault("case_materials", {}).setdefault(artifact.artifact_id, {})
                            material.update(status="available", content=artifact.content,
                                            raw_fields=artifact.raw_fields,
                                            source_refs=[asdict(ref) for ref in artifact.source_refs])
                run_state.metadata["bootstrap"] = self._bootstrap_metadata(bootstrap_result)
                run_state.metadata["bootstrap"]["population_size"] = len(artifacts)
                if bootstrap_result.status == "completed":
                    run_state.status = (
                        "awaiting_initial_review"
                        if run_state.review_policy.initial_review_required
                        else "in_progress"
                    )
                self._write_bootstrap_artifacts(paths, bootstrap_result)
                self._record_event(
                    run_state,
                    "bootstrap_finished",
                    status=bootstrap_result.status,
                    sampled_artifacts=len(bootstrap_result.artifact_ids),
                )
                save_run_state_checkpoint(run_state, paths.checkpoint_path)
                persist_codebook_snapshot(run_state, paths.codebook_snapshot_dir)
                return self.run_summary(run_id)
        finally:
            with self._state_lock:
                self._initializing_runs.discard(run_id)
                self._initialization_cancel_events.pop(run_id, None)

    def cancel_initialization(self, run_id: str) -> dict[str, object]:
        """Request a checkpoint-preserving pause of an active bootstrap."""

        with self._state_lock:
            run_state = self._load_run_state(run_id)
            metadata = dict(run_state.metadata.get("bootstrap", {}))
            status = str(metadata.get("status", "not_run"))
            cancel_event = self._initialization_cancel_events.get(run_id)
            if run_id in self._initializing_runs and cancel_event is not None:
                cancel_event.set()
                metadata["status"] = "cancelling"
                progress = dict(metadata.get("progress", {}))
                progress["status"] = "cancelling"
                metadata["progress"] = progress
                run_state.metadata["bootstrap"] = metadata
                save_run_state_checkpoint(run_state, self._paths_for(run_id).checkpoint_path)
                return self.run_summary(run_id)
            if status in {"running", "cancelling", "interrupted"}:
                run_state.status = "not_started"
                run_state.metadata["bootstrap"] = self._cancelled_bootstrap_metadata(metadata)
                save_run_state_checkpoint(run_state, self._paths_for(run_id).checkpoint_path)
                return self.run_summary(run_id)
            if status == "cancelled":
                return self.run_summary(run_id)
            raise WebWorkflowError("This task is not currently initializing.")

    def stage_review_packet(
        self, run_id: str, kind: str, *, inspection: bool = False,
    ) -> dict[str, object]:
        """Return the material needed for Initial or Final Review."""

        if kind not in {"initial", "final"}:
            raise WebWorkflowError("Stage review kind must be 'initial' or 'final'.")
        run_state = self._load_run_state(run_id)
        expected = "awaiting_initial_review" if kind == "initial" else "awaiting_final_review"
        paths = self._paths_for(run_id)
        review_records = [item for item in run_state.history.stage_reviews if item.kind == kind]
        review_record = review_records[-1] if review_records else None
        if not inspection and run_state.status != expected:
            raise WebWorkflowError(f"This run is not awaiting {kind} review.")
        if inspection:
            if kind == "initial":
                if run_state.metadata.get("bootstrap", {}).get("status") != "completed":
                    raise WebWorkflowError("Initial Review is available after initialization completes.")
                snapshot_path = (
                    paths.codebook_snapshot_dir / f"codebook-v{review_record.codebook_version_after:04d}.json"
                    if review_record else paths.initial_codebook_path
                )
                snapshot = self._read_json_object(snapshot_path)
                if snapshot is None:
                    raise WebWorkflowError("The saved initial codebook is unavailable for inspection.")
                snapshot["codes"] = [CodeState(**item) for item in snapshot.get("codes", [])]
                snapshot["revisions"] = [CodebookChangeState(**item) for item in snapshot.get("revisions", [])]
                # Use a separate state value: inspecting initialization must never
                # replace the current iteration's codebook or change its checkpoint.
                recorded_policy = (
                    review_record.metadata.get("review_policy") if review_record else None
                ) or run_state.metadata.get("initial_review_policy")
                run_state = replace(
                    run_state, codebook=CodebookState(**snapshot),
                    review_policy=ReviewPolicyState(**recorded_policy) if recorded_policy else run_state.review_policy,
                )
            elif (run_state.status != expected and review_record is None
                  and run_state.status not in {"completed", "completed_with_unresolved", "stabilized"}):
                raise WebWorkflowError("Final Review is available after iterative coding finishes.")

        # Persist the review scope and deterministic audit counts that were
        # presented to the researcher. The full evidence remains in the run
        # artifacts and history, while this snapshot makes the decision
        # auditable without reconstructing the packet later.
        review_scope: dict[str, object] = {
            "checkpoint": kind,
            "purpose": (
                "Check the initial codebook and sampled assignments before iteration."
                if kind == "initial"
                else "Check corpus coverage, final categories, unresolved cases, and audit evidence."
            ),
            "required_checks": (
                [
                    "category definitions and inclusion/exclusion conditions",
                    "representative source excerpts and initial assignments",
                    "sample coverage and unsupported provisional interpretations",
                ]
                if kind == "initial"
                else [
                    "corpus manifest and unprocessed artifacts",
                    "final codebook coverage and low-frequency categories",
                    "flagged, unflagged, cross-source, and historical assignments",
                    "unresolved cases and pending retrospective reassessments",
                    "source references, revisions, and audit records",
                ]
            ),
        }
        audit_summary: dict[str, object] = {}
        experiment_protocol = run_state.metadata.get("experiment_protocol", {})
        experiment_variant = (
            str(experiment_protocol.get("variant", "standard"))
            if isinstance(experiment_protocol, dict)
            else "standard"
        )
        packet: dict[str, object] = {
            "kind": kind,
            "inspection_only": inspection,
            "review_record": asdict(review_record) if review_record else None,
            "experiment_variant": experiment_variant,
            "codebook_editing_allowed": (
                not inspection and experiment_variant != "freeze_after_initialization"
            ),
            "review_scope": review_scope,
            "research_question": asdict(run_state.research_question),
            "analysis_protocol": asdict(run_state.analysis_protocol),
            "codebook": serialize_codebook_state(run_state.codebook),
            "context_requests": [
                asdict(item)
                for item in run_state.history.context_requests
                if item.scope == kind or kind == "final"
            ],
            "completion_issues": (
                completion_issues(serialize_run_state_checkpoint(run_state))
                if kind == "final" else []
            ),
            "unresolved_cases": [
                asdict(item) for item in run_state.history.open_unresolved_cases()
            ],
            "pending_retrospective_tasks": [
                asdict(item) for item in run_state.history.pending_retrospective_tasks()
            ],
        }
        if kind == "initial":
            bootstrap = self._read_json_object(paths.bootstrap_manifest_path)
            bootstrap_ids = {
                str(item)
                for item in (bootstrap or {}).get("artifact_ids", [])
            }
            adapter = self._adapter_for(run_state.dataset_metadata.dataset_name)
            all_sampled_artifacts = [
                asdict(artifact)
                for artifact in adapter.iter_artifacts()
                if artifact.artifact_id in bootstrap_ids
            ]
            all_assignments = self._read_jsonl(paths.bootstrap_assignments_path)
            all_initial_codings = self._read_jsonl(paths.bootstrap_initial_codings_path)
            validation_outputs = (
                list((bootstrap or {}).get("validation_outputs", []))
                if isinstance(bootstrap, dict)
                else []
            )
            assignment_by_id = {
                str(row.get("artifact_id")): row
                for row in all_assignments
                if row.get("artifact_id") is not None
            }
            flagged_assignment_ids = {
                str(row.get("artifact_id"))
                for row in validation_outputs
                if isinstance(row, dict)
                and row.get("artifact_id") is not None
                and (
                    bool(row.get("human_review_required"))
                    or bool(row.get("review_criteria"))
                    or any(
                        str(signal.get("signal", "")) != "valid"
                        for signal in row.get("signals", [])
                        if isinstance(signal, dict)
                    )
                )
            }
            representative_assignment_ids: set[str] = set()
            representative_by_code: dict[str, str] = {}
            for code in run_state.codebook.active_codes():
                candidates = [
                    str(row.get("artifact_id"))
                    for row in all_assignments
                    if code.code_id in row.get("code_ids", [])
                    and row.get("artifact_id") is not None
                ]
                if candidates:
                    representative_by_code[code.code_id] = candidates[0]
                    representative_assignment_ids.add(candidates[0])
            if run_state.review_policy.setting == "full":
                # A compatibility/bootstrap implementation may not emit an
                # assignment row even though it did reserve artifacts. Full
                # Review still presents every reserved initial artifact.
                initial_review_assignment_ids = set(assignment_by_id) or set(
                    bootstrap_ids
                )
                coverage_rule = "Full Review: every initial assignment."
            elif run_state.review_policy.setting == "selective":
                initial_review_assignment_ids = (
                    representative_assignment_ids | flagged_assignment_ids
                )
                coverage_rule = (
                    "Selective Review: at least one supporting case per active code "
                    "plus every flagged initial assignment."
                )
            else:
                initial_review_assignment_ids = set()
                coverage_rule = "Automatic: no human Initial Review is required."
            sampled_ids = {
                artifact_id
                for artifact_id in initial_review_assignment_ids
                if artifact_id in bootstrap_ids
            }
            sampled_artifacts = [
                artifact
                for artifact in all_sampled_artifacts
                if str(artifact.get("artifact_id")) in sampled_ids
            ]
            packet.update(
                {
                    "bootstrap": bootstrap,
                    "audit": self._read_json_object(paths.bootstrap_audit_path),
                    "sampled_artifacts": sampled_artifacts,
                    "assignments": [
                        row
                        for row in all_assignments
                        if str(row.get("artifact_id")) in sampled_ids
                    ],
                    "initial_codings": [
                        row
                        for row in all_initial_codings
                        if str(row.get("artifact_id")) in sampled_ids
                    ],
                    "initial_review_coverage": {
                        "rule": coverage_rule,
                        "all_initial_assignment_ids": sorted(assignment_by_id),
                        "review_assignment_ids": sorted(initial_review_assignment_ids),
                        "representative_assignment_ids": sorted(
                            representative_assignment_ids
                        ),
                        "representative_assignment_by_code": representative_by_code,
                        "flagged_assignment_ids": sorted(flagged_assignment_ids),
                        "omitted_assignment_ids": sorted(
                            set(assignment_by_id) - initial_review_assignment_ids
                        ),
                    },
                    "audit_summary": {
                        "all_sampled_artifact_count": len(all_sampled_artifacts),
                        "sampled_artifact_count": len(sampled_artifacts),
                        "assignment_count": len(
                            [
                                row
                                for row in all_assignments
                                if str(row.get("artifact_id")) in sampled_ids
                            ]
                        ),
                        "all_assignment_count": len(all_assignments),
                        "initial_coding_count": len(
                            [
                                row
                                for row in all_initial_codings
                                if str(row.get("artifact_id")) in sampled_ids
                            ]
                        ),
                        "code_count": len(run_state.codebook.active_codes()),
                        "representative_evidence_required": True,
                    },
                }
            )
        else:
            bootstrap_ids = self._bootstrap_artifact_ids(run_state)
            iterative_ids = set(run_state.history.reviewed_artifact_ids()) - bootstrap_ids
            stabilization = (
                run_state.history.stabilization_checks[-1]
                if run_state.history.stabilization_checks
                else None
            )
            packet["stabilization"] = asdict(stabilization) if stabilization else None
            audit_ids = (
                set(stabilization.cross_source_audit_artifact_ids)
                if stabilization
                else set()
            )
            adapter = self._adapter_for(run_state.dataset_metadata.dataset_name)
            packet["cross_source_audit_artifacts"] = [
                asdict(artifact)
                for artifact in adapter.iter_artifacts()
                if artifact.artifact_id in audit_ids
            ]
            packet["cross_source_audit_records"] = [
                asdict(record)
                for record in run_state.history.coding_records
                if record.artifact_id in audit_ids
            ]
            final_scope = self._final_review_artifact_scope(
                run_state,
                cross_source_ids=audit_ids,
            )
            packet["final_review_coverage"] = final_scope
            packet["final_validation_audits"] = list(
                run_state.metadata.get("final_validation_audits", {}).values()
            )
            final_ids = set(final_scope["review_artifact_ids"])
            packet["final_audit_artifacts"] = [
                asdict(artifact)
                for artifact in adapter.iter_artifacts()
                if artifact.artifact_id in final_ids
            ]
            packet["final_audit_records"] = [
                asdict(record)
                for record in run_state.history.coding_records
                if record.artifact_id in final_ids
            ]
            packet["coverage"] = {
                "processed_artifacts": len(self._processed_artifact_ids(run_state)),
                "bootstrap_artifacts": len(bootstrap_ids),
                "iterative_artifacts": len(iterative_ids),
                "input_artifacts": self._input_artifact_count(run_state),
                "code_count": len(run_state.codebook.active_codes()),
                "low_frequency_codes": [
                    asdict(code)
                    for code in run_state.codebook.active_codes()
                    if len(code.representative_artifact_ids) <= 1
                ],
            }
            packet["audit_summary"] = {
                "input_artifacts": self._input_artifact_count(run_state),
                "processed_artifacts": len(self._processed_artifact_ids(run_state)),
                "unprocessed_artifact_count": max(
                    0,
                    self._input_artifact_count(run_state)
                    - len(self._processed_artifact_ids(run_state)),
                ),
                "coding_record_count": len(run_state.history.coding_records),
                "stage_review_count": len(run_state.history.stage_reviews),
                "pending_retrospective_count": len(run_state.history.pending_retrospective_tasks()),
                "open_unresolved_count": len(run_state.history.open_unresolved_cases()),
                "cross_source_audit_status": (
                    stabilization.cross_source_audit_status if stabilization else "not_run"
                ),
                "cross_source_audit_artifact_count": len(audit_ids),
                "final_review_artifact_count": len(final_ids),
                "final_review_flagged_count": len(
                    final_scope["flagged_artifact_ids"]
                ),
                "final_review_unflagged_audit_count": len(
                    final_scope["unflagged_audit_artifact_ids"]
                ),
                "low_frequency_code_count": len(packet["coverage"]["low_frequency_codes"]),
                "retrospective_recoding_suppressed_count": len(
                    run_state.metadata.get("retrospective_suppression_events", [])
                    if isinstance(
                        run_state.metadata.get("retrospective_suppression_events", []),
                        list,
                    )
                    else []
                ),
            }
        return packet

    def _review_setting_is_editable(self, run_state: RunState) -> bool:
        return bool(
            run_state.metadata.get("bootstrap", {}).get("status") == "completed"
            and run_state.status in {
                "awaiting_initial_review", "in_progress", "awaiting_human_review",
                "awaiting_context", "awaiting_next_artifact",
            }
            and not run_state.metadata.get("study_materials")
            and run_state.metadata.get(
                "review_setting_user_selectable",
                run_state.metadata.get("review_mode") != "automatic",
            )
            and run_state.run_id not in self._processing_runs
        )

    def select_initial_review_setting(
        self, run_id: str, *, setting: str, continue_automatic: bool = False,
    ) -> dict[str, object]:
        """Set the routing policy for future work from the Initial Review view."""

        if setting not in {"automatic", "selective", "full"}:
            raise WebWorkflowError("Invalid review setting.")
        if continue_automatic and setting != "automatic":
            raise WebWorkflowError("Automatic continuation requires the Automatic setting.")
        with self._state_lock:
            run_state = self._load_run_state(run_id)
            if not self._review_setting_is_editable(run_state):
                raise WebWorkflowError(
                    "Review settings can change after initialization while the run is idle and iterative work remains; matched studies retain their assigned setting."
                )
            at_initial_checkpoint = run_state.status == "awaiting_initial_review"
            if continue_automatic and not at_initial_checkpoint:
                raise WebWorkflowError("Automatic continuation is only available at the initial checkpoint.")
            if continue_automatic and any(
                item.scope == "initial" and item.status == "pending"
                for item in run_state.history.context_requests
            ):
                raise WebWorkflowError("Resolve pending initial context requests before continuing.")
            run_state.metadata["review_setting_user_selectable"] = True
            previous_policy = asdict(run_state.review_policy)
            previous_setting = run_state.review_policy.setting
            if previous_setting != setting:
                if any(item.kind == "initial" for item in run_state.history.stage_reviews):
                    run_state.metadata.setdefault("initial_review_policy", previous_policy)
                # Existing requests keep the policy under which they were prepared.
                waiting = run_state.metadata.get("awaiting_human_review")
                if isinstance(waiting, dict):
                    waiting.setdefault("review_policy", previous_policy)
                for task in run_state.history.retrospective_tasks:
                    if task.status in {"prepared", "awaiting_human"}:
                        task.metadata.setdefault("review_policy", previous_policy)
                change = {
                    "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                    "previous_setting": previous_setting,
                    "review_setting": setting,
                    "run_status": run_state.status,
                    "processed_artifacts": len(self._processed_artifact_ids(run_state)),
                    "codebook_version": run_state.codebook.version,
                }
                run_state.metadata.setdefault("review_setting_history", []).append(change)
                self._record_event(run_state, "review_setting_selected", checkpoint="initial", **change)
            policy = dict(previous_policy)
            policy.update(setting=setting, initial_review_required=True,
                          final_review_required=True, random_audit_rate=0.10)
            run_state.review_policy = ReviewPolicyState(**policy)
            run_state.metadata["review_mode"] = setting
            run_state.metadata.setdefault("review_sampling_protocol", {}).update(
                setting=setting, unflagged_audit_rate=run_state.review_policy.random_audit_rate,
                effective_unflagged_audit_rate=(run_state.review_policy.random_audit_rate
                    if CODAOrchestrator._selective_sampling_enabled(run_state) else 0.0),
            )
            if continue_automatic:
                run_state.status = "in_progress"
                run_state.metadata["bootstrap"].setdefault("human_reviewed", False)
                self._record_event(run_state, "initial_review_bypassed", review_setting=setting,
                                   human_reviewed=False)
            paths = self._paths_for(run_id)
            manifest = json.loads(paths.run_manifest_path.read_text(encoding="utf-8"))
            manifest["protocol"]["review_policy"] = asdict(run_state.review_policy)
            manifest["protocol"]["review_setting_history"] = run_state.metadata.get("review_setting_history", [])
            self._write_json(paths.run_manifest_path, manifest)
            save_run_state_checkpoint(run_state, paths.checkpoint_path)
            packet = None if continue_automatic else self.stage_review_packet(
                run_id, "initial", inspection=not at_initial_checkpoint,
            )
            return {"run": self.run_summary(run_id), "packet": packet}

    def record_review_timer(
        self,
        run_id: str,
        *,
        action: str,
        scope: str,
        artifact_id: str | None = None,
    ) -> dict[str, object]:
        """Persist an explicit foreground-review pause/resume event."""

        if action not in {"pause", "resume"}:
            raise WebWorkflowError("Review timer action must be pause or resume.")
        if scope not in {"artifact", "initial", "triggered", "final", "rework"}:
            raise WebWorkflowError("Unsupported review timer scope.")
        run_state = self._load_run_state(run_id)
        if scope == "artifact" and not artifact_id:
            raise WebWorkflowError("Artifact timer events require artifact_id.")
        event_name = "review_timer_paused" if action == "pause" else "review_timer_resumed"
        self._record_event(
            run_state,
            event_name,
            timer_scope=scope,
            artifact_id=artifact_id,
        )
        save_run_state_checkpoint(run_state, self._paths_for(run_id).checkpoint_path)
        return {
            "run": self.run_summary(run_id),
            "action": action,
            "scope": scope,
            "artifact_id": artifact_id,
        }

    def submit_stage_review(
        self,
        run_id: str,
        kind: str,
        *,
        decision: str,
        rationale: str,
        revised_codes: list[CodeState] | None = None,
        change_operations: list[CodebookChangeState] | None = None,
        duration_seconds: float | None = None,
    ) -> dict[str, object]:
        """Apply one auditable Initial or Final Review decision."""

        allowed = {
            "accept",
            "revise",
            "reject",
            "request_additional_context",
            "mark_unresolved",
        }
        if kind not in {"initial", "final"} or decision not in allowed:
            raise WebWorkflowError("Invalid stage review kind or decision.")
        if not rationale.strip():
            raise WebWorkflowError("A stage review rationale is required.")
        run_state = self._load_run_state(run_id)
        expected = "awaiting_initial_review" if kind == "initial" else "awaiting_final_review"
        if run_state.status != expected:
            raise WebWorkflowError(f"This run is not awaiting {kind} review.")
        if kind == "initial" and run_state.review_policy.setting == "automatic":
            raise WebWorkflowError("Use Automatic continuation instead of submitting human approval.")
        experiment_protocol = run_state.metadata.get("experiment_protocol", {})
        freeze_after_initialization = (
            isinstance(experiment_protocol, dict)
            and experiment_protocol.get("variant") == "freeze_after_initialization"
            and isinstance(run_state.metadata.get("bootstrap"), dict)
            and run_state.metadata["bootstrap"].get("status") == "completed"
        )
        if freeze_after_initialization and (
            decision == "revise"
            or (kind == "final" and decision == "reject")
            or revised_codes
            or change_operations
        ):
            raise WebWorkflowError(
                "This experiment condition freezes the codebook after initialization; "
                f"{kind.title()} Review may inspect it but cannot submit codebook changes "
                "or reject the frozen final result."
            )
        if any(
            request.scope == kind and request.status == "pending"
            for request in run_state.history.context_requests
        ):
            raise WebWorkflowError(
                f"Resolve or cancel the pending {kind} context request before submitting another stage review."
            )
        if (
            kind == "final"
            and decision == "accept"
            and run_state.history.pending_retrospective_tasks()
        ):
            raise WebWorkflowError(
                "Complete all retrospective propagation tasks before accepting Final Review."
            )

        if kind == "final" and decision in {"accept", "mark_unresolved"}:
            issues = completion_issues(serialize_run_state_checkpoint(run_state))
            if issues:
                raise WebWorkflowError("Cannot finalize analysis: " + " ".join(issues))

        packet_before_review = self.stage_review_packet(run_id, kind)
        review_scope = packet_before_review.get("review_scope", {})
        audit_summary = packet_before_review.get("audit_summary", {})

        before = run_state.codebook.version
        before_codes = list(run_state.codebook.codes)
        stage_changes: list[CodebookChangeState] = []
        if decision == "revise":
            if not revised_codes:
                raise WebWorkflowError("A revise decision requires a revised codebook.")
            revised_codes = self._preserve_system_representatives(
                before_codes,
                revised_codes,
            )
            if change_operations:
                revised_codes = self._normalize_stage_review_codes(
                    revised_codes,
                    change_operations,
                )
                stage_changes = self._validate_stage_review_operations(
                    kind=kind,
                    before_codes=before_codes,
                    revised_codes=revised_codes,
                    operations=change_operations,
                    round_index=len(run_state.history.coding_records),
                    rationale=rationale.strip(),
                )
            else:
                # Backward compatibility for legacy clients is restricted to
                # unambiguous add/refine/rename edits. Structural edits must be
                # stated explicitly so their impact can be propagated.
                stage_changes = self._stage_review_codebook_changes(
                    kind=kind,
                    before_codes=before_codes,
                    revised_codes=revised_codes,
                    round_index=len(run_state.history.coding_records),
                    rationale=rationale.strip(),
                )
            candidate = deepcopy(run_state)
            candidate.codebook = candidate.codebook.next_version(codes=revised_codes)
            candidate_artifacts = {
                item.artifact_id: item for item in
                self._adapter_for(run_state.dataset_metadata.dataset_name).iter_artifacts()
            }
            self._verify_frozen_sources(run_state, candidate_artifacts)
            validation_rows = []
            orchestrator = self._orchestrator_for(run_id)
            scope_ids = (
                run_state.metadata.get("bootstrap", {}).get("artifact_ids", [])
                if kind == "initial" else self._processed_artifact_ids(run_state)
            )
            if not scope_ids:
                scope_ids = run_state.metadata.get("selected_artifact_ids", [])
            if not scope_ids:
                raise WebWorkflowError("Cannot validate a revised codebook without source cases.")
            for artifact_id in sorted(scope_ids):
                artifact = candidate_artifacts.get(artifact_id)
                if artifact is None:
                    raise WebWorkflowError(f"Cannot validate revised codebook: missing {artifact_id}.")
                result = orchestrator.validate_final_record(
                    candidate, artifact,
                    validation_scope="initial_codebook" if kind == "initial" else "final_audit",
                    corpus_audit={"human_revision": True, "reviewer_rationale": rationale,
                                  "candidate_changes": [asdict(change) for change in stage_changes],
                                  "prior_definitions": [asdict(code) for code in before_codes],
                                  "historical_assignments_pending_reassessment": True},
                )
                try:
                    orchestrator.require_supported_revision(result)
                except ValueError as error:
                    failures = run_state.metadata.setdefault("stage_human_revision_failures", {}).setdefault(kind, [])
                    failures.append({"artifact_id": artifact_id, "validation_output": asdict(result),
                                     "candidate_codes": [asdict(code) for code in revised_codes],
                                     "base_version": before})
                    if len(failures) >= run_state.review_policy.automatic_reassessment_limit:
                        run_state.status = "resource_limited"
                        run_state.notes.append(f"{kind.title()} revision exhausted the frozen work limit; candidate not accepted.")
                    save_run_state_checkpoint(run_state, self._paths_for(run_id).checkpoint_path)
                    raise WebWorkflowError(str(error)) from error
                validation_rows.append(asdict(result))
            run_state.metadata.setdefault("human_revision_validations", []).append({
                "stage": kind, "candidate_version": candidate.codebook.version,
                "validation_outputs": validation_rows,
            })
            next_codebook = run_state.codebook.next_version(codes=revised_codes)
            run_state.codebook = replace(
                next_codebook,
                revisions=[*run_state.codebook.revisions, *stage_changes],
            )
            for change in stage_changes:
                run_state.history.append_revision(change)
            if kind == "initial":
                orchestrator = self._orchestrator_for(run_id)
                for change in stage_changes:
                    orchestrator.enqueue_retrospective_tasks(
                        run_state=run_state,
                        change=change,
                        from_codebook_version=before,
                        source_artifact_id="stage-review:initial",
                    )
            if kind == "final":
                orchestrator = self._orchestrator_for(run_id)
                for change in stage_changes:
                    orchestrator.enqueue_retrospective_tasks(
                        run_state=run_state,
                        change=change,
                        from_codebook_version=before,
                        source_artifact_id=f"stage-review:{kind}",
                    )
                self._finish_iterative_coding(run_state)
        cross_source_audit_ids = (
            list(run_state.history.stabilization_checks[-1].cross_source_audit_artifact_ids)
            if kind == "final" and run_state.history.stabilization_checks
            else []
        )
        review = StageReviewState(
            review_id=f"stage-review-{uuid4().hex[:12]}",
            kind=kind,  # type: ignore[arg-type]
            decision=decision,  # type: ignore[arg-type]
            rationale=rationale.strip(),
            codebook_version_before=before,
            codebook_version_after=run_state.codebook.version,
            reviewer_id=(run_state.metadata.get("study_execution", {}).get("participant_id") or "researcher"),
            duration_seconds=duration_seconds,
            artifact_ids=(
                list(run_state.metadata.get("bootstrap", {}).get("artifact_ids", []))
                if kind == "initial"
                and isinstance(run_state.metadata.get("bootstrap"), dict)
                else sorted(self._processed_artifact_ids(run_state))
            ),
            change_ids=[change.change_id for change in stage_changes],
            metadata={
                "review_policy": asdict(run_state.review_policy),
                "added_code_ids": sorted(
                    {code.code_id for code in revised_codes or []}
                    - {code.code_id for code in before_codes}
                ) if decision == "revise" else [],
                "removed_code_ids": sorted(
                    {code.code_id for code in before_codes}
                    - {code.code_id for code in revised_codes or []}
                ) if decision == "revise" else [],
                "cross_source_audit_artifact_ids": cross_source_audit_ids,
                "cross_source_audit_presented": bool(cross_source_audit_ids),
                "review_scope": review_scope,
                "audit_summary": audit_summary,
                "evidence_packet_artifact_ids": sorted(
                    {
                        str(item.get("artifact_id"))
                        for key in (
                            "sampled_artifacts",
                            "cross_source_audit_artifacts",
                            "final_audit_artifacts",
                        )
                        for item in packet_before_review.get(key, [])
                        if isinstance(item, dict) and item.get("artifact_id") is not None
                    }
                ),
                "initial_review_coverage": packet_before_review.get(
                    "initial_review_coverage"
                ),
                "final_review_coverage": packet_before_review.get(
                    "final_review_coverage"
                ),
                "final_validation_audit_ids": [
                    item["audit_id"] for item in packet_before_review.get("final_validation_audits", [])
                ],
                "evidence_packet_unresolved_count": len(
                    packet_before_review.get("unresolved_cases", [])
                ),
            },
        )
        run_state.history.append_stage_review(review)
        if decision == "mark_unresolved":
            run_state.history.append_unresolved(
                UnresolvedCaseState(
                    unresolved_id=f"unresolved-{uuid4().hex[:12]}",
                    artifact_id=f"stage-review:{kind}",
                    reason=rationale.strip(),
                    source=f"{kind}_human_review",
                    created_at_codebook_version=run_state.codebook.version,
                    metadata={
                        "stage_review_id": review.review_id,
                        "review_kind": kind,
                    },
                )
            )
        if decision == "request_additional_context":
            run_state.history.append_context_request(
                ContextRequestState(
                    request_id=f"context-request-{uuid4().hex[:12]}",
                    scope=kind,  # type: ignore[arg-type]
                    reason=rationale.strip(),
                    requested_items=[rationale.strip()],
                    created_at_codebook_version=run_state.codebook.version,
                    metadata={"stage_review_id": review.review_id},
                )
            )
        paths = self._paths_for(run_id)

        if kind == "initial":
            bootstrap = run_state.metadata.get("bootstrap", {})
            if isinstance(bootstrap, dict):
                bootstrap["human_reviewed"] = True
                bootstrap["initial_review_decision"] = decision
            if decision in {"accept", "revise", "mark_unresolved"}:
                run_state.status = "in_progress"
                if (
                    run_state.review_policy.setting == "full"
                    and self._review_budget_exhausted(run_state)
                ):
                    self._mark_remaining_resource_limited(run_state)
            elif decision == "reject":
                run_state.metadata["initial_revision_attempts"] = int(
                    run_state.metadata.get("initial_revision_attempts", 0)
                ) + 1
                run_state.metadata.setdefault("initial_revision_feedback", []).append(rationale.strip())
                self._restore_bootstrap_queue(run_state)
                # Explicit reconsideration must not reuse a rejected induction.
                shutil.rmtree(paths.bootstrap_checkpoint_dir, ignore_errors=True)
                run_state.codebook = CodebookState.empty(
                    run_state.dataset_metadata.dataset_name
                )
                if isinstance(bootstrap, dict):
                    bootstrap["status"] = "not_run"
                    bootstrap["artifact_ids"] = []
                    bootstrap["code_count"] = 0
                if run_state.metadata["initial_revision_attempts"] >= run_state.review_policy.automatic_reassessment_limit:
                    self._mark_remaining_resource_limited(run_state)
                    run_state.notes.append("Initial codebook rejection exhausted the frozen substantive revision limit.")
                else:
                    run_state.status = "not_started"
            else:
                run_state.status = "awaiting_initial_review"
        else:
            if decision in {"accept", "mark_unresolved"}:
                if run_state.history.stabilization_checks:
                    latest_check = run_state.history.stabilization_checks[-1]
                    if (
                        decision == "accept"
                        and latest_check.cross_source_audit_artifact_ids
                    ):
                        latest_check.cross_source_audit_status = "human_review_completed"
                latest_check = (
                    run_state.history.stabilization_checks[-1]
                    if run_state.history.stabilization_checks
                    else None
                )
                run_state.status = (
                    "stabilized"
                    if (
                        decision == "accept"
                        and latest_check is not None
                        and latest_check.stable
                    )
                    else "completed_with_unresolved"
                )
                persist_final_codebook(run_state, paths.final_codebook_path)
                self._record_event(run_state, "outputs_frozen", codebook_version=run_state.codebook.version)
            elif decision == "reject":
                attempts = int(run_state.metadata.get("final_revision_attempts", 0)) + 1
                run_state.metadata["final_revision_attempts"] = attempts
                run_state.metadata.setdefault("final_revision_feedback", []).append(rationale.strip())
                if attempts >= run_state.review_policy.automatic_reassessment_limit:
                    run_state.status = "resource_limited"
                    run_state.notes.append("Final Review rejection exhausted the frozen substantive revision limit; no final approval was recorded.")
                else:
                    for artifact_id in sorted(self._processed_artifact_ids(run_state)):
                        if any(task.artifact_id == artifact_id for task in run_state.history.pending_retrospective_tasks()):
                            continue
                        run_state.history.append_retrospective_task(RetrospectiveRecodingTask(
                            task_id=f"final-reconsider-{uuid4().hex[:12]}", artifact_id=artifact_id,
                            trigger_change_id=review.review_id,
                            from_codebook_version=run_state.codebook.version,
                            target_codebook_version=run_state.codebook.version,
                            reason=rationale.strip(), metadata={"source": "final_review_rejection"},
                        ))
                    run_state.status = "awaiting_final_review"
            else:
                run_state.status = "awaiting_final_review"

        self._record_event(
            run_state,
            "stage_review_submitted",
            kind=kind,
            decision=decision,
            duration_seconds=duration_seconds,
        )
        save_run_state_checkpoint(run_state, paths.checkpoint_path)
        persist_codebook_snapshot(run_state, paths.codebook_snapshot_dir)
        return {"review": asdict(review), "run": self.run_summary(run_id)}

    @staticmethod
    def _preserve_system_representatives(
        existing_codes: list[CodeState],
        submitted_codes: list[CodeState],
    ) -> list[CodeState]:
        """Prevent stage-review payloads from editing provenance lists."""

        existing_by_id = {code.code_id: code for code in existing_codes}
        return [
            replace(
                code,
                representative_artifact_ids=(
                    list(existing_by_id[code.code_id].representative_artifact_ids)
                    if code.code_id in existing_by_id
                    else []
                ),
            )
            for code in submitted_codes
        ]

    @staticmethod
    def _normalize_stage_review_codes(
        revised_codes: list[CodeState],
        operations: list[CodebookChangeState],
    ) -> list[CodeState]:
        """Materialize structural operation semantics in the submitted codebook."""

        by_id = {code.code_id: code for code in revised_codes}
        for operation in operations:
            targets = list(dict.fromkeys(operation.target_code_ids))
            results = list(dict.fromkeys(operation.resulting_code_ids))
            if operation.action == "merge" and len(results) == 1:
                result_id = results[0]
                for target_id in targets:
                    if target_id in by_id and target_id != result_id:
                        target = by_id[target_id]
                        by_id[target_id] = replace(
                            target,
                            status="merged",
                            metadata={**target.metadata, "merged_into": result_id},
                        )
                if result_id in by_id:
                    by_id[result_id] = replace(by_id[result_id], status="active")
            elif operation.action == "split" and len(targets) == 1:
                target_id = targets[0]
                if target_id in by_id:
                    target = by_id[target_id]
                    by_id[target_id] = replace(
                        target,
                        status="split",
                        metadata={**target.metadata, "split_into": results},
                    )
                for result_id in results:
                    if result_id in by_id:
                        by_id[result_id] = replace(by_id[result_id], status="active")
            elif operation.action == "add":
                for result_id in results:
                    if result_id in by_id:
                        by_id[result_id] = replace(by_id[result_id], status="active")
            elif operation.action == "add_parent" and len(results) == 1:
                parent_id = results[0]
                for target_id in targets:
                    if target_id in by_id:
                        by_id[target_id] = replace(
                            by_id[target_id], parent_code_id=parent_id
                        )
                if parent_id in by_id:
                    by_id[parent_id] = replace(by_id[parent_id], status="active")
        return [by_id[code.code_id] for code in revised_codes]

    @staticmethod
    def _validate_stage_review_operations(
        *,
        kind: str,
        before_codes: list[CodeState],
        revised_codes: list[CodeState],
        operations: list[CodebookChangeState],
        round_index: int,
        rationale: str,
    ) -> list[CodebookChangeState]:
        """Validate explicit human operations against the submitted codebook."""

        before_by_id = {code.code_id: code for code in before_codes}
        revised_by_id = {code.code_id: code for code in revised_codes}
        if len(revised_by_id) != len(revised_codes):
            raise WebWorkflowError("Revised code ids must be unique.")
        if any(not code_id.strip() for code_id in revised_by_id):
            raise WebWorkflowError("Revised code ids must not be empty.")
        if set(before_by_id) - set(revised_by_id):
            raise WebWorkflowError(
                "Stage Review cannot delete code records. Keep the code and mark it retired, "
                "or describe an explicit merge/split that preserves its audit trail."
            )

        for code in revised_codes:
            parent_id = code.parent_code_id
            if parent_id is None:
                continue
            if parent_id == code.code_id:
                raise WebWorkflowError("A code cannot be its own parent.")
            parent = revised_by_id.get(parent_id)
            if parent is None:
                raise WebWorkflowError(
                    f"Parent code '{parent_id}' does not exist in the revised codebook."
                )
            if parent.status != "active":
                raise WebWorkflowError(
                    f"Parent code '{parent_id}' must be active."
                )

        for code_id in revised_by_id:
            visited: set[str] = set()
            current_id: str | None = code_id
            while current_id is not None:
                if current_id in visited:
                    raise WebWorkflowError("The revised code hierarchy contains a parent cycle.")
                visited.add(current_id)
                current = revised_by_id[current_id]
                current_id = current.parent_code_id

        added_ids = set(revised_by_id) - set(before_by_id)
        changed_ids = {
            code_id
            for code_id in set(before_by_id) & set(revised_by_id)
            if before_by_id[code_id] != revised_by_id[code_id]
        }
        covered_added: set[str] = set()
        covered_changed: set[str] = set()
        allowed_parent_changes: set[str] = set()
        allowed_status_changes: set[str] = set()
        normalized: list[CodebookChangeState] = []
        for operation in operations:
            if not operation.summary.strip():
                raise WebWorkflowError("Every stage operation requires a summary.")
            if not operation.rationale.strip():
                raise WebWorkflowError("Every stage operation requires a rationale.")
            if operation.action == "no_change":
                raise WebWorkflowError("A revise decision cannot contain a no_change operation.")
            targets = set(operation.target_code_ids)
            results = set(operation.resulting_code_ids)
            if targets - set(before_by_id):
                raise WebWorkflowError("A stage operation references an unknown current code id.")
            if results - set(revised_by_id):
                raise WebWorkflowError("A stage operation references a missing resulting code id.")
            if operation.action == "add":
                if targets or len(results) != 1 or not results <= added_ids:
                    raise WebWorkflowError("Add requires one new result and no current-code targets.")
                if revised_by_id[next(iter(results))].status != "active":
                    raise WebWorkflowError("A newly added code must be active.")
            elif operation.action == "add_parent":
                if len(targets) < 2 or len(results) != 1 or not results <= added_ids:
                    raise WebWorkflowError("Add parent requires at least two current children and one new parent.")
                parent_id = next(iter(results))
                if any(revised_by_id[code_id].parent_code_id != parent_id for code_id in targets):
                    raise WebWorkflowError("Every selected child must reference the new parent code.")
                if revised_by_id[parent_id].status != "active":
                    raise WebWorkflowError("A newly added parent code must be active.")
                if any(revised_by_id[code_id].status != "active" for code_id in targets):
                    raise WebWorkflowError("Add parent can only attach active child codes.")
                covered_changed.update(targets)
                allowed_parent_changes.update(targets)
            elif operation.action in {"refine", "rename"}:
                if len(targets) != 1 or (results and results != targets):
                    raise WebWorkflowError(f"{operation.action.title()} must keep one existing code id.")
                target_id = next(iter(targets))
                if revised_by_id[target_id].status != before_by_id[target_id].status:
                    raise WebWorkflowError(
                        f"{operation.action.title()} cannot change code status. Use merge or split."
                    )
                covered_changed.update(targets)
            elif operation.action == "retire":
                if len(targets) != 1 or (results and results != targets):
                    raise WebWorkflowError("Retire requires one existing code and keeps its id.")
                target_id = next(iter(targets))
                if revised_by_id[target_id].status != "retired":
                    raise WebWorkflowError("A retire operation must mark its target as retired.")
                covered_changed.add(target_id)
                allowed_status_changes.add(target_id)
            elif operation.action == "merge":
                if len(targets) < 2 or len(results) != 1:
                    raise WebWorkflowError("Merge requires at least two targets and one result.")
                result_id = next(iter(results))
                if any(
                    revised_by_id[target_id].status != "merged"
                    for target_id in targets
                    if target_id != result_id
                ):
                    raise WebWorkflowError("Merged source codes must remain in the codebook with status 'merged'.")
                if revised_by_id[result_id].status != "active":
                    raise WebWorkflowError("The merge result must be active.")
                if any(
                    revised_by_id[target_id].metadata.get("merged_into") != result_id
                    for target_id in targets
                    if target_id != result_id
                ):
                    raise WebWorkflowError("Every merged source must record its merge result.")
                covered_changed.update(targets)
                allowed_status_changes.update(targets)
            elif operation.action == "split":
                if len(targets) != 1 or len(results) < 2 or targets & results:
                    raise WebWorkflowError("Split requires one source and at least two distinct results.")
                if revised_by_id[next(iter(targets))].status != "split":
                    raise WebWorkflowError("The split source must remain with status 'split'.")
                source_id = next(iter(targets))
                if set(revised_by_id[source_id].metadata.get("split_into", [])) != results:
                    raise WebWorkflowError("The split source must record all split result ids.")
                if any(revised_by_id[result_id].status != "active" for result_id in results):
                    raise WebWorkflowError("Every split result must be active.")
                covered_changed.update(targets)
                allowed_status_changes.update(targets)
            else:
                raise WebWorkflowError(f"Unsupported stage operation: {operation.action}.")
            covered_added.update(results & added_ids)
            covered_changed.update(results & changed_ids)
            normalized.append(
                replace(
                    operation,
                    round_index=round_index,
                    rationale=operation.rationale.strip() or rationale,
                    decided_by="human",
                    metadata={**operation.metadata, "review_stage": kind},
                )
            )

        changed_parent_ids = {
            code_id
            for code_id in set(before_by_id) & set(revised_by_id)
            if before_by_id[code_id].parent_code_id != revised_by_id[code_id].parent_code_id
        }
        if changed_parent_ids - allowed_parent_changes:
            raise WebWorkflowError(
                "Parent relationships must be changed through an explicit add_parent operation."
            )
        changed_status_ids = {
            code_id
            for code_id in set(before_by_id) & set(revised_by_id)
            if before_by_id[code_id].status != revised_by_id[code_id].status
        }
        if changed_status_ids - allowed_status_changes:
            raise WebWorkflowError(
                "Code status changes must be explained by an explicit retire, merge, or split operation."
            )

        if added_ids - covered_added or changed_ids - covered_changed:
            missing = sorted((added_ids - covered_added) | (changed_ids - covered_changed))
            raise WebWorkflowError(
                "Every changed code must be covered by an explicit stage operation: "
                + ", ".join(missing)
            )
        return normalized

    @staticmethod
    def _stage_review_codebook_changes(
        *,
        kind: str,
        before_codes: list[CodeState],
        revised_codes: list[CodeState],
        round_index: int,
        rationale: str,
    ) -> list[CodebookChangeState]:
        """Turn a stage-level codebook edit into explicit, auditable revisions."""

        before_by_id = {code.code_id: code for code in before_codes}
        revised_by_id = {code.code_id: code for code in revised_codes}
        if len(revised_by_id) != len(revised_codes):
            raise WebWorkflowError("Revised code ids must be unique.")
        removed_ids = set(before_by_id) - set(revised_by_id)
        if removed_ids:
            raise WebWorkflowError(
                "Stage Review cannot silently remove codes. Keep them as retired records "
                "or submit explicit merge/split operations."
            )

        changes: list[CodebookChangeState] = []
        for code_id in sorted(set(revised_by_id) - set(before_by_id)):
            code = revised_by_id[code_id]
            changes.append(
                CodebookChangeState(
                    change_id=f"stage-change-{uuid4().hex[:12]}",
                    action="add",
                    round_index=round_index,
                    summary=f"Add {code.name} during {kind} review.",
                    rationale=rationale,
                    resulting_code_ids=[code_id],
                    artifact_ids=list(code.representative_artifact_ids),
                    decided_by="human",
                    metadata={"review_stage": kind},
                )
            )

        for code_id in sorted(set(before_by_id) & set(revised_by_id)):
            old = before_by_id[code_id]
            new = revised_by_id[code_id]
            if old == new:
                continue
            old_without_name = replace(old, name=new.name)
            if old.status != new.status and new.status == "retired":
                action = "retire"
            else:
                action = "rename" if old_without_name == new and old.name != new.name else "refine"
            changes.append(
                CodebookChangeState(
                    change_id=f"stage-change-{uuid4().hex[:12]}",
                    action=action,
                    round_index=round_index,
                    summary=f"{action.title()} {old.name} during {kind} review.",
                    rationale=rationale,
                    target_code_ids=[code_id],
                    resulting_code_ids=[code_id],
                    artifact_ids=sorted(
                        set(old.representative_artifact_ids)
                        | set(new.representative_artifact_ids)
                    ),
                    decided_by="human",
                    metadata={"review_stage": kind},
                )
            )

        if not changes:
            raise WebWorkflowError("The revised codebook does not differ from the current codebook.")
        return changes

    def list_runs(self) -> list[dict[str, object]]:
        if not self._runs_root.exists():
            return []
        summaries: list[dict[str, object]] = []
        for run_dir in sorted(self._runs_root.iterdir()):
            if not run_dir.is_dir() or not (run_dir / "checkpoint.json").exists():
                continue
            try:
                summaries.append(self.run_summary(run_dir.name))
            except (OSError, ValueError, TypeError, WebWorkflowError):
                continue
        return summaries

    def export_held_out_materials(self, run_id: str) -> dict[str, object]:
        """Export a frozen held-out packet without entering the CODA workflow."""

        run_state = self._load_run_state(run_id)
        if run_state.total_held_out_artifacts == 0:
            raise WebWorkflowError("This run has no held-out evaluation pool.")
        try:
            return export_held_out_materials(
                self._paths_for(run_id).run_dir,
                self._adapter_for(run_state.dataset_metadata.dataset_name),
                self._paths_for(run_id).run_dir / "held_out_materials.json",
            )
        except EvaluationError as error:
            raise WebWorkflowError(str(error)) from error

    def delete_run(self, run_id: str) -> dict[str, object]:
        """Delete one persisted run and all of its derived research records."""

        with self._state_lock:
            paths = self._paths_for(run_id)
            if not paths.run_dir.is_dir() or not paths.checkpoint_path.exists():
                raise WebRunNotFoundError(f"Run '{run_id}' does not exist.")
            run_state = self._load_run_state(run_id)
            if run_id in self._initializing_runs:
                raise WebWorkflowError("Cannot delete a task while initialization is running.")
            self._prepared_reviews.pop(run_id, None)
            task_ids = {task.task_id for task in run_state.history.retrospective_tasks}
            for task_id in task_ids:
                self._prepared_retrospective_reviews.pop((run_id, task_id), None)
            self._active_states.pop(run_id, None)
            self._orchestrators.pop(run_id, None)
            self._output_languages.pop(run_id, None)
            shutil.rmtree(paths.run_dir)
        return {"run_id": run_id, "deleted": True}

    def run_summary(self, run_id: str) -> dict[str, object]:
        with self._state_lock:
            run_state = self._load_run_state(run_id)
            bootstrap_metadata = run_state.metadata.get("bootstrap")
            if (
                isinstance(bootstrap_metadata, dict)
                and str(bootstrap_metadata.get("status", "")) in {"running", "cancelling"}
                and run_id not in self._initializing_runs
            ):
                run_state.metadata["bootstrap"] = self._interrupted_bootstrap_metadata(
                    dict(bootstrap_metadata)
                )
                save_run_state_checkpoint(
                    run_state,
                    self._paths_for(run_id).checkpoint_path,
                )
            reviewed_records = [
                record
                for record in run_state.history.coding_records
                if record.metadata.get("review_origin") != "bootstrap_provisional"
            ]
            # A request for more context is an auditable human action, but it
            # is not a completed coding decision.  Use the latest record per
            # artifact so a context re-review cannot inflate progress counts.
            latest_records_by_artifact: dict[str, CodingRecordState] = {}
            for record in reviewed_records:
                latest_records_by_artifact[record.artifact_id] = record
            cancelled_context_record_ids = {
                str(request.metadata.get("record_id"))
                for request in run_state.history.context_requests
                if request.scope == "artifact"
                and request.status == "cancelled"
                and request.metadata.get("record_id")
            }
            terminal_records = [
                record
                for record in latest_records_by_artifact.values()
                if record.decision != "request_additional_context"
                or record.record_id in cancelled_context_record_ids
            ]
            reviewed = len(terminal_records)
            automatic_reviewed = sum(
                1
                for record in terminal_records
                if record.metadata.get("review_origin")
                in {"automatic_policy", "automatic_unresolved"}
            )
            human_reviewed = sum(
                1
                for record in latest_records_by_artifact.values()
                if record.metadata.get("human_reviewed", True) is True
            )
            bootstrap_metadata = run_state.metadata.get("bootstrap")
            has_bootstrap_metadata = isinstance(bootstrap_metadata, dict)
            bootstrap = bootstrap_metadata if has_bootstrap_metadata else {}
            progress = bootstrap.get("progress", {})
            return {
                "run_id": run_state.run_id,
                "dataset_name": run_state.dataset_metadata.dataset_name,
                "dataset_display_name": run_state.dataset_metadata.display_name,
                "status": run_state.status,
                "run_dir": str(self._paths_for(run_id).run_dir),
                "run_manifest": str(self._paths_for(run_id).run_manifest_path),
                "study_materials": run_state.metadata.get("study_materials"),
                "study_execution": run_state.metadata.get("study_execution", {}),
                "iterative_batch_protocol": run_state.metadata.get("iterative_batch_protocol", {"batch_size": 1}),
                "reviewed_artifacts": reviewed,
                "input_artifacts": int(
                    bootstrap.get("population_size", run_state.total_coding_artifacts)
                ),
                # This is the review denominator (the post-bootstrap queue),
                # while ``reviewed_artifacts`` counts both human and automatic
                # terminal records.
                "human_review_artifacts": run_state.total_coding_artifacts,
                "selected_artifacts": run_state.total_coding_artifacts,
                "coding_pool_artifacts": run_state.total_coding_artifacts,
                "held_out_artifacts": run_state.total_held_out_artifacts,
                "total_selected_artifacts": (
                    run_state.total_coding_artifacts
                    + run_state.total_held_out_artifacts
                ),
                "human_reviewed_artifacts": human_reviewed,
                "auto_processed_artifacts": automatic_reviewed,
                "total_artifacts": run_state.total_coding_artifacts,
                "review_mode": str(run_state.metadata.get("review_mode", "full")),
                "review_setting": run_state.review_policy.setting,
                "review_setting_locked": not self._review_setting_is_editable(run_state),
                "experiment_variant": str(
                    run_state.metadata.get("experiment_protocol", {}).get(
                        "variant", "standard"
                    )
                ),
                "experiment_protocol": dict(
                    run_state.metadata.get("experiment_protocol", {})
                ),
                "review_budget_minutes": run_state.review_policy.review_budget_minutes,
                "review_time_used_seconds": self._human_review_seconds(run_state),
                "review_budget_exhausted": self._review_budget_exhausted(run_state),
                "codebook_version": run_state.codebook.version,
                "code_count": len(run_state.codebook.codes),
                "bootstrap_enabled": bool(bootstrap.get("enabled", False)),
                # Historical runs predate explicit initialization and must remain
                # reviewable rather than being reclassified as pending tasks.
                "bootstrap_status": str(bootstrap.get("status", "skipped")),
                "bootstrap_artifacts": len(bootstrap.get("artifact_ids", [])),
                "bootstrap_code_count": int(bootstrap.get("code_count", 0)),
                "bootstrap_protocol": dict(bootstrap.get("protocol", {})),
                "bootstrap_progress": dict(progress) if isinstance(progress, dict) else {},
                "awaiting_next_artifact": run_state.status == "awaiting_next_artifact",
                "awaiting_context": run_state.status == "awaiting_context",
                "pending_context_request_count": len(
                    run_state.history.pending_context_requests()
                ),
                "retrospective_task_count": len(run_state.history.retrospective_tasks),
                "pending_retrospective_task_count": len(
                    run_state.history.pending_retrospective_tasks()
                ),
                "retrospective_recoding_suppressed_count": len(
                    run_state.metadata.get("retrospective_suppression_events", [])
                    if isinstance(
                        run_state.metadata.get("retrospective_suppression_events", []),
                        list,
                    )
                    else []
                ),
                "open_unresolved_count": len(run_state.history.open_unresolved_cases()),
                "evidence_audit_metrics": self._evidence_audit_metrics(run_state),
                "initial_review": (
                    asdict(run_state.history.latest_stage_review("initial"))
                    if run_state.history.latest_stage_review("initial") is not None
                    else None
                ),
                "final_review": (
                    asdict(run_state.history.latest_stage_review("final"))
                    if run_state.history.latest_stage_review("final") is not None
                    else None
                ),
                "stabilization": (
                    asdict(run_state.history.stabilization_checks[-1])
                    if run_state.history.stabilization_checks
                    else None
                ),
            }

    def current_artifact(self, run_id: str) -> dict[str, object]:
        run_state = self._load_run_state(run_id)
        if self._bootstrap_is_pending(run_state):
            return {
                "artifact": None,
                "message": "Initialize this task before opening its first artifact.",
                "codebook": serialize_codebook_state(run_state.codebook),
            }
        if run_state.status == "awaiting_initial_review":
            return {
                "artifact": None,
                "message": "Complete the initial codebook review before iterative coding.",
                "codebook": serialize_codebook_state(run_state.codebook),
            }
        if run_state.status == "awaiting_final_review":
            return {
                "artifact": None,
                "message": "Iterative coding is complete and the final review is pending.",
                "codebook": serialize_codebook_state(run_state.codebook),
            }
        if run_state.status == "awaiting_context":
            return {
                "artifact": None,
                "message": (
                    "This artifact is waiting for additional context. Resolve or cancel "
                    "the pending context request before continuing."
                ),
                "codebook": serialize_codebook_state(run_state.codebook),
            }
        if run_state.status == "awaiting_next_artifact":
            return {
                "artifact": None,
                "message": "The last review is complete. Advance explicitly before the next artifact.",
                "codebook": serialize_codebook_state(run_state.codebook),
            }
        batch = run_state.current_batch()
        if batch is None:
            return {
                "artifact": None,
                "message": "This run is complete.",
                "codebook": serialize_codebook_state(run_state.codebook),
            }
        pending = pending_artifacts_for_batch(batch, run_state)
        if not pending:
            return {
                "artifact": None,
                "message": "No pending artifacts remain in the current batch.",
                "codebook": serialize_codebook_state(run_state.codebook),
            }
        return {
            "artifact": asdict(pending[0]),
            "batch_id": batch.batch_id,
            "batch_index": batch.batch_index,
            "batch_size": len(batch.artifacts),
            "batch_position": [item.artifact_id for item in batch.artifacts].index(pending[0].artifact_id) + 1,
            "batch_preparation": run_state.metadata.get("iterative_batch_preparations", {}).get(batch.batch_id, {}).get("status"),
            "codebook": serialize_codebook_state(run_state.codebook),
        }

    def prepare_review(self, run_id: str, *, language: str = "en") -> dict[str, object]:
        run_state = self._load_run_state(run_id)
        if self._bootstrap_is_pending(run_state):
            raise WebWorkflowError("Initialize this task before preparing an evidence packet.")
        if run_state.status == "awaiting_initial_review":
            raise WebWorkflowError("Complete the initial codebook review first.")
        if run_state.status == "awaiting_final_review":
            raise WebWorkflowError("This run is waiting for final review.")
        if run_state.status == "awaiting_context":
            raise WebWorkflowError(
                "Resolve or cancel the pending context request before preparing another review."
            )
        if run_state.status in {
            "completed", "stabilized", "completed_with_unresolved", "resource_limited"
        }:
            raise WebWorkflowError("This run has no remaining review work.")
        if (
            run_state.review_policy.setting != "full"
            and run_state.status != "awaiting_human_review"
        ):
            raise WebWorkflowError(
                "Automatic and Selective runs must use automatic processing so the "
                "frozen routing policy decides whether human review is required."
            )
        if run_state.status == "awaiting_next_artifact":
            raise WebWorkflowError("Advance to the next artifact before preparing another review.")
        active_retrospective_ids = {
            task.task_id
            for task in run_state.history.retrospective_tasks
            if (run_id, task.task_id) in self._prepared_retrospective_reviews
        }
        if active_retrospective_ids:
            raise WebWorkflowError(
                "Submit the prepared retrospective review before opening an artifact review."
            )
        if language not in {"en", "zh"}:
            raise WebWorkflowError("language must be 'en' or 'zh'.")
        orchestrator = self._orchestrator_for(run_id)
        previous_language = self._output_languages.get(run_id, "en")
        if previous_language != language:
            self._prepared_reviews.pop(run_id, None)
        orchestrator.set_output_language(language)
        self._output_languages[run_id] = language
        run_state.metadata["output_language"] = language
        prepared = self._prepared_reviews.get(run_id)
        if prepared is None:
            batch, artifact = self._current_pending_artifact(run_state)
            stage_store = self._stage_store(
                run_id,
                orchestrator,
                run_state,
                artifact,
            )
            self._record_event(run_state, "iterative_started")
            self._record_event(
                run_state,
                "artifact_processing_started",
                artifact_id=artifact.artifact_id,
            )
            prepared = self._prepare_iterative_case(
                run_state,
                orchestrator,
                batch,
                artifact,
                allow_reviewed=artifact.artifact_id in set(
                    run_state.metadata.get("reopened_context_artifact_ids", [])
                ),
                # A context request deliberately reopens an already recorded
                # artifact. Keep that provenance distinct so the normal
                # duplicate-review guard does not reject the re-review.
                review_origin=(
                    "context_reopen"
                    if artifact.artifact_id
                    in set(run_state.metadata.get("reopened_context_artifact_ids", []))
                    else "current"
                ),
                stage_store=stage_store,
            )
            self._prepared_reviews[run_id] = prepared
        run_state.metadata["awaiting_human_review"] = {
            "artifact_id": prepared.artifact_id,
            "codebook_version": prepared.codebook_version,
            "routing_decision": asdict(prepared.evidence_packet.routing_decision)
            if prepared.evidence_packet.routing_decision is not None
            else None,
        }
        if (
            prepared.evidence_packet.routing_decision is not None
            and prepared.evidence_packet.routing_decision.route == "human_review"
        ):
            self._record_event(
                run_state,
                "artifact_waiting_for_human_review",
                artifact_id=prepared.artifact_id,
                risk_signals=(
                    list(prepared.evidence_packet.routing_decision.risk_signals)
                    if prepared.evidence_packet.routing_decision is not None
                    else []
                ),
            )
        save_run_state_checkpoint(run_state, self._paths_for(run_id).checkpoint_path)
        persist_codebook_snapshot(run_state, self._paths_for(run_id).codebook_snapshot_dir)
        return self.review_packet(run_id)

    def review_packet(self, run_id: str) -> dict[str, object]:
        run_state = self._load_run_state(run_id)
        prepared = self._prepared_reviews.get(run_id)
        if prepared is None and run_state.status == "awaiting_human_review":
            prepared = self._rebuild_prepared_review(run_id, run_state)
        if prepared is None:
            raise WebWorkflowError("No prepared review packet. Prepare the current artifact first.")
        review_input = self._orchestrator_for(run_id).human_review_input(run_state, prepared)
        return {
            "artifact_id": prepared.artifact_id,
            "codebook_version": prepared.codebook_version,
            "review_input": asdict(review_input),
        }

    def _rebuild_prepared_review(
        self,
        run_id: str,
        run_state: RunState,
    ) -> PreparedArtifactReview:
        """Restore a waiting packet from the persisted stage checkpoints."""

        waiting = run_state.metadata.get("awaiting_human_review")
        if not isinstance(waiting, dict):
            raise WebWorkflowError(
                "The run is waiting for review but has no persisted waiting metadata."
            )
        expected_artifact_id = str(waiting.get("artifact_id", ""))
        batch, artifact = self._current_pending_artifact(run_state)
        if expected_artifact_id and artifact.artifact_id != expected_artifact_id:
            raise WebWorkflowError(
                "The checkpoint waiting artifact does not match the current coding queue."
            )
        language = str(run_state.metadata.get("output_language", "en"))
        if language not in {"en", "zh"}:
            language = "en"
        orchestrator = self._orchestrator_for(run_id)
        orchestrator.set_output_language(language)
        self._output_languages[run_id] = language
        preparation_state = (
            replace(run_state, review_policy=ReviewPolicyState(**waiting["review_policy"]))
            if isinstance(waiting.get("review_policy"), dict) else run_state
        )
        prepared = self._prepare_iterative_case(
            preparation_state, orchestrator, batch, artifact,
            stage_store=self._stage_store(
                run_id, orchestrator, preparation_state, artifact
            ),
        )
        if prepared.evidence_packet.routing_decision is None or prepared.evidence_packet.routing_decision.route != "human_review":
            raise WebWorkflowError(
                "The restored packet no longer requires human review; refresh the run state before continuing."
            )
        expected_version = waiting.get("codebook_version")
        if expected_version is not None and prepared.codebook_version != int(expected_version):
            raise WebWorkflowError(
                "The codebook changed while restoring the waiting evidence packet."
            )
        self._prepared_reviews[run_id] = prepared
        return prepared

    def retrospective_tasks(self, run_id: str) -> dict[str, object]:
        """Return the separate queue for version-triggered historical recoding."""

        run_state = self._load_run_state(run_id)
        return {
            "run_id": run_id,
            "tasks": [asdict(task) for task in run_state.history.retrospective_tasks],
            "pending_count": len(run_state.history.pending_retrospective_tasks()),
        }

    def prepare_retrospective_task(
        self,
        run_id: str,
        task_id: str,
        *,
        language: str = "en",
    ) -> dict[str, object]:
        """Prepare an evidence packet without changing the ordinary artifact queue."""

        if language not in {"en", "zh"}:
            raise WebWorkflowError("language must be 'en' or 'zh'.")
        run_state = self._load_run_state(run_id)
        task = run_state.history.retrospective_task(task_id)
        if task is None:
            raise WebWorkflowError(f"Retrospective task '{task_id}' does not exist.")
        if task.status in {"completed", "cancelled"}:
            raise WebWorkflowError(f"Retrospective task '{task_id}' is no longer actionable.")
        if run_id in self._prepared_reviews or run_state.status in {
            "awaiting_human_review",
            "awaiting_context",
        }:
            raise WebWorkflowError(
                "Complete the current artifact review before opening a retrospective review."
            )
        other_prepared_task_ids = [
            prepared_task_id
            for prepared_run_id, prepared_task_id in self._prepared_retrospective_reviews
            if prepared_run_id == run_id and prepared_task_id != task_id
        ]
        if other_prepared_task_ids:
            raise WebWorkflowError(
                "Submit the currently prepared retrospective review before opening another one."
            )
        if any(
            request.status == "pending"
            and request.metadata.get("retrospective_task_id") == task_id
            for request in run_state.history.context_requests
        ):
            raise WebWorkflowError(
                "Resolve or cancel this retrospective review's context request before preparing it again."
            )
        cache_key = (run_id, task_id)
        prepared = self._prepared_retrospective_reviews.get(cache_key)
        orchestrator = self._orchestrator_for(run_id)
        orchestrator.set_output_language(language)
        self._output_languages[run_id] = language
        if prepared is None:
            batch, artifact = self._batch_and_artifact_for_task(run_state, task)
            task.status = "prepared"
            save_run_state_checkpoint(run_state, self._paths_for(run_id).checkpoint_path)
            try:
                preparation_state = (
                    replace(run_state, review_policy=ReviewPolicyState(**task.metadata["review_policy"]))
                    if isinstance(task.metadata.get("review_policy"), dict) else run_state
                )
                stage_store = self._stage_store(
                    run_id,
                    orchestrator,
                    preparation_state,
                    artifact,
                    review_origin="retrospective",
                    retrospective_task_id=task.task_id,
                )
                prepared = orchestrator.prepare_retrospective_artifact(
                    preparation_state,
                    artifact=artifact,
                    batch=batch,
                    task_id=task.task_id,
                    stage_checkpoint_store=stage_store,
                )
            except Exception:
                task.status = "pending"
                save_run_state_checkpoint(run_state, self._paths_for(run_id).checkpoint_path)
                raise
            automatic_output = orchestrator.automatic_review_if_safe(run_state, prepared)
            if automatic_output is not None:
                result = orchestrator.submit_prepared_review(
                    run_state,
                    prepared_review=prepared,
                    human_review_output=automatic_output,
                )
                if (
                    run_state.status == "awaiting_final_review"
                    and not run_state.history.pending_retrospective_tasks()
                ):
                    self._finish_iterative_coding(run_state)
                persist_artifact_completion(
                    run_state=run_state,
                    batch=prepared.batch,
                    result=result,
                    paths=self._paths_for(run_id),
                )
                save_run_state_checkpoint(
                    run_state, self._paths_for(run_id).checkpoint_path
                )
                stage_store.clear()
                return {
                    "auto_processed": True,
                    "task": asdict(task),
                    "artifact_id": result.artifact_id,
                    "decision": result.human_review_output.decision,
                    "routing_decision": asdict(
                        prepared.evidence_packet.routing_decision
                    ),
                    "codebook": serialize_codebook_state(run_state.codebook),
                    "run": self.run_summary(run_id),
                }
            task.status = "awaiting_human"
            self._prepared_retrospective_reviews[cache_key] = prepared
            save_run_state_checkpoint(run_state, self._paths_for(run_id).checkpoint_path)
        return self.retrospective_review_packet(run_id, task_id)

    def retrospective_review_packet(self, run_id: str, task_id: str) -> dict[str, object]:
        run_state = self._load_run_state(run_id)
        task = run_state.history.retrospective_task(task_id)
        prepared = self._prepared_retrospective_reviews.get((run_id, task_id))
        if task is None or prepared is None:
            raise WebWorkflowError(
                "Prepare this retrospective task before opening its evidence packet."
            )
        review_input = self._orchestrator_for(run_id).human_review_input(run_state, prepared)
        return {
            "task": asdict(task),
            "artifact_id": prepared.artifact_id,
            "codebook_version": prepared.codebook_version,
            "review_kind": "retrospective",
            "review_input": asdict(review_input),
        }

    def submit_retrospective_review(
        self,
        run_id: str,
        task_id: str,
        *,
        human_review_output: HumanReviewOutput,
    ) -> dict[str, object]:
        run_state = self._load_run_state(run_id)
        human_review_output = self._identify_reviewer(run_state, human_review_output)
        task = run_state.history.retrospective_task(task_id)
        prepared = self._prepared_retrospective_reviews.get((run_id, task_id))
        if task is None or prepared is None:
            raise WebWorkflowError("Prepare this retrospective task before submitting it.")
        if task.status in {"completed", "cancelled"}:
            raise WebWorkflowError(f"Retrospective task '{task_id}' is no longer actionable.")
        if task.status != "awaiting_human":
            raise WebWorkflowError(
                f"Retrospective task '{task_id}' is not waiting for a human decision."
            )
        if prepared.codebook_version != run_state.codebook.version:
            self._prepared_retrospective_reviews.pop((run_id, task_id), None)
            task.status = "pending"
            self._stage_store(
                run_id,
                self._orchestrator_for(run_id),
                run_state,
                prepared.artifact,
                review_origin="retrospective",
                retrospective_task_id=task_id,
            ).clear()
            save_run_state_checkpoint(run_state, self._paths_for(run_id).checkpoint_path)
            raise WebWorkflowError(
                "The codebook changed after this retrospective packet was prepared. "
                "Prepare the task again before submitting a decision."
            )
        human_review_output = self._ground_human_review_evidence(
            prepared,
            human_review_output,
        )
        try:
            result = self._orchestrator_for(run_id).submit_prepared_review(
                run_state, prepared_review=prepared, human_review_output=human_review_output,
            )
        except ValueError:
            save_run_state_checkpoint(run_state, self._paths_for(run_id).checkpoint_path)
            raise
        if (
            run_state.status == "awaiting_final_review"
            and not run_state.history.pending_retrospective_tasks()
        ):
            self._finish_iterative_coding(run_state)
        persist_artifact_completion(
            run_state=run_state,
            batch=prepared.batch,
            result=result,
            paths=self._paths_for(run_id),
        )
        self._prepared_retrospective_reviews.pop((run_id, task_id), None)
        self._stage_store(
            run_id,
            self._orchestrator_for(run_id),
            run_state,
            prepared.artifact,
            review_origin="retrospective",
            retrospective_task_id=task_id,
        ).clear()
        return {
            "task": asdict(task),
            "artifact_id": result.artifact_id,
            "decision": result.human_review_output.decision,
            "codebook": serialize_codebook_state(run_state.codebook),
            "run": self.run_summary(run_id),
        }

    def submit_review(
        self,
        run_id: str,
        *,
        human_review_output: HumanReviewOutput,
    ) -> dict[str, object]:
        run_state = self._load_run_state(run_id)
        human_review_output = self._identify_reviewer(run_state, human_review_output)
        if run_state.status != "awaiting_human_review":
            raise WebWorkflowError(
                "The current artifact is not waiting for a human review decision."
            )
        prepared = self._prepared_reviews.get(run_id)
        if prepared is None:
            prepared = self._rebuild_prepared_review(run_id, run_state)
        if prepared is None:
            raise WebWorkflowError("No prepared review packet is available for submission.")
        if prepared.codebook_version != run_state.codebook.version:
            self._prepared_reviews.pop(run_id, None)
            run_state.status = "in_progress"
            self._stage_store(
                run_id,
                self._orchestrator_for(run_id),
                run_state,
                prepared.artifact,
            ).clear()
            save_run_state_checkpoint(run_state, self._paths_for(run_id).checkpoint_path)
            raise WebWorkflowError(
                "The codebook changed after this evidence packet was prepared. "
                "Prepare the artifact again before submitting a decision."
            )
        human_review_output = self._ground_human_review_evidence(
            prepared,
            human_review_output,
        )
        try:
            result = self._orchestrator_for(run_id).submit_prepared_review(
                run_state, prepared_review=prepared, human_review_output=human_review_output,
            )
        except ValueError:
            save_run_state_checkpoint(run_state, self._paths_for(run_id).checkpoint_path)
            raise
        run_state.status = (
            "awaiting_context"
            if human_review_output.decision == "request_additional_context"
            else "awaiting_next_artifact"
        )
        self._update_batch_progress(run_state)
        persist_artifact_completion(
            run_state=run_state,
            batch=prepared.batch,
            result=result,
            paths=self._paths_for(run_id),
        )
        self._prepared_reviews.pop(run_id, None)
        run_state.metadata.pop("awaiting_human_review", None)
        self._stage_store(
            run_id,
            self._orchestrator_for(run_id),
            run_state,
            prepared.artifact,
        ).clear()
        self._record_event(
            run_state,
            "artifact_review_submitted",
            artifact_id=result.artifact_id,
            decision=result.human_review_output.decision,
            duration_seconds=human_review_output.metadata.get("duration_seconds"),
            review_origin=prepared.review_origin,
        )
        self._record_event(
            run_state,
            "artifact_processing_finished",
            artifact_id=result.artifact_id,
            decision=result.human_review_output.decision,
            human_reviewed=True,
        )
        self._record_event(
            run_state,
            "iterative_paused",
            status=run_state.status,
            artifact_id=result.artifact_id,
        )
        save_run_state_checkpoint(run_state, self._paths_for(run_id).checkpoint_path)
        return {
            "artifact_id": result.artifact_id,
            "decision": result.human_review_output.decision,
            "codebook": serialize_codebook_state(run_state.codebook),
            "run": self.run_summary(run_id),
        }

    @staticmethod
    def _identify_reviewer(run_state: RunState, review: HumanReviewOutput) -> HumanReviewOutput:
        execution = run_state.metadata.get("study_execution", {})
        return replace(review, metadata={**review.metadata, **execution,
            "reviewer_id": execution.get("participant_id") or review.metadata.get("reviewer_id", "researcher")})

    @staticmethod
    def _ground_human_review_evidence(
        prepared: PreparedArtifactReview,
        review: HumanReviewOutput,
    ) -> HumanReviewOutput:
        """Canonicalize human-selected excerpts against the original artifact.

        Agent-selected evidence is never promoted to human-confirmed evidence.
        The web reviewer must explicitly select or enter grounded excerpts.
        """

        evidence = review.confirmed_evidence
        grounded: list[EvidenceItem] = []
        for item in evidence:
            if (
                item.field_name != "content"
                and item.field_name not in prepared.artifact.raw_fields
            ):
                raise ValueError(
                    f"Evidence field '{item.field_name}' does not exist in artifact "
                    f"{prepared.artifact.artifact_id}."
                )
            grounded.append(
                build_evidence_item(
                    prepared.artifact,
                    field_name=item.field_name,
                    excerpt=item.excerpt,
                    rationale=item.rationale,
                    rationale_zh=item.rationale_zh,
                    claim_type=item.claim_type,
                    revision=item.revision,
                )
            )
        if review.final_codes and not grounded:
            raise ValueError(
                "Every final code requires at least one human-confirmed structured evidence item."
            )
        evidence_summary = list(review.evidence_summary)
        if grounded and not evidence_summary:
            evidence_summary = [f"{item.field_name}: {item.excerpt}" for item in grounded]
        return replace(
            review,
            confirmed_evidence=grounded,
            evidence_summary=evidence_summary,
        )

    def next_artifact(self, run_id: str) -> dict[str, object]:
        run_state = self._load_run_state(run_id)
        if run_state.status != "awaiting_next_artifact":
            if run_state.status == "awaiting_context":
                raise WebWorkflowError(
                    "Resolve or cancel the pending context request before advancing."
                )
            raise WebWorkflowError("Submit a review before advancing to the next artifact.")
        advance_completed_batches(run_state)
        self._record_stabilization_check(run_state)
        paths = self._paths_for(run_id)
        if run_state.status == "completed":
            self._finish_iterative_coding(run_state)
        elif (
            run_state.review_policy.setting == "full"
            and self._review_budget_exhausted(run_state)
        ):
            self._mark_remaining_resource_limited(run_state)
        else:
            run_state.status = "in_progress"
        save_run_state_checkpoint(run_state, paths.checkpoint_path)
        if (
            run_state.review_policy.setting in {"automatic", "selective"}
            and run_state.status == "in_progress"
        ):
            return self.process_automatic(
                run_id,
                language=self._output_languages.get(run_id, "en"),
                # Keep one navigation request bounded to one LLM-processed
                # artifact. The client can continue immediately while each
                # completed artifact remains an independent recovery point.
                max_artifacts=1,
            )
        return {
            "run": self.run_summary(run_id),
            "current": self.current_artifact(run_id),
        }

    def _finish_iterative_coding(self, run_state: RunState) -> None:
        """Record operational stability before finalization or Final Review."""

        if run_state.review_policy.setting == "automatic":
            run_state.status = "in_progress"
            attempts = run_state.metadata.setdefault("automatic_reassessment_attempts", {})
            while pending := run_state.history.pending_retrospective_tasks():
                task = pending[0]
                count = int(attempts.get(task.artifact_id, 0))
                if count >= run_state.review_policy.automatic_reassessment_limit:
                    task.status = "cancelled"
                    task.metadata["cancellation_reason"] = "prespecified_reassessment_limit"
                    run_state.history.append_unresolved(UnresolvedCaseState(
                        unresolved_id=f"work-limit-{task.task_id}",
                        artifact_id=task.artifact_id,
                        reason="Automatic reassessment reached the prespecified work limit.",
                        source="automatic_reassessment_limit",
                        created_at_codebook_version=run_state.codebook.version,
                        metadata={"task_id": task.task_id, "attempt_count": count},
                    ))
                    continue
                attempts[task.artifact_id] = count + 1
                try:
                    self.prepare_retrospective_task(
                        run_state.run_id, task.task_id,
                        language=str(run_state.metadata.get("output_language", "en")),
                    )
                except Exception:
                    attempts[task.artifact_id] = count
                    run_state.status = "awaiting_next_artifact"
                    save_run_state_checkpoint(run_state, self._paths_for(run_state.run_id).checkpoint_path)
                    raise
        check = self._record_stabilization_check(run_state, final=True)
        try:
            self._run_final_validation(run_state, check)
        except Exception:
            # The next navigation/process request can resume a partial audit.
            # Do not persist a terminal status before validation finishes.
            run_state.status = "awaiting_next_artifact"
            save_run_state_checkpoint(run_state, self._paths_for(run_state.run_id).checkpoint_path)
            raise
        issues = completion_issues(serialize_run_state_checkpoint(run_state))
        if issues:
            run_state.status = "awaiting_next_artifact"
            save_run_state_checkpoint(run_state, self._paths_for(run_state.run_id).checkpoint_path)
            raise WebWorkflowError("Cannot finalize analysis: " + " ".join(issues))
        check = self._record_stabilization_check(run_state, final=True)
        paths = self._paths_for(run_state.run_id)
        if (
            run_state.review_policy.final_review_required
            and self._review_budget_exhausted(run_state)
        ):
            run_state.status = "resource_limited"
            run_state.notes.append(
                "Final Review was not completed because the frozen human-review budget was exhausted."
            )
        elif run_state.review_policy.final_review_required:
            run_state.status = "awaiting_final_review"
        else:
            run_state.status = "stabilized" if check.stable else "completed_with_unresolved"
            persist_final_codebook(run_state, paths.final_codebook_path)
            self._record_event(run_state, "outputs_frozen", codebook_version=run_state.codebook.version)

    def _run_final_validation(
        self,
        run_state: RunState,
        check: StabilizationCheckState,
    ) -> dict[str, object]:
        """Checkpoint final-definition checks independently of human acceptance."""

        artifacts = {
            item.artifact_id: item
            for item in self._adapter_for(run_state.dataset_metadata.dataset_name).iter_artifacts()
        }
        # Check before returning a cached audit too: an active backend must not
        # attest to changed source material merely because it was not restarted.
        self._verify_frozen_sources(run_state, artifacts)

        scope = self._final_review_artifact_scope(
            run_state, cross_source_ids=set(check.cross_source_audit_artifact_ids)
        )
        selected_ids = set(run_state.metadata.get("selected_artifact_ids", []))
        if not selected_ids:
            selected_ids = self._processed_artifact_ids(run_state) | {
                item.artifact_id for batch in run_state.coding_batches for item in batch.artifacts
            }
        latest = {
            artifact_id: run_state.history.latest_record_for_artifact(artifact_id)
            for artifact_id in selected_ids
        }
        unprocessed = sorted(artifact_id for artifact_id, record in latest.items() if record is None)
        frequencies = {
            code.code_id: sum(
                code.code_id in record.final_code_ids
                for record in latest.values() if record is not None
            ) for code in run_state.codebook.active_codes()
        }
        key = hashlib.sha256(json.dumps({
            "codebook": serialize_codebook_state(run_state.codebook),
            "records": [asdict(record) for _, record in sorted(latest.items()) if record],
            "scope": scope,
        }, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()
        audits = run_state.metadata.setdefault("final_validation_audits", {})
        fingerprint = decision_fingerprint(
            serialize_codebook_state(run_state.codebook),
            [asdict(row) for row in run_state.history.coding_records],
        )
        if (key in audits and audits[key].get("status") == "completed"
                and audits[key].get("decision_fingerprint") == fingerprint):
            return audits[key]
        if key in audits and audits[key].get("decision_fingerprint") != fingerprint:
            # Legacy completed audits are evidence of an earlier check, not a
            # current attestation. Keep them, then perform an actual re-audit.
            run_state.metadata.setdefault("legacy_final_validation_audits", []).append(audits.pop(key))
        audit: dict[str, object] = audits.get(key) or {
            "audit_id": key,
            "codebook_version": run_state.codebook.version,
            "coverage": scope,
            "unprocessed_artifact_ids": unprocessed,
            "category_assignment_counts": frequencies,
            "decision_fingerprint": decision_fingerprint(
                serialize_codebook_state(run_state.codebook),
                [asdict(row) for row in run_state.history.coding_records],
            ),
            "validation_outputs": [],
            "status": "running",
            "human_approved": False,
        }
        audits[key] = audit
        paths = self._paths_for(run_state.run_id)
        orchestrator = self._orchestrator_for(run_state.run_id)
        orchestrator.set_output_language(str(run_state.metadata.get("output_language", "en")))
        outputs = audit["validation_outputs"]
        completed_ids = {str(row["artifact_id"]) for row in outputs}
        self._record_event(run_state, "final_validation_started", audit_id=key)
        save_run_state_checkpoint(run_state, paths.checkpoint_path)
        for artifact_id in scope["review_artifact_ids"]:
            if artifact_id in completed_ids:
                continue
            artifact = artifacts.get(artifact_id)
            if artifact is None:
                raise WebWorkflowError(f"Final audit cannot reconstruct artifact {artifact_id}.")
            result = orchestrator.validate_final_record(
                run_state, artifact,
                corpus_audit={
                    "unprocessed_artifact_ids": unprocessed,
                    "category_assignment_counts": frequencies,
                    "pending_reassessments": [asdict(item) for item in run_state.history.pending_retrospective_tasks()],
                },
            )
            outputs.append(asdict(result))
            if result.review_criteria or result.human_review_required or any(
                signal.signal != "valid" for signal in result.signals
            ):
                run_state.history.append_unresolved(UnresolvedCaseState(
                    unresolved_id=f"final-audit-{key[:12]}-{artifact_id}",
                    artifact_id=artifact_id,
                    reason=result.summary or "Final validation requires further assessment.",
                    source="final_validation",
                    created_at_codebook_version=run_state.codebook.version,
                    metadata={"audit_id": key, "review_criteria": result.review_criteria},
                ))
            save_run_state_checkpoint(run_state, paths.checkpoint_path)
        audit["status"] = "completed"
        self._record_event(run_state, "final_validation_finished", audit_id=key)
        save_run_state_checkpoint(run_state, paths.checkpoint_path)
        return audit

    def _record_stabilization_check(
        self,
        run_state: RunState,
        *,
        final: bool = False,
    ) -> StabilizationCheckState:
        """Append one frozen-window operational stability observation."""

        record_count = len(run_state.history.coding_records)
        configured_window = run_state.review_policy.stabilization_window_size
        window_size = min(configured_window, max(1, record_count))
        round_cutoff = max(0, record_count - window_size)
        recent_revisions = [
            revision
            for revision in run_state.history.codebook_revisions
            if revision.round_index >= round_cutoff
        ]
        open_unresolved = len(run_state.history.open_unresolved_cases())
        pending_retrospective = len(run_state.history.pending_retrospective_tasks())
        recent_new = sum(
            revision.action in {"add", "add_parent"} for revision in recent_revisions
        )
        recent_substantive = sum(
            revision.action in {"refine", "merge", "split"}
            for revision in recent_revisions
        )
        reasons: list[str] = []
        if recent_new:
            reasons.append("Recent coding still introduced new categories.")
        if recent_substantive:
            reasons.append("Recent coding still changed category meaning or boundaries.")
        if open_unresolved:
            reasons.append("Open unresolved cases remain.")
        if pending_retrospective:
            reasons.append("Retrospective propagation tasks remain incomplete.")
        audit_status, audit_ids = self._cross_source_audit(run_state, final=final)
        if audit_status == "incomplete":
            reasons.append("Cross-source audit cases have not all been processed.")
        local_stable = not reasons
        previous = (
            run_state.history.stabilization_checks[-1]
            if run_state.history.stabilization_checks
            else None
        )
        if not local_stable:
            consecutive_stable = 0
        elif previous is None:
            consecutive_stable = 1
        elif len(self._processed_artifact_ids(run_state)) > previous.processed_artifacts:
            consecutive_stable = previous.consecutive_stable_batches + 1
        else:
            # A final/reporting check over the same processed batch is not a new
            # stability observation and must not satisfy the consecutive window.
            consecutive_stable = previous.consecutive_stable_batches
        required_consecutive = (
            run_state.review_policy.stabilization_required_consecutive_batches
        )
        check = StabilizationCheckState(
            check_id=f"stability-{uuid4().hex[:12]}",
            codebook_version=run_state.codebook.version,
            processed_artifacts=len(self._processed_artifact_ids(run_state)),
            remaining_artifacts=max(
                0,
                self._input_artifact_count(run_state)
                - len(self._processed_artifact_ids(run_state)),
            ),
            open_unresolved_count=open_unresolved,
            pending_retrospective_count=pending_retrospective,
            recent_new_code_count=recent_new,
            recent_substantive_revision_count=recent_substantive,
            window_size=window_size,
            stable=local_stable and consecutive_stable >= required_consecutive,
            consecutive_stable_batches=consecutive_stable,
            cross_source_audit_status=audit_status,
            cross_source_audit_artifact_ids=audit_ids,
            reasons=reasons or ["No configured instability signal remained."],
            metadata={
                "claim": "coding_stabilization_not_theoretical_saturation",
                "configured_window_size": configured_window,
                "required_consecutive_stable_batches": required_consecutive,
                "final_check": final,
            },
        )
        comparable_fields = (
            "codebook_version",
            "processed_artifacts",
            "remaining_artifacts",
            "open_unresolved_count",
            "pending_retrospective_count",
            "recent_new_code_count",
            "recent_substantive_revision_count",
            "window_size",
            "stable",
            "consecutive_stable_batches",
            "cross_source_audit_status",
            "cross_source_audit_artifact_ids",
            "reasons",
            "metadata",
        )
        if previous is None or any(
            getattr(previous, field_name) != getattr(check, field_name)
            for field_name in comparable_fields
        ):
            run_state.history.append_stabilization_check(check)
        return check

    @staticmethod
    def _final_review_artifact_scope(
        run_state: RunState,
        *,
        cross_source_ids: set[str],
    ) -> dict[str, object]:
        """Build the explicit Final Review evidence coverage manifest."""

        processed_ids = CodaWebService._processed_artifact_ids(run_state)
        latest_records = {
            artifact_id: record
            for artifact_id in processed_ids
            if (record := run_state.history.latest_record_for_artifact(artifact_id))
            is not None
        }

        flagged_ids: set[str] = set()
        for artifact_id, record in latest_records.items():
            metadata = record.metadata if isinstance(record.metadata, dict) else {}
            routing = metadata.get("routing_decision", {})
            if not isinstance(routing, dict):
                routing = {}
            signal_details = routing.get("signal_details", {})
            if not isinstance(signal_details, dict):
                signal_details = {}
            criteria = signal_details.get("review_criteria", [])
            risk_signals = routing.get("risk_signals", [])
            if (
                bool(criteria)
                or bool(risk_signals)
                or routing.get("review_origin") == "risk_criterion"
            ):
                flagged_ids.add(artifact_id)

        low_frequency_ids = {
            artifact_id
            for code in run_state.codebook.active_codes()
            if sum(code.code_id in record.final_code_ids for record in latest_records.values()) <= 1
            for artifact_id, record in latest_records.items()
            if code.code_id in record.final_code_ids
        }
        reassessment_ids = {
            task.artifact_id for task in run_state.history.retrospective_tasks
        }
        unflagged_ids = processed_ids - flagged_ids
        audit_count = max(1, math.ceil(len(unflagged_ids) * 0.10)) if unflagged_ids else 0
        ordered_unflagged = sorted(
            unflagged_ids,
            key=lambda artifact_id: hashlib.sha256(
                f"{run_state.review_policy.random_seed}:final:{artifact_id}".encode(
                    "utf-8"
                )
            ).hexdigest(),
        )
        unflagged_audit_ids = set(ordered_unflagged[:audit_count])
        historical_candidates = unflagged_ids - reassessment_ids
        ordered_historical = sorted(
            historical_candidates,
            key=lambda artifact_id: hashlib.sha256(
                f"{run_state.review_policy.random_seed}:historical:{artifact_id}".encode(
                    "utf-8"
                )
            ).hexdigest(),
        )
        historical_audit_ids = set(ordered_historical[:audit_count])
        review_ids = (
            set(cross_source_ids)
            | low_frequency_ids
            | flagged_ids
            | unflagged_audit_ids
            | historical_audit_ids
        ) & processed_ids
        return {
            "rule": (
                "Final Review includes cross-source cases, low-frequency code "
                "representatives, flagged cases, a deterministic 10% unflagged "
                "audit, and historical cases outside reassessment tasks."
            ),
            "review_artifact_ids": sorted(review_ids),
            "cross_source_artifact_ids": sorted(set(cross_source_ids) & processed_ids),
            "low_frequency_artifact_ids": sorted(low_frequency_ids),
            "flagged_artifact_ids": sorted(flagged_ids),
            "unflagged_audit_artifact_ids": sorted(unflagged_audit_ids),
            "historical_audit_artifact_ids": sorted(historical_audit_ids),
            "reassessment_artifact_ids": sorted(reassessment_ids & processed_ids),
            "processed_artifact_ids": sorted(processed_ids),
        }

    def _cross_source_audit(
        self,
        run_state: RunState,
        *,
        final: bool,
    ) -> tuple[str, list[str]]:
        """Select one deterministic processed case per visible source for auditing."""

        selected_ids = {
            str(item) for item in run_state.metadata.get("selected_artifact_ids", [])
        }
        artifacts = [
            artifact
            for artifact in self._adapter_for(
                run_state.dataset_metadata.dataset_name
            ).iter_artifacts()
            if not selected_ids or artifact.artifact_id in selected_ids
        ]
        by_source: dict[str, list[str]] = {}
        for artifact in artifacts:
            source = str(artifact.metadata.get("repo_name", "")).strip()
            if not source:
                source = (
                    f"source-kind:{artifact.source_refs[0].kind}"
                    if artifact.source_refs
                    else "dataset"
                )
            by_source.setdefault(source, []).append(artifact.artifact_id)
        if len(by_source) <= 1:
            return "not_applicable_single_source", []
        processed = self._processed_artifact_ids(run_state)
        audit_ids = [
            min(
                ids,
                key=lambda artifact_id: hashlib.sha256(
                    f"{run_state.review_policy.random_seed}:{artifact_id}".encode(
                        "utf-8"
                    )
                ).hexdigest(),
            )
            for ids in by_source.values()
        ]
        if not final:
            return "pending_until_final_review", audit_ids
        if set(audit_ids) <= processed:
            if run_state.review_policy.final_review_required:
                return "presented_for_final_review", audit_ids
            return "automatic_validation_coverage", audit_ids
        return "incomplete", audit_ids

    @staticmethod
    def _human_review_seconds(run_state: RunState) -> float:
        """Return recorded human time across stage and artifact reviews."""

        total = sum(
            review.duration_seconds or 0.0
            for review in run_state.history.stage_reviews
        )
        for record in run_state.history.coding_records:
            if record.metadata.get("human_reviewed", True) is not True:
                continue
            duration = record.metadata.get("duration_seconds")
            if isinstance(duration, (int, float)) and duration >= 0:
                total += float(duration)
        return round(total, 3)

    @staticmethod
    def _evidence_audit_metrics(run_state: RunState) -> dict[str, int]:
        """Aggregate explicit span decisions without inferring unseen omissions."""

        totals = {
            "review_records": 0,
            "explicitly_assessed_records": 0,
            "agent_candidate_count": 0,
            "human_confirmed_candidate_count": 0,
            "human_added_count": 0,
            "agent_candidates_not_confirmed_count": 0,
        }
        for record in run_state.history.coding_records:
            audit = record.metadata.get("evidence_unit_audit")
            if not isinstance(audit, dict):
                continue
            totals["review_records"] += 1
            if audit.get("status") == "assessed":
                totals["explicitly_assessed_records"] += 1
            for key in (
                "agent_candidate_count",
                "human_confirmed_candidate_count",
                "human_added_count",
                "agent_candidates_not_confirmed_count",
            ):
                totals[key] += int(audit.get(key, 0))
        return totals

    @classmethod
    def _review_budget_exhausted(cls, run_state: RunState) -> bool:
        budget = run_state.review_policy.review_budget_minutes
        return budget is not None and cls._human_review_seconds(run_state) >= budget * 60

    @staticmethod
    def _budget_exhausted_output(
        prepared_review: PreparedArtifactReview,
    ) -> HumanReviewOutput:
        """Preserve a routed case as unresolved when no human budget remains."""

        routing = prepared_review.evidence_packet.routing_decision
        reasons = routing.reasons + routing.risk_signals if routing is not None else []
        return HumanReviewOutput(
            artifact_id=prepared_review.artifact_id,
            decision="mark_uncertain",
            pre_read_memo="Human review was required, but the frozen review budget was exhausted.",
            rationale=(
                "Review budget exhausted; this case remains unresolved."
                + (f" Routing signals: {'; '.join(reasons)}" if reasons else "")
            ),
            metadata={
                "review_origin": "automatic_unresolved",
                "human_reviewed": False,
                "resource_limit": "review_budget_exhausted",
                "routing_decision": asdict(routing) if routing is not None else None,
            },
        )

    def _mark_remaining_resource_limited(self, run_state: RunState) -> None:
        """Stop a Full Review run without treating untouched cases as accepted."""

        existing = {
            item.artifact_id
            for item in run_state.history.open_unresolved_cases()
            if item.metadata.get("resource_limit") == "review_budget_exhausted"
        }
        for batch in run_state.coding_batches[run_state.current_batch_index :]:
            for artifact in pending_artifacts_for_batch(batch, run_state):
                if artifact.artifact_id in existing:
                    continue
                run_state.history.append_unresolved(
                    UnresolvedCaseState(
                        unresolved_id=f"unresolved-{uuid4().hex[:12]}",
                        artifact_id=artifact.artifact_id,
                        reason="Human review budget was exhausted before this artifact could be reviewed.",
                        source="resource_limit",
                        created_at_codebook_version=run_state.codebook.version,
                        metadata={"resource_limit": "review_budget_exhausted"},
                    )
                )
        run_state.status = "resource_limited"
        run_state.notes.append(
            "Full Review stopped because the frozen human-review budget was exhausted; remaining artifacts are unresolved."
        )

    def _restore_bootstrap_queue(self, run_state: RunState) -> None:
        """Put sampled artifacts back when Initial Review rejects induction."""

        bootstrap = run_state.metadata.get("bootstrap", {})
        sampled_ids = (
            set(str(item) for item in bootstrap.get("artifact_ids", []))
            if isinstance(bootstrap, dict)
            else set()
        )
        if not sampled_ids:
            return
        run_state.metadata.setdefault("rejected_initializations", []).append({
            "codebook": serialize_codebook_state(run_state.codebook),
            "coding_records": [asdict(record) for record in run_state.history.coding_records
                               if record.metadata.get("review_origin") == "bootstrap_provisional"],
            "analytic_memos": [memo for memo in run_state.history.analytic_memos
                               if memo.get("origin") == "bootstrap_induction"],
            "validation_issues": [asdict(item) for item in run_state.history.unresolved_cases
                                  if item.source == "bootstrap_validation"],
        })
        run_state.history.coding_records = [
            record
            for record in run_state.history.coding_records
            if record.metadata.get("review_origin") != "bootstrap_provisional"
        ]
        run_state.history.analytic_memos = [
            memo
            for memo in run_state.history.analytic_memos
            if memo.get("origin") != "bootstrap_induction"
        ]
        selected_ids = {
            str(item) for item in run_state.metadata.get("selected_artifact_ids", [])
        }
        desired_ids = selected_ids or (
            sampled_ids
            | {
                artifact.artifact_id
                for batch in run_state.coding_batches
                for artifact in batch.artifacts
            }
        )
        artifacts = [
            artifact
            for artifact in self._adapter_for(
                run_state.dataset_metadata.dataset_name
            ).iter_artifacts()
            if artifact.artifact_id in desired_ids
        ]
        group_ids = {
            artifact.artifact_id: artifact.artifact_id for artifact in artifacts
        }
        self._set_iterative_micro_batches(
            run_state,
            artifacts,
            group_ids=group_ids,
        )

    @staticmethod
    def _set_iterative_micro_batches(
        run_state: RunState,
        artifacts: list[ArtifactRecord],
        *,
        group_ids: dict[str, str],
    ) -> None:
        """Partition new runs; legacy runs default to one-artifact batches.

        The historical method name remains for compatibility. Multi-case batches
        execute through the shared-snapshot reconciliation barrier, not through
        the old sequential comparison path.
        """

        dataset_name = run_state.dataset_metadata.dataset_name
        artifact_ids = [artifact.artifact_id for artifact in artifacts]
        sampling_manifest = run_state.metadata.get("review_sampling_manifest")
        manifest_ids = (
            [str(item) for item in sampling_manifest.get("population_artifact_ids", [])]
            if isinstance(sampling_manifest, dict)
            else []
        )
        sampling_block_size = int(
            run_state.metadata.get("review_sampling_protocol", {}).get(
                "sampling_block_size", 10
            )
        )
        if run_state.review_policy.setting == "selective" and sampling_manifest is None:
            # Keep the manifest shape for reproducibility and old readers;
            # routing disables draws entirely for batch_size=1 runs.
            run_state.metadata["review_sampling_manifest"] = {
                "setting": "selective",
                "population_artifact_ids": list(artifact_ids),
                "sampled_artifact_ids": [],
                "sample_size": 0,
                "sampling_window_size": sampling_block_size,
                "requested_rate": run_state.review_policy.random_audit_rate,
                "seed": run_state.review_policy.random_seed,
                "rule": (
                    "one stable random-rank audit per complete window of ten "
                    "otherwise-unflagged decisions; execution micro-batches are independent"
                ),
                "streams": {
                    "current": {
                        "eligible_decision_count": 0,
                        "decisions": {},
                        "completed_windows": [],
                        "sampled_artifact_ids": [],
                    },
                    "retrospective": {
                        "eligible_decision_count": 0,
                        "decisions": {},
                        "completed_windows": [],
                        "sampled_artifact_ids": [],
                    },
                },
            }
        elif run_state.review_policy.setting == "selective":
            # The sampling manifest is part of the frozen experimental
            # protocol. A restarted run may reuse it, but must never silently
            # redraw it because a queue or policy value changed.
            if not isinstance(sampling_manifest, dict) or not (
                sampling_manifest.get("sampling_window_size")
                or isinstance(sampling_manifest.get("blocks"), list)
            ):
                raise WebWorkflowError(
                    "The selective-review sampling manifest is missing or invalid; "
                    "the run must be restored from its original checkpoint."
                )
            if manifest_ids != artifact_ids:
                raise WebWorkflowError(
                    "The selective-review artifact population changed after sampling "
                    "was frozen; refusing to redraw the review sample."
                )
            if "sampling_window_size" in sampling_manifest:
                persisted_block_size = int(
                    sampling_manifest.get("sampling_window_size", sampling_block_size)
                )
                if persisted_block_size != sampling_block_size:
                    raise WebWorkflowError(
                        "The selective-review sampling window size changed after it was frozen."
                    )
            sampled_ids = sampling_manifest.get("sampled_artifact_ids", [])
            if not isinstance(sampled_ids, list) or not set(
                str(item) for item in sampled_ids
            ).issubset(set(artifact_ids)):
                raise WebWorkflowError(
                    "The selective-review sampling manifest contains unknown artifact IDs."
                )
        elif run_state.review_policy.setting != "selective":
            run_state.metadata.pop("review_sampling_manifest", None)
        sampling_manifest = run_state.metadata.get("review_sampling_manifest", {})
        if isinstance(sampling_manifest, dict) and sampling_manifest:
            enabled = CODAOrchestrator._selective_sampling_enabled(run_state)
            sampling_manifest["effective_rate"] = run_state.review_policy.random_audit_rate if enabled else 0.0
            sampling_manifest["random_audit_enabled"] = enabled
            sampling_manifest["disabled_reason"] = None if enabled else "configured_iterative_batch_size_is_one"
        sampled_ids = (
            {str(item) for item in sampling_manifest.get("sampled_artifact_ids", [])}
            if isinstance(sampling_manifest, dict)
            else set()
        )
        size = int(run_state.metadata.get("iterative_batch_protocol", {}).get("batch_size", 1))
        chunks = [artifacts[offset:offset + size] for offset in range(0, len(artifacts), size)]
        run_state.coding_batches = [
            ArtifactBatchState(
                batch_id=f"batch-{dataset_name}-{index}",
                dataset_name=dataset_name,
                batch_index=index,
                split_name="coding_pool",
                artifacts=members,
                group_ids={
                    artifact.artifact_id: group_ids.get(
                        artifact.artifact_id, artifact.artifact_id
                    ) for artifact in members
                },
                sampling_note="Shared-snapshot initial comparisons; batch reconciliation precedes validation and review.",
                metadata={
                    "commit_policy": "accepted_decisions_with_stale_proposal_recheck" if size > 1 else "commit_after_batch",
                    "shared_snapshot_reconciliation": size > 1,
                    "selective_random_audit_ids": (
                        [artifact.artifact_id for artifact in members if artifact.artifact_id in sampled_ids]
                        if size > 1 else []
                    ),
                    "selective_random_audit_sample_size": len(sampled_ids) if size > 1 else 0,
                    "selective_random_audit_rule": (
                        "assigned when this artifact becomes the selected rank in a "
                        "complete window of ten otherwise-unflagged decisions"
                    ),
                },
            )
            for index, members in enumerate(chunks)
        ]
        run_state.current_batch_index = 0

    @staticmethod
    def _register_bootstrap_state(
        run_state: RunState,
        result: BootstrapResult,
    ) -> None:
        """Expose provisional initialization evidence to later constant comparison."""

        for packet in result.context_packets:
            artifact_id = packet.get("artifact_id")
            if artifact_id:
                run_state.metadata.setdefault("case_materials", {}).setdefault(
                    artifact_id, {}
                )["context_packet"] = packet
        # Exhausted substantive revisions leave affected initial cases explicit;
        # provisional assignments are never a substitute for resolved validation.
        for output in result.validation_outputs:
            if any(signal.signal != "valid" for signal in output.signals) or any(
                criterion in {"R1", "R2", "R3", "R6"} for criterion in output.review_criteria
            ):
                run_state.history.append_unresolved(UnresolvedCaseState(
                    unresolved_id=f"bootstrap-validation-{uuid4().hex[:12]}",
                    artifact_id=output.artifact_id,
                    reason=output.summary or "Initial validation remained unresolved after the work limit.",
                    source="bootstrap_validation", created_at_codebook_version=result.codebook.version,
                    metadata={"validation_output": asdict(output), "work_limit_exhausted": True},
                ))
        code_names = {code.code_id: code.name for code in result.codebook.codes}
        invalid_ids = {
            output.artifact_id for output in result.validation_outputs
            if any(signal.signal != "valid" for signal in output.signals)
            or any(criterion in {"R1", "R2", "R3", "R6"} for criterion in output.review_criteria)
        }
        existing_ids = set(run_state.history.reviewed_artifact_ids())
        for assignment in result.assignments:
            if assignment.artifact_id in existing_ids:
                continue
            run_state.history.append_record(
                CodingRecordState(
                    record_id=f"bootstrap-{uuid4().hex[:12]}",
                    artifact_id=assignment.artifact_id,
                    dataset_name=run_state.dataset_metadata.dataset_name,
                    batch_index=0,
                    codebook_version=result.codebook.version,
                    decision="mark_uncertain" if assignment.status.startswith("unresolved_") or assignment.artifact_id in invalid_ids else "accept",
                    final_code_ids=[] if assignment.artifact_id in invalid_ids else list(assignment.code_ids),
                    final_code_names=[
                        code_names[code_id]
                        for code_id in ([] if assignment.artifact_id in invalid_ids else assignment.code_ids)
                        if code_id in code_names
                    ],
                    rationale=(
                        "Provisional assignment generated during initial category induction; "
                        "it has not been accepted by a human reviewer."
                    ),
                    evidence_summary=list(assignment.evidence_summary),
                    metadata={
                        "review_origin": "bootstrap_provisional",
                        "provenance": "agent_generated",
                        "human_reviewed": False,
                        "assignment_status": assignment.status,
                    },
                )
            )
        for memo in result.analytic_memos:
            run_state.history.append_analytic_memo(
                {
                    **dict(memo),
                    "origin": "bootstrap_induction",
                    "human_reviewed": False,
                    "codebook_version": result.codebook.version,
                }
            )

    @staticmethod
    def _bootstrap_artifact_ids(run_state: RunState) -> set[str]:
        bootstrap = run_state.metadata.get("bootstrap", {})
        if not isinstance(bootstrap, dict) or bootstrap.get("status") != "completed":
            return set()
        return {str(item) for item in bootstrap.get("artifact_ids", [])}

    @classmethod
    def _processed_artifact_ids(cls, run_state: RunState) -> set[str]:
        return set(run_state.history.reviewed_artifact_ids()) | cls._bootstrap_artifact_ids(
            run_state
        )

    @staticmethod
    def _input_artifact_count(run_state: RunState) -> int:
        bootstrap = run_state.metadata.get("bootstrap", {})
        if isinstance(bootstrap, dict):
            return int(bootstrap.get("population_size", run_state.total_coding_artifacts))
        return run_state.total_coding_artifacts

    def codebook(self, run_id: str) -> dict[str, object]:
        return serialize_codebook_state(self._load_run_state(run_id).codebook)

    def codebook_versions(self, run_id: str) -> dict[str, object]:
        """Return immutable version snapshots and explicit adjacent diffs."""

        run_state = self._load_run_state(run_id)
        paths = self._paths_for(run_id)
        persist_codebook_snapshot(run_state, paths.codebook_snapshot_dir)
        snapshots: list[dict[str, object]] = []
        for path in sorted(paths.codebook_snapshot_dir.glob("codebook-v*.json")):
            payload = self._read_json_object(path)
            if payload is not None:
                snapshots.append(payload)
        diffs: list[dict[str, object]] = []
        for before, after in zip(snapshots, snapshots[1:]):
            diffs.append(self._codebook_diff(before, after))
        return {"snapshots": snapshots, "diffs": diffs}

    def code_artifacts(self, run_id: str, code_id: str) -> dict[str, object]:
        """Return reviewed artifacts assigned to one current or historical code."""

        run_state = self._load_run_state(run_id)
        code = run_state.codebook.get_code(code_id)
        if code is None:
            raise WebWorkflowError(f"Code '{code_id}' does not exist in this codebook.")
        adapter = self._adapter_for(run_state.dataset_metadata.dataset_name)
        artifacts_by_id = {artifact.artifact_id: artifact for artifact in adapter.iter_artifacts()}
        records_by_id = {
            record.artifact_id: record
            for record in run_state.history.coding_records
            if code_id in record.final_code_ids
        }
        artifact_ids = list(dict.fromkeys([
            *records_by_id,
            *code.representative_artifact_ids,
        ]))
        items: list[dict[str, object]] = []
        for artifact_id in artifact_ids:
            artifact = artifacts_by_id.get(artifact_id)
            if artifact is None:
                continue
            record = records_by_id.get(artifact_id)
            items.append({
                "artifact": asdict(artifact),
                "review": asdict(record) if record is not None else None,
            })
        return {
            "codebook_version": run_state.codebook.version,
            "code": asdict(code),
            "artifact_count": len(items),
            "artifacts": items,
        }

    def history(self, run_id: str) -> dict[str, object]:
        run_state = self._load_run_state(run_id)
        history = serialize_run_state_checkpoint(run_state)["history"]
        if not isinstance(history, dict):
            raise WebWorkflowError("Run history has an invalid checkpoint representation.")
        return {
            **history,
            # The checkpoint is authoritative for the human decision timeline.
            # The JSONL trace supplies the persisted agent-side artifact outputs
            # when a researcher needs to inspect an already completed review.
            "artifact_runs": self._read_jsonl(self._paths_for(run_id).artifact_log_path),
            "codebook_versions": self.codebook_versions(run_id),
        }

    def context_requests(self, run_id: str) -> dict[str, object]:
        run_state = self._load_run_state(run_id)
        return {
            "run_id": run_id,
            "requests": [asdict(item) for item in run_state.history.context_requests],
            "pending_count": len(run_state.history.pending_context_requests()),
        }

    def update_analytic_memo_status(
        self,
        run_id: str,
        memo_id: str,
        *,
        status: str,
        rationale: str,
    ) -> dict[str, object]:
        """Resolve or reopen a memo while retaining its complete status history."""

        if status not in {"open", "resolved"}:
            raise WebWorkflowError("Memo status must be 'open' or 'resolved'.")
        if not rationale.strip():
            raise WebWorkflowError("A memo status change requires a rationale.")
        run_state = self._load_run_state(run_id)
        memo = run_state.history.analytic_memo(memo_id)
        if memo is None:
            raise WebWorkflowError(f"Analytic memo '{memo_id}' does not exist.")
        previous = str(memo.get("status", "open"))
        if previous == status:
            raise WebWorkflowError(f"Analytic memo '{memo_id}' is already {status}.")
        history = memo.setdefault("status_history", [])
        if not isinstance(history, list):
            history = []
            memo["status_history"] = history
        history.append(
            {
                "from": previous,
                "status": status,
                "rationale": rationale.strip(),
                "reviewer_id": "researcher",
                "codebook_version": run_state.codebook.version,
            }
        )
        memo["status"] = status
        memo["resolution"] = rationale.strip() if status == "resolved" else ""
        memo["updated_by"] = "researcher"
        save_run_state_checkpoint(run_state, self._paths_for(run_id).checkpoint_path)
        return {"run_id": run_id, "memo": dict(memo)}

    def resolve_context_request(
        self,
        run_id: str,
        request_id: str,
        *,
        supplied_context: list[str],
        resolution: str,
    ) -> dict[str, object]:
        run_state = self._load_run_state(run_id)
        request = next(
            (item for item in run_state.history.context_requests if item.request_id == request_id),
            None,
        )
        if request is None:
            raise WebWorkflowError(f"Context request '{request_id}' does not exist.")
        if request.status != "pending":
            raise WebWorkflowError(f"Context request '{request_id}' is no longer pending.")
        cleaned = [item.strip() for item in supplied_context if item.strip()]
        if not cleaned:
            raise WebWorkflowError("At least one supplied context item is required.")
        if not resolution.strip():
            raise WebWorkflowError("A context resolution note is required.")
        retrospective_task = None
        retrospective_task_id = request.metadata.get("retrospective_task_id")
        if (
            request.scope == "artifact"
            and isinstance(retrospective_task_id, str)
            and retrospective_task_id
        ):
            retrospective_task = run_state.history.retrospective_task(
                retrospective_task_id
            )
            if retrospective_task is None:
                raise WebWorkflowError(
                    f"Retrospective task '{retrospective_task_id}' does not exist."
                )

        # Validate all referenced state before mutating the in-memory checkpoint.
        request.status = "resolved"
        request.supplied_context = cleaned
        request.resolution = resolution.strip()
        request.metadata["resolved_by"] = "researcher"
        if request.scope == "artifact" and request.artifact_id:
            if retrospective_task is not None:
                retrospective_task.status = "pending"
                for unresolved in run_state.history.unresolved_cases:
                    if (
                        unresolved.metadata.get("record_id")
                        == request.metadata.get("record_id")
                        and unresolved.status == "open"
                    ):
                        unresolved.status = "resolved"
                        unresolved.resolution = request.resolution
                save_run_state_checkpoint(
                    run_state, self._paths_for(run_id).checkpoint_path
                )
                return self.context_requests(run_id)
            matching_batch_index = next(
                (
                    index
                    for index, batch in enumerate(run_state.coding_batches)
                    if request.artifact_id in batch.artifact_ids
                ),
                None,
            )
            if matching_batch_index is not None:
                run_state.current_batch_index = min(
                    run_state.current_batch_index,
                    matching_batch_index,
                )
            reopened = run_state.metadata.setdefault("reopened_context_artifact_ids", [])
            if request.artifact_id not in reopened:
                reopened.append(request.artifact_id)
            for unresolved in run_state.history.unresolved_cases:
                if unresolved.artifact_id == request.artifact_id and unresolved.status == "open":
                    unresolved.status = "resolved"
                    unresolved.resolution = request.resolution
            if any(
                item.scope == "artifact" and item.status == "pending"
                for item in run_state.history.context_requests
            ):
                run_state.status = "awaiting_context"
            else:
                run_state.status = "in_progress"
            final_path = self._paths_for(run_id).final_codebook_path
            if final_path.exists():
                final_path.unlink()
        elif request.scope == "initial":
            run_state.status = "awaiting_initial_review"
        elif request.scope == "final":
            run_state.status = "awaiting_final_review"
        save_run_state_checkpoint(run_state, self._paths_for(run_id).checkpoint_path)
        return self.context_requests(run_id)

    def cancel_context_request(self, run_id: str, request_id: str) -> dict[str, object]:
        run_state = self._load_run_state(run_id)
        request = next(
            (item for item in run_state.history.context_requests if item.request_id == request_id),
            None,
        )
        if request is None:
            raise WebWorkflowError(f"Context request '{request_id}' does not exist.")
        if request.status != "pending":
            raise WebWorkflowError(f"Context request '{request_id}' is no longer pending.")
        retrospective_task = None
        retrospective_task_id = request.metadata.get("retrospective_task_id")
        if (
            request.scope == "artifact"
            and isinstance(retrospective_task_id, str)
            and retrospective_task_id
        ):
            retrospective_task = run_state.history.retrospective_task(
                retrospective_task_id
            )
            if retrospective_task is None:
                raise WebWorkflowError(
                    f"Retrospective task '{retrospective_task_id}' does not exist."
                )

        # A failed reference check must leave both the request and queue untouched.
        request.status = "cancelled"
        request.resolution = "Cancelled by researcher."
        if request.scope == "artifact" and request.artifact_id:
            previous = run_state.history.latest_record_for_artifact(request.artifact_id)
            if previous is not None and previous.decision == "request_additional_context":
                run_state.history.append_record(replace(
                    previous, record_id=f"context-cancelled-{uuid4().hex[:12]}",
                    decision="mark_uncertain", final_code_ids=[],
                    rationale="Context request cancelled by researcher; interpretation remains unresolved.",
                    metadata={**previous.metadata, "human_reviewed": False, "duration_seconds": 0,
                              "review_origin": "context_cancellation",
                              "supersedes_record_id": previous.record_id,
                              "context_request_id": request.request_id},
                ))
        if retrospective_task is not None:
            # Cancelling accepts the unresolved retrospective record as the
            # terminal outcome; it must not reopen the ordinary artifact queue.
            retrospective_task.status = "completed"
            if (
                run_state.status == "awaiting_final_review"
                and not run_state.history.pending_retrospective_tasks()
            ):
                self._finish_iterative_coding(run_state)
        elif request.scope == "artifact" and run_state.status == "awaiting_context":
            # Cancellation explicitly accepts the unresolved record as-is and
            # releases the ordinary queue.  The unresolved case remains in
            # history and therefore still affects final stability checks.
            if not any(
                item.scope == "artifact" and item.status == "pending"
                for item in run_state.history.context_requests
            ):
                run_state.status = "awaiting_next_artifact"
        self._update_batch_progress(run_state)
        save_run_state_checkpoint(run_state, self._paths_for(run_id).checkpoint_path)
        return self.context_requests(run_id)

    def _codebook_diff(
        self,
        before: dict[str, object],
        after: dict[str, object],
    ) -> dict[str, object]:
        before_codes = {
            str(code["code_id"]): code
            for code in before.get("codes", [])
            if isinstance(code, dict) and "code_id" in code
        }
        after_codes = {
            str(code["code_id"]): code
            for code in after.get("codes", [])
            if isinstance(code, dict) and "code_id" in code
        }
        added = [after_codes[key] for key in sorted(after_codes.keys() - before_codes.keys())]
        removed = [before_codes[key] for key in sorted(before_codes.keys() - after_codes.keys())]
        changed = [
            {"before": before_codes[key], "after": after_codes[key]}
            for key in sorted(before_codes.keys() & after_codes.keys())
            if before_codes[key] != after_codes[key]
        ]
        return {
            "from_version": before.get("version"),
            "to_version": after.get("version"),
            "added": added,
            "removed": removed,
            "changed": changed,
        }

    def run_artifacts(self, run_id: str) -> dict[str, object]:
        """Return persisted run files as read-only research inspection data."""

        run_state = self._load_run_state(run_id)
        paths = self._paths_for(run_id)
        final_codebook = self._read_json_object(paths.final_codebook_path)
        return {
            "checkpoint": {
                "format": "coda-run-checkpoint",
                "format_version": 1,
                "run_id": run_state.run_id,
                "dataset_name": run_state.dataset_metadata.dataset_name,
                "status": run_state.status,
                "current_batch_index": run_state.current_batch_index,
                "coding_batch_count": len(run_state.coding_batches),
                "review_count": len(run_state.history.coding_records),
                "codebook_version": run_state.codebook.version,
                "code_count": len(run_state.codebook.codes),
                "bootstrap": dict(run_state.metadata.get("bootstrap", {})),
            },
            "reviews": self._read_jsonl(paths.review_log_path),
            "artifact_runs": self._read_jsonl(paths.artifact_log_path),
            "bootstrap": self._read_json_object(paths.bootstrap_manifest_path),
            "final_codebook": {
                "available": final_codebook is not None,
                "snapshot": final_codebook,
            },
        }

    def _read_jsonl(self, path: Path) -> list[dict[str, object]]:
        if not path.exists():
            return []
        records: list[dict[str, object]] = []
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            try:
                payload = json.loads(line)
            except json.JSONDecodeError as error:
                raise WebWorkflowError(
                    f"Invalid JSONL record in {path.name} at line {line_number}."
                ) from error
            if not isinstance(payload, dict):
                raise WebWorkflowError(
                    f"Invalid JSONL record in {path.name} at line {line_number}."
                )
            records.append(payload)
        return records

    @staticmethod
    def _pending_bootstrap_metadata(population_size: int) -> dict[str, object]:
        """Describe the fixed protocol before it has made any model request."""

        config = BootstrapConfig.from_env()
        protocol = {**asdict(config), "population_size": population_size}
        return {
            "enabled": True,
            "status": "not_run",
            "artifact_ids": [],
            "code_count": 0,
            "human_reviewed": False,
            "origin": "llm_bootstrap",
            "error": None,
            "population_size": population_size,
            "protocol": protocol,
            "progress": CodaWebService._bootstrap_progress(
                status="not_run",
                phase="pending",
                population_size=population_size,
            ),
        }

    @staticmethod
    def _bootstrap_metadata(result: BootstrapResult) -> dict[str, object]:
        progress = dict(result.progress) if isinstance(result.progress, dict) else {}
        if not progress:
            sample_size = len(result.artifact_ids)
            progress = {
                "status": result.status,
                "phase": result.status,
                "processed_artifacts": sample_size,
                "total_artifacts": sample_size,
                "overall_completed": sample_size,
                "overall_total": sample_size,
                "percent": 100 if result.status in {"completed", "skipped", "disabled"} else 0,
                "current_artifact_id": None,
            }
        return {
            "enabled": result.status != "disabled",
            "status": result.status,
            "artifact_ids": list(result.artifact_ids),
            "code_count": len(result.codebook.codes),
            "human_reviewed": False,
            "origin": "llm_bootstrap",
            "error": result.error,
            "population_size": int(result.protocol.get("population_size", 0)),
            "protocol": dict(result.protocol),
            "progress": progress,
        }

    @staticmethod
    def _bootstrap_is_pending(run_state: RunState) -> bool:
        bootstrap = run_state.metadata.get("bootstrap")
        return isinstance(bootstrap, dict) and str(bootstrap.get("status", "not_run")) in {
            "not_run",
            "running",
            "cancelling",
            "cancelled",
            "interrupted",
            "failed",
        }

    @staticmethod
    def _interrupted_bootstrap_metadata(previous: dict[str, object]) -> dict[str, object]:
        metadata = dict(previous)
        progress = dict(metadata.get("progress", {}))
        progress.update({"status": "interrupted", "phase": "interrupted"})
        metadata.update({"status": "interrupted", "error": None, "progress": progress})
        return metadata

    @staticmethod
    def _cancelled_bootstrap_metadata(previous: dict[str, object]) -> dict[str, object]:
        metadata = dict(previous)
        progress = dict(metadata.get("progress", {}))
        progress.update({"status": "cancelled", "phase": "cancelled"})
        metadata.update({"status": "cancelled", "error": None, "progress": progress})
        return metadata

    @staticmethod
    def _bootstrap_progress(
        *,
        status: str,
        phase: str,
        population_size: int,
        processed_artifacts: int = 0,
        overall_completed: int | None = None,
        current_artifact_id: str | None = None,
        error: str | None = None,
    ) -> dict[str, object]:
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
        total_artifacts = bootstrap_sample_size(
            population_size,
            BootstrapConfig.from_env(),
        )
        overall_total = total_artifacts * 8
        completed = overall_completed if overall_completed is not None else processed_artifacts
        percent = (
            round(100 * completed / overall_total)
            if overall_total > 0
            else (100 if status in {"completed", "skipped", "disabled"} else 0)
        )
        progress: dict[str, object] = {
            "status": status,
            "phase": phase,
            "processed_artifacts": max(0, processed_artifacts),
            "total_artifacts": total_artifacts,
            "overall_completed": max(0, completed),
            "overall_total": overall_total,
            # The weighted counters are retained for old clients and audit
            # files; the UI should use this explicit stage position instead.
            "stage_index": stage_numbers.get(phase, 0),
            "stage_total": 8,
            "percent": max(0, min(100, percent)),
            "current_artifact_id": current_artifact_id,
        }
        if error:
            progress["error"] = error
        return progress

    @classmethod
    def _running_bootstrap_metadata(
        cls,
        previous: dict[str, object],
        *,
        population_size: int,
    ) -> dict[str, object]:
        metadata = dict(previous)
        metadata.update(
            {
                "enabled": True,
                "status": "running",
                "artifact_ids": [],
                "code_count": 0,
                "human_reviewed": False,
                "origin": "llm_bootstrap",
                "error": None,
                "population_size": population_size,
                "progress": cls._bootstrap_progress(
                    status="running",
                    phase="starting",
                    population_size=population_size,
                ),
            }
        )
        return metadata

    def _persist_bootstrap_progress(
        self,
        run_state: RunState,
        paths: FullRunPaths,
        progress: dict[str, object],
        *,
        population_size: int,
    ) -> None:
        """Persist each callback so polling and restart recovery see live progress."""

        with self._state_lock:
            metadata = dict(run_state.metadata.get("bootstrap", {}))
            progress_copy = dict(progress)
            reported_status = str(progress_copy.get("status", "running"))
            # The final result is committed atomically below, together with the
            # sampled queue and provisional B1. Keep the status running until then.
            cancellation_pending = str(metadata.get("status", "")) == "cancelling"
            metadata["status"] = (
                "cancelling"
                if cancellation_pending
                else "running" if reported_status == "completed" else reported_status
            )
            if cancellation_pending:
                progress_copy["status"] = "cancelling"
            metadata["error"] = progress_copy.get("error")
            metadata["population_size"] = population_size
            metadata["progress"] = progress_copy
            run_state.metadata["bootstrap"] = metadata
            save_run_state_checkpoint(run_state, paths.checkpoint_path)

    @staticmethod
    def _failed_progress(
        run_state: RunState,
        error: Exception,
        *,
        population_size: int,
    ) -> dict[str, object]:
        bootstrap = run_state.metadata.get("bootstrap")
        previous = bootstrap.get("progress", {}) if isinstance(bootstrap, dict) else {}
        progress = dict(previous) if isinstance(previous, dict) else {}
        progress.update(
            {
                "status": "failed",
                "phase": "failed",
                "error": f"{type(error).__name__}: {error}",
            }
        )
        if not progress.get("total_artifacts"):
            progress = CodaWebService._bootstrap_progress(
                status="failed",
                phase="failed",
                population_size=population_size,
                error=f"{type(error).__name__}: {error}",
            )
        return progress

    @staticmethod
    def _run_bootstrap(
        bootstrap: object,
        run_state: RunState,
        artifacts: list[ArtifactRecord],
        *,
        progress_callback: Callable[[dict[str, object]], None],
        checkpoint_dir: Path,
        cancel_requested: Callable[[], bool],
    ) -> BootstrapResult:
        """Call new and legacy Bootstrap implementations through one adapter."""

        run_method = getattr(bootstrap, "run")
        try:
            parameters = inspect.signature(run_method).parameters.values()
            parameter_names = {parameter.name for parameter in parameters}
            accepts_kwargs = any(
                parameter.kind is inspect.Parameter.VAR_KEYWORD
                for parameter in parameters
            )
            accepts_callback = "progress_callback" in parameter_names or accepts_kwargs
            accepts_checkpoint = "checkpoint_dir" in parameter_names or accepts_kwargs
            accepts_cancel = "cancel_requested" in parameter_names or accepts_kwargs
        except (TypeError, ValueError):
            accepts_callback = False
            accepts_checkpoint = False
            accepts_cancel = False
        kwargs: dict[str, object] = {}
        if accepts_callback:
            kwargs["progress_callback"] = progress_callback
        if accepts_checkpoint:
            kwargs["checkpoint_dir"] = checkpoint_dir
        if accepts_cancel:
            kwargs["cancel_requested"] = cancel_requested
        if kwargs:
            return run_method(run_state, artifacts, **kwargs)
        return run_method(run_state, artifacts)

    @staticmethod
    def _write_json(path: Path, payload: object) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    @classmethod
    def _write_bootstrap_artifacts(cls, paths: FullRunPaths, result: BootstrapResult) -> None:
        """Persist automatic work separately from human review records."""

        cls._write_json(paths.bootstrap_manifest_path, result.to_dict())
        with paths.bootstrap_evidence_packets_path.open("w", encoding="utf-8") as handle:
            for packet in result.context_packets:
                handle.write(json.dumps(packet, ensure_ascii=False))
                handle.write("\n")
        with paths.bootstrap_initial_codings_path.open("w", encoding="utf-8") as handle:
            for coding_case in result.initial_codings:
                handle.write(json.dumps(asdict(coding_case), ensure_ascii=False))
                handle.write("\n")
        cls._write_json(
            paths.initial_codebook_path,
            serialize_codebook_state(result.codebook),
        )
        cls._write_json(
            paths.bootstrap_audit_path,
            {
                "status": result.status,
                "warnings": result.audit_warnings,
                "warnings_zh": result.audit_warnings_zh,
                "error": result.error,
            },
        )
        paths.bootstrap_drafts_dir.mkdir(parents=True, exist_ok=True)
        for draft in result.draft_codebooks:
            batch_index = int(draft.get("batch_index", 0))
            cls._write_json(
                paths.bootstrap_drafts_dir / f"draft-{batch_index:04d}.json",
                draft,
            )
        with paths.bootstrap_assignments_path.open("w", encoding="utf-8") as handle:
            for assignment in result.assignments:
                handle.write(json.dumps(asdict(assignment), ensure_ascii=False))
                handle.write("\n")

    def _read_json_object(self, path: Path) -> dict[str, object] | None:
        if not path.exists():
            return None
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as error:
            raise WebWorkflowError(f"Invalid JSON object in {path.name}.") from error
        if not isinstance(payload, dict):
            raise WebWorkflowError(f"Invalid JSON object in {path.name}.")
        return payload

    def _adapter_for(self, dataset_name: str) -> DatasetAdapter:
        factory = self._adapter_factories.get(dataset_name)
        if factory is None:
            choices = ", ".join(sorted(self._adapter_factories))
            raise WebWorkflowError(f"Unknown dataset '{dataset_name}'. Available: {choices}.")
        return factory()

    def _verify_frozen_sources(self, run_state: RunState, artifacts: dict[str, ArtifactRecord]) -> None:
        from coda.study import evidence_sha256
        manifest = self._read_json_object(self._paths_for(run_state.run_id).run_manifest_path) or {}
        for row in manifest.get("data", {}).get("artifacts", []):
            key = row["artifact_id"]
            if row.get("evidence_sha256") and (
                    key not in artifacts or evidence_sha256(artifacts[key]) != row["evidence_sha256"]):
                raise WebWorkflowError(f"Source evidence changed for {key}; restore the frozen run input before continuing.")

    def _paths_for(self, run_id: str) -> FullRunPaths:
        if not run_id or run_id in {".", ".."} or Path(run_id).name != run_id:
            raise WebRunNotFoundError("Invalid run_id.")
        return FullRunPaths.from_run_dir(self._runs_root / run_id)

    def _load_run_state(self, run_id: str) -> RunState:
        with self._state_lock:
            active = self._active_states.get(run_id)
            if active is not None:
                return active
            paths = self._paths_for(run_id)
            if not paths.checkpoint_path.exists():
                raise WebRunNotFoundError(f"Run '{run_id}' does not exist.")
            payload = json.loads(paths.checkpoint_path.read_text(encoding="utf-8"))
            if not isinstance(payload, dict):
                raise WebWorkflowError(f"Run '{run_id}' has an invalid checkpoint.")
            dataset_name = str(payload.get("dataset_name", ""))
            adapter = self._adapter_for(dataset_name)
            metadata = adapter.load_dataset_metadata()
            artifacts_by_id = {
                artifact.artifact_id: artifact for artifact in adapter.iter_artifacts()
            }
            from coda.study import evidence_sha256
            run_manifest = self._read_json_object(paths.run_manifest_path) or {}
            for row in run_manifest.get("data", {}).get("artifacts", []):
                artifact_id = row["artifact_id"]
                if row.get("evidence_sha256") and (
                        artifact_id not in artifacts_by_id or
                        evidence_sha256(artifacts_by_id[artifact_id]) != row["evidence_sha256"]):
                    raise WebWorkflowError(f"Source evidence changed for {artifact_id}; restore the frozen run input before resuming.")
            binding = payload.get("metadata", {}).get("study_materials")
            if binding is not None:
                study_manifest = load_study_manifest(paths.run_dir / "study_manifest.json")
                expected = study_binding(study_manifest, dataset_name, str(binding.get("phase")))
                if binding != expected:
                    raise WebWorkflowError("Checkpoint differs from its frozen study allocation.")
                select_study_artifacts(study_manifest, dataset_name, artifacts_by_id.values(), expected["phase"])
                if payload.get("metadata", {}).get("selected_artifact_ids") != expected["artifact_ids"]:
                    raise WebWorkflowError("Checkpoint changes the frozen study case order.")
            coding_batches = self._restore_batches(
                payload.get("coding_batches", []),
                artifacts_by_id=artifacts_by_id,
            )
            held_out_batches = self._restore_batches(
                payload.get("held_out_batches", []),
                artifacts_by_id=artifacts_by_id,
            )
            run_state = load_run_state_checkpoint(
                paths.checkpoint_path,
                dataset_metadata=metadata,
                coding_batches=coding_batches,
                held_out_batches=held_out_batches,
            )
            self._active_states[run_id] = run_state
            return run_state

    def _restore_batches(
        self,
        descriptors: object,
        *,
        artifacts_by_id: dict[str, ArtifactRecord],
    ) -> list[ArtifactBatchState]:
        if not isinstance(descriptors, list):
            raise WebWorkflowError("Checkpoint batch descriptors must be a list.")
        batches: list[ArtifactBatchState] = []
        for descriptor in descriptors:
            if not isinstance(descriptor, dict):
                raise WebWorkflowError("Checkpoint batch descriptor must be an object.")
            artifact_ids = descriptor.get("artifact_ids", [])
            if not isinstance(artifact_ids, list):
                raise WebWorkflowError("Checkpoint artifact_ids must be a list.")
            try:
                artifacts = [artifacts_by_id[str(artifact_id)] for artifact_id in artifact_ids]
            except KeyError as error:
                raise WebWorkflowError(
                    f"Checkpoint references unavailable artifact '{error.args[0]}'."
                ) from error
            batches.append(
                ArtifactBatchState(
                    batch_id=str(descriptor["batch_id"]),
                    dataset_name=str(descriptor["dataset_name"]),
                    batch_index=int(descriptor["batch_index"]),
                    split_name=descriptor["split_name"],
                    artifacts=artifacts,
                    group_ids=dict(descriptor.get("group_ids", {})),
                    sampling_note=descriptor.get("sampling_note"),
                    metadata=dict(descriptor.get("metadata", {})),
                )
            )
        return batches

    def _orchestrator_for(self, run_id: str) -> CODAOrchestrator:
        orchestrator = self._orchestrators.get(run_id)
        if orchestrator is None:
            orchestrator = self._orchestrator_factory()
            state = self._load_run_state(run_id)
            self._bind_agent_protocol(state, "iterative", [
                ("context", orchestrator._context_agent),
                *orchestrator._coder_agents,
                ("comparison", orchestrator._comparison_agent),
                ("validation", orchestrator._validation_agent),
            ])
            self._orchestrators[run_id] = orchestrator
            orchestrator.set_execution_trace_sink(
                lambda trace: append_jsonl(self._paths_for(run_id).run_dir / "model_calls.jsonl", trace)
            )
            def load_artifact(artifact_id):
                state = self._load_run_state(run_id)
                current = next((item for item in self._adapter_for(
                    state.dataset_metadata.dataset_name
                ).iter_artifacts() if item.artifact_id == artifact_id), None)
                frozen = state.metadata.get("case_materials", {}).get(artifact_id, {})
                if current is not None and "content" in frozen:
                    from coda.study import evidence_sha256
                    if evidence_sha256(current) != evidence_sha256(frozen):
                        raise WebWorkflowError(f"Source evidence changed for historical case {artifact_id}; restore its frozen snapshot.")
                return current
            orchestrator.artifact_loader = load_artifact
        return orchestrator

    def _bind_agent_protocol(self, run_state: RunState, stage: str, agents: list[tuple[str, object]]) -> None:
        signatures = {}
        for role, agent in agents:
            if not hasattr(agent, "_prompt_spec") or not hasattr(agent, "model_config"):
                continue
            config = agent.model_config
            signatures[role] = {
                "model": config.model, "provider": config.provider,
                "temperature": config.temperature, "max_output_tokens": config.max_output_tokens,
                "send_temperature": config.send_temperature,
                "token_limit_parameter": config.token_limit_parameter,
                "base_url": config.resolved_base_url(),
                "api_key_env": config.resolved_api_key_env(),
                "json_mode": config.json_mode,
                "system_prompt": agent._prompt_spec.system_prompt,
                "user_prompt_template": agent._prompt_spec.user_prompt_template,
                "batch_reconciliation_prompt": getattr(agent, "_batch_prompt", None),
                "settings": asdict(agent._settings) if hasattr(agent, "_settings") else None,
            }
        if not signatures:
            return
        frozen = run_state.metadata.setdefault("agent_protocols", {})
        if stage in frozen and frozen[stage] != signatures:
            raise WebWorkflowError("Model, prompt, or decoding settings differ from this run's frozen protocol. Start a new run for changed analytical settings.")
        if stage not in frozen:
            frozen[stage] = signatures
            save_run_state_checkpoint(run_state, self._paths_for(run_state.run_id).checkpoint_path)

    def _prepare_iterative_case(self, run_state, orchestrator, batch, artifact, *,
                                stage_store=None, **kwargs):
        if batch.metadata.get("shared_snapshot_reconciliation"):
            return prepare_batch_case(orchestrator, run_state, batch, artifact,
                directory=self._paths_for(run_state.run_id).stage_checkpoint_dir,
                persist=lambda: save_run_state_checkpoint(run_state,
                    self._paths_for(run_state.run_id).checkpoint_path))
        return orchestrator.prepare_one_artifact(run_state, artifact=artifact, batch=batch,
            stage_checkpoint_store=stage_store, **kwargs)

    @staticmethod
    def _update_batch_progress(run_state):
        reviewed = set(run_state.history.reviewed_artifact_ids())
        reopened = set(run_state.metadata.get("reopened_context_artifact_ids", []))
        for plan in run_state.metadata.get("iterative_batch_preparations", {}).values():
            completed = [key for key in plan["artifact_ids"] if key in reviewed and key not in reopened]
            plan["completed_artifact_ids"] = completed
            plan["status"] = "completed" if len(completed) == len(plan["artifact_ids"]) else "reviewing"

    def _stage_store(
        self,
        run_id: str,
        orchestrator: CODAOrchestrator,
        run_state: RunState,
        artifact: ArtifactRecord,
        *,
        review_origin: str = "current",
        retrospective_task_id: str | None = None,
    ) -> StageCheckpointStore:
        cache_key = orchestrator.stage_cache_key(
            run_state,
            artifact,
            review_origin=review_origin,
            retrospective_task_id=retrospective_task_id,
        )
        identifier = retrospective_task_id or artifact.artifact_id
        file_name = hashlib.sha256(identifier.encode("utf-8")).hexdigest()[:24]
        return StageCheckpointStore(
            self._paths_for(run_id).stage_checkpoint_dir / f"{file_name}.json",
            cache_key=cache_key,
        )

    def _batch_and_artifact_for_task(
        self,
        run_state: RunState,
        task: RetrospectiveRecodingTask,
    ) -> tuple[ArtifactBatchState, ArtifactRecord]:
        for batch in [*run_state.coding_batches, *run_state.held_out_batches]:
            for artifact in batch.artifacts:
                if artifact.artifact_id == task.artifact_id:
                    return batch, artifact
        for artifact in self._adapter_for(
            run_state.dataset_metadata.dataset_name
        ).iter_artifacts():
            if artifact.artifact_id == task.artifact_id:
                return (
                    ArtifactBatchState(
                        batch_id="bootstrap-retrospective",
                        dataset_name=run_state.dataset_metadata.dataset_name,
                        batch_index=0,
                        split_name="coding_pool",
                        artifacts=[artifact],
                        metadata={"origin": "bootstrap_retrospective"},
                    ),
                    artifact,
                )
        raise WebWorkflowError(
            f"Artifact '{task.artifact_id}' for retrospective task '{task.task_id}' "
            "is not present in the reconstructed run data."
        )

    def _current_pending_artifact(
        self,
        run_state: RunState,
    ) -> tuple[ArtifactBatchState, ArtifactRecord]:
        batch = run_state.current_batch()
        if batch is None:
            raise WebWorkflowError("This run has no remaining coding artifacts.")
        pending = pending_artifacts_for_batch(batch, run_state)
        if not pending:
            raise WebWorkflowError("This batch has no pending artifacts.")
        return batch, pending[0]
