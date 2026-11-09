from __future__ import annotations

import unittest

from adapters.base import ArtifactRecord
from coda.splitting import deterministic_held_out_split, split_group_id


class TestHeldOutSplitting(unittest.TestCase):
    def test_split_is_deterministic_and_keeps_visible_groups_whole(self) -> None:
        artifacts = [
            ArtifactRecord(
                artifact_id=f"a{index}",
                content=f"case {index}",
                raw_fields={"repo_name": f"repo-{index // 2}"},
                metadata={"repo_name": f"repo-{index // 2}"},
            )
            for index in range(20)
        ]
        first = deterministic_held_out_split(
            artifacts,
            dataset_name="dockerfile_flakiness",
            split_family="dockerfile_flakiness",
            held_out_target=4,
        )
        second = deterministic_held_out_split(
            list(reversed(artifacts)),
            dataset_name="dockerfile_flakiness",
            split_family="dockerfile_flakiness",
            held_out_target=4,
        )

        coding, held_out, group_ids = first
        self.assertEqual(
            {item.artifact_id for item in held_out},
            {item.artifact_id for item in second[1]},
        )
        self.assertEqual(len(held_out), 4)
        self.assertEqual(len(coding), 16)
        held_groups = {group_ids[item.artifact_id] for item in held_out}
        coding_groups = {group_ids[item.artifact_id] for item in coding}
        self.assertFalse(held_groups & coding_groups)
        for artifact in artifacts:
            self.assertEqual(
                split_group_id("dockerfile_flakiness", artifact),
                group_ids[artifact.artifact_id],
            )

    def test_split_rejects_target_that_leaves_too_few_coding_cases(self) -> None:
        artifacts = [
            ArtifactRecord(str(index), str(index), {})
            for index in range(4)
        ]
        with self.assertRaises(ValueError):
            deterministic_held_out_split(
                artifacts,
                dataset_name="synthetic",
                split_family="synthetic",
                held_out_target=3,
            )

    def test_fairness_group_id_normalizes_record_views_to_base_issue(self) -> None:
        first = ArtifactRecord(
            artifact_id="comment-1",
            content="first",
            raw_fields={"base_issue_url": "https://example.test/issues/1"},
        )
        second = ArtifactRecord(
            artifact_id="comment-2",
            content="second",
            raw_fields={},
            metadata={"base_issue_url": "https://example.test/issues/1"},
        )
        self.assertEqual(
            split_group_id("fairness_api_issue_topic", first),
            split_group_id("fairness_api_issue_topic", second),
        )


if __name__ == "__main__":
    unittest.main()
