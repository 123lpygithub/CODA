from __future__ import annotations

import json
import tempfile
import threading
import unittest
from pathlib import Path

from adapters.base import ArtifactRecord
from adapters.static_analysis import StaticAnalysisNondeterminismAdapter
from coda.bootstrap import (
    BootstrapConfig,
    BootstrapResult,
    EvidenceFirstBootstrap,
    bootstrap_sample_size,
    select_bootstrap_artifacts,
)
from coda.contracts import (
    CoderAgentOutput,
    ContextPacket,
    EvidenceItem,
    InductionAgentOutput,
    ProvisionalCode,
    ValidationOutput,
    ValidationSignal,
)
from coda.full_runner import build_single_batch_run_state
from coda.llm import LLMMessage, LLMModelConfig, LLMResponse
from coda.state import CodeState, CodebookState
from coda.web.runtime import (
    CodaWebService,
    build_default_web_bootstrap,
    build_default_web_orchestrator,
)
from tests.test_web_runtime import _build_test_orchestrator


class _ScriptedBackend:
    def __init__(self) -> None:
        self.assignment_requests: list[dict] = []

    def generate(self, *, messages: list[LLMMessage], config: LLMModelConfig) -> LLMResponse:
        prompt = messages[-1].content
        request = json.loads(prompt)
        if "assignments" in request["required_json"]:
            self.assignment_requests.append(request)
            payload = {
                "assignments": [
                    {
                        "artifact_id": card["artifact_id"],
                        "code_ids": ["analysis-failure"],
                        "evidence_summary": ["The artifact's evidence supports the provisional code."],
                    }
                    for card in request["evidence_cards"]
                ]
            }
        else:
            payload = {"warnings": ["Definitions remain provisional until human review."]}
        return LLMResponse(
            model="test",
            text=json.dumps(payload),
            finish_reason="stop",
            usage={"prompt_tokens": 40, "completion_tokens": 10, "total_tokens": 50},
            elapsed_seconds=0.25,
            estimated_cost_usd=0.001,
        )


def _initial_coder(model: str, call_log: list[tuple[str, int, int]] | None = None):
    def coder(agent_input) -> CoderAgentOutput:
        if call_log is not None:
            call_log.append(
                (
                    agent_input.coder_id,
                    0,
                    0,
                )
            )
        return CoderAgentOutput(
            artifact_id=agent_input.artifact.artifact_id,
            coder_id=agent_input.coder_id,
            provisional_codes=[
                ProvisionalCode(
                    code_name="analysis failure",
                    short_definition="Visible failure in analysis logic.",
                    supporting_evidence=[agent_input.context_packet.evidence_items[0]],
                    relationship_to_codebook="uncertain",
                    proposed_codebook_action="no_change",
                )
            ],
            confidence_level="medium",
            model_metadata={"model": model},
        )

    return coder


def _induction(agent_input) -> InductionAgentOutput:
    artifact_id = agent_input.cases[0].artifact_id
    return InductionAgentOutput(
        codes=[
            CodeState(
                code_id="analysis-failure",
                name="Analysis failure",
                definition="An implementation failure in analysis logic.",
                inclusion_criteria=["The artifact describes an analysis failure."],
                exclusion_criteria=["Pure feature requests."],
                representative_artifact_ids=[artifact_id],
                metadata={
                    "origin": "llm_initial_induction",
                    "human_reviewed": False,
                    "evidence_summary": "Independent codes identify the same visible failure.",
                },
            )
        ],
        change_log=[{"action": "add", "summary": "Induce the provisional code."}],
        analytic_memos=[
            {
                "summary": "Both independent readings identify an analysis failure.",
                "artifact_ids": [artifact_id],
                "source_code_names": ["analysis failure"],
            }
        ],
        model_metadata={"model": "test-induction"},
    )


def _context(agent_input) -> ContextPacket:
    return ContextPacket(
        artifact_id=agent_input.artifact.artifact_id,
        context_brief="Visible implementation evidence.",
        evidence_items=[
            EvidenceItem(
                field_name="content",
                excerpt=agent_input.artifact.content[:80],
                rationale="Grounded symptom.",
            )
        ],
    )


class TestEvidenceFirstBootstrap(unittest.TestCase):
    def test_default_sample_size_is_proportional_for_small_runs(self) -> None:
        self.assertEqual(bootstrap_sample_size(20), 4)
        self.assertEqual(bootstrap_sample_size(2), 1)
        self.assertEqual(bootstrap_sample_size(1), 0)

    def test_default_initial_coders_use_the_configured_distinct_models(self) -> None:
        bootstrap = build_default_web_bootstrap(build_default_web_orchestrator())

        self.assertEqual(
            bootstrap.initial_coder_models,
            {
                "initial-coder-a": "gpt-6.1-sol",
                "initial-coder-b": "gpt-5.6-sol",
            },
        )

    def test_default_iterative_coders_use_the_configured_distinct_models(self) -> None:
        orchestrator = build_default_web_orchestrator()
        models = {
            coder_id: coder.model_config.model
            for coder_id, coder in orchestrator._coder_agents
        }

        self.assertEqual(
            models,
            {"coder-a": "gpt-6.1-sol", "coder-b": "gpt-5.6-sol"},
        )

    def test_new_run_manifest_records_the_current_coder_models(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            service = CodaWebService(runs_root=Path(temp_dir))
            summary = service.create_run(
                dataset_name="static_analysis_nondeterminism",
                artifact_limit=2,
                review_mode="automatic",
            )
            manifest = json.loads(
                Path(str(summary["run_manifest"])).read_text(encoding="utf-8")
            )

        self.assertEqual(manifest["models"]["coder_a"]["model"], "gpt-6.1-sol")
        self.assertEqual(manifest["models"]["coder_b"]["model"], "gpt-5.6-sol")

    def test_leaf_most_assignment_removes_selected_ancestors(self) -> None:
        codes = [
            CodeState("root", "Root", "Organizational root."),
            CodeState("child", "Child", "Specific child.", parent_code_id="root"),
            CodeState("leaf", "Leaf", "Most specific code.", parent_code_id="child"),
            CodeState("peer", "Peer", "Independent code."),
        ]

        normalized = EvidenceFirstBootstrap._leaf_most_code_ids(
            ["root", "child", "leaf", "peer", "leaf"],
            codes,
        )

        self.assertEqual(normalized, ["leaf", "peer"])

    def _run_validation_correction(self, issue_scope: str):
        adapter = StaticAnalysisNondeterminismAdapter()
        artifacts = list(adapter.iter_artifacts())[:3]
        run_state = build_single_batch_run_state(
            adapter.load_dataset_metadata(), artifacts, batch_id=f"scope-{issue_scope}"
        )
        induction_calls: list[list[dict[str, object]]] = []
        validation_calls: dict[str, int] = {}

        def recording_induction(agent_input) -> InductionAgentOutput:
            induction_calls.append(list(agent_input.validation_feedback))
            return _induction(agent_input)

        def scoped_validation(agent_input) -> ValidationOutput:
            artifact_id = agent_input.artifact.artifact_id
            validation_calls[artifact_id] = validation_calls.get(artifact_id, 0) + 1
            if validation_calls[artifact_id] == 1:
                return ValidationOutput(
                    artifact_id=artifact_id,
                    signals=[
                        ValidationSignal(
                            signal=(
                                "use_case_mismatch"
                                if issue_scope == "codebook"
                                else "category_overlap"
                            ),
                            issue_scope=issue_scope,  # type: ignore[arg-type]
                            summary=f"{issue_scope} correction required",
                        )
                    ],
                    summary="Correction required.",
                )
            return ValidationOutput(
                artifact_id=artifact_id,
                signals=[ValidationSignal(signal="valid", summary="Valid.")],
                summary="Valid after correction.",
                confidence_level="high",
            )

        class CountingBackend(_ScriptedBackend):
            def __init__(self) -> None:
                super().__init__()
                self.assignment_calls = 0

            def generate(self, *, messages, config):
                request = json.loads(messages[-1].content)
                if "assignments" in request["required_json"]:
                    self.assignment_calls += 1
                return super().generate(messages=messages, config=config)

        backend = CountingBackend()
        bootstrap = EvidenceFirstBootstrap(
            model_config=LLMModelConfig(model="test", json_mode=False),
            backend=backend,
            context_agent=_context,
            initial_coder_agents=[
                ("initial-a", _initial_coder("model-a")),
                ("initial-b", _initial_coder("model-b")),
            ],
            induction_agent=recording_induction,
            validation_agent=scoped_validation,
            config=BootstrapConfig(
                fraction=0.67,
                minimum_size=2,
                maximum_size=2,
                batch_size=10,
            ),
        )

        return bootstrap.run(run_state, artifacts), induction_calls, backend.assignment_calls

    def test_assignment_scoped_validation_reassigns_without_reinduction(self) -> None:
        result, induction_calls, assignment_calls = self._run_validation_correction(
            "assignment"
        )

        self.assertEqual(result.status, "completed")
        self.assertEqual(len(induction_calls), 1)
        self.assertEqual(assignment_calls, 2)
        self.assertTrue(any("assignment correction" in item for item in result.audit_warnings))

    def test_codebook_scoped_validation_triggers_reinduction(self) -> None:
        result, induction_calls, assignment_calls = self._run_validation_correction(
            "codebook"
        )

        self.assertEqual(result.status, "completed")
        self.assertEqual(len(induction_calls), 2)
        self.assertTrue(induction_calls[1])
        self.assertEqual(induction_calls[1][0]["issue_scope"], "codebook")
        self.assertEqual(assignment_calls, 2)

    def test_human_review_signal_alone_does_not_trigger_automatic_correction(self) -> None:
        outputs = [
            ValidationOutput(
                artifact_id="artifact-1",
                signals=[
                    ValidationSignal(
                        signal="human_review_required",
                        issue_scope="assignment",
                        summary="A researcher should inspect this case.",
                    )
                ],
            )
        ]

        feedback = EvidenceFirstBootstrap._validation_feedback(
            outputs,
            scopes={"assignment", "evidence"},
        )

        self.assertEqual(feedback, [])

    def test_legacy_overlap_signal_is_routed_as_assignment_feedback(self) -> None:
        outputs = [
            ValidationOutput(
                artifact_id="artifact-1",
                signals=[
                    ValidationSignal(
                        signal="category_overlap",
                        summary="Legacy signal without an explicit scope.",
                    )
                ],
            )
        ]

        feedback = EvidenceFirstBootstrap._validation_feedback(
            outputs,
            scopes={"assignment"},
        )

        self.assertEqual(feedback[0]["issue_scope"], "assignment")

    def test_sampler_keeps_visible_groups_together(self) -> None:
        artifacts = [
            ArtifactRecord("a", "alpha analyzer failure", {}, metadata={"repo_name": "one"}),
            ArtifactRecord("b", "alpha analyzer crash", {}, metadata={"repo_name": "one"}),
            ArtifactRecord("c", "beta build failure", {}, metadata={"repo_name": "two"}),
            ArtifactRecord("d", "gamma parser fault", {}, metadata={"repo_name": "three"}),
        ]
        selected, groups = select_bootstrap_artifacts(
            artifacts,
            BootstrapConfig(fraction=0.5, minimum_size=1, maximum_size=2),
        )
        selected_ids = {artifact.artifact_id for artifact in selected}
        self.assertTrue({"a", "b"}.issubset(selected_ids) or not ({"a", "b"} & selected_ids))
        self.assertLess(len(selected), len(artifacts))
        self.assertEqual(groups["a"], groups["b"])

    def test_sampler_covers_available_strata_before_repeating_them(self) -> None:
        artifacts = [
            ArtifactRecord(
                "a",
                "same visible terms",
                {},
                metadata={
                    "discussion_id": "thread-a",
                    "repo_name": "repo-a",
                    "year": "2024",
                },
            ),
            ArtifactRecord(
                "b",
                "same visible terms",
                {},
                metadata={
                    "discussion_id": "thread-b",
                    "repo_name": "repo-a",
                    "year": "2024",
                },
            ),
            ArtifactRecord(
                "c",
                "same visible terms",
                {},
                metadata={
                    "discussion_id": "thread-c",
                    "repo_name": "repo-b",
                    "year": "2025",
                },
            ),
        ]

        selected, _ = select_bootstrap_artifacts(
            artifacts,
            BootstrapConfig(
                fraction=0.67,
                minimum_size=2,
                maximum_size=2,
                stratification_fields=("repo_name", "year"),
            ),
        )

        self.assertEqual(
            {artifact.metadata["repo_name"] for artifact in selected},
            {"repo-a", "repo-b"},
        )

    def test_bootstrap_generates_b1_without_human_records(self) -> None:
        adapter = StaticAnalysisNondeterminismAdapter()
        artifacts = list(adapter.iter_artifacts())[:4]
        run_state = build_single_batch_run_state(
            adapter.load_dataset_metadata(), artifacts, batch_id="test-batch"
        )
        backend = _ScriptedBackend()
        run_state.analysis_protocol.allow_multiple_codes = False
        bootstrap = EvidenceFirstBootstrap(
            model_config=LLMModelConfig(model="test", json_mode=False),
            backend=backend,
            context_agent=_context,
            initial_coder_agents=[
                ("initial-a", _initial_coder("model-a")),
                ("initial-b", _initial_coder("model-b")),
            ],
            induction_agent=_induction,
            config=BootstrapConfig(fraction=0.5, minimum_size=1, maximum_size=2, batch_size=10),
        )
        result = bootstrap.run(run_state, artifacts)
        self.assertEqual(result.status, "completed")
        self.assertEqual(result.codebook.version, 1)
        self.assertEqual(len(result.codebook.codes), 1)
        self.assertEqual(result.codebook.codes[0].metadata["origin"], "llm_initial_induction")
        self.assertFalse(result.codebook.codes[0].metadata["human_reviewed"])
        self.assertTrue(result.assignments)
        self.assertEqual(len(backend.assignment_requests), 1)
        assignment_request = backend.assignment_requests[0]
        self.assertFalse(assignment_request["analysis_protocol"]["allow_multiple_codes"])
        self.assertEqual(assignment_request["research_question"],
                         run_state.research_question.question_text)
        self.assertTrue(assignment_request["original_materials"])
        self.assertEqual(len(result.initial_codings), 2)
        self.assertTrue(result.analytic_memos)
        self.assertEqual(run_state.history.coding_records, [])
        self.assertEqual(len(result.supporting_model_calls), 2)
        for call in result.supporting_model_calls:
            self.assertEqual(call["model"], "test")
            self.assertEqual(call["temperature"], 0.0)
            self.assertEqual(call["max_retries"], 4)
            self.assertEqual(call["finish_reason"], "stop")
            self.assertEqual(call["usage"]["total_tokens"], 50)
            self.assertEqual(call["elapsed_seconds"], 0.25)
            self.assertEqual(call["estimated_cost_usd"], 0.001)

    def test_multi_batch_induction_finishes_with_all_initial_cases(self) -> None:
        adapter = StaticAnalysisNondeterminismAdapter()
        artifacts = list(adapter.iter_artifacts())[:4]
        run_state = build_single_batch_run_state(
            adapter.load_dataset_metadata(), artifacts, batch_id="global-induction"
        )
        seen_case_ids: list[list[str]] = []
        seen_stages: list[str] = []

        def recording_induction(agent_input) -> InductionAgentOutput:
            case_ids = [case.artifact_id for case in agent_input.cases]
            seen_case_ids.append(case_ids)
            seen_stages.append(agent_input.induction_stage)
            return InductionAgentOutput(
                codes=[
                    CodeState(
                        code_id="analysis-failure",
                        name="Analysis failure",
                        definition="An evidence-grounded analysis failure.",
                        representative_artifact_ids=case_ids,
                    )
                ],
                change_log=[],
            )

        bootstrap = EvidenceFirstBootstrap(
            model_config=LLMModelConfig(model="test", json_mode=False),
            backend=_ScriptedBackend(),
            context_agent=_context,
            initial_coder_agents=[
                ("initial-a", _initial_coder("model-a")),
                ("initial-b", _initial_coder("model-b")),
            ],
            induction_agent=recording_induction,
            config=BootstrapConfig(
                fraction=0.99,
                minimum_size=4,
                maximum_size=4,
                batch_size=1,
            ),
        )

        result = bootstrap.run(run_state, artifacts)

        self.assertEqual(result.status, "completed")
        self.assertEqual([len(ids) for ids in seen_case_ids], [1, 1, 1, 3])
        self.assertEqual(
            seen_stages,
            ["incremental_batch"] * 3 + ["global_consolidation"],
        )
        self.assertEqual(result.draft_codebooks[-1]["stage"], "global_consolidation")
        self.assertEqual(
            set(result.draft_codebooks[-1]["artifact_ids"]),
            set(result.artifact_ids),
        )

        # A small initialization sample needs the same semantic consolidation,
        # without an extra induction call solely to mark the stage as final.
        seen_case_ids.clear()
        seen_stages.clear()
        single_batch_bootstrap = EvidenceFirstBootstrap(
            model_config=LLMModelConfig(model="test", json_mode=False),
            backend=_ScriptedBackend(),
            context_agent=_context,
            initial_coder_agents=[
                ("initial-a", _initial_coder("model-a")),
                ("initial-b", _initial_coder("model-b")),
            ],
            induction_agent=recording_induction,
            config=BootstrapConfig(
                fraction=0.99,
                minimum_size=4,
                maximum_size=4,
                batch_size=12,
            ),
        )
        single_batch_result = single_batch_bootstrap.run(run_state, artifacts)
        self.assertEqual(single_batch_result.status, "completed")
        self.assertEqual(seen_stages, ["global_consolidation"])
        self.assertEqual(set(seen_case_ids[0]), set(single_batch_result.artifact_ids))

    def test_initial_coders_run_concurrently_and_preserve_configured_order(self) -> None:
        adapter = StaticAnalysisNondeterminismAdapter()
        artifacts = list(adapter.iter_artifacts())[:2]
        run_state = build_single_batch_run_state(
            adapter.load_dataset_metadata(), artifacts, batch_id="parallel-batch"
        )
        barrier = threading.Barrier(2, timeout=2)

        def blocking_coder(model: str):
            base_coder = _initial_coder(model)

            def coder(agent_input):
                barrier.wait()
                return base_coder(agent_input)

            return coder

        bootstrap = EvidenceFirstBootstrap(
            model_config=LLMModelConfig(model="test", json_mode=False),
            backend=_ScriptedBackend(),
            context_agent=_context,
            initial_coder_agents=[
                ("initial-a", blocking_coder("model-a")),
                ("initial-b", blocking_coder("model-b")),
            ],
            induction_agent=_induction,
            config=BootstrapConfig(
                fraction=0.5,
                minimum_size=1,
                maximum_size=1,
                batch_size=10,
            ),
        )

        result = bootstrap.run(run_state, artifacts)

        self.assertEqual(result.status, "completed")
        self.assertEqual(
            [output.coder_id for output in result.initial_codings[0].coder_outputs],
            ["initial-a", "initial-b"],
        )

    def test_bootstrap_reports_artifact_progress_for_each_stage(self) -> None:
        adapter = StaticAnalysisNondeterminismAdapter()
        artifacts = list(adapter.iter_artifacts())[:4]
        run_state = build_single_batch_run_state(
            adapter.load_dataset_metadata(), artifacts, batch_id="progress-batch"
        )
        progress: list[dict[str, object]] = []
        coder_calls: list[tuple[str, int, int]] = []
        bootstrap = EvidenceFirstBootstrap(
            model_config=LLMModelConfig(model="test", json_mode=False),
            backend=_ScriptedBackend(),
            context_agent=_context,
            initial_coder_agents=[
                ("initial-a", _initial_coder("model-a", coder_calls)),
                ("initial-b", _initial_coder("model-b", coder_calls)),
            ],
            induction_agent=_induction,
            config=BootstrapConfig(fraction=0.5, minimum_size=1, maximum_size=2, batch_size=1),
        )

        result = bootstrap.run(run_state, artifacts, progress_callback=progress.append)

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.progress["processed_artifacts"], 2)
        self.assertEqual(result.progress["total_artifacts"], 2)
        self.assertEqual(result.progress["percent"], 100)
        self.assertEqual(progress[0]["phase"], "evidence")
        self.assertEqual(progress[0]["processed_artifacts"], 0)
        self.assertEqual(progress[-1]["phase"], "completed")
        self.assertEqual(
            [item["phase"] for item in progress if item["phase"] in {"evidence", "initial_coding", "induction", "audit", "assignment"}],
            ["evidence", "evidence", "evidence", "initial_coding", "initial_coding", "initial_coding", "induction", "induction", "induction", "assignment", "assignment", "assignment", "audit"],
        )
        self.assertEqual(len(coder_calls), 4)
        self.assertTrue(all(code_count == 0 and history_count == 0 for _, code_count, history_count in coder_calls))

    def test_failed_bootstrap_resumes_from_persisted_stage_outputs(self) -> None:
        adapter = StaticAnalysisNondeterminismAdapter()
        artifacts = list(adapter.iter_artifacts())[:4]
        run_state = build_single_batch_run_state(
            adapter.load_dataset_metadata(), artifacts, batch_id="resume-bootstrap"
        )
        context_calls: list[str] = []
        coder_calls: list[tuple[str, int, int]] = []

        def counting_context(agent_input) -> ContextPacket:
            context_calls.append(agent_input.artifact.artifact_id)
            return _context(agent_input)

        class FlakyInduction:
            def __init__(self) -> None:
                self.calls = 0

            def __call__(self, agent_input) -> InductionAgentOutput:
                self.calls += 1
                if self.calls == 1:
                    raise RuntimeError("temporary induction failure")
                return _induction(agent_input)

        induction = FlakyInduction()
        bootstrap = EvidenceFirstBootstrap(
            model_config=LLMModelConfig(model="test", json_mode=False),
            backend=_ScriptedBackend(),
            context_agent=counting_context,
            initial_coder_agents=[
                ("initial-a", _initial_coder("model-a", coder_calls)),
                ("initial-b", _initial_coder("model-b", coder_calls)),
            ],
            induction_agent=induction,
            config=BootstrapConfig(
                fraction=0.5,
                minimum_size=1,
                maximum_size=2,
                batch_size=10,
            ),
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            checkpoint_dir = Path(temp_dir) / "bootstrap_checkpoints"
            failed = bootstrap.run(
                run_state,
                artifacts,
                checkpoint_dir=checkpoint_dir,
            )
            self.assertEqual(failed.status, "failed")
            self.assertEqual(len(context_calls), 2)
            self.assertEqual(len(coder_calls), 4)
            self.assertTrue(any(checkpoint_dir.iterdir()))

            resumed = bootstrap.run(
                run_state,
                artifacts,
                checkpoint_dir=checkpoint_dir,
            )

        self.assertEqual(resumed.status, "completed")
        self.assertEqual(induction.calls, 2)
        self.assertEqual(len(context_calls), 2)
        self.assertEqual(len(coder_calls), 4)

    def test_resume_cache_key_changes_with_supporting_model_configuration(self) -> None:
        adapter = StaticAnalysisNondeterminismAdapter()
        artifacts = list(adapter.iter_artifacts())[:4]
        run_state = build_single_batch_run_state(
            adapter.load_dataset_metadata(), artifacts, batch_id="cache-model"
        )
        config = BootstrapConfig(
            fraction=0.5,
            minimum_size=1,
            maximum_size=2,
            batch_size=10,
        )
        selected, _ = select_bootstrap_artifacts(artifacts, config)

        def build(model: str) -> EvidenceFirstBootstrap:
            return EvidenceFirstBootstrap(
                model_config=LLMModelConfig(model=model, json_mode=False),
                backend=_ScriptedBackend(),
                context_agent=_context,
                initial_coder_agents=[
                    ("initial-a", _initial_coder("model-a")),
                    ("initial-b", _initial_coder("model-b")),
                ],
                induction_agent=_induction,
                config=config,
            )

        protocol = {"population_size": len(artifacts)}
        self.assertNotEqual(
            build("assignment-model-a")._resume_cache_key(
                run_state, selected, protocol
            ),
            build("assignment-model-b")._resume_cache_key(
                run_state, selected, protocol
            ),
        )
        # Definition application has its own prompt, so a wording change must
        # invalidate cached assignments even if the category agent is unchanged.
        from unittest.mock import patch
        from coda.prompts import read_prompt_file
        bootstrap = build("assignment-model-a")
        original_key = bootstrap._resume_cache_key(run_state, selected, protocol)
        def changed_prompt(name):
            value = read_prompt_file(name)
            return value + "\nChanged assignment rule." if name == "induction_assignment_system_prompt.txt" else value
        with patch("coda.bootstrap.read_prompt_file", side_effect=changed_prompt):
            self.assertNotEqual(original_key, bootstrap._resume_cache_key(
                run_state, selected, protocol))

    def test_web_run_excludes_successful_bootstrap_sample_from_human_queue(self) -> None:
        bootstrap_ids: list[str] = []

        class SuccessfulBootstrap:
            def run(self, run_state, artifacts):
                bootstrap_artifact = artifacts[0]
                bootstrap_ids.append(bootstrap_artifact.artifact_id)
                code = CodeState(
                    code_id="bootstrap-code",
                    name="Bootstrap code",
                    definition="A provisional initial concept.",
                    representative_artifact_ids=[bootstrap_artifact.artifact_id],
                    metadata={"origin": "llm_bootstrap", "human_reviewed": False},
                )
                return BootstrapResult(
                    codebook=CodebookState(run_state.dataset_metadata.dataset_name, 0, [code]),
                    artifact_ids=[bootstrap_artifact.artifact_id],
                    group_ids={bootstrap_artifact.artifact_id: bootstrap_artifact.artifact_id},
                )

        with tempfile.TemporaryDirectory() as temp_dir:
            service = CodaWebService(
                runs_root=Path(temp_dir) / "runs",
                adapter_factories={"static_analysis_nondeterminism": StaticAnalysisNondeterminismAdapter},
                orchestrator_factory=lambda: _build_test_orchestrator([]),
                bootstrap_factory=lambda _: SuccessfulBootstrap(),
            )
            created = service.create_run(
                dataset_name="static_analysis_nondeterminism", artifact_limit=3
            )
            self.assertEqual(created["bootstrap_status"], "not_run")
            self.assertEqual(created["total_artifacts"], 3)
            self.assertIsNone(service.current_artifact(str(created["run_id"]))["artifact"])

            initialized = service.initialize_run(str(created["run_id"]))
            self.assertEqual(initialized["bootstrap_status"], "completed")
            self.assertEqual(initialized["bootstrap_artifacts"], 1)
            self.assertEqual(initialized["total_artifacts"], 2)
            current = service.current_artifact(str(created["run_id"]))
            self.assertNotEqual(current["artifact"]["artifact_id"], bootstrap_ids[0])
            assigned = service.code_artifacts(str(created["run_id"]), "bootstrap-code")
            self.assertEqual(assigned["artifact_count"], 1)
            self.assertIsNone(assigned["artifacts"][0]["review"])
            run_dir = Path(str(created["run_dir"]))
            self.assertTrue((run_dir / "bootstrap_manifest.json").exists())
            self.assertTrue((run_dir / "bootstrap_initial_codings.jsonl").exists())
            self.assertTrue((run_dir / "initial_codebook_v0.json").exists())
            self.assertTrue((run_dir / "bootstrap_audit.json").exists())
            self.assertTrue((run_dir / "bootstrap_assignments.jsonl").exists())

    def test_web_task_defers_bootstrap_until_explicit_initialization(self) -> None:
        class CountingBootstrap:
            def __init__(self) -> None:
                self.called = False

            def run(self, run_state, artifacts):
                self.called = True
                return BootstrapResult(
                    codebook=CodebookState.empty(run_state.dataset_metadata.dataset_name),
                    artifact_ids=[],
                    group_ids={artifact.artifact_id: artifact.artifact_id for artifact in artifacts},
                    protocol={"population_size": len(artifacts)},
                )

        bootstrap = CountingBootstrap()
        with tempfile.TemporaryDirectory() as temp_dir:
            service = CodaWebService(
                runs_root=Path(temp_dir) / "runs",
                adapter_factories={"static_analysis_nondeterminism": StaticAnalysisNondeterminismAdapter},
                orchestrator_factory=lambda: _build_test_orchestrator([]),
                bootstrap_factory=lambda _: bootstrap,
            )
            created = service.create_run(
                dataset_name="static_analysis_nondeterminism",
                artifact_limit=3,
            )
            run_id = str(created["run_id"])
            self.assertFalse(bootstrap.called)
            self.assertTrue(created["bootstrap_enabled"])
            self.assertEqual(created["bootstrap_status"], "not_run")
            self.assertEqual(created["input_artifacts"], 3)
            self.assertEqual(created["human_review_artifacts"], 3)
            self.assertEqual(created["bootstrap_artifacts"], 0)
            self.assertIsNone(service.current_artifact(run_id)["artifact"])
            self.assertIsNone(service.run_artifacts(run_id)["bootstrap"])

            initialized = service.initialize_run(run_id)
            self.assertTrue(bootstrap.called)
            self.assertEqual(initialized["bootstrap_status"], "completed")
            self.assertIsNotNone(service.current_artifact(run_id)["artifact"])
