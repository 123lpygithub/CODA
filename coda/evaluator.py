"""Independent RQ1 evaluator protocol for frozen CODA outputs.

Evaluator scores are deliberately outside the coding workflow.  This module
only validates the shared rubric, runs the pilot calibration comparison, and
selects a candidate evaluator according to the TSE27-CODA protocol.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
import hashlib
import json
from typing import Any, Iterable
from coda.study import StudyManifestError, verify_study_scores

from coda.evaluation import (
    EvaluationError,
    gwet_ac2_bootstrap,
    validate_rq1_score,
)


CALIBRATION_DIMENSIONS = (
    "clarity",
    "category_boundaries",
    "meaningful_coverage",
    "evidence_support",
)


@dataclass(frozen=True)
class CalibrationConfig:
    """Pre-registered thresholds for evaluator selection."""

    minimum_positive_agreement: float = 0.0
    maximum_agreement_drop: float = 0.15
    bootstrap_replicates: int = 2000
    bootstrap_seed: int = 20260907
    selected_model_count: int = 3


def _unit_key(row: dict[str, Any]) -> tuple[str, str, str, str]:
    unit = str(row.get("unit"))
    if unit == "codebook":
        return (str(row["run_id"]), unit, str(row.get("dimension")), "codebook")
    return (
        str(row["run_id"]),
        unit,
        str(row.get("dimension")),
        f"{row.get('artifact_id')}::{row.get('code_id')}",
    )


def validate_calibration_score(row: dict[str, Any]) -> None:
    """Validate one pilot score using the same rubric as formal RQ1."""

    validate_rq1_score(row)
    if row.get("phase") != "pilot":
        raise EvaluationError("Calibration rows must use phase='pilot'.")
    evaluator_kind = row.get("evaluator_kind")
    if evaluator_kind not in {"human", "llm"}:
        raise EvaluationError("Calibration rows require evaluator_kind human or llm.")
    if evaluator_kind == "llm" and not row.get("candidate_model"):
        raise EvaluationError("LLM calibration rows require candidate_model.")
    if not isinstance(row.get("rationale"), str) or not row["rationale"].strip():
        raise EvaluationError("Calibration scores require a rationale.")


def _paired_scores(
    rows: Iterable[dict[str, Any]],
    left_id: str,
    right_id: str,
    dimension: str,
) -> tuple[list[int], list[int]]:
    by_evaluator: dict[str, dict[tuple[str, str, str, str], dict[str, Any]]] = defaultdict(dict)
    for row in rows:
        if str(row.get("dimension")) != dimension:
            continue
        if row.get("status", "assessable") != "assessable":
            continue
        if not isinstance(row.get("score"), int):
            continue
        by_evaluator[str(row["evaluator_id"])][_unit_key(row)] = row
    shared = sorted(set(by_evaluator[left_id]) & set(by_evaluator[right_id]))
    return (
        [int(by_evaluator[left_id][key]["score"]) for key in shared],
        [int(by_evaluator[right_id][key]["score"]) for key in shared],
    )


def _agreement(
    rows: list[dict[str, Any]],
    left_id: str,
    right_id: str,
    dimension: str,
    config: CalibrationConfig,
) -> dict[str, Any]:
    left, right = _paired_scores(rows, left_id, right_id, dimension)
    if not left:
        return {
            "estimate": None,
            "lower": None,
            "upper": None,
            "items": 0,
            "available": False,
        }
    categories = list(range(1, 6)) if dimension != "evidence_support" else [0, 1, 2]
    result = gwet_ac2_bootstrap(
        left,
        right,
        categories=categories,
        replicates=config.bootstrap_replicates,
        seed=config.bootstrap_seed,
    )
    return {
        "available": True, **result,
        "mean_signed_score_difference_right_minus_left": sum(b - a for a, b in zip(left, right)) / len(left),
    }


def calibrate_evaluators(
    rows: Iterable[dict[str, Any]],
    *,
    candidate_models: Iterable[str],
    human_evaluator_ids: Iterable[str],
    config: CalibrationConfig | None = None,
    materials_by_run: dict[str, dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Compare candidate evaluators against the human-human reference.

    The candidate passes only when it has positive agreement with both human
    raters and its mean agreement is no more than 0.15 below the human-human
    reference, separately over every rubric dimension.
    """

    policy = config or CalibrationConfig()
    materialized = list(rows)
    for row in materialized:
        validate_calibration_score(row)
    isolation: dict[str, Any] = {"verified": False, "reason": "No frozen pilot packets supplied."}
    if materials_by_run is not None:
        try:
            isolation = verify_study_scores(materialized, materials_by_run, "pilot")
        except StudyManifestError as error:
            raise EvaluationError(str(error)) from error
    human_ids = list(dict.fromkeys(str(item) for item in human_evaluator_ids))
    if len(human_ids) != 2:
        raise EvaluationError("Calibration requires exactly two human evaluator IDs.")
    candidates = list(dict.fromkeys(str(item) for item in candidate_models))
    if not candidates:
        raise EvaluationError("At least one candidate evaluator is required.")
    observed_ids = {str(row["evaluator_id"]) for row in materialized}
    missing_humans = set(human_ids) - observed_ids
    if missing_humans:
        raise EvaluationError(f"Missing human calibration scores: {sorted(missing_humans)}")

    seen = set()
    for row in materialized:
        key = (str(row["evaluator_id"]), _unit_key(row))
        if key in seen:
            raise EvaluationError(f"Duplicate calibration rating: {key}")
        seen.add(key)

    human_human = {
        dimension: _agreement(materialized, human_ids[0], human_ids[1], dimension, policy)
        for dimension in CALIBRATION_DIMENSIONS
    }
    candidate_reports: list[dict[str, Any]] = []
    for candidate in candidates:
        candidate_evaluator_ids = sorted(
            {
                str(row["evaluator_id"])
                for row in materialized
                if row.get("evaluator_kind") == "llm"
                and str(row.get("candidate_model")) == candidate
            }
        )
        if not candidate_evaluator_ids and candidate in observed_ids:
            candidate_evaluator_ids = [candidate]
        if len(candidate_evaluator_ids) != 1:
            candidate_reports.append(
                {
                    "candidate_model": candidate,
                    "candidate_evaluator_ids": candidate_evaluator_ids,
                    "dimensions": {},
                    "passes": False,
                    "mean_agreement": None,
                    "failure": (
                        "Expected exactly one evaluator identity for this candidate model."
                    ),
                }
            )
            continue
        candidate_evaluator_id = candidate_evaluator_ids[0]
        human_targets = {
            dimension: set(_unit_key(row) for row in materialized
                if row["evaluator_id"] == human_ids[0]
                and row["dimension"] == dimension
                and row.get("status", "assessable") == "assessable")
                & set(_unit_key(row) for row in materialized
                if row["evaluator_id"] == human_ids[1]
                and row["dimension"] == dimension
                and row.get("status", "assessable") == "assessable")
            for dimension in CALIBRATION_DIMENSIONS
        }
        candidate_numeric = {
            _unit_key(row) for row in materialized
            if row["evaluator_id"] == candidate_evaluator_id
            and row.get("status", "assessable") == "assessable"
        }
        common_rows = [row for row in materialized
                       if _unit_key(row) in human_targets[row["dimension"]]]
        by_human = {
            human_id: {
                dimension: _agreement(
                    common_rows,
                    human_id,
                    candidate_evaluator_id,
                    dimension,
                    policy,
                )
                for dimension in CALIBRATION_DIMENSIONS
            }
            for human_id in human_ids
        }
        dimensions: dict[str, Any] = {}
        passing = True
        means: list[float] = []
        for dimension in CALIBRATION_DIMENSIONS:
            reference = human_human[dimension].get("estimate")
            estimates = [
                by_human[human_id][dimension].get("estimate")
                for human_id in human_ids
            ]
            available = [float(value) for value in estimates if value is not None]
            mean = sum(available) / len(available) if available else None
            delta = mean - float(reference) if mean is not None and reference is not None else None
            # The paper's calibration rule compares every candidate with both
            # independent human raters. A partial overlap is not evidence that
            # the candidate is calibrated and must not pass by averaging only
            # the available side.
            complete_human_comparisons = len(available) == len(human_ids)
            complete_human_comparisons = complete_human_comparisons and bool(
                human_targets[dimension]
            ) and human_targets[dimension].issubset(candidate_numeric)
            reference_available = reference is not None and reference > 0
            positive = (
                complete_human_comparisons
                and min(available) > policy.minimum_positive_agreement
            )
            within_drop = (
                complete_human_comparisons
                and reference_available
                and delta is not None
                and delta >= -policy.maximum_agreement_drop
            )
            dimensions[dimension] = {
                "human_llm": by_human,
                "mean_agreement": mean,
                "human_human_reference": reference,
                "signed_difference": delta,
                "complete_human_comparisons": complete_human_comparisons,
                "reference_available": reference_available,
                "positive_with_both_humans": positive,
                "within_allowed_drop": within_drop,
            }
            passing = passing and positive and within_drop
            if mean is not None:
                means.append(mean)
        candidate_reports.append(
            {
                "candidate_model": candidate,
                "candidate_evaluator_ids": candidate_evaluator_ids,
                "dimensions": dimensions,
                "passes": passing,
                "mean_agreement": sum(means) / len(means) if means else None,
            }
        )

    dataset_reports: dict[str, dict[str, Any]] = {}
    if materials_by_run is not None:
        datasets = sorted({binding["dataset_name"] for binding in isolation["bindings"].values()})
        if len(datasets) > 1:
            for dataset in datasets:
                packets = {run_id: packet for run_id, packet in materials_by_run.items()
                           if isolation["bindings"][run_id]["dataset_name"] == dataset}
                dataset_reports[dataset] = calibrate_evaluators(
                    [row for row in materialized if str(row["run_id"]) in packets],
                    candidate_models=candidates, human_evaluator_ids=human_ids,
                    config=policy, materials_by_run=packets,
                )
            # A pooled agreement must never mask failure in one SE domain.
            for report in candidate_reports:
                domain_candidates = [next(item for item in result["candidates"]
                                          if item["candidate_model"] == report["candidate_model"])
                                     for result in dataset_reports.values()]
                report["passes"] = all(item["passes"] for item in domain_candidates)
                domain_means = [item["dimensions"][dimension]["mean_agreement"]
                                for item in domain_candidates
                                for dimension in CALIBRATION_DIMENSIONS]
                report["mean_agreement"] = (
                    sum(domain_means) / len(domain_means)
                    if domain_means and all(value is not None for value in domain_means)
                    else None
                )
                report["passes_by_dataset"] = {
                    dataset: next(item["passes"] for item in result["candidates"]
                                  if item["candidate_model"] == report["candidate_model"])
                    for dataset, result in dataset_reports.items()
                }
    for report in candidate_reports:
        call_costs = {}
        for row in materialized:
            if row.get("candidate_model") != report["candidate_model"]:
                continue
            metadata = row.get("evaluator_metadata", row.get("model_metadata", {}))
            calls = metadata.get("model_calls", [metadata])
            for call in calls:
                if call.get("call_id"):
                    call_costs[call["call_id"]] = call.get("estimated_cost_usd")
        report["calibration_cost_usd"] = (
            sum(call_costs.values()) if call_costs and all(
                value is not None for value in call_costs.values()) else None
        )
    passing_reports = sorted(
        [report for report in candidate_reports if report["passes"]],
        key=lambda report: (-float(report["mean_agreement"]),
                            report["calibration_cost_usd"]
                            if report["calibration_cost_usd"] is not None else float("inf"),
                            report["candidate_model"]),
    )
    selected = passing_reports[0]["candidate_model"] if passing_reports else None
    selected_models = [report["candidate_model"] for report in passing_reports[:policy.selected_model_count]]
    # Missing costs cannot resolve an exact tie at the retention boundary.
    boundary_tie_unresolved = False
    if len(passing_reports) > policy.selected_model_count:
        left, right = passing_reports[policy.selected_model_count - 1:policy.selected_model_count + 1]
        boundary_tie_unresolved = (left["mean_agreement"] == right["mean_agreement"]
                                  and (left["calibration_cost_usd"] is None
                                       or right["calibration_cost_usd"] is None
                                       or left["calibration_cost_usd"] == right["calibration_cost_usd"]))
    study_scope_complete = True
    if materials_by_run is not None:
        runs_by_dataset = defaultdict(list)
        for run_id, binding in isolation.get("bindings", {}).items():
            runs_by_dataset[binding["dataset_name"]].append(run_id)
        study_scope_complete = len(candidates) == 5 and len(runs_by_dataset) == 3 and all(
            len(run_ids) == 6 and all(sum(
                materials_by_run[run_id].get("review_policy", {}).get("setting") == setting
                for run_id in run_ids
            ) == 2 for setting in ("automatic", "selective", "full"))
            for run_ids in runs_by_dataset.values()
        )
    if len(selected_models) < policy.selected_model_count or boundary_tie_unresolved or not study_scope_complete:
        selected_models = []
    result = {
        "format": "coda-evaluator-calibration",
        "format_version": 2,
        "phase": "pilot",
        "human_evaluator_ids": human_ids,
        "candidate_models": candidates,
        "human_human_reference": human_human,
        "candidates": candidate_reports,
        "selected_candidate_model": selected,  # legacy diagnostic best candidate
        "selected_candidate_models": selected_models,
        "selection_status": "selected" if selected_models else "independent_human_evaluation_required",
        "selection_frozen": bool(selected_models) and materials_by_run is not None,
        "complete_study_scope": study_scope_complete,
        "exploratory": materials_by_run is None,
        "boundary_tie_unresolved": boundary_tie_unresolved,
        "by_dataset": dataset_reports,
        "dataset_scope": sorted({binding["dataset_name"] for binding in isolation.get("bindings", {}).values()}),
        "selected_models_by_dataset": {
            dataset: result["selected_candidate_model"] for dataset, result in dataset_reports.items()
        } if dataset_reports else {
            binding["dataset_name"]: selected for binding in isolation.get("bindings", {}).values()
        },
        "selection_rule": {
            "minimum_positive_agreement": policy.minimum_positive_agreement,
            "maximum_agreement_drop": policy.maximum_agreement_drop,
            "dimensions": list(CALIBRATION_DIMENSIONS),
            "selected_model_count": policy.selected_model_count,
            "ranking": "equal dataset-dimension macro average, then lower calibration API cost",
            "human_and_llm_use_same_rubric": True,
        },
        "workflow_isolation": {
            "scores_are_not_coding_records": True,
            "evaluator_output_does_not_update_codebook": True,
            "pilot_rows_excluded_from_formal_scores": True,
            "pilot_formal_material_isolation_verified": isolation["verified"],
        },
        "study_materials_verification": isolation,
    }
    result["selection_sha256"] = hashlib.sha256(json.dumps(result, sort_keys=True, allow_nan=False).encode()).hexdigest()
    return result


def validate_frozen_selection(selection: dict[str, Any], *, packet: dict[str, Any] | None = None,
                              human_fallback: bool = False) -> None:
    """Bind formal evaluators to the complete, unaltered pilot allocation."""
    body = {key: value for key, value in selection.items() if key != "selection_sha256"}
    actual = hashlib.sha256(json.dumps(body, sort_keys=True, allow_nan=False).encode()).hexdigest()
    if actual != selection.get("selection_sha256"):
        raise EvaluationError("Calibration selection checksum mismatch; regenerate it from the pilot scores.")
    if (not selection.get("complete_study_scope") or
            not selection.get("study_materials_verification", {}).get("verified")):
        raise EvaluationError("Evaluator selection requires all 18 study-bound pilot runs and five candidates.")
    if human_fallback:
        if selection.get("selection_status") != "independent_human_evaluation_required":
            raise EvaluationError("Human fallback was not selected by calibration.")
    elif not selection.get("selection_frozen") or len(set(selection.get("selected_candidate_models", []))) != 3:
        raise EvaluationError("Exactly three selected evaluator models must be frozen.")
    if packet is not None:
        binding = packet.get("study_materials") or {}
        pilot = selection['study_materials_verification'].get('bindings', {}).values()
        if not any(row.get('manifest_sha256') == binding.get('manifest_sha256')
                   and row.get('study_id') == binding.get('study_id')
                   and row.get('dataset_name') == binding.get('dataset_name') for row in pilot):
            raise EvaluationError("Evaluator selection belongs to a different study allocation.")
