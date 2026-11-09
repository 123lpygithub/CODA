from recovery_helpers import *
from adapters import MLSATD23ShadesAdapter
from scripts.prepare_satd_source_context import canonical_comment,comment_spans
rows=json.loads((root/'v9_satd_retry_audit.json').read_text());commits=[r['url'].split('/')[-2] for r in rows if '/api/1/revision/' in r['url']]
def run(a):
 rev=a.raw_fields['comment_introducing_revision'];url=rev+'.diff'
 try:
  raw=get(url);write_json(root/'archive_raw'/(hashlib.sha256(url.encode()).hexdigest()+'.json'),raw)
  lines=raw['text'].splitlines();matches=[l for l in lines if any(w in l.lower() for w in ['better solutions','constraint satisfaction','pre_training','old setup'])]
  return {'artifact_id':a.artifact_id,'url':url,'matches':matches}
 except Exception as e:return {'artifact_id':a.artifact_id,'error':str(e)}
with ThreadPoolExecutor(max_workers=3) as pool:
 results=list(pool.map(run,[a for a in MLSATD23ShadesAdapter().iter_artifacts() if a.raw_fields['comment_introducing_revision'].rsplit('/',1)[-1] in commits]))
write_json(root/'v9_satd_diff_audit.json',results);print(json.dumps(results,indent=2))
