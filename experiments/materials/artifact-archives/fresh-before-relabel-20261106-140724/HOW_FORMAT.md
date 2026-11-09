# Alignment with HOW's public artifact format

The available local replication archive is `SETaxo-Replication.zip`, downloaded from https://zenodo.org/records/21388470 in the preceding investigation. Its recorded MD5 is `c6eb67c7e17b3e0552b2b8868555c5ce`. This analysis inspects the local archive's example schema and exporter implementation, not its taxonomy labels as coding input. The archive contains example trees; those examples are not represented here as the full experimental raw outputs of HOW.

Format sources inspected:

- `examples/tnt-llm.json` and `examples/climb.json`: node keys `category`, `description`, `layer`, `children`.
- `methods/tnt-llm/src/taxonomy_generator/output.py`: `metadata` plus `results`; each result has `id`, `document`, `summary`, `category`, `category_description`.

`GPT6-1/taxonomy.json` uses those four tree-node keys with a synthetic root at layer 0 and the 13 substantive categories at layer 1. The root is not an additional code. A flat codebook is intentional; no artificial hierarchy is introduced simply to resemble an example tree.

`GPT6-1/results.json` preserves HOW's core fields and adds `categories`, `code_ids`, `source_error_ids`, `status`, and `scope_notes`. Its `document` retains the full task, generated program and reference as a serialized JSON object. No 200-character truncation is used. Because CODA-style qualitative coding allows multiple distinct mechanisms per artifact, `category` is only the first-listed compatibility value, not an independently established primary cause. Use the multi-label fields or `assignments.json` for substantive analysis.

The codebook Markdown/CSV, explicit inclusion/exclusion rules, evidence spans, observation records and diagnostic logs supplement that display format. Matching a file schema does not imply identical taxonomy-generation methods, hierarchy depth, category count or empirical quality.
