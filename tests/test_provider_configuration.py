"""Provider selection, credential isolation, and real SDK wire compatibility."""
from __future__ import annotations

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
import unittest
from unittest.mock import patch

from coda.llm import LLMMessage, LLMModelConfig, OpenAIChatBackend, web_model_configurations
from coda.web.runtime import CodaWebService, build_default_web_bootstrap, build_default_web_orchestrator


class ProviderConfigurationTests(unittest.TestCase):
    def test_existing_rightapi_defaults_and_explicit_provider_model(self):
        with patch.dict(os.environ, {}, clear=True):
            configs = web_model_configurations()
            self.assertEqual(configs['coder_a'].model, 'gpt-6.1-sol')
            self.assertEqual(configs['coder_b'].model, 'gpt-5.6-sol')
            self.assertEqual(configs['coder_a'].resolved_api_key_env(), 'RIGHTAPI_API_KEY')
        with patch.dict(os.environ, {'CODA_LLM_PROVIDER': 'deepseek'}, clear=True):
            with self.assertRaisesRegex(ValueError, 'CODA_LLM_MODEL'):
                web_model_configurations()
        with patch.dict(os.environ, {'CODA_LLM_PROVIDER': 'anthropic'}, clear=True):
            with self.assertRaisesRegex(ValueError, 'Unsupported provider'):
                web_model_configurations()

    def test_role_provider_does_not_inherit_other_provider_credentials_or_url(self):
        env = {'CODA_LLM_PROVIDER': 'custom', 'CODA_LLM_MODEL': 'gateway-model',
               'CODA_LLM_BASE_URL': 'https://gateway.example/v1',
               'CODA_LLM_API_KEY_ENV': 'GATEWAY_KEY',
               'CODA_CODER_A_PROVIDER': 'deepseek', 'CODA_CODER_A_MODEL': 'deepseek-chat',
               'CODA_CODER_A_JSON_MODE': 'false'}
        with patch.dict(os.environ, env, clear=True):
            configs = web_model_configurations()
            coder = configs['coder_a']
            self.assertEqual(coder.provider, 'deepseek')
            self.assertEqual(coder.resolved_api_key_env(), 'DEEPSEEK_API_KEY')
            self.assertEqual(coder.resolved_base_url(), 'https://api.deepseek.com/v1')
            self.assertFalse(coder.json_mode)
            self.assertEqual(configs['coder_b'].model, 'gateway-model')
            self.assertEqual(configs['coder_b'].resolved_api_key_env(), 'GATEWAY_KEY')
            del os.environ['CODA_CODER_A_MODEL']
            with self.assertRaisesRegex(ValueError, 'CODA_CODER_A_MODEL'):
                web_model_configurations()

    def test_web_bootstrap_runtime_and_manifest_use_selected_models_without_secrets(self):
        env = {'CODA_LLM_PROVIDER': 'deepseek', 'CODA_LLM_MODEL': 'deepseek-chat',
               'DEEPSEEK_API_KEY': 'test-deepseek-secret',
               'CODA_CODER_A_PROVIDER': 'qwen', 'CODA_CODER_A_MODEL': 'qwen-plus',
               'DASHSCOPE_API_KEY': 'test-qwen-secret'}
        with patch.dict(os.environ, env, clear=True), tempfile.TemporaryDirectory() as root:
            orchestrator = build_default_web_orchestrator()
            bootstrap = build_default_web_bootstrap(orchestrator)
            self.assertEqual(bootstrap.initial_coder_models,
                             {'initial-coder-a': 'qwen-plus', 'initial-coder-b': 'deepseek-chat'})
            self.assertEqual(orchestrator._coder_agents[0][1].model_config.provider, 'qwen')
            service = CodaWebService(runs_root=root)
            runtime = service.runtime_info()
            self.assertTrue(runtime['api_key_available'])
            self.assertEqual(runtime['coder_models'], ['qwen-plus', 'deepseek-chat'])
            summary = service.create_run(dataset_name='static_analysis_nondeterminism', artifact_limit=2)
            manifest = json.loads(Path(summary['run_manifest']).read_text())
            self.assertEqual(manifest['models']['coder_a']['provider'], 'qwen')
            self.assertEqual(manifest['models']['coder_b']['model'], 'deepseek-chat')
            combined = json.dumps([runtime, manifest])
            self.assertNotIn('test-deepseek-secret', combined)
            self.assertNotIn('test-qwen-secret', combined)
            del os.environ['DASHSCOPE_API_KEY']
            self.assertFalse(service.runtime_info()['api_key_available'])

    def test_all_providers_send_credentials_and_json_to_configured_endpoint(self):
        captured = []
        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *args):
                pass
            def do_POST(self):
                body = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
                captured.append((self.path, self.headers.get('Authorization'), body))
                data = json.dumps({'id':'local-test','object':'chat.completion','created':0,
                    'model':body['model'], 'choices':[{'index':0, 'finish_reason':'stop',
                    'message':{'role':'assistant','content':'{"ok": true}'}}],
                    'usage':{'prompt_tokens':2,'completion_tokens':3,'total_tokens':5}}).encode()
                self.send_response(200)
                self.send_header('Content-Type','application/json')
                self.send_header('Content-Length',str(len(data)))
                self.end_headers()
                self.wfile.write(data)
        server = ThreadingHTTPServer(('127.0.0.1',0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            with patch.dict(os.environ, {'LOCAL_TEST_KEY':'local-only-key'}, clear=True):
                for provider in ['rightapi','openai','deepseek','qwen','gemini','openrouter','custom']:
                    config = LLMModelConfig(model='local-model', provider=provider,
                        api_key_env='LOCAL_TEST_KEY', base_url=f'http://127.0.0.1:{server.server_port}/v1',
                        send_temperature=False, json_mode=provider!='gemini')
                    response = OpenAIChatBackend().generate(
                        messages=[LLMMessage('user','Return JSON')], config=config)
                    self.assertEqual(json.loads(response.text), {'ok':True})
                    path, auth, body = captured[-1]
                    self.assertEqual(path, '/v1/chat/completions')
                    self.assertEqual(auth, 'Bearer local-only-key')
                    self.assertNotIn('temperature', body)
                    expected = 'max_completion_tokens' if provider=='openai' else 'max_tokens'
                    self.assertEqual(body[expected], config.max_output_tokens)
                    self.assertEqual('response_format' in body, provider!='gemini')
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=3)

    def test_preflight_checks_selected_keys_without_printing_values(self):
        env = {**os.environ, 'CODA_LLM_PROVIDER':'deepseek', 'CODA_LLM_MODEL':'deepseek-chat',
               'DEEPSEEK_API_KEY':'preflight-private-key'}
        env = {key:value for key,value in env.items()
               if not key.startswith(('CODA_CODER_', 'CODA_STAGE_', 'CODA_INDUCTION_'))}
        script = str(Path(__file__).resolve().parents[1]/'scripts/check_llm_config.py')
        result = subprocess.run([sys.executable,script,'--require-keys'], env=env,
                                capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertNotIn('preflight-private-key',result.stdout+result.stderr)
        self.assertEqual(json.loads(result.stdout)['coder_a']['model'],'deepseek-chat')
        env.pop('DEEPSEEK_API_KEY')
        result = subprocess.run([sys.executable,script,'--require-keys'], env=env,
                                capture_output=True,text=True,timeout=10)
        self.assertEqual(result.returncode,1)
        self.assertIn('DEEPSEEK_API_KEY',result.stderr)

    def test_custom_endpoint_and_request_options_are_validated(self):
        with patch.dict(os.environ, {'CODA_LLM_PROVIDER':'custom','CODA_LLM_MODEL':'local'}, clear=True):
            with self.assertRaisesRegex(ValueError,'BASE_URL'):
                web_model_configurations()
        with self.assertRaisesRegex(ValueError,'token_limit_parameter'):
            LLMModelConfig(model='test',token_limit_parameter='wrong')
        with patch.dict(os.environ, {'CODA_LLM_SEND_TEMPERATURE':'false',
                                    'CODA_LLM_TOKEN_LIMIT_PARAMETER':'max_completion_tokens'}, clear=True):
            config = LLMModelConfig.from_env()
            self.assertFalse(config.send_temperature)
            self.assertEqual(config.token_limit_parameter,'max_completion_tokens')

    def test_endpoint_and_request_contract_change_cannot_silently_resume_frozen_run(self):
        from coda.agents.base import AgentPromptSpec, BaseLLMAgent
        from coda.web.runtime import WebWorkflowError
        from dataclasses import replace
        with patch.dict(os.environ, {}, clear=True), tempfile.TemporaryDirectory() as root:
            service = CodaWebService(runs_root=root)
            summary = service.create_run(dataset_name='static_analysis_nondeterminism', artifact_limit=2)
            state = service._load_run_state(summary['run_id'])
            config = LLMModelConfig(model='same-model',provider='custom',base_url='https://one.example/v1')
            agent = BaseLLMAgent(prompt_spec=AgentPromptSpec('test','fixed','{value}'),
                                 model_config=config, backend=None)
            service._bind_agent_protocol(state,'provider-check',[('test',agent)])
            for changed in (replace(config,base_url='https://two.example/v1'),
                            replace(config,send_temperature=False)):
                other = BaseLLMAgent(prompt_spec=agent._prompt_spec,model_config=changed,backend=None)
                with self.assertRaisesRegex(WebWorkflowError,'frozen protocol'):
                    service._bind_agent_protocol(state,'provider-check',[('test',other)])
