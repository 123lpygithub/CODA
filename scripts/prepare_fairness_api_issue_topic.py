from __future__ import annotations

import argparse
import csv
import json
import re
from collections import OrderedDict
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
UPSTREAM_DIR = REPO_ROOT / "SETaxo_replication" / "upstream_data"
LABELS_PATH = UPSTREAM_DIR / "bias_issue_discussion_topics_labelled_4212_discussions.csv"
METADATA_PATH = UPSTREAM_DIR / "bias_issue_discussions_metadata_4212_discussions.csv"
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
    / "fairness_api_issue_topic.json"
)

DATASET_NAME = "fairness_api_issue_topic"
COMMENT_SUFFIX_PATTERN = re.compile(r"#issuecomment-\d+$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Prepare the latest fairness API issue-topic data into the How-style common layout."
    )
    parser.add_argument(
        "--output-root",
        type=Path,
        default=DATASET_ROOT,
        help="Directory that will contain data/dataset/<dataset>/...",
    )
    return parser.parse_args()


def load_upstream_rows() -> list[dict[str, Any]]:
    with LABELS_PATH.open("r", encoding="utf-8", newline="") as handle:
        label_rows = list(csv.DictReader(handle))
    with METADATA_PATH.open("r", encoding="utf-8", newline="") as handle:
        metadata_rows = list(csv.DictReader(handle))
    metadata_by_id = {row["id"]: row for row in metadata_rows}
    if len(label_rows) != len(metadata_rows):
        msg = "Fairness labels and metadata CSV files must have the same row count."
        raise ValueError(msg)

    prepared: list[dict[str, Any]] = []
    for label_row in label_rows:
        row_id = label_row["id"]
        metadata = metadata_by_id.get(row_id)
        if metadata is None:
            msg = f"Missing metadata row for fairness artifact id={row_id}."
            raise ValueError(msg)
        prepared.append({**label_row, "created_at": metadata.get("created_at", "")})
    return prepared


def build_base_issue_url(url: str) -> str:
    return COMMENT_SUFFIX_PATTERN.sub("", url)


def build_dataset_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    prepared_rows: list[dict[str, Any]] = []
    for row in rows:
        topic_type = row["topic_type"].strip()
        topic_label = row["topic_label"].strip()
        prepared_rows.append(
            {
                "id": int(row["id"]),
                "category": f"{topic_type} -> {topic_label}",
                "issue_content": row.get("text", ""),
                "repo_url": row.get("repo_url", ""),
                "type": row.get("type", ""),
                "url": row.get("url", ""),
                "base_issue_url": build_base_issue_url(row.get("url", "")),
                "created_at": row.get("created_at", ""),
                "dominant_topic": int(row["Dominant Topic"]),
                "correlation": float(row["Correlation"]),
                "topic_type": topic_type,
                "topic_label": topic_label,
            }
        )
    return prepared_rows


def build_taxonomy_payload(rows: list[dict[str, Any]]) -> dict[str, Any]:
    by_top: OrderedDict[str, OrderedDict[str, None]] = OrderedDict()
    for row in rows:
        top, leaf = [part.strip() for part in row["category"].split("->", maxsplit=1)]
        by_top.setdefault(top, OrderedDict())
        by_top[top].setdefault(leaf, None)

    children = []
    for top, leaves in by_top.items():
        leaf_nodes = [
            {
                "category": leaf,
                "description": f"Issue discussion topics under {top.lower()} concerning {leaf.lower()}.",
                "layer": 2,
                "children": [],
            }
            for leaf in leaves
        ]
        children.append(
            {
                "category": top,
                "description": f"Fairness API issue discussion topics related to {top.lower()}.",
                "layer": 1,
                "children": leaf_nodes,
            }
        )

    return {
        "metadata": {
            "source_dataset": DATASET_NAME,
            "source_files": [str(LABELS_PATH), str(METADATA_PATH)],
            "max_layers": 2,
            "top_level_category_count": len(children),
            "leaf_category_count": sum(len(node["children"]) for node in children),
            "conversion_note": (
                "Local How-style conversion built from the latest 4212-row upstream version "
                "dated after the 2025-06-10 repository update, not the How paper's 1946-row input."
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
    settings = json.loads(SETTINGS_PATH.read_text(encoding="utf-8"))
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
