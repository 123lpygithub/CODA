from __future__ import annotations

import json
import re
from dataclasses import asdict, replace
from typing import Any

from adapters.base import ArtifactRecord, SourceRef, TextLocator
from coda.contracts import CoderAgentOutput, ContextPacket, EvidenceItem, ProvisionalCode
from coda.state import AnalysisProtocolState, CodeState, CodingRecordState


_CODEBOOK_RELATIONSHIPS = {
    "reuse_existing_code",
    "new_code",
    "add_parent_code",
    "refine_existing_code",
    "merge_existing_codes",
    "split_existing_code",
    "uncertain",
}

_CONFIDENCE_FACTOR_VALUES = {
    "high",
    "medium",
    "low",
    "not_applicable",
}


def normalize_confidence_factor(value: Any) -> str:
    """Normalize unambiguous model variants to the confidence-factor enum."""

    raw = str(value).strip()
    normalized = re.sub(r"[^a-z0-9]+", "_", raw.casefold()).strip("_")
    aliases = {
        "strong": "high",
        "sufficient": "high",
        "direct": "high",
        "adequate": "high",
        "moderate": "medium",
        "partial": "medium",
        "mixed": "medium",
        "weak": "low",
        "insufficient": "low",
        "limited": "low",
        "unclear": "low",
        "na": "not_applicable",
        "n_a": "not_applicable",
        "none": "not_applicable",
    }
    candidate = aliases.get(normalized, normalized)
    if candidate not in _CONFIDENCE_FACTOR_VALUES:
        allowed_text = ", ".join(sorted(_CONFIDENCE_FACTOR_VALUES))
        raise ValueError(
            f"Confidence factor received unsupported value {raw!r}; expected one of: "
            f"{allowed_text}."
        )
    return candidate


def normalize_confidence_factors(
    value: Any,
    *,
    required_keys: set[str],
    not_applicable_keys: set[str] | None = None,
) -> dict[str, str]:
    """Validate factor names and normalize every factor value."""

    if not isinstance(value, dict):
        raise ValueError("Field 'confidence_factors' must be an object.")
    actual_keys = {str(key) for key in value}
    if actual_keys != required_keys:
        missing = sorted(required_keys - actual_keys)
        unexpected = sorted(actual_keys - required_keys)
        details = []
        if missing:
            details.append(f"missing keys: {', '.join(missing)}")
        if unexpected:
            details.append(f"unexpected keys: {', '.join(unexpected)}")
        raise ValueError(
            "Field 'confidence_factors' must contain exactly the required keys "
            f"({'; '.join(details)})."
        )
    normalized = {
        str(key): normalize_confidence_factor(factor_value)
        for key, factor_value in value.items()
    }
    for key in not_applicable_keys or set():
        if normalized[key] != "not_applicable":
            raise ValueError(
                f"Confidence factor '{key}' must be 'not_applicable' in this stage."
            )
    return normalized


def normalize_codebook_relationship(value: Any) -> str:
    """Normalize common LLM variants to the contract's relationship enum.

    Prompts request exact snake_case values, but models sometimes return labels
    such as ``new code`` or ``reuse``. The persisted contract remains strict;
    this boundary only normalizes unambiguous presentation variants.
    """

    raw = str(value).strip()
    normalized = re.sub(r"[^a-z0-9]+", "_", raw.casefold()).strip("_")
    aliases = {
        "reuse": "reuse_existing_code",
        "reuse_code": "reuse_existing_code",
        "existing_code": "reuse_existing_code",
        "new": "new_code",
        "new_concept": "new_code",
        "new_code_candidate": "new_code",
        "add_parent": "add_parent_code",
        "add_parent_category": "add_parent_code",
        "refine": "refine_existing_code",
        "refinement": "refine_existing_code",
        "refine_code": "refine_existing_code",
        "merge": "merge_existing_codes",
        "merge_existing_code": "merge_existing_codes",
        "split": "split_existing_code",
        "split_code": "split_existing_code",
        "unknown": "uncertain",
        "not_sure": "uncertain",
        "not_applicable": "uncertain",
        "no_clear_relationship": "uncertain",
    }
    non_english_aliases = {
        "复用现有代码": "reuse_existing_code",
        "复用已有代码": "reuse_existing_code",
        "新增代码": "new_code",
        "新增父级代码": "add_parent_code",
        "新增父级类别": "add_parent_code",
        "新代码": "new_code",
        "细化现有代码": "refine_existing_code",
        "细化已有代码": "refine_existing_code",
        "合并现有代码": "merge_existing_codes",
        "合并已有代码": "merge_existing_codes",
        "拆分现有代码": "split_existing_code",
        "拆分已有代码": "split_existing_code",
        "不确定": "uncertain",
    }
    candidate = non_english_aliases.get(raw, aliases.get(normalized, normalized))
    if candidate not in _CODEBOOK_RELATIONSHIPS:
        allowed_text = ", ".join(sorted(_CODEBOOK_RELATIONSHIPS))
        raise ValueError(
            f"Field 'relationship_to_codebook' received unsupported value "
            f"{raw!r}; expected one of: {allowed_text}."
        )
    return candidate


def truncate_text(value: str, *, max_chars: int) -> str:
    text = value.strip()
    if len(text) <= max_chars:
        return text
    return text[: max_chars - 3].rstrip() + "..."


def stringify_raw_fields(
    raw_fields: dict[str, Any],
    *,
    max_value_chars: int,
) -> str:
    rendered: dict[str, Any] = {}
    for key, value in raw_fields.items():
        if isinstance(value, str):
            rendered[key] = truncate_text(value, max_chars=max_value_chars)
        else:
            rendered[key] = value
    return json.dumps(rendered, ensure_ascii=False, indent=2)


def serialize_codebook(codes: list[CodeState]) -> str:
    if not codes:
        return "No active codes yet."
    rows = []
    for code in codes:
        rows.append(
            {
                "code_id": code.code_id,
                "name": code.name,
                "definition": code.definition,
                "inclusion_criteria": code.inclusion_criteria,
                "exclusion_criteria": code.exclusion_criteria,
                "inclusion_criteria_zh": code.metadata.get("inclusion_criteria_zh", []),
                "exclusion_criteria_zh": code.metadata.get("exclusion_criteria_zh", []),
                "representative_artifact_ids": code.representative_artifact_ids,
                "parent_code_id": code.parent_code_id,
            }
        )
    return json.dumps(rows, ensure_ascii=False, indent=2)


def serialize_analysis_protocol(protocol: AnalysisProtocolState | None) -> str:
    """Render the frozen analytical rules supplied to every model stage."""

    if protocol is None:
        return "No explicit analysis protocol was supplied."
    return json.dumps(
        {
            "artifact_unit": protocol.artifact_unit,
            "evidence_unit": protocol.evidence_unit,
            "allow_cross_span_evidence": protocol.allow_cross_span_evidence,
            "allow_multiple_codes": protocol.allow_multiple_codes,
            "allow_unit_adjustment": protocol.allow_unit_adjustment,
            "predefined_codebook_allowed": protocol.predefined_codebook_allowed,
            "held_out_may_update_codebook": protocol.held_out_may_update_codebook,
            "notes": protocol.notes,
        },
        ensure_ascii=False,
        indent=2,
    )


def serialize_history(
    records: list[CodingRecordState],
    *,
    limit: int,
    analytic_memos: list[dict[str, Any]] | None = None,
    unresolved_cases: list[Any] | None = None,
    context_requests: list[Any] | None = None,
    stage_reviews: list[Any] | None = None,
    historical_materials: dict[str, Any] | None = None,
) -> str:
    if not records and not analytic_memos and not unresolved_cases and not context_requests and not stage_reviews:
        return "No reviewed examples yet."
    rows = []
    for record in records[-limit:]:
        human_reviewed = bool(record.metadata.get("human_reviewed", True))
        rows.append(
            {
                "artifact_id": record.artifact_id,
                "record_id": record.record_id,
                "source_material": (historical_materials or {}).get(record.artifact_id, {
                    "status": "unavailable", "reason": "Original historical material was not supplied."}),
                "decision": record.decision,
                "final_code_ids": record.final_code_ids,
                "final_code_names": record.final_code_names,
                "rationale": record.rationale,
                "evidence_summary": record.evidence_summary,
                "codebook_version_before": record.codebook_version_before,
                "codebook_version_after": record.codebook_version_after,
                "human_reviewed": human_reviewed,
                "review_origin": record.metadata.get(
                    "review_origin",
                    "human_review" if human_reviewed else "automatic",
                ),
            }
        )
    return json.dumps(
        {
            "coding_cases": rows,
            "recent_analytic_memos": list(analytic_memos or [])[-limit:],
            "open_unresolved_cases": [
                _serialize_history_item(item)
                for item in list(unresolved_cases or [])
                if getattr(item, "status", "open") == "open"
            ][-limit:],
            "context_requests": [
                _serialize_history_item(item)
                for item in list(context_requests or [])
                if getattr(item, "status", "pending") in {"pending", "resolved"}
            ][-limit:],
            "stage_reviews": [
                _serialize_history_item(item)
                for item in list(stage_reviews or [])
            ][-limit:],
        },
        ensure_ascii=False,
        indent=2,
    )


def _serialize_history_item(item: Any) -> Any:
    """Convert state dataclasses to prompt-safe JSON values."""

    if hasattr(item, "__dataclass_fields__"):
        return asdict(item)
    if isinstance(item, dict):
        return dict(item)
    return str(item)


def find_text_locator(text: str, excerpt: str) -> TextLocator | None:
    if not text or not excerpt:
        return None
    start = text.find(excerpt)
    if start < 0:
        tokens = excerpt.split()
        if not tokens:
            return None
        match = re.search(r"\s+".join(re.escape(token) for token in tokens), text)
        if match is None:
            return None
        return TextLocator(start=match.start(), end=match.end())
    return TextLocator(start=start, end=start + len(excerpt))


def match_source_ref(
    source_refs: list[SourceRef],
    *,
    field_name: str,
) -> SourceRef | None:
    normalized = field_name.strip().casefold()
    for source_ref in source_refs:
        if source_ref.field and source_ref.field.strip().casefold() == normalized:
            return source_ref
    for source_ref in source_refs:
        if source_ref.field and source_ref.field.strip().casefold() in normalized:
            return source_ref
    return source_refs[0] if source_refs else None


def build_evidence_item(
    artifact: ArtifactRecord,
    *,
    field_name: str,
    excerpt: str,
    rationale: str,
    rationale_zh: str = "",
    claim_type: str = "reported",
    revision: str | None = None,
) -> EvidenceItem:
    if revision is not None:
        visible = json.dumps({"content": artifact.content, "raw_fields": artifact.raw_fields,
                              "source_refs": [asdict(ref) for ref in artifact.source_refs]}, ensure_ascii=False)
        if not revision.strip() or revision not in visible:
            raise ValueError("Evidence revision is not present in the supplied source material.")
    raw_value = artifact.raw_fields.get(field_name)
    field_text = raw_value if isinstance(raw_value, str) else artifact.content
    locator = find_text_locator(field_text, excerpt)
    if locator is None or locator.start is None or locator.end is None:
        raise ValueError(
            f"Evidence excerpt is not present in artifact field '{field_name}'."
        )
    exact_excerpt = field_text[locator.start : locator.end]
    source_ref = match_source_ref(artifact.source_refs, field_name=field_name)
    return EvidenceItem(
        field_name=field_name,
        excerpt=exact_excerpt,
        locator=locator,
        source_ref=source_ref,
        rationale=rationale,
        rationale_zh=rationale_zh,
        claim_type=claim_type,
        revision=revision,
    )


def ground_context_packet(
    artifact: ArtifactRecord,
    context_packet: ContextPacket,
) -> ContextPacket:
    """Canonicalize every excerpt to real source offsets or reject the packet."""

    if context_packet.artifact_id != artifact.artifact_id:
        raise ValueError("Context packet belongs to a different artifact.")
    grounded: list[EvidenceItem] = []
    for item in context_packet.evidence_items:
        field_name = item.field_name
        if field_name not in artifact.raw_fields:
            field_name = "content"
        grounded.append(
            build_evidence_item(
                artifact,
                field_name=field_name,
                excerpt=item.excerpt,
                rationale=item.rationale,
                rationale_zh=item.rationale_zh,
                claim_type=item.claim_type,
                revision=item.revision,
            )
        )
    return replace(context_packet, evidence_items=grounded)


def select_relevant_history(
    records: list[CodingRecordState],
    *,
    query_text: str,
    relevant_code_ids: set[str] | None = None,
    representative_artifact_ids: set[str] | None = None,
    limit: int,
) -> list[CodingRecordState]:
    """Retrieve older comparison cases by code links, representatives, and text overlap."""

    if limit <= 0 or not records:
        return []
    query_terms = set(re.findall(r"[a-z0-9_]{3,}", query_text.casefold()))
    code_ids = relevant_code_ids or set()
    representative_ids = representative_artifact_ids or set()
    latest_by_artifact: dict[str, tuple[int, CodingRecordState]] = {}
    for index, record in enumerate(records):
        latest_by_artifact[record.artifact_id] = (index, record)

    scored: list[tuple[float, int, CodingRecordState]] = []
    for index, record in latest_by_artifact.values():
        record_text = " ".join(
            [
                *record.final_code_names,
                record.rationale,
                *record.evidence_summary,
                *record.preserved_alternatives,
            ]
        )
        record_terms = set(re.findall(r"[a-z0-9_]{3,}", record_text.casefold()))
        lexical = len(query_terms & record_terms) / max(1, len(query_terms | record_terms))
        linked = len(code_ids.intersection(record.final_code_ids))
        representative = 1 if record.artifact_id in representative_ids else 0
        boundary = 1 if any(
            signal in {"boundary_unclear", "category_overlap"}
            for signal in record.validation_signals
        ) else 0
        score = lexical + (2.0 * linked) + (1.5 * representative) + (0.5 * boundary)
        scored.append((score, index, record))

    scored.sort(key=lambda item: (item[0], item[1]), reverse=True)
    relevant = [item for item in scored if item[0] > 0][:limit]
    if len(relevant) < limit:
        selected_ids = {item[2].record_id for item in relevant}
        fallback = [item for item in sorted(scored, key=lambda row: row[1], reverse=True) if item[2].record_id not in selected_ids]
        relevant.extend(fallback[: limit - len(relevant)])
    return [item[2] for item in relevant]


def serialize_context_packet(context_packet: ContextPacket) -> str:
    rows = []
    for index, evidence in enumerate(context_packet.evidence_items, start=1):
        rows.append(
            {
                "evidence_id": f"E{index}",
                "claim_type": evidence.claim_type,
                "revision": evidence.revision,
                "source_ref": asdict(evidence.source_ref) if evidence.source_ref else None,
                "location": asdict(evidence.locator) if evidence.locator else None,
                "field_name": evidence.field_name,
                "excerpt": evidence.excerpt,
                "rationale": evidence.rationale,
                "rationale_zh": evidence.rationale_zh,
            }
        )
    return json.dumps(
        {
            "context_brief": context_packet.context_brief,
            "context_brief_zh": context_packet.context_brief_zh,
            "evidence_items": rows,
            "missing_context_warnings": context_packet.missing_context_warnings,
            "missing_context_warnings_zh": context_packet.missing_context_warnings_zh,
            "distracting_information": context_packet.distracting_information,
            "distracting_information_zh": context_packet.distracting_information_zh,
        },
        ensure_ascii=False,
        indent=2,
    )


def serialize_provisional_codes(
    provisional_codes: list[ProvisionalCode],
    context_packet: ContextPacket,
) -> list[dict[str, Any]]:
    evidence_to_id = {
        id(evidence): f"E{index}"
        for index, evidence in enumerate(context_packet.evidence_items, start=1)
    }
    rows = []
    for code in provisional_codes:
        rows.append(
            {
                "code_name": code.code_name,
                "short_definition": code.short_definition,
                "code_name_zh": code.code_name_zh,
                "short_definition_zh": code.short_definition_zh,
                "inclusion_criteria": code.inclusion_criteria,
                "exclusion_criteria": code.exclusion_criteria,
                "inclusion_criteria_zh": code.inclusion_criteria_zh,
                "exclusion_criteria_zh": code.exclusion_criteria_zh,
                "observed_phenomenon": code.observed_phenomenon,
                "observed_phenomenon_zh": code.observed_phenomenon_zh,
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


def serialize_coder_outputs(
    coder_outputs: list[CoderAgentOutput],
    context_packet: ContextPacket,
) -> str:
    rows = []
    for coder_output in coder_outputs:
        rows.append(
            {
                "coder_id": coder_output.coder_id,
                "insufficient_context": coder_output.insufficient_context,
                "overall_uncertainty": coder_output.overall_uncertainty,
                "overall_uncertainty_zh": coder_output.overall_uncertainty_zh,
                "confidence_level": coder_output.confidence_level,
                "confidence_rationale": coder_output.confidence_rationale,
                "confidence_rationale_zh": coder_output.confidence_rationale_zh,
                "confidence_factors": coder_output.confidence_factors,
                "notes": coder_output.notes,
                "notes_zh": coder_output.notes_zh,
                "provisional_codes": serialize_provisional_codes(
                    coder_output.provisional_codes,
                    context_packet,
                ),
            }
        )
    return json.dumps(rows, ensure_ascii=False, indent=2)
