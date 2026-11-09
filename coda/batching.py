"""Shared-snapshot comparison batches with resumable per-case acceptance.

The initial comparison and reconciliation barrier precedes validation/review.
Accepted edits may then advance versions case by case; every stale proposal is
rechecked against the current accepted book before validation and routing.
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import asdict, replace
import hashlib
import json
from pathlib import Path

from coda.contracts import ComparisonOutput
from coda.stage_checkpoints import StageCheckpointStore, _decode
from coda.state import CodebookState, HistoryState


def prepare_batch_case(orchestrator, run_state, batch, artifact, *, directory: Path,
                       persist=lambda: None):
    """Prepare all initial proposals, reconcile once, then validate this case.

    Metadata freezes the base snapshot before calls. Stage files preserve every
    successful call and the complete reconciliation, including restart after only
    part of a batch has been accepted. Never substitute a newer base on restart.
    """
    plans = run_state.metadata.setdefault('iterative_batch_preparations', {})
    plan = plans.get(batch.batch_id)
    if plan is None:
        plan = {
            'status': 'preparing', 'base_version': run_state.codebook.version,
            'codebook': asdict(run_state.codebook), 'history': asdict(run_state.history),
            'artifact_ids': [item.artifact_id for item in batch.artifacts],
            'language': orchestrator._output_language,
        }
        plans[batch.batch_id] = plan
        persist()
    if plan['artifact_ids'] != [item.artifact_id for item in batch.artifacts]:
        raise ValueError('Batch membership differs from its frozen preparation.')
    if plan['language'] != orchestrator._output_language:
        raise ValueError('Keep the frozen batch language when resuming; start a new run to change it.')
    base = deepcopy(run_state)
    base.codebook = _decode(plan['codebook'], CodebookState)
    base.history = _decode(plan['history'], HistoryState)
    # Freeze history for initial comparison but include supplied case context
    # after a deferral only in the subsequent current-book recheck.
    tag = hashlib.sha256(batch.batch_id.encode()).hexdigest()[:20]
    directory = Path(directory)/f'batch-{tag}'
    initial = []
    for member in batch.artifacts:
        key = orchestrator.stage_cache_key(base, member)
        store = StageCheckpointStore(directory/f'initial-{hashlib.sha256(member.artifact_id.encode()).hexdigest()[:20]}.json', cache_key=key)
        prepared = orchestrator.prepare_one_artifact(base, artifact=member, batch=batch,
            allow_reviewed=True, stage_checkpoint_store=store, defer_validation=True)
        initial.append(prepared)
        run_state.metadata.setdefault('case_materials', {})[member.artifact_id] = base.metadata['case_materials'][member.artifact_id]
    reconciliation_key = hashlib.sha256(json.dumps({
        'base': plan['codebook'], 'proposals': [asdict(item) for item in initial],
    }, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
    coordinated = StageCheckpointStore(directory/'reconciliation.json', cache_key=reconciliation_key)
    outputs = coordinated.get('proposals', dict[str, ComparisonOutput])
    if outputs is None:
        try:
            reconcile = getattr(orchestrator._comparison_agent, 'reconcile_batch', None)
            if reconcile is None:
                raise ValueError('Multi-artifact batches require a Comparison agent with reconcile_batch support.')
            outputs = reconcile(run_state=base, prepared=initial)
            if set(outputs) != set(plan['artifact_ids']) or any(
                not isinstance(value, ComparisonOutput) or value.artifact_id != key for key,value in outputs.items()):
                raise ValueError('Reconciliation must cover every batch case exactly once.')
        except Exception as error:
            if orchestrator._failure_policy == 'raise':
                raise
            outputs = {item.artifact_id: orchestrator._failed_comparison_output(item.artifact,error) for item in initial}
        coordinated.put('proposals', {key:asdict(value) for key,value in outputs.items()})
    plan['status'] = 'reviewing'
    plan['reconciliation_sha256'] = reconciliation_key
    persist()
    original = next(item for item in initial if item.artifact_id == artifact.artifact_id)
    # Current state, history, resolved context, and original proposal all affect
    # this recheck. A rejected or edited proposal cannot reuse old acceptance.
    prior = asdict(outputs[artifact.artifact_id])
    recheck_key = hashlib.sha256(json.dumps({
        'case_key': orchestrator.stage_cache_key(run_state,artifact),
        'codebook': asdict(run_state.codebook), 'proposal': prior,
        'records': [asdict(row) for row in run_state.history.coding_records],
    },sort_keys=True,ensure_ascii=False).encode()).hexdigest()
    checked = StageCheckpointStore(directory/f'checked-{hashlib.sha256(artifact.artifact_id.encode()).hexdigest()[:20]}.json',cache_key=recheck_key)
    extra_context = orchestrator._additional_context_for_artifact(run_state,artifact.artifact_id)
    if not extra_context:
        checked.put('context', original.context_packet)
        checked.put('coders', original.coder_outputs)
    if outputs[artifact.artifact_id].model_metadata.get('agent_failure') or (asdict(run_state.codebook) == plan['codebook']
            and not extra_context
            and not any(row.artifact_id == artifact.artifact_id for row in run_state.history.coding_records)):
        checked.put('comparison', outputs[artifact.artifact_id])
    prepared = orchestrator.prepare_one_artifact(run_state,artifact=artifact,batch=batch,
        allow_reviewed=artifact.artifact_id in run_state.metadata.get('reopened_context_artifact_ids', []),
        stage_checkpoint_store=checked, comparison_task='batch_recheck',
        prior_comparison={'base_version':plan['base_version'], 'reconciled_proposal':prior,
                          'batch_case_ids':plan['artifact_ids']})
    return replace(prepared, evidence_packet=replace(prepared.evidence_packet,
        model_metadata={**prepared.evidence_packet.model_metadata,
            'batch_execution': {'batch_id':batch.batch_id, 'artifact_ids':plan['artifact_ids'],
                'base_version':plan['base_version'], 'validated_version':prepared.codebook_version,
                'reconciled_proposal':prior}}))
