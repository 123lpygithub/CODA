import json,sys
ls=[json.loads(l) for l in open('work_ds1/corpus/codeerrors.jsonl')]
start,end=int(sys.argv[1]),int(sys.argv[2])
groups={}
for x in ls: groups.setdefault(x['raw_fields']['task_id'],[]).append(x)
keys=list(groups)
for t in keys[start-1:end]:
    items=groups[t]
    print(f"\n===== TASK {t} | {len(items)} solutions =====")
    print("GT:", items[0]['raw_fields']['ground_truth_code'])
    for x in items:
        print(f"\n--- A{x['artifact_id']} {x['raw_fields']['model']} src{x['source_error_ids']} ---")
        print(x['raw_fields']['incorrect_code'])
