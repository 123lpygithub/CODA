"""Render frozen artifacts for strict, artifact-by-artifact human review.

No classification is performed here.  The full frozen content is printed for
each selected artifact, together with the current analyst decision so that a
reviewer can confirm or correct it.
"""
from __future__ import annotations
import json, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
WORK=ROOT/'work_ds1'

def read(path):
    return [json.loads(l) for l in path.open(encoding='utf-8') if l.strip()]

def decision_map(dataset):
    if dataset=='CodeErrors':
        return {r['artifact_id']:r for r in read(WORK/'decisions/ce.jsonl')}
    if dataset=='SATD':
        return {str(r['row']):r for r in read(WORK/'decisions/satd_redo.jsonl')}
    if dataset=='Privacy':
        return {str(r['row']):r for r in read(WORK/'decisions/privacy_redo.jsonl')}
    raise SystemExit('dataset must be CodeErrors, SATD, or Privacy')

def main():
    dataset=sys.argv[1]; lo=int(sys.argv[2]); hi=int(sys.argv[3])
    rows=read(WORK/'corpus'/f'{dataset.lower()}.jsonl')
    dm=decision_map(dataset)
    for i,row in enumerate(rows,1):
        if not lo<=i<=hi: continue
        key=row['artifact_id'] if dataset=='CodeErrors' else str(i)
        d=dm[key]
        print('\n'+'#'*120)
        print(f'REVIEW {dataset} ROW {i} | {row["artifact_id"]} | CONTENT_CHARS {len(row["content"])}')
        print('CURRENT_CODES:', ','.join(d['code_ids']))
        print('CURRENT_OPEN:', ' | '.join(d.get('open_codes',[])))
        print('CURRENT_MEMO:', d.get('memo', d.get('analytic_memo','')))
        print('FROZEN_CONTENT_BEGIN')
        print(row['content'])
        print('FROZEN_CONTENT_END')

if __name__=='__main__': main()
