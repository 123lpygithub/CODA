"""Deployment origins must allow configured pages, without opening every origin."""
import os
import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from coda.web.api import create_app


class DeploymentCorsTests(unittest.TestCase):
    def preflight(self, client, origin, method='POST'):
        return client.options('/api/runs', headers={
            'Origin': origin,
            'Access-Control-Request-Method': method,
            'Access-Control-Request-Headers': 'content-type',
        })

    def test_deployed_frontends_can_create_and_delete_without_opening_other_origins(self):
        with patch.dict(os.environ, {'CODA_ALLOWED_ORIGINS': 'https://coda.pages.dev/, https://research.example.org'}):
            client = TestClient(create_app(service=object()))
            for origin in ['https://coda.pages.dev', 'https://research.example.org', 'http://127.0.0.1:5173']:
                for method in ['POST', 'DELETE']:
                    response = self.preflight(client, origin, method)
                    self.assertEqual(response.status_code, 200)
                    self.assertEqual(response.headers['access-control-allow-origin'], origin)
            for origin in ['https://unrelated.pages.dev', 'https://coda.pages.dev.evil.example', 'https://random.example']:
                response = self.preflight(client, origin)
                self.assertEqual(response.status_code, 400)
                self.assertNotIn('access-control-allow-origin', response.headers)

    def test_default_configuration_remains_local(self):
        with patch.dict(os.environ, {'CODA_ALLOWED_ORIGINS': ''}):
            client = TestClient(create_app(service=object()))
            self.assertEqual(self.preflight(client, 'http://localhost:5177').status_code, 200)
            self.assertEqual(self.preflight(client, 'https://coda.pages.dev').status_code, 400)

    def test_invalid_origin_configuration_fails_at_startup(self):
        for value in ['*', 'https://*.pages.dev', 'https://site.example/path', 'https://site.example?q=x', 'https://user:pass@site.example', 'not-a-url']:
            with self.subTest(value=value), patch.dict(os.environ, {'CODA_ALLOWED_ORIGINS': value}):
                with self.assertRaisesRegex(ValueError, 'CODA_ALLOWED_ORIGINS'):
                    create_app(service=object())
