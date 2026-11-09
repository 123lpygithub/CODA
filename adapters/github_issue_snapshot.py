"""Offline, evidence-preserving GitHub issue snapshots (no reference labels)."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalize_snapshot(
    artifact_id: str, issue_response: dict[str, Any],
    comment_responses: list[dict[str, Any]], *, comments_complete: bool,
) -> dict[str, Any]:
    issue = issue_response["data"]
    participants: dict[str, str] = {}

    def participant(user: dict[str, Any] | None) -> str:
        key = str((user or {}).get("id", "deleted"))
        return participants.setdefault(key, f"Participant {len(participants) + 1}")

    author = participant(issue.get("user"))
    comments = {}
    for response in comment_responses:
        for comment in response["data"]:
            comments[comment["id"]] = {
                "id": comment["id"], "url": comment["html_url"],
                "created_at": comment["created_at"],
                "updated_at": comment.get("updated_at"),
                "author": participant(comment.get("user")),
                "body": comment.get("body") or "",
            }
    ordered = sorted(comments.values(), key=lambda item: (item["created_at"], item["id"]))
    expected = issue["comments"]
    complete = comments_complete and len(ordered) == expected
    return {
        "format": "coda-github-issue-snapshot", "format_version": 1,
        "artifact_id": artifact_id, "issue_url": issue["html_url"],
        "source_issue_url": issue_response.get("requested_url", issue["url"]).replace("https://api.github.com/repos/", "https://github.com/"),
        "api_url": issue["url"], "title": issue["title"],
        "body": issue.get("body") or "", "author": author,
        "created_at": issue["created_at"], "updated_at": issue["updated_at"],
        "state": issue["state"], "closed_at": issue.get("closed_at"),
        "issue_fetched_at": issue_response["fetched_at"],
        "comments_fetched_at": [page["fetched_at"] for page in comment_responses],
        "expected_comment_count": expected, "retrieved_comment_count": len(ordered),
        "comments_complete": complete, "comments": ordered,
        "evidence_status": "complete" if complete else "partial",
        "scope": "Current retrievable issue body and issue comments; not the original study's historical snapshot. Linked pages and attachments are not fetched.",
    }


def load_snapshot(root: Path, artifact_id: str, issue_url: str) -> dict[str, Any] | None:
    manifest_path = root / "manifest.json"
    if not manifest_path.exists():
        return None
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    entry = manifest.get("artifacts", {}).get(artifact_id, {})
    if entry.get("status") == "unavailable" or not entry.get("file"):
        return None
    path = root / entry["file"]
    if not path.resolve().is_relative_to(root.resolve()):
        raise ValueError("Snapshot path escapes the evidence directory.")
    if sha256_file(path) != entry.get("sha256"):
        raise ValueError(f"Evidence checksum mismatch for {artifact_id}.")
    snapshot = json.loads(path.read_text(encoding="utf-8"))
    if snapshot.get("artifact_id") != artifact_id or snapshot.get("source_issue_url", snapshot.get("issue_url")) != issue_url:
        raise ValueError(f"Evidence identity mismatch for {artifact_id}.")
    return snapshot


def render_discussion(snapshot: dict[str, Any]) -> str:
    comments = snapshot["comments"]
    if not comments:
        return "[No issue comments at retrieval time.]" if snapshot["comments_complete"] else "[Issue comments have not been fully retrieved.]"
    return "\n\n".join(
        f"Comment {index} (source ID {comment['id']}) | {comment['author']} | "
        f"created {comment['created_at']} | updated {comment['updated_at']}\n"
        f"Source: {comment['url']}\n{comment['body'] or '[Empty comment body.]'}"
        for index, comment in enumerate(comments, 1)
    )


def load_archived_supplement(root: Path, artifact_id: str, issue_url: str) -> dict | None:
    path = root / 'manifest.json'
    if not path.exists():
        return None
    entry = json.loads(path.read_text()).get('artifacts', {}).get(artifact_id, {}).get('event_archive', {})
    if not entry.get('file'):
        return None
    target = root / entry['file']
    if not target.resolve().is_relative_to(root.resolve()):
        raise ValueError('Archived issue path escapes its evidence directory.')
    if sha256_file(target) != entry.get('sha256'):
        raise ValueError(f'Archived issue checksum mismatch for {artifact_id}.')
    snapshot = json.loads(target.read_text())
    if snapshot.get('artifact_id') != artifact_id or snapshot.get('source_issue_url') != issue_url:
        raise ValueError(f'Archived issue identity mismatch for {artifact_id}.')
    return snapshot
