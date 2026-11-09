"""Linked evidence collection, boundaries, lineage and agent-visible citations."""
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from adapters.github_linked_evidence import discover_links, load_linked_evidence, snapshot_digest, render_link
from adapters.personal_data_protection_github import PersonalDataProtectionGitHubAdapter
from scripts.prepare_privacy_linked_artifacts import Collector
from scripts.prepare_privacy_issue_discussions import write_json, CacheMiss
from tests.test_privacy_issue_snapshot import issue_response
from adapters.github_issue_snapshot import normalize_snapshot


class LinkedDevelopmentEvidenceTests(unittest.TestCase):
    def test_slash_branch_and_encoded_filename_use_verified_blob_metadata(self):
        payload={'payload':{'refInfo':{'name':'next/v99','currentOid':'b'*40},
                            'path':'dir/test#file.py'}}
        html='<script type="application/json" data-target="react-app.embeddedData">'+json.dumps(payload)+'</script>'
        url='https://github.com/o/r/blob/next/v99/dir/test%23file.py'
        with tempfile.TemporaryDirectory() as directory:
            collector=Collector(Path(directory),Path(directory),1,False)
            with patch('scripts.prepare_privacy_web_evidence.read_page',return_value={'html':html,'url':url,'final_url':url}):
                location=collector.source_location({'url':url})
        self.assertEqual(location,('o/r','b'*40,'dir/test#file.py',True))

    def test_pr_issue_retains_reviews_and_patch_without_inventing_completion(self):
        with tempfile.TemporaryDirectory() as directory:
            collector=Collector(Path(directory),Path(directory),1,True)
            response=issue_response(0)
            response['data'].update(html_url='https://github.com/o/r/pull/2',
                comments_url='https://api.github.com/repos/o/r/issues/2/comments',
                pull_request={'url':'https://api.github.com/repos/o/r/pulls/2'})
            with patch.object(collector,'paginated_records',side_effect=[[],[{'body':'Reviewer concern'}],[]]),patch.object(collector,'api',return_value={'data':{'head':{'sha':'b'*40},'merged':False}}),patch.object(collector,'text',return_value={'text':'patch'}):
                result=collector.pull_request_from_issue(response)
        self.assertEqual(result['status'],'available')
        self.assertIn('Reviewer concern',result['text'])
        self.assertIn('"merged": false',result['text'])

    def test_unavailable_linked_issue_can_retain_explicitly_partial_archive(self):
        historical={'text':'Archived original issue and comments','status':'partial',
                    'historical_evidence':True,'reason':'Historical events only'}
        with tempfile.TemporaryDirectory() as directory:
            collector=Collector(Path(directory),Path(directory),1,False)
            with patch.object(collector,'api',side_effect=CacheMiss('missing')),patch('scripts.prepare_privacy_web_evidence.collect',return_value=('id',None,'404')),patch.object(collector,'historical_issue',return_value=historical):
                result=collector.collect({'url':'https://github.com/o/r/issues/2','kind':'issue'})
        self.assertEqual(result['status'],'partial')
        self.assertTrue(result['historical_evidence'])
        self.assertEqual(result['current_retrieval_error'],'404')

    def test_historical_link_recovery_requires_original_body_and_stays_partial(self):
        events=[{'event_type':'IssuesEvent','action':'opened','title':'Original',
                 'created_at':'2020-01-01 00:00:00','comments':1}]
        snapshot={'issue_body_available':True,'issue_fetched_at':'now',
                  'retrieved_comment_count':1,'expected_comment_count':1,'body':'Original text'}
        with tempfile.TemporaryDirectory() as directory:
            collector=Collector(Path(directory),Path(directory),1,False)
            with patch('scripts.recover_privacy_event_archive.query',return_value=(events,{})),patch('scripts.recover_privacy_event_archive.recover',return_value=('id',snapshot,{'event_count':2})):
                result=collector.historical_issue('o/r','2')
            with patch('scripts.recover_privacy_event_archive.query',return_value=([],{})):
                with self.assertRaisesRegex(ValueError,'No archived issue event'):
                    collector.historical_issue('o/r','2')
        self.assertEqual(result['status'],'partial')
        self.assertTrue(result['historical_evidence'])

    def test_long_patch_is_explicitly_excerpted_without_claiming_full_inspection(self):
        text='one patch line\n'*100
        rendered=render_link({'url':'https://github.com/o/r/pull/2','kind':'pull_request','status':'available','text':text}, max_chars=120)
        self.assertIn('Source excerpt ends here',rendered)
        self.assertIn('Do not infer omitted changes',rendered)
        self.assertEqual(text,'one patch line\n'*100)

    def snapshot(self):
        snapshot = normalize_snapshot('privacy-issue-1', issue_response(0), [], comments_complete=True)
        snapshot['body'] = 'See https://github.com/owner/repo/issues/2 and https://github.com/owner/repo/blob/'+'a'*40+'/src.py#L20-L21. Also https://evil.test/commit/abc and https://github.com/owner/repo/issues/1. Do not treat CSS #123 as a link.'
        return snapshot

    def test_one_hop_discovery_records_location_and_ignores_self_and_foreign_hosts(self):
        links = discover_links(self.snapshot())
        self.assertEqual(len(links), 2)
        self.assertEqual({link['kind'] for link in links}, {'file','issue'})
        self.assertTrue(all(link['cited_in']==['body'] for link in links))
        self.assertTrue(any(link['url'].endswith('#L20-L21') for link in links))

    def test_quoted_issue_links_exclude_quotes_and_creation_forms(self):
        snapshot=self.snapshot()
        snapshot['body']="See 'https://github.com/o/r/issues/60'. Or https://github.com/o/r/issues/new and https://github.com/o/r/pull/new."
        self.assertEqual([x['url'] for x in discover_links(snapshot)],['https://github.com/o/r/issues/60'])

    def test_fixed_file_has_exact_line_context_and_revision(self):
        with tempfile.TemporaryDirectory() as directory:
            collector=Collector(Path(directory),Path(directory),1,True)
            source='\n'.join(f'line {i}' for i in range(1,50))
            raw={'text':source,'sha256':hashlib.sha256(source.encode()).hexdigest(),'fetched_at':'2026-11-05','url':'https://raw.githubusercontent.com/owner/repo/'+'a'*40+'/src.py'}
            with patch.object(collector,'text',return_value=raw), patch.object(collector,'api') as api:
                result=collector.collect(next(i for i in discover_links(self.snapshot()) if i['kind']=='file'))
                api.assert_not_called()
            self.assertEqual(result['status'],'available')
            self.assertTrue(result['immutable_revision'])
            self.assertEqual((result['line_start'],result['line_end']),(8,33))
            self.assertIn('line 20',result['text'])

    def test_branch_context_is_explicit_when_commit_resolution_unavailable(self):
        with tempfile.TemporaryDirectory() as directory:
            collector=Collector(Path(directory),Path(directory),1,True)
            with patch.object(collector,'api',side_effect=CacheMiss('not cached')), patch.object(collector,'text',return_value={'text':'original','sha256':'hash','fetched_at':'date','url':'url'}):
                result=collector.collect({'url':'https://github.com/o/r/blob/main/f.py','kind':'file','cited_in':['body']})
            self.assertEqual(result['status'],'available')
            self.assertFalse(result['immutable_revision'])
            self.assertEqual(result['revision'],'main')

    def test_unavailable_patch_metadata_does_not_assert_merge(self):
        with tempfile.TemporaryDirectory() as directory:
            collector=Collector(Path(directory),Path(directory),1,True)
            with patch.object(collector,'api',side_effect=CacheMiss('not cached')), patch.object(collector,'text',return_value={'text':'patch','sha256':'hash','fetched_at':'date','url':'url'}):
                result=collector.collect({'url':'https://github.com/o/r/pull/2','kind':'pull_request','cited_in':['body']})
            self.assertEqual(result['status'],'available')
            self.assertIn('does not establish merge',result['metadata_status'])
            self.assertFalse(result['immutable_revision'])

    def test_linked_issue_missing_comment_pages_is_partial(self):
        with tempfile.TemporaryDirectory() as directory:
            collector=Collector(Path(directory),Path(directory),1,True)
            response=issue_response(1)
            with patch.object(collector,'api',side_effect=[response,CacheMiss('comments absent')]):
                result=collector.collect({'url':'https://github.com/owner/repo/issues/2','kind':'issue','cited_in':['body']})
            self.assertEqual(result['status'],'partial')
            self.assertEqual(result['retrieved_comment_count'],0)
            self.assertIn('Complete original',result['text'])

    def test_snapshot_lineage_and_adapter_citations_are_checked(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);snapshot=self.snapshot()
            item=dict(discover_links(snapshot)[0],text='Exact linked implementation',status='available')
            payload={'artifact_id':'privacy-issue-1','source_issue_url':snapshot['issue_url'],'issue_snapshot_sha256':snapshot_digest(snapshot),'scope':'Fixed one-hop sources','links':[item]}
            write_json(root/'case.json',payload)
            write_json(root/'manifest.json',{'artifacts':{'privacy-issue-1':{'file':'case.json','sha256':hashlib.sha256((root/'case.json').read_bytes()).hexdigest()}}})
            self.assertEqual(load_linked_evidence(root,'privacy-issue-1',snapshot['issue_url'],snapshot),payload)
            changed=dict(snapshot,body='changed')
            with self.assertRaisesRegex(ValueError,'different issue snapshot'):
                load_linked_evidence(root,'privacy-issue-1',snapshot['issue_url'],changed)
            adapter=PersonalDataProtectionGitHubAdapter(linked_dir=root)
            row={'index':'1','url':'https://api.github.com/repos/owner/repo/issues/1','html_url':snapshot['issue_url'],'title':'Issue','privacy_issue_rater_2':'hidden-category'}
            with patch.object(adapter,'_load_rows',return_value=[row]),patch('adapters.personal_data_protection_github.load_snapshot',return_value=snapshot):
                artifact=next(adapter.iter_artifacts())
            self.assertIn('Exact linked implementation',artifact.content)
            self.assertTrue(any(r.field=='linked_artifact_1' for r in artifact.source_refs))
            self.assertNotIn('hidden-category',artifact.content)
            (root/'case.json').write_text('{}')
            with self.assertRaisesRegex(ValueError,'checksum mismatch'):
                load_linked_evidence(root,'privacy-issue-1',snapshot['issue_url'],snapshot)
