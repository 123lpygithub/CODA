"""Recover explicit external references through verified public tracker copies.

Bugzilla REST retains raw comments. DSpace copies require an exact source backlink
and Jira key. Synchronised Jira links are recorded as copies of their parent
GitHub issue, never as newly recovered independent Jira evidence.
"""
from __future__ import annotations
import argparse
from concurrent.futures import ThreadPoolExecutor,as_completed
import hashlib
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlsplit,parse_qs,urlencode

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from scripts.recover_satd_archived_context import Archive
from scripts.prepare_privacy_issue_discussions import write_json
from scripts.prepare_privacy_linked_artifacts import Collector


def save_recovery(root,item):
    path=root/'external_results'/(hashlib.sha256(item['url'].encode()).hexdigest()+'.json')
    if path.exists():
        previous=json.loads(path.read_text())
        if (previous.get('status')=='available' and item['status']!='available' or
                previous.get('recovered_comment_count',0)>item.get('recovered_comment_count',0)):
            return previous
    write_json(path,item)
    return item


def bugzilla(link,archive):
    number=parse_qs(urlsplit(link['url']).query).get('id',[''])[0]
    if not number.isdigit():raise ValueError('Missing numeric Bugzilla identity.')
    base='https://bugzilla.mozilla.org/rest/bug/'+number
    data,raw=archive.read(base);bugs=json.loads(data)['bugs']
    if len(bugs)!=1 or bugs[0]['id']!=int(number):raise ValueError('Bugzilla identity mismatch.')
    comment_data,comment_raw=archive.read(base+'/comment')
    first=json.loads(comment_data)['bugs'][number]
    comments=first['comments']
    ids=[c['id'] for c in comments];counts=[c['count'] for c in comments]
    if any(c['bug_id']!=int(number) or c.get('is_private') for c in comments):raise ValueError('Unexpected Bugzilla comment identity/private flag.')
    continuous=counts==list(range(len(comments))) and len(set(ids))==len(ids)
    # Raw anonymous API may hide private/deleted comments. State this scope;
    # contiguous public ordinal numbers establish only exposed public coverage.
    document={'bug':{k:bugs[0].get(k) for k in ['id','summary','status','resolution','creation_time','last_change_time','url','see_also','is_open']},
              'comments':[{k:c.get(k) for k in ['id','count','creation_time','time','text','raw_text','attachment_id']} for c in comments]}
    text=json.dumps(document,ensure_ascii=False,indent=2)
    return dict(link,text=text,status='available' if continuous else 'partial',
        source_sha256=raw['sha256'],fetched_at=raw['fetched_at'],retrieval_url=base,
        comment_source_url=base+'/comment',comment_source_sha256=comment_raw['sha256'],
        recovered_comment_count=len(comments),recovery_method='Bugzilla REST identity and contiguous public comment ordinals checked',
        metadata_status='Public Bugzilla REST snapshot; raw metadata and comments retained. No assertion about private/deleted comments or original GitHub discussion completeness.',
        reason='' if continuous else 'Public comment ordinals have gaps.')


def dspace(link,collector):
    key=urlsplit(link['url']).path.rstrip('/').split('/')[-1]
    if not re.fullmatch(r'DS-\d+',key):raise ValueError('Not a DSpace issue key.')
    query='https://api.github.com/search/issues?'+urlencode({'q':f'repo:DSpace/DSpace "[{key}]" in:title'})
    comments_error=None
    try:
        response=collector.api(query)
    except Exception:
        # Reuse already retained official search responses when REST quota is
        # exhausted. Same exact-key/backlink checks apply to every candidate.
        items=[];dates=[]
        for path in (collector.issue_root/'raw').glob('*.json'):
            cached=json.loads(path.read_text());data=cached.get('data')
            if cached.get('requested_url','').startswith('https://api.github.com/search/issues?') and isinstance(data,dict):
                items.extend(data.get('items',[]));dates.append(cached['fetched_at'])
        response={'data':{'items':list({i['id']:i for i in items}.values())},'fetched_at':max(dates) if dates else ''}
    matches=[i for i in response['data']['items'] if i.get('title','').startswith('['+key+']') and link['url'] in (i.get('body') or '') and 'Imported from JIRA' in (i.get('body') or '') and i.get('html_url','').startswith('https://github.com/DSpace/DSpace/issues/')]
    if len(matches)!=1:raise ValueError('No unique imported DSpace issue with exact original backlink.')
    issue=matches[0]
    try:
        comments=collector.paginated_records(issue['comments_url']+'?per_page=100')
        if len({c['id'] for c in comments})!=issue['comments']:raise ValueError('Imported issue comment count mismatch.')
    except Exception:
        try:
            from scripts.prepare_privacy_web_evidence import collect_paginated
            snapshot=collect_paginated(issue['html_url'],'migrated-'+key,collector.root,collector.timeout)
            if not snapshot['title'].startswith('['+key+']') or link['url'] not in snapshot['body']:
                raise ValueError('Migrated issue page lost source identity.')
            comments=[{'id':c['id'],'html_url':c['url'],'body':c['body'],'created_at':c['created_at'],'updated_at':c['updated_at']} for c in snapshot['comments']]
            if not snapshot['comments_complete']:comments_error='Imported GitHub discussion is incomplete.'
        except Exception as error:
            comments=[];comments_error=f'Imported discussion not retrieved: {type(error).__name__}: {error}'
    document={'source_key':key,'imported_issue_url':issue['html_url'],'title':issue['title'],
              'body':issue['body'],'state':issue['state'],'updated_at':issue['updated_at'],
              'comments':[{k:c.get(k) for k in ['id','html_url','body','created_at','updated_at']} for c in comments]}
    return dict(link,status='partial',historical_evidence=True,text=json.dumps(document,ensure_ascii=False,indent=2),
        fetched_at=response['fetched_at'],retrieval_url=issue['html_url'],
        source_sha256=hashlib.sha256(json.dumps(document,ensure_ascii=False,sort_keys=True).encode()).hexdigest(),
        search_query_url=query,expected_imported_comment_count=issue['comments'],
        recovery_method='Official DSpace repository Jira import; exact key and original-source backlink verified',
        recovered_comment_count=len(comments),
        reason=('Official migrated issue body recovered. '+(comments_error or 'All exposed GitHub comments recovered.')+
                ' Original Jira attachments, edit history and import completeness are not established.'))


def sync_copy(link,snapshots):
    matches=[]
    for p in (snapshots/'issues').glob('*.json'):
        snapshot=json.loads(p.read_text());body=snapshot['body']
        if re.search(r'Issue is synchronized with this \[Jira Task\]\('+re.escape(link['url'])+r'\)',body):matches.append(snapshot)
    if len(matches)!=1:raise ValueError('No unique explicit parent-to-Jira synchronization declaration.')
    snapshot=matches[0]
    doc={'parent_issue_url':snapshot['issue_url'],'title':snapshot['title'],'body':snapshot['body'],
         'comments':[{k:c.get(k) for k in ['id','url','body','created_at','updated_at']} for c in snapshot['comments']]}
    return dict(link,status='partial',text=json.dumps(doc,ensure_ascii=False,indent=2),
        fetched_at=snapshot['issue_fetched_at'],retrieval_url=snapshot['issue_url'],
        recovery_method='Explicit GitHub-to-Jira synchronization declaration in original issue body',
        independent_evidence=False,
        reason='Parent GitHub issue explicitly names this synchronized Jira task. This is the already available GitHub-side copy, not separately retrieved Jira content; Jira-specific comments and attachments remain unavailable.')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--snapshots',type=Path,required=True);parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--workers',type=int,default=3);parser.add_argument('--timeout',type=float,default=12)
    args=parser.parse_args();root=args.output.resolve();snapshots=args.snapshots.resolve()
    archive=Archive(root,args.timeout);collector=Collector(root,snapshots,args.timeout,False)
    links={}
    manifest=json.loads((root/'external_manifest.json').read_text())
    for e in manifest['artifacts'].values():
        for l in json.loads((root/e['file']).read_text())['links']:
            host=urlsplit(l['url']).hostname
            if l['status']!='available' and ((host=='bugzilla.mozilla.org' and '/show_bug.cgi' in l['url']) or (host=='jira.lyrasis.org' and '/browse/DS-' in l['url']) or (host=='mozilla-hub.atlassian.net' and '/browse/' in l['url'])):links[l['url']]=l
    def run(link):
        try:
            host=urlsplit(link['url']).hostname
            item=bugzilla(link,archive) if host=='bugzilla.mozilla.org' else dspace(link,collector) if host=='jira.lyrasis.org' else sync_copy(link,snapshots)
            if item.get('independent_evidence') is False:
                # Save the relationship separately: do not improve a missing
                # Jira evidence status by duplicating its parent discussion.
                write_json(root/'sync_relations'/(hashlib.sha256(item['url'].encode()).hexdigest()+'.json'),item)
                return {'url':item['url'],'status':'verified_sync_relation','independent_evidence':False}
            item=save_recovery(root,item)
            return {'url':item['url'],'status':item['status'],'comments':item.get('recovered_comment_count')}
        except Exception as error:return {'url':link['url'],'status':'failed','error':f'{type(error).__name__}: {error}'}
    audit=[]
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        for future in as_completed([pool.submit(run,l) for l in links.values()]):
            item=future.result();audit.append(item);print(json.dumps(item),flush=True)
    write_json(root/'external_recovery_audit.json',audit)


if __name__=='__main__':main()
