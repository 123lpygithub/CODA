from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
UPSTREAM_DIR = REPO_ROOT / "SETaxo_replication" / "upstream_data"
DATASET_ROOT = REPO_ROOT / "SETaxo_replication" / "SETaxo-Replication" / "data" / "dataset"
SETTINGS_ROOT = (
    REPO_ROOT
    / "SETaxo_replication"
    / "SETaxo-Replication"
    / "methods"
    / "CLIMB"
    / "src"
    / "prompts"
    / "settings"
)

SEMANTIC_DATASET = "llm_code_error_semantic"
SYNTACTIC_DATASET = "llm_code_error_syntactic"

TRIPLE_QUOTE_PATTERN = re.compile(r"(?s)\A(.*?(?P<quote>\"\"\"|''').*?(?P=quote))")

SEMANTIC_TAXONOMY = {
    "Aa": {
        "title": "Condition Error",
        "description": "Errors in the conditions that control program behavior.",
        "children": {
            "Aa1": "Missing condition",
            "Aa2": "Incorrect condition",
        },
    },
    "Ab": {
        "title": "Constant Value Error",
        "description": "Errors caused by incorrect constant values.",
        "children": {
            "Ab1": "Constant value error",
        },
    },
    "Ac": {
        "title": "Reference Error",
        "description": "Errors involving wrong or missing references to variables or methods.",
        "children": {
            "Ac1": "Wrong method/variable",
            "Ac2": "Undefined name",
        },
    },
    "Ad": {
        "title": "Operation/Calculation Error",
        "description": "Errors in arithmetic or comparison operations.",
        "children": {
            "Ad1": "Incorrect arithmetic operation",
            "Ad4": "Incorrect comparison operation",
        },
    },
    "Ae": {
        "title": "Garbage Code",
        "description": "Generated code that is unnecessary, meaningless, or logically misdirected.",
        "children": {
            "Ae1": "Only comments",
            "Ae2": "Meaningless code snippet",
            "Ae3": "Wrong (logical) direction",
        },
    },
    "Af": {
        "title": "Incomplete Code",
        "description": "Errors caused by missing one or more required implementation steps.",
        "children": {
            "Af1": "Missing one step",
            "Af2": "Missing multiple steps",
        },
    },
    "Ag": {
        "title": "Memory Error",
        "description": "Errors related to non-terminating behavior such as infinite loops.",
        "children": {
            "Ag1": "Infinite Loop",
        },
    },
}

SYNTACTIC_TAXONOMY = {
    "Ba": {
        "title": "Conditional Error",
        "description": "Errors in conditional statement syntax.",
        "children": {
            "Ba1": "If error",
        },
    },
    "Bb": {
        "title": "Loop Error",
        "description": "Errors in loop statement syntax or construction.",
        "children": {
            "Bb1": "For error",
            "Bb2": "While error",
        },
    },
    "Bc": {
        "title": "Return Error",
        "description": "Errors in return statements or returned expressions.",
        "children": {
            "Bc2": "Incorrect return value",
        },
    },
    "Bd": {
        "title": "Method Call Error",
        "description": "Errors in function names, arguments, or call targets.",
        "children": {
            "Bd1": "Incorrect function name",
            "Bd2": "Incorrect function arguments",
            "Bd3": "Incorrect method call target",
        },
    },
    "Be": {
        "title": "Assignment Error",
        "description": "Errors in assigned expressions, constants, variables, or comparisons.",
        "children": {
            "Be1": "Incorrect arithmetic",
            "Be4": "Incorrect constant",
            "Be5": "Incorrect variable name",
            "Be6": "Incorrect comparison",
        },
    },
    "Bf": {
        "title": "Import Error",
        "description": "Errors in import statements.",
        "children": {
            "Bf1": "Import error",
        },
    },
    "Bg": {
        "title": "Code Block Error",
        "description": "Errors due to missing or malformed code blocks.",
        "children": {
            "Bg1": "Incorrect code block",
            "Bg2": "Missing code block",
        },
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Prepare Defects4CodeLLM into the How-style common dataset layout."
    )
    parser.add_argument(
        "--output-root",
        type=Path,
        default=DATASET_ROOT,
        help="Directory that will contain data/dataset/<dataset>/...",
    )
    return parser.parse_args()


def extract_task_description(code: str) -> str:
    """Approximate the HumanEval prompt from signature + docstring."""

    match = TRIPLE_QUOTE_PATTERN.match(code)
    if match:
        return match.group(1).strip()
    lines = code.splitlines()
    return "\n".join(lines[: min(len(lines), 12)]).strip()


def load_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for path in sorted(UPSTREAM_DIR.glob("defects4codellm_*_error.csv")):
        with path.open("r", encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle):
                enriched = dict(row)
                enriched["source_file"] = path.name
                rows.append(enriched)
    error_ids = [row["Error ID"] for row in rows]
    if len(error_ids) != len(set(error_ids)):
        msg = "Defects4CodeLLM Error ID values must be unique across all CSV files."
        raise ValueError(msg)
    return sorted(rows, key=lambda row: int(row["Error ID"]))


def label_to_path(label: str, taxonomy_definition: dict[str, Any]) -> str:
    code = label.split(" ", maxsplit=1)[0]
    parent_code = code[:-1]
    parent = taxonomy_definition[parent_code]["title"]
    leaf = taxonomy_definition[parent_code]["children"][code]
    return f"{parent} -> {leaf}"


def build_dataset_rows(
    rows: list[dict[str, str]],
    *,
    label_column: str,
    taxonomy_definition: dict[str, Any],
) -> list[dict[str, Any]]:
    prepared_rows: list[dict[str, Any]] = []
    for row in rows:
        prepared_rows.append(
            {
                "id": int(row["Error ID"]),
                "category": label_to_path(row[label_column], taxonomy_definition),
                "task_description": extract_task_description(
                    row["Ground Truth Code (Complete)"]
                ),
                "incorrect_code": row["Incorrect Code (Complete)"],
                "ground_truth_code": row["Ground Truth Code (Complete)"],
                "model": row["Model"],
                "task_id": int(row["Task ID"]),
                "source_file": row["source_file"],
            }
        )
    return prepared_rows


def build_taxonomy_payload(
    *,
    dataset_name: str,
    taxonomy_definition: dict[str, Any],
    source_note: str,
) -> dict[str, Any]:
    children = []
    for parent_code, parent_data in taxonomy_definition.items():
        leaf_nodes = []
        for leaf_code, leaf_title in parent_data["children"].items():
            leaf_nodes.append(
                {
                    "category": leaf_title,
                    "description": f"{leaf_title}.",
                    "layer": 2,
                    "children": [],
                }
            )
        children.append(
            {
                "category": parent_data["title"],
                "description": parent_data["description"],
                "layer": 1,
                "children": leaf_nodes,
            }
        )
    return {
        "metadata": {
            "source_dataset": dataset_name,
            "max_layers": 2,
            "source_note": source_note,
            "parent_codes": list(taxonomy_definition.keys()),
        },
        "taxonomy_structure": {
            "category": "",
            "description": "",
            "layer": 0,
            "children": children,
        },
    }


def load_settings(dataset_name: str) -> dict[str, Any]:
    path = SETTINGS_ROOT / f"{dataset_name}.json"
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def prepare_dataset(
    *,
    dataset_name: str,
    rows: list[dict[str, Any]],
    settings: dict[str, Any],
    taxonomy_payload: dict[str, Any],
    output_root: Path,
) -> None:
    dataset_dir = output_root / dataset_name
    write_json(dataset_dir / f"{dataset_name}.json", rows)
    write_json(dataset_dir / f"{dataset_name}_settings.json", settings)
    write_json(dataset_dir / f"{dataset_name}_taxonomy.json", taxonomy_payload)


def main() -> int:
    args = parse_args()
    raw_rows = load_rows()

    semantic_rows = build_dataset_rows(
        raw_rows,
        label_column="Semantic Characteristics",
        taxonomy_definition=SEMANTIC_TAXONOMY,
    )
    syntactic_rows = build_dataset_rows(
        raw_rows,
        label_column="Syntactic Characteristics",
        taxonomy_definition=SYNTACTIC_TAXONOMY,
    )

    prepare_dataset(
        dataset_name=SEMANTIC_DATASET,
        rows=semantic_rows,
        settings=load_settings(SEMANTIC_DATASET),
        taxonomy_payload=build_taxonomy_payload(
            dataset_name=SEMANTIC_DATASET,
            taxonomy_definition=SEMANTIC_TAXONOMY,
            source_note="Reconstructed from the Defects4CodeLLM paper taxonomy tables.",
        ),
        output_root=args.output_root,
    )
    prepare_dataset(
        dataset_name=SYNTACTIC_DATASET,
        rows=syntactic_rows,
        settings=load_settings(SYNTACTIC_DATASET),
        taxonomy_payload=build_taxonomy_payload(
            dataset_name=SYNTACTIC_DATASET,
            taxonomy_definition=SYNTACTIC_TAXONOMY,
            source_note="Reconstructed from the Defects4CodeLLM paper taxonomy tables.",
        ),
        output_root=args.output_root,
    )

    print(f"Prepared {SEMANTIC_DATASET}: {len(semantic_rows)} records")
    print(f"Prepared {SYNTACTIC_DATASET}: {len(syntactic_rows)} records")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
