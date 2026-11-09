"""Collect one-hop GitHub files, commits, PRs and linked issues from fixed discussions.

Preserves exact retrieval content; links are not evidence of successful fixes.
No recursive crawl and no reference labels. Rerun to retry incomplete entries.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import hashlib
from http.client import HTTPException
import json
from pathlib import Path
import re
import sys
import threading
from urllib.parse import urlsplit, quote, unquote
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from adapters.github_issue_snapshot import load_snapshot
from adapters.github_linked_evidence import discover_links, snapshot_digest
from adapters.personal_data_protection_github import PersonalDataProtectionGitHubAdapter
from scripts.prepare_privacy_issue_discussions import fetch, RateLimited, CacheMiss, write_json


class Collector:
    def __init__(self, root: Path, issue_root: Path, timeout: float, offline: bool):
        self.root, self.issue_root, self.timeout, self.offline = root, issue_root, timeout, offline
        self.rate_limited = threading.Event()
        self._locks_guard = threading.Lock()
        self._locks = {}

    def lock(self, url: str):
        with self._locks_guard:
            return self._locks.setdefault(url, threading.Lock())

    def api(self, url: str) -> dict:
        with self.lock(url):
            return self._api(url)

    def _api(self, url: str) -> dict:
        try:
            return fetch(url, self.issue_root/'raw', self.timeout, 1,
                         offline=self.offline or self.rate_limited.is_set())
        except RateLimited:
            self.rate_limited.set()
            raise

    def text(self, url: str) -> dict:
        with self.lock(url):
            return self._text(url)

    def _text(self, url: str) -> dict:
        allowed = {'github.com', 'raw.githubusercontent.com', 'patch-diff.githubusercontent.com'}
        if urlsplit(url).scheme != 'https' or urlsplit(url).hostname not in allowed:
            raise ValueError('Unsupported development-evidence host.')
        path = self.root/'raw'/(hashlib.sha256(url.encode()).hexdigest()+'.json')
        if path.exists():
            raw = json.loads(path.read_text(encoding='utf-8'))
            if raw.get('url') != url or hashlib.sha256(raw['text'].encode()).hexdigest() != raw.get('sha256'):
                raise ValueError('Linked raw cache identity or checksum mismatch.')
            return raw
        if self.offline:
            raise CacheMiss(url)
        with urlopen(Request(url, headers={'User-Agent':'CODA-research-evidence'}), timeout=self.timeout) as response:
            if urlsplit(response.url).hostname not in allowed:
                raise ValueError('Unsupported evidence redirect.')
            data = response.read(5_000_001)
            if len(data) > 5_000_000:
                raise ValueError('Linked source exceeds 5 MB; retain as an explicit evidence gap.')
            text = data.decode('utf-8')
            if '\x00' in text or 'text/html' in response.headers.get('Content-Type', ''):
                raise ValueError('Binary or HTML content is not a supported source document.')
            raw = {'url':url, 'final_url':response.url, 'text':text,
                   'fetched_at':datetime.now(timezone.utc).isoformat(), 'sha256':hashlib.sha256(data).hexdigest()}
        write_json(path, raw)
        return raw

    def historical_issue(self, repo: str, ident: str) -> dict:
        """Recover explicit linked-issue event text without claiming completeness."""
        from scripts.recover_privacy_event_archive import query, recover
        row={'index':'linked-'+repo.replace('/','-')+'-'+ident,
             'project':repo,'issue_number':ident,
             'html_url':f'https://github.com/{repo}/issues/{ident}',
             'url':f'https://api.github.com/repos/{repo}/issues/{ident}'}
        events,_=query(row,self.root,self.timeout)
        issues=[e for e in events if e['event_type']=='IssuesEvent']
        if not issues:
            raise ValueError('No archived issue event to establish linked issue context.')
        opening=next((e for e in issues if e['action']=='opened'),issues[0])
        row.update(title=opening['title'],created_at=opening['created_at'],
                   **{'#comments':str(max(e['comments'] for e in issues))})
        _,snapshot,audit=recover(row,self.root,self.timeout)
        if snapshot is None or not snapshot.get('issue_body_available'):
            raise ValueError('No original linked issue body in archived events.')
        return {'text':json.dumps(snapshot,ensure_ascii=False,indent=2),'status':'partial',
                'historical_evidence':True,'fetched_at':snapshot['issue_fetched_at'],
                'retrieved_comment_count':snapshot['retrieved_comment_count'],
                'expected_comment_count':snapshot['expected_comment_count'],
                'archive_event_count':audit['event_count'],
                'reason':'Historical GH Archive event text only; current body, edits and discussion completeness are unverified.'}

    def source_location(self, link: dict) -> tuple[str, str, str, bool]:
        """Resolve blob path boundaries from GitHub metadata, including slash refs."""
        parts=urlsplit(link['url']);segments=parts.path.strip('/').split('/')
        repo='/'.join(segments[:2]);start=2 if parts.hostname=='raw.githubusercontent.com' else 3
        ref,filename=unquote(segments[start]),unquote('/'.join(segments[start+1:]))
        if re.fullmatch('[0-9a-fA-F]{40}',ref):
            return repo,ref,filename,True
        try:
            # Blob pages establish both currentOid and the full ref/path split.
            from scripts.prepare_privacy_web_evidence import read_page, EmbeddedIssueParser
            if not self.offline and parts.hostname=='github.com':
                with self.lock('blob:'+link['url'].split('#')[0]):
                    raw=read_page(link['url'].split('#')[0],self.root,self.timeout)
                parser=EmbeddedIssueParser();parser.feed(raw['html'])
                payload=json.loads(''.join(parser.parts))['payload']
                location=payload.get('codeViewBlobLayoutRoute',payload)
                info=location.get('refInfo') or payload.get('refInfo') or {}
                path=location.get('path') or payload.get('path')
                oid=info.get('currentOid');name=info.get('name')
                final_path=unquote(urlsplit(raw.get('final_url',raw['url'])).path)
                final_repo='/'.join(final_path.strip('/').split('/')[:2])
                if (isinstance(path,str) and isinstance(name,str) and
                    isinstance(oid,str) and re.fullmatch('[0-9a-fA-F]{40}',oid) and
                    final_path==f'/{final_repo}/blob/{name}/{path}'):
                    return final_repo,oid,path,True
        except (OSError,HTTPException,ValueError,KeyError,TypeError):
            pass
        try:
            ref=self.api(f'https://api.github.com/repos/{repo}/commits/{quote(ref,safe="")}')['data']['sha']
            return repo,ref,filename,True
        except (OSError,ValueError,KeyError,RateLimited,CacheMiss):
            return repo,ref,filename,False

    def paginated_records(self, url: str) -> list[dict]:
        records=[];seen=set()
        while url:
            if url in seen:raise ValueError('Repeated API pagination URL.')
            seen.add(url);response=self.api(url)
            if not isinstance(response['data'],list):raise ValueError('Expected API record array.')
            records.extend(response['data']);url=response['next_url']
        return records

    def pull_request_from_issue(self, response: dict) -> dict:
        """Retain PR interpretation and review evidence when /issues/N is a PR."""
        issue=response['data'];result={
            'resource_type':'pull_request','canonical_url':issue['html_url'],
            'fetched_at':response['fetched_at'],'status':'partial',
        }
        documents={'issue':{k:issue.get(k) for k in ['title','body','state','closed_at','updated_at']}}
        failures=[]
        for name,url in [('comments',issue['comments_url']+'?per_page=100'),
                         ('reviews',issue['pull_request']['url']+'/reviews?per_page=100'),
                         ('review_comments',issue['pull_request']['url']+'/comments?per_page=100')]:
            try:
                records=self.paginated_records(url)
                documents[name]=[{key:record.get(key) for key in
                    ['id','html_url','body','state','created_at','updated_at','submitted_at',
                     'commit_id','path','line','original_line','diff_hunk'] if key in record}
                    for record in records]
            except (OSError,HTTPException,ValueError,KeyError,RateLimited,CacheMiss) as error:
                failures.append(f'{name}: {error}')
        try:
            metadata=self.api(issue['pull_request']['url'])['data']
            documents['pull_request']={k:metadata.get(k) for k in ['state','merged','merged_at','merge_commit_sha','updated_at']}
            result.update(revision=metadata['head']['sha'],immutable_revision=False)
            raw=self.text(issue['pull_request'].get('patch_url') or issue['html_url']+'.patch')
            documents['patch']=raw['text']
        except (OSError,HTTPException,ValueError,KeyError,RateLimited,CacheMiss) as error:
            failures.append(f'PR metadata/patch: {error}')
        comments=documents.get('comments',[])
        if len({c['id'] for c in comments})!=issue['comments']:
            failures.append('Issue comment count mismatch.')
        result.update(text=json.dumps(documents,ensure_ascii=False,indent=2),
                      status='partial' if failures else 'available',
                      reason='; '.join(failures),retrieved_comment_count=len(comments),
                      expected_comment_count=issue['comments'])
        return result

    def collect(self, link: dict) -> dict:
        result = dict(link)
        parts = urlsplit(link['url'])
        segments = parts.path.strip('/').split('/')
        repo = '/'.join(segments[:2])
        api_base = f'https://api.github.com/repos/{repo}'
        try:
            if link['kind'] == 'file':
                repo,ref,filename,immutable=self.source_location(link)
                if not filename:
                    raise ValueError('Missing linked filename.')
                try:
                    raw = self.text(f'https://raw.githubusercontent.com/{repo}/{quote(ref,safe="/")}/{quote(filename, safe="/")}')
                except (OSError, HTTPException, ValueError, CacheMiss):
                    if not immutable or self.offline:
                        raise
                    from scripts.recover_satd_archived_context import Archive
                    archived = Archive(self.root, self.timeout).source(ref, filename)
                    raw = {'text':archived['source'],'sha256':archived['source_sha256'],
                           'fetched_at':archived['fetched_at'],'url':archived['source_url']}
                    result.update(recovery_method='Software Heritage exact Git revision and verified blob',
                                  git_blob_sha1=archived['git_blob_sha1'])
                result.update(revision=ref, immutable_revision=immutable)
                text = raw['text']
                lines = text.splitlines()
                match = re.fullmatch(r'L(\d+)(?:-L?(\d+))?', parts.fragment)
                if match:
                    first, last = int(match[1]), int(match[2] or match[1])
                    if not 1 <= first <= last <= len(lines):
                        raise ValueError('Cited line range does not exist at retrieved revision.')
                    first, last = max(1, first-12), min(len(lines), last+12)
                    result.update(line_start=first, line_end=last)
                    text = '\n'.join(lines[first-1:last])
                result.update(text=text, source_sha256=raw['sha256'], fetched_at=raw['fetched_at'], retrieval_url=raw['url'], status='available')
            elif link['kind'] in ('commit', 'pull_request'):
                ident = re.sub(r'\.(?:patch|diff)$', '', segments[3])
                if link['kind'] == 'commit' and not re.fullmatch('[0-9a-fA-F]{7,40}', ident):
                    raise ValueError('Invalid commit identifier.')
                if link['kind'] == 'pull_request' and not ident.isdigit():
                    raise ValueError('Invalid pull-request number.')
                metadata = None
                try:
                    endpoint = 'commits' if link['kind']=='commit' else 'pulls'
                    metadata = self.api(f'{api_base}/{endpoint}/{ident}')
                except (OSError, ValueError, KeyError, RateLimited, CacheMiss):
                    pass
                try:
                    raw = self.text(f'https://github.com/{repo}/{segments[2]}/{ident}.patch')
                    result.update(text=raw['text'], source_sha256=raw['sha256'], fetched_at=raw['fetched_at'], retrieval_url=raw['url'], status='available')
                except (OSError, HTTPException, ValueError, CacheMiss) as error:
                    if metadata is None:
                        raise
                    result.update(text='', status='partial', reason=f'Patch not retrieved: {error}')
                if metadata is not None:
                    data = metadata['data']
                    if link['kind']=='pull_request':
                        details = {k:data.get(k) for k in ['title','body','state','merged','merged_at','merge_commit_sha','updated_at']}
                        result.update(revision=data['head']['sha'], immutable_revision=False,
                                      metadata_fetched_at=metadata['fetched_at'])
                        result['text'] = json.dumps(details, ensure_ascii=False, indent=2)+'\n\nPatch:\n'+result['text']
                    else:
                        result.update(revision=data['sha'], immutable_revision=True)
                        result['text'] = json.dumps({
                            'message':data.get('commit', {}).get('message'),
                            'files':[{'filename':f.get('filename'),'status':f.get('status'),'patch':f.get('patch')}
                                     for f in data.get('files', [])],
                        }, ensure_ascii=False, indent=2) + '\n\nPatch:\n' + result['text']
                else:
                    result.update(revision=ident, immutable_revision=link['kind']=='commit' and len(ident)==40,
                                  metadata_status='unavailable; a patch alone does not establish merge or deployment')
            else:
                ident = segments[3]
                if not ident.isdigit():
                    raise ValueError('Invalid linked issue number.')
                try:
                    response = self.api(f'{api_base}/issues/{ident}')
                except (OSError, ValueError, RateLimited, CacheMiss):
                    if self.offline:
                        raise
                    from scripts.prepare_privacy_web_evidence import collect as collect_web
                    web_url = f'https://github.com/{repo}/issues/{ident}'
                    with self.lock('web:' + web_url):
                        _, snapshot, error = collect_web({'index':'linked-'+ident, 'html_url':web_url}, self.root, self.timeout)
                    if snapshot is None:
                        # /issues/N can redirect to /pull/N. Use the canonical
                        # API issue endpoint, which preserves the original link.
                        from scripts.prepare_privacy_web_evidence import read_page
                        try:
                            page=read_page(web_url,self.root,self.timeout)
                            final=urlsplit(page.get('final_url',web_url))
                            target=final.path.strip('/').split('/')
                            if len(target)==4 and target[2]=='pull' and target[3].isdigit():
                                canonical_api=f'https://api.github.com/repos/{"/".join(target[:2])}/issues/{target[3]}'
                                canonical=self.api(canonical_api)
                                if 'pull_request' in canonical['data']:
                                    result.update(self.pull_request_from_issue(canonical))
                                    return result
                        except (OSError,HTTPException,ValueError,KeyError,RateLimited,CacheMiss):
                            pass
                        try:
                            result.update(self.historical_issue(repo,ident))
                            result['current_retrieval_error']=error
                        except (OSError,HTTPException,ValueError,KeyError,TypeError) as archive_error:
                            raise ValueError(f'{error}; archive: {archive_error}') from archive_error
                        return result
                    result.update(text=json.dumps(snapshot, ensure_ascii=False, indent=2),
                                  status='available' if snapshot['comments_complete'] else 'partial',
                                  fetched_at=snapshot['issue_fetched_at'],
                                  retrieved_comment_count=snapshot['retrieved_comment_count'],
                                  expected_comment_count=snapshot['expected_comment_count'],
                                  reason='' if snapshot['comments_complete'] else 'Linked issue discussion is paginated or incomplete.')
                    return result
                data = response['data']
                if 'pull_request' in data:
                    result.update(self.pull_request_from_issue(response))
                    return result
                text = json.dumps({k:data.get(k) for k in ['title','body','state','closed_at','updated_at']}, ensure_ascii=False, indent=2)
                url = data['comments_url']+'?per_page=100&page=1' if data['comments'] else None
                comments, failure = {}, None
                try:
                    while url:
                        page = self.api(url)
                        for comment in page['data']:
                            comments[comment['id']] = {k:comment.get(k) for k in ['id','html_url','body','created_at','updated_at']}
                        url = page['next_url']
                except (OSError, ValueError, RateLimited, CacheMiss) as error:
                    failure = str(error) or type(error).__name__
                complete = not failure and len(comments)==data['comments']
                text += '\n\nComments:\n'+json.dumps(sorted(comments.values(), key=lambda c:(c['created_at'],c['id'])),ensure_ascii=False,indent=2)
                result.update(text=text, status='available' if complete else 'partial', fetched_at=response['fetched_at'],
                              retrieved_comment_count=len(comments), expected_comment_count=data['comments'],
                              reason=failure or ('' if complete else 'Comment count changed during retrieval.'))
        except (OSError, HTTPException, ValueError, KeyError, RateLimited, CacheMiss) as error:
            result.update(status='unavailable', reason=f'{type(error).__name__}: {error}')
        return result


def prepare(args) -> int:
    root, issue_root = args.output.resolve(), args.snapshots.resolve()
    path = root/'manifest.json'
    manifest = json.loads(path.read_text()) if path.exists() else {'format':'coda-privacy-linked-evidence','format_version':1,'artifacts':{}}
    collector = Collector(root, issue_root, args.timeout, args.offline)
    cases, links, old_links = [], {}, {}
    for row in PersonalDataProtectionGitHubAdapter()._load_rows():
        aid = f"privacy-issue-{row['index']}"
        snapshot = load_snapshot(issue_root, aid, row['html_url'])
        discovered = discover_links(snapshot) if snapshot else []
        previous = manifest['artifacts'].get(aid, {})
        if previous.get('file'):
            from adapters.github_linked_evidence import load_linked_evidence
            try:
                payload = load_linked_evidence(root, aid, row['html_url'], snapshot)
            except ValueError as error:
                if 'different issue snapshot' not in str(error):
                    raise
                payload = None
            if payload:
                old_links.update({item['url']:item for item in payload['links'] if item['status']=='available'})
        cases.append((aid, row['html_url'], snapshot, discovered))
        for link in discovered:
            links.setdefault(link['url'], link)
    results = dict(old_links)
    for url in links:
        cached = root/'results'/(hashlib.sha256(url.encode()).hexdigest()+'.json')
        if cached.exists():
            item = json.loads(cached.read_text())
            if item.get('url') != url:
                raise ValueError('Linked result identity mismatch.')
            results[url] = item
    pending = [link for url,link in links.items() if results.get(url, {}).get('status') != 'available']
    if args.kinds:
        pending = [link for link in pending if link['kind'] in args.kinds]
    if args.pending_only:
        pending = [link for link in pending if results.get(link['url'], {}).get('status', 'pending') == 'pending']
    if args.materialize_only:
        pending = []
    if args.limit is not None:
        pending = pending[:args.limit]
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = [executor.submit(collector.collect, link) for link in pending]
        for index, future in enumerate(as_completed(futures), 1):
            result = future.result()
            previous = results.get(result['url'], {})
            if previous.get('text') and result['status']=='unavailable':
                result = dict(previous, last_retry_error=result.get('reason'))
            results[result['url']] = result
            write_json(root/'results'/(hashlib.sha256(result['url'].encode()).hexdigest()+'.json'), result)
            # The text/raw cache is written per request, so interrupted work resumes.
            print(f"{index}/{len(pending)}: {result['kind']} {result['status']}", flush=True)
    for aid, issue_url, snapshot, discovered in cases:
        items = [dict(results.get(link['url'], dict(link,status='pending',reason='Not yet attempted.')), cited_in=link['cited_in']) for link in discovered]
        payload = {'artifact_id':aid,'source_issue_url':issue_url,'issue_snapshot_sha256':snapshot_digest(snapshot),
                   'scope':'One-hop explicitly linked GitHub source files, commit patches, PR metadata/patches, and linked issue discussions. Branch links reflect retrieval-time content unless resolved to a commit. No recursive expansion or external attachments.',
                   'links':items}
        relative = f'issues/{aid}.json'
        write_json(root/relative, payload)
        manifest['artifacts'][aid] = {'file':relative,'sha256':hashlib.sha256((root/relative).read_bytes()).hexdigest(),
                                    'issue_evidence_available':snapshot is not None,'link_count':len(items),
                                    'counts':{s:sum(i['status']==s for i in items) for s in ['available','partial','unavailable','pending']}}
    manifest['counts'] = {s:sum(e['counts'][s] for e in manifest['artifacts'].values()) for s in ['available','partial','unavailable','pending']}
    manifest['unique_link_count'] = len(links)
    manifest['updated_at'] = datetime.now(timezone.utc).isoformat()
    write_json(path, manifest)
    print(json.dumps(manifest['counts']), flush=True)
    return 0 if all(manifest['counts'][status] == 0 for status in ['partial','unavailable','pending']) else 2


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--snapshots', type=Path, default=ROOT/'dataset/personal_data_protection_github/source/github_snapshot_20261105')
    parser.add_argument('--output', type=Path, default=ROOT/'dataset/personal_data_protection_github/source/linked_artifacts_20261105')
    parser.add_argument('--timeout', type=float, default=12)
    parser.add_argument('--workers', type=int, default=4)
    parser.add_argument('--offline', action='store_true')
    parser.add_argument('--materialize-only', action='store_true', help='Build manifests from existing collected results without requests or retries.')
    parser.add_argument('--pending-only', action='store_true', help='Attempt never-collected URLs before retrying known failures.')
    parser.add_argument('--limit', type=int)
    parser.add_argument('--kinds', nargs='+', choices=['file','commit','pull_request','issue'], help='Prioritize selected kinds; retain all discovered links in the manifest.')
    args = parser.parse_args()
    if args.timeout <= 0 or not 1 <= args.workers <= 8 or (args.limit is not None and args.limit < 1):
        parser.error('timeout/limit must be positive and workers between 1 and 8')
    return prepare(args)


if __name__=='__main__':
    raise SystemExit(main())
