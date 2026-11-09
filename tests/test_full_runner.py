from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from adapters.static_analysis import StaticAnalysisNondeterminismAdapter
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
from coda.full_runner import (
    FullRunPaths,
    build_single_batch_run_state,
    pending_artifacts_for_batch,
    run_resumable_full_coding,
)
from coda.orchestrator import CODAOrchestrator
from coda.persistence import load_run_state_checkpoint, save_run_state_checkpoint
from coda.state import CodeState, CodebookChangeState


def _build_test_orchestrator(call_log: list[str]) -> CODAOrchestrator:
    def context_agent(agent_input: ContextAgentInput) -> ContextPacket:
        call_log.append(f"context:{agent_input.artifact.artifact_id}")
        return ContextPacket(
            artifact_id=agent_input.artifact.artifact_id,
            context_brief="context",
            evidence_items=[
                EvidenceItem(
                    field_name="issue/commit content",
                    excerpt=agent_input.artifact.raw_fields["issue/commit content"][:80],
                )
            ],
            source_refs=list(agent_input.artifact.source_refs),
        )

    def coder(agent_input: CoderAgentInput) -> CoderAgentOutput:
        call_log.append(f"{agent_input.coder_id}:{agent_input.artifact.artifact_id}")
        return CoderAgentOutput(
            artifact_id=agent_input.artifact.artifact_id,
            coder_id=agent_input.coder_id,
            provisional_codes=[
                ProvisionalCode(
                    code_name="Analysis Logic",
                    short_definition="Root cause in analysis logic.",
                    supporting_evidence=agent_input.context_packet.evidence_items,
                    relationship_to_codebook="new_code",
                    proposed_codebook_action="add",
                )
            ],
        )

    def arbitration_agent(agent_input: ArbitrationInput) -> ArbitrationOutput:
        call_log.append(f"arbitration:{agent_input.artifact.artifact_id}")
        return ArbitrationOutput(
            artifact_id=agent_input.artifact.artifact_id,
            agreement_summary="agreement",
            disagreement_summary="none",
            recommended_codes=[agent_input.coder_outputs[0].provisional_codes[0]],
        )

    def validation_agent(agent_input: ValidationInput) -> ValidationOutput:
        call_log.append(f"validation:{agent_input.artifact.artifact_id}")
        return ValidationOutput(
            artifact_id=agent_input.artifact.artifact_id,
            signals=[ValidationSignal(signal="valid", summary="ok")],
            summary="ready",
        )

    def human_review_agent(agent_input: HumanReviewInput) -> HumanReviewOutput:
        call_log.append(f"human:{agent_input.artifact.artifact_id}")
        existing = agent_input.codebook.get_code("code-analysis-logic")
        code = CodeState(
            code_id="code-analysis-logic",
            name="Analysis Logic",
            definition="Human-approved code.",
            representative_artifact_ids=(
                [*existing.representative_artifact_ids, agent_input.artifact.artifact_id]
                if existing is not None
                else [agent_input.artifact.artifact_id]
            ),
        )
        changes = [] if existing is not None else [
            CodebookChangeState(
                change_id=f"chg-{agent_input.artifact.artifact_id}",
                action="add",
                round_index=0,
                summary="Add Analysis Logic.",
                rationale="The first reviewed artifact establishes this new concept.",
                resulting_code_ids=[code.code_id],
                artifact_ids=[agent_input.artifact.artifact_id],
            )
        ]
        return HumanReviewOutput(
            artifact_id=agent_input.artifact.artifact_id,
            decision="accept",
            final_codes=[code],
            rationale="accept recommendation",
            evidence_summary=["grounded evidence"],
            codebook_changes=changes,
        )

    return CODAOrchestrator(
        context_agent=context_agent,
        coder_agents=[
            ("coder-a", coder),
            ("coder-b", coder),
        ],
        arbitration_agent=arbitration_agent,
        validation_agent=validation_agent,
        human_review_agent=human_review_agent,
    )


class TestFullRunner(unittest.TestCase):
    def test_run_one_artifact_is_reusable_without_advancing_batch(self) -> None:
        adapter = StaticAnalysisNondeterminismAdapter()
        metadata = adapter.load_dataset_metadata()
        artifacts = list(adapter.iter_artifacts())[:2]
        run_state = build_single_batch_run_state(
            metadata,
            artifacts,
            batch_id="batch-runner-0",
        )
        batch = run_state.current_batch()
        assert batch is not None
        call_log: list[str] = []
        orchestrator = _build_test_orchestrator(call_log)

        result = orchestrator.run_one_artifact(
            run_state,
            artifact=artifacts[0],
            batch=batch,
        )

        self.assertEqual(result.artifact_id, artifacts[0].artifact_id)
        self.assertEqual(run_state.current_batch_index, 0)
        self.assertEqual(run_state.status, "awaiting_human_review")
        self.assertEqual(len(run_state.history.coding_records), 1)
        self.assertEqual(
            pending_artifacts_for_batch(batch, run_state),
            [artifacts[1]],
        )
        self.assertEqual(
            call_log,
            [
                f"context:{artifacts[0].artifact_id}",
                f"coder-a:{artifacts[0].artifact_id}",
                f"coder-b:{artifacts[0].artifact_id}",
                f"arbitration:{artifacts[0].artifact_id}",
                f"validation:{artifacts[0].artifact_id}",
                f"human:{artifacts[0].artifact_id}",
                f"validation:{artifacts[0].artifact_id}",
            ],
        )

    def test_resume_skips_reviewed_artifacts_and_completes_run(self) -> None:
        adapter = StaticAnalysisNondeterminismAdapter()
        metadata = adapter.load_dataset_metadata()
        artifacts = list(adapter.iter_artifacts())[:2]
        initial_run_state = build_single_batch_run_state(
            metadata,
            artifacts,
            batch_id="batch-runner-1",
        )
        batch = initial_run_state.current_batch()
        assert batch is not None

        call_log: list[str] = []
        orchestrator = _build_test_orchestrator(call_log)
        first_result = orchestrator.run_one_artifact(
            initial_run_state,
            artifact=artifacts[0],
            batch=batch,
        )
        self.assertEqual(first_result.artifact_id, artifacts[0].artifact_id)

        with tempfile.TemporaryDirectory() as temp_dir:
            paths = FullRunPaths.from_run_dir(temp_dir)
            save_run_state_checkpoint(initial_run_state, paths.checkpoint_path)
            restored_run_state = load_run_state_checkpoint(
                paths.checkpoint_path,
                dataset_metadata=metadata,
                coding_batches=initial_run_state.coding_batches,
            )

            outputs: list[str] = []
            run_resumable_full_coding(
                orchestrator=orchestrator,
                run_state=restored_run_state,
                paths=paths,
                output_func=outputs.append,
            )

            reviews = [
                json.loads(line)
                for line in Path(paths.review_log_path).read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
            artifact_runs = [
                json.loads(line)
                for line in Path(paths.artifact_log_path).read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
            self.assertFalse(Path(paths.final_codebook_path).exists())
            final_codebook = {"version": restored_run_state.codebook.version}
            self.assertTrue(restored_run_state.metadata["final_validation_audits"])

        self.assertEqual(
            [
                entry
                for entry in call_log
                if entry.endswith(f":{artifacts[1].artifact_id}")
            ],
            [
                f"context:{artifacts[1].artifact_id}",
                f"coder-a:{artifacts[1].artifact_id}",
                f"coder-b:{artifacts[1].artifact_id}",
                f"arbitration:{artifacts[1].artifact_id}",
                f"validation:{artifacts[1].artifact_id}",
                f"human:{artifacts[1].artifact_id}",
                f"validation:{artifacts[1].artifact_id}",
            ],
        )
        self.assertFalse(
            any(entry == f"context:{artifacts[0].artifact_id}" for entry in call_log[6:])
        )
        self.assertEqual(len(reviews), 1)
        self.assertEqual(reviews[0]["artifact_id"], artifacts[1].artifact_id)
        self.assertEqual(len(artifact_runs), 1)
        self.assertEqual(artifact_runs[0]["artifact_id"], artifacts[1].artifact_id)
        self.assertEqual(final_codebook["version"], 1)
        self.assertEqual(restored_run_state.status, "awaiting_final_review")
        self.assertEqual(restored_run_state.current_batch_index, 1)
        self.assertEqual(len(restored_run_state.history.coding_records), 2)
        self.assertTrue(any(line.startswith("[done]") for line in outputs))
        self.assertTrue(any(line.startswith("[codebook] version=1") for line in outputs))
        self.assertTrue(any("Analysis Logic" in line for line in outputs))

    def test_runner_pauses_between_artifacts_and_shows_current_codebook(self) -> None:
        adapter = StaticAnalysisNondeterminismAdapter()
        metadata = adapter.load_dataset_metadata()
        artifacts = list(adapter.iter_artifacts())[:2]
        run_state = build_single_batch_run_state(
            metadata,
            artifacts,
            batch_id="batch-runner-2",
        )
        call_log: list[str] = []
        orchestrator = _build_test_orchestrator(call_log)

        with tempfile.TemporaryDirectory() as temp_dir:
            paths = FullRunPaths.from_run_dir(temp_dir)
            outputs: list[str] = []
            pause_calls: list[str] = []
            run_resumable_full_coding(
                orchestrator=orchestrator,
                run_state=run_state,
                paths=paths,
                output_func=outputs.append,
                pause_func=lambda: pause_calls.append("pause"),
            )

        self.assertEqual(pause_calls, ["pause"])
        self.assertTrue(any(line == "[pause] press Enter to continue to the next artifact..." for line in outputs))
        self.assertTrue(any(line.startswith("[saved] artifact=" + artifacts[0].artifact_id) for line in outputs))
        self.assertTrue(any(line.startswith("[codebook] version=") for line in outputs))
        first_pause_index = outputs.index("[pause] press Enter to continue to the next artifact...")
        saved_index = next(
            index
            for index, line in enumerate(outputs)
            if line.startswith("[saved] artifact=" + artifacts[0].artifact_id)
        )
        next_artifact_index = next(
            index
            for index, line in enumerate(outputs)
            if line == f"[artifact] {artifacts[1].artifact_id}"
        )
        self.assertGreater(first_pause_index, saved_index)
        self.assertLess(first_pause_index, next_artifact_index)


if __name__ == "__main__":
    unittest.main()
