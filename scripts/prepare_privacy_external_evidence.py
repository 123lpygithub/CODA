"""Collect explicitly cited Jira/policy context into offline Privacy evidence.

Rendered HTML extraction is labelled as such; it is never called original Markdown.
Only the explicitly selected public HTTPS hosts below are fetched, with raw caches.
"""
from __future__ import annotations
import argparse
from concurrent.futures import ThreadPoolExecutor,as_completed
from datetime import datetime,timezone
import hashlib
from http.client import HTTPException
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlsplit,urlunsplit
from urllib.request import Request,urlopen

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from adapters import PersonalDataProtectionGitHubAdapter
from adapters.github_issue_snapshot import load_snapshot
from adapters.github_linked_evidence import snapshot_digest
from scripts.prepare_privacy_issue_discussions import write_json

HOSTS={'mozilla-hub.atlassian.net','jira.lyrasis.org','issues.jenkins.io',
       'bugzilla.mozilla.org','bugs.chromium.org','issues.apache.org',
       'ico.org.uk','gdpr-info.eu','gdpr.eu','www.mozilla.org',
       'docs.microsoft.com','learn.microsoft.com','support.google.com',
       'developer.mozilla.org','developers.google.com','www.w3.org','w3c.github.io'}


class VisibleText(HTMLParser):
    def __init__(self):super().__init__(convert_charrefs=True);self.hidden=0;self.parts=[]
    def handle_starttag(self,tag,attrs):
        if tag in ('script','style','noscript','svg'):self.hidden+=1
        if not self.hidden and tag in ('p','div','li','br','h1','h2','h3','pre','tr'):self.parts.append('\n')
    def handle_endtag(self,tag):
        if tag in ('script','style','noscript','svg'):self.hidden=max(0,self.hidden-1)
        if not self.hidden and tag in ('p','div','li','h1','h2','h3','pre','tr'):self.parts.append('\n')
    def handle_data(self,data):
        if not self.hidden:self.parts.append(data)
    def text(self):
        return '\n'.join(line for p in ''.join(self.parts).splitlines() if (line:=' '.join(p.split())))


def discover(snapshot):
    fields=[('body',snapshot['body'])]+[(f'comment_{c["id"]}',c['body']) for c in snapshot['comments']]
    links={}
    for field,text in fields:
        for url in re.findall(r'https://[^\s<>\[\]()"\x27`]+',text):
            url=url.rstrip('.,;:!?~');parts=urlsplit(url)
            if parts.hostname not in HOSTS:continue
            url=urlunsplit((parts.scheme,parts.netloc,parts.path,parts.query,''))
            item=links.setdefault(url,{'url':url,'kind':'external_url','cited_in':[]})
            if field not in item['cited_in']:item['cited_in'].append(field)
    return list(links.values())


def collect(link,root,timeout):
    result=dict(link);url=link['url'];parts=urlsplit(url)
    if parts.hostname not in HOSTS or parts.scheme!='https':raise ValueError('Unsupported public source.')
    # A Jira JSON response contains the original description and available
    # comments; leave partial unless pagination/count checks establish coverage.
    match=re.search(r'/browse/([A-Z][A-Z0-9]+-\d+)',parts.path)
    target=f'https://{parts.hostname}/rest/api/2/issue/{match[1]}' if match else url
    path=root/'external_raw'/(hashlib.sha256(target.encode()).hexdigest()+'.json')
    try:
        if path.exists():
            raw=json.loads(path.read_text())
            if raw['url']!=target or hashlib.sha256(raw['text'].encode()).hexdigest()!=raw['sha256']:raise ValueError('External cache identity/checksum mismatch.')
        else:
            with urlopen(Request(target,headers={'User-Agent':'CODA-research-evidence','Accept':'application/json,text/html,text/plain'}),timeout=timeout) as response:
                if urlsplit(response.url).hostname not in HOSTS:raise ValueError('Unverified external host redirect.')
                data=response.read(5_000_001)
                if len(data)>5_000_000:raise ValueError('External resource exceeds 5 MB.')
                raw={'url':target,'final_url':response.url,'text':data.decode('utf-8'),
                     'content_type':response.headers.get('Content-Type',''),
                     'fetched_at':datetime.now(timezone.utc).isoformat()}
                raw['sha256']=hashlib.sha256(raw['text'].encode()).hexdigest()
            write_json(path,raw)
        if match:
            data=json.loads(raw['text'])
            if data.get('key')!=match[1]:raise ValueError('Jira issue identity mismatch.')
            fields=data['fields'];comments=fields.get('comment') or {}
            complete=len(comments.get('comments',[]))==comments.get('total') and comments.get('startAt',0)==0
            text=json.dumps({'key':data['key'],'summary':fields.get('summary'),
                 'description':fields.get('description'),'status':fields.get('status'),
                 'resolution':fields.get('resolution'),'comments':comments},ensure_ascii=False,indent=2)
            method='Jira REST fields; pagination and count checked'
            status='available' if complete and fields.get('description') is not None else 'partial'
        elif 'text/html' in raw['content_type']:
            parser=VisibleText();parser.feed(raw['text']);text=parser.text()
            if len(text)<150 or any(t in text.lower()[:1200] for t in ['enable javascript and cookies','checking your browser','access denied','just a moment','log in to jira','log in with atlassian']):raise ValueError('No usable rendered source text; login/challenge or empty page.')
            method='Visible text extracted from retrieved HTML; raw HTML retained, not original Markdown'
            # HTML alone does not prove discussion completeness. A redirected
            # documentation landing page also cannot replace the cited page.
            discussion = parts.hostname in {'bugzilla.mozilla.org','bugs.chromium.org','issues.jenkins.io','issues.apache.org','jira.lyrasis.org','mozilla-hub.atlassian.net'}
            redirected = urlsplit(raw['final_url']).path.rstrip('/') != parts.path.rstrip('/')
            status='partial' if discussion or redirected else 'available'
        elif 'text/plain' in raw['content_type'] or 'application/json' in raw['content_type']:
            text=raw['text'];method='Retrieved source text';status='available'
        else:raise ValueError('Unsupported external document type.')
        result.update(text=text,status=status,source_sha256=raw['sha256'],
                      retrieval_url=raw['final_url'],fetched_at=raw['fetched_at'],
                      extraction_method=method,metadata_status=method,
                      reason='' if status=='available' else 'Extracted source is usable, but discussion completeness or redirected page equivalence is not established.')
    except (OSError,HTTPException,ValueError,KeyError) as error:
        result.update(status='unavailable',reason=f'{type(error).__name__}: {error}')
    return result


def prepare(snapshots,output,timeout,workers,materialize_only=False):
    cases=[];links={};results={};path=output/'external_manifest.json'
    for row in PersonalDataProtectionGitHubAdapter()._load_rows():
        aid=f"privacy-issue-{row['index']}";snapshot=load_snapshot(snapshots,aid,row['html_url'])
        found=discover(snapshot) if snapshot else []
        cases.append((aid,row['html_url'],snapshot,found))
        for link in found:links.setdefault(link['url'],link)
    for url in links:
        cache=output/'external_results'/(hashlib.sha256(url.encode()).hexdigest()+'.json')
        if cache.exists():
            item=json.loads(cache.read_text())
            if item['url']!=url:raise ValueError('External result identity mismatch.')
            results[url]=item
    pending=[] if materialize_only else [l for u,l in links.items() if results.get(u,{}).get('status')!='available']
    with ThreadPoolExecutor(max_workers=workers) as pool:
        for n,future in enumerate(as_completed([pool.submit(collect,l,output,timeout) for l in pending]),1):
            item=future.result();previous=results.get(item['url'],{})
            if previous.get('text') and (item['status']=='unavailable' or
                    previous.get('recovery_method') and item['status']!='available'):
                item=dict(previous,last_retry_error=item.get('reason'))
            results[item['url']]=item
            write_json(output/'external_results'/(hashlib.sha256(item['url'].encode()).hexdigest()+'.json'),item)
            print(n,len(pending),item['status'],flush=True)
    manifest={'format':'coda-privacy-external-evidence','artifacts':{},'host_scope':sorted(HOSTS),'unique_url_count':len(links)}
    for aid,url,snapshot,found in cases:
        items=[dict(results.get(l['url'],dict(l,status='pending')),cited_in=l['cited_in']) for l in found]
        payload={'artifact_id':aid,'source_issue_url':url,'issue_snapshot_sha256':snapshot_digest(snapshot),
                 'scope':'Selected explicitly cited public Jira, policy, standards and documentation sources. Retrieval-time text, not proof of case-time behavior or resolution. Raw responses retained. No recursive expansion or claim that all external evidence is covered.','links':items}
        relative=f'external_issues/{aid}.json';write_json(output/relative,payload)
        manifest['artifacts'][aid]={'file':relative,'sha256':hashlib.sha256((output/relative).read_bytes()).hexdigest(),
            'counts':{s:sum(i['status']==s for i in items) for s in ['available','partial','unavailable','pending']}}
    manifest['counts']={s:sum(e['counts'][s] for e in manifest['artifacts'].values()) for s in ['available','partial','unavailable','pending']}
    write_json(path,manifest);print(json.dumps(manifest['counts']),flush=True)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--snapshots',type=Path,required=True);parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--timeout',type=float,default=8);parser.add_argument('--workers',type=int,default=4)
    parser.add_argument('--materialize-only',action='store_true');args=parser.parse_args()
    if args.timeout<=0 or not 1<=args.workers<=8:parser.error('Positive timeout and workers 1–8 required.')
    prepare(args.snapshots.resolve(),args.output.resolve(),args.timeout,args.workers,args.materialize_only)


if __name__=='__main__':main()
