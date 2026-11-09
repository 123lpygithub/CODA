# Dataset evidence and paper alignment

**Current collection:** `paper-20261105-recovered`, frozen inputs
[`evidence-20261105-v8`](evidence-20261105-v8/).
See [the latest recovery report](DATA_RECOVERY_CONTINUATION_20261105.md):
18 deleted-file references, tracker comments and official Jira imports recovered.
v7 remains the preceding reproducible input version.
Use the [experiment run guide](PAPER_EXPERIMENT_RUN_GUIDE.md) for preflight,
matched run creation and monitoring. The dated sections below retain the earlier
recovery history; v3, v5 and v6 are prior collections.

For a primary-source investigation of the original studies, release contents,
remaining retrieval limitations and the next recovery steps, see
[Original studies and data recovery](ORIGINAL_STUDIES_DATA_RECOVERY.md).

The paper dataset descriptions are retained. This implementation supplements the
released evidence; it does not alter published labels or regenerate results.
Code errors is outside this supplementation task.

## ML SATD: fixed-revision source context

The released sample has 856 comments. For each case, the collector uses the
released repository, file path and **comment-introducing commit**, not the current
branch. It retrieves the file once per URL and caches its original UTF-8 source,
retrieval timestamp and SHA-256. Comments sharing a file share that cache.

The CSV renders multiline comments with ` || ` and transforms some punctuation
and escaping. The matcher normalizes comma/semicolon, escaped quotes/slashes,
leading Python comment markers, whitespace and blank lines. It requires the
**whole normalized comment** to have one matching span. Inline comments are
matched using Python comment tokens. It does not use keyword or fuzzy matching.
When matched, it preserves the original source lines with 12 surrounding lines,
file path, introducing commit, source URL, line range and checksums.

Short repeated comments, changed/missing comments, inaccessible commits and
deleted repositories remain explicit gaps. The collector never substitutes the
removal commit or current branch. Introducing-revision context is local evidence,
not proof of the developer's intent, and may need additional researcher context.
The upstream release and its intermediate-processing artifacts are documented at
https://github.com/DavidMOBrien/23Shades and https://doi.org/10.5281/zenodo.7033365.
The CSV is sufficient for fixed-revision retrieval; upstream multi-gigabyte Boa
outputs are not required for this collector.

## Privacy: discussions and linked development material

All 652 confirmed issues remain in the corpus, including unavailable cases.
Issue bodies and paginated issue comments are retrieved using the GitHub REST API.
For incomplete cases, the supplemental web collector can read GitHub's embedded
**original Markdown**, rather than converting displayed HTML to evidence. It
checks canonical issue identity, comment counts and timeline pagination. A page
with omitted comments remains partial. Old complete snapshots are preserved;
a poorer partial response never replaces a richer snapshot.

Linked material is stored separately and bound to the exact parent snapshot hash.
The collector follows one-hop explicit GitHub URLs from issue bodies/comments:

- source files, retaining cited line ranges and surrounding context;
- commit patches;
- PR patches and API metadata when available;
- linked issues and available discussion comments.

It does not infer issue links from arbitrary `#number` tokens, recursively crawl
linked discussions, or download external attachments. Branch-based file links are
resolved to a commit when possible; otherwise they are explicitly marked as
retrieval-time branch references. PR patches without metadata do not establish
merge, deployment or issue resolution. Very large sources remain complete on
disk, while agent input clearly marks an excerpt and asks for context when omitted
material is necessary. Checksummed local evidence fields and SourceRefs let
Context, Coder, Comparison and Validation agents cite the retrieved content.
No collection occurs while an agent codes a case.

A complete **issue** snapshot means its body/comment discussion is complete at
retrieval; it does not imply that all linked evidence is available. Linked status
is recorded separately. Retrieval-time evidence cannot recreate the original
study's historical snapshot. Missing evidence is never generated from reference
labels, titles, closed status or comment counts.

## Evidence profiles and reproducibility

The default profile preserves original agent inputs for historical runs. For a
new analysis set this option in `.env`, restart and create a new run:

```dotenv
CODA_EVIDENCE_PROFILE=paper-20261105
```

A profile identifies the local evidence collection. Frozen study manifests also
verify exact per-case evidence hashes, so changing a collection invalidates reuse
of its previous experimental inputs. Preserve old manifests and exact companion
`agent_inputs.json` files. Old results must not be attributed to enriched inputs.
The legacy allocation remains 557 Code errors cases (113/444), 856 SATD cases
(169/687) and 652 Privacy cases (132/520). These are existing calibration/formal
case allocations, not a new claim about the manuscript's calibration protocol.

## Collection commands

Run from `CODA/`. Optional `GITHUB_TOKEN` or `GH_TOKEN` increases GitHub REST quota.
Keep tokens outside Git. Each collector saves caches and progress for resumption.
Unavailable documents require a later retry or researcher-provided source; they
are not silently removed. GitHub may throttle requests or return 404/410.

```bash
python scripts/prepare_satd_source_context.py \
  --output dataset/ml_satd_23_shades/source/code_context_20261105

python scripts/prepare_privacy_issue_discussions.py \
  --output dataset/personal_data_protection_github/source/github_snapshot_20261105

python scripts/prepare_privacy_web_evidence.py \
  --output dataset/personal_data_protection_github/source/github_snapshot_20261105

# Run after the parent issue collection has finished.
python scripts/prepare_privacy_linked_artifacts.py
```

After evidence changes, create a **new** frozen version (never overwrite one):

```bash
python scripts/refresh_study_evidence.py \
  --source-manifest experiments/materials/coda-calibration20-20261102-v1.json \
  --output experiments/materials/evidence-next-version \
  --study-id coda-evidence-next-version \
  --evidence-profile paper-20261105
```

The refreshed manifest preserves case IDs, repository/task groups, phases and
order. The companion stores exact agent inputs and an audit of changed hashes.
No LLM output or human evaluation score is regenerated by evidence preparation.

The older `eligible-2026-10-13/eligible_cases_audit.json` is historical. An updated
legacy audit is in `eligible-20261105-legacy-evidence/`. Existing evidence v1 is
retained; subsequent supplements use a new version.

## Collected coverage (2026-11-05)

| Evidence layer | Available / complete | Partial / unmatched | Unavailable | Pending |
| --- | ---: | ---: | ---: | ---: |
| SATD source context (856 cases) | 814 | 22 unmatched | 20 (HTTP 404) | 0 |
| Privacy body + discussion (652 cases) | 609 | 27 partial | 16 (HTTP 404) | 0 |
| Privacy explicit case–link records | 246 | 17 partial | 259 | 0 |

Privacy has 517 distinct supported explicit URLs, with 522 case–link records
because a source can be cited by several cases. These counts refer to retrieved
evidence, not completed coding/evaluation. Complete issue discussion and available
linked material are separate claims. Source failures include unavailable GitHub
resources, API quota limits, transport failures and unsupported page payloads.
Rerun the collectors to retry failures; no case is removed from the corpus.

The final frozen input set for this collection is
`evidence-20261105-v3/study_manifest.json`, with exact inputs in
`evidence-20261105-v3/agent_inputs.json` and checksums in its evidence audit.
v1 and v2 remain prior snapshots. Use v3 for the present collection.

Verification: 279 backend tests pass. Original manifest verification passes,
and revised manifests retain the exact case allocation while changing evidence
hashes. Paper dataset wording is unchanged, and the compiled PDF is synchronized
to the FSE directory and the outer workspace. No experimental outputs were rerun.

## Expanded archival recovery (2026-11-05)

Use `CODA_EVIDENCE_PROFILE=paper-20261105-expanded` to reproduce this collection.
The previous `paper-20261105` directories and v1–v3 inputs remain unchanged.
The latest frozen inputs are `evidence-20261105-v5/`, with exact agent inputs,
case allocation and checksums. v4 retains the intermediate expanded snapshot.

| Evidence | Before expansion | After expansion |
| --- | --- | --- |
| SATD usable source context | 814 / 856 | **849 / 856** |
| Privacy complete current discussions | 609 / 652 | **635 / 652** |
| Privacy issues with no body/discussion evidence | 16 | **0** |
| Privacy historical-only cases | 0 | **16** |
| Linked case–source records | 246 available, 17 partial, 259 unavailable | **262 available, 8 partial, 274 unavailable** |

The new discussion content yields 539 distinct linked URLs and 544 case–link
records. This is a larger discovered set; failures should not be compared using
raw counts alone. The parent issue and its linked-source completeness are separate.

SATD recovery uses Software Heritage revision hashes identical to the released Git
commits. File content is checked against its Git blob SHA-1 and archive SHA-256.
All 20 previously inaccessible source files were recovered. Full-comment matches
on unique added diff spans resolve some repeated comments. Five published
introducing-commit pointers delete the target comment: the verified direct parent
is used only when exactly one parent contains a unique full match. The adapter
explicitly reports this revision correction rather than calling it introducing
context. Seven cases remain unresolved (repeated comments or inconsistent
text/revision pointers); they are listed in the coverage JSON.

Privacy pages now use `?timeline_page=N`. The collector merges original Markdown
by comment ID, remaps author IDs consistently across pages, and checks counts,
end-of-pagination and unchanged issue metadata. The remaining current partial is
`AzuraCast/AzuraCast#2303`: both REST and the page expose 3 comments while reporting
4. Five historical comments are preserved in a separate archive supplement,
without pretending they are the present discussion.

For the 16 inaccessible issues, original issue-body and available comment text
were recovered from GH Archive's public event history via ClickHouse. These are
**historical, partial evidence**, not complete current discussions. Wappalyzer's
old repository name `AliasIO/Wappalyzer` is used only after exact opening title,
number and timestamp match the release. Historical supplements remain distinct
from current bodies/comments, with query, retrieval time and checksum provenance.
Hidden manual coding fields are never used to reconstruct text.

Additional collection commands:

```bash
python scripts/prepare_privacy_web_evidence.py \
  --output dataset/personal_data_protection_github/source/github_snapshot_20261105_expanded
python scripts/recover_privacy_event_archive.py \
  --output dataset/personal_data_protection_github/source/github_snapshot_20261105_expanded
python scripts/recover_satd_archived_context.py \
  --output dataset/ml_satd_23_shades/source/code_context_20261105_expanded
python scripts/prepare_privacy_linked_artifacts.py \
  --snapshots dataset/personal_data_protection_github/source/github_snapshot_20261105_expanded \
  --output dataset/personal_data_protection_github/source/linked_artifacts_20261105_expanded
```

See `evidence-20261105-expanded-coverage.json` for case-level unresolved items and
revision corrections. These scripts prepare evidence only; no experiments were
rerun and no paper findings were changed.

Expanded validation: 284 tests pass; the original v3 profile and expanded v5
profile both verify against their corresponding frozen manifests.

## Continued recovery and remaining gaps (2026-11-05)

The latest collection uses `CODA_EVIDENCE_PROFILE=paper-20261105-continued`.
Its frozen inputs are in `evidence-20261105-v6/`. Earlier collections and frozen
inputs remain reproducible and are not overwritten. Exact current coverage and
case/URL-level gaps are in `evidence-20261105-continued-coverage.json`.

| Evidence | Expanded v5 | Continued v6 |
| --- | ---: | ---: |
| SATD uniquely located source contexts | 849 | 849 |
| SATD cases with all exact candidate locations, explicitly ambiguous | 0 | 4 |
| SATD comments without matching contexts | 7 | 3 |
| Privacy complete current discussions | 635 | 635 |
| Privacy partial discussions | 17 | 17 |
| Linked case–source records: available | 262 | 430 |
| Linked case–source records: partial | 8 | 17 |
| Linked case–source records: unavailable | 274 | 95 |
| Linked case–source records: pending | 0 | 0 |

The linked collection has 537 distinct URLs and 542 case–source records. Two
creation-form URLs are excluded after correcting discovery, and a quoted issue
URL is normalized without its trailing quote. Distinct URLs comprise 426
available, 16 partial and 95 unavailable resources. Fifteen partial URLs contain
historical GH Archive issue evidence; one contains a partial current discussion.
A URL cited by several cases contributes several case–source records.

**SATD remaining limitations.** Four cases retain every full-comment candidate at
the exact published revision: `23shades-0006-aaahbghib` (2 locations),
`23shades-0046-aafchcgjg` (2), `23shades-0256-aagcicecj` (5), and
`23shades-0647-aaidbfgae` (2). The adapter exposes separate citable candidate
fields and an explicit ambiguity note. It does not select a location or report
these cases as uniquely located. Complete-evidence sensitivity sampling excludes
this new ambiguous status. The three unmatched cases are Catalyst
`23shades-0027-aajfegaca`, Paysage `23shades-0654-aagbifedh`, and Lightning
`23shades-0725-aahicjieh`. Published text and revision are inconsistent; a similar
shorter comment is insufficient. File-history probes did not resolve these cases;
raw GitHub connection failures and Software Heritage HTTP 429 also limited the
search. Failed access is not proof that a historical version does not exist.

**Privacy remaining limitations.** Sixteen main cases retain historical-only
body/comment evidence. The AzuraCast case still reports four comments but exposes
three current comments; its historical appendix remains separate. All 652 cases
have body evidence, but only 635 have verified complete current discussions.
The 95 unavailable linked resources comprise 78 files and 17 issues. Reasons
include deleted/private resources, absent old branch paths, transfer/PR page
identity requiring further verification, transport failures and rate limiting.
The 17 partial case–source records are usable with their explicit evidence scope,
not complete replacements. Missing linked files cannot be reconstructed from an
issue's title, closure status or reference labels.

The linked collector now falls back to GH Archive for an explicitly cited issue
when API and structured page retrieval fail. It requires original issue-body
events for that exact repository and issue number. Returned evidence always
remains partial, with event-query provenance and an explicit historical scope.
Complete current responses take priority over historical supplements.

To audit the collection offline:

```bash
CODA_EVIDENCE_PROFILE=paper-20261105-continued \
python scripts/audit_dataset_evidence.py --output /tmp/coda-evidence-coverage.json
```

To retry collection, use the earlier commands with directory suffix
`20261105_continued`. Finish parent discussion collection before rematerializing
linked evidence. Any further evidence changes require a new frozen version;
never attribute old experiment outputs to changed inputs. Preserve v6 and its
exact `agent_inputs.json` even if collection directories receive future retries.

Validation: 290 backend tests pass. v3, v5 and v6 verify against their respective
evidence profiles. Code errors inputs, published labels and manuscript source
were not changed by this continuation. No LLM coding or scoring experiment was
rerun.

## Experiment-ready collection v7 (2026-11-05)

The `paper-20261105-ready` profile adds evidence without overwriting v6. Exact
case IDs, source groups, phase assignments and ordering are unchanged. Current
paper Table `datasetsplit` uses 113/444 Code errors, 169/687 SATD and 132/520 Privacy
calibration/formal cases. Two replicates under each of S1/S2/S3 yield 18 runs per
phase, 36 total. These are the current manuscript's allocations.

| Evidence layer | Available / complete | Limited | Unavailable |
| --- | ---: | ---: | ---: |
| SATD contexts, 856 cases | 849 uniquely located | 4 ambiguous; 3 related-history partial | 0 |
| Privacy main discussions, 652 cases | 635 current complete | 16 historical-only; 1 current partial | 0 |
| GitHub case–link records, 542 | 435 | 13 partial | 94 |
| Selected external case–link records, 151 | 45 | 25 partial | 81 |

All 856 SATD cases have viewable excerpts; uniquely located is not synonymous
with the published introducing revision: five of the 849 use a verified direct
parent and retain an explicit correction. Three formerly unmatched comments now
have unique matches at verified ancestor, related-branch and descendant commits.
Those three are `historical_partial`, never exact case-time context. Four repeated
comments retain all exact candidate locations and are not arbitrarily located.

All 652 Privacy cases have retrieved body evidence, including seven whose public
body is empty. An empty retrieved body is not a retrieval failure. Two of those
seven also have no comments; titles/metadata alone cannot support interpretations
that require more text. Evaluators must retain unassessable judgments. Main
discussion counts and linked-material counts remain separate. There are 5,107
comments in the main snapshots; historical appendices remain distinct.

The collector now verifies transferred issue identities, parses slash-containing
branch names from blob metadata and decodes escaped filenames. PRs exposed through
issue endpoints retain available discussion/review material. Selected explicitly
cited Jira, Bugzilla, policy, standards and documentation sources are saved with
raw responses and extraction provenance. HTML text is clearly labelled, and
discussion completeness or redirected-page equivalence is not assumed. This is
one-hop, selected-host context; attachments and all external URLs are not claimed
to be covered. External evidence is checksummed and bound to its parent issue.

Frozen manifest SHA-256:
`07c78f25979e0569d79a68a3a308730174b28368e1623094634c47c2eafa4c1d`.
Exact `agent_inputs.json` SHA-256:
`464384a0a6d7b93d14df0e4f9e5bce67e06a56a9f7c045b8bedb2852af507687`.
Full gaps and retrieval errors: [`evidence-20261105-ready-coverage.json`](evidence-20261105-ready-coverage.json).

Offline verification checks exact companion bytes, source identities and citation
fields, reference-label separation and both phases. Run creation/reload checks
also compare every condition's actual artifacts and order. These checks do not
claim that API models have executed, human reviews have occurred, or scoring is
complete. See the [final preflight report](evidence-20261105-v7/preflight-final.json)
and run guide for the remaining requirements.

The 50-case model-sensitivity supplement also has sufficient conservative
source-complete formal candidates: 444 Code errors, 682 SATD and 412 Privacy.
Known unavailable/partial explicit links and title-only Privacy cases are excluded
from this supplementary sampling pool, while all cases stay in the main study.
Complete here means no known gap within the declared collected scope, not recovery
of every historical revision or attachment.

Final checks: 300 backend tests pass, all 36 conditions pass creation/reload,
and old v3/v5/v6 evidence remains verifiable. The persisted SATD pilot S1/r1
run is `run-60deee5af9d7` (169 cases, not started). No model API calls or scores
were generated during these checks.
