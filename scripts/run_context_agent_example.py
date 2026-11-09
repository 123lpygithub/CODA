from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from adapters.static_analysis import StaticAnalysisNondeterminismAdapter
from coda.agents import ContextLLMAgent
from coda.contracts import ContextAgentInput
from coda.llm import LLMModelConfig, LLMResponse
from coda.state import CodebookState, HistoryState, ResearchQuestionState


class FakeBackend:
    """Small deterministic backend for the first Context Agent example."""

    def generate(self, *, messages, config):
        del messages
        del config
        return LLMResponse(
            model="fake-context-model",
            text="""
            {
              "context_brief": "This artifact centers on exception-path handling and a concurrent modification problem in a static analysis tool.",
              "evidence_items": [
                {
                  "field_name": "issue/commit content",
                  "excerpt": "do not follow exceptional paths and fix concurrent modification exception by using exceptional graph",
                  "rationale": "The commit summary names the behavior under analysis and the intended repair."
                },
                {
                  "field_name": "issue/commit content",
                  "excerpt": "Collection<Unit> handlerUnits = findLocalHandler(body, ex, stmt);",
                  "rationale": "The changed declaration points to exception-handler processing as the concrete implementation site."
                }
              ],
              "missing_context_warnings": [
                "No standalone bug report narrative or reproducer is included."
              ],
              "distracting_information": [
                "Some line edits are mechanical and may not matter for the root-cause interpretation."
              ]
            }
            """,
        )


def main() -> None:
    adapter = StaticAnalysisNondeterminismAdapter()
    metadata = adapter.load_dataset_metadata()
    artifact = next(iter(adapter.iter_artifacts()))

    agent = ContextLLMAgent(
        model_config=LLMModelConfig(model="fake-context-model", provider="custom"),
        backend=FakeBackend(),
    )
    packet = agent(
        ContextAgentInput(
            artifact=artifact,
            research_question=ResearchQuestionState.from_dataset_metadata(metadata),
            codebook=CodebookState.empty(metadata.dataset_name),
            history=HistoryState(),
        )
    )

    print("artifact_id:", packet.artifact_id)
    print("context_brief:", packet.context_brief)
    print("evidence_count:", len(packet.evidence_items))
    for index, item in enumerate(packet.evidence_items, start=1):
        print(f"evidence_{index}_field:", item.field_name)
        print(f"evidence_{index}_excerpt:", item.excerpt)
        print(f"evidence_{index}_locator:", item.locator)
    print("missing_context_warnings:", packet.missing_context_warnings)
    print("distracting_information:", packet.distracting_information)


if __name__ == "__main__":
    main()
