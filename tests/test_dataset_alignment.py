"""Case units, frozen evidence compatibility and exact source-context matching."""
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from adapters import Defects4CodeLLMSemanticAdapter, MLSATD23ShadesAdapter
from adapters.satd_context import load_context
from coda.web.runtime import CodaWebService
from coda.study import load_study_manifest, select_study_artifacts, StudyManifestError

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('prepare_satd_context', ROOT/'scripts/prepare_satd_source_context.py')
preparation = importlib.util.module_from_spec(spec)
spec.loader.exec_module(preparation)


class DatasetAlignmentTests(unittest.TestCase):
    def test_revised_manifest_keeps_allocation_and_requires_matching_profile(self):
        old=load_study_manifest(ROOT/'experiments/materials/coda-calibration20-20261102-v1.json')
        new=load_study_manifest(ROOT/'experiments/materials/evidence-20261105-v1/study_manifest.json')
        for dataset in old['datasets']:
            for before,after in zip(old['datasets'][dataset]['artifacts'],new['datasets'][dataset]['artifacts']):
                for field in ['artifact_id','group_family','group_id','phase','order']:
                    self.assertEqual(before[field],after[field])
        with patch.dict('os.environ',{'CODA_EVIDENCE_PROFILE':''}):
            with self.assertRaisesRegex(StudyManifestError,'CODA_EVIDENCE_PROFILE'):
                select_study_artifacts(new,'llm_code_error_semantic',[],'formal')

    def test_solution_view_retains_old_error_ids_and_all_visible_evidence(self):
        adapter = Defects4CodeLLMSemanticAdapter()
        rows = list(adapter.iter_artifacts())
        solutions = list(adapter.iter_solution_artifacts())
        self.assertEqual(len(rows), 687)
        self.assertEqual(len(solutions), 557)
        self.assertEqual(len({(x.raw_fields['task_id'], x.raw_fields['model'], x.raw_fields['incorrect_code']) for x in solutions}), 557)
        old = {x.artifact_id:x for x in rows}
        for solution in solutions:
            self.assertEqual(solution, old[solution.artifact_id])
            self.assertNotIn('category', solution.raw_fields)
        with tempfile.TemporaryDirectory() as directory:
            service = CodaWebService(runs_root=directory, adapter_factories={'llm_code_error_semantic':Defects4CodeLLMSemanticAdapter})
            self.assertEqual(service.available_datasets()[0]['target_record_count'],557)
            created=service.create_run(dataset_name='llm_code_error_semantic')
            self.assertEqual(created['input_artifacts'],557)

    def test_comment_match_requires_unique_complete_normalized_text(self):
        source='x = 1\n# TODO: fix this\ny = 2\n'
        excerpt=preparation.extract_excerpt(source,'# TODO: fix this')
        self.assertEqual(excerpt,(1,3,source.strip()))
        self.assertIsNone(preparation.extract_excerpt(source+source,'# TODO: fix this'))
        self.assertIsNone(preparation.extract_excerpt(source,'# TODO: missing text'))
        self.assertIsNotNone(preparation.extract_excerpt("'''\nFunctions used\nTODO refactor\n'''", "''' || Functions used || TODO refactor || '''"))
        self.assertIsNotNone(preparation.extract_excerpt('# TODO: name, index\noperation()', 'TODO: name; index'))
        self.assertIsNotNone(preparation.extract_excerpt('"""\nTODO: gains/biases\n\nend\n"""', '\\"\\"\\" || TODO: gains\\/biases || || end || \\"\\"\\"'))
        self.assertIsNone(preparation.extract_excerpt('value = "TODO: name"', 'TODO: name'))
        self.assertIsNone(preparation.extract_excerpt('# TODO: name, index\n# TODO: name; index', 'TODO: name; index'))

    def test_fixed_context_is_checked_and_exposed_without_changing_legacy_view(self):
        adapter=MLSATD23ShadesAdapter()
        legacy=next(iter(adapter.iter_artifacts()))
        fields=legacy.raw_fields
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            payload={'artifact_id':legacy.artifact_id,'revision_url':fields['comment_introducing_revision'],
                     'filename':fields['filename'],'excerpt':'# Original comment\noperation()', 'commit':'a'*40,
                     'source_url':'https://raw.githubusercontent.com/owner/repo/'+'a'*40+'/file.py','line_start':4,'line_end':5}
            path=root/'context.json';path.write_text(json.dumps(payload))
            (root/'manifest.json').write_text(json.dumps({'artifacts':{legacy.artifact_id:{'file':'context.json','sha256':hashlib.sha256(path.read_bytes()).hexdigest()}}}))
            enriched=next(iter(MLSATD23ShadesAdapter(context_dir=root).iter_artifacts()))
            self.assertIn('operation()',enriched.content)
            self.assertTrue(any(ref.field=='source_context' for ref in enriched.source_refs))
            self.assertNotIn('source_context',legacy.raw_fields)
            self.assertNotIn('ML TD Type',enriched.raw_fields)
            with self.assertRaisesRegex(ValueError,'identity mismatch'):
                load_context(root,legacy.artifact_id,'wrong-revision',fields['filename'])
            path.write_text('{}')
            with self.assertRaisesRegex(ValueError,'checksum mismatch'):
                load_context(root,legacy.artifact_id,fields['comment_introducing_revision'],fields['filename'])

    def test_missing_context_is_explicit(self):
        with tempfile.TemporaryDirectory() as directory:
            enriched=next(iter(MLSATD23ShadesAdapter(context_dir=Path(directory)).iter_artifacts()))
            self.assertEqual(enriched.raw_fields['source_context_status'],'unavailable')
            self.assertIn('could not be uniquely matched',enriched.content)

    def test_repeated_comments_expose_all_candidates_without_selecting_one(self):
        source='# TODO fix\nfirst()\n# TODO fix\nsecond()'
        self.assertEqual(preparation.comment_spans(source,'TODO fix'),[(0,1),(2,3)])
        self.assertIsNone(preparation.extract_excerpt(source,'TODO fix'))
        legacy=next(iter(MLSATD23ShadesAdapter().iter_artifacts()))
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            payload={'artifact_id':legacy.artifact_id,
                     'revision_url':legacy.raw_fields['comment_introducing_revision'],
                     'filename':legacy.raw_fields['filename'],'commit':'a'*40,
                     'source_url':'https://github.com/o/r/commit/'+'a'*40,
                     'status':'ambiguous','ambiguity_note':'Two exact matches; no unique location.',
                     'candidates':[{'line_start':1,'line_end':2,'excerpt':'# TODO fix\nfirst()'},
                                   {'line_start':3,'line_end':4,'excerpt':'# TODO fix\nsecond()'}]}
            path=root/'case.json';path.write_text(json.dumps(payload))
            (root/'manifest.json').write_text(json.dumps({'artifacts':{legacy.artifact_id:{'file':'case.json','sha256':hashlib.sha256(path.read_bytes()).hexdigest()}}}))
            enriched=next(iter(MLSATD23ShadesAdapter(context_dir=root).iter_artifacts()))
        self.assertEqual(enriched.raw_fields['source_context_status'],'ambiguous')
        self.assertNotIn('source_context_line_start',enriched.raw_fields)
        self.assertIn('first()',enriched.content)
        self.assertIn('second()',enriched.content)
        self.assertIn('no unique location',enriched.content)
        self.assertEqual({r.field for r in enriched.source_refs if 'candidate' in r.field},
                         {'source_context_candidate_1','source_context_candidate_2'})
