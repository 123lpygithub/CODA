"""FastAPI entry point for the local CODA research workbench."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Literal
from urllib.parse import urlsplit
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from openai import APIConnectionError, APITimeoutError, OpenAIError, RateLimitError
from pydantic import BaseModel, Field

from adapters.base import TextLocator
from coda.contracts import EvidenceItem, HumanReviewOutput
from coda.state import CodeState, CodebookChangeState, ExperimentVariant
from coda.web.runtime import CodaWebService, WebRunNotFoundError, WebWorkflowError
from coda.web.static import WorkbenchFiles


class CreateRunRequest(BaseModel):
    dataset_name: str = Field(min_length=1)
    artifact_limit: int | None = Field(default=None, ge=1)
    iterative_batch_size: int = Field(default=1, ge=1)
    held_out_enabled: bool = False
    held_out_size: int | None = Field(default=None, ge=1)
    review_budget_minutes: int | None = Field(default=None, ge=1)
    review_mode: Literal[
        "automatic",
        "selective",
        "full",
    ] = "selective"
    experiment_variant: ExperimentVariant = "standard"
    study_manifest_path: str | None = None
    study_phase: Literal["pilot", "formal"] | None = None
    participant_id: str | None = Field(default=None, min_length=1)
    replicate_index: int | None = Field(default=None, ge=1, le=2)
    comparison_block_id: str | None = Field(default=None, min_length=1)


class InitialReviewSettingRequest(BaseModel):
    setting: Literal["automatic", "selective", "full"]
    continue_automatic: bool = False


class CodeInput(BaseModel):
    code_id: str = Field(min_length=1)
    name: str = Field(min_length=1)
    definition: str = Field(min_length=1)
    inclusion_criteria: list[str] = Field(default_factory=list)
    exclusion_criteria: list[str] = Field(default_factory=list)
    boundary_artifact_ids: list[str] = Field(default_factory=list)
    counterexample_status: Literal[
        "not_assessed",
        "no_observed_counterexample",
        "observed_counterexample",
    ] = "not_assessed"
    hypothetical_examples: list[str] = Field(default_factory=list)
    parent_code_id: str | None = None
    status: Literal["active", "merged", "split", "retired"] = "active"
    notes: list[str] = Field(default_factory=list)
    metadata: dict[str, object] = Field(default_factory=dict)


class CodebookChangeInput(BaseModel):
    change_id: str | None = None
    action: Literal["add", "add_parent", "refine", "merge", "split", "rename", "retire", "no_change"]
    summary: str = Field(min_length=1)
    rationale: str = ""
    target_code_ids: list[str] = Field(default_factory=list)
    resulting_code_ids: list[str] = Field(default_factory=list)
    artifact_ids: list[str] = Field(default_factory=list)
    metadata: dict[str, object] = Field(default_factory=dict)


class EvidenceLocatorInput(BaseModel):
    start: int | None = Field(default=None, ge=0)
    end: int | None = Field(default=None, ge=0)
    line_start: int | None = Field(default=None, ge=1)
    line_end: int | None = Field(default=None, ge=1)


class EvidenceInput(BaseModel):
    field_name: str = Field(min_length=1)
    excerpt: str = Field(min_length=1)
    locator: EvidenceLocatorInput | None = None
    rationale: str = ""
    rationale_zh: str = ""
    claim_type: Literal["reported", "observed", "inferred"] = "reported"
    revision: str | None = None


class SubmitReviewRequest(BaseModel):
    artifact_id: str = Field(min_length=1)
    decision: Literal[
        "accept",
        "revise",
        "reject",
        "mark_uncertain",
        "request_additional_context",
    ]
    pre_read_memo: str = Field(min_length=1)
    final_codes: list[CodeInput] = Field(default_factory=list)
    rationale: str = Field(min_length=1)
    evidence_summary: list[str] = Field(default_factory=list)
    confirmed_evidence: list[EvidenceInput] = Field(default_factory=list)
    preserved_alternatives: list[str] = Field(default_factory=list)
    codebook_changes: list[CodebookChangeInput] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)
    duration_seconds: float | None = Field(default=None, ge=0)


class StageReviewRequest(BaseModel):
    decision: Literal[
        "accept",
        "revise",
        "reject",
        "request_additional_context",
        "mark_unresolved",
    ]
    rationale: str = Field(min_length=1)
    revised_codes: list[CodeInput] = Field(default_factory=list)
    change_operations: list[CodebookChangeInput] = Field(default_factory=list)
    duration_seconds: float | None = Field(default=None, ge=0)


class ReviewTimerRequest(BaseModel):
    action: Literal["pause", "resume"]
    scope: Literal["artifact", "initial", "triggered", "final", "rework"]
    artifact_id: str | None = None


class ResolveContextRequest(BaseModel):
    supplied_context: list[str] = Field(default_factory=list)
    resolution: str = Field(min_length=1)


class UpdateAnalyticMemoRequest(BaseModel):
    status: Literal["open", "resolved"]
    rationale: str = Field(min_length=1)


def _validate_review_submission(payload: SubmitReviewRequest) -> None:
    """Reject review combinations that would make the audit record incoherent."""

    if not payload.pre_read_memo.strip():
        raise ValueError("Record an independent pre-read memo before submitting a review.")
    if not payload.rationale.strip():
        raise ValueError("Provide a final review rationale before submitting.")
    if payload.decision in {
        "reject",
        "mark_uncertain",
        "request_additional_context",
    }:
        if payload.final_codes or payload.codebook_changes:
            raise ValueError(
                "Reject and mark_uncertain cannot include final codes or codebook changes."
            )
    if payload.final_codes and not payload.confirmed_evidence:
        raise ValueError(
            "Every final code requires at least one human-confirmed structured evidence item."
        )


def _to_human_review_output(
    payload: SubmitReviewRequest,
    *,
    codebook_version: int,
) -> HumanReviewOutput:
    final_codes = [CodeState(**code.model_dump()) for code in payload.final_codes]
    changes = [
        CodebookChangeState(
            change_id=change.change_id or f"web-change-{uuid4().hex[:12]}",
            action=change.action,
            round_index=codebook_version,
            summary=change.summary,
            rationale=change.rationale,
            target_code_ids=change.target_code_ids,
            resulting_code_ids=change.resulting_code_ids,
            artifact_ids=change.artifact_ids,
            metadata=change.metadata,
        )
        for change in payload.codebook_changes
    ]
    confirmed_evidence = [
        EvidenceItem(
            field_name=item.field_name,
            excerpt=item.excerpt,
            locator=(
                TextLocator(**item.locator.model_dump())
                if item.locator is not None
                else None
            ),
            rationale=item.rationale,
            rationale_zh=item.rationale_zh,
            claim_type=item.claim_type,
            revision=item.revision,
        )
        for item in payload.confirmed_evidence
    ]
    return HumanReviewOutput(
        artifact_id=payload.artifact_id,
        decision=payload.decision,
        pre_read_memo=payload.pre_read_memo.strip(),
        final_codes=final_codes,
        rationale=payload.rationale,
        evidence_summary=payload.evidence_summary,
        confirmed_evidence=confirmed_evidence,
        preserved_alternatives=payload.preserved_alternatives,
        codebook_changes=changes,
        request_additional_context=payload.decision == "request_additional_context",
        notes=payload.notes,
        metadata={
            "human_reviewed": True,
            "duration_seconds": payload.duration_seconds,
        },
    )


def _http_error(error: Exception) -> HTTPException:
    if isinstance(error, WebRunNotFoundError):
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))
    if isinstance(error, WebWorkflowError):
        return HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error))
    if isinstance(error, APITimeoutError):
        return HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="LLM 请求超时。请稍后重试；可通过 CODA_LLM_TIMEOUT_SECONDS 增大超时时间。",
        )
    if isinstance(error, RateLimitError):
        return HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="LLM 服务返回限流。请稍后重试。",
        )
    if isinstance(error, APIConnectionError):
        return HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="无法连接 LLM 服务。请检查中转站状态和网络连接。",
        )
    if isinstance(error, OpenAIError):
        return HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"LLM 服务请求失败：{error}",
        )
    return HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(error))


def create_app(
    service: CodaWebService | None = None,
    *,
    frontend_dist: str | Path | None = None,
) -> FastAPI:
    """Create an app; dependency injection keeps API tests model-free."""

    runtime = service or CodaWebService()
    app = FastAPI(
        title="CODA Research Workbench API",
        version="0.1.0",
        description="Local API for evidence-grounded, human-reviewed open coding.",
    )
    # Exact deployment origins, with local development allowed separately.
    # CORS controls browser access; it is not user authentication.
    allowed_origins = []
    for origin in os.environ.get("CODA_ALLOWED_ORIGINS", "").split(","):
        origin = origin.strip().rstrip("/")
        if not origin:
            continue
        parsed = urlsplit(origin)
        if (parsed.scheme not in {"http", "https"} or not parsed.netloc
                or parsed.path or parsed.query or parsed.fragment
                or parsed.username or parsed.password or "*" in origin):
            raise ValueError("CODA_ALLOWED_ORIGINS must contain comma-separated HTTP(S) origins without paths or wildcards.")
        allowed_origins.append(origin)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        # Vite may choose a different local port when another dev server is active.
        # Production browser origins must be listed explicitly above.
        allow_origin_regex=r"https?://(127\.0\.0\.1|localhost):\d+",
        allow_credentials=False,
        # Include POST/DELETE and content-type preflights for the workbench API.
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/api/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/api/runtime")
    def runtime_info() -> dict[str, object]:
        return runtime.runtime_info()

    @app.get("/api/runs/{run_id}/execution")
    def execution_status(run_id: str) -> dict[str, object]:
        try:
            return runtime.execution_status(run_id)
        except (OSError, ValueError, TypeError, WebWorkflowError) as error:
            raise _http_error(error) from error

    @app.get("/api/datasets")
    def list_datasets() -> list[dict[str, object]]:
        try:
            return runtime.available_datasets()
        except (OSError, ValueError, TypeError, WebWorkflowError) as error:
            raise _http_error(error) from error

    @app.post("/api/runs", status_code=status.HTTP_201_CREATED)
    def create_run(payload: CreateRunRequest) -> dict[str, object]:
        try:
            return runtime.create_run(**payload.model_dump())
        except (OSError, ValueError, TypeError, WebWorkflowError) as error:
            raise _http_error(error) from error

    @app.post("/api/runs/{run_id}/initialize")
    def initialize_run(
        run_id: str,
        language: Literal["en", "zh"] = Query(default="en"),
    ) -> dict[str, object]:
        """Run the fixed LLM bootstrap after a task has been created."""

        try:
            return runtime.initialize_run(run_id, language=language)
        except (OSError, RuntimeError, ValueError, TypeError, WebWorkflowError) as error:
            raise _http_error(error) from error

    @app.post("/api/runs/{run_id}/initialize/cancel")
    def cancel_initialization(run_id: str) -> dict[str, object]:
        """Pause initialization without deleting completed stage checkpoints."""

        try:
            return runtime.cancel_initialization(run_id)
        except (OSError, RuntimeError, ValueError, TypeError, WebWorkflowError) as error:
            raise _http_error(error) from error

    @app.get("/api/runs/{run_id}/stage-reviews/{kind}")
    def stage_review_packet(
        run_id: str, kind: Literal["initial", "final"], inspection: bool = Query(default=False),
    ) -> dict[str, object]:
        try:
            return runtime.stage_review_packet(run_id, kind, inspection=inspection)
        except (OSError, ValueError, TypeError, WebWorkflowError) as error:
            raise _http_error(error) from error

    @app.post("/api/runs/{run_id}/initial-review-setting")
    def select_initial_review_setting(run_id: str, payload: InitialReviewSettingRequest) -> dict[str, object]:
        try:
            return runtime.select_initial_review_setting(run_id, **payload.model_dump())
        except (OSError, ValueError, TypeError, WebWorkflowError) as error:
            raise _http_error(error) from error

    @app.post("/api/runs/{run_id}/stage-reviews/{kind}")
    def submit_stage_review(
        run_id: str,
        kind: Literal["initial", "final"],
        payload: StageReviewRequest,
    ) -> dict[str, object]:
        try:
            revised_codes = [
                CodeState(**code.model_dump()) for code in payload.revised_codes
            ]
            change_operations = [
                CodebookChangeState(
                    change_id=change.change_id or f"stage-change-{uuid4().hex[:12]}",
                    action=change.action,
                    round_index=0,
                    summary=change.summary,
                    rationale=change.rationale,
                    target_code_ids=change.target_code_ids,
                    resulting_code_ids=change.resulting_code_ids,
                    artifact_ids=change.artifact_ids,
                    metadata=change.metadata,
                )
                for change in payload.change_operations
            ]
            return runtime.submit_stage_review(
                run_id,
                kind,
                decision=payload.decision,
                rationale=payload.rationale,
                revised_codes=revised_codes,
                change_operations=change_operations,
                duration_seconds=payload.duration_seconds,
            )
        except (OSError, ValueError, TypeError, WebWorkflowError) as error:
            raise _http_error(error) from error

    @app.post("/api/runs/{run_id}/review-timer")
    def review_timer(run_id: str, payload: ReviewTimerRequest) -> dict[str, object]:
        try:
            return runtime.record_review_timer(
                run_id,
                action=payload.action,
                scope=payload.scope,
                artifact_id=payload.artifact_id,
            )
        except (OSError, ValueError, TypeError, WebWorkflowError) as error:
            raise _http_error(error) from error

    @app.post("/api/runs/{run_id}/process-automatic")
    def process_automatic(
        run_id: str,
        language: Literal["en", "zh"] = Query(default="en"),
        max_artifacts: int | None = Query(default=None, ge=1),
    ) -> dict[str, object]:
        """Process safe Automatic/Selective artifacts until human work is needed."""

        try:
            return runtime.process_automatic(run_id, language=language, max_artifacts=max_artifacts)
        except (
            OSError,
            RuntimeError,
            ValueError,
            TypeError,
            OpenAIError,
            WebWorkflowError,
        ) as error:
            raise _http_error(error) from error

    @app.get("/api/runs")
    def list_runs() -> list[dict[str, object]]:
        return runtime.list_runs()

    @app.get("/api/runs/{run_id}")
    def get_run(run_id: str) -> dict[str, object]:
        try:
            return runtime.run_summary(run_id)
        except (OSError, ValueError, TypeError, WebWorkflowError) as error:
            raise _http_error(error) from error

    @app.get("/api/runs/{run_id}/held-out-materials")
    def held_out_materials(run_id: str) -> dict[str, object]:
        """Return the reference-blind packet for a completed held-out split."""

        try:
            return runtime.export_held_out_materials(run_id)
        except (OSError, ValueError, TypeError, WebWorkflowError) as error:
            raise _http_error(error) from error

    @app.delete("/api/runs/{run_id}")
    def delete_run(run_id: str) -> dict[str, object]:
        try:
            return runtime.delete_run(run_id)
        except (OSError, ValueError, TypeError, WebWorkflowError) as error:
            raise _http_error(error) from error

    @app.post("/api/runs/{run_id}/resume")
    def resume_run(run_id: str) -> dict[str, object]:
        try:
            return runtime.run_summary(run_id)
        except (OSError, ValueError, TypeError, WebWorkflowError) as error:
            raise _http_error(error) from error

    @app.get("/api/runs/{run_id}/current-artifact")
    def current_artifact(run_id: str) -> dict[str, object]:
        try:
            return runtime.current_artifact(run_id)
        except (OSError, ValueError, TypeError, WebWorkflowError) as error:
            raise _http_error(error) from error

    @app.post("/api/runs/{run_id}/prepare-review")
    def prepare_review(
        run_id: str,
        language: Literal["en", "zh"] = Query(default="en"),
    ) -> dict[str, object]:
        try:
            return runtime.prepare_review(run_id, language=language)
        except (
            OSError,
            RuntimeError,
            ValueError,
            TypeError,
            OpenAIError,
            WebWorkflowError,
        ) as error:
            raise _http_error(error) from error

    @app.get("/api/runs/{run_id}/review-packet")
    def review_packet(run_id: str) -> dict[str, object]:
        try:
            return runtime.review_packet(run_id)
        except (OSError, ValueError, TypeError, WebWorkflowError) as error:
            raise _http_error(error) from error

    @app.post("/api/runs/{run_id}/submit-review")
    def submit_review(run_id: str, payload: SubmitReviewRequest) -> dict[str, object]:
        try:
            _validate_review_submission(payload)
            codebook = runtime.codebook(run_id)
            review = _to_human_review_output(
                payload,
                codebook_version=int(codebook["version"]),
            )
            return runtime.submit_review(run_id, human_review_output=review)
        except (OSError, ValueError, TypeError, WebWorkflowError) as error:
            raise _http_error(error) from error

    @app.get("/api/runs/{run_id}/retrospective-tasks")
    def retrospective_tasks(run_id: str) -> dict[str, object]:
        try:
            return runtime.retrospective_tasks(run_id)
        except (OSError, ValueError, TypeError, WebWorkflowError) as error:
            raise _http_error(error) from error

    @app.post("/api/runs/{run_id}/retrospective-tasks/{task_id}/prepare")
    def prepare_retrospective_task(
        run_id: str,
        task_id: str,
        language: Literal["en", "zh"] = Query(default="en"),
    ) -> dict[str, object]:
        try:
            return runtime.prepare_retrospective_task(run_id, task_id, language=language)
        except (
            OSError,
            RuntimeError,
            ValueError,
            TypeError,
            OpenAIError,
            WebWorkflowError,
        ) as error:
            raise _http_error(error) from error

    @app.get("/api/runs/{run_id}/retrospective-tasks/{task_id}/review-packet")
    def retrospective_review_packet(run_id: str, task_id: str) -> dict[str, object]:
        try:
            return runtime.retrospective_review_packet(run_id, task_id)
        except (OSError, ValueError, TypeError, WebWorkflowError) as error:
            raise _http_error(error) from error

    @app.post("/api/runs/{run_id}/retrospective-tasks/{task_id}/submit")
    def submit_retrospective_review(
        run_id: str,
        task_id: str,
        payload: SubmitReviewRequest,
    ) -> dict[str, object]:
        try:
            _validate_review_submission(payload)
            codebook = runtime.codebook(run_id)
            review = _to_human_review_output(
                payload,
                codebook_version=int(codebook["version"]),
            )
            return runtime.submit_retrospective_review(
                run_id,
                task_id,
                human_review_output=review,
            )
        except (
            OSError,
            ValueError,
            TypeError,
            OpenAIError,
            WebWorkflowError,
        ) as error:
            raise _http_error(error) from error

    @app.post("/api/runs/{run_id}/next-artifact")
    def next_artifact(run_id: str) -> dict[str, object]:
        try:
            return runtime.next_artifact(run_id)
        except (
            OSError,
            RuntimeError,
            ValueError,
            TypeError,
            OpenAIError,
            WebWorkflowError,
        ) as error:
            raise _http_error(error) from error

    @app.get("/api/runs/{run_id}/codebook")
    def codebook(run_id: str) -> dict[str, object]:
        try:
            return runtime.codebook(run_id)
        except (OSError, ValueError, TypeError, WebWorkflowError) as error:
            raise _http_error(error) from error

    @app.get("/api/runs/{run_id}/codebook/versions")
    def codebook_versions(run_id: str) -> dict[str, object]:
        try:
            return runtime.codebook_versions(run_id)
        except (OSError, ValueError, TypeError, WebWorkflowError) as error:
            raise _http_error(error) from error

    @app.get("/api/runs/{run_id}/codebook/{code_id}/artifacts")
    def code_artifacts(run_id: str, code_id: str) -> dict[str, object]:
        try:
            return runtime.code_artifacts(run_id, code_id)
        except (OSError, ValueError, TypeError, WebWorkflowError) as error:
            raise _http_error(error) from error

    @app.get("/api/runs/{run_id}/history")
    def history(run_id: str) -> dict[str, object]:
        try:
            return runtime.history(run_id)
        except (OSError, ValueError, TypeError, WebWorkflowError) as error:
            raise _http_error(error) from error

    @app.get("/api/runs/{run_id}/context-requests")
    def context_requests(run_id: str) -> dict[str, object]:
        try:
            return runtime.context_requests(run_id)
        except (OSError, ValueError, TypeError, WebWorkflowError) as error:
            raise _http_error(error) from error

    @app.post("/api/runs/{run_id}/analytic-memos/{memo_id}/status")
    def update_analytic_memo_status(
        run_id: str,
        memo_id: str,
        payload: UpdateAnalyticMemoRequest,
    ) -> dict[str, object]:
        try:
            return runtime.update_analytic_memo_status(
                run_id,
                memo_id,
                status=payload.status,
                rationale=payload.rationale,
            )
        except (OSError, ValueError, TypeError, WebWorkflowError) as error:
            raise _http_error(error) from error

    @app.post("/api/runs/{run_id}/context-requests/{request_id}/resolve")
    def resolve_context_request(
        run_id: str,
        request_id: str,
        payload: ResolveContextRequest,
    ) -> dict[str, object]:
        try:
            return runtime.resolve_context_request(
                run_id,
                request_id,
                supplied_context=payload.supplied_context,
                resolution=payload.resolution,
            )
        except (OSError, ValueError, TypeError, WebWorkflowError) as error:
            raise _http_error(error) from error

    @app.post("/api/runs/{run_id}/context-requests/{request_id}/cancel")
    def cancel_context_request(run_id: str, request_id: str) -> dict[str, object]:
        try:
            return runtime.cancel_context_request(run_id, request_id)
        except (OSError, ValueError, TypeError, WebWorkflowError) as error:
            raise _http_error(error) from error

    @app.get("/api/runs/{run_id}/artifacts")
    def run_artifacts(run_id: str) -> dict[str, object]:
        try:
            return runtime.run_artifacts(run_id)
        except (OSError, ValueError, TypeError, WebWorkflowError) as error:
            raise _http_error(error) from error

    if frontend_dist is not None:
        directory = Path(frontend_dist).resolve()
        if not (directory / "index.html").is_file():
            raise ValueError("Built frontend missing; run python scripts/setup_local.py first.")
        app.mount("/", WorkbenchFiles(directory=directory, html=True), name="workbench")

    return app


app = create_app()
