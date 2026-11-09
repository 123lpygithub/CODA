from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from adapters.github_issue_snapshot import load_snapshot, normalize_snapshot, render_discussion
from adapters.personal_data_protection_github import PersonalDataProtectionGitHubAdapter
from scripts import prepare_privacy_issue_discussions as preparation


URL = "https://github.com/owner/repo/issues/1"
API_URL = "https://api.github.com/repos/owner/repo/issues/1"


def issue_response(count: int = 2) -> dict:
    return {
        "fetched_at": "2026-10-18T00:00:00+00:00",
        "data": {
            "number": 1, "url": API_URL, "html_url": URL,
            "title": "Snapshot title", "body": "Complete original **body**",
            "user": {"id": 10, "login": "not-sent-to-agents"},
            "created_at": "2021-01-01T00:00:00Z", "updated_at": "2022-01-01T00:00:00Z",
            "state": "closed", "comments": count, "comments_url": API_URL + "/comments",
        },
    }


def comment_response(number: int, next_url: str | None = None) -> dict:
    return {
        "fetched_at": "2026-10-18T00:00:01+00:00", "next_url": next_url,
        "data": [{
            "id": number, "html_url": URL + f"#issuecomment-{number}",
            "created_at": f"2021-02-{number:02}T00:00:00Z", "updated_at": None,
            "user": {"id": 20}, "body": f"Exact comment {number}",
        }],
    }


class TestPrivacyIssueSnapshot(unittest.TestCase):
    def test_pagination_order_deduplication_and_participant_pseudonyms(self) -> None:
        snapshot = normalize_snapshot("privacy-issue-1", issue_response(), [comment_response(2), comment_response(1), comment_response(1)], comments_complete=True)
        self.assertEqual(snapshot["evidence_status"], "complete")
        self.assertEqual([item["id"] for item in snapshot["comments"]], [1, 2])
        self.assertEqual(snapshot["comments"][0]["author"], "Participant 2")
        self.assertNotIn("not-sent-to-agents", json.dumps(snapshot))
        self.assertIn("Exact comment 1", render_discussion(snapshot))

    def test_missing_comments_are_never_reported_as_complete(self) -> None:
        snapshot = normalize_snapshot("privacy-issue-1", issue_response(), [comment_response(1)], comments_complete=True)
        self.assertEqual(snapshot["evidence_status"], "partial")
        self.assertFalse(snapshot["comments_complete"])
        empty = normalize_snapshot("privacy-issue-1", issue_response(), [], comments_complete=False)
        self.assertIn("not been fully retrieved", render_discussion(empty))
        no_comments = normalize_snapshot("privacy-issue-1", issue_response(0), [], comments_complete=True)
        self.assertEqual(no_comments["evidence_status"], "complete")
        self.assertIn("No issue comments", render_discussion(no_comments))

    def test_checksum_and_identity_mismatches_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            snapshot = normalize_snapshot("privacy-issue-1", issue_response(0), [], comments_complete=True)
            entry = {}
            preparation.save_snapshot(root, entry, snapshot)
            preparation.write_json(root / "manifest.json", {"artifacts": {"privacy-issue-1": entry}})
            self.assertEqual(load_snapshot(root, "privacy-issue-1", URL), snapshot)
            with self.assertRaisesRegex(ValueError, "identity mismatch"):
                load_snapshot(root, "privacy-issue-1", URL + "0")
            (root / entry["file"]).write_text("{}", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "checksum mismatch"):
                load_snapshot(root, "privacy-issue-1", URL)

    def test_adapter_exposes_body_and_comment_sources_without_reference_labels(self) -> None:
        adapter = PersonalDataProtectionGitHubAdapter()
        row = {"index": "1", "url": API_URL, "html_url": URL, "project": "owner/repo", "title": "Released title", "status": "open", "privacy_issue_rater_2": "hidden-label"}
        snapshot = normalize_snapshot("privacy-issue-1", issue_response(), [comment_response(1), comment_response(2)], comments_complete=True)
        with patch.object(adapter, "_load_rows", return_value=[row]), patch("adapters.personal_data_protection_github.load_snapshot", return_value=snapshot):
            artifact = next(iter(adapter.iter_artifacts()))
        self.assertIn("Complete original **body**", artifact.content)
        self.assertIn("Exact comment 2", artifact.content)
        self.assertEqual(artifact.raw_fields["title"], "Released title")
        self.assertEqual(artifact.raw_fields["snapshot_title"], "Snapshot title")
        self.assertNotIn("hidden-label", artifact.content)
        self.assertNotIn("privacy_issue_rater_2", artifact.raw_fields)
        self.assertTrue(any(ref.field == "comment_2" and ref.value.endswith("#issuecomment-2") for ref in artifact.source_refs))

    def test_preparation_follows_pages_and_resumes_completed_cases(self) -> None:
        row = {"index": "1", "url": API_URL, "html_url": URL, "issue_number": "1"}
        next_url = API_URL + "/comments?per_page=100&page=2"
        with tempfile.TemporaryDirectory() as temporary:
            args = argparse.Namespace(output=Path(temporary), limit=None, timeout=1, attempts=1, wait_for_rate_limit=False)
            with patch.object(PersonalDataProtectionGitHubAdapter, "_load_rows", return_value=[row]), patch.object(preparation, "fetch", side_effect=[issue_response(), comment_response(1, next_url), comment_response(2)]) as fetch:
                self.assertEqual(preparation.prepare(args), 0)
                self.assertEqual(fetch.call_count, 3)
                self.assertEqual(fetch.call_args_list[-1].args[0], next_url)
                fetch.reset_mock()
                self.assertEqual(preparation.prepare(args), 0)
                fetch.assert_not_called()

    def test_rate_limit_preserves_body_and_completed_comment_pages(self) -> None:
        row = {"index": "1", "url": API_URL, "html_url": URL, "issue_number": "1"}
        next_url = API_URL + "/comments?per_page=100&page=2"
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            args = argparse.Namespace(output=root, limit=None, timeout=1, attempts=1, wait_for_rate_limit=False)
            with patch.object(PersonalDataProtectionGitHubAdapter, "_load_rows", return_value=[row]), patch.object(preparation, "fetch", side_effect=[issue_response(), comment_response(1, next_url), preparation.RateLimited(123)]):
                self.assertEqual(preparation.prepare(args), 2)
            snapshot = load_snapshot(root, "privacy-issue-1", URL)
            self.assertEqual(snapshot["body"], "Complete original **body**")
            self.assertEqual(snapshot["retrieved_comment_count"], 1)
            self.assertEqual(snapshot["evidence_status"], "partial")

    def test_cached_response_and_offline_mode_do_not_make_requests(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            cache = Path(temporary)
            path = cache / (hashlib.sha256(API_URL.encode()).hexdigest() + ".json")
            preparation.write_json(path, issue_response())
            with patch.object(preparation, "urlopen") as network:
                self.assertEqual(preparation.fetch(API_URL, cache, 1, 1), issue_response())
                with self.assertRaises(preparation.CacheMiss):
                    preparation.fetch(API_URL + "/comments", cache, 1, 1, offline=True)
                network.assert_not_called()

    def test_github_repository_redirect_preserves_original_case_identity(self) -> None:
        row = {"index": "1", "url": API_URL, "html_url": URL, "issue_number": "1"}
        response = issue_response(0)
        response.update({"requested_url": API_URL, "final_url": "https://api.github.com/repositories/123/issues/1"})
        response["data"].update({"url": "https://api.github.com/repos/new-owner/repo/issues/1", "html_url": "https://github.com/new-owner/repo/issues/1"})
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            args = argparse.Namespace(output=root, limit=None, timeout=1, attempts=1, wait_for_rate_limit=False)
            with patch.object(PersonalDataProtectionGitHubAdapter, "_load_rows", return_value=[row]), patch.object(preparation, "fetch", return_value=response):
                self.assertEqual(preparation.prepare(args), 0)
            snapshot = load_snapshot(root, "privacy-issue-1", URL)
            self.assertEqual(snapshot["source_issue_url"], URL)
            self.assertEqual(snapshot["issue_url"], "https://github.com/new-owner/repo/issues/1")


if __name__ == "__main__":
    unittest.main()
