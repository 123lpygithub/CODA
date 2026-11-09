from __future__ import annotations

import unittest

from coda.agents.base import AgentExecutionError, AgentPromptSpec, BaseLLMAgent
from coda.llm import LLMModelConfig, LLMResponse


class ScriptedBackend:
    def __init__(self, responses: list[str]) -> None:
        self.responses = list(responses)
        self.messages = []

    def generate(self, *, messages, config):
        del config
        self.messages.append(messages)
        return LLMResponse(model="test", text=self.responses.pop(0))


class TestAgentFormatRetry(unittest.TestCase):
    def _agent(self, backend: ScriptedBackend) -> BaseLLMAgent:
        return BaseLLMAgent(
            prompt_spec=AgentPromptSpec(
                name="test_agent",
                system_prompt="Return JSON.",
                user_prompt_template="Input: {value}",
            ),
            model_config=LLMModelConfig(model="test", provider="custom"),
            backend=backend,
        )

    def test_malformed_json_receives_one_format_only_retry(self) -> None:
        backend = ScriptedBackend(["not-json", '{"status":"valid"}'])
        agent = self._agent(backend)

        result = agent.invoke_validated_json_object(
            lambda payload, response: {
                "status": payload["status"],
                "metadata": agent.execution_metadata(response),
            },
            value="sample",
        )

        self.assertEqual(result["status"], "valid")
        self.assertEqual(result["metadata"]["format_retry_count"], 1)
        self.assertEqual(len(result["metadata"]["format_retry_errors"]), 1)
        self.assertIn("FORMAT REPAIR ONLY", backend.messages[1][-1].content)

    def test_invalid_enum_receives_one_schema_repair(self) -> None:
        backend = ScriptedBackend(
            ['{"status":"translated-valid"}', '{"status":"valid"}']
        )
        agent = self._agent(backend)

        def parser(payload, response):
            if payload.get("status") != "valid":
                raise AgentExecutionError("status must be exactly 'valid'.")
            return agent.execution_metadata(response)

        metadata = agent.invoke_validated_json_object(parser, value="sample")

        self.assertEqual(metadata["format_retry_count"], 1)
        self.assertIn("status must be exactly", metadata["format_retry_errors"][0])


if __name__ == "__main__":
    unittest.main()
