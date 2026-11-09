from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from adapters.static_analysis import StaticAnalysisNondeterminismAdapter
from coda.agents import (
    ArbitrationLLMAgent,
    ContextLLMAgent,
    ValidationLLMAgent,
    build_open_coder,
)
from coda.contracts import ArbitrationInput, ContextAgentInput, CoderAgentInput, ValidationInput
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
        default_max_output_tokens=1200,
    )
    backend = load_chat_backend(model_config)

    context_agent = ContextLLMAgent(
        model_config=model_config,
        backend=backend,
    )
    coder_a = build_open_coder(
        model_config=LLMModelConfig.from_env(
            default_provider="rightapi",
            default_model="gpt-6.1-sol",
            default_temperature=0.0,
            default_max_output_tokens=1200,
        ),
        backend=backend,
    )
    coder_b = build_open_coder(
        model_config=LLMModelConfig.from_env(
            default_provider="rightapi",
            default_model="gpt-5.6-sol",
            default_temperature=0.0,
            default_max_output_tokens=1200,
        ),
        backend=backend,
    )
    arbitration_agent = ArbitrationLLMAgent(
        model_config=model_config,
        backend=backend,
    )
    validation_agent = ValidationLLMAgent(
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
    coder_outputs = []
    for coder_id, coder in [
        ("coder-a", coder_a),
        ("coder-b", coder_b),
    ]:
        coder_outputs.append(
            coder(
                CoderAgentInput(
                    artifact=artifact,
                    research_question=research_question,
                    context_packet=context_packet,
                    coder_id=coder_id,
                )
            )
        )

    arbitration_output = arbitration_agent(
        ArbitrationInput(
            artifact=artifact,
            research_question=research_question,
            context_packet=context_packet,
            coder_outputs=coder_outputs,
            codebook=codebook,
            history=history,
        )
    )
    validation_output = validation_agent(
        ValidationInput(
            artifact=artifact,
            research_question=research_question,
            context_packet=context_packet,
            coder_outputs=coder_outputs,
            arbitration_output=arbitration_output,
            codebook=codebook,
            history=history,
        )
    )

    print("artifact_id:", artifact.artifact_id)
    print("context_brief:", context_packet.context_brief)
    print("=" * 80)
    print("agreement_summary:", arbitration_output.agreement_summary)
    print("disagreement_summary:", arbitration_output.disagreement_summary)
    print("recommended_codes:", len(arbitration_output.recommended_codes))
    for index, code in enumerate(arbitration_output.recommended_codes, start=1):
        print(f"recommended_{index}_name:", code.code_name)
        print(f"recommended_{index}_relationship:", code.relationship_to_codebook)
        print(f"recommended_{index}_action:", code.proposed_codebook_action)
        print(
            f"recommended_{index}_evidence:",
            [item.excerpt for item in code.supporting_evidence],
        )
    print("preserved_alternatives:", len(arbitration_output.preserved_alternatives))
    for index, code in enumerate(arbitration_output.preserved_alternatives, start=1):
        print(f"alternative_{index}_name:", code.code_name)
        print(f"alternative_{index}_interpretation:", code.alternative_interpretation)
    print("disagreements:", len(arbitration_output.disagreements))
    for index, disagreement in enumerate(arbitration_output.disagreements, start=1):
        print(f"disagreement_{index}_type:", disagreement.disagreement_type)
        print(f"disagreement_{index}_summary:", disagreement.summary)
    print("possible_codebook_changes:", len(arbitration_output.possible_codebook_changes))
    for index, change in enumerate(arbitration_output.possible_codebook_changes, start=1):
        print(f"change_{index}_action:", change.action)
        print(f"change_{index}_summary:", change.summary)
    print("=" * 80)
    print("validation_summary:", validation_output.summary)
    print("human_review_required:", validation_output.human_review_required)
    for index, signal in enumerate(validation_output.signals, start=1):
        print(f"signal_{index}_name:", signal.signal)
        print(f"signal_{index}_summary:", signal.summary)
        print(f"signal_{index}_codes:", signal.related_code_names)
        print(
            f"signal_{index}_evidence:",
            [item.excerpt for item in signal.evidence_items],
        )
    print("validation_notes:", validation_output.notes)


if __name__ == "__main__":
    main()
