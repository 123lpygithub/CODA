from __future__ import annotations

import asyncio
import os
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Literal, Protocol

from openai import AsyncOpenAI, OpenAI

ChatRole = Literal["system", "user", "assistant"]
ProviderName = Literal["openai", "openrouter", "deepseek", "rightapi", "qwen", "gemini", "custom"]

PROVIDER_DEFAULTS: dict[str, tuple[str, str]] = {
    "openai": ("OPENAI_API_KEY", "https://api.openai.com/v1"),
    "openrouter": ("OPENROUTER_API_KEY", "https://openrouter.ai/api/v1"),
    "deepseek": ("DEEPSEEK_API_KEY", "https://api.deepseek.com/v1"),
    "rightapi": ("RIGHTAPI_API_KEY", "https://www.rightapi.ai/v1"),
    "qwen": ("DASHSCOPE_API_KEY", "https://dashscope.aliyuncs.com/compatible-mode/v1"),
    "gemini": ("GEMINI_API_KEY", "https://generativelanguage.googleapis.com/v1beta/openai/"),
    "custom": ("OPENAI_API_KEY", ""),
}


@dataclass(frozen=True)
class LLMMessage:
    """One chat message passed to the model backend."""

    role: ChatRole
    content: str


@dataclass(frozen=True)
class LLMResponse:
    """Normalized response returned by the model backend."""

    model: str
    text: str
    usage: dict[str, int] = field(default_factory=dict)
    finish_reason: str | None = None
    elapsed_seconds: float | None = None
    estimated_cost_usd: float | None = None
    attempt_count: int = 1
    retry_errors: list[dict[str, str]] = field(default_factory=list)
    input_character_count: int | None = None
    message_count: int | None = None
    # Some OpenAI-compatible providers return a structured refusal on the
    # assistant message instead of ordinary content. Keep it separate from
    # malformed JSON so the agent layer can route it directly to R6.
    refusal: str | None = None
    raw_response: Any | None = None
    # Assigned at the agent boundary for every invocation, including repairs.
    # Object addresses are reusable and cannot identify physical API calls.
    call_id: str | None = None


class LLMBackendError(RuntimeError):
    """Raised after an LLM request exhausts its explicit retry budget."""

    def __init__(self, *, attempt_count: int, retry_errors: list[dict[str, str]]) -> None:
        self.attempt_count = attempt_count
        self.retry_errors = retry_errors
        last = retry_errors[-1] if retry_errors else {"type": "unknown", "message": ""}
        super().__init__(
            f"LLM request failed after {attempt_count} attempt(s): "
            f"{last['type']}: {last['message']}"
        )


class LLMRefusalError(RuntimeError):
    """Raised when the provider explicitly refuses an agent request."""

    def __init__(self, refusal: str) -> None:
        self.refusal = refusal
        super().__init__(f"LLM explicitly refused the request: {refusal[:500]}")


class LLMRequestCancelledError(RuntimeError):
    """Raised when the owning workflow cancels an in-flight request or retry."""


@dataclass(frozen=True)
class LLMModelConfig:
    """Provider-agnostic runtime configuration for one chat model."""

    model: str
    provider: ProviderName = "openai"
    temperature: float = 0.0
    max_output_tokens: int = 1200
    api_key_env: str | None = None
    base_url: str | None = None
    organization: str | None = None
    # Proxy-backed models can need more than a minute for a long structured
    # response. Keep this configurable through CODA_LLM_TIMEOUT_SECONDS.
    timeout_seconds: float = 180.0
    # Four retries plus the initial request give five total attempts.
    max_retries: int = 4
    # Web workflows can wait through transient proxy/model timeouts without
    # discarding checkpointed initialization or automatic-processing work.
    retry_timeouts_forever: bool = False
    input_cost_per_million_tokens: float | None = None
    output_cost_per_million_tokens: float | None = None
    json_mode: bool = True
    send_temperature: bool = True
    token_limit_parameter: str = "auto"
    extra_body: dict[str, Any] = field(default_factory=dict)
    extra_headers: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.provider not in PROVIDER_DEFAULTS:
            raise ValueError(f"Unsupported provider: {self.provider}. Supported: {', '.join(PROVIDER_DEFAULTS)}")
        if not self.model.strip():
            raise ValueError("Model must not be empty.")
        if self.token_limit_parameter not in {"auto", "max_tokens", "max_completion_tokens"}:
            raise ValueError("token_limit_parameter must be auto, max_tokens or max_completion_tokens.")
        if self.timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be positive.")
        if self.max_retries < 0:
            raise ValueError("max_retries cannot be negative.")
        if self.input_cost_per_million_tokens is not None and self.input_cost_per_million_tokens < 0:
            raise ValueError("input token cost cannot be negative.")
        if self.output_cost_per_million_tokens is not None and self.output_cost_per_million_tokens < 0:
            raise ValueError("output token cost cannot be negative.")

    @classmethod
    def from_env(
        cls,
        *,
        default_provider: ProviderName = "rightapi",
        default_model: str = "gpt-5.6-sol",
        default_temperature: float = 0.0,
        default_max_output_tokens: int = 1200,
        default_retry_timeouts_forever: bool = False,
        env_prefix: str | None = None,
    ) -> LLMModelConfig:
        """Build runtime model config from environment variables.

        A role prefix (e.g. CODA_CODER_A) overrides global CODA_LLM values.
        Changing a role's provider does not inherit a different provider's URL,
        key-variable name, or model. Secrets are read only when needed and never
        stored in this serializable dataclass.

        Supported variables:
        - CODA_LLM_PROVIDER / CODA_LLM_MODEL
        - CODA_LLM_TEMPERATURE
        - CODA_LLM_MAX_OUTPUT_TOKENS
        - CODA_LLM_TIMEOUT_SECONDS
        - CODA_LLM_MAX_RETRIES
        - CODA_LLM_RETRY_TIMEOUTS_FOREVER
        - CODA_LLM_INPUT_COST_PER_MILLION
        - CODA_LLM_OUTPUT_COST_PER_MILLION
        - CODA_LLM_BASE_URL
        - CODA_LLM_API_KEY_ENV
        """

        def value(name: str, default: str | None = None, *, inherit: bool = True) -> str | None:
            if env_prefix:
                override = os.getenv(f"{env_prefix}_{name}", "").strip()
                if override:
                    return override
            return (os.getenv(f"CODA_LLM_{name}", "").strip() or default) if inherit else default

        global_provider = os.getenv("CODA_LLM_PROVIDER", default_provider).strip().lower()
        provider = str(value("PROVIDER", default_provider)).lower()
        if provider not in PROVIDER_DEFAULTS:
            raise ValueError(f"Unsupported provider: {provider}. Supported: {', '.join(PROVIDER_DEFAULTS)}")
        same_provider = provider == global_provider
        model = value("MODEL", inherit=same_provider)
        if not model:
            if provider != default_provider:
                name = f"{env_prefix}_MODEL" if env_prefix and not same_provider else "CODA_LLM_MODEL"
                raise ValueError(f"Set {name} to a model available from provider '{provider}'.")
            model = default_model
        temperature = float(value("TEMPERATURE", str(default_temperature)))
        max_output_tokens = int(value("MAX_OUTPUT_TOKENS", str(default_max_output_tokens)))
        timeout_seconds = float(value("TIMEOUT_SECONDS", "180"))
        max_retries = int(value("MAX_RETRIES", "4"))
        retry_timeouts_forever = str(value(
            "RETRY_TIMEOUTS_FOREVER", "true" if default_retry_timeouts_forever else "false"
        )).lower() in {"1", "true", "yes", "on"}
        input_cost = value("INPUT_COST_PER_MILLION", inherit=same_provider)
        output_cost = value("OUTPUT_COST_PER_MILLION", inherit=same_provider)
        json_mode = str(value("JSON_MODE", "true")).lower() not in {
            "0",
            "false",
            "no",
            "off",
        }
        base_url = value("BASE_URL", inherit=same_provider)
        api_key_env = value("API_KEY_ENV", inherit=same_provider)
        if provider == "custom" and not base_url:
            raise ValueError("Custom provider requires CODA_LLM_BASE_URL or the role's BASE_URL.")
        return cls(
            model=model,
            provider=provider,  # type: ignore[arg-type]
            temperature=temperature,
            max_output_tokens=max_output_tokens,
            api_key_env=api_key_env,
            base_url=base_url,
            timeout_seconds=timeout_seconds,
            max_retries=max_retries,
            retry_timeouts_forever=retry_timeouts_forever,
            input_cost_per_million_tokens=float(input_cost) if input_cost else None,
            output_cost_per_million_tokens=float(output_cost) if output_cost else None,
            json_mode=json_mode,
            send_temperature=str(value("SEND_TEMPERATURE", "true")).lower() not in {
                "0", "false", "no", "off"
            },
            token_limit_parameter=str(value("TOKEN_LIMIT_PARAMETER", "auto")),
        )

    def resolved_api_key_env(self) -> str:
        """Return the environment variable used to read the API key."""

        if self.api_key_env:
            return self.api_key_env
        return PROVIDER_DEFAULTS[self.provider][0]

    def resolved_base_url(self) -> str | None:
        """Return the provider-specific base URL if one is needed."""

        if self.base_url:
            return self.base_url
        if self.provider == "rightapi":
            return os.getenv("RIGHTAPI_BASE_URL", "https://www.rightapi.ai/v1")
        return PROVIDER_DEFAULTS[self.provider][1] or None

    def api_key_available(self) -> bool:
        """Inspect credential presence without returning its value."""
        return bool(os.getenv(self.resolved_api_key_env(), "").strip())

    def read_api_key(self) -> str:
        """Read the configured API key from the environment."""

        env_name = self.resolved_api_key_env()
        api_key = os.getenv(env_name, "").strip()
        if not api_key:
            msg = f"Missing API key. Set {env_name} before invoking the model."
            raise RuntimeError(msg)
        return api_key


class ChatBackend(Protocol):
    """Minimal interface required by CODA agents."""

    def generate(
        self,
        *,
        messages: list[LLMMessage],
        config: LLMModelConfig,
    ) -> LLMResponse:
        ...


class OpenAIChatBackend:
    """OpenAI-compatible chat backend shared by all current CODA agents."""

    def __init__(
        self,
        client_factory: Callable[..., Any] | None = None,
    ) -> None:
        self._client_factory = client_factory or OpenAI
        self._uses_default_client = client_factory is None
        self._cancel_requested: Callable[[], bool] | None = None

    def set_cancel_requested(self, callback: Callable[[], bool] | None) -> None:
        """Install a workflow-scoped cancellation probe.

        Default SDK requests use a cancellable async transport. The probe is
        checked during an in-flight request as well as before each retry.
        """

        self._cancel_requested = callback

    def _raise_if_cancelled(self) -> None:
        if self._cancel_requested is not None and self._cancel_requested():
            raise LLMRequestCancelledError("The LLM workflow was cancelled.")

    def _client_options(self, config: LLMModelConfig) -> dict[str, Any]:
        kwargs: dict[str, Any] = {
            "api_key": config.read_api_key(),
            "timeout": config.timeout_seconds,
            # CODA owns the retry loop so every actual attempt is auditable.
            "max_retries": 0,
        }
        base_url = config.resolved_base_url()
        if base_url:
            kwargs["base_url"] = base_url
        if config.organization:
            kwargs["organization"] = config.organization
        return kwargs

    def _build_client(self, config: LLMModelConfig) -> Any:
        return self._client_factory(**self._client_options(config))

    async def _cancellable_completion(
        self, request: dict[str, Any], config: LLMModelConfig,
        cancel_requested: Callable[[], bool],
    ) -> Any:
        # Cancelling the SDK task closes the local HTTP request before the
        # workflow can resume. No detached worker may write a late result.
        async with AsyncOpenAI(**self._client_options(config)) as client:
            task = asyncio.create_task(client.chat.completions.create(**request))
            try:
                while not task.done():
                    if cancel_requested():
                        raise LLMRequestCancelledError("The LLM workflow was cancelled.")
                    await asyncio.wait({task}, timeout=0.1)
                if cancel_requested():
                    raise LLMRequestCancelledError("The LLM workflow was cancelled.")
                return await task
            finally:
                if not task.done():
                    task.cancel()
                # Join transport cleanup before returning control to bootstrap.
                await asyncio.gather(task, return_exceptions=True)

    @staticmethod
    def _is_retryable_timeout(error: Exception) -> bool:
        """Recognize client, transport, and proxy timeout failures."""

        current: BaseException | None = error
        visited: set[int] = set()
        while current is not None and id(current) not in visited:
            visited.add(id(current))
            status_code = getattr(current, "status_code", None)
            if status_code in {408, 504, 524}:
                return True
            error_name = type(current).__name__.lower()
            message = str(current).lower()
            if (
                isinstance(current, TimeoutError)
                or "timeout" in error_name
                or "timed out" in message
                or "error 524" in message
                or "origin_response_timeout" in message
            ):
                return True
            current = current.__cause__ or current.__context__
        return False

    @classmethod
    def _is_retryable_transport_error(cls, error: Exception) -> bool:
        if cls._is_retryable_timeout(error):
            return True
        current: BaseException | None = error
        visited: set[int] = set()
        while current is not None and id(current) not in visited:
            visited.add(id(current))
            if (isinstance(current, ConnectionError)
                    or type(current).__name__ == "APIConnectionError"
                    or getattr(current, "status_code", None) in {502, 503}):
                return True
            current = current.__cause__ or current.__context__
        return False

    def generate(
        self,
        *,
        messages: list[LLMMessage],
        config: LLMModelConfig,
    ) -> LLMResponse:
        self._raise_if_cancelled()
        cancel_requested = self._cancel_requested
        cancellable = self._uses_default_client and cancel_requested is not None
        client = None if cancellable else self._build_client(config)
        request: dict[str, Any] = {
            "model": config.model,
            "messages": [
                {"role": message.role, "content": message.content}
                for message in messages
            ],
        }
        if config.send_temperature:
            request["temperature"] = config.temperature
        if config.max_output_tokens > 0:
            token_parameter = config.token_limit_parameter
            if token_parameter == "auto":
                token_parameter = "max_completion_tokens" if config.provider == "openai" else "max_tokens"
            request[token_parameter] = config.max_output_tokens
        if config.json_mode:
            # All current CODA agents return JSON objects. This prevents prose
            # or markdown wrappers; field-level validation remains below.
            request["response_format"] = {"type": "json_object"}
        if config.extra_body:
            request["extra_body"] = dict(config.extra_body)
        if config.extra_headers:
            request["extra_headers"] = dict(config.extra_headers)

        started_at = time.monotonic()
        retry_errors: list[dict[str, str]] = []
        response = None
        attempt_count = 0
        try:
            while True:
                self._raise_if_cancelled()
                attempt_count += 1
                try:
                    if cancellable:
                        response = asyncio.run(self._cancellable_completion(request, config, cancel_requested))
                    else:
                        response = client.chat.completions.create(**request)
                    self._raise_if_cancelled()
                    break
                except Exception as error:
                    if isinstance(error, LLMRequestCancelledError):
                        raise
                    retry_errors.append(
                        {
                            "attempt": str(attempt_count),
                            "type": type(error).__name__,
                            "message": str(error)[:500],
                        }
                    )
                    # Avoid unbounded memory growth during a long provider outage;
                    # attempt_count still records the complete number of attempts.
                    if len(retry_errors) > 100:
                        retry_errors.pop(0)
                    if (
                        config.retry_timeouts_forever
                        and self._is_retryable_transport_error(error)
                    ):
                        # Provider transport failures are operational retries,
                        # not repeated semantic judgments or format repairs.
                        self._raise_if_cancelled()
                        continue
                    if attempt_count > config.max_retries:
                        raise LLMBackendError(
                            attempt_count=attempt_count,
                            retry_errors=retry_errors,
                        ) from error
                    # Other transient failures retain the finite retry budget.
        finally:
            if client is not None and callable(getattr(client, "close", None)):
                client.close()
        if response is None:  # Defensive guard; the loop either returns or raises.
            raise LLMBackendError(
                attempt_count=attempt_count,
                retry_errors=retry_errors,
            )
        elapsed_seconds = time.monotonic() - started_at
        choice = response.choices[0]
        usage = getattr(response, "usage", None)
        usage_dict = {
            "prompt_tokens": int(getattr(usage, "prompt_tokens", 0) or 0),
            "completion_tokens": int(getattr(usage, "completion_tokens", 0) or 0),
            "total_tokens": int(getattr(usage, "total_tokens", 0) or 0),
        }
        message = choice.message
        refusal_value = getattr(message, "refusal", None)
        refusal = str(refusal_value).strip() if refusal_value else None
        text = getattr(message, "content", None) or ""
        estimated_cost_usd = None
        if (
            config.input_cost_per_million_tokens is not None
            and config.output_cost_per_million_tokens is not None
        ):
            estimated_cost_usd = (
                usage_dict["prompt_tokens"]
                * config.input_cost_per_million_tokens
                + usage_dict["completion_tokens"]
                * config.output_cost_per_million_tokens
            ) / 1_000_000
        return LLMResponse(
            model=config.model,
            text=text,
            usage=usage_dict,
            finish_reason=getattr(choice, "finish_reason", None),
            elapsed_seconds=elapsed_seconds,
            estimated_cost_usd=estimated_cost_usd,
            attempt_count=attempt_count,
            retry_errors=retry_errors,
            input_character_count=sum(len(message.content) for message in messages),
            message_count=len(messages),
            refusal=refusal,
            raw_response=response,
        )


def load_chat_backend(config: LLMModelConfig) -> ChatBackend:
    """Return the backend implementation for the given provider."""

    if config.provider in PROVIDER_DEFAULTS:
        return OpenAIChatBackend()
    msg = f"Unsupported provider: {config.provider}"
    raise ValueError(msg)


def web_model_configurations() -> dict[str, LLMModelConfig]:
    """Resolve the same role settings for execution, startup checks and manifests."""
    roles = {
        "context_comparison_iterative_validation": ("CODA_STAGE", "gpt-5.6-sol", 1200),
        "induction_and_bootstrap_validation": ("CODA_INDUCTION", "gpt-5.6-sol", 2600),
        "coder_a": ("CODA_CODER_A", "gpt-6.1-sol", 1600),
        "coder_b": ("CODA_CODER_B", "gpt-5.6-sol", 1600),
    }
    return {role: LLMModelConfig.from_env(
        default_model=model, default_max_output_tokens=tokens,
        default_retry_timeouts_forever=True, env_prefix=prefix,
    ) for role, (prefix, model, tokens) in roles.items()}
