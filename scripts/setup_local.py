"""Install local dependencies and build the single-address CODA workbench."""
from __future__ import annotations

import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import venv

REPO_ROOT = Path(__file__).resolve().parents[1]


def environment_python(root: Path = REPO_ROOT) -> Path:
    return root / ".venv" / ("Scripts/python.exe" if os.name == "nt" else "bin/python")


def main() -> int:
    if sys.version_info < (3, 10):
        print("Python 3.10 or newer is required.", file=sys.stderr)
        return 1
    node = shutil.which("node")
    npm = shutil.which("npm.cmd" if os.name == "nt" else "npm")
    if not node or not npm:
        print("Install Node.js 22.12+ and npm, then rerun this command.", file=sys.stderr)
        return 1
    version = subprocess.check_output([node, "--version"], text=True).strip()
    match = re.fullmatch(r"v(\d+)\.(\d+)\.(\d+)", version)
    if not match or tuple(map(int, match.groups())) < (22, 12, 0):
        print(f"Node.js 22.12+ is required; found {version}.", file=sys.stderr)
        return 1
    python = environment_python()
    if not python.is_file():
        print("Creating .venv ...", flush=True)
        venv.EnvBuilder(with_pip=True).create(REPO_ROOT / ".venv")
    subprocess.run([str(python), "-m", "pip", "install", "-r", "requirements.txt"], cwd=REPO_ROOT, check=True)
    subprocess.run([npm, "ci"], cwd=REPO_ROOT / "frontend", check=True)
    # Local bundles always use the API served from the same local address.
    build_env = dict(os.environ, VITE_API_BASE_URL="")
    subprocess.run([npm, "run", "build"], cwd=REPO_ROOT / "frontend", env=build_env, check=True)
    config = REPO_ROOT / ".env"
    if not config.exists():
        # Exclusive creation also prevents overwriting a configuration created during setup.
        with config.open("x", encoding="utf-8") as output:
            output.write((REPO_ROOT / ".env.example").read_text(encoding="utf-8"))
        if os.name != "nt":
            config.chmod(0o600)
    print("\nSetup complete. Edit .env with your provider, model and API key.")
    print("Then run: python scripts/run_local.py")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except subprocess.CalledProcessError as error:
        print(f"Setup failed (exit {error.returncode}); fix the error above and rerun setup.", file=sys.stderr)
        raise SystemExit(error.returncode)
    except KeyboardInterrupt:
        raise SystemExit(130)
