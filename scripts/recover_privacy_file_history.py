"""Recover deleted linked files at explicit Git commits, keeping historical scope.

Uses the repository's path-filtered commit history and verified parent pointers.
No fork substitution, guessed filename, or claim of case-time equivalence.
"""
from __future__ import annotations
import argparse
import base64
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
from pathlib import Path
import re
import sys
from urllib.parse import quote, unquote, urlsplit, urlencode
from http.client import HTTPException

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from scripts.prepare_privacy_linked_artifacts import Collector
from scripts.prepare_privacy_issue_discussions import write_json, CacheMiss, RateLimited
from scripts.prepare_privacy_web_evidence import EmbeddedIssueParser, read_page


def blob_text(collector,repo,commit,filename):
    url=f'https://github.com/{repo}/blob/{commit}/{quote(filename,safe="/")}'
    raw=read_page(url,collector.root,collector.timeout)
    parser=EmbeddedIssueParser();parser.feed(raw['html'])
    payload=json.loads(''.join(parser.parts))['payload']
    location=payload.get('codeViewBlobLayoutRoute',payload)
    info=location.get('refInfo') or payload.get('refInfo') or {}
    blob=location.get('blob') or payload.get('blob') or {}
    path=location.get('path') or payload.get('path')
    lines=blob.get('rawLines')
    if lines is None:
        lines=payload.get('codeViewBlobLayoutRoute.StyledBlob',{}).get('rawLines')
    if path!=filename or info.get('currentOid')!=commit or not isinstance(lines,list) or not all(isinstance(x,str) for x in lines):
        raise ValueError('Blob page does not verify exact path/revision and original source lines.')
    text='\n'.join(lines)
    return {'url':url,'text':text,'sha256':hashlib.sha256(text.encode()).hexdigest(),
            'fetched_at':raw['fetched_at'],'extraction_method':'GitHub embedded rawLines; line ending bytes may be normalized'}


def historical_text(collector,repo,commit,filename):
    url=f'https://raw.githubusercontent.com/{repo}/{commit}/{quote(filename,safe="/")}'
    try:
        return collector.text(url)
    except (OSError,HTTPException,ValueError):
        # The raw-content host can be unavailable while GitHub REST still
        # serves the identical Git blob. Verify path and blob identity.
        endpoint=f'https://api.github.com/repos/{repo}/contents/{quote(filename,safe="/")}?ref={commit}'
        try:
            response=collector.api(endpoint);data=response['data']
        except Exception:
            return blob_text(collector,repo,commit,filename)
        if data.get('path')!=filename or data.get('type')!='file' or data.get('encoding')!='base64':
            raise ValueError('REST content is not the exact historical text file.')
        content=base64.b64decode(data['content'])
        blob=hashlib.sha1(b'blob '+str(len(content)).encode()+b'\0'+content).hexdigest()
        if blob!=data['sha']:raise ValueError('REST historical Git blob mismatch.')
        text=content.decode('utf-8')
        if '\x00' in text:raise ValueError('Historical resource is binary.')
        return {'url':endpoint,'text':text,'sha256':hashlib.sha256(content).hexdigest(),
                'fetched_at':response['fetched_at'],'git_blob_sha1':blob}


def path_history(collector,repo,filename):
    query='https://api.github.com/repos/'+repo+'/commits?'+urlencode({'path':filename,'per_page':5})
    try:
        history=collector.api(query)
        if isinstance(history['data'],list) and history['data']:return query,history
    except Exception:pass
    # Public history pages do not consume authenticated REST quota. Verify the
    # actual filtered path; never use a repository's unrelated commit list.
    for branch in ('master','main','develop','development','devel'):
        url=f'https://github.com/{repo}/commits/{branch}/{quote(filename,safe="/")}'
        try:
            raw=read_page(url,collector.root,collector.timeout)
            parser=EmbeddedIssueParser();parser.feed(raw['html'])
            route=json.loads(''.join(parser.parts))['payload']['commitsRefRoute']
            if route.get('filters',{}).get('currentBlobPath')!=filename:continue
            records=[{'sha':c['oid'],'parents':[],'commit':{'committer':{'date':c.get('committedDate')}}}
                     for group in route['commitGroups'] for c in group['commits']]
            if records:return url,{'data':records[:5],'fetched_at':raw['fetched_at']}
        except (OSError,HTTPException,ValueError,KeyError):continue
    raise ValueError('No verified exact-path history returned by REST or structured history page.')


def recover(link, collector):
    result=dict(link);segments=urlsplit(link['url']).path.strip('/').split('/')
    repo='/'.join(segments[:2]);filename=unquote('/'.join(segments[4:]))
    if len(segments)<5 or segments[2]!='blob' or re.fullmatch('[0-9a-fA-F]{40}',segments[3]):
        raise ValueError('Only deleted branch-linked files need path history recovery.')
    query,history=path_history(collector,repo,filename)
    if not isinstance(history['data'],list) or not history['data']:
        raise ValueError('No exact-path commit history returned.')
    attempts=[];seen=set()
    for entry in history['data']:
        # A removal commit itself has no file; its verified direct parent may.
        candidates=[entry['sha']]+[p['sha'] for p in entry.get('parents',[])]
        for commit in candidates:
            if commit in seen:continue
            seen.add(commit)
            if not re.fullmatch('[0-9a-fA-F]{40}',commit):raise ValueError('Invalid history commit.')
            url=f'https://raw.githubusercontent.com/{repo}/{commit}/{quote(filename,safe="/")}'
            try:
                raw=historical_text(collector,repo,commit,filename);lines=raw['text'].splitlines()
                anchor=re.fullmatch(r'L(\d+)(?:-L?(\d+))?',urlsplit(link['url']).fragment)
                text=raw['text'];line_note=''
                if anchor:
                    first,last=int(anchor[1]),int(anchor[2] or anchor[1])
                    if not 1<=first<=last<=len(lines):
                        line_note=' The original cited line range does not exist in this historical file; full text retained without relocating the citation.'
                    else:
                        first,last=max(1,first-12),min(len(lines),last+12)
                        text='\n'.join(lines[first-1:last]);result.update(line_start=first,line_end=last)
                result.update(status='partial',historical_evidence=True,revision=commit,immutable_revision=True,
                    retrieval_url=raw['url'],text=text,source_sha256=raw['sha256'],fetched_at=raw['fetched_at'],
                    recovery_method='Exact repository/path Git history; explicit commit or its recorded direct parent',
                    history_query_url=query,history_response_sha256=hashlib.sha256(json.dumps(history['data'],sort_keys=True).encode()).hexdigest(),
                    history_entry_sha=entry['sha'],history_commit_date=entry.get('commit',{}).get('committer',{}).get('date'),
                    reason='Historical file recovered at a verified path-history commit. Original branch target and case-time version are unknown; cited line semantics may differ. Do not infer deployment or resolution.'+line_note)
                return result
            except (OSError,HTTPException,ValueError,CacheMiss,RateLimited) as error:attempts.append(f'{commit}: {error}')
    raise ValueError('No text file retrieved from exact-path history: '+'; '.join(attempts))


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--snapshots',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    p.add_argument('--timeout',type=float,default=12);p.add_argument('--workers',type=int,default=4)
    args=p.parse_args();root=args.output.resolve()
    collector=Collector(root,args.snapshots.resolve(),args.timeout,False)
    manifest=json.loads((root/'manifest.json').read_text());links={}
    for entry in manifest['artifacts'].values():
        for item in json.loads((root/entry['file']).read_text())['links']:
            if item['kind']=='file' and item['status']=='unavailable':links[item['url']]=item
    # Prior recovery may not yet have been rematerialized into the manifest.
    links={u:l for u,l in links.items() if not ((p:=root/'results'/(hashlib.sha256(u.encode()).hexdigest()+'.json')).exists() and json.loads(p.read_text()).get('history_query_url'))}
    audit=[]
    def attempt(link):
        try:
            result=recover(link,collector)
            write_json(root/'results'/(hashlib.sha256(link['url'].encode()).hexdigest()+'.json'),result)
            return {'url':link['url'],'status':result['status'],'revision':result['revision']}
        except Exception as error:
            return {'url':link['url'],'status':'unavailable','error':f'{type(error).__name__}: {error}'}
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        for future in as_completed([pool.submit(attempt,l) for l in links.values()]):
            row=future.result();audit.append(row);print(json.dumps(row),flush=True)
    write_json(root/'file_history_recovery_audit.json',audit)


if __name__=='__main__':main()
