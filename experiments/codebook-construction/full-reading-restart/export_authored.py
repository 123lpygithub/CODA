"""Package authored decisions and source references; never infer categories."""
import argparse
import csv
import hashlib
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

def export(dataset):
    root = HERE / dataset
    spec = importlib.util.spec_from_file_location('authored_' + dataset, root / 'consolidation.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    decisions = module.decisions()
    source = HERE.parent / dataset / 'input' / 'corpus.json'
    corpus = json.loads(source.read_text())
    notes = []
    for name in ('reading_notes.jsonl','reading_notes_staged.jsonl'):
        p = root / name
        if p.exists(): notes.extend(json.loads(line) for line in p.read_text().splitlines() if line.strip())
    by_index = {n['index']: n for n in notes}
    assert len(notes) == len(by_index) == len(corpus)
    assert set(decisions) == set(by_index) == set(range(len(corpus)))
    assert len({c['artifact_id'] for c in corpus}) == len(corpus)
    names = {r[0]:r[1] for r in module.CATEGORIES}
    entries = []
    for key,name,definition,include,exclude in module.CATEGORIES:
        members = [corpus[i]['artifact_id'] for i in range(len(corpus)) if key in decisions[i]]
        assert members, key
        entries.append(dict(code_id=key,name=name,definition=definition,
            inclusion_criteria=include,exclusion_criteria=exclude,
            artifact_count=len(members),supporting_cases=members))
    assignments=[]
    for i, case in enumerate(corpus):
        note = by_index[i]
        fields={s['field']:s for s in case['sections']}
        assert case['artifact_id']==note['artifact_id']
        assert set(note['read_fields'])==set(fields)
        evidence=[]
        for e in note['evidence']:
            section=fields[e['field']]
            assert e['quote'] and e['quote'] in section['text'], (i,e)
            evidence.append(dict(**e,source=section.get('source'),
                field_sha256=hashlib.sha256(section['text'].encode()).hexdigest()))
        # Retain the complete selected comment when the earlier note quote alone is narrow.
        if 'comment_text' in fields and fields['comment_text']['text']:
            section=fields['comment_text']
            if not any(e['field']=='comment_text' and e['quote']==section['text'] for e in evidence):
                evidence.append(dict(field='comment_text',quote=section['text'],source=section.get('source'),
                    field_sha256=hashlib.sha256(section['text'].encode()).hexdigest()))
        assignments.append(dict(case_id=case['artifact_id'],index=i,code_ids=decisions[i],
            code_names=[names[k] for k in decisions[i]],status='coded',
            coding_kind='assistant_authored_full_supplied_text_reading',
            rationale=note['interpretation'],scope_note=note['qualification'],
            provisional_concepts=note['provisional_concepts'],provenance=case['provenance'],
            evidence=evidence,read_fields=note['read_fields'],
            external_follow_up=note.get('follow_up_sources',note.get('external_follow_up',[]))))
        for key in ('supplemental_interpretation', 'visual_evidence', 'visual_sources',
                    'read_pages', 'supplemental_reading_audit'):
            if key in note:
                assignments[-1][key] = note[key]
    metadata=dict(dataset=dataset,run='GPT6-1',artifact_count=len(corpus),coded_artifact_count=len(assignments),
        code_count=len(entries),assignment_count=sum(len(a['code_ids']) for a in assignments),
        method='Inductive consolidation of individually authored full supplied-text reading notes, followed by explicit per-artifact assignment review. No keyword classifier, external model API, or prior codebook assignments were used for consolidation.',
        source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
        source_path=str(source.relative_to(HERE.parent.parent.parent)),
        independence='Reconstruction within the same conversation; not a blinded independent replicate.',
        limits=['Coverage refers to all supplied textual sections, not all content ever linked on the web.',
                'Source revision ambiguity, inaccessible context, tentative proposals and absence of execution evidence remain in individual scope notes.',
                'Coding is assistant-authored; it is not published human annotation, independently validated ground truth, or an experimental system run.',
                'All artifacts are included; unspecified work and comments without established outstanding work are retained explicitly rather than invented as defects.'])
    if dataset == 'Privacy':
        metadata['limits'][-1] = ('All artifacts are included. Reports, proposals, disputed or retracted claims, '
            'implementation evidence and missing context remain distinct; coding a concern does not confirm a violation or a completed fix.')
        metadata['limits'].append('Exact duplicate supplemental text was read once with reconstruction maps. '
            'Long CSS and dependency metadata used reversible lexical views; integrity digests were retained as opaque literals, not verified. '
            'Linked images or external pages not inspected are explicitly qualified; runtime behavior was not reproduced.')
    out=root/'export'/'GPT6-1';out.mkdir(parents=True,exist_ok=True)
    def dump(name,obj): (out/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
    dump('codebook.json',dict(metadata=metadata,codes=entries))
    dump('assignments.json',assignments)
    dump('results.json',dict(metadata=metadata,results=[dict(id=a['case_id'],document='\n\n'.join(s['field']+'\n'+s['text'] for s in corpus[a['index']]['sections']),categories=a['code_names'],code_ids=a['code_ids'],rationale=a['rationale'],scope_note=a['scope_note']) for a in assignments]))
    dump('taxonomy.json',dict(category=dataset,description='Inductively consolidated observations from the supplied corpus.',layer=0,
        children=[dict(category=e['name'],description=e['definition'],layer=1,children=[]) for e in entries]))
    with (out/'codebook.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['code_id','name','definition','inclusion_criteria','exclusion_criteria','artifact_count','supporting_cases']);w.writeheader()
        for e in entries:w.writerow({**e,'supporting_cases':json.dumps(e['supporting_cases'])})
    with (out/'assignments.csv').open('w',newline='') as f:
        keys=['index','case_id','code_ids','code_names','status','rationale','scope_note','evidence']
        w=csv.DictWriter(f,fieldnames=keys);w.writeheader()
        for a in assignments:w.writerow({k:json.dumps(a[k],ensure_ascii=False) if isinstance(a[k],list) else a[k] for k in keys})
    lines=[f'# {dataset} — GPT6-1', '',f'{len(corpus)} artifacts; {len(entries)} codes; {metadata["assignment_count"]} artifact–code assignments.','',metadata['method'],'',
        'Every supplied artifact has an assignment. Codes describe the observed work, concern, or evidence status; they do not establish that a defect was reproduced. Refer to `assignments.json` for individual reasoning, qualifications, source references and evidence.','',
        '## Scope','']+['- '+s for s in metadata['limits']]+['',metadata['independence'],'','## Codebook','',
        '| Code | Name | Artifacts |','|---|---|---:|']
    lines += [f'| {e["code_id"]} | {e["name"]} | {e["artifact_count"]} |' for e in entries]
    for e in entries:
        examples=[a for a in assignments if e['code_id'] in a['code_ids']][:2]
        lines += ['',f'## {e["code_id"]} — {e["name"]}','',e['definition'],'', '**Include:** '+e['inclusion_criteria'],'','**Exclude:** '+e['exclusion_criteria'],'','**Examples:**','']
        lines += [f'- `{a["case_id"]}`: {a["rationale"]} Qualification: {a["scope_note"]}' for a in examples]
    (out/'codebook.md').write_text('\n'.join(lines)+'\n')
    validation=dict(dataset=dataset,source_sha256=metadata['source_sha256'],artifacts=len(corpus),codes=len(entries),
        assignments=metadata['assignment_count'],missing_artifacts=[],duplicate_artifacts=[],invalid_code_references=[],quote_mismatches=[],
        scope='Mechanical coverage, membership and exact quotation integrity; not independent semantic or human validation.',
        output_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in out.iterdir() if p.is_file()})
    (root/'export_validation.json').write_text(json.dumps(validation,indent=2)+'\n')
    print(json.dumps(validation,indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('dataset',choices=['SATD','Privacy']);export(p.parse_args().dataset)
