# CODA

A local workbench for iterative inductive coding with LLM agents and human review.

## Requirements

- Python 3.10+
- Node.js 22.12+ and npm (for installation and rebuilding the frontend)
- An API key for a supported model provider

Use `python3` instead of `python` if required by your system.

## Install

```bash
git clone https://github.com/123lpygithub/CODA.git
cd CODA
python scripts/setup_local.py
```

The setup script creates `.venv`, installs dependencies, builds the frontend,
and creates `.env` if it does not already exist. Run the following commands
from this `CODA/` directory.

## Configure

Edit `.env` with your provider, model, and API key. For the default RightAPI setup:

```dotenv
CODA_LLM_PROVIDER=rightapi
RIGHTAPI_API_KEY=your-api-key
```

For another provider, set its model ID and corresponding key, for example:

```dotenv
CODA_LLM_PROVIDER=deepseek
CODA_LLM_MODEL=deepseek-chat
DEEPSEEK_API_KEY=your-api-key
```

See [.env.example](.env.example) for additional options. The launcher loads `.env`
automatically; existing shell environment variables take priority. Restart after
changing configuration. Keep API keys in `.env` or the backend environment.

## Run

```bash
python scripts/run_local.py
```

Open **http://127.0.0.1:8003**. The same service provides the frontend and API;
no separate frontend process or virtual-environment activation is needed.
Create a run, initialize it, and follow the workflow and review controls.
Progress is saved in `runs/web/` and can be resumed after restarting.
Pause active work before stopping the service with `Ctrl+C`.

To check configuration without calling a model:

```bash
python scripts/run_local.py --check
```

If port 8003 is occupied, run `python scripts/run_local.py --port 8004`
and open http://127.0.0.1:8004 instead.
