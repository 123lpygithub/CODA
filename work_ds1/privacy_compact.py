"""Compact full-text view of one frozen Privacy artifact, without semantic filtering.

The standard synthetic header is collapsed to labeled values; issue body and every
retrieved discussion character are printed.  Ranges are over body + discussion.
"""
from __future__ import annotations
import json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
ROWS=ROOT/'work_ds1/corpus/privacy.jsonl'

def main():
    row=int(sys.argv[1]); rows=[json.loads(l) for l in ROWS.open(encoding='utf-8') if l.strip()]
    r=rows[row-1]; f=r['raw_fields']
    body=f.get('body','') or ''; disc=f.get('discussion','') or ''
    text=body+'\n\n[ALL COMMENTS]\n'+disc
    n=len(text)
    if len(sys.argv)==2: start,end=0,n
    else: start,end=int(sys.argv[2]),int(sys.argv[3])
    assert 0<=start<=end<=n
    print(f'ROW {row} | {r["artifact_id"]} | BODY+DISC_CHARS {n} | RANGE {start}:{end} | AFTER {n-end}')
    print(f'TITLE={f.get("title")} | PROJECT={f.get("project")} | TYPE={f.get("type")} | STATUS={f.get("status")} | NO={f.get("issue_number")} | EVIDENCE={f.get("evidence_status")}')
    print(f'KEYWORDS={f.get("keywords")} | LABELS={f.get("github_labels")}')
    print('TEXT_BEGIN')
    print(text[start:end])
    print('TEXT_END')

if __name__=='__main__': main()
