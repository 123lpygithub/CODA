from __future__ import annotations

from pathlib import Path
import os
from typing import Any, Iterable

from adapters.base import (
    ArtifactRecord,
    DatasetMetadata,
    ReferenceAnnotation,
    ReferenceData,
)
from adapters.common import (
    build_dimension_reference_label,
    build_source_ref,
    infer_source_kind_from_url,
    iter_csv_rows,
    load_json,
    render_content_template,
)
from adapters.satd_context import load_context

_REPO_ROOT = Path(__file__).resolve().parents[1]
_DATASET_NAME = "ml_satd_23_shades"
_DATASET_DIR = _REPO_ROOT / "dataset" / _DATASET_NAME
_DATA_PATH = _DATASET_DIR / "source" / "sampled_label_dataset.csv"
_SETTINGS_PATH = _DATASET_DIR / f"{_DATASET_NAME}_settings.json"
_MANIFEST_PATH = _DATASET_DIR / f"{_DATASET_NAME}_source_metadata.json"


class MLSATD23ShadesAdapter:
    """Adapter for the public 856-comment 23Shades sample."""

    def __init__(self, *, context_dir: Path | None = None) -> None:
        profile = os.environ.get("CODA_EVIDENCE_PROFILE")
        directory = {'paper-20261105':'code_context_20261105', 'paper-20261105-expanded':'code_context_20261105_expanded', 'paper-20261105-continued':'code_context_20261105_continued', 'paper-20261105-ready':'code_context_20261105_ready', 'paper-20261105-recovered':'code_context_20261105_recovered', 'paper-20261105-v9':'code_context_20261105_recovered', 'paper-20261106-v10':'code_context_20261106_v10'}.get(profile)
        self._context_dir = context_dir or (_DATASET_DIR / 'source' / directory if directory else None)

    def load_dataset_metadata(self) -> DatasetMetadata:
        rows = self._load_rows()
        settings = self._load_settings()
        context_notes = []
        if self._context_dir is not None:
            path = self._context_dir / 'manifest.json'
            counts = load_json(path).get('counts', {}) if path.exists() else {}
            context_notes = [
                f"Fixed-revision source context: {counts.get('available', 0)} available, {counts.get('ambiguous', 0)} ambiguous, {counts.get('historical_partial', 0)} related-history partial, {counts.get('unmatched', 0)} unmatched, {counts.get('unavailable', 0)} unavailable; ambiguous locations and revision differences remain explicit.",
                "Excerpts are matched to complete comments after documented release-format normalization; repeated or ambiguous matches are not guessed.",
            ]
        return DatasetMetadata(
            dataset_name=_DATASET_NAME,
            display_name="23 Shades of Self-Admitted Technical Debt",
            task_family="self_admitted_technical_debt_open_coding",
            target_record_count=len(rows),
            bundled=False,
            research_question=(
                "What recurring software and machine-learning-specific technical debt "
                "patterns appear in ML repository comments?"
            ),
            use_case=settings["use_case"],
            data_description=settings["data_description"],
            artifact_unit=("One sampled self-admitted technical-debt comment with source context; any location ambiguity or related-revision substitution is explicit." if os.environ.get('CODA_EVIDENCE_PROFILE') in ('paper-20261105-ready', 'paper-20261105-recovered', 'paper-20261105-v9', 'paper-20261106-v10') else "One sampled self-admitted technical-debt comment and recoverable source-code context at its introducing revision." if self._context_dir is not None else "One sampled self-admitted technical-debt source-code comment."),
            content_template=settings["content_template"],
            source_paths=[_DATA_PATH, _SETTINGS_PATH, _MANIFEST_PATH] + ([self._context_dir] if self._context_dir is not None else []),
            reference_label_mode="multi_label",
            notes=[
                "The coding flow sees comment text and repository provenance, not the paper labels.",
                "Reference labels contain independent software debt, ML debt, and pipeline-stage dimensions.",
                "The public artifact reports 856 sampled comments after filtering package-site comments.",
            ] + context_notes,
        )

    def iter_artifacts(self) -> Iterable[ArtifactRecord]:
        template = self._load_settings()["content_template"]
        for row_number, row in enumerate(self._load_rows(), start=1):
            # The published sample contains three repeated Dataset IDs; retain
            # the source ID while making the CODA artifact key unambiguous.
            artifact_id = f"23shades-{row_number:04d}-{row['Dataset ID']}"
            introduced = row.get("Comment-Introducing Revision", "")
            removed = row.get("Comment-Removing Revision", "")
            source_refs = [
                ref
                for ref in [
                    build_source_ref(
                        kind=infer_source_kind_from_url(introduced, default="commit"),
                        value=introduced,
                        ref_id=artifact_id,
                        field="comment_introducing_revision" if os.environ.get('CODA_EVIDENCE_PROFILE') in ('paper-20261105-ready', 'paper-20261105-recovered', 'paper-20261105-v9', 'paper-20261106-v10') else "Comment-Introducing Revision",
                    ),
                    build_source_ref(
                        kind=infer_source_kind_from_url(removed, default="commit"),
                        value=removed,
                        ref_id=artifact_id,
                        field="comment_removing_revision" if os.environ.get('CODA_EVIDENCE_PROFILE') in ('paper-20261105-ready', 'paper-20261105-recovered', 'paper-20261105-v9', 'paper-20261106-v10') else "Comment-Removing Revision",
                    ),
                ]
                if ref is not None
            ]
            raw_fields = {
                "dataset_id": row.get("Dataset ID", ""),
                "repo_type": row.get("Repo Type", ""),
                "repo_name": row.get("Repo Name", ""),
                "filename": row.get("Filename", ""),
                "comment_introducing_revision": introduced,
                "comment_removing_revision": removed,
                "comment_text": row.get("Comment Text", ""),
            }
            content = render_content_template(template, raw_fields)
            if self._context_dir is not None:
                snapshot = load_context(self._context_dir, artifact_id, introduced, row.get("Filename", ""))
                if snapshot and snapshot.get('status') == 'ambiguous':
                    raw_fields.update(source_context_status='ambiguous',
                                      source_context_commit=snapshot['commit'],
                                      source_context_candidates=snapshot['candidates'],
                                      source_context_ambiguity_note=snapshot['ambiguity_note'])
                    content += f"\n\nSource location ambiguity: {snapshot['ambiguity_note']}"
                    for number, candidate in enumerate(snapshot['candidates'], 1):
                        field=f'source_context_candidate_{number}'
                        raw_fields[field]=candidate['excerpt']
                        content += f"\n\nCandidate {number} at published commit {snapshot['commit']} (lines {candidate['line_start']}–{candidate['line_end']}):\n{candidate['excerpt']}"
                        source_refs.append(build_source_ref(kind='commit',value=snapshot['source_url'],ref_id=artifact_id,field=field))
                elif snapshot:
                    raw_fields.update({
                        "source_context": snapshot["excerpt"],
                        "source_context_commit": snapshot["commit"],
                        "source_context_line_start": snapshot["line_start"],
                        "source_context_line_end": snapshot["line_end"],
                        "source_context_status": snapshot.get('status','available'),
                    })
                    if snapshot.get('revision_relation'):
                        raw_fields['source_context_revision_note'] = snapshot['revision_note']
                        content += f"\n\nSource revision note: {snapshot['revision_note']}"
                        description='related historical' if snapshot.get('status')=='historical_partial' else 'verified predecessor'
                        content += f"\nSource context at {description} commit {snapshot['commit']} (lines {snapshot['line_start']}–{snapshot['line_end']}):\n{snapshot['excerpt']}"
                    else:
                        content += f"\n\nSource context at comment-introducing commit {snapshot['commit']} (lines {snapshot['line_start']}–{snapshot['line_end']}):\n{snapshot['excerpt']}"
                    source_refs.append(build_source_ref(kind="commit", value=snapshot["source_url"], ref_id=artifact_id, field="source_context"))
                else:
                    raw_fields["source_context_status"] = "unavailable"
                    content += "\n\nSource context: unavailable or the released comment could not be uniquely matched at its introducing revision. Interpret the comment within the available evidence."
            yield ArtifactRecord(
                artifact_id=artifact_id,
                content=content,
                raw_fields=raw_fields,
                source_refs=source_refs,
                metadata={
                    "dataset_name": _DATASET_NAME,
                    "repo_name": row.get("Repo Name", ""),
                    "repo_type": row.get("Repo Type", ""),
                },
            )

    def load_reference_data(self) -> ReferenceData:
        rows = self._load_rows()
        annotations = [
            ReferenceAnnotation(
                artifact_id=f"23shades-{row_number:04d}-{row['Dataset ID']}",
                observed_label=build_dimension_reference_label(
                    {
                        "Software SATD Type": row.get("Software TD Type", ""),
                        "ML SATD Type": row.get("ML TD Type", ""),
                        "ML SATD Type 2": row.get("ML TD Type 2", ""),
                        "ML Pipeline Stage": row.get("ML Pipeline Stage", ""),
                    }
                ),
            )
            for row_number, row in enumerate(rows, start=1)
        ]
        dimensions: dict[str, list[str]] = {}
        for column, dimension in [
            ("Software TD Type", "Software SATD Type"),
            ("ML TD Type", "ML SATD Type"),
            ("ML TD Type 2", "ML SATD Type 2"),
            ("ML Pipeline Stage", "ML Pipeline Stage"),
        ]:
            dimensions[dimension] = sorted(
                {row.get(column, "").strip() for row in rows if row.get(column, "").strip()}
            )
        return ReferenceData(
            annotations=annotations,
            taxonomy={"dimensions": dimensions},
            metadata={
                "dataset_name": _DATASET_NAME,
                "source_label_columns": list(dimensions),
                "annotation_count": len(annotations),
            },
        )

    def _load_rows(self) -> list[dict[str, str]]:
        rows = list(iter_csv_rows(_DATA_PATH))
        if not rows:
            raise ValueError(f"{_DATA_PATH} contains no records.")
        required = {"Dataset ID", "Comment Text", "Repo Name"}
        missing = required - set(rows[0])
        if missing:
            raise ValueError(f"{_DATA_PATH} is missing columns: {sorted(missing)}")
        return rows

    def _load_settings(self) -> dict[str, Any]:
        settings = load_json(_SETTINGS_PATH)
        if not isinstance(settings, dict):
            raise TypeError(f"{_SETTINGS_PATH} must contain a JSON object.")
        return settings
