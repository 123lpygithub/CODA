from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Any

from coda.agents.base import AgentExecutionError, AgentPromptSpec, BaseLLMAgent
from coda.agents.common import (
    serialize_analysis_protocol,
    serialize_codebook,
    serialize_coder_outputs,
    serialize_context_packet,
)
from coda.contracts import InductionAgentInput, InductionAgentOutput
from coda.llm import ChatBackend, LLMModelConfig
from coda.parsing import require_fields
from coda.prompts import read_prompt_file
from coda.state import CodeState


@dataclass(frozen=True)
class InductionAgentSettings:
    """Optional operational guardrail for one induction response."""

    max_codes: int | None = None

    def __post_init__(self) -> None:
        if self.max_codes is not None and self.max_codes < 1:
            raise ValueError("Induction max_codes must be positive when configured.")


class InductionLLMAgent(BaseLLMAgent):
    """Compare independent initial codes and induce a provisional codebook."""

    def __init__(
        self,
        *,
        model_config: LLMModelConfig,
        backend: ChatBackend,
        settings: InductionAgentSettings | None = None,
    ) -> None:
        super().__init__(
            prompt_spec=AgentPromptSpec(
                name="induction_agent",
                system_prompt=read_prompt_file("induction_system_prompt.txt"),
                user_prompt_template=read_prompt_file("induction_user_prompt.txt"),
            ),
            model_config=model_config,
            backend=backend,
        )
        self._settings = settings or InductionAgentSettings()

    def __call__(self, agent_input: InductionAgentInput) -> InductionAgentOutput:
        cases = [
            {
                "artifact_id": case.artifact_id,
                "original_material": case.original_material,
                "context_packet": json.loads(serialize_context_packet(case.context_packet)),
                "independent_coder_outputs": json.loads(
                    serialize_coder_outputs(case.coder_outputs, case.context_packet)
                ),
            }
            for case in agent_input.cases
        ]
        return self.invoke_validated_json_object(
            lambda payload, response: self._payload_to_induction_output(
                agent_input, payload, response
            ),
            research_question=agent_input.research_question.question_text,
            analysis_scope=agent_input.research_question.analysis_scope,
            use_case=agent_input.research_question.use_case,
            analysis_protocol=serialize_analysis_protocol(agent_input.analysis_protocol),
            batch_index=agent_input.batch_index,
            induction_stage=agent_input.induction_stage,
            existing_draft_codebook=serialize_codebook(agent_input.existing_draft_codes),
            initial_coding_cases=json.dumps(cases, ensure_ascii=False, indent=2),
            validation_feedback=json.dumps(
                agent_input.validation_feedback,
                ensure_ascii=False,
                indent=2,
            ),
            code_count_instruction=(
                "No category count is predetermined. Return a compact set of reusable "
                "categories after comparing and consolidating observations; preserve local "
                "detail in criteria, evidence summaries, and memos rather than separate entries."
                if self._settings.max_codes is None
                else f"Operational response limit: at most {self._settings.max_codes} entries."
            ),
        )
    def _payload_to_induction_output(
        self,
        agent_input: InductionAgentInput,
        payload: dict[str, Any],
        response,
    ) -> InductionAgentOutput:
        payload = require_fields(
            payload,
            required_fields=["codes", "change_log", "analytic_memos"],
        )
        codes = self._parse_codes(
            payload["codes"],
            allowed_artifact_ids=set(agent_input.allowed_artifact_ids)
            or {case.artifact_id for case in agent_input.cases},
        )
        return InductionAgentOutput(
            codes=codes,
            change_log=self._dict_list(payload["change_log"], "change_log"),
            analytic_memos=self._dict_list(payload["analytic_memos"], "analytic_memos"),
            model_metadata={
                **self.execution_metadata(response),
                "induction_stage": agent_input.induction_stage,
            },
        )

    @staticmethod
    def _dict_list(value: Any, field_name: str) -> list[dict[str, Any]]:
        if not isinstance(value, list) or any(not isinstance(item, dict) for item in value):
            raise AgentExecutionError(f"Field '{field_name}' must be an array of objects.")
        return [dict(item) for item in value]

    @staticmethod
    def _parse_codes(rows: Any, *, allowed_artifact_ids: set[str]) -> list[CodeState]:
        if not isinstance(rows, list):
            raise AgentExecutionError("Induction field 'codes' must be an array.")
        codes: list[CodeState] = []
        ids: set[str] = set()
        parent_ids: dict[str, str | None] = {}
        for row in rows:
            if not isinstance(row, dict):
                raise AgentExecutionError("Each induced code must be an object.")
            code_id = str(row.get("code_id", "")).strip()
            name = str(row.get("name", "")).strip()
            definition = str(row.get("definition", "")).strip()
            name_zh = str(row.get("name_zh", name)).strip()
            definition_zh = str(row.get("definition_zh", definition)).strip()
            inclusion_criteria = InductionLLMAgent._string_list(
                row.get("inclusion_criteria", []), "inclusion_criteria"
            )
            exclusion_criteria = InductionLLMAgent._string_list(
                row.get("exclusion_criteria", []), "exclusion_criteria"
            )
            inclusion_criteria_zh = InductionLLMAgent._string_list(
                row.get("inclusion_criteria_zh", inclusion_criteria),
                "inclusion_criteria_zh",
            )
            exclusion_criteria_zh = InductionLLMAgent._string_list(
                row.get("exclusion_criteria_zh", exclusion_criteria),
                "exclusion_criteria_zh",
            )
            representatives = [
                str(item).strip() for item in row.get("representative_artifact_ids", [])
            ]
            evidence_summary = str(row.get("evidence_summary", "")).strip()
            boundary_artifact_ids = InductionLLMAgent._string_list(
                row.get("boundary_artifact_ids", []), "boundary_artifact_ids"
            )
            counterexample_status = str(
                row.get("counterexample_status", "not_assessed")
            ).strip()
            hypothetical_examples = InductionLLMAgent._string_list(
                row.get("hypothetical_examples", []), "hypothetical_examples"
            )
            raw_parent = row.get("parent_code_id")
            parent_code_id = str(raw_parent).strip() if raw_parent is not None else None
            if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", code_id):
                raise AgentExecutionError("Induced code_id must use lowercase kebab case.")
            if code_id in ids:
                raise AgentExecutionError(f"Duplicate induced code id: {code_id}.")
            if not name or not definition or not representatives or not evidence_summary:
                raise AgentExecutionError("An induced code lacks a definition or evidence trace.")
            if any(item not in allowed_artifact_ids for item in representatives):
                raise AgentExecutionError("An induced code references an unknown artifact.")
            if any(item not in allowed_artifact_ids for item in boundary_artifact_ids):
                raise AgentExecutionError(
                    "An induced code references an unknown boundary artifact."
                )
            if counterexample_status not in {
                "not_assessed",
                "no_observed_counterexample",
                "observed_counterexample",
            }:
                raise AgentExecutionError(
                    "Induced counterexample_status must use the declared provenance enum."
                )
            if (
                counterexample_status == "observed_counterexample"
                and not boundary_artifact_ids
            ):
                raise AgentExecutionError(
                    "An observed counterexample requires at least one boundary artifact id."
                )
            ids.add(code_id)
            parent_ids[code_id] = parent_code_id
            codes.append(
                CodeState(
                    code_id=code_id,
                    name=name,
                    definition=definition,
                    inclusion_criteria=inclusion_criteria,
                    exclusion_criteria=exclusion_criteria,
                    representative_artifact_ids=representatives,
                    boundary_artifact_ids=boundary_artifact_ids,
                    counterexample_status=counterexample_status,  # type: ignore[arg-type]
                    hypothetical_examples=hypothetical_examples,
                    parent_code_id=parent_code_id,
                    notes=["Induced from independent initial coding; not human-reviewed."],
                    metadata={
                        "origin": "llm_initial_induction",
                        "source_stage": "initial_category_induction",
                        "created_at_codebook_version": 1,
                        "human_reviewed": False,
                        "support_count": len(representatives),
                        "evidence_summary": evidence_summary,
                        "name_zh": name_zh,
                        "definition_zh": definition_zh,
                        "inclusion_criteria_zh": inclusion_criteria_zh,
                        "exclusion_criteria_zh": exclusion_criteria_zh,
                        "source_provisional_codes": InductionLLMAgent._string_list(
                            row.get("source_provisional_codes", []),
                            "source_provisional_codes",
                        ),
                    },
                )
            )
        unknown_parents = {
            parent_id
            for parent_id in parent_ids.values()
            if parent_id is not None and parent_id not in ids
        }
        if unknown_parents:
            raise AgentExecutionError(
                "Induced parent_code_id references unknown code(s): "
                + ", ".join(sorted(unknown_parents))
            )
        return codes

    @staticmethod
    def _string_list(value: Any, field_name: str) -> list[str]:
        if not isinstance(value, list):
            raise AgentExecutionError(f"Field '{field_name}' must be an array.")
        return [str(item).strip() for item in value if str(item).strip()]
