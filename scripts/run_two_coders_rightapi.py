from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from adapters.static_analysis import StaticAnalysisNondeterminismAdapter
from coda.agents import (
    ContextLLMAgent,
    build_open_coder,
)
from coda.contracts import ContextAgentInput, CoderAgentInput
from coda.llm import LLMModelConfig, load_chat_backend
from coda.state import CodebookState, HistoryState, ResearchQuestionState


def main() -> None:
    adapter = StaticAnalysisNondeterminismAdapter()
    metadata = adapter.load_dataset_metadata()
    artifact = next(iter(adapter.iter_artifacts()))
    research_question = ResearchQuestionState.from_dataset_metadata(metadata)
    codebook = CodebookState.empty(metadata.dataset_name)
    history = HistoryState()

    model_config = LLMModelConfig.from_env(
        default_provider="rightapi",
        default_model="gpt-5.6-sol",
        default_temperature=0.0,
        default_max_output_tokens=1000,
    )
    backend = load_chat_backend(model_config)

    context_agent = ContextLLMAgent(
        model_config=model_config,
        backend=backend,
    )
    context_packet = context_agent(
        ContextAgentInput(
            artifact=artifact,
            research_question=research_question,
            codebook=codebook,
            history=history,
        )
    )

    coder_a = build_open_coder(
        model_config=LLMModelConfig.from_env(
            default_provider="rightapi",
            default_model="gpt-6.1-sol",
            default_temperature=0.0,
            default_max_output_tokens=1000,
        ),
        backend=backend,
    )
    coder_b = build_open_coder(
        model_config=LLMModelConfig.from_env(
            default_provider="rightapi",
            default_model="gpt-5.6-sol",
            default_temperature=0.0,
            default_max_output_tokens=1000,
        ),
        backend=backend,
    )

    for coder_id, coder in [
        ("coder-a", coder_a),
        ("coder-b", coder_b),
    ]:
        output = coder(
            CoderAgentInput(
                artifact=artifact,
                research_question=research_question,
                context_packet=context_packet,
                coder_id=coder_id,
            )
        )
        print("=" * 80)
        print("coder_id:", output.coder_id)
        print("insufficient_context:", output.insufficient_context)
        print("overall_uncertainty:", output.overall_uncertainty)
        print("notes:", output.notes)
        for index, code in enumerate(output.provisional_codes, start=1):
            print(f"code_{index}_name:", code.code_name)
            print(f"code_{index}_definition:", code.short_definition)
            print(f"code_{index}_relationship:", code.relationship_to_codebook)
            print(f"code_{index}_linked_ids:", code.linked_code_ids)
            print(f"code_{index}_action:", code.proposed_codebook_action)
            print(
                f"code_{index}_evidence:",
                [item.excerpt for item in code.supporting_evidence],
            )
        print("model_metadata:", output.model_metadata)


if __name__ == "__main__":
    main()
