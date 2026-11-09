"""Render exact, non-overlapping ranges of a frozen Privacy artifact.

No classification.  Usage:
  python3 privacy_render.py ROW START END
  python3 privacy_render.py ROW --all
"""
from __future__ import annotations
import json, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
ROWS=ROOT/'work_ds1/corpus/privacy.jsonl'

def main():
    row=int(sys.argv[1]); rows=[json.loads(l) for l in ROWS.open(encoding='utf-8') if l.strip()]
    r=rows[row-1]; n=len(r['content'])
    if len(sys.argv)==2 or sys.argv[2]=='--all': start,end=0,n
    else: start,end=int(sys.argv[2]),int(sys.argv[3])
    assert 0 <= start <= end <= n, (start,end,n)
    print(f'PRIVACY ROW {row} | {r["artifact_id"]} | TOTAL_CHARS {n} | RANGE {start}:{end} | REMAINING_AFTER {n-end}')
    print('RAW_STATUS',r['raw_fields'].get('evidence_status'),'| TITLE',r['raw_fields'].get('title'),'| PROJECT',r['raw_fields'].get('project'))
    print('RANGE_BEGIN')
    print(r['content'][start:end])
    print('RANGE_END')

if __name__=='__main__': main()
