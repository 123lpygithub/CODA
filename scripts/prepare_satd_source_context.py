"""Retrieve source excerpts at comment-introducing commits; never use labels."""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import hashlib
from http.client import HTTPException
import json
from pathlib import Path
import re
import sys
import threading
from urllib.parse import quote
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from adapters.ml_satd_23_shades import MLSATD23ShadesAdapter


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix('.tmp')
    temporary.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    temporary.replace(path)


def canonical_comment(text: str) -> str:
    # The published CSV replaces commas with semicolons, escapes quotes and
    # slashes, and sometimes omits Python's leading comment marker. Normalize
    # these release transformations only; never use fuzzy/keyword similarity.
    text = re.sub(r'\\+(["/])', r'\1', text)
    text = text.replace('\\\\', '\\')
    text = text.replace('\\uFFFF', '').replace('\uffff', '')
    text = re.sub(r'^\s*(?:#\s*)+', '', text)
    return ' '.join(text.replace(',', ';').split())


def comment_spans(source: str, comment: str) -> list[tuple[int, int]]:
    """All whole-comment matches as zero-based, end-exclusive source spans."""
    lines = source.splitlines()
    # The release renders multiline comments with " || ". Require the whole
    # normalized comment to match, rather than matching a generic TODO token.
    pieces = [piece.strip() for piece in re.split(r'\s*\|\|\s*|\n', comment) if canonical_comment(piece)]
    indexed = [(i, canonical_comment(line)) for i, line in enumerate(lines) if canonical_comment(line)]
    normalized = [line for _, line in indexed]
    target = ' '.join(canonical_comment(piece) for piece in pieces)
    if not target:
        return []
    matches = []
    for index in range(len(indexed)):
        if target == ' '.join(normalized[index:index + len(pieces)]):
            matches.append((indexed[index][0], indexed[index + len(pieces) - 1][0] + 1))
    if not matches:
        # A comment can be embedded after a code statement on the same line.
        # Inline matching applies only to the comment token, not arbitrary code
        # or a string literal mentioning TODO.
        import io
        import tokenize
        try:
            matches = [(token.start[0] - 1, token.end[0])
                       for token in tokenize.generate_tokens(io.StringIO(source).readline)
                       if token.type == tokenize.COMMENT and len(pieces) == 1
                       and canonical_comment(token.string) == target]
        except (tokenize.TokenError, IndentationError, SyntaxError):
            matches = []
    return sorted(set(matches))


def extract_excerpt(source: str, comment: str, radius: int = 12) -> tuple[int, int, str] | None:
    lines = source.splitlines()
    matches = comment_spans(source, comment)
    if len(matches) != 1:
        return None
    start, end = matches[0]
    start, end = max(0, start - radius), min(len(lines), end + radius)
    return start + 1, end, '\n'.join(lines[start:end])


def collect(artifact, output: Path, timeout: float) -> tuple[str, dict]:
    fields = artifact.raw_fields
    revision = fields['comment_introducing_revision']
    filename = fields['filename']
    match = re.fullmatch(r'https://github.com/([^/]+/[^/]+)/commit/([0-9a-fA-F]{40})', revision)
    if not match or filename.startswith('/') or '..' in Path(filename).parts:
        return artifact.artifact_id, {'status':'unavailable', 'reason':'No supported fixed revision or file path.'}
    repo, commit = match.groups()
    url = f'https://raw.githubusercontent.com/{repo}/{commit}/{quote(filename, safe="/")}'
    cache = output / 'raw' / (hashlib.sha256(url.encode()).hexdigest() + '.json')
    try:
        if cache.exists():
            raw = json.loads(cache.read_text(encoding='utf-8'))
            if raw.get('url') != url or hashlib.sha256(raw['source'].encode('utf-8')).hexdigest() != raw.get('source_sha256'):
                raise ValueError('Cached source identity or checksum mismatch.')
        else:
            with urlopen(Request(url, headers={'User-Agent':'CODA-research-evidence'}), timeout=timeout) as response:
                data = response.read(5_000_001)
                if len(data) > 5_000_000:
                    raise ValueError('Source exceeds 5 MB collection limit.')
                raw = {'url':url, 'source':data.decode('utf-8'), 'fetched_at':datetime.now(timezone.utc).isoformat(),
                       'source_sha256':hashlib.sha256(data).hexdigest()}
            write_json(cache, raw)
        excerpt = extract_excerpt(raw['source'], fields['comment_text'])
        if excerpt is None:
            return artifact.artifact_id, {'status':'unmatched', 'reason':'Released comment has no unique exact normalized match at introducing revision.', 'source_url':url}
        start, end, text = excerpt
        payload = {'artifact_id':artifact.artifact_id, 'revision_url':revision, 'filename':filename,
                   'commit':commit, 'source_url':url, 'fetched_at':raw['fetched_at'],
                   'source_sha256':raw['source_sha256'], 'line_start':start, 'line_end':end, 'excerpt':text,
                   'match_policy':'unique-release-normalized-v2'}
        relative = f'excerpts/{artifact.artifact_id}.json'
        path = output / relative
        write_json(path,payload)
        return artifact.artifact_id, {'status':'available','file':relative,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
    except (OSError, HTTPException, ValueError, UnicodeError) as error:
        return artifact.artifact_id, {'status':'unavailable','reason':f'{type(error).__name__}: {error}', 'source_url':url}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--timeout', type=float, default=15)
    parser.add_argument('--workers', type=int, default=6)
    parser.add_argument('--max-network-failures', type=int, default=8, help='Stop this invocation after repeated transport failures; rerun to resume.')
    args = parser.parse_args()
    if args.timeout <= 0 or not 1 <= args.workers <= 8 or args.max_network_failures < 1:
        parser.error('timeout must be positive; workers must be 1–8')
    output=args.output.resolve()
    manifest_path=output/'manifest.json'
    csv_path=ROOT/'dataset/ml_satd_23_shades/source/sampled_label_dataset.csv'
    source_hash=hashlib.sha256(csv_path.read_bytes()).hexdigest()
    manifest=json.loads(manifest_path.read_text()) if manifest_path.exists() else {
        'format':'coda-satd-source-context','format_version':1,'released_csv_sha256':source_hash,
        'scope':'Up to 12 surrounding lines at the exact introducing commit; unique normalized comment match required.', 'artifacts':{}}
    if manifest['released_csv_sha256'] != source_hash:
        parser.error('Source sample changed; choose a new output directory.')
    # Cases sharing a file use one request and one cache write.
    groups={}
    for artifact in MLSATD23ShadesAdapter().iter_artifacts():
        if manifest['artifacts'].get(artifact.artifact_id,{}).get('status')=='available':
            from adapters.satd_context import load_context
            load_context(output,artifact.artifact_id,artifact.raw_fields['comment_introducing_revision'],artifact.raw_fields['filename'])
            continue
        fields=artifact.raw_fields
        groups.setdefault((fields['comment_introducing_revision'],fields['filename']),[]).append(artifact)
        manifest['artifacts'].setdefault(artifact.artifact_id, {'status':'pending'})
    manifest['matching_policy'] = 'Unique full comment after release-format normalization (comma/semicolon, escaped quotes/slashes, omitted leading # and blank lines); no fuzzy or keyword matching.'
    write_json(manifest_path, manifest)
    stop = threading.Event()
    def interrupt(signum, frame):
        stop.set()
    import signal
    signal.signal(signal.SIGINT, interrupt)
    signal.signal(signal.SIGTERM, interrupt)
    def collect_group(members):
        results=[]
        for artifact in members:
            if stop.is_set(): break
            results.append(collect(artifact,output,args.timeout))
        return results
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures=[executor.submit(collect_group,members) for members in groups.values()]
        network_failures=0
        for future in as_completed(futures):
            for artifact_id, entry in future.result():
                manifest['artifacts'][artifact_id]=entry
                reason=entry.get('reason','')
                if entry['status']=='unavailable' and any(token in reason for token in ['Timeout','timed out','URLError','Network is unreachable']):
                    network_failures+=1
            if network_failures >= args.max_network_failures:
                stop.set()
            manifest['counts']={status:sum(e['status']==status for e in manifest['artifacts'].values()) for status in ['available','unmatched','unavailable','pending']}
            write_json(manifest_path,manifest)
            print(json.dumps(manifest['counts']),flush=True)


if __name__=='__main__':
    main()
