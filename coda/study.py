"""Frozen, reference-blind pilot/formal materials for the CODA study."""

from __future__ import annotations

import hashlib
import json
import os
import re
from dataclasses import asdict
from pathlib import Path
from typing import Any, Iterable, Mapping

from adapters.base import ArtifactRecord


class StudyManifestError(ValueError):
    """A study allocation or its evidence cannot be verified."""


_ALIASES = {
    "defects4codellm_semantic": "llm_code_error_semantic",
    "defects4codellm_syntactic": "llm_code_error_syntactic",
}
_GROUP_FIELDS = {
    "llm_code_error_semantic": ("code_errors", "task_id"),
    "llm_code_error_syntactic": ("code_errors", "task_id"),
    "ml_satd_23_shades": ("github_repository", "repo_name"),
    "personal_data_protection_github": ("github_repository", "project"),
}


def canonical_dataset(name: str) -> str:
    return _ALIASES.get(name, name)


def _digest(value: object) -> str:
    return hashlib.sha256(json.dumps(
        value, sort_keys=True, ensure_ascii=False, separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")).hexdigest()


def evidence_sha256(artifact: ArtifactRecord | dict[str, Any]) -> str:
    if isinstance(artifact, ArtifactRecord):
        fields = {
            "content": artifact.content,
            "raw_fields": artifact.raw_fields,
            "source_refs": [asdict(ref) for ref in artifact.source_refs],
        }
    else:
        fields = {key: artifact.get(key) for key in ("content", "raw_fields", "source_refs")}
    return _digest(fields)


def study_group(dataset_name: str, artifact: ArtifactRecord) -> tuple[str, str]:
    dataset = canonical_dataset(dataset_name)
    if dataset not in _GROUP_FIELDS:
        raise StudyManifestError(f"No study grouping rule for {dataset_name}.")
    family, field = _GROUP_FIELDS[dataset]

    def normalize(value: object) -> str:
        if family == "code_errors":
            task = str(value).strip().removeprefix("HumanEval/")
            if isinstance(value, bool) or not task.isdigit():
                raise StudyManifestError(f"Invalid HumanEval task for {artifact.artifact_id}.")
            return f"HumanEval/{int(task)}"
        repo = str(value).strip().lower()
        repo = re.sub(r"^https?://(?:www\.)?github\.com/", "", repo)
        repo = repo.rstrip("/").removesuffix(".git")
        if not re.fullmatch(r"[a-z0-9_.-]+/[a-z0-9_.-]+", repo):
            raise StudyManifestError(f"Invalid repository for {artifact.artifact_id}: {value!r}")
        return repo

    values = [mapping[field] for mapping in (artifact.raw_fields, artifact.metadata)
              if field in mapping and mapping[field] is not None and str(mapping[field]).strip()]
    if not values:
        raise StudyManifestError(f"Missing {field} for {artifact.artifact_id}; unsafe ID fallback refused.")
    groups = {normalize(value) for value in values}
    if len(groups) != 1:
        raise StudyManifestError(f"Conflicting {field} for {artifact.artifact_id}.")
    return family, groups.pop()


def build_study_manifest(
    datasets: Mapping[str, Iterable[ArtifactRecord]],
    *,
    study_id: str,
    pilot_group_counts: Mapping[str, int],
    seed: int = 20260907,
) -> dict[str, Any]:
    """Allocate entire tasks/repositories, never reading hidden labels.

    Requested counts concern source groups, not bootstrap artifacts. Shared
    groups selected for pilot in any view stay pilot in every dataset/view.
    """
    if not study_id.strip() or type(seed) is not int:
        raise StudyManifestError("A study ID and integer seed are required.")
    pools: dict[str, list[ArtifactRecord]] = {}
    requested = {canonical_dataset(key): value for key, value in pilot_group_counts.items()}
    for name, items in datasets.items():
        dataset = canonical_dataset(name)
        if dataset in pools:
            raise StudyManifestError(f"Duplicate dataset/view: {dataset}")
        pools[dataset] = list(items)
    if not pools or set(requested) != set(pools):
        raise StudyManifestError("Specify a pilot group count for every selected dataset.")
    rows_by_dataset: dict[str, list[dict[str, Any]]] = {}
    pilot_groups: set[tuple[str, str]] = set()
    for dataset, artifacts in pools.items():
        if not artifacts or len({item.artifact_id for item in artifacts}) != len(artifacts):
            raise StudyManifestError(f"Empty pool or duplicate artifact IDs in {dataset}.")
        rows = []
        for artifact in artifacts:
            family, group_id = study_group(dataset, artifact)
            rows.append({
                "artifact_id": artifact.artifact_id,
                "group_family": family,
                "group_id": group_id,
                "content_sha256": hashlib.sha256(artifact.content.encode("utf-8")).hexdigest(),
                "evidence_sha256": evidence_sha256(artifact),
            })
        groups = sorted({(row["group_family"], row["group_id"]) for row in rows},
                        key=lambda group: _digest([seed, *group]))
        count = requested[dataset]
        if type(count) is not int or not 0 < count < len(groups):
            raise StudyManifestError(f"Pilot count for {dataset} must leave pilot and formal groups.")
        pilot_groups.update(groups[:count])
        rows_by_dataset[dataset] = rows
    entries = {}
    for dataset, rows in rows_by_dataset.items():
        rows.sort(key=lambda row: _digest([seed, _GROUP_FIELDS[dataset][0], row["artifact_id"]]))
        for index, row in enumerate(rows):
            row["phase"] = "pilot" if (row["group_family"], row["group_id"]) in pilot_groups else "formal"
            row["order"] = index
        entries[dataset] = {"requested_pilot_groups": requested[dataset], "artifacts": rows}
    manifest = {
        "format": "coda-study-materials-manifest",
        "format_version": 1,
        "study_id": study_id,
        "seed": seed,
        "grouping_policy": "whole_humaneval_tasks_and_github_repositories",
        "datasets": entries,
        "reference_data_included": False,
    }
    manifest["manifest_sha256"] = _digest(manifest)
    validate_study_manifest(manifest)
    return manifest


def validate_study_manifest(manifest: dict[str, Any]) -> None:
    if not isinstance(manifest, dict) or manifest.get("format") != "coda-study-materials-manifest":
        raise StudyManifestError("Expected a CODA study materials manifest.")
    body = {key: value for key, value in manifest.items() if key != "manifest_sha256"}
    if manifest.get("manifest_sha256") != _digest(body):
        raise StudyManifestError("Study manifest checksum mismatch; do not edit a frozen allocation.")
    if (manifest.get("format_version") != 1 or not manifest.get("study_id")
            or type(manifest.get("seed")) is not int or manifest.get("reference_data_included") is not False):
        raise StudyManifestError("Invalid study manifest header.")
    datasets = manifest.get("datasets")
    if not isinstance(datasets, dict) or not datasets:
        raise StudyManifestError("Study manifest has no datasets.")
    phases_by_group: dict[tuple[str, str], str] = {}
    for dataset, entry in datasets.items():
        if dataset not in _GROUP_FIELDS or not isinstance(entry, dict):
            raise StudyManifestError(f"Invalid study dataset: {dataset}")
        rows = entry.get("artifacts")
        if not isinstance(rows, list) or not rows:
            raise StudyManifestError(f"No study artifacts in {dataset}.")
        seen = set()
        for index, row in enumerate(rows):
            if not isinstance(row, dict) or not isinstance(row.get("artifact_id"), str) or not row["artifact_id"]:
                raise StudyManifestError("Study rows require artifact IDs.")
            if row["artifact_id"] in seen or row.get("order") != index:
                raise StudyManifestError("Study IDs must be unique and order contiguous.")
            seen.add(row["artifact_id"])
            if row.get("phase") not in {"pilot", "formal"}:
                raise StudyManifestError("Study phase must be pilot or formal.")
            if (row.get("group_family") != _GROUP_FIELDS[dataset][0]
                    or not isinstance(row.get("group_id"), str) or not row["group_id"]):
                raise StudyManifestError("Invalid study group.")
            for field in ("content_sha256", "evidence_sha256"):
                if not isinstance(row.get(field), str) or not re.fullmatch(r"[0-9a-f]{64}", row[field]):
                    raise StudyManifestError("Invalid study evidence checksum.")
            group = (row["group_family"], row["group_id"])
            if group in phases_by_group and phases_by_group[group] != row["phase"]:
                raise StudyManifestError(f"Pilot/formal overlap in source group {group}.")
            phases_by_group[group] = row["phase"]
        if {row["phase"] for row in rows} != {"pilot", "formal"}:
            raise StudyManifestError(f"{dataset} must have both pilot and formal material.")


def load_study_manifest(path: str | Path) -> dict[str, Any]:
    try:
        manifest = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise StudyManifestError(f"Cannot read study manifest: {path}") from error
    validate_study_manifest(manifest)
    return manifest


def select_study_artifacts(
    manifest: dict[str, Any], dataset_name: str,
    artifacts: Iterable[ArtifactRecord], phase: str,
) -> list[ArtifactRecord]:
    validate_study_manifest(manifest)
    if manifest.get("evidence_profile") and os.environ.get("CODA_EVIDENCE_PROFILE") != manifest["evidence_profile"]:
        raise StudyManifestError(f"Set CODA_EVIDENCE_PROFILE={manifest['evidence_profile']} before loading this evidence version.")
    if phase not in {"pilot", "formal"}:
        raise StudyManifestError("Study phase must be pilot or formal.")
    dataset = canonical_dataset(dataset_name)
    entry = manifest["datasets"].get(dataset)
    if entry is None:
        raise StudyManifestError(f"Dataset {dataset_name} is not in the study manifest.")
    available = {}
    for artifact in artifacts:
        if artifact.artifact_id in available:
            raise StudyManifestError("Duplicate adapter artifact IDs.")
        available[artifact.artifact_id] = artifact
    selected = []
    # Verify both allocations, so changed pilot evidence cannot be hidden by
    # starting a formal run (and vice versa).
    for row in entry["artifacts"]:
        artifact = available.get(row["artifact_id"])
        if artifact is None:
            raise StudyManifestError(f"Study material missing: {row['artifact_id']}")
        if (study_group(dataset, artifact) != (row["group_family"], row["group_id"])
                or evidence_sha256(artifact) != row["evidence_sha256"]
                or hashlib.sha256(artifact.content.encode("utf-8")).hexdigest() != row["content_sha256"]):
            raise StudyManifestError(f"Study evidence changed: {dataset}/{row['artifact_id']}")
        if row["phase"] == phase:
            selected.append(artifact)
    return selected


def study_binding(manifest: dict[str, Any], dataset_name: str, phase: str) -> dict[str, Any]:
    validate_study_manifest(manifest)
    dataset = canonical_dataset(dataset_name)
    if phase not in {"pilot", "formal"} or dataset not in manifest["datasets"]:
        raise StudyManifestError("Invalid study binding dataset/phase.")
    return {
        "study_id": manifest["study_id"],
        "manifest_sha256": manifest["manifest_sha256"],
        "dataset_name": dataset,
        "phase": phase,
        "artifact_ids": [row["artifact_id"] for row in manifest["datasets"][dataset]["artifacts"]
                         if row["phase"] == phase],
    }


def validate_study_packet(packet: dict[str, Any], phase: str) -> dict[str, Any]:
    """Verify an entire frozen evaluation packet before any LLM calls."""
    manifest = packet.get("study_manifest")
    validate_study_manifest(manifest)
    expected = study_binding(manifest, str(packet.get("dataset_name")), phase)
    if packet.get("study_materials") != expected:
        raise StudyManifestError("Evaluation phase/allocation differs from the frozen study binding.")
    rows = [row for row in manifest["datasets"][expected["dataset_name"]]["artifacts"]
            if row["phase"] == phase]
    artifacts = packet.get("artifacts")
    sensitivity = packet.get("sensitivity_protocol")
    if sensitivity:
        ids = sensitivity.get("artifact_ids", [])
        if (phase != "formal" or len(ids) != 50 or len(set(ids)) != 50
                or not set(ids) <= set(expected["artifact_ids"])
                or sensitivity.get("initialization_artifact_ids") != ids[:10]
                or not sensitivity.get("protocol_sha256")
                or len(set(sensitivity.get("evaluator_models", []))) != 3
                or packet.get("review_policy", {}).get("setting") != "automatic"):
            raise StudyManifestError("Invalid frozen sensitivity subset/protocol.")
        by_id = {row["artifact_id"]: row for row in rows}
        rows = [by_id[key] for key in ids]
        expected_ids = ids
    else:
        expected_ids = expected["artifact_ids"]
    if not isinstance(artifacts, list) or [item.get("artifact_id") for item in artifacts] != expected_ids:
        raise StudyManifestError("Evaluation packet must contain the exact ordered phase corpus.")
    for row, artifact in zip(rows, artifacts):
        if evidence_sha256(artifact) != row["evidence_sha256"]:
            raise StudyManifestError(f"Evaluation evidence changed: {row['artifact_id']}")
    if not packet.get("formal_evaluation_ready"):
        raise StudyManifestError("Study scoring requires frozen, complete outputs.")
    return expected


def study_manifest_summary(manifest: dict[str, Any]) -> dict[str, Any]:
    validate_study_manifest(manifest)
    counts = {}
    for dataset, entry in manifest["datasets"].items():
        counts[dataset] = {
            phase: {
                "artifacts": sum(row["phase"] == phase for row in entry["artifacts"]),
                "groups": len({row["group_id"] for row in entry["artifacts"] if row["phase"] == phase}),
            } for phase in ("pilot", "formal")
        }
    return {"study_id": manifest["study_id"], "manifest_sha256": manifest["manifest_sha256"], "datasets": counts}


def verify_study_scores(
    rows: list[dict[str, Any]], packets: Mapping[str, dict[str, Any]], phase: str,
) -> dict[str, Any]:
    """Bind human/LLM ratings to exact frozen units, with no pilot leakage."""
    if not rows:
        raise StudyManifestError("Study scoring requires nonempty ratings.")
    used_runs = {str(row.get("run_id")) for row in rows}
    if set(packets) != used_runs:
        raise StudyManifestError("Provide exactly one evaluation packet per scored run.")
    bindings = {}
    expected_units = {}
    manifest_id = None
    for run_id, packet in packets.items():
        if packet.get("run_id") != run_id:
            raise StudyManifestError("Evaluation packet run ID mismatch.")
        binding = validate_study_packet(packet, phase)
        identity = (binding["study_id"], binding["manifest_sha256"])
        if manifest_id is not None and identity != manifest_id:
            raise StudyManifestError("Scores mix different frozen study allocations.")
        manifest_id = identity
        bindings[run_id] = binding
        units = {(dimension, "codebook", None, None) for dimension in (
            "clarity", "category_boundaries", "meaningful_coverage",
        )}
        targets = scoring_assignment_targets(packet, phase)
        units.update(
            ("evidence_support", "assignment", artifact["artifact_id"], code_id)
            for artifact in packet["artifacts"]
            for code_id in targets.get(str(artifact["artifact_id"]), [])
        )
        expected_units[run_id] = units
    seen: dict[tuple[str, str], set[tuple[Any, ...]]] = {}
    for row in rows:
        run_id = str(row.get("run_id"))
        if row.get("phase") != phase:
            raise StudyManifestError("Score phase differs from the evaluation allocation.")
        if row.get("study_materials") is not None and row["study_materials"] != bindings[run_id]:
            raise StudyManifestError("Score row changes its study binding.")
        key = (run_id, str(row.get("evaluator_id")))
        unit = (row.get("dimension"), row.get("unit"), row.get("artifact_id"), row.get("code_id"))
        if unit not in expected_units[run_id] or unit in seen.setdefault(key, set()):
            raise StudyManifestError("Score duplicates a unit or refers outside the frozen output.")
        seen[key].add(unit)
    identities = {str(row.get("evaluator_id")) for row in rows}
    if set(seen) != {(run_id, evaluator) for run_id in used_runs for evaluator in identities}:
        raise StudyManifestError("Every evaluator must cover every scored run.")
    if any(units != expected_units[run_id] for (run_id, _), units in seen.items()):
        raise StudyManifestError("Each evaluator must score every requested frozen unit.")
    return {"verified": True, "phase": phase, "bindings": bindings}


def calibration_assignment_targets(packet: dict[str, Any], *, seed: int = 20260907) -> dict[str, str]:
    """Freeze one uniform target per nonempty case, independent of evaluator.

    A case-local RNG makes selection independent of file ordering/chunking.
    The full record remains visible; only the requested scoring target changes.
    """
    import random
    targets = {}
    for artifact in packet.get("artifacts", []):
        code_ids = sorted(set((artifact.get("coding_record") or {}).get("final_code_ids", [])))
        if code_ids:
            key = f"{seed}:{packet.get('run_id')}:{artifact['artifact_id']}"
            targets[str(artifact['artifact_id'])] = random.Random(key).choice(code_ids)
    return targets


def scoring_assignment_targets(packet: dict[str, Any], phase: str) -> dict[str, list[str]]:
    if phase == "pilot":
        expected = calibration_assignment_targets(packet)
        persisted = packet.get("calibration_sampling")
        if persisted is not None and (
                persisted.get("seed") != 20260907 or persisted.get("assignment_targets") != expected):
            raise StudyManifestError("Calibration assignment targets differ from the frozen sample.")
        return {key: [value] for key, value in expected.items()}
    return {str(item['artifact_id']): list((item.get('coding_record') or {}).get('final_code_ids', []))
            for item in packet.get('artifacts', [])}


def verify_formal_run_matrix(packets: Mapping[str, dict[str, Any]]) -> None:
    """A full paper summary requires three datasets, three settings, two runs."""
    from collections import Counter
    groups = Counter((packet.get("dataset_name"),
                      packet.get("review_policy", {}).get("setting"))
                     for packet in packets.values())
    datasets = {key[0] for key in groups}
    expected = {(dataset, setting) for dataset in datasets
                for setting in ("automatic", "selective", "full")}
    if len(datasets) != 3 or set(groups) != expected or any(count != 2 for count in groups.values()):
        raise StudyManifestError("Full formal summary requires 3 datasets x 3 settings x 2 distinct runs (18 packets).")
