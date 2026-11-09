from __future__ import annotations

import json
import tempfile
import threading
import unittest
from dataclasses import replace
from pathlib import Path

from adapters.static_analysis import StaticAnalysisNondeterminismAdapter
from adapters.base import ArtifactRecord
from adapters.defects4codellm import (
    Defects4CodeLLMSemanticAdapter,
    Defects4CodeLLMSyntacticAdapter,
)
from coda.bootstrap import BootstrapCancelledError, BootstrapResult
from coda.contracts import (
    ArbitrationInput,
    ArbitrationOutput,
    CoderAgentInput,
    CoderAgentOutput,
    ContextAgentInput,
    ContextPacket,
    EvidenceItem,
    HumanReviewInput,
    HumanReviewOutput,
    ProvisionalCode,
    ValidationInput,
    ValidationOutput,
    ValidationSignal,
)
from coda.orchestrator import CODAOrchestrator
from coda.state import (
    CodeState,
    CodebookChangeState,
    CodebookState,
    ContextRequestState,
    CodingRecordState,
    RetrospectiveRecodingTask,
)
from coda.persistence import save_run_state_checkpoint
from coda.web.runtime import CodaWebService, WebWorkflowError


def _build_test_orchestrator(
    call_log: list[str],
    *,
    relationship_to_codebook: str = "new_code",
    linked_code_id: str = "analysis-logic",
    coder_confidence_level: str = "low",
    coder_insufficient_context: bool = False,
    validation_confidence_level: str = "low",
    duplicate_new_code_candidate: bool = False,
    codebook_change_action: str | None = None,
) -> CODAOrchestrator:
    def context_agent(agent_input: ContextAgentInput) -> ContextPacket:
        call_log.append(f"context:{agent_input.artifact.artifact_id}")
        return ContextPacket(
            artifact_id=agent_input.artifact.artifact_id,
            context_brief="A concise context brief.",
            evidence_items=[
                EvidenceItem(
                    field_name="content",
                    excerpt=agent_input.artifact.content[:80],
                )
            ],
        )

    def coder(agent_input: CoderAgentInput) -> CoderAgentOutput:
        call_log.append(f"{agent_input.coder_id}:{agent_input.artifact.artifact_id}")
        return CoderAgentOutput(
            artifact_id=agent_input.artifact.artifact_id,
            coder_id=agent_input.coder_id,
            provisional_codes=[
                ProvisionalCode(
                    code_name="Analysis Logic",
                    short_definition="A root cause in analysis logic.",
                    supporting_evidence=agent_input.context_packet.evidence_items,
                    relationship_to_codebook="uncertain",
                    linked_code_ids=[],
                    proposed_codebook_action="no_change",
                )
            ],
            confidence_level=coder_confidence_level,
            insufficient_context=coder_insufficient_context,
            confidence_rationale="The test coder confidence is explicit.",
            confidence_factors={"evidence_support": "direct"},
        )

    def arbitration_agent(agent_input: ArbitrationInput) -> ArbitrationOutput:
        call_log.append(f"arbitration:{agent_input.artifact.artifact_id}")
        provisional = agent_input.coder_outputs[0].provisional_codes[0]
        mapped = ProvisionalCode(
            code_name=provisional.code_name,
            short_definition=provisional.short_definition,
            code_name_zh=provisional.code_name_zh,
            short_definition_zh=provisional.short_definition_zh,
            observed_phenomenon=provisional.observed_phenomenon,
            observed_phenomenon_zh=provisional.observed_phenomenon_zh,
            supporting_evidence=provisional.supporting_evidence,
            relationship_to_codebook=relationship_to_codebook,
            linked_code_ids=(
                [linked_code_id]
                if relationship_to_codebook == "reuse_existing_code"
                else []
            ),
            alternative_interpretation=provisional.alternative_interpretation,
            alternative_interpretation_zh=provisional.alternative_interpretation_zh,
            uncertainty_note=provisional.uncertainty_note,
            uncertainty_note_zh=provisional.uncertainty_note_zh,
            proposed_codebook_action=(
                "no_change"
                if relationship_to_codebook == "reuse_existing_code"
                else "add"
            ),
            proposed_codebook_target_ids=(
                [linked_code_id]
                if relationship_to_codebook == "reuse_existing_code"
                else []
            ),
        )
        recommended_codes = [mapped]
        if duplicate_new_code_candidate:
            recommended_codes.append(
                replace(mapped, code_name="  analysis   logic  ")
            )
        possible_changes = []
        if codebook_change_action is not None:
            possible_changes.append(
                CodebookChangeState(
                    change_id="proposed-change",
                    action=codebook_change_action,  # type: ignore[arg-type]
                    round_index=0,
                    summary="The established category needs a structural revision.",
                    target_code_ids=[linked_code_id],
                    artifact_ids=[agent_input.artifact.artifact_id],
                )
            )
        return ArbitrationOutput(
            artifact_id=agent_input.artifact.artifact_id,
            agreement_summary="The coders agree.",
            disagreement_summary="None.",
            recommended_codes=recommended_codes,
            possible_codebook_changes=possible_changes,
        )

    def validation_agent(agent_input: ValidationInput) -> ValidationOutput:
        call_log.append(f"validation:{agent_input.artifact.artifact_id}")
        return ValidationOutput(
            artifact_id=agent_input.artifact.artifact_id,
            signals=[ValidationSignal(signal="valid", summary="Ready for review.")],
            summary="Ready for review.",
            confidence_level=validation_confidence_level,
            confidence_rationale="The test validation confidence is explicit.",
            confidence_factors={"evidence_support": "direct"},
        )

    def unused_human_reviewer(agent_input: HumanReviewInput) -> HumanReviewOutput:
        call_log.append(f"unexpected-human:{agent_input.artifact.artifact_id}")
        raise AssertionError("The web service must not call a CLI human reviewer.")

    return CODAOrchestrator(
        context_agent=context_agent,
        coder_agents=[("coder-a", coder), ("coder-b", coder)],
        arbitration_agent=arbitration_agent,
        validation_agent=validation_agent,
        human_review_agent=unused_human_reviewer,
    )


def _build_test_bootstrap(_: CODAOrchestrator):
    """Return a deterministic bootstrap result without an external model call."""

    class TestBootstrap:
        def run(self, run_state, artifacts):
            return BootstrapResult(
                codebook=CodebookState.empty(run_state.dataset_metadata.dataset_name),
                artifact_ids=[],
                group_ids={artifact.artifact_id: artifact.artifact_id for artifact in artifacts},
                protocol={"population_size": len(artifacts)},
            )

    return TestBootstrap()


def _build_existing_code_bootstrap(_: CODAOrchestrator):
    """Provide a deterministic B1 so conditional reuse can be tested."""

    class TestBootstrap:
        def run(self, run_state, artifacts):
            code = CodeState(
                code_id="analysis-logic",
                name="Analysis Logic",
                definition="A root cause in analysis logic.",
            )
            return BootstrapResult(
                codebook=CodebookState(
                    dataset_name=run_state.dataset_metadata.dataset_name,
                    version=1,
                    codes=[code],
                ),
                artifact_ids=[],
                group_ids={artifact.artifact_id: artifact.artifact_id for artifact in artifacts},
                protocol={"population_size": len(artifacts)},
            )

    return TestBootstrap()


class TestCodaWebService(unittest.TestCase):
    def test_automatic_finalization_drains_reassessments_with_work_limit(self) -> None:
        calls = []
        with tempfile.TemporaryDirectory() as temp_dir:
            service = CodaWebService(
                runs_root=Path(temp_dir),
                orchestrator_factory=lambda: _build_test_orchestrator(calls, relationship_to_codebook="reuse_existing_code"),
                bootstrap_factory=_build_existing_code_bootstrap,
            )
            summary = service.create_run(dataset_name="static_analysis_nondeterminism", artifact_limit=1, review_mode="automatic")
            run_id = summary["run_id"]
            service.initialize_run(run_id)
            service.process_automatic(run_id)
            state = service._load_run_state(run_id)
            record = state.history.coding_records[0]
            for index in range(3):
                state.history.retrospective_tasks.append(RetrospectiveRecodingTask(
                    task_id=f"task-{index}", artifact_id=record.artifact_id,
                    trigger_change_id="revision", from_codebook_version=0,
                    target_codebook_version=state.codebook.version, reason="Check revised boundary.",
                ))
            service._finish_iterative_coding(state)
            self.assertFalse(state.history.pending_retrospective_tasks())
            self.assertEqual([task.status for task in state.history.retrospective_tasks], ["completed", "completed", "cancelled"])
            self.assertTrue(any(item.source == "automatic_reassessment_limit" for item in state.history.open_unresolved_cases()))
            self.assertEqual(state.status, "completed_with_unresolved")

    def test_final_validation_uses_final_records_and_resumes_after_restart(self) -> None:
        calls = []
        fail = [True]
        def factory():
            orchestrator = _build_test_orchestrator([])
            def validation(agent_input):
                self.assertEqual(agent_input.validation_scope, "final_audit")
                self.assertEqual(agent_input.coder_outputs, [])
                self.assertIn("recorded_assignment", agent_input.corpus_audit)
                calls.append(agent_input.artifact.artifact_id)
                if len(calls) == 2 and fail[0]:
                    fail[0] = False
                    raise RuntimeError("audit interrupted")
                return ValidationOutput(
                    artifact_id=agent_input.artifact.artifact_id,
                    summary="Final assignment checked.",
                    signals=[ValidationSignal(signal="valid", summary="Supported.")],
                )
            orchestrator._validation_agent = validation
            return orchestrator
        with tempfile.TemporaryDirectory() as temp_dir:
            kwargs = dict(
                runs_root=Path(temp_dir),
                orchestrator_factory=factory,
                bootstrap_factory=_build_test_bootstrap,
            )
            service = CodaWebService(**kwargs)
            created = service.create_run(dataset_name="static_analysis_nondeterminism", artifact_limit=3, review_mode="selective")
            run_id = created["run_id"]
            service.initialize_run(run_id)
            state = service._load_run_state(run_id)
            state.codebook = state.codebook.with_codes([CodeState(code_id="c", name="C", definition="Category.")])
            for batch in state.coding_batches:
                state.history.append_record(CodingRecordState(
                    record_id=f"record-{batch.artifact_ids[0]}",
                    artifact_id=batch.artifact_ids[0],
                    dataset_name=state.dataset_metadata.dataset_name,
                    batch_index=batch.batch_index,
                    codebook_version=state.codebook.version,
                    decision="accept", final_code_ids=["c"],
                    metadata={"routing_decision": {"signal_details": {"review_criteria": ["R2"]}}},
                ))
            state.current_batch_index = len(state.coding_batches)
            with self.assertRaisesRegex(RuntimeError, "interrupted"):
                service._finish_iterative_coding(state)
            self.assertEqual(state.status, "awaiting_next_artifact")
            completed_id = calls[0]
            restarted = CodaWebService(**kwargs)
            restored = restarted._load_run_state(run_id)
            restarted._finish_iterative_coding(restored)
            self.assertEqual(calls.count(completed_id), 1)
            packet = restarted.stage_review_packet(run_id, "final")
            self.assertEqual(len(packet["final_validation_audits"]), 1)
            self.assertEqual(packet["final_validation_audits"][0]["status"], "completed")
            self.assertEqual(len(packet["final_validation_audits"][0]["validation_outputs"]), 3)
            before = len(calls)
            restarted._finish_iterative_coding(restored)
            self.assertEqual(len(calls), before)

    def test_automatic_processing_rejects_a_second_request_for_same_run(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            service = CodaWebService(
                runs_root=Path(temp_dir) / "runs",
                adapter_factories={
                    "static_analysis_nondeterminism": StaticAnalysisNondeterminismAdapter
                },
                orchestrator_factory=lambda: _build_test_orchestrator([]),
                bootstrap_factory=_build_test_bootstrap,
            )
            created = service.create_run(
                dataset_name="static_analysis_nondeterminism",
                artifact_limit=1,
                review_mode="automatic",
            )
            run_id = str(created["run_id"])
            service._processing_runs.add(run_id)
            try:
                with self.assertRaisesRegex(WebWorkflowError, "already processing"):
                    service.process_automatic(run_id)
            finally:
                service._processing_runs.discard(run_id)

    def test_freeze_variant_blocks_initial_and_final_review_edits(self) -> None:
        class CodebookBootstrap:
            def run(self, run_state, artifacts):
                code = CodeState(
                    code_id="seed-code",
                    name="Seed concept",
                    definition="Initial definition.",
                )
                return BootstrapResult(
                    codebook=CodebookState(
                        dataset_name=run_state.dataset_metadata.dataset_name,
                        version=1,
                        codes=[code],
                    ),
                    artifact_ids=[],
                    group_ids={item.artifact_id: item.artifact_id for item in artifacts},
                    protocol={"population_size": len(artifacts)},
                )

        with tempfile.TemporaryDirectory() as temp_dir:
            service = CodaWebService(
                runs_root=Path(temp_dir) / "runs",
                adapter_factories={
                    "static_analysis_nondeterminism": StaticAnalysisNondeterminismAdapter
                },
                orchestrator_factory=lambda: _build_test_orchestrator([]),
                bootstrap_factory=lambda _: CodebookBootstrap(),
            )
            created = service.create_run(
                dataset_name="static_analysis_nondeterminism",
                artifact_limit=1,
                review_mode="full",
                experiment_variant="freeze_after_initialization",
            )
            run_id = str(created["run_id"])
            service.initialize_run(run_id)
            packet = service.stage_review_packet(run_id, "initial")
            self.assertFalse(packet["codebook_editing_allowed"])
            frozen_code = service._load_run_state(run_id).codebook.codes[0]
            unchanged_assignment = CODAOrchestrator._apply_experiment_variant(
                service._load_run_state(run_id),
                HumanReviewOutput(
                    artifact_id="future-artifact",
                    decision="accept",
                    final_codes=[
                        replace(
                            frozen_code,
                            representative_artifact_ids=["future-artifact"],
                        )
                    ],
                ),
                review_origin="current",
            )
            self.assertEqual(unchanged_assignment.decision, "accept")
            with self.assertRaisesRegex(WebWorkflowError, "freezes the codebook"):
                service.submit_stage_review(
                    run_id,
                    "initial",
                    decision="revise",
                    rationale="Attempt a prohibited initial-stage edit.",
                    revised_codes=[replace(frozen_code, definition="Changed definition.")],
                )
            self.assertEqual(service._load_run_state(run_id).codebook.version, 1)

            service.submit_stage_review(
                run_id,
                "initial",
                decision="accept",
                rationale="The frozen initial codebook is accepted.",
            )
            artifact = service.current_artifact(run_id)["artifact"]
            self.assertIsNotNone(artifact)
            service.prepare_review(run_id)
            service.submit_review(
                run_id,
                human_review_output=HumanReviewOutput(
                    artifact_id=str(artifact["artifact_id"]),
                    decision="accept",
                    rationale="The new phenomenon would normally add a code.",
                    final_codes=[
                        CodeState(
                            code_id="new-code",
                            name="New concept",
                            definition="A newly observed concept.",
                        )
                    ],
                    evidence_summary=["The artifact supports the new concept."],
                    confirmed_evidence=[
                        EvidenceItem(
                            field_name="content",
                            excerpt=str(artifact["content"])[:60],
                            rationale="This excerpt supports the proposed code.",
                        )
                    ],
                    codebook_changes=[
                        CodebookChangeState(
                            change_id="suppressed-add",
                            action="add",
                            round_index=0,
                            summary="Add the newly observed concept.",
                            rationale="The current codebook does not represent this evidence.",
                            resulting_code_ids=["new-code"],
                        )
                    ],
                ),
            )
            state_after_artifact = service._load_run_state(run_id)
            self.assertEqual(state_after_artifact.codebook.version, 1)
            suppressed_record = state_after_artifact.history.latest_record_for_artifact(
                str(artifact["artifact_id"])
            )
            self.assertEqual(suppressed_record.decision, "mark_uncertain")
            self.assertEqual(
                suppressed_record.metadata["suppressed_codebook_change_details"]["new_code_ids"],
                ["new-code"],
            )
            self.assertEqual(
                len(state_after_artifact.metadata["codebook_suppression_events"]), 1
            )
            service.next_artifact(run_id)
            run_state = service._load_run_state(run_id)
            self.assertEqual(run_state.status, "awaiting_final_review")
            with self.assertRaisesRegex(WebWorkflowError, "cannot submit codebook changes"):
                service.submit_stage_review(
                    run_id,
                    "final",
                    decision="reject",
                    rationale="Rejecting the frozen result would require a codebook revision.",
                )
            with self.assertRaisesRegex(WebWorkflowError, "freezes the codebook"):
                service.submit_stage_review(
                    run_id,
                    "final",
                    decision="revise",
                    rationale="Attempt a prohibited final-stage edit.",
                    revised_codes=[replace(frozen_code, name="Renamed concept")],
                )
            summary = service.run_summary(run_id)
            self.assertEqual(summary["experiment_variant"], "freeze_after_initialization")
            manifest = json.loads(
                Path(str(summary["run_manifest"])).read_text(encoding="utf-8")
            )
            self.assertEqual(
                manifest["protocol"]["experiment"]["variant"],
                "freeze_after_initialization",
            )

    def test_without_retrospective_variant_records_suppressed_impact(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            service = CodaWebService(
                runs_root=Path(temp_dir) / "runs",
                adapter_factories={
                    "static_analysis_nondeterminism": StaticAnalysisNondeterminismAdapter
                },
                orchestrator_factory=lambda: _build_test_orchestrator([]),
                bootstrap_factory=_build_existing_code_bootstrap,
            )
            created = service.create_run(
                dataset_name="static_analysis_nondeterminism",
                artifact_limit=2,
                review_mode="selective",
                experiment_variant="without_retrospective_recoding",
            )
            run_id = str(created["run_id"])
            service.initialize_run(run_id)
            run_state = service._load_run_state(run_id)
            historical_id = str(run_state.metadata["selected_artifact_ids"][0])
            run_state.codebook.codes[0].representative_artifact_ids = [historical_id]
            run_state.history.append_record(
                CodingRecordState(
                    record_id="historical-record",
                    artifact_id=historical_id,
                    dataset_name=run_state.dataset_metadata.dataset_name,
                    batch_index=0,
                    codebook_version=1,
                    decision="accept",
                    final_code_ids=["analysis-logic"],
                )
            )
            change = CodebookChangeState(
                change_id="refine-change",
                action="refine",
                round_index=1,
                summary="Clarify a category boundary.",
                target_code_ids=["analysis-logic"],
            )
            orchestrator = service._orchestrator_for(run_id)
            tasks = orchestrator.enqueue_retrospective_tasks(
                run_state=run_state,
                change=change,
                from_codebook_version=1,
                source_artifact_id="new-artifact",
            )
            self.assertEqual(tasks, [])
            self.assertTrue(change.metadata["retrospective_recoding_suppressed"])
            self.assertEqual(change.metadata["suppressed_affected_artifact_count"], 1)
            event = run_state.metadata["retrospective_suppression_events"][0]
            self.assertEqual(event["change_id"], "refine-change")
            self.assertEqual(event["affected_artifact_ids"], [historical_id])

    def test_new_runs_use_one_coding_pool(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            adapter = StaticAnalysisNondeterminismAdapter()
            artifacts = list(adapter.iter_artifacts())[:30]
            service = CodaWebService(
                runs_root=Path(temp_dir) / "runs",
                adapter_factories={
                    "static_analysis_nondeterminism": StaticAnalysisNondeterminismAdapter
                },
                orchestrator_factory=lambda: _build_test_orchestrator([]),
                bootstrap_factory=_build_test_bootstrap,
            )
            summary = service.create_run(
                dataset_name="static_analysis_nondeterminism",
                artifact_limit=30,
            )
            state = service._load_run_state(str(summary["run_id"]))
            self.assertEqual(state.total_coding_artifacts, 30)
            self.assertEqual(state.total_held_out_artifacts, 0)
            self.assertEqual(len(state.metadata["selected_artifact_ids"]), 30)

    def test_stage_operations_represent_merge_split_and_parent_without_deletion(self) -> None:
        before = [
            CodeState(code_id="a", name="A", definition="A definition."),
            CodeState(code_id="b", name="B", definition="B definition."),
        ]
        merged = [
            replace(before[0], status="merged", metadata={"merged_into": "ab"}),
            replace(before[1], status="merged", metadata={"merged_into": "ab"}),
            CodeState(code_id="ab", name="AB", definition="Merged definition."),
        ]
        merge = CodebookChangeState(
            change_id="merge-ab",
            action="merge",
            round_index=0,
            summary="Merge overlapping categories.",
            rationale="Their evidence and boundaries are indistinguishable.",
            target_code_ids=["a", "b"],
            resulting_code_ids=["ab"],
        )
        changes = CodaWebService._validate_stage_review_operations(
            kind="initial",
            before_codes=before,
            revised_codes=merged,
            operations=[merge],
            round_index=3,
            rationale="Reviewed structure.",
        )
        self.assertEqual(changes[0].round_index, 3)
        self.assertEqual(changes[0].decided_by, "human")

        parented = [
            replace(before[0], parent_code_id="parent"),
            replace(before[1], parent_code_id="parent"),
            CodeState(code_id="parent", name="Parent", definition="Shared parent."),
        ]
        parent = replace(
            merge,
            change_id="parent-ab",
            action="add_parent",
            summary="Add a shared parent.",
            target_code_ids=["a", "b"],
            resulting_code_ids=["parent"],
        )
        self.assertEqual(
            CodaWebService._validate_stage_review_operations(
                kind="initial",
                before_codes=before,
                revised_codes=parented,
                operations=[parent],
                round_index=0,
                rationale="Reviewed hierarchy.",
            )[0].action,
            "add_parent",
        )

        split_codes = [
            replace(
                before[0],
                status="split",
                metadata={"split_into": ["a-1", "a-2"]},
            ),
            before[1],
            CodeState(code_id="a-1", name="A1", definition="First boundary."),
            CodeState(code_id="a-2", name="A2", definition="Second boundary."),
        ]
        split = replace(
            merge,
            change_id="split-a",
            action="split",
            summary="Split a broad category.",
            target_code_ids=["a"],
            resulting_code_ids=["a-1", "a-2"],
        )
        self.assertEqual(
            CodaWebService._validate_stage_review_operations(
                kind="final",
                before_codes=before,
                revised_codes=split_codes,
                operations=[split],
                round_index=0,
                rationale="Reviewed boundaries.",
            )[0].action,
            "split",
        )

        retired = [replace(before[0], status="retired"), before[1]]
        retire = CodebookChangeState(
            change_id="retire-a",
            action="retire",
            round_index=0,
            summary="Retire an unsupported code.",
            rationale="The category is no longer supported.",
            target_code_ids=["a"],
            resulting_code_ids=["a"],
        )
        self.assertEqual(
            CodaWebService._validate_stage_review_operations(
                kind="final",
                before_codes=before,
                revised_codes=retired,
                operations=[retire],
                round_index=0,
                rationale="The category is no longer supported.",
            )[0].action,
            "retire",
        )

        with self.assertRaisesRegex(WebWorkflowError, "cannot delete"):
            CodaWebService._validate_stage_review_operations(
                kind="initial",
                before_codes=before,
                revised_codes=[before[0]],
                operations=[merge],
                round_index=0,
                rationale="Invalid deletion.",
            )

    def test_stage_review_rejects_invalid_hierarchy_and_unexplained_status(self) -> None:
        before = [
            CodeState(code_id="a", name="A", definition="A definition."),
            CodeState(code_id="b", name="B", definition="B definition."),
        ]
        refine = CodebookChangeState(
            change_id="refine-a",
            action="refine",
            round_index=0,
            summary="Refine A.",
            rationale="Clarify its boundary.",
            target_code_ids=["a"],
            resulting_code_ids=["a"],
        )
        with self.assertRaisesRegex(WebWorkflowError, "does not exist"):
            CodaWebService._validate_stage_review_operations(
                kind="initial",
                before_codes=before,
                revised_codes=[replace(before[0], parent_code_id="missing"), before[1]],
                operations=[refine],
                round_index=0,
                rationale="Invalid parent.",
            )

        cycle = [
            replace(before[0], parent_code_id="b"),
            replace(before[1], parent_code_id="a"),
        ]
        with self.assertRaisesRegex(WebWorkflowError, "parent cycle"):
            CodaWebService._validate_stage_review_operations(
                kind="initial",
                before_codes=before,
                revised_codes=cycle,
                operations=[refine],
                round_index=0,
                rationale="Invalid cycle.",
            )

        with self.assertRaisesRegex(WebWorkflowError, "cannot change code status"):
            CodaWebService._validate_stage_review_operations(
                kind="initial",
                before_codes=before,
                revised_codes=[replace(before[0], status="retired"), before[1]],
                operations=[refine],
                round_index=0,
                rationale="Unsupported retirement.",
            )

    def test_artifact_limit_is_deterministic_and_not_input_order_prefix(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            service = CodaWebService(
                runs_root=Path(temp_dir) / "runs",
                adapter_factories={
                    "static_analysis_nondeterminism": StaticAnalysisNondeterminismAdapter
                },
                orchestrator_factory=lambda: _build_test_orchestrator([]),
                bootstrap_factory=_build_test_bootstrap,
            )
            first = service.create_run(
                dataset_name="static_analysis_nondeterminism",
                artifact_limit=10,
                review_mode="selective",
            )
            second = service.create_run(
                dataset_name="static_analysis_nondeterminism",
                artifact_limit=10,
                review_mode="full",
            )
            first_ids = service._load_run_state(str(first["run_id"])).metadata[
                "all_selected_artifact_ids"
            ]
            second_ids = service._load_run_state(str(second["run_id"])).metadata[
                "all_selected_artifact_ids"
            ]
            input_prefix = [
                artifact.artifact_id
                for artifact in list(StaticAnalysisNondeterminismAdapter().iter_artifacts())[:10]
            ]

            self.assertEqual(first_ids, second_ids)
            self.assertNotEqual(first_ids, input_prefix)

    def test_two_views_of_llm_errors_share_selection_and_held_out_split(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            service = CodaWebService(
                runs_root=Path(temp_dir) / "runs",
                adapter_factories={
                    "llm_code_error_semantic": Defects4CodeLLMSemanticAdapter,
                    "llm_code_error_syntactic": Defects4CodeLLMSyntacticAdapter,
                },
                orchestrator_factory=lambda: _build_test_orchestrator([]),
                bootstrap_factory=_build_test_bootstrap,
            )
            semantic = service.create_run(
                dataset_name="llm_code_error_semantic",
                artifact_limit=30,
                review_mode="full",
            )
            syntactic = service.create_run(
                dataset_name="llm_code_error_syntactic",
                artifact_limit=30,
                review_mode="full",
            )
            semantic_state = service._load_run_state(str(semantic["run_id"]))
            syntactic_state = service._load_run_state(str(syntactic["run_id"]))

            self.assertEqual(
                semantic_state.metadata["all_selected_artifact_ids"],
                syntactic_state.metadata["all_selected_artifact_ids"],
            )
            self.assertEqual(semantic_state.total_held_out_artifacts, 0)
            self.assertEqual(syntactic_state.total_held_out_artifacts, 0)

    def test_held_out_artifacts_are_not_passed_to_bootstrap(self) -> None:
        received_ids: list[str] = []

        def recording_bootstrap(_: CODAOrchestrator):
            class RecordingBootstrap:
                def run(self, run_state, artifacts):
                    received_ids.extend(item.artifact_id for item in artifacts)
                    return BootstrapResult(
                        codebook=CodebookState.empty(run_state.dataset_metadata.dataset_name),
                        artifact_ids=[],
                        group_ids={item.artifact_id: item.artifact_id for item in artifacts},
                        protocol={"population_size": len(artifacts)},
                    )

            return RecordingBootstrap()

        with tempfile.TemporaryDirectory() as temp_dir:
            service = CodaWebService(
                runs_root=Path(temp_dir) / "runs",
                adapter_factories={
                    "static_analysis_nondeterminism": StaticAnalysisNondeterminismAdapter
                },
                orchestrator_factory=lambda: _build_test_orchestrator([]),
                bootstrap_factory=recording_bootstrap,
            )
            created = service.create_run(
                dataset_name="static_analysis_nondeterminism",
                artifact_limit=30,
                review_mode="full",
            )
            run_id = str(created["run_id"])
            before = service._load_run_state(run_id)
            service.initialize_run(run_id)

            self.assertEqual(set(received_ids), set(before.metadata["selected_artifact_ids"]))
            self.assertEqual(before.total_held_out_artifacts, 0)

    def test_automatic_terminal_status_reports_reached_stability(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            service = CodaWebService(
                runs_root=Path(temp_dir) / "runs",
                adapter_factories={
                    "static_analysis_nondeterminism": StaticAnalysisNondeterminismAdapter
                },
                orchestrator_factory=lambda: _build_test_orchestrator(
                    [],
                    relationship_to_codebook="reuse_existing_code",
                    coder_confidence_level="high",
                    validation_confidence_level="high",
                ),
                bootstrap_factory=_build_existing_code_bootstrap,
            )
            created = service.create_run(
                dataset_name="static_analysis_nondeterminism",
                artifact_limit=1,
                review_mode="automatic",
            )
            run_id = str(created["run_id"])
            run_state = service._load_run_state(run_id)
            run_state.review_policy.stabilization_required_consecutive_batches = 1
            service.initialize_run(run_id)

            result = service.process_automatic(run_id)

            self.assertEqual(result["run"]["status"], "stabilized")
            self.assertTrue(result["run"]["stabilization"]["stable"])

    def test_next_artifact_bounds_automatic_work_to_one_persisted_artifact(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            service = CodaWebService(
                runs_root=Path(temp_dir) / "runs",
                adapter_factories={
                    "static_analysis_nondeterminism": StaticAnalysisNondeterminismAdapter
                },
                orchestrator_factory=lambda: _build_test_orchestrator(
                    [],
                    relationship_to_codebook="reuse_existing_code",
                    coder_confidence_level="high",
                    validation_confidence_level="high",
                ),
                bootstrap_factory=_build_existing_code_bootstrap,
            )
            created = service.create_run(
                dataset_name="static_analysis_nondeterminism",
                artifact_limit=3,
                review_mode="selective",
            )
            run_id = str(created["run_id"])
            run_state = service._load_run_state(run_id)
            run_state.review_policy.random_audit_rate = 0.0
            service.initialize_run(run_id)
            service.submit_stage_review(
                run_id,
                "initial",
                decision="accept",
                rationale="The initial codebook is ready for iterative coding.",
            )
            run_state = service._load_run_state(run_id)
            run_state.review_policy.random_audit_rate = 0.0
            run_state.review_policy.evidence_audit_rate = 0.0
            first_artifact = run_state.current_batch().artifacts[0]
            run_state.history.append_record(
                CodingRecordState(
                    record_id="seed-reviewed-artifact",
                    artifact_id=first_artifact.artifact_id,
                    dataset_name=run_state.dataset_metadata.dataset_name,
                    batch_index=0,
                    codebook_version=run_state.codebook.version,
                    decision="accept",
                    rationale="Seed the explicit advance boundary.",
                    metadata={"human_reviewed": True},
                )
            )
            run_state.status = "awaiting_next_artifact"

            advanced = service.next_artifact(run_id)

            self.assertEqual(advanced["auto_processed"], 1)
            self.assertEqual(advanced["run"]["reviewed_artifacts"], 2)
            self.assertEqual(advanced["run"]["status"], "awaiting_next_artifact")
            self.assertEqual(len(run_state.history.coding_records), 2)

    def test_analytic_memo_can_be_resolved_and_reopened(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            service = CodaWebService(
                runs_root=Path(temp_dir) / "runs",
                adapter_factories={
                    "static_analysis_nondeterminism": StaticAnalysisNondeterminismAdapter
                },
                orchestrator_factory=lambda: _build_test_orchestrator([]),
                bootstrap_factory=_build_test_bootstrap,
            )
            created = service.create_run(
                dataset_name="static_analysis_nondeterminism",
                artifact_limit=1,
                review_mode="full",
            )
            run_id = str(created["run_id"])
            run_state = service._load_run_state(run_id)
            memo = run_state.history.append_analytic_memo(
                {"memo_type": "boundary", "summary": "Check the category boundary."}
            )
            memo_id = str(memo["memo_id"])

            resolved = service.update_analytic_memo_status(
                run_id,
                memo_id,
                status="resolved",
                rationale="The reviewed evidence establishes the boundary.",
            )
            self.assertEqual(resolved["memo"]["status"], "resolved")
            with self.assertRaisesRegex(WebWorkflowError, "already resolved"):
                service.update_analytic_memo_status(
                    run_id,
                    memo_id,
                    status="resolved",
                    rationale="Duplicate resolution.",
                )
            reopened = service.update_analytic_memo_status(
                run_id,
                memo_id,
                status="open",
                rationale="A later case contradicts the earlier boundary.",
            )
            self.assertEqual(reopened["memo"]["status"], "open")
            self.assertEqual(len(reopened["memo"]["status_history"]), 3)

    def test_hard_blocker_routes_to_human_even_below_score_threshold(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            service = CodaWebService(
                runs_root=Path(temp_dir) / "runs",
                adapter_factories={
                    "static_analysis_nondeterminism": StaticAnalysisNondeterminismAdapter
                },
                orchestrator_factory=lambda: _build_test_orchestrator(
                    [],
                    relationship_to_codebook="reuse_existing_code",
                    coder_confidence_level="low",
                    validation_confidence_level="high",
                    codebook_change_action="merge",
                ),
                bootstrap_factory=_build_existing_code_bootstrap,
            )
            created = service.create_run(
                dataset_name="static_analysis_nondeterminism",
                artifact_limit=1,
                review_mode="selective",
            )
            run_id = str(created["run_id"])
            run_state = service._load_run_state(run_id)
            run_state.review_policy.selective_review_score_threshold = 99
            run_state.review_policy.random_audit_rate = 0.0
            run_state.review_policy.evidence_audit_rate = 0.0
            service.initialize_run(run_id)
            service.submit_stage_review(
                run_id, "initial", decision="accept", rationale="Initial review complete."
            )

            result = service.process_automatic(run_id)

            self.assertTrue(result["stopped_for_human"])
            routing = service.review_packet(run_id)["review_input"]["evidence_packet"]["routing_decision"]
            self.assertIn("structural_codebook_change", routing["signal_details"]["hard_blockers"])

    def test_insufficient_context_is_not_duplicated_as_unstable_coder_output(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            service = CodaWebService(
                runs_root=Path(temp_dir) / "runs",
                adapter_factories={
                    "static_analysis_nondeterminism": StaticAnalysisNondeterminismAdapter
                },
                orchestrator_factory=lambda: _build_test_orchestrator(
                    [],
                    coder_insufficient_context=True,
                    relationship_to_codebook="reuse_existing_code",
                    coder_confidence_level="high",
                    validation_confidence_level="high",
                ),
                bootstrap_factory=_build_existing_code_bootstrap,
            )
            created = service.create_run(
                dataset_name="static_analysis_nondeterminism",
                artifact_limit=1,
                review_mode="selective",
            )
            run_id = str(created["run_id"])
            run_state = service._load_run_state(run_id)
            run_state.review_policy.selective_review_score_threshold = 99
            run_state.review_policy.random_audit_rate = 0.0
            run_state.review_policy.evidence_audit_rate = 0.0
            service.initialize_run(run_id)
            service.submit_stage_review(
                run_id, "initial", decision="accept", rationale="Initial review complete."
            )

            result = service.process_automatic(run_id)

            self.assertTrue(result["stopped_for_human"])
            routing = service.review_packet(run_id)["review_input"]["evidence_packet"][
                "routing_decision"
            ]
            self.assertIn("missing_context", routing["signal_details"]["hard_blockers"])
            self.assertNotIn(
                "unstable_coder_output", routing["signal_details"]["hard_blockers"]
            )
    def test_final_review_exposes_cross_source_cases_and_does_not_double_count_stability(self) -> None:
        class MultiSourceAdapter(StaticAnalysisNondeterminismAdapter):
            def iter_artifacts(self):
                for index, artifact in enumerate(super().iter_artifacts()):
                    yield replace(
                        artifact,
                        metadata={**artifact.metadata, "repo_name": f"repo-{index % 2}"},
                    )

        with tempfile.TemporaryDirectory() as temp_dir:
            service = CodaWebService(
                runs_root=Path(temp_dir) / "runs",
                adapter_factories={
                    "static_analysis_nondeterminism": MultiSourceAdapter
                },
                orchestrator_factory=lambda: _build_test_orchestrator([]),
                bootstrap_factory=_build_test_bootstrap,
            )
            created = service.create_run(
                dataset_name="static_analysis_nondeterminism",
                artifact_limit=2,
                review_mode="full",
            )
            run_id = str(created["run_id"])
            run_state = service._load_run_state(run_id)
            selected_ids = list(run_state.metadata["selected_artifact_ids"])
            for index, artifact_id in enumerate(selected_ids):
                run_state.history.append_record(
                    CodingRecordState(
                        record_id=f"record-{index}",
                        artifact_id=artifact_id,
                        dataset_name=run_state.dataset_metadata.dataset_name,
                        batch_index=index,
                        codebook_version=run_state.codebook.version,
                        decision="accept",
                        rationale="Processed before final audit.",
                        metadata={"human_reviewed": True},
                    )
                )
            run_state.status = "awaiting_final_review"

            first = service._record_stabilization_check(run_state, final=True)
            second = service._record_stabilization_check(run_state, final=True)
            self.assertEqual(first.consecutive_stable_batches, 1)
            self.assertEqual(second.consecutive_stable_batches, 1)
            self.assertEqual(second.cross_source_audit_status, "presented_for_final_review")

            service._run_final_validation(run_state, second)
            packet = service.stage_review_packet(run_id, "final")
            self.assertEqual(len(packet["cross_source_audit_artifacts"]), 2)
            self.assertEqual(len(packet["cross_source_audit_records"]), 2)
            service.submit_stage_review(
                run_id,
                "final",
                decision="accept",
                rationale="Cross-source cases and final boundaries were checked.",
            )
            self.assertEqual(
                run_state.history.stabilization_checks[-1].cross_source_audit_status,
                "human_review_completed",
            )

    def test_current_review_settings_control_stage_review_boundaries(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            full_service = CodaWebService(
                runs_root=Path(temp_dir) / "full-runs",
                adapter_factories={
                    "static_analysis_nondeterminism": StaticAnalysisNondeterminismAdapter
                },
                orchestrator_factory=lambda: _build_test_orchestrator([]),
                bootstrap_factory=_build_test_bootstrap,
            )
            full = full_service.create_run(
                dataset_name="static_analysis_nondeterminism",
                artifact_limit=1,
                review_mode="full",
            )
            full_id = str(full["run_id"])
            full_initialized = full_service.initialize_run(full_id)
            self.assertEqual(full_initialized["status"], "awaiting_initial_review")

            automatic_service = CodaWebService(
                runs_root=Path(temp_dir) / "automatic-runs",
                adapter_factories={
                    "static_analysis_nondeterminism": StaticAnalysisNondeterminismAdapter
                },
                orchestrator_factory=lambda: _build_test_orchestrator(
                    [],
                    relationship_to_codebook="reuse_existing_code",
                    coder_confidence_level="high",
                    validation_confidence_level="high",
                ),
                bootstrap_factory=_build_existing_code_bootstrap,
            )
            automatic = automatic_service.create_run(
                dataset_name="static_analysis_nondeterminism",
                artifact_limit=1,
                review_mode="automatic",
            )
            automatic_id = str(automatic["run_id"])
            initialized = automatic_service.initialize_run(automatic_id)
            self.assertNotEqual(initialized["status"], "awaiting_initial_review")
            processed = automatic_service.process_automatic(automatic_id)
            self.assertEqual(
                processed["run"]["status"], "completed_with_unresolved"
            )

    def test_selective_review_budget_preserves_risky_cases_as_unresolved(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            service = CodaWebService(
                runs_root=Path(temp_dir) / "runs",
                adapter_factories={
                    "static_analysis_nondeterminism": StaticAnalysisNondeterminismAdapter
                },
                orchestrator_factory=lambda: _build_test_orchestrator(
                    [],
                    relationship_to_codebook="reuse_existing_code",
                    coder_confidence_level="low",
                    coder_insufficient_context=True,
                    validation_confidence_level="high",
                ),
                bootstrap_factory=_build_existing_code_bootstrap,
            )
            created = service.create_run(
                dataset_name="static_analysis_nondeterminism",
                artifact_limit=2,
                review_mode="selective",
                review_budget_minutes=1,
            )
            run_id = str(created["run_id"])
            run_state = service._load_run_state(run_id)
            run_state.review_policy.random_audit_rate = 0.0
            service.initialize_run(run_id)
            service.submit_stage_review(
                run_id,
                "initial",
                decision="accept",
                rationale="The initial scheme is usable.",
                duration_seconds=60,
            )

            result = service.process_automatic(run_id)

            self.assertFalse(result["stopped_for_human"])
            self.assertEqual(result["auto_processed"], 2)
            summary = service.run_summary(run_id)
            self.assertEqual(summary["status"], "resource_limited")
            self.assertTrue(summary["review_budget_exhausted"])
            self.assertEqual(summary["review_time_used_seconds"], 60)
            self.assertEqual(summary["open_unresolved_count"], 2)
            records = service.history(run_id)["coding_records"]
            self.assertTrue(
                all(
                    record["metadata"].get("resource_limit")
                    == "review_budget_exhausted"
                    for record in records
                )
            )

    def test_full_review_budget_stops_without_accepting_remaining_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            service = CodaWebService(
                runs_root=Path(temp_dir) / "runs",
                adapter_factories={
                    "static_analysis_nondeterminism": StaticAnalysisNondeterminismAdapter
                },
                orchestrator_factory=lambda: _build_test_orchestrator([]),
                bootstrap_factory=_build_existing_code_bootstrap,
            )
            created = service.create_run(
                dataset_name="static_analysis_nondeterminism",
                artifact_limit=2,
                review_mode="full",
                review_budget_minutes=1,
            )
            run_id = str(created["run_id"])
            service.initialize_run(run_id)

            submitted = service.submit_stage_review(
                run_id,
                "initial",
                decision="accept",
                rationale="The initial scheme is usable.",
                duration_seconds=60,
            )

            self.assertEqual(submitted["run"]["status"], "resource_limited")
            self.assertEqual(submitted["run"]["reviewed_artifacts"], 0)
            self.assertEqual(submitted["run"]["open_unresolved_count"], 2)
            with self.assertRaisesRegex(WebWorkflowError, "no remaining review work"):
                service.prepare_review(run_id)

    def test_selective_final_coverage_counts_bootstrap_and_iterative_artifacts(self) -> None:
        class SampleBootstrap:
            def run(self, run_state, artifacts):
                sample_id = artifacts[0].artifact_id
                code = CodeState(
                    code_id="analysis-logic",
                    name="Analysis Logic",
                    definition="A root cause in analysis logic.",
                    representative_artifact_ids=[sample_id],
                )
                return BootstrapResult(
                    codebook=CodebookState(
                        dataset_name=run_state.dataset_metadata.dataset_name,
                        version=1,
                        codes=[code],
                    ),
                    artifact_ids=[sample_id],
                    group_ids={artifact.artifact_id: artifact.artifact_id for artifact in artifacts},
                    protocol={"population_size": len(artifacts)},
                )

        with tempfile.TemporaryDirectory() as temp_dir:
            service = CodaWebService(
                runs_root=Path(temp_dir) / "runs",
                adapter_factories={
                    "static_analysis_nondeterminism": StaticAnalysisNondeterminismAdapter
                },
                orchestrator_factory=lambda: _build_test_orchestrator(
                    [],
                    relationship_to_codebook="reuse_existing_code",
                    coder_confidence_level="high",
                    validation_confidence_level="high",
                ),
                bootstrap_factory=lambda _: SampleBootstrap(),
            )
            created = service.create_run(
                dataset_name="static_analysis_nondeterminism",
                artifact_limit=2,
                review_mode="selective",
            )
            run_id = str(created["run_id"])
            service.initialize_run(run_id)
            run_state = service._load_run_state(run_id)
            run_state.review_policy.random_audit_rate = 0.0
            service.submit_stage_review(
                run_id,
                "initial",
                decision="accept",
                rationale="The provisional codebook fits the sampled evidence.",
            )
            service.process_automatic(run_id)
            final_packet = service.stage_review_packet(run_id, "final")
            coverage = final_packet["coverage"]
            self.assertEqual(coverage["input_artifacts"], 2)
            self.assertEqual(coverage["processed_artifacts"], 2)
            self.assertEqual(coverage["bootstrap_artifacts"], 1)
            self.assertEqual(coverage["iterative_artifacts"], 1)

    def test_initial_review_packet_exposes_sampled_artifacts_and_bootstrap_coverage(self) -> None:
        class SampleBootstrap:
            def run(self, run_state, artifacts):
                sampled = artifacts[:1]
                return BootstrapResult(
                    codebook=CodebookState.empty(run_state.dataset_metadata.dataset_name),
                    artifact_ids=[artifact.artifact_id for artifact in sampled],
                    group_ids={artifact.artifact_id: artifact.artifact_id for artifact in artifacts},
                    protocol={"population_size": len(artifacts)},
                )

        with tempfile.TemporaryDirectory() as temp_dir:
            service = CodaWebService(
                runs_root=Path(temp_dir) / "runs",
                adapter_factories={
                    "static_analysis_nondeterminism": StaticAnalysisNondeterminismAdapter
                },
                orchestrator_factory=lambda: _build_test_orchestrator([]),
                bootstrap_factory=lambda _: SampleBootstrap(),
            )
            created = service.create_run(
                dataset_name="static_analysis_nondeterminism",
                artifact_limit=2,
                review_mode="full",
            )
            run_id = str(created["run_id"])
            initialized = service.initialize_run(run_id)
            self.assertEqual(initialized["bootstrap_artifacts"], 1)
            packet = service.stage_review_packet(run_id, "initial")
            sampled = packet["sampled_artifacts"]
            self.assertEqual(len(sampled), 1)
            self.assertEqual(
                sampled[0]["artifact_id"],
                packet["bootstrap"]["artifact_ids"][0],
            )

    def test_final_review_accept_is_blocked_before_propagation_without_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            service = CodaWebService(
                runs_root=Path(temp_dir) / "runs",
                adapter_factories={
                    "static_analysis_nondeterminism": StaticAnalysisNondeterminismAdapter
                },
                orchestrator_factory=lambda: _build_test_orchestrator([]),
                bootstrap_factory=_build_test_bootstrap,
            )
            created = service.create_run(
                dataset_name="static_analysis_nondeterminism",
                artifact_limit=1,
                review_mode="full",
            )
            run_id = str(created["run_id"])
            service.initialize_run(run_id)
            run_state = service._load_run_state(run_id)
            run_state.status = "awaiting_final_review"
            run_state.history.append_retrospective_task(
                RetrospectiveRecodingTask(
                    task_id="retro-pending",
                    artifact_id="artifact-1",
                    trigger_change_id="change-1",
                    from_codebook_version=0,
                    target_codebook_version=1,
                    reason="A pending propagation check.",
                )
            )
            before_version = run_state.codebook.version
            with self.assertRaisesRegex(WebWorkflowError, "Complete all retrospective"):
                service.submit_stage_review(
                    run_id,
                    "final",
                    decision="accept",
                    rationale="The result looks complete.",
                )
            self.assertEqual(service.run_summary(run_id)["status"], "awaiting_final_review")
            self.assertEqual(service._load_run_state(run_id).codebook.version, before_version)
            self.assertEqual(service.history(run_id)["stage_reviews"], [])

    def test_initial_review_revision_queues_affected_bootstrap_cases(self) -> None:
        class SampleBootstrap:
            def run(self, run_state, artifacts):
                sample_id = artifacts[0].artifact_id
                code = CodeState(
                    code_id="initial-concept",
                    name="Initial Concept",
                    definition="A provisional concept.",
                    representative_artifact_ids=[sample_id],
                )
                return BootstrapResult(
                    codebook=CodebookState(
                        dataset_name=run_state.dataset_metadata.dataset_name,
                        version=1,
                        codes=[code],
                    ),
                    artifact_ids=[sample_id],
                    group_ids={artifact.artifact_id: artifact.artifact_id for artifact in artifacts},
                    protocol={"population_size": len(artifacts)},
                )

        with tempfile.TemporaryDirectory() as temp_dir:
            service = CodaWebService(
                runs_root=Path(temp_dir) / "runs",
                adapter_factories={
                    "static_analysis_nondeterminism": StaticAnalysisNondeterminismAdapter
                },
                orchestrator_factory=lambda: _build_test_orchestrator([]),
                bootstrap_factory=lambda _: SampleBootstrap(),
            )
            created = service.create_run(
                dataset_name="static_analysis_nondeterminism",
                artifact_limit=2,
                review_mode="full",
            )
            run_id = str(created["run_id"])
            service.initialize_run(run_id)
            packet = service.stage_review_packet(run_id, "initial")
            code = CodeState(
                code_id="initial-concept",
                name="Initial Concept",
                definition="A clarified provisional concept.",
                representative_artifact_ids=packet["codebook"]["codes"][0]["representative_artifact_ids"],
            )
            service.submit_stage_review(
                run_id,
                "initial",
                decision="revise",
                rationale="The definition needs a boundary clarification.",
                revised_codes=[code],
            )
            tasks = service.retrospective_tasks(run_id)
            self.assertEqual(tasks["pending_count"], 1)
            self.assertEqual(tasks["tasks"][0]["artifact_id"], packet["bootstrap"]["artifact_ids"][0])

    def test_selective_mode_automatically_accepts_unambiguous_existing_reuse(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            service = CodaWebService(
                runs_root=Path(temp_dir) / "runs",
                adapter_factories={
                    "static_analysis_nondeterminism": StaticAnalysisNondeterminismAdapter
                },
                orchestrator_factory=lambda: _build_test_orchestrator(
                    [],
                    relationship_to_codebook="reuse_existing_code",
                    coder_confidence_level="high",
                    validation_confidence_level="high",
                ),
                bootstrap_factory=_build_existing_code_bootstrap,
            )
            created = service.create_run(
                dataset_name="static_analysis_nondeterminism",
                artifact_limit=2,
                review_mode="selective",
            )
            run_id = str(created["run_id"])
            run_state = service._load_run_state(run_id)
            run_state.review_policy.random_audit_rate = 0.0
            run_state.review_policy.evidence_audit_rate = 0.0
            service.initialize_run(run_id)
            service.submit_stage_review(
                run_id,
                "initial",
                decision="accept",
                rationale="The initial scheme is usable.",
            )

            result = service.process_automatic(run_id)

            self.assertFalse(result["stopped_for_human"])
            self.assertEqual(result["auto_processed"], 2)
            summary = service.run_summary(run_id)
            self.assertEqual(summary["status"], "awaiting_final_review")
            self.assertEqual(summary["reviewed_artifacts"], 2)
            self.assertEqual(summary["human_reviewed_artifacts"], 0)
            self.assertEqual(summary["auto_processed_artifacts"], 2)
            records = service.history(run_id)["coding_records"]
            self.assertEqual(len(records), 2)
            self.assertTrue(
                all(
                    record["metadata"]["review_origin"] == "automatic_policy"
                    and record["metadata"]["human_reviewed"] is False
                    for record in records
                )
            )

    def test_selective_mode_allows_medium_coder_confidence_without_other_risk(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            service = CodaWebService(
                runs_root=Path(temp_dir) / "runs",
                adapter_factories={
                    "static_analysis_nondeterminism": StaticAnalysisNondeterminismAdapter
                },
                orchestrator_factory=lambda: _build_test_orchestrator(
                    [],
                    relationship_to_codebook="reuse_existing_code",
                    coder_confidence_level="medium",
                    validation_confidence_level="high",
                ),
                bootstrap_factory=_build_existing_code_bootstrap,
            )
            created = service.create_run(
                dataset_name="static_analysis_nondeterminism",
                artifact_limit=1,
                review_mode="selective",
            )
            run_id = str(created["run_id"])
            run_state = service._load_run_state(run_id)
            run_state.review_policy.random_audit_rate = 0.0
            service.initialize_run(run_id)
            service.submit_stage_review(
                run_id, "initial", decision="accept", rationale="Initial review complete."
            )

            result = service.process_automatic(run_id)

            self.assertFalse(result["stopped_for_human"])
            self.assertEqual(result["auto_processed"], 1)

    def test_selective_mode_allows_medium_validation_confidence_without_other_risk(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            service = CodaWebService(
                runs_root=Path(temp_dir) / "runs",
                adapter_factories={
                    "static_analysis_nondeterminism": StaticAnalysisNondeterminismAdapter
                },
                orchestrator_factory=lambda: _build_test_orchestrator(
                    [],
                    relationship_to_codebook="reuse_existing_code",
                    coder_confidence_level="high",
                    validation_confidence_level="medium",
                ),
                bootstrap_factory=_build_existing_code_bootstrap,
            )
            created = service.create_run(
                dataset_name="static_analysis_nondeterminism",
                artifact_limit=1,
                review_mode="selective",
            )
            run_id = str(created["run_id"])
            run_state = service._load_run_state(run_id)
            run_state.review_policy.random_audit_rate = 0.0
            service.initialize_run(run_id)
            service.submit_stage_review(
                run_id, "initial", decision="accept", rationale="Initial review complete."
            )

            result = service.process_automatic(run_id)

            self.assertFalse(result["stopped_for_human"])
            self.assertEqual(result["auto_processed"], 1)

    def test_selective_mode_does_not_stop_for_low_confidence_alone(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            service = CodaWebService(
                runs_root=Path(temp_dir) / "runs",
                adapter_factories={
                    "static_analysis_nondeterminism": StaticAnalysisNondeterminismAdapter
                },
                orchestrator_factory=lambda: _build_test_orchestrator(
                    [],
                    relationship_to_codebook="reuse_existing_code",
                ),
                bootstrap_factory=_build_existing_code_bootstrap,
            )
            created = service.create_run(
                dataset_name="static_analysis_nondeterminism",
                artifact_limit=2,
                review_mode="selective",
            )
            run_id = str(created["run_id"])
            run_state = service._load_run_state(run_id)
            run_state.review_policy.selective_review_score_threshold = 99
            run_state.review_policy.random_audit_rate = 0.0
            run_state.review_policy.evidence_audit_rate = 0.0
            service.initialize_run(run_id)
            service.submit_stage_review(
                run_id, "initial", decision="accept", rationale="Initial review complete."
            )

            result = service.process_automatic(run_id)

            self.assertFalse(result["stopped_for_human"])
            self.assertEqual(result["auto_processed"], 2)
            self.assertNotEqual(service.run_summary(run_id)["status"], "awaiting_human_review")
            self.assertEqual(service.run_summary(run_id)["reviewed_artifacts"], 2)
            self.assertEqual(len(service.history(run_id)["coding_records"]), 2)

    def test_selective_mode_automatically_accepts_safe_local_new_code(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            service = CodaWebService(
                runs_root=Path(temp_dir) / "runs",
                adapter_factories={
                    "static_analysis_nondeterminism": StaticAnalysisNondeterminismAdapter
                },
                orchestrator_factory=lambda: _build_test_orchestrator(
                    [],
                    relationship_to_codebook="new_code",
                    coder_confidence_level="high",
                    validation_confidence_level="high",
                ),
                bootstrap_factory=_build_existing_code_bootstrap,
            )
            created = service.create_run(
                dataset_name="static_analysis_nondeterminism",
                artifact_limit=1,
                review_mode="selective",
            )
            run_id = str(created["run_id"])
            run_state = service._load_run_state(run_id)
            run_state.review_policy.random_audit_rate = 0.0
            run_state.review_policy.evidence_audit_rate = 0.0
            service.initialize_run(run_id)
            service.submit_stage_review(
                run_id, "initial", decision="accept", rationale="Initial review complete."
            )

            result = service.process_automatic(run_id)

            self.assertFalse(result["stopped_for_human"])
            self.assertEqual(result["auto_processed"], 1)
            records = service.history(run_id)["coding_records"]
            self.assertEqual(len(records), 1)
            self.assertEqual(records[0]["metadata"]["review_origin"], "automatic_policy")
            self.assertEqual(len(service.codebook(run_id)["codes"]), 2)
            self.assertTrue(
                any(
                    change["action"] == "add"
                    and change["decided_by"] == "automatic"
                    for change in service.history(run_id)["codebook_revisions"]
                )
            )

    def test_selective_mode_routes_duplicate_new_code_candidates_to_human(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            service = CodaWebService(
                runs_root=Path(temp_dir) / "runs",
                adapter_factories={
                    "static_analysis_nondeterminism": StaticAnalysisNondeterminismAdapter
                },
                orchestrator_factory=lambda: _build_test_orchestrator(
                    [],
                    relationship_to_codebook="new_code",
                    coder_confidence_level="high",
                    validation_confidence_level="high",
                    duplicate_new_code_candidate=True,
                ),
                bootstrap_factory=_build_existing_code_bootstrap,
            )
            created = service.create_run(
                dataset_name="static_analysis_nondeterminism",
                artifact_limit=1,
                review_mode="selective",
            )
            run_id = str(created["run_id"])
            run_state = service._load_run_state(run_id)
            run_state.review_policy.random_audit_rate = 0.0
            run_state.review_policy.evidence_audit_rate = 0.0
            service.initialize_run(run_id)
            service.submit_stage_review(
                run_id, "initial", decision="accept", rationale="Initial review complete."
            )

            result = service.process_automatic(run_id)

            self.assertTrue(result["stopped_for_human"])
            routing = service.review_packet(run_id)["review_input"]["evidence_packet"][
                "routing_decision"
            ]
            self.assertIn("duplicate_new_code_candidate", routing["risk_signals"])
            self.assertEqual(service.history(run_id)["coding_records"], [])

    def test_full_mode_does_not_expose_automatic_processing(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            service = CodaWebService(
                runs_root=Path(temp_dir) / "runs",
                adapter_factories={
                    "static_analysis_nondeterminism": StaticAnalysisNondeterminismAdapter
                },
                orchestrator_factory=lambda: _build_test_orchestrator(
                    [], relationship_to_codebook="reuse_existing_code"
                ),
                bootstrap_factory=_build_existing_code_bootstrap,
            )
            created = service.create_run(
                dataset_name="static_analysis_nondeterminism",
                artifact_limit=1,
                review_mode="full",
            )
            run_id = str(created["run_id"])
            service.initialize_run(run_id)
            service.submit_stage_review(
                run_id, "initial", decision="accept", rationale="Initial review complete."
            )

            with self.assertRaisesRegex(WebWorkflowError, "only for Automatic or Selective"):
                service.process_automatic(run_id)

    def test_web_workflow_prepares_submits_then_requires_explicit_advance(self) -> None:
        call_log: list[str] = []
        with tempfile.TemporaryDirectory() as temp_dir:
            service = CodaWebService(
                runs_root=Path(temp_dir) / "runs",
                adapter_factories={
                    "static_analysis_nondeterminism": StaticAnalysisNondeterminismAdapter
                },
                orchestrator_factory=lambda: _build_test_orchestrator(call_log),
                bootstrap_factory=_build_test_bootstrap,
            )
            created = service.create_run(
                dataset_name="static_analysis_nondeterminism",
                artifact_limit=2,
                review_mode="full",
            )
            run_id = str(created["run_id"])

            self.assertEqual(created["bootstrap_status"], "not_run")
            self.assertIsNone(service.current_artifact(run_id)["artifact"])
            with self.assertRaises(WebWorkflowError):
                service.prepare_review(run_id)

            initialized = service.initialize_run(run_id)
            self.assertEqual(initialized["bootstrap_status"], "completed")
            service.submit_stage_review(
                run_id, "initial", decision="accept", rationale="Initial review complete."
            )

            current = service.current_artifact(run_id)
            artifact = current["artifact"]
            assert isinstance(artifact, dict)
            first_artifact_id = str(artifact["artifact_id"])

            packet = service.prepare_review(run_id)
            self.assertEqual(packet["artifact_id"], first_artifact_id)
            self.assertEqual(packet["codebook_version"], 0)
            self.assertEqual(
                call_log,
                [
                    f"context:{first_artifact_id}",
                    f"coder-a:{first_artifact_id}",
                    f"coder-b:{first_artifact_id}",
                    f"arbitration:{first_artifact_id}",
                    f"validation:{first_artifact_id}",
                ],
            )

            code = CodeState(
                code_id="analysis-logic",
                name="Analysis Logic",
                definition="Human-approved analysis root cause.",
                representative_artifact_ids=[first_artifact_id],
            )
            review = HumanReviewOutput(
                artifact_id=first_artifact_id,
                decision="accept",
                final_codes=[code],
                rationale="The evidence supports the proposed code.",
                evidence_summary=["Issue text supports the root cause."],
                confirmed_evidence=[
                    EvidenceItem(
                        field_name="content",
                        excerpt=str(artifact["content"])[:80],
                        rationale="The artifact text supports the code.",
                    )
                ],
                codebook_changes=[
                    CodebookChangeState(
                        change_id="change-1",
                        action="add",
                        round_index=0,
                        summary="Add Analysis Logic.",
                        rationale="The first reviewed artifact establishes this new concept.",
                        resulting_code_ids=[code.code_id],
                        artifact_ids=[first_artifact_id],
                    )
                ],
            )
            submitted = service.submit_review(run_id, human_review_output=review)
            self.assertEqual(submitted["decision"], "accept")
            self.assertEqual(submitted["codebook"]["version"], 1)
            self.assertEqual(service.run_summary(run_id)["status"], "awaiting_next_artifact")
            self.assertIsNone(service.current_artifact(run_id)["artifact"])

            history = service.history(run_id)
            records = history["coding_records"]
            revisions = history["codebook_revisions"]
            traces = history["artifact_runs"]
            self.assertEqual(len(records), 1)
            self.assertEqual(records[0]["artifact_id"], first_artifact_id)
            self.assertEqual(records[0]["decision"], "accept")
            self.assertEqual(len(revisions), 1)
            self.assertEqual(revisions[0]["action"], "add")
            self.assertEqual(len(traces), 1)
            self.assertEqual(traces[0]["artifact_id"], first_artifact_id)

            artifacts = service.run_artifacts(run_id)
            checkpoint = artifacts["checkpoint"]
            self.assertEqual(checkpoint["run_id"], run_id)
            self.assertEqual(checkpoint["review_count"], 1)
            self.assertEqual(checkpoint["codebook_version"], 1)
            self.assertEqual(len(artifacts["reviews"]), 1)
            self.assertEqual(len(artifacts["artifact_runs"]), 1)
            self.assertFalse(artifacts["final_codebook"]["available"])

            events = service._load_run_state(run_id).metadata["events"]
            event_names = [event["event"] for event in events]
            self.assertIn("run_created", event_names)
            self.assertIn("bootstrap_started", event_names)
            self.assertIn("bootstrap_finished", event_names)
            self.assertIn("artifact_processing_started", event_names)
            self.assertIn("artifact_waiting_for_human_review", event_names)
            self.assertIn("artifact_review_submitted", event_names)
            self.assertIn("artifact_processing_finished", event_names)
            self.assertGreaterEqual(event_names.count("iterative_started"), 1)
            self.assertGreaterEqual(event_names.count("iterative_paused"), 1)

            advanced = service.next_artifact(run_id)
            next_artifact = advanced["current"]["artifact"]
            assert isinstance(next_artifact, dict)
            self.assertNotEqual(next_artifact["artifact_id"], first_artifact_id)
            self.assertEqual(service.run_summary(run_id)["status"], "in_progress")

            run_dir = Path(str(created["run_dir"]))
            self.assertTrue((run_dir / "checkpoint.json").exists())
            self.assertTrue((run_dir / "reviews.jsonl").exists())
            self.assertTrue((run_dir / "artifact_runs.jsonl").exists())

    def test_human_added_evidence_is_grounded_and_invalid_evidence_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            service = CodaWebService(
                runs_root=Path(temp_dir) / "runs",
                adapter_factories={
                    "static_analysis_nondeterminism": StaticAnalysisNondeterminismAdapter
                },
                orchestrator_factory=lambda: _build_test_orchestrator([]),
                bootstrap_factory=_build_test_bootstrap,
            )
            created = service.create_run(
                dataset_name="static_analysis_nondeterminism",
                artifact_limit=1,
                review_mode="full",
            )
            run_id = str(created["run_id"])
            service.initialize_run(run_id)
            service.submit_stage_review(
                run_id, "initial", decision="accept", rationale="Initial review complete."
            )
            packet = service.prepare_review(run_id)
            artifact = packet["review_input"]["artifact"]
            artifact_id = str(packet["artifact_id"])
            content = str(artifact["content"])
            excerpt = content[:80]

            with self.assertRaisesRegex(ValueError, "does not exist in artifact"):
                service.submit_review(
                    run_id,
                    human_review_output=HumanReviewOutput(
                        artifact_id=artifact_id,
                        decision="reject",
                        rationale="The proposed interpretation is not supported.",
                        confirmed_evidence=[
                            EvidenceItem(
                                field_name="missing_field",
                                excerpt=excerpt,
                                rationale="Researcher-added evidence.",
                            )
                        ],
                    ),
                )

            with self.assertRaisesRegex(ValueError, "not present in artifact field"):
                service.submit_review(
                    run_id,
                    human_review_output=HumanReviewOutput(
                        artifact_id=artifact_id,
                        decision="reject",
                        rationale="The proposed interpretation is not supported.",
                        confirmed_evidence=[
                            EvidenceItem(
                                field_name="content",
                                excerpt="This text is not present in the artifact.",
                                rationale="Researcher-added evidence.",
                            )
                        ],
                    ),
                )

            service.submit_review(
                run_id,
                human_review_output=HumanReviewOutput(
                    artifact_id=artifact_id,
                    decision="reject",
                    rationale="The proposed interpretation is not supported.",
                    confirmed_evidence=[
                        EvidenceItem(
                            field_name="content",
                            excerpt=excerpt,
                            rationale="Researcher verified this exact source span.",
                        )
                    ],
                ),
            )
            record = service.history(run_id)["coding_records"][0]
            confirmed = record["metadata"]["confirmed_evidence"]
            self.assertEqual(confirmed[0]["field_name"], "content")
            self.assertEqual(confirmed[0]["excerpt"], excerpt)
            self.assertIsNotNone(confirmed[0]["locator"])
            evidence_audit = record["metadata"]["evidence_unit_audit"]
            self.assertEqual(evidence_audit["status"], "assessed")
            self.assertGreaterEqual(evidence_audit["agent_candidate_count"], 1)
            self.assertFalse(evidence_audit["omission_claimed"])

    def test_retrospective_recoding_is_append_only_and_does_not_block_normal_queue(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            service = CodaWebService(
                runs_root=Path(temp_dir) / "runs",
                adapter_factories={
                    "static_analysis_nondeterminism": StaticAnalysisNondeterminismAdapter
                },
                orchestrator_factory=lambda: _build_test_orchestrator([]),
                bootstrap_factory=_build_test_bootstrap,
            )
            created = service.create_run(
                dataset_name="static_analysis_nondeterminism",
                artifact_limit=2,
                review_mode="full",
            )
            run_id = str(created["run_id"])
            service.initialize_run(run_id)
            service.submit_stage_review(
                run_id, "initial", decision="accept", rationale="Initial review complete."
            )

            first = service.current_artifact(run_id)["artifact"]
            assert isinstance(first, dict)
            first_artifact_id = str(first["artifact_id"])
            service.prepare_review(run_id)
            first_code = CodeState(
                code_id="analysis-logic",
                name="Analysis Logic",
                definition="A root cause in analysis logic.",
                representative_artifact_ids=[first_artifact_id],
            )
            service.submit_review(
                run_id,
                human_review_output=HumanReviewOutput(
                    artifact_id=first_artifact_id,
                    decision="accept",
                    final_codes=[first_code],
                    rationale="The first artifact establishes the concept.",
                    evidence_summary=["The issue text supports the concept."],
                    confirmed_evidence=[
                        EvidenceItem(
                            field_name="content",
                            excerpt=str(first["content"])[:80],
                            rationale="The artifact text supports the code.",
                        )
                    ],
                    codebook_changes=[
                        CodebookChangeState(
                            change_id="add-analysis-logic",
                            action="add",
                            round_index=0,
                            summary="Add Analysis Logic.",
                            rationale="The first artifact establishes this concept.",
                            resulting_code_ids=[first_code.code_id],
                            artifact_ids=[first_artifact_id],
                        )
                    ],
                ),
            )
            service.next_artifact(run_id)

            second = service.current_artifact(run_id)["artifact"]
            assert isinstance(second, dict)
            second_artifact_id = str(second["artifact_id"])
            self.assertNotEqual(first_artifact_id, second_artifact_id)
            service.prepare_review(run_id)
            refined_code = CodeState(
                code_id="analysis-logic",
                name="Analysis Logic",
                definition="A root cause in analysis logic with a clarified boundary.",
                representative_artifact_ids=[first_artifact_id, second_artifact_id],
            )
            service.submit_review(
                run_id,
                human_review_output=HumanReviewOutput(
                    artifact_id=second_artifact_id,
                    decision="revise",
                    final_codes=[refined_code],
                    rationale="The second artifact clarifies the code boundary.",
                    evidence_summary=["The second issue distinguishes the boundary."],
                    confirmed_evidence=[
                        EvidenceItem(
                            field_name="content",
                            excerpt=str(second["content"])[:80],
                            rationale="The artifact text supports the refined boundary.",
                        )
                    ],
                    codebook_changes=[
                        CodebookChangeState(
                            change_id="refine-analysis-logic",
                            action="refine",
                            round_index=1,
                            summary="Refine the Analysis Logic boundary.",
                            rationale="The second artifact exposes a boundary that must be explicit.",
                            target_code_ids=[refined_code.code_id],
                            resulting_code_ids=[refined_code.code_id],
                            artifact_ids=[second_artifact_id],
                            metadata={
                                "affected_historical_artifact_ids": [first_artifact_id]
                            },
                        )
                    ],
                ),
            )

            before_retrospective = service.run_summary(run_id)
            self.assertEqual(before_retrospective["status"], "awaiting_next_artifact")
            tasks = service.retrospective_tasks(run_id)
            self.assertEqual(tasks["pending_count"], 1)
            task = tasks["tasks"][0]
            task_id = str(task["task_id"])
            self.assertEqual(task["artifact_id"], first_artifact_id)

            packet = service.prepare_retrospective_task(run_id, task_id)
            self.assertEqual(packet["review_kind"], "retrospective")
            self.assertEqual(packet["artifact_id"], first_artifact_id)
            self.assertEqual(service.run_summary(run_id)["status"], "awaiting_next_artifact")

            service.submit_retrospective_review(
                run_id,
                task_id,
                human_review_output=HumanReviewOutput(
                    artifact_id=first_artifact_id,
                    decision="accept",
                    final_codes=[refined_code],
                    rationale="The historical artifact remains consistent with the refined code.",
                    evidence_summary=["The original issue supports the refined boundary."],
                    confirmed_evidence=[
                        EvidenceItem(
                            field_name="content",
                            excerpt=str(first["content"])[:80],
                            rationale="The original artifact supports the refined boundary.",
                        )
                    ],
                ),
            )

            completed_tasks = service.retrospective_tasks(run_id)
            self.assertEqual(completed_tasks["pending_count"], 0)
            self.assertEqual(completed_tasks["tasks"][0]["status"], "completed")
            self.assertEqual(service.run_summary(run_id)["status"], "awaiting_next_artifact")
            records = service.history(run_id)["coding_records"]
            self.assertEqual(len(records), 3)
            original = next(record for record in records if record["record_id"] == task["metadata"]["previous_record_id"])
            replacement = records[-1]
            self.assertEqual(original["artifact_id"], first_artifact_id)
            self.assertEqual(replacement["artifact_id"], first_artifact_id)
            self.assertEqual(
                replacement["metadata"]["supersedes_record_id"],
                original["record_id"],
            )
            self.assertEqual(
                service.run_summary(run_id)["reviewed_artifacts"],
                2,
            )

    def test_retrospective_context_request_reopens_only_the_retrospective_task(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            service = CodaWebService(
                runs_root=Path(temp_dir) / "runs",
                adapter_factories={
                    "static_analysis_nondeterminism": StaticAnalysisNondeterminismAdapter
                },
                orchestrator_factory=lambda: _build_test_orchestrator([]),
                bootstrap_factory=_build_test_bootstrap,
            )
            created = service.create_run(
                dataset_name="static_analysis_nondeterminism",
                artifact_limit=1,
                review_mode="full",
            )
            run_id = str(created["run_id"])
            service.initialize_run(run_id)
            service.submit_stage_review(
                run_id, "initial", decision="accept", rationale="Initial review complete."
            )
            artifact_id = str(service.current_artifact(run_id)["artifact"]["artifact_id"])
            service.prepare_review(run_id)
            service.submit_review(
                run_id,
                human_review_output=HumanReviewOutput(
                    artifact_id=artifact_id,
                    decision="mark_uncertain",
                    rationale="The initial proposal is not supported.",
                ),
            )
            service.next_artifact(run_id)

            run_state = service._load_run_state(run_id)
            task = RetrospectiveRecodingTask(
                task_id="retrospective-context-test",
                artifact_id=artifact_id,
                trigger_change_id="manual-audit",
                from_codebook_version=run_state.codebook.version,
                target_codebook_version=run_state.codebook.version,
                reason="Recheck this historical decision.",
            )
            run_state.history.append_retrospective_task(task)
            packet = service.prepare_retrospective_task(run_id, task.task_id)
            self.assertEqual(packet["review_kind"], "retrospective")

            service.submit_retrospective_review(
                run_id,
                task.task_id,
                human_review_output=HumanReviewOutput(
                    artifact_id=artifact_id,
                    decision="request_additional_context",
                    rationale="The historical decision needs reproduction context.",
                    notes=["Provide the reproduction environment."],
                ),
            )
            self.assertEqual(task.status, "awaiting_human")
            request = service.context_requests(run_id)["requests"][-1]
            self.assertEqual(request["metadata"]["retrospective_task_id"], task.task_id)
            with self.assertRaisesRegex(WebWorkflowError, "context request"):
                service.prepare_retrospective_task(run_id, task.task_id)

            service.resolve_context_request(
                run_id,
                request["request_id"],
                supplied_context=["The reproduction uses the default runtime."],
                resolution="The missing environment is now available.",
            )
            self.assertEqual(task.status, "pending")
            self.assertEqual(run_state.status, "awaiting_final_review")
            self.assertNotIn(
                artifact_id,
                run_state.metadata.get("reopened_context_artifact_ids", []),
            )

            reopened = service.prepare_retrospective_task(run_id, task.task_id)
            self.assertEqual(reopened["artifact_id"], artifact_id)
            service.submit_retrospective_review(
                run_id,
                task.task_id,
                human_review_output=HumanReviewOutput(
                    artifact_id=artifact_id,
                    decision="mark_uncertain",
                    rationale="The added context confirms that no code applies.",
                ),
            )
            self.assertEqual(task.status, "completed")
            self.assertEqual(service.retrospective_tasks(run_id)["pending_count"], 0)

    def test_broken_retrospective_context_reference_is_atomic(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            service = CodaWebService(
                runs_root=Path(temp_dir) / "runs",
                adapter_factories={
                    "static_analysis_nondeterminism": StaticAnalysisNondeterminismAdapter
                },
                orchestrator_factory=lambda: _build_test_orchestrator([]),
            )
            created = service.create_run(
                dataset_name="static_analysis_nondeterminism",
                artifact_limit=1,
            )
            run_id = str(created["run_id"])
            run_state = service._load_run_state(run_id)
            request = ContextRequestState(
                request_id="broken-retrospective-context",
                scope="artifact",
                artifact_id="artifact-under-review",
                reason="More context is required.",
                requested_items=["Provide the missing environment."],
                created_at_codebook_version=run_state.codebook.version,
                metadata={"retrospective_task_id": "missing-task"},
            )
            run_state.history.append_context_request(request)

            with self.assertRaisesRegex(WebWorkflowError, "does not exist"):
                service.resolve_context_request(
                    run_id,
                    request.request_id,
                    supplied_context=["The missing environment is now documented."],
                    resolution="Context supplied.",
                )
            self.assertEqual(request.status, "pending")
            self.assertEqual(request.supplied_context, [])
            self.assertEqual(request.resolution, "")
            self.assertNotIn("resolved_by", request.metadata)

            with self.assertRaisesRegex(WebWorkflowError, "does not exist"):
                service.cancel_context_request(run_id, request.request_id)
            self.assertEqual(request.status, "pending")
            self.assertEqual(request.resolution, "")

    def test_prepared_artifact_review_blocks_parallel_retrospective_review(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            service = CodaWebService(
                runs_root=Path(temp_dir) / "runs",
                adapter_factories={
                    "static_analysis_nondeterminism": StaticAnalysisNondeterminismAdapter
                },
                orchestrator_factory=lambda: _build_test_orchestrator([]),
                bootstrap_factory=_build_test_bootstrap,
            )
            created = service.create_run(
                dataset_name="static_analysis_nondeterminism",
                artifact_limit=1,
                review_mode="full",
            )
            run_id = str(created["run_id"])
            service.initialize_run(run_id)
            service.submit_stage_review(
                run_id, "initial", decision="accept", rationale="Initial review complete."
            )
            artifact_id = str(service.current_artifact(run_id)["artifact"]["artifact_id"])
            service.prepare_review(run_id)
            run_state = service._load_run_state(run_id)
            task = RetrospectiveRecodingTask(
                task_id="parallel-retrospective",
                artifact_id=artifact_id,
                trigger_change_id="manual-audit",
                from_codebook_version=run_state.codebook.version,
                target_codebook_version=run_state.codebook.version,
            )
            run_state.history.append_retrospective_task(task)

            with self.assertRaisesRegex(WebWorkflowError, "current artifact review"):
                service.prepare_retrospective_task(run_id, task.task_id)
            self.assertEqual(task.status, "pending")

    def test_retrospective_packet_cache_is_isolated_by_run(self) -> None:
        call_log: list[str] = []
        with tempfile.TemporaryDirectory() as temp_dir:
            service = CodaWebService(
                runs_root=Path(temp_dir) / "runs",
                adapter_factories={
                    "static_analysis_nondeterminism": StaticAnalysisNondeterminismAdapter
                },
                orchestrator_factory=lambda: _build_test_orchestrator(call_log),
                bootstrap_factory=_build_test_bootstrap,
            )
            run_ids: list[str] = []
            for _ in range(2):
                created = service.create_run(
                    dataset_name="static_analysis_nondeterminism",
                    artifact_limit=1,
                    review_mode="full",
                )
                run_id = str(created["run_id"])
                run_ids.append(run_id)
                service.initialize_run(run_id)
                service.submit_stage_review(
                    run_id,
                    "initial",
                    decision="accept",
                    rationale="Initial review complete.",
                )
                artifact_id = str(
                    service.current_artifact(run_id)["artifact"]["artifact_id"]
                )
                run_state = service._load_run_state(run_id)
                run_state.history.append_retrospective_task(
                    RetrospectiveRecodingTask(
                        task_id="shared-task-id",
                        artifact_id=artifact_id,
                        trigger_change_id="manual-audit",
                        from_codebook_version=run_state.codebook.version,
                        target_codebook_version=run_state.codebook.version,
                    )
                )

            service.prepare_retrospective_task(run_ids[0], "shared-task-id")
            first_call_count = len(call_log)
            service.prepare_retrospective_task(run_ids[1], "shared-task-id")

            self.assertGreater(first_call_count, 0)
            self.assertEqual(len(call_log), first_call_count * 2)
            self.assertEqual(
                service._load_run_state(run_ids[0])
                .history.retrospective_task("shared-task-id")
                .status,
                "awaiting_human",
            )
            self.assertEqual(
                service._load_run_state(run_ids[1])
                .history.retrospective_task("shared-task-id")
                .status,
                "awaiting_human",
            )

    def test_stale_prepared_review_is_rejected_without_recording_a_decision(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            service = CodaWebService(
                runs_root=Path(temp_dir) / "runs",
                adapter_factories={
                    "static_analysis_nondeterminism": StaticAnalysisNondeterminismAdapter
                },
                orchestrator_factory=lambda: _build_test_orchestrator([]),
                bootstrap_factory=_build_test_bootstrap,
            )
            created = service.create_run(
                dataset_name="static_analysis_nondeterminism",
                artifact_limit=1,
                review_mode="full",
            )
            run_id = str(created["run_id"])
            service.initialize_run(run_id)
            service.submit_stage_review(
                run_id, "initial", decision="accept", rationale="Initial review complete."
            )
            packet = service.prepare_review(run_id)
            run_state = service._load_run_state(run_id)
            run_state.codebook = run_state.codebook.next_version(
                codes=list(run_state.codebook.codes)
            )

            with self.assertRaisesRegex(WebWorkflowError, "codebook changed"):
                service.submit_review(
                    run_id,
                    human_review_output=HumanReviewOutput(
                        artifact_id=str(packet["artifact_id"]),
                        decision="reject",
                        rationale="This stale packet must not be accepted.",
                    ),
                )
            self.assertEqual(service.history(run_id)["coding_records"], [])
            self.assertEqual(service.run_summary(run_id)["status"], "in_progress")
            refreshed = service.prepare_review(run_id)
            self.assertEqual(refreshed["codebook_version"], 1)

    def test_only_one_retrospective_packet_can_be_open_per_run(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            service = CodaWebService(
                runs_root=Path(temp_dir) / "runs",
                adapter_factories={
                    "static_analysis_nondeterminism": StaticAnalysisNondeterminismAdapter
                },
                orchestrator_factory=lambda: _build_test_orchestrator([]),
                bootstrap_factory=_build_test_bootstrap,
            )
            created = service.create_run(
                dataset_name="static_analysis_nondeterminism",
                artifact_limit=1,
                review_mode="full",
            )
            run_id = str(created["run_id"])
            service.initialize_run(run_id)
            service.submit_stage_review(
                run_id, "initial", decision="accept", rationale="Initial review complete."
            )
            artifact_id = str(service.current_artifact(run_id)["artifact"]["artifact_id"])
            run_state = service._load_run_state(run_id)
            for task_id in ("retrospective-a", "retrospective-b"):
                run_state.history.append_retrospective_task(
                    RetrospectiveRecodingTask(
                        task_id=task_id,
                        artifact_id=artifact_id,
                        trigger_change_id="manual-audit",
                        from_codebook_version=run_state.codebook.version,
                        target_codebook_version=run_state.codebook.version,
                    )
                )

            service.prepare_retrospective_task(run_id, "retrospective-a")
            with self.assertRaisesRegex(WebWorkflowError, "before opening another"):
                service.prepare_retrospective_task(run_id, "retrospective-b")
            self.assertEqual(
                run_state.history.retrospective_task("retrospective-b").status,
                "pending",
            )

    def test_retrospective_recoding_reuses_frozen_automatic_routing(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            service = CodaWebService(
                runs_root=Path(temp_dir) / "runs",
                adapter_factories={
                    "static_analysis_nondeterminism": StaticAnalysisNondeterminismAdapter
                },
                orchestrator_factory=lambda: _build_test_orchestrator(
                    [],
                    relationship_to_codebook="reuse_existing_code",
                    coder_confidence_level="high",
                    validation_confidence_level="high",
                ),
                bootstrap_factory=_build_existing_code_bootstrap,
            )
            created = service.create_run(
                dataset_name="static_analysis_nondeterminism",
                artifact_limit=1,
                review_mode="automatic",
            )
            run_id = str(created["run_id"])
            service.initialize_run(run_id)
            service.process_automatic(run_id)
            run_state = service._load_run_state(run_id)
            artifact_id = run_state.history.coding_records[0].artifact_id
            task = RetrospectiveRecodingTask(
                task_id="retrospective-safe",
                artifact_id=artifact_id,
                trigger_change_id="external-audit",
                from_codebook_version=run_state.codebook.version,
                target_codebook_version=run_state.codebook.version,
                reason="Recheck the historical assignment under the current definition.",
            )
            run_state.history.append_retrospective_task(task)

            result = service.prepare_retrospective_task(run_id, task.task_id)

            self.assertTrue(result["auto_processed"])
            self.assertEqual(result["routing_decision"]["route"], "automatic_accept")
            self.assertEqual(task.status, "completed")
            latest = run_state.history.latest_record_for_artifact(artifact_id)
            self.assertEqual(latest.metadata["review_origin"], "retrospective")
            self.assertEqual(latest.metadata["processing_origin"], "automatic_policy")
            self.assertFalse(latest.metadata["human_reviewed"])

    def test_last_automatic_retrospective_refreshes_final_stability(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            service = CodaWebService(
                runs_root=Path(temp_dir) / "runs",
                adapter_factories={
                    "static_analysis_nondeterminism": StaticAnalysisNondeterminismAdapter
                },
                orchestrator_factory=lambda: _build_test_orchestrator(
                    [],
                    relationship_to_codebook="reuse_existing_code",
                    coder_confidence_level="high",
                    validation_confidence_level="high",
                ),
                bootstrap_factory=_build_existing_code_bootstrap,
            )
            created = service.create_run(
                dataset_name="static_analysis_nondeterminism",
                artifact_limit=1,
                review_mode="selective",
            )
            run_id = str(created["run_id"])
            run_state = service._load_run_state(run_id)
            run_state.review_policy.random_audit_rate = 0.0
            run_state.review_policy.evidence_audit_rate = 0.0
            service.initialize_run(run_id)
            service.submit_stage_review(
                run_id, "initial", decision="accept", rationale="Initial review complete."
            )
            service.process_automatic(run_id)
            self.assertEqual(run_state.status, "awaiting_final_review")
            artifact_id = run_state.history.coding_records[0].artifact_id
            task = RetrospectiveRecodingTask(
                task_id="retrospective-final-refresh",
                artifact_id=artifact_id,
                trigger_change_id="external-audit",
                from_codebook_version=run_state.codebook.version,
                target_codebook_version=run_state.codebook.version,
                reason="Recheck before Final Review.",
            )
            run_state.history.append_retrospective_task(task)
            before_checks = len(run_state.history.stabilization_checks)

            result = service.prepare_retrospective_task(run_id, task.task_id)

            self.assertTrue(result["auto_processed"])
            self.assertEqual(run_state.status, "awaiting_final_review")
            self.assertGreater(len(run_state.history.stabilization_checks), before_checks)
            self.assertEqual(
                run_state.history.stabilization_checks[-1].pending_retrospective_count,
                0,
            )

    def test_bootstrap_progress_is_persisted_while_initialization_is_running(self) -> None:
        started = threading.Event()
        release = threading.Event()
        result_holder: list[dict[str, object]] = []
        error_holder: list[BaseException] = []

        class ProgressBootstrap:
            def run(self, run_state, artifacts, *, progress_callback):
                progress_callback(
                    {
                        "status": "running",
                        "phase": "evidence",
                        "processed_artifacts": 1,
                        "total_artifacts": 2,
                        "overall_completed": 1,
                        "overall_total": 8,
                        "percent": 13,
                        "current_artifact_id": artifacts[0].artifact_id,
                    }
                )
                started.set()
                if not release.wait(timeout=5):
                    raise AssertionError("test bootstrap was not released")
                progress_callback(
                    {
                        "status": "completed",
                        "phase": "completed",
                        "processed_artifacts": 2,
                        "total_artifacts": 2,
                        "overall_completed": 8,
                        "overall_total": 8,
                        "percent": 100,
                        "current_artifact_id": None,
                    }
                )
                return BootstrapResult(
                    codebook=CodebookState.empty(run_state.dataset_metadata.dataset_name),
                    artifact_ids=[],
                    group_ids={artifact.artifact_id: artifact.artifact_id for artifact in artifacts},
                    protocol={"population_size": len(artifacts)},
                )

        with tempfile.TemporaryDirectory() as temp_dir:
            service = CodaWebService(
                runs_root=Path(temp_dir) / "runs",
                adapter_factories={
                    "static_analysis_nondeterminism": StaticAnalysisNondeterminismAdapter
                },
                orchestrator_factory=lambda: _build_test_orchestrator([]),
                bootstrap_factory=lambda _: ProgressBootstrap(),
            )
            created = service.create_run(
                dataset_name="static_analysis_nondeterminism",
                artifact_limit=3,
            )
            run_id = str(created["run_id"])

            def initialize() -> None:
                try:
                    result_holder.append(service.initialize_run(run_id))
                except BaseException as error:  # pragma: no cover - surfaced below
                    error_holder.append(error)

            worker = threading.Thread(target=initialize, daemon=True)
            worker.start()
            self.assertTrue(started.wait(timeout=5))

            live_summary = service.run_summary(run_id)
            self.assertEqual(live_summary["bootstrap_status"], "running")
            self.assertEqual(
                live_summary["bootstrap_progress"]["processed_artifacts"],
                1,
            )
            self.assertEqual(live_summary["bootstrap_progress"]["total_artifacts"], 2)

            checkpoint_path = Path(str(created["run_dir"])) / "checkpoint.json"
            checkpoint = json.loads(checkpoint_path.read_text(encoding="utf-8"))
            self.assertEqual(checkpoint["metadata"]["bootstrap"]["status"], "running")
            self.assertEqual(
                checkpoint["metadata"]["bootstrap"]["progress"]["processed_artifacts"],
                1,
            )

            release.set()
            worker.join(timeout=5)
            self.assertFalse(worker.is_alive())
            self.assertEqual(error_holder, [])
            self.assertEqual(len(result_holder), 1)
            self.assertEqual(result_holder[0]["bootstrap_status"], "completed")

    def test_bootstrap_can_be_cancelled_and_resumed_from_preserved_checkpoints(self) -> None:
        started = threading.Event()

        class CancellableBootstrap:
            calls = 0

            def run(
                self,
                run_state,
                artifacts,
                *,
                progress_callback,
                checkpoint_dir,
                cancel_requested,
            ):
                type(self).calls += 1
                checkpoint_path = Path(checkpoint_dir) / "test-stage.json"
                checkpoint_path.parent.mkdir(parents=True, exist_ok=True)
                checkpoint_path.write_text('{"completed": true}', encoding="utf-8")
                if type(self).calls == 1:
                    progress_callback(
                        {
                            "status": "running",
                            "phase": "evidence",
                            "processed_artifacts": 1,
                            "total_artifacts": 1,
                            "overall_completed": 1,
                            "overall_total": 5,
                            "percent": 20,
                            "current_artifact_id": artifacts[0].artifact_id,
                        }
                    )
                    started.set()
                    while not cancel_requested():
                        threading.Event().wait(0.01)
                    raise BootstrapCancelledError("cancelled by test")
                return BootstrapResult(
                    codebook=CodebookState.empty(run_state.dataset_metadata.dataset_name),
                    artifact_ids=[],
                    group_ids={artifact.artifact_id: artifact.artifact_id for artifact in artifacts},
                    protocol={"population_size": len(artifacts)},
                )

        with tempfile.TemporaryDirectory() as temp_dir:
            service = CodaWebService(
                runs_root=Path(temp_dir) / "runs",
                adapter_factories={
                    "static_analysis_nondeterminism": StaticAnalysisNondeterminismAdapter
                },
                orchestrator_factory=lambda: _build_test_orchestrator([]),
                bootstrap_factory=lambda _: CancellableBootstrap(),
            )
            created = service.create_run(
                dataset_name="static_analysis_nondeterminism",
                artifact_limit=3,
            )
            run_id = str(created["run_id"])
            first_result: list[dict[str, object]] = []

            worker = threading.Thread(
                target=lambda: first_result.append(service.initialize_run(run_id)),
                daemon=True,
            )
            worker.start()
            self.assertTrue(started.wait(timeout=5))

            stopping = service.cancel_initialization(run_id)
            self.assertEqual(stopping["bootstrap_status"], "cancelling")
            worker.join(timeout=5)

            self.assertFalse(worker.is_alive())
            self.assertEqual(first_result[0]["bootstrap_status"], "cancelled")
            checkpoint = Path(str(created["run_dir"])) / "bootstrap_checkpoints" / "test-stage.json"
            self.assertTrue(checkpoint.exists())

            resumed = service.initialize_run(run_id)
            self.assertEqual(resumed["bootstrap_status"], "completed")
            self.assertEqual(CancellableBootstrap.calls, 2)

    def test_stale_running_bootstrap_is_reported_as_interrupted_and_can_resume(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            service = CodaWebService(
                runs_root=Path(temp_dir) / "runs",
                adapter_factories={
                    "static_analysis_nondeterminism": StaticAnalysisNondeterminismAdapter
                },
                orchestrator_factory=lambda: _build_test_orchestrator([]),
                bootstrap_factory=lambda _: type(
                    "CompletedBootstrap",
                    (),
                    {
                        "run": lambda self, run_state, artifacts: BootstrapResult(
                            codebook=CodebookState.empty(run_state.dataset_metadata.dataset_name),
                            artifact_ids=[],
                            group_ids={artifact.artifact_id: artifact.artifact_id for artifact in artifacts},
                            protocol={"population_size": len(artifacts)},
                        )
                    },
                )(),
            )
            created = service.create_run(
                dataset_name="static_analysis_nondeterminism",
                artifact_limit=2,
            )
            run_id = str(created["run_id"])
            state = service._load_run_state(run_id)
            state.metadata["bootstrap"]["status"] = "running"
            from coda.persistence import save_run_state_checkpoint
            save_run_state_checkpoint(state, Path(str(created["run_dir"])) / "checkpoint.json")

            self.assertEqual(service.run_summary(run_id)["bootstrap_status"], "interrupted")
            self.assertEqual(service.initialize_run(run_id)["bootstrap_status"], "completed")

    def test_web_runtime_passes_run_scoped_bootstrap_checkpoint_directory(self) -> None:
        received_checkpoint_dirs: list[Path] = []

        class CheckpointAwareBootstrap:
            def run(self, run_state, artifacts, *, checkpoint_dir):
                received_checkpoint_dirs.append(Path(checkpoint_dir))
                return BootstrapResult(
                    codebook=CodebookState.empty(
                        run_state.dataset_metadata.dataset_name
                    ),
                    artifact_ids=[],
                    group_ids={
                        artifact.artifact_id: artifact.artifact_id
                        for artifact in artifacts
                    },
                    protocol={"population_size": len(artifacts)},
                )

        with tempfile.TemporaryDirectory() as temp_dir:
            runs_root = Path(temp_dir) / "runs"
            service = CodaWebService(
                runs_root=runs_root,
                adapter_factories={
                    "static_analysis_nondeterminism": StaticAnalysisNondeterminismAdapter
                },
                orchestrator_factory=lambda: _build_test_orchestrator([]),
                bootstrap_factory=lambda _: CheckpointAwareBootstrap(),
            )
            created = service.create_run(
                dataset_name="static_analysis_nondeterminism",
                artifact_limit=3,
            )
            run_id = str(created["run_id"])

            service.initialize_run(run_id)

            self.assertEqual(
                received_checkpoint_dirs,
                [runs_root / run_id / "bootstrap_checkpoints"],
            )

    def test_cannot_advance_before_review_submission(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            service = CodaWebService(
                runs_root=Path(temp_dir) / "runs",
                adapter_factories={
                    "static_analysis_nondeterminism": StaticAnalysisNondeterminismAdapter
                },
                orchestrator_factory=lambda: _build_test_orchestrator([]),
            )
            created = service.create_run(
                dataset_name="static_analysis_nondeterminism",
                artifact_limit=1,
            )
            with self.assertRaises(WebWorkflowError):
                service.next_artifact(str(created["run_id"]))


    def test_delete_run_removes_persisted_directory_and_memory_state(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            service = CodaWebService(
                runs_root=Path(temp_dir) / "runs",
                adapter_factories={
                    "static_analysis_nondeterminism": StaticAnalysisNondeterminismAdapter
                },
                orchestrator_factory=lambda: _build_test_orchestrator([]),
            )
            created = service.create_run(
                dataset_name="static_analysis_nondeterminism",
                artifact_limit=1,
            )
            run_id = str(created["run_id"])
            run_dir = Path(str(created["run_dir"]))
            self.assertTrue(run_dir.exists())

            self.assertEqual(service.delete_run(run_id), {"run_id": run_id, "deleted": True})
            self.assertFalse(run_dir.exists())
            self.assertEqual(service.list_runs(), [])
            with self.assertRaisesRegex(WebWorkflowError, "does not exist"):
                service.run_summary(run_id)

    def test_context_request_resolution_requeues_the_artifact(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            service = CodaWebService(
                runs_root=Path(temp_dir) / "runs",
                adapter_factories={
                    "static_analysis_nondeterminism": StaticAnalysisNondeterminismAdapter
                },
                orchestrator_factory=lambda: _build_test_orchestrator([]),
                bootstrap_factory=_build_test_bootstrap,
            )
            created = service.create_run(
                dataset_name="static_analysis_nondeterminism",
                artifact_limit=1,
                review_mode="full",
            )
            run_id = str(created["run_id"])
            service.initialize_run(run_id)
            service.submit_stage_review(
                run_id, "initial", decision="accept", rationale="Initial review complete."
            )
            artifact_id = str(service.current_artifact(run_id)["artifact"]["artifact_id"])
            service.prepare_review(run_id)
            service.submit_review(
                run_id,
                human_review_output=HumanReviewOutput(
                    artifact_id=artifact_id,
                    decision="request_additional_context",
                    rationale="The issue needs the linked reproduction details.",
                    notes=["Please provide the reproduction command and environment."],
                ),
            )
            pending = service.context_requests(run_id)
            self.assertEqual(pending["pending_count"], 1)
            request_id = pending["requests"][0]["request_id"]
            state_before_context = service._load_run_state(run_id)
            artifact = state_before_context.coding_batches[0].artifacts[0]
            orchestrator = service._orchestrator_for(run_id)
            cache_key_without_resolution = orchestrator.stage_cache_key(
                state_before_context, artifact
            )
            resolved = service.resolve_context_request(
                run_id,
                request_id,
                supplied_context=["Reproduction uses the default analysis configuration."],
                resolution="The requested reproduction context has been recorded.",
            )
            self.assertEqual(resolved["pending_count"], 0)
            self.assertEqual(service.run_summary(run_id)["status"], "in_progress")
            state_after_context = service._load_run_state(run_id)
            cache_key_with_resolution = orchestrator.stage_cache_key(
                state_after_context, artifact
            )
            self.assertNotEqual(cache_key_without_resolution, cache_key_with_resolution)
            reopened = service.prepare_review(run_id)
            self.assertEqual(reopened["artifact_id"], artifact_id)
            service.submit_review(
                run_id,
                human_review_output=HumanReviewOutput(
                    artifact_id=artifact_id,
                    decision="reject",
                    rationale="The added context does not support the proposed interpretation.",
                ),
            )
            records = service.history(run_id)["coding_records"]
            self.assertEqual(len(records), 2)
            self.assertEqual(records[-1]["metadata"]["review_origin"], "context_reopen")

    def test_context_request_blocks_artifact_actions_until_resolved_or_cancelled(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            service = CodaWebService(
                runs_root=Path(temp_dir) / "runs",
                adapter_factories={
                    "static_analysis_nondeterminism": StaticAnalysisNondeterminismAdapter
                },
                orchestrator_factory=lambda: _build_test_orchestrator(
                    [],
                    coder_insufficient_context=True,
                ),
                bootstrap_factory=_build_test_bootstrap,
            )
            created = service.create_run(
                dataset_name="static_analysis_nondeterminism",
                artifact_limit=1,
                review_mode="selective",
            )
            run_id = str(created["run_id"])
            service.initialize_run(run_id)
            service.submit_stage_review(
                run_id,
                "initial",
                decision="accept",
                rationale="The deterministic initial codebook review is complete.",
            )
            artifact_id = str(service.current_artifact(run_id)["artifact"]["artifact_id"])
            routed = service.process_automatic(run_id)
            self.assertTrue(routed["stopped_for_human"])
            service.submit_review(
                run_id,
                human_review_output=HumanReviewOutput(
                    artifact_id=artifact_id,
                    decision="request_additional_context",
                    rationale="The available artifact omits the execution environment.",
                    notes=["Please provide the runtime version and configuration."],
                ),
            )

            self.assertEqual(service.run_summary(run_id)["status"], "awaiting_context")
            summary = service.run_summary(run_id)
            self.assertEqual(summary["reviewed_artifacts"], 0)
            self.assertEqual(summary["human_reviewed_artifacts"], 1)
            self.assertEqual(summary["pending_context_request_count"], 1)
            with self.assertRaisesRegex(WebWorkflowError, "pending context request"):
                service.prepare_review(run_id)
            with self.assertRaisesRegex(WebWorkflowError, "pending context request"):
                service.next_artifact(run_id)
            with self.assertRaisesRegex(WebWorkflowError, "pending context request"):
                service.process_automatic(run_id)

            request_id = service.context_requests(run_id)["requests"][0]["request_id"]
            service.cancel_context_request(run_id, request_id)
            cancelled_summary = service.run_summary(run_id)
            self.assertEqual(cancelled_summary["status"], "awaiting_next_artifact")
            self.assertEqual(cancelled_summary["reviewed_artifacts"], 1)
            self.assertEqual(cancelled_summary["open_unresolved_count"], 1)

    def test_stage_context_request_can_be_viewed_but_not_resubmitted(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            service = CodaWebService(
                runs_root=Path(temp_dir) / "runs",
                adapter_factories={
                    "static_analysis_nondeterminism": StaticAnalysisNondeterminismAdapter
                },
                orchestrator_factory=lambda: _build_test_orchestrator([]),
                bootstrap_factory=_build_test_bootstrap,
            )
            created = service.create_run(
                dataset_name="static_analysis_nondeterminism",
                artifact_limit=1,
                review_mode="full",
            )
            run_id = str(created["run_id"])
            service.initialize_run(run_id)
            first = service.submit_stage_review(
                run_id,
                "initial",
                decision="request_additional_context",
                rationale="The sampled material needs the original project context.",
            )
            self.assertEqual(first["run"]["status"], "awaiting_initial_review")

            # Refreshing the stage-review page must remain possible while the
            # pending request is being resolved; only a second decision is blocked.
            packet = service.stage_review_packet(run_id, "initial")
            self.assertEqual(len(packet["context_requests"]), 1)
            request_id = packet["context_requests"][0]["request_id"]
            with self.assertRaisesRegex(WebWorkflowError, "pending initial context request"):
                service.submit_stage_review(
                    run_id,
                    "initial",
                    decision="accept",
                    rationale="Retry should be blocked until the request is resolved.",
                )

            service.resolve_context_request(
                run_id,
                request_id,
                supplied_context=["The project uses the default runtime configuration."],
                resolution="The requested project context was added to the audit trail.",
            )
            accepted = service.submit_stage_review(
                run_id,
                "initial",
                decision="accept",
                rationale="The sampled material is now interpretable.",
            )
            self.assertEqual(accepted["run"]["status"], "in_progress")

    def test_initial_mark_unresolved_records_concern_and_continues(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            service = CodaWebService(
                runs_root=Path(temp_dir) / "runs",
                adapter_factories={
                    "static_analysis_nondeterminism": StaticAnalysisNondeterminismAdapter
                },
                orchestrator_factory=lambda: _build_test_orchestrator([]),
                bootstrap_factory=_build_test_bootstrap,
            )
            created = service.create_run(
                dataset_name="static_analysis_nondeterminism",
                artifact_limit=1,
                review_mode="full",
            )
            run_id = str(created["run_id"])
            service.initialize_run(run_id)

            result = service.submit_stage_review(
                run_id,
                "initial",
                decision="mark_unresolved",
                rationale="The initial granularity remains uncertain.",
            )

            self.assertEqual(result["run"]["status"], "in_progress")
            unresolved = service.history(run_id)["unresolved_cases"]
            self.assertEqual(len(unresolved), 1)
            self.assertEqual(unresolved[0]["artifact_id"], "stage-review:initial")
            self.assertEqual(unresolved[0]["source"], "initial_human_review")

    def test_final_mark_unresolved_closes_run_with_auditable_concern(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            service = CodaWebService(
                runs_root=Path(temp_dir) / "runs",
                adapter_factories={
                    "static_analysis_nondeterminism": StaticAnalysisNondeterminismAdapter
                },
                orchestrator_factory=lambda: _build_test_orchestrator([]),
                bootstrap_factory=_build_test_bootstrap,
            )
            created = service.create_run(
                dataset_name="static_analysis_nondeterminism",
                artifact_limit=1,
                review_mode="full",
            )
            run_id = str(created["run_id"])
            service.initialize_run(run_id)
            service.submit_stage_review(
                run_id, "initial", decision="accept", rationale="Initial review complete."
            )
            artifact_id = str(service.current_artifact(run_id)["artifact"]["artifact_id"])
            service.prepare_review(run_id)
            service.submit_review(
                run_id,
                human_review_output=HumanReviewOutput(
                    artifact_id=artifact_id,
                    decision="mark_uncertain",
                    rationale="No defensible code assignment is supported.",
                ),
            )
            advanced = service.next_artifact(run_id)
            self.assertEqual(advanced["run"]["status"], "awaiting_final_review")

            result = service.submit_stage_review(
                run_id,
                "final",
                decision="mark_unresolved",
                rationale="The final category coverage cannot be resolved from available data.",
            )

            self.assertEqual(result["run"]["status"], "completed_with_unresolved")
            unresolved = service.history(run_id)["unresolved_cases"]
            self.assertEqual(unresolved[-1]["artifact_id"], "stage-review:final")
            self.assertEqual(unresolved[-1]["source"], "final_human_review")
            self.assertTrue(service.run_artifacts(run_id)["final_codebook"]["available"])


if __name__ == "__main__":
    unittest.main()
