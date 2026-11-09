"""Retain verified related-revision SATD context without rewriting source pointers.

Candidates come from released preprocessing rows, never reference coding labels.
Related branch/later context remains partial and cannot prove case-time behavior.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys
from urllib.parse import quote

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from adapters import MLSATD23ShadesAdapter
from scripts.prepare_satd_source_context import extract_excerpt, write_json
from scripts.recover_satd_archived_context import Archive


def verify_relation(data: dict, candidate: str, published: str) -> str:
    if data.get('base_commit',{}).get('sha')!=candidate:
        raise ValueError('Comparison base differs from candidate.')
    status=data.get('status')
    if status=='ahead' and data.get('behind_by')==0 and data.get('merge_base_commit',{}).get('sha')==candidate:
        return 'verified-ancestor'
    if status=='behind' and data.get('ahead_by')==0 and data.get('merge_base_commit',{}).get('sha')==published:
        return 'verified-descendant'
    if status=='diverged' and data.get('merge_base_commit',{}).get('sha'):
        return 'verified-related-branch'
    raise ValueError('Comparison does not prove a supported revision relation.')


def recover(artifact, candidate: dict, root: Path, archive: Archive) -> dict:
    fields=artifact.raw_fields
    published=fields['comment_introducing_revision'].rsplit('/',1)[-1]
    repo=fields['comment_introducing_revision'].split('github.com/')[1].split('/commit/')[0]
    commit=candidate['commit']
    expected=f'https://raw.githubusercontent.com/{repo}/{commit}/{quote(fields["filename"],safe="/")}'
    if candidate['source_url'].lower()!=expected.lower() or not candidate.get('unique_match'):
        raise ValueError('Candidate source identity or original full-comment match missing.')
    compare=f'https://api.github.com/repos/{repo}/compare/{commit}...{published}'
    data,relation_raw=archive.read(compare)
    relation=verify_relation(json.loads(data),commit,published)
    source,raw=archive.read(expected)
    excerpt=extract_excerpt(source.decode(),fields['comment_text'])
    if excerpt is None:raise ValueError('No unique complete normalized comment at related revision.')
    first,last,text=excerpt
    note=(f'The released introducing pointer does not contain the full comment. This excerpt uniquely matches it at a {relation} revision. '
          'It is supplemental historical context, not evidence that the published case revision has this implementation. '
          'Do not infer case-time behavior or debt resolution from the alternate version.')
    payload={'artifact_id':artifact.artifact_id,'revision_url':fields['comment_introducing_revision'],
             'published_commit':published,'filename':fields['filename'],'commit':commit,
             'source_url':expected,'source_sha256':raw['sha256'],'fetched_at':raw['fetched_at'],
             'line_start':first,'line_end':last,'excerpt':text,'status':'historical_partial',
             'revision_relation':relation,'revision_note':note,
             'match_policy':'unique-full-comment-at-related-revision-from-released-preprocessing-record',
             'alternate_dataset_id':candidate['alternate_dataset_id'],
             'comparison_url':compare,'comparison_sha256':relation_raw['sha256'],
             'original_comment_and_revision_preserved':True}
    relative=f'excerpts/{artifact.artifact_id}.json';path=root/relative;write_json(path,payload)
    return {'status':'historical_partial','file':relative,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
            'revision_relation':relation}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--candidates',type=Path,required=True)
    p.add_argument('--timeout',type=float,default=12)
    args=p.parse_args();root=args.output.resolve();manifest=json.loads((root/'manifest.json').read_text())
    candidates=json.loads(args.candidates.read_text());archive=Archive(root,args.timeout)
    for artifact in MLSATD23ShadesAdapter().iter_artifacts():
        entry=manifest['artifacts'][artifact.artifact_id]
        if entry['status'] not in ('unmatched','unavailable'):continue
        attempts=[]
        for c in candidates:
            if c['artifact_id']!=artifact.artifact_id or not c.get('unique_match'):continue
            try:
                manifest['artifacts'][artifact.artifact_id]=recover(artifact,c,root,archive)
                break
            except (OSError,ValueError,KeyError) as e:attempts.append(str(e))
        else:entry['history_recovery_errors']=attempts
        manifest['counts']={s:sum(e['status']==s for e in manifest['artifacts'].values()) for s in
                            ['available','ambiguous','historical_partial','unmatched','unavailable','pending']}
        write_json(root/'manifest.json',manifest)
        print(artifact.artifact_id,manifest['artifacts'][artifact.artifact_id]['status'],attempts,flush=True)


if __name__=='__main__':main()
