import json,sys,re
ds,start,end=sys.argv[1],int(sys.argv[2]),int(sys.argv[3])
mode=sys.argv[4] if len(sys.argv)>4 else 'full'
ls=[json.loads(l) for l in open('work_ds1/corpus/%s.jsonl'%ds)]
for i,x in enumerate(ls[start-1:end],start):
    if ds=='satd':
        rf=x['raw_fields']
        print(f"[{i}] {x['artifact_id']} | {rf['Repo Type']} | {rf['Repo Name']} | {rf['Filename']}")
        print(f"    COMMENT: {rf['Comment Text']!r}")
    elif ds=='privacy':
        rf=x['raw_fields']
        print(f"[{i}] {x['artifact_id']} | {rf['type']} | {rf['project']} | {rf['status']} | {rf['evidence_status']} | {rf['keywords']}")
        print(f"    TITLE: {rf['title']}")
        print(f"    BODY: {rf['body']}")
        print(f"    DISC: {rf['discussion']}")
    else:
        rf=x['raw_fields']
        print(f"[{i}] id={x['artifact_id']} task={rf['task_id']} model={rf['model']} src={x['source_error_ids']}")
        print("    INCORRECT:")
        print(rf['incorrect_code'])
        print("    GT:")
        print(rf['ground_truth_code'])
    print()
