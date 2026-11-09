from __future__ import annotations

import json
from dataclasses import asdict, dataclass, replace
from typing import Any

from coda.agents.base import AgentExecutionError, AgentPromptSpec, BaseLLMAgent
from coda.agents.common import (
    normalize_codebook_relationship,
    select_relevant_history,
    serialize_analysis_protocol,
    serialize_codebook,
    serialize_coder_outputs,
    serialize_context_packet,
    serialize_history,
)
from coda.contracts import (
    AnalyticMemo,
    ArbitrationInput,
    ArbitrationOutput,
    ComparisonFinding,
    DisagreementRecord,
    EvidenceItem,
    HistoricalExample,
    ProvisionalCode,
)
from coda.llm import ChatBackend, LLMModelConfig
from coda.parsing import require_fields
from coda.prompts import read_prompt_file
from coda.state import CodeState, CodebookChangeState, CodingRecordState

_ALLOWED_RELATIONSHIPS = {
    "reuse_existing_code",
    "new_code",
    "add_parent_code",
    "refine_existing_code",
    "merge_existing_codes",
    "split_existing_code",
    "uncertain",
}
_ALLOWED_DISAGREEMENT_TYPES = {
    "evidence_disagreement",
    "semantic_disagreement",
    "granularity_disagreement",
    "codebook_boundary_disagreement",
    "missing_context_disagreement",
    "output_format_inconsistency",
}
_ALLOWED_CODEBOOK_ACTIONS = {
    "add",
    "add_parent",
    "refine",
    "merge",
    "split",
    "rename",
    "retire",
    "no_change",
}
_ALLOWED_COMPARISON_TYPES = {"case_to_case", "case_to_code", "code_to_code"}
_ALLOWED_COMPARISON_FINDINGS = {
    "same_phenomenon",
    "distinct_phenomenon",
    "partial_overlap",
    "granularity_difference",
    "boundary_case",
    "insufficient_evidence",
}
_ALLOWED_MEMO_TYPES = {
    "comparison",
    "category_boundary",
    "alternative_interpretation",
    "change_rationale",
    "unresolved_question",
}
_ALLOWED_MEMO_STATUSES = {"open", "resolved"}


@dataclass(frozen=True)
class ComparisonAgentSettings:
    """Configuration for constant comparison over one incoming artifact."""

    history_example_limit: int = 6
    max_recommended_codes: int = 3
    max_preserved_alternatives: int = 3


def _build_evidence_lookup(
    evidence_items: list[EvidenceItem],
) -> dict[str, EvidenceItem]:
    return {
        f"E{index}": evidence_item
        for index, evidence_item in enumerate(evidence_items, start=1)
    }


def _history_by_artifact_id(
    records: list[CodingRecordState],
) -> dict[str, CodingRecordState]:
    by_artifact_id: dict[str, CodingRecordState] = {}
    for record in records:
        by_artifact_id[record.artifact_id] = record
    return by_artifact_id


def _require_string_list(value: Any, *, field_name: str) -> list[str]:
    if not isinstance(value, list):
        raise AgentExecutionError(f"Field '{field_name}' must be a list.")
    return [str(item).strip() for item in value]


def _resolve_evidence_refs(
    refs: Any,
    *,
    evidence_lookup: dict[str, EvidenceItem],
    field_name: str,
) -> list[EvidenceItem]:
    ref_names = _require_string_list(refs, field_name=field_name)
    resolved: list[EvidenceItem] = []
    for ref_name in ref_names:
        evidence = evidence_lookup.get(ref_name)
        if evidence is None:
            raise AgentExecutionError(
                f"Unknown evidence ref '{ref_name}' in field '{field_name}'."
            )
        resolved.append(evidence)
    return resolved


def _require_allowed_value(
    value: Any,
    *,
    field_name: str,
    allowed_values: set[str],
) -> str:
    normalized = str(value).strip()
    if normalized not in allowed_values:
        allowed_text = ", ".join(sorted(allowed_values))
        raise AgentExecutionError(
            f"Field '{field_name}' must be one of: {allowed_text}."
        )
    return normalized


class ComparisonLLMAgent(BaseLLMAgent):
    """LLM-backed agent for coder synthesis and constant comparison."""

    def __init__(
        self,
        *,
        model_config: LLMModelConfig,
        backend: ChatBackend,
        settings: ComparisonAgentSettings | None = None,
    ) -> None:
        prompt_spec = AgentPromptSpec(
            name="comparison_agent",
            system_prompt=read_prompt_file("comparison_system_prompt.txt"),
            user_prompt_template=read_prompt_file("comparison_user_prompt.txt"),
        )
        super().__init__(
            prompt_spec=prompt_spec,
            model_config=model_config,
            backend=backend,
        )
        self._settings = settings or ComparisonAgentSettings()
        self._batch_prompt = read_prompt_file('comparison_batch_system_prompt.txt')

    def __call__(self, agent_input: ArbitrationInput) -> ArbitrationOutput:
        first = self._invoke_task(agent_input)
        needs_refinement = any(change.action != "no_change" for change in first.possible_codebook_changes) or any(
            code.relationship_to_codebook not in {"reuse_existing_code", "uncertain"}
            for code in first.recommended_codes
        )
        if agent_input.defer_refinement or agent_input.task != "case_comparison" or not needs_refinement:
            return first
        # Comparing a case does not silently edit a definition. Refinement is a
        # separate call with the same base version and the preceding proposal.
        refined = self._invoke_task(replace(
            agent_input, task="codebook_refinement", prior_comparison=asdict(first),
        ))
        return replace(refined, model_metadata={
            **refined.model_metadata,
            "case_comparison_model_metadata": first.model_metadata,
            "model_calls": [*first.model_metadata.get("model_calls", []),
                            *refined.model_metadata.get("model_calls", [])],
        })

    def reconcile_batch(self, *, run_state, prepared):
        """One Comparison call, with case-local evidence IDs and a shared base.

        Reconciliation proposes definitions; it never accepts edits. Every
        per-case result is parsed against its own sources and the same codebook.
        """
        agent = BaseLLMAgent(prompt_spec=AgentPromptSpec(
            'comparison_batch_reconciliation',
            self._prompt_spec.system_prompt + '\n' + self._batch_prompt,
            '{payload}'), model_config=self.model_config, backend=self._backend)
        agent.set_output_language(self._output_language)
        agent.trace_sink = self.trace_sink
        inputs = {item.artifact_id: ArbitrationInput(
            artifact=item.artifact, research_question=run_state.research_question,
            context_packet=item.context_packet, coder_outputs=item.coder_outputs,
            codebook=run_state.codebook, history=run_state.history,
            analysis_protocol=run_state.analysis_protocol,
            historical_materials=run_state.metadata.get('case_materials', {}),
        ) for item in prepared}
        def parse(payload, response):
            rows = payload.get('case_proposals')
            if not isinstance(rows, list) or len(rows) != len(inputs):
                raise AgentExecutionError('Reconciliation must return exactly one proposal per batch case.')
            result = {}
            for row in rows:
                if not isinstance(row, dict) or row.get('artifact_id') not in inputs or row['artifact_id'] in result:
                    raise AgentExecutionError('Reconciliation contains duplicate or unknown cases.')
                output = self._payload_to_arbitration_output(inputs[row['artifact_id']], row, response)
                result[row['artifact_id']] = replace(output, model_metadata={
                    **output.model_metadata, 'task': 'batch_reconciliation',
                    'model_calls': agent.execution_metadata(response).get('model_calls', []),
                    'batch_case_ids': list(inputs)})
            self._validate_batch_consistency(result)
            return result
        return agent.invoke_validated_json_object(parse, payload=json.dumps({
            'research_question': asdict(run_state.research_question),
            'analysis_protocol': asdict(run_state.analysis_protocol),
            'base_codebook': asdict(run_state.codebook),
            'reviewed_history': serialize_history(
                list({record.record_id:record for value in inputs.values()
                      for record in self._select_history(value)}.values()),
                limit=self._settings.history_example_limit * len(inputs),
                analytic_memos=run_state.history.analytic_memos,
                historical_materials=run_state.metadata.get('case_materials', {})),
            'cases': [{'artifact_id':item.artifact_id, 'original_material':asdict(item.artifact),
                       'context_packet':json.loads(serialize_context_packet(item.context_packet)),
                       'coder_outputs':json.loads(serialize_coder_outputs(item.coder_outputs,item.context_packet)),
                       'proposal':json.loads(self._batch_proposal_json(item))} for item in prepared],
            'response_format': read_prompt_file('comparison_user_prompt.txt').split('Return a JSON object',1)[-1]
                .replace('{max_recommended_codes}', str(self._settings.max_recommended_codes))
                .replace('{max_preserved_alternatives}', str(self._settings.max_preserved_alternatives)),
        }, ensure_ascii=False))

    @staticmethod
    def _batch_proposal_json(item):
        # Initial proposal evidence is already available in the local context
        # packet. Explicit evidence refs prevent cross-case E1 confusion.
        proposal = asdict(item.arbitration_output)
        return json.dumps(proposal, ensure_ascii=False)

    @staticmethod
    def _validate_batch_consistency(outputs):
        definitions, edits = {}, {}
        for output in outputs.values():
            for candidate in output.recommended_codes:
                if candidate.relationship_to_codebook == 'reuse_existing_code':
                    continue
                name = ' '.join(candidate.code_name.split()).casefold()
                signature = (candidate.short_definition, tuple(candidate.inclusion_criteria),
                             tuple(candidate.exclusion_criteria))
                if name in definitions and definitions[name] != signature:
                    raise AgentExecutionError('A shared batch category has incompatible definitions; reconcile or explicitly defer it.')
                definitions[name] = signature
            for change in output.possible_codebook_changes:
                if change.action in {'no_change','add'}:
                    continue
                signature = (change.action, tuple(sorted(change.target_code_ids)),
                             tuple(sorted(change.metadata.get('resulting_code_names', []))))
                for target in change.target_code_ids:
                    if target in edits and edits[target] != signature:
                        raise AgentExecutionError('Conflicting batch operations target the same category; reconcile or defer the conflicting operation.')
                    edits[target] = signature

    def screen_historical_impacts(self, *, change, codebook, cases):
        """Screen all earlier summaries/decisions; this never reassigns a case."""
        agent = BaseLLMAgent(
            prompt_spec=AgentPromptSpec(
                "comparison_impact_screening",
                read_prompt_file("comparison_impact_system_prompt.txt"),
                "{payload}",
            ), model_config=self.model_config, backend=self._backend,
            bilingual_output=False,
        )
        agent.trace_sink = self.trace_sink
        def parse(payload, response):
            for field in ("affected_cases", "unchecked_cases"):
                if not isinstance(payload.get(field), list):
                    raise AgentExecutionError(f"Missing {field} list.")
                seen = set()
                for row in payload[field]:
                    if (not isinstance(row, dict) or row.get("artifact_id") not in cases
                            or row["artifact_id"] in seen or not str(row.get("reason", "")).strip()):
                        raise AgentExecutionError("Impact screening contains an unknown/duplicate case or missing reason.")
                    seen.add(row["artifact_id"])
            return {**payload, "model_metadata": agent.execution_metadata(response)}
        return agent.invoke_validated_json_object(parse, payload=json.dumps({
            "change": asdict(change), "codebook": [asdict(code) for code in codebook.active_codes()], "cases": cases,
        }, ensure_ascii=False))

    def _invoke_task(self, agent_input: ArbitrationInput) -> ArbitrationOutput:
        relevant_history = self._select_history(agent_input)

        return self.invoke_validated_json_object(
            lambda payload, response: self._payload_to_arbitration_output(
                agent_input, payload, response
            ),
            comparison_task=agent_input.task,
            prior_comparison_json=json.dumps(agent_input.prior_comparison, ensure_ascii=False),
            research_question=agent_input.research_question.question_text,
            analysis_scope=agent_input.research_question.analysis_scope,
            use_case=agent_input.research_question.use_case,
            analysis_protocol=serialize_analysis_protocol(agent_input.analysis_protocol),
            artifact_id=agent_input.artifact.artifact_id,
            artifact_content=agent_input.artifact.content,
            context_packet_json=serialize_context_packet(agent_input.context_packet),
            coder_outputs_json=serialize_coder_outputs(
                agent_input.coder_outputs,
                agent_input.context_packet,
            ),
            codebook_snapshot=serialize_codebook(agent_input.codebook.active_codes()),
            history_snapshot=serialize_history(
                relevant_history,
                limit=self._settings.history_example_limit,
                analytic_memos=agent_input.history.analytic_memos,
                unresolved_cases=agent_input.history.unresolved_cases,
                context_requests=agent_input.history.context_requests,
                stage_reviews=agent_input.history.stage_reviews,
                historical_materials=agent_input.historical_materials,
            ),
            max_recommended_codes=self._settings.max_recommended_codes,
            max_preserved_alternatives=self._settings.max_preserved_alternatives,
        )

    def _select_history(
        self,
        agent_input: ArbitrationInput,
    ) -> list[CodingRecordState]:
        relevant_code_ids = {
            code_id
            for output in agent_input.coder_outputs
            for code in output.provisional_codes
            for code_id in [*code.linked_code_ids, *code.proposed_codebook_target_ids]
        }
        representative_ids = {
            artifact_id
            for code in agent_input.codebook.active_codes()
            if code.code_id in relevant_code_ids
            for artifact_id in code.representative_artifact_ids
        }
        return select_relevant_history(
            agent_input.history.coding_records,
            query_text=" ".join(
                [
                    agent_input.artifact.content,
                    agent_input.context_packet.context_brief,
                    *(code.observed_phenomenon or code.short_definition for output in agent_input.coder_outputs for code in output.provisional_codes),
                ]
            ),
            relevant_code_ids=relevant_code_ids,
            representative_artifact_ids=representative_ids,
            limit=self._settings.history_example_limit,
        )

    def _payload_to_arbitration_output(
        self,
        agent_input: ArbitrationInput,
        payload: dict[str, Any],
        response,
    ) -> ArbitrationOutput:
        payload = dict(payload)
        # Responses persisted before constant-comparison fields were introduced
        # remain readable. The current prompt always requests both arrays.
        payload.setdefault("comparison_findings", [])
        payload.setdefault("analytic_memos", [])
        payload.setdefault("prior_human_conflicts", [])
        payload.setdefault("agreement_summary_zh", payload["agreement_summary"])
        payload.setdefault("disagreement_summary_zh", payload["disagreement_summary"])
        payload = require_fields(
            payload,
            required_fields=[
                "agreement_summary",
                "agreement_summary_zh",
                "disagreement_summary",
                "disagreement_summary_zh",
                "recommended_codes",
                "preserved_alternatives",
                "disagreements",
                "relevant_historical_artifact_ids",
                "possible_codebook_changes",
                "comparison_findings",
                "analytic_memos",
                "prior_human_conflicts",
            ],
        )
        evidence_lookup = _build_evidence_lookup(
            agent_input.context_packet.evidence_items
        )
        history_lookup = _history_by_artifact_id(self._select_history(agent_input))
        active_code_ids = {
            code.code_id for code in agent_input.codebook.active_codes()
        }
        recommended_codes = self._parse_codes(
            payload["recommended_codes"],
            evidence_lookup=evidence_lookup,
            active_code_ids=active_code_ids,
        )
        preserved_alternatives = self._parse_codes(
            payload["preserved_alternatives"],
            evidence_lookup=evidence_lookup,
            active_code_ids=active_code_ids,
        )
        possible_codebook_changes = self._parse_codebook_changes(
            payload["possible_codebook_changes"],
            artifact_id=agent_input.artifact.artifact_id,
            round_index=len(agent_input.history.coding_records),
            history_lookup=history_lookup,
            active_code_ids=active_code_ids,
        )
        self._validate_new_code_label_collisions(
            active_codes=agent_input.codebook.active_codes(),
            candidates=[*recommended_codes, *preserved_alternatives],
        )
        self._validate_change_recommendation_consistency(
            changes=possible_codebook_changes,
            candidates=[*recommended_codes, *preserved_alternatives],
        )
        return ArbitrationOutput(
            artifact_id=agent_input.artifact.artifact_id,
            agreement_summary=str(payload["agreement_summary"]).strip(),
            disagreement_summary=str(payload["disagreement_summary"]).strip(),
            agreement_summary_zh=str(payload["agreement_summary_zh"]).strip(),
            disagreement_summary_zh=str(payload["disagreement_summary_zh"]).strip(),
            recommended_codes=recommended_codes,
            preserved_alternatives=preserved_alternatives,
            disagreements=self._parse_disagreements(
                payload["disagreements"],
                evidence_lookup=evidence_lookup,
            ),
            relevant_historical_examples=self._parse_history_examples(
                payload["relevant_historical_artifact_ids"],
                history_lookup=history_lookup,
            ),
            possible_codebook_changes=possible_codebook_changes,
            comparison_findings=self._parse_comparison_findings(
                payload["comparison_findings"],
                artifact_id=agent_input.artifact.artifact_id,
                evidence_lookup=evidence_lookup,
                history_lookup=history_lookup,
                active_code_ids=active_code_ids,
            ),
            analytic_memos=self._parse_analytic_memos(
                payload["analytic_memos"],
                artifact_id=agent_input.artifact.artifact_id,
                history_lookup=history_lookup,
                active_code_ids=active_code_ids,
            ),
            prior_human_conflicts=self._parse_prior_human_conflicts(
                payload["prior_human_conflicts"],
                active_code_ids=active_code_ids,
            ),
            model_metadata={
                **self.execution_metadata(response),
                "task": agent_input.task,
                "base_version": agent_input.codebook.version,
                "scope": {
                    "inspected_case_ids": [agent_input.artifact.artifact_id],
                    "historical_source_case_ids": [record.artifact_id for record in self._select_history(agent_input)
                                                   if record.artifact_id in agent_input.historical_materials],
                    "uninspected_case_ids": sorted({record.artifact_id for record in agent_input.history.coding_records}
                                                    - {record.artifact_id for record in self._select_history(agent_input)}),
                },
            },
        )

    def _parse_codes(
        self,
        rows: Any,
        *,
        evidence_lookup: dict[str, EvidenceItem],
        active_code_ids: set[str],
    ) -> list[ProvisionalCode]:
        if not isinstance(rows, list):
            raise AgentExecutionError("Arbitration code lists must be arrays.")
        parsed: list[ProvisionalCode] = []
        for row in rows:
            if not isinstance(row, dict):
                raise AgentExecutionError("Arbitration code entry must be an object.")
            # New recommendations commonly do not reuse a current code.
            row = dict(row)
            row.setdefault("linked_code_ids", [])
            row.setdefault("code_name_zh", row.get("code_name", ""))
            row.setdefault("short_definition_zh", row.get("short_definition", ""))
            row.setdefault("observed_phenomenon", row.get("short_definition", ""))
            row.setdefault(
                "observed_phenomenon_zh",
                row.get("short_definition_zh", row.get("short_definition", "")),
            )
            row.setdefault("alternative_interpretation_zh", row.get("alternative_interpretation", ""))
            row.setdefault("uncertainty_note_zh", row.get("uncertainty_note", ""))
            row = require_fields(
                row,
                required_fields=[
                    "code_name",
                    "code_name_zh",
                    "short_definition",
                    "short_definition_zh",
                    "observed_phenomenon",
                    "observed_phenomenon_zh",
                    "supporting_evidence_refs",
                    "relationship_to_codebook",
                    "linked_code_ids",
                    "alternative_interpretation",
                    "alternative_interpretation_zh",
                    "uncertainty_note",
                    "uncertainty_note_zh",
                    "proposed_codebook_action",
                    "proposed_codebook_target_ids",
                ],
            )
            row = dict(row)
            row.setdefault("summary_zh", row.get("summary", ""))
            relationship = _require_allowed_value(
                normalize_codebook_relationship(row["relationship_to_codebook"]),
                field_name="relationship_to_codebook",
                allowed_values=_ALLOWED_RELATIONSHIPS,
            )
            linked_code_ids = self._known_code_ids(
                row["linked_code_ids"],
                active_code_ids=active_code_ids,
                field_name="linked_code_ids",
            )
            proposed_action = _require_allowed_value(
                row["proposed_codebook_action"],
                field_name="proposed_codebook_action",
                allowed_values=_ALLOWED_CODEBOOK_ACTIONS,
            )
            proposed_targets = self._known_code_ids(
                row["proposed_codebook_target_ids"],
                active_code_ids=active_code_ids,
                field_name="proposed_codebook_target_ids",
            )
            self._validate_relationship_targets(
                relationship=relationship,
                linked_code_ids=linked_code_ids,
                action=proposed_action,
                target_code_ids=proposed_targets,
            )
            parsed.append(
                ProvisionalCode(
                    code_name=str(row["code_name"]).strip(),
                    short_definition=str(row["short_definition"]).strip(),
                    code_name_zh=str(row["code_name_zh"]).strip(),
                    short_definition_zh=str(row["short_definition_zh"]).strip(),
                    observed_phenomenon=str(row["observed_phenomenon"]).strip(),
                    observed_phenomenon_zh=str(
                        row["observed_phenomenon_zh"]
                    ).strip(),
                    supporting_evidence=_resolve_evidence_refs(
                        row["supporting_evidence_refs"],
                        evidence_lookup=evidence_lookup,
                        field_name="supporting_evidence_refs",
                    ),
                    relationship_to_codebook=relationship,  # type: ignore[arg-type]
                    linked_code_ids=linked_code_ids,
                    alternative_interpretation=str(
                        row["alternative_interpretation"]
                    ).strip(),
                    alternative_interpretation_zh=str(
                        row["alternative_interpretation_zh"]
                    ).strip(),
                    uncertainty_note=str(row["uncertainty_note"]).strip(),
                    uncertainty_note_zh=str(row["uncertainty_note_zh"]).strip(),
                    proposed_codebook_action=proposed_action,  # type: ignore[arg-type]
                    proposed_codebook_target_ids=proposed_targets,
                    inclusion_criteria=_require_string_list(row.get("inclusion_criteria", []), field_name="inclusion_criteria"),
                    exclusion_criteria=_require_string_list(row.get("exclusion_criteria", []), field_name="exclusion_criteria"),
                    inclusion_criteria_zh=_require_string_list(row.get("inclusion_criteria_zh", []), field_name="inclusion_criteria_zh"),
                    exclusion_criteria_zh=_require_string_list(row.get("exclusion_criteria_zh", []), field_name="exclusion_criteria_zh"),
                )
            )
        return parsed

    def _parse_disagreements(
        self,
        rows: Any,
        *,
        evidence_lookup: dict[str, EvidenceItem],
    ) -> list[DisagreementRecord]:
        if not isinstance(rows, list):
            raise AgentExecutionError("Disagreements must be an array.")
        parsed: list[DisagreementRecord] = []
        for row in rows:
            if not isinstance(row, dict):
                raise AgentExecutionError("Disagreement entry must be an object.")
            row = dict(row)
            row.setdefault("summary_zh", row.get("summary", ""))
            row = require_fields(
                row,
                required_fields=[
                    "disagreement_type",
                    "summary",
                    "summary_zh",
                    "coder_ids",
                    "affected_code_names",
                    "evidence_refs",
                ],
            )
            parsed.append(
                DisagreementRecord(
                    disagreement_type=_require_allowed_value(
                        row["disagreement_type"],
                        field_name="disagreement_type",
                        allowed_values=_ALLOWED_DISAGREEMENT_TYPES,
                    ),  # type: ignore[arg-type]
                    summary=str(row["summary"]).strip(),
                    summary_zh=str(row["summary_zh"]).strip(),
                    coder_ids=_require_string_list(
                        row["coder_ids"],
                        field_name="coder_ids",
                    ),
                    affected_code_names=_require_string_list(
                        row["affected_code_names"],
                        field_name="affected_code_names",
                    ),
                    evidence_items=_resolve_evidence_refs(
                        row["evidence_refs"],
                        evidence_lookup=evidence_lookup,
                        field_name="evidence_refs",
                    ),
                )
            )
        return parsed

    def _parse_history_examples(
        self,
        rows: Any,
        *,
        history_lookup: dict[str, CodingRecordState],
    ) -> list[HistoricalExample]:
        if not isinstance(rows, list):
            raise AgentExecutionError(
                "Historical example field must be a list of artifact ids."
            )
        examples: list[HistoricalExample] = []
        for artifact_id in rows:
            record = history_lookup.get(str(artifact_id))
            if record is None:
                continue
            examples.append(
                HistoricalExample(
                    artifact_id=record.artifact_id,
                    code_ids=list(record.final_code_ids),
                    code_names=list(record.final_code_names),
                    note=record.rationale,
                    human_reviewed=bool(record.metadata.get("human_reviewed", True)),
                    review_origin=str(record.metadata.get("review_origin", "human_review")),
                )
            )
        return examples

    @staticmethod
    def _parse_prior_human_conflicts(
        rows: Any,
        *,
        active_code_ids: set[str],
    ) -> list[dict[str, Any]]:
        if not isinstance(rows, list):
            raise AgentExecutionError("prior_human_conflicts must be an array.")
        conflicts: list[dict[str, Any]] = []
        for row in rows:
            if not isinstance(row, dict):
                raise AgentExecutionError("Each prior-human conflict must be an object.")
            code_ids = _require_string_list(
                row.get("code_ids", []), field_name="prior_human_conflicts.code_ids"
            )
            unknown = set(code_ids) - active_code_ids
            if unknown:
                raise AgentExecutionError(
                    "Prior-human conflict references unknown code id(s): "
                    + ", ".join(sorted(unknown))
                )
            summary = str(row.get("summary", "")).strip()
            summary_zh = str(row.get("summary_zh", summary)).strip()
            rationale = str(row.get("rationale", "")).strip()
            if not code_ids or not summary or not rationale:
                raise AgentExecutionError("Prior-human conflict is incomplete.")
            conflicts.append(
                {
                    "code_ids": code_ids,
                    "summary": summary,
                    "summary_zh": summary_zh,
                    "rationale": rationale,
                }
            )
        return conflicts

    def _parse_codebook_changes(
        self,
        rows: Any,
        *,
        artifact_id: str,
        round_index: int,
        history_lookup: dict[str, CodingRecordState],
        active_code_ids: set[str],
    ) -> list[CodebookChangeState]:
        if not isinstance(rows, list):
            raise AgentExecutionError("Codebook change proposals must be an array.")
        changes: list[CodebookChangeState] = []
        for index, row in enumerate(rows, start=1):
            if not isinstance(row, dict):
                raise AgentExecutionError(
                    "Codebook change proposal must be a JSON object."
                )
            row = dict(row)
            row.setdefault("summary_zh", row.get("summary", ""))
            row.setdefault("rationale_zh", row.get("rationale", ""))
            row = require_fields(
                row,
                required_fields=[
                    "action",
                    "summary",
                    "summary_zh",
                    "rationale",
                    "rationale_zh",
                    "target_code_ids",
                    "resulting_code_names",
                ],
            )
            action = _require_allowed_value(
                row["action"],
                field_name="action",
                allowed_values=_ALLOWED_CODEBOOK_ACTIONS,
            )
            target_code_ids = self._known_code_ids(
                row["target_code_ids"],
                active_code_ids=active_code_ids,
                field_name="target_code_ids",
            )
            self._validate_action_targets(action, target_code_ids)
            changes.append(
                CodebookChangeState(
                    change_id=f"proposal-{artifact_id}-{index}",
                    action=action,  # type: ignore[arg-type]
                    round_index=round_index,
                    summary=str(row["summary"]).strip(),
                    summary_zh=str(row["summary_zh"]).strip(),
                    rationale=str(row["rationale"]).strip(),
                    rationale_zh=str(row["rationale_zh"]).strip(),
                    target_code_ids=target_code_ids,
                    resulting_code_ids=[],
                    artifact_ids=[artifact_id],
                    decided_by="comparison_agent",
                    metadata={
                        "changes_existing_meaning": row.get("changes_existing_meaning") is True,
                        "resulting_code_names": _require_string_list(
                            row["resulting_code_names"],
                            field_name="resulting_code_names",
                        ),
                        "affected_historical_artifact_ids": self._known_history_ids(
                            row.get("affected_historical_artifact_ids", []),
                            history_lookup=history_lookup,
                            field_name="affected_historical_artifact_ids",
                        ),
                    },
                )
            )
        return changes

    @staticmethod
    def _validate_action_targets(action: str, target_code_ids: list[str]) -> None:
        """Reject structurally impossible category-change proposals."""

        minimum_targets = {
            "add_parent": 2,
            "refine": 1,
            "merge": 2,
            "split": 1,
            "rename": 1,
        }
        minimum = minimum_targets.get(action, 0)
        if len(target_code_ids) < minimum:
            raise AgentExecutionError(
                f"Action '{action}' requires at least {minimum} active target code id(s)."
            )

    @staticmethod
    def _validate_new_code_label_collisions(
        *,
        active_codes: list[CodeState],
        candidates: list[ProvisionalCode],
    ) -> None:
        """Reject additions whose English or Chinese label is already active."""

        active_labels: set[str] = set()
        for code in active_codes:
            labels = [code.name, code.metadata.get("name_zh", "")]
            active_labels.update(
                " ".join(str(label).split()).casefold()
                for label in labels
                if str(label).strip()
            )
        for candidate in candidates:
            if (
                candidate.relationship_to_codebook != "new_code"
                and candidate.proposed_codebook_action != "add"
            ):
                continue
            candidate_labels = {
                " ".join(label.split()).casefold()
                for label in [candidate.code_name, candidate.code_name_zh]
                if label.strip()
            }
            if candidate_labels & active_labels:
                raise AgentExecutionError(
                    "New-code candidate duplicates an active English or Chinese label. "
                    "Use reuse/refine, or provide a genuinely distinct label and boundary."
                )

    @staticmethod
    def _validate_change_recommendation_consistency(
        *,
        changes: list[CodebookChangeState],
        candidates: list[ProvisionalCode],
    ) -> None:
        """Require every actionable proposal to include editable result definitions."""

        required_result_counts: dict[str, tuple[int, int | None]] = {
            "add": (1, None),
            "add_parent": (1, 1),
            "refine": (1, 1),
            "merge": (1, 1),
            "split": (2, None),
            "rename": (1, 1),
        }
        for change in changes:
            if change.action not in required_result_counts:
                continue
            resulting_names = change.metadata.get("resulting_code_names", [])
            if not isinstance(resulting_names, list):
                resulting_names = []
            normalized_result_names = {
                " ".join(str(name).split()).casefold()
                for name in resulting_names
                if str(name).strip()
            }
            minimum, maximum = required_result_counts[change.action]
            result_count = len(normalized_result_names)
            if result_count < minimum or (
                maximum is not None and result_count > maximum
            ):
                expected = str(minimum) if maximum == minimum else f"at least {minimum}"
                raise AgentExecutionError(
                    f"Codebook change '{change.action}' requires {expected} distinct "
                    "resulting_code_names."
                )
            target_ids = set(change.target_code_ids)
            matching = [
                candidate
                for candidate in candidates
                if candidate.proposed_codebook_action == change.action
                and set(candidate.proposed_codebook_target_ids) == target_ids
                and " ".join(candidate.code_name.split()).casefold()
                in normalized_result_names
            ]
            matched_names = {
                " ".join(candidate.code_name.split()).casefold()
                for candidate in matching
            }
            if (
                len(matching) != result_count
                or matched_names != normalized_result_names
            ):
                raise AgentExecutionError(
                    f"Codebook change '{change.action}' requires exactly one matching "
                    "recommended or preserved candidate definition for every resulting "
                    "code name, with the same target code ids."
                )

    @classmethod
    def _validate_relationship_targets(
        cls,
        *,
        relationship: str,
        linked_code_ids: list[str],
        action: str,
        target_code_ids: list[str],
    ) -> None:
        """Keep candidate mappings consistent with the active codebook."""

        required_links = {
            "reuse_existing_code": 1,
            "add_parent_code": 2,
            "refine_existing_code": 1,
            "merge_existing_codes": 2,
            "split_existing_code": 1,
        }
        minimum = required_links.get(relationship, 0)
        if len(linked_code_ids) < minimum:
            raise AgentExecutionError(
                f"Relationship '{relationship}' requires at least {minimum} active linked code id(s)."
            )
        cls._validate_action_targets(action, target_code_ids)

    def _parse_comparison_findings(
        self,
        rows: Any,
        *,
        artifact_id: str,
        evidence_lookup: dict[str, EvidenceItem],
        history_lookup: dict[str, CodingRecordState],
        active_code_ids: set[str],
    ) -> list[ComparisonFinding]:
        if not isinstance(rows, list):
            raise AgentExecutionError("Comparison findings must be an array.")
        findings: list[ComparisonFinding] = []
        for index, raw_row in enumerate(rows, start=1):
            if not isinstance(raw_row, dict):
                raise AgentExecutionError("Comparison finding must be a JSON object.")
            row = dict(raw_row)
            row.setdefault("summary_zh", row.get("summary", ""))
            row.setdefault("implication_zh", row.get("implication", ""))
            row = require_fields(
                row,
                required_fields=[
                    "comparison_type",
                    "finding",
                    "summary",
                    "summary_zh",
                    "compared_artifact_ids",
                    "compared_code_ids",
                    "evidence_refs",
                    "implication",
                    "implication_zh",
                ],
            )
            findings.append(
                ComparisonFinding(
                    comparison_id=f"comparison-{artifact_id}-{index}",
                    comparison_type=_require_allowed_value(
                        row["comparison_type"],
                        field_name="comparison_type",
                        allowed_values=_ALLOWED_COMPARISON_TYPES,
                    ),  # type: ignore[arg-type]
                    finding=_require_allowed_value(
                        row["finding"],
                        field_name="finding",
                        allowed_values=_ALLOWED_COMPARISON_FINDINGS,
                    ),  # type: ignore[arg-type]
                    summary=str(row["summary"]).strip(),
                    summary_zh=str(row["summary_zh"]).strip(),
                    current_artifact_id=artifact_id,
                    compared_artifact_ids=self._known_history_ids(
                        row["compared_artifact_ids"],
                        history_lookup=history_lookup,
                        field_name="compared_artifact_ids",
                    ),
                    compared_code_ids=self._known_code_ids(
                        row["compared_code_ids"],
                        active_code_ids=active_code_ids,
                        field_name="compared_code_ids",
                    ),
                    evidence_items=_resolve_evidence_refs(
                        row["evidence_refs"],
                        evidence_lookup=evidence_lookup,
                        field_name="evidence_refs",
                    ),
                    implication=str(row["implication"]).strip(),
                    implication_zh=str(row["implication_zh"]).strip(),
                    resolution_status=(
                        _require_allowed_value(row["resolution_status"], field_name="resolution_status",
                            allowed_values={"unresolved", "resolved", "complementary", "permitted"})
                        if row.get("resolution_status") is not None else None
                    ),
                )
            )
        for finding in findings:
            if finding.comparison_type == "case_to_case" and not finding.compared_artifact_ids:
                raise AgentExecutionError(
                    "A case_to_case finding must reference at least one reviewed artifact."
                )
            if finding.comparison_type == "case_to_code" and not finding.compared_code_ids:
                raise AgentExecutionError(
                    "A case_to_code finding must reference at least one active code."
                )
            if finding.comparison_type == "code_to_code" and len(finding.compared_code_ids) < 2:
                raise AgentExecutionError(
                    "A code_to_code finding must reference at least two active codes."
                )
        return findings

    def _parse_analytic_memos(
        self,
        rows: Any,
        *,
        artifact_id: str,
        history_lookup: dict[str, CodingRecordState],
        active_code_ids: set[str],
    ) -> list[AnalyticMemo]:
        if not isinstance(rows, list):
            raise AgentExecutionError("Analytic memos must be an array.")
        memos: list[AnalyticMemo] = []
        for index, raw_row in enumerate(rows, start=1):
            if not isinstance(raw_row, dict):
                raise AgentExecutionError("Analytic memo must be a JSON object.")
            row = dict(raw_row)
            row.setdefault("summary_zh", row.get("summary", ""))
            row.setdefault("status", "open")
            row = require_fields(
                row,
                required_fields=[
                    "memo_type",
                    "summary",
                    "summary_zh",
                    "artifact_ids",
                    "code_ids",
                    "status",
                ],
            )
            referenced_artifacts = _require_string_list(
                row["artifact_ids"], field_name="artifact_ids"
            )
            valid_artifact_ids = {artifact_id, *history_lookup.keys()}
            unknown_artifacts = set(referenced_artifacts) - valid_artifact_ids
            if unknown_artifacts:
                raise AgentExecutionError(
                    "Unknown artifact ids in field 'artifact_ids': "
                    + ", ".join(sorted(unknown_artifacts))
                )
            memos.append(
                AnalyticMemo(
                    memo_id=f"memo-{artifact_id}-{index}",
                    memo_type=_require_allowed_value(
                        row["memo_type"],
                        field_name="memo_type",
                        allowed_values=_ALLOWED_MEMO_TYPES,
                    ),  # type: ignore[arg-type]
                    summary=str(row["summary"]).strip(),
                    summary_zh=str(row["summary_zh"]).strip(),
                    artifact_ids=referenced_artifacts,
                    code_ids=self._known_code_ids(
                        row["code_ids"],
                        active_code_ids=active_code_ids,
                        field_name="code_ids",
                    ),
                    status=_require_allowed_value(
                        row["status"],
                        field_name="status",
                        allowed_values=_ALLOWED_MEMO_STATUSES,
                    ),  # type: ignore[arg-type]
                )
            )
        return memos

    @staticmethod
    def _known_history_ids(
        value: Any,
        *,
        history_lookup: dict[str, CodingRecordState],
        field_name: str,
    ) -> list[str]:
        artifact_ids = _require_string_list(value, field_name=field_name)
        unknown = set(artifact_ids) - set(history_lookup)
        if unknown:
            raise AgentExecutionError(
                f"Unknown historical artifact ids in field '{field_name}': "
                + ", ".join(sorted(unknown))
            )
        return artifact_ids

    @staticmethod
    def _known_code_ids(
        value: Any,
        *,
        active_code_ids: set[str],
        field_name: str,
    ) -> list[str]:
        code_ids = _require_string_list(value, field_name=field_name)
        unknown = set(code_ids) - active_code_ids
        if unknown:
            raise AgentExecutionError(
                f"Unknown active code ids in field '{field_name}': "
                + ", ".join(sorted(unknown))
            )
        return code_ids


# Keep the original class names available to scripts and old integrations.
ArbitrationAgentSettings = ComparisonAgentSettings
ArbitrationLLMAgent = ComparisonLLMAgent
