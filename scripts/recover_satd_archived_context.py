"""Recover missing SATD files by exact Git revision from Software Heritage.

Git blob hashes, archive checksums and the published full comment are verified.
An ambiguous source comment may be resolved only by a unique added-line span in
that same commit's diff. Never substitutes a newer branch or another repository.
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
from urllib.parse import quote
from urllib.request import Request, urlopen

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from adapters import MLSATD23ShadesAdapter
from scripts.prepare_satd_source_context import canonical_comment, comment_spans, extract_excerpt, write_json


class Archive:
    def __init__(self,root:Path,timeout:float):
        self.root,self.timeout=root,timeout
        self.guard=threading.Lock();self.locks={}

    def read(self,url:str) -> tuple[bytes,dict]:
        with self.guard:
            lock=self.locks.setdefault(url,threading.Lock())
        with lock:
            path=self.root/'archive_raw'/(hashlib.sha256(url.encode()).hexdigest()+'.json')
            if path.exists():
                raw=json.loads(path.read_text());data=raw['text'].encode('utf-8')
                if raw.get('url')!=url or hashlib.sha256(data).hexdigest()!=raw['sha256']:
                    raise ValueError('Archive cache checksum/identity mismatch.')
                return data,raw
            with urlopen(Request(url,headers={'User-Agent':'CODA-research-evidence'}),timeout=self.timeout) as response:
                data=response.read(20_000_001)
                if len(data)>20_000_000:raise ValueError('Archive resource exceeds collection limit.')
                raw={'url':url,'final_url':response.url,'text':data.decode('utf-8'),
                     'fetched_at':datetime.now(timezone.utc).isoformat(),'sha256':hashlib.sha256(data).hexdigest()}
            write_json(path,raw)
            return data,raw

    def json(self,url:str) -> dict:
        data,_=self.read(url);return json.loads(data)

    def source(self,commit:str,filename:str) -> dict:
        revision=self.json(f'https://archive.softwareheritage.org/api/1/revision/{commit}/')
        if revision['id']!=commit:raise ValueError('Archive revision differs from published commit.')
        entry=self.json(f'https://archive.softwareheritage.org/api/1/directory/{revision["directory"]}/{quote(filename,safe="/")}/')
        if entry['type']!='file':raise ValueError('Archived path is not a file.')
        blob=entry['target']
        url=f'https://archive.softwareheritage.org/api/1/content/sha1_git:{blob}/raw/'
        data,raw=self.read(url)
        if hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()!=blob:
            raise ValueError('Archived file Git blob checksum mismatch.')
        if entry.get('checksums',{}).get('sha256',raw['sha256'])!=raw['sha256']:
            raise ValueError('Archived file SHA-256 mismatch.')
        return {'source':data.decode('utf-8'),'source_url':url,'source_sha256':raw['sha256'],
                'fetched_at':raw['fetched_at'],'archive_directory':revision['directory'],'git_blob_sha1':blob,
                'archive_revision_url':f'https://archive.softwareheritage.org/api/1/revision/{commit}/'}


def added_lines(diff:str,filename:str) -> set[int]:
    """New-side line numbers only for the exact target path."""
    current=None;line=None;added=set()
    for value in diff.splitlines():
        if value.startswith('diff --git '):current=None;line=None
        elif value.startswith('+++ b/'):
            current=value[6:];line=None
        elif value.startswith('@@ '):
            match=re.match(r'@@ -\d+(?:,\d+)? \+(\d+)(?:,\d+)? @@',value)
            line=int(match[1]) if match else None
        elif current==filename and line is not None:
            if value.startswith('+'):added.add(line);line+=1
            elif value.startswith(' '):line+=1
            elif value.startswith('-') or value.startswith('\\'):pass
            else:line=None
    return added


def changed_comment_excerpt(source:str,comment:str,diff:str,filename:str) -> tuple[int,int,str]|None:
    lines=source.splitlines()
    pieces=[canonical_comment(p) for p in re.split(r'\s*\|\|\s*|\n',comment) if canonical_comment(p)]
    indexed=[(i+1,canonical_comment(line)) for i,line in enumerate(lines) if canonical_comment(line)]
    target=' '.join(pieces);changed=added_lines(diff,filename);matches=[]
    for index in range(len(indexed)-len(pieces)+1):
        block=indexed[index:index+len(pieces)]
        if ' '.join(t for _,t in block)==target and any(n in changed for n,_ in block):
            matches.append((block[0][0],block[-1][0]))
    # For inline Python comments, tokenize the full field (rather than code text).
    if not matches and len(pieces)==1:
        import io,tokenize
        try:
            for token in tokenize.generate_tokens(io.StringIO(source).readline):
                if token.type==tokenize.COMMENT and canonical_comment(token.string)==target and token.start[0] in changed:
                    matches.append((token.start[0],token.end[0]))
        except (tokenize.TokenError,IndentationError,SyntaxError):pass
    if len(matches)!=1:return None
    first,last=matches[0];first=max(1,first-12);last=min(len(lines),last+12)
    return first,last,'\n'.join(lines[first-1:last])


def recover(artifact,root:Path,archive:Archive) -> tuple[str,dict]:
    fields=artifact.raw_fields;revision=fields['comment_introducing_revision'];filename=fields['filename']
    commit=revision.rsplit('/',1)[-1];repo=revision.split('github.com/',1)[1].split('/commit/')[0]
    manifest=json.loads((root/'manifest.json').read_text());previous=manifest['artifacts'][artifact.artifact_id]
    attempts=[]
    try:
        url=f'https://raw.githubusercontent.com/{repo}/{commit}/{quote(filename,safe="/")}'
        cache=root/'raw'/(hashlib.sha256(url.encode()).hexdigest()+'.json')
        if cache.exists():
            raw=json.loads(cache.read_text())
            if raw.get('url')!=url or hashlib.sha256(raw['source'].encode()).hexdigest()!=raw['source_sha256']:
                raise ValueError('Source cache mismatch.')
            raw=dict(raw,source_url=url)
        else:
            raw=archive.source(commit,filename)
        excerpt=extract_excerpt(raw['source'],fields['comment_text'])
        policy='unique-release-normalized-v2'
        diff_url=revision+'.diff'
        if excerpt is None:
            try:
                data,diff_raw=archive.read(diff_url)
                excerpt=changed_comment_excerpt(raw['source'],fields['comment_text'],data.decode('utf-8'),filename)
                policy='unique-full-comment-on-added-lines-of-exact-commit'
            except (OSError,HTTPException,ValueError,KeyError) as error:
                attempts.append(f'Diff: {type(error).__name__}: {error}')
        if excerpt is None:
            # Some released "introducing" pointers actually delete the exact
            # comment. Recover its verified direct parent and label this
            # difference; never call parent context the introducing version.
            target=canonical_comment(fields['comment_text'])
            try:
                diff_text=data.decode('utf-8')
                current=None;removed=False
                for line in diff_text.splitlines():
                    if line.startswith('diff --git '):current=None
                    elif line.startswith('--- a/'):current=line[6:]
                    elif current==filename and line.startswith('-') and canonical_comment(line[1:])==target:
                        removed=True
                if removed:
                    revision_data=archive.json(f'https://archive.softwareheritage.org/api/1/revision/{commit}/')
                    candidates=[]
                    for relation in revision_data['parents']:
                        parent=relation['id']
                        parent_raw=archive.source(parent,filename)
                        parent_excerpt=extract_excerpt(parent_raw['source'],fields['comment_text'])
                        if parent_excerpt:
                            candidates.append((parent,parent_raw,parent_excerpt))
                    # Merge commits can have two parents. Accept only one parent
                    # with a uniquely matching full comment, never choose one.
                    if len(candidates)==1:
                        parent,parent_raw,parent_excerpt=candidates[0]
                        raw,excerpt=parent_raw,parent_excerpt
                        raw.update(published_commit=commit,revision_relation='direct-parent-before-published-commit',
                                   revision_note='The published introducing-commit pointer deletes this exact comment. The source is from its verified direct parent, where the full comment uniquely matches.')
                        commit=parent
                        policy='unique-full-comment-in-verified-parent-before-deletion'
            except (OSError,HTTPException,ValueError,KeyError,UnboundLocalError) as error:
                attempts.append(f'Parent recovery: {type(error).__name__}: {error}')
        if excerpt is None:
            spans = comment_spans(raw['source'], fields['comment_text'])
            if len(spans) > 1:
                lines = raw['source'].splitlines()
                candidates = []
                for start, end in spans:
                    first, last = max(0, start-12), min(len(lines), end+12)
                    candidates.append({'comment_line_start':start+1, 'comment_line_end':end,
                                       'line_start':first+1, 'line_end':last,
                                       'excerpt':'\n'.join(lines[first:last])})
                payload = {k:v for k,v in raw.items() if k not in ['source','url']}
                payload.update(artifact_id=artifact.artifact_id, revision_url=revision,
                               filename=filename, commit=commit, status='ambiguous',
                               match_policy='all-full-comment-candidates-at-exact-published-revision',
                               candidates=candidates,
                               ambiguity_note='The released comment occurs at multiple source locations. These are all exact full-comment candidates; no location is selected or attributed uniquely to this case.')
                relative=f'excerpts/{artifact.artifact_id}.json';path=root/relative;write_json(path,payload)
                return artifact.artifact_id,{'status':'ambiguous','file':relative,
                    'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'candidate_count':len(candidates)}
            return artifact.artifact_id,dict(previous,recovery_status='unmatched',recovery_attempts=attempts or ['Full comment not uniquely attributable at the exact revision.'])
        first,last,text=excerpt
        payload={k:v for k,v in raw.items() if k not in ['source','url']}
        payload.update(artifact_id=artifact.artifact_id,revision_url=revision,filename=filename,commit=commit,
                       line_start=first,line_end=last,excerpt=text,match_policy=policy)
        if policy.startswith('unique-full'):payload.update(match_diff_url=diff_url,match_diff_sha256=diff_raw['sha256'])
        relative=f'excerpts/{artifact.artifact_id}.json';path=root/relative;write_json(path,payload)
        return artifact.artifact_id,{'status':'available','file':relative,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
    except (OSError,HTTPException,ValueError,KeyError,TypeError) as error:
        return artifact.artifact_id,dict(previous,recovery_status='unavailable',recovery_attempts=[f'{type(error).__name__}: {error}'])


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--timeout',type=float,default=15)
    parser.add_argument('--workers',type=int,default=4)
    args=parser.parse_args()
    if args.timeout<=0 or not 1<=args.workers<=8:parser.error('Positive timeout; workers 1–8.')
    root=args.output.resolve();path=root/'manifest.json';manifest=json.loads(path.read_text());archive=Archive(root,args.timeout)
    artifacts=[a for a in MLSATD23ShadesAdapter().iter_artifacts() if manifest['artifacts'][a.artifact_id]['status'] not in ('available','ambiguous')]
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        for future in as_completed([executor.submit(recover,a,root,archive) for a in artifacts]):
            aid,entry=future.result();manifest['artifacts'][aid]=entry
            manifest['counts']={s:sum(e['status']==s for e in manifest['artifacts'].values()) for s in ['available','ambiguous','unmatched','unavailable','pending']}
            manifest['supplemental_recovery']='Exact Software Heritage Git revision and verified Git blob; full-comment diff disambiguation where unique.'
            write_json(path,manifest);print(aid,entry['status'],manifest['counts'],flush=True)


if __name__=='__main__':main()
