"""Read fixed source excerpts, without fetching during analysis."""
import hashlib
import json
from pathlib import Path


def load_context(root: Path, artifact_id: str, revision_url: str, filename: str) -> dict | None:
    manifest_path = root / "manifest.json"
    if not manifest_path.exists():
        return None
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    entry = manifest.get("artifacts", {}).get(artifact_id, {})
    if not entry.get("file"):
        return None
    path = root / entry["file"]
    if not path.resolve().is_relative_to(root.resolve()):
        raise ValueError("SATD context path escapes the evidence directory.")
    if hashlib.sha256(path.read_bytes()).hexdigest() != entry.get("sha256"):
        raise ValueError(f"SATD context checksum mismatch for {artifact_id}.")
    payload = json.loads(path.read_text(encoding="utf-8"))
    if (payload.get("artifact_id"), payload.get("revision_url"), payload.get("filename")) != (artifact_id, revision_url, filename):
        raise ValueError(f"SATD context identity mismatch for {artifact_id}.")
    return payload
