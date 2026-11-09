import json,sys,io,tokenize,re
ls=[json.loads(l) for l in open('work_ds1/corpus/codeerrors.jsonl')]
g={}
for x in ls: g.setdefault(x['raw_fields']['task_id'],[]).append(x)
def compact(code):
    try: toks=list(tokenize.generate_tokens(io.StringIO(code).readline))
    except Exception: return re.sub(r'\s+',' ',re.sub(r'(?m)#.*$','',code)).strip()
    keep=[]
    for tok in toks:
        if tok.type==tokenize.COMMENT: continue
        if tok.type in (tokenize.NL,tokenize.NEWLINE,tokenize.INDENT,tokenize.DEDENT,tokenize.ENCODING): continue
        if tok.type==tokenize.STRING and len(tok.string)>80: continue
        keep.append(tok.string)
    return re.sub(r'\s+',' ',' '.join(keep)).strip()
for t in sys.argv[1:]:
    items=g[t]; rf=items[0]['raw_fields']
    print(f"\n== T{t} n={len(items)}")
    print("DESC:", ' '.join(rf['task_description'].split())[:300])
    print("GT:", compact(rf['ground_truth_code'])[:700])
    for x in items:
        print(f" A{x['artifact_id']}[{x['raw_fields']['model'][:9]}]s{x['source_error_ids']}: {compact(x['raw_fields']['incorrect_code'])[:800]}")
