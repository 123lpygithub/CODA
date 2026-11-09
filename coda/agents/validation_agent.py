from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

from coda.agents.base import AgentExecutionError, AgentPromptSpec, BaseLLMAgent
from coda.agents.common import (
    normalize_confidence_factors,
    select_relevant_history,
    serialize_analysis_protocol,
    serialize_codebook,
    serialize_coder_outputs,
    serialize_context_packet,
    serialize_history,
)
from coda.contracts import (
    ArbitrationOutput,
    ConfidenceLevel,
    EvidenceItem,
    ValidationInput,
    ValidationIssueScope,
    ValidationOutput,
    ReviewCriterion,
    ValidationSignal,
)
from coda.llm import ChatBackend, LLMModelConfig
from coda.parsing import require_fields
from coda.prompts import read_prompt_file

_ALLOWED_VALIDATION_SIGNALS = {
    "valid",
    "evidence_insufficient",
    "unsupported_inference",
    "use_case_mismatch",
    "category_overlap",
    "boundary_unclear",
    "context_missing",
    "human_review_required",
}
_ALLOWED_CONFIDENCE_LEVELS = {"high", "medium", "low"}
_ALLOWED_ISSUE_SCOPES = {"none", "evidence", "assignment", "codebook", "context"}
_ALLOWED_REVIEW_CRITERIA = {"R1", "R2", "R3", "R4", "R5", "R6"}

_DEFAULT_SCOPE_BY_SIGNAL: dict[str, ValidationIssueScope] = {
    "valid": "none",
    "evidence_insufficient": "evidence",
    "unsupported_inference": "evidence",
    "use_case_mismatch": "codebook",
    "category_overlap": "assignment",
    "boundary_unclear": "assignment",
    "context_missing": "context",
    "human_review_required": "assignment",
}


def _parse_confidence_level(value: Any) -> ConfidenceLevel:
    normalized = str(value).strip().casefold()
    if normalized not in _ALLOWED_CONFIDENCE_LEVELS:
        raise AgentExecutionError(
            "Field 'confidence_level' must be one of: high, medium, low."
        )
    return normalized  # type: ignore[return-value]


@dataclass(frozen=True)
class ValidationAgentSettings:
    """Configuration for the first Validation Agent implementation."""

    history_example_limit: int = 6


def _build_evidence_lookup(
    evidence_items: list[EvidenceItem],
) -> dict[str, EvidenceItem]:
    return {
        f"E{index}": evidence_item
        for index, evidence_item in enumerate(evidence_items, start=1)
    }


def _normalize_code_name(name: str) -> str:
    return " ".join(name.split()).strip().casefold().replace("-", " ")


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


def _require_signal_name(value: Any) -> str:
    normalized = str(value).strip()
    if normalized not in _ALLOWED_VALIDATION_SIGNALS:
        allowed_text = ", ".join(sorted(_ALLOWED_VALIDATION_SIGNALS))
        raise AgentExecutionError(
            f"Field 'signal' must be one of: {allowed_text}."
        )
    return normalized


def _require_issue_scope(value: Any, *, signal: str) -> ValidationIssueScope:
    normalized = str(value).strip()
    if normalized not in _ALLOWED_ISSUE_SCOPES:
        allowed_text = ", ".join(sorted(_ALLOWED_ISSUE_SCOPES))
        raise AgentExecutionError(
            f"Field 'issue_scope' must be one of: {allowed_text}."
        )
    if signal == "valid" and normalized != "none":
        raise AgentExecutionError("A 'valid' signal must use issue_scope 'none'.")
    if signal != "valid" and normalized == "none":
        raise AgentExecutionError("A non-valid signal cannot use issue_scope 'none'.")
    return normalized  # type: ignore[return-value]


def _build_preliminary_signals(agent_input: ValidationInput) -> list[dict[str, Any]]:
    signals: list[dict[str, Any]] = []
    recommended_codes = agent_input.arbitration_output.recommended_codes
    if not recommended_codes:
        signals.append(
            {
                "signal": "human_review_required",
                "issue_scope": "assignment",
                "summary": "Arbitration did not produce any recommended code.",
                "related_code_names": [],
                "evidence_refs": [],
            }
        )
    for code in recommended_codes:
        if not code.supporting_evidence:
            signals.append(
                {
                    "signal": "evidence_insufficient",
                    "issue_scope": "evidence",
                    "summary": f"Recommended code '{code.code_name}' has no supporting evidence.",
                    "related_code_names": [code.code_name],
                    "evidence_refs": [],
                }
            )
        elif any(
            item.locator is None
            or item.locator.start is None
            or item.locator.end is None
            for item in code.supporting_evidence
        ):
            signals.append(
                {
                    "signal": "evidence_insufficient",
                    "issue_scope": "evidence",
                    "summary": f"Recommended code '{code.code_name}' contains unlocated evidence.",
                    "related_code_names": [code.code_name],
                    "evidence_refs": [],
                }
            )
    if agent_input.context_packet.missing_context_warnings:
        signals.append(
            {
                "signal": "context_missing",
                "issue_scope": "context",
                "summary": "Context Agent reported missing-context warnings.",
                "related_code_names": [code.code_name for code in recommended_codes],
                "evidence_refs": [],
            }
        )
    active_code_names = {
        _normalize_code_name(code.name): code.name
        for code in agent_input.codebook.active_codes()
    }
    for code in recommended_codes:
        if (
            code.relationship_to_codebook == "new_code"
            and _normalize_code_name(code.code_name) in active_code_names
        ):
            signals.append(
                {
                    "signal": "category_overlap",
                    "issue_scope": "assignment",
                    "summary": (
                        f"Proposed new code '{code.code_name}' overlaps with an existing "
                        f"active code name."
                    ),
                    "related_code_names": [code.code_name],
                    "evidence_refs": [],
                }
            )
    if agent_input.arbitration_output.disagreements:
        signals.append(
            {
                "signal": "boundary_unclear",
                "issue_scope": "assignment",
                "summary": "Arbitration preserved substantive disagreement across coders.",
                "related_code_names": [
                    code.code_name for code in recommended_codes
                ],
                "evidence_refs": [],
            }
        )
    if not signals:
        signals.append(
            {
                "signal": "valid",
                "issue_scope": "none",
                "summary": "No immediate structural problems were detected before validation.",
                "related_code_names": [code.code_name for code in recommended_codes],
                "evidence_refs": [],
            }
        )
    return signals


def _serialize_arbitration_output(
    arbitration_output: ArbitrationOutput,
    evidence_items: list[EvidenceItem],
) -> str:
    evidence_to_id = {
        id(evidence): f"E{index}"
        for index, evidence in enumerate(evidence_items, start=1)
    }

    def serialize_codes(codes):
        rows: list[dict[str, Any]] = []
        for code in codes:
            rows.append(
                {
                    "code_name": code.code_name,
                    "short_definition": code.short_definition,
                    "code_name_zh": code.code_name_zh,
                    "short_definition_zh": code.short_definition_zh,
                    "inclusion_criteria": code.inclusion_criteria,
                    "exclusion_criteria": code.exclusion_criteria,
                    "supporting_evidence_refs": [
                        evidence_to_id[id(item)]
                        for item in code.supporting_evidence
                        if id(item) in evidence_to_id
                    ],
                    "relationship_to_codebook": code.relationship_to_codebook,
                    "linked_code_ids": code.linked_code_ids,
                    "alternative_interpretation": code.alternative_interpretation,
                    "alternative_interpretation_zh": code.alternative_interpretation_zh,
                    "uncertainty_note": code.uncertainty_note,
                    "uncertainty_note_zh": code.uncertainty_note_zh,
                    "proposed_codebook_action": code.proposed_codebook_action,
                    "proposed_codebook_target_ids": code.proposed_codebook_target_ids,
                }
            )
        return rows

    return json.dumps(
        {
            "agreement_summary": arbitration_output.agreement_summary,
            "agreement_summary_zh": arbitration_output.agreement_summary_zh,
            "disagreement_summary": arbitration_output.disagreement_summary,
            "disagreement_summary_zh": arbitration_output.disagreement_summary_zh,
            "recommended_codes": serialize_codes(arbitration_output.recommended_codes),
            "preserved_alternatives": serialize_codes(
                arbitration_output.preserved_alternatives
            ),
            "disagreements": [
                {
                    "disagreement_type": disagreement.disagreement_type,
                    "summary": disagreement.summary,
                    "summary_zh": disagreement.summary_zh,
                    "coder_ids": disagreement.coder_ids,
                    "affected_code_names": disagreement.affected_code_names,
                }
                for disagreement in arbitration_output.disagreements
            ],
            "comparison_findings": [
                {
                    "comparison_type": finding.comparison_type,
                    "finding": finding.finding,
                    "summary": finding.summary,
                    "summary_zh": finding.summary_zh,
                    "compared_artifact_ids": finding.compared_artifact_ids,
                    "compared_code_ids": finding.compared_code_ids,
                    "implication": finding.implication,
                    "implication_zh": finding.implication_zh,
                }
                for finding in arbitration_output.comparison_findings
            ],
            "analytic_memos": [
                {
                    "memo_type": memo.memo_type,
                    "summary": memo.summary,
                    "summary_zh": memo.summary_zh,
                    "artifact_ids": memo.artifact_ids,
                    "code_ids": memo.code_ids,
                    "status": memo.status,
                }
                for memo in arbitration_output.analytic_memos
            ],
        },
        ensure_ascii=False,
        indent=2,
    )


class ValidationLLMAgent(BaseLLMAgent):
    """LLM-backed Validation Agent for structured risk signaling."""

    def __init__(
        self,
        *,
        model_config: LLMModelConfig,
        backend: ChatBackend,
        settings: ValidationAgentSettings | None = None,
    ) -> None:
        prompt_spec = AgentPromptSpec(
            name="validation_agent",
            system_prompt=read_prompt_file("validation_system_prompt.txt"),
            user_prompt_template=read_prompt_file("validation_user_prompt.txt"),
        )
        super().__init__(
            prompt_spec=prompt_spec,
            model_config=model_config,
            backend=backend,
        )
        self._settings = settings or ValidationAgentSettings()

    def __call__(self, agent_input: ValidationInput) -> ValidationOutput:
        relevant_code_ids = {
            code_id
            for code in agent_input.arbitration_output.recommended_codes
            for code_id in [*code.linked_code_ids, *code.proposed_codebook_target_ids]
        }
        representative_ids = {
            artifact_id
            for code in agent_input.codebook.active_codes()
            if code.code_id in relevant_code_ids
            for artifact_id in code.representative_artifact_ids
        }
        relevant_history = select_relevant_history(
            agent_input.history.coding_records,
            query_text=" ".join(
                [
                    agent_input.artifact.content,
                    agent_input.context_packet.context_brief,
                    *(code.observed_phenomenon for code in agent_input.arbitration_output.recommended_codes),
                ]
            ),
            relevant_code_ids=relevant_code_ids,
            representative_artifact_ids=representative_ids,
            limit=self._settings.history_example_limit,
        )
        return self.invoke_validated_json_object(
            lambda payload, response: self._payload_to_validation_output(
                agent_input, payload, response
            ),
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
            arbitration_output_json=_serialize_arbitration_output(
                agent_input.arbitration_output,
                agent_input.context_packet.evidence_items,
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
            preliminary_signals_json=json.dumps(
                _build_preliminary_signals(agent_input),
                ensure_ascii=False,
                indent=2,
            ),
            validation_scope=agent_input.validation_scope,
            corpus_audit_json=json.dumps(agent_input.corpus_audit, ensure_ascii=False),
        )

    def _payload_to_validation_output(
        self,
        agent_input: ValidationInput,
        payload: dict[str, Any],
        response,
    ) -> ValidationOutput:
        payload = dict(payload)
        payload.setdefault("summary_zh", payload["summary"])
        payload.setdefault("notes_zh", payload.get("notes", []))
        # Confidence is descriptive only; R1-R6 and policy determine routing.
        payload.setdefault("confidence_level", "low")
        payload.setdefault("confidence_rationale", payload["summary"])
        payload.setdefault("confidence_rationale_zh", payload["summary_zh"])
        payload.setdefault("confidence_factors", {})
        payload = require_fields(
            payload,
            required_fields=[
                "signals",
                "human_review_required",
                "summary",
                "summary_zh",
                "notes",
                "notes_zh",
            ],
        )
        evidence_lookup = _build_evidence_lookup(
            agent_input.context_packet.evidence_items
        )
        signal_rows = payload["signals"]
        if not isinstance(signal_rows, list):
            raise AgentExecutionError("Validation output field 'signals' must be a list.")
        signals: list[ValidationSignal] = []
        for row in signal_rows:
            if not isinstance(row, dict):
                raise AgentExecutionError("Validation signal must be a JSON object.")
            row = dict(row)
            row.setdefault("summary_zh", row.get("summary", ""))
            signal_name = _require_signal_name(row.get("signal", ""))
            # Old model responses and persisted checkpoints predate issue_scope.
            # Infer a conservative routing scope rather than invalidating them.
            row.setdefault("issue_scope", _DEFAULT_SCOPE_BY_SIGNAL[signal_name])
            row = require_fields(
                row,
                required_fields=[
                    "signal",
                    "issue_scope",
                    "summary",
                    "summary_zh",
                    "related_code_names",
                    "evidence_refs",
                ],
            )
            signals.append(
                ValidationSignal(
                    signal=signal_name,  # type: ignore[arg-type]
                    summary=str(row["summary"]).strip(),
                    issue_scope=_require_issue_scope(
                        row["issue_scope"],
                        signal=signal_name,
                    ),
                    summary_zh=str(row["summary_zh"]).strip(),
                    related_code_names=_require_string_list(
                        row["related_code_names"],
                        field_name="related_code_names",
                    ),
                    evidence_items=_resolve_evidence_refs(
                        row["evidence_refs"],
                        evidence_lookup=evidence_lookup,
                        field_name="evidence_refs",
                    ),
                )
            )
        notes = payload["notes"]
        notes_zh = payload["notes_zh"]
        if not isinstance(notes, list):
            raise AgentExecutionError("Validation output field 'notes' must be a list.")
        if not isinstance(notes_zh, list):
            raise AgentExecutionError("Validation output field 'notes_zh' must be a list.")
        confidence_factors = normalize_confidence_factors(
            payload["confidence_factors"],
            required_keys={
                "evidence_support",
                "coder_agreement",
                "codebook_fit",
                "interpretive_ambiguity",
            },
        )
        criteria = payload.get("review_criteria", [])
        if not isinstance(criteria, list) or any(str(item) not in _ALLOWED_REVIEW_CRITERIA for item in criteria):
            raise AgentExecutionError("Validation output field 'review_criteria' must contain only R1-R6.")
        review_questions = payload.get("review_questions", [])
        review_questions_zh = payload.get("review_questions_zh", [])
        if not isinstance(review_questions, list) or not isinstance(review_questions_zh, list):
            raise AgentExecutionError("Validation review questions must be lists.")
        normalized_criteria = [str(item) for item in criteria]
        if not isinstance(payload["human_review_required"], bool):
            raise AgentExecutionError("Validation human_review_required must be a JSON boolean.")
        if payload["human_review_required"] and not normalized_criteria:
            raise AgentExecutionError("A human review request requires at least one R1-R6 criterion.")
        if len(review_questions) != len(normalized_criteria) or len(review_questions_zh) != len(normalized_criteria):
            raise AgentExecutionError(
                "Validation output must provide exactly one English and one Chinese "
                "review question for every R1-R6 criterion."
            )
        if any(not str(item).strip() for item in [*review_questions, *review_questions_zh]):
            raise AgentExecutionError(
                "Validation review questions must not contain empty strings."
            )
        return ValidationOutput(
            artifact_id=agent_input.artifact.artifact_id,
            signals=signals,
            human_review_required=bool(payload["human_review_required"]),
            summary=str(payload["summary"]).strip(),
            summary_zh=str(payload["summary_zh"]).strip(),
            confidence_level=_parse_confidence_level(payload["confidence_level"]),
            confidence_rationale=str(payload["confidence_rationale"]).strip(),
            confidence_rationale_zh=str(payload["confidence_rationale_zh"]).strip(),
            confidence_factors=confidence_factors,
            review_criteria=normalized_criteria,  # type: ignore[list-item]
            review_questions=[str(item).strip() for item in review_questions],
            review_questions_zh=[str(item).strip() for item in review_questions_zh],
            notes=[str(item).strip() for item in notes],
            notes_zh=[str(item).strip() for item in notes_zh],
            model_metadata=self.execution_metadata(response),
        )
