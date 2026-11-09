from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Literal, Protocol

SourceKind = Literal[
    "issue",
    "pull_request",
    "commit",
    "patch",
    "discussion",
    "repository",
    "build_log",
    "dockerfile",
    "external_url",
    "other",
]

ReferenceLabelMode = Literal["single_label", "multi_label"]


@dataclass(frozen=True)
class TextLocator:
    """Locate evidence within a raw field by character offsets or line numbers."""

    start: int | None = None
    end: int | None = None
    line_start: int | None = None
    line_end: int | None = None


@dataclass(frozen=True)
class SourceRef:
    """Pointer back to the original source or a specific raw field."""

    kind: SourceKind
    value: str
    ref_id: str | None = None
    field: str | None = None
    locator: TextLocator | None = None


@dataclass(frozen=True)
class ArtifactRecord:
    """Agent-facing artifact used inside CODA.

    Reference labels and taxonomy must never be embedded here.
    """

    artifact_id: str
    content: str
    raw_fields: dict[str, Any]
    source_refs: list[SourceRef] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ReferenceLabel:
    """Hidden human label for one artifact.

    For single-label tasks, use ``label_path``.
    For multi-label tasks, use ``label_paths``.
    """

    label_text: str
    label_mode: ReferenceLabelMode
    label_path: list[str] | None = None
    label_paths: list[list[str]] | None = None


@dataclass(frozen=True)
class ReferenceAnnotation:
    """Hidden reference annotation for one artifact."""

    artifact_id: str
    observed_label: ReferenceLabel


@dataclass(frozen=True)
class ReferenceData:
    """Reference material used only outside the main coding flow."""

    annotations: list[ReferenceAnnotation] = field(default_factory=list)
    taxonomy: dict[str, Any] | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class DatasetMetadata:
    """Shared task-level metadata returned by every adapter."""

    dataset_name: str
    display_name: str
    task_family: str
    target_record_count: int
    bundled: bool
    research_question: str
    use_case: str
    data_description: str
    artifact_unit: str
    content_template: str
    source_paths: list[Path]
    reference_label_mode: ReferenceLabelMode
    notes: list[str] = field(default_factory=list)
    data_available: bool = True
    availability_message: str | None = None


class DatasetAdapter(Protocol):
    """Minimal interface every CODA dataset adapter must implement."""

    def load_dataset_metadata(self) -> DatasetMetadata:
        """Return task-level metadata needed by the runtime."""
        ...

    def iter_artifacts(self) -> Iterable[ArtifactRecord]:
        """Yield agent-facing artifacts only."""
        ...

    def load_reference_data(self) -> ReferenceData | None:
        """Return hidden labels and taxonomy for evaluation-only use."""
        ...
