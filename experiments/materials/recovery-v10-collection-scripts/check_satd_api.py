from recover import *
coverage=json.loads((ROOT/'experiments/materials/evidence-20261105-v9-coverage.json').read_text())
def run(g):
 url=g['revision_url'].replace('https://github.com/','https://api.github.com/repos/').replace('/commit/','/commits/')
 try:
  raw=get(url);data=json.loads(raw['text']);assert data['sha']==g['revision_url'].rsplit('/',1)[-1]
  matches=[{k:f.get(k) for k in ['filename','previous_filename','status','patch','raw_url']} for f in data['files'] if f['filename']==g['filename'] or f.get('previous_filename')==g['filename']]
  return {'artifact_id':g['artifact_id'],'status':'retrieved','url':url,'parents':data['parents'],'matching_files':matches,'sha256':raw['sha256']}
 except Exception as e:return {'artifact_id':g['artifact_id'],'status':'failed','url':url,'reason':str(e)}
with ThreadPoolExecutor(max_workers=3) as p:out=list(p.map(run,coverage['satd']['remaining_gaps']))
write_json(AUDIT/'satd_commit_api.json',out)
for r in out:print(json.dumps(r,ensure_ascii=False)[:7000])
