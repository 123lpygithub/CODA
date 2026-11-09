"""Multi-case shared snapshot, reconciliation, review and restart regressions."""
from dataclasses import replace
import json
from pathlib import Path
import tempfile
import unittest

from coda.contracts import HumanReviewOutput, ComparisonOutput, ProvisionalCode
from coda.web.runtime import CodaWebService
from test_web_runtime import _build_test_orchestrator, _build_test_bootstrap


class MultiBatchTests(unittest.TestCase):
    def factory(self, calls, observations, fail=None):
        orchestrator = _build_test_orchestrator(calls)
        old = orchestrator._comparison_agent
        class Comparison:
            def __call__(self, value):
                observations.append(('compare',value.artifact.artifact_id,value.codebook.version,value.task))
                output = old(value)
                if value.task == 'batch_recheck' and value.codebook.active_codes():
                    code = value.codebook.active_codes()[0]
                    output = replace(output, recommended_codes=[replace(output.recommended_codes[0],
                        code_name=code.name,short_definition=code.definition,
                        relationship_to_codebook='reuse_existing_code',linked_code_ids=[code.code_id],
                        proposed_codebook_action='no_change')], possible_codebook_changes=[])
                return output
            def reconcile_batch(self, *, run_state, prepared):
                observations.append(('reconcile',run_state.codebook.version,len(prepared)))
                if fail is not None and fail[0]:
                    fail[0] = False
                    raise RuntimeError('Interrupted reconciliation')
                return {item.artifact_id:item.arbitration_output for item in prepared}
        orchestrator._comparison_agent = Comparison()
        original_validation = orchestrator._validation_agent
        def validate(value):
            observations.append(('validate', value.artifact.artifact_id,value.codebook.version))
            return original_validation(value)
        orchestrator._validation_agent = validate
        return orchestrator

    def service(self, root, calls, observations, fail=None):
        return CodaWebService(runs_root=Path(root), bootstrap_factory=_build_test_bootstrap,
            orchestrator_factory=lambda:self.factory(calls,observations,fail))

    def test_initial_comparison_barrier_rechecks_new_version_and_reuses_shared_addition(self):
        calls, observations = [], []
        with tempfile.TemporaryDirectory() as root:
            service = self.service(root,calls,observations)
            run_id = service.create_run(dataset_name='static_analysis_nondeterminism', artifact_limit=3,
                review_mode='automatic', iterative_batch_size=3)['run_id']
            service.initialize_run(run_id)
            state = service._load_run_state(run_id)
            self.assertEqual([len(batch.artifacts) for batch in state.coding_batches],[3])
            service.process_automatic(run_id,max_artifacts=1)
            first = [row for row in observations if row[0]=='compare']
            self.assertEqual(len(first),3)
            self.assertEqual({row[2] for row in first},{0})
            reconcile = next(index for index,row in enumerate(observations) if row[0]=='reconcile')
            validate = next(index for index,row in enumerate(observations) if row[0]=='validate')
            self.assertLess(reconcile,validate)
            self.assertEqual(len(state.codebook.active_codes()),1)
            # Reload with fresh service/agents: no initial Context/Coder or
            # reconciliation calls may repeat after a partially committed batch.
            service = self.service(root,calls,observations)
            service.process_automatic(run_id,max_artifacts=2)
            state = service._load_run_state(run_id)
            self.assertEqual(len(state.codebook.active_codes()),1)
            self.assertEqual(len(state.history.reviewed_artifact_ids()),3)
            self.assertEqual(sum(row[0]=='reconcile' for row in observations),1)
            self.assertEqual(sum(row.startswith('context:') for row in calls),3)
            self.assertTrue(any(row[0]=='compare' and row[3]=='batch_recheck' and row[2]==1 for row in observations))
            self.assertEqual(state.codebook.version,1)
            self.assertEqual(next(iter(state.metadata['iterative_batch_preparations'].values()))['status'],'completed')

    def test_interrupted_reconciliation_resumes_initial_calls_without_mutation(self):
        calls, observations, fail = [], [], [True]
        with tempfile.TemporaryDirectory() as root:
            service = self.service(root,calls,observations,fail)
            run_id = service.create_run(dataset_name='static_analysis_nondeterminism',artifact_limit=3,
                review_mode='automatic',iterative_batch_size=2)['run_id']
            service.initialize_run(run_id)
            with self.assertRaisesRegex(RuntimeError,'Interrupted reconciliation'):
                service.process_automatic(run_id,max_artifacts=1)
            self.assertEqual(service._load_run_state(run_id).codebook.version,0)
            self.assertEqual(service._load_run_state(run_id).history.coding_records,[])
            self.assertFalse(any(row[0]=='validate' for row in observations))
            service = self.service(root,calls,observations,fail)
            service.process_automatic(run_id,max_artifacts=1)
            self.assertEqual(sum(row.startswith('context:') for row in calls),2)
            self.assertEqual([len(item.artifacts) for item in service._load_run_state(run_id).coding_batches],[2,1])

    def test_full_review_packet_restores_without_model_repetition(self):
        calls, observations = [], []
        with tempfile.TemporaryDirectory() as root:
            service = self.service(root,calls,observations)
            run_id = service.create_run(dataset_name='static_analysis_nondeterminism',artifact_limit=2,
                review_mode='full',iterative_batch_size=2)['run_id']
            service.initialize_run(run_id)
            service.submit_stage_review(run_id,'initial',decision='accept',rationale='Initial scope reviewed.')
            packet = service.prepare_review(run_id)
            counts = (len(calls),len(observations))
            service = self.service(root,calls,observations)
            restored = service.review_packet(run_id)
            self.assertEqual(restored['artifact_id'],packet['artifact_id'])
            self.assertEqual((len(calls),len(observations)),counts)
            # Reject means reconsidering the case, not accepting its proposed
            # new category or allowing dependent cases to use it as existing.
            service.submit_review(run_id,human_review_output=HumanReviewOutput(
                artifact_id=packet['artifact_id'],decision='reject',rationale='Reconsider the category boundary.'))
            service.next_artifact(run_id)
            service.prepare_review(run_id)
            self.assertTrue(any(row[0]=='compare' and row[3]=='batch_recheck' for row in observations))
            self.assertEqual(service._load_run_state(run_id).codebook.version,0)

    def test_batch_membership_and_size_are_frozen_and_pending_batch_blocks_completion(self):
        from coda.completion import completion_issues
        from coda.web.api import CreateRunRequest
        from pydantic import ValidationError
        with self.assertRaises(ValidationError):
            CreateRunRequest(dataset_name='d',iterative_batch_size=0)
        issues = completion_issues({'history':{},'metadata':{'iterative_batch_preparations':{
            'b':{'status':'preparing'}}}},require_audit=False)
        self.assertTrue(any('batches' in issue for issue in issues))

    def test_llm_reconciliation_parses_local_evidence_and_repairs_incomplete_batch_once(self):
        from coda.agents.arbitration_agent import ComparisonLLMAgent
        from coda.llm import LLMModelConfig, LLMResponse
        from coda.agents.base import AgentExecutionError
        responses, messages = [], []
        class Backend:
            def generate(self, **kwargs):
                messages.append(kwargs['messages'])
                return LLMResponse(model='test',text=json.dumps(responses.pop(0)))
        def row(artifact_id):
            return {'artifact_id':artifact_id,'agreement_summary':'Supported common concept.',
                'disagreement_summary':'None.', 'recommended_codes':[{
                    'code_name':'Shared concept','short_definition':'A supported common definition.',
                    'supporting_evidence_refs':['E1'],'relationship_to_codebook':'new_code',
                    'linked_code_ids':[],'alternative_interpretation':'','uncertainty_note':'',
                    'proposed_codebook_action':'add','proposed_codebook_target_ids':[]}],
                'preserved_alternatives':[],'disagreements':[],
                'relevant_historical_artifact_ids':[],'possible_codebook_changes':[]}
        with tempfile.TemporaryDirectory() as root:
            service = self.service(root,[],[])
            run_id = service.create_run(dataset_name='static_analysis_nondeterminism',artifact_limit=2,
                                       review_mode='automatic')['run_id']
            service.initialize_run(run_id)
            state = service._load_run_state(run_id)
            # Gather separate initial proposals without Validation or routing.
            orchestrator = service._orchestrator_for(run_id)
            prepared = [orchestrator.prepare_one_artifact(state,artifact=batch.artifacts[0],
                batch=batch,defer_validation=True) for batch in state.coding_batches]
            rows = [row(item.artifact_id) for item in prepared]
            responses.extend([{'case_proposals':rows[:1]},{'case_proposals':rows}])
            agent = ComparisonLLMAgent(model_config=LLMModelConfig(model='test'),backend=Backend())
            outputs = agent.reconcile_batch(run_state=state,prepared=prepared)
            self.assertEqual(set(outputs),set(row['artifact_id'] for row in rows))
            self.assertEqual(len(messages),2)
            self.assertTrue(all(len(output.model_metadata['model_calls'])==2 for output in outputs.values()))
            for item in prepared:
                self.assertEqual(outputs[item.artifact_id].recommended_codes[0].supporting_evidence,
                                 item.context_packet.evidence_items)
            self.assertIn('base_codebook',messages[0][1].content)
            responses.extend([{'case_proposals':[rows[0],rows[0]]}]*2)
            with self.assertRaises(AgentExecutionError): agent.reconcile_batch(run_state=state,prepared=prepared)

    def test_conflicting_same_category_definitions_and_operations_cannot_pass_reconciliation(self):
        from coda.agents.arbitration_agent import ComparisonLLMAgent
        from coda.agents.base import AgentExecutionError
        from coda.state import CodebookChangeState
        outputs = {key:ComparisonOutput(artifact_id=key,agreement_summary='Supported',disagreement_summary='',
            recommended_codes=[ProvisionalCode(code_name='Same concept',short_definition=definition,
                                               relationship_to_codebook='new_code')])
            for key,definition in [('a','One meaning'),('b','Another meaning')]}
        with self.assertRaises(AgentExecutionError): ComparisonLLMAgent._validate_batch_consistency(outputs)

        for key,action in [('a','merge'),('b','split')]:
            outputs[key] = replace(outputs[key],recommended_codes=[],possible_codebook_changes=[
                CodebookChangeState(change_id=key,action=action,round_index=0,summary='Conflicting edit',
                                    target_code_ids=['old'])])
        with self.assertRaises(AgentExecutionError): ComparisonLLMAgent._validate_batch_consistency(outputs)

    def test_single_artifact_selective_skips_saved_random_draws_but_keeps_r2_review(self):
        from coda.contracts import ValidationOutput, ValidationSignal
        from coda.orchestrator import CODAOrchestrator
        with tempfile.TemporaryDirectory() as root:
            service = self.service(root,[],[])
            run_id = service.create_run(dataset_name='static_analysis_nondeterminism',artifact_limit=2,
                review_mode='selective',iterative_batch_size=1)['run_id']
            service.initialize_run(run_id)
            service.submit_stage_review(run_id,'initial',decision='accept',rationale='Initial review complete.')
            state = service._load_run_state(run_id)
            artifact = state.coding_batches[0].artifacts[0]
            manifest = state.metadata['review_sampling_manifest']
            manifest['streams']['current']['decisions'][artifact.artifact_id] = {'sampled':True}
            manifest['sampled_artifact_ids'] = [artifact.artifact_id]
            manifest['streams']['retrospective']['decisions'][artifact.artifact_id] = {'sampled':True}
            for stream in ('current','retrospective'):
                self.assertFalse(CODAOrchestrator._selective_audit_membership(state,
                    artifact_id=artifact.artifact_id,stream=stream))
                self.assertEqual(manifest['streams'][stream]['eligible_decision_count'],0)
            orchestrator = service._orchestrator_for(run_id)
            prepared = orchestrator.prepare_one_artifact(state,artifact=artifact,batch=state.coding_batches[0])
            route = prepared.evidence_packet.routing_decision
            self.assertFalse(route.random_audit)
            self.assertEqual(route.route,'automatic_accept')
            self.assertEqual(route.signal_details['effective_random_audit_rate'],0)
            orchestrator._validation_agent = lambda value:ValidationOutput(
                artifact_id=value.artifact.artifact_id,review_criteria=['R2'],
                signals=[ValidationSignal(signal='evidence_insufficient',summary='Need original log.')])
            prepared = orchestrator.prepare_one_artifact(state,artifact=artifact,batch=state.coding_batches[0])
            self.assertEqual(prepared.evidence_packet.routing_decision.route,'human_review')
            self.assertIn('R2',prepared.evidence_packet.routing_decision.signal_details['review_criteria'])

    def test_multi_case_run_keeps_sampling_for_single_case_tail_and_reassessment(self):
        from coda.orchestrator import CODAOrchestrator
        with tempfile.TemporaryDirectory() as root:
            service = self.service(root,[],[])
            run_id = service.create_run(dataset_name='static_analysis_nondeterminism',artifact_limit=3,
                review_mode='selective',iterative_batch_size=2)['run_id']
            service.initialize_run(run_id)
            state = service._load_run_state(run_id)
            self.assertEqual(len(state.coding_batches[-1].artifacts),1)
            tail = state.coding_batches[-1].artifacts[0].artifact_id
            manifest = state.metadata['review_sampling_manifest']
            for stream in ('current','retrospective'):
                manifest['streams'][stream]['decisions'][tail] = {'sampled':True}
                self.assertTrue(CODAOrchestrator._selective_audit_membership(state,
                    artifact_id=tail,stream=stream))


if __name__ == '__main__': unittest.main()
