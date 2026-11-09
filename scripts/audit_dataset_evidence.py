"""Report available evidence and explicit gaps for a selected local collection."""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from adapters import MLSATD23ShadesAdapter, PersonalDataProtectionGitHubAdapter
from adapters.github_issue_snapshot import load_snapshot
from adapters.github_linked_evidence import load_linked_evidence


def audit() -> dict:
    satd = MLSATD23ShadesAdapter()
    privacy = PersonalDataProtectionGitHubAdapter()
    if satd._context_dir is None or privacy._linked_dir is None:
        raise ValueError('Select a supplemental CODA_EVIDENCE_PROFILE.')
    sm = json.loads((satd._context_dir/'manifest.json').read_text())
    pm = json.loads((privacy._snapshot_dir/'manifest.json').read_text())
    satd_gaps, corrections = [], []
    # Adapters check checksums, identity and agent-visible rendering.
    satd_artifacts = list(satd.iter_artifacts())
    privacy_artifacts = list(privacy.iter_artifacts())
    for artifact in satd_artifacts:
        entry = sm['artifacts'][artifact.artifact_id]
        if entry['status'] != 'available':
            satd_gaps.append({'artifact_id':artifact.artifact_id,'status':entry['status'],
                              'candidate_count':entry.get('candidate_count',0),
                              'revision_url':artifact.raw_fields['comment_introducing_revision'],
                              'filename':artifact.raw_fields['filename'],
                              'comment':artifact.raw_fields['comment_text'],
                              'attempts':entry.get('recovery_attempts',[])})
        if artifact.raw_fields.get('source_context_revision_note'):
            corrections.append({'artifact_id':artifact.artifact_id,
                                'source_commit':artifact.raw_fields['source_context_commit'],
                                'note':artifact.raw_fields['source_context_revision_note']})
    unique_links, all_links, privacy_gaps, external_links = {}, [], [], []
    for row in privacy._load_rows():
        aid = f"privacy-issue-{row['index']}"
        snapshot = load_snapshot(privacy._snapshot_dir,aid,row['html_url'])
        if not snapshot or snapshot['evidence_status'] != 'complete':
            privacy_gaps.append({'artifact_id':aid,'issue_url':row['html_url'],
                                 'historical_only':bool(snapshot and snapshot.get('historical_evidence')),
                                 'body_available':bool(snapshot and snapshot.get('issue_body_available',True)),
                                 'retrieved_comments':snapshot['retrieved_comment_count'] if snapshot else 0,
                                 'expected_comments':snapshot['expected_comment_count'] if snapshot else None})
        linked = load_linked_evidence(privacy._linked_dir,aid,row['html_url'],snapshot)
        for link in linked['links'] if linked else []:
            all_links.append(link)
            unique_links[link['url']] = link
        if os.environ.get('CODA_EVIDENCE_PROFILE') in ('paper-20261105-ready', 'paper-20261105-recovered', 'paper-20261105-v9', 'paper-20261106-v10'):
            external = load_linked_evidence(privacy._linked_dir,aid,row['html_url'],snapshot,
                                           manifest_name='external_manifest.json')
            external_links.extend(external['links'] if external else [])
    return {'date':datetime.now(timezone.utc).date().isoformat(),
            'evidence_profile':os.environ.get('CODA_EVIDENCE_PROFILE'),
            'satd':{'case_count':len(satd_artifacts),'counts':sm['counts'],
                    'remaining_gaps':satd_gaps,'version_corrections':corrections},
            'privacy':{'case_count':len(privacy_artifacts),'counts':pm['counts'],
                       'historical_only_cases':sum(x['historical_only'] for x in privacy_gaps),
                       'remaining_gaps':privacy_gaps,
                       'retrieved_comments':sum(a.raw_fields['retrieved_comment_count'] for a in privacy_artifacts)},
            'linked_artifacts':{'unique_url_count':len(unique_links),'case_link_count':len(all_links),
                                'case_link_status_counts':dict(Counter(x['status'] for x in all_links)),
                                'unique_url_status_counts':dict(Counter(x['status'] for x in unique_links.values())),
                                'historical_only_unique_urls':sum(bool(x.get('historical_evidence')) for x in unique_links.values()),
                                'remaining_gaps':[x for x in unique_links.values() if x['status']!='available']},
            'external_artifacts':{'unique_url_count':len({x['url'] for x in external_links}),
                                  'case_link_count':len(external_links),
                                  'case_link_status_counts':dict(Counter(x['status'] for x in external_links)),
                                  'remaining_gaps':[x for x in {i['url']:i for i in external_links}.values() if x['status']!='available']},
            'experimental_outputs_recomputed':False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    args = parser.parse_args()
    result = audit()
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({key:{k:v for k,v in value.items() if k not in ('remaining_gaps','version_corrections')}
                      for key,value in result.items() if isinstance(value,dict)},indent=2))


if __name__ == '__main__':
    main()
