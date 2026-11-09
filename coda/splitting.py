"""Deterministic, reference-blind artifact splitting for CODA runs."""

from __future__ import annotations

import hashlib
from collections import defaultdict

from adapters.base import ArtifactRecord


def default_held_out_size(total_artifacts: int) -> int:
    """Scale the recommended reservation for intentionally small runs."""

    if total_artifacts <= 1:
        return 0
    if total_artifacts <= 100:
        recommended = 12
    elif total_artifacts <= 1000:
        recommended = 50
    else:
        recommended = 100
    scaled_minimum = max(1, round(total_artifacts * 0.20))
    return min(recommended, scaled_minimum, total_artifacts - 2)


def _visible_value(artifact: ArtifactRecord, field: str) -> str | None:
    value = artifact.metadata.get(field)
    if value is None:
        value = artifact.raw_fields.get(field)
    if isinstance(value, str) and value.strip():
        return value.strip()
    return None


def split_group_id(dataset_name: str, artifact: ArtifactRecord) -> str:
    """Return only grouping metadata needed to prevent related-case leakage."""

    group_fields: tuple[str, ...] = ()
    if dataset_name == "fairness_api_issue_topic":
        group_fields = ("base_issue_url", "issue_url")
    elif dataset_name == "dockerfile_flakiness":
        group_fields = ("repo_name",)
    for field in group_fields:
        value = _visible_value(artifact, field)
        if value is not None:
            family = "issue" if dataset_name == "fairness_api_issue_topic" else field
            return f"{family}:{value}"
    # Paired LLM semantic/syntactic views share IDs and a split-family seed.
    return f"artifact:{artifact.artifact_id}"


def deterministic_held_out_split(
    artifacts: list[ArtifactRecord],
    *,
    dataset_name: str,
    split_family: str,
    held_out_target: int,
    seed: int = 20260907,
) -> tuple[list[ArtifactRecord], list[ArtifactRecord], dict[str, str]]:
    """Split complete visible groups, choosing a deterministic count near target.

    The dynamic program never reads reference labels. It chooses the largest
    whole-group subset not exceeding the requested target and leaves at least
    two artifacts in the coding pool for the initial coding workflow.
    """

    if held_out_target < 1:
        raise ValueError("held_out_target must be positive when held-out is enabled.")
    if held_out_target > len(artifacts) - 2:
        raise ValueError(
            "Held-out reservation must leave at least two artifacts in the coding pool."
        )

    members_by_group: dict[str, list[ArtifactRecord]] = defaultdict(list)
    for artifact in artifacts:
        members_by_group[split_group_id(dataset_name, artifact)].append(artifact)

    ranked_group_ids = sorted(
        members_by_group,
        key=lambda group_id: hashlib.sha256(
            f"{seed}:{split_family}:{group_id}".encode("utf-8")
        ).hexdigest(),
    )
    choices: dict[int, tuple[str, ...]] = {0: ()}
    for group_id in ranked_group_ids:
        group_size = len(members_by_group[group_id])
        for current_size, chosen in sorted(choices.items(), reverse=True):
            new_size = current_size + group_size
            if new_size <= held_out_target and new_size not in choices:
                choices[new_size] = (*chosen, group_id)

    actual_count = max(choices)
    if actual_count == 0:
        raise ValueError(
            "No complete source group can be reserved at this size; increase the "
            "held-out target or run without a held-out split."
        )
    held_group_ids = set(choices[actual_count])
    coding: list[ArtifactRecord] = []
    held_out: list[ArtifactRecord] = []
    group_ids: dict[str, str] = {}
    for artifact in artifacts:
        group_id = split_group_id(dataset_name, artifact)
        group_ids[artifact.artifact_id] = group_id
        (held_out if group_id in held_group_ids else coding).append(artifact)
    if len(coding) < 2:
        raise ValueError("Held-out split leaves fewer than two coding artifacts.")
    return coding, held_out, group_ids
