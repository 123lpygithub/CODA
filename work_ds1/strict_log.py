"""Maintain an append-only strict-review log; no semantic classification."""
from __future__ import annotations
import hashlib, json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; WORK=ROOT/'work_ds1'
LOG=WORK/'strict_review_log.jsonl'

def read(path): return [json.loads(l) for l in path.open(encoding='utf-8') if l.strip()]

def main():
    dataset=sys.argv[1]; lo=int(sys.argv[2]); hi=int(sys.argv[3]); outcome=sys.argv[4] if len(sys.argv)>4 else 'confirmed'
    rows=read(WORK/'corpus'/f'{dataset.lower()}.jsonl')
    existing={}
    if LOG.exists():
        for r in read(LOG): existing[(r['dataset'],r['artifact_id'])]=r
    with LOG.open('a',encoding='utf-8') as f:
        for i,row in enumerate(rows,1):
            if not lo<=i<=hi: continue
            rec={'dataset':dataset,'row':i,'artifact_id':row['artifact_id'],
                 'content_sha256':hashlib.sha256(row['content'].encode('utf-8')).hexdigest(),
                 'outcome':outcome}
            existing[(dataset,row['artifact_id'])]=rec
            f.write(json.dumps(rec,ensure_ascii=False)+'\n')
    # compact duplicate records while preserving the latest outcome
    with LOG.open('w',encoding='utf-8') as f:
        for r in sorted(existing.values(), key=lambda x:(x['dataset'],x['row'])):
            f.write(json.dumps(r,ensure_ascii=False)+'\n')
    print('logged',dataset,lo,hi,outcome,'total',len(existing))

if __name__=='__main__': main()
