"""Display original material only; never infer codes or attest reading."""
import argparse
import hashlib
import json
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument('dataset', choices=['SATD', 'Privacy'])
p.add_argument('start', type=int)
p.add_argument('stop', type=int)
p.add_argument('--offset', type=int, default=0)
p.add_argument('--length', type=int)
a = p.parse_args()
root = Path(__file__).resolve().parent.parent
raw = (root / a.dataset / 'input' / 'corpus.json').read_bytes()
corpus = json.loads(raw)
assert 0 <= a.start < a.stop <= len(corpus)
assert a.offset >= 0
if a.offset or a.length is not None:
    assert a.stop == a.start + 1, 'Paginate only one record at a time'
print('SOURCE SHA256', hashlib.sha256(raw).hexdigest())
for i in range(a.start, a.stop):
    case = corpus[i]
    parts = [f'RECORD {i}: {case["artifact_id"]}',
             'PROVENANCE ' + json.dumps(case['provenance'], ensure_ascii=False)]
    for s in case['sections']:
        parts.append('FIELD ' + s['field'] + ' META ' + json.dumps(
            {k: v for k, v in s.items() if k not in ['field', 'text']}, ensure_ascii=False))
        parts.append(s['text'])
        parts.append('END FIELD ' + s['field'])
    rendered = '\n'.join(parts) + '\n'
    end = len(rendered) if a.length is None else min(len(rendered), a.offset + a.length)
    print(f'RENDERED RANGE [{a.offset}, {end}) / {len(rendered)}')
    print(rendered[a.offset:end])
    print('END RECORD' if end == len(rendered) else 'RECORD CONTINUES')
