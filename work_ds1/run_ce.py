import json,re,subprocess,sys,os,tempfile
ls=[json.loads(l) for l in open('work_ds1/corpus/codeerrors.jsonl')]
RUNNER = r'''
import sys,json,re
src=open(sys.argv[1]).read()
tests=json.load(open(sys.argv[2]))
ns={}
out=[]
try:
    exec(compile(src,'<artifact>','exec'),ns)
except SyntaxError as e:
    print(json.dumps({'load_error':'SyntaxError: %s'%e})); sys.exit()
except Exception as e:
    print(json.dumps({'load_error':'%s: %s'%(type(e).__name__,e)})); sys.exit()
for expr,expected in tests:
    try:
        val=eval(expr,ns)
        got=repr(val)
        out.append({'expr':expr,'expected':expected,'got':got,'ok':got==expected})
    except Exception as e:
        out.append({'expr':expr,'expected':expected,'got':None,'error':'%s: %s'%(type(e).__name__,e),'ok':False})
print(json.dumps({'tests':out}))
'''
open('work_ds1/_runner.py','w').write(RUNNER)

def extract_tests(desc):
    lines=desc.splitlines(); tests=[]
    for i,l in enumerate(lines):
        s=l.strip()
        if s.startswith('>>>'):
            expr=s[3:].strip()
            expected=None
            if i+1<len(lines):
                nxt=lines[i+1].strip()
                if nxt and not nxt.startswith('>>>') and not nxt.startswith('"""'):
                    expected=nxt
            tests.append([expr,expected])
    return tests

results={}
for x in ls:
    aid=x['artifact_id']; rf=x['raw_fields']
    tests=extract_tests(rf['task_description'])
    if not tests: results[aid]={'tests':[],'note':'no doctest'}; continue
    with tempfile.NamedTemporaryFile('w',suffix='.py',delete=False) as f:
        f.write(rf['incorrect_code']); src=f.name
    tp=src+'.tests.json'
    json.dump(tests,open(tp,'w'))
    try:
        r=subprocess.run([sys.executable,'work_ds1/_runner.py',src,tp],capture_output=True,text=True,timeout=5)
        results[aid]=json.loads(r.stdout.strip().splitlines()[-1]) if r.stdout.strip() else {'error':r.stderr[-300:]}
    except subprocess.TimeoutExpired:
        results[aid]={'timeout':True}
    os.unlink(src); os.unlink(tp)
json.dump(results,open('work_ds1/ce_doctest_results.json','w'),indent=0)
from collections import Counter
c=Counter()
for aid,r in results.items():
    if 'load_error' in r: c['load_error']+=1
    elif r.get('timeout'): c['timeout']+=1
    elif 'error' in r: c['runner_error']+=1
    elif r.get('note'): c['no_tests']+=1
    else:
        t=r['tests']
        c['pass' if all(z['ok'] for z in t) else 'fail']+=1
print(c, 'total', len(results))
