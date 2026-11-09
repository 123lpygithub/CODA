from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from typing import Any

from coda.agents.base import AgentExecutionError, AgentPromptSpec, BaseLLMAgent
from coda.agents.common import (
    build_evidence_item,
    serialize_analysis_protocol,
    stringify_raw_fields,
)
from coda.contracts import ContextAgentInput, ContextPacket, EvidenceItem
from coda.llm import ChatBackend, LLMModelConfig
from coda.parsing import require_fields
from coda.prompts import read_prompt_file


@dataclass(frozen=True)
class ContextAgentSettings:
    """Configuration for the first Context Agent implementation."""

    raw_field_char_limit: int = 1600
    history_example_limit: int = 3
    base_evidence_items: int = 4
    maximum_evidence_items: int = 8
    characters_per_extra_evidence: int = 2500

    def __post_init__(self) -> None:
        if self.base_evidence_items < 1:
            raise ValueError("base_evidence_items must be positive.")
        if self.maximum_evidence_items < self.base_evidence_items:
            raise ValueError("maximum_evidence_items cannot be below the base limit.")
        if self.characters_per_extra_evidence < 1:
            raise ValueError("characters_per_extra_evidence must be positive.")


class ContextLLMAgent(BaseLLMAgent):
    """First-pass Context Agent that prepares grounded context packets."""

    def __init__(
        self,
        *,
        model_config: LLMModelConfig,
        backend: ChatBackend,
        settings: ContextAgentSettings | None = None,
    ) -> None:
        prompt_spec = AgentPromptSpec(
            name="context_agent",
            system_prompt=read_prompt_file("context_system_prompt.txt"),
            user_prompt_template=read_prompt_file("context_user_prompt.txt"),
        )
        super().__init__(
            prompt_spec=prompt_spec,
            model_config=model_config,
            backend=backend,
        )
        self._settings = settings or ContextAgentSettings()

    def __call__(self, agent_input: ContextAgentInput) -> ContextPacket:
        max_evidence_items = self._max_evidence_items(agent_input)
        return self.invoke_validated_json_object(
            lambda payload, response: self._payload_to_context_packet(
                agent_input,
                payload,
                response,
                max_evidence_items=max_evidence_items,
            ),
            dataset_name=agent_input.research_question.dataset_name,
            research_question=agent_input.research_question.question_text,
            analysis_scope=agent_input.research_question.analysis_scope,
            use_case=agent_input.research_question.use_case,
            artifact_unit=agent_input.research_question.artifact_unit,
            analysis_protocol=serialize_analysis_protocol(agent_input.analysis_protocol),
            artifact_id=agent_input.artifact.artifact_id,
            artifact_content=agent_input.artifact.content,
            raw_fields_json=stringify_raw_fields(
                agent_input.artifact.raw_fields,
                max_value_chars=self._settings.raw_field_char_limit,
            ),
            additional_context_json=json.dumps(
                list(agent_input.additional_context),
                ensure_ascii=False,
                indent=2,
            ),
            source_refs_json=json.dumps(
                [
                    {
                        "kind": source_ref.kind,
                        "value": source_ref.value,
                        "ref_id": source_ref.ref_id,
                        "field": source_ref.field,
                        "locator": asdict(source_ref.locator) if source_ref.locator else None,
                    }
                    for source_ref in agent_input.artifact.source_refs
                ],
                ensure_ascii=False,
                indent=2,
            ),
            max_evidence_items=max_evidence_items,
        )

    def _max_evidence_items(self, agent_input: ContextAgentInput) -> int:
        extra_items = (
            len(agent_input.artifact.content)
            // self._settings.characters_per_extra_evidence
        )
        return min(
            self._settings.maximum_evidence_items,
            self._settings.base_evidence_items + extra_items,
        )

    def _payload_to_context_packet(
        self,
        agent_input: ContextAgentInput,
        payload: dict[str, Any],
        response,
        *,
        max_evidence_items: int,
    ) -> ContextPacket:
        payload = dict(payload)
        payload.setdefault("context_brief_zh", payload["context_brief"])
        payload.setdefault("missing_context_warnings_zh", payload.get("missing_context_warnings", []))
        payload.setdefault("distracting_information_zh", payload.get("distracting_information", []))
        payload = require_fields(
            payload,
            required_fields=[
                "context_brief",
                "context_brief_zh",
                "evidence_items",
                "missing_context_warnings",
                "missing_context_warnings_zh",
                "distracting_information",
                "distracting_information_zh",
            ],
        )
        if len(str(payload["context_brief"]).split()) > 150:
            raise AgentExecutionError("Context summary exceeds the 150-word limit; shorten the summary without changing its interpretation.")
        evidence_rows = payload.get("evidence_items", [])
        if not isinstance(evidence_rows, list):
            msg = "Context agent output field 'evidence_items' must be a list."
            raise AgentExecutionError(msg)
        if not evidence_rows and not payload.get("missing_context_warnings"):
            raise AgentExecutionError("An empty evidence list requires an explicit missing-context explanation.")
        if len(evidence_rows) > max_evidence_items:
            raise AgentExecutionError(
                "Context agent must return at most "
                f"{max_evidence_items} grounded evidence items."
            )

        evidence_items: list[EvidenceItem] = []
        for row in evidence_rows:
            if not isinstance(row, dict):
                raise AgentExecutionError(
                    "Context agent evidence item must be a JSON object."
                )
            row = dict(row)
            row.setdefault("rationale_zh", row["rationale"])
            row = require_fields(
                row,
                required_fields=["field_name", "excerpt", "rationale", "rationale_zh"],
            )
            claim_type = str(row.get("claim_type", "reported"))
            if claim_type not in {"reported", "observed", "inferred"}:
                raise AgentExecutionError("Evidence claim_type must be reported, observed, or inferred.")
            field_name = str(row["field_name"])
            excerpt = str(row["excerpt"]).strip()
            rationale = str(row["rationale"]).strip()
            rationale_zh = str(row["rationale_zh"]).strip()
            if field_name not in agent_input.artifact.raw_fields:
                field_name = "content"
            if excerpt:
                try:
                    evidence_items.append(
                        build_evidence_item(
                            agent_input.artifact,
                            field_name=field_name,
                            excerpt=excerpt,
                            rationale=rationale,
                            rationale_zh=rationale_zh,
                            claim_type=claim_type,
                            revision=str(row["revision"]) if row.get("revision") is not None else None,
                        )
                    )
                except ValueError as error:
                    raise AgentExecutionError(str(error)) from error

        if not evidence_items and not payload.get("missing_context_warnings"):
            raise AgentExecutionError("No grounded evidence remains; provide a missing-context explanation rather than empty excerpts.")

        missing_context_warnings = payload.get("missing_context_warnings", [])
        missing_context_warnings_zh = payload.get("missing_context_warnings_zh", [])
        distracting_information = payload.get("distracting_information", [])
        distracting_information_zh = payload.get("distracting_information_zh", [])
        if not isinstance(missing_context_warnings, list):
            raise AgentExecutionError(
                "Context agent output field 'missing_context_warnings' must be a list."
            )
        if not isinstance(distracting_information, list):
            raise AgentExecutionError(
                "Context agent output field 'distracting_information' must be a list."
            )
        if not isinstance(missing_context_warnings_zh, list):
            raise AgentExecutionError(
                "Context agent output field 'missing_context_warnings_zh' must be a list."
            )
        if not isinstance(distracting_information_zh, list):
            raise AgentExecutionError(
                "Context agent output field 'distracting_information_zh' must be a list."
            )

        model_metadata = self.execution_metadata(response)
        model_metadata["context_construction"] = {
            "raw_field_char_limit": self._settings.raw_field_char_limit,
            "max_evidence_items": max_evidence_items,
            "evidence_limit_rule": "base_plus_one_per_visible_character_bucket",
            "characters_per_extra_evidence": self._settings.characters_per_extra_evidence,
            "source": "artifact_content_raw_fields_source_refs_and_researcher_context",
            "codebook_or_history_included": False,
        }
        return ContextPacket(
            artifact_id=agent_input.artifact.artifact_id,
            context_brief=str(payload["context_brief"]).strip(),
            context_brief_zh=str(payload["context_brief_zh"]).strip(),
            evidence_items=evidence_items,
            missing_context_warnings=[str(item).strip() for item in missing_context_warnings],
            missing_context_warnings_zh=[str(item).strip() for item in missing_context_warnings_zh],
            distracting_information=[str(item).strip() for item in distracting_information],
            distracting_information_zh=[str(item).strip() for item in distracting_information_zh],
            source_refs=list(agent_input.artifact.source_refs),
            model_metadata=model_metadata,
        )
