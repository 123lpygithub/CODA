"""Package manually authored analysis; no model calls or text classification."""
from pathlib import Path
import csv, json, hashlib, collections
w = Path(__file__).resolve().parents[1]
d = w / 'direct-analysis/Privacy'
out = w.parents[1] / 'Artifact/Privacy/GPT6-1'
out.mkdir(parents=True, exist_ok=True)
corpus_path = w / 'Privacy/input/corpus.json'
corpus = json.loads(corpus_path.read_text())
obs = {r['index']: r for r in map(json.loads, (d/'observations.jsonl').read_text().splitlines())}
primary = {int(i): a for i, a in map(str.split, (d/'primary_mapping.txt').read_text().splitlines())}
secondary = {int(i): letters for i, letters in json.loads((d/'secondary_mapping.json').read_text()).items()}
defs = []
for line in (d/'category_definitions.tsv').read_text().splitlines():
    a, group, name, definition, inclusion, exclusion = line.split('\t')
    defs.append(dict(id=f'P{ord(a)-64:02d}', letter=a, group=group, name=name, definition=definition,
                     inclusion=inclusion, exclusion=exclusion,
                     kind='evidence_qualification' if a == 'U' else 'substantive_concern'))
by = {c['letter']: c for c in defs}
assert set(obs) == set(primary) == set(range(652))
assignments = []
ledger = []
for i, x in enumerate(corpus):
    r = obs[i]
    assert r['artifact_id'] == x['artifact_id']
    letters = [primary[i]] + secondary.get(i, [])
    assert len(letters) == len(set(letters))
    evidence, supplemental = [], []
    for sn, s in enumerate(x['sections']):
        read = s['field'] in r['read_fields']
        item = dict(section_index=sn, field=s['field'], quote=s['text'], source=s.get('source'), scope=s.get('scope'))
        if read:
            item['review_scope'] = 'Primary discussion or selected supplemental section; repetitive logs/code outputs may be sampled as stated in scope_note.'
            evidence.append(item)
        else:
            item['review_scope'] = 'Retained source context; not independently read or asserted as supporting evidence.'
            supplemental.append(item)
    assignments.append(dict(case_id=x['artifact_id'], index=i, code_ids=[by[a]['id'] for a in letters],
                            primary_code_id=by[letters[0]]['id'], status='coded',
                            coding_kind=by[letters[0]]['kind'], rationale=r['interpretation'],
                            scope_note=r['scope_note'], provisional_concept=r['provisional_concept'],
                            provenance=x['provenance'], evidence=evidence,
                            supplemental_context=supplemental, supplemental_review=r['supplemental_review']))
    ledger.append(dict(index=i, case_id=x['artifact_id'], reviewed_fields=r['read_fields'],
                       retained_unreviewed_fields=[s['field'] for s in supplemental],
                       scope_note=r['scope_note'], supplemental_review=r['supplemental_review']))
representatives = dict(A=[11,567,607], B=[98,556,585], C=[21,632,651], D=[76,603,635],
                       E=[45,534,561], F=[26,269,484], G=[55,557,644], H=[126,549,643],
                       I=[234,528,595], J=[71,492,636], K=[27,442,626], L=[64,438,648],
                       M=[24,542,612], N=[12,357,586], O=[52,465,625], P=[34,505,623],
                       Q=[101,135,369], R=[236,547,621], S=[44,553,647], T=[172,196,401],
                       U=[93,256,611])
for c in defs:
    supporting = [a for a in assignments if c['id'] in a['code_ids']]
    c['supporting_case_ids'] = [a['case_id'] for a in supporting]
    c['case_count'] = len(supporting)
    c['primary_case_count'] = sum(a['primary_code_id'] == c['id'] for a in assignments)
    c['representative_evidence'] = []
    for i in representatives[c['letter']]:
        a = assignments[i]
        assert c['id'] in a['code_ids']
        c['representative_evidence'].append(dict(case_id=a['case_id'], interpretation=a['rationale'],
                                                scope_note=a['scope_note'], source=a['provenance'],
                                                evidence_fields=[e['field'] for e in a['evidence']]))
qualified = [a['case_id'] for a in assignments if a['coding_kind'] == 'evidence_qualification']
meta = dict(label='GPT6-1', dataset='Privacy', round=1,
    research_question='What reusable privacy concerns, implementation requirements and evidence qualifications are expressed in the supplied software-project issues and discussions?',
    artifact_count=len(corpus), assignment_count=sum(len(a['code_ids']) for a in assignments),
    code_count=len(defs), substantive_code_count=20, evidence_qualification_code_count=1,
    substantively_coded_artifacts=len(corpus)-len(qualified), evidence_qualified_artifacts=len(qualified),
    analysis_method='Direct assistant reading of primary issue discussions, per-artifact observations, selective supplemental-source checks, inductive consolidation and manually authored assignments. Scripts only package and validate the authored analysis.',
    external_model_api_calls=0, human_reference_labels_used=False, human_reviewed=False,
    label_note='GPT6-1 is the user-requested output label; it does not attest to a separately invoked model endpoint.',
    source_corpus_sha256=hashlib.sha256(corpus_path.read_bytes()).hexdigest(), source_profile='paper-20261106-v10',
    scope='All 652 artifact records are coded. Available primary titles, bodies and discussions were reviewed; repetitive diagnostic blocks were inspected selectively where noted. Selected linked source excerpts were checked. Other supplemental material is retained but not claimed to have been read. Images referenced by Markdown were not independently visually inspected.',
    limitations=[
        'Current retrievable discussions may include later changes and are not the original study historical snapshot; GH Archive records can be incomplete or contain conflicting context.',
        'Codes describe supported concerns, requests or discussions, not confirmed defects, legal determinations or independently verified remediation.',
        'P21 explicitly retains records whose supplied evidence does not establish a specific privacy issue. Full coding coverage is not equivalent to every artifact establishing a substantive defect.',
        'Quoted source contains participant claims; inclusion as evidence does not endorse those claims. Source patches are not runtime verification.',
        'This is one assistant analysis without an external LLM API or independent human validation. No human reference codebook or fixed category cap was used.'])
def dump(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n')
dump(out/'codebook.json', dict(metadata=meta, codes=defs))
dump(out/'assignments.json', assignments)
root = dict(category='Root', description=meta['research_question'], layer=0, children=[])
for group in dict.fromkeys(c['group'] for c in defs):
    root['children'].append(dict(category=group, description='Organizational heading; not independently assigned.', layer=1,
       children=[dict(category=c['name'], description=c['definition'], layer=2, children=[]) for c in defs if c['group']==group]))
dump(out/'taxonomy.json', root)
dump(out/'results.json', dict(metadata=meta, results=[dict(id=a['case_id'],
    document='\n\n'.join('['+s['field']+']\n'+s['text'] for s in x['sections']),
    code_ids=a['code_ids'], categories=[next(c['name'] for c in defs if c['id']==cid) for cid in a['code_ids']],
    rationale=a['rationale'], scope_note=a['scope_note'], reviewed_fields=obs[a['index']]['read_fields'])
    for x,a in zip(corpus,assignments)]))
with (out/'codebook.csv').open('w', newline='') as f:
    fields=['id','group','name','definition','inclusion','exclusion','kind','primary_case_count','case_count']
    writer=csv.DictWriter(f, fieldnames=fields, extrasaction='ignore');writer.writeheader();writer.writerows(defs)
with (out/'assignments.csv').open('w', newline='') as f:
    fields=['case_id','index','primary_code_id','code_ids','status','coding_kind','rationale','scope_note']
    writer=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');writer.writeheader()
    writer.writerows({**a,'code_ids':';'.join(a['code_ids'])} for a in assignments)
md=['# Privacy — GPT6-1','',
    f"All **652 artifacts** are included in **{meta['assignment_count']} assignments** to **21 codes**: 20 substantive concern codes and one evidence-qualification code. **{len(qualified)} artifacts** receive the latter because a specific privacy issue is unsupported or corrected in the available record.",'',
    'Categories were induced from direct reading of issue material. They describe concerns and implementation needs, whether proposed, contested, corrected or reportedly resolved. They do not label every issue as a confirmed privacy violation. One primary code identifies each case’s principal concern; additional codes capture explicitly distinct concerns in broader discussions. No fixed code-count cap or reference human categories were used.','',
    '`assignments.json` separates reviewed evidence from retained supplemental context and preserves case rationale, caveats, source locations and provenance. `results.json` retains the full supplied text for every artifact and the reviewed-field list. `taxonomy.json` uses a category/description/layer/children presentation compatible with the requested HOW-style organization; it is not a reproduction of HOW’s generation procedure.','',
    '| Code | Category | Primary artifacts | All supporting artifacts |','|---|---|---:|---:|']
for c in defs: md.append(f"| {c['id']} | {c['name']} | {c['primary_case_count']} | {c['case_count']} |")
md+=['','Primary counts sum to 652. Supporting counts overlap where a case has more than one distinct concern. Group headings organize the codebook and are not assigned codes.','']
for c in defs:
    md += [f"## {c['id']} — {c['name']}",'',c['definition'],'',f"**Include:** {c['inclusion']}",'',
           f"**Exclude/boundary:** {c['exclusion']}",'',f"**Supporting artifacts:** {c['case_count']}; primary in {c['primary_case_count']}. Full IDs are in the structured codebook.",'']
    for e in c['representative_evidence']:
        md += [f"- `{e['case_id']}`: {e['interpretation']} Scope: {e['scope_note']}"]
    md+=['']
md+=['## Method and limits','',meta['scope'],'',*['- '+x for x in meta['limitations']], '',
     'Coverage, source-text equality and references are checked programmatically. These checks do not constitute independent semantic review. Process notes and audits are stored outside Artifact under experiments/codebook-construction/direct-analysis/Privacy.']
(out/'codebook.md').write_text('\n'.join(md)+'\n')
assert len({a['case_id'] for a in assignments})==652
assert all(a['code_ids'] and set(a['code_ids']) <= {c['id'] for c in defs} for a in assignments)
assert sum(c['primary_case_count'] for c in defs)==652
for x,a in zip(corpus,assignments):
    sections=a['evidence']+a['supplemental_context']
    assert sorted(e['section_index'] for e in sections)==list(range(len(x['sections'])))
    for e in sections: assert e['quote']==x['sections'][e['section_index']]['text']
dump(d/'reading_scope.json', dict(scope=meta['scope'], artifacts=ledger))
audit=dict(artifacts=652,covered=652,missing=[],duplicates=[],assignments=meta['assignment_count'],codes=len(defs),
           substantive_codes=20,evidence_qualification_codes=1,evidence_qualified_artifacts=len(qualified),
           verbatim_evidence_check='passed',reference_check='passed',coverage_check='passed',
           output_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in out.iterdir() if p.is_file()})
dump(d/'audit.json',audit)
dump(d/'status.json',dict(state='complete',reviewed_primary_artifacts=652,total_artifacts=652,final_codebook_exported=True,output=str(out),method=meta['analysis_method']))
print(json.dumps(audit,indent=2))
