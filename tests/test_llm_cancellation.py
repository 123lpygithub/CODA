"""Cancellation must close an in-flight provider request before bootstrap resumes."""
from __future__ import annotations

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
import socket
import threading
import time
import unittest
from unittest.mock import patch

from coda.llm import LLMMessage, LLMModelConfig, LLMRequestCancelledError, OpenAIChatBackend


class InflightCancellationTests(unittest.TestCase):
    def run_slow_provider(self, *, timeout_first: bool) -> None:
        started = threading.Event()
        disconnected = threading.Event()
        release = threading.Event()
        cancelled = threading.Event()
        requests: list[dict] = []

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *_):
                pass

            def do_POST(self):
                requests.append(json.loads(self.rfile.read(int(self.headers['Content-Length']))))
                if timeout_first and len(requests) == 1:
                    body = b'{"error":{"message":"gateway timed out"}}'
                    self.send_response(504)
                elif not release.is_set():
                    started.set()
                    # Observe the actual TCP close while the provider has sent
                    # neither response headers nor body. No fake SDK cancellation.
                    self.connection.settimeout(5)
                    try:
                        if self.connection.recv(1) == b'':
                            disconnected.set()
                    except (ConnectionResetError, BrokenPipeError):
                        disconnected.set()
                    except socket.timeout:
                        pass
                    return
                else:
                    body = json.dumps({
                        'id': 'resumed', 'object': 'chat.completion', 'created': 0,
                        'model': 'local', 'choices': [{'index': 0,
                            'finish_reason': 'stop',
                            'message': {'role': 'assistant', 'content': '{"resumed":true}'}}],
                    }).encode()
                    self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Content-Length', str(len(body)))
                self.end_headers()
                self.wfile.write(body)

        server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        server.daemon_threads = True
        server_thread = threading.Thread(target=server.serve_forever, daemon=True)
        server_thread.start()
        results: list[object] = []
        backend = OpenAIChatBackend()
        backend.set_cancel_requested(cancelled.is_set)
        config = LLMModelConfig(model='local', provider='custom',
            base_url=f'http://127.0.0.1:{server.server_port}/v1',
            api_key_env='CODA_CANCELLATION_TEST_KEY', timeout_seconds=180,
            retry_timeouts_forever=True)

        def generate():
            try:
                results.append(backend.generate(messages=[LLMMessage('user', 'test')], config=config))
            except Exception as error:
                results.append(error)

        try:
            with patch.dict(os.environ, {'CODA_CANCELLATION_TEST_KEY': 'local-test-only'}):
                worker = threading.Thread(target=generate, daemon=True)
                worker.start()
                self.assertTrue(started.wait(5), 'Provider request did not start')
                stop_time = time.monotonic()
                cancelled.set()
                worker.join(2)
                self.assertFalse(worker.is_alive(), 'Stop waited for the 180-second timeout')
                self.assertLess(time.monotonic() - stop_time, 2)
                self.assertEqual(len(results), 1)
                self.assertIsInstance(results[0], LLMRequestCancelledError)
                self.assertTrue(disconnected.wait(2), 'Cancelled request left its socket open')
                expected_attempts = 2 if timeout_first else 1
                self.assertEqual(len(requests), expected_attempts, 'Cancellation initiated another retry')
                # A new bootstrap invocation can reuse the backend after cancellation
                # without an older request remaining alive to write a late result.
                release.set()
                cancelled.clear()
                response = backend.generate(messages=[LLMMessage('user', 'resume')], config=config)
                self.assertEqual(json.loads(response.text), {'resumed': True})
                self.assertEqual(response.attempt_count, 1)
        finally:
            cancelled.set()
            release.set()
            server.shutdown()
            server.server_close()
            server_thread.join(2)

    def test_stop_closes_request_without_waiting_for_provider_timeout(self):
        self.run_slow_provider(timeout_first=False)

    def test_stop_interrupts_a_request_after_an_unlimited_transport_retry(self):
        self.run_slow_provider(timeout_first=True)

    def test_cancelled_workflow_does_not_open_provider_request(self):
        backend = OpenAIChatBackend()
        backend.set_cancel_requested(lambda: True)
        with self.assertRaises(LLMRequestCancelledError):
            backend.generate(messages=[LLMMessage('user', 'cancelled')],
                config=LLMModelConfig(model='unused', provider='custom', base_url='http://127.0.0.1:1'))


if __name__ == '__main__':
    unittest.main()
