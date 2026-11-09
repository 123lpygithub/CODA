from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from adapters.static_analysis import StaticAnalysisNondeterminismAdapter
from coda.bootstrap import BootstrapConfig
from coda.contracts import (
    ComparisonOutput,
    ContextPacket,
    EvidencePacket,
    ValidationInput,
)
from coda.full_runner import build_single_batch_run_state
from coda.manifest import build_run_manifest, write_run_manifest


class TestManifestAndComparisonCompatibility(unittest.TestCase):
    def test_legacy_arbitration_field_populates_canonical_comparison_field(self) -> None:
        adapter = StaticAnalysisNondeterminismAdapter()
        artifact = next(iter(adapter.iter_artifacts()))
        run_state = build_single_batch_run_state(
            adapter.load_dataset_metadata(), [artifact], batch_id="compatibility-batch"
        )
        comparison = ComparisonOutput(
            artifact_id=artifact.artifact_id,
            agreement_summary="Agreement.",
            disagreement_summary="None.",
        )
        packet = EvidencePacket(
            artifact_id=artifact.artifact_id,
            original_artifact=artifact,
            research_question=run_state.research_question,
            context_packet=ContextPacket(
                artifact_id=artifact.artifact_id,
                context_brief="Context.",
            ),
            coder_outputs=[],
            arbitration_output=comparison,
        )
        validation_input = ValidationInput(
            artifact=artifact,
            research_question=run_state.research_question,
            context_packet=packet.context_packet,
            coder_outputs=[],
            arbitration_output=comparison,
            codebook=run_state.codebook,
            history=run_state.history,
        )

        self.assertIs(packet.comparison_output, comparison)
        self.assertIs(validation_input.comparison_output, comparison)

    def test_manifest_records_environment_protocol_and_data_hashes(self) -> None:
        adapter = StaticAnalysisNondeterminismAdapter()
        artifacts = list(adapter.iter_artifacts())[:2]
        run_state = build_single_batch_run_state(
            adapter.load_dataset_metadata(), artifacts, batch_id="manifest-batch"
        )

        manifest = build_run_manifest(
            run_state,
            artifacts,
            project_root=Path(__file__).resolve().parents[1],
            bootstrap_config=BootstrapConfig(
                fraction=0.5,
                minimum_size=1,
                maximum_size=1,
            ),
            model_configurations={"comparison": {"model": "test-model"}},
        )

        self.assertEqual(manifest["format"], "coda-run-manifest")
        self.assertEqual(manifest["data"]["selected_artifact_count"], 2)
        self.assertTrue(manifest["data"]["artifact_selection_sha256"])
        self.assertTrue(manifest["data"]["source_checksums"])
        self.assertIn("git", manifest["environment"])
        self.assertEqual(manifest["models"]["comparison"]["model"], "test-model")
        with tempfile.TemporaryDirectory() as temporary:
            destination = write_run_manifest(
                Path(temporary) / "run_manifest.json",
                manifest,
            )
            self.assertTrue(destination.exists())


if __name__ == "__main__":
    unittest.main()
