"""Atomic, input-fingerprinted checkpoints for resumable initialization."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path
from typing import Any

from coda.stage_checkpoints import StageCheckpointStore


class BootstrapCheckpointStore:
    """Persist each initialization unit independently under one cache key."""

    def __init__(self, root: str | Path, *, cache_key: str) -> None:
        self.root = Path(root)
        self.cache_key = cache_key

    def get(self, stage: str, expected_type: Any) -> Any | None:
        return self._stage_store(stage).get("result", expected_type)

    def put(self, stage: str, value: Any) -> None:
        self._stage_store(stage).put("result", value)

    def _stage_store(self, stage: str) -> StageCheckpointStore:
        normalized = re.sub(r"[^A-Za-z0-9._-]+", "-", stage).strip("-") or "stage"
        digest = hashlib.sha256(stage.encode("utf-8")).hexdigest()[:12]
        path = self.root / f"{normalized[:96]}-{digest}.json"
        return StageCheckpointStore(path, cache_key=self.cache_key)
