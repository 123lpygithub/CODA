"""Supplement incomplete Privacy evidence using GitHub's embedded original Markdown.

No HTML-to-text reconstruction: only structured original body/comment fields.
A discussion is complete only when comment counts and both timeline directions
confirm full coverage. Paginated pages remain partial and can be resumed via REST.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import hashlib
from http.client import HTTPException
from html.parser import HTMLParser
import json
from pathlib import Path
import sys
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from adapters.github_issue_snapshot import normalize_snapshot, load_snapshot
from adapters.personal_data_protection_github import PersonalDataProtectionGitHubAdapter
from scripts.prepare_privacy_issue_discussions import save_snapshot, update_manifest, write_json


class EmbeddedIssueParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.active=False
        self.parts=[]

    def handle_starttag(self, tag, attrs):
        attrs=dict(attrs)
        if tag=='script' and attrs.get('data-target')=='react-app.embeddedData' and attrs.get('type')=='application/json':
            self.active=True

    def handle_data(self, data):
        if self.active:
            self.parts.append(data)

    def handle_endtag(self, tag):
        if tag=='script':
            self.active=False


def embedded_issue(html: str) -> dict:
    parser=EmbeddedIssueParser();parser.feed(html)
    payload=json.loads(''.join(parser.parts))
    return payload['payload']['issueViewerRoute']['data']['repository']['issue']


def parse_snapshot(html: str, artifact_id: str, source_url: str, fetched_at: str, final_url: str | None = None) -> dict:
    issue=embedded_issue(html)
    final_identity=(final_url or source_url).split('?')[0].rstrip('/')
    if urlsplit(issue['url']).hostname!='github.com' or issue['number']!=int(final_identity.split('/')[-1]):
        raise ValueError('Unexpected issue identity in embedded GitHub data.')
    repo=issue['repository']['nameWithOwner']
    canonical=f'https://github.com/{repo}/issues/{issue["number"]}'
    if issue['url'].lower()!=canonical.lower():
        raise ValueError('Embedded repository and issue URL differ.')
    if issue['url'].lower().rstrip('/') != final_identity.lower():
        raise ValueError('Embedded issue does not match the final GitHub redirect URL.')
    def user(author):
        return {'id':author.get('id') or author.get('login')} if author else None
    api='https://api.github.com/repos/'+repo+'/issues/'+str(issue['number'])
    response={'requested_url':source_url.replace('https://github.com/','https://api.github.com/repos/'),
              'fetched_at':fetched_at,'data':{
                  'url':api,'html_url':canonical,'number':issue['number'],'title':issue['title'],
                  'body':issue['body'],'user':user(issue.get('author')),'created_at':issue['createdAt'],
                  'updated_at':issue['updatedAt'],'state':issue['state'].lower(),'closed_at':None,
                  'comments':issue['totalCommentsCount']}}
    comments={}; pagination=False
    for field in ['timelineItems','backTimelineItems']:
        timeline=issue.get(field) or {}
        page=timeline.get('pageInfo') or {}
        if field=='timelineItems':
            pagination=page.get('hasNextPage',True) or page.get('hasPreviousPage',True)
        for edge in timeline.get('edges',[]):
            node=edge.get('node') or {}
            if node.get('__typename')!='IssueComment':
                continue
            # Missing/hidden bodies must not silently become empty evidence.
            if not isinstance(node.get('body'),str):
                continue
            ident=node['databaseId']
            comments[ident]={'id':ident,'html_url':node['url'],'created_at':node['createdAt'],
                             'updated_at':node.get('lastEditedAt'),
                             'body':node['body'],'user':user(node.get('author'))}
    pages=[{'fetched_at':fetched_at,'data':list(comments.values())}]
    snapshot=normalize_snapshot(artifact_id,response,pages,comments_complete=not pagination)
    snapshot.update(retrieval_method='GitHub public issue page embedded original Markdown',
                    retrieval_url=source_url, closed_at_available=False)
    if canonical.lower()!=source_url.split('?')[0].rstrip('/').lower():
        snapshot.update(identity_relation='GitHub HTTPS redirect to canonical issue',
                        canonical_redirect_url=final_identity)
    snapshot['scope']="Retrieval-time original issue/comment Markdown from GitHub's structured page data; full discussion only when count and pagination checks pass. Closure time is not available from this endpoint. Linked material is stored separately."
    return snapshot


def read_page(url: str, root: Path, timeout: float) -> dict:
    cache=root/'web_raw'/(hashlib.sha256(url.encode()).hexdigest()+'.json')
    if cache.exists():
        raw=json.loads(cache.read_text())
        if raw['url']!=url or hashlib.sha256(raw['html'].encode()).hexdigest()!=raw['sha256']:
            raise ValueError('Web cache identity or checksum mismatch.')
        return raw
    with urlopen(Request(url,headers={'User-Agent':'CODA-research-evidence'}),timeout=timeout) as response:
        if urlsplit(response.url).hostname!='github.com':
            raise ValueError('Unsupported issue redirect.')
        data=response.read(10_000_001)
        if len(data)>10_000_000:
            raise ValueError('Issue page exceeds 10 MB.')
        raw={'url':url,'final_url':response.url,'html':data.decode('utf-8'),'fetched_at':datetime.now(timezone.utc).isoformat(),'sha256':hashlib.sha256(data).hexdigest()}
    write_json(cache,raw)
    return raw


def collect_paginated(url: str, aid: str, root: Path, timeout: float) -> dict:
    raw=read_page(url,root,timeout)
    snapshot=parse_snapshot(raw['html'],aid,url,raw['fetched_at'],raw.get('final_url'))
    pages=[raw]
    comments={c['id']:c for c in snapshot['comments']}
    issue=embedded_issue(raw['html'])
    first=issue['timelineItems']
    expected=snapshot['expected_comment_count']
    complete=not first['pageInfo'].get('hasNextPage',True) and not first['pageInfo'].get('hasPreviousPage',True)
    participants={}
    def merge_participants(s):
        # Participant labels are local to each page; remap using the original
        # author IDs from that page, never equating "Participant 2" across pages.
        original=embedded_issue(s['html'])
        authors={}
        for field in ['timelineItems','backTimelineItems']:
            for edge in (original.get(field) or {}).get('edges',[]):
                n=edge.get('node') or {}
                if n.get('__typename')=='IssueComment':
                    a=n.get('author') or {};authors[n.get('databaseId')]=a.get('id') or a.get('login') or 'deleted'
        return authors
    # Author of the issue occupies Participant 1.
    author=issue.get('author') or {}
    participants[author.get('id') or author.get('login') or 'deleted']='Participant 1'
    pages_seen=set()
    for page_number in range(1,10001):
        if complete:
            break
        try:
            page=read_page(snapshot['issue_url']+'?timeline_page='+str(page_number),root,timeout)
            extra=parse_snapshot(page['html'],aid,snapshot['issue_url'],page['fetched_at'],page.get('final_url'))
            page_issue=embedded_issue(page['html'])
            if extra['issue_url']!=snapshot['issue_url'] or extra['expected_comment_count']!=expected or extra['updated_at']!=snapshot['updated_at'] or extra['body']!=snapshot['body']:
                raise ValueError('Issue changed during pagination; use a new retrieval snapshot.')
            timeline=page_issue['timelineItems'];info=timeline['pageInfo']
            signature=(info.get('startCursor'),info.get('endCursor'))
            if signature in pages_seen:
                raise ValueError('Repeated timeline page; pagination made no progress.')
            pages_seen.add(signature)
            pages.append(page)
            comments.update({c['id']:c for c in extra['comments']})
            complete=not info.get('hasNextPage',True)
        except (OSError,HTTPException,ValueError,KeyError,TypeError) as error:
            snapshot['pagination_error']=f'{type(error).__name__}: {error}'
            break
    for page in pages:
        authors=merge_participants(page)
        for ident,key in authors.items():
            if ident in comments:
                comments[ident]['author']=participants.setdefault(key,f'Participant {len(participants)+1}')
    snapshot['comments']=sorted(comments.values(),key=lambda c:(c['created_at'],c['id']))
    snapshot['retrieved_comment_count']=len(comments)
    snapshot['comments_complete']=complete and len(comments)==expected
    snapshot['evidence_status']='complete' if snapshot['comments_complete'] else 'partial'
    snapshot['comments_fetched_at']=[p['fetched_at'] for p in pages]
    snapshot['timeline_page_urls']=[p['url'] for p in pages]
    snapshot['scope']="Retrieval-time original Markdown from GitHub's structured issue pages, including numbered timeline pages. Discussion complete only after pagination, comment-ID, expected-count and unchanged-issue checks. Closure timestamp is unavailable; linked material is stored separately."
    return snapshot


def collect(row: dict, root: Path, timeout: float) -> tuple[str,dict|None,str|None]:
    aid=f"privacy-issue-{row['index']}";url=row['html_url']
    cache=root/'web_raw'/(hashlib.sha256(url.encode()).hexdigest()+'.json')
    try:
        if urlsplit(url).scheme!='https' or urlsplit(url).hostname!='github.com':
            raise ValueError('Unsupported issue host.')
        return aid,collect_paginated(url,aid,root,timeout),None
    except (OSError,HTTPException,ValueError,KeyError,TypeError) as error:
        return aid,None,f'{type(error).__name__}: {error}'


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--timeout',type=float,default=12)
    parser.add_argument('--workers',type=int,default=4)
    args=parser.parse_args()
    if args.timeout<=0 or not 1<=args.workers<=8:
        parser.error('timeout positive; workers 1–8')
    root=args.output.resolve();path=root/'manifest.json'
    manifest=json.loads(path.read_text())
    rows=[row for row in PersonalDataProtectionGitHubAdapter()._load_rows() if manifest['artifacts'][f"privacy-issue-{row['index']}"]['status']!='complete']
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures={executor.submit(collect,row,root,args.timeout):row for row in rows}
        for future in as_completed(futures):
            aid,snapshot,error=future.result();entry=manifest['artifacts'][aid]
            if snapshot:
                existing=load_snapshot(root,aid,futures[future]['html_url'])
                # Preserve a richer partial snapshot instead of dropping comment pages.
                if not existing or snapshot['evidence_status']=='complete' or snapshot['retrieved_comment_count']>=existing['retrieved_comment_count']:
                    save_snapshot(root,entry,snapshot)
                    entry.pop('error',None)
                entry['web_retrieval_status']=snapshot['evidence_status']
            else:
                entry['web_error']=error
            update_manifest(root,manifest)
            print(aid,entry['status'],manifest['counts'],flush=True)
    return 0


if __name__=='__main__':
    raise SystemExit(main())
