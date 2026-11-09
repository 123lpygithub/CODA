# SATD / gpt5.6-1

Schema: `coda.artifact.v1`. Artifacts: **856**; codes: **14**; artifact–code assignments: **1066**.

This package uses the common seven-file format. All existing coding decisions, evidence and limitations are preserved. Additional source-specific fields are retained in `extensions`; original codebook text is retained in `codebook.json` metadata extensions and the local pre-conversion backup.

## Scope and method

逐条完整阅读、开放编码、持续比较、逐条人工 assignment、code-to-artifact 反向复核；程序仅转换格式和验证。

单一 AI 编码；机械一致性检查不构成人工复核。Privacy 的 metadata-only 材料只按可用标题和元数据作最小判断。

## Codes

| Code | Name | Artifacts |
|---|---|---:|
| SD01 | 未说明内容的待办或低信息债务标记 | 80 |
| SD02 | 功能、支持范围或组件集成未完成 | 161 |
| SD03 | 设计、架构或重构债务 | 77 |
| SD04 | 临时 workaround、hack 或实验性方案 | 42 |
| SD05 | 已知正确性、可靠性或数据质量缺陷 | 74 |
| SD06 | 测试、验证或测试隔离债务 | 77 |
| SD07 | 文档、示例或教学材料债务 | 16 |
| SD08 | 兼容性、可移植性或外部依赖债务 | 87 |
| SD09 | 性能、可扩展性或资源效率债务 | 55 |
| SD10 | 局部可维护性、清理、格式或死代码债务 | 80 |
| SD11 | API、接口契约、封装或参数验证债务 | 102 |
| SD12 | 硬编码假设、占位值或配置策略债务 | 35 |
| SD13 | 尚未解决的设计决策或需求不确定性 | 150 |
| SD14 | 债务状态不明确或可能只是解释性注释 | 30 |

## SD01 — 未说明内容的待办或低信息债务标记

文本明确留下待办、修复或改进信号，但没有足够对象、动作、原因或完成标准来判断具体技术机制。

- Include: 孤立 `TODO`/`FIXME`；单个名词或符号；`do this better`、`make nicer`、`something smarter?`；截断后只剩无法解释的改进判断。
- Exclude: 即使对象未命名，只要明确写出“未实现”仍用 SD02；纯粹解释现有步骤且没有待办信号用 SD14；明确询问两个方案如何选择用 SD13。
- Boundary/examples: row 2 只有 `!TODO`；row 435 只有 `AAM METRIC`；row 467 虽说“需要修复”，但问题本身完全缺失。
- Supporting artifacts: 80; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "23shades-0002-aaehidhih",
    "row": 2,
    "field": "comment_text",
    "quote": "!TODO",
    "interpretation": "只有无内容的 TODO，无法支持更具体的债务判断。"
  }
]
````

## SD02 — 功能、支持范围或组件集成未完成

所需能力、分支、输入/输出类型、数据流程、模型/格式覆盖、组件接入或一般实现明确尚未完成。

- Include: `not implemented`；只支持部分模型、类型、维度或格式；组件尚未启用或集成；缺少保存、加载、转换、计算或命令能力。
- Exclude: 已有能力但其接口契约或验证不稳用 SD11；已明确产生错误数据或状态用 SD05；整体职责或抽象结构需要重组用 SD03；只有名词而无动作不能凭上下文猜测，用 SD01。
- Boundary/examples: row 123 明确说权重冻结未实现；row 319 不支持 dense 输入；row 713 既缺 imgaug 参数注册能力又依赖外部上游，因此同时使用 SD08。
- Supporting artifacts: 161; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "23shades-0123-aagfeiiaj",
    "row": 123,
    "field": "comment_text",
    "quote": "Freeze weights - TODO: NOT IMPLEMENTED!",
    "interpretation": "权重冻结功能被明确标记为未实现。"
  }
]
````

## SD03 — 设计、架构或重构债务

模块边界、职责分配、依赖方向、状态归属、抽象层次、数据结构或跨组件组织需要结构性调整。

- Include: 拆分类/函数；移动逻辑到正确模块；消除循环依赖或全局状态；建立统一抽象；重构对象生命周期或数据模型。
- Exclude: 纯局部命名、格式、重复代码和死代码用 SD10；已有公共接口的参数、返回或封装规则用 SD11；单纯缺能力用 SD02。
- Boundary/examples: row 1 推迟了共享函数的正式模块化；row 311 要消除全局状态；row 640 要拆解模块循环依赖。
- Supporting artifacts: 77; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "23shades-0001-aahiieiig",
    "row": 1,
    "field": "comment_text",
    "quote": "''' || Functions used by more than one algorithm || TODO refactor properly later || '''",
    "interpretation": "共享函数被放在临时位置，作者明确推迟了模块边界和复用结构的正式重构。"
  }
]
````

## SD04 — 临时 workaround、hack 或实验性方案

作者明确把现有路径描述为 hack、workaround、kludge、temporary、WIP、testing-only 或短期最小修复。

- Include: 为上游 bug 保留的绕行；测试性 hack；临时硬编码或短期代码；明确的最小可用修复。
- Exclude: 仅有兼容约束而没有临时绕行用 SD08；普通旧代码清理用 SD10；作者只是不确定方案是否正确用 SD13。
- Boundary/examples: row 5 是布局兼容 hack；row 177 是 messy 的最小修复；row 769 主动利用上游 bug，故同时使用 SD08。
- Supporting artifacts: 42; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "23shades-0005-aaebbecaa",
    "row": 5,
    "field": "comment_text",
    "quote": "# Hack to center SVG as justify-content is broken:",
    "interpretation": "这是为外部布局行为失效而保留的明确 hack，同时受浏览器或布局兼容约束。"
  }
]
````

## SD05 — 已知正确性、可靠性或数据质量缺陷

文本直接支持当前实现会产生错误、遗漏、冲突、数据丢失、竞态、溢出、错误占位值、异常副作用或不可靠结果。

- Include: 明确 bug；off-by-one；状态未初始化；字段被忽略或元数据丢失；错误的坐标方向；不安全的并发或资源生命周期；错误占位值误表征真实数据。
- Exclude: 只有怀疑、尚未检查或正确方向未定用 SD06/SD13；缺少一种新能力但现有范围内没有错误用 SD02；固定假设只有潜在风险而未证实错误用 SD12。
- Boundary/examples: row 30 明确称 `predict_proba` 的状态变化为 bug；row 274 时间索引已丢失；row 627 是明确 off-by-one。
- Supporting artifacts: 74; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "23shades-0030-aaedcebdc",
    "row": 30,
    "field": "comment_text",
    "quote": "[todo]: this is a bug; predict_proba should not change",
    "interpretation": "作者明确称 predict_proba 的非预期状态变化为 bug。"
  }
]
````

## SD06 — 测试、验证或测试隔离债务

测试缺失、禁用、失败、断言过弱、测试环境受限，或某行为/命题尚未通过检查、基准或验证确认。

- Include: `needs testing`；补测试；测试只检查长度或写日志；测试 fixture 硬编码；“尚未检查是否工作”；数学或兼容等价性待验证。
- Exclude: 已经确认的生产行为错误用 SD05；测试之外的开放产品/设计选择用 SD13；普通事实说明用 SD14。
- Boundary/examples: row 273 的 ARIMA 测试只有长度断言；row 386 测试被禁用；row 662 应从 logging 改为实际断言 values。
- Supporting artifacts: 77; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "23shades-0273-aaebjbbei",
    "row": 273,
    "field": "comment_text",
    "quote": "TODO currently tests only run fit",
    "interpretation": "ARIMA 测试只有弱长度断言，没有验证预测内容。"
  }
]
````

## SD07 — 文档、示例或教学材料债务

模块/API 文档、README、docstring、格式说明、教程、示例或入门材料不完整、过时或尚未编写。

- Include: 文档占位；缺使用示例；文档与实现不同步；输出目录缺 README；已有代码尚未整理为教程。
- Exclude: 格式本身未定义而影响机器接口时还使用 SD11；示例明确有 bug 用 SD05；实现能力缺失用 SD02。
- Boundary/examples: row 33 缺模块概要和长描述；row 45 的 diff 格式既未文档化又未形成契约，故同时使用 SD11；row 378 文档与实现不同步。
- Supporting artifacts: 16; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "23shades-0033-aadhcadac",
    "row": 33,
    "field": "comment_text",
    "quote": ":synopsis: TODO",
    "interpretation": "模块概要和长描述仍是文档占位。"
  }
]
````

## SD08 — 兼容性、可移植性或外部依赖债务

债务由特定版本、平台、运行环境、后端、字符/文件格式、外部 API、依赖升级、弃用迁移或上游能力限制驱动。

- Include: Python/NumPy/Pandas/TensorFlow 等版本差异；跨框架迁移；等待上游修复；平台路径或 CI 环境问题；旧格式、旧接口或外部依赖替换。
- Exclude: 针对兼容问题采用的明确临时绕行还需 SD04；仅是局部代码删除且没有版本/依赖条件用 SD10；一般缺功能用 SD02。
- Boundary/examples: row 52 是 Python 3.4 打包问题；row 120 是 Numba issue 的 workaround，故同时使用 SD04；row 673 是模块名与标准库冲突。
- Supporting artifacts: 87; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "23shades-0052-aaahbjdic",
    "row": 52,
    "field": "comment_text",
    "quote": "apparently package_deps are broken in 3.4",
    "interpretation": "打包依赖配置在特定 Python 版本上已知失效。"
  }
]
````

## SD09 — 性能、可扩展性或资源效率债务

已知或明确提出的慢路径、复杂度风险、重复计算、未利用并行/设备能力、内存浪费、组合爆炸或资源扩展不足。

- Include: O(N²)；并行化机会；重复加载或复制；lazy loading；GPU/multi-GPU 扩展；缓存、内存布局和预计算优化。
- Exclude: 只有“可能更快”且尚需验证时可同时使用 SD06/SD13；功能完全缺失用 SD02；结构重构若有独立架构意义再加 SD03。
- Boundary/examples: row 51 生成所有组合；row 156 每批重复创建 inferer；row 733 是大图上的 O(N²) 风险。
- Supporting artifacts: 55; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "23shades-0051-aagacefbc",
    "row": 51,
    "field": "comment_text",
    "quote": "All possibilities will be generated TODO",
    "interpretation": "无约束生成所有组合形成明显的扩展性风险，但具体剪枝策略未说明。"
  }
]
````

## SD10 — 局部可维护性、清理、格式或死代码债务

局部代码、测试或配置中的命名、格式、重复、冗余、弃用、死代码、魔法数字、日志风格或可读性清理。

- Include: 删除旧方法；统一内部命名；消除重复代码；清理 unused 对象；发布前格式整理；复用已有 helper；局部可读性改善。
- Exclude: 跨模块职责或抽象结构用 SD03；公共参数/返回/封装契约用 SD11；版本或外部依赖驱动的清理同时或改用 SD08。
- Boundary/examples: row 25 是格式清理；row 459 是重复测试；row 794/795 是两个独立 unused artifact。
- Supporting artifacts: 80; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "23shades-0025-aajffcjii",
    "row": 25,
    "field": "comment_text",
    "quote": "@TODO: code formatting issue for 20.07 release",
    "interpretation": "这是明确的发布前代码格式清理项。"
  }
]
````

## SD11 — API、接口契约、封装或参数验证债务

公共或内部调用边界的参数、返回类型、格式/schema、可见性、封装、错误/警告、输入验证、扩展钩子或行为契约不完整或不一致。

- Include: 返回类型不符；参数含义不一致；缺输入验证；字段 schema 不完整；实现细节泄漏；应私有化；错误类型或消息不合适；需正式配置开关。
- Exclude: 能力根本不存在用 SD02；跨模块组织重构用 SD03；错误行为已经造成数据丢失或运行失败时可同时使用 SD05。
- Boundary/examples: row 102 子类返回类型违反父类；row 384 `validation_split` 被接受却未使用，故同时使用 SD05；row 847 应返回 copy 保护内部状态。
- Supporting artifacts: 102; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "23shades-0102-aajeddgaa",
    "row": 102,
    "field": "comment_text",
    "quote": "FIXME: Return type \\\"None\\\" of \\\"fit\\\" incompatible with return type \\\"float\\\" in supertype \\\"Model\\\"",
    "interpretation": "子类 fit 的返回类型违反父类声明的接口契约。"
  }
]
````

## SD12 — 硬编码假设、占位值或配置策略债务

常量、固定长度/比例/路径、占位数据、默认策略、数据/训练假设或运行参数被硬编码，需要配置化、动态计算、校准或替换。

- Include: 魔法数字；固定四字节标签；随机占位标签；任意 threshold；硬编码 ratios；未外置的 seed、dtype、process 数；缺乏依据的默认值。
- Exclude: 硬编码已明确产生错误时同时使用 SD05；一般参数验证用 SD11；单纯局部命名或死代码用 SD10。
- Boundary/examples: row 46 把未知置信度硬编码为 1；row 452 是任意 threshold；row 814 的默认 sample 数没有依据。
- Supporting artifacts: 35; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "23shades-0046-aafchcgjg",
    "row": 46,
    "field": "comment_text",
    "quote": "\\\"confidence\\\": 1  # todo discussion confidence from GNormPlus is not provided so just putting in here 1",
    "interpretation": "未知置信度被硬编码成 1，会把占位值误表征为真实确定性。"
  }
]
````

## SD13 — 尚未解决的设计决策或需求不确定性

作者记录了尚未选择的方向、未确认的必要性、开放需求、候选方案或需要先调查的语义，而不是一个已证实的单一路径缺陷。

- Include: 问句；`may`、`maybe`、`perhaps`；两个候选方案；是否弃用、是否新增能力、是否采用某种返回类型；现有行为是否重要尚未确定。
- Exclude: 只是尚未执行但方向明确的工作使用相应具体类别；仅需测试既定行为用 SD06；没有足够内容形成决策问题用 SD01。
- Boundary/examples: row 11 问 gains/biases 是否可训练；row 271 在 cpickle 与 JSON 之间选择；row 729 已知破坏 layer sharing，但其重要性仍未确认，故同时使用 SD05。
- Supporting artifacts: 150; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "23shades-0011-aageijaai",
    "row": 11,
    "field": "comment_text",
    "quote": "# TODO: do we want gains\\/biases to be trainable?",
    "interpretation": "增益和偏置是否可训练是明确未解决的设计选择。"
  }
]
````

## SD14 — 债务状态不明确或可能只是解释性注释

文本只描述一个必要步骤、已存在行为、环境约束或事实，或者截断到无法确认待办；没有直接证据表明尚未完成、存在问题或需要后续动作。

- Include: `needed for correct ...`；解释测试夹具或导入为何存在；说明兼容代码当前用途但没有清理计划；纯事实性类型/缩放陈述。
- Exclude: 明确但低信息的 TODO/FIXME 用 SD01；已知问题、开放决策或具体改进分别用对应类别。SD14 不是兜底“其他”类。
- Boundary/examples: row 142 只解释 SysEx 正确处理的必要性；row 176 只解释更新 loss history；row 728 只陈述单个 content word 时进入分支。
- Supporting artifacts: 30; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "23shades-0142-aaeeiicii",
    "row": 142,
    "field": "comment_text",
    "quote": "needed for correct SysEx event handling",
    "interpretation": "文本只解释某步骤对正确处理 SysEx 的必要性。"
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

# gpt5.6-1 — SATD 最终编码本

本轮覆盖 **856 个 artifact**，形成 **14 个可分配 code**，共记录 **1066 个 artifact–code assignment**。全部 856 个 artifact 均已编码，未决 0 个。允许在存在彼此独立证据时进行多重编码，因此类别覆盖数之和可以超过 artifact 数。

本 codebook 来自逐条完整阅读、开放编码、持续比较和反向成员复核；不继承旧 assignment 或 codebook。关键词、正则、聚类和脚本没有用于决定类别，脚本只将已经人工确认的决定转换为 GPT6-1 的发布表现形式并检查一致性。

## 类别一览

|Code|类别|覆盖 artifact 数|
|---|---|---:|
|SD01|未说明内容的待办或低信息债务标记|80|
|SD02|功能、支持范围或组件集成未完成|161|
|SD03|设计、架构或重构债务|77|
|SD04|临时 workaround、hack 或实验性方案|42|
|SD05|已知正确性、可靠性或数据质量缺陷|74|
|SD06|测试、验证或测试隔离债务|77|
|SD07|文档、示例或教学材料债务|16|
|SD08|兼容性、可移植性或外部依赖债务|87|
|SD09|性能、可扩展性或资源效率债务|55|
|SD10|局部可维护性、清理、格式或死代码债务|80|
|SD11|API、接口契约、封装或参数验证债务|102|
|SD12|硬编码假设、占位值或配置策略债务|35|
|SD13|尚未解决的设计决策或需求不确定性|150|
|SD14|债务状态不明确或可能只是解释性注释|30|

## 使用规则

- 编码作者在注释中承认、推迟、质疑或解释的债务机制，不按编程语言、项目、模型或领域命名。
- `TODO`、`FIXME`、`HACK` 只提供语用线索，不能自动决定类别；无内容标记使用 SD01。
- 明确未完成、已知错误、改进机会、开放决策和普通解释性注释必须区分。
- 一个 artifact 可多标签，例如“测试 workaround + 外部版本兼容”或“功能缺失 + 架构重构”；近义描述不重复贴标签。
- 问句、`may`、`maybe`、`perhaps` 不自动视为已证实缺陷；若核心是尚未决定的方向，使用 SD13。
- 只有“为何此步骤必要”的事实说明，不因被数据集收录就强行解释成技术债务，使用 SD14。
- 证据不足时不推断性能、安全、隐私、正确性或兼容性；截断文本按仍可直接支持的最小含义编码。

## SD01 未说明内容的待办或低信息债务标记

文本明确留下待办、修复或改进信号，但没有足够对象、动作、原因或完成标准来判断具体技术机制。

- 纳入：孤立 `TODO`/`FIXME`；单个名词或符号；`do this better`、`make nicer`、`something smarter?`；截断后只剩无法解释的改进判断。
- 排除与边界：即使对象未命名，只要明确写出“未实现”仍用 SD02；纯粹解释现有步骤且没有待办信号用 SD14；明确询问两个方案如何选择用 SD13。
- 支持：80 个 artifact。完整列表见 `codebook.json` 的 `supporting_cases`。
- 边界案例：row 2 只有 `!TODO`；row 435 只有 `AAM METRIC`；row 467 虽说“需要修复”，但问题本身完全缺失。
- 代表案例：artifact `23shades-0002-aaehidhih`（row 2；完整材料见 `results.json`）。

````text
!TODO
````

只有无内容的 TODO，无法支持更具体的债务判断。

## SD02 功能、支持范围或组件集成未完成

所需能力、分支、输入/输出类型、数据流程、模型/格式覆盖、组件接入或一般实现明确尚未完成。

- 纳入：`not implemented`；只支持部分模型、类型、维度或格式；组件尚未启用或集成；缺少保存、加载、转换、计算或命令能力。
- 排除与边界：已有能力但其接口契约或验证不稳用 SD11；已明确产生错误数据或状态用 SD05；整体职责或抽象结构需要重组用 SD03；只有名词而无动作不能凭上下文猜测，用 SD01。
- 支持：161 个 artifact。完整列表见 `codebook.json` 的 `supporting_cases`。
- 边界案例：row 123 明确说权重冻结未实现；row 319 不支持 dense 输入；row 713 既缺 imgaug 参数注册能力又依赖外部上游，因此同时使用 SD08。
- 代表案例：artifact `23shades-0123-aagfeiiaj`（row 123；完整材料见 `results.json`）。

````text
Freeze weights - TODO: NOT IMPLEMENTED!
````

权重冻结功能被明确标记为未实现。

## SD03 设计、架构或重构债务

模块边界、职责分配、依赖方向、状态归属、抽象层次、数据结构或跨组件组织需要结构性调整。

- 纳入：拆分类/函数；移动逻辑到正确模块；消除循环依赖或全局状态；建立统一抽象；重构对象生命周期或数据模型。
- 排除与边界：纯局部命名、格式、重复代码和死代码用 SD10；已有公共接口的参数、返回或封装规则用 SD11；单纯缺能力用 SD02。
- 支持：77 个 artifact。完整列表见 `codebook.json` 的 `supporting_cases`。
- 边界案例：row 1 推迟了共享函数的正式模块化；row 311 要消除全局状态；row 640 要拆解模块循环依赖。
- 代表案例：artifact `23shades-0001-aahiieiig`（row 1；完整材料见 `results.json`）。

````text
''' || Functions used by more than one algorithm || TODO refactor properly later || '''
````

共享函数被放在临时位置，作者明确推迟了模块边界和复用结构的正式重构。

## SD04 临时 workaround、hack 或实验性方案

作者明确把现有路径描述为 hack、workaround、kludge、temporary、WIP、testing-only 或短期最小修复。

- 纳入：为上游 bug 保留的绕行；测试性 hack；临时硬编码或短期代码；明确的最小可用修复。
- 排除与边界：仅有兼容约束而没有临时绕行用 SD08；普通旧代码清理用 SD10；作者只是不确定方案是否正确用 SD13。
- 支持：42 个 artifact。完整列表见 `codebook.json` 的 `supporting_cases`。
- 边界案例：row 5 是布局兼容 hack；row 177 是 messy 的最小修复；row 769 主动利用上游 bug，故同时使用 SD08。
- 代表案例：artifact `23shades-0005-aaebbecaa`（row 5；完整材料见 `results.json`）。

````text
# Hack to center SVG as justify-content is broken:
````

这是为外部布局行为失效而保留的明确 hack，同时受浏览器或布局兼容约束。

## SD05 已知正确性、可靠性或数据质量缺陷

文本直接支持当前实现会产生错误、遗漏、冲突、数据丢失、竞态、溢出、错误占位值、异常副作用或不可靠结果。

- 纳入：明确 bug；off-by-one；状态未初始化；字段被忽略或元数据丢失；错误的坐标方向；不安全的并发或资源生命周期；错误占位值误表征真实数据。
- 排除与边界：只有怀疑、尚未检查或正确方向未定用 SD06/SD13；缺少一种新能力但现有范围内没有错误用 SD02；固定假设只有潜在风险而未证实错误用 SD12。
- 支持：74 个 artifact。完整列表见 `codebook.json` 的 `supporting_cases`。
- 边界案例：row 30 明确称 `predict_proba` 的状态变化为 bug；row 274 时间索引已丢失；row 627 是明确 off-by-one。
- 代表案例：artifact `23shades-0030-aaedcebdc`（row 30；完整材料见 `results.json`）。

````text
[todo]: this is a bug; predict_proba should not change
````

作者明确称 predict_proba 的非预期状态变化为 bug。

## SD06 测试、验证或测试隔离债务

测试缺失、禁用、失败、断言过弱、测试环境受限，或某行为/命题尚未通过检查、基准或验证确认。

- 纳入：`needs testing`；补测试；测试只检查长度或写日志；测试 fixture 硬编码；“尚未检查是否工作”；数学或兼容等价性待验证。
- 排除与边界：已经确认的生产行为错误用 SD05；测试之外的开放产品/设计选择用 SD13；普通事实说明用 SD14。
- 支持：77 个 artifact。完整列表见 `codebook.json` 的 `supporting_cases`。
- 边界案例：row 273 的 ARIMA 测试只有长度断言；row 386 测试被禁用；row 662 应从 logging 改为实际断言 values。
- 代表案例：artifact `23shades-0273-aaebjbbei`（row 273；完整材料见 `results.json`）。

````text
TODO currently tests only run fit
````

ARIMA 测试只有弱长度断言，没有验证预测内容。

## SD07 文档、示例或教学材料债务

模块/API 文档、README、docstring、格式说明、教程、示例或入门材料不完整、过时或尚未编写。

- 纳入：文档占位；缺使用示例；文档与实现不同步；输出目录缺 README；已有代码尚未整理为教程。
- 排除与边界：格式本身未定义而影响机器接口时还使用 SD11；示例明确有 bug 用 SD05；实现能力缺失用 SD02。
- 支持：16 个 artifact。完整列表见 `codebook.json` 的 `supporting_cases`。
- 边界案例：row 33 缺模块概要和长描述；row 45 的 diff 格式既未文档化又未形成契约，故同时使用 SD11；row 378 文档与实现不同步。
- 代表案例：artifact `23shades-0033-aadhcadac`（row 33；完整材料见 `results.json`）。

````text
:synopsis: TODO
````

模块概要和长描述仍是文档占位。

## SD08 兼容性、可移植性或外部依赖债务

债务由特定版本、平台、运行环境、后端、字符/文件格式、外部 API、依赖升级、弃用迁移或上游能力限制驱动。

- 纳入：Python/NumPy/Pandas/TensorFlow 等版本差异；跨框架迁移；等待上游修复；平台路径或 CI 环境问题；旧格式、旧接口或外部依赖替换。
- 排除与边界：针对兼容问题采用的明确临时绕行还需 SD04；仅是局部代码删除且没有版本/依赖条件用 SD10；一般缺功能用 SD02。
- 支持：87 个 artifact。完整列表见 `codebook.json` 的 `supporting_cases`。
- 边界案例：row 52 是 Python 3.4 打包问题；row 120 是 Numba issue 的 workaround，故同时使用 SD04；row 673 是模块名与标准库冲突。
- 代表案例：artifact `23shades-0052-aaahbjdic`（row 52；完整材料见 `results.json`）。

````text
apparently package_deps are broken in 3.4
````

打包依赖配置在特定 Python 版本上已知失效。

## SD09 性能、可扩展性或资源效率债务

已知或明确提出的慢路径、复杂度风险、重复计算、未利用并行/设备能力、内存浪费、组合爆炸或资源扩展不足。

- 纳入：O(N²)；并行化机会；重复加载或复制；lazy loading；GPU/multi-GPU 扩展；缓存、内存布局和预计算优化。
- 排除与边界：只有“可能更快”且尚需验证时可同时使用 SD06/SD13；功能完全缺失用 SD02；结构重构若有独立架构意义再加 SD03。
- 支持：55 个 artifact。完整列表见 `codebook.json` 的 `supporting_cases`。
- 边界案例：row 51 生成所有组合；row 156 每批重复创建 inferer；row 733 是大图上的 O(N²) 风险。
- 代表案例：artifact `23shades-0051-aagacefbc`（row 51；完整材料见 `results.json`）。

````text
All possibilities will be generated TODO
````

无约束生成所有组合形成明显的扩展性风险，但具体剪枝策略未说明。

## SD10 局部可维护性、清理、格式或死代码债务

局部代码、测试或配置中的命名、格式、重复、冗余、弃用、死代码、魔法数字、日志风格或可读性清理。

- 纳入：删除旧方法；统一内部命名；消除重复代码；清理 unused 对象；发布前格式整理；复用已有 helper；局部可读性改善。
- 排除与边界：跨模块职责或抽象结构用 SD03；公共参数/返回/封装契约用 SD11；版本或外部依赖驱动的清理同时或改用 SD08。
- 支持：80 个 artifact。完整列表见 `codebook.json` 的 `supporting_cases`。
- 边界案例：row 25 是格式清理；row 459 是重复测试；row 794/795 是两个独立 unused artifact。
- 代表案例：artifact `23shades-0025-aajffcjii`（row 25；完整材料见 `results.json`）。

````text
@TODO: code formatting issue for 20.07 release
````

这是明确的发布前代码格式清理项。

## SD11 API、接口契约、封装或参数验证债务

公共或内部调用边界的参数、返回类型、格式/schema、可见性、封装、错误/警告、输入验证、扩展钩子或行为契约不完整或不一致。

- 纳入：返回类型不符；参数含义不一致；缺输入验证；字段 schema 不完整；实现细节泄漏；应私有化；错误类型或消息不合适；需正式配置开关。
- 排除与边界：能力根本不存在用 SD02；跨模块组织重构用 SD03；错误行为已经造成数据丢失或运行失败时可同时使用 SD05。
- 支持：102 个 artifact。完整列表见 `codebook.json` 的 `supporting_cases`。
- 边界案例：row 102 子类返回类型违反父类；row 384 `validation_split` 被接受却未使用，故同时使用 SD05；row 847 应返回 copy 保护内部状态。
- 代表案例：artifact `23shades-0102-aajeddgaa`（row 102；完整材料见 `results.json`）。

````text
FIXME: Return type \"None\" of \"fit\" incompatible with return type \"float\" in supertype \"Model\"
````

子类 fit 的返回类型违反父类声明的接口契约。

## SD12 硬编码假设、占位值或配置策略债务

常量、固定长度/比例/路径、占位数据、默认策略、数据/训练假设或运行参数被硬编码，需要配置化、动态计算、校准或替换。

- 纳入：魔法数字；固定四字节标签；随机占位标签；任意 threshold；硬编码 ratios；未外置的 seed、dtype、process 数；缺乏依据的默认值。
- 排除与边界：硬编码已明确产生错误时同时使用 SD05；一般参数验证用 SD11；单纯局部命名或死代码用 SD10。
- 支持：35 个 artifact。完整列表见 `codebook.json` 的 `supporting_cases`。
- 边界案例：row 46 把未知置信度硬编码为 1；row 452 是任意 threshold；row 814 的默认 sample 数没有依据。
- 代表案例：artifact `23shades-0046-aafchcgjg`（row 46；完整材料见 `results.json`）。

````text
\"confidence\": 1  # todo discussion confidence from GNormPlus is not provided so just putting in here 1
````

未知置信度被硬编码成 1，会把占位值误表征为真实确定性。

## SD13 尚未解决的设计决策或需求不确定性

作者记录了尚未选择的方向、未确认的必要性、开放需求、候选方案或需要先调查的语义，而不是一个已证实的单一路径缺陷。

- 纳入：问句；`may`、`maybe`、`perhaps`；两个候选方案；是否弃用、是否新增能力、是否采用某种返回类型；现有行为是否重要尚未确定。
- 排除与边界：只是尚未执行但方向明确的工作使用相应具体类别；仅需测试既定行为用 SD06；没有足够内容形成决策问题用 SD01。
- 支持：150 个 artifact。完整列表见 `codebook.json` 的 `supporting_cases`。
- 边界案例：row 11 问 gains/biases 是否可训练；row 271 在 cpickle 与 JSON 之间选择；row 729 已知破坏 layer sharing，但其重要性仍未确认，故同时使用 SD05。
- 代表案例：artifact `23shades-0011-aageijaai`（row 11；完整材料见 `results.json`）。

````text
# TODO: do we want gains\/biases to be trainable?
````

增益和偏置是否可训练是明确未解决的设计选择。

## SD14 债务状态不明确或可能只是解释性注释

文本只描述一个必要步骤、已存在行为、环境约束或事实，或者截断到无法确认待办；没有直接证据表明尚未完成、存在问题或需要后续动作。

- 纳入：`needed for correct ...`；解释测试夹具或导入为何存在；说明兼容代码当前用途但没有清理计划；纯事实性类型/缩放陈述。
- 排除与边界：明确但低信息的 TODO/FIXME 用 SD01；已知问题、开放决策或具体改进分别用对应类别。SD14 不是兜底“其他”类。
- 支持：30 个 artifact。完整列表见 `codebook.json` 的 `supporting_cases`。
- 边界案例：row 142 只解释 SysEx 正确处理的必要性；row 176 只解释更新 loss history；row 728 只陈述单个 content word 时进入分支。
- 代表案例：artifact `23shades-0142-aaeeiicii`（row 142；完整材料见 `results.json`）。

````text
needed for correct SysEx event handling
````

文本只解释某步骤对正确处理 SysEx 的必要性。

## 冻结边界与多标签规则

- SD02 vs SD11：能力、类型或分支根本缺失用 SD02；已有接口但参数、返回、验证、格式或封装不稳用 SD11。
- SD03 vs SD10：跨模块、依赖方向、职责、状态归属和抽象结构用 SD03；局部命名、格式、重复、死代码和清理用 SD10。
- SD04 vs SD08：外部版本、平台或依赖约束本身用 SD08；为该约束保留的明确临时绕行可同时使用 SD04。
- SD05 vs SD12：硬编码假设已明确造成错误或误表征时同时使用 SD05；只有潜在风险或配置僵硬时保留 SD12。
- SD06 vs SD13：行为、命题或实现状态需要验证用 SD06；最终方向或需求本身尚未决定用 SD13；两者独立并存时可多标签。
- SD01 vs SD14：SD01 仍明确是待办但内容不足；SD14 连“存在待办”都不能可靠确认，更像说明、事实或截断残片。
- 完整比较 856 条后没有出现需要新增第 15 类的稳定反例。

## 配套文件

- `codebook.json`：结构化定义、支持案例、计数、代表证据和方法元数据。
- `codebook.csv`：表格化 codebook。
- `assignments.json` / `assignments.csv`：每个 artifact 的 code、理由、逐字证据与证据限制。
- `taxonomy.json`：与 GPT6-1 一致的 HOW-style 类别树。
- `results.json`：冻结材料正文与最终类别的逐条组合。
