# Codebook artifacts

All datasets and runs use the same seven-file package and the same JSON fields,
field types and CSV headers. The common format is based on the GPT6-1 presentation
and is identified as `coda.artifact.v1`. Coding decisions remain specific to each
run; format normalization does not merge, rename or reassign semantic codes.

```text
Artifact/
├── README.md
├── SCHEMA.json
├── FORMAT_VALIDATION.json
├── CodeErrors/
├── SATD/
└── Privacy/
```

Each dataset has six run directories: `GPT6-1`, `GPT6-2`, `deepseek-1`,
`deepseek-2`, `gpt5.6-1` and `gpt5.6-2`. Every run directory contains exactly:

| File | Contents |
|---|---|
| `codebook.md` | Definitions, inclusion/exclusion rules, examples and original scope notes |
| `codebook.json` | Common metadata and code records with complete reverse memberships |
| `codebook.csv` | The same public code fields as the JSON codebook |
| `assignments.json` | One assignment per artifact, including rationale, evidence and qualifications |
| `assignments.csv` | The same public assignment fields in tabular form |
| `taxonomy.json` | Category tree containing every code as a leaf |
| `results.json` | Full supplied documents and their assignments |

## Coverage

| Dataset | Run | Artifacts | Codes | Artifact–code assignments |
|---|---|---:|---:|---:|
| CodeErrors | [GPT6-1](CodeErrors/GPT6-1/codebook.md) | 557 | 17 | 729 |
| CodeErrors | [GPT6-2](CodeErrors/GPT6-2/codebook.md) | 557 | 13 | 706 |
| CodeErrors | [deepseek-1](CodeErrors/deepseek-1/codebook.md) | 557 | 15 | 735 |
| CodeErrors | [deepseek-2](CodeErrors/deepseek-2/codebook.md) | 557 | 28 | 1228 |
| CodeErrors | [gpt5.6-1](CodeErrors/gpt5.6-1/codebook.md) | 557 | 14 | 946 |
| CodeErrors | [gpt5.6-2](CodeErrors/gpt5.6-2/codebook.md) | 557 | 29 | 1254 |
| SATD | [GPT6-1](SATD/GPT6-1/codebook.md) | 856 | 18 | 869 |
| SATD | [GPT6-2](SATD/GPT6-2/codebook.md) | 856 | 18 | 1546 |
| SATD | [deepseek-1](SATD/deepseek-1/codebook.md) | 856 | 18 | 1072 |
| SATD | [deepseek-2](SATD/deepseek-2/codebook.md) | 856 | 30 | 938 |
| SATD | [gpt5.6-1](SATD/gpt5.6-1/codebook.md) | 856 | 14 | 1066 |
| SATD | [gpt5.6-2](SATD/gpt5.6-2/codebook.md) | 856 | 20 | 1580 |
| Privacy | [GPT6-1](Privacy/GPT6-1/codebook.md) | 652 | 18 | 980 |
| Privacy | [GPT6-2](Privacy/GPT6-2/codebook.md) | 652 | 11 | 1877 |
| Privacy | [deepseek-1](Privacy/deepseek-1/codebook.md) | 652 | 11 | 1948 |
| Privacy | [deepseek-2](Privacy/deepseek-2/codebook.md) | 652 | 31 | 2841 |
| Privacy | [gpt5.6-1](Privacy/gpt5.6-1/codebook.md) | 652 | 16 | 1752 |
| Privacy | [gpt5.6-2](Privacy/gpt5.6-2/codebook.md) | 652 | 28 | 3187 |

There are 18 packages, 12,390 artifact records across runs and 25,254 artifact–code
assignments. Each run covers the same dataset size; these are repeated analyses,
not 12,390 distinct source artifacts. Evidence snapshots and record order can
differ across runs. Compare records by `case_id`, not by row position.

## Common schema

The machine-readable contract is [SCHEMA.json](SCHEMA.json). It defines
`codebook`, `assignments`, `results` and `taxonomy` in `definitions`.

- `codebook.json`: `{metadata, codes}`. Code fields are `code_id`, `name`,
  `definition`, `inclusion_criteria`, `exclusion_criteria`, `boundary_examples`,
  `artifact_count`, `supporting_cases`, `representative_evidence`, `extensions`.
- `assignments.json`: an array with `case_id`, `index`, `row`, `code_ids`,
  `code_names`, `status`, `coding_kind`, `rationale`, `observation`, `scope_note`,
  `provisional_concepts`, `provenance`, `evidence`, `read_fields`,
  `external_follow_up`, `extensions`.
- `results.json`: `{metadata, results}`. Each result has `id`, `index`, `row`,
  `document`, `categories`, `code_ids`, `status`, `rationale`, `observation`,
  `scope_note`, `evidence_status`, `extensions`.
- `taxonomy.json`: `category`, `description`, `layer`, `children`; each leaf
  additionally has `code_id`. Original grouping trees remain in codebook
  metadata extensions.

`index` is zero-based and `row` is one-based within a package. IDs are strings.
Inclusion, exclusion, scope and rationale are strings; evidence and representative
evidence are arrays. Each CSV uses the corresponding JSON field order, excluding
`extensions`; arrays and objects are serialized as JSON inside CSV cells.

Run-specific diagnostics, review history, source fields, outcome details and
original field values are retained in `extensions.original_record`. Original
codebook text, method metadata and taxonomy are retained in codebook metadata
extensions. Evidence item fields retain their original coordinates and provenance;
analytical notes remain distinguishable from direct quotations where the source
record makes that distinction.

## Preservation and validation

[FORMAT_VALIDATION.json](FORMAT_VALIDATION.json) records all 18 packages, checksums,
schema and CSV agreement, complete forward/reverse membership, and conversion
equivalence. All original assignment code lists, rationales, evidence and supplied
full documents were checked against the pre-conversion packages. Semantic
definitions and original records are preserved; no classification was rerun.

The pre-conversion packages and displaced process files are retained locally at
`/home/peiyuan/CODA/Artifact/format_unification/original/` and
`/home/peiyuan/CODA/Artifact/format_unification/replaced_packages/`. They are outside
the publication tree. The local conversion and verification script is
`/home/peiyuan/CODA/Artifact/format_unification/unify_packages.py`.

Coverage refers to supplied text. Missing bodies, inaccessible links, images and
attachments remain evidence limitations. In SATD/Privacy GPT6-2, SATD uses 856
released comments; Privacy has 536 complete snapshots, 115 metadata-only records
and one partial snapshot. Mechanical validation establishes presentation and
conversion integrity, not independent semantic accuracy or human double coding.
Run labels identify result versions; they are not verified API model identities.
