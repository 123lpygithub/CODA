# Run the four fresh analyses

The complete method and scope are specified in [PLAN.md](PLAN.md). Input preparation and offline validation are complete. Model execution has not started: the agent environment and local `.env` had no usable API credential, and the launch attempt stopped before any model request. Four prepared directories are not four completed codebooks.

Use the project's environment with `openai` installed. From the canonical CODA directory, in a terminal where the provider key is already exported:

```bash
python experiments/codebook-construction/_execution/run_codebooks.py --dataset all --run all
```

Defaults: `RIGHTAPI_API_KEY`, `https://www.rightapi.ai/v1`, requested model `gpt-6.1-sol`. Model availability must be confirmed by the provider; no live API validation was possible during preparation. To use another OpenAI-compatible endpoint:

```bash
python experiments/codebook-construction/_execution/run_codebooks.py --dataset all --run all \
  --key-env OPENAI_API_KEY --base-url https://api.openai.com/v1 --model MODEL_ID
```

Keys are read only from the named environment variable and never saved in logs. Do not put the key in the command line or share it in chat. Parameters and actual returned model IDs are retained. The runner uses Chat Completions JSON mode and `max_completion_tokens`; providers must support those parameters. Original dataset text will be sent to the chosen endpoint.

Run one analysis at a time with `--dataset SATD --run GPT6-1`, etc. Four analyses default to sequential execution. This avoids accidental provider overload. Changing prompts, model, input or script configuration after a run starts is rejected; preserve existing outputs and use a new directory for a changed method.

```bash
python experiments/codebook-construction/_execution/run_codebooks.py --preflight
python experiments/codebook-construction/_execution/test_execution.py
```

Input sizes: SATD 856 artifacts and 873,948 source characters; Privacy 652 artifacts and 23,581,652 source characters. This includes complete downloaded linked texts rather than frontend excerpts. Identical sections within a case are stored once with aliases. Commentary timestamps and source limitations are retained. Reading requests per run are 856 and 2,139 respectively; case synthesis, induction, consolidation, assignment and possible repair add further requests. This is a substantial full-corpus analysis, not a single short model request. Actual usage is saved with each response; no unmeasured price or token total is asserted.

Successful calls are cached in that run only. Rerunning the same command after a transient failure resumes validated responses. There are four transport attempts per request, one format/evidence repair and at most three substantive refinement cycles. Failures remain `incomplete`; no fabricated final codebook is produced. There is no unattended background model process currently running.

Final outputs are written only after every artifact has a valid supported assignment and no declared category gap remains: `codebook.md/json/csv`, `assignments.json/csv`, `taxonomy.json`, `results.json`. Observations, candidate revisions and requests/responses remain for audit. Exact quote checks verify traceability, not semantic correctness; these analyses are not human-approved results.

Existing CodeErrors results were moved intact under `Artifact/CodeErrors`. The relocation manifest verifies 687 files byte-for-byte. Their old documented scripts belong to that existing analysis and must not be used to construct the new runs.

Inputs, intermediate results, coverage audits, and execution state live under `experiments/codebook-construction/`. Only the seven final result files per run are exported to `artifact/<dataset>/<run>/`. Legacy CodeErrors scripts and documents are archived for provenance; their historical relative paths are not live output paths.
