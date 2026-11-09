from __future__ import annotations

import unittest

from adapters.base import ArtifactRecord
from coda.agents import (
    ContextAgentSettings,
    ContextLLMAgent,
    build_open_coder,
)
from coda.agents.common import (
    normalize_codebook_relationship,
    normalize_confidence_factor,
)
from coda.contracts import ContextAgentInput, CoderAgentInput
from coda.llm import LLMModelConfig, LLMResponse
from coda.state import CodeState, CodebookState, HistoryState, ResearchQuestionState


class FakeContextBackend:
    def generate(self, *, messages, config):
        del messages
        del config
        return LLMResponse(
            model="fake-context-model",
            text="""
            {
              "context_brief": "The artifact discusses exception-path handling and concurrent modification.",
              "evidence_items": [
                {
                  "field_name": "issue/commit content",
                  "excerpt": "do not follow exceptional paths and fix concurrent modification exception by using exceptional graph",
                  "rationale": "The summary line identifies the main issue."
                },
                {
                  "field_name": "issue/commit content",
                  "excerpt": "Iterator<Unit> unitIt = body.getUnits().snapshotIterator();",
                  "rationale": "This line shows the snapshot-iteration fix."
                }
              ],
              "missing_context_warnings": [],
              "distracting_information": []
            }
            """,
        )


class FakeCoderBackend:
    def __init__(self) -> None:
        self.user_prompts: list[str] = []

    def generate(self, *, messages, config):
        del config
        user_prompt = messages[-1].content
        self.user_prompts.append(user_prompt)
        text = """
            {
              "provisional_codes": [
                {
                  "code_name": "Exceptional Path Control",
                  "short_definition": "The artifact suggests the tool followed or modeled exceptional paths in a way that destabilized the analysis.",
                  "supporting_evidence_refs": ["E1"],
                  "relationship_to_codebook": "uncertain",
                  "linked_code_ids": [],
                  "alternative_interpretation": "The issue might still belong under a broader traversal-instability code.",
                  "uncertainty_note": "The exact boundary with concurrent-modification concerns remains fuzzy.",
                  "proposed_codebook_action": "no_change",
                  "proposed_codebook_target_ids": []
                }
              ],
              "insufficient_context": false,
              "overall_uncertainty": "moderate",
              "confidence_level": "high",
              "confidence_rationale": "The visible evidence supports a stable descriptive reading.",
              "confidence_factors": {
                "evidence_support": "strong",
                "context_sufficiency": "sufficient",
                "codebook_fit": "not applicable",
                "interpretive_ambiguity": "low"
              },
              "notes": ["The current codebook may be too broad for this case."]
            }
            """
        return LLMResponse(model="fake-coder-model", text=text)


class MissingLinkageCoderBackend:
    def generate(self, *, messages, config):
        del messages
        del config
        return LLMResponse(
            model="fake-coder-model",
            text='''
            {
              "provisional_codes": [{
                "code_name": "New concept",
                "short_definition": "A concept not represented by the current codebook.",
                "supporting_evidence_refs": ["E1"],
                "relationship_to_codebook": "uncertain",
                "alternative_interpretation": "",
                "uncertainty_note": "",
                "proposed_codebook_action": "no_change",
                "proposed_codebook_target_ids": []
              }],
              "insufficient_context": false,
              "overall_uncertainty": "low",
              "confidence_level": "medium",
              "confidence_rationale": "The evidence supports a provisional reading.",
              "confidence_factors": {
                "evidence_support": "direct",
                "context_sufficiency": "moderate",
                "codebook_fit": "n/a",
                "interpretive_ambiguity": "medium"
              },
              "notes": []
            }
            ''',
        )


class TestCoderAgents(unittest.TestCase):
    def test_normalize_common_relationship_variants(self) -> None:
        self.assertEqual(
            normalize_codebook_relationship("new code"),
            "new_code",
        )
        self.assertEqual(
            normalize_codebook_relationship("Reuse"),
            "reuse_existing_code",
        )
        self.assertEqual(
            normalize_codebook_relationship("merge-existing-code"),
            "merge_existing_codes",
        )
        self.assertEqual(
            normalize_codebook_relationship("新增代码"),
            "new_code",
        )
        self.assertEqual(
            normalize_codebook_relationship("add parent"),
            "add_parent_code",
        )

    def test_normalize_common_confidence_factor_variants(self) -> None:
        self.assertEqual(normalize_confidence_factor("strong"), "high")
        self.assertEqual(normalize_confidence_factor("sufficient"), "high")
        self.assertEqual(normalize_confidence_factor("moderate"), "medium")
        self.assertEqual(normalize_confidence_factor("weak"), "low")
        self.assertEqual(normalize_confidence_factor("not applicable"), "not_applicable")
        with self.assertRaises(ValueError):
            normalize_confidence_factor("fairly convincing")

    def _build_context_packet(self):
        artifact = ArtifactRecord(
            artifact_id="artifact-1",
            content=(
                "Issue/Commit Content:\n"
                "do not follow exceptional paths and fix concurrent modification exception by using exceptional graph\n"
                "Iterator<Unit> unitIt = body.getUnits().snapshotIterator();\n"
            ),
            raw_fields={
                "issue/commit content": (
                    "do not follow exceptional paths and fix concurrent modification exception by using exceptional graph\n"
                    "Iterator<Unit> unitIt = body.getUnits().snapshotIterator();\n"
                )
            },
            source_refs=[],
        )
        metadata_like = type(
            "MetadataLike",
            (),
            {
                "dataset_name": "demo",
                "research_question": "What root-cause categories explain the issue?",
                "data_description": "Demo data",
                "use_case": "Demo use case",
                "artifact_unit": "One artifact",
            },
        )()
        research_question = ResearchQuestionState.from_dataset_metadata(metadata_like)
        context_agent = ContextLLMAgent(
            model_config=LLMModelConfig(model="fake-context", provider="custom"),
            backend=FakeContextBackend(),
            settings=ContextAgentSettings(raw_field_char_limit=400),
        )
        packet = context_agent(
            ContextAgentInput(
                artifact=artifact,
                research_question=research_question,
            )
        )
        return artifact, research_question, packet

    def test_two_blind_coders_do_not_receive_codebook_or_history(self) -> None:
        artifact, research_question, context_packet = self._build_context_packet()
        codebook = CodebookState(
            dataset_name="demo",
            version=1,
            codes=[
                CodeState(
                    code_id="code-existing",
                    name="Analysis Traversal Instability",
                    definition="Existing broad code.",
                )
            ],
        )
        history = HistoryState()
        backend = FakeCoderBackend()

        coder_a = build_open_coder(
            model_config=LLMModelConfig(model="gpt-6.1-sol", provider="custom"),
            backend=backend,
        )
        coder_b = build_open_coder(
            model_config=LLMModelConfig(model="gpt-5.6-sol", provider="custom"),
            backend=backend,
        )

        first_output = coder_a(
            CoderAgentInput(
                artifact=artifact,
                research_question=research_question,
                context_packet=context_packet,
                coder_id="coder-a",
            )
        )
        second_output = coder_b(
            CoderAgentInput(
                artifact=artifact,
                research_question=research_question,
                context_packet=context_packet,
                coder_id="coder-b",
            )
        )

        self.assertEqual(first_output.coder_id, "coder-a")
        self.assertEqual(second_output.coder_id, "coder-b")
        self.assertEqual(first_output.provisional_codes[0].relationship_to_codebook, "uncertain")
        self.assertEqual(second_output.provisional_codes[0].relationship_to_codebook, "uncertain")
        self.assertEqual(
            first_output.provisional_codes[0].supporting_evidence[0].excerpt,
            context_packet.evidence_items[0].excerpt,
        )
        self.assertEqual(second_output.provisional_codes[0].proposed_codebook_action, "no_change")
        self.assertEqual(
            first_output.confidence_factors,
            {
                "evidence_support": "high",
                "context_sufficiency": "high",
                "codebook_fit": "not_applicable",
                "interpretive_ambiguity": "low",
            },
        )
        self.assertEqual(first_output.model_metadata["perspective"], "blind_open_coding")
        self.assertEqual(second_output.model_metadata["perspective"], "blind_open_coding")
        self.assertEqual(first_output.model_metadata["model"], "gpt-6.1-sol")
        self.assertEqual(second_output.model_metadata["model"], "gpt-5.6-sol")
        self.assertEqual(len(backend.user_prompts), 2)
        for prompt in backend.user_prompts:
            self.assertNotIn("Current Codebook Snapshot", prompt)
            self.assertNotIn("Recent Reviewed History", prompt)
            self.assertNotIn("code-existing", prompt)
            normalized_prompt = " ".join(prompt.split())
            self.assertIn("evidence-near provisional labels", normalized_prompt)
            self.assertIn(
                "Do not deliberately broaden a candidate",
                normalized_prompt,
            )
            self.assertIn("reusable codebook category or parent theme is too broad", normalized_prompt)
            self.assertIn("single analytical question", normalized_prompt)
            self.assertIn("independent-resolution test", normalized_prompt)
            self.assertIn(
                "differs from the reference",
                normalized_prompt,
            )

    def test_missing_linked_code_ids_defaults_to_empty_for_new_code(self) -> None:
        artifact, research_question, context_packet = self._build_context_packet()
        coder = build_open_coder(
            model_config=LLMModelConfig(model="fake-coder", provider="custom"),
            backend=MissingLinkageCoderBackend(),
        )
        output = coder(
            CoderAgentInput(
                artifact=artifact,
                research_question=research_question,
                context_packet=context_packet,
                coder_id="coder-b",
            )
        )
        self.assertEqual(output.provisional_codes[0].linked_code_ids, [])


if __name__ == "__main__":
    unittest.main()
