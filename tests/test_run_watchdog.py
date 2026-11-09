from __future__ import annotations

from concurrent.futures import Future
from copy import deepcopy
import json
from pathlib import Path
from types import SimpleNamespace
import tempfile
import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from coda.llm import LLMMessage, LLMModelConfig, OpenAIChatBackend
from coda.run_watchdog import APIRequestError, RunWatchdog, next_operation
from coda.web.api import create_app
from tests import test_web_held_out as held_out_fixtures


def observation() -> dict:
    return {
        "backend_instance_id": "server-a", "initialization_active": False, "processing_active": False,
        "run": {"run_id": "run-test", "run_dir": "runs/test", "status": "in_progress",
                "review_setting": "automatic", "bootstrap_status": "completed",
                "bootstrap_progress": {}, "reviewed_artifacts": 4, "input_artifacts": 20,
                "codebook_version": 1, "code_count": 3},
    }


class WatchdogTests(unittest.TestCase):
    def test_active_request_is_not_restarted_even_at_100_percent(self) -> None:
        value = observation()
        value["initialization_active"] = True
        value["run"]["bootstrap_status"] = "running"
        value["run"]["bootstrap_progress"] = {"overall_percent": 100}
        self.assertEqual(next_operation(value), "busy")
        value["initialization_active"] = False
        self.assertEqual(next_operation(value), "initialize")

    def test_human_checkpoints_and_cancel_are_preserved(self) -> None:
        for status in ("awaiting_initial_review", "awaiting_human_review", "awaiting_final_review", "awaiting_context"):
            value = observation()
            value["run"]["status"] = status
            self.assertEqual(next_operation(value), "human_review")
        value = observation()
        value["run"]["bootstrap_status"] = "cancelled"
        self.assertEqual(next_operation(value), "cancelled")
        self.assertEqual(next_operation(value, resume_cancelled=True), "initialize")

    def test_transport_failure_resumes_but_format_failure_does_not(self) -> None:
        value = observation()
        value["run"]["bootstrap_status"] = "failed"
        value["run"]["bootstrap_progress"] = {"error": "LLMBackendError: APIConnectionError: Connection error"}
        self.assertEqual(next_operation(value), "initialize")
        value["run"]["bootstrap_progress"]["error"] = "AgentExecutionError: Invalid code definitions"
        self.assertEqual(next_operation(value), "invalid_initialization")

    def test_http_timeout_does_not_duplicate_active_backend_work(self) -> None:
        class Client:
            def __init__(self):
                self.value = observation()
                self.value["processing_active"] = True

            def request(self, *_args, **_kwargs):
                return deepcopy(self.value)

        with tempfile.TemporaryDirectory() as temporary:
            client = Client()
            state = {"run_id": "run-test"}
            monitor = RunWatchdog(client, Path(temporary) / "watch.json", state)
            monitor.pending = Future()
            monitor.pending.set_exception(APIRequestError("HTTP timeout", transient=True))
            with patch.object(monitor, "launch") as launch:
                self.assertEqual(monitor.tick(), "busy")
                launch.assert_not_called()
                client.value["processing_active"] = False
                self.assertEqual(monitor.tick(), "process")
                launch.assert_called_once_with("process")
            saved = json.loads((Path(temporary) / "watch.json").read_text())
            self.assertEqual(saved["run_id"], "run-test")

    def test_backend_restart_resumes_same_run_and_semantic_errors_stop(self) -> None:
        value = observation()
        value["run"]["bootstrap_status"] = "running"
        value["backend_instance_id"] = "server-b"
        client = SimpleNamespace(request=lambda *_args, **_kwargs: deepcopy(value))
        with tempfile.TemporaryDirectory() as temporary:
            monitor = RunWatchdog(client, Path(temporary) / "watch.json", {"run_id": "run-test"})
            with patch.object(monitor, "launch") as launch:
                self.assertEqual(monitor.tick(), "initialize")
                launch.assert_called_once_with("initialize")
            monitor.pending = Future()
            monitor.pending.set_exception(APIRequestError("HTTP 422: Invalid assignment"))
            with self.assertRaises(APIRequestError):
                monitor.tick()

    def test_live_execution_endpoint_and_bounded_processing(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            service = held_out_fixtures.TestWebHeldOutRuns()._service(Path(temporary) / "runs")
            run = service.create_run(dataset_name="static_analysis_nondeterminism", artifact_limit=4)
            run_id = run["run_id"]
            with TestClient(create_app(service)) as client:
                with patch.dict("os.environ", {"RIGHTAPI_API_KEY": "test-only-key"}):
                    runtime = client.get("/api/runtime").json()
                    self.assertTrue(runtime["api_key_available"])
                    self.assertNotIn("test-only-key", json.dumps(runtime))
                service._processing_runs.add(run_id)
                self.assertTrue(client.get(f"/api/runs/{run_id}/execution").json()["processing_active"])
                service._processing_runs.discard(run_id)
                with patch.object(service, "process_automatic", return_value={"ok": True}) as process:
                    response = client.post(f"/api/runs/{run_id}/process-automatic?language=zh&max_artifacts=1")
                    self.assertEqual(response.status_code, 200)
                    process.assert_called_once_with(run_id, language="zh", max_artifacts=1)

    def test_provider_connection_retries_are_distinct_from_semantic_retries(self) -> None:
        completions = SimpleNamespace(create=None)
        calls = []

        def create(**_kwargs):
            calls.append(1)
            if len(calls) <= 6:
                raise ConnectionError("Temporary transport loss")
            return SimpleNamespace(
                choices=[SimpleNamespace(message=SimpleNamespace(content='{"ok":true}'), finish_reason="stop")],
                usage=None, model="fake",
            )

        completions.create = create
        backend = OpenAIChatBackend(client_factory=lambda **_kwargs: SimpleNamespace(chat=SimpleNamespace(completions=completions)))
        with patch.dict("os.environ", {"CODA_TEST_KEY": "test-only-key"}):
            result = backend.generate(
                messages=[LLMMessage(role="user", content="test")],
                config=LLMModelConfig(model="fake", provider="custom", api_key_env="CODA_TEST_KEY",
                                      max_retries=0, retry_timeouts_forever=True),
            )
        self.assertEqual(result.attempt_count, 7)
        self.assertEqual(len(result.retry_errors), 6)
        self.assertFalse(OpenAIChatBackend._is_retryable_transport_error(ValueError("Wrong JSON")))


if __name__ == "__main__":
    unittest.main()
