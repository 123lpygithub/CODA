"""Create a new evidence version while retaining every frozen case allocation."""
from __future__ import annotations
import argparse
from dataclasses import asdict
import hashlib
import json
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from adapters import Defects4CodeLLMSemanticAdapter, MLSATD23ShadesAdapter, PersonalDataProtectionGitHubAdapter
from coda.study import evidence_sha256, load_study_manifest, select_study_artifacts, study_group, validate_study_manifest


def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-manifest',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--study-id',required=True)
    parser.add_argument('--evidence-profile',choices=['paper-20261105','paper-20261105-expanded','paper-20261105-continued','paper-20261105-ready','paper-20261105-recovered','paper-20261105-v9','paper-20261106-v10'],required=True)
    args=parser.parse_args()
    if args.output.exists(): parser.error('Use a new output directory; existing snapshots cannot be overwritten.')
    os.environ['CODA_EVIDENCE_PROFILE']=args.evidence_profile
    old=load_study_manifest(args.source_manifest)
    adapters=[Defects4CodeLLMSemanticAdapter(), MLSATD23ShadesAdapter(), PersonalDataProtectionGitHubAdapter()]
    pools={adapter.load_dataset_metadata().dataset_name:{a.artifact_id:a for a in adapter.iter_artifacts()} for adapter in adapters}
    manifest=json.loads(json.dumps(old))
    manifest.update(study_id=args.study_id, evidence_profile=args.evidence_profile,
                    previous_manifest_sha256=old['manifest_sha256'])
    changed={}
    for dataset,entry in manifest['datasets'].items():
        changed[dataset]=0
        for row in entry['artifacts']:
            artifact=pools[dataset][row['artifact_id']]
            if study_group(dataset,artifact)!=(row['group_family'],row['group_id']):
                parser.error('Group changed; a pure evidence refresh cannot change the allocation.')
            digest=evidence_sha256(artifact)
            changed[dataset]+=digest!=row['evidence_sha256']
            row.update(evidence_sha256=digest,content_sha256=hashlib.sha256(artifact.content.encode()).hexdigest())
    manifest.pop('manifest_sha256')
    manifest['manifest_sha256']=hashlib.sha256(json.dumps(manifest,sort_keys=True,ensure_ascii=False,separators=(',',':'),allow_nan=False).encode()).hexdigest()
    validate_study_manifest(manifest)
    for dataset in manifest['datasets']:
        for phase in ['pilot','formal']:
            select_study_artifacts(manifest,dataset,pools[dataset].values(),phase)
    # Store exact inputs as an immutable offline companion, not only hashes.
    evidence={dataset:[asdict(pools[dataset][row['artifact_id']]) for row in entry['artifacts']]
              for dataset,entry in manifest['datasets'].items()}
    evidence_text=json.dumps(evidence,ensure_ascii=False,indent=2)+'\n'
    audit={'previous_manifest_sha256':old['manifest_sha256'],'manifest_sha256':manifest['manifest_sha256'],
           'evidence_profile':args.evidence_profile,'changed_evidence_counts':changed,
           'case_ids_groups_phases_and_order_preserved':True,
           'input_snapshot_sha256':hashlib.sha256(evidence_text.encode()).hexdigest(),
           'experimental_outputs_recomputed':False}
    args.output.mkdir(parents=True)
    for name,value in [('study_manifest.json',manifest),('evidence_audit.json',audit)]:
        (args.output/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
    (args.output/'agent_inputs.json').write_text(evidence_text)
    print(json.dumps(audit,indent=2))


if __name__=='__main__': main()
