import os
import unittest
from types import SimpleNamespace

from coda.agents import AgentExecutionError, AgentPromptSpec, BaseLLMAgent
from coda.llm import (
    LLMMessage,
    LLMModelConfig,
    LLMRequestCancelledError,
    LLMResponse,
    OpenAIChatBackend,
)
from coda.parsing import extract_json_array, extract_json_object, require_fields


class FakeBackend:
    def __init__(self, text: str) -> None:
        self._text = text
        self.messages = []

    def generate(self, *, messages, config):
        self.messages.append(messages)
        return LLMResponse(model=config.model, text=self._text)


class ParsingTests(unittest.TestCase):
    def test_extract_json_object_from_fenced_text(self):
        text = '```json\n{"summary": "x", "items": [1, 2]}\n```'
        payload = extract_json_object(text)
        self.assertEqual(payload, {"summary": "x", "items": [1, 2]})

    def test_extract_json_array_from_free_text(self):
        text = 'Result:\n[{"title": "A"}, {"title": "B"}]\nDone.'
        payload = extract_json_array(text)
        self.assertEqual(payload, [{"title": "A"}, {"title": "B"}])

    def test_require_fields_raises_when_missing(self):
        with self.assertRaises(ValueError):
            require_fields({"a": 1}, required_fields=["a", "b"])


class LLMLayerTests(unittest.TestCase):
    def test_openai_backend_stops_infinite_timeout_retries_when_cancelled(self):
        class Completions:
            def __init__(self):
                self.calls = 0

            def create(self, **_):
                self.calls += 1
                raise TimeoutError("provider timed out")

        completions = Completions()
        client = SimpleNamespace(chat=SimpleNamespace(completions=completions))
        backend = OpenAIChatBackend(client_factory=lambda **_: client)
        backend.set_cancel_requested(lambda: completions.calls >= 1)
        original = os.environ.get("CODA_RETRY_TEST_KEY")
        os.environ["CODA_RETRY_TEST_KEY"] = "test-key"
        try:
            with self.assertRaises(LLMRequestCancelledError):
                backend.generate(
                    messages=[LLMMessage(role="user", content="test")],
                    config=LLMModelConfig(
                        model="fake",
                        provider="custom",
                        api_key_env="CODA_RETRY_TEST_KEY",
                        retry_timeouts_forever=True,
                    ),
                )
        finally:
            if original is None:
                os.environ.pop("CODA_RETRY_TEST_KEY", None)
            else:
                os.environ["CODA_RETRY_TEST_KEY"] = original

        self.assertEqual(completions.calls, 1)

    def test_openai_backend_records_explicit_retry_attempts(self):
        class Completions:
            def __init__(self):
                self.calls = 0

            def create(self, **request):
                del request
                self.calls += 1
                if self.calls < 3:
                    raise TimeoutError(f"timeout-{self.calls}")
                return SimpleNamespace(
                    choices=[
                        SimpleNamespace(
                            message=SimpleNamespace(content='{"ok": true}'),
                            finish_reason="stop",
                        )
                    ],
                    usage=SimpleNamespace(
                        prompt_tokens=3,
                        completion_tokens=2,
                        total_tokens=5,
                    ),
                )

        completions = Completions()
        client = SimpleNamespace(
            chat=SimpleNamespace(completions=completions)
        )
        original = os.environ.get("CODA_RETRY_TEST_KEY")
        os.environ["CODA_RETRY_TEST_KEY"] = "test-key"
        try:
            backend = OpenAIChatBackend(client_factory=lambda **_: client)
            response = backend.generate(
                messages=[LLMMessage(role="user", content="test")],
                config=LLMModelConfig(
                    model="fake",
                    provider="custom",
                    api_key_env="CODA_RETRY_TEST_KEY",
                    max_retries=2,
                ),
            )
        finally:
            if original is None:
                os.environ.pop("CODA_RETRY_TEST_KEY", None)
            else:
                os.environ["CODA_RETRY_TEST_KEY"] = original

        self.assertEqual(response.attempt_count, 3)
        self.assertEqual(
            [error["message"] for error in response.retry_errors],
            ["timeout-1", "timeout-2"],
        )
        self.assertEqual(response.usage["total_tokens"], 5)

    def test_openai_backend_retries_timeouts_without_attempt_limit(self):
        class Completions:
            def __init__(self):
                self.calls = 0

            def create(self, **request):
                del request
                self.calls += 1
                if self.calls < 5:
                    raise TimeoutError(f"timeout-{self.calls}")
                return SimpleNamespace(
                    choices=[
                        SimpleNamespace(
                            message=SimpleNamespace(content='{"ok": true}'),
                            finish_reason="stop",
                        )
                    ],
                    usage=SimpleNamespace(
                        prompt_tokens=1,
                        completion_tokens=1,
                        total_tokens=2,
                    ),
                )

        completions = Completions()
        client = SimpleNamespace(chat=SimpleNamespace(completions=completions))
        original = os.environ.get("CODA_RETRY_TEST_KEY")
        os.environ["CODA_RETRY_TEST_KEY"] = "test-key"
        try:
            response = OpenAIChatBackend(
                client_factory=lambda **_: client
            ).generate(
                messages=[LLMMessage(role="user", content="test")],
                config=LLMModelConfig(
                    model="fake",
                    provider="custom",
                    api_key_env="CODA_RETRY_TEST_KEY",
                    max_retries=0,
                    retry_timeouts_forever=True,
                ),
            )
        finally:
            if original is None:
                os.environ.pop("CODA_RETRY_TEST_KEY", None)
            else:
                os.environ["CODA_RETRY_TEST_KEY"] = original

        self.assertEqual(response.attempt_count, 5)
        self.assertEqual(len(response.retry_errors), 4)

    def test_timeout_detection_includes_cloudflare_524(self):
        error = RuntimeError("Error 524: origin_response_timeout")
        self.assertTrue(OpenAIChatBackend._is_retryable_timeout(error))
        self.assertFalse(
            OpenAIChatBackend._is_retryable_timeout(
                RuntimeError("invalid authentication credentials")
            )
        )

    def test_model_config_resolves_provider_defaults(self):
        config = LLMModelConfig(model="gpt-test", provider="openrouter")
        self.assertEqual(config.resolved_api_key_env(), "OPENROUTER_API_KEY")
        self.assertEqual(config.resolved_base_url(), "https://openrouter.ai/api/v1")

    def test_model_config_resolves_rightapi_defaults(self):
        config = LLMModelConfig(model="gpt-test", provider="rightapi")
        self.assertEqual(config.resolved_api_key_env(), "RIGHTAPI_API_KEY")
        self.assertEqual(
            config.resolved_base_url(),
            "https://www.rightapi.ai/v1",
        )

    def test_model_config_from_env_uses_coda_runtime_defaults(self):
        original = {
            "CODA_LLM_TEMPERATURE": os.environ.get("CODA_LLM_TEMPERATURE"),
            "CODA_LLM_MAX_OUTPUT_TOKENS": os.environ.get("CODA_LLM_MAX_OUTPUT_TOKENS"),
            "CODA_LLM_TIMEOUT_SECONDS": os.environ.get("CODA_LLM_TIMEOUT_SECONDS"),
            "CODA_LLM_MAX_RETRIES": os.environ.get("CODA_LLM_MAX_RETRIES"),
            "CODA_LLM_RETRY_TIMEOUTS_FOREVER": os.environ.get(
                "CODA_LLM_RETRY_TIMEOUTS_FOREVER"
            ),
            "CODA_LLM_BASE_URL": os.environ.get("CODA_LLM_BASE_URL"),
            "CODA_LLM_API_KEY_ENV": os.environ.get("CODA_LLM_API_KEY_ENV"),
        }
        os.environ["CODA_LLM_TEMPERATURE"] = "0.2"
        os.environ["CODA_LLM_MAX_OUTPUT_TOKENS"] = "321"
        os.environ["CODA_LLM_TIMEOUT_SECONDS"] = "12"
        os.environ["CODA_LLM_MAX_RETRIES"] = "4"
        os.environ["CODA_LLM_RETRY_TIMEOUTS_FOREVER"] = "true"
        os.environ["CODA_LLM_BASE_URL"] = "https://example.test/v1"
        os.environ["CODA_LLM_API_KEY_ENV"] = "SPECIAL_KEY"
        try:
            config = LLMModelConfig.from_env()
        finally:
            for key, value in original.items():
                if value is None:
                    os.environ.pop(key, None)
                else:
                    os.environ[key] = value

        self.assertEqual(config.provider, "rightapi")
        self.assertEqual(config.model, "gpt-5.6-sol")
        self.assertEqual(config.temperature, 0.2)
        self.assertEqual(config.max_output_tokens, 321)
        self.assertEqual(config.timeout_seconds, 12.0)
        self.assertEqual(config.max_retries, 4)
        self.assertTrue(config.retry_timeouts_forever)
        self.assertEqual(config.base_url, "https://example.test/v1")
        self.assertEqual(config.api_key_env, "SPECIAL_KEY")

    def test_read_api_key_raises_when_missing(self):
        config = LLMModelConfig(
            model="gpt-test",
            provider="custom",
            api_key_env="CODA_FAKE_API_KEY",
        )
        original = os.environ.pop("CODA_FAKE_API_KEY", None)
        try:
            with self.assertRaises(RuntimeError):
                config.read_api_key()
        finally:
            if original is not None:
                os.environ["CODA_FAKE_API_KEY"] = original


class BaseAgentTests(unittest.TestCase):
    def test_base_agent_parses_json_object(self):
        agent = BaseLLMAgent(
            prompt_spec=AgentPromptSpec(
                name="context",
                system_prompt="You are a coder.",
                user_prompt_template="Artifact: {artifact}",
            ),
            model_config=LLMModelConfig(model="dummy", provider="custom"),
            backend=FakeBackend('{"context_brief": "ok"}'),
        )
        payload = agent.invoke_json_object(artifact="demo")
        self.assertEqual(payload["context_brief"], "ok")

        metadata = agent.execution_metadata(
            LLMResponse(model="dummy", text='{"context_brief": "ok"}')
        )
        self.assertEqual(metadata["prompt_contract_version"], 1)
        self.assertEqual(len(metadata["system_prompt_sha256"]), 64)
        self.assertEqual(len(metadata["user_prompt_template_sha256"]), 64)

    def test_base_agent_repeats_output_language_in_user_prompt(self):
        backend = FakeBackend('{"context_brief": "ok"}')
        agent = BaseLLMAgent(
            prompt_spec=AgentPromptSpec(
                name="context",
                system_prompt="You are a context agent.",
                user_prompt_template="Artifact: {artifact}",
            ),
            model_config=LLMModelConfig(model="dummy", provider="custom"),
            backend=backend,
        )

        agent.set_output_language("zh")
        agent.invoke_json_object(artifact="demo")
        system_prompt, user_prompt = backend.messages[-1]
        self.assertIn("请使用中文回答", system_prompt.content)
        self.assertIn("请使用中文回答", user_prompt.content)
        self.assertIn("JSON 字段名必须严格保持", user_prompt.content)
        self.assertIn("relationship_to_codebook must be exactly one of", user_prompt.content)

        agent.set_output_language("en")
        agent.invoke_json_object(artifact="demo")
        _system_prompt, user_prompt = backend.messages[-1]
        self.assertIn("Answer in English", user_prompt.content)

    def test_base_agent_reports_missing_prompt_variable(self):
        agent = BaseLLMAgent(
            prompt_spec=AgentPromptSpec(
                name="context",
                system_prompt="You are a coder.",
                user_prompt_template="Artifact: {artifact}",
            ),
            model_config=LLMModelConfig(model="dummy", provider="custom"),
            backend=FakeBackend('{"context_brief": "ok"}'),
        )
        with self.assertRaises(AgentExecutionError):
            agent.invoke_text()


if __name__ == "__main__":
    unittest.main()
