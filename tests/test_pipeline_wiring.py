from __future__ import annotations

import unittest

from adapters.static_analysis import StaticAnalysisNondeterminismAdapter
from coda.contracts import (
    AnalyticMemo,
    ArbitrationInput,
    ArbitrationOutput,
    CoderAgentInput,
    CoderAgentOutput,
    ContextAgentInput,
    ContextPacket,
    EvidenceItem,
    HumanReviewInput,
    HumanReviewOutput,
    ProvisionalCode,
    ValidationInput,
    ValidationOutput,
    ValidationSignal,
)
from coda.orchestrator import CODAOrchestrator
from coda.state import ArtifactBatchState, CodeState, CodebookChangeState, RunState


class TestPipelineWiring(unittest.TestCase):
    def test_automatic_commits_validated_structural_changes(self) -> None:
        adapter = StaticAnalysisNondeterminismAdapter()
        metadata = adapter.load_dataset_metadata()
        artifact = next(iter(adapter.iter_artifacts()))
        evidence = EvidenceItem(field_name="content", excerpt=artifact.content[:40])
        relationships = {
            "refine": "refine_existing_code", "merge": "merge_existing_codes",
            "split": "split_existing_code", "add_parent": "add_parent_code",
        }
        for action, relationship in relationships.items():
            with self.subTest(action=action):
                batch = ArtifactBatchState("b", metadata.dataset_name, 0, "coding_pool", [artifact])
                state = RunState.initialize(metadata, coding_batches=[batch])
                state.review_policy.setting = "automatic"
                state.codebook = state.codebook.with_codes([
                    CodeState(code_id="c1", name="First", definition="First definition."),
                    CodeState(code_id="c2", name="Second", definition="Second definition."),
                ])
                targets = ["c1", "c2"] if action in {"merge", "add_parent"} else ["c1"]
                names = ["Revised", "Separated"] if action == "split" else ["Revised"]
                def coder(agent_input):
                    return CoderAgentOutput(
                        artifact_id=artifact.artifact_id, coder_id=agent_input.coder_id,
                        provisional_codes=[ProvisionalCode(code_name="Observed", short_definition="Observation.", supporting_evidence=[evidence])],
                    )
                def comparison(_):
                    return ArbitrationOutput(
                        artifact_id=artifact.artifact_id,
                        agreement_summary="Compatible readings.", disagreement_summary="",
                        recommended_codes=[ProvisionalCode(
                            code_name=name, short_definition=f"{name} grounded definition.",
                            supporting_evidence=[evidence], relationship_to_codebook=relationship,
                            proposed_codebook_action=action, proposed_codebook_target_ids=targets,
                            linked_code_ids=targets,
                        ) for name in names],
                        possible_codebook_changes=[CodebookChangeState(
                            change_id="change", action=action, round_index=0,
                            summary="Validated structural change.", rationale="Source supports this definition.",
                            target_code_ids=targets, metadata={"resulting_code_names": names},
                        )],
                    )
                orchestrator = CODAOrchestrator(
                    context_agent=lambda _: ContextPacket(artifact_id=artifact.artifact_id, context_brief="Source.", evidence_items=[evidence]),
                    coder_agents=[("a", coder), ("b", coder)], comparison_agent=comparison,
                    validation_agent=lambda _: ValidationOutput(
                        artifact_id=artifact.artifact_id, review_criteria=["R4"],
                        signals=[ValidationSignal(signal="valid", summary="Supported change.")],
                    ),
                    human_review_agent=lambda _: self.fail("S1 must not request human review"),
                )
                prepared = orchestrator.prepare_one_artifact(state, artifact=artifact)
                self.assertEqual(prepared.evidence_packet.routing_decision.route, "automatic_accept")
                output = orchestrator.automatic_review_if_safe(state, prepared)
                self.assertFalse(output.metadata["human_reviewed"])
                orchestrator.submit_prepared_review(state, prepared_review=prepared, human_review_output=output)
                self.assertEqual(state.codebook.version, 1)
                self.assertEqual(state.history.codebook_revisions[-1].action, action)
                if action == "refine":
                    self.assertEqual(state.codebook.get_code("c1").definition, "Revised grounded definition.")
                if action == "merge":
                    self.assertEqual(state.codebook.get_code("c1").status, "merged")
                if action == "split":
                    self.assertEqual(state.codebook.get_code("c1").status, "split")
                if action == "add_parent":
                    self.assertEqual(state.codebook.get_code("c1").parent_code_id, output.final_codes[0].code_id)

    def test_automatic_preserves_explicit_r_criterion_as_unresolved(self) -> None:
        adapter = StaticAnalysisNondeterminismAdapter()
        metadata = adapter.load_dataset_metadata()
        artifact = list(adapter.iter_artifacts())[0]
        batch = ArtifactBatchState(
            batch_id="batch-automatic-r2",
            dataset_name=metadata.dataset_name,
            batch_index=0,
            split_name="coding_pool",
            artifacts=[artifact],
        )
        run_state = RunState.initialize(metadata, coding_batches=[batch])
        run_state.review_policy.setting = "automatic"
        evidence = EvidenceItem(field_name="content", excerpt=artifact.content[:40])

        def context(_: ContextAgentInput) -> ContextPacket:
            return ContextPacket(
                artifact_id=artifact.artifact_id,
                context_brief="Grounded context.",
                evidence_items=[evidence],
            )

        def coder(agent_input: CoderAgentInput) -> CoderAgentOutput:
            return CoderAgentOutput(
                artifact_id=artifact.artifact_id,
                coder_id=agent_input.coder_id,
                provisional_codes=[
                    ProvisionalCode(
                        code_name="Observed failure",
                        short_definition="A failure supported by the artifact.",
                        supporting_evidence=[evidence],
                    )
                ],
            )

        def comparison(_: ArbitrationInput) -> ArbitrationOutput:
            return ArbitrationOutput(
                artifact_id=artifact.artifact_id,
                agreement_summary="The independent readings are compatible.",
                disagreement_summary="",
                recommended_codes=[
                    ProvisionalCode(
                        code_name="Observed failure",
                        short_definition="A failure supported by the artifact.",
                        supporting_evidence=[evidence],
                        relationship_to_codebook="new_code",
                    )
                ],
            )

        def validation(_: ValidationInput) -> ValidationOutput:
            return ValidationOutput(
                artifact_id=artifact.artifact_id,
                signals=[ValidationSignal(signal="valid", summary="Valid.")],
                review_criteria=["R2"],
                summary="The criterion is explicit even though no extra warning signal was emitted.",
            )

        orchestrator = CODAOrchestrator(
            context_agent=context,
            coder_agents=[("coder-a", coder), ("coder-b", coder)],
            comparison_agent=comparison,
            validation_agent=validation,
            human_review_agent=lambda _: HumanReviewOutput(
                artifact_id=artifact.artifact_id,
                decision="reject",
            ),
        )
        prepared = orchestrator.prepare_one_artifact(
            run_state,
            artifact=artifact,
            batch=batch,
        )

        routing = prepared.evidence_packet.routing_decision
        self.assertIsNotNone(routing)
        self.assertEqual(routing.route, "unresolved")
        self.assertIn("R2", routing.signal_details["review_criteria"])
        self.assertEqual(len(routing.signal_details["review_questions"]), 1)
        self.assertEqual(len(routing.signal_details["review_questions_zh"]), 1)

    def test_human_review_without_criterion_is_r6(self) -> None:
        adapter = StaticAnalysisNondeterminismAdapter()
        metadata = adapter.load_dataset_metadata()
        artifact = list(adapter.iter_artifacts())[0]
        evidence = EvidenceItem(
            field_name="content",
            excerpt=artifact.content[:80],
        )
        batch = ArtifactBatchState(
            batch_id="batch-r6-missing-criterion",
            dataset_name=metadata.dataset_name,
            batch_index=0,
            split_name="coding_pool",
            artifacts=[artifact],
        )
        run_state = RunState.initialize(metadata, coding_batches=[batch])

        def context(_: object) -> ContextPacket:
            return ContextPacket(
                artifact_id=artifact.artifact_id,
                context_brief="The artifact contains an observable failure.",
                evidence_items=[evidence],
            )

        def coder(agent_input: object) -> CoderAgentOutput:
            return CoderAgentOutput(
                artifact_id=artifact.artifact_id,
                coder_id=getattr(agent_input, "coder_id", "coder"),
                provisional_codes=[
                    ProvisionalCode(
                        code_name="Observed failure",
                        short_definition="A failure supported by the artifact.",
                        supporting_evidence=[evidence],
                    )
                ],
            )

        def comparison(_: object) -> ArbitrationOutput:
            return ArbitrationOutput(
                artifact_id=artifact.artifact_id,
                agreement_summary="The independent readings are compatible.",
                disagreement_summary="",
                recommended_codes=[
                    ProvisionalCode(
                        code_name="Observed failure",
                        short_definition="A failure supported by the artifact.",
                        supporting_evidence=[evidence],
                        relationship_to_codebook="new_code",
                    )
                ],
            )

        def validation(_: object) -> ValidationOutput:
            return ValidationOutput(
                artifact_id=artifact.artifact_id,
                signals=[ValidationSignal(signal="valid", summary="Valid.")],
                human_review_required=True,
                review_criteria=[],
                summary="The model explicitly requests review but gives no criterion.",
            )

        orchestrator = CODAOrchestrator(
            context_agent=context,
            coder_agents=[("coder-a", coder), ("coder-b", coder)],
            comparison_agent=comparison,
            validation_agent=validation,
            human_review_agent=lambda _: HumanReviewOutput(
                artifact_id=artifact.artifact_id,
                decision="reject",
            ),
        )
        prepared = orchestrator.prepare_one_artifact(
            run_state,
            artifact=artifact,
            batch=batch,
        )

        routing = prepared.evidence_packet.routing_decision
        self.assertIsNotNone(routing)
        self.assertIn("R6", routing.signal_details["review_criteria"])
        self.assertEqual(len(routing.signal_details["review_questions"]), 1)
        self.assertEqual(len(routing.signal_details["review_questions_zh"]), 1)
        self.assertEqual(routing.route, "human_review")

    def test_unusable_agent_output_becomes_r6_review_packet(self) -> None:
        adapter = StaticAnalysisNondeterminismAdapter()
        metadata = adapter.load_dataset_metadata()
        artifact = list(adapter.iter_artifacts())[0]
        batch = ArtifactBatchState(
            batch_id="batch-r6",
            dataset_name=metadata.dataset_name,
            batch_index=0,
            split_name="coding_pool",
            artifacts=[artifact],
        )
        run_state = RunState.initialize(metadata, coding_batches=[batch])
        run_state.review_policy.setting = "selective"

        def failing(_: object) -> object:
            raise RuntimeError("simulated malformed response")

        orchestrator = CODAOrchestrator(
            context_agent=failing,
            coder_agents=[("coder-a", failing), ("coder-b", failing)],
            comparison_agent=failing,
            validation_agent=failing,
            human_review_agent=failing,
            failure_policy="route_to_r6",
        )
        prepared = orchestrator.prepare_one_artifact(
            run_state,
            artifact=artifact,
            batch=batch,
        )
        routing = prepared.evidence_packet.routing_decision
        self.assertIsNotNone(routing)
        self.assertEqual(routing.route, "human_review")
        self.assertIn("R6", routing.signal_details["review_criteria"])
        self.assertTrue(prepared.validation_output.model_metadata["agent_failure"])
        self.assertEqual(len(routing.signal_details["review_questions"]), len(routing.signal_details["review_criteria"]))
        self.assertEqual(len(routing.signal_details["review_questions_zh"]), len(routing.signal_details["review_criteria"]))

    def test_orchestrator_wires_full_no_model_pipeline(self) -> None:
        adapter = StaticAnalysisNondeterminismAdapter()
        metadata = adapter.load_dataset_metadata()
        artifacts = list(adapter.iter_artifacts())[:2]
        batch = ArtifactBatchState(
            batch_id="batch-0",
            dataset_name=metadata.dataset_name,
            batch_index=0,
            split_name="coding_pool",
            artifacts=artifacts,
        )
        run_state = RunState.initialize(metadata, coding_batches=[batch])

        call_log: list[str] = []

        def context_agent(agent_input: ContextAgentInput) -> ContextPacket:
            call_log.append(f"context:{agent_input.artifact.artifact_id}")
            return ContextPacket(
                artifact_id=agent_input.artifact.artifact_id,
                context_brief="context",
                evidence_items=[
                    EvidenceItem(
                        field_name="issue/commit content",
                        excerpt=agent_input.artifact.raw_fields["issue/commit content"][:80],
                    )
                ],
                source_refs=list(agent_input.artifact.source_refs),
            )

        def make_coder(coder_name: str):
            def coder(agent_input: CoderAgentInput) -> CoderAgentOutput:
                call_log.append(f"{coder_name}:{agent_input.artifact.artifact_id}")
                return CoderAgentOutput(
                    artifact_id=agent_input.artifact.artifact_id,
                    coder_id=agent_input.coder_id,
                    provisional_codes=[
                        ProvisionalCode(
                            code_name="Analysis Logic",
                            short_definition="Root cause in analysis logic.",
                            supporting_evidence=agent_input.context_packet.evidence_items,
                            relationship_to_codebook="new_code",
                            proposed_codebook_action="add",
                        )
                    ],
                )

            return coder

        def arbitration_agent(agent_input: ArbitrationInput) -> ArbitrationOutput:
            call_log.append(f"arbitration:{agent_input.artifact.artifact_id}")
            first_code = agent_input.coder_outputs[0].provisional_codes[0]
            return ArbitrationOutput(
                artifact_id=agent_input.artifact.artifact_id,
                agreement_summary="agreement",
                disagreement_summary="none",
                preserved_alternatives=[first_code],
                possible_codebook_changes=[
                    CodebookChangeState(
                        change_id=f"proposal-a-{agent_input.artifact.artifact_id}",
                        action="add",
                        round_index=0,
                        summary="Add Analysis Logic.",
                        rationale="The current evidence supports the concept.",
                        artifact_ids=[agent_input.artifact.artifact_id],
                        decided_by="comparison_agent",
                        metadata={"resulting_code_names": ["Analysis Logic"]},
                    ),
                    CodebookChangeState(
                        change_id=f"proposal-b-{agent_input.artifact.artifact_id}",
                        action="add",
                        round_index=0,
                        summary="Equivalent duplicate add proposal.",
                        rationale="The same concept was emitted twice.",
                        artifact_ids=[agent_input.artifact.artifact_id],
                        decided_by="comparison_agent",
                        metadata={"resulting_code_names": ["analysis logic"]},
                    ),
                    CodebookChangeState(
                        change_id=f"proposal-no-change-{agent_input.artifact.artifact_id}",
                        action="no_change",
                        round_index=0,
                        summary="No category update.",
                        rationale="No change packet should be shown.",
                        artifact_ids=[agent_input.artifact.artifact_id],
                        decided_by="comparison_agent",
                    ),
                ],
                analytic_memos=[
                    AnalyticMemo(
                        memo_id=f"memo-{agent_input.artifact.artifact_id}",
                        memo_type="comparison",
                        summary="Keep checking whether this broad code has a recurring subtype.",
                        summary_zh="继续检查这个宽泛 code 是否存在反复出现的子类型。",
                        artifact_ids=[agent_input.artifact.artifact_id],
                        status="open",
                    )
                ],
            )

        def validation_agent(agent_input: ValidationInput) -> ValidationOutput:
            call_log.append(f"validation:{agent_input.artifact.artifact_id}")
            return ValidationOutput(
                artifact_id=agent_input.artifact.artifact_id,
                signals=[ValidationSignal(signal="valid", summary="ok")],
                summary="ready",
            )

        def human_review_agent(agent_input: HumanReviewInput) -> HumanReviewOutput:
            call_log.append(f"human:{agent_input.artifact.artifact_id}")
            existing = agent_input.codebook.get_code("code-analysis-logic")
            code = CodeState(
                code_id="code-analysis-logic",
                name="Analysis Logic",
                definition="Human-approved code.",
                representative_artifact_ids=(
                    [*existing.representative_artifact_ids, agent_input.artifact.artifact_id]
                    if existing is not None
                    else [agent_input.artifact.artifact_id]
                ),
            )
            changes = [] if existing is not None else [
                CodebookChangeState(
                    change_id=f"chg-{agent_input.artifact.artifact_id}",
                    action="add",
                    round_index=0,
                    summary="Add Analysis Logic.",
                    rationale="The first reviewed artifact establishes this new concept.",
                    resulting_code_ids=[code.code_id],
                    artifact_ids=[agent_input.artifact.artifact_id],
                )
            ]
            return HumanReviewOutput(
                artifact_id=agent_input.artifact.artifact_id,
                decision="accept",
                final_codes=[code],
                rationale="accept recommendation",
                evidence_summary=["grounded evidence"],
                codebook_changes=changes,
            )

        orchestrator = CODAOrchestrator(
            context_agent=context_agent,
            coder_agents=[
                ("coder-a", make_coder("coder-a")),
                ("coder-b", make_coder("coder-b")),
            ],
            arbitration_agent=arbitration_agent,
            validation_agent=validation_agent,
            human_review_agent=human_review_agent,
        )

        batch_result = orchestrator.run_current_batch(run_state)

        self.assertEqual(batch_result.batch_id, "batch-0")
        self.assertEqual(len(batch_result.artifact_results), 2)
        self.assertEqual(run_state.status, "completed")
        self.assertEqual(run_state.current_batch_index, 1)
        self.assertEqual(len(run_state.history.coding_records), 2)
        self.assertEqual(len(run_state.history.codebook_revisions), 1)
        self.assertEqual(len(run_state.history.analytic_memos), 2)
        self.assertEqual(run_state.history.analytic_memos[0]["memo_type"], "comparison")
        self.assertEqual(run_state.codebook.version, 1)
        self.assertEqual(len(run_state.codebook.codes), 1)
        self.assertEqual(run_state.codebook.codes[0].name, "Analysis Logic")
        self.assertEqual(
            batch_result.artifact_results[0].evidence_packet.candidate_definitions,
            ["Root cause in analysis logic.", "Root cause in analysis logic."],
        )
        self.assertEqual(
            batch_result.artifact_results[0].human_review_output.decision,
            "accept",
        )
        self.assertEqual(
            len(batch_result.artifact_results[0].evidence_packet.codebook_change_packets),
            1,
        )
        self.assertEqual(
            batch_result.artifact_results[0]
            .evidence_packet.codebook_change_packets[0]
            .proposed_codes[0]
            .name,
            "Analysis Logic",
        )
        self.assertEqual(
            call_log,
            [
                f"context:{artifacts[0].artifact_id}",
                f"coder-a:{artifacts[0].artifact_id}",
                f"coder-b:{artifacts[0].artifact_id}",
                f"arbitration:{artifacts[0].artifact_id}",
                f"validation:{artifacts[0].artifact_id}",
                f"human:{artifacts[0].artifact_id}",
                f"validation:{artifacts[0].artifact_id}",
                f"context:{artifacts[1].artifact_id}",
                f"coder-a:{artifacts[1].artifact_id}",
                f"coder-b:{artifacts[1].artifact_id}",
                f"arbitration:{artifacts[1].artifact_id}",
                f"validation:{artifacts[1].artifact_id}",
                f"human:{artifacts[1].artifact_id}",
            ],
        )

    def test_representative_artifact_updates_do_not_bump_codebook_version(self) -> None:
        adapter = StaticAnalysisNondeterminismAdapter()
        metadata = adapter.load_dataset_metadata()
        artifacts = list(adapter.iter_artifacts())[:2]
        batch = ArtifactBatchState(
            batch_id="batch-1",
            dataset_name=metadata.dataset_name,
            batch_index=0,
            split_name="coding_pool",
            artifacts=artifacts,
        )
        run_state = RunState.initialize(metadata, coding_batches=[batch])
        existing_code = CodeState(
            code_id="code-analysis-logic",
            name="Analysis Logic",
            definition="Existing stable code.",
            representative_artifact_ids=["artifact-old"],
        )
        run_state.codebook = run_state.codebook.next_version(codes=[existing_code])

        def context_agent(agent_input: ContextAgentInput) -> ContextPacket:
            return ContextPacket(
                artifact_id=agent_input.artifact.artifact_id,
                context_brief="context",
                evidence_items=[
                    EvidenceItem(
                        field_name="issue/commit content",
                        excerpt=agent_input.artifact.raw_fields["issue/commit content"][:80],
                    )
                ],
                source_refs=list(agent_input.artifact.source_refs),
            )

        def coder(agent_input: CoderAgentInput) -> CoderAgentOutput:
            return CoderAgentOutput(
                artifact_id=agent_input.artifact.artifact_id,
                coder_id=agent_input.coder_id,
                provisional_codes=[
                    ProvisionalCode(
                        code_name="Analysis Logic",
                        short_definition="Root cause in analysis logic.",
                        supporting_evidence=agent_input.context_packet.evidence_items,
                        relationship_to_codebook="reuse_existing_code",
                        linked_code_ids=["code-analysis-logic"],
                        proposed_codebook_action="no_change",
                        proposed_codebook_target_ids=["code-analysis-logic"],
                    )
                ],
            )

        def arbitration_agent(agent_input: ArbitrationInput) -> ArbitrationOutput:
            return ArbitrationOutput(
                artifact_id=agent_input.artifact.artifact_id,
                agreement_summary="agreement",
                disagreement_summary="none",
                recommended_codes=[agent_input.coder_outputs[0].provisional_codes[0]],
            )

        def validation_agent(agent_input: ValidationInput) -> ValidationOutput:
            return ValidationOutput(
                artifact_id=agent_input.artifact.artifact_id,
                signals=[ValidationSignal(signal="valid", summary="ok")],
                summary="ready",
            )

        def human_review_agent(agent_input: HumanReviewInput) -> HumanReviewOutput:
            updated_code = CodeState(
                code_id="code-analysis-logic",
                name="Analysis Logic",
                definition="Existing stable code.",
                representative_artifact_ids=[
                    "artifact-old",
                    agent_input.artifact.artifact_id,
                ],
            )
            return HumanReviewOutput(
                artifact_id=agent_input.artifact.artifact_id,
                decision="accept",
                final_codes=[updated_code],
                rationale="reuse existing code",
                evidence_summary=["grounded evidence"],
                codebook_changes=[],
            )

        orchestrator = CODAOrchestrator(
            context_agent=context_agent,
            coder_agents=[
                ("coder-a", coder),
                ("coder-b", coder),
            ],
            arbitration_agent=arbitration_agent,
            validation_agent=validation_agent,
            human_review_agent=human_review_agent,
        )

        orchestrator.run_current_batch(run_state)

        self.assertEqual(run_state.codebook.version, 1)
        self.assertEqual(len(run_state.history.codebook_revisions), 0)
        self.assertEqual(
            run_state.codebook.codes[0].representative_artifact_ids,
            ["artifact-old", artifacts[0].artifact_id, artifacts[1].artifact_id],
        )


if __name__ == "__main__":
    unittest.main()
