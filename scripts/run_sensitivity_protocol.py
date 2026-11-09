"""Execute frozen supplementary sensitivity runs with checkpoint resume.

This runner performs real API calls only with --execute. It does not fabricate
scores; use the independent evaluator pipeline on the resulting frozen outputs.
"""
from __future__ import annotations
import argparse
from dataclasses import replace
import hashlib
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from adapters.base import ArtifactRecord, SourceRef, TextLocator
from coda.agents import ContextLLMAgent, ComparisonLLMAgent, ValidationLLMAgent, InductionLLMAgent, build_open_coder, build_initial_open_coder
from coda.bootstrap import BootstrapConfig, EvidenceFirstBootstrap
from coda.llm import LLMModelConfig, load_chat_backend
from coda.orchestrator import CODAOrchestrator
from coda.persistence import save_run_state_checkpoint
from coda.sensitivity import verify_sensitivity_run
from coda.study import evidence_sha256, validate_study_packet
from coda.web.runtime import CodaWebService, _ADAPTER_FACTORIES


def build_service(root, dataset, artifacts, role_models, initial_ids):
    def config(role):
        # Retain provider/key/timeout configuration, explicitly bind the model
        # rather than allowing an environment default to change the condition.
        return replace(LLMModelConfig.from_env(default_provider='rightapi', default_model=role_models[role],
            default_max_output_tokens=6000, default_retry_timeouts_forever=True),
            model=role_models[role], max_output_tokens=6000, temperature=0.0)
    configs = {role: config(role) for role in role_models}
    backends = {role: load_chat_backend(value) for role, value in configs.items()}
    class FrozenAdapter:
        def load_dataset_metadata(self): return _ADAPTER_FACTORIES[dataset]().load_dataset_metadata()
        def iter_artifacts(self): yield from artifacts
    def orchestrator_factory():
        return CODAOrchestrator(
            context_agent=ContextLLMAgent(model_config=configs['context'], backend=backends['context']),
            coder_agents=[('coder-a', build_open_coder(model_config=configs['coder_a'], backend=backends['coder_a'])),
                          ('coder-b', build_open_coder(model_config=configs['coder_b'], backend=backends['coder_b']))],
            comparison_agent=ComparisonLLMAgent(model_config=configs['comparison'], backend=backends['comparison']),
            validation_agent=ValidationLLMAgent(model_config=configs['validation'], backend=backends['validation']),
            human_review_agent=lambda _: (_ for _ in ()).throw(RuntimeError('Automatic only')),
            failure_policy='route_to_r6')
    def bootstrap_factory(orchestrator):
        return EvidenceFirstBootstrap(model_config=configs['initial_assignment'], backend=backends['initial_assignment'],
            context_agent=orchestrator.prepare_context,
            initial_coder_agents=[('initial-coder-a', build_initial_open_coder(model_config=configs['coder_a'], backend=backends['coder_a'])),
                                  ('initial-coder-b', build_initial_open_coder(model_config=configs['coder_b'], backend=backends['coder_b']))],
            induction_agent=InductionLLMAgent(model_config=configs['induction'], backend=backends['induction']),
            validation_agent=ValidationLLMAgent(model_config=configs['validation'], backend=backends['validation']),
            config=BootstrapConfig(batch_size=10, fixed_artifact_ids=tuple(initial_ids)))
    return CodaWebService(runs_root=root, adapter_factories={dataset: FrozenAdapter},
                         orchestrator_factory=orchestrator_factory, bootstrap_factory=bootstrap_factory)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('protocol', type=Path)
    parser.add_argument('--packet', type=Path, action='append', required=True)
    parser.add_argument('--runs-root', type=Path, default=Path('runs/sensitivity'))
    parser.add_argument('--execute', action='store_true')
    args = parser.parse_args()
    protocol = json.loads(args.protocol.read_text())
    unsigned = {key: value for key, value in protocol.items() if key != 'protocol_sha256'}
    if hashlib.sha256(json.dumps(unsigned, sort_keys=True).encode()).hexdigest() != protocol.get('protocol_sha256'):
        parser.error('Protocol hash mismatch.')
    packets = {}
    for path in args.packet:
        packet = json.loads(path.read_text())
        validate_study_packet(packet, 'formal')
        if packet['dataset_name'] in packets:
            parser.error('Duplicate dataset packet.')
        packets[packet['dataset_name']] = packet
    if set(packets) != set(protocol['datasets']):
        parser.error('Supply exactly the three frozen dataset packets.')
    for dataset, packet in packets.items():
        if packet['study_materials'] != protocol['datasets'][dataset]['source_study_materials']:
            parser.error('Sensitivity protocol and input packet study allocation differ.')
    run_index_path = args.runs_root / 'sensitivity_run_index.json'
    index = json.loads(run_index_path.read_text()) if run_index_path.exists() else {'protocol_sha256': protocol['protocol_sha256'], 'runs': {}}
    if index['protocol_sha256'] != protocol['protocol_sha256']: parser.error('Runs root belongs to a different frozen protocol.')
    for condition in protocol['runs']:
        dataset = condition['dataset_name']
        source = {item['artifact_id']: item for item in packets[dataset]['artifacts']}
        artifacts = []
        for key in condition['artifact_ids']:
            item = source[key]
            if evidence_sha256(item) != protocol['datasets'][dataset]['evidence_sha256'][key]:
                parser.error(f'Frozen evidence mismatch: {dataset}/{key}')
            refs = [SourceRef(**{**ref, 'locator': TextLocator(**ref['locator']) if ref.get('locator') else None}) for ref in item.get('source_refs', [])]
            artifacts.append(ArtifactRecord(key, item['content'], item.get('raw_fields', {}), source_refs=refs))
        key = f"{dataset}:{condition['condition']}"
        if not args.execute:
            print(json.dumps({'condition': key, 'cases': len(artifacts), 'initial': 10, 'models': condition['role_models']}))
            continue
        service = build_service(args.runs_root, dataset, artifacts, condition['role_models'], condition['initialization_artifact_ids'])
        if key not in index['runs']:
            created = service.create_run(dataset_name=dataset, review_mode='automatic')
            run_id = created['run_id']
            state = service._load_run_state(run_id)
            state.metadata['sensitivity_protocol'] = {**condition,
                'protocol_sha256': protocol['protocol_sha256'],
                'evaluator_models': protocol['evaluator_models']}
            # FrozenAdapter already yields the chosen order; no artifact_limit sorting.
            save_run_state_checkpoint(state, service._paths_for(run_id).checkpoint_path)
            manifest_path = service._paths_for(run_id).run_manifest_path
            manifest = json.loads(manifest_path.read_text())
            manifest['models'] = condition['role_models']
            manifest['protocol']['sensitivity'] = state.metadata['sensitivity_protocol']
            manifest_path.write_text(json.dumps(manifest, indent=2)+'\n')
            index['runs'][key] = run_id
            run_index_path.parent.mkdir(parents=True, exist_ok=True)
            temporary = run_index_path.with_suffix('.tmp')
            temporary.write_text(json.dumps(index, indent=2)+'\n')
            temporary.replace(run_index_path)
        run_id = index['runs'][key]
        state = service._load_run_state(run_id)
        verify_sensitivity_run(protocol, state, condition['role_models'])
        if service._bootstrap_is_pending(state):
            service.initialize_run(run_id)
            state = service._load_run_state(run_id)
        if state.status not in {'completed', 'stabilized', 'completed_with_unresolved'}:
            result = service.process_automatic(run_id)
            print(json.dumps({'condition': key, 'run_id': run_id, 'status': result['run']['status']}))
        state = service._load_run_state(run_id)
        if state.status in {'completed', 'stabilized', 'completed_with_unresolved'}:
            from coda.evaluation import export_rq1_materials, _write_json
            packet = export_rq1_materials(service._paths_for(run_id).run_dir,
                service._adapter_for(dataset))
            packet['study_manifest'] = packets[dataset]['study_manifest']
            packet['study_materials'] = packets[dataset]['study_materials']
            validate_study_packet(packet, 'formal')
            packet['study_materials_verified'] = True
            _write_json(service._paths_for(run_id).run_dir / 'rq1_materials.json', packet)


if __name__ == '__main__': main()
