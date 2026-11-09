from __future__ import annotations

import unittest

from coda.calibration import CalibrationCase, evaluate_thresholds
from coda.semantic_retrieval import rank_semantic_impacts


class TestCalibrationAndRetrieval(unittest.TestCase):
    def test_threshold_report_exposes_recall_and_review_burden(self) -> None:
        cases = [
            CalibrationCase("a", ("missing_context",), True),
            CalibrationCase("b", ("moderate_confidence",), False),
            CalibrationCase(
                "c",
                ("moderate_confidence", "coder_disagreement"),
                True,
            ),
        ]

        rows = evaluate_thresholds(
            cases,
            risk_weights={
                "missing_context": 3,
                "moderate_confidence": 1,
                "coder_disagreement": 2,
            },
            thresholds=[2, 3, 4],
        )

        self.assertEqual(rows[1]["threshold"], 3)
        self.assertEqual(rows[1]["review_count"], 2)
        self.assertEqual(rows[1]["risky_case_recall"], 1.0)
        self.assertEqual(rows[2]["miss_count"], 2)

    def test_semantic_retrieval_returns_explainable_ranked_matches(self) -> None:
        matches = rank_semantic_impacts(
            "unsafe mutable collection traversal",
            {
                "a": "failure while traversing a mutable collection",
                "b": "documentation typo in command help",
                "c": "safe snapshot traversal over collection values",
            },
            top_k=2,
            minimum_score=0.01,
        )

        self.assertEqual(len(matches), 2)
        self.assertEqual(matches[0].document_id, "a")
        self.assertIn("collection", matches[0].shared_terms)


if __name__ == "__main__":
    unittest.main()
