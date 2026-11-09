"""Bounded diagnostic examples, not an official benchmark test suite."""
import ast, json, subprocess, sys, pathlib
ROOT=pathlib.Path(__file__).resolve().parent
corpus={x['case_id']:x for x in json.loads((ROOT/'input/corpus.json').read_text())}
# Manually selected inputs from task examples or constructed from supplied requirements.
checks=[
('393','find_zero',[[100,1]],-100,'linear polynomial with a root at the initial left endpoint'),
('729','sorted_list_sum',[['zz','aaaa']],['zz','aaaa'],'length-primary rule and reference; conflicts with equal-length assumption'),
('357','odd_count',[['3']],['the number of odd elements 1n the str1ng 1 of the 1nput.'],'canonical task example'),
('547','sort_array',[[2,1]],[1,2],'numeric tie-break for equal bit counts'),
('151','rolling_max',[[1,2,3,2,3,4,2]],[1,2,3,3,3,4,4],'task example'),
('151','rolling_max',[[-2,-1]],[-2,-1],'valid negative input'),
('188','change_base',[8,3],'22','task example'),
('188','change_base',[0,2],'0','zero representation required by ordinary positional notation'),
('25','change_base',[8,3],'22','task example'),
('46','iscube',[-1],True,'task example'),
('81','move_one_ball',[[3,5,4,1,2]],False,'task example'),
('111','largest_smallest_integers',[[0]],[None,None],'task example; tuples normalized as JSON arrays'),
('356','histogram',['a'],{'a':1},'one-character valid input'),
('359','max_fill',[[[1],[1]],2],2,'each well requires a separate lowering'),
('415','minPath',[[[1,2],[3,4]],2],[1,2],'lexicographic path rule'),
('377','is_equal_to_sum_even',[8],True,'task example'),
('379','file_name_check',['a.ttt'],'No','extension outside the allowed list'),
('531','unique_digits',[[15,15,2]],[15,15],'digit filtering with repeated qualifying inputs'),
('547','sort_array',[[1,5,2,3,4]],[1,2,4,3,5],'prose and reference ordering; printed example conflicts'),
('598','int_to_mini_roman',[19],'xix','task example'),
('387','do_algebra',[['+','*','-'],[2,3,4,5]],9,'task example'),
('732','Strongest_Extension',['X',['a','BB']],'X.BB','second extension has greater strength'),
('729','sorted_list_sum',[['zz','aa']],['aa','zz'],'equal-length inputs satisfying the restrictive assumption'),
('122','order_by_points',[[1,-1]],[-1,1],'negative digit-sum example rule'),
('137','solve',['1234'],'4321','task example'),
('138','string_to_md5',['Hello world'],'3e25960a79dbc69b674cd4ec67a72c62','task example in supplied standalone source'),
('737','eat',[2,11,5],[7,0],'task example'),
('551','maximum',[[4,-4,4],0],[],'allowed zero selection size'),
('131','even_odd_count',[0],[1,0],'zero is an integer with one even decimal digit'),
('278','valid_date',['06/04/2020'],False,'task example invalid format'),
]
runner='''import json,sys,resource
resource.setrlimit(resource.RLIMIT_CPU,(2,2))
resource.setrlimit(resource.RLIMIT_AS,(256*1024*1024,256*1024*1024))
p=json.load(sys.stdin)
try:
 ns={};exec(compile(p['source'],'<supplied-artifact>','exec'),ns)
 value=ns[p['function']](*p['args'])
 print(json.dumps({'outcome':'returned','value':value}))
except Exception as e:
 print(json.dumps({'outcome':'exception','type':type(e).__name__,'message':str(e)[:400]}))
'''
results=[]
for cid,fun,args,expected,origin in checks:
 payload={'source':corpus[cid]['incorrect_code'],'function':fun,'args':args}
 try:
  p=subprocess.run([sys.executable,'-I','-c',runner],input=json.dumps(payload),text=True,capture_output=True,timeout=4)
  actual=json.loads(p.stdout) if p.stdout else {'outcome':'process_exit','returncode':p.returncode,'stderr':p.stderr[:400]}
 except subprocess.TimeoutExpired: actual={'outcome':'timeout','seconds':4}
 results.append({'case_id':cid,'function':fun,'args':args,'expected':expected,'expectation_basis':origin,'actual':actual,'matches_expected':actual.get('outcome')=='returned' and actual.get('value')==expected,'source_unchanged':True})
(ROOT/'diagnostics.json').write_text(json.dumps(results,indent=2,ensure_ascii=False)+'\n')
print(json.dumps(results,indent=2))
parses=[]
for cid,c in corpus.items():
 try: ast.parse(c['incorrect_code']);parses.append({'case_id':cid,'parseable':True})
 except SyntaxError as e: parses.append({'case_id':cid,'parseable':False,'error':e.msg,'line':e.lineno})
(ROOT/'syntax_audit.json').write_text(json.dumps(parses,indent=2)+'\n')
print('Parse failures:',[x['case_id'] for x in parses if not x['parseable']])
