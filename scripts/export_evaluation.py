"""Export offline RQ1 materials or RQ2 metrics from a frozen CODA run."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from adapters import (
    CommonSenseViolatingBugAdapter,
    CppOopRelatedFeatureAdapter,
    Defects4CodeLLMSemanticAdapter,
    Defects4CodeLLMSyntacticAdapter,
    DockerfileFlakinessAdapter,
    FairnessApiIssueTopicAdapter,
    MLSATD23ShadesAdapter,
    PersonalDataProtectionGitHubAdapter,
    QuantumClassicalIssueAdapter,
    StaticAnalysisNondeterminismAdapter,
)
from coda.evaluation import (
    EvaluationError,
    export_held_out_materials,
    export_rq1_materials,
    export_rq2_metrics,
    summarize_held_out_packet_scores,
    summarize_rq2_runs,
)


ADAPTERS = {
    "common_sense_violating_bug": CommonSenseViolatingBugAdapter,
    "cpp_oop_related_feature": CppOopRelatedFeatureAdapter,
    "defects4codellm_semantic": Defects4CodeLLMSemanticAdapter,
    "defects4codellm_syntactic": Defects4CodeLLMSyntacticAdapter,
    "llm_code_error_semantic": Defects4CodeLLMSemanticAdapter,
    "llm_code_error_syntactic": Defects4CodeLLMSyntacticAdapter,
    "dockerfile_flakiness": DockerfileFlakinessAdapter,
    "fairness_api_issue_topic": FairnessApiIssueTopicAdapter,
    "ml_satd_23_shades": MLSATD23ShadesAdapter,
    "personal_data_protection_github": PersonalDataProtectionGitHubAdapter,
    "quantum_classical_issue": QuantumClassicalIssueAdapter,
    "static_analysis_nondeterminism": StaticAnalysisNondeterminismAdapter,
}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_dir", type=Path, nargs="*")
    parser.add_argument(
        "--kind",
        choices=("rq1", "rq2", "rq2-runs", "held-out", "held-out-scores"),
        required=True,
    )
    parser.add_argument("--dataset", choices=sorted(ADAPTERS))
    parser.add_argument("--output", type=Path)
    parser.add_argument("--allow-incomplete", action="store_true")
    parser.add_argument("--packet", type=Path, help="Held-out materials JSON for score validation")
    args = parser.parse_args()
    if args.kind == "rq2-runs":
        if not args.run_dir:
            parser.error("provide one or more run directories for --kind rq2-runs")
        output = args.output or Path("rq2_run_summary.json")
        result = summarize_rq2_runs(args.run_dir)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(
            json.dumps(result, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(json.dumps({"output": str(output), "format": result["format"]}, ensure_ascii=False))
        return
    if args.kind == "held-out-scores":
        if len(args.run_dir) != 1 or args.packet is None:
            parser.error(
                "provide one score file and --packet <held_out_materials.json> "
                "for --kind held-out-scores"
            )
        try:
            score_text = args.run_dir[0].read_text(encoding="utf-8")
            if args.run_dir[0].suffix.lower() == ".jsonl":
                rows = [
                    json.loads(line)
                    for line in score_text.splitlines()
                    if line.strip()
                ]
            else:
                score_payload = json.loads(score_text)
                rows = score_payload.get("scores", score_payload) if isinstance(score_payload, dict) else score_payload
            if not isinstance(rows, list) or not all(isinstance(row, dict) for row in rows):
                raise EvaluationError("Score input must be an array or an object with a scores array.")
            packet = json.loads(args.packet.read_text(encoding="utf-8"))
            if not isinstance(packet, dict):
                raise EvaluationError("Held-out packet must be a JSON object.")
            result = summarize_held_out_packet_scores(packet, rows)
        except (OSError, json.JSONDecodeError, EvaluationError) as error:
            parser.error(str(error))
        encoded = json.dumps(result, ensure_ascii=False, indent=2)
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(encoded + "\n", encoding="utf-8")
            print(json.dumps({"output": str(args.output), "format": result["format"]}, ensure_ascii=False))
        else:
            print(encoded)
        return
    if len(args.run_dir) != 1:
        parser.error("provide exactly one run directory for --kind rq1, rq2, or held-out")
    run_dir = args.run_dir[0]
    if args.kind in {"rq1", "held-out"}:
        if not args.dataset:
            parser.error("--dataset is required for --kind rq1 or held-out")
        if args.kind == "rq1":
            output = args.output or run_dir / "rq1_materials.json"
            result = export_rq1_materials(
                run_dir,
                ADAPTERS[args.dataset](),
                output,
                allow_incomplete=args.allow_incomplete,
            )
        else:
            output = args.output or run_dir / "held_out_materials.json"
            result = export_held_out_materials(
                run_dir,
                ADAPTERS[args.dataset](),
                output,
                allow_incomplete=args.allow_incomplete,
            )
    else:
        output = args.output or run_dir / "rq2_metrics.json"
        result = export_rq2_metrics(run_dir, output)
    print(json.dumps({"output": str(output), "format": result["format"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
