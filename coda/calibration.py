"""Offline calibration helpers for CODA's frozen selective-review policy."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Literal


RiskAggregation = Literal["sum", "max"]


@dataclass(frozen=True)
class CalibrationCase:
    artifact_id: str
    risk_signals: tuple[str, ...]
    should_review: bool


def calculate_risk_score(
    weighted_risks: dict[str, int],
    aggregation: RiskAggregation,
) -> int:
    """Calculate a deterministic score from unique observable risk signals."""

    if aggregation == "max":
        return max(weighted_risks.values(), default=0)
    if aggregation == "sum":
        return sum(weighted_risks.values())
    raise ValueError("aggregation must be 'sum' or 'max'.")


def evaluate_thresholds(
    cases: Iterable[CalibrationCase],
    *,
    risk_weights: dict[str, int],
    thresholds: Iterable[int],
    aggregation: RiskAggregation = "sum",
) -> list[dict[str, float | int]]:
    """Report pilot review burden and risky-case recall without changing policy."""

    frozen_cases = list(cases)
    risky_total = sum(1 for case in frozen_cases if case.should_review)
    rows: list[dict[str, float | int]] = []
    for threshold in thresholds:
        if threshold < 1:
            raise ValueError("Calibration thresholds must be positive.")
        selected = [
            case
            for case in frozen_cases
            if calculate_risk_score(
                {
                    signal: risk_weights.get(signal, 0)
                    for signal in set(case.risk_signals)
                },
                aggregation,
            )
            >= threshold
        ]
        selected_ids = {case.artifact_id for case in selected}
        caught = sum(
            1
            for case in frozen_cases
            if case.should_review and case.artifact_id in selected_ids
        )
        missed = risky_total - caught
        total = len(frozen_cases)
        rows.append(
            {
                "threshold": threshold,
                "review_count": len(selected),
                "review_rate": len(selected) / total if total else 0.0,
                "risky_case_count": risky_total,
                "risky_case_recall": caught / risky_total if risky_total else 1.0,
                "miss_count": missed,
                "miss_rate": missed / risky_total if risky_total else 0.0,
            }
        )
    return rows
