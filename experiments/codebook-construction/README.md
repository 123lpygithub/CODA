# Dataset codebooks

| Dataset | First result | Second result | Status |
|---|---|---|---|
| Code errors | [CodeErrors/GPT6-1](CodeErrors/GPT6-1/codebook.md) | [CodeErrors/GPT6-2](CodeErrors/GPT6-2/codebook.md) | Existing completed analyses; relocated without content changes |
| ML SATD | `SATD/GPT6-1/` | `SATD/GPT6-2/` | Inputs and execution prepared; no model analysis completed |
| Privacy | `Privacy/GPT6-1/` | `Privacy/GPT6-2/` | Inputs and execution prepared; no model analysis completed |

See [the execution plan](_execution/PLAN.md) and [running instructions](_execution/README.md).

Each dataset owns its own input and run directories. Do not interpret the directory names as verified model identifiers or the two runs as independent human coders. Existing CodeErrors outputs preserve their original methods and caveats. New SATD/Privacy runs use separate stateless API calls and caches and never read another run's taxonomy.
