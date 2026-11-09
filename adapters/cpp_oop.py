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
_DATASET_NAME = "cpp_oop_related_feature"
_DATASET_DIR = (
    _REPO_ROOT / "dataset" / _DATASET_NAME
)
_DATA_PATH = _DATASET_DIR / f"{_DATASET_NAME}.json"
_SETTINGS_PATH = _DATASET_DIR / f"{_DATASET_NAME}_settings.json"
_TAXONOMY_PATH = _DATASET_DIR / f"{_DATASET_NAME}_taxonomy.json"


class CppOopRelatedFeatureAdapter:
    """Adapter for the C++ OOP-related feature task."""

    def load_dataset_metadata(self) -> DatasetMetadata:
        rows = self._load_rows()
        settings = self._load_settings()
        categories = [row["category"] for row in rows if "category" in row]
        return DatasetMetadata(
            dataset_name=_DATASET_NAME,
            display_name="C++ OOP-Related Feature",
            task_family="bug_patch_analysis",
            target_record_count=len(rows),
            bundled=True,
            research_question=(
                "What OOP-related feature categories explain compiler bugs in C++ when "
                "jointly analyzing bug reports and their fixes?"
            ),
            use_case=settings["use_case"],
            data_description=settings["data_description"],
            artifact_unit="One C++ compiler bug report paired with its corresponding patch.",
            content_template=settings["content_template"],
            source_paths=[_DATA_PATH, _SETTINGS_PATH, _TAXONOMY_PATH],
            reference_label_mode=infer_reference_label_mode(categories),
            notes=[
                "Main coding flow must not see the raw 'category' field.",
                "Both bug report and patch content must remain available for evidence grounding.",
            ],
        )

    def iter_artifacts(self) -> Iterable[ArtifactRecord]:
        template = self._load_settings()["content_template"]
        for row in self._load_rows():
            artifact_id = str(row["id"])
            bug_link = row.get("bug_link")
            patch_link = row.get("patch_link")
            source_refs = []
            bug_source_ref = build_source_ref(
                kind=infer_source_kind_from_url(bug_link),
                value=bug_link,
                ref_id=f"{artifact_id}:bug",
                field="bug_link",
            )
            if bug_source_ref is not None:
                source_refs.append(bug_source_ref)
            patch_source_ref = build_source_ref(
                kind=infer_source_kind_from_url(patch_link),
                value=patch_link,
                ref_id=f"{artifact_id}:patch",
                field="patch_link",
            )
            if patch_source_ref is not None:
                source_refs.append(patch_source_ref)

            raw_fields = {
                "id": row["id"],
                "bug_content": row.get("bug_content", ""),
                "patch_content": row.get("patch_content", ""),
                "bug_link": bug_link,
                "patch_link": patch_link,
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
