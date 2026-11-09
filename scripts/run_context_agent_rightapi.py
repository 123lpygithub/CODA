from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from adapters.static_analysis import StaticAnalysisNondeterminismAdapter
from coda.agents import ContextLLMAgent
from coda.contracts import ContextAgentInput
from coda.llm import LLMModelConfig, load_chat_backend
from coda.state import CodebookState, HistoryState, ResearchQuestionState


def main() -> None:
    adapter = StaticAnalysisNondeterminismAdapter()
    metadata = adapter.load_dataset_metadata()
    artifact = next(iter(adapter.iter_artifacts()))

    model_config = LLMModelConfig.from_env(
        default_provider="rightapi",
        default_model="gpt-5.6-sol",
        default_temperature=0.0,
        default_max_output_tokens=900,
    )
    backend = load_chat_backend(model_config)
    agent = ContextLLMAgent(
        model_config=model_config,
        backend=backend,
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
        print(f"evidence_{index}_rationale:", item.rationale)
    print("missing_context_warnings:", packet.missing_context_warnings)
    print("distracting_information:", packet.distracting_information)
    print("model_metadata:", packet.model_metadata)


if __name__ == "__main__":
    main()
