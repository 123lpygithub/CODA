from recovery_helpers import *
jobs=[('catalyst-team/catalyst','69c078ac203ff211ea68c70eed1f9c847b86a84a','dl/callbacks.py'),('drckf/paysage','a28501f94342560209e174b0f8ecd2ea67accd6a','paysage/models/model.py'),('Lightning-AI/pytorch-lightning','cb67e1d0b29e1da251c064c78220aa78b44e0620','pytorch_lightning/trainer/trainer.py')]
def attempt(repo,commit,path):
 records=[]
 for url in [f'https://raw.githubusercontent.com/{repo}/{commit}/{path}',f'https://archive.softwareheritage.org/api/1/revision/{commit}/']:
  try:
   raw=get(url);write_json(root/'archive_raw'/(hashlib.sha256(url.encode()).hexdigest()+'.json'),raw)
   item={'url':url,'retrieved':True,'sha256':raw['sha256'],'preview':raw['text'][:120]}
  except Exception as e:item={'url':url,'retrieved':False,'reason':str(e)}
  records.append(item)
 return records
rows=[]
with ThreadPoolExecutor(max_workers=3) as pool:
 for f in as_completed([pool.submit(attempt,*j) for j in jobs]):rows.extend(f.result())
write_json(root/'v9_satd_retry_audit.json',rows);print(json.dumps(rows,indent=2))
