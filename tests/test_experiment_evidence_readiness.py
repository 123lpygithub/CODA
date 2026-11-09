"""Historical evidence and external context must remain bounded and citable."""
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from adapters import MLSATD23ShadesAdapter, PersonalDataProtectionGitHubAdapter
from adapters.github_issue_snapshot import normalize_snapshot
from adapters.github_linked_evidence import load_linked_evidence, snapshot_digest
from scripts.prepare_privacy_external_evidence import collect, discover
from scripts.prepare_privacy_issue_discussions import write_json
from scripts.recover_satd_related_history import verify_relation
from scripts.prepare_paper_experiment import verify_bundle, condition_plan
from coda.sensitivity import complete_evidence_case
from tests.test_privacy_issue_snapshot import issue_response

PAPER_BUNDLE = Path(__file__).resolve().parents[1]/'experiments/materials/evidence-20261105-v7'


class ExperimentEvidenceReadinessTests(unittest.TestCase):
    def test_complete_discussion_does_not_hide_missing_linked_sources(self):
        item={'content':'Source text','raw_fields':{'evidence_status':'complete','body':'Original'}}
        self.assertTrue(complete_evidence_case(item))
        for status in ('partial','unavailable','pending'):
            fields=dict(item['raw_fields'],linked_artifact_1=f'Source: URL\nKind: file; availability: {status}\nGap')
            self.assertFalse(complete_evidence_case(dict(item,raw_fields=fields)))
        fields=dict(item['raw_fields'],external_artifact_1='Source: URL\nKind: external_url; availability: available; retrieved: now\nText')
        self.assertTrue(complete_evidence_case(dict(item,raw_fields=fields)))
        self.assertFalse(complete_evidence_case({'content':'Title only','raw_fields':{'evidence_status':'complete','body':'','retrieved_comment_count':0}}))

    @unittest.skipUnless(PAPER_BUNDLE.is_dir(), 'Archived experiment evidence is not included in the repository.')
    def test_frozen_paper_bundle_and_all_matched_conditions(self):
        root=Path(__file__).resolve().parents[1]/'experiments/materials/evidence-20261105-v7'
        with patch.dict('os.environ',{}):
            manifest,pools,report=verify_bundle(root)
        conditions=condition_plan(manifest,pools)
        self.assertEqual(len(conditions),36)
        self.assertEqual(len({c['condition_id'] for c in conditions}),36)
        for dataset in pools:
            for phase in ('pilot','formal'):
                for replicate in (1,2):
                    block=[c for c in conditions if (c['dataset_name'],c['study_phase'],c['replicate_index'])==(dataset,phase,replicate)]
                    self.assertEqual({c['review_mode'] for c in block},{'automatic','selective','full'})
                    self.assertEqual(len({c['ordered_evidence_sha256'] for c in block}),1)
                    self.assertEqual(len({c['comparison_block_id'] for c in block}),1)
        self.assertEqual(report['ml_satd_23_shades']['evidence_status_counts']['historical_partial'],3)
        self.assertEqual(len(report['personal_data_protection_github']['retrieved_empty_body_cases']),7)

    @unittest.skipUnless(PAPER_BUNDLE.is_dir(), 'Archived experiment evidence is not included in the repository.')
    def test_preflight_refuses_tampered_frozen_companion(self):
        source=Path(__file__).resolve().parents[1]/'experiments/materials/evidence-20261105-v7'
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            for name in ('study_manifest.json','evidence_audit.json'):
                (root/name).write_bytes((source/name).read_bytes())
            (root/'agent_inputs.json').write_text('{}')
            with self.assertRaisesRegex(ValueError,'checksum mismatch'):
                verify_bundle(root)

    def test_revision_relations_cannot_be_inferred_from_comment_similarity(self):
        a,b,c='a'*40,'b'*40,'c'*40
        common={'base_commit':{'sha':a}}
        self.assertEqual(verify_relation(dict(common,status='ahead',behind_by=0,merge_base_commit={'sha':a}),a,b),'verified-ancestor')
        self.assertEqual(verify_relation(dict(common,status='behind',ahead_by=0,merge_base_commit={'sha':b}),a,b),'verified-descendant')
        self.assertEqual(verify_relation(dict(common,status='diverged',merge_base_commit={'sha':c}),a,b),'verified-related-branch')
        for data in [dict(common,status='ahead',behind_by=0,merge_base_commit={'sha':c}),
                     dict(common,status='behind',ahead_by=1,merge_base_commit={'sha':b}),
                     dict(common,status='diverged'),{'base_commit':{'sha':b}}]:
            with self.assertRaises(ValueError):verify_relation(data,a,b)

    def test_related_history_remains_partial_in_agent_input(self):
        with patch.dict('os.environ',{'CODA_EVIDENCE_PROFILE':''}):
            original=next(MLSATD23ShadesAdapter().iter_artifacts())
        fields=original.raw_fields
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            payload={'artifact_id':original.artifact_id,'revision_url':fields['comment_introducing_revision'],
                     'filename':fields['filename'],'status':'historical_partial','excerpt':'# Original comment\noperation()',
                     'commit':'a'*40,'line_start':1,'line_end':2,'revision_relation':'verified-descendant',
                     'revision_note':'Later revision; not evidence of case-time behavior.',
                     'source_url':'https://raw.githubusercontent.com/o/r/'+'a'*40+'/file.py'}
            write_json(root/'case.json',payload)
            write_json(root/'manifest.json',{'artifacts':{original.artifact_id:{'file':'case.json','sha256':hashlib.sha256((root/'case.json').read_bytes()).hexdigest()}}})
            enriched=next(MLSATD23ShadesAdapter(context_dir=root).iter_artifacts())
        self.assertEqual(enriched.raw_fields['source_context_status'],'historical_partial')
        self.assertIn('not evidence of case-time behavior',enriched.content)
        self.assertIn('related historical',enriched.content)

    def test_external_context_checks_lineage_and_citations_without_manual_labels(self):
        snapshot=normalize_snapshot('privacy-issue-1',issue_response(0),[],comments_complete=True)
        snapshot['body']='See https://gdpr-info.eu/art-17-gdpr/#one and https://evil.test/not-allowed'
        links=discover(snapshot)
        self.assertEqual([x['url'] for x in links],['https://gdpr-info.eu/art-17-gdpr/'])
        self.assertEqual(links[0]['cited_in'],['body'])
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            payload={'artifact_id':'privacy-issue-1','source_issue_url':snapshot['issue_url'],
                     'issue_snapshot_sha256':snapshot_digest(snapshot),'scope':'Retrieval-time external context',
                     'links':[dict(links[0],status='available',text='Exact source text')]}
            write_json(root/'case.json',payload)
            write_json(root/'external_manifest.json',{'artifacts':{'privacy-issue-1':{'file':'case.json','sha256':hashlib.sha256((root/'case.json').read_bytes()).hexdigest()}}})
            row={'index':'1','html_url':snapshot['issue_url'],'title':'Original','privacy_issue_rater_2':'secret-human-label'}
            adapter=PersonalDataProtectionGitHubAdapter(linked_dir=root)
            with patch.dict('os.environ',{'CODA_EVIDENCE_PROFILE':'paper-20261105-ready'}),patch.object(adapter,'_load_rows',return_value=[row]),patch('adapters.personal_data_protection_github.load_snapshot',return_value=snapshot):
                artifact=next(adapter.iter_artifacts())
            self.assertIn('Exact source text',artifact.content)
            self.assertNotIn('secret-human-label',artifact.content)
            self.assertTrue(any(r.field=='external_artifact_1' for r in artifact.source_refs))
            with self.assertRaisesRegex(ValueError,'different issue snapshot'):
                load_linked_evidence(root,'privacy-issue-1',snapshot['issue_url'],dict(snapshot,body='Changed'),manifest_name='external_manifest.json')
            (root/'case.json').write_text('{}')
            with self.assertRaisesRegex(ValueError,'checksum mismatch'):
                load_linked_evidence(root,'privacy-issue-1',snapshot['issue_url'],snapshot,manifest_name='external_manifest.json')

    def test_external_html_is_not_mistaken_for_complete_discussion_or_cited_page(self):
        for url,final in [('https://bugzilla.mozilla.org/show_bug.cgi?id=1','https://bugzilla.mozilla.org/show_bug.cgi?id=1'),
                          ('https://docs.microsoft.com/old-page','https://learn.microsoft.com/landing')]:
            with self.subTest(url=url),tempfile.TemporaryDirectory() as directory:
                root=Path(directory);html='<p>Retrieved public text. '+('Source details '*30)+'</p><script>HIDDEN SCRIPT</script>'
                raw={'url':url,'final_url':final,'text':html,'content_type':'text/html','sha256':hashlib.sha256(html.encode()).hexdigest(),'fetched_at':'now'}
                write_json(root/'external_raw'/(hashlib.sha256(url.encode()).hexdigest()+'.json'),raw)
                item=collect({'url':url,'kind':'external_url'},root,1)
                self.assertEqual(item['status'],'partial')
                self.assertNotIn('HIDDEN SCRIPT',item['text'])
                self.assertIn('not original Markdown',item['extraction_method'])
