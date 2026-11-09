from recovery_helpers import *
from urllib.parse import urlencode,quote
results=[]
def save(linkurl,raw,method,reason,**extras):
 p=root/'external_results'/(hashlib.sha256(linkurl.encode()).hexdigest()+'.json');old=json.loads(p.read_text())
 old.update(status='partial',text=raw['text'],retrieval_url=raw['final_url'],source_sha256=raw['sha256'],fetched_at=raw['fetched_at'],recovery_method=method,reason=reason,**extras);write_json(p,old)
 write_json(root/'archive_raw'/(hashlib.sha256(raw['url'].encode()).hexdigest()+'.json'),raw)
 results.append({'url':linkurl,'status':'partial','retrieval_url':raw['final_url']})
for path,commit,url in [
 ('articles/azure-monitor/platform/data-locations.md','24591d15d33a12a33c971a30d6fa345e3a331be8','https://docs.microsoft.com/en-us/azure/azure-monitor/platform/data-locations'),
 ('articles/cognitive-services/Face/Face-API-How-to-Topics/HowtoAnalyzeVideo_Face.md','5412f882a720a72fc42691627b3ece498fd678f4','https://docs.microsoft.com/en-us/azure/cognitive-services/face/face-api-how-to-topics/howtoanalyzevideo_face')]:
 try:
  raw=get(f'https://raw.githubusercontent.com/MicrosoftDocs/azure-docs/{commit}/{path}')
  print(path,raw['text'][:800],flush=True)
  save(url,raw,'Official MicrosoftDocs exact source-path Git history; verified parent of removing/renaming commit','Historical original-path documentation recovered; exact case-time deployed page is not established.',revision=commit,historical_evidence=True)
 except Exception as e:results.append({'url':url,'status':'failed','reason':str(e)})
url='https://w3c.github.io/webappsec-feature-policy/'
try:
 from scripts.prepare_privacy_external_evidence import VisibleText
 redirect=get(url);target='https://w3c.github.io/webappsec-permissions-policy/'
 assert target in redirect['text']
 raw=get(target);write_json(root/'archive_raw'/(hashlib.sha256(raw['url'].encode()).hexdigest()+'.json'),raw)
 parser=VisibleText();parser.feed(raw['text']);body=parser.text();assert len(body)>10000 and 'Permissions Policy' in body
 save(url,raw,'Explicit original W3C moved-page link to official successor specification','Current successor specification; original Feature Policy version and case-time equivalence are not established.',migration_notice_url=url,migration_notice_sha256=redirect['sha256'])
 p=root/'external_results'/(hashlib.sha256(url.encode()).hexdigest()+'.json');d=json.loads(p.read_text());d['text']=body;write_json(p,d)
 write_json(root/'archive_raw'/(hashlib.sha256(url.encode()).hexdigest()+'.json'),redirect)
except Exception as e:results.append({'url':url,'status':'failed','reason':str(e)})
write_json(root/'v9_official_documents_audit.json',results);print(json.dumps(results,indent=2))
