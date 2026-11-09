# deepseek-2 — SATD 最终编码本

本轮覆盖 **856 个 自承认技术债务注释 artifact**，形成 **30 个可分配 code**，共记录 **938 个 artifact–code assignment**。全部 856 个 artifact 均已编码，未决 0 个。允许在存在彼此独立证据时进行多重编码，因此类别覆盖数之和可以超过 artifact 数。

本 codebook 来自逐条完整阅读冻结材料、逐篇 memo、开放编码、持续比较和逐条 assignment 复核。关键词、正则、聚类和脚本没有用于决定类别；脚本只做格式转换、重复复核裁定和一致性校验。

## 范围与限制

- 覆盖范围是冻结材料中的全部文本；未读取的外链、附件和图片不作推断。
- 单一 AI 编码，未经人工审核，也不构成独立双编码。
- code 表示材料支持的主题、机制或证据状态，不等于确认违规、缺陷已复现或修复已完成。

## 类别一览

| Code | 名称 | Artifacts |
|---|---|---:|
| SD01 | known correctness defect or runtime failure | 15 |
| SD02 | unverified behavior, comprehension, or suspected defect | 76 |
| SD03 | open design, organizational, or speculative proposal | 50 |
| SD04 | unimplemented named capability or api-parity gap | 122 |
| SD05 | deferred feature activation or restoration | 6 |
| SD06 | component integration or workflow wiring gap | 4 |
| SD07 | configuration externalization, parameterization, or argument propagation | 29 |
| SD08 | redundant or inert parameter or api surface debt | 4 |
| SD09 | validation, guard, contract, or diagnostic feedback gap | 40 |
| SD10 | test coverage, compatibility, or tooling infrastructure debt | 54 |
| SD11 | documentation, observability, or reporting gap | 28 |
| SD12 | self-labeled hack, shared-state, or coupling smell | 22 |
| SD13 | test-only scaffolding in production code | 3 |
| SD14 | deferred structural refactor, representation, or interface redesign | 47 |
| SD15 | structural relocation, extraction, duplication, coupling, or canonical migration | 32 |
| SD16 | naming or api-cleanup debt | 14 |
| SD17 | performance, idiom, or redundant recomputation debt | 34 |
| SD18 | external-dependency workaround or cross-file or external-source debt | 44 |
| SD19 | methodological or domain-assumption concern | 14 |
| SD20 | alternative algorithm, model, or heuristic quality debt | 23 |
| SD21 | device, memory, aliasing, or state-serialization debt | 17 |
| SD22 | packaging, manual-setup, or asset-bundling gap | 4 |
| SD23 | behavioral override or normative policy reversal | 6 |
| SD24 | version- or status-gated removal | 19 |
| SD25 | cleanup, dead-code removal, or unscheduled deletion | 13 |
| SD26 | personal-state or hand-off deferral | 8 |
| SD27 | deferred benchmark or parallelism work | 12 |
| SD28 | enhancement or example-quality desire | 11 |
| SD29 | formatting, style, readability, or organizational cleanup | 9 |
| SD30 | bare or underspecified deferred marker | 178 |

## 使用规则

- 以注释直接表达的债务、未完成工作、设计不确定性或证据状态为单位。
- 不把注释中的关键词当作缺陷确认；范围、意图和证据限制写入逐条 assignment。
- 允许多重编码，只要同一 artifact 中存在彼此独立的可支持主题。

## SD01 — known correctness defect or runtime failure

Comment asserts existing or generated code yields wrong results, mishandles inputs, loses data, breaks an invariant, or throws an exception, and the author treats the behavior as defective.

**Include:** Declarative bug/broken; wrong labels; shadowed logic; empty documents; off-by-one; pasted traceback; confirmed behavior norm not met.

**Exclude:** Style/refactor admissions; missing features; performance wishes; unverified suspicions; open questions; tests absent.

**Support:** 15 artifact(s). 完整列表见 `codebook.json`。

**Boundary:** Contrast with unverified behavior: symptom or concrete wrongness is asserted.

**Example:** `23shades-0030-aaedcebdc` — The author explicitly asserts a bug: predict_proba is changing when it should not. This is a declarative correctness defect with a named symptom (output mutation), not an unverified suspicion.

````text
[todo]: this is a bug; predict_proba should not change
````


## SD02 — unverified behavior, comprehension, or suspected defect

Author lacks confirmation about runtime behavior, input acceptance, concurrency, semantics, why code exists, or suspects a specific structural, shape, traversal, numerical, or theoretical problem without asserting a failure symptom; verification or investigation is deferred.

**Include:** 'check/verify' untested behavior; 'haven't checked'; 'might not work'; 'what does this do?'; suspected stride/alignment or shape mismatch.

**Exclude:** Known defects with symptoms; open design questions; performance benchmarks; committed deletions.

**Support:** 76 artifact(s). 完整列表见 `codebook.json`。

**Boundary:** Named mechanism but no confirmed wrong output; includes comprehension gaps.

**Example:** `23shades-0066-aahhdbjej` — The author states they need to 'find out why' the neg_ prefix is needed, which is a comprehension gap about why existing code exists, with investigation deferred and no defect asserted.

````text
find out why prefix neg_ is needed
````


## SD03 — open design, organizational, or speculative proposal

Author poses an unresolved design, API, placement, suitability, or feature-adoption question, possibly with a provisional answer or hedge, and does not commit to implementation; alternatives remain pending.

**Include:** 'where should this hook be called?'; 'dataframe pass needed?'; 'more flexible signature?'; 'maybe a DefaultEnvironment?'; 'Is that ok?'; modal hedges.

**Exclude:** Empirical checks; concrete missing computations; committed refinements; version-gated removal.

**Support:** 50 artifact(s). 完整列表见 `codebook.json`。

**Boundary:** Question with no committed remedy; committed refactors sans query go to structural codes.

**Example:** `23shades-0011-aageijaai` — The author poses an unresolved design question about whether gains/biases should be trainable, without committing to an implementation or claiming a defect. The decision remains open and is phrased as an open question.

````text
# TODO: do we want gains/biases to be trainable?
````


## SD04 — unimplemented named capability or api-parity gap

A specific named function, input mode, operator, command, module feature, domain class, distribution step, placeholder, or public symbol is absent or partly implemented, including API-parity gaps; work is additive functionality.

**Include:** Missing optimizer/loader/attack/metric; missing 1D or matrix input; NumPy/scipy parity symbols; NOT IMPLEMENTED; 'write resolve method'; ignored weight; empty stub.

**Exclude:** Existing component merely inactive; config exposure; integration plumbing; structural refactor; scope limits not intended to extend.

**Support:** 122 artifact(s). 完整列表见 `codebook.json`。

**Boundary:** New capability named; contrast activation of existing capability.

**Example:** `23shades-0008-aagcbjjcd` — The TODO names a specific missing input mode: landmarks are loaded for the training set but not currently loaded for the validation and test sets, an additive capability gap.

````text
# TODO : load landmarks in validation and test set also.
````


## SD05 — deferred feature activation or restoration

An existing capability is present but switched off in an entry point/configuration, or was dropped during migration and should be enabled, restored, or ported back.

**Include:** 'turn on' mode/flag; built component not switched on; migration tag with reintroduce/port for named capability.

**Exclude:** New capabilities never present; config externalization; input validation; dead-code relocation.

**Support:** 6 artifact(s). 完整列表见 `codebook.json`。

**Boundary:** Capability exists; only gate or restoration missing.

**Example:** `23shades-0159-aajbiahbe` — The TODO sits on an already-constructed audio component and simply says to turn it on, meaning an existing capability is present but gated off in the code path.

````text
self._audio = audio.AudioComponent(self) # TODO turn on
````


## SD06 — component integration or workflow wiring gap

Named existing components are not wired into the workflow, pipeline, or architecture; pending work is composition or plumbing, not a new algorithm.

**Include:** Integrate frontend and model into workflow; call remote model where component exists.

**Exclude:** Adding absent algorithms; structural refactors; documentation.

**Support:** 4 artifact(s). 完整列表见 `codebook.json`。

**Boundary:** Distinct from missing capability: parts exist, just not connected.

**Example:** `23shades-0009-aagdfgjig` — The TODO states that the existing code should be changed to call a remote model, indicating that a named existing component (remote model) is not wired into the current workflow. The pending work is integration or plumbing rather than creating a new algorithm.

````text
# TODO Change to call remote model
````


## SD07 — configuration externalization, parameterization, or argument propagation

A hard-coded, fixed, computed-in-module, workspace-specific, or magic value/path/param/dtype/threshold should be exposed as configuration, derived, or passed to all sibling calls; includes unresolved configurability gaps.

**Include:** Make thresholds/seeds/process counts configurable; move to config; path portability; pass dictionary to all calls; 'hard coded for now'; 'make dtype configurable'.

**Exclude:** Adding wholly new capability; inert parameters; input validation; arbitrary logic relocation; simple naming.

**Support:** 29 artifact(s). 完整列表见 `codebook.json`。

**Boundary:** Value is fixed or propagation incomplete; not behavior change.

**Example:** `23shades-0046-aafchcgjg` — A confidence value is hard-coded to a magic constant 1 directly in the writer rather than derived or configurable, reflecting an unresolved fixed-parameter gap.

````text
"confidence": 1  # todo discussion confidence from GNormPlus is not provided so just putting in here 1
````


## SD08 — redundant or inert parameter or api surface debt

Overlapping configuration knobs should be consolidated/removed, or a named option/parameter has no effect on behavior and silently misleads; API-surface redundancy or unwired config.

**Include:** 'alpha_mean and density overlap - remove one'; explicit 'X is not used' for named option without warning/error.

**Exclude:** Simple renames; adding new parameters; hardcoded constants needing externalization; feature activation.

**Support:** 4 artifact(s). 完整列表见 `codebook.json`。

**Boundary:** Parameter exists but redundant or ineffective.

**Example:** `23shades-0246-aafehehgb` — Two configuration knobs, alpha_mean and density, are stated to overlap, and the proposed remedy is to remove one. This is API-surface redundancy in named parameters, not a missing feature or behavior change.

````text
TODO alpha_mean and density overlap - remove one of them
````


## SD09 — validation, guard, contract, or diagnostic feedback gap

Required guards, type/default checks, shape compatibility, invalid layer combinations, argument contracts, or runtime preconditions are absent, undefined, unsafe, or undiagnosed; includes unresolved isinstance-vs-duck-typing validation debates.

**Include:** Validate/normalize/set defaults; shape match; warn/error for Reshape; disable X without Y; duplicate check; exclusive open.

**Exclude:** Wrong results already produced; inert parameters; documentation; unimplemented code.

**Support:** 40 artifact(s). 完整列表见 `codebook.json`。

**Boundary:** Enforcement or diagnostic is missing; no wrong output asserted.

**Example:** `23shades-0004-aaejjacgf` — The note flags that a US value may in some cases be insufficient to hold the complete number, pointing to a missing guard or capacity precondition rather than an asserted wrong output.

````text
!TODO: In some cases; US is not enough to hold the complete number
````


## SD10 — test coverage, compatibility, or tooling infrastructure debt

Tests are missing, disabled, stubbed, weakly asserting, or failing due to CI/platform/encoding/dependency environment; admitted gap is verification or tooling, not production logic.

**Include:** Add tests; skipped tests; compatibility TODO in tests; placeholder assertions; broken check; GPU mocking; CI/encoding failures.

**Exclude:** Production defects; stale docs; test-message wording; verification of named invariant in production.

**Support:** 54 artifact(s). 完整列表见 `codebook.json`。

**Boundary:** Concern confined to test code/harness/tooling.

**Example:** `23shades-0019-aaigjhibg` — The TODO sits in a chainerx unit test file and says 'Fix compatibility', indicating a test-harness/platform compatibility gap rather than production logic. The concern is confined to test code.

````text
((); 0); # TODO(sonots): Fix compatibility
````


## SD11 — documentation, observability, or reporting gap

Deferred work is to write docs/docstrings/README/tutorials, explain an opaque parameter, clarify test messages, or add logging, timing, warnings, or reporting output; behavior is not claimed wrong.

**Include:** Update docs; create docstring; 'figure out what size does'; better test message; charts/summary/json output; add warning/logging.

**Exclude:** Runtime error behavior changes; missing tests; inert parameters; core logic defects.

**Support:** 28 artifact(s). 完整列表见 `codebook.json`。

**Boundary:** Communicative or observation output, not control flow.

**Example:** `23shades-0018-aajcabgbe` — The TODO proposes turning the phantom-generation code into a tutorial, which is documentation/educational output rather than a code-behavior change. It defers writing instructional material.

````text
#TODO: this can become a nice tutorial for generating phantoms
````


## SD12 — self-labeled hack, shared-state, or coupling smell

Author labels code a hack/kludge/for-now or mutable shared/global state that should be local, or code that exists solely to satisfy another module's method/flag, admitting hidden coupling.

**Include:** Hack/kludge labels; avoid module-level global; make attribute not part of self; block exists for another file's method.

**Exclude:** Known defects; micro-optimizations; missing state propagation; dead-code relocation.

**Support:** 22 artifact(s). 完整列表见 `codebook.json`。

**Boundary:** Author flags the smell; no concrete defect claimed.

**Example:** `23shades-0005-aaebbecaa` — The author self-labels the SVG-centering approach as a 'Hack', explicitly acknowledging a kludge used to work around broken justify-content behavior.

````text
# Hack to center SVG as justify-content is broken:
````


## SD13 — test-only scaffolding in production code

A parameter, constant, or branch exists only to satisfy tests but lives in shipped application code; test concern mixed into production.

**Include:** 'for testing only!' on production GUI/config parameter; test-convenience hardcode.

**Exclude:** Test-file compatibility workarounds; feature flags unrelated to tests.

**Support:** 3 artifact(s). 完整列表见 `codebook.json`。

**Boundary:** Scaffolding shipped in app code, not test files.

**Example:** `23shades-0022-aahdfibcf` — The comment explicitly labels 'nrows' as existing 'for testing only!' inside a production GUI module (interactive_summary.py). This is test-convenience scaffolding shipped in application code.

````text
@todo nrows is for testing only!
````


## SD14 — deferred structural refactor, representation, or interface redesign

Deferred change to data representation, object model, local code shape, public signature/input contract, or abstraction level (dict to tuple, split functions, separate data from metadata, narrow over-general implementation, lighter identifier).

**Include:** Return dict to list/tuple; named tuple/enum; split block; separate metadata from data; parameterize class attributes; pass id instead of object.

**Exclude:** Pure identifier renames; performance substitutes; adding missing features; class/file relocation.

**Support:** 47 artifact(s). 完整列表见 `codebook.json`。

**Boundary:** Reshapes data contract or local code structure, no movement.

**Example:** `23shades-0003-aaejjbhji` — The note suggests an empty dictionary would suffice instead of the current structure, which is a deferred change to the local data representation chosen in the code.

````text
!TODO: An empty dictionary would actually also do here ... despite the fact that
````


## SD15 — structural relocation, extraction, duplication, coupling, or canonical migration

Existing code is misplaced, wrongly partitioned, duplicated, entangled across layers, or bespoke where a library abstraction exists; remedy is move, extract into class/file, consolidate, delete, decouple, or propagate canonical change.

**Include:** Separate class/file; move to backend; merge duplicate scripts; use standard library; 'add to other loaders too'; decouple DDP from SLURM; unify data resources.

**Exclude:** Local representation choices; performance-only work; API-breaking input redesign; pure renames; dead-code deletion without relocation.

**Support:** 32 artifact(s). 完整列表见 `codebook.json`。

**Boundary:** Code or resource moves/merges/deduplicates; target named.

**Example:** `23shades-0001-aahiieiig` — The comment states the functions are shared by multiple algorithms and should be refactored properly, indicating existing code is entangled and the remedy is reorganization/consolidation rather than a new capability or fix.

````text
Functions used by more than one algorithm || TODO refactor properly later
````


## SD16 — naming or api-cleanup debt

Proposed rename of an identifier, parameter, field, or option for consistency, spelling, or convention alignment; primarily nomenclature and public-surface tidiness.

**Include:** 'change normalizazion_database to normalise'; 'random_state to rng'; 'sizes to size?'; standardizing '_offset' vs 'offset'.

**Exclude:** Conceptual/representation refactors; adding new parameters; removing inert parameters.

**Support:** 14 artifact(s). 完整列表见 `codebook.json`。

**Boundary:** Pure name change, no contract shape change; signature narrowing goes elsewhere.

**Example:** `23shades-0076-aajfajibh` — The FIXME asks to homogenize the meaning of the `margin` parameter, which is parameter/API-surface consistency cleanup. It names no wrong behavior or missing capability; the debt is semantic naming/API tidiness around a public parameter.

````text
FIXME homogeneize the meaning of margin parameter
````


## SD17 — performance, idiom, or redundant recomputation debt

Working code is inefficient in time/memory or non-idiomatic, performs redundant recomputation or initialization, or artifact names a faster/cheaper primitive, vectorization, in-place rewrite, lazy loading, or complexity concern.

**Include:** np.partition; work inplace; broadcast; O(N); avoid CSR; memory notes; save grids once; config loaded once.

**Exclude:** Structural refactors for style; adding GPU support as capability; correctness verification; algorithmic redesign beyond spot optimization.

**Support:** 34 artifact(s). 完整列表见 `codebook.json`。

**Boundary:** Cost or repeated work named; behavior unchanged.

**Example:** `23shades-0017-aaffedgad` — The TODO asks to 'improve the copying of parameters', naming a copying operation that is presumably inefficient or awkward; the target is a cheaper/cleaner copy mechanism, with no correctness fault claimed. This is performance/idiom debt about redundant or costly copying.

````text
#TODO: improve the copying of parameters
````


## SD18 — external-dependency workaround or cross-file or external-source debt

Local code compensates for a named third-party/upstream/rendering/library/version constraint or lags external API drift; or debt originates in another file, external repo, or informal source.

**Include:** Library issue IDs; ONNX-conditioned change; svhn val-set workaround; 'TODO for replacer.py'; backward-compat shims for CPython/pandas bug.

**Exclude:** Self-labeled hacks without external cause; test-environment adaptations; local correctness defects.

**Support:** 44 artifact(s). 完整列表见 `codebook.json`。

**Boundary:** Cause external; local fix is stopgap.

**Example:** `23shades-0005-aaebbecaa` — The workaround exists because a named external rendering feature (justify-content) is broken, so the local code compensates for an upstream constraint.

````text
# Hack to center SVG as justify-content is broken:
````


## SD19 — methodological or domain-assumption concern

Current statistical/algorithmic approach or WIP feature rests on a strong dataset-wide or domain assumption that may not generalize; documented inline without concrete fix.

**Include:** 'We are conditioning on...'; questionable reward assumptions; WIP 'assumes all sequences...'; restrictive preconditions.

**Exclude:** Concrete failing input combinations; known defects; performance; missing features.

**Support:** 14 artifact(s). 完整列表见 `codebook.json`。

**Boundary:** Concern is assumption validity, not implementation bug.

**Example:** `23shades-0045-aajdcegja` — The docstring documents a dataset/module-wide assumption: all diff tools assume notebooks are already converted to the same format version (v4). This is a strong precondition that may not generalize and is noted inline without a concrete fix.

````text
All diff tools here currently assumes the notebooks have already been
````


## SD20 — alternative algorithm, model, or heuristic quality debt

Artifact names a specific alternative mathematical formulation/algorithmic option, says a core algorithm or heuristic should be improved, or proposes changing a named model capacity/hyperparameter from a hunch; no failing input recorded.

**Include:** 'Dehaze with 1/t'; improve pruner/scheduler; 'double num_filters'; 'better job guessing defaults'; 'improve number parsing'.

**Exclude:** Spot performance vectorization; correctness fixes; adding missing input-shape support; scalar config externalization.

**Support:** 23 artifact(s). 完整列表见 `codebook.json`。

**Boundary:** Approach or default quality is target, not a fixed constant.

**Example:** `23shades-0006-aaahbghib` — The comment proposes using a regex 'or something' as an alternative approach to the current ad-hoc parsing, naming a better formulation/method for the logic.

````text
# hackier; fixme to use regex or something
````


## SD21 — device, memory, aliasing, or state-serialization debt

Code makes a suboptimal hardware/device decision, has aliasing/copy-semantics uncertainty, unresolved reference-count ownership, import-cycle blocker, or fails to pass values/checkpoints across process boundaries.

**Include:** use is_cuda for GPU; 'is incref required?'; __deepcopy__; 'copy ?'; import issue; 'pass best score'; incomplete checkpoint state.

**Exclude:** Generic performance copy-removal; confirmed leak; packaging metadata; general cross-process logging.

**Support:** 17 artifact(s). 完整列表见 `codebook.json`。

**Boundary:** State movement across hardware, memory, or process.

**Example:** `23shades-0176-aadhfdfce` — The concern is passing/updating loss history state, i.e., state propagation across the run rather than a pure algorithm. The note addresses maintaining state consistency for loss history.

````text
this is needed to update loss history
````


## SD22 — packaging, manual-setup, or asset-bundling gap

A packaging manifest lacks required declarations, a setup/provisioning step is delegated to the user, or generated output depends on external assets/CDNs that should be bundled so output is self-contained.

**Include:** setup.py install_requires TODOs; incomplete pip installs; 'please download the dataset from'; include mpld3 JS libs; CDN references.

**Exclude:** Runtime capability gaps; documentation gaps; external library limitation.

**Support:** 4 artifact(s). 完整列表见 `codebook.json`。

**Boundary:** Distribution or self-containment concern.

**Example:** `23shades-0052-aaahbjdic` — The comment concerns package_deps in setup.py - packaging manifest declarations - so the issue sits in distribution/packaging setup.

````text
apparently package_deps are broken in 3.4
````


## SD23 — behavioral override or normative policy reversal

Current behavior is too aggressive, strict, or a configuration choice may be wrong; gating/relaxing is proposed, or a normative rule current code should adopt is asserted with relatively strong commitment.

**Include:** 'do not replace unless explicitly noticed'; 'don't make these a constant initializer'; 'dummy_na=False is what you want'; 'should not log nested parameters'.

**Exclude:** Missing capability; validation-only asks; correctness defect with concrete symptom; hedged suggestions.

**Support:** 6 artifact(s). 完整列表见 `codebook.json`。

**Boundary:** Policy change committed or strongly asserted.

**Example:** `23shades-0074-aajfadgji` — The FIXME proposes changing the current normalization policy by not applying L2 normalization for every metric. It is a relatively strong normative rule about desired behavior, with no concrete failing input or wrong output asserted.

````text
FIXME don't l2_normalize for any metric
````


## SD24 — version- or status-gated removal

Removal or substitution of code is tied to a release version, API experimental status, or deprecation state; debt is time-bounded or status-bounded with no re-enablement.

**Include:** 'in 1.1'; 'Remove in 0.26'; 'v1.3.0'; 'remove once estimator is no longer experimental'.

**Exclude:** Unscheduled cleanup; re-enablement or restoration of working capability; external library upgrade alone.

**Support:** 19 artifact(s). 完整列表见 `codebook.json`。

**Boundary:** Trigger is version/status; contrast activation code for re-enablement.

**Example:** `23shades-0061-aagfgggge` — The pending work is explicitly tied to a release status ('coming in next release'), which is a status-gated deferral of the addition.

````text
(TODO: coming in next release)
````


## SD25 — cleanup, dead-code removal, or unscheduled deletion

Working code should be deleted, de-duplicated locally, renamed locally, or tidied without claiming behavioral fault; removal or cleanup has no version, status, or named replacement trigger.

**Include:** 'clean up these initialization'; 'get rid of' code; 'remove timestamp_series_type'; vague 'deal with better'.

**Exclude:** Coupling or relocation with a named target; version/status-gated removal; magic constants needing derivation; structural consolidation.

**Support:** 13 artifact(s). 完整列表见 `codebook.json`。

**Boundary:** Deletion with no fault or relocation target.

**Example:** `23shades-0058-aaahbfbhe` — The author questions whether the code is still needed and floats deprecation, which is an unscheduled cleanup/deletion of possibly working code with no behavioral fault named and no version or status trigger.

````text
DEPRICATE? I don't think this is needed anymore
````


## SD26 — personal-state or hand-off deferral

TODO postpones work by citing author's momentary personal state (sleepiness, lack of time), waiting on a stated precondition, or delegating to another collaborator, without claiming a defect.

**Include:** 'too sleepy'; 'no time today'; 'can you?'; 'I can't manage'; waits on base distributions; 'set check_hash to True on final model'.

**Exclude:** Version-gated removal; open design choices; generic deferral without handoff or precondition.

**Support:** 8 artifact(s). 完整列表见 `codebook.json`。

**Boundary:** Deferral rationale is logistical or delegated.

**Example:** `23shades-0008-aagcbjjcd` — The TODO postpones the work by citing the author's momentary personal state ('too sleepy to do it today'), a logistical deferral rather than a claimed defect.

````text
# TODO : load landmarks in validation and test set also. I'm too sleepy to do it today -_- zzz... zzz...
````


## SD27 — deferred benchmark or parallelism work

Empirical comparison, measurement, optimization, timing, parallelization, or incremental infrastructure work is outstanding; no correctness problem is alleged.

**Include:** 'compare the performance!'; 'very inefficient'; 'TODO: parallelize'; 'try without copying'.

**Exclude:** Verification by reading code; suspected correctness defects; device-capability handling; theoretical numerical precision.

**Support:** 12 artifact(s). 完整列表见 `codebook.json`。

**Boundary:** Measurement or concurrency only.

**Example:** `23shades-0086-aaicdjedb` — The note proposes using n_jobs in this code path, which is a parallelization/performance improvement rather than a correctness fix. It names outstanding concurrency work with no alleged wrong result.

````text
FIXME: can use n_jobs here too
````


## SD28 — enhancement or example-quality desire

Desirable improvement to working code, examples, or data that is not a defect: better illustrative dataset, optional multi-GPU support, example-quality suggestion.

**Include:** 'use faithful dataset'; future multi-GPU enhancement; example-quality suggestion.

**Exclude:** Broken behavior; absent core functionality; generic hardcoding smell.

**Support:** 11 artifact(s). 完整列表见 `codebook.json`。

**Boundary:** Nice-to-have, not gap or bug.

**Example:** `23shades-0036-aaibigjdc` — The TODO asks to use the 'faithful' dataset in the GMM plotting example, which is an example-quality improvement to working code rather than a defect or missing capability. The example functions; the desire is a nicer illustrative dataset.

````text
TODO: use the faithful dataset
````


## SD29 — formatting, style, readability, or organizational cleanup

The admitted debt is cosmetic or presentational: formatting/lint conformance, banner or grouping tidiness, or a low-confidence claim that code is hard to read, misnamed stylistically, or "could be smarter" without naming a speed, correctness or structural mechanism.

**Include:** Formatting/lint TODO; reorganize banners or grouping; "dense and confusing, clean up"; "change to functional style"; "could be smarter" with no named property or target.

**Exclude:** Deletion of working code with no fault (SD23); structural factoring or representation change (SD14/SD15); a named performance cost (SD17); bare marker with no object at all (SD21).

**Support:** 9 artifact(s). 完整列表见 `codebook.json`。

**Boundary:** If a concrete target or mechanism is named, use the specific code; this code is the residual presentational/low-confidence wish.

**Example:** `23shades-0010-aaaedagad` — The comment suggests a potential rewrite of names, indexing, and UUID handling without naming a concrete correctness, structural, or performance mechanism. It is a low-confidence presentational or cleanup wish.

````text
# TODO May want to rewrite name; index; uuid; etc.
````


## SD30 — bare or underspecified deferred marker

TODO has only a marker, author tag, lone noun/symbol/fragment, pronoun, truncated fragment, generic phrase, or self-doubting note with no reconstructable action or target; only debt location is inferable.

**Include:** '!TODO'; lone 'TODO'; author tag; 'market value'; 'documentation'; 'sweep'; 'debug'; 'dtype'; 'maxpool?'; 'maybe done'.

**Exclude:** Any interpretable defect, feature, mechanism, or direction; named verification target.

**Support:** 178 artifact(s). 完整列表见 `codebook.json`。

**Boundary:** Merge only when nothing concrete can be reconstructed.

**Example:** `23shades-0002-aaehidhih` — The artifact consists solely of a bare TODO marker with no further text, so no concrete action, target, or mechanism can be reconstructed.

````text
!TODO
````

## 配套文件

- `codebook.json`：结构化定义、支持案例、计数、代表证据和方法元数据。
- `codebook.csv`：表格化 codebook。
- `assignments.json` / `assignments.csv`：每个 artifact 的 code、理由、逐字证据、来源与证据限制。
- `taxonomy.json`：HOW-style 类别树。
- `results.json`：冻结材料正文与最终编码的逐条组合。
