import json,sys,io,tokenize,re
ls=[json.loads(l) for l in open('work_ds1/corpus/codeerrors.jsonl')]
groups={}
for x in ls: groups.setdefault(x['raw_fields']['task_id'],[]).append(x)
keys=list(groups)
start,end=int(sys.argv[1]),int(sys.argv[2])
LIM=int(sys.argv[3]) if len(sys.argv)>3 else 380

def strip_desc(code,desc):
    if desc and desc in code: return code.replace(desc,'',1)
    return code

def compact(code):
    try:
        toks=list(tokenize.generate_tokens(io.StringIO(code).readline))
    except Exception as e:
        # fall back: strip comments line-wise
        c=re.sub(r'(?m)#.*$','',code)
        return re.sub(r'\s+',' ',c).strip(), 'SYNTAX'
    keep=[]; has_code=False; has_comment=False
    for tok in toks:
        if tok.type==tokenize.COMMENT: has_comment=True; continue
        if tok.type in (tokenize.NL,tokenize.NEWLINE,tokenize.INDENT,tokenize.DEDENT,tokenize.ENCODING): continue
        if tok.type==tokenize.STRING and len(tok.string)>80: continue
        if tok.string.strip(): has_code=True
        keep.append(tok.string)
    s=re.sub(r'\s+',' ',' '.join(keep)).strip()
    return s, ('COMMENTONLY' if (has_comment and not has_code) else 'OK')

for t in keys[start-1:end]:
    items=groups[t]; rf=items[0]['raw_fields']; desc=rf['task_description']
    gt,_=compact(strip_desc(rf['ground_truth_code'],desc))
    print(f"\n== T{t} n={len(items)}")
    print(" GT> "+gt[:LIM])
    for x in items:
        body=strip_desc(x['raw_fields']['incorrect_code'],desc)
        s,flag=compact(body)
        tail = '' if len(s)<=LIM else ' …TAIL:'+s[-90:]
        print(f" A{x['artifact_id']}[{x['raw_fields']['model'][:9]}]s{x['source_error_ids']} <{flag}> {s[:LIM]}{tail}")
