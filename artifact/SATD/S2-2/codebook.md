# SATD / S2-2

Schema: `coda.artifact.v1`. Artifacts: **856**; codes: **20**; artifact–code assignments: **1580**.

This package uses the common seven-file format. All existing coding decisions, evidence and limitations are preserved. Additional source-specific fields are retained in `extensions`; original codebook text is retained in `codebook.json` metadata extensions and the local pre-conversion backup.

## Scope and method

逐条完整阅读、开放编码、持续比较、逐条人工 assignment；程序仅转换格式并验证。

单一 AI 编码；机械一致性检查不构成人工双重编码或语义准确性证明。

## Codes

| Code | Name | Artifacts |
|---|---|---:|
| SATD01 | Missing or expanded functionality | 157 |
| SATD02 | Known correctness defect | 65 |
| SATD03 | Input, type, shape, or boundary coverage | 112 |
| SATD04 | Testing or verification debt | 67 |
| SATD05 | Documentation, example, or user guidance debt | 20 |
| SATD06 | Performance or resource-efficiency debt | 57 |
| SATD07 | Architecture, modularity, or responsibility refactoring | 86 |
| SATD08 | API, contract, naming, or behavioral-design debt | 149 |
| SATD09 | Configuration, defaults, or flexibility debt | 51 |
| SATD10 | Compatibility, dependency, version, or external-workaround debt | 128 |
| SATD11 | Cleanup, removal, deprecation, or dead-code debt | 83 |
| SATD12 | Maintainability, readability, or local code-quality debt | 45 |
| SATD13 | Algorithm, model, data, or result-quality debt | 71 |
| SATD14 | Robustness, validation, error handling, or recovery debt | 48 |
| SATD15 | Observability, logging, diagnostics, or provenance debt | 21 |
| SATD16 | Concurrency, parallelism, distribution, or device-scaling debt | 31 |
| SATD17 | Numerical precision, stability, or mathematical-representation debt | 22 |
| SATD18 | Investigation, uncertainty, rationale, or design-choice debt | 184 |
| SATD19 | Build, packaging, deployment, or operational-infrastructure debt | 17 |
| SATD20 | Insufficiently specified or non-actionable evidence | 166 |

## SATD01 — Missing or expanded functionality

A capability, operation, integration, data path, model component, or supported scenario is absent, incomplete, or explicitly planned for implementation/extension.

- Include: “implement …”, unsupported backbones/types/operations, unfinished functionality, missing integrations.
- Exclude: a capability exists but behaves incorrectly (`SATD02`); only tests are missing (`SATD04`); the request is solely to expose an existing choice as configuration (`SATD09`).
- Boundary/examples: `23shades-0564-aafjicajb`, “Implement Conv Transpose.”
- Supporting artifacts: 157; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "23shades-0007-aaaegfgeb",
    "row": 7,
    "field": "comment_text",
    "quote": "reverse bw",
    "interpretation": "拼接前反转bw是未完成步骤，也暗示当前处理顺序不符合预期。"
  }
]
````

## SATD02 — Known correctness defect

The artifact reports behavior known or strongly asserted to be wrong, inconsistent with an expected result, or already failing.

- Include: wrong results, ignored required values, off-by-one errors, broken behavior, explicit fixes to known faults.
- Exclude: a possible defect still requiring investigation (`SATD18`); unsupported inputs without an observed wrong result (`SATD03`); numerical overflow/precision mechanisms (`SATD17`, optionally also this code when failure is explicit).
- Boundary/examples: `23shades-0627-aaidgcaed`, an admitted off-by-one error.
- Supporting artifacts: 65; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "23shades-0007-aaaegfgeb",
    "row": 7,
    "field": "comment_text",
    "quote": "reverse bw",
    "interpretation": "拼接前反转bw是未完成步骤，也暗示当前处理顺序不符合预期。"
  }
]
````

## SATD03 — Input, type, shape, or boundary coverage

The implementation does not cover a class of inputs, data types, shapes, formats, values, or boundary conditions.

- Include: `None`, strings, tuples, dictionaries, short names, multiple speakers, dynamic shapes, empty/zero/singleton cases, unsupported file/data variants.
- Exclude: a wholly new domain capability (`SATD01`); validation or recovery is the central issue (`SATD14`); only test coverage is missing (`SATD04`).
- Boundary/examples: `23shades-0552-aabfjgehb`, “handle Nones.”
- Supporting artifacts: 112; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "23shades-0004-aaejjacgf",
    "row": 4,
    "field": "comment_text",
    "quote": "In some cases",
    "interpretation": "当前US表示在某些数值范围下容量不足，既是边界规模覆盖限制，也是数值表示范围问题。"
  }
]
````

## SATD04 — Testing or verification debt

Automated tests, assertions, validation experiments, coverage, or confirmation of correctness are absent or insufficient.

- Include: untested code, missing test cases, weak assertions, requests to verify whether behavior works, hardware-dependent tests that cannot run broadly.
- Exclude: runtime input validation (`SATD14`); diagnostic logging (`SATD15`); an already confirmed implementation defect (`SATD02`) unless missing regression coverage is also explicit.
- Boundary/examples: `23shades-0571-aagfabdib`, missing `test_to_set_fw_dic()` test code.
- Supporting artifacts: 67; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "23shades-0019-aaigjhibg",
    "row": 19,
    "field": "comment_text",
    "quote": "Fix compatibility",
    "interpretation": "数学测试存在未说明目标环境的兼容问题，兼具测试覆盖与依赖/后端兼容债务。"
  }
]
````

## SATD05 — Documentation, example, or user guidance debt

Explanations, API documentation, tutorials, examples, comments, user-facing instructions, or source references are missing, incomplete, or misleading.

- Include: placeholder docs, incomplete download instructions, examples needing replacement, missing provenance references.
- Exclude: runtime error messages or logs (`SATD15`); uncertainty internal to the implementer (`SATD18`); packaging metadata (`SATD19`).
- Boundary/examples: `23shades-0635-aaedbcjji`, an incomplete dataset-download instruction.
- Supporting artifacts: 20; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "23shades-0018-aajcabgbe",
    "row": 18,
    "field": "comment_text",
    "quote": "can become a nice tutorial",
    "interpretation": "现有phantom生成能力尚未转化为教程，债务位于用户教育材料。"
  }
]
````

## SATD06 — Performance or resource-efficiency debt

Runtime, memory, I/O, algorithmic complexity, redundant computation, copying, loading, or resource use is known or suspected to be inefficient.

- Include: slow loops, O(N²) work, excessive memory, eager loading, unnecessary full-distribution computation, repeated caching, GPU utilization for efficiency.
- Exclude: parallel/distributed capability is itself the central missing mechanism (`SATD16`, which may co-occur); numerical correctness (`SATD17`); general code elegance without an efficiency claim (`SATD12`).
- Boundary/examples: `23shades-0733-aajacfjii`, O(N²) behavior that may be too slow for large graphs.
- Supporting artifacts: 57; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "23shades-0037-aajffhihe",
    "row": 37,
    "field": "comment_text",
    "quote": "It is incomplete",
    "interpretation": "unparser只覆盖有限AST节点，同时考虑迁移到更快的_ast表示；功能、性能和Python AST依赖迁移均明确，但方案仍未确定。"
  }
]
````

## SATD07 — Architecture, modularity, or responsibility refactoring

Component boundaries, dependency direction, module ownership, lifecycle structure, duplication, or separation of responsibilities requires redesign or refactoring.

- Include: circular dependencies, moving logic to another module, extracting functions, breaking up modules, de-duplicating implementations, separating functional and stateful layers.
- Exclude: local readability/style cleanup (`SATD12`); public parameter/name/return-contract changes (`SATD08`); simple removal of obsolete code (`SATD11`).
- Boundary/examples: `23shades-0640-aaghjahhi`, “Properly break circular dependencies.”
- Supporting artifacts: 86; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "23shades-0001-aahiieiig",
    "row": 1,
    "field": "comment_text",
    "quote": "Functions used by more than one algorithm",
    "interpretation": "共享算法函数的组织被明确标为以后妥善重构，核心是跨算法工具的模块与职责边界。"
  }
]
````

## SATD08 — API, contract, naming, or behavioral-design debt

A callable interface, return structure, lifecycle hook, ownership rule, naming convention, data-model contract, or externally visible behavior is unclear, inconsistent, or needs redesign.

- Include: renaming parameters/modules, changing return types, deciding in-place semantics, correcting responsibility in a functional API, standardizing field names.
- Exclude: adding a configuration knob to vary an otherwise clear behavior (`SATD09`); internal module decomposition (`SATD07`); unsupported data variants (`SATD03`).
- Boundary/examples: `23shades-0575-aaejcccgj`, a functional API should not instantiate an `nn.Module`.
- Supporting artifacts: 149; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "23shades-0010-aaaedagad",
    "row": 10,
    "field": "comment_text",
    "quote": "May want to rewrite",
    "interpretation": "name/index/uuid等标识设计可能重写，涉及数据/API契约，但语气表明方案尚未确定。"
  }
]
````

## SATD09 — Configuration, defaults, or flexibility debt

A hard-coded choice should be configurable, a default is absent/arbitrary/questionable, or callers need control over an existing behavior.

- Include: configurable dtype, optional reshape/copy, default monitors, magic values that should come from data/configuration, arbitrary sample counts.
- Exclude: unsupported input types (`SATD03`); a new capability rather than control over an existing one (`SATD01`); a naming/return-contract change (`SATD08`).
- Boundary/examples: `23shades-0590-aafiggbeh`, “make configurable.”
- Supporting artifacts: 51; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "23shades-0012-aafaehach",
    "row": 12,
    "field": "comment_text",
    "quote": "Set name",
    "interpretation": "name为None时应使用functionality.__name__补充默认名称，属于明确默认行为缺口。"
  }
]
````

## SATD10 — Compatibility, dependency, version, or external-workaround debt

Code is constrained by, adapting to, or temporarily working around an external library, platform, protocol, repository, model version, or backward-compatibility requirement.

- Include: dependency-version workarounds, upstream issues, Python-version compatibility, API migrations, behavior retained until an external capability arrives, cross-repository coordinated changes.
- Exclude: internal deprecation with no external/version condition (`SATD11`); build/package declarations (`SATD19`); concurrency limitations (`SATD16`).
- Boundary/examples: `23shades-0586-aagdaagij`, temporary preprocessing retained until InceptionResNetV2 is retrained.
- Supporting artifacts: 128; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "23shades-0005-aaebbecaa",
    "row": 5,
    "field": "comment_text",
    "quote": "Hack to center SVG",
    "interpretation": "SVG居中依赖针对失效justify-content的外部布局workaround，且被作者明确称为hack。"
  }
]
````

## SATD11 — Cleanup, removal, deprecation, or dead-code debt

Obsolete, redundant, unused, temporary, debug, compatibility, or deprecated material is explicitly slated for removal or retirement.

- Include: version-scheduled deletion, dead-code candidates, removing debug tasks, cleanup after an experiment or migration.
- Exclude: replacing a flawed architecture while preserving functionality (`SATD07`); deletion whose purpose is only guessed from an underspecified “remove” (`SATD20` also applies); upstream/version compatibility conditions (`SATD10` may co-occur).
- Boundary/examples: `23shades-0656-aaefbgdbg`, “remove dummy / debug tasks.”
- Supporting artifacts: 83; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "23shades-0022-aahdfibcf",
    "row": 22,
    "field": "comment_text",
    "quote": "nrows is for testing only",
    "interpretation": "仅供测试的nrows混入一般实现，需要隔离职责并清理测试专用接口。"
  }
]
````

## SATD12 — Maintainability, readability, or local code-quality debt

The admitted problem is local clarity, complexity, style, duplication at a small scale, formatting, elegance, or maintainability without a more specific architectural or functional claim.

- Include: ugly/dense/confusing code, “make nicer,” local cleanup, prettier implementation, unexplained hacks when maintainability is explicit.
- Exclude: module/dependency restructuring (`SATD07`); performance claims (`SATD06`); an artifact too vague to identify even local code quality (`SATD20`).
- Boundary/examples: `23shades-0742-aahedhicb`, dense and confusing code needing cleanup.
- Supporting artifacts: 45; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "23shades-0003-aaejjbhji",
    "row": 3,
    "field": "comment_text",
    "quote": "An empty dictionary would actually also do here",
    "interpretation": "作者认为当前数据结构可用更简单的空字典替代，属于局部清理；但理由在句中截断，保留证据不足。"
  }
]
````

## SATD13 — Algorithm, model, data, or result-quality debt

The selected algorithm, learned-model behavior, data quality, heuristic, metric, training strategy, or result quality is inadequate or requires improvement/selection.

- Include: poor model results, questionable hard-example mining, arbitrary heuristics, incomplete training labels, method/backend selection based on quality.
- Exclude: purely computational efficiency (`SATD06`); numerical overflow/precision (`SATD17`); ordinary implementation correctness (`SATD02`).
- Boundary/examples: `23shades-0559-aafdibbge`, inability to obtain good results with the current approach.
- Supporting artifacts: 71; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "23shades-0036-aaibigjdc",
    "row": 36,
    "field": "comment_text",
    "quote": "use the faithful dataset",
    "interpretation": "绘图示例需换成faithful dataset，核心是示例数据的代表性与结果展示质量。"
  }
]
````

## SATD14 — Robustness, validation, error handling, or recovery debt

The implementation lacks input/state validation, safe failure, useful exception behavior, retry/backoff, recovery, or defensive handling of runtime hazards.

- Include: divide-by-zero protection, more specific exceptions, malformed-input prevention, HTTP 429 backoff, defensive copies, validation before an invalid operation.
- Exclude: testing that validation works (`SATD04`); logging only (`SATD15`); unsupported but otherwise valid input kinds (`SATD03`).
- Boundary/examples: `23shades-0596-aagbdjhgb`, making a calculation safe against division by zero.
- Supporting artifacts: 48; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "23shades-0048-aagaijehb",
    "row": 48,
    "field": "comment_text",
    "quote": "add arguments compatibility check",
    "interpretation": "参数组合兼容检查尚未实现，运行前验证不足。"
  }
]
````

## SATD15 — Observability, logging, diagnostics, or provenance debt

Runtime events, timing, failures, origins, or state are insufficiently logged, messaged, measured, or traceable.

- Include: missing log messages/levels, weak error diagnostics, timing instrumentation, source provenance, clearer user-facing failure context.
- Exclude: general documentation (`SATD05`); test assertions (`SATD04`); algorithm metrics used to improve model quality (`SATD13`).
- Boundary/examples: `23shades-0588-aaeiaghhj`, a missing log message.
- Supporting artifacts: 21; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "23shades-0046-aafchcgjg",
    "row": 46,
    "field": "reading_memo.evidence",
    "quote": "confidence is not provided",
    "interpretation": "缺失的上游confidence被硬编码为1，形成不真实默认值并损害置信度来源可追踪性。"
  }
]
````

## SATD16 — Concurrency, parallelism, distribution, or device-scaling debt

Work cannot safely or efficiently execute across threads, processes, workers, devices, batches, or distributed partitions, or lacks the mechanisms to do so.

- Include: parallelization, GPU/multi-GPU handling, multi-thread safety, distributed state transfer, load rebalancing, batched/distributed execution.
- Exclude: performance without a concurrency mechanism (`SATD06`); ordinary blocking calls without a stated concurrency design (`SATD06` or `SATD14` as supported); external device-library compatibility (`SATD10`, optionally co-coded).
- Boundary/examples: `23shades-0631-aaecaicdb`, “parallelize.”
- Supporting artifacts: 31; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "23shades-0049-aagaggihd",
    "row": 49,
    "field": "comment_text",
    "quote": "future enhancement TODO for running on multiple GPU",
    "interpretation": "多GPU运行是明确的未来功能增强，并涉及设备并行扩展。"
  }
]
````

## SATD17 — Numerical precision, stability, or mathematical-representation debt

Floating-point stability, overflow/underflow, precision, scaling, mathematical-domain representation, or numerically safe formulation is inadequate or uncertain.

- Include: precision overflow, log-density versus density, unsafe numerical scaling, unexplained low digits of accuracy.
- Exclude: general wrong logic (`SATD02`); divide-by-zero as a defensive runtime boundary (`SATD14`, unless a broader stability formulation is explicit); tensor shape/type coverage (`SATD03`).
- Boundary/examples: `23shades-0803-aaichjjjg`, avoiding precision overflow.
- Supporting artifacts: 22; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "23shades-0004-aaejjacgf",
    "row": 4,
    "field": "comment_text",
    "quote": "In some cases",
    "interpretation": "当前US表示在某些数值范围下容量不足，既是边界规模覆盖限制，也是数值表示范围问题。"
  }
]
````

## SATD18 — Investigation, uncertainty, rationale, or design-choice debt

The artifact records an unresolved question, unknown cause, uncertain correctness, unclear rationale, technology choice, or need for investigation rather than a settled implementation action.

- Include: “why does this happen?”, “is this needed?”, competing design options, uncertain API behavior, root-cause research, knowledge gaps.
- Exclude: a confirmed defect with a clear action (`SATD02`); an artifact so short that even the question/object is unavailable (`SATD20`); a defined algorithm-quality experiment (`SATD13`, possibly co-coded).
- Boundary/examples: `23shades-0841-aagcbggid`, uncertainty about which implementation direction is best.
- Supporting artifacts: 184; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "23shades-0006-aaahbghib",
    "row": 6,
    "field": "comment_text",
    "quote": "hackier",
    "interpretation": "当前解析方案被认为hacky，计划改用regex或其他办法；具体替代仍未决定。"
  }
]
````

## SATD19 — Build, packaging, deployment, or operational-infrastructure debt

Installation metadata, dependency declarations, archive/build outputs, deployment configuration, artifact release, data acquisition infrastructure, or operational setup is incomplete or needs change.

- Include: missing package requirements, archive-format changes, release integrity configuration, build/deployment environment setup.
- Exclude: runtime library compatibility (`SATD10`); application-level configuration (`SATD09`); model checkpoint semantics (`SATD08` or `SATD01` unless the issue is release infrastructure).
- Boundary/examples: `23shades-0645-aadbbbcgh`, missing package requirements in `setup.py`.
- Supporting artifacts: 17; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "23shades-0025-aajffcjii",
    "row": 25,
    "field": "comment_text",
    "quote": "code formatting issue",
    "interpretation": "明确是20.07发布前的代码格式清理，包含局部可维护性与发布准备维度。"
  }
]
````

## SATD20 — Insufficiently specified or non-actionable evidence

The artifact does not contain enough information to determine a substantive debt category or identify the object/action with defensible specificity.

- Include: empty/bare TODOs, “fix this later,” “U,” truncated fragments whose missing portion contains the needed object, comments that merely explain behavior without admitting a defect or improvement.
- Exclude: short comments that nevertheless name a clear action and object, such as “Implement Conv Transpose” (`SATD01`); uncertainty with an identifiable subject (`SATD18`).
- Boundary/examples: `23shades-0752-aagfegjcg`, the complete admitted comment is only “TODO: U.”
- Supporting artifacts: 166; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "23shades-0002-aaehidhih",
    "row": 2,
    "field": "comment_text",
    "quote": "!TODO",
    "interpretation": "完整材料只有无对象的!TODO，无法防御性地判断具体债务内容。"
  }
]
````

## Files

- `codebook.md`, `codebook.json`, `codebook.csv`: definitions and complete reverse memberships.
- `assignments.json`, `assignments.csv`: one record per artifact, including decisions and evidence.
- `taxonomy.json`: category tree with every code as a leaf.
- `results.json`: supplied full documents aligned to their assignments.

## Original codebook

The original codebook text below preserves run-specific scope, combination rules and qualifications. Links and filenames in that historical text describe the original package; use the seven files above for the normalized interface. The exact original text is also stored in metadata extensions.

# gpt5.6-2 — SATD 最终编码本

本轮覆盖 **856 个 artifact**，形成 **20 个可分配 code**，共记录 **1580 个 artifact–code assignment**。全部 artifact 均已逐件阅读并编码。

本文件按 GPT6-1 七文件发布格式生成。语义判断来自已完成的逐件阅读与人工 assignment；格式转换程序不读取正文选择代码，只负责序列化、计数和一致性核验。

## 类别一览

|Code|类别|覆盖 artifact 数|
|---|---|---:|
|SATD01|Missing or expanded functionality|157|
|SATD02|Known correctness defect|65|
|SATD03|Input, type, shape, or boundary coverage|112|
|SATD04|Testing or verification debt|67|
|SATD05|Documentation, example, or user guidance debt|20|
|SATD06|Performance or resource-efficiency debt|57|
|SATD07|Architecture, modularity, or responsibility refactoring|86|
|SATD08|API, contract, naming, or behavioral-design debt|149|
|SATD09|Configuration, defaults, or flexibility debt|51|
|SATD10|Compatibility, dependency, version, or external-workaround debt|128|
|SATD11|Cleanup, removal, deprecation, or dead-code debt|83|
|SATD12|Maintainability, readability, or local code-quality debt|45|
|SATD13|Algorithm, model, data, or result-quality debt|71|
|SATD14|Robustness, validation, error handling, or recovery debt|48|
|SATD15|Observability, logging, diagnostics, or provenance debt|21|
|SATD16|Concurrency, parallelism, distribution, or device-scaling debt|31|
|SATD17|Numerical precision, stability, or mathematical-representation debt|22|
|SATD18|Investigation, uncertainty, rationale, or design-choice debt|184|
|SATD19|Build, packaging, deployment, or operational-infrastructure debt|17|
|SATD20|Insufficiently specified or non-actionable evidence|166|

## 使用规则

- 每个 artifact 至少一个代码；有独立材料支持时允许多重编码。
- 不从关键词、文件名、标签或关闭状态单独推断语义类别或处理结果。

## SATD01 Missing or expanded functionality

A capability, operation, integration, data path, model component, or supported scenario is absent, incomplete, or explicitly planned for implementation/extension.

- 纳入：“implement …”, unsupported backbones/types/operations, unfinished functionality, missing integrations.
- 排除与边界：a capability exists but behaves incorrectly (`SATD02`); only tests are missing (`SATD04`); the request is solely to expose an existing choice as configuration (`SATD09`).
- 边界说明：`23shades-0564-aafjicajb`, “Implement Conv Transpose.”
- 支持：157 个 artifact；完整列表见 `codebook.json`。
- 代表案例：artifact `23shades-0007-aaaegfgeb`（row 7；完整材料见 `results.json`）。

````text
reverse bw
````

拼接前反转bw是未完成步骤，也暗示当前处理顺序不符合预期。

## SATD02 Known correctness defect

The artifact reports behavior known or strongly asserted to be wrong, inconsistent with an expected result, or already failing.

- 纳入：wrong results, ignored required values, off-by-one errors, broken behavior, explicit fixes to known faults.
- 排除与边界：a possible defect still requiring investigation (`SATD18`); unsupported inputs without an observed wrong result (`SATD03`); numerical overflow/precision mechanisms (`SATD17`, optionally also this code when failure is explicit).
- 边界说明：`23shades-0627-aaidgcaed`, an admitted off-by-one error.
- 支持：65 个 artifact；完整列表见 `codebook.json`。
- 代表案例：artifact `23shades-0007-aaaegfgeb`（row 7；完整材料见 `results.json`）。

````text
reverse bw
````

拼接前反转bw是未完成步骤，也暗示当前处理顺序不符合预期。

## SATD03 Input, type, shape, or boundary coverage

The implementation does not cover a class of inputs, data types, shapes, formats, values, or boundary conditions.

- 纳入：`None`, strings, tuples, dictionaries, short names, multiple speakers, dynamic shapes, empty/zero/singleton cases, unsupported file/data variants.
- 排除与边界：a wholly new domain capability (`SATD01`); validation or recovery is the central issue (`SATD14`); only test coverage is missing (`SATD04`).
- 边界说明：`23shades-0552-aabfjgehb`, “handle Nones.”
- 支持：112 个 artifact；完整列表见 `codebook.json`。
- 代表案例：artifact `23shades-0004-aaejjacgf`（row 4；完整材料见 `results.json`）。

````text
In some cases
````

当前US表示在某些数值范围下容量不足，既是边界规模覆盖限制，也是数值表示范围问题。

## SATD04 Testing or verification debt

Automated tests, assertions, validation experiments, coverage, or confirmation of correctness are absent or insufficient.

- 纳入：untested code, missing test cases, weak assertions, requests to verify whether behavior works, hardware-dependent tests that cannot run broadly.
- 排除与边界：runtime input validation (`SATD14`); diagnostic logging (`SATD15`); an already confirmed implementation defect (`SATD02`) unless missing regression coverage is also explicit.
- 边界说明：`23shades-0571-aagfabdib`, missing `test_to_set_fw_dic()` test code.
- 支持：67 个 artifact；完整列表见 `codebook.json`。
- 代表案例：artifact `23shades-0019-aaigjhibg`（row 19；完整材料见 `results.json`）。

````text
Fix compatibility
````

数学测试存在未说明目标环境的兼容问题，兼具测试覆盖与依赖/后端兼容债务。

## SATD05 Documentation, example, or user guidance debt

Explanations, API documentation, tutorials, examples, comments, user-facing instructions, or source references are missing, incomplete, or misleading.

- 纳入：placeholder docs, incomplete download instructions, examples needing replacement, missing provenance references.
- 排除与边界：runtime error messages or logs (`SATD15`); uncertainty internal to the implementer (`SATD18`); packaging metadata (`SATD19`).
- 边界说明：`23shades-0635-aaedbcjji`, an incomplete dataset-download instruction.
- 支持：20 个 artifact；完整列表见 `codebook.json`。
- 代表案例：artifact `23shades-0018-aajcabgbe`（row 18；完整材料见 `results.json`）。

````text
can become a nice tutorial
````

现有phantom生成能力尚未转化为教程，债务位于用户教育材料。

## SATD06 Performance or resource-efficiency debt

Runtime, memory, I/O, algorithmic complexity, redundant computation, copying, loading, or resource use is known or suspected to be inefficient.

- 纳入：slow loops, O(N²) work, excessive memory, eager loading, unnecessary full-distribution computation, repeated caching, GPU utilization for efficiency.
- 排除与边界：parallel/distributed capability is itself the central missing mechanism (`SATD16`, which may co-occur); numerical correctness (`SATD17`); general code elegance without an efficiency claim (`SATD12`).
- 边界说明：`23shades-0733-aajacfjii`, O(N²) behavior that may be too slow for large graphs.
- 支持：57 个 artifact；完整列表见 `codebook.json`。
- 代表案例：artifact `23shades-0037-aajffhihe`（row 37；完整材料见 `results.json`）。

````text
It is incomplete
````

unparser只覆盖有限AST节点，同时考虑迁移到更快的_ast表示；功能、性能和Python AST依赖迁移均明确，但方案仍未确定。

## SATD07 Architecture, modularity, or responsibility refactoring

Component boundaries, dependency direction, module ownership, lifecycle structure, duplication, or separation of responsibilities requires redesign or refactoring.

- 纳入：circular dependencies, moving logic to another module, extracting functions, breaking up modules, de-duplicating implementations, separating functional and stateful layers.
- 排除与边界：local readability/style cleanup (`SATD12`); public parameter/name/return-contract changes (`SATD08`); simple removal of obsolete code (`SATD11`).
- 边界说明：`23shades-0640-aaghjahhi`, “Properly break circular dependencies.”
- 支持：86 个 artifact；完整列表见 `codebook.json`。
- 代表案例：artifact `23shades-0001-aahiieiig`（row 1；完整材料见 `results.json`）。

````text
Functions used by more than one algorithm
````

共享算法函数的组织被明确标为以后妥善重构，核心是跨算法工具的模块与职责边界。

## SATD08 API, contract, naming, or behavioral-design debt

A callable interface, return structure, lifecycle hook, ownership rule, naming convention, data-model contract, or externally visible behavior is unclear, inconsistent, or needs redesign.

- 纳入：renaming parameters/modules, changing return types, deciding in-place semantics, correcting responsibility in a functional API, standardizing field names.
- 排除与边界：adding a configuration knob to vary an otherwise clear behavior (`SATD09`); internal module decomposition (`SATD07`); unsupported data variants (`SATD03`).
- 边界说明：`23shades-0575-aaejcccgj`, a functional API should not instantiate an `nn.Module`.
- 支持：149 个 artifact；完整列表见 `codebook.json`。
- 代表案例：artifact `23shades-0010-aaaedagad`（row 10；完整材料见 `results.json`）。

````text
May want to rewrite
````

name/index/uuid等标识设计可能重写，涉及数据/API契约，但语气表明方案尚未确定。

## SATD09 Configuration, defaults, or flexibility debt

A hard-coded choice should be configurable, a default is absent/arbitrary/questionable, or callers need control over an existing behavior.

- 纳入：configurable dtype, optional reshape/copy, default monitors, magic values that should come from data/configuration, arbitrary sample counts.
- 排除与边界：unsupported input types (`SATD03`); a new capability rather than control over an existing one (`SATD01`); a naming/return-contract change (`SATD08`).
- 边界说明：`23shades-0590-aafiggbeh`, “make configurable.”
- 支持：51 个 artifact；完整列表见 `codebook.json`。
- 代表案例：artifact `23shades-0012-aafaehach`（row 12；完整材料见 `results.json`）。

````text
Set name
````

name为None时应使用functionality.__name__补充默认名称，属于明确默认行为缺口。

## SATD10 Compatibility, dependency, version, or external-workaround debt

Code is constrained by, adapting to, or temporarily working around an external library, platform, protocol, repository, model version, or backward-compatibility requirement.

- 纳入：dependency-version workarounds, upstream issues, Python-version compatibility, API migrations, behavior retained until an external capability arrives, cross-repository coordinated changes.
- 排除与边界：internal deprecation with no external/version condition (`SATD11`); build/package declarations (`SATD19`); concurrency limitations (`SATD16`).
- 边界说明：`23shades-0586-aagdaagij`, temporary preprocessing retained until InceptionResNetV2 is retrained.
- 支持：128 个 artifact；完整列表见 `codebook.json`。
- 代表案例：artifact `23shades-0005-aaebbecaa`（row 5；完整材料见 `results.json`）。

````text
Hack to center SVG
````

SVG居中依赖针对失效justify-content的外部布局workaround，且被作者明确称为hack。

## SATD11 Cleanup, removal, deprecation, or dead-code debt

Obsolete, redundant, unused, temporary, debug, compatibility, or deprecated material is explicitly slated for removal or retirement.

- 纳入：version-scheduled deletion, dead-code candidates, removing debug tasks, cleanup after an experiment or migration.
- 排除与边界：replacing a flawed architecture while preserving functionality (`SATD07`); deletion whose purpose is only guessed from an underspecified “remove” (`SATD20` also applies); upstream/version compatibility conditions (`SATD10` may co-occur).
- 边界说明：`23shades-0656-aaefbgdbg`, “remove dummy / debug tasks.”
- 支持：83 个 artifact；完整列表见 `codebook.json`。
- 代表案例：artifact `23shades-0022-aahdfibcf`（row 22；完整材料见 `results.json`）。

````text
nrows is for testing only
````

仅供测试的nrows混入一般实现，需要隔离职责并清理测试专用接口。

## SATD12 Maintainability, readability, or local code-quality debt

The admitted problem is local clarity, complexity, style, duplication at a small scale, formatting, elegance, or maintainability without a more specific architectural or functional claim.

- 纳入：ugly/dense/confusing code, “make nicer,” local cleanup, prettier implementation, unexplained hacks when maintainability is explicit.
- 排除与边界：module/dependency restructuring (`SATD07`); performance claims (`SATD06`); an artifact too vague to identify even local code quality (`SATD20`).
- 边界说明：`23shades-0742-aahedhicb`, dense and confusing code needing cleanup.
- 支持：45 个 artifact；完整列表见 `codebook.json`。
- 代表案例：artifact `23shades-0003-aaejjbhji`（row 3；完整材料见 `results.json`）。

````text
An empty dictionary would actually also do here
````

作者认为当前数据结构可用更简单的空字典替代，属于局部清理；但理由在句中截断，保留证据不足。

## SATD13 Algorithm, model, data, or result-quality debt

The selected algorithm, learned-model behavior, data quality, heuristic, metric, training strategy, or result quality is inadequate or requires improvement/selection.

- 纳入：poor model results, questionable hard-example mining, arbitrary heuristics, incomplete training labels, method/backend selection based on quality.
- 排除与边界：purely computational efficiency (`SATD06`); numerical overflow/precision (`SATD17`); ordinary implementation correctness (`SATD02`).
- 边界说明：`23shades-0559-aafdibbge`, inability to obtain good results with the current approach.
- 支持：71 个 artifact；完整列表见 `codebook.json`。
- 代表案例：artifact `23shades-0036-aaibigjdc`（row 36；完整材料见 `results.json`）。

````text
use the faithful dataset
````

绘图示例需换成faithful dataset，核心是示例数据的代表性与结果展示质量。

## SATD14 Robustness, validation, error handling, or recovery debt

The implementation lacks input/state validation, safe failure, useful exception behavior, retry/backoff, recovery, or defensive handling of runtime hazards.

- 纳入：divide-by-zero protection, more specific exceptions, malformed-input prevention, HTTP 429 backoff, defensive copies, validation before an invalid operation.
- 排除与边界：testing that validation works (`SATD04`); logging only (`SATD15`); unsupported but otherwise valid input kinds (`SATD03`).
- 边界说明：`23shades-0596-aagbdjhgb`, making a calculation safe against division by zero.
- 支持：48 个 artifact；完整列表见 `codebook.json`。
- 代表案例：artifact `23shades-0048-aagaijehb`（row 48；完整材料见 `results.json`）。

````text
add arguments compatibility check
````

参数组合兼容检查尚未实现，运行前验证不足。

## SATD15 Observability, logging, diagnostics, or provenance debt

Runtime events, timing, failures, origins, or state are insufficiently logged, messaged, measured, or traceable.

- 纳入：missing log messages/levels, weak error diagnostics, timing instrumentation, source provenance, clearer user-facing failure context.
- 排除与边界：general documentation (`SATD05`); test assertions (`SATD04`); algorithm metrics used to improve model quality (`SATD13`).
- 边界说明：`23shades-0588-aaeiaghhj`, a missing log message.
- 支持：21 个 artifact；完整列表见 `codebook.json`。
- 代表案例：artifact `23shades-0046-aafchcgjg`（row 46；完整材料见 `results.json`）。

````text
confidence is not provided
````

缺失的上游confidence被硬编码为1，形成不真实默认值并损害置信度来源可追踪性。

## SATD16 Concurrency, parallelism, distribution, or device-scaling debt

Work cannot safely or efficiently execute across threads, processes, workers, devices, batches, or distributed partitions, or lacks the mechanisms to do so.

- 纳入：parallelization, GPU/multi-GPU handling, multi-thread safety, distributed state transfer, load rebalancing, batched/distributed execution.
- 排除与边界：performance without a concurrency mechanism (`SATD06`); ordinary blocking calls without a stated concurrency design (`SATD06` or `SATD14` as supported); external device-library compatibility (`SATD10`, optionally co-coded).
- 边界说明：`23shades-0631-aaecaicdb`, “parallelize.”
- 支持：31 个 artifact；完整列表见 `codebook.json`。
- 代表案例：artifact `23shades-0049-aagaggihd`（row 49；完整材料见 `results.json`）。

````text
future enhancement TODO for running on multiple GPU
````

多GPU运行是明确的未来功能增强，并涉及设备并行扩展。

## SATD17 Numerical precision, stability, or mathematical-representation debt

Floating-point stability, overflow/underflow, precision, scaling, mathematical-domain representation, or numerically safe formulation is inadequate or uncertain.

- 纳入：precision overflow, log-density versus density, unsafe numerical scaling, unexplained low digits of accuracy.
- 排除与边界：general wrong logic (`SATD02`); divide-by-zero as a defensive runtime boundary (`SATD14`, unless a broader stability formulation is explicit); tensor shape/type coverage (`SATD03`).
- 边界说明：`23shades-0803-aaichjjjg`, avoiding precision overflow.
- 支持：22 个 artifact；完整列表见 `codebook.json`。
- 代表案例：artifact `23shades-0004-aaejjacgf`（row 4；完整材料见 `results.json`）。

````text
In some cases
````

当前US表示在某些数值范围下容量不足，既是边界规模覆盖限制，也是数值表示范围问题。

## SATD18 Investigation, uncertainty, rationale, or design-choice debt

The artifact records an unresolved question, unknown cause, uncertain correctness, unclear rationale, technology choice, or need for investigation rather than a settled implementation action.

- 纳入：“why does this happen?”, “is this needed?”, competing design options, uncertain API behavior, root-cause research, knowledge gaps.
- 排除与边界：a confirmed defect with a clear action (`SATD02`); an artifact so short that even the question/object is unavailable (`SATD20`); a defined algorithm-quality experiment (`SATD13`, possibly co-coded).
- 边界说明：`23shades-0841-aagcbggid`, uncertainty about which implementation direction is best.
- 支持：184 个 artifact；完整列表见 `codebook.json`。
- 代表案例：artifact `23shades-0006-aaahbghib`（row 6；完整材料见 `results.json`）。

````text
hackier
````

当前解析方案被认为hacky，计划改用regex或其他办法；具体替代仍未决定。

## SATD19 Build, packaging, deployment, or operational-infrastructure debt

Installation metadata, dependency declarations, archive/build outputs, deployment configuration, artifact release, data acquisition infrastructure, or operational setup is incomplete or needs change.

- 纳入：missing package requirements, archive-format changes, release integrity configuration, build/deployment environment setup.
- 排除与边界：runtime library compatibility (`SATD10`); application-level configuration (`SATD09`); model checkpoint semantics (`SATD08` or `SATD01` unless the issue is release infrastructure).
- 边界说明：`23shades-0645-aadbbbcgh`, missing package requirements in `setup.py`.
- 支持：17 个 artifact；完整列表见 `codebook.json`。
- 代表案例：artifact `23shades-0025-aajffcjii`（row 25；完整材料见 `results.json`）。

````text
code formatting issue
````

明确是20.07发布前的代码格式清理，包含局部可维护性与发布准备维度。

## SATD20 Insufficiently specified or non-actionable evidence

The artifact does not contain enough information to determine a substantive debt category or identify the object/action with defensible specificity.

- 纳入：empty/bare TODOs, “fix this later,” “U,” truncated fragments whose missing portion contains the needed object, comments that merely explain behavior without admitting a defect or improvement.
- 排除与边界：short comments that nevertheless name a clear action and object, such as “Implement Conv Transpose” (`SATD01`); uncertainty with an identifiable subject (`SATD18`).
- 边界说明：`23shades-0752-aagfegjcg`, the complete admitted comment is only “TODO: U.”
- 支持：166 个 artifact；完整列表见 `codebook.json`。
- 代表案例：artifact `23shades-0002-aaehidhih`（row 2；完整材料见 `results.json`）。

````text
!TODO
````

完整材料只有无对象的!TODO，无法防御性地判断具体债务内容。

## 配套文件

- `codebook.json`：结构化定义、成员、计数和代表证据。
- `codebook.csv`：表格化 codebook。
- `assignments.json` / `assignments.csv`：逐 artifact 的代码、理由、阅读摘要、证据和限制。
- `taxonomy.json`：与 GPT6-1 一致的 HOW-style 类别树。
- `results.json`：冻结材料全文与最终类别的逐条组合。
