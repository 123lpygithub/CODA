# SATD / deepseek-1

Schema: `coda.artifact.v1`. Artifacts: **856**; codes: **18**; artifact–code assignments: **1072**.

This package uses the common seven-file format. All existing coding decisions, evidence and limitations are preserved. Additional source-specific fields are retained in `extensions`; original codebook text is retained in `codebook.json` metadata extensions and the local pre-conversion backup.

## Scope and method

Inductive consolidation of individually authored full supplied-text reading notes, followed by explicit per-artifact assignment review. No keyword classifier or prior codebook assignments were used for consolidation.

Coverage refers to all supplied textual sections, not all content ever linked on the web.
Source revision ambiguity, inaccessible context, tentative proposals and absence of execution evidence remain in individual scope notes.
Coding is assistant-authored; it is not published human annotation, independently validated ground truth, or an experimental system run.
All artifacts are included; unspecified work and comments without established outstanding work are retained explicitly rather than invented as defects.

## Codes

| Code | Name | Artifacts |
|---|---|---:|
| SATD-01 | 结构、职责、命名与格式重构 | 99 |
| SATD-02 | 行为与正确性缺陷 | 48 |
| SATD-03 | 输入校验、边界与异常 | 59 |
| SATD-04 | 功能补全与实现缺失 | 124 |
| SATD-05 | 范围与泛化扩展 | 88 |
| SATD-06 | 外部依赖、版本与平台约束 | 53 |
| SATD-07 | 性能、内存与效率 | 46 |
| SATD-08 | 临时绕行、hack 与硬编码 | 45 |
| SATD-09 | 算法、数据假设与语义适用性 | 29 |
| SATD-10 | 配置、参数与默认值 | 37 |
| SATD-11 | 测试与验证 | 60 |
| SATD-12 | 文档与说明 | 18 |
| SATD-13 | 弃用、移除与清理 | 44 |
| SATD-14 | 数据、接口与表示契约 | 55 |
| SATD-15 | 日志、可观察性与展示 | 20 |
| SATD-16 | 未决问题、调查与设计疑问 | 111 |
| SATD-17 | 空 TODO 与证据不足 | 100 |
| SATD-18 | 替代方案与替代实现 | 36 |

## SATD-01 — 结构、职责、命名与格式重构

当前实现的结构、职责、抽象、命名或代码格式需要整理。

- Include: 提取/移动/复用/去耦、命名统一、格式整理、模块化。
- Exclude: 仅新增行为用 SATD-04；仅性能诉求用 SATD-07。
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 99; complete membership in `supporting_cases`.

````json
[]
````

## SATD-02 — 行为与正确性缺陷

注释指出行为错误、结果不一致、契约违背或具体正确性风险。

- Include: 明确 bug、错误结果、语义不一致、条件性正确性风险。
- Exclude: 仅 TODO 或一般优化不纳入；尚未支持的新范围用 SATD-04。
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 48; complete membership in `supporting_cases`.

````json
[]
````

## SATD-03 — 输入校验、边界与异常

需要验证输入、形状、状态、生命周期或错误路径，并保护边界条件。

- Include: 空值、除零、类型/形状检查、异常策略、并发保护。
- Exclude: 新增单元测试用 SATD-11；一般功能缺失用 SATD-04。
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 59; complete membership in `supporting_cases`.

````json
[]
````

## SATD-04 — 功能补全与实现缺失

所需能力、分支、类型、数据流、格式覆盖或一般实现明确尚未完成。

- Include: not implemented、只支持部分输入/模型/格式、缺少保存/加载/转换能力。
- Exclude: 已有能力但接口契约不稳用 SATD-14；已产生错误数据用 SATD-02。
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 124; complete membership in `supporting_cases`.

````json
[]
````

## SATD-05 — 范围与泛化扩展

把已有能力扩展到更多输入、平台、模型、配置或使用场景。

- Include: 支持其他类型/模型/优化器/平台、扩大覆盖范围、增加通用分支。
- Exclude: 全新缺失能力用 SATD-04；结构性抽象用 SATD-01。
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 88; complete membership in `supporting_cases`.

````json
[]
````

## SATD-06 — 外部依赖、版本与平台约束

工作受外部库、版本、平台、浏览器或上游组件约束。

- Include: 兼容性修复、版本升级、平台差异、上游缺陷、依赖迁移。
- Exclude: 纯内部设计问题用 SATD-01；性能问题用 SATD-07。
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 53; complete membership in `supporting_cases`.

````json
[]
````

## SATD-07 — 性能、内存与效率

执行速度、内存、资源使用或可扩展性需要改善。

- Include: 加速、减少内存/分配、并行化、避免重复计算。
- Exclude: 功能正确性缺陷用 SATD-02；一般重构用 SATD-01。
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 46; complete membership in `supporting_cases`.

````json
[]
````

## SATD-08 — 临时绕行、hack 与硬编码

为绕过问题而采用临时、脆弱或硬编码方案。

- Include: hack、workaround、硬编码常量/路径、测试专用开关、非常规绕行。
- Exclude: 正式设计选择用 SATD-16；纯参数默认值用 SATD-10。
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 45; complete membership in `supporting_cases`.

````json
[]
````

## SATD-09 — 算法、数据假设与语义适用性

算法或数据假设在特定语义、分布或边界下不成立。

- Include: 度量/归一化假设、编码映射、数据分布、语义等价性、适用性疑问。
- Exclude: 明确公式 bug 用 SATD-02；纯性能用 SATD-07。
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 29; complete membership in `supporting_cases`.

````json
[]
````

## SATD-10 — 配置、参数与默认值

配置项、参数语义、默认值或选项组合需要调整。

- Include: 新增/统一参数、默认值变更、配置开关、参数命名语义。
- Exclude: 硬编码常量用 SATD-08；一般 API 契约用 SATD-14。
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 37; complete membership in `supporting_cases`.

````json
[]
````

## SATD-11 — 测试与验证

需要增加、修改或隔离测试、验证步骤或测试环境。

- Include: 补单测/集成测试、测试专用逻辑、验证行为、测试隔离。
- Exclude: 生产输入校验用 SATD-03；文档示例用 SATD-12。
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 60; complete membership in `supporting_cases`.

````json
[]
````

## SATD-12 — 文档与说明

需要补充或修改文档、注释、示例、教程或说明。

- Include: docstring、README、教程、示例、格式说明。
- Exclude: 接口契约本身缺失用 SATD-14；纯命名整理用 SATD-01。
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 18; complete membership in `supporting_cases`.

````json
[]
````

## SATD-13 — 弃用、移除与清理

需要删除、弃用或清理旧代码、依赖、配置或兼容分支。

- Include: 移除旧 API/依赖/测试、删除死代码、弃用迁移。
- Exclude: 局部格式整理用 SATD-01；替代实现用 SATD-18。
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 44; complete membership in `supporting_cases`.

````json
[]
````

## SATD-14 — 数据、接口与表示契约

数据格式、接口契约、序列化、字段语义或表示约定需要明确或修正。

- Include: 字段格式、序列化格式、API 返回契约、编码约定、命名表示。
- Exclude: 纯文档说明用 SATD-12；一般功能缺失用 SATD-04。
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 55; complete membership in `supporting_cases`.

````json
[]
````

## SATD-15 — 日志、可观察性与展示

日志、错误展示、调试输出或用户可见呈现需要调整。

- Include: 日志内容、错误显示、UI 展示、调试可观察性。
- Exclude: 隐私/安全问题用 SATD-02/03；纯文档用 SATD-12。
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 20; complete membership in `supporting_cases`.

````json
[]
````

## SATD-16 — 未决问题、调查与设计疑问

注释提出尚未决定的方向、待调查问题或设计疑问。

- Include: 问句、是否/如何选择、待确认语义、设计探索。
- Exclude: 明确 TODO 动作有对象用对应机制；纯解释用 SATD-17。
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 111; complete membership in `supporting_cases`.

````json
[]
````

## SATD-17 — 空 TODO 与证据不足

只有待办标记或低信息文本，无法判断具体技术机制。

- Include: 孤立 TODO/FIXME、单个名词、截断到无法解释的改进判断。
- Exclude: 明确写出未实现对象用 SATD-04；解释性注释用 SATD-16。
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 100; complete membership in `supporting_cases`.

````json
[]
````

## SATD-18 — 替代方案与替代实现

提出另一种实现、方案、数据源或技术路线。

- Include: 改用其他库/模型/数据/算法、替代实现、迁移方案。
- Exclude: 纯重构用 SATD-01；外部兼容约束用 SATD-06。
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

# SATD — deepseek-1

856 artifacts; 18 codes; 1072 artifact–code assignments.

Inductive consolidation of individually authored full supplied-text reading notes, followed by explicit per-artifact assignment review. No keyword classifier or prior codebook assignments were used for consolidation.

Every supplied artifact has an assignment. Codes describe the observed work, concern, or evidence status; they do not establish that a defect was reproduced. Refer to `assignments.json` for individual reasoning, qualifications, source references and evidence.

## Scope

- Coverage refers to all supplied textual sections, not all content ever linked on the web.
- Source revision ambiguity, inaccessible context, tentative proposals and absence of execution evidence remain in individual scope notes.
- Coding is assistant-authored; it is not published human annotation, independently validated ground truth, or an experimental system run.
- All artifacts are included; unspecified work and comments without established outstanding work are retained explicitly rather than invented as defects.

Single-analyst reconstruction; not a blinded independent replicate.

## Codebook

| Code | Name | Artifacts |
|---|---|---:|
| SATD-01 | 结构、职责、命名与格式重构 | 99 |
| SATD-02 | 行为与正确性缺陷 | 48 |
| SATD-03 | 输入校验、边界与异常 | 59 |
| SATD-04 | 功能补全与实现缺失 | 124 |
| SATD-05 | 范围与泛化扩展 | 88 |
| SATD-06 | 外部依赖、版本与平台约束 | 53 |
| SATD-07 | 性能、内存与效率 | 46 |
| SATD-08 | 临时绕行、hack 与硬编码 | 45 |
| SATD-09 | 算法、数据假设与语义适用性 | 29 |
| SATD-10 | 配置、参数与默认值 | 37 |
| SATD-11 | 测试与验证 | 60 |
| SATD-12 | 文档与说明 | 18 |
| SATD-13 | 弃用、移除与清理 | 44 |
| SATD-14 | 数据、接口与表示契约 | 55 |
| SATD-15 | 日志、可观察性与展示 | 20 |
| SATD-16 | 未决问题、调查与设计疑问 | 111 |
| SATD-17 | 空 TODO 与证据不足 | 100 |
| SATD-18 | 替代方案与替代实现 | 36 |

## SATD-01 — 结构、职责、命名与格式重构

当前实现的结构、职责、抽象、命名或代码格式需要整理。

**Include:** 提取/移动/复用/去耦、命名统一、格式整理、模块化。

**Exclude:** 仅新增行为用 SATD-04；仅性能诉求用 SATD-07。

**Examples:**

- `23shades-0001-aahiieiig`: 明确承诺稍后重构多个算法共用的函数，属于职责与结构整理。 Evidence: `''' || Functions used by more than one algorithm || TODO refactor properly later || '''`
- `23shades-0010-aaaedagad`: 计划重写 name、index、uuid 等字段，属结构与命名整理。 Evidence: `# TODO May want to rewrite name; index; uuid; etc.`

## SATD-02 — 行为与正确性缺陷

注释指出行为错误、结果不一致、契约违背或具体正确性风险。

**Include:** 明确 bug、错误结果、语义不一致、条件性正确性风险。

**Exclude:** 仅 TODO 或一般优化不纳入；尚未支持的新范围用 SATD-04。

**Examples:**

- `23shades-0019-aaigjhibg`: 注释写明“((); 0); # TODO(sonots): Fix compatibility”：要求修复兼容性，属外部版本/平台约束下的缺陷。 Evidence: `((); 0); # TODO(sonots): Fix compatibility`
- `23shades-0020-aaigjhiah`: 注释写明“((); 0); # TODO(sonots): Fix compatibility”：与上条同源，要求修复兼容性。 Evidence: `((); 0); # TODO(sonots): Fix compatibility`

## SATD-03 — 输入校验、边界与异常

需要验证输入、形状、状态、生命周期或错误路径，并保护边界条件。

**Include:** 空值、除零、类型/形状检查、异常策略、并发保护。

**Exclude:** 新增单元测试用 SATD-11；一般功能缺失用 SATD-04。

**Examples:**

- `23shades-0004-aaejjacgf`: 指出 US 类型在某些情况下容不下完整数值，是表示容量与数值边界问题。 Evidence: `!TODO: In some cases; US is not enough to hold the complete number`
- `23shades-0048-aagaijehb`: 注释写明“\/\/TODO in future add arguments compatibility check”：计划增加参数兼容性检查。 Evidence: `\/\/TODO in future add arguments compatibility check`

## SATD-04 — 功能补全与实现缺失

所需能力、分支、类型、数据流、格式覆盖或一般实现明确尚未完成。

**Include:** not implemented、只支持部分输入/模型/格式、缺少保存/加载/转换能力。

**Exclude:** 已有能力但接口契约不稳用 SATD-14；已产生错误数据用 SATD-02。

**Examples:**

- `23shades-0007-aaaegfgeb`: 指出拼接前需要 reverse bw 这一缺失步骤。 Evidence: `# reverse bw; before concat TODO`
- `23shades-0008-aagcbjjcd`: 要求把 landmark 加载扩展到验证集和测试集，既是补功能也是扩范围。 Evidence: `# TODO : load landmarks in validation and test set also. I'm too sleepy to do it today -_- zzz... zzz...`

## SATD-05 — 范围与泛化扩展

把已有能力扩展到更多输入、平台、模型、配置或使用场景。

**Include:** 支持其他类型/模型/优化器/平台、扩大覆盖范围、增加通用分支。

**Exclude:** 全新缺失能力用 SATD-04；结构性抽象用 SATD-01。

**Examples:**

- `23shades-0008-aagcbjjcd`: 要求把 landmark 加载扩展到验证集和测试集，既是补功能也是扩范围。 Evidence: `# TODO : load landmarks in validation and test set also. I'm too sleepy to do it today -_- zzz... zzz...`
- `23shades-0013-aaebbeedd`: 注释写明“## elif (): ## FIXME: handle other bases here”：要求处理其他基类分支，属覆盖范围扩展。 Evidence: `## elif (): ## FIXME: handle other bases here`

## SATD-06 — 外部依赖、版本与平台约束

工作受外部库、版本、平台、浏览器或上游组件约束。

**Include:** 兼容性修复、版本升级、平台差异、上游缺陷、依赖迁移。

**Exclude:** 纯内部设计问题用 SATD-01；性能问题用 SATD-07。

**Examples:**

- `23shades-0019-aaigjhibg`: 注释写明“((); 0); # TODO(sonots): Fix compatibility”：要求修复兼容性，属外部版本/平台约束下的缺陷。 Evidence: `((); 0); # TODO(sonots): Fix compatibility`
- `23shades-0020-aaigjhiah`: 注释写明“((); 0); # TODO(sonots): Fix compatibility”：与上条同源，要求修复兼容性。 Evidence: `((); 0); # TODO(sonots): Fix compatibility`

## SATD-07 — 性能、内存与效率

执行速度、内存、资源使用或可扩展性需要改善。

**Include:** 加速、减少内存/分配、并行化、避免重复计算。

**Exclude:** 功能正确性缺陷用 SATD-02；一般重构用 SATD-01。

**Examples:**

- `23shades-0037-aajffhihe`: 明确说明 unparse 不完整、只支持部分语句；并建议改用 _ast 以提速。 Evidence: `\"\"\" Turn compiler.ast structures back into executable python code. ||  ||     The unparse method takes a compiler.ast tree and transforms it back into ||     valid python code.  It is incomplete and currently only wor`
- `23shades-0086-aaicdjedb`: 注释写明“FIXME: can use n_jobs here too”：指出此处也可用 n_jobs 并行。 Evidence: `FIXME: can use n_jobs here too`

## SATD-08 — 临时绕行、hack 与硬编码

为绕过问题而采用临时、脆弱或硬编码方案。

**Include:** hack、workaround、硬编码常量/路径、测试专用开关、非常规绕行。

**Exclude:** 正式设计选择用 SATD-16；纯参数默认值用 SATD-10。

**Examples:**

- `23shades-0005-aaebbecaa`: 为绕开 justify-content 失效而使用 hack，诱因在浏览器/CSS 渲染行为。 Evidence: `# Hack to center SVG as justify-content is broken:`
- `23shades-0006-aaahbghib`: 自称更 hack 的实现，并提议改用正则，属临时绕行。 Evidence: `# hackier; fixme to use regex or something`

## SATD-09 — 算法、数据假设与语义适用性

算法或数据假设在特定语义、分布或边界下不成立。

**Include:** 度量/归一化假设、编码映射、数据分布、语义等价性、适用性疑问。

**Exclude:** 明确公式 bug 用 SATD-02；纯性能用 SATD-07。

**Examples:**

- `23shades-0024-aaeibiccf`: 指出 arabtex 与 iso8859-6 因一对二映射需单独处理，属编码覆盖与映射假设。 Evidence: `@todo: arabtex and iso8859-6 need individual handling because in some cases using one-two mapping`
- `23shades-0050-aabcjdaea`: 对零和博弈下双值误差是否应乘 2 存疑，属建模假设。 Evidence: `all games are zero sum that are trained and because 2 values; x2 the error.  XXX`

## SATD-10 — 配置、参数与默认值

配置项、参数语义、默认值或选项组合需要调整。

**Include:** 新增/统一参数、默认值变更、配置开关、参数命名语义。

**Exclude:** 硬编码常量用 SATD-08；一般 API 契约用 SATD-14。

**Examples:**

- `23shades-0011-aageijaai`: 以疑问形式提出是否让增益和偏置可训练，属未决设计兼参数选项。 Evidence: `# TODO: do we want gains\/biases to be trainable?`
- `23shades-0012-aafaehach`: 要求在 name 为 None 时用函数名补默认名，是补全行为兼默认值。 Evidence: `# TODO: Set name (using \"functionality.__name__\") if name is None`

## SATD-11 — 测试与验证

需要增加、修改或隔离测试、验证步骤或测试环境。

**Include:** 补单测/集成测试、测试专用逻辑、验证行为、测试隔离。

**Exclude:** 生产输入校验用 SATD-03；文档示例用 SATD-12。

**Examples:**

- `23shades-0022-aahdfibcf`: 指出 nrows 仅供测试，属测试专用设置与硬编码。 Evidence: `@todo nrows is for testing only!`
- `23shades-0038-aaeiaheab`: 注释写明“\"\"\"Convert MdC transliterated text to Unicode. || || TODO: Add tests and clean up. || \"\"\"”：要求增加测试并清理代码。 Evidence: `\"\"\"Convert MdC transliterated text to Unicode. ||  || TODO: Add tests and clean up. || \"\"\"`

## SATD-12 — 文档与说明

需要补充或修改文档、注释、示例、教程或说明。

**Include:** docstring、README、教程、示例、格式说明。

**Exclude:** 接口契约本身缺失用 SATD-14；纯命名整理用 SATD-01。

**Examples:**

- `23shades-0018-aajcabgbe`: 认为该代码可发展为生成 phantom 的教程，属文档/教学材料。 Evidence: `#TODO: this can become a nice tutorial for generating phantoms`
- `23shades-0032-aaejahaed`: 注释写明“\"\"\" || .. todo:: || doc || \"\"\"”：todo 要求补文档。 Evidence: `\"\"\" || .. todo:: ||     doc || \"\"\"`

## SATD-13 — 弃用、移除与清理

需要删除、弃用或清理旧代码、依赖、配置或兼容分支。

**Include:** 移除旧 API/依赖/测试、删除死代码、弃用迁移。

**Exclude:** 局部格式整理用 SATD-01；替代实现用 SATD-18。

**Examples:**

- `23shades-0029-aajfejjdb`: 注释写明“@TODO: remove time usage; use it under the hood”：要求移除显式 time 使用并交给底层实现。 Evidence: `@TODO: remove time usage; use it under the hood`
- `23shades-0038-aaeiaheab`: 注释写明“\"\"\"Convert MdC transliterated text to Unicode. || || TODO: Add tests and clean up. || \"\"\"”：要求增加测试并清理代码。 Evidence: `\"\"\"Convert MdC transliterated text to Unicode. ||  || TODO: Add tests and clean up. || \"\"\"`

## SATD-14 — 数据、接口与表示契约

数据格式、接口契约、序列化、字段语义或表示约定需要明确或修正。

**Include:** 字段格式、序列化格式、API 返回契约、编码约定、命名表示。

**Exclude:** 纯文档说明用 SATD-12；一般功能缺失用 SATD-04。

**Examples:**

- `23shades-0003-aaejjbhji`: 提出空字典也可满足需求，但句子在 despite the fact that 处截断，替代方案的完整理由不可知。 Evidence: `!TODO: An empty dictionary would actually also do here ... despite the fact that`
- `23shades-0004-aaejjacgf`: 指出 US 类型在某些情况下容不下完整数值，是表示容量与数值边界问题。 Evidence: `!TODO: In some cases; US is not enough to hold the complete number`

## SATD-15 — 日志、可观察性与展示

日志、错误展示、调试输出或用户可见呈现需要调整。

**Include:** 日志内容、错误显示、UI 展示、调试可观察性。

**Exclude:** 隐私/安全问题用 SATD-02/03；纯文档用 SATD-12。

**Examples:**

- `23shades-0005-aaebbecaa`: 为绕开 justify-content 失效而使用 hack，诱因在浏览器/CSS 渲染行为。 Evidence: `# Hack to center SVG as justify-content is broken:`
- `23shades-0059-aacjfgieb`: 注释写明“Double newlines seem to mess with the rendering”：指出双换行破坏渲染，属显示缺陷。 Evidence: `Double newlines seem to mess with the rendering`

## SATD-16 — 未决问题、调查与设计疑问

注释提出尚未决定的方向、待调查问题或设计疑问。

**Include:** 问句、是否/如何选择、待确认语义、设计探索。

**Exclude:** 明确 TODO 动作有对象用对应机制；纯解释用 SATD-17。

**Examples:**

- `23shades-0003-aaejjbhji`: 提出空字典也可满足需求，但句子在 despite the fact that 处截断，替代方案的完整理由不可知。 Evidence: `!TODO: An empty dictionary would actually also do here ... despite the fact that`
- `23shades-0011-aageijaai`: 以疑问形式提出是否让增益和偏置可训练，属未决设计兼参数选项。 Evidence: `# TODO: do we want gains\/biases to be trainable?`

## SATD-17 — 空 TODO 与证据不足

只有待办标记或低信息文本，无法判断具体技术机制。

**Include:** 孤立 TODO/FIXME、单个名词、截断到无法解释的改进判断。

**Exclude:** 明确写出未实现对象用 SATD-04；解释性注释用 SATD-16。

**Examples:**

- `23shades-0002-aaehidhih`: cltk/cltk 的 cltk/parse/classical_latin/parse_latin_analyses.py 仅含 '!TODO' 标记，未说明待办对象、动作或原因，无法进一步细分技术债机制；第 2 条按证据不足记录。 Evidence: `!TODO`
- `23shades-0014-aadbjfiab`: mesnico/learning-relationship-aware-visual-features 的 networkx/networkx/algorithms/isomorphism/isomorphvf2.py 仅含 '## TODO:' 标记，未说明待办对象、动作或原因，无法进一步细分技术债机制；第 14 条按证据不足记录。 Evidence: `## TODO:`

## SATD-18 — 替代方案与替代实现

提出另一种实现、方案、数据源或技术路线。

**Include:** 改用其他库/模型/数据/算法、替代实现、迁移方案。

**Exclude:** 纯重构用 SATD-01；外部兼容约束用 SATD-06。

**Examples:**

- `23shades-0197-aadbceejg`: 注释建议用类列表替代当前单类实现，以消除对单一类的需要；这是替代表示兼范围扩展，不是单纯结构整理。 Evidence: `TODO - a list of classes would be better eliminating the need for the one`
- `23shades-0198-aajeiegcd`: 注释明确要在上述展平方案之外探索替代做法；句子虽截断，但替代方案意图可辨。 Evidence: `TODO - as an alternative to the above flattening approach; explore an`
