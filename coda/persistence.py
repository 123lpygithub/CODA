from __future__ import annotations

import json
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any

from adapters.base import DatasetMetadata
from coda.contracts import HumanReviewOutput
from coda.orchestrator import ArtifactRunResult
from coda.state import (
    AnalysisProtocolState,
    ArtifactBatchState,
    CodeState,
    CodebookChangeState,
    CodebookState,
    ContextRequestState,
    CodingRecordState,
    HistoryState,
    ReviewPolicyState,
    RetrospectiveRecodingTask,
    ResearchQuestionState,
    RunState,
    StabilizationCheckState,
    StageReviewState,
    UnresolvedCaseState,
)

_CHECKPOINT_FORMAT = "coda-run-checkpoint"
_CHECKPOINT_VERSION = 1


def _to_jsonable(value: Any) -> Any:
    if is_dataclass(value):
        return _to_jsonable(asdict(value))
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, dict):
        return {str(key): _to_jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_to_jsonable(item) for item in value]
    return value


def _batch_descriptor(batch: ArtifactBatchState) -> dict[str, Any]:
    return {
        "batch_id": batch.batch_id,
        "dataset_name": batch.dataset_name,
        "batch_index": batch.batch_index,
        "split_name": batch.split_name,
        "artifact_ids": list(batch.artifact_ids),
        "size": batch.size,
        "group_ids": dict(batch.group_ids),
        "sampling_note": batch.sampling_note,
        "metadata": _to_jsonable(batch.metadata),
    }


def serialize_run_state_checkpoint(run_state: RunState) -> dict[str, Any]:
    """Serialize the evolving CODA runtime state without duplicating artifacts."""

    return {
        "format": _CHECKPOINT_FORMAT,
        "format_version": _CHECKPOINT_VERSION,
        "dataset_name": run_state.dataset_metadata.dataset_name,
        "dataset_metadata_snapshot": _to_jsonable(run_state.dataset_metadata),
        "run_id": run_state.run_id,
        "research_question": _to_jsonable(run_state.research_question),
        "analysis_protocol": _to_jsonable(run_state.analysis_protocol),
        "review_policy": _to_jsonable(run_state.review_policy),
        "codebook": _to_jsonable(run_state.codebook),
        "history": _to_jsonable(run_state.history),
        "coding_batches": [_batch_descriptor(batch) for batch in run_state.coding_batches],
        "held_out_batches": [
            _batch_descriptor(batch) for batch in run_state.held_out_batches
        ],
        "current_batch_index": run_state.current_batch_index,
        "status": run_state.status,
        "notes": list(run_state.notes),
        "metadata": _to_jsonable(run_state.metadata),
    }


def save_run_state_checkpoint(run_state: RunState, path: str | Path) -> Path:
    """Atomically persist the current runtime checkpoint to disk."""

    checkpoint_path = Path(path)
    checkpoint_path.parent.mkdir(parents=True, exist_ok=True)
    payload = serialize_run_state_checkpoint(run_state)
    tmp_path = checkpoint_path.with_suffix(checkpoint_path.suffix + ".tmp")
    tmp_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    tmp_path.replace(checkpoint_path)
    return checkpoint_path


def _expect_mapping(value: Any, *, field_name: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        msg = f"{field_name} must be a JSON object."
        raise TypeError(msg)
    return value


def _research_question_from_dict(data: dict[str, Any]) -> ResearchQuestionState:
    return ResearchQuestionState(
        dataset_name=str(data["dataset_name"]),
        question_text=str(data["question_text"]),
        analysis_scope=str(data["analysis_scope"]),
        use_case=str(data["use_case"]),
        artifact_unit=str(data["artifact_unit"]),
        sensitizing_concepts=list(data.get("sensitizing_concepts", [])),
        notes=list(data.get("notes", [])),
    )


def _code_state_from_dict(data: dict[str, Any]) -> CodeState:
    return CodeState(
        code_id=str(data["code_id"]),
        name=str(data["name"]),
        definition=str(data["definition"]),
        inclusion_criteria=list(data.get("inclusion_criteria", [])),
        exclusion_criteria=list(data.get("exclusion_criteria", [])),
        representative_artifact_ids=list(data.get("representative_artifact_ids", [])),
        boundary_artifact_ids=list(data.get("boundary_artifact_ids", [])),
        counterexample_status=data.get("counterexample_status", "not_assessed"),
        hypothetical_examples=list(data.get("hypothetical_examples", [])),
        parent_code_id=data.get("parent_code_id"),
        status=data.get("status", "active"),
        notes=list(data.get("notes", [])),
        metadata=dict(data.get("metadata", {})),
    )


def _codebook_change_from_dict(data: dict[str, Any]) -> CodebookChangeState:
    return CodebookChangeState(
        change_id=str(data["change_id"]),
        action=data["action"],
        round_index=int(data["round_index"]),
        summary=str(data["summary"]),
        summary_zh=str(data.get("summary_zh", "")),
        rationale=str(data.get("rationale", "")),
        rationale_zh=str(data.get("rationale_zh", "")),
        target_code_ids=list(data.get("target_code_ids", [])),
        resulting_code_ids=list(data.get("resulting_code_ids", [])),
        artifact_ids=list(data.get("artifact_ids", [])),
        decided_by=str(data.get("decided_by", "human")),
        metadata=dict(data.get("metadata", {})),
    )


def _codebook_state_from_dict(data: dict[str, Any]) -> CodebookState:
    return CodebookState(
        dataset_name=str(data["dataset_name"]),
        version=int(data["version"]),
        codes=[
            _code_state_from_dict(_expect_mapping(code, field_name="codebook.code"))
            for code in data.get("codes", [])
        ],
        sensitizing_concepts=list(data.get("sensitizing_concepts", [])),
        revisions=[
            _codebook_change_from_dict(
                _expect_mapping(revision, field_name="codebook.revision")
            )
            for revision in data.get("revisions", [])
        ],
        notes=list(data.get("notes", [])),
    )


def _coding_record_from_dict(data: dict[str, Any]) -> CodingRecordState:
    return CodingRecordState(
        record_id=str(data["record_id"]),
        artifact_id=str(data["artifact_id"]),
        dataset_name=str(data["dataset_name"]),
        batch_index=int(data["batch_index"]),
        codebook_version=int(data["codebook_version"]),
        decision=data["decision"],
        codebook_version_before=(
            int(data["codebook_version_before"])
            if data.get("codebook_version_before") is not None
            else None
        ),
        codebook_version_after=(
            int(data["codebook_version_after"])
            if data.get("codebook_version_after") is not None
            else None
        ),
        pre_read_memo=str(data.get("pre_read_memo", "")),
        final_code_ids=list(data.get("final_code_ids", [])),
        final_code_names=list(data.get("final_code_names", [])),
        rationale=str(data.get("rationale", "")),
        evidence_summary=list(data.get("evidence_summary", [])),
        preserved_alternatives=list(data.get("preserved_alternatives", [])),
        validation_signals=list(data.get("validation_signals", [])),
        notes=list(data.get("notes", [])),
        metadata=dict(data.get("metadata", {})),
    )


def _retrospective_task_from_dict(data: dict[str, Any]) -> RetrospectiveRecodingTask:
    return RetrospectiveRecodingTask(
        task_id=str(data["task_id"]),
        artifact_id=str(data["artifact_id"]),
        trigger_change_id=str(data["trigger_change_id"]),
        from_codebook_version=int(data["from_codebook_version"]),
        target_codebook_version=int(data["target_codebook_version"]),
        status=data.get("status", "pending"),
        reason=str(data.get("reason", "")),
        attempt_count=int(data.get("attempt_count", 0)),
        metadata=dict(data.get("metadata", {})),
    )


def _analysis_protocol_from_dict(
    data: dict[str, Any] | None,
    *,
    artifact_unit: str,
) -> AnalysisProtocolState:
    payload = dict(data or {})
    payload.setdefault("artifact_unit", artifact_unit)
    return AnalysisProtocolState(**payload)


def _review_policy_from_dict(data: dict[str, Any] | None) -> ReviewPolicyState:
    payload = dict(data or {})
    legacy_mode = payload.pop("review_mode", None)
    if "setting" not in payload and legacy_mode is not None:
        payload["setting"] = {
            "every_artifact": "full",
            "conditional": "selective",
        }.get(str(legacy_mode), str(legacy_mode))
    return ReviewPolicyState(**payload)


def _unresolved_case_from_dict(data: dict[str, Any]) -> UnresolvedCaseState:
    return UnresolvedCaseState(**data)


def _stage_review_from_dict(data: dict[str, Any]) -> StageReviewState:
    return StageReviewState(**data)


def _stabilization_check_from_dict(data: dict[str, Any]) -> StabilizationCheckState:
    return StabilizationCheckState(**data)


def _context_request_from_dict(data: dict[str, Any]) -> ContextRequestState:
    return ContextRequestState(**data)


def _history_state_from_dict(data: dict[str, Any]) -> HistoryState:
    return HistoryState(
        coding_records=[
            _coding_record_from_dict(
                _expect_mapping(record, field_name="history.coding_record")
            )
            for record in data.get("coding_records", [])
        ],
        codebook_revisions=[
            _codebook_change_from_dict(
                _expect_mapping(revision, field_name="history.codebook_revision")
            )
            for revision in data.get("codebook_revisions", [])
        ],
        analytic_memos=[
            dict(_expect_mapping(memo, field_name="history.analytic_memo"))
            for memo in data.get("analytic_memos", [])
        ],
        retrospective_tasks=[
            _retrospective_task_from_dict(
                _expect_mapping(task, field_name="history.retrospective_task")
            )
            for task in data.get("retrospective_tasks", [])
        ],
        unresolved_cases=[
            _unresolved_case_from_dict(
                _expect_mapping(item, field_name="history.unresolved_case")
            )
            for item in data.get("unresolved_cases", [])
        ],
        stage_reviews=[
            _stage_review_from_dict(
                _expect_mapping(item, field_name="history.stage_review")
            )
            for item in data.get("stage_reviews", [])
        ],
        stabilization_checks=[
            _stabilization_check_from_dict(
                _expect_mapping(item, field_name="history.stabilization_check")
            )
            for item in data.get("stabilization_checks", [])
        ],
        context_requests=[
            _context_request_from_dict(
                _expect_mapping(item, field_name="history.context_request")
            )
            for item in data.get("context_requests", [])
        ],
        notes=list(data.get("notes", [])),
    )


def _validate_batch_descriptors(
    payload: dict[str, Any],
    *,
    coding_batches: list[ArtifactBatchState],
    held_out_batches: list[ArtifactBatchState],
) -> None:
    expected_coding = [_batch_descriptor(batch) for batch in coding_batches]
    checkpoint_coding = payload.get("coding_batches", [])
    if checkpoint_coding != expected_coding:
        msg = "Checkpoint coding_batches do not match the provided runtime batches."
        raise ValueError(msg)
    expected_held_out = [_batch_descriptor(batch) for batch in held_out_batches]
    if payload.get("held_out_batches", []) != expected_held_out:
        msg = "Checkpoint held_out_batches do not match the provided runtime batches."
        raise ValueError(msg)


def restore_run_state_from_checkpoint(
    payload: dict[str, Any],
    *,
    dataset_metadata: DatasetMetadata,
    coding_batches: list[ArtifactBatchState],
    held_out_batches: list[ArtifactBatchState] | None = None,
) -> RunState:
    """Restore RunState from serialized checkpoint data plus reconstructed batches."""

    if payload.get("format") != _CHECKPOINT_FORMAT:
        msg = "Unsupported checkpoint format."
        raise ValueError(msg)
    if int(payload.get("format_version", 0)) != _CHECKPOINT_VERSION:
        msg = "Unsupported checkpoint version."
        raise ValueError(msg)
    dataset_name = str(payload.get("dataset_name"))
    if dataset_name != dataset_metadata.dataset_name:
        msg = (
            "Checkpoint dataset_name does not match the provided dataset metadata: "
            f"{dataset_name} != {dataset_metadata.dataset_name}"
        )
        raise ValueError(msg)

    provided_held_out = list(held_out_batches or [])
    _validate_batch_descriptors(
        payload,
        coding_batches=list(coding_batches),
        held_out_batches=provided_held_out,
    )

    return RunState(
        run_id=str(payload["run_id"]),
        dataset_metadata=dataset_metadata,
        research_question=_research_question_from_dict(
            _expect_mapping(payload["research_question"], field_name="research_question")
        ),
        codebook=_codebook_state_from_dict(
            _expect_mapping(payload["codebook"], field_name="codebook")
        ),
        history=_history_state_from_dict(
            _expect_mapping(payload["history"], field_name="history")
        ),
        coding_batches=list(coding_batches),
        held_out_batches=provided_held_out,
        analysis_protocol=_analysis_protocol_from_dict(
            payload.get("analysis_protocol")
            if isinstance(payload.get("analysis_protocol"), dict)
            else None,
            artifact_unit=dataset_metadata.artifact_unit,
        ),
        review_policy=_review_policy_from_dict(
            payload.get("review_policy")
            if isinstance(payload.get("review_policy"), dict)
            else {
                "review_mode": dict(payload.get("metadata", {})).get(
                    "review_mode", "full"
                )
            }
        ),
        current_batch_index=int(payload.get("current_batch_index", 0)),
        status=payload.get("status", "not_started"),
        notes=list(payload.get("notes", [])),
        metadata=dict(payload.get("metadata", {})),
    )


def load_run_state_checkpoint(
    path: str | Path,
    *,
    dataset_metadata: DatasetMetadata,
    coding_batches: list[ArtifactBatchState],
    held_out_batches: list[ArtifactBatchState] | None = None,
) -> RunState:
    """Load a persisted checkpoint file and rebuild RunState."""

    checkpoint_path = Path(path)
    payload = json.loads(checkpoint_path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        msg = f"{checkpoint_path} must contain a JSON object."
        raise TypeError(msg)
    return restore_run_state_from_checkpoint(
        payload,
        dataset_metadata=dataset_metadata,
        coding_batches=coding_batches,
        held_out_batches=held_out_batches,
    )


def append_jsonl(path: str | Path, payload: dict[str, Any]) -> Path:
    """Append one JSON line to a log file."""

    jsonl_path = Path(path)
    jsonl_path.parent.mkdir(parents=True, exist_ok=True)
    with jsonl_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False))
        handle.write("\n")
    return jsonl_path


def serialize_human_review_output(review_output: HumanReviewOutput) -> dict[str, Any]:
    return _to_jsonable(review_output)


def serialize_artifact_run_result(result: ArtifactRunResult) -> dict[str, Any]:
    payload = _to_jsonable(result)
    # Canonical name first; retain the legacy key for one compatibility cycle.
    payload["comparison_output"] = payload.get("arbitration_output")
    evidence_packet = payload.get("evidence_packet")
    if isinstance(evidence_packet, dict):
        evidence_packet.setdefault(
            "comparison_output",
            evidence_packet.get("arbitration_output"),
        )
    return payload


def serialize_codebook_state(codebook: CodebookState) -> dict[str, Any]:
    return _to_jsonable(codebook)


def persist_codebook_snapshot(run_state: RunState, directory: str | Path) -> Path:
    """Write an immutable snapshot for the current codebook version."""

    snapshot_dir = Path(directory)
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    snapshot_path = snapshot_dir / f"codebook-v{run_state.codebook.version:04d}.json"
    if snapshot_path.exists():
        return snapshot_path
    tmp_path = snapshot_path.with_suffix(snapshot_path.suffix + ".tmp")
    tmp_path.write_text(
        json.dumps(serialize_codebook_state(run_state.codebook), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    tmp_path.replace(snapshot_path)
    return snapshot_path
