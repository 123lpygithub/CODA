"""Taxonomy building and conversion for CLIMB."""

from __future__ import annotations

from typing import Dict, List, Optional

import pandas as pd


def build_taxonomy_level(
    items_list: List[Dict],
    level_num: int,
    generator,
    examiner,
    min_parents_ratio: float = 0.2,
    max_parents_ratio: float = 0.7,
    target_categories: Optional[int] = None,
    max_retries: int = 3,
    allow_failed_output: bool = False,
) -> Optional[List[Dict]]:
    """Build a taxonomy level using Generator/Examiner multi-agent approach."""
    n_items = len(items_list)
    if target_categories is not None:
        min_parents = max(1, target_categories)
        max_parents = max(min_parents, target_categories)
    else:
        min_parents = max(1, int(n_items * min_parents_ratio))
        max_parents = min(n_items - 1 if n_items > 1 else 1, int(n_items * max_parents_ratio))
        min_parents = min(min_parents, max_parents) if max_parents > 0 else 1

    print(f"\n🏗️  Building Level {level_num}: Grouping {n_items} canonical items")
    print(f"   Target: {min_parents}-{max_parents} parent categories")

    previous_issues = None
    previous_flawed_output = None
    is_retry_for_json = False
    last_llm_output = None

    for attempt in range(max_retries):
        print(f"\n   Attempt {attempt + 1}/{max_retries}...")
        llm_output, json_str = generator.generate_parent_level(
            child_items=items_list,
            level_name=f"Level {level_num - 1} Items",
            previous_issues=previous_issues,
            previous_flawed_output=previous_flawed_output,
            is_retry_for_json=is_retry_for_json,
        )
        is_retry_for_json = False
        if json_str:
            previous_flawed_output = json_str
        if llm_output:
            last_llm_output = llm_output
        if llm_output is None:
            print("   ❌ GeneratorAgent failed this attempt.")
            previous_issues = ["Generator Error: Failed to produce valid JSON"]
            is_retry_for_json = True
            if attempt == max_retries - 1:
                print("   ❌ Max retries reached for generator failure.")
                return None
            continue
        is_valid, validation_issues, corrected_taxonomy = examiner.examine_taxonomy(
            canonical_input_items=items_list,
            llm_output_taxonomy=llm_output,
            min_parents_expected=min_parents,
            max_parents_expected=max_parents,
        )
        previous_issues = validation_issues
        if is_valid:
            print(f"   ✅ Level {level_num} validated successfully! Generated {len(corrected_taxonomy)} parents.")
            return corrected_taxonomy
        print(f"   ⚠️  Validation failed (Attempt {attempt + 1}):")
        for issue in validation_issues:
            print(f"      - {issue}")
        if attempt == max_retries - 1:
            print("   ❌ Max retries reached for validation errors.")
            if allow_failed_output and last_llm_output:
                print("   ⚠️  Returning last LLM output despite validation failure.")
                return last_llm_output
            return None
        print("   🔄 Retrying with semantic feedback...")
    return None


def convert_taxonomy_to_tree_format(taxonomy_data: Dict) -> Dict:
    """Convert taxonomy data to nested tree structure."""
    title_to_node = {}
    level_keys = [int(k) for k in taxonomy_data if k != "0"]
    max_level = max(level_keys) if level_keys else 0
    root_node = {"name": "Root", "children": []}

    if max_level == 0:
        if "0" in taxonomy_data:
            for item in taxonomy_data["0"]["Leaf Items"]:
                root_node["children"].append({"name": item["title"], "children": []})
        return root_node

    for level in range(max_level, 0, -1):
        level_str = str(level)
        if level_str not in taxonomy_data:
            continue
        for item in taxonomy_data[level_str]:
            title = item["title"]
            node = {"name": title, "children": []}
            if level == max_level:
                root_node["children"].append(node)
            else:
                for parent_level in range(level + 1, max_level + 1):
                    parent_level_str = str(parent_level)
                    if parent_level_str in taxonomy_data:
                        for parent_item in taxonomy_data[parent_level_str]:
                            if "kids" in parent_item and title in parent_item["kids"]:
                                title_to_node[parent_item["title"]]["children"].append(node)
                                break
            title_to_node[title] = node

    if "0" in taxonomy_data:
        for item in taxonomy_data["0"]["Leaf Items"]:
            title = item["title"]
            leaf_node = {"name": title, "children": []}
            found = False
            for level_str in ["1", "2", "3"]:
                if level_str in taxonomy_data:
                    for parent_item in taxonomy_data[level_str]:
                        if "kids" in parent_item and title in parent_item["kids"]:
                            if not found:
                                title_to_node[parent_item["title"]]["children"].append(leaf_node)
                                found = True
                            break
            if not found:
                root_node["children"].append(leaf_node)
    return root_node


def get_tree_depth(node: Dict, depth: int = 0) -> int:
    """Get tree depth."""
    if not node.get("children"):
        return depth
    return max(get_tree_depth(c, depth + 1) for c in node["children"])


def convert_tree_to_taxonomy_structure(tree_root: Dict, description_map: Dict) -> Dict:
    """Convert tree structure to evaluation-compatible taxonomy_structure."""

    def build(node: Dict, layer: int) -> Dict:
        children_nodes = node.get("children", [])
        this = {
            "category": node["name"],
            "description": description_map.get(node["name"], ""),
            "layer": layer,
            "children": [],
        }
        this["children"] = [build(child, layer + 1) for child in children_nodes]
        return this

    return build(tree_root, 0)


def build_description_map(taxonomy_data: Dict) -> Dict[str, str]:
    """Build a mapping from node title to description for all levels."""
    desc_map = {}
    for item in taxonomy_data.get("0", {}).get("Leaf Items", []):
        desc_map[item["title"]] = item.get("description", "")
    for level_key, items in taxonomy_data.items():
        if level_key == "0":
            continue
        for item in items:
            desc_map[item["title"]] = item.get("description", "")
    return desc_map


def build_entry_assignments(
    df: pd.DataFrame,
    cluster2canonical_map: Dict,
    taxonomy_data: Dict,
    dataset_type: str = "generic",
    cluster_id_map: Optional[Dict] = None,
    description_map: Optional[Dict[str, str]] = None,
) -> List[Dict]:
    """Build entry-to-category assignments in evaluation-compatible format."""
    leaf_to_path = {}
    if description_map is None:
        description_map = build_description_map(taxonomy_data)
    max_level = max([int(k) for k in taxonomy_data if k != "0"], default=0)

    for leaf_item in taxonomy_data.get("0", {}).get("Leaf Items", []):
        leaf_title = leaf_item["title"]
        path_parts = []
        current_title = leaf_title
        for level_num in range(1, max_level + 1):
            level_str = str(level_num)
            if level_str in taxonomy_data:
                for parent_item in taxonomy_data[level_str]:
                    if "kids" in parent_item and current_title in parent_item["kids"]:
                        path_parts.insert(0, parent_item["title"])
                        current_title = parent_item["title"]
                        break
        path_parts.append(leaf_item["title"])
        leaf_to_path[leaf_item["title"]] = " -> ".join(path_parts)

    results = []
    for _, row in df.iterrows():
        cluster_id = row["cluster_id"]
        canonical_id = cluster_id_map[cluster_id] if cluster_id_map and cluster_id in cluster_id_map else cluster_id
        canonical_title = cluster2canonical_map[canonical_id]
        if dataset_type == "wang2025ICSE":
            document = str(row.get("task_description", ""))
        else:
            document = str(row.get("content", row.get("text", "")))
        category_path = leaf_to_path.get(canonical_title, canonical_title)
        category_description = description_map.get(canonical_title, "")
        results.append({
            "id": str(row["id"]),
            "document": document[:200] + ("..." if len(document) > 200 else ""),
            "category": category_path,
            "category_description": category_description,
        })
    return results
