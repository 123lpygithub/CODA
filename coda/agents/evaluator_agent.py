"""Independent evaluator agent for frozen CODA evaluation packets.

This agent is intentionally outside the coding workflow. It can only produce
RQ1 score rows; it has no codebook mutation or review-routing API.
"""

from __future__ import annotations

import json
import random
from typing import Any

from coda.agents.base import AgentExecutionError, AgentPromptSpec, BaseLLMAgent
from coda.evaluation import validate_rq1_score
from coda.llm import ChatBackend, LLMModelConfig
from coda.parsing import require_fields
from coda.prompts import read_prompt_file


def build_blinded_evaluator_packet(packet: dict[str, Any], *, seed: int = 20260907) -> dict[str, Any]:
    """Expose evidence and interpretations, excluding execution and approvals."""

    code_fields = (
        "code_id", "name", "definition", "inclusion_criteria", "exclusion_criteria",
        "parent_code_id", "representative_artifact_ids", "boundary_artifact_ids",
    )
    codes = [
        {key: code[key] for key in code_fields if key in code}
        for code in packet.get("codebook", {}).get("codes", [])
        if code.get("status", "active") == "active"
    ]
    artifacts = []
    for item in packet.get("artifacts", []):
        record = item.get("coding_record") or {}
        artifacts.append({
            "artifact_id": item["artifact_id"],
            "content": item.get("content", ""),
            "raw_fields": item.get("raw_fields", {}),
            "source_refs": item.get("source_refs", []),
            "coding_record": {
                key: record[key] for key in (
                    "final_code_ids", "rationale", "evidence_summary", "preserved_alternatives",
                ) if key in record
            },
        })
    # Same frozen presentation for every evaluator, independent of input order.
    # The seed and ordered identifiers suffice to reproduce this randomization.
    codes.sort(key=lambda item: str(item['code_id']))
    artifacts.sort(key=lambda item: str(item['artifact_id']))
    presentation = random.Random(seed)
    presentation.shuffle(codes)
    presentation.shuffle(artifacts)
    return {
        "research_question": {
            key: packet.get("research_question", {}).get(key)
            for key in ("question_text", "analysis_scope", "artifact_unit")
        },
        "analysis_protocol": {
            key: packet.get("analysis_protocol", {}).get(key)
            for key in ("artifact_unit", "evidence_unit", "allow_multiple_codes", "allow_cross_span_evidence")
        },
        "codebook": {"codes": codes},
        "artifacts": artifacts,
        "scoring_assignment_targets": packet.get("scoring_assignment_targets"),
        "evaluation_scope": packet.get("evaluation_scope", "codebook_and_assignments"),
        "presentation_seed": seed,
    }


class EvaluatorLLMAgent(BaseLLMAgent):
    """Score one frozen RQ1 packet using the independent evaluation rubric."""

    def __init__(self, *, model_config: LLMModelConfig, backend: ChatBackend) -> None:
        super().__init__(
            prompt_spec=AgentPromptSpec(
                name="independent_rq1_evaluator",
                system_prompt=read_prompt_file("evaluator_system_prompt.txt"),
                user_prompt_template=read_prompt_file("evaluator_user_prompt.txt"),
            ),
            model_config=model_config,
            backend=backend,
            bilingual_output=False,
        )

    def __call__(
        self,
        *,
        packet: dict[str, Any],
        run_id: str,
        evaluator_id: str,
        phase: str = "formal",
        candidate_model: str | None = None,
    ) -> list[dict[str, Any]]:
        if phase not in {"pilot", "formal"}:
            raise ValueError("Evaluator phase must be 'pilot' or 'formal'.")
        if not run_id.strip() or not evaluator_id.strip():
            raise ValueError("run_id and evaluator_id are required.")
        if candidate_model is not None and candidate_model != self.model_config.model:
            raise ValueError("Candidate evaluator identity must match the actual model configuration.")
        return self.invoke_validated_json_object(
            lambda payload, response: self._parse_scores(
                payload,
                response,
                run_id=run_id,
                evaluator_id=evaluator_id,
                phase=phase,
                candidate_model=candidate_model,
                packet=packet,
            ),
            packet_json=json.dumps(build_blinded_evaluator_packet(packet), ensure_ascii=False, indent=2),
        )

    def _parse_scores(
        self,
        payload: dict[str, Any],
        response: Any,
        *,
        run_id: str,
        evaluator_id: str,
        phase: str,
        candidate_model: str | None,
        packet: dict[str, Any],
    ) -> list[dict[str, Any]]:
        payload = require_fields(payload, required_fields=["scores"])
        rows = payload["scores"]
        if not isinstance(rows, list):
            raise AgentExecutionError("Evaluator field 'scores' must be a list.")
        metadata = self.execution_metadata(response)
        normalized: list[dict[str, Any]] = []
        for index, raw_row in enumerate(rows):
            if not isinstance(raw_row, dict):
                raise AgentExecutionError(f"Evaluator score {index} must be an object.")
            row = dict(raw_row)
            row["run_id"] = run_id
            row["evaluator_id"] = evaluator_id
            row["phase"] = phase
            if candidate_model is not None:
                row["candidate_model"] = candidate_model
            row["evaluator_kind"] = "llm"
            if not isinstance(row.get("rationale"), str) or not row["rationale"].strip():
                raise AgentExecutionError(
                    f"Evaluator score {index} requires a non-empty rationale."
                )
            try:
                validate_rq1_score(row)
            except Exception as error:
                raise AgentExecutionError(
                    f"Invalid evaluator score {index}: {error}"
                ) from error
            row["evaluator_metadata"] = metadata
            normalized.append(row)
        if not normalized:
            raise AgentExecutionError("Evaluator must return at least one score row.")
        if "evaluation_scope" in packet:
            scope = packet["evaluation_scope"]
            expected = set()
            if scope in {"codebook_only", "codebook_and_assignments"}:
                expected.update((dimension, "codebook", None, None) for dimension in (
                    "clarity", "category_boundaries", "meaningful_coverage",
                ))
            if scope in {"assignments_only", "codebook_and_assignments"}:
                expected.update(
                    ("evidence_support", "assignment", artifact["artifact_id"], code_id)
                    for artifact in packet.get("artifacts", [])
                    for code_id in (
                        packet["scoring_assignment_targets"].get(str(artifact["artifact_id"]), [])
                        if packet.get("scoring_assignment_targets") is not None
                        else (artifact.get("coding_record") or {}).get("final_code_ids", [])
                    )
                )
            actual = [
                (row["dimension"], row["unit"], row.get("artifact_id"), row.get("code_id"))
                for row in normalized
            ]
            if len(actual) != len(set(actual)) or set(actual) != expected:
                raise AgentExecutionError(
                    "Evaluator must score every requested unit exactly once, without extra units."
                )
        return normalized
