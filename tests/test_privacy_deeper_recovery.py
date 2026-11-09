"""Recovered deleted files and migrated issues retain identity and evidence scope."""
import base64
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from scripts.prepare_privacy_linked_artifacts import Collector
from scripts.prepare_privacy_issue_discussions import CacheMiss, write_json
from scripts.recover_privacy_file_history import historical_text, blob_text, recover
from scripts.recover_privacy_external_context import bugzilla, dspace, sync_copy, save_recovery


class PrivacyDeeperRecoveryTests(unittest.TestCase):
    def test_retry_does_not_replace_richer_migrated_discussion_with_body_only(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            old={'url':'https://jira.lyrasis.org/browse/DS-42','status':'partial','text':'Body and 24 comments','recovered_comment_count':24}
            save_recovery(root,old)
            chosen=save_recovery(root,dict(old,text='Body only',recovered_comment_count=0))
            self.assertEqual(chosen,old)

    def test_rest_file_fallback_checks_original_git_blob(self):
        source=b'Original historical text\n';sha=hashlib.sha1(b'blob '+str(len(source)).encode()+b'\0'+source).hexdigest()
        data={'path':'file.md','type':'file','encoding':'base64','content':base64.b64encode(source).decode(),'sha':sha}
        with tempfile.TemporaryDirectory() as directory:
            collector=Collector(Path(directory),Path(directory),1,True)
            with patch.object(collector,'text',side_effect=OSError('host unavailable')),patch.object(collector,'api',return_value={'data':data,'fetched_at':'now'}):
                result=historical_text(collector,'o/r','a'*40,'file.md')
                self.assertEqual(result['text'],source.decode())
                self.assertEqual(result['git_blob_sha1'],sha)
            with patch.object(collector,'text',side_effect=OSError('host unavailable')),patch.object(collector,'api',return_value={'data':dict(data,sha='b'*40),'fetched_at':'now'}):
                with self.assertRaisesRegex(ValueError,'blob mismatch'):historical_text(collector,'o/r','a'*40,'file.md')

    def test_blob_page_requires_exact_path_and_revision(self):
        payload={'payload':{'codeViewBlobLayoutRoute':{'path':'file.py','refInfo':{'currentOid':'a'*40},'blob':{}},
                            'codeViewBlobLayoutRoute.StyledBlob':{'rawLines':['# Original','operation()']}}}
        raw={'html':'<script type="application/json" data-target="react-app.embeddedData">'+json.dumps(payload)+'</script>','fetched_at':'now'}
        with tempfile.TemporaryDirectory() as directory:
            collector=Collector(Path(directory),Path(directory),1,True)
            with patch('scripts.recover_privacy_file_history.read_page',return_value=raw):
                self.assertIn('operation()',blob_text(collector,'o/r','a'*40,'file.py')['text'])
                with self.assertRaisesRegex(ValueError,'exact path/revision'):blob_text(collector,'o/r','b'*40,'file.py')

    def test_deleted_file_uses_verified_parent_and_never_claims_case_time_equivalence(self):
        history={'data':[{'sha':'a'*40,'parents':[{'sha':'b'*40}]}]}
        raw={'url':'https://raw.githubusercontent.com/o/r/'+'b'*40+'/file.py','text':'one\ntwo','sha256':'hash','fetched_at':'now'}
        with tempfile.TemporaryDirectory() as directory:
            collector=Collector(Path(directory),Path(directory),1,True)
            with patch('scripts.recover_privacy_file_history.path_history',return_value=('query',history)),patch('scripts.recover_privacy_file_history.historical_text',side_effect=[CacheMiss('deleted'),raw]):
                result=recover({'url':'https://github.com/o/r/blob/main/file.py#L99','kind':'file'},collector)
        self.assertEqual(result['revision'],'b'*40)
        self.assertEqual(result['status'],'partial')
        self.assertTrue(result['historical_evidence'])
        self.assertIn('case-time version are unknown',result['reason'])
        self.assertIn('line range does not exist',result['reason'])
        self.assertNotIn('line_start',result)

    def test_bugzilla_verifies_identity_and_public_comment_ordinals(self):
        metadata={'bugs':[{'id':42,'summary':'Original issue'}]}
        comments={'bugs':{'42':{'comments':[{'id':1,'count':0,'bug_id':42,'text':'Original body'},{'id':2,'count':1,'bug_id':42,'text':'Reply'}]}}}
        class Archive:
            def read(self,url):
                return json.dumps(comments if url.endswith('/comment') else metadata).encode(),{'sha256':'hash','fetched_at':'now'}
        link={'url':'https://bugzilla.mozilla.org/show_bug.cgi?id=42','kind':'external_url'}
        result=bugzilla(link,Archive())
        self.assertEqual(result['status'],'available')
        self.assertEqual(result['recovered_comment_count'],2)
        self.assertIn('private/deleted',result['metadata_status'])
        comments['bugs']['42']['comments'][1]['count']=3
        self.assertEqual(bugzilla(link,Archive())['status'],'partial')
        comments['bugs']['42']['comments'][0]['bug_id']=43
        with self.assertRaisesRegex(ValueError,'identity'):bugzilla(link,Archive())

    def test_dspace_requires_official_exact_source_backlink_and_keeps_missing_comments_partial(self):
        url='https://jira.lyrasis.org/browse/DS-42'
        issue={'title':'[DS-42] Original','html_url':'https://github.com/DSpace/DSpace/issues/500',
               'body':'Imported from JIRA '+url,'comments':3,'comments_url':'comments','state':'open','updated_at':'now'}
        with tempfile.TemporaryDirectory() as directory:
            collector=Collector(Path(directory),Path(directory),1,True)
            with patch.object(collector,'api',return_value={'data':{'items':[issue]},'fetched_at':'now'}),patch.object(collector,'paginated_records',side_effect=CacheMiss('comments unavailable')),patch('scripts.prepare_privacy_web_evidence.collect_paginated',side_effect=OSError('page unavailable')):
                result=dspace({'url':url,'kind':'external_url'},collector)
                self.assertEqual(result['status'],'partial')
                self.assertEqual(result['recovered_comment_count'],0)
                self.assertEqual(result['expected_imported_comment_count'],3)
                self.assertIn('not retrieved',result['reason'])
            with patch.object(collector,'api',return_value={'data':{'items':[dict(issue,body='No source backlink')]},'fetched_at':'now'}):
                with self.assertRaisesRegex(ValueError,'exact original backlink'):dspace({'url':url},collector)

    def test_jira_sync_relationship_is_not_independent_evidence(self):
        url='https://mozilla-hub.atlassian.net/browse/FNXV2-42'
        snapshot={'issue_url':'https://github.com/o/r/issues/1','title':'Original','body':'Issue is synchronized with this [Jira Task]('+url+')','comments':[],'issue_fetched_at':'now'}
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);write_json(root/'issues'/'case.json',snapshot)
            result=sync_copy({'url':url},root)
        self.assertFalse(result['independent_evidence'])
        self.assertIn('not separately retrieved Jira content',result['reason'])
