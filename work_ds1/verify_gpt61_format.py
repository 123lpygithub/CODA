"""Structural audit of the GPT6-1-compatible deepseek-1 delivery."""
from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'Artifact'
ANALYST = 'deepseek-1'


def read_jsonl(path):
    return [json.loads(line) for line in path.open(encoding='utf-8') if line.strip()]


def sha(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def audit(dataset, expected):
    base = OUT / dataset / ANALYST
    artifacts = read_jsonl(base / 'artifacts.jsonl')
    assignments = json.loads((base / 'assignments.json').read_text(encoding='utf-8'))
    results = json.loads((base / 'results.json').read_text(encoding='utf-8'))
    book = json.loads((base / 'codebook.json').read_text(encoding='utf-8'))
    taxonomy = json.loads((base / 'taxonomy.json').read_text(encoding='utf-8'))

    assert len(artifacts) == expected
    assert len(assignments) == expected
    assert len(results['results']) == expected
    assert set(results) == {'metadata', 'results'}
    assert results['metadata'] == book['metadata']

    artifacts_by_id = {a['artifact_id']: a for a in artifacts}
    assignments_by_id = {a['case_id']: a for a in assignments}
    results_by_id = {r['id']: r for r in results['results']}
    assert len(artifacts_by_id) == len(assignments_by_id) == len(results_by_id) == expected
    assert set(artifacts_by_id) == set(assignments_by_id) == set(results_by_id)

    if dataset == 'CodeErrors':
        codes = {c['id']: c for c in book['codes']}
        assert all({'id', 'group', 'name', 'name_zh', 'definition', 'inclusion', 'exclusion',
                    'supporting_case_ids', 'case_count', 'representative_evidence'} <= set(c) for c in book['codes'])
        assert sum(len(g['children']) for g in taxonomy['children']) == len(codes)
        leaf_ids = {leaf.get('code_id') for g in taxonomy['children'] for leaf in g['children']}
        assert leaf_ids == set(codes)
        members = {cid: set(c['supporting_case_ids']) for cid, c in codes.items()}
        for cid, c in codes.items():
            assert c['case_count'] == len(c['supporting_case_ids'])
    else:
        codes = {c['code_id']: c for c in book['codes']}
        assert all({'code_id', 'name', 'definition', 'inclusion_criteria', 'exclusion_criteria',
                    'artifact_count', 'supporting_cases'} <= set(c) for c in book['codes'])
        assert len(taxonomy['children']) == len(codes)
        assert {leaf.get('code_id') for leaf in taxonomy['children']} == set(codes)
        members = {cid: set(c['supporting_cases']) for cid, c in codes.items()}
        for cid, c in codes.items():
            assert c['artifact_count'] == len(c['supporting_cases'])

    assert all(c['definition'].strip() for c in book['codes'])
    assert all(c.get('inclusion_criteria', c.get('inclusion', '')).strip() for c in book['codes'])
    assert all(c.get('exclusion_criteria', c.get('exclusion', '')).strip() for c in book['codes'])

    span_count = 0
    for case_id, a in assignments_by_id.items():
        assert a['code_ids']
        assert a['status'] == 'coded'
        assert a['rationale'].strip()
        assert a['evidence']
        assert set(a['code_ids']) == {cid for cid, ids in members.items() if case_id in ids}
        content = artifacts_by_id[case_id]['content']
        for ev in a['evidence']:
            assert content[ev['start_char']:ev['end_char']] == ev['quote']
            assert ev['field_sha256'] == sha(content)
            span_count += 1
        r = results_by_id[case_id]
        assert r['code_ids'] == a['code_ids']
        assert r['document'] == content
        assert r['categories'] == [codes[cid]['name'] for cid in a['code_ids']]
        if dataset == 'CodeErrors':
            assert r['summary'] == a['rationale']
        else:
            assert r['rationale'] == a['rationale']

    assert sum(len(a['code_ids']) for a in assignments) == book['metadata'].get(
        'assignment_count', sum(len(a['code_ids']) for a in assignments))

    # CSV header checks.
    with (base / 'codebook.csv').open(encoding='utf-8', newline='') as f:
        header = next(csv.reader(f))
    expected_header = (['id', 'group', 'name', 'name_zh', 'definition', 'inclusion', 'exclusion',
                        'case_count', 'supporting_case_ids'] if dataset == 'CodeErrors' else
                       ['code_id', 'name', 'definition', 'inclusion_criteria', 'exclusion_criteria',
                        'artifact_count', 'supporting_cases'])
    assert header == expected_header
    with (base / 'assignments.csv').open(encoding='utf-8', newline='') as f:
        assert next(csv.reader(f))

    return {
        'dataset': dataset,
        'artifacts': len(artifacts),
        'assignments': len(assignments),
        'results': len(results['results']),
        'codes': len(codes),
        'assignment_count': sum(len(a['code_ids']) for a in assignments),
        'evidence_spans': span_count,
        'taxonomy_leaves': (sum(len(g['children']) for g in taxonomy['children']) if dataset == 'CodeErrors' else len(taxonomy['children'])),
        'status': 'passed',
    }


def main():
    reports = [audit('CodeErrors', 557), audit('SATD', 856), audit('Privacy', 652)]
    print(json.dumps({'format': 'GPT6-1-compatible', 'datasets': reports,
                      'total_artifacts': sum(r['artifacts'] for r in reports),
                      'classification_by_this_script': False,
                      'all_checks': 'passed'}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
