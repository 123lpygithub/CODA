from recovery_helpers import *
from urllib.parse import urlencode,urlsplit,unquote,quote
import re
from collections import defaultdict
m=json.loads((root/'manifest.json').read_text());groups=defaultdict(dict)
for e in m['artifacts'].values():
 for l in json.loads((root/e['file']).read_text())['links']:
  if l['kind']=='file' and l['status']=='unavailable':
   parts=urlsplit(l['url']).path.strip('/').split('/');repo='/'.join(parts[:2]);path=unquote('/'.join(parts[4:]))
   if path.endswith('.7z') or parts[3]=='next':continue
   groups[(repo,path)][l['url']]=l

def rawget(url):
 path=root/'archive_raw'/(hashlib.sha256(url.encode()).hexdigest()+'.json')
 if path.exists():
  raw=json.loads(path.read_text());assert raw['url']==url and raw['sha256']==hashlib.sha256(raw['text'].encode()).hexdigest();return raw
 raw=get(url);write_json(path,raw);return raw

def recover(key,links):
 repo,path=key;endpoint=f'https://api.github.com/repos/{repo}/commits?'+urlencode({'path':path,'per_page':1})
 try:
  hist=rawget(endpoint);entries=json.loads(hist['text']);assert isinstance(entries,list) and entries,'No exact-path history'
  entry=entries[0];errs=[]
  for commit in [entry['sha']]+[p['sha'] for p in entry['parents']]:
   try:
    raw=rawget(f'https://raw.githubusercontent.com/{repo}/{commit}/{quote(path,safe="/")}');assert '\x00' not in raw['text']
    for url,link in links.items():
     item=dict(link,status='partial',historical_evidence=True,revision=commit,immutable_revision=True,retrieval_url=raw['final_url'],text=raw['text'],source_sha256=raw['sha256'],fetched_at=raw['fetched_at'],history_query_url=endpoint,history_response_sha256=hist['sha256'],history_entry_sha=entry['sha'],history_commit_date=entry['commit']['committer']['date'],recovery_method='Exact repository/path REST Git history; explicit commit or verified direct parent; full source retained',reason='Historical source recovered. Original branch target and case-time equivalence are unknown; do not infer deployment or resolution. Original line anchor is retained in URL; not relocated to a guessed matching line.')
     write_json(root/'results'/(hashlib.sha256(url.encode()).hexdigest()+'.json'),item)
    return {'repo':repo,'path':path,'status':'partial','links':len(links),'revision':commit}
   except Exception as e:errs.append(str(e))
  raise ValueError('; '.join(errs))
 except Exception as e:return {'repo':repo,'path':path,'status':'failed','reason':str(e)}
results=[]
with ThreadPoolExecutor(max_workers=4) as pool:
 for f in as_completed([pool.submit(recover,k,v) for k,v in groups.items()]):
  item=f.result();results.append(item);print(json.dumps(item),flush=True)
write_json(root/'v9_file_history_audit.json',results)
