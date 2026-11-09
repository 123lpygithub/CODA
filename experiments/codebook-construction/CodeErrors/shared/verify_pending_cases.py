"""Execute unchanged pending-case programs against retained upstream tests and witnesses."""
import ast
import hashlib
import json
from pathlib import Path
import subprocess
import sys

P = Path(__file__).resolve().parent
cases = {c['case_id']: c for c in json.loads((P / 'corpus.json').read_text())}
worker = r'''
import ast,json,resource,sys
resource.setrlimit(resource.RLIMIT_CPU,(3,3))
resource.setrlimit(resource.RLIMIT_AS,(268435456,268435456))
p=json.load(sys.stdin)
ns={}
try:
    exec(compile(p['source'],'<unchanged-case-source>','exec'),ns)
    fn=ns[p['entry_point']]
    if p['mode']=='call':
        value=fn(*p['args'])
        result={'kind':'return','value':value}
    else:
        exec(compile(p['test'],'<official-HumanEval-test>','exec'),ns)
        if p['entry_point']=='sorted_list_sum':
            tree=ast.parse(p['test'])
            assertions=[n for n in ast.walk(tree) if isinstance(n,ast.Assert)]
            judgments=[]
            for n in assertions:
                assert isinstance(n.test,ast.Compare)
                env=dict(ns,candidate=fn)
                call=n.test.left
                actual=eval(compile(ast.Expression(call),'<official-test-input>','eval'),env)
                expected=eval(compile(ast.Expression(n.test.comparators[0]),'<official-test-expected>','eval'),env)
                judgments.append({'input':ast.literal_eval(call.args[0]),'actual':actual,'expected':expected,'passed':actual==expected,'assertion':ast.get_source_segment(p['test'],n)})
            result={'kind':'official_assertions','assertion_count':len(judgments),'passed_count':sum(r['passed'] for r in judgments),'assertions':judgments}
        else:
            ns['check'](fn)
            result={'kind':'official_check','passed':True}
except Exception as e:
    result={'kind':'exception','type':type(e).__name__,'message':str(e)[:300]}
print(json.dumps(result))
'''

def execute(source, task, mode, args=None):
    payload={'source':source,'entry_point':task['entry_point'],'test':task['test'],'mode':mode,'args':args}
    try:
        result=subprocess.run([sys.executable,'-I','-c',worker],input=json.dumps(payload),text=True,capture_output=True,timeout=6)
        return json.loads(result.stdout) if result.stdout else {'kind':'process_failure','returncode':result.returncode,'stderr':result.stderr[:300]}
    except subprocess.TimeoutExpired:
        return {'kind':'timeout','seconds':6}

records=[]
for cid,tid,args in [('393','32',[[100,1]]),('729','149',[['aaaa','bbbb','dd','cc']])]:
    case=cases[cid]
    path=P/'humaneval-evidence'/f'{tid}.json'
    task=json.loads(path.read_text())
    assert str(case['task_id'])==tid
    record={'case_id':cid,'task_id':task['task_id'],'source_code_sha256':hashlib.sha256(case['incorrect_code'].encode()).hexdigest(),'upstream_task_path':str(path.relative_to(P)),'upstream_task_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'witness_args':args,'test_origin':'393: analyst-constructed endpoint-root witness in stated domain. 729: literal existing official HumanEval assertion.','checks':{}}
    for field,code in [('incorrect_code',case['incorrect_code']),('ground_truth_code',case['ground_truth_code']),('upstream_canonical',task['prompt']+task['canonical_solution'])]:
        record['checks'][field]={'witness':execute(code,task,'call',args),'official_test':execute(code,task,'test')}
    records.append(record)
a,b=records
assert a['checks']['incorrect_code']['witness']['kind']=='return'
assert abs(a['checks']['incorrect_code']['witness']['value']+100)>1
assert a['checks']['ground_truth_code']['witness']=={'kind':'return','value':-100.0}
assert b['checks']['incorrect_code']['witness']=={'kind':'return','value':['aaaa','bbbb','cc','dd']}
assert b['checks']['ground_truth_code']['witness']=={'kind':'return','value':['cc','dd','aaaa','bbbb']}
assert b['checks']['incorrect_code']['official_test']['passed_count']==6
assert b['checks']['incorrect_code']['official_test']['assertion_count']==7
assert b['checks']['ground_truth_code']['official_test']['passed_count']==7
assert b['checks']['upstream_canonical']['official_test']['passed_count']==7
(P/'pending_case_verification.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
for rec in records:
    print(rec['case_id'],json.dumps(rec['checks'],ensure_ascii=False))
print('PASS: both assignments supported by unchanged-source execution; official mixed-length test resolves Task 149 operational scope')
