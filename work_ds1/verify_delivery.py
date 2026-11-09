"""Independent structural audit of the deepseek-1 delivery.

This program does not assign codes.  It checks the delivered files against the
frozen corpora, code definitions, explicit memberships and verbatim evidence.
"""
from __future__ import annotations

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


def audit(dataset, expected, source_name):
    base = OUT / dataset / ANALYST
    artifacts = read_jsonl(base / 'artifacts.jsonl')
    assignments = read_jsonl(base / 'assignments.jsonl')
    book = json.loads((base / 'codebook.json').read_text(encoding='utf-8'))
    coverage = json.loads((base / 'coverage_report.json').read_text(encoding='utf-8'))
    assert len(artifacts) == len(assignments) == expected, (len(artifacts), len(assignments), expected)
    artifact_by_id = {row['artifact_id']: row for row in artifacts}
    assignment_by_id = {row['artifact_id']: row for row in assignments}
    assert len(artifact_by_id) == len(assignment_by_id) == expected
    assert set(artifact_by_id) == set(assignment_by_id)
    assert coverage['expected_artifacts'] == coverage['coded_artifacts'] == expected
    assert coverage['unassigned_artifacts'] == 0
    assert not coverage['missing_rows']
    assert not coverage['duplicate_rows']
    assert not coverage['undefined_codes']

    codes = {}
    for row in book['codes']:
        row = dict(row)
        code_id = row.get('code_id', row.get('id'))
        row['code_id'] = code_id
        row['inclusion_criteria'] = row.get('inclusion_criteria', row.get('inclusion', ''))
        row['exclusion_criteria'] = row.get('exclusion_criteria', row.get('exclusion', ''))
        row['artifact_ids'] = row.get('artifact_ids', row.get('supporting_case_ids', row.get('supporting_cases', [])))
        row['artifact_count'] = row.get('artifact_count', row.get('case_count', len(row['artifact_ids'])))
        codes[code_id] = row
    assert len(codes) == book.get('code_count', len(book['codes']))
    for code_id, code in codes.items():
        assert code['definition'].strip()
        assert code['inclusion_criteria'].strip()
        assert code['exclusion_criteria'].strip()
        assert code['artifact_count'] == len(code['artifact_ids'])
        assert len(set(code['artifact_ids'])) == len(code['artifact_ids'])

    members = {code_id: set(code['artifact_ids']) for code_id, code in codes.items()}
    span_count = 0
    for artifact_id, assignment in assignment_by_id.items():
        artifact = artifact_by_id[artifact_id]
        assert assignment['code_ids']
        assert assignment['open_codes']
        assert assignment['analytic_memo'].strip()
        assert sha(artifact['content']) == assignment['content_sha256']
        assert assignment['content_sha256'] == hashlib.sha256(artifact['content'].encode('utf-8')).hexdigest()
        forward = set(assignment['code_ids'])
        reverse = {code_id for code_id, ids in members.items() if artifact_id in ids}
        assert forward == reverse, (artifact_id, forward, reverse)
        assert forward <= set(codes)
        for evidence in assignment['evidence']:
            quote = evidence['quote']
            start, end = evidence['start_char'], evidence['end_char']
            assert artifact['content'][start:end] == quote, (artifact_id, start, end)
            assert quote
            span_count += 1
    assert set(members) == set(codes)
    for code_id, ids in members.items():
        for artifact_id in ids:
            assert code_id in assignment_by_id[artifact_id]['code_ids']
    assert sum(len(row['code_ids']) for row in assignments) == coverage['assignment_count']
    assert span_count == coverage['evidence_quotes_checked']
    return {
        'dataset': dataset,
        'artifacts': len(artifacts),
        'unique_ids': len(artifact_by_id),
        'codes': len(codes),
        'assignments': sum(len(row['code_ids']) for row in assignments),
        'multi_label_artifacts': sum(len(row['code_ids']) > 1 for row in assignments),
        'evidence_spans': span_count,
        'status': 'passed',
    }


def main():
    reports = [
        audit('CodeErrors', 557, 'codeerrors'),
        audit('SATD', 856, 'satd'),
        audit('Privacy', 652, 'privacy'),
    ]
    # Cross-check frozen corpora.
    for dataset, name, expected in [('CodeErrors', 'codeerrors', 557), ('SATD', 'satd', 856), ('Privacy', 'privacy', 652)]:
        corpus = read_jsonl(ROOT / 'work_ds1' / 'corpus' / f'{name}.jsonl')
        delivered = read_jsonl(OUT / dataset / ANALYST / 'artifacts.jsonl')
        assert len(corpus) == len(delivered) == expected
        assert [x['artifact_id'] for x in corpus] == [x['artifact_id'] for x in delivered]
        assert [x['content'] for x in corpus] == [x['content'] for x in delivered]
        assert hashlib.sha256((ROOT / 'work_ds1' / 'corpus' / f'{name}.jsonl').read_bytes()).hexdigest() == hashlib.sha256((OUT / dataset / ANALYST / 'artifacts.jsonl').read_bytes()).hexdigest()
    # Dataset-specific checks.
    ce = read_jsonl(OUT / 'CodeErrors' / ANALYST / 'assignments.jsonl')
    assert len({row['task_id'] for row in ce}) == 150
    assert all(row['evidence'] for row in ce)
    satd = read_jsonl(OUT / 'SATD' / ANALYST / 'assignments.jsonl')
    assert len({row['row'] for row in satd}) == 856
    privacy = read_jsonl(OUT / 'Privacy' / ANALYST / 'assignments.jsonl')
    assert Counter(row['evidence_availability'] for row in privacy) == {'complete': 633, 'partial': 19}
    print(json.dumps({'datasets': reports, 'total_artifacts': sum(x['artifacts'] for x in reports),
                      'classification_by_this_script': False, 'all_checks': 'passed'}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
