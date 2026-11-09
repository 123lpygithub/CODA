from __future__ import annotations

import unittest

from adapters.static_analysis import StaticAnalysisNondeterminismAdapter
from coda.agents.common import serialize_codebook
from coda.contracts import HumanReviewOutput, ValidationOutput
from coda.orchestrator import CODAOrchestrator
from coda.state import ArtifactBatchState, CodeState, CodebookChangeState, RunState


class TestCodebookTransformations(unittest.TestCase):
    def setUp(self) -> None:
        adapter = StaticAnalysisNondeterminismAdapter()
        self.metadata = adapter.load_dataset_metadata()
        self.artifact = next(adapter.iter_artifacts())
        self.batch = ArtifactBatchState(
            batch_id="codebook-change-batch",
            dataset_name=self.metadata.dataset_name,
            batch_index=0,
            split_name="coding_pool",
            artifacts=[self.artifact],
        )
        self.orchestrator = CODAOrchestrator(
            context_agent=lambda _: None,  # type: ignore[arg-type, return-value]
            coder_agents=[
                ("unused-a", lambda _: None),
                ("unused-b", lambda _: None),
            ],  # type: ignore[arg-type, return-value]
            arbitration_agent=lambda _: None,  # type: ignore[arg-type, return-value]
            validation_agent=lambda _: None,  # type: ignore[arg-type, return-value]
            human_review_agent=lambda _: None,  # type: ignore[arg-type, return-value]
        )

    def _run_state(self, codes: list[CodeState]) -> RunState:
        run_state = RunState.initialize(self.metadata, coding_batches=[self.batch])
        run_state.codebook = run_state.codebook.with_codes(codes)
        return run_state

    def _apply(
        self,
        run_state: RunState,
        *,
        final_codes: list[CodeState],
        change: CodebookChangeState,
    ) -> None:
        self.orchestrator._apply_human_review(
            run_state=run_state,
            batch=self.batch,
            human_review_output=HumanReviewOutput(
                artifact_id=self.artifact.artifact_id,
                decision="revise",
                pre_read_memo="Initial reading recorded before Agent suggestions.",
                final_codes=final_codes,
                rationale="The reviewed evidence requires this codebook operation.",
                evidence_summary=["Artifact text provides the reviewed evidence."],
                codebook_changes=[change],
            ),
            validation_output=ValidationOutput(artifact_id=self.artifact.artifact_id),
        )

    def test_add_creates_one_versioned_revision(self) -> None:
        run_state = self._run_state([])
        added = CodeState(
            code_id="code-ordering",
            name="Ordering Failure",
            definition="A failure caused by unstable execution ordering.",
            representative_artifact_ids=[self.artifact.artifact_id],
        )
        self._apply(
            run_state,
            final_codes=[added],
            change=CodebookChangeState(
                change_id="add-ordering",
                action="add",
                round_index=0,
                summary="Add Ordering Failure.",
                rationale="The current codebook has no code for this phenomenon.",
                resulting_code_ids=[added.code_id],
            ),
        )

        self.assertEqual(run_state.codebook.version, 1)
        self.assertEqual(run_state.codebook.codes, [added])
        self.assertEqual([change.action for change in run_state.codebook.revisions], ["add"])

    def test_refine_and_rename_update_the_same_existing_code(self) -> None:
        original = CodeState(
            code_id="code-analysis",
            name="Analysis Problem",
            definition="A broad analysis problem.",
        )
        refined = CodeState(
            code_id=original.code_id,
            name="Analysis Problem",
            definition="A defect in analysis traversal or control-flow modeling.",
            representative_artifact_ids=[self.artifact.artifact_id],
        )
        run_state = self._run_state([original])
        self._apply(
            run_state,
            final_codes=[refined],
            change=CodebookChangeState(
                change_id="refine-analysis",
                action="refine",
                round_index=0,
                summary="Refine Analysis Problem boundary.",
                rationale="The original definition was too broad.",
                target_code_ids=[original.code_id],
            ),
        )
        self.assertEqual(run_state.codebook.version, 1)
        self.assertEqual(run_state.codebook.codes[0].definition, refined.definition)

        renamed = CodeState(
            code_id=original.code_id,
            name="Analysis Traversal Defect",
            definition=refined.definition,
            representative_artifact_ids=[self.artifact.artifact_id],
        )
        self._apply(
            run_state,
            final_codes=[renamed],
            change=CodebookChangeState(
                change_id="rename-analysis",
                action="rename",
                round_index=1,
                summary="Rename Analysis Problem.",
                rationale="The new label is more precise.",
                target_code_ids=[original.code_id],
            ),
        )
        self.assertEqual(run_state.codebook.version, 2)
        self.assertEqual(run_state.codebook.codes[0].name, renamed.name)

    def test_merge_marks_sources_and_preserves_one_active_result(self) -> None:
        first = CodeState("code-iteration", "Unsafe Iteration", "Unsafe mutable traversal.")
        second = CodeState("code-concurrency", "Concurrent Modification", "Mutation during traversal.")
        merged = CodeState(
            "code-mutable-traversal",
            "Unsafe Mutable Traversal",
            "Traversal over data that may be structurally modified.",
            representative_artifact_ids=[self.artifact.artifact_id],
        )
        run_state = self._run_state([first, second])
        self._apply(
            run_state,
            final_codes=[merged],
            change=CodebookChangeState(
                change_id="merge-traversal",
                action="merge",
                round_index=0,
                summary="Merge overlapping traversal codes.",
                rationale="The two old codes express one stable concept.",
                target_code_ids=[first.code_id, second.code_id],
                resulting_code_ids=[merged.code_id],
            ),
        )

        by_id = {code.code_id: code for code in run_state.codebook.codes}
        self.assertEqual(run_state.codebook.version, 1)
        self.assertEqual(by_id[first.code_id].status, "merged")
        self.assertEqual(by_id[second.code_id].status, "merged")
        self.assertEqual(by_id[merged.code_id].status, "active")
        self.assertEqual(by_id[first.code_id].metadata["merged_into"], merged.code_id)

    def test_split_marks_source_and_activates_each_result(self) -> None:
        original = CodeState("code-control-flow", "Control-Flow Problem", "A broad control-flow issue.")
        normal = CodeState(
            "code-normal-flow",
            "Normal-Flow Traversal",
            "Incorrect traversal of normal control-flow edges.",
            representative_artifact_ids=[self.artifact.artifact_id],
        )
        exceptional = CodeState(
            "code-exceptional-flow",
            "Exceptional-Flow Traversal",
            "Incorrect traversal of exceptional control-flow edges.",
            representative_artifact_ids=[self.artifact.artifact_id],
        )
        run_state = self._run_state([original])
        self._apply(
            run_state,
            final_codes=[normal, exceptional],
            change=CodebookChangeState(
                change_id="split-control-flow",
                action="split",
                round_index=0,
                summary="Split normal and exceptional flow issues.",
                rationale="The original code conflated two stable mechanisms.",
                target_code_ids=[original.code_id],
                resulting_code_ids=[normal.code_id, exceptional.code_id],
            ),
        )

        by_id = {code.code_id: code for code in run_state.codebook.codes}
        self.assertEqual(run_state.codebook.version, 1)
        self.assertEqual(by_id[original.code_id].status, "split")
        self.assertEqual(by_id[original.code_id].metadata["split_into"], [normal.code_id, exceptional.code_id])
        self.assertEqual(by_id[normal.code_id].status, "active")
        self.assertEqual(by_id[exceptional.code_id].status, "active")

    def test_add_parent_preserves_children_and_sets_parent_relationship(self) -> None:
        first = CodeState(
            "code-normal-flow",
            "Normal-Flow Traversal",
            "Incorrect traversal of normal control-flow edges.",
        )
        second = CodeState(
            "code-exceptional-flow",
            "Exceptional-Flow Traversal",
            "Incorrect traversal of exceptional control-flow edges.",
        )
        parent = CodeState(
            "code-control-flow-traversal",
            "Control-Flow Traversal",
            "Problems caused by traversing control-flow edges with incorrect semantics.",
            representative_artifact_ids=[self.artifact.artifact_id],
        )
        run_state = self._run_state([first, second])
        self._apply(
            run_state,
            final_codes=[parent],
            change=CodebookChangeState(
                change_id="add-control-flow-parent",
                action="add_parent",
                round_index=0,
                summary="Add a shared control-flow parent.",
                rationale="The two codes are distinct subtypes with a useful shared abstraction.",
                target_code_ids=[first.code_id, second.code_id],
                resulting_code_ids=[parent.code_id],
            ),
        )

        by_id = {code.code_id: code for code in run_state.codebook.codes}
        self.assertEqual(run_state.codebook.version, 1)
        self.assertEqual(by_id[first.code_id].status, "active")
        self.assertEqual(by_id[second.code_id].status, "active")
        self.assertEqual(by_id[first.code_id].parent_code_id, parent.code_id)
        self.assertEqual(by_id[second.code_id].parent_code_id, parent.code_id)
        self.assertEqual(by_id[parent.code_id].status, "active")
        self.assertEqual(run_state.history.codebook_revisions[0].action, "add_parent")
        self.assertIn('"parent_code_id": null', serialize_codebook([parent]))
        self.assertIn('"parent_code_id": "code-control-flow-traversal"', serialize_codebook([by_id[first.code_id]]))

    def test_add_parent_rejects_inactive_child(self) -> None:
        inactive = CodeState(
            "code-old",
            "Old Code",
            "A retired source code.",
            status="merged",
        )
        active = CodeState("code-active", "Active Code", "An active subtype.")
        parent = CodeState("code-parent", "Parent", "A shared parent concept.")
        run_state = self._run_state([inactive, active])
        with self.assertRaisesRegex(ValueError, "active child codes"):
            self.orchestrator._resolve_codebook_changes(
                existing_codes=run_state.codebook.codes,
                human_review_output=HumanReviewOutput(
                    artifact_id=self.artifact.artifact_id,
                    decision="revise",
                    rationale="The parent relationship is deliberately invalid.",
                    final_codes=[parent],
                    codebook_changes=[CodebookChangeState(
                        change_id="invalid-parent",
                        action="add_parent",
                        round_index=0,
                        summary="Invalid parent operation.",
                        rationale="The test must reject an inactive child.",
                        target_code_ids=[inactive.code_id, active.code_id],
                        resulting_code_ids=[parent.code_id],
                    )],
                ),
            )


if __name__ == "__main__":
    unittest.main()
