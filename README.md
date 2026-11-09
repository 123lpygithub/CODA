# CODA

A local workbench for iterative inductive coding with LLM agents and human review.

## Requirements

- Python 3.10+
- Node.js 22.12+ and npm (for installation and rebuilding the frontend)
- An API key for a supported model provider

Use `python3` instead of `python` if required by your system.

## Install

```bash
git clone https://github.com/linli1724647576/FSE27-CODA.git
cd FSE27-CODA/CODA
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

## Update

Stop the service, then run:

```bash
git pull --ff-only
python scripts/setup_local.py
python scripts/run_local.py
```

Existing `.env` and `runs/` are preserved and excluded from Git.

## Paper dataset evidence

For a new analysis with recovered SATD source context and supplemental Privacy
discussions and linked development material, set
`CODA_EVIDENCE_PROFILE=paper-20261106-v10` in `.env`. Restart the backend and create a
new run. Missing sources remain explicit evidence gaps. Leave this option unset
when reproducing the older frozen study inputs.

The latest coverage and remaining limitations are recorded in
[the v10 evidence report](experiments/materials/DATA_RECOVERY_V10_20261106.md).

See [dataset evidence and collection commands](experiments/materials/DATASET_ALIGNMENT.md)
for coverage, resumable collectors and the matching study manifests.

Verify the current frozen paper inputs without calling a model:

```bash
python scripts/prepare_paper_experiment.py --bundle experiments/materials/evidence-20261106-v10
```

For matched calibration/formal runs, human-review requirements and monitoring
commands, see [the experiment run guide](experiments/materials/PAPER_EXPERIMENT_RUN_GUIDE.md).
