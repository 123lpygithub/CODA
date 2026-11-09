import json,sys
ls=[json.loads(l) for l in open('work_ds1/corpus/codeerrors.jsonl')]
start,end=int(sys.argv[1]),int(sys.argv[2])
groups={}
for x in ls:
    groups.setdefault(x['raw_fields']['task_id'],[]).append(x)
keys=list(groups)
for t in keys[start-1:end]:
    items=groups[t]
    rf=items[0]['raw_fields']
    print(f"\n########## TASK {t}  ({len(items)} solutions) ##########")
    print("TASK DESCRIPTION:")
    print(rf['task_description'])
    print("\nREFERENCE (ground truth):")
    print(rf['ground_truth_code'])
    for x in items:
        r=x['raw_fields']
        print(f"\n--- ARTIFACT {x['artifact_id']} | model={r['model']} | source_ids={x['source_error_ids']} ---")
        print(r['incorrect_code'])
