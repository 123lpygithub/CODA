"""Recovery must preserve source identity, history and pagination boundaries."""
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from scripts.prepare_privacy_web_evidence import collect_paginated
from scripts.recover_satd_archived_context import Archive, added_lines, changed_comment_excerpt, recover as recover_satd
from types import SimpleNamespace
from scripts.recover_privacy_event_archive import recover
from tests import test_privacy_web_evidence as web_fixtures


class ArchiveRecoveryTests(unittest.TestCase):
    def test_repeated_comment_recovery_retains_every_exact_candidate(self):
        source='# TODO fix\nfirst()\n# TODO fix\nsecond()'
        artifact=SimpleNamespace(artifact_id='case',raw_fields={
            'comment_introducing_revision':'https://github.com/o/r/commit/'+'a'*40,
            'filename':'f.py','comment_text':'TODO fix'})
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            (root/'manifest.json').write_text(json.dumps({'artifacts':{'case':{'status':'unmatched'}}}))
            archive=Archive(root,1)
            with patch.object(archive,'source',return_value={'source':source,'source_url':'original','source_sha256':'digest'}),patch.object(archive,'read',return_value=(b'',{'sha256':'diffdigest'})):
                aid,entry=recover_satd(artifact,root,archive)
            payload=json.loads((root/entry['file']).read_text())
        self.assertEqual(entry['status'],'ambiguous')
        self.assertEqual(entry['candidate_count'],2)
        self.assertEqual([c['comment_line_start'] for c in payload['candidates']],[1,3])
        self.assertNotIn('line_start',payload)

    def test_diff_disambiguation_uses_exact_path_and_new_line_numbers(self):
        source='# TODO fix\nfirst()\n# TODO fix\nsecond()'
        diff='diff --git a/f.py b/f.py\n--- a/f.py\n+++ b/f.py\n@@ -1,2 +1,4 @@\n # TODO fix\n first()\n+# TODO fix\n+second()\n'
        self.assertEqual(added_lines(diff,'f.py'),{3,4})
        self.assertEqual(added_lines(diff,'other.py'),set())
        self.assertIsNotNone(changed_comment_excerpt(source,'TODO fix',diff,'f.py'))
        self.assertIsNone(changed_comment_excerpt(source,'TODO missing',diff,'f.py'))

    def test_archive_verifies_git_blob_and_sha256(self):
        data=b'# TODO fix\noperation()\n'
        digest=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        commit='a'*40
        entry={'type':'file','target':digest,'checksums':{'sha256':hashlib.sha256(data).hexdigest()}}
        with tempfile.TemporaryDirectory() as directory:
            archive=Archive(Path(directory),1)
            with patch.object(archive,'json',side_effect=[{'id':commit,'directory':'d'*40},entry]),patch.object(archive,'read',return_value=(data,{'sha256':hashlib.sha256(data).hexdigest(),'fetched_at':'now'})):
                result=archive.source(commit,'f.py')
            self.assertEqual(result['git_blob_sha1'],digest)
            with patch.object(archive,'json',side_effect=[{'id':commit,'directory':'d'*40},dict(entry,target='b'*40)]),patch.object(archive,'read',return_value=(data,{'sha256':hashlib.sha256(data).hexdigest(),'fetched_at':'now'})):
                with self.assertRaisesRegex(ValueError,'Git blob'):
                    archive.source(commit,'f.py')

    def test_numbered_timeline_pages_merge_original_comments_and_remap_authors(self):
        fixture=web_fixtures.PrivacyWebEvidenceTests()
        first=fixture.page(next_page=True,count=2)
        second=json.loads(first.split('>',1)[1].rsplit('</script>',1)[0])
        issue=second['payload']['issueViewerRoute']['data']['repository']['issue']
        issue['timelineItems']['pageInfo']={'hasNextPage':False,'hasPreviousPage':True,'startCursor':'two','endCursor':'two'}
        node=issue['timelineItems']['edges'][0]['node']
        node.update(databaseId=20,body='Second original comment',url='https://github.com/o/r/issues/1#issuecomment-20',author={'id':'C'})
        second='<script type="application/json" data-target="react-app.embeddedData">'+json.dumps(second)+'</script>'
        pages=[{'url':'https://github.com/o/r/issues/1','html':first,'fetched_at':'now'},
               {'url':'https://github.com/o/r/issues/1?timeline_page=1','html':second,'fetched_at':'later'}]
        with tempfile.TemporaryDirectory() as directory,patch('scripts.prepare_privacy_web_evidence.read_page',side_effect=pages):
            snapshot=collect_paginated('https://github.com/o/r/issues/1','privacy-issue-1',Path(directory),1)
        self.assertTrue(snapshot['comments_complete'])
        self.assertEqual([c['id'] for c in snapshot['comments']],[10,20])
        self.assertNotEqual(snapshot['comments'][0]['author'],snapshot['comments'][1]['author'])

    def test_changed_issue_during_pagination_stays_partial(self):
        fixture=web_fixtures.PrivacyWebEvidenceTests();first=fixture.page(next_page=True,count=2)
        second=first.replace('Original *Markdown*','Changed body')
        with tempfile.TemporaryDirectory() as directory,patch('scripts.prepare_privacy_web_evidence.read_page',side_effect=[{'url':'url','html':first,'fetched_at':'now'},{'url':'url','html':second,'fetched_at':'later'}]):
            snapshot=collect_paginated('https://github.com/o/r/issues/1','privacy-issue-1',Path(directory),1)
        self.assertEqual(snapshot['evidence_status'],'partial')
        self.assertIn('changed',snapshot['pagination_error'])

    def test_historical_events_cannot_be_reported_as_current_complete_discussion(self):
        row={'index':'1','project':'o/r','issue_number':'1','html_url':'https://github.com/o/r/issues/1','url':'https://api.github.com/repos/o/r/issues/1','title':'Title','created_at':'2020-01-01 00:00:00.000000','#comments':'0'}
        event={'event_type':'IssuesEvent','action':'opened','body':'Archived original','title':'Title','created_at':'2020-01-01 00:00:00','updated_at':'2020-01-01 00:00:00','state':'open','comments':0}
        with tempfile.TemporaryDirectory() as directory,patch('scripts.recover_privacy_event_archive.query',return_value=([event],{'url':'https://play.clickhouse.com/','fetched_at':'now','response_sha256':'hash'})):
            aid,snapshot,audit=recover(row,Path(directory),1)
        self.assertEqual(snapshot['evidence_status'],'partial')
        self.assertTrue(snapshot['historical_evidence'])
        self.assertEqual(snapshot['body'],'Archived original')
