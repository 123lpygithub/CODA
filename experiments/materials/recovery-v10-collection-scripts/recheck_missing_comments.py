from recover import *
from scripts.recover_privacy_event_archive import recover as archive_recover
from adapters import PersonalDataProtectionGitHubAdapter
root=AUDIT/'fresh_event_queries';ids={'21474','2476','2308','8843'}
rows=[r for r in PersonalDataProtectionGitHubAdapter()._load_rows() if r['index'] in ids]
def run(row):
 aid,snapshot,audit=archive_recover(row,root,18)
 if snapshot:write_json(root/'snapshots'/(aid+'.json'),snapshot)
 manifest=json.loads((ISSUE/'manifest.json').read_text());e=manifest['artifacts'][aid];old=json.loads((ISSUE/e['file']).read_text());known={str(c['id']) for c in old['comments']}
 if e.get('event_archive',{}).get('file'):
  prev=json.loads((ISSUE/e['event_archive']['file']).read_text());known.update(str(c['id']) for c in prev['comments'])
 new=[c for c in snapshot['comments'] if str(c['id']) not in known] if snapshot else []
 return {'artifact_id':aid,'audit':audit,'additional_comments':len(new),'additional_comment_ids':[c['id'] for c in new]}
with ThreadPoolExecutor(max_workers=4) as p:out=list(p.map(run,rows))
write_json(root/'audit.json',out);print(json.dumps(out,indent=2))
