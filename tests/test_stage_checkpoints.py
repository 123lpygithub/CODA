from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from adapters.static_analysis import StaticAnalysisNondeterminismAdapter
from coda.contracts import (
    CoderAgentOutput,
    ComparisonOutput,
    ContextPacket,
    EvidenceItem,
    HumanReviewOutput,
    ProvisionalCode,
    ValidationOutput,
    ValidationSignal,
)
from coda.full_runner import build_single_batch_run_state
from coda.orchestrator import CODAOrchestrator
from coda.stage_checkpoints import StageCheckpointStore


class TestStageCheckpoints(unittest.TestCase):
    def test_legacy_validation_signal_defaults_issue_scope(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "legacy-validation.json"
            store = StageCheckpointStore(path, cache_key="legacy")
            store.put(
                "validation",
                ValidationOutput(
                    artifact_id="artifact-1",
                    signals=[
                        ValidationSignal(
                            signal="category_overlap",
                            issue_scope="assignment",
                            summary="Overlapping assignment.",
                        )
                    ],
                ),
            )
            payload = json.loads(path.read_text(encoding="utf-8"))
            del payload["stages"]["validation"]["signals"][0]["issue_scope"]
            path.write_text(json.dumps(payload), encoding="utf-8")

            restored = store.get("validation", ValidationOutput)

        self.assertIsNotNone(restored)
        self.assertEqual(restored.signals[0].issue_scope, "none")

    def test_failed_peer_coder_resumes_without_repeating_successful_coder(self) -> None:
        adapter = StaticAnalysisNondeterminismAdapter()
        artifact = next(iter(adapter.iter_artifacts()))
        run_state = build_single_batch_run_state(
            adapter.load_dataset_metadata(), [artifact], batch_id="coder-checkpoint-batch"
        )
        calls = {"context": 0, "coder-a": 0, "coder-b": 0}

        def context_agent(agent_input):
            calls["context"] += 1
            return ContextPacket(
                artifact_id=artifact.artifact_id,
                context_brief="Grounded context.",
                evidence_items=[
                    EvidenceItem(field_name="content", excerpt=artifact.content[:40])
                ],
            )

        def coder(agent_input):
            calls[agent_input.coder_id] += 1
            if agent_input.coder_id == "coder-b" and calls["coder-b"] == 1:
                raise RuntimeError("temporary coder-b failure")
            return CoderAgentOutput(
                artifact_id=artifact.artifact_id,
                coder_id=agent_input.coder_id,
                provisional_codes=[
                    ProvisionalCode(
                        code_name=f"Observed failure {agent_input.coder_id}",
                        short_definition="A visible failure.",
                        supporting_evidence=agent_input.context_packet.evidence_items,
                    )
                ],
                confidence_level="high",
            )

        def comparison(agent_input):
            return ComparisonOutput(
                artifact_id=artifact.artifact_id,
                agreement_summary="The readings agree.",
                disagreement_summary="None.",
                recommended_codes=agent_input.coder_outputs[0].provisional_codes,
            )

        def validation(agent_input):
            return ValidationOutput(
                artifact_id=artifact.artifact_id,
                signals=[ValidationSignal(signal="valid", summary="Valid.")],
                summary="Ready.",
                confidence_level="high",
            )

        orchestrator = CODAOrchestrator(
            context_agent=context_agent,
            coder_agents=[("coder-a", coder), ("coder-b", coder)],
            comparison_agent=comparison,
            validation_agent=validation,
            human_review_agent=lambda _: HumanReviewOutput(
                artifact_id=artifact.artifact_id,
                decision="reject",
                rationale="Not used.",
            ),
        )
        with tempfile.TemporaryDirectory() as temporary:
            store = StageCheckpointStore(
                Path(temporary) / "artifact.json",
                cache_key=orchestrator.stage_cache_key(run_state, artifact),
            )

            with self.assertRaisesRegex(RuntimeError, "temporary coder-b failure"):
                orchestrator.prepare_one_artifact(
                    run_state,
                    artifact=artifact,
                    stage_checkpoint_store=store,
                )

            prepared = orchestrator.prepare_one_artifact(
                run_state,
                artifact=artifact,
                stage_checkpoint_store=store,
            )

        self.assertEqual(len(prepared.coder_outputs), 2)
        self.assertEqual(calls, {"context": 1, "coder-a": 1, "coder-b": 2})

    def test_failed_late_stage_resumes_without_repeating_completed_agents(self) -> None:
        adapter = StaticAnalysisNondeterminismAdapter()
        artifact = next(iter(adapter.iter_artifacts()))
        run_state = build_single_batch_run_state(
            adapter.load_dataset_metadata(), [artifact], batch_id="checkpoint-batch"
        )
        calls = {"context": 0, "coder": 0, "comparison": 0, "validation": 0}

        def context_agent(agent_input):
            calls["context"] += 1
            return ContextPacket(
                artifact_id=artifact.artifact_id,
                context_brief="Grounded context.",
                evidence_items=[
                    EvidenceItem(
                        field_name="content",
                        excerpt=artifact.content[:40],
                    )
                ],
            )

        def coder(agent_input):
            calls["coder"] += 1
            return CoderAgentOutput(
                artifact_id=artifact.artifact_id,
                coder_id=agent_input.coder_id,
                provisional_codes=[
                    ProvisionalCode(
                        code_name="Observed failure",
                        short_definition="A visible failure.",
                        supporting_evidence=agent_input.context_packet.evidence_items,
                    )
                ],
                confidence_level="high",
            )

        def comparison(agent_input):
            calls["comparison"] += 1
            return ComparisonOutput(
                artifact_id=artifact.artifact_id,
                agreement_summary="The readings agree.",
                disagreement_summary="None.",
                recommended_codes=agent_input.coder_outputs[0].provisional_codes,
            )

        def validation(agent_input):
            calls["validation"] += 1
            if calls["validation"] == 1:
                raise RuntimeError("temporary validation failure")
            return ValidationOutput(
                artifact_id=artifact.artifact_id,
                signals=[ValidationSignal(signal="valid", summary="Valid.")],
                summary="Ready.",
                confidence_level="high",
            )

        orchestrator = CODAOrchestrator(
            context_agent=context_agent,
            coder_agents=[("coder-a", coder), ("coder-b", coder)],
            comparison_agent=comparison,
            validation_agent=validation,
            human_review_agent=lambda _: HumanReviewOutput(
                artifact_id=artifact.artifact_id,
                decision="reject",
                rationale="Not used.",
            ),
        )
        with tempfile.TemporaryDirectory() as temporary:
            key = orchestrator.stage_cache_key(run_state, artifact)
            store = StageCheckpointStore(
                Path(temporary) / "artifact.json",
                cache_key=key,
            )

            with self.assertRaisesRegex(RuntimeError, "temporary validation failure"):
                orchestrator.prepare_one_artifact(
                    run_state,
                    artifact=artifact,
                    stage_checkpoint_store=store,
                )

            prepared = orchestrator.prepare_one_artifact(
                run_state,
                artifact=artifact,
                stage_checkpoint_store=store,
            )

        self.assertEqual(prepared.validation_output.summary, "Ready.")
        self.assertEqual(calls, {
            "context": 1,
            "coder": 2,
            "comparison": 1,
            "validation": 2,
        })


if __name__ == "__main__":
    unittest.main()
