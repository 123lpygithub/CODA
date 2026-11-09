"""Freeze grouped pilot/formal CODA materials without calling LLMs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from adapters import (
    Defects4CodeLLMSemanticAdapter, Defects4CodeLLMSyntacticAdapter,
    MLSATD23ShadesAdapter, PersonalDataProtectionGitHubAdapter,
)
from coda.manifest import write_run_manifest
from coda.study import (
    StudyManifestError, build_study_manifest, canonical_dataset,
    load_study_manifest, select_study_artifacts, study_manifest_summary,
)

ADAPTERS = {
    "llm_code_error_semantic": Defects4CodeLLMSemanticAdapter,
    "llm_code_error_syntactic": Defects4CodeLLMSyntacticAdapter,
    "ml_satd_23_shades": MLSATD23ShadesAdapter,
    "personal_data_protection_github": PersonalDataProtectionGitHubAdapter,
}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--study-id")
    parser.add_argument("--pilot-groups", action="append", metavar="DATASET=COUNT",
                        help="Choose datasets and explicit pilot task/repository counts.")
    parser.add_argument("--seed", type=int, default=20260907)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--verify", type=Path, help="Verify an existing manifest against current source data.")
    parser.add_argument("--case-list", type=Path,
                        help="Optional JSON mapping dataset names to exact eligible artifact ID arrays.")
    args = parser.parse_args()
    try:
        if args.verify:
            if args.output or args.pilot_groups or args.study_id or args.case_list:
                parser.error("--verify cannot be combined with creation arguments.")
            manifest = load_study_manifest(args.verify)
            for dataset in manifest["datasets"]:
                select_study_artifacts(manifest, dataset, ADAPTERS[dataset]().iter_artifacts(), "formal")
        else:
            if not args.study_id or not args.output or not args.pilot_groups:
                parser.error("Creation requires --study-id, --output and --pilot-groups.")
            if args.output.exists():
                parser.error("Manifest already exists; verify it or choose a new study/output path.")
            counts = {}
            for spec in args.pilot_groups:
                dataset, count = spec.rsplit("=", 1)
                dataset = canonical_dataset(dataset)
                if dataset not in ADAPTERS or dataset in counts:
                    parser.error(f"Unknown or duplicate dataset: {dataset}")
                counts[dataset] = int(count)
            case_lists = json.loads(args.case_list.read_text(encoding="utf-8")) if args.case_list else None
            if case_lists is not None:
                if not isinstance(case_lists, dict):
                    parser.error("--case-list must be an object mapping dataset names to ID arrays.")
                case_lists = {canonical_dataset(key): value for key, value in case_lists.items()}
                if set(case_lists) != set(counts):
                    parser.error("The case list must contain exactly the selected datasets.")
            pools = {}
            for dataset in counts:
                items = list(ADAPTERS[dataset]().iter_artifacts())
                if case_lists is not None:
                    ids = case_lists[dataset]
                    if not isinstance(ids, list) or not all(isinstance(item, str) for item in ids) or len(set(ids)) != len(ids):
                        parser.error(f"Case IDs for {dataset} must be a unique string array.")
                    by_id = {item.artifact_id: item for item in items}
                    if set(ids) - set(by_id):
                        parser.error(f"Case list references unavailable artifacts in {dataset}.")
                    items = [by_id[item] for item in ids]
                pools[dataset] = items
            manifest = build_study_manifest(pools, study_id=args.study_id,
                                            pilot_group_counts=counts, seed=args.seed)
            write_run_manifest(args.output, manifest)
        print(json.dumps(study_manifest_summary(manifest), ensure_ascii=False, indent=2))
    except (StudyManifestError, OSError, ValueError, KeyError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
