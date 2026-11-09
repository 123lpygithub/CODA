"""Recover historical public issue text from GH Archive's ClickHouse mirror.

Historical events supplement unavailable evidence; they never prove complete
current discussions. Human reference labels are not queried or exposed.
"""
from __future__ import annotations
import argparse
from concurrent.futures import ThreadPoolExecutor,as_completed
from datetime import datetime,timezone
import hashlib,json
from pathlib import Path
import sys
from urllib.parse import urlencode
from urllib.request import Request,urlopen

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from adapters import PersonalDataProtectionGitHubAdapter
from adapters.github_issue_snapshot import load_snapshot,normalize_snapshot
from scripts.prepare_privacy_issue_discussions import write_json,save_snapshot,update_manifest


def query(row:dict,root:Path,timeout:float,repo_override:str|None=None):
    repo=repo_override or row['project'];number=int(row['issue_number'])
    import re
    if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+',repo):raise ValueError('Invalid repository.')
    sql=("SELECT event_type,action,actor_login,created_at,updated_at,title,body,comment_id,comments,state,closed_at,file_time,repo_name,number "
         f"FROM github_events WHERE repo_name='{repo}' AND number={number} "
         "AND event_type IN ('IssuesEvent','IssueCommentEvent') ORDER BY created_at,file_time FORMAT JSON")
    url='https://play.clickhouse.com/?'+urlencode({'user':'play','query':sql})
    path=root/'event_archive_raw'/(hashlib.sha256(url.encode()).hexdigest()+'.json')
    if path.exists():
        raw=json.loads(path.read_text())
        if raw.get('url')!=url or hashlib.sha256(json.dumps(raw['response'],ensure_ascii=False,sort_keys=True).encode()).hexdigest()!=raw['response_sha256']:
            raise ValueError('Event archive cache mismatch.')
    else:
        with urlopen(Request(url,headers={'User-Agent':'CODA-research-evidence'}),timeout=timeout) as response:
            data=json.load(response)
        if 'exception' in data:raise ValueError(data['exception'])
        raw={'url':url,'query':sql,'fetched_at':datetime.now(timezone.utc).isoformat(),'response':data,
             'response_sha256':hashlib.sha256(json.dumps(data,ensure_ascii=False,sort_keys=True).encode()).hexdigest()}
        write_json(path,raw)
    events=raw['response']['data']
    if any(e['repo_name']!=repo or e['number']!=number for e in events):raise ValueError('Archived event case identity mismatch.')
    return events,raw


def recover(row,root,timeout):
    aid=f"privacy-issue-{row['index']}"
    try:
        events,raw=query(row,root,timeout)
        if not events and row['project'].lower()=='wappalyzer/wappalyzer':
            # Historical name verified against the release's number, opening
            # timestamp and exact title; reject unrelated same-number issues.
            candidate,alternate=query(row,root,timeout,'AliasIO/Wappalyzer')
            opening=next((e for e in candidate if e['event_type']=='IssuesEvent' and e['action']=='opened'),None)
            if opening and opening['title']==row['title'] and opening['created_at']==row['created_at'].split('.')[0]:
                events,raw=candidate,alternate
        issue_events=[e for e in events if e['event_type']=='IssuesEvent']
        comments={}
        for event in events:
            if event['event_type']=='IssueCommentEvent' and event['comment_id']:
                first=comments.get(event['comment_id'],{}).get('comment_created_at',event['created_at'])
                comments[event['comment_id']]=dict(event,comment_created_at=first)
        issue_event=next((e for e in reversed(issue_events) if e['body']),None)
        if not issue_event and not comments:return aid,None,{'status':'no_text','event_count':len(events)}
        def iso(t):return t.replace(' ','T')+'Z'
        issue_url=row['html_url'];api=row['url']
        latest=issue_events[-1] if issue_events else {}
        expected=max([int(row.get('#comments') or 0)]+[e['comments'] for e in issue_events]+[len(comments)])
        data={'number':int(row['issue_number']),'url':api,'html_url':issue_url,
              'title':issue_event['title'] if issue_event else row['title'],
              'body':issue_event['body'] if issue_event else '[Original issue body not present in retrieved archive events.]',
              'user':{'id':'archived-issue-author'},'created_at':iso(row['created_at'].split('.')[0]),
              'updated_at':iso(latest.get('updated_at') or events[-1]['updated_at']),
              'state':latest.get('state') if latest.get('state') in ['open','closed'] else 'unknown',
              'closed_at':None,'comments':expected}
        pages=[{'fetched_at':raw['fetched_at'],'data':[
            {'id':ident,'html_url':issue_url+f'#issuecomment-{ident}','created_at':iso(event['comment_created_at']),
             'updated_at':iso(event['updated_at']),'user':{'id':event['actor_login']},'body':event['body']}
            for ident,event in comments.items()]}]
        snapshot=normalize_snapshot(aid,{'requested_url':api,'fetched_at':raw['fetched_at'],'data':data},pages,comments_complete=False)
        snapshot.update(retrieval_method='GH Archive public events mirrored by ClickHouse',
                        archive_query_url=raw['url'],archive_response_sha256=raw['response_sha256'],
                        archive_event_count=len(events),issue_body_available=issue_event is not None,
                        archive_latest_event_at=events[-1]['created_at'],historical_evidence=True)
        snapshot['scope']='Historical GitHub public event text retrieved from GH Archive via ClickHouse. This is not a current issue snapshot or proof of a complete discussion. Event coverage can omit edits, deletions and comments. Archived issue-body and comment versions must be interpreted within this stated scope. Linked development material is collected separately.'
        return aid,snapshot,{'status':'recovered_historical','event_count':len(events),'comment_count':len(comments),'issue_body_available':issue_event is not None}
    except (OSError,ValueError,KeyError,TypeError) as error:
        return aid,None,{'status':'failed','error':f'{type(error).__name__}: {error}'}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--timeout',type=float,default=30)
    parser.add_argument('--workers',type=int,default=4)
    args=parser.parse_args();root=args.output.resolve();path=root/'manifest.json';manifest=json.loads(path.read_text())
    rows=[r for r in PersonalDataProtectionGitHubAdapter()._load_rows() if manifest['artifacts'][f"privacy-issue-{r['index']}"]['status']!='complete']
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        for future in as_completed([executor.submit(recover,r,root,args.timeout) for r in rows]):
            aid,snapshot,audit=future.result();entry=manifest['artifacts'][aid];entry['event_archive']=audit
            if snapshot:
                existing=load_snapshot(root,aid,entry['issue_url'])
                if not existing:
                    save_snapshot(root,entry,snapshot)
                else:
                    # Keep current evidence; archive versions are a separate appendix.
                    relative=f'archived_issues/{aid}.json';write_json(root/relative,snapshot)
                    entry['event_archive'].update(file=relative,sha256=hashlib.sha256((root/relative).read_bytes()).hexdigest())
            update_manifest(root,manifest);print(aid,audit,manifest['counts'],flush=True)


if __name__=='__main__':main()
