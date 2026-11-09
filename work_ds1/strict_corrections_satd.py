"""Explicit corrections from the strict SATD artifact-by-artifact review."""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; WORK=ROOT/'work_ds1'
p=WORK/'decisions/satd_redo.jsonl'
rows=[json.loads(l) for l in p.open(encoding='utf-8') if l.strip()]
by={r['row']:r for r in rows}
def setr(n,codes,open_codes,memo):
    r=by[n]; r['code_ids']=codes; r['open_codes']=open_codes; r['memo']=memo

# row 189: only a bare marker embedded after an emit mapping; no object/action.
setr(189,['SATD-17'],['空TODO'],'注释仅含末尾 TODO 标记，未说明待办对象、动作或原因；无法进一步细分。')
# row 209: sort indices then intersect in order to make return efficient.
setr(209,['SATD-07'],['排序索引以加速求交'],'注释要求先排序索引再按序求交，以便更高效地返回；属于性能与效率改进，不是待调查的设计疑问。')
with p.open('w',encoding='utf-8') as f:
    for r in rows: f.write(json.dumps(r,ensure_ascii=False)+'\n')
print('corrected SATD 189,209')
