"""Check reference integrity across main/staged notes; never certify actual reading."""
import hashlib
import json
from collections import Counter
from pathlib import Path
HERE=Path(__file__).resolve().parent
progress={}
for dataset in ('SATD','Privacy'):
    source=HERE.parent/dataset/'input/corpus.json'
    corpus=json.loads(source.read_text())
    notes=[]
    for name in ('reading_notes.jsonl','reading_notes_staged.jsonl'):
        p=HERE/dataset/name
        if p.exists():notes.extend(json.loads(l) for l in p.read_text().splitlines() if l.strip())
    errors=[]
    counts=Counter(n['index'] for n in notes)
    for index,count in counts.items():
        if count!=1:errors.append([index,'duplicate notes',count])
    for n in notes:
        index=n['index']
        if not 0<=index<len(corpus):errors.append([index,'out of range']);continue
        r=corpus[index];fields={s['field']:s['text'] for s in r['sections']}
        if n['artifact_id']!=r['artifact_id']:errors.append([index,'artifact ID mismatch'])
        if set(n['read_fields'])!=set(fields):errors.append([index,'field coverage'])
        if not n['interpretation'] or not n['evidence']:errors.append([index,'missing authored interpretation/evidence'])
        for e in n['evidence']:
            if not e['quote'] or e['quote'] not in fields.get(e['field'],''):errors.append([index,'quote mismatch',e])
    missing=sorted(set(range(len(corpus)))-set(counts))
    publication=HERE/dataset/'publication.json'
    published=json.loads(publication.read_text()) if publication.exists() else None
    progress[dataset]=dict(state='published_supplied_text_reconstruction' if published else 'reading_in_progress',
        total_artifacts=len(corpus),authored_notes=len(notes),missing_note_indices=missing,
        source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),note_integrity_errors=errors,
        final_codebook_ready=bool(published),publication=published,
        external_follow_up_artifacts=sorted(n['index'] for n in notes if n.get('external_follow_up') or n.get('follow_up_sources')),
        validation_scope='References, field sets and exact quotes only; does not independently prove reading or semantic correctness.')
    print(dataset,len(notes),'notes; missing',missing,'errors',errors)
(HERE/'progress.json').write_text(json.dumps(progress,ensure_ascii=False,indent=2)+'\n')
raise SystemExit(any(v['note_integrity_errors'] for v in progress.values()))
