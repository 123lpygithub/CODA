"""Apply a JSON patch file of privacy decisions onto privacy_redo.jsonl (keyed by row)."""
from __future__ import annotations
import json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'work_ds1/decisions/privacy_redo.jsonl'
patch=json.load(open(sys.argv[1],encoding='utf-8'))
rows=[json.loads(l) for l in P.open(encoding='utf-8') if l.strip()]
idx={r['row']:r for r in rows}
for p in patch:
    r=idx[p['row']]
    for k in ('code_ids','open_codes','memo','outcome','evidence_quotes','evidence_availability'):
        assert k in p, (p['row'],k)
    r.update({k:p[k] for k in ('code_ids','open_codes','memo','outcome','evidence_quotes','evidence_availability')})
    assert r['artifact_id']==p['artifact_id'], (p['row'],r['artifact_id'],p['artifact_id'])
with P.open('w',encoding='utf-8') as f:
    for r in rows: f.write(json.dumps(r,ensure_ascii=False)+'\n')
print('applied',len(patch),'rows')
