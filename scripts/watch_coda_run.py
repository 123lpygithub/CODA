"""Create/resume a local CODA run and monitor it until completion or human work."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import fcntl
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from coda.run_watchdog import APIRequestError, LocalAPIClient, RunWatchdog, WatchdogError


def main() -> None:
    from dotenv import load_dotenv
    load_dotenv(ROOT / '.env', override=False, interpolate=False)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--api-url", default="http://127.0.0.1:8003")
    parser.add_argument("--dataset", default="ml_satd_23_shades")
    parser.add_argument("--review-mode", choices=("automatic", "selective", "full"), default="automatic")
    parser.add_argument("--artifact-limit", type=int)
    parser.add_argument("--iterative-batch-size", type=int, default=1)
    parser.add_argument("--run-id", help="Attach to an existing run without creating another.")
    parser.add_argument("--state", type=Path, required=True, help="Persisted monitor state; reuse to resume.")
    parser.add_argument("--interval", type=float, default=30)
    parser.add_argument("--language", choices=("en", "zh"))
    parser.add_argument("--resume-cancelled", action="store_true")
    parser.add_argument("--study-manifest", type=Path)
    parser.add_argument("--study-phase", choices=("pilot", "formal"))
    parser.add_argument("--participant-id")
    parser.add_argument("--replicate-index", type=int, choices=(1, 2))
    parser.add_argument("--comparison-block-id")
    args = parser.parse_args()
    args.state.parent.mkdir(parents=True, exist_ok=True)
    client = LocalAPIClient(args.api_url)
    with args.state.with_suffix(".lock").open("a") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            parser.error("Another monitor already owns this state file.")
        if args.state.exists():
            state = json.loads(args.state.read_text(encoding="utf-8"))
            if state.get("format") != "coda-run-watchdog" or not state.get("run_id"):
                parser.error("The monitor state has no valid persisted run ID.")
            if state.get("api_url") != args.api_url or args.run_id and state["run_id"] != args.run_id:
                parser.error("The API/run ID differs from the persisted monitor state.")
            if args.language and args.language != state.get("language"):
                parser.error("Keep the persisted language when resuming stage checkpoints.")
        else:
            runtime = client.request("GET", "/api/runtime")
            if not runtime.get("api_key_available"):
                parser.error("The backend cannot read its API key; start it in the exported-key terminal.")
            if not runtime.get("retry_timeouts_forever"):
                parser.error("Enable CODA_LLM_RETRY_TIMEOUTS_FOREVER=true on the backend before this run.")
            if (args.study_manifest is None) != (args.study_phase is None):
                parser.error("Provide both --study-manifest and --study-phase.")
            if args.run_id:
                run = client.request("GET", f"/api/runs/{args.run_id}")
            else:
                payload = {"dataset_name": args.dataset, "review_mode": args.review_mode,
                           "iterative_batch_size": args.iterative_batch_size}
                for name in ('participant_id', 'replicate_index', 'comparison_block_id'):
                    if getattr(args, name) is not None:
                        payload[name] = getattr(args, name)
                if args.artifact_limit is not None:
                    payload["artifact_limit"] = args.artifact_limit
                if args.study_manifest:
                    payload.update(study_manifest_path=str(args.study_manifest.resolve()), study_phase=args.study_phase)
                # Creation has no model calls. If its response is lost, do not
                # blindly create another task; attach with --run-id instead.
                run = client.request("POST", "/api/runs", payload, timeout=60)
            state = {"format": "coda-run-watchdog", "format_version": 1,
                     "created_at_utc": datetime.now(timezone.utc).isoformat(), "api_url": args.api_url,
                     "run_id": run["run_id"], "dataset_name": run["dataset_name"], "run_dir": run["run_dir"],
                     "review_setting": run["review_setting"], "input_artifacts": run["input_artifacts"],
                     "language": args.language or "zh", "study_materials": run.get("study_materials")}
        monitor = RunWatchdog(client, args.state, state, interval_seconds=args.interval,
                             language=state["language"], resume_cancelled=args.resume_cancelled,
                             log_callback=lambda row: print(json.dumps(row, ensure_ascii=False), flush=True))
        monitor.save()
        print(json.dumps({"run_id": state["run_id"], "run_dir": state["run_dir"],
                          "state": str(args.state), "resume": "Reuse the same --state to continue."}), flush=True)
        try:
            reason = monitor.run()
            if reason == "complete":
                from scripts.export_evaluation import ADAPTERS
                from coda.evaluation import export_rq1_materials, export_rq2_metrics
                run_dir = Path(state["run_dir"])
                export_rq1_materials(run_dir, ADAPTERS[state["dataset_name"]](), run_dir / "rq1_materials.json")
                export_rq2_metrics(run_dir, run_dir / "rq2_metrics.json")
                monitor.log("outputs_exported", rq1=str(run_dir / "rq1_materials.json"), rq2=str(run_dir / "rq2_metrics.json"))
            elif reason == "invalid_initialization":
                parser.error("Initialization failed for a non-transport reason; inspect the packet before retrying.")
        except KeyboardInterrupt:
            monitor.stop_event.set()
            monitor.log("monitor_stopped", note="No further requests will be submitted. An in-flight case may finish.")
        except (WatchdogError, ValueError, OSError) as error:
            monitor.log("monitor_failed", error=str(error))
            raise SystemExit(1) from error


if __name__ == "__main__":
    main()
