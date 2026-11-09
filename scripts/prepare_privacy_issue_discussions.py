"""Fetch resumable public issue evidence without exposing study annotations."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import time
from datetime import datetime, timezone
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from adapters.github_issue_snapshot import normalize_snapshot, sha256_file
from adapters.personal_data_protection_github import PersonalDataProtectionGitHubAdapter

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "dataset/personal_data_protection_github/source/github_snapshot"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


class RateLimited(Exception):
    def __init__(self, reset: float):
        self.reset = reset


class CacheMiss(Exception):
    pass


def fetch(url: str, cache: Path, timeout: float, attempts: int, *, offline: bool = False) -> dict:
    if urlparse(url).hostname != "api.github.com" or urlparse(url).scheme != "https":
        raise ValueError("Only HTTPS api.github.com evidence requests are supported.")
    path = cache / (hashlib.sha256(url.encode()).hexdigest() + ".json")
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    if offline:
        raise CacheMiss(url)
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "CODA-research-evidence", "X-GitHub-Api-Version": "2022-11-28"}
    token = os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    for attempt in range(attempts):
        try:
            with urlopen(Request(url, headers=headers), timeout=timeout) as response:
                links = response.headers.get("Link", "")
                match = re.search(r'<([^>]+)>;\s*rel="next"', links)
                payload = {
                    "requested_url": url, "final_url": response.url,
                    "fetched_at": utc_now(), "etag": response.headers.get("ETag"),
                    "last_modified": response.headers.get("Last-Modified"),
                    "next_url": match.group(1) if match else None,
                    "data": json.load(response),
                }
            write_json(path, payload)
            return payload
        except HTTPError as exc:
            if exc.code in (403, 429) and (exc.headers.get("X-RateLimit-Remaining") == "0" or exc.headers.get("Retry-After") or exc.code == 429):
                reset = float(exc.headers.get("X-RateLimit-Reset", time.time() + 60))
                reset = max(reset, time.time() + float(exc.headers.get("Retry-After", "5")))
                raise RateLimited(reset + 2) from exc
            if exc.code < 500 or attempt + 1 == attempts:
                raise
        except (URLError, TimeoutError, OSError):
            if attempt + 1 == attempts:
                raise
        time.sleep(min(2 ** attempt, 10))
    raise RuntimeError("No request attempts configured.")


def update_manifest(root: Path, manifest: dict) -> None:
    entries = manifest["artifacts"].values()
    manifest["updated_at"] = utc_now()
    manifest["counts"] = {
        state: sum(entry["status"] == state for entry in entries)
        for state in ("complete", "partial", "unavailable", "pending")
    }
    write_json(root / "manifest.json", manifest)


def prepare(args: argparse.Namespace) -> int:
    rows = PersonalDataProtectionGitHubAdapter()._load_rows()
    root = args.output.resolve()
    csv_path = ROOT / "dataset/personal_data_protection_github/source/extracted/coded_issue_data.csv"
    source_hash = sha256_file(csv_path)
    path = root / "manifest.json"
    if path.exists():
        manifest = json.loads(path.read_text(encoding="utf-8"))
        if manifest.get("released_csv_sha256") != source_hash:
            raise ValueError("Released source changed; create a new snapshot directory.")
    else:
        manifest = {
            "format": "coda-privacy-evidence-manifest", "format_version": 1,
            "created_at": utc_now(), "released_csv_sha256": source_hash,
            "original_study_material": "652 privacy-related issues analyzed by the authors; the released CSV contains titles, metadata and separate annotations.",
            "supplemental_material": "GitHub REST issue bodies and all available issue comments collected during this snapshot; not historical reconstruction.",
            "artifacts": {
                f"privacy-issue-{row['index']}": {"issue_url": row["html_url"], "status": "pending"}
                for row in rows
            },
        }
    update_manifest(root, manifest)
    processed = 0
    for row in rows:
        artifact_id = f"privacy-issue-{row['index']}"
        entry = manifest["artifacts"][artifact_id]
        if entry["status"] == "complete":
            if sha256_file(root / entry["file"]) != entry["sha256"]:
                raise ValueError(f"Evidence checksum mismatch for {artifact_id}.")
            continue
        if args.limit is not None and processed >= args.limit:
            break
        while True:
            issue = None
            pages = []
            try:
                issue = fetch(row["url"], root / "raw", args.timeout, args.attempts, offline=getattr(args, "offline", False))
                issue_data = issue["data"]
                canonical_api = issue.get("final_url", row["url"])
                canonical_html = issue_data.get("url", "").replace("https://api.github.com/repos/", "https://github.com/")
                # GitHub redirects renamed repositories to numeric repository endpoints.
                numeric_target = bool(re.fullmatch(r"https://api\.github\.com/repositories/\d+/issues/" + str(issue_data.get("number")), canonical_api))
                if (not numeric_target and issue_data.get("url", "").lower() != canonical_api.lower()) or issue_data.get("html_url", "").lower() != canonical_html.lower():
                    issue = None
                    raise ValueError("Response identity does not match GitHub's canonical redirect target.")
                url = issue_data["comments_url"] + "?per_page=100&page=1" if issue_data["comments"] else None
                while url:
                    page = fetch(url, root / "raw", args.timeout, args.attempts, offline=getattr(args, "offline", False))
                    if not isinstance(page["data"], list):
                        raise ValueError("Comments response must be an array.")
                    pages.append(page)
                    url = page["next_url"]
                snapshot = normalize_snapshot(artifact_id, issue, pages, comments_complete=True)
                save_snapshot(root, entry, snapshot)
                entry.pop("error", None)
                break
            except CacheMiss:
                if issue:
                    save_snapshot(root, entry, normalize_snapshot(artifact_id, issue, pages, comments_complete=False))
                    entry["error"] = "Not all comment pages have been retrieved."
                break
            except RateLimited as exc:
                if issue:
                    save_snapshot(root, entry, normalize_snapshot(artifact_id, issue, pages, comments_complete=False))
                update_manifest(root, manifest)
                if not args.wait_for_rate_limit:
                    print("GitHub API rate limit reached. Cached evidence is saved; rerun to resume, or use --wait-for-rate-limit.", flush=True)
                    return 2
                print(f"GitHub rate limit; resume at {datetime.fromtimestamp(exc.reset, timezone.utc).isoformat()} (cached work retained).", flush=True)
                while time.time() < exc.reset:
                    time.sleep(min(30, max(0, exc.reset - time.time())))
            except (HTTPError, URLError, OSError, ValueError, KeyError) as exc:
                if issue:
                    save_snapshot(root, entry, normalize_snapshot(artifact_id, issue, pages, comments_complete=False))
                else:
                    entry["status"] = "unavailable"
                    entry.pop("file", None)
                    entry.pop("sha256", None)
                entry["error"] = f"{type(exc).__name__}: {exc}"
                entry["last_attempt_at"] = utc_now()
                break
        processed += 1
        update_manifest(root, manifest)
        print(f"{artifact_id}: {entry['status']} | {manifest['counts']}", flush=True)
    update_manifest(root, manifest)
    print(json.dumps(manifest["counts"]), flush=True)
    return 0 if manifest["counts"]["complete"] == len(rows) else 2


def save_snapshot(root: Path, entry: dict, snapshot: dict) -> None:
    relative = f"issues/{snapshot['artifact_id']}.json"
    path = root / relative
    write_json(path, snapshot)
    entry.update({
        "status": snapshot["evidence_status"], "file": relative,
        "sha256": sha256_file(path), "issue_fetched_at": snapshot["issue_fetched_at"],
        "retrieved_comment_count": snapshot["retrieved_comment_count"],
        "expected_comment_count": snapshot["expected_comment_count"],
    })


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--limit", type=int, help="Process at most this many unfinished issues.")
    parser.add_argument("--timeout", type=float, default=30)
    parser.add_argument("--attempts", type=int, default=5)
    parser.add_argument("--wait-for-rate-limit", action="store_true")
    parser.add_argument("--offline", action="store_true", help="Rebuild incomplete snapshots from cached responses only, without network requests.")
    args = parser.parse_args()
    if args.attempts < 1 or args.timeout <= 0 or (args.limit is not None and args.limit < 1):
        parser.error("attempts, timeout and limit must be positive")
    return prepare(args)


if __name__ == "__main__":
    raise SystemExit(main())
