"""Run the built workbench and API as one local service, loading .env."""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import subprocess
import sys

from setup_local import REPO_ROOT, environment_python


def load_local_environment(root: Path = REPO_ROOT) -> None:
    from dotenv import load_dotenv

    # Explicit shell exports take priority; treat key values literally.
    load_dotenv(root / ".env", override=False, interpolate=False)


def main() -> int:
    python = environment_python()
    if not python.is_file():
        print("Run python scripts/setup_local.py first.", file=sys.stderr)
        return 1
    # Use the project environment without requiring shell-specific activation commands.
    if Path(sys.prefix).absolute() != (REPO_ROOT / ".venv").absolute():
        command = [str(python), str(Path(__file__).resolve()), *sys.argv[1:]]
        if os.name != "nt":
            os.execv(str(python), command)
        child = subprocess.Popen(command)
        try:
            return child.wait()
        except KeyboardInterrupt:
            # The console has already delivered Ctrl+C to the child as well.
            return child.wait()
    os.chdir(REPO_ROOT)
    sys.path.insert(0, str(REPO_ROOT))
    try:
        load_local_environment()
    except ImportError:
        print("Dependencies are incomplete; rerun python scripts/setup_local.py.", file=sys.stderr)
        return 1
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=None)
    parser.add_argument("--runs-root", default=None)
    parser.add_argument("--check", action="store_true", help="Check local configuration without starting or calling models.")
    args = parser.parse_args()
    try:
        port = args.port if args.port is not None else int(os.environ.get("CODA_API_PORT", "8003"))
        if not 1 <= port <= 65535:
            raise ValueError("CODA_API_PORT / --port must be between 1 and 65535.")
    except ValueError:
        print("CODA_API_PORT / --port must be an integer between 1 and 65535.", file=sys.stderr)
        return 1
    frontend_dist = REPO_ROOT / "frontend" / "dist"
    if not (frontend_dist / "index.html").is_file():
        print("Built frontend missing; run python scripts/setup_local.py first.", file=sys.stderr)
        return 1
    result = subprocess.run([sys.executable, "scripts/check_llm_config.py", "--require-keys"], cwd=REPO_ROOT)
    if result.returncode:
        print("Edit .env or export the missing model settings, then retry.", file=sys.stderr)
        return result.returncode
    if args.check:
        print("Local configuration and frontend are ready. No model request was made.")
        return 0
    import uvicorn
    from coda.web.api import create_app
    from coda.web.runtime import CodaWebService

    runs_root = args.runs_root or os.environ.get("CODA_RUNS_ROOT", "runs/web")
    service = CodaWebService(runs_root=runs_root)
    print(f"\nOpen http://127.0.0.1:{port} — press Ctrl+C to stop.", flush=True)
    uvicorn.run(create_app(service, frontend_dist=frontend_dist), host="127.0.0.1", port=port)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
