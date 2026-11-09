"""Export deepseek-1 decisions in the GPT6-1 delivery layout.

This script does not classify.  It reads the existing analyst-authored codebook
and assignments, then serializes them into the six-file GPT6-1-compatible
structure, preserving all code IDs, evidence spans and reading decisions.
"""
from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter, OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'Artifact'
ANALYST = 'deepseek-1'
DATASETS = ['CodeErrors', 'SATD', 'Privacy']


def read_jsonl(path):
    return [json.loads(line) for line in path.open(encoding='utf-8') if line.strip()]


def write_json(path, obj):
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def sha(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def write_csv(path, header, rows):
    with path.open('w', encoding='utf-8', newline='') as target:
        writer = csv.writer(target)
        writer.writerow(header)
        for row in rows:
            writer.writerow(row)


def evidence_payload(assignment, artifacts_by_id):
    content = artifacts_by_id[assignment['artifact_id']]['content']
    result = []
    for ev in assignment['evidence']:
        quote = ev['quote']
        assert content[ev['start_char']:ev['end_char']] == quote
        result.append({
            'field': 'content',
            'quote': quote,
            'start_char': ev['start_char'],
            'end_char': ev['end_char'],
            'source': 'artifacts.jsonl',
            'field_sha256': sha(content),
        })
    return result


def taxonomy_from_codes(dataset, codes):
    """GPT6-1 taxonomy shape.  CodeErrors retains its explicit groups."""
    if dataset == 'CodeErrors':
        groups = OrderedDict()
        for code in codes:
            groups.setdefault(code.get('group', 'Failure mechanism'), []).append(code)
        children = []
        for group, members in groups.items():
            children.append({
                'category': group,
                'description': 'Organizational heading; not independently assigned.',
                'layer': 1,
                'children': [
                    {
                        'category': code['name'],
                        'description': code['definition'],
                        'layer': 2,
                        'children': [],
                        'code_id': code['code_id'],
                    }
                    for code in members
                ],
            })
        return {
            'category': 'Root',
            'description': 'Inductively consolidated failure mechanisms in the deepseek-1 CodeErrors codebook.',
            'layer': 0,
            'children': children,
        }
    return {
        'category': dataset,
        'description': f'Inductively consolidated observations from the deepseek-1 {dataset} corpus.',
        'layer': 0,
        'children': [
            {
                'category': code['name'],
                'description': code['definition'],
                'layer': 1,
                'children': [],
                'code_id': code['code_id'],
            }
            for code in codes
        ],
    }


def representative_evidence(dataset, code, assignments_by_artifact):
    if not code['artifact_ids']:
        return None
    for artifact_id in code['artifact_ids']:
        assignment = assignments_by_artifact[artifact_id]
        if assignment.get('evidence'):
            ev = assignment['evidence'][0]
            return {
                'case_id': artifact_id,
                'field': 'content',
                'start_char': ev['start_char'],
                'end_char': ev['end_char'],
                'quote': ev['quote'],
                'interpretation': assignment['analytic_memo'],
            }
    return None


def convert(dataset):
    base = OUT / dataset / ANALYST
    old_book = json.loads((base / 'codebook.json').read_text(encoding='utf-8'))
    artifacts = read_jsonl(base / 'artifacts.jsonl')
    assignments = read_jsonl(base / 'assignments.jsonl')
    artifacts_by_id = {row['artifact_id']: row for row in artifacts}
    assignments_by_id = {row['artifact_id']: row for row in assignments}
    codes = []
    for code in old_book['codes']:
        code = dict(code)
        if 'code_id' not in code:
            code['code_id'] = code['id']
        code['artifact_ids'] = code.get('artifact_ids', code.get('supporting_case_ids', code.get('supporting_cases', [])))
        code['artifact_count'] = code.get('artifact_count', code.get('case_count', len(code['artifact_ids'])))
        code['inclusion_criteria'] = code.get('inclusion_criteria', code.get('inclusion', ''))
        code['exclusion_criteria'] = code.get('exclusion_criteria', code.get('exclusion', ''))
        codes.append(code)

    # Re-derive membership from assignments, then assert the prior codebook agrees.
    members = OrderedDict((code['code_id'], []) for code in codes)
    for assignment in assignments:
        for code_id in assignment['code_ids']:
            members[code_id].append(assignment['artifact_id'])
    for code in codes:
        assert set(code['artifact_ids']) == set(members[code['code_id']]), code['code_id']
        assert code['artifact_count'] == len(members[code['code_id']]), code['code_id']

    if dataset == 'CodeErrors':
        code_rows = []
        for code in codes:
            code_rows.append({
                'id': code['code_id'],
                'group': code.get('group', 'Failure mechanism'),
                'name': code['name'],
                'name_zh': code.get('name_zh', code['name']),
                'definition': code['definition'],
                'inclusion': code['inclusion_criteria'],
                'exclusion': code['exclusion_criteria'],
                'supporting_case_ids': members[code['code_id']],
                'case_count': len(members[code['code_id']]),
                'representative_evidence': representative_evidence(dataset, code, assignments_by_id),
            })
        codebook = {
            'metadata': {
                'label': ANALYST,
                'dataset': 'llm_code_error_semantic',
                'research_question': 'What reusable failure mechanisms explain the supplied LLM-generated code errors?',
                'source_records': old_book['metadata'].get('source_records', 687),
                'solution_cases': len(artifacts),
                'tasks': old_book['metadata'].get('tasks', 150),
                'analysis_method': 'Single-analyst full-text reading, inductive consolidation, explicit per-artifact mapping and verbatim evidence review',
                'round': 1,
                'reading_order': 'ascending artifact row',
                'independent_blinded_replication': False,
                'human_reviewed': False,
                'model_identifier': 'deepseek-1 is the requested artifact label; the exact upstream generation parameters were not used for classification.',
                'api_calls_for_this_artifact': 0,
                'temperature': None,
                'seed': None,
                'resource_usage': None,
                'reference_categories_used_for_induction': False,
                'reference_implementations_read': True,
                'source_corpus_sha256': old_book['metadata'].get('corpus_sha256'),
                'unresolved_case_ids': [],
                'leaf_code_count': len(code_rows),
                'assignment_mode': 'multiple labels for separately evidenced defects; no duplicate parent/child assignments',
                'status': 'all cases coded',
                'artifact_revision': 1,
                'supplemental_resolution_case_ids': [],
                'resolution_record': None,
                'taxonomy_structure': None,
                'compatibility_note': 'GPT6-1-compatible serialization of the deepseek-1 codebook and assignments.',
            },
            'codes': code_rows,
        }
    else:
        code_rows = []
        for code in codes:
            code_rows.append({
                'code_id': code['code_id'],
                'name': code['name'],
                'definition': code['definition'],
                'inclusion_criteria': code['inclusion_criteria'],
                'exclusion_criteria': code['exclusion_criteria'],
                'artifact_count': len(members[code['code_id']]),
                'supporting_cases': members[code['code_id']],
            })
        codebook = {
            'metadata': {
                'dataset': dataset,
                'run': ANALYST,
                'artifact_count': len(artifacts),
                'coded_artifact_count': len(assignments),
                'code_count': len(code_rows),
                'assignment_count': sum(len(a['code_ids']) for a in assignments),
                'method': 'Inductive consolidation of individually authored full supplied-text reading notes, followed by explicit per-artifact assignment review. No keyword classifier or prior codebook assignments were used for consolidation.',
                'source_sha256': old_book['metadata'].get('corpus_sha256'),
                'source_path': f'work_ds1/corpus/{dataset.lower()}.jsonl',
                'independence': 'Single-analyst reconstruction; not a blinded independent replicate.',
                'limits': [
                    'Coverage refers to all supplied textual sections, not all content ever linked on the web.',
                    'Source revision ambiguity, inaccessible context, tentative proposals and absence of execution evidence remain in individual scope notes.',
                    'Coding is assistant-authored; it is not published human annotation, independently validated ground truth, or an experimental system run.',
                    'All artifacts are included; unspecified work and comments without established outstanding work are retained explicitly rather than invented as defects.',
                ],
            },
            'codes': code_rows,
        }

    taxonomy = taxonomy_from_codes(dataset, codes)
    codebook['metadata']['taxonomy_structure'] = taxonomy
    write_json(base / 'codebook.json', codebook)
    write_json(base / 'taxonomy.json', taxonomy)

    code_csv_header = (['id', 'group', 'name', 'name_zh', 'definition', 'inclusion', 'exclusion', 'case_count', 'supporting_case_ids']
                       if dataset == 'CodeErrors' else
                       ['code_id', 'name', 'definition', 'inclusion_criteria', 'exclusion_criteria', 'artifact_count', 'supporting_cases'])
    code_csv_rows = []
    for code in codebook['codes']:
        if dataset == 'CodeErrors':
            code_csv_rows.append([
                code['id'], code['group'], code['name'], code['name_zh'], code['definition'],
                code['inclusion'], code['exclusion'], code['case_count'],
                ';'.join(code['supporting_case_ids']),
            ])
        else:
            code_csv_rows.append([
                code['code_id'], code['name'], code['definition'], code['inclusion_criteria'],
                code['exclusion_criteria'], code['artifact_count'],
                json.dumps(code['supporting_cases'], ensure_ascii=False),
            ])
    write_csv(base / 'codebook.csv', code_csv_header, code_csv_rows)

    # GPT6-1 assignment records.  Preserve source-specific provenance fields.
    assignment_rows = []
    for assignment in assignments:
        artifact = artifacts_by_id[assignment['artifact_id']]
        if dataset == 'CodeErrors':
            row = {
                'case_id': assignment['artifact_id'],
                'source_error_ids': [assignment['artifact_id']],
                'task_id': int(assignment['task_id']) if str(assignment.get('task_id', '')).isdigit() else assignment.get('task_id'),
                'source_model': assignment.get('model'),
                'code_ids': assignment['code_ids'],
                'status': 'coded',
                'rationale': assignment['analytic_memo'],
                'evidence': evidence_payload(assignment, artifacts_by_id),
                'syntax_check': None,
                'witness_indices': [],
                'decision_basis': assignment.get('coding_basis'),
                'reviewed_in_round': 1,
                'open_codes': assignment['open_codes'],
            }
        else:
            row = {
                'case_id': assignment['artifact_id'],
                'index': assignment.get('row', 0) - 1,
                'code_ids': assignment['code_ids'],
                'code_names': [next(c['name'] for c in codes if c['code_id'] == cid) for cid in assignment['code_ids']],
                'status': 'coded',
                'coding_kind': 'assistant_authored_full_supplied_text_reading',
                'rationale': assignment['analytic_memo'],
                'scope_note': assignment.get('outcome', ''),
                'provisional_concepts': assignment['open_codes'],
                'provenance': {
                    'dataset': dataset,
                    'artifact_id': assignment['artifact_id'],
                    'row': assignment.get('row'),
                },
                'evidence': evidence_payload(assignment, artifacts_by_id),
                'read_fields': ['all supplied body and discussion text'],
                'external_follow_up': [],
                'open_codes': assignment['open_codes'],
            }
            if dataset == 'Privacy':
                row['evidence_availability'] = assignment.get('evidence_availability')
                row['reading_scope'] = assignment.get('reading_scope')
                row['outcome'] = assignment.get('outcome')
        assignment_rows.append(row)
    write_json(base / 'assignments.json', assignment_rows)
    if dataset == 'CodeErrors':
        write_csv(base / 'assignments.csv',
                  ['case_id', 'source_error_ids', 'task_id', 'source_model', 'codes', 'status', 'rationale'],
                  [[r['case_id'], ';'.join(r['source_error_ids']), r['task_id'], r['source_model'],
                    ';'.join(r['code_ids']), r['status'], r['rationale']] for r in assignment_rows])
    elif dataset == 'SATD':
        write_csv(base / 'assignments.csv',
                  ['index', 'case_id', 'code_ids', 'code_names', 'status', 'rationale', 'scope_note', 'evidence'],
                  [[r['index'], r['case_id'], json.dumps(r['code_ids'], ensure_ascii=False),
                    json.dumps(r['code_names'], ensure_ascii=False), r['status'], r['rationale'],
                    r['scope_note'], json.dumps(r['evidence'], ensure_ascii=False)] for r in assignment_rows])
    else:
        write_csv(base / 'assignments.csv',
                  ['index', 'case_id', 'code_ids', 'code_names', 'status', 'rationale', 'scope_note', 'evidence', 'evidence_availability', 'outcome'],
                  [[r['index'], r['case_id'], json.dumps(r['code_ids'], ensure_ascii=False),
                    json.dumps(r['code_names'], ensure_ascii=False), r['status'], r['rationale'],
                    r['scope_note'], json.dumps(r['evidence'], ensure_ascii=False),
                    r['evidence_availability'], r['outcome']] for r in assignment_rows])

    # Results: id, document, categories, code_ids, rationale, scope_note (+ CodeErrors fields).
    results = []
    for assignment in assignments:
        artifact = artifacts_by_id[assignment['artifact_id']]
        names = [next(c['name'] for c in codes if c['code_id'] == cid) for cid in assignment['code_ids']]
        if dataset == 'CodeErrors':
            results.append({
                'id': assignment['artifact_id'],
                'document': artifact['content'],
                'summary': assignment['analytic_memo'],
                'category': names[0] if names else '',
                'category_description': next((c['definition'] for c in codes if c['code_id'] == assignment['code_ids'][0]), ''),
                'categories': names,
                'code_ids': assignment['code_ids'],
                'status': 'coded',
                'source_error_ids': [assignment['artifact_id']],
            })
        else:
            results.append({
                'id': assignment['artifact_id'],
                'document': artifact['content'],
                'categories': names,
                'code_ids': assignment['code_ids'],
                'rationale': assignment['analytic_memo'],
                'scope_note': assignment.get('outcome', ''),
            })
    results_obj = {'metadata': codebook['metadata'], 'results': results}
    write_json(base / 'results.json', results_obj)
    return codebook, assignment_rows


def main():
    for dataset in DATASETS:
        book, rows = convert(dataset)
        print(dataset, 'codes', len(book['codes']), 'assignments', len(rows),
              'assignment_count', book['metadata'].get('assignment_count', sum(len(r['code_ids']) for r in rows)))


if __name__ == '__main__':
    main()
