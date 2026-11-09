"""Paper RQ1 aggregation: common assessability, then equal model/run weights."""
from __future__ import annotations
from collections import defaultdict
from statistics import mean
from typing import Any

DIMENSIONS = ('clarity', 'category_boundaries', 'meaningful_coverage')


def aggregate_paper_rq1(rows: list[dict[str, Any]], *,
                        evaluator_ids: list[str] | None = None,
                        packets: dict[str, dict[str, Any]] | None = None,
                        human_fallback: bool = False) -> dict[str, Any]:
    evaluators = sorted(set(evaluator_ids or [str(row['evaluator_id']) for row in rows]))
    expected_evaluators = 2 if human_fallback else 3
    if len(evaluators) != expected_evaluators:
        return {'available': False, 'reason': f'Exactly {expected_evaluators} independent evaluator identities are required.'}
    grouped = defaultdict(dict)
    for row in rows:
        if str(row['evaluator_id']) not in evaluators:
            raise ValueError('Scores contain an evaluator outside the frozen selection.')
        key = (str(row['run_id']), row['dimension'], row.get('artifact_id'), row.get('code_id'))
        evaluator = str(row['evaluator_id'])
        if evaluator in grouped[key]:
            raise ValueError(f'Duplicate rating: {key}, {evaluator}')
        grouped[key][evaluator] = row
    run_ids = sorted(set(str(row['run_id']) for row in rows))
    per_run = {}
    groups = defaultdict(list)
    for run_id in run_ids:
        packet = (packets or {}).get(run_id, {})
        run_rows = [row for row in rows if str(row['run_id']) == run_id]
        policy = packet.get('review_policy', {})
        dataset = packet.get('dataset_name') or run_rows[0].get('dataset_name', 'unspecified')
        configuration = policy.get('setting') or run_rows[0].get('configuration', 'unspecified')
        result = {'codebook': {}}
        for dimension in DIMENSIONS:
            ratings = grouped.get((run_id, dimension, None, None), {})
            result['codebook'][dimension] = (mean(ratings[evaluator]['score'] for evaluator in evaluators)
                if set(ratings) == set(evaluators) else None)
        targets = {(artifact['artifact_id'], code_id)
                   for artifact in packet.get('artifacts', [])
                   for code_id in (artifact.get('coding_record') or {}).get('final_code_ids', [])}
        if not packet:
            targets = {(key[2], key[3]) for key in grouped
                       if key[0] == run_id and key[1] == 'evidence_support'}
        common = []
        unassessable = 0
        missing = []
        for artifact_id, code_id in sorted(targets):
            ratings = grouped.get((run_id, 'evidence_support', artifact_id, code_id), {})
            if set(ratings) != set(evaluators):
                missing.append([artifact_id, code_id])
            elif any(row.get('status', 'assessable') == 'unassessable' for row in ratings.values()):
                unassessable += 1
            else:
                common.append(ratings)
        proportions = {
            str(score): mean(sum(ratings[evaluator]['score'] == score for ratings in common) / len(common)
                             for evaluator in evaluators)
            if common and not missing else None for score in (0, 1, 2)
        }
        result['evidence_support'] = {
            'proportions': proportions, 'fully_supported_rate': proportions['2'],
            'common_assessable_count': len(common), 'submitted_assignments': len(targets),
            'unassessable_count': unassessable,
            'unassessable_rate': unassessable / len(targets) if targets and not missing else None,
            'missing_rating_targets': missing,
        }
        planned = packet.get('artifacts', [])
        result['unresolved_case_rate'] = (
            sum((item.get('coding_record') or {}).get('decision') not in {'accept', 'revise'}
                for item in planned) / len(planned) if planned else None
        )
        per_run[run_id] = result
        groups[(dataset, configuration)].append(run_id)
    aggregate = {}
    for (dataset, configuration), ids in groups.items():
        complete_runs = len(ids) == 2
        def equal(values):
            return mean(values) if complete_runs and all(value is not None for value in values) else None
        aggregate[f'{dataset}:{configuration}'] = {
            'run_ids': ids, 'expected_run_count': 2,
            'codebook': {dimension: equal([per_run[key]['codebook'][dimension] for key in ids])
                         for dimension in DIMENSIONS},
            'evidence_support_proportions': {
                score: equal([per_run[key]['evidence_support']['proportions'][score] for key in ids])
                for score in ('0', '1', '2')},
            'unassessable_assignment_rate': equal([per_run[key]['evidence_support']['unassessable_rate'] for key in ids]),
            'unresolved_case_rate': equal([per_run[key]['unresolved_case_rate'] for key in ids]),
        }
    return {'available': True, 'evaluator_ids': evaluators,
            'by_run': per_run, 'by_dataset_configuration': aggregate,
            'assessment_mode': 'independent_humans' if human_fallback else 'three_frozen_models',
            'protocol': f'common assessable assignments; equal weights for {expected_evaluators} evaluators and two runs'}
