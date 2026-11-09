"""Persist explicitly authored completed notes out of order; no classification."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def save(dataset, rows):
    corpus=json.loads((ROOT.parent/dataset/'input/corpus.json').read_text())
    target=ROOT/dataset/'reading_notes_staged.jsonl'
    staged=[json.loads(x) for x in target.read_text().splitlines()] if target.exists() else []
    base=[json.loads(x) for x in (ROOT/dataset/'reading_notes.jsonl').read_text().splitlines()]
    seen={x['index'] for x in base+staged}
    for index, interpretation, concept, field, quote, qualification in rows:
        assert index not in seen,index
        record=corpus[index]
        fields={s['field']:s['text'] for s in record['sections']}
        assert quote and quote in fields[field],(index,quote)
        staged.append(dict(index=index,artifact_id=record['artifact_id'],read_fields=list(fields),interpretation=interpretation,provisional_concepts=[concept],evidence=[dict(field=field,quote=quote)],qualification=qualification))
        seen.add(index)
    target.write_text(''.join(json.dumps(n,ensure_ascii=False)+'\n' for n in sorted(staged,key=lambda n:n['index'])))
    print(dataset,len(base),'sequential +',len(staged),'staged =',len(seen),'completed notes')
