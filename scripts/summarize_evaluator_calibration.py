"""Summarize pilot human/LLM evaluator calibration."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from coda.evaluator import CalibrationConfig, calibrate_evaluators


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scores", type=Path, help="Pilot calibration JSON or JSONL")
    parser.add_argument("--candidate-model", action="append", required=True)
    parser.add_argument("--human-evaluator", action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--bootstrap-replicates", type=int, default=2000)
    parser.add_argument("--seed", type=int, default=20260907)
    parser.add_argument("--packet", type=Path, action="append", help="Frozen pilot packet; repeat per run.")
    parser.add_argument("--exploratory", action="store_true")
    args = parser.parse_args()
    if not args.packet and not args.exploratory:
        parser.error("Provide --packet for each scored run, or explicitly use --exploratory.")
    packets = None
    if args.packet:
        packets = {}
        for path in args.packet:
            packet = json.loads(path.read_text(encoding="utf-8"))
            run_id = packet.get("run_id")
            if not run_id or run_id in packets:
                parser.error("Each --packet must identify a unique run.")
            packets[run_id] = packet
    if args.scores.suffix.lower() == ".jsonl":
        rows = [json.loads(line) for line in args.scores.read_text(encoding="utf-8").splitlines() if line.strip()]
    else:
        payload = json.loads(args.scores.read_text(encoding="utf-8"))
        rows = payload.get("scores", payload) if isinstance(payload, dict) else payload
    result = calibrate_evaluators(
        rows,
        candidate_models=args.candidate_model,
        human_evaluator_ids=args.human_evaluator,
        config=CalibrationConfig(
            bootstrap_replicates=args.bootstrap_replicates,
            bootstrap_seed=args.seed,
        ),
        materials_by_run=packets,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), "selected_candidate_models": result["selected_candidate_models"], "selection_status": result["selection_status"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
