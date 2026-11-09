All datasets and runs use the same seven-file package and the same JSON fields,
field types and CSV headers. The common format is based on the S3-1 presentation
and is identified as `coda.artifact.v1`. Coding decisions remain specific to each
run; format normalization does not merge, rename or reassign semantic codes.

```text
artifact/
├── README.md
├── CodeErrors/
├── SATD/
└── Privacy/
```

Each dataset has six run directories: `S1-1`, `S1-2`, `S2-1`,
`S2-2`, `S3-1` and `S3-2`. The directory labels are DeepSeek → S1,
GPT-5.6 → S2 and GPT-6 → S3; the suffix retains the original round.
Every run directory contains exactly:

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
| CodeErrors | [S3-1](CodeErrors/S3-1/codebook.md) | 557 | 17 | 729 |
| CodeErrors | [S3-2](CodeErrors/S3-2/codebook.md) | 557 | 13 | 706 |
| CodeErrors | [S1-1](CodeErrors/S1-1/codebook.md) | 557 | 15 | 735 |
| CodeErrors | [S1-2](CodeErrors/S1-2/codebook.md) | 557 | 28 | 1228 |
| CodeErrors | [S2-1](CodeErrors/S2-1/codebook.md) | 557 | 14 | 946 |
| CodeErrors | [S2-2](CodeErrors/S2-2/codebook.md) | 557 | 29 | 1254 |
| SATD | [S3-1](SATD/S3-1/codebook.md) | 856 | 18 | 869 |
| SATD | [S3-2](SATD/S3-2/codebook.md) | 856 | 18 | 1546 |
| SATD | [S1-1](SATD/S1-1/codebook.md) | 856 | 18 | 1072 |
| SATD | [S1-2](SATD/S1-2/codebook.md) | 856 | 30 | 938 |
| SATD | [S2-1](SATD/S2-1/codebook.md) | 856 | 14 | 1066 |
| SATD | [S2-2](SATD/S2-2/codebook.md) | 856 | 20 | 1580 |
| Privacy | [S3-1](Privacy/S3-1/codebook.md) | 652 | 18 | 980 |
| Privacy | [S3-2](Privacy/S3-2/codebook.md) | 652 | 11 | 1877 |
| Privacy | [S1-1](Privacy/S1-1/codebook.md) | 652 | 15 | 2183 |
| Privacy | [S1-2](Privacy/S1-2/codebook.md) | 652 | 31 | 2841 |
| Privacy | [S2-1](Privacy/S2-1/codebook.md) | 652 | 16 | 1752 |
| Privacy | [S2-2](Privacy/S2-2/codebook.md) | 652 | 28 | 3187 |

There are 18 packages, 12,390 artifact records across runs and 25,489 artifact–code
assignments. Each run covers the same dataset size; these are repeated analyses,
not 12,390 distinct source artifacts. Evidence snapshots and record order can
differ across runs. Compare records by `case_id`, not by row position.

Privacy S1-1 includes a documented refinement of its existing analysis: A, C
and E were split into seven assignable subcodes (15 codes in total). Each
new subcode has 54–151 artifacts; parent groups are not counted as codes.
The refinement reviews existing case notes and quotations, with targeted
source checks; it is not a new independent full-corpus reading round.
Current decisions and boundary corrections are recorded in
`assignments.json` under `extensions.refinement_review`.

## Common schema

The JSON structures shared by all packages are described below.

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
