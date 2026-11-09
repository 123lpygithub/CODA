from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable

from adapters.base import ArtifactRecord, DatasetMetadata, ReferenceAnnotation, ReferenceData
from adapters.common import (
    build_reference_label,
    build_source_ref,
    infer_reference_label_mode,
    load_json,
    render_content_template,
)

_REPO_ROOT = Path(__file__).resolve().parents[1]
_DATASET_NAME = "fairness_api_issue_topic"
_DATASET_DIR = (
    _REPO_ROOT / "dataset" / _DATASET_NAME
)
_DATA_PATH = _DATASET_DIR / f"{_DATASET_NAME}.json"
_SETTINGS_PATH = _DATASET_DIR / f"{_DATASET_NAME}_settings.json"
_TAXONOMY_PATH = _DATASET_DIR / f"{_DATASET_NAME}_taxonomy.json"


class FairnessApiIssueTopicAdapter:
    """Adapter for fairness API issue-discussion topics using the latest upstream release."""

    def load_dataset_metadata(self) -> DatasetMetadata:
        rows = self._load_rows()
        settings = self._load_settings()
        categories = [row["category"] for row in rows if row.get("category")]
        return DatasetMetadata(
            dataset_name=_DATASET_NAME,
            display_name="Fairness API Issue Topic",
            task_family="issue_discussion_analysis",
            target_record_count=len(rows),
            bundled=False,
            research_question=(
                "What recurring issue discussion topics arise when developers use fairness API libraries?"
            ),
            use_case=settings["use_case"],
            data_description=settings["data_description"],
            artifact_unit="One issue or issue-comment discussion record from a fairness API repository.",
            content_template=settings["content_template"],
            source_paths=[_DATA_PATH, _SETTINGS_PATH, _TAXONOMY_PATH],
            reference_label_mode=infer_reference_label_mode(categories),
            notes=[
                "Main coding flow must not see the raw 'category' field.",
                "Prepared records follow the local How-style layout under data/dataset/.",
                "Current implementation uses the latest 4212-row upstream version rather than the How paper's 1946-row snapshot.",
            ],
        )

    def iter_artifacts(self) -> Iterable[ArtifactRecord]:
        template = self._load_settings()["content_template"]
        for row in self._load_rows():
            artifact_id = str(row["id"])
            row_url = row.get("url", "")
            base_issue_url = row.get("base_issue_url", "")
            source_refs = [
                ref
                for ref in [
                    build_source_ref(kind="issue", value=row_url, ref_id=artifact_id, field="issue_content"),
                    build_source_ref(
                        kind="issue",
                        value=base_issue_url if base_issue_url != row_url else None,
                        ref_id=artifact_id,
                        field="base_issue_url",
                    ),
                    build_source_ref(
                        kind="repository",
                        value=row.get("repo_url", ""),
                        ref_id=artifact_id,
                        field="repo_url",
                    ),
                ]
                if ref is not None
            ]
            raw_fields = {
                "id": row["id"],
                "issue_content": row.get("issue_content", ""),
                "repo_url": row.get("repo_url", ""),
                "type": row.get("type", ""),
                "url": row_url,
                "base_issue_url": base_issue_url,
                "created_at": row.get("created_at", ""),
            }
            yield ArtifactRecord(
                artifact_id=artifact_id,
                content=render_content_template(template, raw_fields),
                raw_fields=raw_fields,
                source_refs=source_refs,
                metadata={
                    "dataset_name": _DATASET_NAME,
                    "type": row.get("type", ""),
                    "repo_url": row.get("repo_url", ""),
                    "base_issue_url": base_issue_url,
                    "created_at": row.get("created_at", ""),
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
                "conversion_note": "Built from the latest 4212-row upstream version.",
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
