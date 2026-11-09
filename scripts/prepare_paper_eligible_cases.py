"""Prepare reference-blind, solution-level eligible cases for the CODA paper.

This does not allocate pilot groups, create runs, or modify the source datasets.
Pass the generated case list to create_study_manifest.py before formal runs.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from adapters.defects4codellm import Defects4CodeLLMSemanticAdapter
from adapters.ml_satd_23_shades import MLSATD23ShadesAdapter
from adapters.personal_data_protection_github import PersonalDataProtectionGitHubAdapter
from coda.study import evidence_sha256


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    output_dir = args.output_dir
    case_path = output_dir / "eligible_cases.json"
    audit_path = output_dir / "eligible_cases_audit.json"
    if case_path.exists() or audit_path.exists():
        parser.error("Outputs already exist; use a new directory to preserve the previous snapshot.")

    groups = {}
    for artifact in Defects4CodeLLMSemanticAdapter().iter_artifacts():
        fields = artifact.raw_fields
        key = (str(fields["task_id"]), str(fields["model"]), fields["incorrect_code"])
        groups.setdefault(key, []).append(artifact)
    representatives = []
    mappings = []
    for members in groups.values():
        members.sort(key=lambda artifact: int(artifact.artifact_id))
        representative = members[0]
        evidence = (representative.raw_fields["task_description"],
                    representative.raw_fields["ground_truth_code"])
        if any((member.raw_fields["task_description"], member.raw_fields["ground_truth_code"])
               != evidence for member in members):
            parser.error(f"Conflicting visible evidence for solution {representative.artifact_id}.")
        representatives.append(representative)
        mappings.append({
            "representative_artifact_id": representative.artifact_id,
            "source_artifact_ids": [member.artifact_id for member in members],
            "evidence_sha256": evidence_sha256(representative),
        })
    representatives.sort(key=lambda artifact: int(artifact.artifact_id))
    mappings.sort(key=lambda row: int(row["representative_artifact_id"]))
    pools = {
        "llm_code_error_semantic": representatives,
        "ml_satd_23_shades": list(MLSATD23ShadesAdapter().iter_artifacts()),
        "personal_data_protection_github": list(PersonalDataProtectionGitHubAdapter().iter_artifacts()),
    }
    case_list = {dataset: [artifact.artifact_id for artifact in artifacts]
                 for dataset, artifacts in pools.items()}
    audit = {
        "format": "coda-paper-eligible-case-audit",
        "format_version": 1,
        "reference_data_included": False,
        "code_solution_key": ["task_id", "model", "incorrect_code"],
        "representative_rule": "smallest numeric Error ID",
        "code_error_source_rows": sum(len(group) for group in groups.values()),
        "code_solution_mapping": mappings,
        "eligible_counts": {dataset: len(artifacts) for dataset, artifacts in pools.items()},
        "evidence_checksums": {
            dataset: {artifact.artifact_id: evidence_sha256(artifact) for artifact in artifacts}
            for dataset, artifacts in pools.items()
        },
        "limitations": [
            "These are eligible pools, not pilot/formal allocations or completed experiments.",
            "Privacy includes locally restored bodies/discussions when available; inspect evidence_status per case for missing sources.",
            "SATD includes fixed-revision excerpts when the selected evidence profile enables them; repeated full-comment matches are supplied as explicitly ambiguous candidate locations. Inspect source_context_status.",
            "The syntactic view is not an additional independent dataset.",
        ],
    }
    case_text = json.dumps(case_list, ensure_ascii=False, indent=2) + "\n"
    audit["eligible_cases_sha256"] = hashlib.sha256(case_text.encode("utf-8")).hexdigest()
    output_dir.mkdir(parents=True, exist_ok=True)
    case_path.write_text(case_text, encoding="utf-8")
    audit_path.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"case_list": str(case_path), "audit": str(audit_path),
                      "eligible_counts": audit["eligible_counts"],
                      "code_error_source_rows": audit["code_error_source_rows"]}, indent=2))


if __name__ == "__main__":
    main()
