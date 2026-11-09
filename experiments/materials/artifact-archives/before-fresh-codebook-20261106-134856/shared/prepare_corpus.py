import json,hashlib,io,tokenize
from pathlib import Path
root=Path(__file__).resolve().parents[2];out=root/'Artifact/shared'
rows=json.loads((root/'dataset/llm_code_error_semantic/llm_code_error_semantic.json').read_text());groups={}
for r in rows:groups.setdefault((r['task_id'],r['model'],r['incorrect_code']),[]).append(r)
cases=[]
for g in groups.values():
 r=min(g,key=lambda r:int(r['id']));cases.append({'case_id':str(r['id']),'source_ids':[str(x['id']) for x in g],**{k:r[k] for k in ['task_id','model','task_description','incorrect_code','ground_truth_code','source_file']}})
cases.sort(key=lambda r:(int(r['task_id']),int(r['case_id'])))
(out/'corpus.json').write_text(json.dumps(cases,ensure_ascii=False,indent=2))
def compact(s):
 # Remove only repeated triple-quoted function documentation; keep all executable lines/comments.
 import re
 return re.sub(r'(?s)(\"\"\".*?\"\"\"|\x27\x27\x27.*?\x27\x27\x27)','',s).strip()
bytask={}
for c in cases:bytask.setdefault(c['task_id'],[]).append(c)
parts=[]
for task,cs in bytask.items():
 s=f'\nTASK {task}\n'+cs[0]['task_description']+'\nREFERENCE\n'+compact(cs[0]['ground_truth_code'])+'\n'
 for c in cs:s+=f"CASE {c['case_id']} ({c['model']}; source ids={','.join(c['source_ids'])})\n"+compact(c['incorrect_code'])+'\n'
 
 import re
 docs=[]
 for c in cs:
  for field in ['incorrect_code','ground_truth_code']:
   for doc in re.findall(r'(?s)"""(.*?)"""',c[field]):
    if doc.strip() not in cs[0]['task_description'] and doc.strip() not in docs:docs.append(doc.strip())
 if docs:s+='ADDITIONAL SOURCE DOCSTRINGS\n'+'\n'.join(docs)+'\n'
 parts.append(s)
for i in range(0,len(parts),10):(out/f'reading-{i//10+1:02d}.txt').write_text(''.join(parts[i:i+10]))
print('cases',len(cases),'tasks',len(parts),'chars',sum(map(len,parts)))
