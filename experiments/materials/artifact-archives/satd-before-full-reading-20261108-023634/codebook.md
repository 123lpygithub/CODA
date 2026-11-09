# SATD — GPT6-1

All **856 artifacts** are included in **869 assignments** to **22 codes**: 20 substantive concern codes and 2 evidence-qualification codes.

The codebook was derived from direct reading of the supplied comments and source excerpts. No human reference categories or external model API were used. Codes describe the concern expressed by the material; a proposed change or question is not automatically a confirmed bug. S21 and S22 explicitly retain unclear markers and explanatory/instructional annotations, so full coverage does not falsely imply that every artifact establishes unresolved production debt.

All source sections, source locations, revision notes, and case-specific limitations are embedded in `assignments.json`; `results.json` includes each complete supplied document. The nested `taxonomy.json` provides a category/description/layer/children presentation; organizational headings are not additional assigned codes.

| Code | Category | Artifacts |
|---|---|---:|
| S01 | Unimplemented operation or component | 61 |
| S02 | Restricted supported cases | 92 |
| S03 | Computation or transformation mismatch | 30 |
| S04 | Incomplete output or state representation | 38 |
| S05 | Missing validation or enforcement | 21 |
| S06 | Incomplete exceptional-case handling | 19 |
| S07 | Insufficient executable verification | 51 |
| S08 | Unvalidated model or evaluation choice | 23 |
| S09 | Avoidable computational overhead | 40 |
| S10 | Excessive memory or storage footprint | 10 |
| S11 | Poor responsibility separation or reuse | 90 |
| S12 | Unclear or inconsistent interface contract | 61 |
| S13 | Insufficient documentation or examples | 16 |
| S14 | Insufficient diagnostic presentation | 19 |
| S15 | Rigid configuration or defaults | 31 |
| S16 | External compatibility constraint or workaround | 51 |
| S17 | Obsolete or transitional code | 34 |
| S18 | State and execution coordination | 20 |
| S19 | Provisional heuristic or workaround | 22 |
| S20 | Unresolved semantic or design assumption | 84 |
| S21 | Unspecified pending work | 24 |
| S22 | Explanatory or instructional annotation | 32 |

Counts overlap only where an artifact explicitly supports distinct concerns. No category-count cap or human codebook was used.

## S01 — Unimplemented operation or component

An intended operation or component is absent, disabled, stubbed, or replaced by placeholder behavior.

**Include:** Explicit implementation requests, empty methods, missing model components, or inactive intended features.

**Exclude/boundary:** Use S02 for additional variants of an already supported operation; S04 for persistence; S07 for missing tests.

**Supporting artifacts:** 61. See the JSON for the full ID list.

- `23shades-0388-aagaghfcd`: Fixed reference-point loss is zero and marked work in progress with a shared-position assumption.
- `23shades-0407-aaijdefji`: argpartition is listed as an unimplemented array operation.
- `23shades-0689-aaacjhcjh`: Spacing module consists of imports and a TODO for run-on and split handling.

## S02 — Restricted supported cases

An existing operation supports only a subset of required input forms, algorithms, entities, dimensions, or execution modes.

**Include:** Explicit unsupported variants, restrictive assumptions, or requests to generalize case coverage.

**Exclude/boundary:** Do not infer missing support merely from an untested case; use S07 or S20 for verification alone.

**Supporting artifacts:** 92. See the JSON for the full ID list.

- `23shades-0851-aajgdbgid`: Constructor introspection removes the first argument assuming self; staticmethod initialization violates this assumption.
- `23shades-0241-aajfahgcg`: Center-distance implementation supports cosine distance and requests Euclidean/angular options.
- `23shades-0302-aahiiggad`: Environment exposes discrete buttons; continuous DELTA actions need Box-space handling.

## S03 — Computation or transformation mismatch

The source identifies a concrete mismatch between implemented processing and an intended semantic requirement.

**Include:** Incorrect selection, alignment, counting, transformations, or a stated wrong algorithmic component.

**Exclude/boundary:** Use S20 for questions without a supported mismatch, S06 for exceptional-input handling, and S19 for provisional approximations.

**Supporting artifacts:** 30. See the JSON for the full ID list.

- `23shades-0488-aaahbjgif`: Polygon annotations should be clipped before mask conversion and rasterization.
- `23shades-0035-aahfiaifg`: CSV corpus still serializes as SVMLight rather than CSV.
- `23shades-0387-aahiiejjd`: Batched multi-body action policy notes backpropagation must use the corresponding reward too.

## S04 — Incomplete output or state representation

Required output, metadata, identifiers, persisted state, or provenance is omitted, lossy, unstable, or inadequately represented.

**Include:** Missing save/load behavior, missing output fields, unstable indices, lossy metadata conversion, and serialization-format changes.

**Exclude/boundary:** Use S14 for diagnostic presentation, S12 for general interface redesign, and S16 when the central concern is external compatibility.

**Supporting artifacts:** 38. See the JSON for the full ID list.

- `23shades-0346-aahiiefbj`: Agent close returns without action and requests saving.
- `23shades-0576-aaeihdcgb`: Constant Series conversion populates data but leaves index and name pending.
- `23shades-0350-aadfcfcca`: Molecular structure conversion omits biological assembly information and requires extra parsing.

## S05 — Missing validation or enforcement

A required validity, consistency, integrity, or authorization check is absent or incomplete.

**Include:** Input-schema checks, cross-input consistency, configuration validation, hash checking, and access preconditions.

**Exclude/boundary:** Use S06 for response to failure after it occurs; S07 for tests; retain uncertainty when a check already partly exists.

**Supporting artifacts:** 21. See the JSON for the full ID list.

- `23shades-0235-aaebjiiah`: Forecaster validates X and y separately but lacks joint consistency checks.
- `23shades-0048-aagaijehb`: Linear-model wrapper requests checks for compatible argument combinations.
- `23shades-0485-aafhihfed`: Layer freezing assumes QuartzNet encoder structure without checking model type.

## S06 — Incomplete exceptional-case handling

Exceptional states, numerical limits, invalid inputs, or failures lack adequate recovery, reporting, or protection.

**Include:** Zero denominators, overflow range, None values, retries, missing error branches, and poor exception diagnostics.

**Exclude/boundary:** Use S05 for ordinary precondition checks and S20 when only the desirability of a nonexceptional behavior is questioned.

**Supporting artifacts:** 19. See the JSON for the full ID list.

- `23shades-0598-aahiijgjf`: Invalid estimator type filter raises generic Exception rather than a specific exception.
- `23shades-0604-aajcjaefh`: Vector assignment rethrows exceptions without explaining vector lengths.
- `23shades-0791-aahgcaaac`: Adding keyed vectors may need warning when extras mismatch existing attributes.

## S07 — Insufficient executable verification

Tests, assertions, fixtures, or coverage are missing, disabled, weak, or require adaptation.

**Include:** Explicit requests for tests, failed or skipped tests, absent value assertions, and unverified test tolerances.

**Exclude/boundary:** Do not claim a production defect solely from a test gap; use S08 for empirical model/protocol evaluation.

**Supporting artifacts:** 51. See the JSON for the full ID list.

- `23shades-0230-aahjecdhj`: Excel test data lacks index metadata, and frame equality disables name checks.
- `23shades-0360-aajecehjc`: Ligand loading tests request additional file formats.
- `23shades-0386-aaiehihbh`: Partial node setter/getter assertions are commented out and marked to enable later.

## S08 — Unvalidated model or evaluation choice

Modeling, preprocessing, sampling, or evaluation choices need empirical assessment, broader measurement, or a sounder evaluation protocol.

**Include:** Architecture experiments, missing evaluation metrics, inadequate model results, train/test reuse, and sampling balance for evaluation.

**Exclude/boundary:** Use S07 for software tests and S20 for unverified local semantic assumptions without an empirical comparison request.

**Supporting artifacts:** 23. See the JSON for the full ID list.

- `23shades-0534-aaeebgfej`: Perceptron author proposes experiments with additional layers.
- `23shades-0749-aaihgdiif`: Arithmetic-expression enumeration starts at two operands; author asks to try smaller numbers.
- `23shades-0261-aaaiefadd`: Numeric-feature standardization needs checking once a downstream ML model exists.

## S09 — Avoidable computational overhead

Existing processing incurs unnecessary execution cost or could exploit parallelism, optimized primitives, caching, or reduced repeated work.

**Include:** Explicit slowness, unnecessary full sorting, repeated computation, host/device transfer, and proposed parallelization.

**Exclude/boundary:** Use S10 for storage/retention pressure; do not assume a proposed optimization has a measured benefit.

**Supporting artifacts:** 40. See the JSON for the full ID list.

- `23shades-0406-aahhejjge`: Tiling replaced a slower implementation; broadcasting is proposed for additional speed.
- `23shades-0636-aaibjdfgf`: LARS routine has an empty precompute TODO.
- `23shades-0776-aaieahjdd`: Equal-width bins need extrema but compute a full distribution for in-memory data.

## S10 — Excessive memory or storage footprint

Data representation, eager loading, or retained intermediates impose unnecessary memory or serialized-size cost.

**Include:** Sparse data stored densely, eager corpus loading, retained graph arrays, and oversized serialized graphs.

**Exclude/boundary:** Use S18 for ownership correctness and S09 for runtime cost without a stated footprint concern.

**Supporting artifacts:** 10. See the JSON for the full ID list.

- `23shades-0820-aajggjjdf`: Full block covariance would be too large, so source covariance is filled with NaN.
- `23shades-0530-aajacfjji`: Graph output arrays remain referenced until auto-initializing hooks allow None placeholders.
- `23shades-0153-aajacaegh`: Intermediate graph arrays could be freed when no longer needed, accounting for retain flags and backward schedule.

## S11 — Poor responsibility separation or reuse

Code organization, dependency structure, duplicated logic, or implementation complexity calls for restructuring or reuse.

**Include:** Extract/move helpers, remove circular coupling, use existing abstractions, simplify dense logic, and replace magic identifiers.

**Exclude/boundary:** Use S12 for public naming/contracts; do not attribute functional failure to a refactoring request alone.

**Supporting artifacts:** 90. See the JSON for the full ID list.

- `23shades-0678-aafeaiffi`: Loss is implemented through Lambda; author requests a custom Keras layer.
- `23shades-0446-aaedjcbec`: TriMesh should inherit from Graph when that abstraction exists.
- `23shades-0244-aafhgihee`: CPU-count/thread-pool setup should also be adopted in other loaders.

## S12 — Unclear or inconsistent interface contract

Names, types, parameter representations, API exposure, or abstraction boundaries inadequately communicate or coordinate intended use.

**Include:** Renaming, contradictory return contracts, redundant parameters, overloaded flags, generic annotations, and public API requests.

**Exclude/boundary:** Use S15 for selectable configuration and S11 for internal code placement or duplication.

**Supporting artifacts:** 61. See the JSON for the full ID list.

- `23shades-0609-aagcdcjae`: Histogram function signature is identified as potentially too restrictive.
- `23shades-0336-aafehbbbf`: Image resizing argument sizes may be renamed size.
- `23shades-0340-aaebjbdgg`: Task metadata setup receives a whole pandas container instead of a dedicated metadata container.

## S13 — Insufficient documentation or examples

Explanations, docstrings, usage examples, tutorials, or format specifications need creation or correction.

**Include:** Explicit documentation requests and inadequate representative examples.

**Exclude/boundary:** Use S14 for runtime diagnostics and S22 for explanatory comments that do not request documentation changes.

**Supporting artifacts:** 16. See the JSON for the full ID list.

- `23shades-0036-aaibigjdc`: Gaussian-mixture demonstration requests the faithful dataset instead of synthetic samples.
- `23shades-0193-aajfaiafb`: Module docstring contains only TODO.
- `23shades-0231-aafchbajj`: Feature-generator implementation lacks introductory explanation.

## S14 — Insufficient diagnostic presentation

Logs, plots, runtime feedback, or displayed analysis details are missing, misleading, or insufficiently useful.

**Include:** Missing visualizations, suppressed logging, diagnostic metadata, and loss of detail in plots.

**Exclude/boundary:** Use S04 for durable analytical records and S07 for tests that merely log instead of assert.

**Supporting artifacts:** 19. See the JSON for the full ID list.

- `23shades-0390-aagdhccjd`: Multiple active features enter a pass branch where a warning should be written.
- `23shades-0198-aajeiegcd`: Class-specific importances are averaged; stacked bars are proposed to retain class-feature differences.
- `23shades-0588-aaeiaghhj`: Existing-model message is constructed but never logged.

## S15 — Rigid configuration or defaults

Fixed values, environment-specific paths, or poorly derived defaults should become selectable, inferred, or consistently propagated.

**Include:** Hard-coded thresholds, resource counts, split ratios, dimensions, paths, missing defaults, and configuration precedence.

**Exclude/boundary:** Use S20 for uncertainty about a value without a request for configurability; fixed values alone do not establish debt.

**Supporting artifacts:** 31. See the JSON for the full ID list.

- `23shades-0461-aaidhjgaj`: Plotting currently tracks shared x axes manually; comment requests automation.
- `23shades-0768-aaahbfbgd`: Training requires an explicitly supplied monitor; a reasonable default is proposed.
- `23shades-0327-aadagfcdg`: Dataset shuffling seeds NumPy with fixed 1; author requests a seed option.

## S16 — External compatibility constraint or workaround

Dependency versions, platform behavior, external APIs, or package integration constrain functionality or require adaptation.

**Include:** Upstream bugs, missing external APIs, environment-specific failures, compatibility shims, and dependency migrations.

**Exclude/boundary:** Use S17 for scheduled retirement of transitional interfaces and S11 for internal dependency organization.

**Supporting artifacts:** 51. See the JSON for the full ID list.

- `23shades-0683-aaeihdfda`: Numba lacks np.isin in nopython mode, so membership is implemented with a comprehension.
- `23shades-0822-aahjfbdfa`: List-to-set conversion is deferred until set can be assumed builtin.
- `23shades-0120-aaeihdgig`: Range-index inequality converts results through NumPy pending a referenced Numba fix.

## S17 — Obsolete or transitional code

Temporary, deprecated, redundant, or debugging code is retained pending removal or migration completion.

**Include:** Scheduled API/test removal, old aliases, debug prints, migration scaffolding, and explicit unused-code removal.

**Exclude/boundary:** Do not imply removal is already safe when the source makes it conditional; use S16 for a still-required compatibility mechanism.

**Supporting artifacts:** 34. See the JSON for the full ID list.

- `23shades-0676-aaicjgced`: DeprecationDict should become ordinary dict after version transition.
- `23shades-0155-aafibegdj`: Image size property is marked probably unnecessary during transition.
- `23shades-0647-aaidbfgae`: Both candidate locations warn on deprecated score properties; planned version should raise errors.

## S18 — State and execution coordination

State ownership, lifecycle ordering, concurrent access, scheduling, or cross-worker coordination needs correction or redesign.

**Include:** Thread-local state, file races, resource sessions, blocking execution, stale training state, shared-layer identity, and state propagation order.

**Exclude/boundary:** Use S10 for memory pressure alone and S20 for an unresolved question without a stated coordination obligation.

**Supporting artifacts:** 20. See the JSON for the full ID list.

- `23shades-0299-aahiiegbc`: Agent update delegates only algorithm update while generic memory/network coordination is deferred.
- `23shades-0614-aaadihafg`: Actor-critic epsilon variable creation and moving update are marked as needing a better approach.
- `23shades-0349-aagciihdj`: Dataflow contexts should be returned to a shared list so another waiter can receive its context.

## S19 — Provisional heuristic or workaround

A local approximation, forced assumption, fallback, or brittle convention substitutes for a better justified general solution.

**Include:** Explicit hacks, arbitrary first-match selection, patched malformed spans, fixed substitute values, and fragile naming conventions.

**Exclude/boundary:** Use S16 for external-compatibility-driven workarounds; preserve whether the current workaround is already effective.

**Supporting artifacts:** 22. See the JSON for the full ID list.

- `23shades-0537-aaeidjjhd`: Evaluation-node extraction depends on reordering after parallel-loop fusion and should be more robust.
- `23shades-0165-aajaicjbh`: Binary versus categorical model is inferred from score-list length and called hacky.
- `23shades-0849-aaibjdjdc`: Estimator classifier detection recursively probes estimator/steps attributes as temporary solution.

## S20 — Unresolved semantic or design assumption

The author questions correctness, necessity, interpretation, or design semantics without enough evidence to establish a specific defect.

**Include:** Questions about formulas, boundary conventions, unnecessary operations, ambiguous defaults, and possibly stale TODOs.

**Exclude/boundary:** Use a concrete substantive code when the intended change is explicit; retain the question instead of converting it into a confirmed fault.

**Supporting artifacts:** 84. See the JSON for the full ID list.

- `23shades-0694-aaidhabjj`: Initial trade date may need interval alignment, adjacent to datetime preprocessing.
- `23shades-0276-aaadbjbdj`: Dehazing comment requests reciprocal-transmission treatment; current expression already divides by transmission.
- `23shades-0439-aaeeicdeh`: Audio frame count may need an extra frame-size contribution to cover the signal.

## S21 — Unspecified pending work

A revision marker exists but available material does not establish a sufficiently specific substantive concern.

**Include:** Bare TODO/FIXME, opaque experiment markers, unspecified bugs, and unclear inactive alternatives.

**Exclude/boundary:** Do not use when surrounding context identifies a concrete missing operation or concern; this records evidence limits, not a defect type.

**Supporting artifacts:** 24. See the JSON for the full ID list.

- `23shades-0371-aaadajhci`: Prediction setup is marked to be modified without identifying the required change.
- `23shades-0195-aaibgjfcg`: Bare TODO precedes fixed model dimensions 3 and 300.
- `23shades-0187-aadfababd`: Correction-loading function is marked TODO although a body already exists.

## S22 — Explanatory or instructional annotation

The selected annotation describes implemented behavior, an existing safeguard, or an instructional task without establishing unresolved production work.

**Include:** Already implemented operations, explanatory needed-for comments, equivalent implementations, and exercise placeholders.

**Exclude/boundary:** Do not count this as confirmed technical debt; use a substantive code when an explicit remaining change is supported.

**Supporting artifacts:** 32. See the JSON for the full ID list.

- `23shades-0794-aahdadjbj`: Shared port is explicitly set to unused zero in game joining.
- `23shades-0056-aaeeibecj`: Comment explains a circular shift required for phase, and following code performs it.
- `23shades-0826-aaeieahii`: String-length send array uses uint32 and comment notes offset type.

## Method and limits

All 856 input records and their available source sections were read. Provisional observations were compared across cases and consolidated by the underlying maintenance concern. One primary code was manually assigned to every artifact; a second code was added only for an explicitly distinct concern. Packaging checks verify coverage, references, and verbatim source evidence; they do not constitute independent semantic validation.

- Source-context ambiguity and historical revision limitations remain in evidence and scope notes.
- Questions, proposals, implemented workarounds, and confirmed mismatches are distinguished in case rationales.
- This is one assistant analysis, not independent human validation or two independent coding runs.
