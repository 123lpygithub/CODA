from recover import *
context=ROOT/'dataset/ml_satd_23_shades/source/code_context_20261106_v10'
m=json.loads((context/'manifest.json').read_text());rows=json.loads((AUDIT/'satd_commit_api.json').read_text())
notes={
'23shades-0006-aaahbghib':'The verified published-commit diff comments out two copies of the same comment; it does not establish one unique source location.',
'23shades-0046-aafchcgjg':'The verified published-commit diff adds two copies of the same complete comment; the released record has no line identifier to choose between them.',
'23shades-0256-aagcicecj':'The verified published-commit diff contains more than one added occurrence of the target comment, alongside a removed occurrence. The change alone does not uniquely identify the sampled location.',
'23shades-0647-aaidbfgae':'The verified published-commit diff adds two copies of the exact comment, so introduction history does not disambiguate their locations.',
'23shades-0027-aajfegaca':'The published-commit API confirms the file modification but its returned patch contains no occurrence of the released target comment. This does not resolve the previously documented version mismatch.',
'23shades-0654-aagbifedh':'The published-commit diff deletes a shorter comment without the words "as needed". It does not establish the full released comment at that revision; the related-history excerpt remains supplemental.',
'23shades-0725-aahicjieh':'The published-commit API confirms a trainer.py modification but its returned patch contains no occurrence of the released pre_training comment. The related-history excerpt remains supplemental.'}
for r in rows:
 if r['status']!='retrieved':continue
 aid=r['artifact_id'];entry=m['artifacts'][aid];p=context/entry['file'];d=json.loads(p.read_text());dest=context/'verification'/(aid+'.json');write_json(dest,r)
 d['commit_verification']={'url':r['url'],'response_sha256':r['sha256'],'file':str(dest.relative_to(context)),'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'note':notes[aid]}
 key='ambiguity_note' if d['status']=='ambiguous' else 'revision_note'
 d[key]+=' Additional commit verification: '+notes[aid]
 write_json(p,d);entry['sha256']=hashlib.sha256(p.read_bytes()).hexdigest()
write_json(context/'manifest.json',m);print('Verified seven commit responses; existing ambiguity/partial status preserved.')
