"""Offline evaluation exports and metrics for the TSE27-CODA protocol.

This module deliberately runs after a CODA run has been frozen.  It never
loads ``DatasetAdapter.load_reference_data()``: published labels and
taxonomies are evaluation-only material and must not leak into the coding
workflow or the RQ1 evaluator packet.
"""

from __future__ import annotations

from coda.completion import completion_issues

import hashlib
import json
import math
import random
import statistics
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Sequence

from adapters.base import ArtifactRecord, DatasetAdapter
from coda.study import (
    StudyManifestError, load_study_manifest, select_study_artifacts,
    study_binding, validate_study_packet,
    verify_study_scores,
)


class EvaluationError(ValueError):
    """Raised when a run cannot produce a defensible evaluation artifact."""


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise EvaluationError(f"Required file is missing: {path}")
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise EvaluationError(f"Invalid JSON in {path}") from error
    if not isinstance(payload, dict):
        raise EvaluationError(f"Expected a JSON object in {path}")
    return payload


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            payload = json.loads(line)
        except json.JSONDecodeError as error:
            raise EvaluationError(f"Invalid JSONL at {path}:{line_number}") from error
        if not isinstance(payload, dict):
            raise EvaluationError(f"Expected an object at {path}:{line_number}")
        rows.append(payload)
    return rows


def _write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    temporary.replace(path)


def _latest_by_artifact(records: Iterable[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    latest: dict[str, dict[str, Any]] = {}
    for record in records:
        artifact_id = record.get("artifact_id")
        if artifact_id is None:
            continue
        # Append-only history is ordered by creation.  Replacing the previous
        # value preserves the latest reassessment for an artifact.
        latest[str(artifact_id)] = record
    return latest


def _record_metadata(record: dict[str, Any]) -> dict[str, Any]:
    metadata = record.get("metadata", {})
    return metadata if isinstance(metadata, dict) else {}


def _selected_artifact_ids(
    checkpoint: dict[str, Any],
    manifest: dict[str, Any] | None,
) -> list[str]:
    if manifest:
        data = manifest.get("data", {})
        rows = data.get("coding_pool_artifacts", data.get("artifacts", []))
        if isinstance(rows, list):
            ids = [str(row["artifact_id"]) for row in rows if isinstance(row, dict) and row.get("artifact_id")]
            if ids:
                return ids
    metadata = checkpoint.get("metadata", {})
    ids = metadata.get("selected_artifact_ids", []) if isinstance(metadata, dict) else []
    if isinstance(ids, list) and ids:
        return [str(item) for item in ids]
    batches = checkpoint.get("coding_batches", [])
    return [
        str(artifact_id)
        for batch in batches
        if isinstance(batch, dict)
        for artifact_id in batch.get("artifact_ids", [])
    ]


def _artifact_payload(artifact: ArtifactRecord) -> dict[str, Any]:
    return {
        "artifact_id": artifact.artifact_id,
        "content": artifact.content,
        "raw_fields": dict(artifact.raw_fields),
        "source_refs": [
            {
                "kind": ref.kind,
                "value": ref.value,
                "ref_id": ref.ref_id,
                "field": ref.field,
                "locator": (
                    {
                        "start": ref.locator.start,
                        "end": ref.locator.end,
                        "line_start": ref.locator.line_start,
                        "line_end": ref.locator.line_end,
                    }
                    if ref.locator is not None
                    else None
                ),
            }
            for ref in artifact.source_refs
        ],
        "metadata": dict(artifact.metadata),
    }


def export_rq1_materials(
    run_dir: str | Path,
    adapter: DatasetAdapter,
    output_path: str | Path | None = None,
    *,
    allow_incomplete: bool = False,
) -> dict[str, Any]:
    """Export the frozen, reference-blind material needed for RQ1 scoring.

    The exported object contains the original agent-facing artifacts, the
    final codebook, the latest coding record for every artifact, and the full
    agent trace when it is available.  It intentionally does not include the
    adapter's hidden labels or taxonomy.
    """

    root = Path(run_dir)
    checkpoint = _read_json(root / "checkpoint.json")
    manifest = _read_json(root / "run_manifest.json") if (root / "run_manifest.json").exists() else None
    final_path = root / "final_codebook.json"
    if final_path.exists():
        codebook = _read_json(final_path)
    elif allow_incomplete:
        raw_codebook = checkpoint.get("codebook")
        if not isinstance(raw_codebook, dict):
            raise EvaluationError("Incomplete checkpoint has no codebook object.")
        codebook = raw_codebook
    else:
        raise EvaluationError(
            f"{root} has no final_codebook.json; freeze the run before formal RQ1 evaluation."
        )

    bootstrap_manifest = (
        _read_json(root / "bootstrap_manifest.json")
        if (root / "bootstrap_manifest.json").exists()
        else None
    )
    bootstrap_packets = _read_jsonl(root / "bootstrap_evidence_packets.jsonl")
    bootstrap_codings = _read_jsonl(root / "bootstrap_initial_codings.jsonl")
    bootstrap_assignments = _read_jsonl(root / "bootstrap_assignments.jsonl")
    selected_ids = _selected_artifact_ids(checkpoint, manifest)
    adapter_artifacts = list(adapter.iter_artifacts())
    artifacts_by_id = {
        artifact.artifact_id: _artifact_payload(artifact)
        for artifact in adapter_artifacts
    }
    study_manifest = None
    binding = checkpoint.get("metadata", {}).get("study_materials")
    if binding is not None:
        try:
            study_manifest = load_study_manifest(root / "study_manifest.json")
            expected = study_binding(study_manifest, str(checkpoint.get("dataset_name")), str(binding.get("phase")))
            selected = select_study_artifacts(
                study_manifest, str(checkpoint.get("dataset_name")), adapter_artifacts, expected["phase"],
            )
            if (binding != expected or selected_ids != [item.artifact_id for item in selected]
                    or not manifest or manifest.get("protocol", {}).get("study_materials") != binding):
                raise StudyManifestError("Run differs from the frozen study allocation or order.")
        except StudyManifestError as error:
            raise EvaluationError(str(error)) from error
    missing = [artifact_id for artifact_id in selected_ids if artifact_id not in artifacts_by_id]
    if missing:
        raise EvaluationError(
            f"The adapter cannot reconstruct {len(missing)} selected artifacts: {missing[:5]}"
        )
    # A live adapter must never silently replace the evidence used for coding.
    # This check also protects exploratory runs without a study allocation.
    from coda.study import evidence_sha256
    if manifest:
        for frozen in manifest.get("data", {}).get("artifacts", []):
            artifact_id = frozen["artifact_id"]
            if (artifact_id in artifacts_by_id and frozen.get("evidence_sha256")
                    and evidence_sha256(artifacts_by_id[artifact_id]) != frozen["evidence_sha256"]):
                raise EvaluationError(f"Source evidence changed from run manifest: {artifact_id}.")
    frozen_materials = checkpoint.get("metadata", {}).get("case_materials", {})
    for artifact_id in selected_ids:
        frozen = frozen_materials.get(artifact_id, {})
        if "content" in frozen and evidence_sha256(frozen) != evidence_sha256(artifacts_by_id[artifact_id]):
            raise EvaluationError(f"Source evidence changed after coding: {artifact_id}. Restore the frozen snapshot before export.")

    history = checkpoint.get("history", {})
    records = history.get("coding_records", []) if isinstance(history, dict) else []
    if not isinstance(records, list):
        raise EvaluationError("checkpoint.history.coding_records must be a list.")
    if binding is not None and any(
        isinstance(record, dict) and str(record.get("artifact_id")) not in selected_ids for record in records
    ):
        raise EvaluationError("Study history contains cases outside its frozen phase corpus.")
    latest_records = _latest_by_artifact(item for item in records if isinstance(item, dict))
    traces = _latest_by_artifact(_read_jsonl(root / "artifact_runs.jsonl"))
    bootstrap_packets_by_id = _latest_by_artifact(bootstrap_packets)
    bootstrap_codings_by_id = _latest_by_artifact(bootstrap_codings)
    bootstrap_assignments_by_id = _latest_by_artifact(bootstrap_assignments)
    missing_records = [
        artifact_id for artifact_id in selected_ids if artifact_id not in latest_records
    ]
    terminal_statuses = {"completed", "stabilized", "completed_with_unresolved"}
    formal_ready = (
        final_path.exists()
        and not allow_incomplete
        and checkpoint.get("status") in terminal_statuses
        and not missing_records
    )
    if not allow_incomplete and missing_records:
        raise EvaluationError(
            "Formal RQ1 export requires one latest coding record per selected artifact; "
            f"missing {len(missing_records)} records: {missing_records[:5]}"
        )
    if not allow_incomplete and checkpoint.get("status") not in terminal_statuses:
        raise EvaluationError(
            "Formal RQ1 export requires a terminal run status; "
            f"got {checkpoint.get('status')!r}."
        )
    unresolved = history.get("unresolved_cases", []) if isinstance(history, dict) else []
    pending_tasks = [
        task for task in history.get("retrospective_tasks", [])
        if isinstance(task, dict) and task.get("status", "pending") not in {"completed", "cancelled"}
    ]
    if not allow_incomplete and pending_tasks:
        raise EvaluationError("Formal RQ1 export requires completed retrospective reassessments.")
    if not allow_incomplete and codebook != checkpoint.get("codebook"):
        raise EvaluationError("The frozen codebook does not match the latest checkpoint.")
    gate_issues = completion_issues(
        checkpoint, require_approval=True,
        require_audit=True,
    )
    if gate_issues and not allow_incomplete:
        raise EvaluationError("Formal export blocked: " + " ".join(gate_issues))
    formal_ready = formal_ready and not gate_issues
    unresolved_by_artifact: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in unresolved if isinstance(unresolved, list) else []:
        if isinstance(item, dict) and item.get("artifact_id") is not None:
            unresolved_by_artifact[str(item["artifact_id"])].append(item)

    artifacts = []
    for artifact_id in selected_ids:
        artifacts.append(
            {
                **artifacts_by_id[artifact_id],
                "coding_record": latest_records.get(artifact_id),
                "agent_trace": traces.get(artifact_id),
                "bootstrap_context_packet": bootstrap_packets_by_id.get(artifact_id),
                "bootstrap_initial_coding": bootstrap_codings_by_id.get(artifact_id),
                "bootstrap_assignment": bootstrap_assignments_by_id.get(artifact_id),
                "unresolved_cases": unresolved_by_artifact.get(artifact_id, []),
            }
        )

    protocol = manifest.get("protocol", {}) if manifest else {}
    output: dict[str, Any] = {
        "format": "coda-rq1-evaluation-materials",
        "format_version": 1,
        "exported_at_utc": datetime.now(timezone.utc).isoformat(),
        "run_id": checkpoint.get("run_id"),
        "dataset_name": checkpoint.get("dataset_name"),
        "status": checkpoint.get("status"),
        "formal_evaluation_ready": formal_ready,
        "study_materials_verified": binding is not None,
        "study_materials": binding,
        "study_manifest": study_manifest,
        "study_execution": checkpoint.get("metadata", {}).get("study_execution", {}),
        "iterative_batch_protocol": checkpoint.get("metadata", {}).get("iterative_batch_protocol", {"batch_size": 1}),
        "iterative_batch_preparations": {key: {field:value for field,value in plan.items()
            if field not in {"codebook", "history"}} for key,plan in
            checkpoint.get("metadata", {}).get("iterative_batch_preparations", {}).items()},
        "sensitivity_protocol": checkpoint.get("metadata", {}).get("sensitivity_protocol"),
        "protocol": protocol,
        "research_question": checkpoint.get("research_question"),
        "analysis_protocol": checkpoint.get("analysis_protocol"),
        "review_policy": checkpoint.get("review_policy"),
        "codebook": codebook,
        "artifacts": artifacts,
        "bootstrap_manifest": bootstrap_manifest,
        "bootstrap_evidence_packets": bootstrap_packets,
        "bootstrap_initial_codings": bootstrap_codings,
        "bootstrap_assignments": bootstrap_assignments,
        "all_coding_records": records,
        "stage_reviews": history.get("stage_reviews", []) if isinstance(history, dict) else [],
        "codebook_revisions": history.get("codebook_revisions", []) if isinstance(history, dict) else [],
        "unresolved_cases": unresolved if isinstance(unresolved, list) else [],
        "reference_data_included": False,
        "missing_coding_record_artifact_ids": missing_records,
        "final_validation_audits": checkpoint.get("metadata", {}).get("final_validation_audits", {}),
        "evaluation_notes": [
            "Published reference labels and taxonomies are intentionally excluded.",
            "Evidence support must be scored per artifact-code assignment.",
            "Clarity, category boundaries, and meaningful coverage are codebook-level scores.",
        ],
    }
    if binding is not None and not allow_incomplete:
        try:
            validate_study_packet(output, binding["phase"])
        except StudyManifestError as error:
            raise EvaluationError(str(error)) from error
    from coda.study import calibration_assignment_targets
    output["calibration_sampling"] = {
        "seed": 20260907,
        "policy": "one uniform assignment per nonempty case; full record remains visible",
        "assignment_targets": calibration_assignment_targets(output),
    }
    if output_path is not None:
        _write_json(Path(output_path), output)
    return output


def _held_out_artifact_ids(
    checkpoint: dict[str, Any],
    manifest: dict[str, Any] | None,
) -> list[str]:
    if manifest:
        rows = manifest.get("data", {}).get("held_out_artifacts", [])
        if isinstance(rows, list):
            ids = [
                str(row["artifact_id"])
                for row in rows
                if isinstance(row, dict) and row.get("artifact_id")
            ]
            if ids:
                return ids
    split_manifest = checkpoint.get("split_manifest", {})
    assignments = split_manifest.get("assignments", []) if isinstance(split_manifest, dict) else []
    if isinstance(assignments, list):
        ids = [
            str(row["artifact_id"])
            for row in assignments
            if isinstance(row, dict)
            and row.get("split_name") == "held_out_pool"
            and row.get("artifact_id")
        ]
        if ids:
            return ids
    return [
        str(artifact_id)
        for batch in checkpoint.get("held_out_batches", [])
        if isinstance(batch, dict)
        for artifact_id in batch.get("artifact_ids", [])
    ]


def export_held_out_materials(
    run_dir: str | Path,
    adapter: DatasetAdapter,
    output_path: str | Path | None = None,
    *,
    allow_incomplete: bool = False,
) -> dict[str, Any]:
    """Export a frozen-codebook application packet without reference labels."""

    root = Path(run_dir)
    checkpoint = _read_json(root / "checkpoint.json")
    manifest = (
        _read_json(root / "run_manifest.json")
        if (root / "run_manifest.json").exists()
        else None
    )
    held_out_ids = _held_out_artifact_ids(checkpoint, manifest)
    if not held_out_ids:
        raise EvaluationError("This run has no held-out evaluation pool.")
    main_materials = export_rq1_materials(
        root,
        adapter,
        allow_incomplete=allow_incomplete,
    )
    coding_ids = {
        str(item["artifact_id"])
        for item in main_materials.get("artifacts", [])
        if isinstance(item, dict) and item.get("artifact_id")
    }
    overlap = coding_ids & set(held_out_ids)
    if overlap:
        raise EvaluationError(
            "The split is invalid because coding and held-out pools overlap: "
            f"{sorted(overlap)[:5]}"
        )
    final_path = root / "final_codebook.json"
    if final_path.exists():
        codebook = _read_json(final_path)
    elif allow_incomplete:
        raw_codebook = checkpoint.get("codebook")
        if not isinstance(raw_codebook, dict):
            raise EvaluationError("Incomplete checkpoint has no codebook object.")
        codebook = raw_codebook
    else:
        raise EvaluationError(
            "Held-out application requires final_codebook.json after the main run is frozen."
        )

    terminal_statuses = {"completed", "stabilized", "completed_with_unresolved"}
    if not allow_incomplete and checkpoint.get("status") not in terminal_statuses:
        raise EvaluationError(
            "Held-out application requires a terminal main run; "
            f"got {checkpoint.get('status')!r}."
        )
    artifacts_by_id = {
        artifact.artifact_id: _artifact_payload(artifact)
        for artifact in adapter.iter_artifacts()
    }
    missing = [artifact_id for artifact_id in held_out_ids if artifact_id not in artifacts_by_id]
    if missing:
        raise EvaluationError(
            f"The adapter cannot reconstruct {len(missing)} held-out artifacts: {missing[:5]}"
        )
    protocol = manifest.get("protocol", {}) if manifest else {}
    output: dict[str, Any] = {
        "format": "coda-held-out-application-materials",
        "format_version": 1,
        "exported_at_utc": datetime.now(timezone.utc).isoformat(),
        "run_id": checkpoint.get("run_id"),
        "dataset_name": checkpoint.get("dataset_name"),
        "main_run_status": checkpoint.get("status"),
        "codebook_version": codebook.get("version"),
        "codebook": codebook,
        "artifacts": [
            {
                **artifacts_by_id[artifact_id],
                "split_name": "held_out_pool",
            }
            for artifact_id in held_out_ids
        ],
        "protocol": protocol,
        "reference_data_included": False,
        "application_instructions": [
            "Use only the frozen codebook and the original artifact.",
            "Do not add, rename, merge, split, retire, or refine codes.",
            "Record existing code IDs, an application decision, a brief rationale, and active time.",
            "Keep these decisions separate from the CODA run; they must not update the codebook.",
        ],
        "judgment_schema": {
            "required_fields": [
                "run_id",
                "evaluator_id",
                "artifact_id",
                "decision",
                "code_ids",
                "rationale",
            ],
            "decision_values": {
                "assigned": "One or more frozen codes adequately represent the in-scope case.",
                "uncertain": "A plausible existing code may apply, but the case cannot be assigned reliably.",
                "unable_to_apply": "The in-scope case exposes a gap in the frozen codebook.",
                "out_of_scope": "The case is outside the stated analysis scope.",
            },
            "optional_fields": ["duration_seconds", "evidence_excerpt"],
            "score_file_format": "JSON array or JSON Lines; one judgment per evaluator and artifact.",
        },
        "evaluation_notes": [
            "Published reference labels and taxonomies are intentionally excluded.",
            "The held-out pool was not used for bootstrap, iterative coding, or human review.",
            "This packet is an independent applicability evaluation, not another coding round.",
        ],
    }
    if output_path is not None:
        _write_json(Path(output_path), output)
    return output


_HELD_OUT_DECISIONS = {
    "assigned",
    "uncertain",
    "unable_to_apply",
    "out_of_scope",
}


def validate_held_out_score(
    row: dict[str, Any],
    *,
    valid_code_ids: set[str] | None = None,
) -> None:
    """Validate one independent held-out application record."""

    for field in ("run_id", "evaluator_id", "artifact_id", "decision"):
        if not row.get(field):
            raise EvaluationError(f"Held-out score requires {field}.")
    decision = str(row["decision"])
    if decision not in _HELD_OUT_DECISIONS:
        raise EvaluationError(
            f"Unsupported held-out decision: {decision}. "
            f"Expected one of {sorted(_HELD_OUT_DECISIONS)}."
        )
    code_ids = row.get("code_ids", [])
    if not isinstance(code_ids, list) or any(not isinstance(code_id, str) for code_id in code_ids):
        raise EvaluationError("Held-out score code_ids must be a list of strings.")
    if len(code_ids) != len(set(code_ids)):
        raise EvaluationError("Held-out score code_ids must be unique.")
    if valid_code_ids is not None and any(code_id not in valid_code_ids for code_id in code_ids):
        raise EvaluationError("Held-out score references a code not present in the frozen codebook.")
    if decision == "assigned" and not code_ids:
        raise EvaluationError("An assigned held-out artifact requires at least one code ID.")
    if decision in {"unable_to_apply", "out_of_scope"} and code_ids:
        raise EvaluationError(
            "A codebook-gap or out-of-scope judgment cannot contain code IDs."
        )
    if not isinstance(row.get("rationale"), str) or not row["rationale"].strip():
        raise EvaluationError("Held-out score requires a non-empty rationale.")
    duration = row.get("duration_seconds")
    if duration is not None and (
        not isinstance(duration, (int, float)) or isinstance(duration, bool) or duration < 0
    ):
        raise EvaluationError("duration_seconds must be a non-negative number.")


def summarize_held_out_scores(
    rows: Iterable[dict[str, Any]],
    *,
    valid_code_ids: set[str] | None = None,
) -> dict[str, Any]:
    """Summarize applicability and agreement without using hidden labels."""

    materialized = list(rows)
    for row in materialized:
        validate_held_out_score(row, valid_code_ids=valid_code_ids)
    if not materialized:
        raise EvaluationError("At least one held-out score row is required.")

    total = len(materialized)
    decisions = Counter(str(row["decision"]) for row in materialized)
    in_scope_count = sum(
        count
        for decision, count in decisions.items()
        if decision != "out_of_scope"
    )
    durations = [
        float(row["duration_seconds"])
        for row in materialized
        if row.get("duration_seconds") is not None
    ]
    by_artifact: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in materialized:
        by_artifact[(str(row["run_id"]), str(row["artifact_id"]))].append(row)

    exact_matches = 0
    jaccard_values: list[float] = []
    decision_matches = 0
    pair_count = 0
    for artifact_rows in by_artifact.values():
        for index, left in enumerate(artifact_rows):
            left_codes = set(left.get("code_ids", []))
            for right in artifact_rows[index + 1:]:
                right_codes = set(right.get("code_ids", []))
                pair_count += 1
                exact_matches += int(left_codes == right_codes)
                union = left_codes | right_codes
                jaccard_values.append(
                    1.0 if not union else len(left_codes & right_codes) / len(union)
                )
                decision_matches += int(left["decision"] == right["decision"])

    result = {
        "format": "coda-held-out-application-summary",
        "format_version": 1,
        "row_count": total,
        "run_ids": sorted({str(row["run_id"]) for row in materialized}),
        "evaluator_ids": sorted({str(row["evaluator_id"]) for row in materialized}),
        "artifact_count": len(by_artifact),
        "decision_counts": dict(sorted(decisions.items())),
        "applicability": {
            "in_scope_count": in_scope_count,
            "assigned_rate": (
                decisions.get("assigned", 0) / in_scope_count
                if in_scope_count
                else None
            ),
            "uncertain_rate": (
                decisions.get("uncertain", 0) / in_scope_count
                if in_scope_count
                else None
            ),
            "unable_to_apply_rate": (
                decisions.get("unable_to_apply", 0) / in_scope_count
                if in_scope_count
                else None
            ),
            "out_of_scope_rate": decisions.get("out_of_scope", 0) / total,
            "mean_codes_when_assigned": (
                statistics.mean(
                    len(row.get("code_ids", []))
                    for row in materialized
                    if row["decision"] == "assigned"
                )
                if decisions.get("assigned")
                else None
            ),
        },
        "effort": {
            "timed_row_count": len(durations),
            "mean_duration_seconds": statistics.mean(durations) if durations else None,
            "median_duration_seconds": statistics.median(durations) if durations else None,
        },
        "agreement": {
            "pair_count": pair_count,
            "exact_set_agreement": exact_matches / pair_count if pair_count else None,
            "mean_code_set_jaccard": statistics.mean(jaccard_values) if jaccard_values else None,
            "decision_agreement": decision_matches / pair_count if pair_count else None,
            "note": (
                "Agreement is computed only when multiple independent evaluators "
                "scored the same run/artifact; no hidden reference labels are used."
            ),
        },
    }
    return result


def summarize_held_out_packet_scores(
    packet: dict[str, Any],
    rows: Iterable[dict[str, Any]],
) -> dict[str, Any]:
    """Check a score file against its exported packet and report completeness."""

    if packet.get("format") != "coda-held-out-application-materials":
        raise EvaluationError("Unsupported held-out application packet format.")
    run_id = str(packet.get("run_id") or "")
    artifact_rows = packet.get("artifacts", [])
    if not run_id or not isinstance(artifact_rows, list):
        raise EvaluationError("Held-out packet has no run ID or artifact list.")
    expected_ids = {
        str(item["artifact_id"])
        for item in artifact_rows
        if isinstance(item, dict) and item.get("artifact_id")
    }
    if not expected_ids:
        raise EvaluationError("Held-out packet contains no artifacts.")
    codebook = packet.get("codebook", {})
    codes = codebook.get("codes", []) if isinstance(codebook, dict) else []
    valid_code_ids = {
        str(code["code_id"])
        for code in codes
        if isinstance(code, dict)
        and code.get("code_id")
        and code.get("status", "active") == "active"
    }

    materialized = list(rows)
    seen: set[tuple[str, str]] = set()
    for row in materialized:
        validate_held_out_score(row, valid_code_ids=valid_code_ids)
        if str(row["run_id"]) != run_id:
            raise EvaluationError("Held-out score row run_id does not match the packet.")
        artifact_id = str(row["artifact_id"])
        if artifact_id not in expected_ids:
            raise EvaluationError(
                f"Score references artifact {artifact_id!r} outside the held-out packet."
            )
        key = (str(row["evaluator_id"]), artifact_id)
        if key in seen:
            raise EvaluationError(
                f"Duplicate held-out judgment for evaluator/artifact: {key}."
            )
        seen.add(key)

    summary = summarize_held_out_scores(materialized, valid_code_ids=valid_code_ids)
    evaluator_ids = sorted({str(row["evaluator_id"]) for row in materialized})
    judgments_by_evaluator: dict[str, set[str]] = defaultdict(set)
    for row in materialized:
        judgments_by_evaluator[str(row["evaluator_id"])].add(str(row["artifact_id"]))
    summary.update(
        {
            "packet_id": run_id,
            "dataset_name": packet.get("dataset_name"),
            "expected_artifact_count": len(expected_ids),
            "completion_by_evaluator": {
                evaluator_id: {
                    "completed": len(judgments_by_evaluator[evaluator_id]),
                    "expected": len(expected_ids),
                    "completion_rate": (
                        len(judgments_by_evaluator[evaluator_id]) / len(expected_ids)
                    ),
                    "missing_artifact_ids": sorted(
                        expected_ids - judgments_by_evaluator[evaluator_id]
                    ),
                }
                for evaluator_id in evaluator_ids
            },
            "reference_data_included": False,
        }
    )
    return summary


_CODEBOOK_DIMENSIONS = {
    "clarity",
    "category_boundaries",
    "meaningful_coverage",
}


def validate_rq1_score(row: dict[str, Any]) -> None:
    """Validate one independent RQ1 evaluator row."""

    if not row.get("run_id"):
        raise EvaluationError("RQ1 score requires run_id.")
    if not row.get("evaluator_id"):
        raise EvaluationError("RQ1 score requires evaluator_id.")
    dimension = row.get("dimension")
    status = row.get("status", "assessable")
    if dimension in _CODEBOOK_DIMENSIONS:
        if row.get("unit") != "codebook":
            raise EvaluationError(f"{dimension} must use unit=codebook.")
        score = row.get("score")
        if status != "assessable" or type(score) is not int or not 1 <= score <= 5:
            raise EvaluationError(f"{dimension} requires an integer score from 1 to 5.")
    elif dimension == "evidence_support":
        if row.get("unit") != "assignment":
            raise EvaluationError("evidence_support must use unit=assignment.")
        if not row.get("artifact_id") or not row.get("code_id"):
            raise EvaluationError("evidence_support requires artifact_id and code_id.")
        if status == "assessable":
            score = row.get("score")
            if type(score) is not int or score not in {0, 1, 2}:
                raise EvaluationError("evidence_support score must be 0, 1, or 2.")
        elif status != "unassessable":
            raise EvaluationError("evidence_support status must be assessable or unassessable.")
    else:
        raise EvaluationError(f"Unsupported RQ1 dimension: {dimension}")


def _summarize_rq1_dimensions(rows: Iterable[dict[str, Any]]) -> dict[str, Any]:
    by_dimension: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_dimension[str(row["dimension"])].append(row)
    summary: dict[str, Any] = {}
    for dimension, dimension_rows in by_dimension.items():
        assessable = [row["score"] for row in dimension_rows
                      if row.get("status", "assessable") == "assessable"]
        entry: dict[str, Any] = {
            "count": len(dimension_rows),
            "assessable_count": len(assessable),
            "unassessable_count": len(dimension_rows) - len(assessable),
            "unassessable_rate": (len(dimension_rows) - len(assessable)) / len(dimension_rows),
            "distribution": dict(sorted(Counter(assessable).items())),
        }
        if assessable:
            entry.update({"mean": statistics.mean(assessable),
                          "median": statistics.median(assessable)})
        if dimension == "evidence_support":
            entry["fully_supported_rate"] = (
                sum(score == 2 for score in assessable) / len(assessable)
                if assessable else None
            )
            cases: dict[tuple[str, str, str], list[int]] = defaultdict(list)
            for row in dimension_rows:
                key = (str(row["run_id"]), str(row["evaluator_id"]), str(row["artifact_id"]))
                cases.setdefault(key, [])
                if row.get("status", "assessable") == "assessable":
                    cases[key].append(row["score"])
            proportions = [sum(score == 2 for score in scores) / len(scores)
                           for scores in cases.values() if scores]
            entry["case_mean_fully_supported_rate"] = (
                statistics.mean(proportions) if proportions else None
            )
            entry["assessable_case_judgment_count"] = len(proportions)
            entry["unassessable_case_judgment_count"] = len(cases) - len(proportions)
        summary[dimension] = entry
    return summary


def summarize_rq1_scores(
    rows: Iterable[dict[str, Any]],
    *,
    agreement_replicates: int = 2000,
    agreement_seed: int = 20260907,
    materials_by_run: dict[str, dict[str, Any]] | None = None,
    selected_evaluator_models: list[str] | None = None,
    human_fallback: bool = False,
) -> dict[str, Any]:
    """Summarize independently supplied RQ1 scores without inventing scores."""

    materialized = list(rows)
    for row in materialized:
        validate_rq1_score(row)
    if human_fallback:
        if selected_evaluator_models is not None or len({row['evaluator_id'] for row in materialized}) != 2:
            raise EvaluationError("Human fallback requires exactly two independent humans and no selected LLMs.")
        if any(row.get("evaluator_kind") != "human" or row.get("candidate_model") for row in materialized):
            raise EvaluationError("Human fallback accepts independent human scoring records only.")
    isolation: dict[str, Any] = {"verified": False, "reason": "No frozen formal packets supplied."}
    if materials_by_run is not None:
        try:
            isolation = verify_study_scores(materialized, materials_by_run, "formal")
        except StudyManifestError as error:
            raise EvaluationError(str(error)) from error
    if selected_evaluator_models is not None:
        if len(set(selected_evaluator_models)) != 3:
            raise EvaluationError("Formal evaluation requires three frozen models.")
        models_by_identity = {}
        for row in materialized:
            metadata = row.get("evaluator_metadata", {})
            model = row.get("candidate_model") or metadata.get("model")
            if model not in selected_evaluator_models:
                raise EvaluationError("Scores include a model outside the frozen evaluator selection.")
            models_by_identity.setdefault(str(row["evaluator_id"]), set()).add(model)
        if len(models_by_identity) != 3 or any(len(models) != 1 for models in models_by_identity.values()) or set.union(*models_by_identity.values()) != set(selected_evaluator_models):
            raise EvaluationError("Each frozen model must have exactly one consistent evaluator identity.")
    by_run_evaluator: dict[str, dict[str, list[dict[str, Any]]]] = defaultdict(lambda: defaultdict(list))
    for row in materialized:
        by_run_evaluator[str(row["run_id"])][str(row["evaluator_id"])].append(row)
    summary = _summarize_rq1_dimensions(materialized)
    grouped: dict[tuple[str, str, str], dict[str, int]] = defaultdict(dict)
    for row in materialized:
        if row.get("status", "assessable") != "assessable":
            continue
        if not isinstance(row.get("score"), int):
            continue
        unit_id = (
            "codebook"
            if row.get("unit") == "codebook"
            else f"{row.get('artifact_id')}::{row.get('code_id')}"
        )
        grouped[(str(row["run_id"]), str(row["dimension"]), unit_id)][
            str(row["evaluator_id"])
        ] = int(row["score"])

    by_run_dimension: dict[tuple[str, str], list[tuple[int, int]]] = defaultdict(list)
    for (run_id, dimension, _), ratings in grouped.items():
        # Pairwise agreement is defined only for exactly two complete ratings
        # of the same unit. Incomplete units remain in the descriptive scores.
        if len(ratings) == 2:
            values = list(ratings.values())
            by_run_dimension[(run_id, dimension)].append((values[0], values[1]))
    agreement: dict[str, Any] = {}
    for (run_id, dimension), pairs in by_run_dimension.items():
        left = [pair[0] for pair in pairs]
        right = [pair[1] for pair in pairs]
        agreement[f"{run_id}:{dimension}"] = gwet_ac2_bootstrap(
            left,
            right,
            categories=[0, 1, 2] if dimension == "evidence_support" else list(range(1, 6)),
            replicates=agreement_replicates,
            seed=agreement_seed,
        )
    from coda.rq1_aggregation import aggregate_paper_rq1
    paper_summary = aggregate_paper_rq1(materialized, packets=materials_by_run,
                                       human_fallback=human_fallback)
    return {
        "paper_aggregation": paper_summary,
        "descriptive_dimensions_only": True,
        "format": "coda-rq1-score-summary",
        "study_materials_verification": isolation,
        "dimensions": summary,
        "by_run_evaluator": {
            run_id: {evaluator_id: _summarize_rq1_dimensions(evaluator_rows)
                     for evaluator_id, evaluator_rows in evaluator_groups.items()}
            for run_id, evaluator_groups in by_run_evaluator.items()
        },
        "agreement": agreement,
        "agreement_protocol": {
            "statistic": "Gwet AC2 with quadratic weights",
            "bootstrap": "paired item bootstrap percentile interval",
            "replicates": agreement_replicates,
            "seed": agreement_seed,
        },
    }


def _quadratic_weights(category_count: int) -> list[list[float]]:
    if category_count < 2:
        raise EvaluationError("At least two categories are required for AC2.")
    denominator = float((category_count - 1) ** 2)
    return [
        [1.0 - ((row - column) ** 2) / denominator for column in range(category_count)]
        for row in range(category_count)
    ]


def gwet_ac2(
    rater_a: Sequence[int],
    rater_b: Sequence[int],
    *,
    categories: Sequence[int] | None = None,
) -> float:
    """Compute Gwet's AC1/AC2 point estimate with quadratic weights.

    With non-identity quadratic weights this is AC2.  The implementation
    follows the two-rater agreement-matrix formulation used by ``irrCAC``;
    confidence intervals should be obtained by a pre-registered bootstrap,
    not inferred from this point estimate.
    """

    if len(rater_a) != len(rater_b) or not rater_a:
        raise EvaluationError("AC2 requires two equally sized, non-empty ratings.")
    values = list(categories) if categories is not None else sorted(set(rater_a) | set(rater_b))
    if len(values) == 1:
        return 1.0
    if len(values) < 1:
        raise EvaluationError("AC2 requires at least one observed category.")
    index = {value: position for position, value in enumerate(values)}
    if any(value not in index for value in (*rater_a, *rater_b)):
        raise EvaluationError("All ratings must occur in categories.")
    weights = _quadratic_weights(len(values))
    n = len(rater_a)
    observed = 0.0
    marginal_counts = [0] * len(values)
    for left, right in zip(rater_a, rater_b):
        left_index = index[left]
        right_index = index[right]
        observed += weights[left_index][right_index]
        marginal_counts[left_index] += 1
        marginal_counts[right_index] += 1
    p_a = observed / n
    total_ratings = 2 * n
    p_i = [count / total_ratings for count in marginal_counts]
    weight_sum = sum(sum(row) for row in weights)
    p_e = weight_sum * sum(probability * (1.0 - probability) for probability in p_i)
    p_e /= len(values) * (len(values) - 1)
    if math.isclose(p_e, 1.0):
        return 1.0 if math.isclose(p_a, 1.0) else 0.0
    return (p_a - p_e) / (1.0 - p_e)


def gwet_ac2_bootstrap(
    rater_a: Sequence[int],
    rater_b: Sequence[int],
    *,
    categories: Sequence[int] | None = None,
    replicates: int = 2000,
    seed: int = 20260907,
    confidence_level: float = 0.95,
) -> dict[str, Any]:
    """Return a reproducible paired percentile bootstrap interval for AC2."""

    if replicates < 100:
        raise EvaluationError("AC2 bootstrap requires at least 100 replicates.")
    if not 0.0 < confidence_level < 1.0:
        raise EvaluationError("confidence_level must be between 0 and 1.")
    if len(rater_a) != len(rater_b) or not rater_a:
        raise EvaluationError("AC2 bootstrap requires two equally sized, non-empty ratings.")
    point = gwet_ac2(rater_a, rater_b, categories=categories)
    rng = random.Random(seed)
    indices = list(range(len(rater_a)))
    estimates: list[float] = []
    for _ in range(replicates):
        sample = [rng.choice(indices) for _ in indices]
        estimates.append(
            gwet_ac2(
                [rater_a[index] for index in sample],
                [rater_b[index] for index in sample],
                categories=categories,
            )
        )
    estimates.sort()

    def percentile(value: float) -> float:
        position = (len(estimates) - 1) * value
        lower = math.floor(position)
        upper = math.ceil(position)
        if lower == upper:
            return estimates[lower]
        fraction = position - lower
        return estimates[lower] + fraction * (estimates[upper] - estimates[lower])

    alpha = (1.0 - confidence_level) / 2.0
    return {
        "estimate": point,
        "lower": percentile(alpha),
        "upper": percentile(1.0 - alpha),
        "confidence_level": confidence_level,
        "bootstrap_replicates": replicates,
        "bootstrap_seed": seed,
        "items": len(rater_a),
    }


def _iter_model_metadata(value: Any) -> Iterable[dict[str, Any]]:
    if isinstance(value, dict):
        # Physical calls are authoritative. Do not also count their aggregate
        # metadata or recurse through aliases and count them as fresh calls.
        calls = value.get("model_calls")
        if isinstance(calls, list):
            yield from (row for row in calls if isinstance(row, dict))
            return
        if isinstance(value.get("usage"), dict) and (
            value.get("call_id") or value.get("call_kind") == "bootstrap_supporting_call"
            or value.get("agent") or value.get("model")
        ):
            yield value
            return
        for child in value.values():
            yield from _iter_model_metadata(child)
    elif isinstance(value, list):
        for child in value:
            yield from _iter_model_metadata(child)


def _sum_model_usage(metadata_rows: Iterable[dict[str, Any]]) -> dict[str, Any]:
    unique = {}
    legacy_rows = 0
    for row in metadata_rows:
        key = row.get("call_id")
        if not key:
            # Historical traces lack identity; identical repeated structures
            # are deduplicated, but cannot establish exact physical call counts.
            legacy_rows += 1
            key = "legacy:" + hashlib.sha256(json.dumps(row, sort_keys=True, default=str).encode()).hexdigest()
        unique.setdefault(key, row)
    rows = list(unique.values())
    totals = {
        "call_identity_verified": legacy_rows == 0,
        "failed_attempt_costs_known": False,
        "logical_calls": len(rows),
        "actual_attempts": 0,
        "retry_count": 0,
        "format_retry_count": 0,
        "timeout_count": 0,
        "input_tokens": 0,
        "output_tokens": 0,
        "total_tokens": 0,
        "model_execution_seconds": 0.0,
        "estimated_cost_usd": 0.0,
        "estimated_cost_available": True,
        "models": Counter(),
    }
    for row in rows:
        usage = row.get("usage", {})
        if isinstance(usage, dict):
            totals["input_tokens"] += int(usage.get("prompt_tokens", 0) or 0)
            totals["output_tokens"] += int(usage.get("completion_tokens", 0) or 0)
            totals["total_tokens"] += int(usage.get("total_tokens", 0) or 0)
        attempts = int(row.get("attempt_count", 1) or 1)
        totals["actual_attempts"] += attempts
        totals["retry_count"] += max(0, attempts - 1)
        totals["format_retry_count"] += int(row.get("format_retry_count", 0) or 0)
        errors = row.get("retry_errors", [])
        if isinstance(errors, list):
            totals["timeout_count"] += sum(
                1
                for error in errors
                if isinstance(error, dict)
                and any(
                    token in f"{error.get('type', '')} {error.get('message', '')}".lower()
                    for token in ("timeout", "timed out", "524", "504")
                )
            )
        totals["model_execution_seconds"] += float(row.get("elapsed_seconds", 0.0) or 0.0)
        cost = row.get("estimated_cost_usd")
        if cost is None:
            totals["estimated_cost_available"] = False
        else:
            totals["estimated_cost_usd"] += float(cost)
        model = row.get("model")
        if model:
            totals["models"][str(model)] += 1
    totals["model_execution_seconds"] = round(totals["model_execution_seconds"], 3)
    totals["estimated_cost_usd"] = (
        round(totals["estimated_cost_usd"], 8)
        if totals["estimated_cost_available"]
        else None
    )
    totals["models"] = dict(sorted(totals["models"].items()))
    return totals


def _event_timestamp(event: dict[str, Any]) -> datetime | None:
    raw = event.get("timestamp_utc")
    if not isinstance(raw, str) or not raw:
        return None
    try:
        parsed = datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _lifecycle_metrics(events: Any) -> dict[str, Any]:
    """Summarize persisted run events without inventing missing timings."""

    rows = [
        event
        for event in events
        if isinstance(event, dict) and _event_timestamp(event) is not None
    ] if isinstance(events, list) else []
    rows.sort(key=lambda event: _event_timestamp(event) or datetime.min.replace(tzinfo=timezone.utc))

    def paired_elapsed(start_event: str, end_events: set[str]) -> float:
        open_started: list[datetime] = []
        total = 0.0
        for event in rows:
            timestamp = _event_timestamp(event)
            if timestamp is None:
                continue
            name = event.get("event")
            if name == start_event:
                open_started.append(timestamp)
            elif name in end_events and open_started:
                started = open_started.pop(0)
                total += max(0.0, (timestamp - started).total_seconds())
        return round(total, 3)

    waiting_starts: dict[str, list[datetime]] = defaultdict(list)
    waiting_seconds = 0.0
    for event in rows:
        timestamp = _event_timestamp(event)
        if timestamp is None:
            continue
        name = event.get("event")
        artifact_id = event.get("artifact_id")
        key = str(artifact_id) if artifact_id is not None else ""
        if name == "artifact_waiting_for_human_review" and key:
            waiting_starts[key].append(timestamp)
        elif name == "artifact_review_submitted" and key and waiting_starts[key]:
            started = waiting_starts[key].pop(0)
            waiting_seconds += max(0.0, (timestamp - started).total_seconds())

    timer_starts: dict[str, list[datetime]] = defaultdict(list)
    foreground_seconds = 0.0
    timer_event_count = 0
    for event in rows:
        timestamp = _event_timestamp(event)
        if timestamp is None:
            continue
        name = event.get("event")
        if name not in {"review_timer_resumed", "review_timer_paused"}:
            continue
        timer_event_count += 1
        scope = str(event.get("timer_scope", "unknown"))
        key = f"{scope}:{event.get('artifact_id') or ''}"
        if name == "review_timer_resumed":
            timer_starts[key].append(timestamp)
        elif timer_starts[key]:
            foreground_seconds += max(
                0.0, (timestamp - timer_starts[key].pop(0)).total_seconds()
            )

    first = _event_timestamp(rows[0]) if rows else None
    last = _event_timestamp(rows[-1]) if rows else None
    freezes = [event for event in rows if event.get("event") == "outputs_frozen"]
    frozen_at = _event_timestamp(freezes[-1]) if freezes else None
    observed_elapsed = (last - first).total_seconds() if first and last else None
    return {
        "event_count": len(rows),
        "observed_elapsed_seconds": round(max(0.0, observed_elapsed), 3)
        if observed_elapsed is not None
        else None,
        "initiation_to_freeze_seconds": round((frozen_at - first).total_seconds(), 3)
        if frozen_at and first else None,
        "bootstrap_elapsed_seconds": paired_elapsed(
            "bootstrap_started",
            {"bootstrap_finished", "bootstrap_cancelled"},
        ),
        "iterative_elapsed_seconds": paired_elapsed(
            "iterative_started",
            {"iterative_finished", "iterative_paused"},
        ),
        "human_waiting_seconds": round(waiting_seconds, 3),
        "explicit_foreground_timer_seconds": round(foreground_seconds, 3)
        if timer_event_count
        else None,
        "explicit_foreground_timer_event_count": timer_event_count,
        "timing_available": bool(rows),
    }


def _per_case_effort(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Keep artifact-level effort auditable without pooling it for inference."""

    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        artifact_id = record.get("artifact_id")
        if artifact_id is None or str(artifact_id).startswith("stage-review:"):
            continue
        grouped[str(artifact_id)].append(record)

    rows: list[dict[str, Any]] = []
    for artifact_id, artifact_records in sorted(grouped.items()):
        active_seconds = 0.0
        rework_seconds = 0.0
        human_review_count = 0
        rework_count = 0
        latest = artifact_records[-1]
        route_origins: set[str] = set()
        criteria: set[str] = set()
        for record in artifact_records:
            metadata = _record_metadata(record)
            route = metadata.get("routing_decision", {})
            if isinstance(route, dict):
                origin = route.get("review_origin")
                if origin:
                    route_origins.add(str(origin))
                details = route.get("signal_details", {})
                if isinstance(details, dict):
                    criteria.update(str(item) for item in details.get("review_criteria", []))
            if metadata.get("human_reviewed", True) is not True:
                continue
            human_review_count += 1
            seconds = float(metadata.get("duration_seconds", 0.0) or 0.0)
            active_seconds += seconds
            if metadata.get("review_origin") == "retrospective":
                rework_count += 1
                rework_seconds += seconds
        rows.append(
            {
                "artifact_id": artifact_id,
                "review_record_count": len(artifact_records),
                "human_review_count": human_review_count,
                "rework_count": rework_count,
                "active_human_seconds": round(active_seconds, 3),
                "rework_seconds": round(rework_seconds, 3),
                "latest_decision": latest.get("decision"),
                "latest_codebook_version": latest.get("codebook_version_after"),
                "route_origins": sorted(route_origins),
                "review_criteria": sorted(criteria),
            }
        )
    return rows


def _stage_workload(
    *,
    records: list[dict[str, Any]],
    stage_reviews: list[dict[str, Any]],
) -> dict[str, Any]:
    """Separate checkpoint and artifact-review workload for RQ2 reporting."""

    coding_reviews = [
        record
        for record in records
        if not str(record.get("artifact_id", "")).startswith("stage-review:")
    ]
    return {
        "initial_review": {
            "review_count": sum(1 for item in stage_reviews if item.get("kind") == "initial"),
            "active_seconds": round(
                sum(
                    float(item.get("duration_seconds", 0.0) or 0.0)
                    for item in stage_reviews
                    if item.get("kind") == "initial"
                ),
                3,
            ),
        },
        "triggered_review": {
            "review_count": sum(
                1
                for item in coding_reviews
                if _record_metadata(item).get("human_reviewed", True) is True
                and _record_metadata(item).get("review_origin") != "retrospective"
            ),
            "active_seconds": round(
                sum(
                    float(_record_metadata(item).get("duration_seconds", 0.0) or 0.0)
                    for item in coding_reviews
                    if _record_metadata(item).get("human_reviewed", True) is True
                    and _record_metadata(item).get("review_origin") != "retrospective"
                ),
                3,
            ),
        },
        "rework": {
            "review_count": sum(
                1
                for item in coding_reviews
                if _record_metadata(item).get("human_reviewed", True) is True
                and _record_metadata(item).get("review_origin") == "retrospective"
            ),
            "active_seconds": round(
                sum(
                    float(_record_metadata(item).get("duration_seconds", 0.0) or 0.0)
                    for item in coding_reviews
                    if _record_metadata(item).get("human_reviewed", True) is True
                    and _record_metadata(item).get("review_origin") == "retrospective"
                ),
                3,
            ),
        },
        "final_review": {
            "review_count": sum(1 for item in stage_reviews if item.get("kind") == "final"),
            "active_seconds": round(
                sum(
                    float(item.get("duration_seconds", 0.0) or 0.0)
                    for item in stage_reviews
                    if item.get("kind") == "final"
                ),
                3,
            ),
        },
    }


def summarize_rq2_metrics(run_dir: str | Path) -> dict[str, Any]:
    """Aggregate available timing, usage, review, and completion data."""

    root = Path(run_dir)
    checkpoint = _read_json(root / "checkpoint.json")
    history = checkpoint.get("history", {})
    if not isinstance(history, dict):
        raise EvaluationError("checkpoint.history must be an object.")
    records = [item for item in history.get("coding_records", []) if isinstance(item, dict)]
    stage_reviews = [item for item in history.get("stage_reviews", []) if isinstance(item, dict)]
    initial_seconds = sum(
        float(item.get("duration_seconds", 0.0) or 0.0)
        for item in stage_reviews
        if item.get("kind") == "initial"
    )
    final_seconds = sum(
        float(item.get("duration_seconds", 0.0) or 0.0)
        for item in stage_reviews
        if item.get("kind") == "final"
    )
    triggered_seconds = 0.0
    rework_seconds = 0.0
    for record in records:
        record_metadata = _record_metadata(record)
        if record_metadata.get("human_reviewed", True) is not True:
            continue
        seconds = float(record_metadata.get("duration_seconds", 0.0) or 0.0)
        if record_metadata.get("review_origin") == "retrospective":
            rework_seconds += seconds
        else:
            triggered_seconds += seconds

    trace_rows = _read_jsonl(root / "artifact_runs.jsonl")
    bootstrap_codings = _read_jsonl(root / "bootstrap_initial_codings.jsonl")
    supporting = _read_json(root / "bootstrap_manifest.json").get("supporting_model_calls", []) if (root / "bootstrap_manifest.json").exists() else []
    final_audits = checkpoint.get("metadata", {}).get("final_validation_audits", {})
    metadata_rows = list(_iter_model_metadata(trace_rows)) + list(_iter_model_metadata(bootstrap_codings)) + list(_iter_model_metadata(supporting)) + list(_iter_model_metadata(final_audits))
    # The append-only physical-call ledger also retains failed/refused calls
    # and human-revision checks absent from accepted artifact records.
    metadata_rows.extend(_read_jsonl(root / "model_calls.jsonl"))
    usage = _sum_model_usage(metadata_rows)

    latest = _latest_by_artifact(records)
    unresolved = history.get("unresolved_cases", [])
    open_unresolved = len({
        str(item.get("artifact_id")) for item in unresolved
        if isinstance(item, dict) and item.get("status", "open") == "open"
        and item.get("artifact_id") is not None
        and not str(item["artifact_id"]).startswith("stage-review:")
    }) if isinstance(unresolved, list) else 0
    metadata = checkpoint.get("metadata", {})
    bootstrap = metadata.get("bootstrap", {}) if isinstance(metadata, dict) else {}
    input_count = int(bootstrap.get("population_size", 0) or 0) if isinstance(bootstrap, dict) else 0
    if input_count == 0:
        input_count = sum(
            len(batch.get("artifact_ids", []))
            for batch in checkpoint.get("coding_batches", [])
            if isinstance(batch, dict)
            and isinstance(batch.get("artifact_ids", []), list)
        )
    processed = len({artifact_id for artifact_id, record in latest.items()
                     if not str(artifact_id).startswith("stage-review:")
                     and record.get("decision") not in {"reject", "request_additional_context"}})
    pending = max(0, input_count - processed)
    human_reviewed_artifacts = sum(
        1
        for record in latest.values()
        if not str(record.get("artifact_id", "")).startswith("stage-review:")
        and _record_metadata(record).get("human_reviewed", True) is True
    )
    automatic_processed_artifacts = sum(
        1
        for record in latest.values()
        if not str(record.get("artifact_id", "")).startswith("stage-review:")
        and _record_metadata(record).get("review_origin")
        in {"automatic_policy", "automatic_unresolved"}
    )
    total_human = initial_seconds + triggered_seconds + final_seconds + rework_seconds
    lifecycle = _lifecycle_metrics(
        metadata.get("events", []) if isinstance(metadata, dict) else []
    )
    experiment_protocol = (
        metadata.get("experiment_protocol", {})
        if isinstance(metadata, dict)
        else {}
    )
    if not isinstance(experiment_protocol, dict):
        experiment_protocol = {}
    per_case = _per_case_effort(records)
    processed_case_effort = [item for item in per_case
                             if item["latest_decision"] not in {"reject", "request_additional_context"}]
    stage_workload = _stage_workload(records=records, stage_reviews=stage_reviews)
    suppression_events = (
        metadata.get("retrospective_suppression_events", [])
        if isinstance(metadata, dict)
        else []
    )
    if not isinstance(suppression_events, list):
        suppression_events = []
    codebook_suppression_events = (
        metadata.get("codebook_suppression_events", [])
        if isinstance(metadata, dict)
        else []
    )
    if not isinstance(codebook_suppression_events, list):
        codebook_suppression_events = []
    held_out_count = sum(
        len(batch.get("artifact_ids", []))
        for batch in checkpoint.get("held_out_batches", [])
        if isinstance(batch, dict) and isinstance(batch.get("artifact_ids", []), list)
    )
    suppressed_affected_ids = {
        str(artifact_id)
        for event in suppression_events
        if isinstance(event, dict)
        for artifact_id in event.get("affected_artifact_ids", [])
    }
    return {
        "format": "coda-rq2-metrics",
        "format_version": 1,
        "run_id": checkpoint.get("run_id"),
        "dataset_name": checkpoint.get("dataset_name"),
        "status": checkpoint.get("status"),
        "study_materials": checkpoint.get("metadata", {}).get("study_materials"),
        "study_execution": checkpoint.get("metadata", {}).get("study_execution", {}),
        "review_setting": checkpoint.get("review_policy", {}).get("setting") if isinstance(checkpoint.get("review_policy"), dict) else None,
        "experiment_variant": experiment_protocol.get("variant", "standard"),
        "experiment_protocol": experiment_protocol,
        "held_out_enabled": held_out_count > 0,
        "held_out_artifact_count": held_out_count,
        "suppressed_codebook_change_count": len(codebook_suppression_events),
        "human_time": {
            "initial_review_seconds": round(initial_seconds, 3),
            "triggered_review_seconds": round(triggered_seconds, 3),
            "final_review_seconds": round(final_seconds, 3),
            "rework_seconds": round(rework_seconds, 3),
            "total_seconds": round(total_human, 3),
        },
        "lifecycle_time": lifecycle,
        "stage_workload": stage_workload,
        "per_case_effort": per_case,
        "per_processed_case": {
            "case_count": len(processed_case_effort),
            "mean_active_human_seconds": (
                statistics.mean(
                    float(item["active_human_seconds"]) for item in processed_case_effort
                )
                if processed_case_effort
                else None
            ),
            "median_active_human_seconds": (
                statistics.median(
                    float(item["active_human_seconds"]) for item in processed_case_effort
                )
                if processed_case_effort
                else None
            ),
            "cases_with_rework": sum(
                1 for item in processed_case_effort if int(item["rework_count"]) > 0
            ),
        },
        "llm_usage": usage,
        "completion": {
            "input_artifacts": input_count,
            "held_out_artifacts": held_out_count,
            "total_selected_artifacts": input_count + held_out_count,
            "processed_artifacts": processed,
            "pending_artifacts": pending,
            "open_unresolved_cases": open_unresolved,
            "retrospective_tasks": len(history.get("retrospective_tasks", [])),
            "retrospective_recoding_suppressed_events": len(suppression_events),
            "codebook_refinement_suppressed_events": len(
                codebook_suppression_events
            ),
            "retrospective_recoding_suppressed_affected_artifacts": len(
                suppressed_affected_ids
            ),
            "human_reviewed_artifacts": human_reviewed_artifacts,
            "automatic_processed_artifacts": automatic_processed_artifacts,
            "completion_rate": processed / input_count if input_count else None,
            "unresolved_rate": open_unresolved / input_count if input_count else None,
        },
        "limitations": [
            "Lifecycle timing uses persisted UTC event timestamps and excludes time before run creation.",
            "Recorded human active time and waiting time are reported separately; they can overlap model execution.",
            "A missing token price is reported as null rather than estimated.",
        ],
    }


_RQ2_AGGREGATE_METRICS: tuple[tuple[str, str], ...] = (
    ("human_time", "initial_review_seconds"),
    ("human_time", "triggered_review_seconds"),
    ("human_time", "final_review_seconds"),
    ("human_time", "rework_seconds"),
    ("human_time", "total_seconds"),
    ("lifecycle_time", "bootstrap_elapsed_seconds"),
    ("lifecycle_time", "iterative_elapsed_seconds"),
    ("lifecycle_time", "human_waiting_seconds"),
    ("lifecycle_time", "explicit_foreground_timer_seconds"),
    ("lifecycle_time", "explicit_foreground_timer_event_count"),
    ("lifecycle_time", "observed_elapsed_seconds"),
    ("lifecycle_time", "initiation_to_freeze_seconds"),
    ("llm_usage", "logical_calls"),
    ("llm_usage", "actual_attempts"),
    ("llm_usage", "retry_count"),
    ("llm_usage", "format_retry_count"),
    ("llm_usage", "timeout_count"),
    ("llm_usage", "input_tokens"),
    ("llm_usage", "output_tokens"),
    ("llm_usage", "total_tokens"),
    ("llm_usage", "model_execution_seconds"),
    ("llm_usage", "estimated_cost_usd"),
    ("completion", "input_artifacts"),
    ("completion", "held_out_artifacts"),
    ("completion", "total_selected_artifacts"),
    ("completion", "processed_artifacts"),
    ("completion", "pending_artifacts"),
    ("completion", "open_unresolved_cases"),
    ("completion", "retrospective_tasks"),
    ("completion", "retrospective_recoding_suppressed_events"),
    ("completion", "retrospective_recoding_suppressed_affected_artifacts"),
    ("completion", "codebook_refinement_suppressed_events"),
    ("completion", "human_reviewed_artifacts"),
    ("completion", "automatic_processed_artifacts"),
    ("completion", "completion_rate"),
    ("completion", "unresolved_rate"),
)


def _describe_numeric(values: Iterable[int | float]) -> dict[str, Any]:
    materialized = [float(value) for value in values]
    if not materialized:
        return {
            "count": 0,
            "mean": None,
            "median": None,
            "min": None,
            "max": None,
        }
    return {
        "count": len(materialized),
        "mean": round(statistics.mean(materialized), 6),
        "median": round(statistics.median(materialized), 6),
        "min": round(min(materialized), 6),
        "max": round(max(materialized), 6),
    }


def summarize_rq2_runs(run_dirs: Iterable[str | Path]) -> dict[str, Any]:
    """Aggregate descriptive RQ2 metrics across completed or partial runs.

    The input runs are never pooled as if they were artifact-level replicates.
    Each run remains visible in ``runs`` and group summaries report only
    descriptive statistics across run-level values.
    """

    run_results = [summarize_rq2_metrics(run_dir) for run_dir in run_dirs]
    if not run_results:
        raise EvaluationError("At least one run directory is required.")

    grouped: dict[tuple[str, str, str, int, str, str], list[dict[str, Any]]] = defaultdict(list)
    for result in run_results:
        key = (
            str(result.get("dataset_name") or "unknown"),
            str(result.get("review_setting") or "unknown"),
            str(result.get("experiment_variant") or "standard"),
            int(result.get("held_out_artifact_count", 0) or 0),
            str((result.get("study_materials") or {}).get("manifest_sha256", "unbound")),
            str((result.get("study_materials") or {}).get("phase", "exploratory")),
        )
        grouped[key].append(result)

    group_rows: list[dict[str, Any]] = []
    for (dataset_name, review_setting, experiment_variant, held_out_count, study_hash, study_phase), rows in sorted(grouped.items()):
        metric_summary: dict[str, dict[str, Any]] = {}
        for section, metric in _RQ2_AGGREGATE_METRICS:
            values = []
            for row in rows:
                value = row.get(section, {}).get(metric)
                if isinstance(value, (int, float)) and not isinstance(value, bool):
                    values.append(value)
            metric_summary[f"{section}.{metric}"] = _describe_numeric(values)
        for stage in ("initial_review", "triggered_review", "rework", "final_review"):
            for metric in ("review_count", "active_seconds"):
                values = [
                    row.get("stage_workload", {})
                    .get(stage, {})
                    .get(metric)
                    for row in rows
                ]
                metric_summary[f"stage_workload.{stage}.{metric}"] = _describe_numeric(
                    value
                    for value in values
                    if isinstance(value, (int, float)) and not isinstance(value, bool)
                )
        for metric in ("mean_active_human_seconds", "median_active_human_seconds", "cases_with_rework"):
            values = [
                row.get("per_processed_case", {}).get(metric)
                for row in rows
            ]
            metric_summary[f"per_processed_case.{metric}"] = _describe_numeric(
                value
                for value in values
                if isinstance(value, (int, float)) and not isinstance(value, bool)
            )
        group_rows.append(
            {
                "group_id": (
                    f"dataset={dataset_name};review_setting={review_setting};"
                    f"experiment_variant={experiment_variant};"
                    f"held_out_artifacts={held_out_count};study_manifest={study_hash};phase={study_phase}"
                ),
                "dataset_name": dataset_name,
                "review_setting": review_setting,
                "experiment_variant": experiment_variant,
                "held_out_artifact_count": held_out_count,
                "study_manifest_sha256": study_hash,
                "study_phase": study_phase,
                "run_count": len(rows),
                "run_ids": [str(row.get("run_id")) for row in rows],
                "study_execution": [row.get("study_execution", {}) for row in rows],
                "metrics": metric_summary,
            }
        )

    return {
        "format": "coda-rq2-run-summary",
        "format_version": 1,
        "run_count": len(run_results),
        "runs": run_results,
        "groups": group_rows,
        "grouping": [
            "dataset_name",
            "review_setting",
            "experiment_variant",
            "held_out_artifact_count",
            "study_manifest_sha256",
            "study_phase",
        ],
        "aggregation_protocol": {
            "unit": "run",
            "statistics": ["count", "mean", "median", "min", "max"],
            "inference": "descriptive_only",
            "note": (
                "Runs are not pooled into artifact-level observations; no "
                "significance test is computed by this exporter."
            ),
        },
    }


def export_rq2_metrics(run_dir: str | Path, output_path: str | Path | None = None) -> dict[str, Any]:
    result = summarize_rq2_metrics(run_dir)
    if output_path is not None:
        _write_json(Path(output_path), result)
    return result
