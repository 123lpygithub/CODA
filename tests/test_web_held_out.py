from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from adapters.static_analysis import StaticAnalysisNondeterminismAdapter
from coda.full_runner import persist_final_codebook
from coda.persistence import save_run_state_checkpoint
from coda.state import CodingRecordState
from coda.web.api import create_app
from coda.web.runtime import CodaWebService, WebWorkflowError
from tests.test_web_runtime import _build_test_bootstrap, _build_test_orchestrator
from fastapi.testclient import TestClient


class TestWebHeldOutRuns(unittest.TestCase):
    def _service(self, root: Path) -> CodaWebService:
        return CodaWebService(
            runs_root=root,
            adapter_factories={
                "static_analysis_nondeterminism": StaticAnalysisNondeterminismAdapter
            },
            orchestrator_factory=lambda: _build_test_orchestrator([]),
            bootstrap_factory=_build_test_bootstrap,
        )

    def test_run_reserves_and_restores_held_out_without_coding_it(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            runs_root = Path(temporary) / "runs"
            service = self._service(runs_root)
            summary = service.create_run(
                dataset_name="static_analysis_nondeterminism",
                artifact_limit=20,
                review_mode="full",
                held_out_enabled=True,
                held_out_size=4,
            )
            self.assertEqual(summary["coding_pool_artifacts"], 16)
            self.assertEqual(summary["held_out_artifacts"], 4)
            self.assertEqual(summary["total_selected_artifacts"], 20)

            run_dir = Path(summary["run_dir"])
            checkpoint = json.loads((run_dir / "checkpoint.json").read_text(encoding="utf-8"))
            manifest = json.loads((run_dir / "run_manifest.json").read_text(encoding="utf-8"))
            split = json.loads((run_dir / "split_manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(len(checkpoint["coding_batches"][0]["artifact_ids"]), 16)
            self.assertEqual(len(checkpoint["held_out_batches"][0]["artifact_ids"]), 4)
            self.assertEqual(manifest["data"]["selected_artifact_count"], 20)
            self.assertEqual(manifest["data"]["coding_pool_artifact_count"], 16)
            self.assertEqual(manifest["data"]["held_out_artifact_count"], 4)
            self.assertEqual(
                {row["split_name"] for row in split["assignments"]},
                {"coding_pool", "held_out_pool"},
            )

            restored = self._service(runs_root)._load_run_state(summary["run_id"])
            coding_ids = {
                artifact.artifact_id
                for batch in restored.coding_batches
                for artifact in batch.artifacts
            }
            held_out_ids = {
                artifact.artifact_id
                for batch in restored.held_out_batches
                for artifact in batch.artifacts
            }
            self.assertEqual(len(coding_ids), 16)
            self.assertEqual(len(held_out_ids), 4)
            self.assertFalse(coding_ids & held_out_ids)
            self.assertEqual(
                restored.metadata["bootstrap"]["population_size"],
                len(coding_ids),
            )

    def test_held_out_is_off_by_default(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            summary = self._service(Path(temporary) / "runs").create_run(
                dataset_name="static_analysis_nondeterminism",
                artifact_limit=4,
                review_mode="full",
            )
            self.assertEqual(summary["coding_pool_artifacts"], 4)
            self.assertEqual(summary["held_out_artifacts"], 0)

    def test_selective_audit_is_sampled_over_unflagged_decision_windows(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            service = self._service(Path(temporary) / "runs")
            summary = service.create_run(
                dataset_name="static_analysis_nondeterminism",
                artifact_limit=20,
                review_mode="selective",
                iterative_batch_size=10,
            )
            service.initialize_run(summary["run_id"])
            state = service._load_run_state(summary["run_id"])
            manifest = state.metadata["review_sampling_manifest"]
            self.assertEqual(manifest["population_artifact_ids"], [
                artifact.artifact_id
                for batch in state.coding_batches
                for artifact in batch.artifacts
            ])
            self.assertEqual(manifest["sampled_artifact_ids"], [])
            self.assertEqual(manifest["sampling_window_size"], 10)
            self.assertEqual(manifest["streams"]["current"]["eligible_decision_count"], 0)

            artifact_ids = manifest["population_artifact_ids"]
            sampled = [
                service._orchestrator_for(summary["run_id"])._selective_audit_membership(
                    state,
                    artifact_id=artifact_id,
                    stream="current",
                )
                for artifact_id in artifact_ids[:10]
            ]
            self.assertEqual(sum(sampled), 1)
            self.assertEqual(
                state.metadata["review_sampling_manifest"]["streams"]["current"][
                    "eligible_decision_count"
                ],
                10,
            )

    def test_selective_sampling_manifest_is_frozen_after_initial_creation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            service = self._service(Path(temporary) / "runs")
            summary = service.create_run(
                dataset_name="static_analysis_nondeterminism",
                artifact_limit=20,
                review_mode="selective",
            )
            service.initialize_run(summary["run_id"])
            state = service._load_run_state(summary["run_id"])
            artifacts = [
                artifact
                for batch in state.coding_batches
                for artifact in batch.artifacts
            ]
            with self.assertRaisesRegex(WebWorkflowError, "population changed"):
                CodaWebService._set_iterative_micro_batches(
                    state,
                    artifacts[:-1],
                    group_ids={artifact.artifact_id: artifact.artifact_id for artifact in artifacts[:-1]},
                )

    def test_http_export_requires_a_frozen_run_and_keeps_packet_separate(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            runs_root = Path(temporary) / "runs"
            service = self._service(runs_root)
            summary = service.create_run(
                dataset_name="static_analysis_nondeterminism",
                artifact_limit=3,
                review_mode="full",
                held_out_enabled=True,
                held_out_size=1,
            )
            client = TestClient(create_app(service))
            run_id = summary["run_id"]
            run_dir = Path(summary["run_dir"])
            state = service._load_run_state(run_id)
            initial_record_count = len(state.history.coding_records)

            pending = client.get(f"/api/runs/{run_id}/held-out-materials")
            self.assertEqual(pending.status_code, 409)
            self.assertFalse((run_dir / "held_out_materials.json").exists())

            for batch in state.coding_batches:
                for artifact in batch.artifacts:
                    state.history.coding_records.append(
                        CodingRecordState(
                            record_id=f"test-{artifact.artifact_id}",
                            artifact_id=artifact.artifact_id,
                            dataset_name=state.dataset_metadata.dataset_name,
                            batch_index=batch.batch_index,
                            codebook_version=state.codebook.version,
                            decision="accept",
                            rationale="Test fixture completion record.",
                        )
                    )
            from coda.state import StageReviewState
            state.history.append_stage_review(StageReviewState(
                review_id="fixture-final", kind="final", decision="accept",
                rationale="Fixture reviewed.",
                codebook_version_before=state.codebook.version,
                codebook_version_after=state.codebook.version,
            ))
            service._run_final_validation(state, service._record_stabilization_check(state, final=True))
            state.status = "completed"
            paths = service._paths_for(run_id)
            persist_final_codebook(state, paths.final_codebook_path)
            save_run_state_checkpoint(state, paths.checkpoint_path)

            response = client.get(f"/api/runs/{run_id}/held-out-materials")
            self.assertEqual(response.status_code, 200)
            packet = response.json()
            self.assertEqual(packet["format"], "coda-held-out-application-materials")
            self.assertFalse(packet["reference_data_included"])
            self.assertEqual(len(packet["artifacts"]), 1)
            self.assertTrue((run_dir / "held_out_materials.json").exists())
            self.assertEqual(len(state.history.coding_records), initial_record_count + 2)


if __name__ == "__main__":
    unittest.main()
