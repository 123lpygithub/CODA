from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from fastapi.testclient import TestClient
from httpx import Request
from openai import APITimeoutError

from adapters.static_analysis import StaticAnalysisNondeterminismAdapter
from coda.web.api import _http_error, create_app
from coda.web.runtime import CodaWebService
from tests.test_web_runtime import _build_test_bootstrap, _build_test_orchestrator


class TestCodaWebApi(unittest.TestCase):
    def test_llm_timeout_is_translated_to_gateway_timeout(self) -> None:
        error = _http_error(APITimeoutError(Request("POST", "https://example.test")))
        self.assertEqual(error.status_code, 504)
        self.assertIn("LLM 请求超时", str(error.detail))

    def test_analytic_memo_status_lifecycle_is_available_over_http(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            service = CodaWebService(
                runs_root=Path(temp_dir) / "runs",
                adapter_factories={
                    "static_analysis_nondeterminism": StaticAnalysisNondeterminismAdapter
                },
                orchestrator_factory=lambda: _build_test_orchestrator([]),
                bootstrap_factory=_build_test_bootstrap,
            )
            client = TestClient(create_app(service))
            created = client.post(
                "/api/runs",
                json={
                    "dataset_name": "static_analysis_nondeterminism",
                    "artifact_limit": 1,
                    "review_mode": "full",
                },
            ).json()
            run_id = created["run_id"]
            memo = service._load_run_state(run_id).history.append_analytic_memo(
                {"memo_type": "boundary", "summary": "Review this boundary."}
            )

            response = client.post(
                f"/api/runs/{run_id}/analytic-memos/{memo['memo_id']}/status",
                json={
                    "status": "resolved",
                    "rationale": "The source evidence now resolves the boundary.",
                },
            )

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["memo"]["status"], "resolved")
            history = client.get(f"/api/runs/{run_id}/history").json()
            self.assertEqual(history["analytic_memos"][0]["status"], "resolved")

    def _create_prepared_run(
        self,
        client: TestClient,
        *,
        artifact_limit: int = 1,
    ) -> tuple[str, str]:
        created = client.post(
            "/api/runs",
            json={
                "dataset_name": "static_analysis_nondeterminism",
                "artifact_limit": artifact_limit,
                "review_mode": "full",
            },
        )
        self.assertEqual(created.status_code, 201)
        run_id = created.json()["run_id"]
        initialized = client.post(f"/api/runs/{run_id}/initialize")
        self.assertEqual(initialized.status_code, 200)
        initial_review = client.post(
            f"/api/runs/{run_id}/stage-reviews/initial",
            json={"decision": "accept", "rationale": "Initial review complete."},
        )
        self.assertEqual(initial_review.status_code, 200)
        artifact_id = client.get(f"/api/runs/{run_id}/current-artifact").json()["artifact"]["artifact_id"]
        self.assertEqual(client.post(f"/api/runs/{run_id}/prepare-review").status_code, 200)
        return run_id, artifact_id

    def test_create_then_initialize_over_http(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            service = CodaWebService(
                runs_root=Path(temp_dir) / "runs",
                adapter_factories={"static_analysis_nondeterminism": StaticAnalysisNondeterminismAdapter},
                orchestrator_factory=lambda: _build_test_orchestrator([]),
                bootstrap_factory=_build_test_bootstrap,
            )
            client = TestClient(create_app(service))
            response = client.post(
                "/api/runs",
                json={
                    "dataset_name": "static_analysis_nondeterminism",
                    "artifact_limit": 2,
                    "review_mode": "full",
                    "experiment_variant": "freeze_after_initialization",
                },
            )
            self.assertEqual(response.status_code, 201)
            summary = response.json()
            self.assertEqual(summary["bootstrap_status"], "not_run")
            self.assertEqual(
                summary["experiment_variant"], "freeze_after_initialization"
            )
            self.assertIsNone(client.get(f"/api/runs/{summary['run_id']}/current-artifact").json()["artifact"])

            initialized = client.post(f"/api/runs/{summary['run_id']}/initialize")
            self.assertEqual(initialized.status_code, 200)
            self.assertEqual(initialized.json()["bootstrap_status"], "completed")
            initial_review = client.post(
                f"/api/runs/{summary['run_id']}/stage-reviews/initial",
                json={"decision": "accept", "rationale": "Initial review complete."},
            )
            self.assertEqual(initial_review.status_code, 200)
            self.assertEqual(summary["input_artifacts"], 2)
            self.assertIsNotNone(client.get(f"/api/runs/{summary['run_id']}/current-artifact").json()["artifact"])

    def test_cancel_initialization_endpoint_delegates_to_runtime(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            service = CodaWebService(runs_root=Path(temp_dir) / "runs")
            service.cancel_initialization = lambda run_id: {  # type: ignore[method-assign]
                "run_id": run_id,
                "bootstrap_status": "cancelling",
            }
            client = TestClient(create_app(service))

            response = client.post("/api/runs/run-test/initialize/cancel")

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["bootstrap_status"], "cancelling")

    def test_review_lifecycle_is_available_over_http(self) -> None:
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
            client = TestClient(create_app(service))

            self.assertEqual(client.get("/api/health").json(), {"status": "ok"})
            cors = client.options(
                "/api/datasets",
                headers={
                    "Origin": "http://127.0.0.1:5175",
                    "Access-Control-Request-Method": "GET",
                },
            )
            self.assertEqual(cors.status_code, 200)
            self.assertEqual(cors.headers["access-control-allow-origin"], "http://127.0.0.1:5175")
            created = client.post(
                "/api/runs",
                json={
                    "dataset_name": "static_analysis_nondeterminism",
                    "artifact_limit": 2,
                    "review_mode": "full",
                },
            )
            self.assertEqual(created.status_code, 201)
            run_id = created.json()["run_id"]

            self.assertIsNone(client.get(f"/api/runs/{run_id}/current-artifact").json()["artifact"])
            self.assertEqual(client.post(f"/api/runs/{run_id}/prepare-review").status_code, 409)
            self.assertEqual(client.post(f"/api/runs/{run_id}/initialize").status_code, 200)
            self.assertEqual(
                client.post(
                    f"/api/runs/{run_id}/stage-reviews/initial",
                    json={
                        "decision": "accept",
                        "rationale": "Initial review complete.",
                    },
                ).status_code,
                200,
            )

            current = client.get(f"/api/runs/{run_id}/current-artifact")
            self.assertEqual(current.status_code, 200)
            artifact_id = current.json()["artifact"]["artifact_id"]

            packet = client.post(f"/api/runs/{run_id}/prepare-review")
            self.assertEqual(packet.status_code, 200)
            self.assertEqual(packet.json()["artifact_id"], artifact_id)
            self.assertEqual(len(packet.json()["review_input"]["evidence_packet"]["coder_outputs"]), 2)

            submitted = client.post(
                f"/api/runs/{run_id}/submit-review",
                json={
                    "artifact_id": artifact_id,
                    "decision": "accept",
                    "pre_read_memo": "The issue appears to describe a root cause in analysis logic.",
                    "final_codes": [
                        {
                            "code_id": "analysis-logic",
                            "name": "Analysis Logic",
                            "definition": "Human-approved analysis root cause.",
                            "representative_artifact_ids": [artifact_id],
                        }
                    ],
                    "rationale": "The evidence supports this code.",
                    "evidence_summary": ["Issue text supports the root cause."],
                    "confirmed_evidence": [{
                        "field_name": "content",
                        "excerpt": "Tool:",
                        "rationale": "The artifact text supports the code.",
                    }],
                    "duration_seconds": 12.5,
                    "codebook_changes": [
                        {
                            "action": "add",
                            "summary": "Add Analysis Logic.",
                            "rationale": "The first reviewed artifact establishes this new concept.",
                            "resulting_code_ids": ["analysis-logic"],
                            "artifact_ids": [artifact_id],
                        }
                    ],
                },
            )
            self.assertEqual(submitted.status_code, 200)
            self.assertEqual(submitted.json()["run"]["status"], "awaiting_next_artifact")
            self.assertEqual(submitted.json()["codebook"]["version"], 1)

            versions = client.get(f"/api/runs/{run_id}/codebook/versions")
            self.assertEqual(versions.status_code, 200)
            self.assertEqual([snapshot["version"] for snapshot in versions.json()["snapshots"]], [0, 1])
            self.assertEqual(versions.json()["diffs"][0]["added"][0]["code_id"], "analysis-logic")

            assigned = client.get(
                f"/api/runs/{run_id}/codebook/analysis-logic/artifacts"
            )
            self.assertEqual(assigned.status_code, 200)
            self.assertEqual(assigned.json()["artifact_count"], 1)
            self.assertEqual(
                assigned.json()["artifacts"][0]["artifact"]["artifact_id"],
                artifact_id,
            )

            history = client.get(f"/api/runs/{run_id}/history")
            self.assertEqual(history.status_code, 200)
            self.assertEqual(len(history.json()["coding_records"]), 1)
            self.assertEqual(history.json()["coding_records"][0]["artifact_id"], artifact_id)
            self.assertEqual(
                history.json()["coding_records"][0]["pre_read_memo"],
                "The issue appears to describe a root cause in analysis logic.",
            )
            self.assertEqual(
                history.json()["coding_records"][0]["metadata"]["duration_seconds"],
                12.5,
            )
            self.assertEqual(len(history.json()["codebook_revisions"]), 1)
            self.assertEqual(len(history.json()["artifact_runs"]), 1)

            artifacts = client.get(f"/api/runs/{run_id}/artifacts")
            self.assertEqual(artifacts.status_code, 200)
            self.assertEqual(artifacts.json()["checkpoint"]["review_count"], 1)
            self.assertEqual(len(artifacts.json()["reviews"]), 1)
            self.assertEqual(len(artifacts.json()["artifact_runs"]), 1)

            blocked_current = client.get(f"/api/runs/{run_id}/current-artifact")
            self.assertIsNone(blocked_current.json()["artifact"])
            advanced = client.post(f"/api/runs/{run_id}/next-artifact")
            self.assertEqual(advanced.status_code, 200)
            self.assertIsNotNone(advanced.json()["current"]["artifact"])

    def test_api_rejects_incoherent_terminal_review(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            service = CodaWebService(
                runs_root=Path(temp_dir) / "runs",
                adapter_factories={
                    "static_analysis_nondeterminism": StaticAnalysisNondeterminismAdapter
                },
                orchestrator_factory=lambda: _build_test_orchestrator([]),
                bootstrap_factory=_build_test_bootstrap,
            )
            client = TestClient(create_app(service))
            created = client.post(
                "/api/runs",
                json={
                    "dataset_name": "static_analysis_nondeterminism",
                    "artifact_limit": 1,
                    "review_mode": "full",
                },
            )
            run_id = created.json()["run_id"]
            self.assertEqual(client.post(f"/api/runs/{run_id}/initialize").status_code, 200)
            self.assertEqual(
                client.post(
                    f"/api/runs/{run_id}/stage-reviews/initial",
                    json={"decision": "accept", "rationale": "Initial review complete."},
                ).status_code,
                200,
            )
            artifact_id = client.get(f"/api/runs/{run_id}/current-artifact").json()["artifact"]["artifact_id"]
            self.assertEqual(client.post(f"/api/runs/{run_id}/prepare-review").status_code, 200)

            rejected = client.post(
                f"/api/runs/{run_id}/submit-review",
                json={
                    "artifact_id": artifact_id,
                    "decision": "reject",
                    "pre_read_memo": "The artifact does not support a stable code.",
                    "final_codes": [
                        {
                            "code_id": "should-not-persist",
                            "name": "Should Not Persist",
                            "definition": "An invalid reject combination.",
                        }
                    ],
                    "rationale": "The candidates are unsupported.",
                    "evidence_summary": ["The artifact is ambiguous."],
                },
            )
            self.assertEqual(rejected.status_code, 422)
            self.assertIn("cannot include final codes", rejected.json()["detail"])

            missing_memo = client.post(
                f"/api/runs/{run_id}/submit-review",
                json={
                    "artifact_id": artifact_id,
                    "decision": "accept",
                    "pre_read_memo": " ",
                    "rationale": "A valid rationale without the required memo.",
                },
            )
            self.assertEqual(missing_memo.status_code, 422)
            self.assertIn("pre-read memo", missing_memo.json()["detail"])

    def test_api_rejects_add_of_an_existing_code(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            service = CodaWebService(
                runs_root=Path(temp_dir) / "runs",
                adapter_factories={
                    "static_analysis_nondeterminism": StaticAnalysisNondeterminismAdapter
                },
                orchestrator_factory=lambda: _build_test_orchestrator([]),
                bootstrap_factory=_build_test_bootstrap,
            )
            client = TestClient(create_app(service))
            run_id, first_artifact_id = self._create_prepared_run(client, artifact_limit=2)
            first_review = {
                "artifact_id": first_artifact_id,
                "decision": "accept",
                "pre_read_memo": "The first artifact suggests a new analysis concept.",
                "final_codes": [{
                    "code_id": "analysis-logic",
                    "name": "Analysis Logic",
                    "definition": "A human-approved analysis root cause.",
                    "representative_artifact_ids": [first_artifact_id],
                }],
                "rationale": "The evidence supports the new concept.",
                "evidence_summary": ["The issue text supports the root cause."],
                "confirmed_evidence": [{
                    "field_name": "content",
                    "excerpt": "Tool:",
                    "rationale": "The artifact text supports the code.",
                }],
                "codebook_changes": [{
                    "action": "add",
                    "summary": "Add Analysis Logic.",
                    "rationale": "The concept is absent from the current codebook.",
                    "resulting_code_ids": ["analysis-logic"],
                }],
            }
            self.assertEqual(
                client.post(f"/api/runs/{run_id}/submit-review", json=first_review).status_code,
                200,
            )
            self.assertEqual(client.post(f"/api/runs/{run_id}/next-artifact").status_code, 200)
            second_artifact_id = client.get(
                f"/api/runs/{run_id}/current-artifact"
            ).json()["artifact"]["artifact_id"]
            self.assertEqual(client.post(f"/api/runs/{run_id}/prepare-review").status_code, 200)

            duplicate_add = client.post(
                f"/api/runs/{run_id}/submit-review",
                json={
                    "artifact_id": second_artifact_id,
                    "decision": "revise",
                    "pre_read_memo": "This artifact fits the existing concept.",
                    "final_codes": [{
                        "code_id": "analysis-logic",
                        "name": "Analysis Logic",
                        "definition": "A human-approved analysis root cause.",
                    }],
                    "rationale": "The code already exists, so it must not be added again.",
                    "evidence_summary": ["The issue is another analysis root cause."],
                    "confirmed_evidence": [{
                        "field_name": "content",
                        "excerpt": "Tool:",
                        "rationale": "The artifact text supports the code.",
                    }],
                    "codebook_changes": [{
                        "action": "add",
                        "summary": "Incorrectly add the existing code again.",
                        "rationale": "This is deliberately invalid.",
                        "resulting_code_ids": ["analysis-logic"],
                    }],
                },
            )
            self.assertEqual(duplicate_add.status_code, 422)
            self.assertIn("Add cannot reuse an existing code id", duplicate_add.json()["detail"])

    def test_api_rejects_merge_with_fewer_than_two_targets(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            service = CodaWebService(
                runs_root=Path(temp_dir) / "runs",
                adapter_factories={
                    "static_analysis_nondeterminism": StaticAnalysisNondeterminismAdapter
                },
                orchestrator_factory=lambda: _build_test_orchestrator([]),
                bootstrap_factory=_build_test_bootstrap,
            )
            client = TestClient(create_app(service))
            run_id, artifact_id = self._create_prepared_run(client)
            invalid_merge = client.post(
                f"/api/runs/{run_id}/submit-review",
                json={
                    "artifact_id": artifact_id,
                    "decision": "revise",
                    "pre_read_memo": "The relationship between concepts is not established.",
                    "rationale": "This request is deliberately malformed.",
                    "codebook_changes": [{
                        "action": "merge",
                        "summary": "Attempt a merge without enough source codes.",
                        "rationale": "This should be rejected by the workflow boundary.",
                        "resulting_code_ids": ["merged-code"],
                    }],
                },
            )
            self.assertEqual(invalid_merge.status_code, 422)
            self.assertIn("Merge requires at least two targets", invalid_merge.json()["detail"])

    def test_api_applies_add_parent_without_merging_children(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            service = CodaWebService(
                runs_root=Path(temp_dir) / "runs",
                adapter_factories={
                    "static_analysis_nondeterminism": StaticAnalysisNondeterminismAdapter
                },
                orchestrator_factory=lambda: _build_test_orchestrator([]),
                bootstrap_factory=_build_test_bootstrap,
            )
            client = TestClient(create_app(service))
            run_id, first_artifact_id = self._create_prepared_run(client, artifact_limit=2)
            first_review = {
                "artifact_id": first_artifact_id,
                "decision": "revise",
                "pre_read_memo": "The first artifact establishes two distinct traversal subtypes.",
                "final_codes": [
                    {
                        "code_id": "normal-flow",
                        "name": "Normal Flow",
                        "definition": "Incorrect traversal of normal control-flow edges.",
                    },
                    {
                        "code_id": "exceptional-flow",
                        "name": "Exceptional Flow",
                        "definition": "Incorrect traversal of exceptional control-flow edges.",
                    },
                ],
                "rationale": "The subtypes should remain separate for later coding.",
                "evidence_summary": ["The artifact distinguishes normal and exceptional traversal."],
                "confirmed_evidence": [{
                    "field_name": "content",
                    "excerpt": "Tool:",
                    "rationale": "The artifact text supports the codes.",
                }],
                "codebook_changes": [
                    {
                        "action": "add",
                        "summary": "Add Normal Flow.",
                        "rationale": "The first subtype is not represented.",
                        "resulting_code_ids": ["normal-flow"],
                    },
                    {
                        "action": "add",
                        "summary": "Add Exceptional Flow.",
                        "rationale": "The second subtype is not represented.",
                        "resulting_code_ids": ["exceptional-flow"],
                    },
                ],
            }
            self.assertEqual(
                client.post(f"/api/runs/{run_id}/submit-review", json=first_review).status_code,
                200,
            )
            self.assertEqual(client.post(f"/api/runs/{run_id}/next-artifact").status_code, 200)
            second_artifact_id = client.get(
                f"/api/runs/{run_id}/current-artifact"
            ).json()["artifact"]["artifact_id"]
            self.assertEqual(client.post(f"/api/runs/{run_id}/prepare-review").status_code, 200)

            parent_review = client.post(
                f"/api/runs/{run_id}/submit-review",
                json={
                    "artifact_id": second_artifact_id,
                    "decision": "revise",
                    "pre_read_memo": "The second artifact suggests a shared higher-level traversal concept.",
                    "final_codes": [{
                        "code_id": "control-flow-traversal",
                        "name": "Control Flow Traversal",
                        "definition": "Problems caused by incorrect control-flow traversal semantics.",
                    }],
                    "rationale": "The two existing subtype codes share a useful parent abstraction.",
                    "evidence_summary": ["The artifact supports a shared control-flow traversal concern."],
                    "confirmed_evidence": [{
                        "field_name": "content",
                        "excerpt": "Tool:",
                        "rationale": "The artifact text supports the parent concept.",
                    }],
                    "codebook_changes": [{
                        "action": "add_parent",
                        "summary": "Add Control Flow Traversal as a parent.",
                        "rationale": "The child codes remain analytically distinct but share this broader concept.",
                        "target_code_ids": ["normal-flow", "exceptional-flow"],
                        "resulting_code_ids": ["control-flow-traversal"],
                    }],
                },
            )
            self.assertEqual(parent_review.status_code, 200)
            codebook = parent_review.json()["codebook"]
            # The two additions in the first artifact form one atomic commit;
            # the parent addition in the second artifact forms the next one.
            self.assertEqual(codebook["version"], 2)
            self.assertEqual(len(codebook["revisions"]), 3)
            by_id = {code["code_id"]: code for code in codebook["codes"]}
            self.assertEqual(by_id["normal-flow"]["status"], "active")
            self.assertEqual(by_id["exceptional-flow"]["status"], "active")
            self.assertEqual(by_id["normal-flow"]["parent_code_id"], "control-flow-traversal")
            self.assertEqual(by_id["exceptional-flow"]["parent_code_id"], "control-flow-traversal")
            self.assertEqual(by_id["control-flow-traversal"]["status"], "active")


    def test_api_deletes_a_saved_run(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            service = CodaWebService(
                runs_root=Path(temp_dir) / "runs",
                adapter_factories={
                    "static_analysis_nondeterminism": StaticAnalysisNondeterminismAdapter
                },
                orchestrator_factory=lambda: _build_test_orchestrator([]),
            )
            client = TestClient(create_app(service))
            created = client.post(
                "/api/runs",
                json={"dataset_name": "static_analysis_nondeterminism", "artifact_limit": 1},
            )
            self.assertEqual(created.status_code, 201)
            run_id = created.json()["run_id"]

            deleted = client.delete(f"/api/runs/{run_id}")
            self.assertEqual(deleted.status_code, 200)
            self.assertEqual(deleted.json(), {"run_id": run_id, "deleted": True})
            self.assertEqual(client.get("/api/runs").json(), [])
            self.assertEqual(client.get(f"/api/runs/{run_id}").status_code, 404)

    def test_delete_is_allowed_by_cors_preflight(self) -> None:
        client = TestClient(create_app(CodaWebService(runs_root=Path("/tmp/coda-test-cors"))))
        response = client.options(
            "/api/runs/example",
            headers={
                "Origin": "http://127.0.0.1:5173",
                "Access-Control-Request-Method": "DELETE",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("DELETE", response.headers.get("access-control-allow-methods", ""))


if __name__ == "__main__":
    unittest.main()
