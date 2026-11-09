from __future__ import annotations

import unittest

from adapters.ml_satd_23_shades import MLSATD23ShadesAdapter
from adapters.personal_data_protection_github import PersonalDataProtectionGitHubAdapter


class TestNewDatasetAdapters(unittest.TestCase):
    def test_23_shades_uses_public_sample_and_hides_labels(self) -> None:
        adapter = MLSATD23ShadesAdapter()
        metadata = adapter.load_dataset_metadata()
        artifacts = list(adapter.iter_artifacts())
        reference = adapter.load_reference_data()

        self.assertEqual(metadata.target_record_count, 856)
        self.assertEqual(len(artifacts), 856)
        self.assertEqual(len({item.artifact_id for item in artifacts}), 856)
        self.assertTrue(all(item.content.strip() for item in artifacts))
        self.assertTrue(all("Software TD Type" not in item.content for item in artifacts))
        self.assertTrue(all("ML TD Type" not in item.content for item in artifacts))
        self.assertTrue(all("Software TD Type" not in item.raw_fields for item in artifacts))
        self.assertEqual(len(reference.annotations), 856)
        self.assertEqual(
            {item.artifact_id for item in reference.annotations},
            {item.artifact_id for item in artifacts},
        )
        self.assertTrue(all(item.source_refs for item in artifacts))

    def test_privacy_dataset_selects_the_652_confirmed_issues(self) -> None:
        adapter = PersonalDataProtectionGitHubAdapter()
        metadata = adapter.load_dataset_metadata()
        artifacts = list(adapter.iter_artifacts())
        reference = adapter.load_reference_data()

        self.assertEqual(metadata.target_record_count, 652)
        self.assertEqual(len(artifacts), 652)
        self.assertEqual(len({item.artifact_id for item in artifacts}), 652)
        self.assertTrue(all(item.content.strip() for item in artifacts))
        self.assertTrue(all("privacy_issue_rater" not in item.content for item in artifacts))
        self.assertTrue(all("privacy_issue_rater" not in item.raw_fields for item in artifacts))
        self.assertTrue(all("is_privacy_related" not in item.raw_fields for item in artifacts))
        self.assertEqual(len(reference.annotations), 652)
        self.assertEqual(
            {item.artifact_id for item in reference.annotations},
            {item.artifact_id for item in artifacts},
        )
        self.assertTrue(all(item.source_refs for item in artifacts))


if __name__ == "__main__":
    unittest.main()
