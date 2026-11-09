from __future__ import annotations

from dataclasses import asdict, dataclass, replace
import hashlib
import time
from uuid import uuid4
from pathlib import Path
from typing import Any, Callable, TypeVar

from coda.llm import (
    ChatBackend,
    LLMMessage,
    LLMModelConfig,
    LLMRefusalError,
    LLMResponse,
)
from coda.parsing import extract_json_array, extract_json_object

OutputLanguage = str
ValidatedOutput = TypeVar("ValidatedOutput")


@dataclass(frozen=True)
class AgentPromptSpec:
    """Prompt definition shared by role-specific agents."""

    name: str
    system_prompt: str
    user_prompt_template: str


class AgentExecutionError(RuntimeError):
    """Raised when an agent cannot produce contract-compliant output."""


class AgentRefusalError(AgentExecutionError):
    """Raised for an explicit provider refusal; this must route directly to R6."""

    def __init__(self, refusal: str) -> None:
        self.refusal = refusal
        super().__init__(f"The provider explicitly refused this agent request: {refusal[:500]}")


class BaseLLMAgent:
    """Shared prompt rendering and LLM invocation logic for CODA agents."""

    def __init__(
        self,
        *,
        prompt_spec: AgentPromptSpec,
        model_config: LLMModelConfig,
        backend: ChatBackend,
        bilingual_output: bool = True,
    ) -> None:
        self._prompt_spec = prompt_spec
        self._model_config = model_config
        self._backend = backend
        self._bilingual_output = bilingual_output
        self._output_language: OutputLanguage = "en"
        self._format_retry_metadata: dict[str, dict[str, Any]] = {}
        self._response_traces: dict[str, dict[str, Any]] = {}
        self.execution_log: list[dict[str, Any]] = []
        self.trace_sink: Callable[[dict[str, Any]], None] | None = None

    @property
    def prompt_name(self) -> str:
        return self._prompt_spec.name

    @property
    def model_config(self) -> LLMModelConfig:
        """Expose immutable model identity for reproducibility records."""

        return self._model_config

    def render_user_prompt(self, **template_values: Any) -> str:
        """Fill the user prompt template with runtime values."""

        try:
            return self._prompt_spec.user_prompt_template.format(**template_values)
        except KeyError as error:
            msg = f"Missing prompt variable for {self.prompt_name}: {error.args[0]}"
            raise AgentExecutionError(msg) from error

    def build_messages(self, *, user_prompt: str) -> list[LLMMessage]:
        """Convert one rendered prompt into chat messages."""

        language_instruction = self._language_instruction()
        return [
            LLMMessage(
                role="system",
                content=self._prompt_spec.system_prompt + language_instruction,
            ),
            LLMMessage(role="user", content=user_prompt + language_instruction),
        ]

    def _language_instruction(self) -> str:
        """Require paired bilingual text from one shared analysis."""

        if not self._bilingual_output:
            return (
                "\n\nReturn the requested JSON contract exactly. Keep rubric dimension and "
                "status tokens in English. Do not add translations, markdown, or fields "
                "outside the contract. Preserve identifiers and quoted source text."
            )

        if self._output_language == "zh":
            preferred_language = (
                "请使用中文回答中文 *_zh 字段，同时生成对应的英文 canonical 字段。"
            )
        else:
            preferred_language = (
                "Answer in English in the canonical fields and also provide the paired "
                "Chinese *_zh fields."
            )
        return (
            "\n\n"
            + preferred_language
            + " The two versions must come from one shared analysis and express the same "
            "meaning, not two independent analyses. JSON 字段名必须严格保持 as specified "
            "by the contract. Preserve verbatim evidence excerpts, source text, identifiers, "
            "and code in their original language; do not translate them. "
            "For every enum field, copy one allowed token exactly as written in the prompt. "
            "Never replace enum tokens with synonyms, spaces, hyphens, explanations, or a "
            "translation. In particular, relationship_to_codebook must be exactly one of "
            "reuse_existing_code, new_code, refine_existing_code, merge_existing_codes, "
            "add_parent_code, split_existing_code, uncertain. Return one JSON object only, with no markdown."
        )

    def set_output_language(self, language: OutputLanguage) -> None:
        """Set the natural language used by this agent's generated explanations."""

        if language not in {"en", "zh"}:
            raise ValueError("Output language must be 'en' or 'zh'.")
        self._output_language = language

    def invoke_text(self, **template_values: Any) -> LLMResponse:
        """Render prompt and send one chat request."""

        user_prompt = self.render_user_prompt(**template_values)
        messages = self.build_messages(user_prompt=user_prompt)
        return self._generate(messages)

    def invoke_json_object(self, **template_values: Any) -> dict[str, Any]:
        """Invoke the backend and parse the first JSON object in the reply."""

        payload, _response = self.invoke_json_object_with_response(**template_values)
        return payload

    def invoke_json_object_with_response(
        self,
        **template_values: Any,
    ) -> tuple[dict[str, Any], LLMResponse]:
        """Invoke the backend and return both parsed JSON and raw response."""

        response = self.invoke_text(**template_values)
        payload = extract_json_object(response.text)
        if payload is None:
            msg = f"{self.prompt_name} did not return a JSON object."
            raise AgentExecutionError(msg)
        return payload, response

    def invoke_validated_json_object(
        self,
        parser: Callable[[dict[str, Any], LLMResponse], ValidatedOutput],
        **template_values: Any,
    ) -> ValidatedOutput:
        """Parse and validate structured output, with one format-only repair."""

        user_prompt = self.render_user_prompt(**template_values)
        messages = self.build_messages(user_prompt=user_prompt)
        first_response = self._generate(messages)
        if first_response.refusal:
            raise AgentRefusalError(first_response.refusal)
        first_hash = hashlib.sha256(first_response.text.encode("utf-8")).hexdigest()
        self._format_retry_metadata[first_response.call_id] = {
            "format_retry_count": 0,
            "format_retry_errors": [],
            "original_response_sha256": first_hash,
        }
        try:
            payload = extract_json_object(first_response.text)
            if payload is None:
                raise AgentExecutionError(
                    f"{self.prompt_name} did not return a JSON object."
                )
            return parser(payload, first_response)
        except (AgentExecutionError, ValueError, TypeError, KeyError) as error:
            validation_error = f"{type(error).__name__}: {error}"

        repair_messages = [
            *messages,
            LLMMessage(role="assistant", content=first_response.text),
            LLMMessage(
                role="user",
                content=(
                    "FORMAT REPAIR ONLY. Do not redo or reinterpret the analysis. "
                    "Return the same analysis as one JSON object that satisfies the "
                    "original contract. Correct only malformed JSON, missing fields, "
                    "field types, invalid enum tokens, or explicit summary-length limits.\n\n"
                    f"Validation error:\n{validation_error}\n\n"
                    "Return one corrected JSON object and no markdown."
                ),
            ),
        ]
        repaired_response = self._generate(repair_messages, format_retry_count=1)
        if repaired_response.refusal:
            raise AgentRefusalError(repaired_response.refusal)
        self._format_retry_metadata[repaired_response.call_id] = {
            "format_retry_count": 1,
            "format_retry_errors": [validation_error],
            "original_response_sha256": first_hash,
            "model_calls": [self._response_traces[first_response.call_id],
                            {**self._response_traces[repaired_response.call_id],
                             "format_retry_count": 1}],
        }
        repaired_payload = extract_json_object(repaired_response.text)
        if repaired_payload is None:
            raise AgentExecutionError(
                f"{self.prompt_name} format repair did not return a JSON object."
            )
        try:
            return parser(repaired_payload, repaired_response)
        except (AgentExecutionError, ValueError, TypeError, KeyError) as error:
            raise AgentExecutionError(
                f"{self.prompt_name} remained unusable after one format repair: {error}"
            ) from error

    def invoke_json_array(self, **template_values: Any) -> list[Any]:
        """Invoke the backend and parse the first JSON array in the reply."""

        response = self.invoke_text(**template_values)
        payload = extract_json_array(response.text)
        if payload is None:
            msg = f"{self.prompt_name} did not return a JSON array."
            raise AgentExecutionError(msg)
        return payload

    def _generate(self, messages: list[LLMMessage], *, format_retry_count: int = 0) -> LLMResponse:
        call_id = f"call-{uuid4().hex}"
        # Configuration contains environment-variable names, never the resolved
        # API key. Do not persist provider-specific secret fields in extra_body.
        config = asdict(self._model_config)
        def redact(value):
            if isinstance(value, dict):
                return {key: ("[REDACTED]" if any(token in key.lower().replace('-', '_')
                        for token in ("api_key", "authorization", "password", "secret", "access_token"))
                        and key != "api_key_env" else redact(item))
                        for key, item in value.items()}
            if isinstance(value, list):
                return [redact(item) for item in value]
            return value
        trace = {
            "call_id": call_id, "agent": self.prompt_name,
            "format_retry_count": format_retry_count,
            "provider": self._model_config.provider,
            "model": self._model_config.model,
            "messages": [asdict(message) for message in messages],
            "config": redact(config), "status": "running",
        }
        self.execution_log.append(trace)
        started_at = time.monotonic()
        try:
            response = self._backend.generate(messages=messages, config=self._model_config)
        except Exception as error:
            trace.update({"status": "failed", "error_type": type(error).__name__,
                          "error": str(error),
                          "attempt_count": getattr(error, "attempt_count", 1),
                          "retry_errors": getattr(error, "retry_errors", []),
                          "elapsed_seconds": time.monotonic() - started_at,
                          "usage": {}, "estimated_cost_usd": None})
            if self.trace_sink is not None:
                self.trace_sink(dict(trace))
            raise
        response = replace(response, call_id=call_id)
        raw = response.raw_response
        if hasattr(raw, "model_dump"):
            raw = raw.model_dump(mode="json")
        if not isinstance(raw, (dict, list, str, int, float, bool, type(None))):
            raw = None
        trace.update({
            "status": "completed", "response_text": response.text,
            "refusal": response.refusal, "finish_reason": response.finish_reason,
            "usage": dict(response.usage), "elapsed_seconds": response.elapsed_seconds,
            "estimated_cost_usd": response.estimated_cost_usd,
            "attempt_count": response.attempt_count,
            "retry_errors": list(response.retry_errors),
            "raw_response": redact(raw),
        })
        self._response_traces[response.call_id] = trace
        if self.trace_sink is not None:
            self.trace_sink(dict(trace))
        return response

    def execution_metadata(self, response: LLMResponse) -> dict[str, Any]:
        """Return the reproducibility record shared by every LLM agent."""

        metadata = {
            "agent": self.prompt_name,
            "prompt_contract_version": 1,
            "system_prompt_sha256": hashlib.sha256(
                self._prompt_spec.system_prompt.encode("utf-8")
            ).hexdigest(),
            "user_prompt_template_sha256": hashlib.sha256(
                self._prompt_spec.user_prompt_template.encode("utf-8")
            ).hexdigest(),
            "provider": self._model_config.provider,
            "model": self._model_config.model,
            "temperature": self._model_config.temperature,
            "max_output_tokens": self._model_config.max_output_tokens,
            "timeout_seconds": self._model_config.timeout_seconds,
            "max_retries": self._model_config.max_retries,
            "retry_timeouts_forever": self._model_config.retry_timeouts_forever,
            "finish_reason": response.finish_reason,
            "usage": dict(response.usage),
            "elapsed_seconds": response.elapsed_seconds,
            "estimated_cost_usd": response.estimated_cost_usd,
            "attempt_count": response.attempt_count,
            "retry_errors": list(response.retry_errors),
            "input_character_count": response.input_character_count,
            "message_count": response.message_count,
            "refusal": response.refusal,
        }
        trace = self._response_traces.get(response.call_id)
        if trace is not None:
            metadata.update({"call_id": trace["call_id"], "model_calls": [trace]})
        metadata.update(
            self._format_retry_metadata.get(
                response.call_id,
                {
                    "format_retry_count": 0,
                    "format_retry_errors": [],
                    "original_response_sha256": hashlib.sha256(
                        response.text.encode("utf-8")
                    ).hexdigest(),
                },
            )
        )
        return metadata

    @staticmethod
    def load_prompt_text(path: str | Path) -> str:
        """Read one prompt file from disk."""

        return Path(path).read_text(encoding="utf-8")
