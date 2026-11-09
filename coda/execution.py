"""Freeze the paper's six-reviewer, eighteen-run allocation from a real roster."""
from __future__ import annotations

from collections import Counter
from itertools import permutations
import random
from typing import Any

from coda.study import StudyManifestError, _digest, validate_study_manifest


def build_execution_plan(manifest: dict[str, Any], participants: list[dict[str, Any]], *,
                         phase: str = 'formal', seed: int = 20260907,
                         excluded_participant_ids: list[str] | None = None) -> dict[str, Any]:
    """Allocate attested eligible reviewers; never infer human qualifications.

    The roster records externally checked eligibility. Random tie breaking among
    feasible allocations minimizes experience imbalance across datasets. Task
    order is distinct from the ordered dataset pair: half start under S3.
    """
    validate_study_manifest(manifest)
    datasets = sorted(manifest['datasets'])
    ids = [item.get('participant_id') for item in participants]
    if phase not in {'pilot', 'formal'} or len(datasets) != 3 or len(participants) != 6:
        raise StudyManifestError('Allocation requires three datasets, six participants, and a pilot/formal phase.')
    if any(not isinstance(key, str) or not key.strip() for key in ids) or len(set(ids)) != 6:
        raise StudyManifestError('Supply six distinct nonempty participant IDs.')
    if set(ids) & set(excluded_participant_ids or []):
        raise StudyManifestError('Pilot reviewers and formal reviewers must be separate.')
    for person in participants:
        experience = person.get('experience_years')
        if (person.get('eligibility_confirmed') is not True or type(experience) not in {int, float}
                or experience < 0 or not set(person.get('eligible_datasets', [])).issubset(datasets)):
            raise StudyManifestError('Roster requires checked eligibility, experience, and eligible dataset IDs.')
    pairs = list(permutations(datasets, 2))
    feasible = []
    for allocation in permutations(sorted(participants, key=lambda person: person['participant_id'])):
        if any(not set(pair).issubset(person['eligible_datasets']) for pair, person in zip(pairs, allocation)):
            continue
        experience_totals = [sum(person['experience_years'] for pair, person in zip(pairs, allocation)
                                 if dataset in pair) for dataset in datasets]
        imbalance = max(experience_totals) - min(experience_totals)
        feasible.append((imbalance, allocation))
    if not feasible:
        raise StudyManifestError('No domain-eligible allocation covers all six ordered pairs.')
    best = min(item[0] for item in feasible)
    randomizer = random.Random(seed)
    chosen = randomizer.choice([allocation for score, allocation in feasible if score == best])
    starts_s2 = set(randomizer.sample(range(6), 3))
    runs = []
    counts = Counter()
    for index, ((left, right), person) in enumerate(zip(pairs, chosen)):
        order = [(left, 'selective'), (right, 'full')]
        if index not in starts_s2:
            order.reverse()
        for task_order, (dataset, setting) in enumerate(order, 1):
            counts[dataset, setting] += 1
            runs.append({'dataset_name': dataset, 'review_mode': setting, 'study_phase': phase,
                         'participant_id': person['participant_id'], 'task_order': task_order,
                         'replicate_index': counts[dataset, setting],
                         'comparison_block_id': f'{phase}:pair-{index + 1}'})
    for dataset in datasets:
        for replicate in (1, 2):
            runs.append({'dataset_name': dataset, 'review_mode': 'automatic', 'study_phase': phase,
                         'participant_id': None, 'task_order': None, 'replicate_index': replicate,
                         'comparison_block_id': f'{phase}:{dataset}:automatic-{replicate}'})
    plan = {'format': 'coda-study-execution-plan', 'format_version': 1,
            'study_id': manifest['study_id'], 'manifest_sha256': manifest['manifest_sha256'],
            'phase': phase, 'seed': seed, 'participants': participants, 'runs': runs,
            'experience_imbalance': best,
            'eligibility_source': 'researcher-confirmed roster; software does not verify qualifications'}
    plan['plan_sha256'] = _digest(plan)
    return plan
