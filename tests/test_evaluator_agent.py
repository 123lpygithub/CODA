from __future__ import annotations

import json
import unittest

from coda.agents.evaluator_agent import EvaluatorLLMAgent, build_blinded_evaluator_packet
from coda.llm import LLMModelConfig, LLMResponse


class FakeEvaluatorBackend:
    def __init__(self, payload: dict) -> None:
        self.payload = payload

    def generate(self, *, messages, config) -> LLMResponse:
        return LLMResponse(model=config.model, text=json.dumps(self.payload))


class TestEvaluatorAgent(unittest.TestCase):
    def test_evaluator_rejects_incomplete_codebook_scoring(self) -> None:
        agent = EvaluatorLLMAgent(
            model_config=LLMModelConfig(model="test-model"),
            backend=FakeEvaluatorBackend({"scores": [{
                "dimension": "clarity", "unit": "codebook", "score": 4,
                "status": "assessable", "rationale": "Clear.",
            }]}),
        )
        with self.assertRaisesRegex(Exception, "every requested unit"):
            agent(packet={"evaluation_scope": "codebook_only"}, run_id="r", evaluator_id="e")

    def test_evaluator_input_hides_operational_provenance(self) -> None:
        packet = {
            "run_id": "full-review-run", "review_policy": {"setting": "full"},
            "codebook": {"codes": [{"code_id": "c", "name": "C", "metadata": {"human_reviewed": True}}]},
            "artifacts": [{
                "artifact_id": "a", "content": "Original source.",
                "agent_trace": {"model": "coding-model"},
                "coding_record": {"final_code_ids": ["c"], "rationale": "Supported.", "metadata": {"human_reviewed": True}, "decision": "accept"},
            }],
        }
        blinded = build_blinded_evaluator_packet(packet)
        serialized = json.dumps(blinded)
        for value in ("full-review-run", "human_reviewed", "agent_trace", "coding-model", '"decision"'):
            self.assertNotIn(value, serialized)
        self.assertEqual(blinded["artifacts"][0]["content"], "Original source.")
        self.assertEqual(blinded["artifacts"][0]["coding_record"]["final_code_ids"], ["c"])

    def test_evaluator_emits_valid_rows_without_mutating_packet(self) -> None:
        packet = {
            "run_id": "run-frozen",
            "codebook": {"version": 2, "codes": []},
            "artifacts": [],
        }
        payload = {
            "scores": [
                {
                    "dimension": "clarity",
                    "unit": "codebook",
                    "score": 4,
                    "status": "assessable",
                    "rationale": "Definitions are understandable.",
                }
            ]
        }
        agent = EvaluatorLLMAgent(
            model_config=LLMModelConfig(model="test-model"),
            backend=FakeEvaluatorBackend(payload),
        )
        rows = agent(
            packet=packet,
            run_id="run-frozen",
            evaluator_id="candidate-a",
            phase="pilot",
            candidate_model="test-model",
        )
        self.assertEqual(rows[0]["run_id"], "run-frozen")
        self.assertEqual(rows[0]["evaluator_id"], "candidate-a")
        self.assertEqual(rows[0]["phase"], "pilot")
        self.assertEqual(rows[0]["candidate_model"], "test-model")
        self.assertEqual(packet["codebook"]["version"], 2)

    def test_evaluator_rejects_assignment_without_identifiers(self) -> None:
        agent = EvaluatorLLMAgent(
            model_config=LLMModelConfig(model="test-model"),
            backend=FakeEvaluatorBackend(
                {
                    "scores": [
                        {
                            "dimension": "evidence_support",
                            "unit": "assignment",
                            "score": 2,
                            "status": "assessable",
                            "rationale": "Supported.",
                        }
                    ]
                }
            ),
        )
        with self.assertRaises(Exception):
            agent(packet={}, run_id="run-frozen", evaluator_id="candidate-a")


if __name__ == "__main__":
    unittest.main()
