from __future__ import annotations

from copy import deepcopy
from dataclasses import asdict, replace
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from fastapi.testclient import TestClient

from adapters import Defects4CodeLLMSemanticAdapter, MLSATD23ShadesAdapter, PersonalDataProtectionGitHubAdapter
from adapters.base import ArtifactRecord
from coda.agents.evaluator_agent import build_blinded_evaluator_packet
from coda.evaluation import EvaluationError, export_rq1_materials, summarize_rq1_scores
from coda.evaluation import summarize_rq2_runs
from coda.evaluator import CalibrationConfig, calibrate_evaluators
from coda.manifest import write_run_manifest
from coda.persistence import save_run_state_checkpoint
from coda.state import CodingRecordState
from coda.study import (
    StudyManifestError, build_study_manifest, select_study_artifacts, study_binding,
    study_group, validate_study_manifest, validate_study_packet, verify_study_scores,
)
from coda.web.api import create_app
from coda.web.runtime import CodaWebService, WebWorkflowError
from tests.test_web_runtime import _build_test_bootstrap, _build_test_orchestrator


SEMANTIC = "llm_code_error_semantic"
SYNTACTIC = "llm_code_error_syntactic"


def _cases() -> list[ArtifactRecord]:
    return [ArtifactRecord(
        artifact_id=f"case-{task}-{index}", content=f"Task {task} source {index}",
        raw_fields={"task_id": task, "source": f"print({task})"},
        metadata={"task_id": task},
    ) for task in range(4) for index in range(2)]


def _manifest() -> dict:
    return build_study_manifest({SEMANTIC: _cases()}, study_id="test-study",
                                pilot_group_counts={SEMANTIC: 1}, seed=17)


def _packet(manifest: dict, phase: str) -> dict:
    artifacts = select_study_artifacts(manifest, SEMANTIC, _cases(), phase)
    return {
        "run_id": f"run-{phase}", "dataset_name": SEMANTIC,
        "formal_evaluation_ready": True, "study_manifest": manifest,
        "study_materials": study_binding(manifest, SEMANTIC, phase),
        "codebook": {"codes": [{"code_id": "c1", "name": "A", "definition": "A case"}]},
        "artifacts": [{**asdict(item), "coding_record": {"final_code_ids": ["c1"]}} for item in artifacts],
    }


def _ratings(packet: dict) -> list[dict]:
    base = {"run_id": packet["run_id"], "evaluator_id": "e1", "phase": packet["study_materials"]["phase"]}
    return [
        {**base, "dimension": dim, "unit": "codebook", "score": 4}
        for dim in ("clarity", "category_boundaries", "meaningful_coverage")
    ] + [
        {**base, "dimension": "evidence_support", "unit": "assignment", "score": 2,
         "artifact_id": item["artifact_id"], "code_id": "c1"}
        for item in packet["artifacts"]
    ]


class StudyManifestTests(unittest.TestCase):
    def test_tasks_and_alternate_views_are_isolated_and_deterministic(self) -> None:
        manifest = build_study_manifest(
            {"defects4codellm_semantic": _cases(), SYNTACTIC: list(reversed(_cases()))},
            study_id="views", pilot_group_counts={SEMANTIC: 1, SYNTACTIC: 1}, seed=17,
        )
        self.assertEqual(manifest["datasets"][SEMANTIC]["artifacts"], manifest["datasets"][SYNTACTIC]["artifacts"])
        rows = manifest["datasets"][SEMANTIC]["artifacts"]
        self.assertFalse({r["group_id"] for r in rows if r["phase"] == "pilot"} &
                         {r["group_id"] for r in rows if r["phase"] == "formal"})
        second = build_study_manifest(
            {SYNTACTIC: _cases(), SEMANTIC: _cases()}, study_id="views",
            pilot_group_counts={SEMANTIC: 1, SYNTACTIC: 1}, seed=17,
        )
        self.assertEqual(manifest, second)

    def test_repository_normalization_and_shared_domain_groups(self) -> None:
        def cases(field: str, repos: list[str]) -> list[ArtifactRecord]:
            return [ArtifactRecord(str(i), repo, {field: repo}) for i, repo in enumerate(repos)]
        manifest = build_study_manifest(
            {"ml_satd_23_shades": cases("repo_name", ["Owner/A", "owner/B", "owner/C"]),
             "personal_data_protection_github": cases("project", ["https://github.com/owner/a/", "owner/b", "owner/c"])},
            study_id="repos", pilot_group_counts={"ml_satd_23_shades": 1, "personal_data_protection_github": 1},
        )
        left = {r["group_id"]: r["phase"] for r in manifest["datasets"]["ml_satd_23_shades"]["artifacts"]}
        right = {r["group_id"]: r["phase"] for r in manifest["datasets"]["personal_data_protection_github"]["artifacts"]}
        self.assertEqual(left, right)

    def test_missing_or_conflicting_group_has_no_artifact_id_fallback(self) -> None:
        with self.assertRaisesRegex(StudyManifestError, "Missing task_id"):
            study_group(SEMANTIC, ArtifactRecord("one", "source", {}))
        with self.assertRaisesRegex(StudyManifestError, "Conflicting"):
            study_group(SEMANTIC, ArtifactRecord("one", "source", {"task_id": 1}, metadata={"task_id": 2}))

    def test_evidence_drift_in_either_phase_and_missing_material_are_rejected(self) -> None:
        manifest = _manifest()
        pilot = select_study_artifacts(manifest, SEMANTIC, _cases(), "pilot")[0]
        changed = [replace(item, raw_fields={**item.raw_fields, "source": "changed"})
                   if item.artifact_id == pilot.artifact_id else item for item in _cases()]
        with self.assertRaisesRegex(StudyManifestError, "evidence changed"):
            select_study_artifacts(manifest, SEMANTIC, changed, "formal")
        with self.assertRaisesRegex(StudyManifestError, "missing"):
            select_study_artifacts(manifest, SEMANTIC, _cases()[1:], "formal")

    def test_checksum_and_group_overlap_validation(self) -> None:
        manifest = _manifest()
        manifest["seed"] += 1
        with self.assertRaisesRegex(StudyManifestError, "checksum"):
            validate_study_manifest(manifest)
        manifest = _manifest()
        rows = manifest["datasets"][SEMANTIC]["artifacts"]
        rows[0]["phase"] = "formal" if rows[0]["phase"] == "pilot" else "pilot"
        body = {k: v for k, v in manifest.items() if k != "manifest_sha256"}
        manifest["manifest_sha256"] = hashlib.sha256(json.dumps(
            body, sort_keys=True, ensure_ascii=False, separators=(",", ":"), allow_nan=False,
        ).encode()).hexdigest()
        with self.assertRaisesRegex(StudyManifestError, "overlap"):
            validate_study_manifest(manifest)

    def test_packet_and_ratings_cannot_change_phase_units_or_order(self) -> None:
        packet = _packet(_manifest(), "formal")
        validate_study_packet(packet, "formal")
        with self.assertRaisesRegex(StudyManifestError, "phase/allocation"):
            validate_study_packet(packet, "pilot")
        changed = deepcopy(packet)
        changed["artifacts"].reverse()
        with self.assertRaisesRegex(StudyManifestError, "ordered"):
            validate_study_packet(changed, "formal")
        ratings = _ratings(packet)
        verified = verify_study_scores(ratings, {packet["run_id"]: packet}, "formal")
        self.assertTrue(verified["verified"])
        with self.assertRaisesRegex(StudyManifestError, "every requested"):
            verify_study_scores(ratings[:-1], {packet["run_id"]: packet}, "formal")
        with self.assertRaisesRegex(StudyManifestError, "duplicates"):
            verify_study_scores(ratings + [ratings[0]], {packet["run_id"]: packet}, "formal")
        ratings[0]["phase"] = "pilot"
        with self.assertRaisesRegex(StudyManifestError, "Score phase"):
            verify_study_scores(ratings, {packet["run_id"]: packet}, "formal")

    def test_summary_is_honest_and_manifest_is_not_in_evaluator_prompt(self) -> None:
        packet = _packet(_manifest(), "formal")
        rows = _ratings(packet)
        self.assertFalse(summarize_rq1_scores(rows)["study_materials_verification"]["verified"])
        self.assertTrue(summarize_rq1_scores(rows, materials_by_run={packet["run_id"]: packet})[
            "study_materials_verification"]["verified"])
        blinded = build_blinded_evaluator_packet(packet)
        self.assertNotIn("study_manifest", blinded)
        self.assertNotIn("study_materials", blinded)

    def test_score_summary_rejects_mixing_different_study_manifests(self) -> None:
        left = _packet(_manifest(), "formal")
        manifest = build_study_manifest({SEMANTIC: _cases()}, study_id="another-study",
                                        pilot_group_counts={SEMANTIC: 1}, seed=17)
        right = _packet(manifest, "formal")
        right["run_id"] = "another-run"
        with self.assertRaisesRegex(StudyManifestError, "different frozen"):
            verify_study_scores(_ratings(left) + _ratings(right),
                                {left["run_id"]: left, right["run_id"]: right}, "formal")

    def test_calibration_reports_domains_and_does_not_mask_domain_failure(self) -> None:
        privacy = "personal_data_protection_github"
        privacy_cases = [replace(item, raw_fields={"project": f"owner/repo-{item.raw_fields['task_id']}"},
                                 metadata={}) for item in _cases()]
        manifest = build_study_manifest({SEMANTIC: _cases(), privacy: privacy_cases}, study_id="domains",
                                        pilot_group_counts={SEMANTIC: 1, privacy: 1})
        left = _packet(manifest, "pilot")
        right = {
            **deepcopy(left), "run_id": "privacy-pilot", "dataset_name": privacy,
            "study_materials": study_binding(manifest, privacy, "pilot"),
            "artifacts": [{**asdict(item), "coding_record": {"final_code_ids": ["c1"]}}
                          for item in select_study_artifacts(manifest, privacy, privacy_cases, "pilot")],
        }
        packets = {left["run_id"]: left, right["run_id"]: right}
        rows = []
        for packet in packets.values():
            for evaluator in ("human-a", "human-b", "candidate"):
                for row in _ratings(packet):
                    row.update(evaluator_id=evaluator, rationale="Rubric-grounded rating",
                               evaluator_kind="llm" if evaluator == "candidate" else "human")
                    if evaluator == "candidate":
                        row["candidate_model"] = "candidate-model"
                        if packet["dataset_name"] == privacy:
                            row["score"] = 0 if row["dimension"] == "evidence_support" else 1
                    rows.append(row)
        result = calibrate_evaluators(
            rows, candidate_models=["candidate-model"], human_evaluator_ids=["human-a", "human-b"],
            materials_by_run=packets, config=CalibrationConfig(bootstrap_replicates=100),
        )
        self.assertTrue(result["by_dataset"][SEMANTIC]["candidates"][0]["passes"])
        self.assertFalse(result["by_dataset"][privacy]["candidates"][0]["passes"])
        self.assertIsNone(result["selected_candidate_model"])
        self.assertTrue(result["study_materials_verification"]["verified"])

    def test_rq2_separates_pilot_formal_and_manifest_versions(self) -> None:
        from tests.test_evaluation import TestEvaluation
        with tempfile.TemporaryDirectory() as temporary:
            dirs = []
            for index, (manifest_hash, phase) in enumerate((("a", "pilot"), ("a", "formal"), ("b", "formal"))):
                root = Path(temporary) / str(index)
                root.mkdir()
                TestEvaluation()._write_run(root)
                checkpoint = json.loads((root / "checkpoint.json").read_text())
                checkpoint["run_id"] = f"run-{index}"
                checkpoint["metadata"]["study_materials"] = {"manifest_sha256": manifest_hash, "phase": phase}
                write_run_manifest(root / "checkpoint.json", checkpoint)
                dirs.append(root)
            self.assertEqual(len(summarize_rq2_runs(dirs)["groups"]), 3)

    def test_real_adapters_support_grouping_without_loading_reference_data(self) -> None:
        from unittest.mock import patch
        for factory in (Defects4CodeLLMSemanticAdapter, MLSATD23ShadesAdapter, PersonalDataProtectionGitHubAdapter):
            adapter = factory()
            with patch.object(factory, "load_reference_data", side_effect=AssertionError("Hidden reference access")):
                dataset = adapter.load_dataset_metadata().dataset_name
                artifacts = list(adapter.iter_artifacts())
                manifest = build_study_manifest({dataset: artifacts}, study_id="real-adapter-test",
                                                pilot_group_counts={dataset: 1})
                selected = select_study_artifacts(manifest, dataset, artifacts, "formal")
                self.assertLess(len(selected), len(artifacts))
                self.assertGreater(len(selected), 0)

    def test_evaluator_script_rejects_unbound_or_wrong_phase_before_api_call(self) -> None:
        script = Path(__file__).resolve().parents[1] / "scripts/run_llm_evaluator.py"
        with tempfile.TemporaryDirectory() as temporary:
            packet_path = Path(temporary) / "packet.json"
            packet = _packet(_manifest(), "pilot")
            packet_path.write_text(json.dumps(packet))
            result = subprocess.run(
                [sys.executable, str(script), str(packet_path), "--run-id", packet["run_id"],
                 "--evaluator-id", "test", "--model", "unused", "--phase", "formal",
                 "--output", str(Path(temporary) / "scores.json")], capture_output=True, text=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("phase/allocation", result.stderr)
            self.assertFalse((Path(temporary) / "scores.json").exists())


class StudyRuntimeTests(unittest.TestCase):
    @staticmethod
    def _service(root: Path) -> CodaWebService:
        return CodaWebService(
            runs_root=root,
            adapter_factories={SEMANTIC: Defects4CodeLLMSemanticAdapter},
            orchestrator_factory=lambda: _build_test_orchestrator([]),
            bootstrap_factory=_build_test_bootstrap,
        )

    def test_create_restore_export_and_drift_detection(self) -> None:
        adapter = Defects4CodeLLMSemanticAdapter()
        artifacts = list(adapter.iter_artifacts())[:20]
        manifest = build_study_manifest({SEMANTIC: artifacts}, study_id="runtime-test",
                                        pilot_group_counts={SEMANTIC: 1})
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            path = write_run_manifest(root / "materials.json", manifest)
            service = self._service(root / "runs")
            with TestClient(create_app(service=service)) as client:
                response = client.post("/api/runs", json={
                    "dataset_name": SEMANTIC, "review_mode": "automatic",
                    "study_manifest_path": str(path), "study_phase": "formal",
                })
            self.assertEqual(response.status_code, 201, response.text)
            summary = response.json()
            state = service._load_run_state(summary["run_id"])
            binding = study_binding(manifest, SEMANTIC, "formal")
            self.assertEqual(state.metadata["selected_artifact_ids"], binding["artifact_ids"])
            self.assertEqual(summary["study_materials"], binding)
            path.unlink()  # Restart uses the run's immutable snapshot.
            restored = self._service(root / "runs")._load_run_state(summary["run_id"])
            self.assertEqual(restored.metadata["study_materials"], binding)
            restored.status = "completed"
            restored.history.coding_records = [CodingRecordState(
                record_id=f"record-{index}", artifact_id=artifact_id, codebook_version=restored.codebook.version,
                dataset_name=SEMANTIC, batch_index=0,
                decision="accept", rationale="Test record", final_code_ids=[],
            ) for index, artifact_id in enumerate(binding["artifact_ids"])]
            run_dir = Path(summary["run_dir"])
            from dataclasses import asdict
            from coda.completion import decision_fingerprint
            from coda.persistence import serialize_codebook_state
            restored.metadata["final_validation_audits"] = {"fixture": {
                "status": "completed", "decision_fingerprint": decision_fingerprint(
                    serialize_codebook_state(restored.codebook),
                    [asdict(row) for row in restored.history.coding_records]),
            }}
            save_run_state_checkpoint(restored, run_dir / "checkpoint.json")
            from coda.persistence import serialize_codebook_state
            write_run_manifest(run_dir / "final_codebook.json", serialize_codebook_state(restored.codebook))
            packet = export_rq1_materials(run_dir, adapter)
            self.assertTrue(packet["study_materials_verified"])
            validate_study_packet(packet, "formal")
            checkpoint = json.loads((run_dir / "checkpoint.json").read_text())
            checkpoint["metadata"]["study_materials"]["phase"] = "pilot"
            write_run_manifest(run_dir / "checkpoint.json", checkpoint)
            with self.assertRaisesRegex(WebWorkflowError, "allocation"):
                self._service(root / "runs")._load_run_state(summary["run_id"])
            with self.assertRaisesRegex(EvaluationError, "allocation"):
                export_rq1_materials(run_dir, adapter)

    def test_bound_runs_reject_truncation_and_holdout_and_unpaired_arguments(self) -> None:
        adapter = Defects4CodeLLMSemanticAdapter()
        manifest = build_study_manifest({SEMANTIC: list(adapter.iter_artifacts())[:20]},
                                        study_id="runtime-test", pilot_group_counts={SEMANTIC: 1})
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            path = write_run_manifest(root / "materials.json", manifest)
            service = self._service(root / "runs")
            for kwargs, message in (({"artifact_limit": 1}, "artifact_limit"),
                                    ({"held_out_enabled": True}, "held-out")):
                with self.assertRaisesRegex(WebWorkflowError, message):
                    service.create_run(dataset_name=SEMANTIC, study_manifest_path=str(path),
                                       study_phase="formal", **kwargs)
            with self.assertRaisesRegex(WebWorkflowError, "both"):
                service.create_run(dataset_name=SEMANTIC, study_phase="formal")


if __name__ == "__main__":
    unittest.main()
