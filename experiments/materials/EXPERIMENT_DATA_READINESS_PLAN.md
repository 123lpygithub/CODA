# Experiment data readiness work plan

Target: provide executable, reference-blind inputs for the current paper's 557
Code errors, 856 ML SATD and 652 Privacy cases. Preserve manuscript wording and
existing frozen inputs. Complete evidence and experimental readiness are reported
separately; no labels are used to invent evidence or force assessability.

| Task | Acceptance condition | Status |
| --- | --- | --- |
| Verify current paper | Current dataset units and calibration/formal allocation identified | Complete: 20% grouped calibration; 80% formal; two runs/configuration |
| Repair GitHub source collection | Slash refs, encoded filenames, redirected issue identities handled and tested | Complete; 435 available, 13 partial, 94 unavailable case–link records |
| Resolve remaining SATD historical context | Alternative source matched and revision relationship proven, or explicit uncertainty retained | Complete: 849 unique locations, 4 ambiguous, 3 verified related-history partial; no unmatched cases |
| Supplement Privacy discussions and related evidence | Preserve complete current and historical-only evidence separately, no weaker replacement | Complete within retrievable scope: 635 current complete, 16 historical-only, 1 current partial; selected external context added |
| Freeze experiment bundle | Exact case counts, groups, order, evidence hashes, same materials for S1/S2/S3 | Complete: evidence-20261105-v7, old inputs preserved |
| Validate execution | Offline preparation, run creation, input citation checks, initialization/iteration integration checks | Complete offline: all 36 conditions created/reloaded; full backend suite passes; actual model execution remains separate |
| Document limitations and commands | Reproducible preflight, per-case gaps, concrete run plan; no claim experiments finished | Complete: PAPER_EXPERIMENT_RUN_GUIDE.md and v7/preflight-final.json |

The data-preparation acceptance conditions are met. This does not mean all
original-study evidence is recoverable or that the experiment has been run.
Live model availability, independent human participation and evaluator scoring
remain required. The current agent process has no readable model credentials;
no real API execution is asserted. Seven retrieved Privacy bodies are empty,
including two cases without comments. Missing essential evidence remains
unassessable. The user-approved single-case batch audit exception is recorded
explicitly because the current paper still describes rounded-up sampling.

Final validation: 300 backend tests pass; all 36 paper conditions pass temporary
creation/reload with exact matched evidence. v3, v5 and v6 frozen inputs still
verify. A persistent 169-case SATD pilot S1/r1 run was created as
`run-60deee5af9d7`, status `not_started`. Model-sensitivity source-complete formal
pools contain 444/682/412 cases, respectively, each exceeding the required 50.
