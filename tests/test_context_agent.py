from __future__ import annotations

import unittest

from adapters.base import ArtifactRecord
from adapters.static_analysis import StaticAnalysisNondeterminismAdapter
from coda.agents import ContextLLMAgent
from coda.agents.base import AgentExecutionError
from coda.agents.context_agent import ContextAgentSettings
from coda.contracts import ContextAgentInput
from coda.llm import LLMModelConfig, LLMResponse
from coda.state import CodebookState, ContextRequestState, HistoryState, ResearchQuestionState


class FakeBackend:
    last_messages = None

    def generate(self, *, messages, config):
        self.last_messages = messages
        del config
        return LLMResponse(
            model="fake-model",
            text="""
            {
              "context_brief": "The artifact discusses exception-path handling in a static analysis tool.",
              "evidence_items": [
                {
                  "field_name": "issue/commit content",
                  "excerpt": "do not follow exceptional paths and fix concurrent modification exception by using exceptional graph",
                  "rationale": "This sentence states the problem focus and the intended fix direction."
                },
                {
                  "field_name": "issue/commit content",
                  "excerpt": "Collection<Unit> handlerUnits = findLocalHandler(body, ex, stmt);",
                  "rationale": "This code change shows the implementation point related to exception handling."
                }
              ],
              "missing_context_warnings": [
                "The artifact does not show a failing execution trace or reproducer."
              ],
              "distracting_information": [
                "Import and formatting edits may be secondary to the root-cause analysis."
              ]
            }
            """,
        )


class EvidenceCountBackend:
    def __init__(self, evidence_count: int) -> None:
        self.evidence_count = evidence_count

    def generate(self, *, messages, config):
        del messages, config
        evidence_items = [
            {
                "field_name": "body",
                "excerpt": f"evidence-{index}",
                "rationale": "Relevant visible evidence.",
            }
            for index in range(self.evidence_count)
        ]
        return LLMResponse(
            model="fake-model",
            text=__import__("json").dumps(
                {
                    "context_brief": "Context.",
                    "evidence_items": evidence_items,
                    "missing_context_warnings": [],
                    "distracting_information": [],
                }
            ),
        )


class TestContextAgent(unittest.TestCase):
    def test_context_agent_builds_grounded_context_packet(self) -> None:
        adapter = StaticAnalysisNondeterminismAdapter()
        metadata = adapter.load_dataset_metadata()
        artifact = next(iter(adapter.iter_artifacts()))
        agent = ContextLLMAgent(
            model_config=LLMModelConfig(model="fake-model", provider="custom"),
            backend=FakeBackend(),
        )

        packet = agent(
            ContextAgentInput(
                artifact=artifact,
                research_question=ResearchQuestionState.from_dataset_metadata(metadata),
            )
        )

        self.assertEqual(packet.artifact_id, artifact.artifact_id)
        self.assertIn("exception-path handling", packet.context_brief)
        self.assertEqual(len(packet.evidence_items), 2)
        self.assertEqual(
            packet.evidence_items[0].field_name,
            "issue/commit content",
        )
        self.assertIsNotNone(packet.evidence_items[0].locator)
        self.assertEqual(
            packet.evidence_items[0].source_ref.value,
            artifact.source_refs[0].value,
        )
        self.assertEqual(len(packet.missing_context_warnings), 1)
        self.assertEqual(len(packet.distracting_information), 1)
        self.assertEqual(packet.model_metadata["agent"], "context_agent")

    def test_context_agent_receives_reopened_material_and_state_signals(self) -> None:
        adapter = StaticAnalysisNondeterminismAdapter()
        metadata = adapter.load_dataset_metadata()
        artifact = next(iter(adapter.iter_artifacts()))
        backend = FakeBackend()
        history = HistoryState()
        history.context_requests.append(
            ContextRequestState(
                request_id="context-request-test",
                scope="artifact",
                artifact_id=artifact.artifact_id,
                reason="The failing trace is missing.",
                requested_items=["The failing trace"],
                created_at_codebook_version=0,
            )
        )
        agent = ContextLLMAgent(
            model_config=LLMModelConfig(model="fake-model", provider="custom"),
            backend=backend,
        )

        agent(
            ContextAgentInput(
                artifact=artifact,
                research_question=ResearchQuestionState.from_dataset_metadata(metadata),
                additional_context=["The failing trace shows a mutable collection update."],
            )
        )

        rendered = "\n".join(message.content for message in backend.last_messages or [])
        self.assertIn("The failing trace shows a mutable collection update.", rendered)
        # The Context Agent may use resolved material, but must not receive
        # request ids or other historical state that could anchor coding.
        self.assertNotIn("context-request-test", rendered)

    def test_long_material_allows_more_grounded_evidence_items(self) -> None:
        content = " ".join(f"evidence-{index}" for index in range(6)) + " " + ("x" * 80)
        artifact = ArtifactRecord("long", content, {"body": content})
        agent = ContextLLMAgent(
            model_config=LLMModelConfig(model="fake-model", provider="custom"),
            backend=EvidenceCountBackend(6),
            settings=ContextAgentSettings(
                base_evidence_items=4,
                maximum_evidence_items=6,
                characters_per_extra_evidence=20,
            ),
        )
        metadata = StaticAnalysisNondeterminismAdapter().load_dataset_metadata()

        packet = agent(
            ContextAgentInput(
                artifact=artifact,
                research_question=ResearchQuestionState.from_dataset_metadata(metadata),
            )
        )

        self.assertEqual(len(packet.evidence_items), 6)
        self.assertEqual(
            packet.model_metadata["context_construction"]["max_evidence_items"],
            6,
        )

    def test_short_material_rejects_evidence_above_its_limit(self) -> None:
        content = " ".join(f"evidence-{index}" for index in range(5))
        artifact = ArtifactRecord("short", content, {"body": content})
        agent = ContextLLMAgent(
            model_config=LLMModelConfig(model="fake-model", provider="custom"),
            backend=EvidenceCountBackend(5),
            settings=ContextAgentSettings(
                base_evidence_items=4,
                maximum_evidence_items=6,
                characters_per_extra_evidence=1000,
            ),
        )
        metadata = StaticAnalysisNondeterminismAdapter().load_dataset_metadata()

        with self.assertRaisesRegex(AgentExecutionError, "at most 4"):
            agent(
                ContextAgentInput(
                    artifact=artifact,
                    research_question=ResearchQuestionState.from_dataset_metadata(metadata),
                )
            )


if __name__ == "__main__":
    unittest.main()
