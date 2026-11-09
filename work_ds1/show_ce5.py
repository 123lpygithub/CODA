import json,sys,io,tokenize,re
ls=[json.loads(l) for l in open('work_ds1/corpus/codeerrors.jsonl')]
groups={}
for x in ls: groups.setdefault(x['raw_fields']['task_id'],[]).append(x)
keys=list(groups)
start,end=int(sys.argv[1]),int(sys.argv[2])

def compact(code):
    try:
        toks=list(tokenize.generate_tokens(io.StringIO(code).readline))
    except Exception:
        return re.sub(r'\s+',' ',code)[:600]
    keep=[]
    for tok in toks:
        if tok.type==tokenize.COMMENT: continue
        if tok.type in (tokenize.NL,tokenize.NEWLINE,tokenize.INDENT,tokenize.DEDENT,tokenize.ENCODING): continue
        if tok.type==tokenize.STRING and len(tok.string)>60: continue
        keep.append(tok.string)
    s=' '.join(keep)
    return re.sub(r'\s+',' ',s).strip()

for t in keys[start-1:end]:
    items=groups[t]; rf=items[0]['raw_fields']
    print(f"\n===== T{t} ({len(items)})")
    print("GT:", compact(rf['ground_truth_code'])[:500])
    for x in items:
        print(f"  A{x['artifact_id']}[{x['raw_fields']['model'][:9]}]s{x['source_error_ids']}: {compact(x['raw_fields']['incorrect_code'])[:600]}")
