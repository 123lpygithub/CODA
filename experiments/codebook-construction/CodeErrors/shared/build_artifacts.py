"""Format analyst-authored codebooks/assignments and validate coverage. No model calls or inferred labels."""
from pathlib import Path
import json,csv,hashlib,collections,ast
P=Path(__file__).resolve().parent; ROOT=P.parent
cases=json.loads((P/'corpus.json').read_text());byid={c['case_id']:c for c in cases}
obs={r['case_id']:r['observation'] for r in csv.DictReader((P/'observations-1.tsv').open(),delimiter='\t')}
defs=list(csv.DictReader((P/'code_definitions.tsv').open(),delimiter='\t'))
witness=json.loads((P/'witness_results.json').read_text());syntax={r['case_id']:r for r in json.loads((P/'syntax_audit.json').read_text())}
# Original source retained exactly; plain-text evidence includes requirements and reference code.
(P/'cases').mkdir(exist_ok=True)
for c in cases:
 text='CASE '+c['case_id']+'\nSOURCE ERROR IDS '+', '.join(c['source_ids'])+'\nTASK DESCRIPTION\n'+c['task_description']+'\n\nGENERATED CODE\n'+c['incorrect_code']+'\n\nREFERENCE CODE\n'+c['ground_truth_code']+'\n'
 (P/'cases'/f"{c['case_id']}.txt").write_text(text)
def dump(path,obj):path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
resolutions=json.loads((P/'pending_case_resolutions.json').read_text())
resolution_by_id={r['case_id']:r for r in resolutions['cases']}
allmaps={};summary=[]
for rnd in [1]:
 out=ROOT/f'GPT6-{rnd}'
 pairs=[l.split() for l in (P/f'round{rnd}-map.txt').read_text().splitlines() if l and not l.startswith('#')]
 assert len(pairs)==len(dict(pairs))==len(cases)
 mapping={k:[] if v=='U' else v.split(',') for k,v in pairs}
 for cid,decision in resolution_by_id.items():
  assert cid in mapping and not mapping[cid], 'Resolution must target a previously unresolved case.'
  mapping[cid]=decision['code_ids']
 allmaps[rnd]=mapping
 assert set(mapping)==set(byid)
 codes=[]
 for d in [d for d in defs if int(d['round'])==rnd]:
  ids=[c['case_id'] for c in cases if d['id'] in mapping[c['case_id']]]
  assert ids
  c=byid[d['example_id']];lines=c['incorrect_code'].splitlines();hits=[i+1 for i,l in enumerate(lines) if d['evidence_needle'] in l];assert hits,(d['id'],d['evidence_needle'])
  assert c['case_id'] in ids
  codes.append({'id':d['id'],'group':d['group'],'name':d['name'],'name_zh':d['name_zh'],'definition':d['definition'],'inclusion':d['inclusion'],'exclusion':d['exclusion'],'supporting_case_ids':ids,'case_count':len(ids),'representative_evidence':{'case_id':c['case_id'],'field':'incorrect_code','line_start':hits[0],'quote':lines[hits[0]-1],'interpretation':obs[c['case_id']] if c['case_id']!='393' else 'When the left bracket is an exact root, the strict product<0 condition discards it. Witness [100,1] returns approximately +100 instead of -100.'}})
 known={d['id'] for d in codes};assert all(set(x)<=known for x in mapping.values())
 meta={'label':out.name,'dataset':'llm_code_error_semantic','research_question':'What reusable failure mechanisms explain the supplied LLM-generated code errors?','source_records':687,'solution_cases':557,'tasks':150,'analysis_method':'Assistant-led source reading, inductive consolidation, explicit case mapping and focused execution checks','round':rnd,'reading_order':'ascending task_id, ascending representative Error ID','independent_blinded_replication':False,'human_reviewed':False,'model_identifier':'GPT6-1 is the requested artifact label; original generation parameters were not captured in provider execution metadata.','api_calls_for_this_artifact':0,'temperature':None,'seed':None,'resource_usage':None,'reference_categories_used_for_induction':False,'reference_implementations_read':True,'source_corpus_sha256':hashlib.sha256((P/'corpus.json').read_bytes()).hexdigest(),'unresolved_case_ids':[k for k,v in mapping.items() if not v],'leaf_code_count':len(codes),'assignment_mode':'multiple labels for separately evidenced defects; no duplicate parent/child assignments','status':'all cases coded; two initial deferrals resolved with explicit supplemental evidence','artifact_revision':2,'supplemental_resolution_case_ids':sorted(resolution_by_id),'resolution_record':'../shared/pending_case_resolutions.json'}
 groups=list(dict.fromkeys(d['group'] for d in codes))
 tree={'category':'Root','description':'Inductively consolidated failure mechanisms in the Code errors corpus.','layer':0,'children':[{'category':g,'description':'Organizational heading; not independently assigned.','layer':1,'children':[{'category':d['name'],'description':d['definition'],'layer':2,'children':[]} for d in codes if d['group']==g]} for g in groups]}
 assignments=[];results=[];name={d['id']:d for d in codes}
 for cid,labels in mapping.items():
  c=byid[cid];why=obs[cid]
  status='unresolved' if not labels else 'coded'
  if cid in resolution_by_id:why=resolution_by_id[cid]['rationale']
  doc=(P/'cases'/f'{cid}.txt').read_text();quote=c['incorrect_code'];evidence={'path':f'../shared/cases/{cid}.txt','field':'incorrect_code','line_start':1,'line_end':len(quote.splitlines()),'quote':quote,'sha256':hashlib.sha256(quote.encode()).hexdigest()}
  rec={'case_id':cid,'source_error_ids':c['source_ids'],'task_id':c['task_id'],'source_model':c['model'],'code_ids':labels,'status':status,'rationale':why,'evidence':[evidence],'syntax_check':syntax[cid],'witness_indices':[i for i,w in enumerate(witness) if w['case_id']==cid],'decision_basis':'source interpretation; witness where linked','reviewed_in_round':rnd}
  if cid in resolution_by_id:
   decision=resolution_by_id[cid]
   rec.update(decision_basis=decision['decision_basis'],scope_note=decision['scope_note'],supplemental_resolution=decision)
   rec['evidence'].extend(decision['evidence_additions'])
  assignments.append(rec)
  paths=[name[l]['group']+' -> '+name[l]['name'] for l in labels]
  results.append({'id':cid,'document':doc,'summary':why,'category':paths[0] if paths else '', 'category_description':name[labels[0]]['definition'] if labels else '', 'categories':paths,'code_ids':labels,'status':status,'source_error_ids':c['source_ids']})
 dump(out/'codebook.json',{'metadata':meta,'codes':codes});dump(out/'taxonomy.json',tree);dump(out/'assignments.json',assignments);dump(out/'results.json',{'metadata':{**meta,'taxonomy_structure':tree,'compatibility_note':'HOW-style metadata/results envelope; category is first-listed label for legacy consumers. categories/code_ids preserve all labels. Unresolved records have empty category; exclude explicitly from label metrics.'},'results':results});dump(out/'metadata.json',meta)
 with (out/'codebook.csv').open('w',newline='') as f:
  w=csv.writer(f);w.writerow(['id','group','name','name_zh','definition','inclusion','exclusion','case_count','supporting_case_ids']);w.writerows([d['id'],d['group'],d['name'],d['name_zh'],d['definition'],d['inclusion'],d['exclusion'],d['case_count'],';'.join(d['supporting_case_ids'])] for d in codes)
 with (out/'assignments.csv').open('w',newline='') as f:
  w=csv.writer(f);w.writerow(['case_id','source_error_ids','task_id','source_model','codes','status','rationale']);w.writerows([a['case_id'],';'.join(a['source_error_ids']),a['task_id'],a['source_model'],';'.join(a['code_ids']),a['status'],a['rationale']] for a in assignments)
 text=f'# {out.name} — Code errors 最终编码本\n\n本轮覆盖 **557 份生成代码、687 条来源记录、150 个任务**。共有 **{len(codes)} 个可分配 code**，组织在 {len(groups)} 个导航分组下；分组不是额外编码。已归类 {sum(bool(x) for x in mapping.values())} 份，未决 {sum(not x for x in mapping.values())} 份。允许针对独立缺陷进行多重编码，因此类别覆盖数之和可以超过案例数。\n\n这是同一助手会话中的第 '+str(rnd)+' 轮完整阅读与归纳，未使用原始人工类别作为模板，也未经过人工审核。本目录保留第一轮归纳的 17 个类别，并按补充证据完成 393、729 两个原未决案例的编码；补充决策单独留痕。完整方法见 [README](../README.md)。\n\n## 类别一览\n\n|Code|类别|英文名称|覆盖案例数|\n|---|---|---|---:|\n'
 for d in codes:text+=f"|{d['id']}|{d['name_zh']}|{d['name']}|{d['case_count']}|\n"
 text+='\n## 使用规则\n\n以交付代码中的可观察失败机制为单位，不推断模型的心理原因。优先选择能准确解释证据的具体类别；一个缺陷不同时归到泛化类别与具体类别。只有存在不同证据支持的不同缺陷时才多重编码。题目约束优先，参考实现用于理解而非要求相同算法；材料冲突进入未决记录。\n'
 for d in codes:
  e=d['representative_evidence'];text+=f"\n## {d['id']} {d['name_zh']}\n\n**{d['name']}**\n\n{d['definition']}\n\n- 纳入：{d['inclusion']}\n- 排除与边界：{d['exclusion']}\n- 支持：{d['case_count']} 份代码。完整列表见 codebook.json 的 supporting_case_ids。\n- 代表案例：[Error ID {e['case_id']}](../shared/cases/{e['case_id']}.txt)，生成代码第 {e['line_start']} 行。\n\n```python\n{e['quote']}\n```\n\n{e['interpretation']}\n"
 text+='\n## 未决记录\n\n'
 for a in assignments:
  if a['status']=='unresolved':text+=f"- [案例 {a['case_id']}](../shared/cases/{a['case_id']}.txt)：{a['rationale']}\n"
 if not any(a['status']=='unresolved' for a in assignments):text+='全部 557 个 artifact 均已编码，无未决案例。393 和 729 的补充判断见 [材料核查说明](../DATA_NOTES.md)。\n'
 text+='\n## 随附文件\n\n`taxonomy.json` 是 HOW 风格分类树；`results.json` 是其 metadata/results 风格结果包；`codebook.json` 保存完整定义和边界；`assignments.json`/`.csv` 保存逐例编码；`metadata.json` 记录本轮范围与方法。所有执行见证集中保存在 `../shared/witness_results.json`。\n'
 (out/'codebook.md').write_text(text)
 summary.append({'label':out.name,'codes':len(codes),'groups':len(groups),'cases':len(assignments),'coded':sum(bool(x) for x in mapping.values()),'unresolved':meta['unresolved_case_ids'],'assignments':sum(map(len,mapping.values()))})
dump(ROOT/'validation.json',{'rounds':summary,'source_id_coverage':len({i for c in cases for i in c['source_ids']}),'unique_cases':len(cases),'witness_checks':len(witness),'all_assignment_ids_valid':True,'all_code_examples_quote_original_source':True,'no_unassigned_cases_except_explicit_unresolved':True})
print(json.dumps(summary,indent=2))
