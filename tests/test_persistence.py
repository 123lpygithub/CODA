from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from adapters.static_analysis import StaticAnalysisNondeterminismAdapter
from coda.persistence import (
    load_run_state_checkpoint,
    save_run_state_checkpoint,
    serialize_run_state_checkpoint,
)
from coda.state import (
    ArtifactBatchState,
    CodeState,
    CodebookChangeState,
    CodingRecordState,
    RunState,
)


class TestPersistence(unittest.TestCase):
    def test_checkpoint_round_trip_restores_run_state_payload(self) -> None:
        adapter = StaticAnalysisNondeterminismAdapter()
        metadata = adapter.load_dataset_metadata()
        artifacts = list(adapter.iter_artifacts())[:2]
        batch = ArtifactBatchState(
            batch_id="batch-persist-1",
            dataset_name=metadata.dataset_name,
            batch_index=0,
            split_name="coding_pool",
            artifacts=artifacts,
        )
        run_state = RunState.initialize(metadata, coding_batches=[batch])
        code = CodeState(
            code_id="code-analysis-logic",
            name="Analysis Logic",
            definition="Human-approved code.",
            representative_artifact_ids=[artifacts[0].artifact_id],
        )
        change = CodebookChangeState(
            change_id="chg-1",
            action="add",
            round_index=0,
            summary="Add Analysis Logic.",
            resulting_code_ids=[code.code_id],
            artifact_ids=[artifacts[0].artifact_id],
        )
        run_state.codebook = run_state.codebook.next_version(
            codes=[code],
            new_revision=change,
        )
        run_state.history.append_revision(change)
        run_state.history.append_record(
            CodingRecordState(
                record_id="record-1",
                artifact_id=artifacts[0].artifact_id,
                dataset_name=metadata.dataset_name,
                batch_index=0,
                codebook_version=1,
                decision="accept",
                final_code_ids=[code.code_id],
                final_code_names=[code.name],
                rationale="accept recommendation",
                evidence_summary=["grounded evidence"],
            )
        )

        payload = serialize_run_state_checkpoint(run_state)
        self.assertEqual(payload["dataset_name"], metadata.dataset_name)
        self.assertEqual(payload["codebook"]["version"], 1)
        self.assertEqual(payload["coding_batches"][0]["artifact_ids"], batch.artifact_ids)
        self.assertEqual(payload["history"]["coding_records"][0]["artifact_id"], artifacts[0].artifact_id)

    def test_checkpoint_file_round_trip(self) -> None:
        adapter = StaticAnalysisNondeterminismAdapter()
        metadata = adapter.load_dataset_metadata()
        artifacts = list(adapter.iter_artifacts())[:2]
        batch = ArtifactBatchState(
            batch_id="batch-persist-2",
            dataset_name=metadata.dataset_name,
            batch_index=0,
            split_name="coding_pool",
            artifacts=artifacts,
        )
        run_state = RunState.initialize(metadata, coding_batches=[batch])
        code = CodeState(
            code_id="code-analysis-logic",
            name="Analysis Logic",
            definition="Human-approved code.",
            representative_artifact_ids=[artifacts[0].artifact_id],
        )
        change = CodebookChangeState(
            change_id="chg-2",
            action="add",
            round_index=0,
            summary="Add Analysis Logic.",
            resulting_code_ids=[code.code_id],
            artifact_ids=[artifacts[0].artifact_id],
        )
        run_state.codebook = run_state.codebook.next_version(
            codes=[code],
            new_revision=change,
        )
        run_state.history.append_revision(change)
        run_state.history.append_record(
            CodingRecordState(
                record_id="record-2",
                artifact_id=artifacts[0].artifact_id,
                dataset_name=metadata.dataset_name,
                batch_index=0,
                codebook_version=1,
                decision="accept",
                final_code_ids=[code.code_id],
                final_code_names=[code.name],
                rationale="accept recommendation",
                evidence_summary=["grounded evidence"],
            )
        )
        run_state.history.notes.append("history note")
        run_state.current_batch_index = 0
        run_state.status = "in_progress"

        with tempfile.TemporaryDirectory() as temp_dir:
            checkpoint_path = Path(temp_dir) / "checkpoint.json"
            save_run_state_checkpoint(run_state, checkpoint_path)
            restored = load_run_state_checkpoint(
                checkpoint_path,
                dataset_metadata=metadata,
                coding_batches=[batch],
            )
            file_payload = json.loads(checkpoint_path.read_text(encoding="utf-8"))

        self.assertEqual(file_payload["format"], "coda-run-checkpoint")
        self.assertEqual(restored.run_id, run_state.run_id)
        self.assertEqual(restored.dataset_metadata.dataset_name, metadata.dataset_name)
        self.assertEqual(restored.current_batch_index, run_state.current_batch_index)
        self.assertEqual(restored.status, "in_progress")
        self.assertEqual(restored.history.notes, ["history note"])
        self.assertEqual(len(restored.history.coding_records), 1)
        self.assertEqual(restored.history.coding_records[0].artifact_id, artifacts[0].artifact_id)
        self.assertEqual(restored.codebook.version, 1)
        self.assertEqual(restored.codebook.codes[0].code_id, code.code_id)


if __name__ == "__main__":
    unittest.main()
