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
from adapters.github_issue_snapshot import load_snapshot, render_discussion, load_archived_supplement
from adapters.github_linked_evidence import load_linked_evidence, render_link

_REPO_ROOT = Path(__file__).resolve().parents[1]
_DATASET_NAME = "personal_data_protection_github"
_DATASET_DIR = _REPO_ROOT / "dataset" / _DATASET_NAME
_DATA_PATH = (
    _DATASET_DIR
    / "source"
    / "extracted"
    / "coded_issue_data.csv"
)
_SETTINGS_PATH = _DATASET_DIR / f"{_DATASET_NAME}_settings.json"
_MANIFEST_PATH = _DATASET_DIR / f"{_DATASET_NAME}_source_metadata.json"
_SNAPSHOT_DIR = _DATASET_DIR / "source" / "github_snapshot"


class PersonalDataProtectionGitHubAdapter:
    """Adapter for the paper's 652 manually confirmed privacy-related issues."""

    def __init__(self, *, snapshot_dir: Path | None = None, linked_dir: Path | None = None) -> None:
        profile = os.environ.get("CODA_EVIDENCE_PROFILE")
        suffix = {'paper-20261105':'20261105', 'paper-20261105-expanded':'20261105_expanded', 'paper-20261105-continued':'20261105_continued', 'paper-20261105-ready':'20261105_ready', 'paper-20261105-recovered':'20261105_recovered', 'paper-20261105-v9':'20261105_v9', 'paper-20261106-v10':'20261106_v10'}.get(profile)
        self._snapshot_dir = snapshot_dir or (_SNAPSHOT_DIR.with_name('github_snapshot_' + suffix) if suffix else _SNAPSHOT_DIR)
        self._linked_dir = linked_dir or (_SNAPSHOT_DIR.with_name('linked_artifacts_' + suffix) if suffix else None)

    def load_dataset_metadata(self) -> DatasetMetadata:
        rows = self._load_rows()
        settings = self._load_settings()
        snapshot_manifest = self._snapshot_dir / "manifest.json"
        counts = load_json(snapshot_manifest).get("counts", {}) if snapshot_manifest.exists() else {}
        linked_notes = []
        if self._linked_dir is not None:
            path = self._linked_dir / 'manifest.json'
            linked_counts = load_json(path).get('counts', {}) if path.exists() else {}
            linked_notes = [
                f"Linked development evidence: {linked_counts.get('available', 0)} available case-link records, {linked_counts.get('partial', 0)} partial, {linked_counts.get('unavailable', 0)} unavailable.",
                "One-hop explicit GitHub files, commit patches, PRs and issue discussions are included when retrievable. Availability is separate from evidence of merge, deployment or resolution.",
            ]
        return DatasetMetadata(
            dataset_name=_DATASET_NAME,
            display_name="Personal Data and Data Protection Issues on GitHub",
            task_family="privacy_issue_inductive_coding",
            target_record_count=len(rows),
            bundled=False,
            research_question=(
                "What personal-data and data-protection concerns arise in these "
                "issues, and how are they addressed in the available evidence?"
            ),
            use_case=settings["use_case"],
            data_description=settings["data_description"],
            artifact_unit="One privacy-related GitHub issue: released metadata plus a fixed supplemental body/comment snapshot where available, with explicit evidence gaps.",
            content_template=settings["content_template"],
            source_paths=[_DATA_PATH, _SETTINGS_PATH, _MANIFEST_PATH, self._snapshot_dir] + ([self._linked_dir] if self._linked_dir else []),
            reference_label_mode="multi_label",
            notes=[
                "The published replication package contains issue titles and metadata, but not issue bodies or comments.",
                "CODA supplements the release with offline GitHub body/comment snapshots; no network fetching occurs during coding.",
                f"Supplemental evidence: {counts.get('complete', 0)} complete, {counts.get('partial', 0)} partial, {counts.get('unavailable', 0)} unavailable; remaining records have released metadata only.",
                "Supplemental snapshots reflect retrieval-time content, not the original study's historical evidence; missing text and discussion must not be inferred from titles or counts.",
                "The five manual coding dimensions are isolated in ReferenceData and are never sent to agents.",
                "Reporter and discussant identities are intentionally withheld from agent-facing fields.",
                "Comment counts and closed status do not establish discussion content or reasons for resolution.",
            ] + linked_notes,
        )

    def iter_artifacts(self) -> Iterable[ArtifactRecord]:
        template = self._load_settings()["content_template"]
        for row in self._load_rows():
            artifact_id = f"privacy-issue-{row['index']}"
            issue_url = row.get("url", "")
            html_url = row.get("html_url", "")
            snapshot = load_snapshot(self._snapshot_dir, artifact_id, html_url)
            source_refs = [
                ref
                for ref in [
                    build_source_ref(
                        kind=infer_source_kind_from_url(issue_url, default="issue"),
                        value=issue_url,
                        ref_id=artifact_id,
                        field="issue_url" if os.environ.get('CODA_EVIDENCE_PROFILE') in ('paper-20261105-ready', 'paper-20261105-recovered', 'paper-20261105-v9', 'paper-20261106-v10') else "url",
                    ),
                    build_source_ref(
                        kind="issue",
                        value=html_url,
                        ref_id=artifact_id,
                        field="html_url",
                    ),
                    build_source_ref(
                        kind="repository",
                        value=(
                            f"https://github.com/{row.get('project', '').strip()}"
                            if row.get("project", "").strip()
                            else None
                        ),
                        ref_id=artifact_id,
                        field="project",
                    ),
                ]
                if ref is not None
            ]
            raw_fields = {
                "index": row.get("index", ""),
                "issue_url": issue_url,
                "html_url": html_url,
                "created_at": row.get("created_at", ""),
                "title": row.get("title", ""),
                "keywords": row.get("keywords", ""),
                "type": row.get("type", ""),
                "project": row.get("project", ""),
                "comment_count": row.get("#comments", ""),
                "discussant_count": row.get("#discussants", ""),
                "reporting_date": row.get("reporting_date", ""),
                "last_active_date": row.get("last_active_date", ""),
                "status": row.get("status", ""),
                "github_labels": row.get("labels", ""),
                "label_count": row.get("#labels", ""),
                "issue_number": row.get("issue_number", ""),
                "harmonized_labels": row.get("harmonized_labels", ""),
                "body": snapshot["body"] if snapshot else "[Issue body not retrieved.]",
                "discussion": render_discussion(snapshot) if snapshot else "[Issue discussion not retrieved.]",
                "snapshot_title": snapshot["title"] if snapshot else "[Not retrieved.]",
                "snapshot_status": snapshot["state"] if snapshot else "[Not retrieved.]",
                "snapshot_fetched_at": snapshot["issue_fetched_at"] if snapshot else "[Not retrieved.]",
                "snapshot_updated_at": snapshot["updated_at"] if snapshot else "[Not retrieved.]",
                "evidence_status": snapshot["evidence_status"] if snapshot else "metadata_only",
                "evidence_scope": snapshot["scope"] if snapshot else "Released title and metadata only; no body or discussion is available.",
                "retrieved_comment_count": snapshot["retrieved_comment_count"] if snapshot else 0,
                "snapshot_expected_comment_count": snapshot["expected_comment_count"] if snapshot else "unknown",
            }
            if snapshot:
                # Expose each comment separately so evidence can cite exact text.
                for comment in snapshot["comments"]:
                    field = f"comment_{comment['id']}"
                    raw_fields[field] = comment["body"]
                    source_refs.append(build_source_ref(
                        kind="discussion", value=comment["url"],
                        ref_id=artifact_id, field=field,
                    ))
                source_refs.append(build_source_ref(
                    kind="issue", value=snapshot["issue_url"], ref_id=artifact_id, field="body",
                ))
            content = render_content_template(template, raw_fields)
            if os.environ.get('CODA_EVIDENCE_PROFILE') in ('paper-20261105-expanded', 'paper-20261105-continued', 'paper-20261105-ready', 'paper-20261105-recovered', 'paper-20261105-v9', 'paper-20261106-v10'):
                archived = load_archived_supplement(self._snapshot_dir, artifact_id, html_url)
                if archived:
                    raw_fields['historical_evidence_scope'] = archived['scope']
                    raw_fields['historical_issue_body'] = archived['body']
                    raw_fields['historical_issue_discussion'] = render_discussion(archived)
                    content += '\n\nHistorical event-archive supplement:\n' + archived['scope'] + '\nArchived body:\n' + archived['body'] + '\nArchived discussion:\n' + raw_fields['historical_issue_discussion']
                    source_refs.append(build_source_ref(kind='external_url', value=archived['archive_query_url'], ref_id=artifact_id, field='historical_issue_body'))
                    for comment in archived['comments']:
                        field=f"historical_comment_{comment['id']}"
                        raw_fields[field]=comment['body']
                        source_refs.append(build_source_ref(kind='discussion',value=comment['url'],ref_id=artifact_id,field=field))
            if self._linked_dir is not None:
                linked = load_linked_evidence(self._linked_dir, artifact_id, html_url, snapshot)
                raw_fields['linked_evidence_scope'] = linked['scope'] if linked else 'Linked development material has not been collected.'
                links = linked['links'] if linked else []
                raw_fields['linked_evidence_count'] = len(links)
                raw_fields['linked_evidence_available_count'] = sum(item['status'] == 'available' for item in links)
                content += '\n\nLinked development evidence:\n' + raw_fields['linked_evidence_scope']
                if not links:
                    content += '\n[No supported explicit links found in the available discussion.]' if linked and snapshot else '\n[Linked development evidence unavailable.]'
                for index, item in enumerate(links, 1):
                    field = f'linked_artifact_{index}'
                    raw_fields[field] = render_link(item)
                    content += '\n\n' + raw_fields[field]
                    source_refs.append(build_source_ref(
                        kind={'file':'other', 'pull_request':'pull_request', 'commit':'commit', 'issue':'issue'}[item['kind']],
                        value=item['url'], ref_id=artifact_id, field=field,
                    ))
                if os.environ.get('CODA_EVIDENCE_PROFILE') in ('paper-20261105-ready', 'paper-20261105-recovered', 'paper-20261105-v9', 'paper-20261106-v10'):
                    external = load_linked_evidence(self._linked_dir, artifact_id, html_url, snapshot,
                                                    manifest_name='external_manifest.json')
                    if external:
                        raw_fields['external_evidence_scope'] = external['scope']
                        raw_fields['external_evidence_count'] = len(external['links'])
                        content += '\n\nExplicitly cited external context:\n' + external['scope']
                        for index, item in enumerate(external['links'], 1):
                            field = f'external_artifact_{index}'
                            raw_fields[field] = render_link(item)
                            content += '\n\n' + raw_fields[field]
                            source_refs.append(build_source_ref(kind='external_url', value=item['url'],
                                                                ref_id=artifact_id, field=field))
            yield ArtifactRecord(
                artifact_id=artifact_id,
                content=content,
                raw_fields=raw_fields,
                source_refs=source_refs,
                metadata={
                    "dataset_name": _DATASET_NAME,
                    "project": row.get("project", ""),
                    "issue_type": row.get("type", ""),
                    "evidence_status": raw_fields["evidence_status"],
                    "evidence_snapshot_fetched_at": raw_fields["snapshot_fetched_at"],
                },
            )

    def load_reference_data(self) -> ReferenceData:
        rows = self._load_rows()
        annotations = [
            ReferenceAnnotation(
                artifact_id=f"privacy-issue-{row['index']}",
                observed_label=build_dimension_reference_label(
                    {
                        "Trigger": row.get("trigger_rater_2", ""),
                        "Privacy Issue": row.get("privacy_issue_rater_2", ""),
                        "Consent Interaction": row.get("consent_interaction_rater_2", ""),
                        "Resolution": row.get("resolution_rater_2", ""),
                        "Reason for Resolution": row.get("reason_rater_2_category", ""),
                    }
                ),
            )
            for row in rows
        ]
        dimension_columns = {
            "Trigger": "trigger_rater_2",
            "Privacy Issue": "privacy_issue_rater_2",
            "Consent Interaction": "consent_interaction_rater_2",
            "Resolution": "resolution_rater_2",
            "Reason for Resolution": "reason_rater_2_category",
        }
        dimensions = {
            dimension: sorted(
                {
                    row.get(column, "").strip()
                    for row in rows
                    if row.get(column, "").strip()
                }
            )
            for dimension, column in dimension_columns.items()
        }
        return ReferenceData(
            annotations=annotations,
            taxonomy={"dimensions": dimensions},
            metadata={
                "dataset_name": _DATASET_NAME,
                "annotation_count": len(annotations),
                "reference_rater": "rater_2 / final released coding fields",
            },
        )

    def _load_rows(self) -> list[dict[str, str]]:
        rows = [
            row
            for row in iter_csv_rows(_DATA_PATH, delimiter=";")
            if row.get("is_privacy_related", "").strip().lower() == "true"
        ]
        if not rows:
            raise ValueError(f"{_DATA_PATH} contains no privacy-related records.")
        required = {"index", "title", "url", "is_privacy_related"}
        missing = required - set(rows[0])
        if missing:
            raise ValueError(f"{_DATA_PATH} is missing columns: {sorted(missing)}")
        return rows

    def _load_settings(self) -> dict[str, Any]:
        settings = load_json(_SETTINGS_PATH)
        if not isinstance(settings, dict):
            raise TypeError(f"{_SETTINGS_PATH} must contain a JSON object.")
        return settings
