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
    infer_reference_label_mode,
    load_json,
    render_content_template,
)

_REPO_ROOT = Path(__file__).resolve().parents[1]
_DATASET_NAME = "dockerfile_flakiness"
_DATASET_DIR = (
    _REPO_ROOT / "dataset" / _DATASET_NAME
)
_DATA_PATH = _DATASET_DIR / f"{_DATASET_NAME}.json"
_SETTINGS_PATH = _DATASET_DIR / f"{_DATASET_NAME}_settings.json"
_TAXONOMY_PATH = _DATASET_DIR / f"{_DATASET_NAME}_taxonomy.json"


class DockerfileFlakinessAdapter:
    """Adapter for the Dockerfile flakiness taxonomy task."""

    def load_dataset_metadata(self) -> DatasetMetadata:
        rows = self._load_rows()
        settings = self._load_settings()
        categories = [row["category"] for row in rows if row.get("category")]
        return DatasetMetadata(
            dataset_name=_DATASET_NAME,
            display_name="Dockerfile Flakiness",
            task_family="build_failure_analysis",
            target_record_count=len(rows),
            bundled=False,
            research_question=(
                "What recurring categories characterize flaky Dockerfile build failures?"
            ),
            use_case=settings["use_case"],
            data_description=settings["data_description"],
            artifact_unit="One flaky Docker build instance with Dockerfile context and build error.",
            content_template=settings["content_template"],
            source_paths=[_DATA_PATH, _SETTINGS_PATH, _TAXONOMY_PATH],
            reference_label_mode=infer_reference_label_mode(categories),
            notes=[
                "Main coding flow must not see the raw 'category' field.",
                "Prepared records follow the How-style local layout under data/dataset/.",
                "Human labels are collapsed to a two-layer taxonomy for alignment with the How study.",
            ],
        )

    def iter_artifacts(self) -> Iterable[ArtifactRecord]:
        template = self._load_settings()["content_template"]
        for row in self._load_rows():
            artifact_id = str(row["id"])
            source_value = f"{row.get('repo_name', '')}@{row.get('build_time', '')}"
            source_ref = build_source_ref(
                kind="repository",
                value=source_value.strip("@"),
                ref_id=artifact_id,
                field="repo_name",
            )
            source_refs = [source_ref] if source_ref is not None else []
            raw_fields = {
                "id": row["id"],
                "dockerfile": row.get("dockerfile", ""),
                "build_error": row.get("build_error", ""),
                "build_output": row.get("build_output", ""),
                "repo_name": row.get("repo_name", ""),
                "build_time": row.get("build_time", ""),
                "error_summary": row.get("error_summary", ""),
                "dockerfile_error_segment": row.get("dockerfile_error_segment", ""),
                "dockerfile_error_line": row.get("dockerfile_error_line"),
                "dockerfile_exit_code": row.get("dockerfile_exit_code"),
                "sources_of_error": row.get("sources_of_error", []),
                "stderr_line": row.get("stderr_line"),
            }
            yield ArtifactRecord(
                artifact_id=artifact_id,
                content=render_content_template(template, raw_fields),
                raw_fields=raw_fields,
                source_refs=source_refs,
                metadata={
                    "dataset_name": _DATASET_NAME,
                    "repo_name": row.get("repo_name", ""),
                    "build_time": row.get("build_time", ""),
                },
            )

    def load_reference_data(self) -> ReferenceData:
        annotations = [
            ReferenceAnnotation(
                artifact_id=str(row["id"]),
                observed_label=build_reference_label(row["category"]),
            )
            for row in self._load_rows()
            if row.get("category")
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
