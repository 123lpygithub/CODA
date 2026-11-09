# Full-reading reconstruction

Status: completed and published as GPT6-1 for SATD (856 artifacts, 18 categories, 869 assignments) and Privacy (652 artifacts, 18 categories, 980 assignments). Previous packages are archived outside Artifact; CodeErrors is unchanged.

## Scope and method

- Reconstruct SATD and Privacy from the prepared source corpora, without consulting existing codebooks, assignments, or published human categories.
- Read every supplied textual section, including source-context alternatives, chronology notes, linked material and external material. Read long sections in consecutive, non-overlapping pages. Exact duplicate text may be read once with explicit cross-references; near duplicates are not treated as identical.
- Record inaccessible sources, referenced images requiring visual inspection, and any truncated or unavailable source content as outstanding evidence limitations. Downloading or displaying text does not by itself establish reading completion.
- Author a case-specific interpretation, provisional concepts, quotations, technical/contextual qualifications and unresolved questions after reading. No keyword classifier or programmatic category inference.
- Consolidate concepts only after reading; document merges and retained distinctions. Recheck every assignment against the resulting definitions. Evidence-insufficient material must remain explicit rather than be assigned a fabricated defect.
- Scripts may paginate input, record hashes, package authored analysis and check integrity. They must not manufacture interpretation, read-status attestations, or assignments.

## Work list

1. [x] Inspect source schema and volume; establish a separate reconstruction workspace.
2. [x] Read all 856 SATD artifacts and all their supplied sections; author individual notes.
3. [x] Read all 652 Privacy artifacts and all their supplied sections; author individual notes.
4. [x] Follow up evidence-dependent questions where possible; record inspected visual evidence and explicitly qualify uninspected or unavailable items.
5. [x] Induce each codebook from the new observations, documenting category boundaries and consolidation.
6. [x] Reassess all artifacts against final definitions; inspect counterexamples and overlapping categories.
7. [x] Validate coverage and evidence links; publish new result packages with an honest completeness statement.

## Continuation

`read_source.py DATASET START STOP` displays whole records in the half-open index range. Its optional `--offset` and `--length` paginate a single rendered record without elision. It does not mark records read or assign categories.

`SATD/reading_notes.jsonl` and `Privacy/reading_notes.jsonl` contain assistant-authored observations from this reconstruction only. A record is complete only when every supplied section has been read; source availability and semantic certainty remain separate.

This is a reconstruction in the same conversation, not a claim of a blinded independent model run. Previously encountered concepts cannot literally be erased from model context; existing result files are excluded as analytical inputs.

All seven steps are complete within the supplied-text scope. Unverified external content is an evidence limitation retained in individual records, not a claim of verified source completeness. Package checks are recorded in `final_package_validation.json`; publication locations and backups are in each dataset's `publication.json`.
