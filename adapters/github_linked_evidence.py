"""Checksummed, offline linked development evidence for Privacy cases."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
from urllib.parse import urlsplit, urlunsplit


def discover_links(snapshot: dict) -> list[dict]:
    """One-hop explicit GitHub URLs, without guessing from #tokens in code."""
    origin = snapshot['issue_url'].split('#')[0]
    fields = [('body', snapshot['body'])] + [(f"comment_{c['id']}", c['body']) for c in snapshot['comments']]
    found = {}
    for field, text in fields:
        urls = re.findall(r'https://(?:github\.com|raw\.githubusercontent\.com)/[^\s<>\[\]()"\x27`]+', text)
        for url in urls:
            url = url.rstrip('.,;:!?~')
            parts = urlsplit(url)
            segments = parts.path.strip('/').split('/')
            if parts.hostname == 'raw.githubusercontent.com':
                kind = 'file' if len(segments) >= 4 else None
            else:
                kind = {'blob':'file', 'commit':'commit', 'pull':'pull_request', 'issues':'issue'}.get(segments[2] if len(segments) >= 4 else '')
            if not kind or url.split('#')[0] == origin:
                continue
            if kind in ('issue','pull_request') and not segments[3].isdigit():
                continue  # Creation forms and collection pages are not artifacts.
            canonical = urlunsplit((parts.scheme, parts.netloc, parts.path, '', parts.fragment))
            item = found.setdefault(canonical, {'url':canonical, 'kind':kind, 'cited_in':[]})
            if field not in item['cited_in']:
                item['cited_in'].append(field)
    return list(found.values())


def load_linked_evidence(root: Path, artifact_id: str, issue_url: str, snapshot: dict | None, *, manifest_name: str = 'manifest.json') -> dict | None:
    if manifest_name not in ('manifest.json', 'external_manifest.json'):
        raise ValueError('Unsupported linked evidence manifest.')
    manifest = root / manifest_name
    if not manifest.exists():
        return None
    entry = json.loads(manifest.read_text(encoding='utf-8')).get('artifacts', {}).get(artifact_id, {})
    if not entry.get('file'):
        return None
    path = root / entry['file']
    if not path.resolve().is_relative_to(root.resolve()):
        raise ValueError('Linked evidence path escapes its directory.')
    data = path.read_bytes()
    if hashlib.sha256(data).hexdigest() != entry.get('sha256'):
        raise ValueError(f'Linked evidence checksum mismatch for {artifact_id}.')
    payload = json.loads(data)
    if (payload.get('artifact_id'), payload.get('source_issue_url')) != (artifact_id, issue_url):
        raise ValueError(f'Linked evidence identity mismatch for {artifact_id}.')
    digest = snapshot_digest(snapshot)
    if payload.get('issue_snapshot_sha256') != digest:
        raise ValueError(f'Linked evidence was collected from a different issue snapshot for {artifact_id}; rerun collection.')
    return payload


def snapshot_digest(snapshot: dict | None) -> str:
    return hashlib.sha256(json.dumps(snapshot, sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode()).hexdigest()


def render_link(item: dict, max_chars: int = 24000) -> str:
    header = f"Source: {item['url']}\nKind: {item['kind']}; availability: {item['status']}"
    if item.get('fetched_at'):
        header += f"; retrieved: {item['fetched_at']}"
    if item.get('revision'):
        header += f"\nRevision/reference: {item['revision']}; immutable: {item.get('immutable_revision', False)}"
    if item.get('line_start'):
        header += f"\nSource lines: {item['line_start']}–{item['line_end']}"
    if item.get('metadata_status'):
        header += '\nMetadata: ' + item['metadata_status']
    if item.get('reason') and item.get('text'):
        header += '\nEvidence gap: ' + item['reason']
    text = item.get('text') or item.get('reason', 'Not retrieved.')
    if len(text) > max_chars:
        # Preserve the full document on disk. Clearly delimit the agent-visible
        # excerpt so an omitted patch hunk cannot be treated as inspected.
        end = text.rfind('\n', 0, max_chars)
        end = end if end > 0 else max_chars
        text = text[:end] + f'\n[Source excerpt ends here: {end}/{len(text)} characters shown. Full retrieved text is retained in the linked-evidence snapshot. Do not infer omitted changes or outcomes; request additional context if needed.]'
    return header + '\n' + text
