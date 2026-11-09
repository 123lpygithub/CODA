import json,sys
ls=[json.loads(l) for l in open('work_ds1/corpus/codeerrors.jsonl')]
start,end=int(sys.argv[1]),int(sys.argv[2])
groups={}
for x in ls: groups.setdefault(x['raw_fields']['task_id'],[]).append(x)
keys=list(groups)
def body(code, desc):
    # strip the task description (shared docstring) to keep only the implementation
    c = code
    if desc and desc in c:
        c = c.replace(desc, '', 1)
    c = c.strip('\n')
    return c
for t in keys[start-1:end]:
    items=groups[t]
    rf=items[0]['raw_fields']
    desc=rf['task_description']
    # first line of description tells the signature
    sig=[l for l in desc.splitlines() if l.startswith('def ') or l.startswith('from ')][:2]
    print(f"\n===== TASK {t} | {len(items)} sol | {' / '.join(sig)}")
    print("GT-BODY:", body(rf['ground_truth_code'], desc)[:900].replace('\n','\n    '))
    for x in items:
        print(f"  --- A{x['artifact_id']} [{x['raw_fields']['model']}] src{x['source_error_ids']}")
        print('    ' + body(x['raw_fields']['incorrect_code'], desc)[:1200].replace('\n','\n    '))
