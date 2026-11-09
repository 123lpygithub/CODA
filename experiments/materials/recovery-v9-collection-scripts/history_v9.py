from recovery_helpers import *
from urllib.parse import urlencode,quote
jobs=[('MicrosoftDocs/azure-docs','articles/azure-monitor/platform/data-locations.md'),('MicrosoftDocs/azure-docs','articles/cognitive-services/Face/Face-API-How-to-Topics/HowtoAnalyzeVideo_Face.md')]
for repo,path in jobs:
 url=f'https://api.github.com/repos/{repo}/commits?'+urlencode({'path':path,'per_page':3})
 try:
  raw=get(url);write_json(root/'archive_raw'/(hashlib.sha256(url.encode()).hexdigest()+'.json'),raw)
  data=json.loads(raw['text']);print(path,json.dumps([{'sha':d['sha'],'parents':[p['sha'] for p in d['parents']],'date':d['commit']['committer']['date'],'message':d['commit']['message'][:100]} for d in data]),flush=True)
 except Exception as e:print(path,str(e),flush=True)
