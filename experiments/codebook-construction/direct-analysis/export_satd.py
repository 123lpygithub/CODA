from pathlib import Path
import csv,json,hashlib,collections
w=Path(__file__).resolve().parents[1];d=w/'direct-analysis/SATD';out=w.parents[1]/'Artifact/SATD/GPT6-1';out.mkdir(parents=True,exist_ok=True)
corpus=json.loads((w/'SATD/input/corpus.json').read_text());obs={r['index']:r for r in map(json.loads,(d/'observations.jsonl').read_text().splitlines())}
primary={int(i):a for i,a in map(str.split,(d/'primary_mapping.txt').read_text().splitlines())}
# Secondary assignments are manually selected for distinct concerns explicitly present in the same artifact.
secondary={71:['G'],78:['M'],260:['H'],296:['K'],304:['F'],312:['K'],424:['O'],638:['G'],678:['I'],712:['G'],717:['E'],755:['I'],846:['J']}
defs=[]
for line in (d/'category_definitions.tsv').read_text().splitlines():
 a,g,n,de,inc,exc=line.split('\t');defs.append(dict(id='S%02d'%(ord(a)-64),letter=a,group=g,name=n,definition=de,inclusion=inc,exclusion=exc,kind='evidence_qualification' if a in 'UV' else 'substantive_concern'))
by={r['letter']:r for r in defs};assignments=[]
for i,x in enumerate(corpus):
 r=obs[i];assert r['artifact_id']==x['artifact_id'];letters=[primary[i]]+secondary.get(i,[]);evidence=[]
 for sn,s in enumerate(x['sections']):
  evidence.append(dict(section_index=sn,field=s['field'],quote=s['text'],source=s.get('source'),scope=s.get('scope')))
 assignments.append(dict(case_id=x['artifact_id'],index=i,code_ids=[by[a]['id'] for a in letters],status='coded',coding_kind=by[letters[0]]['kind'],rationale=r['interpretation'],scope_note=r['scope_note'],provisional_concept=r['provisional_concept'],provenance=x['provenance'],evidence=evidence))
for code in defs:
 support=[a for a in assignments if code['id'] in a['code_ids']];code['supporting_case_ids']=[a['case_id'] for a in support];code['case_count']=len(support)
 code['representative_evidence']=[dict(case_id=a['case_id'],quote=a['evidence'][0]['quote'],interpretation=a['rationale']) for a in support[:3]]
meta=dict(label='GPT6-1',dataset='SATD',research_question='What reusable maintenance concerns and evidence qualifications are expressed by the supplied ML-project code comments and their source context?',artifact_count=len(corpus),assignment_count=sum(len(a['code_ids']) for a in assignments),code_count=len(defs),substantive_code_count=sum(c['kind']=='substantive_concern' for c in defs),round=1,analysis_method='Direct assistant reading of all supplied sections, per-artifact notes, inductive consolidation and manually authored assignments; scripts only package and validate the analysis.',external_model_api_calls=0,human_reference_labels_used=False,human_reviewed=False,label_note='GPT6-1 is the user-requested output label; it does not attest to a separately invoked model endpoint.',source_corpus_sha256=hashlib.sha256((w/'SATD/input/corpus.json').read_bytes()).hexdigest(),source_profile='paper-20261106-v10',scope='The supplied comment and retrieved source excerpts, not entire repositories or executed behavior. All artifacts are coded; evidence-qualification codes do not assert a technical-debt defect.',limitations=['Source-context ambiguity and historical revision limitations remain in evidence and scope notes.','Questions, proposals, implemented workarounds, and confirmed mismatches are distinguished in case rationales.','This is one assistant analysis, not independent human validation or two independent coding runs.'])
def dump(name,x): (out/name).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
dump('codebook.json',dict(metadata=meta,codes=defs));dump('assignments.json',assignments)
root=dict(category='Root',description=meta['research_question'],layer=0,children=[])
for group in dict.fromkeys(c['group'] for c in defs):
 root['children'].append(dict(category=group,description='Organizational heading; not independently assigned.',layer=1,children=[dict(category=c['name'],description=c['definition'],layer=2,children=[]) for c in defs if c['group']==group]))
dump('taxonomy.json',root)
res=[]
for x,a in zip(corpus,assignments):
 res.append(dict(id=a['case_id'],document='\n\n'.join('['+s['field']+']\n'+s['text'] for s in x['sections']),code_ids=a['code_ids'],categories=[next(c['name'] for c in defs if c['id']==cid) for cid in a['code_ids']],rationale=a['rationale'],scope_note=a['scope_note']))
dump('results.json',dict(metadata=meta,results=res))
with (out/'codebook.csv').open('w',newline='') as f:
 fields=['id','group','name','definition','inclusion','exclusion','kind','case_count'];wr=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');wr.writeheader();wr.writerows(defs)
with (out/'assignments.csv').open('w',newline='') as f:
 fields=['case_id','index','code_ids','status','coding_kind','rationale','scope_note'];wr=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');wr.writeheader();wr.writerows({**a,'code_ids':';'.join(a['code_ids'])} for a in assignments)
md=['# SATD — GPT6-1','',f"All **{len(corpus)} artifacts** are included in **{meta['assignment_count']} assignments** to **{len(defs)} codes**: 20 substantive concern codes and 2 evidence-qualification codes.",'','The codebook was derived from direct reading of the supplied comments and source excerpts. No human reference categories or external model API were used. Codes describe the concern expressed by the material; a proposed change or question is not automatically a confirmed bug. S21 and S22 explicitly retain unclear markers and explanatory/instructional annotations, so full coverage does not falsely imply that every artifact establishes unresolved production debt.','', 'All source sections, source locations, revision notes, and case-specific limitations are embedded in `assignments.json`; `results.json` includes each complete supplied document. The nested `taxonomy.json` provides a category/description/layer/children presentation; organizational headings are not additional assigned codes.','','| Code | Category | Artifacts |','|---|---|---:|']
for c in defs:md.append(f"| {c['id']} | {c['name']} | {c['case_count']} |")
md+=['','Counts overlap only where an artifact explicitly supports distinct concerns. No category-count cap or human codebook was used.','']
for c in defs:
 md += [f"## {c['id']} — {c['name']}",'',c['definition'],'',f"**Include:** {c['inclusion']}",'',f"**Exclude/boundary:** {c['exclusion']}",'',f"**Supporting artifacts:** {c['case_count']}. See the JSON for the full ID list.",'']
 for e in c['representative_evidence']:md += [f"- `{e['case_id']}`: {e['interpretation']}"]
 md+=['']
md+=['## Method and limits','','All 856 input records and their available source sections were read. Provisional observations were compared across cases and consolidated by the underlying maintenance concern. One primary code was manually assigned to every artifact; a second code was added only for an explicitly distinct concern. Packaging checks verify coverage, references, and verbatim source evidence; they do not constitute independent semantic validation.','',*['- '+s for s in meta['limitations']]]
(out/'codebook.md').write_text('\n'.join(md)+'\n')
assert len(obs)==len(primary)==len(corpus)==856
assert len({a['case_id'] for a in assignments})==856
assert all(a['code_ids'] and set(a['code_ids'])<={c['id'] for c in defs} for a in assignments)
for a,x in zip(assignments,corpus):
 for e in a['evidence']:assert e['quote']==x['sections'][e['section_index']]['text']
audit=dict(artifacts=856,covered=856,missing=[],duplicates=[],assignments=meta['assignment_count'],codes=len(defs),verbatim_evidence_check='passed',reference_check='passed',coverage_check='passed',output_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in out.iterdir() if p.is_file()})
(d/'audit.json').write_text(json.dumps(audit,indent=2)+'\n');(d/'status.json').write_text(json.dumps(dict(state='complete',reviewed_artifacts=856,total_artifacts=856,final_codebook_exported=True,output=str(out)),indent=2)+'\n');print(json.dumps(audit,indent=2))
