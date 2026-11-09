# How Well Do LLMs Generate Taxonomies in the SE Domain?

Replication package for **“How Well Do LLMs Generate Taxonomies in the SE Domain? A Multi-perspective Evaluation Framework,”** accepted at the ASE 2026 Research Papers Track.

- Paper/preprint: <https://arxiv.org/abs/2608.01592>
- Archived package on Zenodo: <https://doi.org/10.5281/zenodo.21388470>
- Artifact status and requested badges: [`STATUS.md`](STATUS.md)
- Hardware, software, runtime, and API requirements: [`REQUIREMENTS.md`](REQUIREMENTS.md)
- Dataset schema, provenance, licensing, and ethics: [`DATA.md`](DATA.md)
- ASE artifact abstract: [`ARTIFACT_ABSTRACT.md`](ARTIFACT_ABSTRACT.md)

The package evaluates TnT-LLM and CLIMB on software-engineering artifacts from four perspectives: taxonomy quality (RQ1), alignment with human-defined taxonomies (RQ2), reliability under independent annotation (RQ3), and runtime/cost (RQ4).

## Getting Started — under 30 minutes

The smoke test is offline, makes no API calls, and validates the artifact layout, bundled dataset counts and schemas, example taxonomy trees, and Python syntax.

### Download and extract the Zenodo archive

Download `SETaxo-Replication.zip` from the Zenodo record linked above, then extract it with a standard archive tool:

```bash
unzip SETaxo-Replication.zip
cd SETaxo-Replication
```

All subsequent commands assume the current directory is the extracted `SETaxo-Replication` directory.

### Option A: prebuilt ARM64 container

Download `SETaxo-Replication-full-linux-arm64.tar.gz` from the same Zenodo record, then load and run it with Docker:

```bash
docker load --input SETaxo-Replication-full-linux-arm64.tar.gz
docker run --rm setaxo-artifact:full
```

The image is also compatible with Podman. Expected final line:

```text
SMOKE TEST PASSED
```

### Option B: build the smoke container

```bash
docker build --target smoke -t setaxo-artifact:smoke .
docker run --rm setaxo-artifact:smoke
```

Podman can be substituted for Docker. Expected final line:

```text
SMOKE TEST PASSED
```

### Option C: local Python

Python 3.11 or newer is sufficient; no packages need to be installed.

```bash
python3 artifact/smoke_test.py
```

Expected final line: `SMOKE TEST PASSED`.

## What the artifact contains

```text
artifact/                  smoke test and reduced/full reproduction scripts
data/dataset/              redistributable converted datasets and taxonomies
data/SLR_for_dataset/      literature-search exports, screening criteria, notebooks
methods/tnt-llm/           adapted TnT-LLM implementation
methods/CLIMB/             adapted CLIMB implementation
evaluation/                RQ1–RQ3 evaluation programs and prompts
examples/                  generated taxonomy examples
```

## Dataset overview

The study uses eight taxonomies from seven papers. “Bundled” indicates that the converted input is redistributed in this source package.

| Dataset | Dataset directory | Items | Layers/top/leaf | Bundled |
|---|---|---:|---:|:---:|
| Static Analysis Nondeterminism | `static_analysis_nondeterminism` | 81 | 1/6/– | yes |
| LLM Code Error (Semantic) | `llm_code_error_semantic` | 687 | 2/7/13 | no |
| LLM Code Error (Syntactic) | `llm_code_error_syntactic` | 687 | 2/7/14 | no |
| Dockerfile Flakiness | `dockerfile_flakiness` | 974 | 2/7/29 | no |
| Quantum Classical Issue | `quantum_classical_issue` | 483 | 4/5/69 | yes |
| Fairness API Issue Topic | `fairness_api_issue_topic` | 1,946 | 2/6/10 | no |
| Common Sense-Violating Bug | `common_sense_violating_bug` | 982 | 2/3/23 | yes |
| C++ OOP-Related Feature | `cpp_oop_related_feature` | 788 | 2/6/17 | yes |

Dataset sources and licenses are documented in `DATA.md` and `LICENSE`. Prompt settings for all eight datasets are retained so that directly obtained source data can be converted to the common schema.

## Full environment

The preferred environment is the `full` Docker target:

```bash
docker build --target full -t setaxo-artifact:full .
docker run --rm setaxo-artifact:full
```

The image installs Python 3.13.5, the pinned dependencies in `requirements.txt`, and the required NLTK resources.

For a native installation:

```bash
python3.13 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m nltk.downloader punkt punkt_tab wordnet omw-1.4 averaged_perceptron_tagger_eng
```

### Automated regression tests

The test suite covers both method pipelines, their API adapters, the evaluation metrics, and the result summarizers. External model calls are replaced with deterministic test doubles, so this command does not consume API credits:

```bash
docker run --rm setaxo-artifact:full \
  python -m unittest discover -s tests -v
```

Expected result: `Ran 24 tests` followed by `OK`.

## Reduced scope — less than one day

The reduced reproduction workflow uses all 81 records from the bundled Static Analysis Nondeterminism dataset. It runs TnT-LLM and CLIMB independently to generate one single-layer taxonomy with each method, evaluates both outputs, and derives result tables while limiting API usage and cost.

| Research question | Included | Reduced-scope workflow |
|---|:---:|---|
| RQ1: Quality | yes | Evaluates the human, TnT-LLM, and CLIMB taxonomies with GPT-5.2 only. |
| RQ2: Alignment | yes | Computes Nodes, CEDS, and category-heading HSR against the bundled human-defined taxonomy. |
| RQ3: Reliability | no | Deliberately not run because item-level annotation requires substantially more LLM calls. The implementation remains covered by offline regression tests. |
| RQ4: Efficiency | yes | Derives runtime and provider-reported generation cost from the two generated result files. |

`OPEN_ROUTER_API_KEY` is used for taxonomy generation and RQ1. `OPENAI_API_KEY` is used for CLIMB embeddings and RQ2 HSR. CEDS may download and cache SciBERT model files.

For a local run, copy the credential template and fill in your own keys. The resulting `.env` file is ignored by Git and must not be added to the archive:

```bash
cp .env.example .env
```

Run locally in the full environment:

```bash
bash artifact/run_lightweight.sh
```

Or pass credentials to the container at runtime:

```bash
docker run --rm \
  --env OPENAI_API_KEY \
  --env OPEN_ROUTER_API_KEY \
  -v "$PWD/methods:/artifact/methods" \
  -v "$PWD/evaluation:/artifact/evaluation" \
  setaxo-artifact:full \
  bash artifact/run_lightweight.sh
```

The reduced scope fixes the generator to `openrouter/mistral-large-2512`, which OpenRouter resolves to `mistralai/mistral-large-2512`, and fixes the RQ1 evaluator to `openai/gpt-5.2`. Mistral Large 3 is one of the five paper generators; using one generator and one evaluator instead of the full model panels is an explicit cost-saving measure. Both methods use the complete 81-record dataset with `--max_layers 1` and at most six categories. Every invocation writes to a new directory, so existing results cannot enter the evaluation.

```text
evaluation/lightweight_reproduction/run_*/
  tnt-llm/results_*.json
  climb/results_*.json
  quality/static_analysis_nondeterminism/
  alignment/alignment_{nodes,ceds,hsr}.csv
  tables/rq{1,2,4}_*.csv
```

Set `SETAXO_LIGHTWEIGHT_OUTPUT_DIR` to place the run directories elsewhere. A successful run ends with:

```text
RQ1 QUALITY: PASSED
RQ2 ALIGNMENT: PASSED
RQ3 RELIABILITY: NOT RUN (excluded from the reduced scope because of API cost)
RQ4 EFFICIENCY: PASSED
REDUCED-SCOPE REPRODUCTION PASSED
```

The workflow reproduces the analysis procedure on the bundled reduced scope; it does not claim to regenerate the paper's aggregate numerical tables. RQ3 is intentionally outside this workflow because its cost scales with the number of items, taxonomies, and evaluator models. Its evaluator and metric implementation are retained for reuse and are exercised with deterministic test doubles by the offline test suite.

## Full scope — paper-scale RQ1–RQ4 reproduction

The full scope runs the main study protocol over all eight datasets. For each dataset it generates taxonomies with both TnT-LLM and CLIMB using all five generator models from the paper:

- `openai/gpt-5.2`
- `google/gemini-3-pro-preview`
- `deepseek/deepseek-v3.2`
- `meta-llama/llama-4-maverick`
- `mistralai/mistral-large-2512`

RQ1 and RQ3 use the paper's three-model evaluation panel: `openai/gpt-5.2`, `google/gemini-3-pro-preview`, and `deepseek/deepseek-v3.2`. RQ2 computes Nodes, CEDS, and HSR over category headings, and RQ4 is derived from the generation metadata. TnT-LLM uses `--batch_size 20`; both methods use the dataset-specific layer/top/leaf constraints in the Dataset overview table.

Four source datasets are not redistributed because they do not state a redistribution license. Obtain those datasets from the sources in `DATA.md` and place the converted JSON files in the documented common layout before starting. The full script checks all required files and exits before making an API call if anything is missing.

The full run is intentionally guarded because it performs many commercial API calls. Review the estimated paper-scale cost, configure provider spending limits, and then run:

```bash
export SETAXO_CONFIRM_FULL_RUN=YES
bash artifact/run_full.sh
```

Set `SETAXO_FULL_OUTPUT_DIR` to move the output root. Each invocation creates a fresh `run_*` directory containing generation results, RQ1 quality results, RQ2 alignment results, RQ3 reliability results, and derived RQ1–RQ4 tables.

The full scope records the exact model identifiers used in the paper. Hosted preview endpoints can be retired; if a paper model is no longer offered, the historical protocol cannot be rerun exactly. Do not silently substitute a newer model, because that would no longer be the paper configuration. The reduced scope is the recommended exercisability route during artifact evaluation.

## License

The authors' original code is MIT-licensed. Adapted methods and bundled datasets retain their source licenses; see [`LICENSE`](LICENSE) for attribution and scope. Data without an explicit redistribution license is not bundled.
