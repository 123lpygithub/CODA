# SATD — deepseek-1 method and delivery format

This directory contains the deepseek-1 codebook and per-artifact decisions serialized in the GPT6-1 delivery layout. The format conversion does not reclassify or replace the analyst's decisions.

## Files

- `codebook.json` — metadata, code definitions, inclusion/exclusion boundaries, supporting cases, and representative evidence.
- `codebook.csv` — tabular view of the same code definitions.
- `codebook.md` — human-readable codebook.
- `taxonomy.json` — hierarchical view of the codebook.
- `assignments.json` — one record per artifact with code IDs, rationale, provenance, and verbatim evidence.
- `assignments.csv` — tabular assignment view.
- `results.json` — metadata plus the source document and assigned categories for every artifact.
- `artifacts.jsonl` — frozen source text used for evidence verification.

## Method

Each artifact was read in full, including title, metadata, body, and all locally available discussion. Decisions were recorded as open codes, an analytic memo, an outcome, and exact evidence quotes. The open codes were then consolidated into the final codebook by explicit comparison; the codebook was not produced by keyword matching.

An artifact may carry multiple codes only when the material supports multiple independently evidenced mechanisms. A closed issue, a label, a merged PR, or a participant's legal claim is not treated as proof of implementation, verification, or compliance.

## Evidence and limits

- Every `assignments.json` evidence quote was checked against `artifacts.jsonl` using character offsets.
- The `results.json` document is the frozen source text; the codebook and assignments remain the authoritative coding record.
- External links, images, videos, attachments, and linked PRs that were not retrieved are not counted as read.
- This is a single-AI-analyst reconstruction. There is no independent human double coding or inter-coder agreement statistic. Structural checks do not establish interpretive uniqueness, legal correctness, or runtime verification.
