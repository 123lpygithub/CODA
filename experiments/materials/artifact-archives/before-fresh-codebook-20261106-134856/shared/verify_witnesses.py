"""Run explicitly selected, inspected source programs unchanged in bounded subprocesses.
This is supporting evidence, not an exhaustive HumanEval test run.
"""
import json, subprocess, sys, ast
from pathlib import Path
P=Path(__file__).resolve().parent
cases={c['case_id']:c for c in json.loads((P/'corpus.json').read_text())}
witnesses=[
 ('393','find_zero',[[100,1]],-100),('151','rolling_max',[[1,2,3,2,3,4,2]],[1,2,3,3,3,4,4]),
 ('163','count_distinct_characters',['aA'],1),('13','remove_duplicates',[[1,2,2,3]],[1,3]),
 ('359','max_fill',[[[1,0],[1,0]],2],2),('401','is_multiply_prime',[8],True),
 ('547','sort_array',[[4,2,1]],[1,2,4]),('400','total_match',[['a'],['b']],['a']),
 ('523','closest_integer',['14.5'],15),('520','count_up_to',[0],[]),
 ('426','truncate_number',[3.5],0.5),('435','string_xor',['010','110'],'100'),
 ('609','separate_paren_groups',['()'],['()']),('182','decode_cyclic',['bca'],'abc'),
 ('427','below_zero',[[2,-1]],False),('150','filter_by_substring',[['ba'],'a'],['ba']),
 ('141','has_close_elements',[[0,10,0.1,20],0.2],True),
 ('334','fib4',[3],0),('81','move_one_ball',[[3,2,1]],False),
 ('434','make_palindrome',['ab'],'aba'),('353','rounded_avg',[1,5],'0b11'),
 ('367','intersection',[[1,3],[1,3]],'YES'),('125','sorted_list_sum',[['bb','aa']],['aa','bb']),
 ('387','do_algebra',[['+','*','-'],[2,3,4,5]],9),
 ('729','sorted_list_sum',[['bb','aa']],['aa','bb']),
 ('729','sorted_list_sum',[['aaaa','bb']],['bb','aaaa']),
 ('111','largest_smallest_integers',[[0]],[None,None]),
 ('142','separate_paren_groups',['()'],['()']),
 ('436','greatest_common_divisor',[25,15],5),
]
worker=r'''
import json,sys,resource
resource.setrlimit(resource.RLIMIT_CPU,(2,2));resource.setrlimit(resource.RLIMIT_AS,(268435456,268435456))
x=json.load(sys.stdin)
try:
 ns={};exec(compile(x['source'],'<original-source>','exec'),ns)
 result=ns[x['function']](*x['args'])
 print(json.dumps({'kind':'return','value':result}))
except Exception as e:
 print(json.dumps({'kind':'exception','type':type(e).__name__,'message':str(e)[:300]}))
'''
result=[]
for cid,fn,args,expected in witnesses:
 c=cases[cid];rec={'case_id':cid,'function':fn,'args':args,'expected_from_contract':expected,'test_origin':'analyst_constructed','domain_note':'Mixed-length witness is outside one contradictory equal-length clause; diagnostic only.' if cid=='729' and len(set(map(len,args[0])))>1 else 'Selected from stated input domain.'}
 for field in ['incorrect_code','ground_truth_code']:
  try:
   p=subprocess.run([sys.executable,'-I','-c',worker],input=json.dumps({'source':c[field],'function':fn,'args':args}),text=True,capture_output=True,timeout=4)
   rec[field]=json.loads(p.stdout) if p.stdout else {'kind':'process_failure','returncode':p.returncode,'stderr':p.stderr[:300]}
  except subprocess.TimeoutExpired:rec[field]={'kind':'timeout','seconds':4}
 result.append(rec)
(P/'witness_results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
for r in result: print(r['case_id'],r['incorrect_code'], 'expected',r['expected_from_contract'])
audit=[]
for c in cases.values():
 row={'case_id':c['case_id']}
 for f in ['incorrect_code','ground_truth_code']:
  try:ast.parse(c[f]);row[f]={'parseable':True}
  except SyntaxError as e:row[f]={'parseable':False,'line':e.lineno,'message':e.msg}
 audit.append(row)
(P/'syntax_audit.json').write_text(json.dumps(audit,indent=2))
