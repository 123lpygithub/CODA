# Codebook artifacts

Codebooks and artifact-level coding results are organized by dataset and run.

```text
Artifact/
├── README.md
├── CodeErrors/
│   ├── GPT6-1/
│   ├── GPT6-2/
│   ├── gpt5.6-1/
│   ├── gpt5.6-2/
│   └── deepseek-2/
├── SATD/
│   ├── GPT6-1/
│   ├── GPT6-2/
│   ├── gpt5.6-1/
│   ├── gpt5.6-2/
│   └── deepseek-2/
├── Privacy/
│   ├── GPT6-1/
│   ├── GPT6-2/
│   ├── gpt5.6-1/
│   ├── gpt5.6-2/
│   └── deepseek-2/
```

| Dataset / run | Artifacts covered | Codes | Artifact–code assignments |
|---|---:|---:|---:|
| CodeErrors / GPT6-1 | 557 / 557 | 17 | See existing result package |
| CodeErrors / GPT6-2 | 557 / 557 | 13 | See existing result package |
| CodeErrors / gpt5.6-1 | 557 / 557 | 14 | 946 |
| CodeErrors / gpt5.6-2 | 557 / 557 | 29 | 1254 |
| SATD / GPT6-1 | 856 / 856 | 18 | 869 |
| SATD / GPT6-2 | 856 / 856 | 18 | 1546 |
| SATD / gpt5.6-1 | 856 / 856 | 14 | 1066 |
| SATD / gpt5.6-2 | 856 / 856 | 20 | 1580 |
| Privacy / GPT6-1 | 652 / 652 | 18 | 980 |
| Privacy / GPT6-2 | 652 / 652 | 11 | 1877 |
| Privacy / gpt5.6-1 | 652 / 652 | 16 | 1752 |
| Privacy / gpt5.6-2 | 652 / 652 | 28 | 3187 |
| CodeErrors / deepseek-2 | 557 / 557 | 28 | 1228 |
| SATD / deepseek-2 | 856 / 856 | 30 | 938 |
| Privacy / deepseek-2 | 652 / 652 | 31 | 2841 |

SATD and Privacy GPT6-1 contain the completed reconstruction from individual readings of every artifact's supplied textual sections. Exact duplicate supplementary content was read once with source mappings; long CSS and dependency metadata used reversible representations. Classifications were individually authored, without keyword classification or external model API calls. Multiple codes are assigned when distinct concerns are supported. CodeErrors packages are preserved unchanged.

| File | Contents |
|---|---|
| `codebook.md` | Readable definitions, inclusion/exclusion criteria and examples |
| `codebook.json` | Structured codebook, supporting case IDs, counts and method metadata |
| `codebook.csv` | Tabular codebook |
| `assignments.json` | Every artifact's codes, reasoning, quotations, provenance and qualifications |
| `assignments.csv` | Tabular coding records |
| `taxonomy.json` | HOW-style category tree: `category`, `description`, `layer`, `children` |
| `results.json` | Supplied textual documents and their assigned categories |

All supplied artifacts have nonempty assignments. This does not mean every reported defect is confirmed: evidence-limited, disputed, retracted or explanatory material remains explicitly qualified. Coverage concerns the supplied text; inaccessible links, uninspected images, revision uncertainty and lack of runtime verification remain documented. Mechanical integrity checks do not constitute independent semantic or human validation. GPT6-1 identifies the requested result version, not a verified API model identity or a blinded independent replicate.

## deepseek-2

The `deepseek-2` run publishes three complete codebooks in the same seven-file presentation contract as GPT6-1: `codebook.md/json/csv`, `assignments.json/csv`, `taxonomy.json`, and `results.json`. All 2,065 artifacts were read individually and assigned; the process packages, per-artifact reading memos, frozen inputs and validation report are kept in `Artifact/deepseek-2/`.

- [CodeErrors / deepseek-2](CodeErrors/deepseek-2/codebook.md)
- [SATD / deepseek-2](SATD/deepseek-2/codebook.md)
- [Privacy / deepseek-2](Privacy/deepseek-2/codebook.md)

CodeErrors uses 28 failure-mechanism codes in four navigation groups. SATD uses 30 debt/evidence-state codes. Privacy uses 27 privacy-theme codes plus four evidence-state codes, with at least one theme and exactly one state per artifact. Privacy has 11 artifacts with two complete review records; the later review is published and all review variants are retained in `assignments.json` under `review_history`. See `Artifact/deepseek-2/FSE_DEEPSEEK2_VALIDATION.json` for the mechanical audit.

## gpt5.6-1

The `gpt5.6-1` run is published alongside the existing GPT6 runs using the same seven-file presentation contract as GPT6-1: `codebook.md/json/csv`, `assignments.json/csv`, `taxonomy.json`, and `results.json`. Its three packages preserve the completed source-blind rereading and manual coding decisions for all 2,065 artifacts; the schema conversion did not reclassify any artifact. The conversion and equivalence audit are recorded in `Artifact/gpt5.6-1/FSE_GPT56_VALIDATION.json` at the repository workspace root.

- [CodeErrors / gpt5.6-1](CodeErrors/gpt5.6-1/codebook.md)
- [SATD / gpt5.6-1](SATD/gpt5.6-1/codebook.md)
- [Privacy / gpt5.6-1](Privacy/gpt5.6-1/codebook.md)

Reading notes, reconstruction maps, source materials, audits and prior-package backups remain outside `Artifact`. See [the reconstruction plan](../experiments/codebook-construction/full-reading-restart/PLAN.md) and [package validation](../experiments/codebook-construction/full-reading-restart/final_package_validation.json). SATD and Privacy also include the requested result 2 in `GPT6-2/`; its format and evidence limits are documented below.

## SATD and Privacy: result 2 (GPT6-2)

The requested result 2 is published here:

- [SATD codebook](SATD/GPT6-2/CODEBOOK.md) and [all 856 artifact analyses](SATD/GPT6-2/ARTIFACTS.md).
- [Privacy codebook](Privacy/GPT6-2/CODEBOOK.md) and [all 652 artifact analyses](Privacy/GPT6-2/ARTIFACTS.md).

These packages were copied byte-for-byte from the completed `Artifact/SATD/2/` and `Artifact/Privacy/2/` outputs in the repository root. For this result 2, use the FSE paths above as the delivery location. Existing GPT6-1 and CodeErrors results are preserved.

Each GPT6-2 package includes `CODEBOOK.md`, `codebook.json`, `ARTIFACTS.md`, `assignments.jsonl`, the frozen `artifacts.jsonl`, individual reading memos, explicit memberships, `METHOD.md`, and coverage/hash reports. The file-format table above describes the earlier packages; GPT6-2 uses these filenames. Classifications are authored semantic decisions; scripts serialize and check them rather than classify by keywords.

Reading coverage is all locally available artifact text: SATD has 856 released comments; Privacy has 536 complete current snapshots, 115 metadata-only records, and one partial snapshot. Missing bodies, external pages, images and attachments are not claimed as read. This is single-AI coding without independent double coding; mechanical checks do not establish semantic accuracy or equivalence to the original paper's codebook. The run label denotes result 2, not a verified model identity or independent replicate.
