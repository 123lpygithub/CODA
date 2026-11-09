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
_DATASET_ROOT = _REPO_ROOT / "dataset"


class _Defects4CodeLLMBaseAdapter:
    """Shared loader for the two Defects4CodeLLM task variants."""

    dataset_name: str
    display_name: str
    research_question: str
    label_column: str
    settings_file_name: str

    def load_dataset_metadata(self) -> DatasetMetadata:
        rows = self._load_rows()
        settings = self._load_settings()
        categories = [row["category"] for row in rows if row.get("category")]
        return DatasetMetadata(
            dataset_name=self.dataset_name,
            display_name=self.display_name,
            task_family="code_generation_error_analysis",
            target_record_count=len(rows),
            bundled=True,
            research_question=self.research_question,
            use_case=settings["use_case"],
            data_description=settings["data_description"],
            artifact_unit="One LLM code-generation error instance keyed by Error ID.",
            content_template=settings["content_template"],
            source_paths=[self._data_path(), self._settings_path(), self._taxonomy_path()],
            reference_label_mode=infer_reference_label_mode(categories),
            notes=[
                "Main coding flow must not see the raw 'category' field.",
                "Prepared datasets follow the How-style common layout under data/dataset/.",
                "Semantic and syntactic tasks share the same 687 artifacts and differ only in the hidden taxonomy path.",
            ],
        )

    def iter_artifacts(self) -> Iterable[ArtifactRecord]:
        template = self._load_settings()["content_template"]
        for row in self._load_rows():
            artifact_id = str(row["id"])
            source_ref = build_source_ref(
                kind="other",
                value=f"{row['source_file']}#error_id={artifact_id}",
                ref_id=artifact_id,
                field="source_file",
            )
            source_refs = [source_ref] if source_ref is not None else []
            raw_fields = {
                "id": row["id"],
                "model": row["model"],
                "task_id": row["task_id"],
                "task_description": row["task_description"],
                "incorrect_code": row["incorrect_code"],
                "ground_truth_code": row["ground_truth_code"],
                "source_file": row["source_file"],
            }
            yield ArtifactRecord(
                artifact_id=artifact_id,
                content=render_content_template(template, raw_fields),
                raw_fields=raw_fields,
                source_refs=source_refs,
                metadata={
                    "dataset_name": self.dataset_name,
                    "model": row["model"],
                    "task_id": row["task_id"],
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
        taxonomy = load_json(self._taxonomy_path())
        return ReferenceData(
            annotations=annotations,
            taxonomy=taxonomy,
            metadata={
                "dataset_name": self.dataset_name,
                "annotation_count": len(annotations),
                "taxonomy_path": str(self._taxonomy_path()),
            },
        )

    def iter_solution_artifacts(self) -> Iterable[ArtifactRecord]:
        """Use one visible-evidence representative per generated solution.

        Keep iter_artifacts() at Error-ID level for historical run recovery and
        the published annotations. Never use the hidden category to group cases.
        """
        groups: dict[tuple[str, str, str], list[ArtifactRecord]] = {}
        for artifact in self.iter_artifacts():
            fields = artifact.raw_fields
            key = (str(fields["task_id"]), str(fields["model"]), fields["incorrect_code"])
            groups.setdefault(key, []).append(artifact)
        representatives = []
        for members in groups.values():
            members.sort(key=lambda artifact: int(artifact.artifact_id))
            first = members[0]
            if any(member.content != first.content for member in members):
                raise ValueError(f"Conflicting source evidence for solution {first.artifact_id}.")
            representatives.append(first)
        yield from sorted(representatives, key=lambda artifact: int(artifact.artifact_id))

    def _dataset_dir(self) -> Path:
        return _DATASET_ROOT / self.dataset_name

    def _data_path(self) -> Path:
        return self._dataset_dir() / f"{self.dataset_name}.json"

    def _settings_path(self) -> Path:
        return self._dataset_dir() / f"{self.dataset_name}_settings.json"

    def _taxonomy_path(self) -> Path:
        return self._dataset_dir() / f"{self.dataset_name}_taxonomy.json"

    def _load_settings(self) -> dict[str, Any]:
        settings = load_json(self._settings_path())
        if not isinstance(settings, dict):
            msg = f"{self._settings_path()} must contain a JSON object."
            raise TypeError(msg)
        return settings

    def _load_rows(self) -> list[dict[str, Any]]:
        rows = load_json(self._data_path())
        if not isinstance(rows, list):
            msg = f"{self._data_path()} must contain a list of records."
            raise TypeError(msg)
        return rows


class Defects4CodeLLMSemanticAdapter(_Defects4CodeLLMBaseAdapter):
    """Semantic-characteristics view of Defects4CodeLLM."""

    dataset_name = "llm_code_error_semantic"
    display_name = "LLM Code Error (Semantic)"
    research_question = (
        "What semantic root-cause categories characterize LLM code-generation errors?"
    )
    settings_file_name = "llm_code_error_semantic.json"


class Defects4CodeLLMSyntacticAdapter(_Defects4CodeLLMBaseAdapter):
    """Syntactic-characteristics view of Defects4CodeLLM."""

    dataset_name = "llm_code_error_syntactic"
    display_name = "LLM Code Error (Syntactic)"
    research_question = (
        "What syntactic root-cause categories characterize LLM code-generation errors?"
    )
    settings_file_name = "llm_code_error_syntactic.json"
