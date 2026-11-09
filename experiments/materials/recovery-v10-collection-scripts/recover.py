"""Targeted new collection; preserves v9 and does not reconstruct text from labels."""
import sys,json,hashlib,subprocess,tempfile,re
from pathlib import Path
from datetime import datetime,timezone
from concurrent.futures import ThreadPoolExecutor,as_completed
from urllib.parse import urlsplit,quote,unquote,urlencode
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT))
from scripts.prepare_privacy_issue_discussions import write_json,save_snapshot,update_manifest
from adapters.github_issue_snapshot import normalize_snapshot
from scripts.prepare_privacy_external_evidence import collect,HOSTS
LINK=ROOT/'dataset/personal_data_protection_github/source/linked_artifacts_20261106_v10'
ISSUE=LINK.with_name('github_snapshot_20261106_v10')
AUDIT=ROOT/'experiments/materials/evidence-20261106-v10-recovery';AUDIT.mkdir(exist_ok=True)
def get(url,binary=False):
 with tempfile.TemporaryDirectory() as t:
  r=subprocess.run(['curl','-4','--location','--fail','--silent','--show-error','--connect-timeout','5','--max-time','18','--max-filesize','10000000','--user-agent','CODA-research-evidence','--output',t+'/body','--write-out','%{url_effective}\n%{content_type}',url],capture_output=True,text=True,timeout=22)
  if r.returncode:raise ValueError(r.stderr.strip())
  final,ct=r.stdout.split('\n',1);data=Path(t+'/body').read_bytes();h=hashlib.sha256(data).hexdigest();stamp=datetime.now(timezone.utc).isoformat()
  if binary:
   p=AUDIT/'binary'/h;p.parent.mkdir(exist_ok=True);p.write_bytes(data);return {'url':url,'final_url':final,'content_type':ct,'sha256':h,'file':str(p.relative_to(ROOT)),'bytes':len(data),'fetched_at':stamp}
  raw={'url':url,'final_url':final,'text':data.decode('utf-8'),'content_type':ct,'sha256':h,'fetched_at':stamp}
  write_json(LINK/'archive_raw'/(hashlib.sha256(url.encode()).hexdigest()+'.json'),raw);return raw

def main_issue(gap):
 url=gap['issue_url'].replace('https://github.com/','https://api.github.com/repos/')
 try:
  raw=get(url);d=json.loads(raw['text']);assert str(d['number'])==url.rsplit('/',1)[-1]
  # Require the original identity or the canonical redirect returned by GitHub.
  assert d['html_url'].lower()==gap['issue_url'].lower() or raw['final_url'].lower()==d['url'].lower()
  pages=[];comments=[]
  for page in range(1,2+(d['comments']//100)):
   r=get(d['comments_url']+f'?per_page=100&page={page}');cs=json.loads(r['text']);assert isinstance(cs,list)
   assert all(c['issue_url']==d['url'] for c in cs)
   comments+=cs;pages.append({'data':cs,'fetched_at':r['fetched_at']})
   if len(cs)<100:break
  wrapped={'data':d,'requested_url':url,'fetched_at':raw['fetched_at']}
  snap=normalize_snapshot(gap['artifact_id'],wrapped,pages,comments_complete=True)
  oldm=json.loads((ISSUE/'manifest.json').read_text());old=json.loads((ISSUE/oldm['artifacts'][gap['artifact_id']]['file']).read_text())
  oldids={c['id'] for c in old['comments']};newids={c['id'] for c in snap['comments']}
  result={'kind':'main_issue','artifact_id':gap['artifact_id'],'url':url,'status':snap['evidence_status'],'comments':len(newids),'expected':d['comments'],'added_comment_ids':sorted(newids-oldids),'old_comments_absent_now':sorted(oldids-newids)}
  # Do not replace a richer historical record by a narrower new snapshot.
  if oldids-newids:result.update(applied=False,reason='Existing comment IDs absent from current response; preserve prior snapshot and retain raw new response.')
  else:write_json(AUDIT/'proposed_issues'/(gap['artifact_id']+'.json'),snap);result['applied']=True
  return result
 except Exception as e:return {'kind':'main_issue','artifact_id':gap['artifact_id'],'url':url,'status':'failed','reason':str(e)}

def file_history(link):
 url=link['url'];parts=urlsplit(url).path.strip('/').split('/');repo='/'.join(parts[:2]);path=unquote('/'.join(parts[4:]))
 if path.endswith('.7z'):
  try:return {'kind':'binary','url':url,'status':'downloaded','raw':get('https://raw.githubusercontent.com/'+repo+'/'+parts[3]+'/'+quote(path,safe='/'),True)}
  except Exception as e:return {'kind':'binary','url':url,'status':'failed','reason':str(e)}
 if parts[3]=='next':path=unquote('/'.join(parts[5:])) # cited ref next/v99
 try:
  # Current source, if obtainable, remains retrieval-time evidence.
  target='https://raw.githubusercontent.com/'+repo+'/'+('/'.join(parts[3:5]) if parts[3]=='next' else parts[3])+'/'+quote(path,safe='/')
  try:
   raw=get(target);item=dict(link,status='partial',text=raw['text'],retrieval_url=raw['final_url'],source_sha256=raw['sha256'],fetched_at=raw['fetched_at'],reason='Source at cited branch recovered at retrieval time; branch revision and case-time equivalence are not established.')
  except Exception:
   endpoint='https://api.github.com/repos/'+repo+'/commits?'+urlencode({'path':path,'per_page':3});hist=get(endpoint);entries=json.loads(hist['text']);assert isinstance(entries,list) and entries,'No exact-path public history'
   raw=None
   for entry in entries:
    for commit in [entry['sha']]+[x['sha'] for x in entry['parents']]:
     try:raw=get(f'https://raw.githubusercontent.com/{repo}/{commit}/{quote(path,safe="/")}');break
     except Exception:pass
    if raw:break
   assert raw,'No source found in returned commits or direct parents'
   item=dict(link,status='partial',text=raw['text'],retrieval_url=raw['final_url'],source_sha256=raw['sha256'],fetched_at=raw['fetched_at'],revision=commit,immutable_revision=True,historical_evidence=True,history_query_url=endpoint,history_response_sha256=hist['sha256'],recovery_method='Exact path Git history and recorded commit or direct parent',reason='Historical source recovered; original case-time branch target and cited line equivalence remain unknown.')
  assert '\x00' not in item['text'];write_json(LINK/'results'/(hashlib.sha256(url.encode()).hexdigest()+'.json'),item)
  return {'kind':'file','url':url,'status':item['status'],'retrieval_url':item['retrieval_url']}
 except Exception as e:return {'kind':'file','url':url,'status':'failed','reason':str(e)}

def external(link):
 url=link['url'];parts=urlsplit(url)
 if parts.hostname in ['jira.lyrasis.org','mozilla-hub.atlassian.net']:return {'kind':'external','url':url,'status':'not_retried','reason':'Prior verified 404/403 or profile link; no new source identified.'}
 try:
  raw=get(url);assert urlsplit(raw['final_url']).hostname in HOSTS
  write_json(LINK/'external_raw'/(hashlib.sha256(url.encode()).hexdigest()+'.json'),raw)
  result=collect(link,LINK,1)
  if result['status']!='unavailable':write_json(LINK/'external_results'/(hashlib.sha256(url.encode()).hexdigest()+'.json'),result)
  return {'kind':'external','url':url,'status':result['status'],'reason':result.get('reason','')}
 except Exception as e:return {'kind':'external','url':url,'status':'failed','reason':str(e)}

def satd(gap):
 url=gap['revision_url']+'.diff'
 try:
  raw=get(url);matches=[l for l in raw['text'].splitlines() if any(s in l.lower() for s in ['better solutions','constraint satisfaction','pre_training','old setup','regex or something','partition','gnormplus','raise error in 1.1'])]
  return {'kind':'satd_diff','artifact_id':gap['artifact_id'],'url':url,'status':'retrieved','sha256':raw['sha256'],'relevant_lines':matches}
 except Exception as e:return {'kind':'satd_diff','artifact_id':gap['artifact_id'],'url':url,'status':'failed','reason':str(e)}

def main():
 coverage=json.loads((ROOT/'experiments/materials/evidence-20261105-v9-coverage.json').read_text());jobs=[]
 jobs += [(main_issue,x) for x in coverage['privacy']['remaining_gaps']]
 jobs += [(file_history,x) for x in coverage['linked_artifacts']['remaining_gaps'] if x['status']=='unavailable' and x['kind']=='file']
 jobs += [(external,x) for x in coverage['external_artifacts']['remaining_gaps'] if x['status']=='unavailable']
 jobs += [(satd,x) for x in coverage['satd']['remaining_gaps']]
 results=[]
 with ThreadPoolExecutor(max_workers=6) as pool:
  fs=[pool.submit(fn,x) for fn,x in jobs]
  for f in as_completed(fs):
   r=f.result();results.append(r);write_json(AUDIT/'attempts.json',results);print(json.dumps({k:v for k,v in r.items() if k not in ['raw','relevant_lines']},ensure_ascii=False),flush=True)
 manifest=json.loads((ISSUE/'manifest.json').read_text())
 for r in results:
  if r['kind']=='main_issue' and r.get('applied'):
   aid=r['artifact_id'];snap=json.loads((AUDIT/'proposed_issues'/(aid+'.json')).read_text());save_snapshot(ISSUE,manifest['artifacts'][aid],snap)
 update_manifest(ISSUE,manifest)
 print('MAIN COUNTS',manifest['counts'],flush=True)
if __name__=='__main__':main()
