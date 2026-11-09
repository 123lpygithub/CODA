"""One completion gate shared by runtime finalization and formal exports."""
from __future__ import annotations

import hashlib
import json
from typing import Any


def decision_fingerprint(codebook: dict[str, Any], records: list[dict[str, Any]]) -> str:
    latest = {str(row['artifact_id']): row for row in records}
    return hashlib.sha256(json.dumps({
        'codebook': codebook,
        'records': [latest[key] for key in sorted(latest)],
    }, sort_keys=True, ensure_ascii=False).encode('utf-8')).hexdigest()


def completion_issues(payload: dict[str, Any], *, require_approval: bool = False,
                      require_audit: bool = True) -> list[str]:
    history = payload.get('history', {})
    metadata = payload.get('metadata', {})
    codebook = payload.get('codebook', {})
    records = history.get('coding_records', [])
    latest = {str(row['artifact_id']): row for row in records}
    selected = set(metadata.get('selected_artifact_ids', []))
    if not selected:
        selected = {key for batch in payload.get('coding_batches', [])
                    for key in batch.get('artifact_ids', [])}
        selected.update(metadata.get('bootstrap', {}).get('artifact_ids', []))
    unresolved = {row.get('artifact_id') for row in history.get('unresolved_cases', [])
                  if row.get('status', 'open') == 'open'}
    issues = []
    missing = sorted(key for key in selected if key not in latest and key not in unresolved)
    rejected = sorted(key for key in selected if latest.get(key, {}).get('decision') == 'reject')
    if missing:
        issues.append(f'Unprocessed artifacts: {missing}')
    if rejected:
        issues.append(f'Rejected proposals awaiting reconsideration: {rejected}')
    if any(latest.get(key, {}).get('decision') == 'request_additional_context' for key in selected):
        issues.append('Case decisions requesting context must be reconsidered before completion.')
    if any(row.get('status', 'pending') == 'pending'
           for row in history.get('context_requests', [])):
        issues.append('Pending context requests remain (artifact, initial, or final scope).')
    if any(row.get('status', 'pending') not in {'completed', 'cancelled'}
           for row in history.get('retrospective_tasks', [])):
        issues.append('Complete all retrospective propagation tasks before final acceptance.')
    if metadata.get('awaiting_human_review') or metadata.get('reopened_context_artifact_ids'):
        issues.append('Prepared reviews or reopened cases remain pending.')
    if any(row.get('status') != 'completed'
           for row in metadata.get('iterative_batch_preparations', {}).values()):
        issues.append('Unfinished comparison batches remain pending.')
    if require_audit:
        fingerprint = decision_fingerprint(codebook, records)
        audits = metadata.get('final_validation_audits', {}).values()
        if not any(row.get('status') == 'completed'
                   and row.get('decision_fingerprint') == fingerprint for row in audits):
            issues.append('Final validation of the current codebook and decisions is incomplete.')
    if require_approval and payload.get('review_policy', {}).get('final_review_required', True):
        reviews = [row for row in history.get('stage_reviews', []) if row.get('kind') == 'final']
        if not reviews or reviews[-1].get('decision') not in {'accept', 'mark_unresolved'} or reviews[-1].get('codebook_version_after') != codebook.get('version'):
            issues.append('Final human review of the current version has not been completed.')
    return issues
