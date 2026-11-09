from __future__ import annotations

import unittest

from adapters.base import ArtifactRecord
from coda.agents import ArbitrationLLMAgent, ValidationLLMAgent
from coda.agents.base import AgentExecutionError
from coda.contracts import (
    ArbitrationInput,
    ArbitrationOutput,
    CoderAgentOutput,
    ContextPacket,
    DisagreementRecord,
    EvidenceItem,
    ProvisionalCode,
    ValidationInput,
)
from coda.llm import LLMModelConfig, LLMResponse
from coda.state import (
    CodeState,
    CodebookChangeState,
    CodebookState,
    CodingRecordState,
    HistoryState,
    ResearchQuestionState,
)


class FakeArbitrationBackend:
    def generate(self, *, messages, config):
        del messages
        del config
        return LLMResponse(
            model="fake-arbitration-model",
            text="""
            {
              "agreement_summary": "Both coders agree the artifact reflects an analysis-side fault.",
              "disagreement_summary": "They disagree on whether the current codebook is specific enough.",
              "recommended_codes": [
                {
                  "code_name": "Analysis Traversal Instability",
                  "short_definition": "Mutable traversal and exceptional-path handling destabilize the analysis.",
                  "supporting_evidence_refs": ["E1", "E2"],
                  "relationship_to_codebook": "reuse_existing_code",
                  "linked_code_ids": ["code-existing"],
                  "alternative_interpretation": "Could also be carved out as a narrower exceptional-path code.",
                  "uncertainty_note": "Boundary with exceptional-path modeling is still somewhat fuzzy.",
                  "proposed_codebook_action": "no_change",
                  "proposed_codebook_target_ids": ["code-existing"]
                }
              ],
              "preserved_alternatives": [
                {
                  "code_name": "Exceptional Path Control",
                  "short_definition": "Exceptional-path modeling itself may deserve a separate code.",
                  "supporting_evidence_refs": ["E1"],
                  "relationship_to_codebook": "new_code",
                  "linked_code_ids": [],
                  "alternative_interpretation": "This may still be a subtype of the broader instability code.",
                  "uncertainty_note": "Needs more examples before stabilizing.",
                  "proposed_codebook_action": "add",
                  "proposed_codebook_target_ids": []
                }
              ],
              "disagreements": [
                {
                  "disagreement_type": "semantic_disagreement",
                  "summary": "One coder prefers a broad existing category while the other proposes a narrower new one.",
                  "coder_ids": ["coder-a", "coder-b"],
                  "affected_code_names": ["Analysis Traversal Instability", "Exceptional Path Control"],
                  "evidence_refs": ["E1"]
                }
              ],
              "relevant_historical_artifact_ids": ["artifact-h1", "artifact-missing"],
              "possible_codebook_changes": [
                {
                  "action": "add",
                  "summary": "Track exceptional-path issues separately if similar cases accumulate.",
                  "rationale": "The current artifact exposes a possibly recurring subtype.",
                  "target_code_ids": [],
                  "resulting_code_names": ["Exceptional Path Control"],
                  "affected_historical_artifact_ids": ["artifact-h1"]
                }
              ],
              "comparison_findings": [
                {
                  "comparison_type": "case_to_case",
                  "finding": "same_phenomenon",
                  "summary": "The current case shares the traversal instability pattern with the reviewed case.",
                  "summary_zh": "当前案例与已审核案例共享遍历不稳定模式。",
                  "compared_artifact_ids": ["artifact-h1"],
                  "compared_code_ids": [],
                  "evidence_refs": ["E1"],
                  "implication": "Retain the broad phenomenon while checking the exceptional-path boundary.",
                  "implication_zh": "保留宽泛现象，同时核对异常路径边界。"
                },
                {
                  "comparison_type": "case_to_code",
                  "finding": "partial_overlap",
                  "summary": "The current evidence fits the existing broad code but may expose a subtype.",
                  "summary_zh": "当前证据符合已有宽泛 code，但可能暴露子类型。",
                  "compared_artifact_ids": [],
                  "compared_code_ids": ["code-existing"],
                  "evidence_refs": ["E1", "E2"],
                  "implication": "Do not merge or split until the boundary is supported by more cases.",
                  "implication_zh": "在更多案例支持边界前，不要合并或拆分。"
                }
              ],
              "analytic_memos": [
                {
                  "memo_type": "category_boundary",
                  "summary": "Determine whether exceptional-path handling recurs as a distinct subtype.",
                  "summary_zh": "确定异常路径处理是否反复作为独立子类型出现。",
                  "artifact_ids": ["artifact-1", "artifact-h1"],
                  "code_ids": ["code-existing"],
                  "status": "open"
                }
              ]
            }
            """,
        )


class FakeInvalidArbitrationBackend:
    def generate(self, *, messages, config):
        del messages
        del config
        return LLMResponse(
            model="fake-arbitration-model",
            text="""
            {
              "agreement_summary": "summary",
              "disagreement_summary": "summary",
              "recommended_codes": [
                {
                  "code_name": "Bad Evidence Ref",
                  "short_definition": "Invalid evidence id should fail.",
                  "supporting_evidence_refs": ["E9"],
                  "relationship_to_codebook": "new_code",
                  "linked_code_ids": [],
                  "alternative_interpretation": "",
                  "uncertainty_note": "",
                  "proposed_codebook_action": "add",
                  "proposed_codebook_target_ids": []
                }
              ],
              "preserved_alternatives": [],
              "disagreements": [],
              "relevant_historical_artifact_ids": [],
              "possible_codebook_changes": []
            }
            """,
        )


class FakeUnknownCodeArbitrationBackend(FakeArbitrationBackend):
    def generate(self, *, messages, config):
        response = super().generate(messages=messages, config=config)
        return LLMResponse(
            model=response.model,
            text=response.text.replace("code-existing", "code-does-not-exist"),
        )


class FakeValidationBackend:
    def __init__(self) -> None:
        self.last_user_prompt = ""

    def generate(self, *, messages, config):
        del config
        self.last_user_prompt = messages[-1].content
        return LLMResponse(
            model="fake-validation-model",
            text="""
            {
              "signals": [
                {
                  "signal": "boundary_unclear",
                  "summary": "The recommended and alternative codes still have a fuzzy boundary.",
                  "related_code_names": ["Analysis Traversal Instability", "Exceptional Path Control"],
                  "evidence_refs": ["E1"]
                },
                {
                  "signal": "human_review_required",
                  "summary": "The case is interpretable, but codebook revision should remain a human decision.",
                  "related_code_names": ["Exceptional Path Control"],
                  "evidence_refs": []
                }
              ],
              "human_review_required": true,
              "review_criteria": ["R3"],
              "review_questions": ["Where should these category boundaries be drawn?"],
              "review_questions_zh": ["这些类别的边界应如何划分？"],
              "confidence_level": "medium",
              "confidence_rationale": "The evidence is supported but the category boundary remains unclear.",
              "confidence_factors": {
                "evidence_support": "strong",
                "coder_agreement": "mixed",
                "codebook_fit": "moderate",
                "interpretive_ambiguity": "high"
              },
              "summary": "The coding result is plausible but should be reviewed before changing the codebook.",
              "notes": [
                "The artifact is suitable for human review.",
                "More examples would help determine whether the alternative should become a new stable code."
              ]
            }
            """,
        )


def _build_fixture():
    artifact = ArtifactRecord(
        artifact_id="artifact-1",
        content=(
            "Issue/Commit Content:\n"
            "do not follow exceptional paths and fix concurrent modification exception by using exceptional graph\n"
            "Iterator<Unit> unitIt = body.getUnits().snapshotIterator();\n"
        ),
        raw_fields={
            "issue/commit content": (
                "do not follow exceptional paths and fix concurrent modification exception by using exceptional graph\n"
                "Iterator<Unit> unitIt = body.getUnits().snapshotIterator();\n"
            )
        },
        source_refs=[],
    )
    research_question = ResearchQuestionState(
        dataset_name="demo",
        question_text="What root-cause categories explain the issue?",
        analysis_scope="Static analysis bug reports and patches.",
        use_case="Build an evolving qualitative codebook.",
        artifact_unit="One issue/commit record",
    )
    context_packet = ContextPacket(
        artifact_id=artifact.artifact_id,
        context_brief="The artifact points to exceptional-path handling and concurrent modification during traversal.",
        evidence_items=[
            EvidenceItem(
                field_name="issue/commit content",
                excerpt="do not follow exceptional paths and fix concurrent modification exception by using exceptional graph",
                rationale="The summary sentence states the main failure mode.",
            ),
            EvidenceItem(
                field_name="issue/commit content",
                excerpt="Iterator<Unit> unitIt = body.getUnits().snapshotIterator();",
                rationale="The patch line shows the concrete traversal fix.",
            ),
        ],
    )
    codebook = CodebookState(
        dataset_name="demo",
        version=1,
        codes=[
            CodeState(
                code_id="code-existing",
                name="Analysis Traversal Instability",
                definition="Existing broad code for unstable traversal logic.",
            )
        ],
    )
    history = HistoryState(
        coding_records=[
            CodingRecordState(
                record_id="record-h1",
                artifact_id="artifact-h1",
                dataset_name="demo",
                batch_index=0,
                codebook_version=0,
                decision="accept",
                final_code_ids=["code-existing"],
                final_code_names=["Analysis Traversal Instability"],
                rationale="Earlier reviewed case with similar traversal failure.",
                evidence_summary=["Historical evidence"],
            )
        ]
    )
    coder_outputs = [
        CoderAgentOutput(
            artifact_id=artifact.artifact_id,
            coder_id="coder-a",
            provisional_codes=[
                ProvisionalCode(
                    code_name="Analysis Traversal Instability",
                    short_definition="The artifact fits the existing traversal-instability category.",
                    supporting_evidence=context_packet.evidence_items,
                    relationship_to_codebook="reuse_existing_code",
                    linked_code_ids=["code-existing"],
                    alternative_interpretation="Could be split into a narrower exceptional-path subtype.",
                    uncertainty_note="The evidence mixes two technical signals.",
                    proposed_codebook_action="no_change",
                    proposed_codebook_target_ids=["code-existing"],
                )
            ],
        ),
        CoderAgentOutput(
            artifact_id=artifact.artifact_id,
            coder_id="coder-b",
            provisional_codes=[
                ProvisionalCode(
                    code_name="Exceptional Path Control",
                    short_definition="The artifact may justify a new code focused on exceptional-path handling.",
                    supporting_evidence=[context_packet.evidence_items[0]],
                    relationship_to_codebook="new_code",
                    linked_code_ids=[],
                    alternative_interpretation="It may still belong under the broader traversal-instability code.",
                    uncertainty_note="The subtype boundary needs more examples.",
                    proposed_codebook_action="add",
                    proposed_codebook_target_ids=[],
                )
            ],
        ),
    ]
    return artifact, research_question, context_packet, codebook, history, coder_outputs


class TestArbitrationAndValidationAgents(unittest.TestCase):
    def test_new_code_cannot_duplicate_an_active_bilingual_label(self) -> None:
        existing = CodeState(
            code_id="existing-recurrence-code",
            name="Missing recurrence base-state initialization",
            definition="A recurrence starts without its required seed.",
            metadata={"name_zh": "递推基础状态初始化缺失"},
        )
        duplicate = ProvisionalCode(
            code_name="Recurrence seed omission",
            code_name_zh="递推基础状态初始化缺失",
            short_definition="A recurrence starts without its required seed.",
            relationship_to_codebook="new_code",
            proposed_codebook_action="add",
        )

        with self.assertRaisesRegex(
            AgentExecutionError,
            "duplicates an active English or Chinese label",
        ):
            ArbitrationLLMAgent._validate_new_code_label_collisions(
                active_codes=[existing],
                candidates=[duplicate],
            )

    def test_codebook_change_requires_matching_editable_candidate_definition(self) -> None:
        change = CodebookChangeState(
            change_id="proposal-parent",
            action="add_parent",
            round_index=0,
            summary="Add a shared parent category.",
            rationale="Two recurring child codes may share a useful abstraction.",
            target_code_ids=["code-a", "code-b"],
            decided_by="comparison_agent",
            metadata={"resulting_code_names": ["Different Parent"]},
        )
        unrelated_candidate = ProvisionalCode(
            code_name="Different Parent",
            short_definition="A candidate attached to a different pair of children.",
            relationship_to_codebook="add_parent_code",
            linked_code_ids=["code-a", "code-c"],
            proposed_codebook_action="add_parent",
            proposed_codebook_target_ids=["code-a", "code-c"],
        )

        with self.assertRaisesRegex(
            AgentExecutionError,
            "requires exactly one matching recommended or preserved candidate definition",
        ):
            ArbitrationLLMAgent._validate_change_recommendation_consistency(
                changes=[change],
                candidates=[unrelated_candidate],
            )

    def test_add_parent_requires_at_least_two_distinct_children(self) -> None:
        with self.assertRaisesRegex(AgentExecutionError, "at least 2 active target"):
            ArbitrationLLMAgent._validate_action_targets(
                "add_parent",
                ["only-child"],
            )
        with self.assertRaisesRegex(AgentExecutionError, "at least 2 active linked"):
            ArbitrationLLMAgent._validate_relationship_targets(
                relationship="add_parent_code",
                linked_code_ids=["only-child"],
                action="add_parent",
                target_code_ids=["only-child", "second-child"],
            )

    def test_arbitration_agent_parses_outputs_and_maps_references(self) -> None:
        (
            artifact,
            research_question,
            context_packet,
            codebook,
            history,
            coder_outputs,
        ) = _build_fixture()
        agent = ArbitrationLLMAgent(
            model_config=LLMModelConfig(model="fake-arbitration", provider="custom"),
            backend=FakeArbitrationBackend(),
        )

        output = agent(
            ArbitrationInput(
                artifact=artifact,
                research_question=research_question,
                context_packet=context_packet,
                coder_outputs=coder_outputs,
                codebook=codebook,
                history=history,
            )
        )

        self.assertEqual(output.artifact_id, artifact.artifact_id)
        self.assertEqual(output.recommended_codes[0].code_name, "Analysis Traversal Instability")
        self.assertEqual(
            output.recommended_codes[0].supporting_evidence[0].excerpt,
            context_packet.evidence_items[0].excerpt,
        )
        self.assertEqual(
            output.preserved_alternatives[0].relationship_to_codebook,
            "new_code",
        )
        self.assertEqual(
            output.disagreements[0].disagreement_type,
            "semantic_disagreement",
        )
        self.assertEqual(
            output.relevant_historical_examples[0].artifact_id,
            "artifact-h1",
        )
        self.assertEqual(
            output.possible_codebook_changes[0].action,
            "add",
        )
        self.assertEqual(
            output.possible_codebook_changes[0].metadata["resulting_code_names"],
            ["Exceptional Path Control"],
        )
        self.assertEqual(len(output.comparison_findings), 2)
        self.assertEqual(output.comparison_findings[0].comparison_type, "case_to_case")
        self.assertEqual(output.analytic_memos[0].status, "open")
        self.assertEqual(
            output.possible_codebook_changes[0].metadata["affected_historical_artifact_ids"],
            ["artifact-h1"],
        )

    def test_arbitration_agent_rejects_unknown_evidence_refs(self) -> None:
        (
            artifact,
            research_question,
            context_packet,
            codebook,
            history,
            coder_outputs,
        ) = _build_fixture()
        agent = ArbitrationLLMAgent(
            model_config=LLMModelConfig(model="fake-arbitration", provider="custom"),
            backend=FakeInvalidArbitrationBackend(),
        )

        with self.assertRaises(AgentExecutionError):
            agent(
                ArbitrationInput(
                    artifact=artifact,
                    research_question=research_question,
                    context_packet=context_packet,
                    coder_outputs=coder_outputs,
                    codebook=codebook,
                    history=history,
                )
            )

    def test_comparison_agent_rejects_unknown_active_code_references(self) -> None:
        (
            artifact,
            research_question,
            context_packet,
            codebook,
            history,
            coder_outputs,
        ) = _build_fixture()
        agent = ArbitrationLLMAgent(
            model_config=LLMModelConfig(model="fake-arbitration", provider="custom"),
            backend=FakeUnknownCodeArbitrationBackend(),
        )

        with self.assertRaisesRegex(AgentExecutionError, "Unknown active code ids"):
            agent(
                ArbitrationInput(
                    artifact=artifact,
                    research_question=research_question,
                    context_packet=context_packet,
                    coder_outputs=coder_outputs,
                    codebook=codebook,
                    history=history,
                )
            )

    def test_validation_agent_parses_outputs_and_uses_preliminary_signals(self) -> None:
        (
            artifact,
            research_question,
            context_packet,
            codebook,
            history,
            coder_outputs,
        ) = _build_fixture()
        arbitration_output = ArbitrationOutput(
            artifact_id=artifact.artifact_id,
            agreement_summary="Both coders agree this is an analysis-side fault.",
            disagreement_summary="The main disagreement is whether a new subtype is needed.",
            recommended_codes=[
                coder_outputs[0].provisional_codes[0],
                ProvisionalCode(
                    code_name="Analysis Traversal Instability",
                    short_definition="Duplicate-name new code to trigger overlap signaling.",
                    supporting_evidence=[context_packet.evidence_items[0]],
                    relationship_to_codebook="new_code",
                    linked_code_ids=[],
                    alternative_interpretation="Could just reuse the existing code.",
                    uncertainty_note="Boundary remains unclear.",
                    proposed_codebook_action="add",
                    proposed_codebook_target_ids=[],
                ),
            ],
            preserved_alternatives=[coder_outputs[1].provisional_codes[0]],
            disagreements=[
                DisagreementRecord(
                    disagreement_type="semantic_disagreement",
                    summary="Subtype versus broad category.",
                    coder_ids=["coder-a", "coder-b"],
                    affected_code_names=[
                        "Analysis Traversal Instability",
                        "Exceptional Path Control",
                    ],
                    evidence_items=[context_packet.evidence_items[0]],
                )
            ],
        )
        backend = FakeValidationBackend()
        agent = ValidationLLMAgent(
            model_config=LLMModelConfig(model="fake-validation", provider="custom"),
            backend=backend,
        )

        output = agent(
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

        self.assertEqual(output.artifact_id, artifact.artifact_id)
        self.assertTrue(output.human_review_required)
        self.assertEqual(output.signals[0].signal, "boundary_unclear")
        self.assertEqual(output.signals[0].issue_scope, "assignment")
        self.assertEqual(
            output.signals[0].evidence_items[0].excerpt,
            context_packet.evidence_items[0].excerpt,
        )
        self.assertIn('"signal": "category_overlap"', backend.last_user_prompt)
        self.assertIn('"signal": "boundary_unclear"', backend.last_user_prompt)
        self.assertEqual(
            output.summary,
            "The coding result is plausible but should be reviewed before changing the codebook.",
        )
        self.assertEqual(
            output.confidence_factors,
            {
                "evidence_support": "high",
                "coder_agreement": "medium",
                "codebook_fit": "medium",
                "interpretive_ambiguity": "high",
            },
        )


if __name__ == "__main__":
    unittest.main()
