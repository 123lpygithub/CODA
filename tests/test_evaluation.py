from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from adapters.static_analysis import StaticAnalysisNondeterminismAdapter
from coda.evaluation import (
    EvaluationError,
    export_held_out_materials,
    export_rq1_materials,
    gwet_ac2,
    gwet_ac2_bootstrap,
    summarize_rq1_scores,
    summarize_rq2_metrics,
    summarize_rq2_runs,
    summarize_held_out_packet_scores,
    _lifecycle_metrics,
)
from coda.evaluator import CalibrationConfig, calibrate_evaluators


class TestEvaluation(unittest.TestCase):
    def test_formal_agreement_uses_full_rubric_even_when_one_rating_is_unobserved(self) -> None:
        rows = [
            {"run_id": "r", "evaluator_id": evaluator_id, "unit": "assignment",
             "dimension": "evidence_support", "artifact_id": f"a-{index}",
             "code_id": "c", "score": score}
            for evaluator_id, scores in (("left", [0, 0, 1]), ("right", [0, 1, 1]))
            for index, score in enumerate(scores)
        ]
        summary = summarize_rq1_scores(rows, agreement_replicates=100)
        estimate = summary["agreement"]["r:evidence_support"]["estimate"]
        self.assertAlmostEqual(estimate, gwet_ac2([0, 0, 1], [0, 1, 1], categories=[0, 1, 2]))
        self.assertNotAlmostEqual(estimate, gwet_ac2([0, 0, 1], [0, 1, 1], categories=[0, 1]))

    def test_support_reports_case_and_assignment_weighting_without_filling_missing_scores(self) -> None:
        rows = [
            {"run_id": "r", "evaluator_id": "e", "unit": "assignment",
             "dimension": "evidence_support", "artifact_id": artifact_id,
             "code_id": f"c-{index}", "score": score, "status": "assessable"}
            for index, (artifact_id, score) in enumerate([
                ("a", 2), ("a", 0), ("a", 0), ("b", 2),
            ])
        ]
        rows.append({"run_id": "r", "evaluator_id": "e", "unit": "assignment",
                     "dimension": "evidence_support", "artifact_id": "c", "code_id": "missing",
                     "status": "unassessable"})
        rows.append({"run_id": "other", "evaluator_id": "e", "unit": "assignment",
                     "dimension": "evidence_support", "artifact_id": "a", "code_id": "other",
                     "status": "unassessable"})
        summary = summarize_rq1_scores(rows, agreement_replicates=10)
        support = summary["by_run_evaluator"]["r"]["e"]["evidence_support"]
        self.assertEqual(support["fully_supported_rate"], 0.5)
        self.assertAlmostEqual(support["case_mean_fully_supported_rate"], 2 / 3)
        self.assertEqual(support["unassessable_count"], 1)
        self.assertEqual(support["unassessable_rate"], 0.2)
        self.assertEqual(support["assessable_case_judgment_count"], 2)
        missing = summary["by_run_evaluator"]["other"]["e"]["evidence_support"]
        self.assertIsNone(missing["fully_supported_rate"])
        self.assertIsNone(missing["case_mean_fully_supported_rate"])

    def test_calibration_pairs_different_codebooks_by_run_id(self) -> None:
        from coda.evaluator import _paired_scores
        rows = [
            {"run_id": run_id, "evaluator_id": evaluator_id, "unit": "codebook", "dimension": "clarity", "score": score}
            for evaluator_id, values in (("human", [1, 3, 5]), ("model", [2, 3, 4]))
            for run_id, score in zip(("a", "b", "c"), values)
        ]
        self.assertEqual(_paired_scores(rows, "human", "model", "clarity"), ([1, 3, 5], [2, 3, 4]))

    def test_formal_export_rejects_pending_reassessments_and_stale_snapshot(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self._write_run(root)
            checkpoint = json.loads((root / "checkpoint.json").read_text())
            checkpoint["history"]["retrospective_tasks"] = [{"status": "pending"}]
            (root / "checkpoint.json").write_text(json.dumps(checkpoint))
            with self.assertRaisesRegex(EvaluationError, "reassessments"):
                export_rq1_materials(root, StaticAnalysisNondeterminismAdapter())
            checkpoint["history"]["retrospective_tasks"] = []
            checkpoint["codebook"]["version"] = 2
            (root / "checkpoint.json").write_text(json.dumps(checkpoint))
            with self.assertRaisesRegex(EvaluationError, "frozen codebook"):
                export_rq1_materials(root, StaticAnalysisNondeterminismAdapter())

    def test_explicit_foreground_timer_pairs_active_segments(self) -> None:
        metrics = _lifecycle_metrics([
            {"event": "review_timer_resumed", "timestamp_utc": "2026-01-01T00:00:00+00:00", "timer_scope": "artifact", "artifact_id": "a"},
            {"event": "review_timer_paused", "timestamp_utc": "2026-01-01T00:00:05+00:00", "timer_scope": "artifact", "artifact_id": "a"},
            {"event": "review_timer_resumed", "timestamp_utc": "2026-01-01T00:01:00+00:00", "timer_scope": "artifact", "artifact_id": "a"},
            {"event": "review_timer_paused", "timestamp_utc": "2026-01-01T00:01:07+00:00", "timer_scope": "artifact", "artifact_id": "a"},
        ])
        self.assertEqual(metrics["explicit_foreground_timer_seconds"], 12.0)
        self.assertEqual(metrics["explicit_foreground_timer_event_count"], 4)

    def test_evaluator_calibration_selects_candidate_without_touching_coding(self) -> None:
        rows = []
        ratings = {
            "human-a": [1, 2, 3, 4, 5],
            "human-b": [1, 2, 3, 4, 5],
            "candidate": [1, 2, 3, 4, 5],
        }
        for evaluator_id, values in ratings.items():
            for dimension in ("clarity", "category_boundaries", "meaningful_coverage"):
                for index, score in enumerate(values):
                    rows.append(
                        {
                            "run_id": f"pilot-run-{index}",
                            "evaluator_id": evaluator_id,
                            "evaluator_kind": "llm" if evaluator_id == "candidate" else "human",
                            "candidate_model": "model-a" if evaluator_id == "candidate" else None,
                            "phase": "pilot",
                            "dimension": dimension,
                            "unit": "codebook",
                            "score": score,
                            "status": "assessable",
                            "rationale": "The rubric supports this rating.",
                        }
                    )
            evidence_scores = [0, 1, 2, 2, 1]
            for index, score in enumerate(evidence_scores):
                rows.append(
                    {
                        "run_id": "pilot-run",
                        "evaluator_id": evaluator_id,
                        "evaluator_kind": "llm" if evaluator_id == "candidate" else "human",
                        "candidate_model": "model-a" if evaluator_id == "candidate" else None,
                        "phase": "pilot",
                        "dimension": "evidence_support",
                        "unit": "assignment",
                        "artifact_id": f"artifact-{index}",
                        "code_id": "code-a",
                        "score": score,
                        "status": "assessable",
                        "rationale": "The rubric supports this rating.",
                    }
                )
        result = calibrate_evaluators(
            rows,
            candidate_models=["model-a"],
            human_evaluator_ids=["human-a", "human-b"],
            config=CalibrationConfig(bootstrap_replicates=100, bootstrap_seed=7),
        )
        self.assertEqual(result["selected_candidate_model"], "model-a")
        self.assertTrue(result["workflow_isolation"]["evaluator_output_does_not_update_codebook"])

    def test_evaluator_calibration_rejects_partial_human_overlap(self) -> None:
        rows = []
        for evaluator_id, evaluator_kind in (
            ("human-a", "human"),
            ("human-b", "human"),
            ("candidate", "llm"),
        ):
            for index in range(4):
                for dimension in (
                    "clarity",
                    "category_boundaries",
                    "meaningful_coverage",
                    "evidence_support",
                ):
                    row = {
                        "run_id": f"pilot-run-{index}",
                        "evaluator_id": evaluator_id,
                        "evaluator_kind": evaluator_kind,
                        "candidate_model": "model-partial" if evaluator_kind == "llm" else None,
                        "phase": "pilot",
                        "dimension": dimension,
                        "unit": "codebook" if dimension != "evidence_support" else "assignment",
                        "artifact_id": f"artifact-{index}" if dimension == "evidence_support" else None,
                        "code_id": "code-a" if dimension == "evidence_support" else None,
                        "score": 4 if dimension != "evidence_support" else 2,
                        "status": "assessable",
                        "rationale": "The rubric supports this rating.",
                    }
                    rows.append(row)
        # Remove one candidate dimension entirely. The candidate must not pass
        # by averaging the one remaining human comparison.
        rows = [
            row
            for row in rows
            if not (
                row["evaluator_id"] == "candidate"
                and row["dimension"] == "meaningful_coverage"
            )
        ]
        result = calibrate_evaluators(
            rows,
            candidate_models=["model-partial"],
            human_evaluator_ids=["human-a", "human-b"],
            config=CalibrationConfig(bootstrap_replicates=100, bootstrap_seed=9),
        )
        report = result["candidates"][0]
        self.assertFalse(report["passes"])
        self.assertFalse(
            report["dimensions"]["meaningful_coverage"]["complete_human_comparisons"]
        )
    def _write_run(self, root: Path) -> None:
        checkpoint = {
            "run_id": "run-test",
            "dataset_name": "static_analysis_nondeterminism",
            "status": "completed",
            "research_question": {"question_text": "What patterns occur?"},
            "analysis_protocol": {},
            "review_policy": {"setting": "selective"},
            "codebook": {"dataset_name": "static_analysis_nondeterminism", "version": 1, "codes": []},
            "coding_batches": [{"artifact_ids": ["1", "2"]}],
            "metadata": {"selected_artifact_ids": ["1", "2"], "bootstrap": {"population_size": 2}},
            "history": {
                "coding_records": [
                    {
                        "record_id": "r1",
                        "artifact_id": "1",
                        "metadata": {"human_reviewed": True, "duration_seconds": 4},
                    },
                    {
                        "record_id": "r2",
                        "artifact_id": "2",
                        "metadata": {"human_reviewed": False},
                    },
                ],
                "stage_reviews": [
                    {"kind": "initial", "duration_seconds": 3},
                    {"kind": "final", "duration_seconds": 2},
                ],
                "unresolved_cases": [],
                "retrospective_tasks": [],
                "codebook_revisions": [],
            },
        }
        from coda.completion import decision_fingerprint
        checkpoint["history"]["stage_reviews"][-1].update({
            "decision": "accept", "codebook_version_after": 1,
        })
        checkpoint["metadata"]["final_validation_audits"] = {"fixture": {
            "status": "completed", "codebook_version": 1,
            "decision_fingerprint": decision_fingerprint(checkpoint["codebook"], checkpoint["history"]["coding_records"]),
        }}
        checkpoint["metadata"]["events"] = [
            {"event": "run_created", "timestamp_utc": "2026-01-01T00:00:00+00:00"},
            {"event": "bootstrap_started", "timestamp_utc": "2026-01-01T00:00:01+00:00"},
            {"event": "bootstrap_finished", "timestamp_utc": "2026-01-01T00:00:06+00:00"},
            {"event": "iterative_started", "timestamp_utc": "2026-01-01T00:00:07+00:00"},
            {"event": "artifact_waiting_for_human_review", "timestamp_utc": "2026-01-01T00:00:08+00:00", "artifact_id": "1"},
            {"event": "artifact_review_submitted", "timestamp_utc": "2026-01-01T00:00:18+00:00", "artifact_id": "1"},
            {"event": "artifact_processing_finished", "timestamp_utc": "2026-01-01T00:00:19+00:00", "artifact_id": "1", "human_reviewed": True},
            {"event": "iterative_paused", "timestamp_utc": "2026-01-01T00:00:20+00:00", "status": "awaiting_human_review"},
        ]
        (root / "checkpoint.json").write_text(json.dumps(checkpoint), encoding="utf-8")
        (root / "final_codebook.json").write_text(json.dumps(checkpoint["codebook"]), encoding="utf-8")
        (root / "run_manifest.json").write_text(
            json.dumps({"data": {"artifacts": [{"artifact_id": "1"}, {"artifact_id": "2"}]}}),
            encoding="utf-8",
        )
        (root / "artifact_runs.jsonl").write_text(
            json.dumps({
                "artifact_id": "1",
                "context_packet": {"model_metadata": {"usage": {"prompt_tokens": 2, "completion_tokens": 1, "total_tokens": 3}, "elapsed_seconds": 0.5, "attempt_count": 2, "retry_errors": [{"type": "APITimeoutError", "message": "timeout"}], "model": "test"}},
            }) + "\n",
            encoding="utf-8",
        )

    def test_exports_reference_blind_rq1_materials(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self._write_run(root)
            result = export_rq1_materials(root, StaticAnalysisNondeterminismAdapter())
            self.assertEqual(result["format"], "coda-rq1-evaluation-materials")
            self.assertFalse(result["reference_data_included"])
            self.assertEqual(len(result["artifacts"]), 2)
            self.assertIn("coding_record", result["artifacts"][0])

    def test_rq1_score_summary_keeps_unassessable_separate(self) -> None:
        result = summarize_rq1_scores([
            {"run_id": "r", "evaluator_id": "h1", "unit": "codebook", "dimension": "clarity", "score": 4},
            {"run_id": "r", "evaluator_id": "h1", "unit": "assignment", "dimension": "evidence_support", "artifact_id": "a", "code_id": "c", "score": 2},
            {"run_id": "r", "evaluator_id": "h1", "unit": "assignment", "dimension": "evidence_support", "artifact_id": "b", "code_id": "c", "status": "unassessable"},
        ])
        self.assertEqual(result["dimensions"]["evidence_support"]["unassessable_count"], 1)
        self.assertEqual(result["dimensions"]["evidence_support"]["fully_supported_rate"], 1.0)

    def test_gwet_ac2_perfect_agreement_is_one(self) -> None:
        self.assertAlmostEqual(gwet_ac2([1, 2, 3, 4, 5], [1, 2, 3, 4, 5], categories=[1, 2, 3, 4, 5]), 1.0)
        self.assertEqual(gwet_ac2([2, 2], [2, 2]), 1.0)

    def test_gwet_ac2_bootstrap_is_reproducible_and_has_interval(self) -> None:
        first = gwet_ac2_bootstrap(
            [1, 2, 3, 4, 5, 4],
            [1, 2, 3, 4, 4, 5],
            categories=[1, 2, 3, 4, 5],
            replicates=100,
            seed=17,
        )
        second = gwet_ac2_bootstrap(
            [1, 2, 3, 4, 5, 4],
            [1, 2, 3, 4, 4, 5],
            categories=[1, 2, 3, 4, 5],
            replicates=100,
            seed=17,
        )
        self.assertEqual(first, second)
        self.assertLessEqual(first["lower"], first["estimate"])
        self.assertLessEqual(first["estimate"], first["upper"])
        with self.assertRaises(EvaluationError):
            gwet_ac2_bootstrap([1], [1], categories=[1, 2], replicates=99)

    def test_rq2_counts_human_and_retry_time(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self._write_run(root)
            result = summarize_rq2_metrics(root)
            self.assertEqual(result["human_time"]["total_seconds"], 9.0)
            self.assertEqual(result["llm_usage"]["logical_calls"], 1)
            self.assertEqual(result["llm_usage"]["retry_count"], 1)
            self.assertEqual(result["completion"]["processed_artifacts"], 2)
            self.assertEqual(result["lifecycle_time"]["bootstrap_elapsed_seconds"], 5.0)
            self.assertEqual(result["lifecycle_time"]["iterative_elapsed_seconds"], 13.0)
            self.assertEqual(result["lifecycle_time"]["human_waiting_seconds"], 10.0)
            self.assertEqual(result["lifecycle_time"]["observed_elapsed_seconds"], 20.0)

    def test_rq2_run_summary_groups_by_protocol_and_keeps_raw_runs(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            first = root / "run-a"
            second = root / "run-b"
            first.mkdir()
            second.mkdir()
            self._write_run(first)
            self._write_run(second)
            checkpoint = json.loads((second / "checkpoint.json").read_text(encoding="utf-8"))
            checkpoint["run_id"] = "run-b"
            checkpoint["review_policy"]["setting"] = "full"
            checkpoint["metadata"]["experiment_protocol"] = {
                "variant": "without_retrospective_recoding",
                "retrospective_recoding_enabled": False,
            }
            checkpoint["metadata"]["retrospective_suppression_events"] = [
                {"change_id": "c1", "affected_artifact_ids": ["1", "2"]}
            ]
            (second / "checkpoint.json").write_text(
                json.dumps(checkpoint), encoding="utf-8"
            )
            result = summarize_rq2_runs([first, second])
            self.assertEqual(result["run_count"], 2)
            self.assertEqual(len(result["runs"]), 2)
            self.assertEqual(len(result["groups"]), 2)
            disabled = next(
                group
                for group in result["groups"]
                if group["experiment_variant"] == "without_retrospective_recoding"
            )
            self.assertEqual(disabled["metrics"]["completion.retrospective_recoding_suppressed_events"]["mean"], 1.0)
            self.assertEqual(result["aggregation_protocol"]["inference"], "descriptive_only")

    def test_rq2_fallback_counts_coding_batches_without_bootstrap_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self._write_run(root)
            checkpoint = json.loads((root / "checkpoint.json").read_text(encoding="utf-8"))
            checkpoint["metadata"].pop("bootstrap")
            checkpoint["coding_batches"] = [
                {"batch_id": "batch-0", "artifact_ids": ["1", "2", "3"]}
            ]
            (root / "checkpoint.json").write_text(
                json.dumps(checkpoint), encoding="utf-8"
            )
            result = summarize_rq2_metrics(root)
            self.assertEqual(result["completion"]["input_artifacts"], 3)
            self.assertEqual(result["completion"]["pending_artifacts"], 1)

    def test_formal_rq1_requires_final_codebook(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self._write_run(root)
            (root / "final_codebook.json").unlink()
            with self.assertRaises(EvaluationError):
                export_rq1_materials(root, StaticAnalysisNondeterminismAdapter())

    def test_held_out_export_is_reference_blind_and_scores_are_packet_scoped(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self._write_run(root)
            adapter = StaticAnalysisNondeterminismAdapter()
            checkpoint = json.loads((root / "checkpoint.json").read_text(encoding="utf-8"))
            held_artifacts = list(adapter.iter_artifacts())[2:4]
            checkpoint["held_out_batches"] = [
                {
                    "artifact_ids": [item.artifact_id for item in held_artifacts],
                    "split_name": "held_out_pool",
                }
            ]
            checkpoint["codebook"]["codes"] = [
                {"code_id": "code-a", "name": "Code A", "status": "active"}
            ]
            from coda.completion import decision_fingerprint
            checkpoint["metadata"]["final_validation_audits"]["fixture"]["decision_fingerprint"] = decision_fingerprint(
                checkpoint["codebook"], checkpoint["history"]["coding_records"])

            (root / "checkpoint.json").write_text(
                json.dumps(checkpoint), encoding="utf-8"
            )
            (root / "final_codebook.json").write_text(
                json.dumps(checkpoint["codebook"]), encoding="utf-8"
            )
            manifest = json.loads((root / "run_manifest.json").read_text(encoding="utf-8"))
            manifest["data"]["held_out_artifacts"] = [
                {"artifact_id": item.artifact_id} for item in held_artifacts
            ]
            (root / "run_manifest.json").write_text(
                json.dumps(manifest), encoding="utf-8"
            )
            packet = export_held_out_materials(root, adapter)

            self.assertEqual(packet["format"], "coda-held-out-application-materials")
            self.assertFalse(packet["reference_data_included"])
            self.assertEqual(
                {item["artifact_id"] for item in packet["artifacts"]},
                {item.artifact_id for item in held_artifacts},
            )
            self.assertNotIn("category", packet["artifacts"][0]["raw_fields"])

            rows = [
                {
                    "run_id": "run-test",
                    "evaluator_id": evaluator,
                    "artifact_id": held_artifacts[0].artifact_id,
                    "decision": "assigned",
                    "code_ids": ["code-a"],
                    "rationale": "The definition covers the observed case.",
                    "duration_seconds": 20,
                }
                for evaluator in ("coder-a", "coder-b")
            ]
            summary = summarize_held_out_packet_scores(packet, rows)
            self.assertEqual(summary["agreement"]["exact_set_agreement"], 1.0)
            self.assertEqual(summary["completion_by_evaluator"]["coder-a"]["expected"], 2)
            self.assertEqual(summary["completion_by_evaluator"]["coder-a"]["completed"], 1)
            with self.assertRaises(EvaluationError):
                summarize_held_out_packet_scores(
                    packet,
                    [{**rows[0], "artifact_id": "not-held-out"}],
                )

    def test_held_out_export_requires_terminal_frozen_run(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self._write_run(root)
            (root / "final_codebook.json").unlink()
            adapter = StaticAnalysisNondeterminismAdapter()
            with self.assertRaises(EvaluationError):
                export_held_out_materials(root, adapter)


if __name__ == "__main__":
    unittest.main()
