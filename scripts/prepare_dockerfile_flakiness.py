from __future__ import annotations

import argparse
import gzip
import json
from collections import OrderedDict
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
UPSTREAM_PATH = (
    REPO_ROOT
    / "SETaxo_replication"
    / "upstream_data"
    / "docker_repo_possible_flaky_dataset.json.gz"
)
DATASET_ROOT = REPO_ROOT / "SETaxo_replication" / "SETaxo-Replication" / "data" / "dataset"
SETTINGS_PATH = (
    REPO_ROOT
    / "SETaxo_replication"
    / "SETaxo-Replication"
    / "methods"
    / "CLIMB"
    / "src"
    / "prompts"
    / "settings"
    / "dockerfile_flakiness.json"
)

DATASET_NAME = "dockerfile_flakiness"
EXCLUDED_OFF_TOPIC_GROUPS = {
    "Docker System Issues",
    "Project specific Issues",
    "Infrastructure Issues",
}
OFF_TOPIC_TOP_LEVEL = "Off-Topic Errors"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Prepare Dockerfile flakiness data into the How-style common layout."
    )
    parser.add_argument(
        "--output-root",
        type=Path,
        default=DATASET_ROOT,
        help="Directory that will contain data/dataset/<dataset>/...",
    )
    return parser.parse_args()


def load_upstream_rows() -> list[dict[str, Any]]:
    with gzip.open(UPSTREAM_PATH, "rt", encoding="utf-8") as handle:
        rows = json.load(handle)
    if not isinstance(rows, list):
        msg = f"{UPSTREAM_PATH} must contain a JSON array."
        raise TypeError(msg)
    return rows


def split_category_path(category: str) -> list[str]:
    return [part.strip() for part in category.split("->") if part.strip()]


def should_keep(parts: list[str]) -> bool:
    if len(parts) < 2:
        return True
    if parts[0] != OFF_TOPIC_TOP_LEVEL:
        return True
    return parts[1] not in EXCLUDED_OFF_TOPIC_GROUPS


def collapse_category_path(parts: list[str]) -> str:
    if not parts:
        msg = "Dockerfile category path must not be empty."
        raise ValueError(msg)
    if parts[0] == OFF_TOPIC_TOP_LEVEL:
        return OFF_TOPIC_TOP_LEVEL
    if len(parts) < 2:
        msg = f"Expected at least two layers for non-off-topic category: {parts!r}"
        raise ValueError(msg)
    return f"{parts[0]} -> {parts[1]}"


def build_dataset_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    prepared_rows: list[dict[str, Any]] = []
    next_id = 1
    for row in rows:
        category = row.get("category", "")
        parts = split_category_path(category)
        if not should_keep(parts):
            continue
        metadata = row.get("metadata") or {}
        build_error = metadata.get("error_segment") or metadata.get("error_summary") or row.get(
            "build_output", ""
        )
        prepared_rows.append(
            {
                "id": next_id,
                "category": collapse_category_path(parts),
                "dockerfile": row.get("dockerfile", ""),
                "build_error": build_error,
                "build_output": row.get("build_output", ""),
                "repo_name": row.get("repo_name", ""),
                "build_time": row.get("build_time", ""),
                "error_summary": metadata.get("error_summary", ""),
                "dockerfile_error_segment": metadata.get("dockerfile_error_segment", ""),
                "dockerfile_error_line": metadata.get("dockerfile_error_line"),
                "dockerfile_exit_code": metadata.get("dockerfile_exit_code"),
                "sources_of_error": metadata.get("sources_of_error", []),
                "stderr_line": metadata.get("stderr_line"),
                "original_category": row.get("category", ""),
            }
        )
        next_id += 1
    return prepared_rows


def build_taxonomy_payload(rows: list[dict[str, Any]]) -> dict[str, Any]:
    by_top: OrderedDict[str, OrderedDict[str, None]] = OrderedDict()
    for row in rows:
        parts = split_category_path(row["category"])
        top = parts[0]
        by_top.setdefault(top, OrderedDict())
        if len(parts) > 1:
            by_top[top].setdefault(parts[1], None)

    children = []
    for top, second_level in by_top.items():
        leaf_nodes = [
            {
                "category": name,
                "description": f"Dockerfile flakiness cases under {top.lower()} involving {name.lower()}.",
                "layer": 2,
                "children": [],
            }
            for name in second_level.keys()
        ]
        children.append(
            {
                "category": top,
                "description": f"Dockerfile flakiness cases belonging to {top.lower()}.",
                "layer": 1,
                "children": leaf_nodes,
            }
        )

    return {
        "metadata": {
            "source_dataset": DATASET_NAME,
            "source_file": str(UPSTREAM_PATH),
            "max_layers": 2,
            "top_level_category_count": len(children),
            "leaf_category_count": sum(len(node["children"]) for node in children),
            "filter_rule": (
                "Exclude Off-Topic Errors -> Docker System Issues, "
                "Project specific Issues, and Infrastructure Issues."
            ),
            "collapse_rule": (
                "Map retained non-off-topic labels to Top -> SecondLevel; "
                "map retained off-topic labels to Off-Topic Errors."
            ),
        },
        "taxonomy_structure": {
            "category": "",
            "description": "",
            "layer": 0,
            "children": children,
        },
    }


def load_settings() -> dict[str, Any]:
    with SETTINGS_PATH.open("r", encoding="utf-8") as handle:
        settings = json.load(handle)
    if not isinstance(settings, dict):
        msg = f"{SETTINGS_PATH} must contain a JSON object."
        raise TypeError(msg)
    return settings


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> None:
    args = parse_args()
    dataset_dir = args.output_root / DATASET_NAME
    rows = build_dataset_rows(load_upstream_rows())
    taxonomy = build_taxonomy_payload(rows)
    settings = load_settings()

    write_json(dataset_dir / f"{DATASET_NAME}.json", rows)
    write_json(dataset_dir / f"{DATASET_NAME}_taxonomy.json", taxonomy)
    write_json(dataset_dir / f"{DATASET_NAME}_settings.json", settings)

    print(f"Prepared {len(rows)} records into {dataset_dir}")
    print(
        "Taxonomy structure:",
        taxonomy["metadata"]["max_layers"],
        taxonomy["metadata"]["top_level_category_count"],
        taxonomy["metadata"]["leaf_category_count"],
    )


if __name__ == "__main__":
    main()
