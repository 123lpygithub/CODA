"""Reproducibility manifest for one CODA run."""

from __future__ import annotations

import hashlib
import json
import platform
import subprocess
import sys
from dataclasses import asdict
from datetime import datetime, timezone
from importlib import metadata as package_metadata
from pathlib import Path
from typing import Any, Iterable

from adapters.base import ArtifactRecord
from coda.bootstrap import BootstrapConfig
from coda.state import RunState


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _path_checksum(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"path": str(path), "kind": "unavailable", "sha256": None}
    if path.is_file():
        return {"path": str(path), "kind": "file", "sha256": _sha256(path)}
    files = sorted(item for item in path.rglob("*") if item.is_file())
    digest = hashlib.sha256()
    for item in files:
        digest.update(str(item.relative_to(path)).encode("utf-8"))
        digest.update(_sha256(item).encode("ascii"))
    return {
        "path": str(path),
        "kind": "directory",
        "file_count": len(files),
        "sha256": digest.hexdigest(),
    }


def _git_state(project_root: Path) -> dict[str, Any]:
    try:
        commit = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=project_root,
            check=True,
            capture_output=True,
            text=True,
            timeout=5,
        ).stdout.strip()
        status = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=project_root,
            check=True,
            capture_output=True,
            text=True,
            timeout=5,
        ).stdout
        return {"commit": commit, "dirty": bool(status.strip())}
    except (OSError, subprocess.SubprocessError):
        return {"commit": "unavailable", "dirty": "unavailable"}


def _dependency_versions(names: Iterable[str]) -> dict[str, str]:
    versions: dict[str, str] = {}
    for name in names:
        try:
            versions[name] = package_metadata.version(name)
        except package_metadata.PackageNotFoundError:
            versions[name] = "unavailable"
    return versions


def build_run_manifest(
    run_state: RunState,
    artifacts: list[ArtifactRecord],
    *,
    held_out_artifacts: list[ArtifactRecord] | None = None,
    project_root: str | Path = ".",
    bootstrap_config: BootstrapConfig | None = None,
    model_configurations: dict[str, Any] | None = None,
) -> dict[str, Any]:
    from coda.study import evidence_sha256
    root = Path(project_root).resolve()
    selection_rows = [
        {
            "artifact_id": artifact.artifact_id,
            "evidence_sha256": evidence_sha256(artifact),
            "content_sha256": hashlib.sha256(
                artifact.content.encode("utf-8")
            ).hexdigest(),
        }
        for artifact in artifacts
    ]
    coding_selection_hash = hashlib.sha256(
        json.dumps(selection_rows, sort_keys=True).encode("utf-8")
    ).hexdigest()
    held_out_rows = [
        {
            "artifact_id": artifact.artifact_id,
            "evidence_sha256": evidence_sha256(artifact),
            "content_sha256": hashlib.sha256(
                artifact.content.encode("utf-8")
            ).hexdigest(),
        }
        for artifact in (held_out_artifacts or [])
    ]
    selection_hash = hashlib.sha256(
        json.dumps([*selection_rows, *held_out_rows], sort_keys=True).encode("utf-8")
    ).hexdigest()
    held_out_hash = hashlib.sha256(
        json.dumps(held_out_rows, sort_keys=True).encode("utf-8")
    ).hexdigest()
    lock_files = []
    for relative_path in ("requirements.txt", "frontend/package-lock.json"):
        path = root / relative_path
        lock_files.append(
            {
                "path": relative_path,
                "sha256": _sha256(path) if path.exists() else None,
            }
        )
    return {
        "format": "coda-run-manifest",
        "format_version": 1,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "run_id": run_state.run_id,
        "dataset_name": run_state.dataset_metadata.dataset_name,
        "study_execution": run_state.metadata.get("study_execution", {}),
        "environment": {
            "python": sys.version,
            "platform": platform.platform(),
            "git": _git_state(root),
            "dependencies": _dependency_versions(
                ["fastapi", "openai", "pydantic", "uvicorn"]
            ),
            "lock_files": lock_files,
        },
        "data": {
            "source_checksums": [
                _path_checksum(Path(path))
                for path in run_state.dataset_metadata.source_paths
            ],
            "selected_artifact_count": len(artifacts) + len(held_out_rows),
            "coding_pool_artifact_count": len(artifacts),
            "artifact_selection_sha256": selection_hash,
            "coding_pool_selection_sha256": coding_selection_hash,
            "artifacts": selection_rows,
            "coding_pool_artifacts": selection_rows,
            "held_out_artifact_count": len(held_out_rows),
            "held_out_selection_sha256": held_out_hash,
            "held_out_artifacts": held_out_rows,
            "dataset_target_record_count": run_state.dataset_metadata.target_record_count,
            "selection_rule": (
                "The selected coding pool is the exact run input; artifact_limit "
                "uses the deterministic selection order recorded above."
            ),
            "reference_data_hidden": True,
        },
        "protocol": {
            "research_question": asdict(run_state.research_question),
            "analysis_protocol": asdict(run_state.analysis_protocol),
            "review_policy": asdict(run_state.review_policy),
            "bootstrap": asdict(bootstrap_config or BootstrapConfig.from_env()),
            "experiment": dict(run_state.metadata.get("experiment_protocol", {})),
            "study_materials": run_state.metadata.get("study_materials"),
            "iterative_batches": run_state.metadata.get("iterative_batch_protocol", {"batch_size": 1}),
        },
        "models": dict(model_configurations or {}),
    }


def write_run_manifest(path: str | Path, manifest: dict[str, Any]) -> Path:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_suffix(destination.suffix + ".tmp")
    temporary.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    temporary.replace(destination)
    return destination
