from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable

from adapters.base import (
    ArtifactRecord,
    DatasetMetadata,
    ReferenceAnnotation,
    ReferenceData,
)
from adapters.common import (
    build_reference_label,
    build_source_ref,
    infer_source_kind_from_url,
    infer_reference_label_mode,
    load_json,
    render_content_template,
)

_REPO_ROOT = Path(__file__).resolve().parents[1]
_DATASET_NAME = "common_sense_violating_bug"
_DATASET_DIR = (
    _REPO_ROOT / "dataset" / _DATASET_NAME
)
_DATA_PATH = _DATASET_DIR / f"{_DATASET_NAME}.json"
_SETTINGS_PATH = _DATASET_DIR / f"{_DATASET_NAME}_settings.json"
_TAXONOMY_PATH = _DATASET_DIR / f"{_DATASET_NAME}_taxonomy.json"


class CommonSenseViolatingBugAdapter:
    """Adapter for the common-sense-violating bug task."""

    def load_dataset_metadata(self) -> DatasetMetadata:
        rows = self._load_rows()
        settings = self._load_settings()
        categories = [row["category"] for row in rows if "category" in row]
        return DatasetMetadata(
            dataset_name=_DATASET_NAME,
            display_name="Common Sense-Violating Bug",
            task_family="bug_report_analysis",
            target_record_count=len(rows),
            bundled=True,
            research_question=(
                "What categories explain common sense-violating bugs reported in open-source "
                "Android applications?"
            ),
            use_case=settings["use_case"],
            data_description=settings["data_description"],
            artifact_unit="One GitHub bug report.",
            content_template=settings["content_template"],
            source_paths=[_DATA_PATH, _SETTINGS_PATH, _TAXONOMY_PATH],
            reference_label_mode=infer_reference_label_mode(categories),
            notes=[
                "Main coding flow must not see the raw 'category' field.",
                "The visible artifact is only the bug report and its source link.",
            ],
        )

    def iter_artifacts(self) -> Iterable[ArtifactRecord]:
        template = self._load_settings()["content_template"]
        for row in self._load_rows():
            artifact_id = str(row["id"])
            link = row.get("link")
            source_ref = build_source_ref(
                kind=infer_source_kind_from_url(link),
                value=link,
                ref_id=artifact_id,
                field="link",
            )
            source_refs = [source_ref] if source_ref is not None else []
            raw_fields = {
                "id": row["id"],
                "bug_report": row.get("bug_report", ""),
                "link": link,
            }
            yield ArtifactRecord(
                artifact_id=artifact_id,
                content=render_content_template(template, raw_fields),
                raw_fields=raw_fields,
                source_refs=source_refs,
                metadata={"dataset_name": _DATASET_NAME},
            )

    def load_reference_data(self) -> ReferenceData:
        annotations = [
            ReferenceAnnotation(
                artifact_id=str(row["id"]),
                observed_label=build_reference_label(row["category"]),
            )
            for row in self._load_rows()
            if "category" in row
        ]
        taxonomy = load_json(_TAXONOMY_PATH)
        return ReferenceData(
            annotations=annotations,
            taxonomy=taxonomy,
            metadata={
                "dataset_name": _DATASET_NAME,
                "taxonomy_path": str(_TAXONOMY_PATH),
                "annotation_count": len(annotations),
            },
        )

    def _load_rows(self) -> list[dict[str, Any]]:
        rows = load_json(_DATA_PATH)
        if not isinstance(rows, list):
            msg = f"{_DATA_PATH} must contain a list of records."
            raise TypeError(msg)
        return rows

    def _load_settings(self) -> dict[str, Any]:
        settings = load_json(_SETTINGS_PATH)
        if not isinstance(settings, dict):
            msg = f"{_SETTINGS_PATH} must contain a JSON object."
            raise TypeError(msg)
        return settings
