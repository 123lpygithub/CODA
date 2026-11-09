"""Print effective web model configuration without making a model request."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from coda.llm import web_model_configurations


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--require-keys", action="store_true",
                        help="Fail if any role's selected credential variable is empty.")
    args = parser.parse_args()
    try:
        configs = web_model_configurations()
    except ValueError as error:
        print(f"Invalid LLM configuration: {error}", file=sys.stderr)
        return 2
    rows = {role: {
        "provider": config.provider, "model": config.model,
        "base_url": config.resolved_base_url(),
        "api_key_env": config.resolved_api_key_env(),
        "api_key_available": config.api_key_available(),
        "json_mode": config.json_mode,
    } for role, config in configs.items()}
    print(json.dumps(rows, ensure_ascii=False, indent=2))
    missing = sorted({config.resolved_api_key_env() for config in configs.values()
                      if not config.api_key_available()})
    if args.require_keys and missing:
        print("Missing API key environment variables: " + ", ".join(missing), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
