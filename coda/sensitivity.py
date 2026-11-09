"""Freeze and validate the supplementary 3-dataset x 3-model experiment."""
from __future__ import annotations
import hashlib
import json
import random
import re
from typing import Any
from coda.study import evidence_sha256, StudyManifestError

ROLES = ('context', 'coder_a', 'coder_b', 'induction', 'comparison', 'validation', 'initial_assignment')


def complete_evidence_case(item: dict[str, Any]) -> bool:
    """Conservative source completeness for the paper's 50-case supplement.

    Primary analysis retains incomplete cases. Only this supplementary sample
    excludes known missing linked context; successful discussion retrieval alone
    must not erase an explicitly unavailable supporting file.
    """
    fields = item.get('raw_fields', {})
    if (not item.get('content') or item.get('evidence_incomplete') or
            fields.get('evidence_status', 'complete') != 'complete' or
            any(word in str(fields.get('source_context_status', '')).lower()
                for word in ('missing', 'partial', 'unavailable', 'pending', 'ambiguous'))):
        return False
    if 'evidence_status' in fields and not str(fields.get('body', '')).strip() and not fields.get('retrieved_comment_count', 0):
        return False
    for key, text in fields.items():
        if re.fullmatch(r'(?:linked|external)_artifact_\d+', key):
            header = str(text).split('\n', 2)
            if len(header) < 2 or not re.search(r'\bavailability: available(?:;|$)', header[1]):
                return False
    return True


def build_sensitivity_protocol(packets: dict[str, dict[str, Any]], *,
                               reference_models: dict[str, str],
                               alternative_a: str = 'Deepseek-V4-Pro',
                               alternative_b: str = 'Qwen-3.7-Max',
                               evaluator_models: list[str], seed: int = 20260907) -> dict[str, Any]:
    if len(packets) != 3 or len(set(evaluator_models)) != 3:
        raise StudyManifestError('Sensitivity requires three datasets and three frozen evaluator models.')
    if set(reference_models) != set(ROLES) or not all(reference_models.values()):
        raise StudyManifestError('Reference model assignment must explicitly bind all LLM roles.')
    if alternative_a == alternative_b or set(evaluator_models) & {alternative_a, alternative_b}:
        raise StudyManifestError('Alternative backbones must be distinct and excluded from the evaluators.')
    protocol = {'format': 'coda-sensitivity-protocol', 'format_version': 1,
                'seed': seed, 'review_setting': 'automatic', 'repeats': 1,
                'evaluator_models': evaluator_models, 'datasets': {}, 'runs': [],
                'execution_batch_policy': 'one_artifact_micro_batch',
                'paper_batch_exception': 'User-approved micro-batches retained; 40 cases are not executed as four atomic batches.'}
    for dataset, packet in sorted(packets.items()):
        if packet.get('dataset_name') != dataset or not packet.get('formal_evaluation_ready'):
            raise StudyManifestError('Supply complete frozen formal packets identified by dataset.')
        phase = (packet.get('study_materials') or {}).get('phase')
        if phase != 'formal':
            raise StudyManifestError('Sensitivity sampling must use the formal pool.')
        # Require a complete evidence snapshot explicitly; missing issue context
        # cannot be made complete by a random sampler.
        available = [item for item in packet.get('artifacts', []) if complete_evidence_case(item)]
        if len(available) < 50:
            raise StudyManifestError(f'{dataset}: fewer than 50 complete cases available.')
        available.sort(key=lambda item: item['artifact_id'])
        selected = random.Random(f'{seed}:{dataset}').sample(available, 50)
        ids = [item['artifact_id'] for item in selected]
        protocol['datasets'][dataset] = {
            'artifact_ids': ids, 'initialization_artifact_ids': ids[:10],
            'iterative_artifact_ids': ids[10:],
            'evidence_sha256': {item['artifact_id']: evidence_sha256(item) for item in selected},
            'source_study_materials': packet['study_materials'],
        }
        for name, models in [('Ref', reference_models),
                             ('MA', {role: alternative_a for role in ROLES}),
                             ('MB', {role: alternative_b for role in ROLES})]:
            protocol['runs'].append({'dataset_name': dataset, 'condition': name,
                                     'role_models': models, 'replicate': 1,
                                     'artifact_ids': ids, 'initialization_artifact_ids': ids[:10]})
    protocol['protocol_sha256'] = hashlib.sha256(json.dumps(protocol, sort_keys=True).encode()).hexdigest()
    return protocol


def verify_sensitivity_run(protocol: dict[str, Any], state, role_models: dict[str, str]) -> None:
    binding = state.metadata.get('sensitivity_protocol', {})
    expected = next((row for row in protocol['runs'] if row['dataset_name'] == state.dataset_metadata.dataset_name
                     and row['condition'] == binding.get('condition')), None)
    if expected is None or role_models != expected['role_models']:
        raise StudyManifestError('Run model roles differ from the frozen sensitivity condition.')
    if binding.get('protocol_sha256') != protocol.get('protocol_sha256'):
        raise StudyManifestError('Run is bound to a different sensitivity protocol.')
    if state.metadata.get('selected_artifact_ids') != expected['artifact_ids']:
        raise StudyManifestError('Run cases/order differ from the frozen sensitivity corpus.')
    if state.review_policy.setting != 'automatic':
        raise StudyManifestError('Sensitivity runs require Automatic.')
