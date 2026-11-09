"""Audit retained first-round outputs against every source record and HOW schemas."""
import ast
import csv
import gzip
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path

P = Path(__file__).resolve().parent
root = P.parent
out = root / 'GPT6-1'
corpus = json.loads((P / 'corpus.json').read_text())
ci = {c['case_id']: c for c in corpus}
source_path = root.parent / 'dataset/llm_code_error_semantic/llm_code_error_semantic.json'
source = json.loads(source_path.read_text())
si = {str(r['id']): r for r in source}
assert len(si) == len(source) == 687
source_groups = defaultdict(list)
for row in source:
    source_groups[(row['task_id'], row['model'], row['incorrect_code'])].append(str(row['id']))
assert len(source_groups) == len(corpus) == len(ci) == 557
ids = [i for c in corpus for i in c['source_ids']]
assert len(ids) == len(set(ids)) == 687 and set(ids) == set(si)
for c in corpus:
    assert set(c['source_ids']) == set(source_groups[(c['task_id'], c['model'], c['incorrect_code'])])
    assert c['case_id'] == min(c['source_ids'], key=int)
    for i in c['source_ids']:
        for k in ['task_id', 'model', 'task_description', 'incorrect_code', 'ground_truth_code', 'source_file']:
            assert c[k] == si[i][k]
    assert 'category' not in c
observations = list(csv.DictReader((P / 'observations-1.tsv').open(), delimiter='\t'))
assert len(observations) == len({r['case_id'] for r in observations}) == 557
assert {r['case_id'] for r in observations} == set(ci)
pairs = [line.split() for line in (P / 'round1-map.txt').read_text().splitlines() if line and not line.startswith('#')]
assert len(pairs) == len(dict(pairs)) == 557 and set(dict(pairs)) == set(ci)
assert {f.stem for f in (P / 'cases').glob('*.txt')} == set(ci)
resolutions = {r['case_id']: r for r in json.loads((P / 'pending_case_resolutions.json').read_text())['cases']}
baseline = json.loads((P / 'pending_resolution_baseline.json').read_text())
book = json.loads((out / 'codebook.json').read_text())
codes = {c['id']: c for c in book['codes']}
a = json.loads((out / 'assignments.json').read_text())
byid = {x['case_id']: x for x in a}
assert len(a) == len(byid) == 557 and set(byid) == set(ci)
for x in a:
    c = ci[x['case_id']]
    expected_labels = dict(pairs)[x['case_id']]
    assert x['code_ids'] == (resolutions[x['case_id']]['code_ids'] if x['case_id'] in resolutions else ([] if expected_labels == 'U' else expected_labels.split(',')))
    if x['case_id'] not in resolutions:
        assert hashlib.sha256(json.dumps(x, sort_keys=True, ensure_ascii=False).encode()).hexdigest() == baseline['record_sha256'][x['case_id']]
    assert x['source_error_ids'] == c['source_ids']
    assert x['task_id'] == c['task_id'] and x['source_model'] == c['model']
    assert set(x['code_ids']) <= codes.keys()
    assert (x['status'] == 'unresolved') == (len(x['code_ids']) == 0)
    assert x['reviewed_in_round'] == 1
    for e in x['evidence']:
        field_text = c[e['field']]
        expected_quote = field_text if e['line_start'] == 1 and e['line_end'] == len(field_text.splitlines()) else '\n'.join(field_text.splitlines()[e['line_start'] - 1:e['line_end']])
        assert e['quote'] == expected_quote
        assert e['sha256'] == hashlib.sha256(e['quote'].encode()).hexdigest()
        assert (out / e['path']).is_file()
for k, c in codes.items():
    expected = {x['case_id'] for x in a if k in x['code_ids']}
    assert expected == set(c['supporting_case_ids']) and len(expected) == c['case_count']
    e = c['representative_evidence']
    assert ci[e['case_id']]['incorrect_code'].splitlines()[e['line_start'] - 1] == e['quote']

def walk(t, depth=0):
    assert set(t) == {'category', 'description', 'layer', 'children'} and t['layer'] == depth
    assert isinstance(t['category'], str) and isinstance(t['description'], str)
    assert isinstance(t['children'], list)
    for child in t['children']:
        walk(child, depth + 1)

tree = json.loads((out / 'taxonomy.json').read_text())
walk(tree)
walk(json.loads((P / 'how-format/example_taxonomy.json').read_text()))
assert {(g['category'], c['category'], c['description']) for g in tree['children'] for c in g['children']} == {(c['group'], c['name'], c['definition']) for c in codes.values()}
# Check official output source contains the fields being compared, without importing its dependencies.
required = {'id', 'document', 'summary', 'category', 'category_description'}
for filename in ['tnt_output.py', 'climb_output.py']:
    parsed = ast.parse((P / 'how-format' / filename).read_text())
    keys = {n.value for n in ast.walk(parsed) if isinstance(n, ast.Constant) and isinstance(n.value, str)}
    assert {'metadata', 'results'} <= keys
    if filename == 'tnt_output.py':
        assert required <= keys and 'taxonomy_structure' in keys
r = json.loads((out / 'results.json').read_text())
assert set(r) == {'metadata', 'results'} and r['metadata']['taxonomy_structure'] == tree
assert len(r['results']) == len({x['id'] for x in r['results']}) == 557
for x in r['results']:
    assignment = byid[x['id']]
    assert required <= x.keys()
    assert x['document'] == (P / 'cases' / f"{x['id']}.txt").read_text()
    assert x['summary'] == assignment['rationale']
    assert x['code_ids'] == assignment['code_ids'] and x['status'] == assignment['status']
    assert x['source_error_ids'] == assignment['source_error_ids']
    paths = [codes[k]['group'] + ' -> ' + codes[k]['name'] for k in assignment['code_ids']]
    assert x['categories'] == paths and x['category'] == (paths[0] if paths else '')
    assert x['category_description'] == (codes[assignment['code_ids'][0]]['definition'] if paths else '')

upstream = P / 'humaneval-evidence'
provenance = json.loads((upstream / 'provenance.json').read_text())
archive_bytes = (upstream / 'HumanEval.jsonl.gz').read_bytes()
assert hashlib.sha256(archive_bytes).hexdigest() == provenance['source_sha256']
official = {r['task_id']: r for r in map(json.loads, gzip.decompress(archive_bytes).decode().splitlines())}
verification = {r['case_id']: r for r in json.loads((P / 'pending_case_verification.json').read_text())}
assert set(resolutions) == {'393', '729'}
for cid, decision in resolutions.items():
    task_path = upstream / (str(ci[cid]['task_id']) + '.json')
    assert json.loads(task_path.read_text()) == official['HumanEval/' + str(ci[cid]['task_id'])]
    checked = verification[cid]
    assert checked['source_code_sha256'] == hashlib.sha256(ci[cid]['incorrect_code'].encode()).hexdigest()
    assert checked['upstream_task_sha256'] == hashlib.sha256(task_path.read_bytes()).hexdigest()
    assert byid[cid]['supplemental_resolution'] == decision
assert verification['729']['checks']['incorrect_code']['official_test']['passed_count'] == 6
assert verification['729']['checks']['ground_truth_code']['official_test']['passed_count'] == 7
assert abs(verification['393']['checks']['incorrect_code']['witness']['value'] + 100) > 1
unresolved = [x['case_id'] for x in a if x['status'] == 'unresolved']
report = {
    'retained_result': 'GPT6-1',
    'source_records': len(source),
    'expected_artifacts': len(source_groups),
    'recorded_artifacts': len(a),
    'missing_artifact_ids': sorted(set(ci) - set(byid)),
    'extra_artifact_ids': sorted(set(byid) - set(ci)),
    'duplicate_artifact_ids': len(a) - len(byid),
    'source_records_covered': len(ids),
    'observation_records': len(observations),
    'mapping_records': len(pairs),
    'tasks': len({c['task_id'] for c in corpus}),
    'coded_artifacts': sum(x['status'] == 'coded' for x in a),
    'unresolved_artifact_ids': unresolved,
    'supplementally_resolved_case_ids': sorted(resolutions),
    'other_555_assignments_unchanged': True,
    'unresolved_source_record_ids': [i for x in a if x['status'] == 'unresolved' for i in x['source_error_ids']],
    'code_count': len(codes),
    'navigation_group_count': len(tree['children']),
    'taxonomy_nodes_excluding_root': len(tree['children']) + len(codes),
    'assignment_count': sum(len(x['code_ids']) for x in a),
    'artifacts_by_label_count': dict(sorted(Counter(len(x['code_ids']) for x in a).items())),
    'all_source_fields_match': True,
    'all_evidence_quotes_and_checksums_match': True,
    'all_results_match_assignments': True,
    'how_taxonomy_node_schema_matches': True,
    'how_result_core_fields_match': True,
    'how_format_differences': [
        'Four parent nodes are navigation groups rather than independently assigned codes.',
        'Multiple code_ids/categories extend the upstream single category field.',
        'The compatibility category retains only the first-listed code; no priority is established.',
        'Both initial deferrals are resolved with supplemental evidence; explicit status remains in every record.',
        'Summary contains analyst rationale rather than a separate source-summary agent output.',
        'Original API generation settings and usage were not captured; this is an assistant-session analysis.',
    ],
    'second_round_output_present': (root / 'GPT6-2').exists(),
    'source_dataset_sha256': hashlib.sha256(source_path.read_bytes()).hexdigest(),
    'corpus_sha256': hashlib.sha256((P / 'corpus.json').read_bytes()).hexdigest(),
    'assignments_sha256': hashlib.sha256((out / 'assignments.json').read_bytes()).hexdigest(),
}
assert not report['second_round_output_present']
(root / 'coverage_audit.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
checks = []
for f in sorted(root.rglob('*')):
    if f.is_file() and f.name != 'SHA256SUMS' and '__pycache__' not in str(f):
        checks.append(hashlib.sha256(f.read_bytes()).hexdigest() + '  ' + str(f.relative_to(root)))
(root / 'SHA256SUMS').write_text('\n'.join(checks) + '\n')
print(json.dumps(report, ensure_ascii=False, indent=2))
print('PASS; retained output coverage, HOW schema and file checksums verified')
