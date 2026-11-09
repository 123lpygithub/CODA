"""Export manually analyzed observations and decisions; no automatic semantic classification."""
import ast,csv,hashlib,json,shutil,collections
from pathlib import Path
P=Path(__file__).resolve().parent
OUT=P/'export'; R=OUT/'GPT6-1'; S=OUT/'shared'
R.mkdir(parents=True,exist_ok=True);S.mkdir(parents=True,exist_ok=True)
def dump(path,obj):path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def csvout(path,rows,fields):
 with path.open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
  for row in rows:w.writerow({k:json.dumps(row[k],ensure_ascii=False) if isinstance(row[k],(dict,list)) else row[k] for k in fields})
corpus=json.loads((P/'input/corpus.json').read_text()); manifest=json.loads((P/'input/manifest.json').read_text())
obs=list(csv.DictReader((P/'observations.tsv').open(),delimiter='\t'));mapping=list(csv.DictReader((P/'mapping.tsv').open(),delimiter='\t'))
notes={i:x['observation'] for x in obs for i in x['case_ids'].split(',')}; maps={i:['C'+v for v in x['codes'].split(',')] for x in mapping for i in x['case_ids'].split(',')}
assert len(notes)==len(maps)==557 and set(notes)==set(maps)=={x['case_id'] for x in corpus}
codebook=json.loads((P/'definitions.json').read_text()); bycode={x['id']:x for x in codebook}
diagnostics=json.loads((P/'diagnostics.json').read_text());bydiag=collections.defaultdict(list)
for i,x in enumerate(diagnostics,1):x['diagnostic_id']=f'D{i:03}';bydiag[x['case_id']].append(x['diagnostic_id'])
def evidence(source,field):
 lines=source.splitlines();spans=[]
 try:
  tree=ast.parse(source)
  def visit(body):
   for node in body:
    if isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)):visit(node.body)
    elif isinstance(node,ast.Expr) and isinstance(node.value,ast.Constant) and isinstance(node.value.value,str):continue
    else:spans.append((node.lineno,node.end_lineno))
  visit(tree.body)
 except SyntaxError:
  # Whole source is needed to demonstrate a truncation; do not invent an executable excerpt.
  spans=[(1,len(lines))]
 if not spans:spans=[(1,len(lines))]
 return [{'field':field,'start_line':a,'end_line':b,'quote':'\n'.join(lines[a-1:b])} for a,b in spans]
assignments=[]
for c in corpus:
 cid=c['case_id'];codes=maps[cid];scope=[];status='coded_static_evidence'
 if 'C02' in codes:scope.append('Dependency finding applies to the supplied standalone Python source. No unseen harness imports or helper definitions are assumed.')
 if 'C01' in codes:scope.append('The record establishes incompleteness or nonfunctional behavior in the supplied artifact; it does not identify whether generation or data extraction caused it. Local observations are not a claim that truncated source executes.')
 if c['task_id']==149:scope.append('The length-first ordering rule and reference permit varied lengths, while one sentence assumes equal lengths. C11 for case 729 is conditional on the varied-length interpretation; it is not a demonstrated defect under the restrictive equal-length assumption.')
 if c['task_id']==116:scope.append('Printed examples conflict with the bit-count ordering rule. Coding follows the explicit bit-count and numeric tie-break rule, supported by the reference.')
 if cid=='357':scope.append('The generated docstring changes example outputs. The canonical task_description and reference require replacing every i; that canonical contract is used.')
 if cid=='393':scope.append('task_description contains only the poly helper signature; find_zero requirements are available in the generated program docstring. The endpoint defect is directly reproduced for [100,1]. The residual-accuracy concern is a separate static observation.')
 if cid=='188':scope.append('The zero-input observation uses ordinary positional notation; the positive example (8,3) independently demonstrates the division defect. The supplied reference is not treated as infallible on zero.')
 if c['task_id']==95:scope.append('The supplied reference has a source-format problem; interpretation relies on task requirements and generated behavior rather than executing that reference as an oracle.')
 if 'C03' in codes or len(codes)>1:scope.append('Additional local defects are static observations; an earlier exception can prevent later operations from being reached. Multi-label coding does not assert that every defect manifests in the same execution.')
 if cid=='729':status='coded_conditional_on_specification'
 elif bydiag[cid]:status='coded_with_focused_diagnostic'
 req=c['task_description'].splitlines()
 ev=[{'field':'task_description','start_line':1,'end_line':len(req),'quote':'\n'.join(req)}]+evidence(c['incorrect_code'],'incorrect_code')
 if cid in ['393','729','357','547']:
  lines=c['ground_truth_code'].splitlines();ev.append({'field':'ground_truth_code','start_line':1,'end_line':len(lines),'quote':'\n'.join(lines)})
 assignments.append({'case_id':cid,'source_error_ids':c['source_ids'],'task_id':c['task_id'],'source_model':c['model'],'code_ids':codes,'code_names':[bycode[k]['name'] for k in codes],'rationale':notes[cid],'evidence':ev,'scope_notes':scope,'status':status,'diagnostic_ids':bydiag[cid],'source_file':c['source_file'],'generated_source_sha256':hashlib.sha256(c['incorrect_code'].encode()).hexdigest()})
bycase={x['case_id']:x for x in assignments}
for code in codebook:
 supporting=[a for a in assignments if code['id'] in a['code_ids']]
 code['supporting_case_ids']=[a['case_id'] for a in supporting];code['artifact_count']=len(supporting);code['source_record_count']=sum(len(a['source_error_ids']) for a in supporting)
 code['representative_evidence']=[{'case_id':cid,'rationale':bycase[cid]['rationale'],'evidence':[e for e in bycase[cid]['evidence'] if e['field']=='incorrect_code']} for cid in code.pop('representative_ids')]
metadata={'label':'GPT6-1','dataset':'Code errors','research_question':'What recurring failure patterns are present in the supplied generated programs relative to the supplied task requirements?','analysis_date':'2026-11-06','analyst':'Codex assistant in the current conversation','model':'Not independently recorded by an API response; GPT6-1 is an output label, not a verified model identifier.','method':'Fresh single-assistant full-corpus reading, per-artifact observation, manual cross-case consolidation and manual assignment, followed by boundary review and focused diagnostics.','artifacts':557,'source_records':687,'tasks':150,'code_count':len(codebook),'assignment_count':sum(len(a['code_ids']) for a in assignments),'source_sha256':manifest['source_sha256'],'corpus_sha256':manifest['corpus_sha256'],'human_category_fields_used':False,'previous_result_used_as_coding_input':False,'blinding':'The conversation contains prior knowledge. This is a fresh source-based reanalysis, not a blinded independent replication.','dynamic_verification':{'diagnostic_inputs':len(diagnostics),'distinct_artifacts':len(bydiag)-sum(not v for v in bydiag.values()),'official_test_suite':False},'runtime_settings':{'python':'Python 3 used for diagnostics; see diagnostics script','api_temperature':None,'api_seed':None,'api_usage':None},'assignment_semantics':'Multi-label descriptions of distinct observed mechanisms, not mutually exclusive primary causes. First listed code has no causal ranking.','coverage_semantics':'All artifacts have coding decisions. Case 729 has a conditional ordering code; coded does not mean an unconditional defect is proven.'}
dump(R/'codebook.json',{'metadata':metadata,'codes':codebook});dump(R/'assignments.json',assignments)
csvout(R/'codebook.csv',codebook,['id','name','name_zh','definition','inclusion','exclusion','artifact_count','source_record_count','supporting_case_ids'])
csvout(R/'assignments.csv',assignments,['case_id','source_error_ids','task_id','source_model','code_ids','code_names','rationale','status','scope_notes','diagnostic_ids'])
(R/'observations.jsonl').write_text(''.join(json.dumps({'case_id':c['case_id'],'task_id':c['task_id'],'observation':notes[c['case_id']]},ensure_ascii=False)+'\n' for c in corpus))
tree={'category':'Code errors','description':metadata['research_question'],'layer':0,'children':[{'category':x['name'],'description':x['definition'],'layer':1,'children':[]} for x in codebook]}
dump(R/'taxonomy.json',tree)
results=[]
for c,a in zip(corpus,assignments):
 results.append({'id':c['case_id'],'document':json.dumps({'task_description':c['task_description'],'generated_program':c['incorrect_code'],'reference_program':c['ground_truth_code']},ensure_ascii=False,indent=2),'summary':a['rationale'],'category':a['code_names'][0],'category_description':bycode[a['code_ids'][0]]['definition'],'categories':a['code_names'],'code_ids':a['code_ids'],'source_error_ids':a['source_error_ids'],'status':a['status'],'scope_notes':a['scope_notes']})
dump(R/'results.json',{'metadata':{**metadata,'taxonomy_structure':tree,'format_note':'HOW-style metadata/results with multi-label extensions. category is a compatibility projection only.'},'results':results})
dump(R/'method.json',metadata);dump(R/'diagnostics.json',diagnostics)
shutil.copy2(P/'syntax_audit.json',R/'syntax_audit.json')
for name in ['corpus.json','manifest.json']:shutil.copy2(P/'input'/name,S/name)
for name in ['mapping.tsv','observations.tsv','definitions.json','export.py','read_materials.py','diagnostics.py']:shutil.copy2(P/name,S/name)
# Preserve full original reading batches and compact reading views, with exact repeat references.
shutil.copytree(P/'input',S/'input',dirs_exist_ok=True)
for path in P.glob('read-*.txt'):shutil.copy2(path,S/path.name)
logs=[]
for p in sorted(P.glob('read-*.txt')):
 import re
 tids=[int(t) for t in re.findall(r'^TASK (\d+)',p.read_text(),re.M)]
 logs.append({'file':'../shared/'+p.name,'sha256':sha(p),'task_ids':tids,'case_ids':[c['case_id'] for c in corpus if c['task_id'] in tids],'status':'read_and_observed','view':'Full executable structure with shared specifications; exact repeats identified, consecutive repeated lines counted; raw source retained in shared/corpus.json.'})
dump(R/'reading_log.json',logs)
# Verify evidence and coverage before writing a successful audit.
source_ids=[sid for c in corpus for sid in c['source_ids']]
assert len(source_ids)==len(set(source_ids))==687
for c,a in zip(corpus,assignments):
 assert a['case_id']==c['case_id'] and a['code_ids'] and len(a['code_ids'])==len(set(a['code_ids']))
 for e in a['evidence']:assert e['quote']=='\n'.join(c[e['field']].splitlines()[e['start_line']-1:e['end_line']])
 for code in a['code_ids']:assert code in bycode and a['case_id'] in bycode[code]['supporting_case_ids']
assert set(cid for log in logs for cid in log['case_ids'])==set(bycase)
assert all(x['artifact_count'] for x in codebook)
parse=json.loads((R/'syntax_audit.json').read_text());assert all('C01' in bycase[x['case_id']]['code_ids'] for x in parse if not x['parseable'])
audit={'artifacts':557,'coded_artifacts':len(assignments),'uncoded_artifacts':0,'source_records':len(source_ids),'tasks':len({c['task_id'] for c in corpus}),'codes':len(codebook),'assignments':metadata['assignment_count'],'multi_coded_artifacts':sum(len(a['code_ids'])>1 for a in assignments),'conditional_case_ids':['729'],'syntax_failures':sum(not x['parseable'] for x in parse),'diagnostic_inputs':len(diagnostics),'diagnostic_artifacts':len({d['case_id'] for d in diagnostics}),'all_source_ids_unique':True,'all_evidence_spans_match':True,'all_codes_have_support':True,'all_reading_views_covered':True,'human_validation_performed':False,'semantic_correctness_guaranteed':False}
dump(OUT/'coverage_audit.json',audit)
md=['# Code errors — inductive codebook (GPT6-1)','',f"557 artifacts · 687 source records · 150 tasks · {len(codebook)} codes · {metadata['assignment_count']} artifact–code assignments.",'','Each artifact has at least one code. Codes describe distinct observed mechanisms and may co-occur. Case 729 is conditional on an explicitly recorded interpretation of conflicting task requirements. This is a single-assistant source-based analysis, not a human-validated gold codebook.','', '| Code | Name | Artifacts |','|---|---|---:|']
md += [f"| {x['id']} | {x['name']} | {x['artifact_count']} |" for x in codebook]
for x in codebook:
 md += ['',f"## {x['id']} — {x['name']}",'',x['name_zh'],'',x['definition'],'','**Include**','']+['- '+v for v in x['inclusion']]+['','**Exclude / distinguish**','']+['- '+v for v in x['exclusion']]+['','**Representative cases**','']+[f"- Case {e['case_id']}: {e['rationale']}" for e in x['representative_evidence']]+['',f"Supporting artifacts: **{x['artifact_count']}**. Exact source excerpts and all supporting IDs are in `codebook.json`; per-artifact requirements, evidence and caveats are in `assignments.json`."]
(R/'codebook.md').write_text('\n'.join(md)+'\n')
print(json.dumps(audit,indent=2));print('Frequencies:',[(x['id'],x['artifact_count']) for x in codebook])
