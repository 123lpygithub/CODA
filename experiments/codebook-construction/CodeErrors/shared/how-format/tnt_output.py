"""Save classification results to JSON."""

from __future__ import annotations

import json
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

from langchain_core.runnables import RunnableConfig

from taxonomy_generator.configuration import Configuration
from taxonomy_generator.hierarchy import (
    extract_category_descriptions,
    extract_category_paths,
)
from taxonomy_generator.state import State
from taxonomy_generator import usage as usage_module


def _get_actual_category_depth(
    node: Optional[Dict[str, Any]],
    depth: int = 0,
) -> int:
    """Return the deepest category layer, excluding the synthetic root."""
    if not isinstance(node, dict):
        return depth
    children = [child for child in node.get("children", []) if isinstance(child, dict)]
    if not children:
        return depth
    return max(_get_actual_category_depth(child, depth + 1) for child in children)


def _latest_categories(state: State) -> list[dict[str, Any]]:
    """Return the latest flat category list stored in the generation state."""
    if not state.clusters:
        return []
    latest = state.clusters[-1]
    if isinstance(latest, list) and latest and isinstance(latest[0], list):
        latest = latest[0]
    if isinstance(latest, dict):
        latest = [latest]
    if not isinstance(latest, list):
        return []
    return [category for category in latest if isinstance(category, dict)]


def save_results_to_json(
    state: State,
    hierarchy: Optional[Dict[str, Any]] = None,
    output_dir: Optional[Path] = None,
    config: Optional[RunnableConfig] = None,
    hierarchical_review: Any = None,
) -> Path:
    """Save classification results to JSON file."""
    if output_dir is None:
        script_dir = Path(__file__).resolve().parents[2]
        output_dir = script_dir / "results"

    output_dir.mkdir(parents=True, exist_ok=True)
    doc_id_to_path = extract_category_paths(hierarchy) if hierarchy else {}

    category_name_to_desc = {
        category["name"]: category.get("description", "")
        for category in _latest_categories(state)
        if category.get("name")
    }

    results = []
    for doc in state.documents:
        doc_id = (
            doc.id
            if hasattr(doc, "id")
            else (doc.get("id") if isinstance(doc, dict) else str(doc))
        )
        doc_content = (
            doc.content
            if hasattr(doc, "content")
            else (doc.get("content") if isinstance(doc, dict) else "")
        )
        doc_summary = (
            getattr(doc, "summary", None)
            if hasattr(doc, "summary")
            else (doc.get("summary") if isinstance(doc, dict) else None)
        )

        if doc_id in doc_id_to_path:
            category_str = " -> ".join(doc_id_to_path[doc_id])
        else:
            category_str = (
                doc.category
                if hasattr(doc, "category")
                else (doc.get("category") if isinstance(doc, dict) else "")
            )

        category_desc = (
            category_name_to_desc.get(category_str.split(" -> ")[-1], "")
            if category_str
            else ""
        )

        results.append(
            {
                "id": doc_id,
                "document": doc_content,
                "summary": doc_summary if doc_summary is not None else "",
                "category": category_str,
                "category_description": category_desc,
            }
        )

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = output_dir / f"results_{timestamp}.json"

    metadata = {}
    if config is not None:
        configuration = Configuration.from_runnable_config(config)
        configurable = config.get("configurable") or {}
        metadata = {
            "dataset": configurable.get("dataset_name"),
            "use_case": state.use_case,
            "model": configuration.model,
            "temperature": configuration.temperature,
            "seed": configuration.seed,
            "batch_size": configuration.batch_size,
            "sample_size": configuration.sample_size,
            "summary_length": configuration.summary_length,
            "explanation_length": configuration.explanation_length,
            "suggestion_length": configuration.suggestion_length,
            "max_num_category_top": configuration.max_num_category_top,
            "max_num_category_leaf": configuration.max_num_category_leaf,
            "category_name_length": configuration.category_name_length,
            "category_description_length": configuration.category_description_length,
            "max_layers": configurable.get("max_layers"),
            "actual_max_layers": _get_actual_category_depth(hierarchy),
        }

    if usage_module.execution_start_time is not None:
        metadata["execution_time_seconds"] = (
            time.time() - usage_module.execution_start_time
        )

    if usage_module.usage_stats and usage_module.usage_stats.get("api_calls", 0) > 0:
        metadata["usage"] = {
            "total_prompt_tokens": usage_module.usage_stats["total_prompt_tokens"],
            "total_completion_tokens": usage_module.usage_stats[
                "total_completion_tokens"
            ],
            "total_tokens": usage_module.usage_stats["total_tokens"],
            "total_cost_credits": usage_module.usage_stats["total_cost_credits"],
            "api_calls": usage_module.usage_stats["api_calls"],
        }

    if hierarchical_review is not None:
        metadata["hierarchical_review"] = hierarchical_review

    path_to_desc = extract_category_descriptions(hierarchy) if hierarchy else {}
    for rec in results:
        if not rec.get("category_description"):
            desc = path_to_desc.get(rec.get("category", ""))
            if desc:
                rec["category_description"] = desc

    def _prune(node: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "category": node.get("category", ""),
            "description": node.get("description", ""),
            "layer": node.get("layer", 0),
            "children": [_prune(c) for c in (node.get("children") or [])],
        }

    if hierarchy:
        metadata["taxonomy_structure"] = _prune(hierarchy)

    payload = {"metadata": metadata, "results": results}
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    return output_file
