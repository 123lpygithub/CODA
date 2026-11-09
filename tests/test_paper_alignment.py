"""Regression checks for the paper's decision and measurement boundaries."""
from __future__ import annotations

import json
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path

from coda.agents.base import AgentPromptSpec, BaseLLMAgent
from coda.completion import completion_issues, decision_fingerprint
from coda.contracts import HumanReviewOutput, ValidationOutput, ValidationSignal
from coda.evaluation import _iter_model_metadata, _sum_model_usage, EvaluationError
from coda.evaluator import calibrate_evaluators, CalibrationConfig
from coda.llm import LLMModelConfig, LLMResponse
from coda.rq1_aggregation import aggregate_paper_rq1
from coda.study import calibration_assignment_targets, scoring_assignment_targets, verify_formal_run_matrix, StudyManifestError
from coda.web.runtime import CodaWebService, WebWorkflowError
from adapters.static_analysis import StaticAnalysisNondeterminismAdapter
from test_web_runtime import _build_test_orchestrator, _build_test_bootstrap, _build_existing_code_bootstrap


class PaperAlignmentTests(unittest.TestCase):
    def _service(self, root, orchestrator):
        service = CodaWebService(
            runs_root=Path(root),
            adapter_factories={'static_analysis_nondeterminism': StaticAnalysisNondeterminismAdapter},
            orchestrator_factory=lambda: orchestrator, bootstrap_factory=_build_test_bootstrap,
        )
        summary = service.create_run(dataset_name='static_analysis_nondeterminism',
                                     artifact_limit=1, review_mode='full')
        run_id = summary['run_id']
        service.initialize_run(run_id)
        service.submit_stage_review(run_id, 'initial', decision='accept', rationale='Reviewed.')
        return service, run_id

    def test_revised_assignment_is_validated_before_commit_and_failure_is_atomic(self):
        orchestrator = _build_test_orchestrator([])
        with tempfile.TemporaryDirectory() as root:
            service, run_id = self._service(root, orchestrator)
            service.prepare_review(run_id)
            prepared = service._prepared_reviews[run_id]
            state = service._load_run_state(run_id)
            before_version = state.codebook.version
            before_records = len(state.history.coding_records)
            from coda.state import CodeState, CodebookChangeState
            code = CodeState(code_id='revised', name='Revised concept', definition='A new supported boundary.')
            inputs = []
            def validate(agent_input):
                inputs.append(agent_input)
                return ValidationOutput(artifact_id=prepared.artifact_id, review_criteria=['R2'],
                    signals=[ValidationSignal(signal='unsupported_inference', summary='Missing support.')])
            orchestrator._validation_agent = validate
            with self.assertRaisesRegex(ValueError, 'remains pending'):
                orchestrator.submit_prepared_review(state, prepared_review=prepared,
                    human_review_output=HumanReviewOutput(
                        artifact_id=prepared.artifact_id, decision='revise', final_codes=[code],
                        codebook_changes=[CodebookChangeState(
                            change_id='add-revised', action='add', round_index=0,
                            summary='Add supported concept.', rationale='Source supports the concept.', resulting_code_ids=['revised'])],
                        rationale='Revised interpretation.', evidence_summary=['Source excerpt'],
                        confirmed_evidence=prepared.context_packet.evidence_items))
            self.assertEqual(state.codebook.version, before_version)
            self.assertEqual(len(state.history.coding_records), before_records)
            self.assertIsNone(state.codebook.get_code('revised'))
            self.assertEqual(inputs[0].codebook.get_code('revised').definition, code.definition)
            self.assertEqual(inputs[0].comparison_output.recommended_codes[0].code_name, code.name)

    def test_reject_reopens_case_then_prespecified_limit_marks_unresolved(self):
        with tempfile.TemporaryDirectory() as root:
            service, run_id = self._service(root, _build_test_orchestrator([]))
            state = service._load_run_state(run_id)
            artifact_id = service.current_artifact(run_id)['artifact']['artifact_id']
            for attempt in range(2):
                service.prepare_review(run_id)
                service.submit_review(run_id, human_review_output=HumanReviewOutput(
                    artifact_id=artifact_id, decision='reject', rationale='Reconsider the interpretation.'))
                if attempt == 0:
                    self.assertNotIn(artifact_id, state.history.reviewed_artifact_ids())
                    service.next_artifact(run_id)
            self.assertEqual(state.history.latest_record_for_artifact(artifact_id).decision, 'mark_uncertain')
            self.assertTrue(state.history.open_unresolved_cases())
            self.assertTrue(state.history.latest_record_for_artifact(artifact_id).metadata['work_limit_exhausted'])

    def test_completion_gate_checks_all_context_scopes_and_stale_audits(self):
        payload = {'codebook': {'version': 1}, 'coding_batches': [{'artifact_ids': ['a']}],
                   'metadata': {}, 'history': {'coding_records': [{'artifact_id': 'a', 'decision': 'accept'}]}}
        history = payload['history']
        payload['metadata']['final_validation_audits'] = {'audit': {
            'status': 'completed', 'decision_fingerprint': decision_fingerprint(payload['codebook'], history['coding_records'])}}
        self.assertEqual(completion_issues(payload), [])
        history['context_requests'] = [{'scope': 'artifact', 'status': 'pending'}]
        self.assertTrue(any('context' in issue for issue in completion_issues(payload)))
        history['context_requests'] = []
        history['coding_records'][0]['decision'] = 'reject'
        issues = completion_issues(payload)
        self.assertTrue(any('Rejected' in issue for issue in issues))
        self.assertTrue(any('validation' in issue for issue in issues))

    def test_physical_calls_deduplicate_aliases_and_keep_both_format_responses(self):
        class Backend:
            def __init__(self): self.count = 0
            def generate(self, **kwargs):
                self.count += 1
                return LLMResponse(model='test', text='invalid' if self.count == 1 else '{"ok": true}',
                    usage={'prompt_tokens': 10, 'completion_tokens': 2, 'total_tokens': 12},
                    estimated_cost_usd=.1)
        agent = BaseLLMAgent(prompt_spec=AgentPromptSpec('test', 'System', '{input}'),
                             model_config=LLMModelConfig(model='test'), backend=Backend())
        metadata = agent.invoke_validated_json_object(lambda payload, response: agent.execution_metadata(response), input='Evidence')
        trace = {'model_metadata': metadata}
        usage = _sum_model_usage(_iter_model_metadata([trace, {'evidence_packet': trace}, trace]))
        self.assertEqual(usage['logical_calls'], 2)
        self.assertEqual(usage['input_tokens'], 20)
        self.assertEqual(usage['format_retry_count'], 1)
        self.assertAlmostEqual(usage['estimated_cost_usd'], .2)
        self.assertEqual(metadata['model_calls'][0]['messages'][1]['role'], 'user')
        self.assertEqual(metadata['model_calls'][0]['response_text'], 'invalid')

    def test_common_assessable_support_and_equal_run_weights(self):
        rows = []
        for run_id in ('one', 'two'):
            for evaluator in ('a', 'b', 'c'):
                for artifact, score in [('x', 2), ('y', 0)]:
                    row = dict(run_id=run_id, evaluator_id=evaluator, dimension='evidence_support',
                               artifact_id=artifact, code_id='c', score=score, dataset_name='d', configuration='automatic')
                    if artifact == 'x' and evaluator == 'c':
                        row.update(status='unassessable', score=None)
                    rows.append(row)
                for dimension in ('clarity', 'category_boundaries', 'meaningful_coverage'):
                    rows.append(dict(run_id=run_id, evaluator_id=evaluator, dimension=dimension,
                                     score=3, dataset_name='d', configuration='automatic'))
        result = aggregate_paper_rq1(rows)
        self.assertEqual(result['by_run']['one']['evidence_support']['fully_supported_rate'], 0)
        self.assertEqual(result['by_run']['one']['evidence_support']['unassessable_rate'], .5)
        self.assertEqual(result['by_dataset_configuration']['d:automatic']['codebook']['clarity'], 3)
        rows.pop()
        incomplete = aggregate_paper_rq1(rows)
        self.assertIsNone(incomplete['by_dataset_configuration']['d:automatic']['codebook']['meaningful_coverage'])

    def test_calibration_sampling_is_case_local_and_leaves_full_record_intact(self):
        packet = {'run_id': 'r', 'artifacts': [{'artifact_id': 'a', 'coding_record': {'final_code_ids': ['c1', 'c2']}},
                                              {'artifact_id': 'b', 'coding_record': {'final_code_ids': []}}]}
        target = calibration_assignment_targets(packet)
        self.assertEqual(set(target), {'a'})
        self.assertEqual(target, calibration_assignment_targets({**packet, 'artifacts': list(reversed(packet['artifacts']))}))
        self.assertEqual(len(packet['artifacts'][0]['coding_record']['final_code_ids']), 2)

    def test_three_evaluators_selected_by_macro_agreement_and_cost(self):
        rows = []
        for evaluator in ('h1', 'h2', 'm1', 'm2', 'm3', 'm4', 'm5'):
            for index in range(6):
                for dimension in ('clarity', 'category_boundaries', 'meaningful_coverage', 'evidence_support'):
                    row = dict(run_id=f'r{index}', evaluator_id=evaluator,
                               evaluator_kind='human' if evaluator.startswith('h') else 'llm',
                               candidate_model=evaluator if evaluator.startswith('m') else None,
                               phase='pilot', dimension=dimension,
                               unit='assignment' if dimension == 'evidence_support' else 'codebook',
                               score=index % 3 if dimension == 'evidence_support' else index % 5 + 1,
                               rationale='Independent rubric rating.')
                    if dimension == 'evidence_support': row.update(artifact_id='a', code_id='c')
                    if evaluator.startswith('m'):
                        row['evaluator_metadata'] = {'model_calls': [{'call_id': evaluator, 'estimated_cost_usd': int(evaluator[1:])}]}
                    rows.append(row)
        result = calibrate_evaluators(rows, candidate_models=['m1', 'm2', 'm3', 'm4', 'm5'],
                                      human_evaluator_ids=['h1', 'h2'], config=CalibrationConfig(bootstrap_replicates=100))
        self.assertEqual(result['selected_candidate_models'], ['m1', 'm2', 'm3'])
        self.assertFalse(result['selection_frozen'])  # Unbound diagnostic scores cannot freeze a study.
        partial = calibrate_evaluators([row for row in rows if row['evaluator_id'] in {'h1','h2','m1'}],
                                       candidate_models=['m1'], human_evaluator_ids=['h1','h2'],
                                       config=CalibrationConfig(bootstrap_replicates=100))
        self.assertEqual(partial['selected_candidate_models'], [])
        self.assertEqual(partial['selection_status'], 'independent_human_evaluation_required')

    def test_unusable_second_response_has_exactly_one_repair_and_stable_call_ids(self):
        from coda.agents.base import AgentExecutionError
        class Backend:
            def generate(self, **kwargs): return LLMResponse(model='test', text='{}')
        agent = BaseLLMAgent(prompt_spec=AgentPromptSpec('test', 'system', '{input}'),
                             model_config=LLMModelConfig(model='test'), backend=Backend())
        def parse(payload, response): return payload['missing']
        with self.assertRaisesRegex(AgentExecutionError, 'after one format repair'):
            agent.invoke_validated_json_object(parse, input='source')
        self.assertEqual(len(agent.execution_log), 2)
        self.assertEqual(len({row['call_id'] for row in agent.execution_log}), 2)
        self.assertEqual(agent.execution_log[1]['format_retry_count'], 1)

    def test_stage_revision_failure_is_atomic_persistent_and_bounded(self):
        orchestrator = _build_test_orchestrator([])
        with tempfile.TemporaryDirectory() as root:
            service = CodaWebService(runs_root=Path(root),
                adapter_factories={'static_analysis_nondeterminism': StaticAnalysisNondeterminismAdapter},
                orchestrator_factory=lambda: orchestrator, bootstrap_factory=_build_existing_code_bootstrap)
            run_id = service.create_run(dataset_name='static_analysis_nondeterminism', artifact_limit=2, review_mode='full')['run_id']
            service.initialize_run(run_id)
            state = service._load_run_state(run_id)
            version = state.codebook.version
            revised = [replace(code, definition=code.definition + ' Clarified candidate.') for code in state.codebook.codes]
            received = []
            def validate(value):
                received.append(value)
                return ValidationOutput(artifact_id=value.artifact.artifact_id,
                    signals=[ValidationSignal(signal='unsupported_inference', summary='Not supported.')], review_criteria=['R2'])
            orchestrator._validation_agent = validate
            for index in range(2):
                with self.assertRaisesRegex(WebWorkflowError, 'remains pending'):
                    service.submit_stage_review(run_id, 'initial', decision='revise',
                        rationale='Check revised scope.', revised_codes=revised)
                self.assertEqual(state.codebook.version, version)
                checkpoint = json.loads(service._paths_for(run_id).checkpoint_path.read_text())
                self.assertEqual(len(checkpoint['metadata']['stage_human_revision_failures']['initial']), index + 1)
            self.assertEqual(state.status, 'resource_limited')
            self.assertEqual(received[0].codebook.codes[0].definition, revised[0].definition)

    def test_final_gate_blocks_artifact_context_for_all_terminal_decisions(self):
        from coda.state import ContextRequestState
        with tempfile.TemporaryDirectory() as root:
            service, run_id = self._service(root, _build_test_orchestrator([]))
            service.prepare_review(run_id)
            artifact_id = service._prepared_reviews[run_id].artifact_id
            service.submit_review(run_id, human_review_output=HumanReviewOutput(
                artifact_id=artifact_id, decision='mark_uncertain', rationale='Explicit unresolved outcome.'))
            service.next_artifact(run_id)
            state = service._load_run_state(run_id)
            self.assertEqual(state.status, 'awaiting_final_review')
            state.history.append_context_request(ContextRequestState(request_id='pending',
                scope='artifact', artifact_id=artifact_id, reason='Missing source', requested_items=['Source'],
                created_at_codebook_version=state.codebook.version))
            for decision in ('accept', 'mark_unresolved'):
                with self.assertRaisesRegex(WebWorkflowError, 'context'):
                    service.submit_stage_review(run_id, 'final', decision=decision, rationale='Cannot skip pending work.')
            self.assertFalse(service._paths_for(run_id).final_codebook_path.exists())

    def test_legacy_audit_is_rechecked_instead_of_trusted(self):
        calls = []
        with tempfile.TemporaryDirectory() as root:
            service, run_id = self._service(root, _build_test_orchestrator(calls))
            service.prepare_review(run_id)
            artifact_id = service._prepared_reviews[run_id].artifact_id
            service.submit_review(run_id, human_review_output=HumanReviewOutput(
                artifact_id=artifact_id, decision='mark_uncertain', rationale='Unresolved.'))
            service.next_artifact(run_id)
            state = service._load_run_state(run_id)
            for audit in state.metadata['final_validation_audits'].values():
                audit.pop('decision_fingerprint')
            count = len(calls)
            result = service._run_final_validation(state, state.history.stabilization_checks[-1])
            self.assertGreater(len(calls), count)
            self.assertTrue(result['decision_fingerprint'])
            self.assertTrue(state.metadata['legacy_final_validation_audits'])

    def test_frozen_sampling_rejects_changed_targets_and_formal_matrix_checks_repeats(self):
        packet = {'run_id': 'r', 'artifacts': [{'artifact_id': 'a', 'coding_record': {'final_code_ids': ['c1', 'c2']}}]}
        targets = calibration_assignment_targets(packet)
        packet['calibration_sampling'] = {'seed': 20260907, 'assignment_targets': targets}
        self.assertEqual(scoring_assignment_targets(packet, 'pilot'), {key: [value] for key, value in targets.items()})
        packet['calibration_sampling']['assignment_targets'] = {'a': 'foreign'}
        with self.assertRaises(StudyManifestError): scoring_assignment_targets(packet, 'pilot')
        packets = {f'{dataset}-{setting}-{repeat}': {'dataset_name': dataset, 'review_policy': {'setting': setting}}
                   for dataset in ('d1','d2','d3') for setting in ('automatic','selective','full') for repeat in range(2)}
        verify_formal_run_matrix(packets)
        packets.pop(next(iter(packets)))
        with self.assertRaises(StudyManifestError): verify_formal_run_matrix(packets)

    def test_rq1_weights_runs_equally_despite_different_assignment_counts(self):
        rows = []
        packets = {}
        for run_id, count, score in [('small', 1, 2), ('large', 9, 0)]:
            packets[run_id] = {'dataset_name':'d', 'review_policy':{'setting':'automatic'},
                'artifacts':[{'artifact_id':str(index), 'coding_record':{'final_code_ids':['c'], 'decision':'accept'}} for index in range(count)]}
            for evaluator in ('a','b','c'):
                for index in range(count):
                    rows.append(dict(run_id=run_id, evaluator_id=evaluator, dimension='evidence_support',
                                     artifact_id=str(index), code_id='c', score=score))
                for dimension in ('clarity','category_boundaries','meaningful_coverage'):
                    rows.append(dict(run_id=run_id, evaluator_id=evaluator, dimension=dimension, score=3))
        result = aggregate_paper_rq1(rows, packets=packets)
        self.assertEqual(result['by_dataset_configuration']['d:automatic']['evidence_support_proportions']['2'], .5)
        human_rows = [{**row, 'evaluator_kind':'human'} for row in rows if row['evaluator_id'] != 'c']
        from coda.evaluation import summarize_rq1_scores
        for row in human_rows:
            row['unit'] = 'assignment' if row['dimension'] == 'evidence_support' else 'codebook'
        human = summarize_rq1_scores(human_rows, human_fallback=True, agreement_replicates=100)
        self.assertTrue(human['paper_aggregation']['available'])
        self.assertEqual(human['paper_aggregation']['assessment_mode'], 'independent_humans')

    def test_sensitivity_protocol_has_nine_conditions_and_identical_frozen_cases(self):
        from coda.sensitivity import build_sensitivity_protocol, ROLES
        packets = {dataset: {'dataset_name':dataset, 'formal_evaluation_ready':True,
            'study_materials':{'phase':'formal'}, 'artifacts':[
                {'artifact_id':str(index), 'content':'original evidence', 'raw_fields':{}, 'source_refs':[]}
                for index in range(55)]} for dataset in ('d1','d2','d3')}
        protocol = build_sensitivity_protocol(packets, reference_models={role:'ref' for role in ROLES},
                                               evaluator_models=['e1','e2','e3'])
        self.assertEqual(len(protocol['runs']),9)
        for dataset in packets:
            conditions = [row for row in protocol['runs'] if row['dataset_name'] == dataset]
            self.assertEqual(len(conditions[0]['artifact_ids']),50)
            self.assertTrue(all(row['artifact_ids'] == conditions[0]['artifact_ids'] for row in conditions))
            self.assertEqual(conditions[0]['initialization_artifact_ids'], conditions[0]['artifact_ids'][:10])

    def test_sensitivity_does_not_treat_ambiguous_locations_as_complete(self):
        from coda.sensitivity import build_sensitivity_protocol, ROLES
        packets={dataset:{'dataset_name':dataset,'formal_evaluation_ready':True,
                 'study_materials':{'phase':'formal'},'artifacts':[
                     {'artifact_id':str(i),'content':'source','source_refs':[],
                      'raw_fields':{'source_context_status':'available' if i<49 else 'ambiguous'}}
                     for i in range(55)]} for dataset in ('d1','d2','d3')}
        with self.assertRaisesRegex(StudyManifestError,'fewer than 50 complete cases'):
            build_sensitivity_protocol(packets,reference_models={role:'ref' for role in ROLES},
                                       evaluator_models=['e1','e2','e3'])

    def test_impact_screening_repairs_unknown_case_without_approving_assignments(self):
        from coda.agents.arbitration_agent import ComparisonLLMAgent
        from coda.state import CodebookState, CodebookChangeState
        class Backend:
            def __init__(self): self.count = 0
            def generate(self, **kwargs):
                self.count += 1
                return LLMResponse(model='test', text=json.dumps({'affected_cases':[
                    {'artifact_id':'foreign' if self.count == 1 else 'old', 'reason':'Related phenomenon.'}], 'unchecked_cases':[]}))
        backend=Backend()
        agent=ComparisonLLMAgent(model_config=LLMModelConfig(model='test'), backend=backend)
        output=agent.screen_historical_impacts(change=CodebookChangeState(
            change_id='added', action='add', round_index=1, summary='New category'),
            codebook=CodebookState.empty('d'), cases={'old':{'summary':'Earlier wording'}})
        self.assertEqual(output['affected_cases'][0]['artifact_id'],'old')
        self.assertEqual(backend.count,2)
        self.assertEqual(len(output['model_metadata']['model_calls']),2)

    def test_context_summary_length_is_repaired_with_original_evidence_preserved(self):
        from coda.agents.context_agent import ContextLLMAgent
        from coda.contracts import ContextAgentInput
        from adapters.base import ArtifactRecord
        from coda.state import ResearchQuestionState
        class Backend:
            def __init__(self): self.count=0
            def generate(self, **kwargs):
                self.count += 1
                return LLMResponse(model='test', text=json.dumps({
                    'context_brief': 'word '*151 if self.count == 1 else 'A supported observation.',
                    'evidence_items':[{'field_name':'text', 'excerpt':'source excerpt',
                        'rationale':'Reported behavior', 'claim_type':'reported', 'revision':'r1'}],
                    'missing_context_warnings':[], 'distracting_information':[]}))
        backend=Backend()
        agent=ContextLLMAgent(model_config=LLMModelConfig(model='test'), backend=backend)
        packet=agent(ContextAgentInput(artifact=ArtifactRecord('a','source excerpt',{'text':'source excerpt', 'revision':'r1'}),
            research_question=ResearchQuestionState(dataset_name='d', question_text='What phenomena?', analysis_scope='all', use_case='study', artifact_unit='case')))
        self.assertLessEqual(len(packet.context_brief.split()),150)
        self.assertEqual(packet.evidence_items[0].claim_type,'reported')
        self.assertEqual(packet.evidence_items[0].revision,'r1')
        self.assertEqual(backend.count,2)


    def _three_dataset_materials(self, count=12):
        from adapters.base import ArtifactRecord
        from coda.study import build_study_manifest, select_study_artifacts, study_binding
        from dataclasses import asdict
        datasets = ('llm_code_error_semantic', 'ml_satd_23_shades', 'personal_data_protection_github')
        cases = {}
        for dataset in datasets:
            field = {'llm_code_error_semantic':'task_id', 'ml_satd_23_shades':'repo_name',
                     'personal_data_protection_github':'project'}[dataset]
            cases[dataset] = [ArtifactRecord(f'{dataset}-{i}', f'Original source {i}',
                {field: i if field == 'task_id' else f'owner/repo-{i}'}) for i in range(count)]
        manifest = build_study_manifest(cases, study_id='complete-pilot',
                                        pilot_group_counts={dataset:6 for dataset in datasets})
        def packet(dataset, phase, setting='automatic', replicate=1):
            return {'run_id':f'{dataset}:{phase}:{setting}:{replicate}', 'dataset_name':dataset,
                'review_policy':{'setting':setting}, 'study_manifest':manifest,
                'study_materials':study_binding(manifest,dataset,phase), 'formal_evaluation_ready':True,
                'codebook':{'codes':[{'code_id':'c', 'name':'Concept', 'definition':'Supported distinction.'}]},
                'artifacts':[{**asdict(item), 'coding_record':{'final_code_ids':['c']}}
                    for item in select_study_artifacts(manifest,dataset,cases[dataset],phase)]}
        return manifest, datasets, packet

    def test_full_pilot_selection_is_frozen_and_tampering_is_rejected(self):
        from coda.evaluator import validate_frozen_selection
        manifest, datasets, packet = self._three_dataset_materials()
        packets, rows = {}, []
        for dataset in datasets:
            for setting in ('automatic','selective','full'):
                for replicate in (1,2):
                    value = packet(dataset,'pilot',setting,replicate)
                    packets[value['run_id']] = value
                    for evaluator in ('h1','h2','m1','m2','m3','m4','m5'):
                        base = {'run_id':value['run_id'], 'evaluator_id':evaluator, 'phase':'pilot',
                            'evaluator_kind':'human' if evaluator.startswith('h') else 'llm',
                            'candidate_model':evaluator if evaluator.startswith('m') else None,
                            'rationale':'Independent test rating.'}
                        if evaluator.startswith('m'):
                            base['evaluator_metadata'] = {'model_calls':[{'call_id':f"{value['run_id']}:{evaluator}",
                                'estimated_cost_usd':int(evaluator[1:])}]}
                        for dimension in ('clarity','category_boundaries','meaningful_coverage'):
                            rows.append({**base, 'dimension':dimension, 'unit':'codebook', 'score':replicate+2})
                        for index, artifact in enumerate(value['artifacts']):
                            rows.append({**base, 'dimension':'evidence_support','unit':'assignment',
                                'artifact_id':artifact['artifact_id'], 'code_id':'c', 'score':index%3})
        result = calibrate_evaluators(rows, candidate_models=['m1','m2','m3','m4','m5'],
            human_evaluator_ids=['h1','h2'], materials_by_run=packets,
            config=CalibrationConfig(bootstrap_replicates=100))
        self.assertTrue(result['selection_frozen'])
        self.assertEqual(result['selected_candidate_models'],['m1','m2','m3'])
        self.assertEqual(len(result['by_dataset']),3)
        validate_frozen_selection(result, packet=packet(datasets[0],'formal'))
        result['selected_candidate_models'][0] = 'foreign'
        with self.assertRaisesRegex(EvaluationError,'checksum'):
            validate_frozen_selection(result)

    def test_participant_allocation_is_balanced_eligible_and_preserves_identity(self):
        from coda.execution import build_execution_plan
        manifest, datasets, _ = self._three_dataset_materials()
        roster = [{'participant_id':f'p{i}', 'experience_years':i+1,
                   'eligible_datasets':list(datasets), 'eligibility_confirmed':True} for i in range(6)]
        plan = build_execution_plan(manifest, roster)
        self.assertEqual(len(plan['runs']),18)
        reviewed = [row for row in plan['runs'] if row['participant_id']]
        self.assertEqual(sum(row['task_order']==1 and row['review_mode']=='selective' for row in reviewed),3)
        self.assertEqual(sum(row['task_order']==1 and row['review_mode']=='full' for row in reviewed),3)
        for person in roster:
            tasks = [row for row in reviewed if row['participant_id']==person['participant_id']]
            self.assertEqual({row['review_mode'] for row in tasks},{'selective','full'})
            self.assertEqual(len({row['dataset_name'] for row in tasks}),2)
        with self.assertRaisesRegex(StudyManifestError,'separate'):
            build_execution_plan(manifest,roster,excluded_participant_ids=['p1'])
        with tempfile.TemporaryDirectory() as root:
            service = CodaWebService(runs_root=Path(root), orchestrator_factory=lambda:_build_test_orchestrator([]),
                bootstrap_factory=_build_test_bootstrap)
            run_id = service.create_run(dataset_name='static_analysis_nondeterminism',artifact_limit=1,
                review_mode='full',participant_id='p1',replicate_index=2,comparison_block_id='pair-1')['run_id']
            service.initialize_run(run_id)
            service.submit_stage_review(run_id,'initial',decision='accept',rationale='Inspected.')
            service.prepare_review(run_id)
            state = service._load_run_state(run_id)
            artifact_id = service._prepared_reviews[run_id].artifact_id
            service.submit_review(run_id,human_review_output=HumanReviewOutput(
                artifact_id=artifact_id,decision='mark_uncertain',rationale='Not resolved.'))
            self.assertEqual(state.history.stage_reviews[0].reviewer_id,'p1')
            self.assertEqual(state.history.coding_records[-1].metadata['participant_id'],'p1')
            from coda.evaluation import summarize_rq2_metrics
            self.assertEqual(summarize_rq2_metrics(service._paths_for(run_id).run_dir)['study_execution']['replicate_index'],2)

    def test_blind_random_order_is_reproducible_and_model_identity_cannot_be_spoofed(self):
        from coda.agents.evaluator_agent import build_blinded_evaluator_packet, EvaluatorLLMAgent
        source = {'codebook':{'codes':[{'code_id':str(i)} for i in range(12)]},
                  'artifacts':[{'artifact_id':str(i),'content':'Evidence'} for i in range(12)]}
        first = build_blinded_evaluator_packet(source)
        second = build_blinded_evaluator_packet({**source,'artifacts':list(reversed(source['artifacts']))})
        self.assertEqual(first,second)
        self.assertNotEqual([item['artifact_id'] for item in first['artifacts']],sorted(str(i) for i in range(12)))
        agent = EvaluatorLLMAgent(model_config=LLMModelConfig(model='actual'),backend=None)
        with self.assertRaisesRegex(ValueError,'actual model'):
            agent(packet=source,run_id='r',evaluator_id='e',candidate_model='pretend')

    def test_automatic_new_category_preserves_inclusion_and_exclusion(self):
        orchestrator = _build_test_orchestrator([])
        original = orchestrator._comparison_agent
        def compare(value):
            output = original(value)
            return replace(output,recommended_codes=[replace(code,inclusion_criteria=['Required condition'],
                exclusion_criteria=['Different phenomenon']) for code in output.recommended_codes])
        orchestrator._comparison_agent = compare
        # Compatibility aliases share one Comparison role; replace its callable.
        orchestrator._arbitration_agent = compare
        with tempfile.TemporaryDirectory() as root:
            service = CodaWebService(runs_root=Path(root),orchestrator_factory=lambda:orchestrator,
                                    bootstrap_factory=_build_test_bootstrap)
            run_id = service.create_run(dataset_name='static_analysis_nondeterminism',artifact_limit=1,
                                        review_mode='automatic')['run_id']
            service.initialize_run(run_id)
            service.process_automatic(run_id)
            code = service._load_run_state(run_id).codebook.active_codes()[0]
            self.assertEqual(code.inclusion_criteria,['Required condition'])
            self.assertEqual(code.exclusion_criteria,['Different phenomenon'])

    def test_active_backend_rejects_source_drift_before_cached_final_audit(self):
        from adapters.base import ArtifactRecord
        from coda.state import StabilizationCheckState
        with tempfile.TemporaryDirectory() as root:
            service, run_id = self._service(root,_build_test_orchestrator([]))
            state = service._load_run_state(run_id)
            artifacts = list(service._adapter_for(state.dataset_metadata.dataset_name).iter_artifacts())
            class Changed:
                def iter_artifacts(self):
                    yield from [replace(item,content=item.content+' changed') for item in artifacts]
            service._adapter_factories[state.dataset_metadata.dataset_name] = Changed
            with self.assertRaisesRegex(WebWorkflowError,'Source evidence changed'):
                service._run_final_validation(state,None)

    def test_evaluator_cli_resumes_completed_chunks_without_rescoring(self):
        import importlib.util
        from types import SimpleNamespace
        from unittest.mock import patch
        spec = importlib.util.spec_from_file_location('paper_evaluator_cli',Path(__file__).parents[1]/'scripts/run_llm_evaluator.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        calls, failed = [], [False]
        class Agent:
            def __init__(self,**kwargs):
                self._prompt_spec = SimpleNamespace(system_prompt='fixed',user_prompt_template='fixed')
            def __call__(self,*,packet,run_id,evaluator_id,phase,candidate_model):
                scope = packet['evaluation_scope']
                calls.append(scope)
                if scope == 'assignments_only' and not failed[0]:
                    failed[0]=True
                    raise RuntimeError('Simulated connection loss')
                base = {'run_id':run_id,'evaluator_id':evaluator_id,'phase':phase,'candidate_model':candidate_model}
                if scope == 'codebook_only':
                    return [{**base,'dimension':dimension,'unit':'codebook','score':3} for dimension in (
                        'clarity','category_boundaries','meaningful_coverage')]
                return [{**base,'dimension':'evidence_support','unit':'assignment','score':2,
                    'artifact_id':key,'code_id':code} for key,codes in packet['scoring_assignment_targets'].items() for code in codes]
        with tempfile.TemporaryDirectory() as root:
            source, output = Path(root)/'packet.json',Path(root)/'scores.json'
            source.write_text(json.dumps({'run_id':'r','codebook':{'codes':[]},'artifacts':[
                {'artifact_id':'a','coding_record':{'final_code_ids':['x','y']}}]}))
            argv=['run_llm_evaluator.py',str(source),'--run-id','r','--evaluator-id','e',
                  '--model','actual','--phase','pilot','--exploratory','--output',str(output)]
            with patch.object(module,'EvaluatorLLMAgent',Agent),patch.object(module,'load_chat_backend',return_value=None),patch('sys.argv',argv):
                with self.assertRaisesRegex(RuntimeError,'connection loss'):
                    module.main()
                module.main()
                module.main()
            self.assertEqual(calls,['codebook_only','assignments_only','assignments_only'])
            self.assertEqual(len(json.loads(output.read_text())),4)

    def test_sensitivity_cli_dry_run_execute_and_resume_frozen_nine_conditions(self):
        import importlib.util
        from unittest.mock import patch
        from coda.sensitivity import build_sensitivity_protocol,ROLES
        from coda.bootstrap import BootstrapResult,BootstrapAssignment
        from coda.state import CodeState,CodebookState
        from coda.web.runtime import _ADAPTER_FACTORIES
        _, datasets, packet = self._three_dataset_materials(count=65)
        packets = {dataset:packet(dataset,'formal') for dataset in datasets}
        protocol = build_sensitivity_protocol(packets,reference_models={role:'reference' for role in ROLES},
                                               evaluator_models=['e1','e2','e3'])
        spec=importlib.util.spec_from_file_location('paper_sensitivity_cli',Path(__file__).parents[1]/'scripts/run_sensitivity_protocol.py')
        module=importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        calls=[]
        def build_service(root,dataset,artifacts,role_models,initial_ids):
            class Adapter:
                def load_dataset_metadata(self):return _ADAPTER_FACTORIES[dataset]().load_dataset_metadata()
                def iter_artifacts(self):yield from artifacts
            class Bootstrap:
                def run(self,state,source):
                    code=CodeState(code_id='analysis-logic',name='Analysis Logic',definition='A root cause in analysis logic.',
                                   representative_artifact_ids=[initial_ids[0]])
                    return BootstrapResult(codebook=CodebookState(dataset_name=dataset,version=1,codes=[code]),
                        artifact_ids=initial_ids,group_ids={item.artifact_id:item.artifact_id for item in source},
                        assignments=[BootstrapAssignment(key,['analysis-logic'],['Original evidence']) for key in initial_ids])
            return CodaWebService(runs_root=root,adapter_factories={dataset:Adapter},
                orchestrator_factory=lambda:_build_test_orchestrator(calls,relationship_to_codebook='reuse_existing_code'),
                bootstrap_factory=lambda _:Bootstrap())
        with tempfile.TemporaryDirectory() as root:
            root=Path(root)
            plan=root/'protocol.json'
            plan.write_text(json.dumps(protocol))
            argv=['run_sensitivity_protocol.py',str(plan),'--runs-root',str(root/'runs')]
            for dataset,source in packets.items():
                path=root/f'{dataset}.json'
                path.write_text(json.dumps(source))
                argv.extend(['--packet',str(path)])
            with patch('sys.argv',argv),patch.object(module,'build_service',side_effect=AssertionError('Dry run called agents')):
                module.main()
            self.assertFalse((root/'runs').exists())
            with patch('sys.argv',argv+['--execute']),patch.object(module,'build_service',side_effect=build_service):
                module.main()
                count=len(calls)
                module.main()
                self.assertEqual(len(calls),count)
            index=json.loads((root/'runs/sensitivity_run_index.json').read_text())
            self.assertEqual(len(index['runs']),9)
            from coda.study import validate_study_packet
            for run_id in index['runs'].values():
                frozen=json.loads((root/'runs'/run_id/'rq1_materials.json').read_text())
                self.assertEqual(len(frozen['artifacts']),50)
                self.assertTrue(frozen['formal_evaluation_ready'])
                validate_study_packet(frozen,'formal')

    def test_human_blind_worksheet_roundtrip_rejects_missing_and_duplicate_targets(self):
        import importlib.util
        from unittest.mock import patch
        from coda.study import StudyManifestError
        modules = []
        for name in ('export_evaluator_targets', 'import_evaluator_worksheet'):
            spec = importlib.util.spec_from_file_location(name, Path(__file__).parents[1]/'scripts'/f'{name}.py')
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            modules.append(module)
        exporter, importer = modules
        _, datasets, build_packet = self._three_dataset_materials()
        with tempfile.TemporaryDirectory() as root:
            root = Path(root)
            packet_path = root/'packet.json'
            packet = build_packet(datasets[0], 'pilot')
            packet_path.write_text(json.dumps(packet))
            presentation, output = root/'blind', root/'ratings.json'
            with patch('sys.argv', ['export', '--packet', str(packet_path), '--phase', 'pilot',
                                    '--evaluator-id', 'human-a', '--output-dir', str(presentation)]):
                exporter.main()
            blinded = json.loads((presentation/'output-001.json').read_text())
            self.assertNotIn('run_id', blinded)
            self.assertNotIn('review_policy', blinded)
            worksheet_path = presentation/'worksheet.json'
            rows = json.loads(worksheet_path.read_text())
            self.assertTrue(all(row['score'] is None for row in rows))
            for row in rows:
                row.update(score=2 if row['unit'] == 'assignment' else 3,
                           rationale='Independently checked against the supplied evidence.')
            argv = ['import', str(worksheet_path), '--private-index', str(presentation/'private_index.json'),
                    '--packet', str(packet_path), '--output', str(output)]
            for invalid in (rows[:-1], rows + [rows[-1]]):
                worksheet_path.write_text(json.dumps(invalid))
                with patch('sys.argv', argv), self.assertRaises(StudyManifestError):
                    importer.main()
                self.assertFalse(output.exists())
            worksheet_path.write_text(json.dumps(rows))
            with patch('sys.argv', argv):
                importer.main()
            ratings = json.loads(output.read_text())
            self.assertEqual(len(ratings), len(rows))
            self.assertTrue(all(row['run_id'] == packet['run_id'] for row in ratings))
            self.assertTrue(all(row['study_materials'] == packet['study_materials'] for row in ratings))
            with patch('sys.argv', argv), self.assertRaises(SystemExit):
                importer.main()  # Independent ratings must never be overwritten.

    def test_context_deferral_is_valid_but_empty_excerpts_and_invented_revisions_are_repaired(self):
        from adapters.base import ArtifactRecord
        from coda.agents.context_agent import ContextLLMAgent
        from coda.agents.base import AgentExecutionError
        from coda.contracts import ContextAgentInput
        from coda.state import ResearchQuestionState
        payload = {'context_brief': 'The source does not establish the execution environment.',
                   'evidence_items': [], 'missing_context_warnings': ['Execution log is unavailable.'],
                   'distracting_information': []}
        class Backend:
            def __init__(self): self.count = 0
            def generate(self, **kwargs):
                self.count += 1
                return LLMResponse(model='test', text=json.dumps(payload))
        backend = Backend()
        agent = ContextLLMAgent(model_config=LLMModelConfig(model='test'), backend=backend)
        value = ContextAgentInput(artifact=ArtifactRecord('a','source excerpt',{'text':'source excerpt'}),
            research_question=ResearchQuestionState(dataset_name='d', question_text='What phenomena?',
                analysis_scope='all', use_case='study', artifact_unit='case'))
        result = agent(value)
        self.assertEqual(result.evidence_items, [])
        self.assertEqual(backend.count, 1)  # A valid deferral is not a formatting failure.
        payload['missing_context_warnings'] = []
        payload['evidence_items'] = [{'field_name': 'text', 'excerpt': '', 'rationale': 'Empty'}]
        with self.assertRaises(AgentExecutionError): agent(value)
        self.assertEqual(backend.count, 3)
        payload['evidence_items'] = [{'field_name': 'text', 'excerpt': 'source excerpt',
                                     'rationale': 'Observed source', 'revision': 'invented-revision'}]
        with self.assertRaises(AgentExecutionError): agent(value)
        self.assertEqual(backend.count, 5)

    def test_frozen_agent_protocol_rejects_prompt_drift_but_allows_timeout_change(self):
        agent = BaseLLMAgent(prompt_spec=AgentPromptSpec('test', 'fixed role', '{input}'),
                             model_config=LLMModelConfig(model='test'), backend=None)
        with tempfile.TemporaryDirectory() as root:
            service, run_id = self._service(root, _build_test_orchestrator([]))
            state = service._load_run_state(run_id)
            service._bind_agent_protocol(state, 'regression', [('coder', agent)])
            agent = BaseLLMAgent(prompt_spec=agent._prompt_spec,
                model_config=replace(agent.model_config, timeout_seconds=30), backend=None)
            service._bind_agent_protocol(state, 'regression', [('coder', agent)])
            agent._prompt_spec = AgentPromptSpec('test', 'changed analytical role', '{input}')
            with self.assertRaisesRegex(WebWorkflowError, 'frozen protocol'):
                service._bind_agent_protocol(state, 'regression', [('coder', agent)])

    def test_cancelled_context_retains_request_and_creates_explicit_unresolved_record(self):
        with tempfile.TemporaryDirectory() as root:
            service, run_id = self._service(root, _build_test_orchestrator([]))
            service.prepare_review(run_id)
            artifact_id = service._prepared_reviews[run_id].artifact_id
            service.submit_review(run_id, human_review_output=HumanReviewOutput(
                artifact_id=artifact_id, decision='request_additional_context',
                rationale='Need the original execution log.', notes=['Supply the log.']))
            request = service.context_requests(run_id)['requests'][0]
            service.cancel_context_request(run_id, request['request_id'])
            state = service._load_run_state(run_id)
            record = state.history.latest_record_for_artifact(artifact_id)
            self.assertEqual(record.decision, 'mark_uncertain')
            self.assertEqual(record.final_code_ids, [])
            self.assertEqual(record.metadata['review_origin'], 'context_cancellation')
            self.assertTrue(state.history.open_unresolved_cases())
            self.assertEqual(state.history.context_requests[0].status, 'cancelled')
            self.assertTrue(any(row.decision == 'request_additional_context' for row in state.history.coding_records))


if __name__ == '__main__': unittest.main()
