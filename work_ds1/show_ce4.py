import json,sys,io,tokenize,re
ls=[json.loads(l) for l in open('work_ds1/corpus/codeerrors.jsonl')]
groups={}
for x in ls: groups.setdefault(x['raw_fields']['task_id'],[]).append(x)
keys=list(groups)
start,end=int(sys.argv[1]),int(sys.argv[2])

def compact(code, desc):
    c=code
    if desc and desc in c: c=c.replace(desc,'',1)
    # try to remove comments via tokenize
    try:
        out=[]; toks=list(tokenize.generate_tokens(io.StringIO(c).readline))
        last=(1,0); lines=c.splitlines()
        # simpler: regex strip full-line and trailing comments is unsafe for strings; use tokenize spans
        keep=[]; prev_end=(1,0)
        for tok in toks:
            if tok.type==tokenize.COMMENT:
                continue
            if tok.type in (tokenize.NL, tokenize.NEWLINE, tokenize.INDENT, tokenize.DEDENT):
                continue
            keep.append(tok.string)
        s=' '.join(keep)
        s=re.sub(r'\s+',' ',s)
        return s
    except Exception:
        return re.sub(r'\s+',' ',c)

for t in keys[start-1:end]:
    items=groups[t]; rf=items[0]['raw_fields']; desc=rf['task_description']
    print(f"\n===== T{t} ({len(items)}) {rf['ground_truth_code'].splitlines()[0][:80] if rf['ground_truth_code'] else ''}")
    print("GT:", compact(rf['ground_truth_code'],desc)[:420])
    for x in items:
        print(f"  A{x['artifact_id']} [{x['raw_fields']['model'][:9]}] s{x['source_error_ids']}: {compact(x['raw_fields']['incorrect_code'],desc)[:520]}")
