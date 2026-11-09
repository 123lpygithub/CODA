"""The local distribution serves its bundle, never project data or API fallbacks."""
import importlib.util
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from coda.web.api import create_app


class LocalWorkbenchTests(unittest.TestCase):
    def test_bundle_and_api_share_one_address_without_exposing_other_files(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            dist = root / "dist"
            (dist / "assets").mkdir(parents=True)
            (dist / "index.html").write_text('<html>CODA<script src="/assets/app-123.js"></script></html>')
            (dist / "assets" / "app-123.js").write_text('fetch("/api/health")')
            (dist / ".env").write_text("private")
            (root / "private.json").write_text("private")
            if os.name != "nt":
                (dist / "linked.json").symlink_to(root / "private.json")
            client = TestClient(create_app(service=object(), frontend_dist=dist))
            home = client.get("/")
            self.assertEqual(home.status_code, 200)
            self.assertIn("CODA", home.text)
            self.assertEqual(home.headers["cache-control"], "no-cache")
            asset = client.get("/assets/app-123.js")
            self.assertEqual(asset.status_code, 200)
            self.assertIn("immutable", asset.headers["cache-control"])
            self.assertEqual(client.get("/api/health").json(), {"status": "ok"})
            for path in ["/api/missing", "/assets/missing.js", "/.env", "/%2eenv", "/assets/../../private.json", "/linked.json"]:
                with self.subTest(path=path):
                    response = client.get(path)
                    self.assertEqual(response.status_code, 404)
                    self.assertNotIn("private", response.text)
            self.assertEqual(client.post("/api/missing").status_code, 404)
            self.assertEqual(client.get("/docs").status_code, 200)

    def test_missing_build_fails_with_setup_instruction(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(ValueError, "setup_local.py"):
                create_app(service=object(), frontend_dist=directory)

    def test_api_only_mode_still_works(self):
        client = TestClient(create_app(service=object()))
        self.assertEqual(client.get("/").status_code, 404)
        self.assertEqual(client.get("/api/health").status_code, 200)

    def test_env_is_loaded_literally_without_overriding_exports(self):
        scripts = Path(__file__).resolve().parents[1] / "scripts"
        with patch.object(sys, "path", [str(scripts), *sys.path]):
            spec = importlib.util.spec_from_file_location("coda_test_run_local", scripts / "run_local.py")
            launcher = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(launcher)
        with tempfile.TemporaryDirectory() as directory, patch.dict(os.environ, {"CODA_TEST_EXPORT": "existing"}):
            root = Path(directory)
            (root / ".env").write_text('CODA_TEST_EXPORT=from-file\nCODA_TEST_LITERAL="${CODA_TEST_EXPORT} $(not-a-command)"\n')
            launcher.load_local_environment(root)
            self.assertEqual(os.environ["CODA_TEST_EXPORT"], "existing")
            self.assertEqual(os.environ["CODA_TEST_LITERAL"], "${CODA_TEST_EXPORT} $(not-a-command)")
