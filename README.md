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

## Update an existing installation

This section is only for an existing clone of this repository. It updates the
application code, Python dependencies, and the built frontend; it does not
change the dataset evidence profile described below.

Stop the service, then run:

```bash
git pull --ff-only origin main
python scripts/setup_local.py
python scripts/run_local.py
```

Run these commands from the repository root. Existing `.env` configuration and
local `runs/` are preserved because they are excluded from Git.

## Optional: reproduce the paper dataset evidence

This section is not required to install or use CODA. It is only for reproducing
paper experiments with a particular frozen evidence collection. The evidence
profile selects locally included supplemental SATD source context and Privacy
issue discussions/development material; it does not update the application or
download new evidence.

For a new analysis using the latest recovered evidence bundled in this
repository, set the following in `.env`:

```dotenv
CODA_EVIDENCE_PROFILE=paper-20261106-v10
```

Restart the backend and create a new run after changing the profile. Missing
sources remain explicit evidence gaps. Leave this option unset for normal use
or when reproducing the older frozen study inputs.

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
