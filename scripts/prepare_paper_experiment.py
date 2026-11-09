"""Verify frozen paper inputs and prepare matched runs without model calls.

Default: offline preflight and 36-condition plan. --check-run-creation additionally
creates and reloads every condition in a temporary directory. --create-run
persists only the explicitly selected condition; human decisions are never filled.
"""
from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import asdict
import hashlib
import json
import os
from pathlib import Path
import shlex
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from adapters import Defects4CodeLLMSemanticAdapter, MLSATD23ShadesAdapter, PersonalDataProtectionGitHubAdapter
from coda.llm import web_model_configurations
from coda.study import evidence_sha256, load_study_manifest, select_study_artifacts
from coda.sensitivity import complete_evidence_case
from coda.web.runtime import CodaWebService

ADAPTERS = {'llm_code_error_semantic': Defects4CodeLLMSemanticAdapter,
            'ml_satd_23_shades': MLSATD23ShadesAdapter,
            'personal_data_protection_github': PersonalDataProtectionGitHubAdapter}
EXPECTED = {'llm_code_error_semantic': (557, 113, 444),
            'ml_satd_23_shades': (856, 169, 687),
            'personal_data_protection_github': (652, 132, 520)}


def verify_bundle(bundle: Path):
    manifest = load_study_manifest(bundle / 'study_manifest.json')
    audit = json.loads((bundle / 'evidence_audit.json').read_text())
    data = (bundle / 'agent_inputs.json').read_bytes()
    if (audit['manifest_sha256'] != manifest['manifest_sha256'] or
            hashlib.sha256(data).hexdigest() != audit['input_snapshot_sha256']):
        raise ValueError('Frozen companion or manifest checksum mismatch.')
    if set(manifest['datasets']) != set(EXPECTED):
        raise ValueError('The paper requires exactly the three study datasets.')
    # Select the profile from the verified manifest, never silently from a shell
    # default. Live sources must still equal the exact frozen companion.
    os.environ['CODA_EVIDENCE_PROFILE'] = manifest['evidence_profile']
    frozen = json.loads(data)
    pools, report = {}, {}
    hidden = {'Software TD Type','ML TD Type','ML TD Type 2','ML Pipeline Stage',
              'is_privacy_related','trigger_rater_2','privacy_issue_rater_2',
              'consent_interaction_rater_2','resolution_rater_2','reason_rater_2_category',
              'error_type','error_category','observed_label','taxonomy'}
    for dataset, factory in ADAPTERS.items():
        adapter = factory()
        artifacts = (list(adapter.iter_solution_artifacts()) if dataset == 'llm_code_error_semantic'
                     else list(adapter.iter_artifacts()))
        if len(artifacts) != EXPECTED[dataset][0]:
            raise ValueError(f'{dataset}: unexpected source-case count.')
        snapshots = {item['artifact_id']:item for item in frozen[dataset]}
        if len(snapshots) != len(frozen[dataset]) or set(snapshots) != {a.artifact_id for a in artifacts}:
            raise ValueError(f'{dataset}: companion/source case identities differ.')
        states = Counter()
        empty_bodies = []
        for artifact in artifacts:
            if not artifact.content.strip() or hidden.intersection(artifact.raw_fields):
                raise ValueError(f'{dataset}/{artifact.artifact_id}: empty evidence or hidden reference field.')
            if asdict(artifact) != snapshots[artifact.artifact_id]:
                raise ValueError(f'{dataset}/{artifact.artifact_id}: exact frozen input differs.')
            for ref in artifact.source_refs:
                if ref.field and ref.field not in artifact.raw_fields:
                    raise ValueError(f'{dataset}/{artifact.artifact_id}: invalid source field {ref.field}.')
            if dataset == 'ml_satd_23_shades':
                if not (artifact.raw_fields.get('source_context') or artifact.raw_fields.get('source_context_candidates')):
                    raise ValueError('SATD has no viewable code context.')
                states[artifact.raw_fields['source_context_status']] += 1
            elif dataset == 'personal_data_protection_github':
                if artifact.raw_fields.get('body') is None or artifact.raw_fields['body'] == '[Issue body not retrieved.]':
                    raise ValueError('Privacy has no issue-body evidence.')
                if not artifact.raw_fields['body'].strip():
                    empty_bodies.append(artifact.artifact_id)
                states[artifact.raw_fields['evidence_status']] += 1
        pools[dataset] = {}
        for index, phase in enumerate(('pilot','formal'), 1):
            selected = select_study_artifacts(manifest, dataset, artifacts, phase)
            if len(selected) != EXPECTED[dataset][index]:
                raise ValueError(f'{dataset}/{phase}: unexpected phase count.')
            pools[dataset][phase] = selected
        report[dataset] = {'source_cases':len(artifacts), 'pilot_cases':len(pools[dataset]['pilot']),
                           'formal_cases':len(pools[dataset]['formal']), 'evidence_status_counts':dict(states),
                           'retrieved_empty_body_cases':empty_bodies,
                           'formal_cases_without_known_evidence_gaps':sum(complete_evidence_case(asdict(a)) for a in pools[dataset]['formal'])}
        if report[dataset]['formal_cases_without_known_evidence_gaps'] < 50:
            raise ValueError(f'{dataset}: fewer than 50 source-complete supplementary cases.')
    return manifest, pools, report


def condition_plan(manifest, pools):
    return [{'condition_id':f'{phase}:{dataset}:S{mode_index}:r{replicate}',
             'dataset_name':dataset, 'study_phase':phase, 'review_mode':mode,
             'replicate_index':replicate,
             'comparison_block_id':f'{manifest["study_id"]}:{phase}:{dataset}:r{replicate}',
             'case_count':len(pools[dataset][phase]),
             'ordered_evidence_sha256':hashlib.sha256(json.dumps(
                 [(a.artifact_id,evidence_sha256(a)) for a in pools[dataset][phase]],
                 separators=(',',':')).encode()).hexdigest(),
             'human_review_required':mode != 'automatic'}
            for phase in ('pilot','formal') for dataset in ADAPTERS for replicate in (1,2)
            for mode_index, mode in enumerate(('automatic','selective','full'),1)]


def create_condition(service, condition, manifest_path, participant_id=None):
    return service.create_run(dataset_name=condition['dataset_name'], review_mode=condition['review_mode'],
                              study_manifest_path=str(manifest_path.resolve()), study_phase=condition['study_phase'],
                              participant_id=participant_id, replicate_index=condition['replicate_index'],
                              comparison_block_id=condition['comparison_block_id'], iterative_batch_size=1)


def check_run_creation(conditions, manifest_path, pools):
    checks=[]
    with tempfile.TemporaryDirectory(prefix='coda-paper-preflight-') as temporary:
        service=CodaWebService(runs_root=temporary, adapter_factories=ADAPTERS)
        for condition in conditions:
            created=create_condition(service,condition,manifest_path,
                'temporary-preflight-reviewer' if condition['human_review_required'] else None)
            resumed=CodaWebService(runs_root=temporary, adapter_factories=ADAPTERS)
            state=resumed._load_run_state(created['run_id'])
            expected=pools[condition['dataset_name']][condition['study_phase']]
            actual=[a for batch in state.coding_batches for a in batch.artifacts]
            if ([asdict(a) for a in actual] != [asdict(a) for a in expected] or
                    state.review_policy.setting != condition['review_mode'] or
                    state.metadata['study_execution']['replicate_index'] != condition['replicate_index'] or
                    state.metadata['review_sampling_protocol']['effective_unflagged_audit_rate'] != 0):
                raise ValueError(f'Run creation/reload differs: {condition["condition_id"]}')
            if not resumed._bootstrap_is_pending(state):
                raise ValueError('Creation unexpectedly performed initialization.')
            checks.append(condition['condition_id'])
            print(f'Verified create/reload: {condition["condition_id"]}',flush=True)
    return checks


def main():
    from dotenv import load_dotenv
    load_dotenv(ROOT / '.env', override=False, interpolate=False)
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bundle',type=Path,required=True,help='Path to a locally retained frozen evidence bundle.')
    parser.add_argument('--output',type=Path,help='Write preflight report; use a new file.')
    parser.add_argument('--check-run-creation',action='store_true')
    parser.add_argument('--create-run',action='store_true')
    parser.add_argument('--dataset',choices=tuple(ADAPTERS))
    parser.add_argument('--phase',choices=('pilot','formal'))
    parser.add_argument('--review-mode',choices=('automatic','selective','full'))
    parser.add_argument('--replicate',type=int,choices=(1,2))
    parser.add_argument('--participant-id')
    parser.add_argument('--runs-root',type=Path,default=ROOT/'runs/paper')
    args=parser.parse_args()
    if args.output and args.output.exists():parser.error('Preserve prior preflight reports; choose a new output file.')
    if args.create_run:
        if not all([args.dataset,args.phase,args.review_mode,args.replicate]):parser.error('Creation requires dataset, phase, review mode and replicate.')
        if args.review_mode!='automatic' and not (args.participant_id or '').strip():parser.error('Reviewed experiment runs require the assigned real participant ID.')
        if args.review_mode=='automatic' and args.participant_id:parser.error('Automatic runs do not have a human participant.')
    elif any([args.dataset,args.phase,args.review_mode,args.replicate,args.participant_id]):
        parser.error('Condition arguments require --create-run.')
    manifest,pools,datasets=verify_bundle(args.bundle.resolve())
    conditions=condition_plan(manifest,pools)
    configs=web_model_configurations()
    models={role:config.model for role,config in configs.items()}
    expected_models={role:('gpt-6.1-sol' if role=='coder_a' else 'gpt-5.6-sol') for role in configs}
    result={'format':'coda-paper-data-preflight','manifest_sha256':manifest['manifest_sha256'],
            'evidence_profile':manifest['evidence_profile'],'inputs_verified':True,
            'reference_fields_excluded':True,'source_citation_fields_verified':True,
            'datasets':datasets,'conditions':conditions,'condition_count':len(conditions),
            'models':models,'models_match_paper':models==expected_models,
            'credential_available_by_role':{r:c.api_key_available() for r,c in configs.items()},
            'transport_timeout_retry_unlimited':all(c.retry_timeouts_forever for c in configs.values()),
            'single_artifact_batches_skip_random_audit':True,
            'paper_exception':'Single-artifact iterative batches skip the 10% audit by explicit project decision; the current manuscript still describes rounded-up batch sampling.',
            'fully_complete_original_evidence':False,
            'experiment_outputs_generated':False,'model_calls_made':False,
            'remaining_requirements':['Keep partial/historical source limitations visible during coding and evaluation.',
                'Assign trained independent human reviewers to S2/S3; never auto-fill their decisions.',
                'Finish calibration scoring and freeze selected evaluators before formal scoring.',
                'Real model/provider availability requires a live API check; credential presence alone is insufficient.']}
    if args.check_run_creation:
        result['temporary_create_reload_checks']=check_run_creation(conditions,args.bundle/'study_manifest.json',pools)
    if args.create_run:
        if not result['models_match_paper']:parser.error('Effective models differ from the paper; fix role configuration before creating this experiment.')
        selected=next(c for c in conditions if (c['dataset_name'],c['study_phase'],c['review_mode'],c['replicate_index']) == (args.dataset,args.phase,args.review_mode,args.replicate))
        created=create_condition(CodaWebService(runs_root=args.runs_root,adapter_factories=ADAPTERS),selected,
                                 args.bundle/'study_manifest.json',args.participant_id)
        result['created_run']=created
        print('Run created without model calls: '+created['run_id'],flush=True)
        print('Start/monitor against a backend using this profile and runs root:\n'+shlex.join([
            sys.executable,'scripts/watch_coda_run.py','--run-id',created['run_id'],
            '--state',str(args.runs_root/'monitors'/f'{created["run_id"]}.json'),'--language','en']),flush=True)
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({key:value for key,value in result.items() if key not in ('conditions','created_run','temporary_create_reload_checks')},ensure_ascii=False,indent=2))


if __name__=='__main__':main()
