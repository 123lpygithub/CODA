from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from coda.agents.base import AgentExecutionError, AgentPromptSpec, BaseLLMAgent
from coda.agents.common import (
    normalize_confidence_factors,
    serialize_analysis_protocol,
    serialize_context_packet,
)
from coda.contracts import (
    ConfidenceLevel,
    CoderAgentInput,
    CoderAgentOutput,
    EvidenceItem,
    ProvisionalCode,
)
from coda.llm import ChatBackend, LLMModelConfig
from coda.parsing import require_fields
from coda.prompts import read_prompt_file

_ALLOWED_CONFIDENCE_LEVELS = {"high", "medium", "low"}


def _parse_confidence_level(value: Any) -> ConfidenceLevel:
    normalized = str(value).strip().casefold()
    if normalized not in _ALLOWED_CONFIDENCE_LEVELS:
        raise AgentExecutionError(
            "Field 'confidence_level' must be one of: high, medium, low."
        )
    return normalized  # type: ignore[return-value]


@dataclass(frozen=True)
class CoderAgentSettings:
    """Configuration for independent coder agents."""

    max_codes: int = 3


@dataclass(frozen=True)
class CoderPerspective:
    """Prompt identity for an independent, codebook-blind coder."""

    name: str
    strategy_instructions: str
    system_prompt_file: str
    user_prompt_file: str


BLIND_OPEN_CODING_PERSPECTIVE = CoderPerspective(
    name="blind_open_coding",
    strategy_instructions=(
        "Record the concrete observation, then give it the smallest evidence-supported "
        "analytical label above incidental syntax or identifiers. Stop before constructing "
        "a reusable codebook category or parent theme. "
        "Do not compare against a codebook, reuse labels, or recommend codebook "
        "changes; those decisions belong to Induction initially and Comparison during iteration. Avoid separate codes "
        "for differences limited to identifiers, literal values, APIs, or locations."
    ),
    system_prompt_file="coder_system_prompt.txt",
    user_prompt_file="coder_user_prompt.txt",
)

# The stage changes the downstream agent, not the independent coding prompt.
INITIAL_OPEN_CODING_PERSPECTIVE = BLIND_OPEN_CODING_PERSPECTIVE


def _build_evidence_lookup(
    evidence_items: list[EvidenceItem],
) -> dict[str, EvidenceItem]:
    return {
        f"E{index}": evidence_item
        for index, evidence_item in enumerate(evidence_items, start=1)
    }


class IndependentCoderLLMAgent(BaseLLMAgent):
    """LLM-backed independent coder that emits provisional codes."""

    def __init__(
        self,
        *,
        perspective: CoderPerspective,
        model_config: LLMModelConfig,
        backend: ChatBackend,
        settings: CoderAgentSettings | None = None,
    ) -> None:
        prompt_spec = AgentPromptSpec(
            name=f"coder_agent_{perspective.name}",
            system_prompt=read_prompt_file(perspective.system_prompt_file),
            user_prompt_template=read_prompt_file(perspective.user_prompt_file),
        )
        super().__init__(
            prompt_spec=prompt_spec,
            model_config=model_config,
            backend=backend,
        )
        self._perspective = perspective
        self._settings = settings or CoderAgentSettings()

    def __call__(self, agent_input: CoderAgentInput) -> CoderAgentOutput:
        # Keep one orchestration input contract, but deliberately do not expose
        # codebook/history to the independent open coder.
        return self.invoke_validated_json_object(
            lambda payload, response: self._payload_to_coder_output(
                agent_input, payload, response
            ),
            coder_id=agent_input.coder_id,
            coder_strategy=self._perspective.strategy_instructions,
            research_question=agent_input.research_question.question_text,
            analysis_scope=agent_input.research_question.analysis_scope,
            use_case=agent_input.research_question.use_case,
            analysis_protocol=serialize_analysis_protocol(agent_input.analysis_protocol),
            artifact_id=agent_input.artifact.artifact_id,
            artifact_content=agent_input.artifact.content,
            context_packet_json=serialize_context_packet(agent_input.context_packet),
            max_codes=self._settings.max_codes,
        )

    def _payload_to_coder_output(
        self,
        agent_input: CoderAgentInput,
        payload: dict[str, Any],
        response,
    ) -> CoderAgentOutput:
        payload = dict(payload)
        payload.setdefault("overall_uncertainty_zh", payload["overall_uncertainty"])
        payload.setdefault("notes_zh", payload.get("notes", []))
        # Confidence is descriptive metadata only. Missing legacy values do not
        # create a review criterion or change Selective/Automatic routing.
        payload.setdefault("confidence_level", "low")
        payload.setdefault("confidence_rationale", payload["overall_uncertainty"])
        payload.setdefault("confidence_rationale_zh", payload["overall_uncertainty_zh"])
        payload.setdefault("confidence_factors", {})
        payload = require_fields(
            payload,
            required_fields=[
                "provisional_codes",
                "insufficient_context",
                "overall_uncertainty",
                "overall_uncertainty_zh",
                "notes",
                "notes_zh",
            ],
        )
        provisional_rows = payload["provisional_codes"]
        if not isinstance(provisional_rows, list):
            raise AgentExecutionError(
                "Coder agent output field 'provisional_codes' must be a list."
            )
        evidence_lookup = _build_evidence_lookup(agent_input.context_packet.evidence_items)
        provisional_codes: list[ProvisionalCode] = []
        for row in provisional_rows:
            provisional_codes.append(
                self._parse_provisional_code(
                    row=row,
                    evidence_lookup=evidence_lookup,
                )
            )
        insufficient_context = bool(payload["insufficient_context"])
        overall_uncertainty = str(payload["overall_uncertainty"]).strip()
        overall_uncertainty_zh = str(payload["overall_uncertainty_zh"]).strip()
        confidence_factors = normalize_confidence_factors(
            payload["confidence_factors"],
            required_keys={
                "evidence_support",
                "context_sufficiency",
                "codebook_fit",
                "interpretive_ambiguity",
            },
            not_applicable_keys={"codebook_fit"},
        )
        confidence_level = _parse_confidence_level(payload["confidence_level"])
        if insufficient_context and (
            confidence_level == "high"
            or confidence_factors["context_sufficiency"] == "high"
        ):
            raise AgentExecutionError(
                "When 'insufficient_context' is true, 'confidence_level' and "
                "confidence_factors.context_sufficiency' cannot be high."
            )
        notes = payload["notes"]
        notes_zh = payload["notes_zh"]
        if not isinstance(notes, list):
            raise AgentExecutionError("Coder agent output field 'notes' must be a list.")
        if not isinstance(notes_zh, list):
            raise AgentExecutionError("Coder agent output field 'notes_zh' must be a list.")
        return CoderAgentOutput(
            artifact_id=agent_input.artifact.artifact_id,
            coder_id=agent_input.coder_id,
            provisional_codes=provisional_codes,
            insufficient_context=insufficient_context,
            overall_uncertainty=overall_uncertainty,
            overall_uncertainty_zh=overall_uncertainty_zh,
            confidence_level=confidence_level,
            confidence_rationale=str(payload["confidence_rationale"]).strip(),
            confidence_rationale_zh=str(payload["confidence_rationale_zh"]).strip(),
            confidence_factors=confidence_factors,
            notes=[str(item).strip() for item in notes],
            notes_zh=[str(item).strip() for item in notes_zh],
            model_metadata={
                **self.execution_metadata(response),
                "perspective": self._perspective.name,
            },
        )

    def _parse_provisional_code(
        self,
        *,
        row: Any,
        evidence_lookup: dict[str, EvidenceItem],
    ) -> ProvisionalCode:
        if not isinstance(row, dict):
            raise AgentExecutionError("Each provisional code must be a JSON object.")
        # These fields remain in the shared contract for Comparison Agent input,
        # but a blind coder must leave all codebook decisions neutral.
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
        supporting_evidence_refs = row["supporting_evidence_refs"]
        linked_code_ids = row["linked_code_ids"]
        proposed_codebook_target_ids = row["proposed_codebook_target_ids"]
        if not isinstance(supporting_evidence_refs, list):
            raise AgentExecutionError(
                "Provisional code field 'supporting_evidence_refs' must be a list."
            )
        if not isinstance(linked_code_ids, list):
            raise AgentExecutionError(
                "Provisional code field 'linked_code_ids' must be a list."
            )
        if not isinstance(proposed_codebook_target_ids, list):
            raise AgentExecutionError(
                "Provisional code field 'proposed_codebook_target_ids' must be a list."
            )
        unknown_evidence = [
            str(ref) for ref in supporting_evidence_refs if ref not in evidence_lookup
        ]
        if unknown_evidence:
            raise AgentExecutionError(
                "Unknown supporting evidence ref(s): " + ", ".join(unknown_evidence)
            )
        supporting_evidence = [evidence_lookup[ref] for ref in supporting_evidence_refs]
        relationship = str(row["relationship_to_codebook"]).strip()
        action = str(row["proposed_codebook_action"]).strip()
        if relationship != "uncertain":
            raise AgentExecutionError(
                "Blind coder field 'relationship_to_codebook' must be 'uncertain'."
            )
        if action != "no_change":
            raise AgentExecutionError(
                "Blind coder field 'proposed_codebook_action' must be 'no_change'."
            )
        linked_ids = [str(item).strip() for item in linked_code_ids]
        target_ids = [str(item).strip() for item in proposed_codebook_target_ids]
        if linked_ids or target_ids:
            raise AgentExecutionError(
                "Blind coder must leave linked_code_ids and proposed_codebook_target_ids empty."
            )
        return ProvisionalCode(
            code_name=str(row["code_name"]).strip(),
            short_definition=str(row["short_definition"]).strip(),
            code_name_zh=str(row["code_name_zh"]).strip(),
            short_definition_zh=str(row["short_definition_zh"]).strip(),
            observed_phenomenon=str(row["observed_phenomenon"]).strip(),
            observed_phenomenon_zh=str(row["observed_phenomenon_zh"]).strip(),
            supporting_evidence=supporting_evidence,
            relationship_to_codebook="uncertain",
            linked_code_ids=linked_ids,
            alternative_interpretation=str(row["alternative_interpretation"]).strip(),
            alternative_interpretation_zh=str(row["alternative_interpretation_zh"]).strip(),
            uncertainty_note=str(row["uncertainty_note"]).strip(),
            uncertainty_note_zh=str(row["uncertainty_note_zh"]).strip(),
            proposed_codebook_action="no_change",
            proposed_codebook_target_ids=target_ids,
        )


def build_open_coder(
    *,
    model_config: LLMModelConfig,
    backend: ChatBackend,
    settings: CoderAgentSettings | None = None,
) -> IndependentCoderLLMAgent:
    """Build the shared codebook-blind coder used by iterative coding."""

    return IndependentCoderLLMAgent(
        perspective=BLIND_OPEN_CODING_PERSPECTIVE,
        model_config=model_config,
        backend=backend,
        settings=settings,
    )


def build_initial_open_coder(
    *,
    model_config: LLMModelConfig,
    backend: ChatBackend,
    settings: CoderAgentSettings | None = None,
) -> IndependentCoderLLMAgent:
    """Build a coder that cannot rely on an existing codebook or reviewed history."""

    return IndependentCoderLLMAgent(
        perspective=INITIAL_OPEN_CODING_PERSPECTIVE,
        model_config=model_config,
        backend=backend,
        settings=settings,
    )
