"""Original Markdown recovery must distinguish complete from truncated timelines."""
import json
import unittest
from scripts.prepare_privacy_web_evidence import parse_snapshot


class PrivacyWebEvidenceTests(unittest.TestCase):
    def page(self, next_page=False, count=1):
        node={'__typename':'IssueComment','databaseId':10,'url':'https://github.com/o/r/issues/1#issuecomment-10','body':'Exact **comment**','createdAt':'2022-01-02','author':{'id':'A','login':'person'}}
        issue={'url':'https://github.com/o/r/issues/1','number':1,'repository':{'nameWithOwner':'o/r'},'title':'Title','body':'Original *Markdown*','createdAt':'2022-01-01','updatedAt':'2022-01-02','state':'CLOSED','totalCommentsCount':count,'author':{'id':'B'},'timelineItems':{'pageInfo':{'hasNextPage':next_page,'hasPreviousPage':False},'edges':[{'node':node}]}}
        payload={'payload':{'issueViewerRoute':{'data':{'repository':{'issue':issue}}}}}
        return '<script type="application/json" data-target="react-app.embeddedData">'+json.dumps(payload)+'</script>'

    def test_original_markdown_and_count_verified_complete(self):
        s=parse_snapshot(self.page(),'privacy-issue-1','https://github.com/o/r/issues/1','now')
        self.assertEqual(s['body'],'Original *Markdown*')
        self.assertEqual(s['comments'][0]['body'],'Exact **comment**')
        self.assertEqual(s['evidence_status'],'complete')
        self.assertFalse(s['closed_at_available'])
        self.assertNotIn('login',json.dumps(s))

    def test_pagination_or_count_mismatch_cannot_be_complete(self):
        for page in [self.page(next_page=True),self.page(count=2)]:
            s=parse_snapshot(page,'privacy-issue-1','https://github.com/o/r/issues/1','now')
            self.assertEqual(s['evidence_status'],'partial')

    def test_unexpected_issue_number_is_rejected(self):
        with self.assertRaisesRegex(ValueError,'identity'):
            parse_snapshot(self.page(),'privacy-issue-2','https://github.com/o/r/issues/2','now')

    def test_verified_redirect_can_transfer_issue_to_another_number(self):
        s=parse_snapshot(self.page(),'privacy-issue-old','https://github.com/old/repo/issues/99',
                         'now','https://github.com/o/r/issues/1')
        self.assertEqual(s['source_issue_url'],'https://github.com/old/repo/issues/99')
        self.assertEqual(s['issue_url'],'https://github.com/o/r/issues/1')
        self.assertIn('redirect',s['identity_relation'])
        with self.assertRaisesRegex(ValueError,'identity'):
            parse_snapshot(self.page(),'id','https://github.com/old/repo/issues/99',
                           'now','https://github.com/o/r/issues/3')
