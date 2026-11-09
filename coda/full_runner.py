from __future__ import annotations

import json
import hashlib
import os
import tempfile
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

from adapters.base import ArtifactRecord
from coda.orchestrator import ArtifactRunResult, CODAOrchestrator
from coda.persistence import (
    append_jsonl,
    persist_codebook_snapshot,
    save_run_state_checkpoint,
    serialize_artifact_run_result,
    serialize_codebook_state,
    serialize_human_review_output,
    serialize_run_state_checkpoint,
)
from coda.manifest import build_run_manifest, write_run_manifest
from coda.state import ArtifactBatchState, RunState
from coda.stage_checkpoints import StageCheckpointStore

OutputFunc = Callable[[str], None]
PauseFunc = Callable[[], None]


@dataclass(frozen=True)
class FullRunPaths:
    run_dir: Path
    checkpoint_path: Path
    review_log_path: Path
    artifact_log_path: Path
    final_codebook_path: Path
    codebook_snapshot_dir: Path
    bootstrap_manifest_path: Path
    bootstrap_evidence_packets_path: Path
    bootstrap_initial_codings_path: Path
    bootstrap_drafts_dir: Path
    initial_codebook_path: Path
    bootstrap_audit_path: Path
    bootstrap_assignments_path: Path
    bootstrap_checkpoint_dir: Path
    stage_checkpoint_dir: Path
    run_manifest_path: Path

    @classmethod
    def from_run_dir(cls, run_dir: str | Path) -> FullRunPaths:
        base_dir = Path(run_dir)
        return cls(
            run_dir=base_dir,
            checkpoint_path=base_dir / "checkpoint.json",
            review_log_path=base_dir / "reviews.jsonl",
            artifact_log_path=base_dir / "artifact_runs.jsonl",
            final_codebook_path=base_dir / "final_codebook.json",
            codebook_snapshot_dir=base_dir / "codebook_snapshots",
            bootstrap_manifest_path=base_dir / "bootstrap_manifest.json",
            bootstrap_evidence_packets_path=base_dir / "bootstrap_evidence_packets.jsonl",
            bootstrap_initial_codings_path=base_dir / "bootstrap_initial_codings.jsonl",
            bootstrap_drafts_dir=base_dir / "bootstrap_codebook_drafts",
            initial_codebook_path=base_dir / "initial_codebook_v0.json",
            bootstrap_audit_path=base_dir / "bootstrap_audit.json",
            bootstrap_assignments_path=base_dir / "bootstrap_assignments.jsonl",
            bootstrap_checkpoint_dir=base_dir / "bootstrap_checkpoints",
            stage_checkpoint_dir=base_dir / "stage_checkpoints",
            run_manifest_path=base_dir / "run_manifest.json",
        )


def build_single_batch_run_state(
    dataset_metadata,
    artifacts: list[ArtifactRecord],
    *,
    batch_id: str,
    run_id: str | None = None,
) -> RunState:
    """Build the simplest CODA runtime: one coding batch over the given artifacts."""

    batch = ArtifactBatchState(
        batch_id=batch_id,
        dataset_name=dataset_metadata.dataset_name,
        batch_index=0,
        split_name="coding_pool",
        artifacts=artifacts,
    )
    return RunState.initialize(
        dataset_metadata,
        coding_batches=[batch],
        run_id=run_id,
    )


def pending_artifacts_for_batch(
    batch: ArtifactBatchState,
    run_state: RunState,
) -> list[ArtifactRecord]:
    """Return artifacts that still need human-reviewed CODA processing."""

    reviewed_ids = set(run_state.history.reviewed_artifact_ids())
    reopened_ids = {
        str(item)
        for item in run_state.metadata.get("reopened_context_artifact_ids", [])
        if isinstance(item, str)
    }
    return [
        artifact
        for artifact in batch.artifacts
        if artifact.artifact_id not in reviewed_ids
        or artifact.artifact_id in reopened_ids
    ]


def advance_completed_batches(run_state: RunState) -> bool:
    """Advance across any fully reviewed batches during resume or after completion."""

    advanced = False
    while True:
        batch = run_state.current_batch()
        if batch is None:
            break
        if pending_artifacts_for_batch(batch, run_state):
            break
        run_state.advance_to_next_batch()
        advanced = True
    if run_state.has_remaining_coding_batches():
        if run_state.history.coding_records:
            run_state.status = "in_progress"
        else:
            run_state.status = "not_started"
    else:
        run_state.status = "completed"
    return advanced


def _build_review_log_entry(
    *,
    run_state: RunState,
    batch: ArtifactBatchState,
    result: ArtifactRunResult,
) -> dict[str, object]:
    latest_record = run_state.history.latest_record_for_artifact(result.artifact_id)
    latest_record_id = latest_record.record_id if latest_record is not None else (
        f"{result.artifact_id}:v{run_state.codebook.version}"
    )
    return {
        "completion_id": latest_record_id,
        "run_id": run_state.run_id,
        "dataset_name": run_state.dataset_metadata.dataset_name,
        "artifact_id": result.artifact_id,
        "batch_id": batch.batch_id,
        "batch_index": batch.batch_index,
        "decision": result.human_review_output.decision,
        "final_codes": [
            {
                "code_id": code.code_id,
                "name": code.name,
                "definition": code.definition,
                "representative_artifact_ids": list(code.representative_artifact_ids),
            }
            for code in result.human_review_output.final_codes
        ],
        "rationale": result.human_review_output.rationale,
        "evidence_summary": list(result.human_review_output.evidence_summary),
        "preserved_alternatives": list(result.human_review_output.preserved_alternatives),
        "codebook_changes": [
            {
                "change_id": change.change_id,
                "action": change.action,
                "round_index": change.round_index,
                "summary": change.summary,
                "artifact_ids": list(change.artifact_ids),
                "resulting_code_ids": list(change.resulting_code_ids),
            }
            for change in result.human_review_output.codebook_changes
        ],
        "coding_record": latest_record.__dict__ if latest_record is not None else None,
        "codebook_version_after_review": run_state.codebook.version,
    }


def _build_artifact_run_log_entry(
    *,
    run_state: RunState,
    batch: ArtifactBatchState,
    result: ArtifactRunResult,
) -> dict[str, object]:
    payload = serialize_artifact_run_result(result)
    latest_record = run_state.history.latest_record_for_artifact(result.artifact_id)
    payload["completion_id"] = latest_record.record_id if latest_record is not None else (
        f"{result.artifact_id}:v{run_state.codebook.version}"
    )
    payload["run_id"] = run_state.run_id
    payload["dataset_name"] = run_state.dataset_metadata.dataset_name
    payload["batch_id"] = batch.batch_id
    payload["batch_index"] = batch.batch_index
    payload["codebook_version_after_review"] = run_state.codebook.version
    return payload


def persist_artifact_completion(
    *,
    run_state: RunState,
    batch: ArtifactBatchState,
    result: ArtifactRunResult,
    paths: FullRunPaths,
) -> None:
    """Persist the authoritative checkpoint first, then append human-readable logs."""

    save_run_state_checkpoint(run_state, paths.checkpoint_path)
    persist_codebook_snapshot(run_state, paths.codebook_snapshot_dir)
    _append_jsonl_once(
        paths.review_log_path,
        _build_review_log_entry(run_state=run_state, batch=batch, result=result),
    )
    _append_jsonl_once(
        paths.artifact_log_path,
        _build_artifact_run_log_entry(run_state=run_state, batch=batch, result=result),
    )


def _append_jsonl_once(path: Path, payload: dict[str, object]) -> None:
    """Append a completion log once so a failed request can be retried safely."""

    completion_id = payload.get("completion_id")
    if completion_id is not None and path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                existing = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(existing, dict) and existing.get("completion_id") == completion_id:
                return
    append_jsonl(path, payload)


def persist_final_codebook(run_state: RunState, path: str | Path) -> Path:
    final_path = Path(path)
    final_path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(
        serialize_codebook_state(run_state.codebook),
        ensure_ascii=False,
        indent=2,
    )
    # Never expose a partially written final artifact if the process stops
    # while serializing or flushing the JSON file.
    fd, temporary_name = tempfile.mkstemp(
        prefix=f".{final_path.name}.",
        suffix=".tmp",
        dir=final_path.parent,
        text=True,
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as temporary_file:
            temporary_file.write(payload)
            temporary_file.flush()
            os.fsync(temporary_file.fileno())
        os.replace(temporary_name, final_path)
    except Exception:
        try:
            os.unlink(temporary_name)
        except FileNotFoundError:
            pass
        raise
    return final_path


def _render_codebook_snapshot(output: OutputFunc, run_state: RunState) -> None:
    codebook = run_state.codebook
    output(
        f"[codebook] version={codebook.version} "
        f"codes={len(codebook.codes)} revisions={len(codebook.revisions)}"
    )
    if not codebook.codes:
        output("[codebook] (empty)")
        return
    for code in codebook.codes:
        output(f"- {code.code_id}: {code.name} [{code.status}]")
        output(f"  definition={code.definition}")
        if code.representative_artifact_ids:
            output("  representatives=" + ", ".join(code.representative_artifact_ids))
        if code.parent_code_id is not None:
            output(f"  parent={code.parent_code_id}")


def run_resumable_full_coding(
    *,
    orchestrator: CODAOrchestrator,
    run_state: RunState,
    paths: FullRunPaths,
    output_func: OutputFunc | None = None,
    pause_func: PauseFunc | None = None,
) -> RunState:
    """Run already initialized material with per-artifact checkpointing.

    The maintained complete Initial/Triggered/Final Review workflow is
    CodaWebService (also usable headlessly). This low-level compatibility helper
    preserves pending stage reviews and propagation tasks for that service;
    it must never declare those tasks accepted on behalf of a researcher.
    """

    output = output_func or print
    paths.run_dir.mkdir(parents=True, exist_ok=True)
    if (run_state.review_policy.initial_review_required and run_state.metadata.get("bootstrap")
            and not any(row.kind == "initial" and row.decision in {"accept", "revise", "mark_unresolved"}
                        for row in run_state.history.stage_reviews)):
        run_state.status = "awaiting_initial_review"
        save_run_state_checkpoint(run_state, paths.checkpoint_path)
        output("[paused] Complete Initial Review through the workbench service before iterative coding.")
        return run_state
    if run_state.history.pending_context_requests():
        run_state.status = "awaiting_context"
        save_run_state_checkpoint(run_state, paths.checkpoint_path)
        output("[paused] Resolve pending context requests before resuming.")
        return run_state
    if not paths.run_manifest_path.exists():
        artifacts = [
            artifact
            for batch in run_state.coding_batches
            for artifact in batch.artifacts
        ]
        write_run_manifest(
            paths.run_manifest_path,
            build_run_manifest(run_state, artifacts),
        )
    orchestrator.set_execution_trace_sink(lambda trace: append_jsonl(paths.run_dir / "model_calls.jsonl", trace))
    persist_codebook_snapshot(run_state, paths.codebook_snapshot_dir)

    if advance_completed_batches(run_state):
        save_run_state_checkpoint(run_state, paths.checkpoint_path)

    total_artifacts = run_state.total_coding_artifacts
    while True:
        batch = run_state.current_batch()
        if batch is None:
            break
        pending = pending_artifacts_for_batch(batch, run_state)
        output(
            f"[batch {batch.batch_index}] pending={len(pending)} "
            f"reviewed={total_artifacts - len(pending)}/{total_artifacts}"
        )
        for artifact in pending:
            output(f"[artifact] {artifact.artifact_id}")
            cache_key = orchestrator.stage_cache_key(run_state, artifact)
            cache_file = hashlib.sha256(
                artifact.artifact_id.encode("utf-8")
            ).hexdigest()[:24]
            stage_store = StageCheckpointStore(
                paths.stage_checkpoint_dir / f"{cache_file}.json",
                cache_key=cache_key,
            )
            result = orchestrator.run_one_artifact(
                run_state,
                artifact=artifact,
                batch=batch,
                stage_checkpoint_store=stage_store,
            )
            advance_completed_batches(run_state)
            persist_artifact_completion(
                run_state=run_state,
                batch=batch,
                result=result,
                paths=paths,
            )
            if result.human_review_output.decision == "request_additional_context":
                run_state.status = "awaiting_context"
                save_run_state_checkpoint(run_state, paths.checkpoint_path)
                output("[paused] Resolve the pending context request before continuing.")
                return run_state
            latest = run_state.history.latest_record_for_artifact(artifact.artifact_id)
            output(
                f"[saved] artifact={artifact.artifact_id} "
                f"decision={result.human_review_output.decision} "
                f"codebook_v={run_state.codebook.version} "
                f"records={len(run_state.history.coding_records)} "
                f"record_id={(latest.record_id if latest is not None else 'n/a')}"
            )
            if run_state.has_remaining_coding_batches():
                _render_codebook_snapshot(output, run_state)
                if pause_func is not None:
                    output("[pause] press Enter to continue to the next artifact...")
                    pause_func()
        if not pending:
            advance_completed_batches(run_state)
            if run_state.current_batch() is batch:
                msg = f"Batch {batch.batch_id} has no pending artifacts but was not advanced."
                raise RuntimeError(msg)

    from coda.completion import completion_issues, decision_fingerprint
    from coda.state import UnresolvedCaseState
    selected_artifacts = {item.artifact_id: item for batch in run_state.coding_batches for item in batch.artifacts}
    fingerprint = decision_fingerprint(serialize_codebook_state(run_state.codebook),
                                       [asdict(row) for row in run_state.history.coding_records])
    audits = run_state.metadata.setdefault("final_validation_audits", {})
    if audits.get(fingerprint, {}).get("status") != "completed":
        audit = audits.setdefault(fingerprint, {"status": "running", "codebook_version": run_state.codebook.version,
            "decision_fingerprint": fingerprint, "validation_outputs": []})
        done = {row["artifact_id"] for row in audit["validation_outputs"]}
        for artifact_id, artifact in selected_artifacts.items():
            if artifact_id in done:
                continue
            result = orchestrator.validate_final_record(run_state, artifact, corpus_audit={"scope": "cli_full_corpus"})
            audit["validation_outputs"].append(asdict(result))
            if result.human_review_required or result.review_criteria or any(signal.signal != "valid" for signal in result.signals):
                run_state.history.append_unresolved(UnresolvedCaseState(
                    unresolved_id=f"cli-final-{fingerprint[:12]}-{artifact_id}", artifact_id=artifact_id,
                    reason=result.summary or "Final validation requires assessment.", source="final_validation",
                    created_at_codebook_version=run_state.codebook.version))
            save_run_state_checkpoint(run_state, paths.checkpoint_path)
        audit["status"] = "completed"
    issues = completion_issues(serialize_run_state_checkpoint(run_state))
    if issues:
        run_state.status = "awaiting_next_artifact"
    elif run_state.review_policy.final_review_required:
        run_state.status = "awaiting_final_review"
    else:
        run_state.status = "completed_with_unresolved" if run_state.history.open_unresolved_cases() else "completed"
        persist_final_codebook(run_state, paths.final_codebook_path)
        run_state.metadata.setdefault("events", []).append({
            "event": "outputs_frozen", "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "codebook_version": run_state.codebook.version,
        })
    save_run_state_checkpoint(run_state, paths.checkpoint_path)
    output(
        f"[done] status={run_state.status} reviewed={len(run_state.history.coding_records)} "
        f"codebook_v={run_state.codebook.version} "
        f"final_codebook={paths.final_codebook_path if paths.final_codebook_path.exists() else 'pending'}"
    )
    _render_codebook_snapshot(output, run_state)
    return run_state


def serialize_human_review_log_entry(review_output: ArtifactRunResult) -> dict[str, object]:
    """Small helper for inspection tools that consume persisted run records."""

    return serialize_human_review_output(review_output.human_review_output)
