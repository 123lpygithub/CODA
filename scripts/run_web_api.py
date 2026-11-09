from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import uvicorn

from coda.web.api import create_app
from coda.web.runtime import CodaWebService


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the local CODA Web API.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--runs-root", default="runs/web")
    parser.add_argument("--frontend-dist", help="Optionally serve a built frontend from this directory.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    service = CodaWebService(runs_root=args.runs_root)
    uvicorn.run(create_app(service, frontend_dist=args.frontend_dist), host=args.host, port=args.port)


if __name__ == "__main__":
    main()
