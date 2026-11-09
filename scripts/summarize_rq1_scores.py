"""Validate and summarize independent RQ1 score rows."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from coda.evaluation import EvaluationError, summarize_rq1_scores
from coda.study import verify_formal_run_matrix, StudyManifestError
from coda.evaluator import validate_frozen_selection


def _read_rows(path: Path) -> list[dict[str, object]]:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".jsonl":
        rows = [json.loads(line) for line in text.splitlines() if line.strip()]
    else:
        payload = json.loads(text)
        rows = payload.get("scores", payload) if isinstance(payload, dict) else payload
    if not isinstance(rows, list) or not all(isinstance(row, dict) for row in rows):
        raise EvaluationError("Score input must be a JSON array or an object with a scores array.")
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scores", type=Path, help="JSON or JSONL score rows")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--bootstrap-replicates", type=int, default=2000)
    parser.add_argument("--seed", type=int, default=20260907)
    parser.add_argument("--packet", type=Path, action="append", help="Frozen formal packet; repeat per run.")
    parser.add_argument("--exploratory", action="store_true")
    parser.add_argument("--selection", type=Path, help="Frozen calibration selection")
    parser.add_argument("--human-fallback", action="store_true", help="Two independent human raters after insufficient qualifying models")
    parser.add_argument("--partial-summary", action="store_true", help="Report a subset or sensitivity runs; not the complete paper study")
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
        if not args.exploratory and not args.partial_summary:
            try:
                verify_formal_run_matrix(packets)
            except StudyManifestError as error:
                parser.error(str(error))
    selected_models = None
    if not args.exploratory:
        if not args.selection:
            parser.error("Provide --selection for formal aggregation.")
        selection = json.loads(args.selection.read_text())
        for packet in (packets or {}).values():
            validate_frozen_selection(selection, packet=packet, human_fallback=args.human_fallback)
        if args.human_fallback:
            if (selection.get("selection_status") != "independent_human_evaluation_required"
                    or not selection.get("complete_study_scope")
                    or not selection.get("study_materials_verification", {}).get("verified")):
                parser.error("Human fallback requires completed, study-bound calibration with insufficient qualifying models.")
        elif not selection.get("selection_frozen"):
            parser.error("Three-model selection is not frozen; use independent human evaluation.")
        else:
            selected_models = selection.get("selected_candidate_models", [])
    result = summarize_rq1_scores(
        _read_rows(args.scores),
        agreement_replicates=args.bootstrap_replicates,
        agreement_seed=args.seed,
        materials_by_run=packets,
        selected_evaluator_models=selected_models,
        human_fallback=args.human_fallback,
    )
    result["complete_paper_study"] = not args.exploratory and not args.partial_summary
    encoded = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded + "\n", encoding="utf-8")
        print(json.dumps({"output": str(args.output), "format": result["format"]}, ensure_ascii=False))
    else:
        print(encoded)


if __name__ == "__main__":
    main()
