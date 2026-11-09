from recover import *
# Exact official historical source already retained for the external documentation URL.
pairs={
'https://github.com/Microsoft/azure-docs/blob/master/articles/azure-monitor/platform/data-locations.md':'https://docs.microsoft.com/en-us/azure/azure-monitor/platform/data-locations',
'https://github.com/Microsoft/azure-docs/blob/master/articles/cognitive-services/Face/Face-API-How-to-Topics/HowtoAnalyzeVideo_Face.md':'https://docs.microsoft.com/en-us/azure/cognitive-services/face/face-api-how-to-topics/howtoanalyzevideo_face'}
rows=[]
for original,external in pairs.items():
 p=LINK/'results'/(hashlib.sha256(original.encode()).hexdigest()+'.json');old=json.loads(p.read_text());e=json.loads((LINK/'external_results'/(hashlib.sha256(external.encode()).hexdigest()+'.json')).read_text())
 raw=get(e['retrieval_url']);assert '/MicrosoftDocs/azure-docs/' in raw['url'];assert unquote(urlsplit(original).path).split('/master/',1)[1]==urlsplit(raw['url']).path.split('/',4)[-1]
 old.update(status='partial',text=raw['text'],source_sha256=raw['sha256'],retrieval_url=raw['final_url'],fetched_at=raw['fetched_at'],historical_evidence=True,revision=raw['url'].split('/')[5],immutable_revision=True,related_external_source=external,original_recovery=e,recovery_method='Reuse exact same path in official MicrosoftDocs repository; historical source and removing-commit evidence retained with linked external documentation',reason='Official historical source at exact path; original case-time branch target unknown. No deployment or resolution inference.')
 write_json(p,old);rows.append({'url':original,'status':'partial','retrieval_url':raw['url']})
write_json(AUDIT/'verified_source_reuse.json',rows);print(rows)
