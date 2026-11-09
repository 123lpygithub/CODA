"""Freeze label-free, full-source inputs for two independent codebook runs."""
from pathlib import Path
import hashlib,json,random
ROOT=Path(__file__).resolve().parents[3]
ART=Path(__file__).resolve().parent.parent;BUNDLE=ROOT/'experiments/materials/evidence-20261106-v10'
def digest(data):return hashlib.sha256(data).hexdigest()
def write(p,obj):
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def freeze():
 payload=json.loads((BUNDLE/'agent_inputs.json').read_text());audit=json.loads((BUNDLE/'evidence_audit.json').read_text())
 assert digest((BUNDLE/'agent_inputs.json').read_bytes())==audit['input_snapshot_sha256']
 privacy_root=ROOT/'dataset/personal_data_protection_github/source/linked_artifacts_20261106_v10'
 reports={}
 for name,key,count in [('SATD','ml_satd_23_shades',856),('Privacy','personal_data_protection_github',652)]:
  out=ART/name/'input'
  if (out/'corpus.json').exists():raise ValueError(f'Input already frozen: {out}; preserve it.')
  corpus=[];aliases=0
  snapshot_root=ROOT/'dataset/personal_data_protection_github/source/github_snapshot_20261106_v10'
  snapshots=json.loads((snapshot_root/'manifest.json').read_text()) if name=='Privacy' else {}
  manifests={m:json.loads((privacy_root/m).read_text()) for m in ['manifest.json','external_manifest.json']} if name=='Privacy' else {}
  for a in payload[key]:
   fields=a['raw_fields'];sections=[];seen={}
   refs={r['field']:r['value'] for r in a['source_refs'] if r.get('field')}
   def add(field,text,source=None,scope=None):
    if not isinstance(text,str) or not text.strip():return
    if text in seen:
     seen[text]['aliases'].append(field);return
    row={'field':field,'text':text,'source':source or refs.get(field),'scope':scope,'aliases':[]};sections.append(row);seen[text]=row
   if name=='SATD':
    keys=['comment_text','source_context','source_context_ambiguity_note','source_context_revision_note']
    keys += sorted(k for k in fields if k.startswith('source_context_candidate_'))
    for k in keys:add(k,fields.get(k))
    provenance={k:fields.get(k) for k in ['dataset_id','repo_name','filename','comment_introducing_revision','comment_removing_revision','source_context_status','source_context_commit']}
   else:
    for k in ['title','body','evidence_scope','historical_issue_body','historical_evidence_scope']:add(k,fields.get(k))
    snapshot_entry=snapshots['artifacts'][a['artifact_id']]
    chronology={}
    for entry in [snapshot_entry,snapshot_entry.get('event_archive',{})]:
     if entry.get('file'):
      raw=(snapshot_root/entry['file']).read_bytes();assert digest(raw)==entry['sha256']
      snap=json.loads(raw)
      for c in snap['comments']:
       prefix='historical_comment_' if entry is not snapshot_entry else 'comment_'
       chronology[prefix+str(c['id'])]={k:c.get(k) for k in ['created_at','updated_at','author']}
    for k in fields:
     if k.startswith('comment_') and k[len('comment_'):].isdigit() or k.startswith('historical_comment_'):add(k,fields[k],scope=chronology.get(k))
    # Use full cache text, not the 24,000-character rendering in agent_inputs.
    for m,manifest in manifests.items():
     entry=manifest['artifacts'][a['artifact_id']];path=privacy_root/entry['file'];raw=path.read_bytes();assert digest(raw)==entry['sha256']
     cache=json.loads(raw)
     for i,l in enumerate(cache['links'],1):
      field=('linked' if m=='manifest.json' else 'external')+f'_{i}'
      scope={k:l.get(k) for k in ['status','reason','revision','retrieval_url','fetched_at','historical_evidence']}
      add(field,l.get('text') or '[Source unavailable] '+l.get('reason',''),l['url'],scope)
    provenance={k:fields.get(k) for k in ['issue_url','html_url','project','created_at','snapshot_status','snapshot_updated_at','evidence_status','retrieved_comment_count','snapshot_expected_comment_count']}
   aliases+=sum(len(x['aliases']) for x in sections)
   corpus.append({'artifact_id':a['artifact_id'],'provenance':provenance,'sections':sections})
  assert len(corpus)==count and len({x['artifact_id'] for x in corpus})==count
  write(out/'corpus.json',corpus)
  manifest={'dataset':name,'source_profile':'paper-20261106-v10','source_snapshot_sha256':audit['input_snapshot_sha256'],'artifact_count':count,'corpus_sha256':digest((out/'corpus.json').read_bytes()),'characters':sum(len(s['text']) for a in corpus for s in a['sections']),'duplicate_section_aliases':aliases,'original_annotations_excluded':True,'github_label_fields_excluded':True,'full_downloaded_link_text_used':True,'source_scope':'All retained v10 source material; no reconstruction of unavailable evidence.'}
  write(out/'manifest.json',manifest)
  for run,seed in [('GPT6-1',6101),('GPT6-2',6102)]:
   dest=ART/name/run;dest.mkdir(parents=True,exist_ok=True);ids=[a['artifact_id'] for a in corpus];random.Random(seed).shuffle(ids)
   write(dest/'order.json',{'seed':seed,'artifact_ids':ids,'corpus_sha256':manifest['corpus_sha256']})
   write(dest/'status.json',{'state':'prepared','artifact_count':count,'completed_artifacts':0,'model_calls':0,'reason':'Independent model execution has not started; API credentials unavailable during preparation.'})
  reports[name]=manifest
 write(ART/'_execution/input_audit.json',reports);print(json.dumps(reports,indent=2))
if __name__=='__main__':freeze()
