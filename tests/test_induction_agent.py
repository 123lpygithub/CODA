from __future__ import annotations

import json
import unittest

from coda.agents.induction_agent import InductionLLMAgent
from coda.contracts import (
    CoderAgentOutput,
    ContextPacket,
    EvidenceItem,
    InductionAgentInput,
    InitialCodingCase,
    ProvisionalCode,
)
from coda.llm import LLMMessage, LLMModelConfig, LLMResponse
from coda.state import ResearchQuestionState


class _InductionBackend:
    def __init__(self) -> None:
        self.messages: list[LLMMessage] = []

    def generate(self, *, messages, config) -> LLMResponse:
        self.messages = list(messages)
        payload = {
            "codes": [
                {
                    "code_id": "unstable-analysis-traversal",
                    "name": "Unstable analysis traversal",
                    "name_zh": "不稳定的分析遍历",
                    "definition": "Analysis fails while traversing mutable state.",
                    "definition_zh": "分析在遍历可变状态时失败。",
                    "inclusion_criteria": ["Failure occurs during traversal."],
                    "exclusion_criteria": ["Unrelated parser failures."],
                    "inclusion_criteria_zh": ["故障发生在遍历期间。"],
                    "exclusion_criteria_zh": ["与解析器无关的故障。"],
                    "representative_artifact_ids": ["a-1"],
                    "boundary_artifact_ids": [],
                    "counterexample_status": "no_observed_counterexample",
                    "hypothetical_examples": [
                        "A parser-only failure would remain outside this code."
                    ],
                    "evidence_summary": "Both readings cite the traversal failure.",
                    "source_provisional_codes": ["unsafe traversal", "mutable walk"],
                    "parent_code_id": None,
                }
            ],
            "change_log": [{"action": "add", "summary": "Induce one shared concept."}],
            "analytic_memos": [
                {
                    "summary": "Wording differs but the evidenced boundary agrees.",
                    "artifact_ids": ["a-1"],
                    "source_code_names": ["unsafe traversal", "mutable walk"],
                }
            ],
        }
        return LLMResponse(model=config.model, text=json.dumps(payload))


class TestInductionAgent(unittest.TestCase):
    def test_induces_from_both_independent_outputs_with_provenance(self) -> None:
        backend = _InductionBackend()
        evidence = EvidenceItem(field_name="content", excerpt="iteration failed")
        context = ContextPacket(
            artifact_id="a-1",
            context_brief="Traversal failure.",
            evidence_items=[evidence],
        )
        outputs = [
            CoderAgentOutput(
                artifact_id="a-1",
                coder_id=coder_id,
                provisional_codes=[
                    ProvisionalCode(
                        code_name=code_name,
                        short_definition="Failure while traversing mutable state.",
                        supporting_evidence=[evidence],
                        relationship_to_codebook="new_code",
                    )
                ],
            )
            for coder_id, code_name in [
                ("initial-coder-a", "unsafe traversal"),
                ("initial-coder-b", "mutable walk"),
            ]
        ]
        question = ResearchQuestionState(
            dataset_name="test",
            question_text="What failure mechanisms occur?",
            analysis_scope="Issue reports",
            use_case="failure analysis",
            artifact_unit="issue",
        )
        agent = InductionLLMAgent(
            model_config=LLMModelConfig(model="induction-test", json_mode=False),
            backend=backend,
        )

        result = agent(
            InductionAgentInput(
                research_question=question,
                cases=[InitialCodingCase("a-1", context, outputs)],
                allowed_artifact_ids=["a-1"],
                induction_stage="global_consolidation",
            )
        )

        self.assertEqual(result.codes[0].metadata["origin"], "llm_initial_induction")
        self.assertEqual(
            result.codes[0].metadata["source_provisional_codes"],
            ["unsafe traversal", "mutable walk"],
        )
        self.assertEqual(result.model_metadata["model"], "induction-test")
        self.assertEqual(result.model_metadata["induction_stage"], "global_consolidation")
        self.assertEqual(
            result.codes[0].counterexample_status,
            "no_observed_counterexample",
        )
        self.assertEqual(result.codes[0].boundary_artifact_ids, [])
        self.assertEqual(len(result.codes[0].hypothetical_examples), 1)
        self.assertEqual(result.codes[0].metadata["created_at_codebook_version"], 1)
        self.assertEqual(
            result.codes[0].metadata["inclusion_criteria_zh"],
            ["故障发生在遍历期间。"],
        )
        self.assertEqual(
            result.codes[0].metadata["exclusion_criteria_zh"],
            ["与解析器无关的故障。"],
        )
        rendered_prompt = backend.messages[-1].content
        normalized_prompt = " ".join(rendered_prompt.split())
        self.assertIn("Induction stage: global_consolidation", normalized_prompt)
        self.assertIn("initial-coder-a", normalized_prompt)
        self.assertIn("initial-coder-b", normalized_prompt)
        self.assertIn("perform a granularity audit", normalized_prompt)
        self.assertIn("analytical-axis audit", normalized_prompt)
        self.assertIn("independently meaningful units", normalized_prompt)
        self.assertIn("observation-level candidate", normalized_prompt)
        self.assertIn("no accidental one-to-one promotion", normalized_prompt)


if __name__ == "__main__":
    unittest.main()
