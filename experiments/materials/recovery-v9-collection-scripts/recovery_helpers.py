import sys,json,hashlib,subprocess,tempfile
from pathlib import Path
from datetime import datetime,timezone
from concurrent.futures import ThreadPoolExecutor,as_completed
ROOT=Path('/home/peiyuan/CODA/FSE27-CODA/CODA');sys.path.insert(0,str(ROOT))
from scripts.prepare_privacy_issue_discussions import write_json
from scripts.prepare_privacy_external_evidence import collect,HOSTS
from urllib.parse import urlsplit
root=ROOT/'dataset/personal_data_protection_github/source/linked_artifacts_20261105_v9'
def get(url):
 with tempfile.TemporaryDirectory() as t:
  r=subprocess.run(['curl','--location','--fail','--silent','--show-error','--connect-timeout','6','--max-time','18','--max-filesize','5000000','--user-agent','CODA-research-evidence','--output',t+'/body','--write-out','%{url_effective}\n%{content_type}',url],capture_output=True,text=True,timeout=22)
  if r.returncode:raise ValueError(r.stderr.strip())
  final,ct=r.stdout.split('\n',1);data=Path(t+'/body').read_text()
  return {'url':url,'final_url':final,'text':data,'content_type':ct,'fetched_at':datetime.now(timezone.utc).isoformat(),'sha256':hashlib.sha256(data.encode()).hexdigest()}
def ext(link):
 url=link['url']
 try:
  raw=get(url)
  if urlsplit(raw['final_url']).hostname not in HOSTS:raise ValueError('Unverified redirected host: '+raw['final_url'])
  write_json(root/'external_raw'/(hashlib.sha256(url.encode()).hexdigest()+'.json'),raw)
  result=collect(link,root,1)
  if result['status']!='unavailable':write_json(root/'external_results'/(hashlib.sha256(url.encode()).hexdigest()+'.json'),result)
  return {'url':url,'status':result['status'],'reason':result.get('reason'),'final_url':raw['final_url']}
 except Exception as e:return {'url':url,'status':'failed','reason':str(e)}
def dspace(key,number):
 url='https://jira.lyrasis.org/browse/'+key
 path=root/'external_results'/(hashlib.sha256(url.encode()).hexdigest()+'.json');old=json.loads(path.read_text())
 try:
  base=f'https://api.github.com/repos/DSpace/DSpace/issues/{number}'
  raw=get(base);issue=json.loads(raw['text']);comments=[];sources=[raw]
  assert issue['number']==number and issue['title'].startswith('['+key+']') and url in issue['body'] and 'Imported from JIRA' in issue['body']
  for page in range(1,1+max(1,(issue['comments']+99)//100)):
   cr=get(base+f'/comments?per_page=100&page={page}');sources.append(cr);comments.extend(json.loads(cr['text']))
  assert len(comments)==issue['comments'] and len({c['id'] for c in comments})==len(comments)
  assert all(c['issue_url']==base for c in comments)
  for source in sources:write_json(root/'archive_raw'/(hashlib.sha256(source['url'].encode()).hexdigest()+'.json'),source)
  doc={'source_key':key,'imported_issue_url':issue['html_url'],'title':issue['title'],'body':issue['body'],'state':issue['state'],'updated_at':issue['updated_at'],'comments':[{k:c.get(k) for k in ['id','html_url','body','created_at','updated_at']} for c in comments]}
  old.update(text=json.dumps(doc,ensure_ascii=False,indent=2),status='partial',fetched_at=raw['fetched_at'],recovered_comment_count=len(comments),expected_imported_comment_count=issue['comments'],source_sha256=hashlib.sha256(json.dumps(doc,ensure_ascii=False,sort_keys=True).encode()).hexdigest(),raw_sources=[{'url':x['url'],'sha256':x['sha256']} for x in sources],reason='Official migrated issue body and all currently exposed GitHub comments recovered. Original Jira attachments, edit history and import completeness are not established.')
  write_json(path,old)
  return {'url':url,'status':'partial','comments':len(comments),'identity_verified':True}
 except Exception as e:return {'url':url,'status':'failed','reason':str(e)}
