"""Single-owner API driver that monitors and resumes a persisted CODA run."""

from __future__ import annotations

from concurrent.futures import Future
from datetime import datetime, timezone
import json
from pathlib import Path
from threading import Event, Thread
import time
from typing import Any, Callable
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlparse
from urllib.request import Request, urlopen


TERMINAL = {"completed", "completed_with_unresolved", "stabilized"}
REVIEW_STATES = {"awaiting_initial_review", "awaiting_human_review", "awaiting_final_review", "awaiting_context"}


class WatchdogError(RuntimeError):
    pass


class APIRequestError(WatchdogError):
    def __init__(self, message: str, *, transient: bool = False) -> None:
        super().__init__(message)
        self.transient = transient


def transient_failure(message: str) -> bool:
    text = message.lower()
    return any(token in text for token in (
        "timeout", "timed out", "apiconnectionerror", "connection error",
        "connection reset", "connection refused", "bad gateway", "service unavailable",
        "error code: 502", "error code: 503", "error code: 504", "error code: 524",
    ))


class LocalAPIClient:
    def __init__(self, base_url: str) -> None:
        parsed = urlparse(base_url)
        if parsed.scheme != "http" or parsed.hostname not in {"127.0.0.1", "localhost", "::1"}:
            raise WatchdogError("The watchdog supports a local HTTP CODA backend only.")
        self.base_url = base_url.rstrip("/")

    def request(self, method: str, path: str, payload: dict | None = None, *, timeout: float = 10) -> dict:
        data = json.dumps(payload).encode("utf-8") if payload is not None else None
        request = Request(self.base_url + path, data=data, method=method,
                          headers={"Content-Type": "application/json"})
        try:
            with urlopen(request, timeout=timeout) as response:
                result = json.loads(response.read())
        except HTTPError as error:
            detail = error.read().decode("utf-8", errors="replace")[:1000]
            raise APIRequestError(f"HTTP {error.code}: {detail}", transient=(
                error.code in {408, 502, 503, 504, 524}
                or error.code == 500 and transient_failure(detail)
            )) from error
        except (URLError, TimeoutError, ConnectionError, OSError) as error:
            raise APIRequestError(f"Backend connection interrupted: {type(error).__name__}", transient=True) from error
        except (json.JSONDecodeError, UnicodeDecodeError) as error:
            raise APIRequestError("Backend returned an invalid JSON response.") from error
        if not isinstance(result, dict):
            raise APIRequestError("Expected a CODA API object response.")
        return result


def next_operation(observation: dict[str, Any], *, resume_cancelled: bool = False) -> str:
    run = observation["run"]
    if observation.get("initialization_active") or observation.get("processing_active"):
        return "busy"
    if run["status"] in TERMINAL:
        return "complete"
    if run["status"] in REVIEW_STATES:
        return "human_review"
    if run["status"] == "resource_limited":
        return "resource_limited"
    bootstrap = run.get("bootstrap_status", "not_run")
    if bootstrap == "cancelled" and not resume_cancelled:
        return "cancelled"
    if bootstrap == "failed":
        error = (run.get("bootstrap_progress") or {}).get("error", "")
        if not transient_failure(str(error)):
            return "invalid_initialization"
    if bootstrap in {"not_run", "failed", "interrupted", "running", "cancelling", "cancelled"}:
        return "initialize"
    if run.get("review_setting") == "full":
        return "human_review"
    return "process"


class RunWatchdog:
    def __init__(
        self, client: LocalAPIClient, state_path: Path, state: dict[str, Any],
        *, interval_seconds: float = 30, language: str = "zh",
        resume_cancelled: bool = False,
        log_callback: Callable[[dict[str, Any]], None] | None = None,
    ) -> None:
        if not 1 <= interval_seconds <= 60:
            raise WatchdogError("The check interval must be between 1 and 60 seconds.")
        self.client = client
        self.state_path = state_path
        self.state = state
        self.interval_seconds = interval_seconds
        self.language = language
        self.resume_cancelled = resume_cancelled
        self.log_callback = log_callback
        self.pending: Future | None = None
        self.stop_event = Event()
        self.last_progress: tuple | None = None
        self.last_progress_at = time.monotonic()
        self.last_observation: dict | None = None

    def save(self) -> None:
        self.state_path.parent.mkdir(parents=True, exist_ok=True)
        temporary = self.state_path.with_suffix(self.state_path.suffix + ".tmp")
        temporary.write_text(json.dumps(self.state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        temporary.replace(self.state_path)

    def log(self, event: str, **details: Any) -> None:
        row = {"timestamp_utc": datetime.now(timezone.utc).isoformat(),
               "event": event, "run_id": self.state["run_id"], **details}
        self.state["last_check"] = row
        self.save()
        with self.state_path.with_suffix(".jsonl").open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
        if self.log_callback:
            self.log_callback(row)

    def launch(self, operation: str) -> None:
        run_id = quote(self.state["run_id"], safe="")
        suffix = "initialize" if operation == "initialize" else "process-automatic"
        query = f"?language={self.language}" + ("&max_artifacts=1" if operation == "process" else "")
        self.pending = Future()
        future = self.pending
        self.state["last_operation"] = operation
        self.log("request_started", operation=operation)

        def request() -> None:
            try:
                result = self.client.request("POST", f"/api/runs/{run_id}/{suffix}{query}", timeout=600)
                future.set_result(result)
            except Exception as error:
                future.set_exception(error)

        # Closing the monitor must not wait for a long HTTP response. The
        # backend owns its in-flight request; the next monitor observes it.
        Thread(target=request, name="coda-watchdog-request", daemon=True).start()

    def tick(self) -> str:
        if self.pending is not None and self.pending.done():
            try:
                self.pending.result()
                self.log("request_finished", operation=self.state.get("last_operation"))
            except APIRequestError as error:
                # Another client may own the queue. Observe its live flags
                # before deciding whether a continuation is safe.
                busy_error = "already processing" in str(error) or "already initializing" in str(error)
                if not error.transient and not busy_error:
                    self.log("request_failed", error=str(error), retryable=False)
                    raise
                self.log("request_interrupted", error=str(error), retryable=True)
            finally:
                self.pending = None
        observation = self.client.request("GET", f"/api/runs/{quote(self.state['run_id'], safe='')}/execution")
        self.last_observation = observation
        run = observation["run"]
        progress = run.get("bootstrap_progress") or {}
        signature = (run["status"], run.get("reviewed_artifacts"), run.get("codebook_version"),
                     progress.get("phase"), progress.get("overall_completed"), progress.get("processed_artifacts"),
                     run.get("pending_retrospective_task_count"), observation.get("last_event"))
        if signature != self.last_progress:
            self.last_progress_at = time.monotonic()
            self.last_progress = signature
        operation = next_operation(observation, resume_cancelled=self.resume_cancelled)
        self.state["run_dir"] = run["run_dir"]
        self.state["status"] = run["status"]
        self.log(
            "check", action=operation, status=run["status"],
            bootstrap_status=run.get("bootstrap_status"),
            bootstrap_phase=progress.get("phase"),
            phase_completed=progress.get("processed_artifacts", 0),
            phase_total=progress.get("total_artifacts", 0),
            processed=run.get("reviewed_artifacts", 0), total=run.get("input_artifacts", 0),
            code_count=run.get("code_count", 0), unresolved=run.get("open_unresolved_count", 0),
            pending_reassessments=run.get("pending_retrospective_task_count", 0),
            backend_instance_id=observation.get("backend_instance_id"),
            seconds_since_progress=round(time.monotonic() - self.last_progress_at),
        )
        if operation in {"initialize", "process"} and self.pending is None:
            self.launch(operation)
        return operation

    def run(self) -> str:
        while not self.stop_event.is_set():
            try:
                operation = self.tick()
            except APIRequestError as error:
                if not error.transient:
                    raise
                self.log("backend_unavailable", error=str(error))
                operation = "offline"
            if operation in {"complete", "resource_limited", "cancelled", "invalid_initialization"}:
                self.log("monitor_finished", reason=operation)
                return operation
            self.stop_event.wait(self.interval_seconds)
        return "stopped"
