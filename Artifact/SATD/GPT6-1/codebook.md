# SATD / GPT6-1

Schema: `coda.artifact.v1`. Artifacts: **856**; codes: **18**; artifact–code assignments: **869**.

This package uses the common seven-file format. All existing coding decisions, evidence and limitations are preserved. Additional source-specific fields are retained in `extensions`; original codebook text is retained in `codebook.json` metadata extensions and the local pre-conversion backup.

## Scope and method

Inductive consolidation of individually authored full supplied-text reading notes, followed by explicit per-artifact assignment review. No keyword classifier, external model API, or prior codebook assignments were used for consolidation.

Coverage refers to all supplied textual sections, not all content ever linked on the web.
Source revision ambiguity, inaccessible context, tentative proposals and absence of execution evidence remain in individual scope notes.
Coding is assistant-authored; it is not published human annotation, independently validated ground truth, or an experimental system run.
All artifacts are included; unspecified work and comments without established outstanding work are retained explicitly rather than invented as defects.

## Codes

| Code | Name | Artifacts |
|---|---|---:|
| IMP | Unfinished functionality | 74 |
| EXT | Restricted supported cases | 109 |
| REP | Incomplete or mismatched information representation | 45 |
| ALG | Behavioral or analytical correctness concern | 34 |
| VAL | Incomplete validation or failure handling | 26 |
| DES | Unresolved design or interpretation choice | 124 |
| ARC | Structural simplification and responsibility placement | 112 |
| NAM | Unclear or inconsistent interface naming | 24 |
| CFG | Inflexible configuration or defaults | 27 |
| PER | Avoidable computation or memory cost | 47 |
| TST | Insufficient verification coverage | 60 |
| DOC | Incomplete documentation or examples | 19 |
| DEP | Dependency and version adaptation | 60 |
| OUT | Incomplete result delivery or traceability | 23 |
| RES | Resource lifecycle and concurrent-state coordination | 11 |
| OBS | Insufficient or intrusive operational diagnostics | 14 |
| UNC | Unspecified remaining work | 24 |
| EXPL | Implemented behavior without established remaining work | 36 |

## IMP — Unfinished functionality

A named operation, workflow step, or output is absent, stubbed, disabled, or explicitly awaiting implementation.

- Include: Include pass/NotImplementedError, inactive drafts, or a concrete missing step.
- Exclude: Exclude extension of a functioning operation to additional input/backend combinations (EXT); absent tests (TST).
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 74; complete membership in `supporting_cases`.

````json
[]
````

## EXT — Restricted supported cases

An implemented operation does not cover a stated input type, shape, backend, format, model family, or execution mode.

- Include: Include an explicit unsupported combination or requested generalization.
- Exclude: Exclude an entirely missing operation (IMP) and merely questioning whether an unspecified extension is needed (DES).
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 109; complete membership in `supporting_cases`.

````json
[]
````

## REP — Incomplete or mismatched information representation

A data representation, interface contract, conversion, or persistence path loses information or cannot express the intended semantics.

- Include: Include omitted metadata, incompatible shapes/contracts, lossy reduction, and mismatched producer/consumer granularity.
- Exclude: Exclude changes motivated only by clearer organization (ARC) or naming (NAM); do not infer actual loss when only potential loss is documented.
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 45; complete membership in `supporting_cases`.

````json
[]
````

## ALG — Behavioral or analytical correctness concern

The material identifies a specific discrepancy, faulty assumption, numerical hazard, or methodological problem in implemented computation or evaluation.

- Include: Include source-visible contradictions and explicitly reported incorrect behavior; retain conditionality and lack of execution evidence.
- Exclude: Exclude open-ended choices without a concrete discrepancy (DES), and missing precondition checks (VAL).
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 34; complete membership in `supporting_cases`.

````json
[]
````

## VAL — Incomplete validation or failure handling

Required input, state, consistency, authorization, or failure conditions are insufficiently checked or handled.

- Include: Include omitted checks, overbroad exception handling, and missing recovery/error policy.
- Exclude: Exclude an unsupported input explicitly rejected by design (EXT); message clarity alone belongs to OBS.
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 26; complete membership in `supporting_cases`.

````json
[]
````

## DES — Unresolved design or interpretation choice

The developer has not settled whether an algorithm, parameter policy, representation, or architectural alternative is appropriate.

- Include: Include genuine questions about meaning, necessity, tradeoffs, and correctness where no definite defect is established.
- Exclude: Exclude a concrete prescribed refactoring (ARC), a visible discrepancy (ALG), and a marker with no interpretable requested change (UNC).
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 124; complete membership in `supporting_cases`.

````json
[]
````

## ARC — Structural simplification and responsibility placement

Existing behavior needs clearer abstraction, consolidation, decomposition, dependency separation, or placement.

- Include: Include duplicated logic, ad hoc wrappers, private-API coupling, circular dependencies, obsolete code cleanup, and moving responsibilities.
- Exclude: Exclude mere renaming (NAM), dependency-version migrations (DEP), and a new missing behavior (IMP).
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 112; complete membership in `supporting_cases`.

````json
[]
````

## NAM — Unclear or inconsistent interface naming

Names, aliases, parameter terminology, or exposed method names inadequately communicate their role or differ across related interfaces.

- Include: Include renaming, constants/enums replacing magic identifiers, and ambiguous terminology.
- Exclude: Exclude substantive representation changes (REP) or an unsettled behavior rather than naming (DES).
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 24; complete membership in `supporting_cases`.

````json
[]
````

## CFG — Inflexible configuration or defaults

A meaningful option, default, path, threshold, or resource setting is hardcoded, inaccessible, or disconnected from configuration.

- Include: Include exposing controls and replacing personal paths or architecture-specific constants with derived settings.
- Exclude: Exclude an unresolved choice of the right value without a request for configuration (DES); missing combinations belong to EXT.
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 27; complete membership in `supporting_cases`.

````json
[]
````

## PER — Avoidable computation or memory cost

The material identifies redundant computation, costly representations, unnecessary transfers, or opportunities for parallelism, reuse, or reduced memory.

- Include: Include proposed optimizations without claiming a measured improvement.
- Exclude: Exclude resource correctness/lifecycle problems (RES) and replacing code solely for organization (ARC).
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 47; complete membership in `supporting_cases`.

````json
[]
````

## TST — Insufficient verification coverage

Tests, assertions, examples used for verification, or checks of an implementation remain missing, disabled, weak, or unreliable.

- Include: Include untested paths, loose tolerances, broken fixtures, and required test expansion.
- Exclude: Exclude production validation (VAL) and scheduled retirement of a still-useful compatibility test (DEP).
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 60; complete membership in `supporting_cases`.

````json
[]
````

## DOC — Incomplete documentation or examples

Explanations, API documentation, tutorials, usage examples, or instructions are missing, outdated, or inconsistent with the shown behavior.

- Include: Include module/docstring placeholders and proposed explanatory examples.
- Exclude: Exclude runtime diagnostics (OBS) and missing functional output (OUT).
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 19; complete membership in `supporting_cases`.

````json
[]
````

## DEP — Dependency and version adaptation

Behavior relies on a compatibility workaround, historical dependency constraint, or planned version/API migration.

- Include: Include temporary aliases, legacy loaders, upstream limitations, and deferred cleanup after minimum-version changes.
- Exclude: Exclude generic coupling without version/dependency constraints (ARC); retain whether a workaround already functions.
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 60; complete membership in `supporting_cases`.

````json
[]
````

## OUT — Incomplete result delivery or traceability

Computed results or their provenance are not adequately saved, exposed, visualized, or reported.

- Include: Include missing model/checkpoint persistence, evaluation exports, metadata lineage, and result visualization.
- Exclude: Exclude runtime warnings/logging (OBS), documentation (DOC), or a proposed data structure change with no delivery concern (REP).
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 23; complete membership in `supporting_cases`.

````json
[]
````

## RES — Resource lifecycle and concurrent-state coordination

State ownership, cleanup, shutdown, asynchronous result routing, or concurrent access needs explicit coordination.

- Include: Include races, retained resources, thread-local state, and uncertain reference ownership.
- Exclude: Exclude solely performance-motivated allocation reductions without a lifecycle issue (PER).
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 11; complete membership in `supporting_cases`.

````json
[]
````

## OBS — Insufficient or intrusive operational diagnostics

Warnings, errors, status messages, logging, or debug output inadequately support operation or require cleanup.

- Include: Include missing/incorrect messages, overly generic exception types, and temporary debug prints.
- Exclude: Exclude validation logic itself (VAL), analytical result reporting (OUT), or explanatory documentation (DOC).
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 14; complete membership in `supporting_cases`.

````json
[]
````

## UNC — Unspecified remaining work

A supplied TODO or similar marker does not identify enough remaining behavior to support a more specific work category.

- Include: Use only when surrounding source still leaves the intended change indeterminate; retain the concrete context in the case rationale.
- Exclude: Exclude interpretable alternatives (DES), named missing functionality (IMP), or explanatory comments without outstanding work (EXPL).
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 24; complete membership in `supporting_cases`.

````json
[]
````

## EXPL — Implemented behavior without established remaining work

The selected comment describes an implemented safeguard, constraint, transformation, or educational instruction, without establishing outstanding maintenance work in the supplied context.

- Include: Include explanatory XXX/maybe comments, implemented requested-looking operations, and explicit teaching scaffolds.
- Exclude: Exclude active compatibility debt with a stated migration/removal dependency (DEP) and unknown TODO intent (UNC).
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 36; complete membership in `supporting_cases`.

````json
[]
````

## Files

- `codebook.md`, `codebook.json`, `codebook.csv`: definitions and complete reverse memberships.
- `assignments.json`, `assignments.csv`: one record per artifact, including decisions and evidence.
- `taxonomy.json`: category tree with every code as a leaf.
- `results.json`: supplied full documents aligned to their assignments.

## Original codebook

The original codebook text below preserves run-specific scope, combination rules and qualifications. Links and filenames in that historical text describe the original package; use the seven files above for the normalized interface. The exact original text is also stored in metadata extensions.

# SATD — GPT6-1

856 artifacts; 18 codes; 869 artifact–code assignments.

Inductive consolidation of individually authored full supplied-text reading notes, followed by explicit per-artifact assignment review. No keyword classifier, external model API, or prior codebook assignments were used for consolidation.

Every supplied artifact has an assignment. Codes describe the observed work, concern, or evidence status; they do not establish that a defect was reproduced. Refer to `assignments.json` for individual reasoning, qualifications, source references and evidence.

## Scope

- Coverage refers to all supplied textual sections, not all content ever linked on the web.
- Source revision ambiguity, inaccessible context, tentative proposals and absence of execution evidence remain in individual scope notes.
- Coding is assistant-authored; it is not published human annotation, independently validated ground truth, or an experimental system run.
- All artifacts are included; unspecified work and comments without established outstanding work are retained explicitly rather than invented as defects.

Reconstruction within the same conversation; not a blinded independent replicate.

## Codebook

| Code | Name | Artifacts |
|---|---|---:|
| IMP | Unfinished functionality | 74 |
| EXT | Restricted supported cases | 109 |
| REP | Incomplete or mismatched information representation | 45 |
| ALG | Behavioral or analytical correctness concern | 34 |
| VAL | Incomplete validation or failure handling | 26 |
| DES | Unresolved design or interpretation choice | 124 |
| ARC | Structural simplification and responsibility placement | 112 |
| NAM | Unclear or inconsistent interface naming | 24 |
| CFG | Inflexible configuration or defaults | 27 |
| PER | Avoidable computation or memory cost | 47 |
| TST | Insufficient verification coverage | 60 |
| DOC | Incomplete documentation or examples | 19 |
| DEP | Dependency and version adaptation | 60 |
| OUT | Incomplete result delivery or traceability | 23 |
| RES | Resource lifecycle and concurrent-state coordination | 11 |
| OBS | Insufficient or intrusive operational diagnostics | 14 |
| UNC | Unspecified remaining work | 24 |
| EXPL | Implemented behavior without established remaining work | 36 |

## IMP — Unfinished functionality

A named operation, workflow step, or output is absent, stubbed, disabled, or explicitly awaiting implementation.

**Include:** Include pass/NotImplementedError, inactive drafts, or a concrete missing step.

**Exclude:** Exclude extension of a functioning operation to additional input/backend combinations (EXT); absent tests (TST).

**Examples:**

- `23shades-0694-aaidhabjj`: A trailing-stop simulation stores the input datetime without the proposed interval preprocessing. The comments distinguish entry time from activation time because slippage can intervene, then ask how to set the original-date interval. Qualification: The precise interval rule is not supplied; do not invent rounding behavior or a demonstrated trading error.
- `23shades-0388-aagaghfcd`: Within a multi-term representation-learning loss, fixed_ref_point_loss remains zero and is marked work in progress. Its planned use assumes a common Baxter-arm position across all sequences. Temporal coherence itself is already calculated above. Qualification: Do not describe temporal-coherence computation as absent merely because its name occurs in the comment; the final loss expression is only partially shown.

## EXT — Restricted supported cases

An implemented operation does not cover a stated input type, shape, backend, format, model family, or execution mode.

**Include:** Include an explicit unsupported combination or requested generalization.

**Exclude:** Exclude an entirely missing operation (IMP) and merely questioning whether an unspecified extension is needed (DES).

**Examples:**

- `23shades-0241-aajfahgcg`: CenterDistanceModule documents and implements an interface for embedding-to-center cosine distance; the author wants alternatives such as Euclidean and angular metrics. Qualification: This is missing choice of metric, not evidence that the current cosine metric is wrong.
- `23shades-0302-aahiiggad`: The VizDoom wrapper represents every button as a two-valued discrete action. Continuous DELTA buttons require a different action representation, identified by the author as gym Box. Qualification: The excerpt also contains repeat assignment, but the target concern is action-space coverage, not a separately inferred repeat defect.

## REP — Incomplete or mismatched information representation

A data representation, interface contract, conversion, or persistence path loses information or cannot express the intended semantics.

**Include:** Include omitted metadata, incompatible shapes/contracts, lossy reduction, and mismatched producer/consumer granularity.

**Exclude:** Exclude changes motivated only by clearer organization (ARC) or naming (NAM); do not infer actual loss when only potential loss is documented.

**Examples:**

- `23shades-0820-aajggjjdf`: The inverse solution stores NaN for source covariance because the free-orientation block-diagonal form lacks an efficient storage representation; materializing a huge dense matrix is rejected. The code uses weighted eigen leads so the omitted covariance is currently not consumed downstream. Qualification: A deliberate representation compromise with a stated mitigating condition; not evidence that computed outputs are invalid.
- `23shades-0628-aaifedeec`: Module boundary extraction tests each output against a single input_to_node mapping. The author notes a value can feed multiple nodes, so one consumer association may omit another consumer outside the module. Qualification: The full map construction is not shown; the interpretation follows the acknowledged fan-out issue rather than a tested failing graph.

## ALG — Behavioral or analytical correctness concern

The material identifies a specific discrepancy, faulty assumption, numerical hazard, or methodological problem in implemented computation or evaluation.

**Include:** Include source-visible contradictions and explicitly reported incorrect behavior; retain conditionality and lack of execution evidence.

**Exclude:** Exclude open-ended choices without a concrete discrepancy (DES), and missing precondition checks (VAL).

**Examples:**

- `23shades-0851-aajgdbgid`: Constructor introspection unconditionally removes the first argument as self. The author acknowledges that a staticmethod initializer violates this assumption: a real argument would be removed, or an empty list could fail. Qualification: This is an acknowledged edge-case assumption, not evidence that ordinary estimator constructors fail.
- `23shades-0727-aaheacagj`: Training uses random binary labels converted to categorical targets. The author explicitly wants actual externally supplied targets. Qualification: No quality estimate or production-use claim follows from this demonstrable placeholder.

## VAL — Incomplete validation or failure handling

Required input, state, consistency, authorization, or failure conditions are insufficiently checked or handled.

**Include:** Include omitted checks, overbroad exception handling, and missing recovery/error policy.

**Exclude:** Exclude an unsupported input explicitly rejected by design (EXT); message clarity alone belongs to OBS.

**Examples:**

- `23shades-0639-aaecjeidf`: Prediction comparisons extract the second-last ARFF column by position without checking returned headers. The TODO asks to confirm the expected predict/correct feature identities programmatically. Qualification: The extraction shown selects one column despite the preceding last-two-columns comment; do not claim both columns are compared.
- `23shades-0235-aaebjiiah`: Forecasting validation checks y and X separately but requests joint consistency checks between target and exogenous data. Qualification: No precise length/index invariant is specified; individual validation is already present.

## DES — Unresolved design or interpretation choice

The developer has not settled whether an algorithm, parameter policy, representation, or architectural alternative is appropriate.

**Include:** Include genuine questions about meaning, necessity, tradeoffs, and correctness where no definite defect is established.

**Exclude:** Exclude a concrete prescribed refactoring (ARC), a visible discrepancy (ALG), and a marker with no interpretable requested change (UNC).

**Examples:**

- `23shades-0609-aagcdcjae`: The author questions the flexibility of plot_histogram's signature, which exposes axes, bins, contents and normalization plus variadic arguments. The neighboring request for a richer plotting concept is context rather than proof of an incorrect histogram. Qualification: The desired signature and unsupported caller scenario are unspecified; retain the tentative nature of the request.
- `23shades-0439-aaeeicdeh`: The frame-count property currently uses ceiling(signal length / hop size). The author asks whether to add frame_size to the numerator to cover the whole audio signal, explicitly noting signal_frame must also change. Qualification: Coverage depends on frame positioning/padding not supplied here; cannot conclude actual signal samples are lost.

## ARC — Structural simplification and responsibility placement

Existing behavior needs clearer abstraction, consolidation, decomposition, dependency separation, or placement.

**Include:** Include duplicated logic, ad hoc wrappers, private-API coupling, circular dependencies, obsolete code cleanup, and moving responsibilities.

**Exclude:** Exclude mere renaming (NAM), dependency-version migrations (DEP), and a new missing behavior (IMP).

**Examples:**

- `23shades-0678-aafeaiffi`: The loss is already computed with a Lambda wrapping yolo_loss on the CPU. The requested change is to encapsulate that operation in a custom Keras layer, not to introduce a missing loss calculation. Qualification: No numerical failure or runtime defect is established by this excerpt.
- `23shades-0461-aaidhjgaj`: Portfolio visualization explicitly initializes shared-axis state and alters x-axis display by subplot position. The author requests automation of this repeated shared-x coordination. Qualification: The supplied context ends before the plotting calls; a malfunction of sharing is not demonstrated.

## NAM — Unclear or inconsistent interface naming

Names, aliases, parameter terminology, or exposed method names inadequately communicate their role or differ across related interfaces.

**Include:** Include renaming, constants/enums replacing magic identifiers, and ambiguous terminology.

**Exclude:** Exclude substantive representation changes (REP) or an unsettled behavior rather than naming (DES).

**Examples:**

- `23shades-0336-aafehbbbf`: The resize API uses the plural sizes for the common target size of multiple images. The author considers singular size to better express this meaning. Qualification: This is a tentative naming refinement, not a resize defect or lack of supported dimensions.
- `23shades-0253-aaebaidgd`: A field named phonemes can hold tones alone or tones plus phones, depending on target_type. The requested tgt_labels rename would reflect its actual broader meaning. Qualification: This is semantic naming clarity; the current assignment explicitly supports tones.

## CFG — Inflexible configuration or defaults

A meaningful option, default, path, threshold, or resource setting is hardcoded, inaccessible, or disconnected from configuration.

**Include:** Include exposing controls and replacing personal paths or architecture-specific constants with derived settings.

**Exclude:** Exclude an unresolved choice of the right value without a request for configuration (DES); missing combinations belong to EXT.

**Examples:**

- `23shades-0768-aaahbfbgd`: Initialization asserts a monitor is supplied. The author considers a sensible default to remove that mandatory configuration burden, analogous to a neighboring optimizer-default proposal. Qualification: A monitor exists when supplied; this is not missing monitoring implementation.
- `23shades-0327-aadagfcdg`: Dataset shuffling seeds NumPy with literal 1. The requested improvement is making this seed configurable so other reproducible splits can be selected. Qualification: The current operation already fixes a seed; claiming absent reproducibility would reverse the evidence.

## PER — Avoidable computation or memory cost

The material identifies redundant computation, costly representations, unnecessary transfers, or opportunities for parallelism, reuse, or reduced memory.

**Include:** Include proposed optimizations without claiming a measured improvement.

**Exclude:** Exclude resource correctness/lifecycle problems (RES) and replacing code solely for organization (ARC).

**Examples:**

- `23shades-0820-aajggjjdf`: The inverse solution stores NaN for source covariance because the free-orientation block-diagonal form lacks an efficient storage representation; materializing a huge dense matrix is rejected. The code uses weighted eigen leads so the omitted covariance is currently not consumed downstream. Qualification: A deliberate representation compromise with a stated mitigating condition; not evidence that computed outputs are invalid.
- `23shades-0406-aahhejjge`: The mesh-grid implementation already replaced multiplication by ones with tile and reports a speedup. A further broadcasting optimization remains proposed. Qualification: The reported sixfold improvement concerns the existing tile change, not a measured benefit from the future broadcast proposal.

## TST — Insufficient verification coverage

Tests, assertions, examples used for verification, or checks of an implementation remain missing, disabled, weak, or unreliable.

**Include:** Include untested paths, loose tolerances, broken fixtures, and required test expansion.

**Exclude:** Exclude production validation (VAL) and scheduled retirement of a still-useful compatibility test (DEP).

**Examples:**

- `23shades-0230-aahjecdhj`: Excel input comparisons disable name checking while TODOs ask for an index in the fixture and question whether reading preserves index names. This leaves metadata agreement unchecked. Qualification: Cannot conclude the reader itself drops index names; the adjacent comment poses that as a question.
- `23shades-0360-aajecehjc`: The ligand-loading test uses one PDBQT fixture and checks nine returned ligands and nonzero coordinates. The author wants tests for additional input formats. Qualification: Lack of format tests does not establish lack of implementation support for those formats.

## DOC — Incomplete documentation or examples

Explanations, API documentation, tutorials, usage examples, or instructions are missing, outdated, or inconsistent with the shown behavior.

**Include:** Include module/docstring placeholders and proposed explanatory examples.

**Exclude:** Exclude runtime diagnostics (OBS) and missing functional output (OUT).

**Examples:**

- `23shades-0036-aaibigjdc`: A Gaussian-mixture plotting example currently constructs random transformed data. Its module docstring requests replacing the example input with the faithful dataset. Qualification: No Gaussian-mixture algorithm defect or missing experimental validation is established.
- `23shades-0193-aajfaiafb`: The module-level docstring consists only of TODO between the license/authorship header and imports. The visible missing content is a module description. Qualification: The bare marker does not establish an unimplemented model or unspecified runtime bug.

## DEP — Dependency and version adaptation

Behavior relies on a compatibility workaround, historical dependency constraint, or planned version/API migration.

**Include:** Include temporary aliases, legacy loaders, upstream limitations, and deferred cleanup after minimum-version changes.

**Exclude:** Exclude generic coupling without version/dependency constraints (ARC); retain whether a workaround already functions.

**Examples:**

- `23shades-0416-aaiibahhd`: Package imports and exports for new TensorFlow model classes are commented out until ModelV1 deprecation removes circular dependencies. Qualification: The classes may exist elsewhere; this is deferred package exposure, not proof that the model implementations are absent.
- `23shades-0362-aahchacde`: During TensorFlow 2 migration, optimizer construction receives the optimizer type while former optimize plumbing is commented out. The target TODO asks to restore optimizer parameters. Qualification: Schedulers and TensorBoard are neighboring migration work, not additional assertions about this target comment.

## OUT — Incomplete result delivery or traceability

Computed results or their provenance are not adequately saved, exposed, visualized, or reported.

**Include:** Include missing model/checkpoint persistence, evaluation exports, metadata lineage, and result visualization.

**Exclude:** Exclude runtime warnings/logging (OBS), documentation (DOC), or a proposed data structure change with no delivery concern (REP).

**Examples:**

- `23shades-0780-aaididbfa`: The sentence writer emits word, lemma and POS fields; writing an index remains TODO. Qualification: Index format and exact unit are unspecified.
- `23shades-0198-aajeiegcd`: Class-specific feature importances are averaged to one vector. A proposed stacked chart would preserve the per-class distinctions instead. Qualification: A visualization alternative, not proof averaging is invalid. Context is the verified parent of a published pointer that deletes the comment.

## RES — Resource lifecycle and concurrent-state coordination

State ownership, cleanup, shutdown, asynchronous result routing, or concurrent access needs explicit coordination.

**Include:** Include races, retained resources, thread-local state, and uncertain reference ownership.

**Exclude:** Exclude solely performance-motivated allocation reductions without a lifecycle issue (PER).

**Examples:**

- `23shades-0349-aagciihdj`: Concurrent run_dataflow callers sharing an orchestrator need the completed/submitted context routed through shared run_operations bookkeeping so each waiting invocation gets its own result. Qualification: The adjacent concurrency-cap and identity-check TODOs are distinct; no concrete deadlock trace is present.
- `23shades-0014-aadbjfiab`: Graph matching raises global recursion limits but relies on manual restoration because a destructor combined with cyclic references caused collection problems in the described runtime. The planned structural remedy is nonrecursive matching. Qualification: A manual restoration method is present; do not claim the current implementation installs the leaking destructor or generalize its historical GC behavior to every Python version.

## OBS — Insufficient or intrusive operational diagnostics

Warnings, errors, status messages, logging, or debug output inadequately support operation or require cleanup.

**Include:** Include missing/incorrect messages, overly generic exception types, and temporary debug prints.

**Exclude:** Exclude validation logic itself (VAL), analytical result reporting (OUT), or explanatory documentation (DOC).

**Examples:**

- `23shades-0390-aagdhccjd`: When a featurizer contains multiple active feature groups, atom-index extraction passes silently; the author requests a warning. The single-feature branch fills atom-index information later used in display strings. Qualification: Possible downstream indexing problems deserve investigation, but the explicit requested change is a warning, not proof of an observed crash.
- `23shades-0598-aahiijgjf`: Invalid estimator-type filters already raise an error with an explanatory message, but use generic Exception. The author requests a more specific exception type. Qualification: Input checking is present; the concern is exception specificity, not missing validation.

## UNC — Unspecified remaining work

A supplied TODO or similar marker does not identify enough remaining behavior to support a more specific work category.

**Include:** Use only when surrounding source still leaves the intended change indeterminate; retain the concrete context in the case rationale.

**Exclude:** Exclude interpretable alternatives (DES), named missing functionality (IMP), or explanatory comments without outstanding work (EXPL).

**Examples:**

- `23shades-0371-aaadajhci`: A generic modification TODO precedes switching the predictor model to inference mode and building its graph. This locates the concern in prediction initialization without specifying a replacement or defect. Qualification: Do not invent an incorrect training flag; inference mode is appropriate for prediction.
- `23shades-0195-aaibgjfcg`: A bare TODO precedes literal maxout_pieces=3 and hidden_size=300 used for two pretraining objectives. It plausibly concerns these fixed model choices, but does not explicitly request configurability. Qualification: Keep configuration exposure as a possible interpretation rather than treating it as an explicit developer request.

## EXPL — Implemented behavior without established remaining work

The selected comment describes an implemented safeguard, constraint, transformation, or educational instruction, without establishing outstanding maintenance work in the supplied context.

**Include:** Include explanatory XXX/maybe comments, implemented requested-looking operations, and explicit teaching scaffolds.

**Exclude:** Exclude active compatibility debt with a stated migration/removal dependency (DEP) and unknown TODO intent (UNC).

**Examples:**

- `23shades-0276-aaadbjbdj`: The target comment asks for reciprocal-transmission dehazing, but the displayed active RGB loop already divides its adjusted pixel values by transmission. The excerpt contains alternative commented formulas, so the TODO may describe work already reflected in the code or an unresolved formulation choice. Qualification: Do not code a missing reciprocal or missing RGB processing solely from the TODO; both operations appear in the supplied context. No test or intended formula beyond the note is supplied.
- `23shades-0794-aahdadjbj`: The comment unused annotates a protocol field explicitly set to zero while other game/client ports are populated. It explains why a field is neutral rather than requesting removal of dead code. Qualification: Do not infer technical debt or an unnecessary assignment from the isolated word unused.
