import importlib.util,json,tempfile,unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location('execution',Path(__file__).with_name('run_codebooks.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Integrity(unittest.TestCase):
 def test_no_material_lost_in_segmenting(self):
  case={'artifact_id':'x','provenance':{},'sections':[{'field':'body','text':'甲乙\n'*20000,'source':'s','scope':None},{'field':'comment','text':'later reply','source':'c','scope':{'created_at':'t'}}]}
  pieces=m.pieces(case,101)
  for s in case['sections']:self.assertEqual(''.join(p['text'] for p in pieces if p['field']==s['field']),s['text'])
 def test_invented_evidence_rejected(self):
  case={'artifact_id':'x','sections':[{'field':'body','text':'proposed fix'}]}
  for evidence in [[{'field':'body','quote':'fixed'}],[{'field':'wrong','quote':'proposed'}],[{'field':'body','quote':''}],[{'artifact_id':'y','field':'body','quote':'proposed'}]]:
   with self.assertRaises(ValueError):m.evidence_valid(evidence,case)
  m.evidence_valid([{'field':'body','quote':'proposed'}],case)
 def test_run_orders_are_same_corpus_different_order(self):
  for name,count in [('SATD',856),('Privacy',652)]:
   root=m.WORK/name;corpus=json.loads((root/'input/corpus.json').read_text());orders=[json.loads((root/r/'order.json').read_text()) for r in ['GPT6-1','GPT6-2']]
   self.assertEqual(len(corpus),count);self.assertEqual(set(orders[0]['artifact_ids']),set(orders[1]['artifact_ids']));self.assertNotEqual(orders[0]['artifact_ids'],orders[1]['artifact_ids']);self.assertEqual(orders[0]['corpus_sha256'],orders[1]['corpus_sha256'])
 def test_reference_fields_and_codes_not_supplied(self):
  forbidden={'harmonized_labels','github_labels','trigger_rater_2','privacy_issue_rater_2','consent_interaction_rater_2','resolution_rater_2','ML TD Type','Software TD Type','code_ids','taxonomy'}
  def walk(obj):
   if isinstance(obj,dict):
    self.assertFalse(forbidden.intersection(obj))
    for x in obj.values():walk(x)
   elif isinstance(obj,list):
    for x in obj:walk(x)
  for name in ['SATD','Privacy']:walk(json.loads((m.WORK/name/'input/corpus.json').read_text()))
if __name__=='__main__':unittest.main()
