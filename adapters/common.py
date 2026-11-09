from __future__ import annotations

import csv
import gzip
import json
import re
from pathlib import Path
from typing import Any, Iterable, Mapping

from adapters.base import ReferenceLabel, ReferenceLabelMode, SourceKind, SourceRef

_PLACEHOLDER_PATTERN = re.compile(r"\{([^{}]+)\}")


def load_json(path: Path) -> Any:
    """Load a UTF-8 JSON file."""

    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_json_gz(path: Path) -> Any:
    """Load a UTF-8 JSON.GZ file."""

    with gzip.open(path, "rt", encoding="utf-8") as handle:
        return json.load(handle)


def load_csv_rows(path: Path, *, delimiter: str = ",") -> list[dict[str, str]]:
    """Load a delimited text file as a list of dict rows."""

    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle, delimiter=delimiter))


def iter_csv_rows(path: Path, *, delimiter: str = ",") -> Iterable[dict[str, str]]:
    """Yield delimited rows one by one."""

    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle, delimiter=delimiter)
        for row in reader:
            yield dict(row)


def render_content_template(template: str, values: Mapping[str, Any]) -> str:
    """Render templates whose placeholders may contain spaces or '/'."""

    def replace(match: re.Match[str]) -> str:
        key = match.group(1)
        value = values.get(key, "")
        if value is None:
            return ""
        return str(value)

    return _PLACEHOLDER_PATTERN.sub(replace, template).strip()


def split_label_path(label_text: str) -> list[str]:
    """Split taxonomy path text such as 'A -> B -> C'."""

    return [part.strip() for part in label_text.split("->") if part.strip()]


def build_reference_label(category: str | list[str]) -> ReferenceLabel:
    """Convert raw category field into the unified hidden label object."""

    if isinstance(category, list):
        label_paths = [split_label_path(label_text) for label_text in category]
        return ReferenceLabel(
            label_text=" | ".join(category),
            label_mode="multi_label",
            label_paths=label_paths,
        )

    return ReferenceLabel(
        label_text=category,
        label_mode="single_label",
        label_path=split_label_path(category),
    )


def build_dimension_reference_label(
    dimensions: Mapping[str, Any],
) -> ReferenceLabel:
    """Represent several independent reference-coding dimensions as one label.

    CODA's reference contract stores one annotation per artifact. Some published
    studies code each artifact along several independent dimensions, so each
    non-empty dimension becomes a separate path without exposing it to agents.
    """

    paths: list[list[str]] = []
    rendered: list[str] = []
    for dimension, value in dimensions.items():
        values = value if isinstance(value, list) else [value]
        for item in values:
            text = str(item or "").strip()
            if not text:
                continue
            rendered.append(f"{dimension}: {text}")
            paths.append([dimension, text])
    return ReferenceLabel(
        label_text=" | ".join(rendered),
        label_mode="multi_label",
        label_paths=paths,
    )


def infer_reference_label_mode(categories: Iterable[str | list[str]]) -> ReferenceLabelMode:
    """Infer whether a task is single-label or multi-label from raw categories."""

    for category in categories:
        if isinstance(category, list):
            return "multi_label"
    return "single_label"


def build_source_ref(
    *,
    kind: SourceKind,
    value: str | None,
    ref_id: str | None = None,
    field: str | None = None,
) -> SourceRef | None:
    """Create a source reference only when the source value exists."""

    if not value:
        return None
    return SourceRef(kind=kind, value=value, ref_id=ref_id, field=field)


def infer_source_kind_from_url(url: str | None, default: SourceKind = "external_url") -> SourceKind:
    """Infer a coarse source kind from a URL."""

    if not url:
        return default
    if "/commit/" in url:
        return "commit"
    if "/pull/" in url:
        return "pull_request"
    if "/issues/" in url:
        return "issue"
    return default
