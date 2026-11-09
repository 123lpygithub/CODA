import ast,json,re,tokenize,io
from pathlib import Path
P=Path(__file__).parent;c=json.loads((P/'input/corpus.json').read_text());groups={}
for r in c:groups.setdefault(r['task_id'],[]).append(r)
def compact(s):
 try:
  t=ast.parse(s)
  for n in ast.walk(t):
   if isinstance(n,(ast.Module,ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)) and n.body and isinstance(n.body[0],ast.Expr) and isinstance(n.body[0].value,ast.Constant) and isinstance(n.body[0].value.value,str):n.body=n.body[1:] or [ast.Pass()]
  text=ast.unparse(t)
 except SyntaxError:text=re.sub(r'(?s)""".*?"""|\x27\x27\x27.*?\x27\x27\x27','[docstring shown in task]',s)
 lines=text.splitlines();result=[];i=0
 while i<len(lines):
  n=1
  while i+n<len(lines) and lines[i+n]==lines[i]:n+=1
  result.append(lines[i]+(f' [line repeated {n} times]' if n>1 else ''));i+=n
 return '\n'.join(result)
parts=[]
for tid,rows in groups.items():
 docs=[]
 for r in rows:
  for key in ['task_description','incorrect_code','ground_truth_code']:
   for doc in re.findall(r'(?s)"""(.*?)"""|\x27\x27\x27(.*?)\x27\x27\x27',r[key]):
    v=next(x for x in doc if x).strip()
    if v not in docs:docs.append(v)
 text=f'\nTASK {tid} IDs '+','.join(r['case_id'] for r in rows)+'\nSPEC\n'+'\n'.join(docs)+'\nREF\n'+compact(rows[0]['ground_truth_code'])+'\n'
 seen={}
 for r in rows:
  code=compact(r['incorrect_code']);text+='CASE '+r['case_id']+'\n'
  if code in seen:text+='EXACT EXECUTABLE STRUCTURE SAME AS CASE '+seen[code]+'\n'
  else:text+=code+'\n';seen[code]=r['case_id']
 parts.append(text)
for i in range(0,len(parts),10):(P/f'read-{i//10+1:02}.txt').write_text(''.join(parts[i:i+10]))
print('chars',sum(map(len,parts)),'batches',len(parts)//10)
