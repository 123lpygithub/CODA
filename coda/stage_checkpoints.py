"""Atomic per-stage checkpoints for resumable artifact preparation."""

from __future__ import annotations

import json
import types
from dataclasses import asdict, fields, is_dataclass
from pathlib import Path
from typing import Any, Literal, Union, get_args, get_origin, get_type_hints


def _decode(value: Any, expected_type: Any) -> Any:
    if expected_type is Any:
        return value
    origin = get_origin(expected_type)
    args = get_args(expected_type)
    if origin in {Union, types.UnionType}:
        if value is None and type(None) in args:
            return None
        for candidate in args:
            if candidate is type(None):
                continue
            try:
                return _decode(value, candidate)
            except (TypeError, ValueError, KeyError):
                continue
        raise TypeError(f"Cannot decode value as {expected_type!r}.")
    if origin is list:
        return [_decode(item, args[0]) for item in value]
    if origin is tuple:
        return tuple(_decode(item, args[0]) for item in value)
    if origin is dict:
        return {
            _decode(key, args[0]): _decode(item, args[1])
            for key, item in value.items()
        }
    if origin is Literal:
        if value not in args:
            raise ValueError(f"Value {value!r} is outside {args!r}.")
        return value
    if is_dataclass(expected_type):
        if not isinstance(value, dict):
            raise TypeError(f"Expected an object for {expected_type.__name__}.")
        hints = get_type_hints(expected_type)
        names = {item.name for item in fields(expected_type)}
        return expected_type(
            **{
                name: _decode(item, hints.get(name, Any))
                for name, item in value.items()
                if name in names
            }
        )
    if expected_type in {str, int, float, bool}:
        return expected_type(value)
    return value


class StageCheckpointStore:
    """Store completed Agent outputs under one immutable preparation key."""

    def __init__(self, path: str | Path, *, cache_key: str) -> None:
        self.path = Path(path)
        self.cache_key = cache_key

    def get(self, stage: str, expected_type: Any) -> Any | None:
        payload = self._read()
        if payload.get("cache_key") != self.cache_key:
            return None
        stages = payload.get("stages", {})
        if not isinstance(stages, dict) or stage not in stages:
            return None
        return _decode(stages[stage], expected_type)

    def put(self, stage: str, value: Any) -> None:
        payload = self._read()
        if payload.get("cache_key") != self.cache_key:
            payload = {
                "format": "coda-stage-checkpoint",
                "format_version": 1,
                "cache_key": self.cache_key,
                "stages": {},
            }
        stages = payload.setdefault("stages", {})
        if not isinstance(stages, dict):
            stages = {}
            payload["stages"] = stages
        stages[stage] = asdict(value) if is_dataclass(value) else [
            asdict(item) if is_dataclass(item) else item for item in value
        ] if isinstance(value, list) else value
        self._write(payload)

    def clear(self) -> None:
        self.path.unlink(missing_ok=True)

    def _read(self) -> dict[str, Any]:
        if not self.path.exists():
            return {}
        try:
            payload = json.loads(self.path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return {}
        return payload if isinstance(payload, dict) else {}

    def _write(self, payload: dict[str, Any]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary = self.path.with_suffix(self.path.suffix + ".tmp")
        temporary.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        temporary.replace(self.path)
