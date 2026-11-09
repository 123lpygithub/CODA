"""Review coverage is chosen at Initial Review without repeating initialization."""

import json
from pathlib import Path
import tempfile
import unittest

from fastapi.testclient import TestClient

from adapters import StaticAnalysisNondeterminismAdapter
from coda.bootstrap import BootstrapAssignment, BootstrapResult
from coda.persistence import save_run_state_checkpoint
from coda.state import CodebookState, CodeState
from coda.web.api import create_app
from coda.web.runtime import CodaWebService
from tests.test_web_runtime import _build_test_bootstrap, _build_existing_code_bootstrap, _build_test_orchestrator


class TestInitialReviewSetting(unittest.TestCase):
    def service(self, root, bootstrap=_build_test_bootstrap):
        return CodaWebService(
            runs_root=root,
            adapter_factories={"static_analysis_nondeterminism": StaticAnalysisNondeterminismAdapter},
            orchestrator_factory=lambda: _build_test_orchestrator([]),
            bootstrap_factory=bootstrap,
        )

    def create(self, client, setting="selective"):
        response = client.post("/api/runs", json={
            "dataset_name": "static_analysis_nondeterminism", "artifact_limit": 5,
            "review_mode": setting,
        })
        self.assertEqual(response.status_code, 201, response.text)
        return response.json()["run_id"]

    def test_selection_refreshes_coverage_and_persists_without_recoding(self):
        calls = []

        def bootstrap_factory(_):
            class Bootstrap:
                def run(self, run_state, artifacts):
                    calls.append("bootstrap")
                    ids = [item.artifact_id for item in artifacts[:3]]
                    return BootstrapResult(
                        codebook=CodebookState(
                            dataset_name=run_state.dataset_metadata.dataset_name, version=1,
                            codes=[CodeState(code_id="logic", name="Logic", definition="Analysis logic.",
                                             representative_artifact_ids=[ids[0]])],
                        ),
                        artifact_ids=ids,
                        group_ids={item.artifact_id: item.artifact_id for item in artifacts},
                        assignments=[BootstrapAssignment(item, ["logic"], ["Direct source evidence."]) for item in ids],
                    )
            return Bootstrap()

        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            service = self.service(root, bootstrap_factory)
            client = TestClient(create_app(service))
            run_id = self.create(client)
            endpoint = f"/api/runs/{run_id}/initial-review-setting"
            self.assertEqual(client.post(endpoint, json={"setting": "full"}).status_code, 409)
            initialized = client.post(f"/api/runs/{run_id}/initialize").json()
            self.assertEqual(initialized["status"], "awaiting_initial_review")
            self.assertFalse(initialized["review_setting_locked"])
            initial_packet = client.get(f"/api/runs/{run_id}/stage-reviews/initial").json()
            self.assertEqual(len(initial_packet["assignments"]), 1)
            for setting, count in (("full", 3), ("automatic", 0), ("selective", 1)):
                with self.subTest(setting=setting):
                    response = client.post(endpoint, json={"setting": setting})
                    self.assertEqual(response.status_code, 200, response.text)
                    result = response.json()
                    self.assertEqual(result["run"]["status"], "awaiting_initial_review")
                    self.assertEqual(result["run"]["review_setting"], setting)
                    self.assertEqual(result["run"]["review_mode"], setting)
                    self.assertFalse(result["run"]["review_setting_locked"])
                    self.assertEqual(len(result["packet"]["assignments"]), count)
                    checkpoint = json.loads((root / run_id / "checkpoint.json").read_text())
                    policy = checkpoint["review_policy"]
                    self.assertEqual(policy["initial_review_required"], setting != "automatic")
                    self.assertEqual(policy["final_review_required"], setting != "automatic")
                    self.assertEqual(policy["random_audit_rate"], 0 if setting == "automatic" else .1)
                    manifest = json.loads(Path(result["run"]["run_manifest"]).read_text())
                    self.assertEqual(manifest["protocol"]["review_policy"], policy)
                    reloaded = self.service(root).run_summary(run_id)
                    self.assertEqual(reloaded["review_setting"], setting)
                    self.assertFalse(reloaded["review_setting_locked"])
            self.assertEqual(calls, ["bootstrap"])
            response = client.post(f"/api/runs/{run_id}/stage-reviews/initial", json={
                "decision": "accept", "rationale": "Reviewed the initial definitions and evidence.",
            })
            self.assertEqual(response.status_code, 200, response.text)
            self.assertFalse(client.get(f"/api/runs/{run_id}").json()["review_setting_locked"])
            changed = client.post(endpoint, json={"setting": "full"})
            self.assertEqual(changed.status_code, 200, changed.text)
            self.assertTrue(changed.json()["packet"]["inspection_only"])
            self.assertEqual(changed.json()["packet"]["codebook"]["version"], 1)
            self.assertEqual(client.get(f"/api/runs/{run_id}").json()["initial_review"]["metadata"]["review_policy"]["setting"], "selective")

    def test_can_change_policy_after_initial_review_while_idle_and_preserve_pending_route(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            service = self.service(root, _build_existing_code_bootstrap)
            client = TestClient(create_app(service))
            run_id = self.create(client)
            client.post(f"/api/runs/{run_id}/initialize")
            accepted = client.post(f"/api/runs/{run_id}/stage-reviews/initial", json={
                "decision": "accept", "rationale": "Reviewed the initial codebook and evidence.",
            })
            self.assertEqual(accepted.status_code, 200, accepted.text)
            state = service._load_run_state(run_id)
            pending = state.current_batch().artifacts[0]
            state.status = "awaiting_human_review"
            state.metadata["awaiting_human_review"] = {
                "artifact_id": pending.artifact_id,
                "codebook_version": state.codebook.version,
                "routing_decision": {"route": "human_review", "setting": "selective"},
            }
            save_run_state_checkpoint(state, service._paths_for(run_id).checkpoint_path)
            endpoint = f"/api/runs/{run_id}/initial-review-setting"
            result = client.post(endpoint, json={"setting": "full"})
            self.assertEqual(result.status_code, 200, result.text)
            summary = result.json()["run"]
            self.assertEqual(summary["review_setting"], "full")
            self.assertFalse(summary["review_setting_locked"])
            waiting = service._load_run_state(run_id).metadata["awaiting_human_review"]
            self.assertEqual(waiting["review_policy"]["setting"], "selective")
            self.assertEqual(service._load_run_state(run_id).review_policy.setting, "full")
            stage = service._load_run_state(run_id).history.stage_reviews[-1]
            self.assertEqual(stage.metadata["review_policy"]["setting"], "selective")
            self.assertEqual(len(service._load_run_state(run_id).metadata["review_setting_history"]), 1)
            service._processing_runs.add(run_id)
            try:
                blocked = client.post(endpoint, json={"setting": "automatic"})
                self.assertEqual(blocked.status_code, 409)
            finally:
                service._processing_runs.discard(run_id)

    def test_pending_review_keeps_original_route_across_restart_after_mode_change(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            service = self.service(root, _build_existing_code_bootstrap)
            client = TestClient(create_app(service))
            run_id = self.create(client, "full")
            client.post(f"/api/runs/{run_id}/initialize")
            response = client.post(f"/api/runs/{run_id}/stage-reviews/initial", json={
                "decision": "accept", "rationale": "Checked the initial definitions and source material.",
            })
            self.assertEqual(response.status_code, 200, response.text)
            original = service.prepare_review(run_id)
            self.assertEqual(original["review_input"]["evidence_packet"]["routing_decision"]["setting"], "full")
            response = client.post(f"/api/runs/{run_id}/initial-review-setting", json={"setting": "automatic"})
            self.assertEqual(response.status_code, 200, response.text)
            self.assertFalse(response.json()["run"]["review_setting_locked"])
            restarted = self.service(root, _build_existing_code_bootstrap)
            restored = restarted.review_packet(run_id)
            routing = restored["review_input"]["evidence_packet"]["routing_decision"]
            self.assertEqual(routing["setting"], "full")
            self.assertEqual(routing["route"], "human_review")
            self.assertEqual(restarted._load_run_state(run_id).review_policy.setting, "automatic")
            self.assertEqual(restarted._load_run_state(run_id).status, "awaiting_human_review")

    def test_automatic_continuation_records_no_human_approval(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            service = self.service(root)
            client = TestClient(create_app(service))
            run_id = self.create(client)
            client.post(f"/api/runs/{run_id}/initialize")
            endpoint = f"/api/runs/{run_id}/initial-review-setting"
            self.assertEqual(client.post(endpoint, json={"setting": "full", "continue_automatic": True}).status_code, 409)
            client.post(endpoint, json={"setting": "automatic"})
            # A radio selection neither approves the codebook nor leaves the checkpoint.
            response = client.post(f"/api/runs/{run_id}/stage-reviews/initial", json={
                "decision": "accept", "rationale": "Must not become a human approval.",
            })
            self.assertEqual(response.status_code, 409)
            result = client.post(endpoint, json={"setting": "automatic", "continue_automatic": True})
            self.assertEqual(result.status_code, 200, result.text)
            self.assertEqual(result.json()["run"]["status"], "in_progress")
            self.assertFalse(result.json()["run"]["review_setting_locked"])
            self.assertIsNone(result.json()["packet"])
            state = self.service(root)._load_run_state(run_id)
            self.assertEqual(state.history.stage_reviews, [])
            self.assertFalse(state.metadata["bootstrap"]["human_reviewed"])
            self.assertFalse(state.review_policy.final_review_required)
            self.assertEqual(client.post(endpoint, json={"setting": "selective"}).status_code, 200)

    def test_study_assignment_is_not_editable(self):
        with tempfile.TemporaryDirectory() as temp:
            service = self.service(Path(temp))
            client = TestClient(create_app(service))
            run_id = self.create(client)
            client.post(f"/api/runs/{run_id}/initialize")
            state = service._load_run_state(run_id)
            state.metadata["study_materials"] = {"study_id": "matched-test"}
            save_run_state_checkpoint(state, service._paths_for(run_id).checkpoint_path)
            response = client.post(f"/api/runs/{run_id}/initial-review-setting", json={"setting": "full"})
            self.assertEqual(response.status_code, 409)
            self.assertEqual(client.get(f"/api/runs/{run_id}").json()["review_setting"], "selective")

    def test_historical_initial_inspection_uses_saved_snapshot_without_mutation(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            service = self.service(root, _build_existing_code_bootstrap)
            client = TestClient(create_app(service))
            run_id = self.create(client)
            client.post(f"/api/runs/{run_id}/initialize")
            response = client.post(f"/api/runs/{run_id}/stage-reviews/initial", json={
                "decision": "accept", "rationale": "Initial definitions and evidence checked.",
            })
            self.assertEqual(response.status_code, 200, response.text)
            state = service._load_run_state(run_id)
            state.codebook = CodebookState(
                dataset_name=state.codebook.dataset_name, version=3,
                codes=[CodeState(code_id="later", name="Later category", definition="Added during iteration.")],
            )
            checkpoint = service._paths_for(run_id).checkpoint_path
            save_run_state_checkpoint(state, checkpoint)
            before = checkpoint.read_bytes()
            endpoint = f"/api/runs/{run_id}/stage-reviews/initial"
            self.assertEqual(client.get(endpoint).status_code, 409)
            response = client.get(endpoint + "?inspection=true")
            self.assertEqual(response.status_code, 200, response.text)
            packet = response.json()
            self.assertTrue(packet["inspection_only"])
            self.assertEqual(packet["codebook"]["version"], 1)
            self.assertEqual(packet["codebook"]["codes"][0]["code_id"], "analysis-logic")
            self.assertEqual(packet["review_record"]["decision"], "accept")
            self.assertEqual(checkpoint.read_bytes(), before)
            self.assertEqual(service._load_run_state(run_id).codebook.version, 3)
            changed = client.post(f"/api/runs/{run_id}/initial-review-setting", json={"setting": "full"})
            self.assertEqual(changed.status_code, 200, changed.text)
            self.assertEqual(changed.json()["packet"]["codebook"]["version"], 1)
            self.assertEqual(changed.json()["run"]["review_setting"], "full")
            self.assertEqual(client.get(f"/api/runs/{run_id}/stage-reviews/final?inspection=true").status_code, 409)

    def test_inspection_before_initialization_reports_unavailable(self):
        with tempfile.TemporaryDirectory() as temp:
            client = TestClient(create_app(self.service(Path(temp))))
            run_id = self.create(client)
            response = client.get(f"/api/runs/{run_id}/stage-reviews/initial?inspection=true")
            self.assertEqual(response.status_code, 409)

    def test_explicit_automatic_api_run_keeps_its_existing_routing(self):
        with tempfile.TemporaryDirectory() as temp:
            client = TestClient(create_app(self.service(Path(temp))))
            run_id = self.create(client, "automatic")
            result = client.post(f"/api/runs/{run_id}/initialize").json()
            self.assertEqual(result["status"], "in_progress")
            self.assertTrue(result["review_setting_locked"])


if __name__ == "__main__":
    unittest.main()
