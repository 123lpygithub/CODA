"""Serialize explicitly authored notes; never interpret or classify source text."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def save(dataset, rows):
    corpus=json.loads((ROOT.parent/dataset/'input/corpus.json').read_text())
    out=ROOT/dataset/'reading_notes.jsonl'
    existing=[json.loads(s) for s in out.read_text().splitlines()]
    notes=[]
    for index, interpretation, concept, field, quote, qualification in rows:
        assert index==len(existing)+len(notes), (index,len(existing)+len(notes))
        r=corpus[index]
        fields={s['field']:s['text'] for s in r['sections']}
        assert quote and quote in fields[field], (index,quote)
        notes.append(dict(index=index,artifact_id=r['artifact_id'],read_fields=list(fields),interpretation=interpretation,provisional_concepts=[concept],evidence=[dict(field=field,quote=quote)],qualification=qualification))
    with out.open('a') as f:
        for note in notes:f.write(json.dumps(note,ensure_ascii=False)+'\n')
    print(dataset,len(existing)+len(notes))
