# CodeErrors / gpt5.6-2

Schema: `coda.artifact.v1`. Artifacts: **557**; codes: **29**; artifact–code assignments: **1254**.

This package uses the common seven-file format. All existing coding decisions, evidence and limitations are preserved. Additional source-specific fields are retained in `extensions`; original codebook text is retained in `codebook.json` metadata extensions and the local pre-conversion backup.

## Scope and method

逐条完整阅读、开放编码、持续比较、逐条人工 assignment；程序仅转换格式并验证。

单一 AI 编码；机械一致性检查不构成人工双重编码或语义准确性证明。

## Codes

| Code | Name | Artifacts |
|---|---|---:|
| CE01 | 无可执行实现 / NO_EXECUTABLE_IMPLEMENTATION | 52 |
| CE02 | 占位、示例硬编码或退化实现 / PLACEHOLDER_OR_HARDCODED_SOLUTION | 52 |
| CE03 | 语法错误或生成截断 / SYNTAX_OR_GENERATION_TRUNCATION | 29 |
| CE04 | 返回或最终收尾缺失 / RETURN_OR_FINALIZATION_MISSING | 12 |
| CE05 | 缺失或未定义依赖 / MISSING_OR_UNDEFINED_DEPENDENCY | 48 |
| CE06 | 任务或需求建模错误 / TASK_OR_REQUIREMENT_MISMODELING | 69 |
| CE07 | 输入表示或解析错误 / INPUT_REPRESENTATION_OR_PARSING | 27 |
| CE08 | 类型、容器或 API 误用 / TYPE_CONTAINER_OR_API_MISUSE | 26 |
| CE09 | 角色、层级或分析单位混淆 / ROLE_LEVEL_OR_UNIT_CONFUSION | 82 |
| CE10 | 必要谓词或筛选遗漏 / REQUIRED_PREDICATE_OR_FILTER_OMITTED | 57 |
| CE11 | 错误、反向或擅加谓词 / WRONG_OR_EXTRA_PREDICATE | 65 |
| CE12 | 分支、模式或组合覆盖不完整 / BRANCH_OR_MODE_COVERAGE | 36 |
| CE13 | 边界、基例与端点错误 / BOUNDARY_BASE_OR_EDGE_CASE | 70 |
| CE14 | 搜索或候选空间不完整/错误 / INCOMPLETE_OR_WRONG_SEARCH_SPACE | 63 |
| CE15 | 算法、公式或递推错误 / ALGORITHM_FORMULA_OR_RECURRENCE | 37 |
| CE16 | 操作顺序、优先级、结合性或逆变换错误 / OPERATION_ORDER_PRECEDENCE_OR_INVERSE | 20 |
| CE17 | 状态、控制流或终止错误 / STATE_CONTROL_OR_TERMINATION | 39 |
| CE18 | 计数、聚合或分组错误 / COUNTING_AGGREGATION_OR_GROUPING | 60 |
| CE19 | 作用域、量词或局部/全局混淆 / SCOPE_QUANTIFIER_OR_GLOBAL_LOCAL_CONFUSION | 22 |
| CE20 | 排序键、方向、主次级或排名错误 / SORT_KEY_DIRECTION_OR_RANKING | 26 |
| CE21 | 平局、多重性或等价类错误 / TIE_MULTIPLICITY_OR_EQUIVALENCE | 37 |
| CE22 | 位置/顺序保持或输入变异错误 / POSITION_ORDER_PRESERVATION_OR_MUTATION | 52 |
| CE23 | 输出类型、形状、长度或协议错误 / OUTPUT_TYPE_SHAPE_OR_PROTOCOL | 67 |
| CE24 | 数值符号、精度、舍入或数值规范化 / NUMERIC_SIGN_PRECISION_OR_ROUNDING | 36 |
| CE25 | 字符串大小写、边界、token 或分隔语义 / STRING_CASE_TOKEN_OR_DELIMITER_SEMANTICS | 55 |
| CE26 | 资源、容量或守恒约束错误 / RESOURCE_CAPACITY_OR_CONSERVATION | 11 |
| CE27 | 方向、对称排列或端点规范化 / DIRECTION_SYMMETRY_OR_ENDPOINT_NORMALIZATION | 15 |
| CE28 | 优化或选择目标错误 / WRONG_OPTIMIZATION_OR_SELECTION_OBJECTIVE | 40 |
| CE29 | 处理阶段或变换遗漏 / PIPELINE_STAGE_OR_TRANSFORMATION_OMITTED | 49 |

## CE01 — 无可执行实现 / NO_EXECUTABLE_IMPLEMENTATION

函数主体只有 `pass`、空白、TODO/注释，或虽有草稿文字却没有任何可执行求解步骤。

- Include: 显式 `pass`；docstring 后只有空白；全部候选实现均被注释掉。
- Exclude: 有可执行但恒定或身份输出（CE02）；代码因生成中断而不能解析（CE03）；已有有效计算但仅漏写 `return`（CE04）。
- Boundary/examples: artifact 734 的 `int_to_mini_roman` 只有 `pass`。
- Supporting artifacts: 52; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "1",
    "row": 1,
    "field": "incorrect_code",
    "quote": "# TODO: Implement this function",
    "interpretation": "主体只有被注释的重复草稿，没有任何可执行求解步骤；未执行的注释候选不作为占位实现编码。"
  }
]
````

## CE02 — 占位、示例硬编码或退化实现 / PLACEHOLDER_OR_HARDCODED_SOLUTION

以常量、身份函数、少量示例表、固定长度展开或与输入无关的重复生成替代通用求解。

- Include: 恒定 `True/False/0/[]`；原样返回输入；只硬编码已知示例或有限长度；重复常量、重复 replace/append 等生成退化。
- Exclude: 完全没有可执行语句（CE01）；正常算法仅漏一个边界（CE13）。
- Boundary/examples: artifact 647 对所有输入返回 `-1`；artifact 459 只记忆前五个示例。
- Supporting artifacts: 52; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "17",
    "row": 11,
    "field": "incorrect_code",
    "quote": "xs = [x / max(xs) for x in xs]",
    "interpretation": "重复无关变换替代求根，且最终没有返回。"
  }
]
````

## CE03 — 语法错误或生成截断 / SYNTAX_OR_GENERATION_TRUNCATION

材料中的实现因未闭合字符串、括号、调用、条件体或中途截断而不能作为完整程序解析。

- Include: 未闭合 docstring；末行停在 `append(`、孤立点号、缺少条件体；语法不完整。
- Exclude: 代码可解析但在未定义名字处运行失败（CE05）；可解析且隐式返回 `None`（CE04）。
- Boundary/examples: artifact 342 的 docstring 未闭合。
- Supporting artifacts: 29; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "101",
    "row": 79,
    "field": "reading_memo.evidence",
    "quote": "if k > n * m: return []（实际允许重复访问）",
    "interpretation": "实现建模为错误的最小路径和且在未完成append处截断，输出形状也不符。"
  }
]
````

## CE04 — 返回或最终收尾缺失 / RETURN_OR_FINALIZATION_MISSING

已有可执行步骤或部分求解，但没有返回所需结果、返回路径不全，或把中间状态当作最终结果。

- Include: 计算后无 `return`；部分路径隐式 `None`；只返回中间直方图而未做最终筛选。
- Exclude: 函数完全没有可执行求解步骤（CE01）；返回存在但结构错误（CE23）。
- Boundary/examples: artifact 356 构造候选结果却没有最终 `return`。
- Supporting artifacts: 12; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "17",
    "row": 11,
    "field": "incorrect_code",
    "quote": "xs = [x / max(xs) for x in xs]",
    "interpretation": "重复无关变换替代求根，且最终没有返回。"
  }
]
````

## CE05 — 缺失或未定义依赖 / MISSING_OR_UNDEFINED_DEPENDENCY

核心路径引用未导入模块、未定义辅助函数、变量或不可用 API；若补齐依赖，已有主体可能部分或全部成立。

- Include: 缺 `import hashlib`；调用材料中没有的 `is_prime`；引用未定义 `planets`/变量。
- Exclude: 对象存在但 API 使用方式错误（CE08）；语法导致标识符根本不可执行（CE03）。
- Boundary/examples: artifact 740 缺 `hashlib` 导入。
- Supporting artifacts: 48; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "5",
    "row": 5,
    "field": "incorrect_code",
    "quote": "palindrome_prefix = find_palindrome_prefix(string)",
    "interpretation": "依赖未定义辅助函数，并搜索/拼接了错误方向的回文片段。"
  }
]
````

## CE06 — 任务或需求建模错误 / TASK_OR_REQUIREMENT_MISMODELING

实现求解了与规格不同的概念，或以无关代理量替代目标性质。

- Include: 以奇偶性代理素性；把回文变为“全相等”；把路径问题建成传统最小路径和；把数位任务做成整体整数任务。
- Exclude: 正确任务模型下只漏部分候选（CE14）；单个公式写错（CE15）。
- Boundary/examples: artifact 730 用奇偶性代替素性。
- Supporting artifacts: 69; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "17",
    "row": 11,
    "field": "incorrect_code",
    "quote": "xs = [x / max(xs) for x in xs]",
    "interpretation": "重复无关变换替代求根，且最终没有返回。"
  }
]
````

## CE07 — 输入表示或解析错误 / INPUT_REPRESENTATION_OR_PARSING

错误理解输入的词法、分隔、字段、进制、token 或外层/内层结构，导致进入算法前即取错数据。

- Include: 按 `|` 拆开本应完整的音符 token；把英文数字词直接 `int`；取错字段；把列表字符串表示逐字符解析。
- Exclude: 正确解析后对类型调用错误 API（CE08）；只遗漏一种合法分隔符时可同时用 CE25。
- Boundary/examples: artifact 725 用最后两位 `x % 100` 冒充首位。
- Supporting artifacts: 27; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "6",
    "row": 6,
    "field": "incorrect_code",
    "quote": "for x in music_string.split('|')",
    "interpretation": "错误拆分音符token，并把无效片段静默映射为默认值。"
  }
]
````

## CE08 — 类型、容器或 API 误用 / TYPE_CONTAINER_OR_API_MISUSE

对对象采用不适用的运算、容器接口或库语义，或混淆标量、列表、字符串、集合与函数对象。

- Include: 对字符串做 `% 2`；对 Python 列表使用布尔高级索引；返回函数对象；把整数切片。
- Exclude: 所需 API 仅未导入（CE05）；输出类型与规格不一致但内部类型操作合法（CE23）。
- Boundary/examples: artifact 435 对字符串位直接执行 XOR。
- Supporting artifacts: 26; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "8",
    "row": 7,
    "field": "incorrect_code",
    "quote": "numbers = [int(i) for i in numbers]",
    "interpretation": "把英文数词直接作整数转换且返回了错误表示。"
  }
]
````

## CE09 — 角色、层级或分析单位混淆 / ROLE_LEVEL_OR_UNIT_CONFUSION

把索引当元素、名称当位置、参数角色互换、整体当数位、行内容当坐标，或在错误的数据层级运算。

- Include: 索引条件施加到值；字符串长度代替字符总量；主串与模式角色颠倒；整数与其数位混淆。
- Exclude: 单纯解析失败（CE07）；正确层级上公式错误（CE15）。
- Boundary/examples: artifact 727 把星球名称和轨道位置混淆。
- Supporting artifacts: 82; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "29",
    "row": 22,
    "field": "incorrect_code",
    "quote": "len(set(s0) & set(s1)) == len(s0) == len(s1)",
    "interpretation": "用原字符串长度约束字符集合，混淆集合与多重性。"
  }
]
````

## CE10 — 必要谓词或筛选遗漏 / REQUIRED_PREDICATE_OR_FILTER_OMITTED

主要数据流存在，但缺少一个或多个规格要求的资格、有效性、类型、范围或类别条件，造成过度纳入。

- Include: 未筛整数/正数/奇数；未验证三角不等式；未检查首位；未限制索引位置。
- Exclude: 使用了错误的代理谓词（CE11或CE06）；整个搜索过程不存在（CE14）。
- Boundary/examples: artifact 731 未排除负数和非整数。
- Supporting artifacts: 57; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "40",
    "row": 28,
    "field": "reading_memo.evidence",
    "quote": "area = (s * (s-a) * (s-b) * (s-c)) ** 0.5",
    "interpretation": "海伦计算前遗漏三角有效性资格检查。"
  }
]
````

## CE11 — 错误、反向或擅加谓词 / WRONG_OR_EXTRA_PREDICATE

条件存在但对象、方向、严格性或逻辑组合错误，或添加规格没有的限制，造成过度接受或拒绝。

- Include: `>=` 与 `>` 错置；末位条件反转；擅加长度/年份限制；必要条件当充分条件；恒真/恒假验证。
- Exclude: 条件完全缺失（CE10）；纯端点偏一（CE13）。
- Boundary/examples: artifact 725 用 `x % 100 in [1,3,5,7,9]` 作为首位检查。
- Supporting artifacts: 65; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "6",
    "row": 6,
    "field": "incorrect_code",
    "quote": "for x in music_string.split('|')",
    "interpretation": "错误拆分音符token，并把无效片段静默映射为默认值。"
  }
]
````

## CE12 — 分支、模式或组合覆盖不完整 / BRANCH_OR_MODE_COVERAGE

多分支、多模式或条件组合需求只实现一支，分支合并错误，或特殊情形被不当地泛化。

- Include: 只处理空白分隔而漏逗号与计数后备；无字母分支漏掉；平方/立方条件被合并；资源充足分支泛化到不足情形。
- Exclude: 漏枚举候选对象（CE14）；仅循环端点错误（CE13）。
- Boundary/examples: artifact 737 只实现库存足够的更新公式。
- Supporting artifacts: 36; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "58",
    "row": 43,
    "field": "incorrect_code",
    "quote": "pivot = array[0]",
    "interpretation": "排序方向的条件分支未实现，递归近似固定升序。"
  }
]
````

## CE13 — 边界、基例与端点错误 / BOUNDARY_BASE_OR_EDGE_CASE

算法主体接近规格，但在空输入、零/一、首末位置、包含端点、递归基例、off-by-one 或极小规模上失败。

- Include: range漏上界；空列表 `max`；递归基例值错；切片端点偏一；长度1越界。
- Exclude: 候选域整体被错误限制（CE14）；擅加语义条件（CE11）。
- Boundary/examples: artifact 437 产生空前缀并遗漏完整前缀。
- Supporting artifacts: 70; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "3",
    "row": 3,
    "field": "incorrect_code",
    "quote": "return [delimeter] + [numbers[i] for i in range(len(numbers) - 1)] + [delimeter]",
    "interpretation": "分隔符位置、元素保留和空输入结构均不符合协议。"
  }
]
````

## CE14 — 搜索或候选空间不完整/错误 / INCOMPLETE_OR_WRONG_SEARCH_SPACE

需要枚举、查找或探索多个候选时，只考察固定、相邻、首个、少数示例或错误候选域。

- Include: 只检查相邻三元组；只旋转一次；只比较前两项；只把 c 当斜边；未遍历所有组合。
- Exclude: 候选齐全但评分目标错误（CE28）；循环端点仅偏一（CE13）。
- Boundary/examples: artifact 733 未枚举 b 的所有循环旋转。
- Supporting artifacts: 63; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "5",
    "row": 5,
    "field": "incorrect_code",
    "quote": "palindrome_prefix = find_palindrome_prefix(string)",
    "interpretation": "依赖未定义辅助函数，并搜索/拼接了错误方向的回文片段。"
  }
]
````

## CE15 — 算法、公式或递推错误 / ALGORITHM_FORMULA_OR_RECURRENCE

任务模型大体正确，但数学公式、状态转移、闭式、递推或核心运算关系不正确。

- Include: 错误勾股/海伦/导数公式；递推窗口公式错误；碰撞数误算；资源更新公式错误。
- Exclude: 完全求解了另一个任务（CE06）；只把运算顺序/优先级弄错（CE16）。
- Boundary/examples: artifact 737 用 `number+need, remaining-need` 无条件更新。
- Supporting artifacts: 37; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "23",
    "row": 17,
    "field": "incorrect_code",
    "quote": "for i in range(len(l) - 2)",
    "interpretation": "只检查相邻三元组且和为零的代数关系写反。"
  }
]
````

## CE16 — 操作顺序、优先级、结合性或逆变换错误 / OPERATION_ORDER_PRECEDENCE_OR_INVERSE

所需步骤存在或可辨认，但执行顺序、括号、优先级、组合方式或正逆方向错误。

- Include: 先平方再 ceiling；表达式全左结合；decode 复制 encode；元音跳过先换大小写；循环移位方向相反。
- Exclude: 排序方向/主次键错误（CE20）；普通公式项错误（CE15）。
- Boundary/examples: artifact 387 忽略运算符优先级与幂结合性。
- Supporting artifacts: 20; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "21",
    "row": 15,
    "field": "reading_memo.evidence",
    "quote": "decode_cyclic 中仍为 group[1:] + group[0]",
    "interpretation": "解码复制正向左循环而非执行逆向循环。"
  }
]
````

## CE17 — 状态、控制流或终止错误 / STATE_CONTROL_OR_TERMINATION

累计状态未保存/错误更新，返回时机过早，递归不收敛，循环不终止，或候选间状态相互污染。

- Include: 未传递前缀余额；前向递归；全局 visited 污染路径；过早返回首个候选；记录时机错误。
- Exclude: 递归基例值单独错误（CE13）；状态公式本身错误可同时用 CE15。
- Boundary/examples: artifact 2 的递归没有传递累计余额。
- Supporting artifacts: 39; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "2",
    "row": 2,
    "field": "reading_memo.evidence",
    "quote": "if operations[0] < 0: return True",
    "interpretation": "递归未携带累计余额，把前缀累计性质降成逐项负号检查。"
  }
]
````

## CE18 — 计数、聚合或分组错误 / COUNTING_AGGREGATION_OR_GROUPING

计数单位、聚合对象、分组层级、去重方式或累积范围不符合规格。

- Include: 存在性代替出现次数；求和代替计数；逐格代替逐井；全局取整代替逐组取整；多计或漏计。
- Exclude: 选错最大/最小目标（CE28）；候选根本未枚举（CE14）。
- Boundary/examples: artifact 726 把三元组计数替换成3的倍数个数。
- Supporting artifacts: 60; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "19",
    "row": 13,
    "field": "incorrect_code",
    "quote": "if \"7\" in str(i):",
    "interpretation": "按含7的数计一次，而非统计每次数字7出现。"
  }
]
````

## CE19 — 作用域、量词或局部/全局混淆 / SCOPE_QUANTIFIER_OR_GLOBAL_LOCAL_CONFUSION

把存在性当全称、局部窗口当全局集合、逐元素性质当跨元素一致性，或把子序列问题收紧为整串有效性。

- Include: 局部三字符互异改成全串只有3种字符；存在有效子序列改成整个输入平衡；每个 key 合法误作所有 key 同一大小写。
- Exclude: 候选列表不完整（CE14）；聚合单位错误（CE18）。
- Boundary/examples: artifact 519 只验证各键自身大小写合法，未验证全局一致。
- Supporting artifacts: 22; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "2",
    "row": 2,
    "field": "reading_memo.evidence",
    "quote": "if operations[0] < 0: return True",
    "interpretation": "递归未携带累计余额，把前缀累计性质降成逐项负号检查。"
  }
]
````

## CE20 — 排序键、方向、主次级或排名错误 / SORT_KEY_DIRECTION_OR_RANKING

排序/排名存在，但使用了错误键、方向、主次级关系或仅字典序等不完整复合键。

- Include: 长度主键遗漏；降序结果应升序；按字符串字典序代替数值；多关键字优先级颠倒。
- Exclude: 平局规则、稳定性或 distinct 语义（CE21）；优化目标不是排序而是路径/距离时用 CE28。
- Boundary/examples: artifact 729 只按字典序，遗漏长度主键。
- Supporting artifacts: 26; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "56",
    "row": 42,
    "field": "incorrect_code",
    "quote": "sorted(s.split(), key=lambda x: ''.join(sorted(x)))",
    "interpretation": "在词间而非词内排序，破坏词序与空白保真。"
  }
]
````

## CE21 — 平局、多重性或等价类错误 / TIE_MULTIPLICITY_OR_EQUIVALENCE

没有正确处理平局、重复值、集合/多重集合、distinct、稳定首现或等价类规范化。

- Include: 平局未按字典序；set 去重代替删除所有重复；第二小未去重；同值次数约束错；排序后丢失首现映射。
- Exclude: 一般顺序/位置保持（CE22）；普通筛选遗漏（CE10）。
- Boundary/examples: artifact 732 排序后无法保留强度平局时的原始首项。
- Supporting artifacts: 37; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "13",
    "row": 10,
    "field": "incorrect_code",
    "quote": "return list(set(numbers))",
    "interpretation": "set的去重/无序语义不等于删除所有重复值并保持原序。"
  }
]
````

## CE22 — 位置/顺序保持或输入变异错误 / POSITION_ORDER_PRESERVATION_OR_MUTATION

错误重排、删除、复制或修改原位置；未保持非目标元素/原顺序；产生未要求的原地变异。

- Include: 分区拼接代替原位回填；全局排序破坏受保护位置；输入原地修改；含字母串被反转。
- Exclude: 排序方向/键本身错误（CE20）；仅输出格式错误（CE23）。
- Boundary/examples: artifact 739 在含字母情形错误反转字符顺序。
- Supporting artifacts: 52; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "3",
    "row": 3,
    "field": "incorrect_code",
    "quote": "return [delimeter] + [numbers[i] for i in range(len(numbers) - 1)] + [delimeter]",
    "interpretation": "分隔符位置、元素保留和空输入结构均不符合协议。"
  }
]
````

## CE23 — 输出类型、形状、长度或协议错误 / OUTPUT_TYPE_SHAPE_OR_PROTOCOL

返回内容的容器类型、字段、长度、模板、前后缀、分隔、布尔/字符串协议或结构不符合规格。

- Include: 返回字典而非众数字母；漏 `0b`；元组字段含义错；列表长度错误；模板替换错误。
- Exclude: 值本身算法错误但输出结构正确（CE15）；完全缺少返回（CE04）。
- Boundary/examples: artifact 353 计算值正确但移除了 `0b` 前缀。
- Supporting artifacts: 67; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "3",
    "row": 3,
    "field": "incorrect_code",
    "quote": "return [delimeter] + [numbers[i] for i in range(len(numbers) - 1)] + [delimeter]",
    "interpretation": "分隔符位置、元素保留和空输入结构均不符合协议。"
  }
]
````

## CE24 — 数值符号、精度、舍入或数值规范化 / NUMERIC_SIGN_PRECISION_OR_ROUNDING

负号语义、浮点稳定性、整数除法、数值字符串规范化或舍入规则处理错误。

- Include: 先 `abs` 丢失带符号首位；浮点立方根精确相等；银行家舍入不符；真除法破坏整数状态；逗号小数未规范化。
- Exclude: 一般范围/端点错误（CE13）；类型 API 本身不可用（CE08，可共现）。
- Boundary/examples: artifact 724 用 `abs` 抹去负号权重。
- Supporting artifacts: 36; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "46",
    "row": 34,
    "field": "incorrect_code",
    "quote": "return a**(1/3) % 1 == 0",
    "interpretation": "浮点立方根精确比较不稳健且负数产生复数域问题。"
  }
]
````

## CE25 — 字符串大小写、边界、token 或分隔语义 / STRING_CASE_TOKEN_OR_DELIMITER_SEMANTICS

大小写覆盖、逐字符变换、词/句边界、分隔符集合、空白保真或重叠字符串语义处理错误。

- Include: 只处理小写元音；`I` 前缀过宽；逗号未分隔；用 `str.count` 漏重叠；大小写互换只做单向。
- Exclude: 输入字段解析的结构性误解（CE07，可共现）；输出分隔协议（CE23）。
- Boundary/examples: artifact 739 有字母时未逐字符 swapcase。
- Supporting artifacts: 55; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "6",
    "row": 6,
    "field": "incorrect_code",
    "quote": "for x in music_string.split('|')",
    "interpretation": "错误拆分音符token，并把无效片段静默映射为默认值。"
  }
]
````

## CE26 — 资源、容量或守恒约束错误 / RESOURCE_CAPACITY_OR_CONSERVATION

任务包含库存、容量、供需、可用次数或守恒关系时，没有限制消耗、错误跨组共享资源或更新出非法状态。

- Include: 库存不足仍消费 need；井之间共享桶容量余量；交换所需奇数与可供偶数未比较。
- Exclude: 一般资格条件遗漏（CE10）；普通算术公式错误但无资源含义（CE15）。
- Boundary/examples: artifact 737 产生负库存。
- Supporting artifacts: 11; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "82",
    "row": 65,
    "field": "incorrect_code",
    "quote": "sum(lst1) == sum(lst2) and sum(lst1) % 2 == 0",
    "interpretation": "资源供需关系被无关总和条件替代。"
  }
]
````

## CE27 — 方向、对称排列或端点规范化 / DIRECTION_SYMMETRY_OR_ENDPOINT_NORMALIZATION

规格对输入排列、两个端点、正反方向或对称角色不敏感，但实现只处理一个方向/排列且未规范化。

- Include: a>b 未交换；只把 c 当斜边；只检查一种加法排列；只接受单调递增而不接受递减。
- Exclude: 编码/解码的逆操作错误（CE16）；排序升降方向错误（CE20）。
- Boundary/examples: artifact 735 漏掉 a、b 作为斜边的对称情形。
- Supporting artifacts: 15; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "139",
    "row": 110,
    "field": "reading_memo.evidence",
    "quote": "range(a,b+1)",
    "interpretation": "未规范化反向端点且候选域错误扩展到多位整数。"
  }
]
````

## CE28 — 优化或选择目标错误 / WRONG_OPTIMIZATION_OR_SELECTION_OBJECTIVE

候选已经存在或搜索框架可辨认，但最小/最大、最近/极值、完整词典序/局部代理等目标函数错误。

- Include: 选最小强度而非最大；最近数对取全局极值；路径只比较末项；最大合格值取首个合格值。
- Exclude: 候选空间本身缺失（CE14，可共现）；排序键规则（CE20）。
- Boundary/examples: artifact 732 将强度升序后选择最小值。
- Supporting artifacts: 40; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "9",
    "row": 8,
    "field": "incorrect_code",
    "quote": "numbers.sort()",
    "interpretation": "最近数对目标被替换为全局最小值与最大值。"
  }
]
````

## CE29 — 处理阶段或变换遗漏 / PIPELINE_STAGE_OR_TRANSFORMATION_OMITTED

多阶段需求中，数据流总体方向可辨认，但跳过了一个核心中间变换、构造或后处理阶段。

- Include: 直接把 N 转二进制而未先求十进制数位和；只筛选未映射；未构造规定数组即计数；已取得候选却未做最终过滤。
- Exclude: 整个算法不存在（CE01）；单个资格谓词遗漏（CE10）；只缺返回（CE04）。
- Boundary/examples: artifact 726 未构造 `a[i]=i*i-i+1`。
- Supporting artifacts: 49; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "54",
    "row": 40,
    "field": "incorrect_code",
    "quote": "return bin(N)[2:]",
    "interpretation": "跳过十进制数位求和，直接编码原数。"
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

# gpt5.6-2 — CodeErrors 最终编码本

本轮覆盖 **557 个 artifact**，形成 **29 个可分配 code**，共记录 **1254 个 artifact–code assignment**。全部 artifact 均已逐件阅读并编码。

本文件按 GPT6-1 七文件发布格式生成。语义判断来自已完成的逐件阅读与人工 assignment；格式转换程序不读取正文选择代码，只负责序列化、计数和一致性核验。

## 类别一览

|Code|类别|覆盖 artifact 数|
|---|---|---:|
|CE01|无可执行实现 / NO_EXECUTABLE_IMPLEMENTATION|52|
|CE02|占位、示例硬编码或退化实现 / PLACEHOLDER_OR_HARDCODED_SOLUTION|52|
|CE03|语法错误或生成截断 / SYNTAX_OR_GENERATION_TRUNCATION|29|
|CE04|返回或最终收尾缺失 / RETURN_OR_FINALIZATION_MISSING|12|
|CE05|缺失或未定义依赖 / MISSING_OR_UNDEFINED_DEPENDENCY|48|
|CE06|任务或需求建模错误 / TASK_OR_REQUIREMENT_MISMODELING|69|
|CE07|输入表示或解析错误 / INPUT_REPRESENTATION_OR_PARSING|27|
|CE08|类型、容器或 API 误用 / TYPE_CONTAINER_OR_API_MISUSE|26|
|CE09|角色、层级或分析单位混淆 / ROLE_LEVEL_OR_UNIT_CONFUSION|82|
|CE10|必要谓词或筛选遗漏 / REQUIRED_PREDICATE_OR_FILTER_OMITTED|57|
|CE11|错误、反向或擅加谓词 / WRONG_OR_EXTRA_PREDICATE|65|
|CE12|分支、模式或组合覆盖不完整 / BRANCH_OR_MODE_COVERAGE|36|
|CE13|边界、基例与端点错误 / BOUNDARY_BASE_OR_EDGE_CASE|70|
|CE14|搜索或候选空间不完整/错误 / INCOMPLETE_OR_WRONG_SEARCH_SPACE|63|
|CE15|算法、公式或递推错误 / ALGORITHM_FORMULA_OR_RECURRENCE|37|
|CE16|操作顺序、优先级、结合性或逆变换错误 / OPERATION_ORDER_PRECEDENCE_OR_INVERSE|20|
|CE17|状态、控制流或终止错误 / STATE_CONTROL_OR_TERMINATION|39|
|CE18|计数、聚合或分组错误 / COUNTING_AGGREGATION_OR_GROUPING|60|
|CE19|作用域、量词或局部/全局混淆 / SCOPE_QUANTIFIER_OR_GLOBAL_LOCAL_CONFUSION|22|
|CE20|排序键、方向、主次级或排名错误 / SORT_KEY_DIRECTION_OR_RANKING|26|
|CE21|平局、多重性或等价类错误 / TIE_MULTIPLICITY_OR_EQUIVALENCE|37|
|CE22|位置/顺序保持或输入变异错误 / POSITION_ORDER_PRESERVATION_OR_MUTATION|52|
|CE23|输出类型、形状、长度或协议错误 / OUTPUT_TYPE_SHAPE_OR_PROTOCOL|67|
|CE24|数值符号、精度、舍入或数值规范化 / NUMERIC_SIGN_PRECISION_OR_ROUNDING|36|
|CE25|字符串大小写、边界、token 或分隔语义 / STRING_CASE_TOKEN_OR_DELIMITER_SEMANTICS|55|
|CE26|资源、容量或守恒约束错误 / RESOURCE_CAPACITY_OR_CONSERVATION|11|
|CE27|方向、对称排列或端点规范化 / DIRECTION_SYMMETRY_OR_ENDPOINT_NORMALIZATION|15|
|CE28|优化或选择目标错误 / WRONG_OPTIMIZATION_OR_SELECTION_OBJECTIVE|40|
|CE29|处理阶段或变换遗漏 / PIPELINE_STAGE_OR_TRANSFORMATION_OMITTED|49|

## 使用规则

- CE01 不自动附带 CE04；只有存在实质计算但最终返回缺失时才用 CE04。
- CE03 与 CE05 区分“不能解析”和“能解析但名字未定义”。
- CE06 用于任务概念被替换；CE15 用于仍在正确概念内但公式错误。
- CE10 是条件遗漏；CE11 是已有条件错误、反向或擅加。
- CE14 是候选空间；CE28 是候选评分/选择目标。二者可共现，但需要两项独立证据。
- CE20 是排序规则；CE21 是平局、多重性与等价类；CE22 是原位置/顺序和输入变异。
- CE18 聚焦计数与聚合；CE19 聚焦存在/全称、局部/全局等量词作用域。
- CE24 只用于数值表示的符号、精度、舍入或规范化，不作为所有算术错误的兜底代码。

## CE01 无可执行实现 / NO_EXECUTABLE_IMPLEMENTATION

函数主体只有 `pass`、空白、TODO/注释，或虽有草稿文字却没有任何可执行求解步骤。

- 纳入：显式 `pass`；docstring 后只有空白；全部候选实现均被注释掉。
- 排除与边界：有可执行但恒定或身份输出（CE02）；代码因生成中断而不能解析（CE03）；已有有效计算但仅漏写 `return`（CE04）。
- 边界说明：artifact 734 的 `int_to_mini_roman` 只有 `pass`。
- 支持：52 个 artifact；完整列表见 `codebook.json`。
- 代表案例：artifact `1`（row 1；完整材料见 `results.json`）。

````text
# TODO: Implement this function
````

主体只有被注释的重复草稿，没有任何可执行求解步骤；未执行的注释候选不作为占位实现编码。

## CE02 占位、示例硬编码或退化实现 / PLACEHOLDER_OR_HARDCODED_SOLUTION

以常量、身份函数、少量示例表、固定长度展开或与输入无关的重复生成替代通用求解。

- 纳入：恒定 `True/False/0/[]`；原样返回输入；只硬编码已知示例或有限长度；重复常量、重复 replace/append 等生成退化。
- 排除与边界：完全没有可执行语句（CE01）；正常算法仅漏一个边界（CE13）。
- 边界说明：artifact 647 对所有输入返回 `-1`；artifact 459 只记忆前五个示例。
- 支持：52 个 artifact；完整列表见 `codebook.json`。
- 代表案例：artifact `17`（row 11；完整材料见 `results.json`）。

````text
xs = [x / max(xs) for x in xs]
````

重复无关变换替代求根，且最终没有返回。

## CE03 语法错误或生成截断 / SYNTAX_OR_GENERATION_TRUNCATION

材料中的实现因未闭合字符串、括号、调用、条件体或中途截断而不能作为完整程序解析。

- 纳入：未闭合 docstring；末行停在 `append(`、孤立点号、缺少条件体；语法不完整。
- 排除与边界：代码可解析但在未定义名字处运行失败（CE05）；可解析且隐式返回 `None`（CE04）。
- 边界说明：artifact 342 的 docstring 未闭合。
- 支持：29 个 artifact；完整列表见 `codebook.json`。
- 代表案例：artifact `101`（row 79；完整材料见 `results.json`）。

````text
if k > n * m: return []（实际允许重复访问）
````

实现建模为错误的最小路径和且在未完成append处截断，输出形状也不符。

## CE04 返回或最终收尾缺失 / RETURN_OR_FINALIZATION_MISSING

已有可执行步骤或部分求解，但没有返回所需结果、返回路径不全，或把中间状态当作最终结果。

- 纳入：计算后无 `return`；部分路径隐式 `None`；只返回中间直方图而未做最终筛选。
- 排除与边界：函数完全没有可执行求解步骤（CE01）；返回存在但结构错误（CE23）。
- 边界说明：artifact 356 构造候选结果却没有最终 `return`。
- 支持：12 个 artifact；完整列表见 `codebook.json`。
- 代表案例：artifact `17`（row 11；完整材料见 `results.json`）。

````text
xs = [x / max(xs) for x in xs]
````

重复无关变换替代求根，且最终没有返回。

## CE05 缺失或未定义依赖 / MISSING_OR_UNDEFINED_DEPENDENCY

核心路径引用未导入模块、未定义辅助函数、变量或不可用 API；若补齐依赖，已有主体可能部分或全部成立。

- 纳入：缺 `import hashlib`；调用材料中没有的 `is_prime`；引用未定义 `planets`/变量。
- 排除与边界：对象存在但 API 使用方式错误（CE08）；语法导致标识符根本不可执行（CE03）。
- 边界说明：artifact 740 缺 `hashlib` 导入。
- 支持：48 个 artifact；完整列表见 `codebook.json`。
- 代表案例：artifact `5`（row 5；完整材料见 `results.json`）。

````text
palindrome_prefix = find_palindrome_prefix(string)
````

依赖未定义辅助函数，并搜索/拼接了错误方向的回文片段。

## CE06 任务或需求建模错误 / TASK_OR_REQUIREMENT_MISMODELING

实现求解了与规格不同的概念，或以无关代理量替代目标性质。

- 纳入：以奇偶性代理素性；把回文变为“全相等”；把路径问题建成传统最小路径和；把数位任务做成整体整数任务。
- 排除与边界：正确任务模型下只漏部分候选（CE14）；单个公式写错（CE15）。
- 边界说明：artifact 730 用奇偶性代替素性。
- 支持：69 个 artifact；完整列表见 `codebook.json`。
- 代表案例：artifact `17`（row 11；完整材料见 `results.json`）。

````text
xs = [x / max(xs) for x in xs]
````

重复无关变换替代求根，且最终没有返回。

## CE07 输入表示或解析错误 / INPUT_REPRESENTATION_OR_PARSING

错误理解输入的词法、分隔、字段、进制、token 或外层/内层结构，导致进入算法前即取错数据。

- 纳入：按 `|` 拆开本应完整的音符 token；把英文数字词直接 `int`；取错字段；把列表字符串表示逐字符解析。
- 排除与边界：正确解析后对类型调用错误 API（CE08）；只遗漏一种合法分隔符时可同时用 CE25。
- 边界说明：artifact 725 用最后两位 `x % 100` 冒充首位。
- 支持：27 个 artifact；完整列表见 `codebook.json`。
- 代表案例：artifact `6`（row 6；完整材料见 `results.json`）。

````text
for x in music_string.split('|')
````

错误拆分音符token，并把无效片段静默映射为默认值。

## CE08 类型、容器或 API 误用 / TYPE_CONTAINER_OR_API_MISUSE

对对象采用不适用的运算、容器接口或库语义，或混淆标量、列表、字符串、集合与函数对象。

- 纳入：对字符串做 `% 2`；对 Python 列表使用布尔高级索引；返回函数对象；把整数切片。
- 排除与边界：所需 API 仅未导入（CE05）；输出类型与规格不一致但内部类型操作合法（CE23）。
- 边界说明：artifact 435 对字符串位直接执行 XOR。
- 支持：26 个 artifact；完整列表见 `codebook.json`。
- 代表案例：artifact `8`（row 7；完整材料见 `results.json`）。

````text
numbers = [int(i) for i in numbers]
````

把英文数词直接作整数转换且返回了错误表示。

## CE09 角色、层级或分析单位混淆 / ROLE_LEVEL_OR_UNIT_CONFUSION

把索引当元素、名称当位置、参数角色互换、整体当数位、行内容当坐标，或在错误的数据层级运算。

- 纳入：索引条件施加到值；字符串长度代替字符总量；主串与模式角色颠倒；整数与其数位混淆。
- 排除与边界：单纯解析失败（CE07）；正确层级上公式错误（CE15）。
- 边界说明：artifact 727 把星球名称和轨道位置混淆。
- 支持：82 个 artifact；完整列表见 `codebook.json`。
- 代表案例：artifact `29`（row 22；完整材料见 `results.json`）。

````text
len(set(s0) & set(s1)) == len(s0) == len(s1)
````

用原字符串长度约束字符集合，混淆集合与多重性。

## CE10 必要谓词或筛选遗漏 / REQUIRED_PREDICATE_OR_FILTER_OMITTED

主要数据流存在，但缺少一个或多个规格要求的资格、有效性、类型、范围或类别条件，造成过度纳入。

- 纳入：未筛整数/正数/奇数；未验证三角不等式；未检查首位；未限制索引位置。
- 排除与边界：使用了错误的代理谓词（CE11或CE06）；整个搜索过程不存在（CE14）。
- 边界说明：artifact 731 未排除负数和非整数。
- 支持：57 个 artifact；完整列表见 `codebook.json`。
- 代表案例：artifact `40`（row 28；完整材料见 `results.json`）。

````text
area = (s * (s-a) * (s-b) * (s-c)) ** 0.5
````

海伦计算前遗漏三角有效性资格检查。

## CE11 错误、反向或擅加谓词 / WRONG_OR_EXTRA_PREDICATE

条件存在但对象、方向、严格性或逻辑组合错误，或添加规格没有的限制，造成过度接受或拒绝。

- 纳入：`>=` 与 `>` 错置；末位条件反转；擅加长度/年份限制；必要条件当充分条件；恒真/恒假验证。
- 排除与边界：条件完全缺失（CE10）；纯端点偏一（CE13）。
- 边界说明：artifact 725 用 `x % 100 in [1,3,5,7,9]` 作为首位检查。
- 支持：65 个 artifact；完整列表见 `codebook.json`。
- 代表案例：artifact `6`（row 6；完整材料见 `results.json`）。

````text
for x in music_string.split('|')
````

错误拆分音符token，并把无效片段静默映射为默认值。

## CE12 分支、模式或组合覆盖不完整 / BRANCH_OR_MODE_COVERAGE

多分支、多模式或条件组合需求只实现一支，分支合并错误，或特殊情形被不当地泛化。

- 纳入：只处理空白分隔而漏逗号与计数后备；无字母分支漏掉；平方/立方条件被合并；资源充足分支泛化到不足情形。
- 排除与边界：漏枚举候选对象（CE14）；仅循环端点错误（CE13）。
- 边界说明：artifact 737 只实现库存足够的更新公式。
- 支持：36 个 artifact；完整列表见 `codebook.json`。
- 代表案例：artifact `58`（row 43；完整材料见 `results.json`）。

````text
pivot = array[0]
````

排序方向的条件分支未实现，递归近似固定升序。

## CE13 边界、基例与端点错误 / BOUNDARY_BASE_OR_EDGE_CASE

算法主体接近规格，但在空输入、零/一、首末位置、包含端点、递归基例、off-by-one 或极小规模上失败。

- 纳入：range漏上界；空列表 `max`；递归基例值错；切片端点偏一；长度1越界。
- 排除与边界：候选域整体被错误限制（CE14）；擅加语义条件（CE11）。
- 边界说明：artifact 437 产生空前缀并遗漏完整前缀。
- 支持：70 个 artifact；完整列表见 `codebook.json`。
- 代表案例：artifact `3`（row 3；完整材料见 `results.json`）。

````text
return [delimeter] + [numbers[i] for i in range(len(numbers) - 1)] + [delimeter]
````

分隔符位置、元素保留和空输入结构均不符合协议。

## CE14 搜索或候选空间不完整/错误 / INCOMPLETE_OR_WRONG_SEARCH_SPACE

需要枚举、查找或探索多个候选时，只考察固定、相邻、首个、少数示例或错误候选域。

- 纳入：只检查相邻三元组；只旋转一次；只比较前两项；只把 c 当斜边；未遍历所有组合。
- 排除与边界：候选齐全但评分目标错误（CE28）；循环端点仅偏一（CE13）。
- 边界说明：artifact 733 未枚举 b 的所有循环旋转。
- 支持：63 个 artifact；完整列表见 `codebook.json`。
- 代表案例：artifact `5`（row 5；完整材料见 `results.json`）。

````text
palindrome_prefix = find_palindrome_prefix(string)
````

依赖未定义辅助函数，并搜索/拼接了错误方向的回文片段。

## CE15 算法、公式或递推错误 / ALGORITHM_FORMULA_OR_RECURRENCE

任务模型大体正确，但数学公式、状态转移、闭式、递推或核心运算关系不正确。

- 纳入：错误勾股/海伦/导数公式；递推窗口公式错误；碰撞数误算；资源更新公式错误。
- 排除与边界：完全求解了另一个任务（CE06）；只把运算顺序/优先级弄错（CE16）。
- 边界说明：artifact 737 用 `number+need, remaining-need` 无条件更新。
- 支持：37 个 artifact；完整列表见 `codebook.json`。
- 代表案例：artifact `23`（row 17；完整材料见 `results.json`）。

````text
for i in range(len(l) - 2)
````

只检查相邻三元组且和为零的代数关系写反。

## CE16 操作顺序、优先级、结合性或逆变换错误 / OPERATION_ORDER_PRECEDENCE_OR_INVERSE

所需步骤存在或可辨认，但执行顺序、括号、优先级、组合方式或正逆方向错误。

- 纳入：先平方再 ceiling；表达式全左结合；decode 复制 encode；元音跳过先换大小写；循环移位方向相反。
- 排除与边界：排序方向/主次键错误（CE20）；普通公式项错误（CE15）。
- 边界说明：artifact 387 忽略运算符优先级与幂结合性。
- 支持：20 个 artifact；完整列表见 `codebook.json`。
- 代表案例：artifact `21`（row 15；完整材料见 `results.json`）。

````text
decode_cyclic 中仍为 group[1:] + group[0]
````

解码复制正向左循环而非执行逆向循环。

## CE17 状态、控制流或终止错误 / STATE_CONTROL_OR_TERMINATION

累计状态未保存/错误更新，返回时机过早，递归不收敛，循环不终止，或候选间状态相互污染。

- 纳入：未传递前缀余额；前向递归；全局 visited 污染路径；过早返回首个候选；记录时机错误。
- 排除与边界：递归基例值单独错误（CE13）；状态公式本身错误可同时用 CE15。
- 边界说明：artifact 2 的递归没有传递累计余额。
- 支持：39 个 artifact；完整列表见 `codebook.json`。
- 代表案例：artifact `2`（row 2；完整材料见 `results.json`）。

````text
if operations[0] < 0: return True
````

递归未携带累计余额，把前缀累计性质降成逐项负号检查。

## CE18 计数、聚合或分组错误 / COUNTING_AGGREGATION_OR_GROUPING

计数单位、聚合对象、分组层级、去重方式或累积范围不符合规格。

- 纳入：存在性代替出现次数；求和代替计数；逐格代替逐井；全局取整代替逐组取整；多计或漏计。
- 排除与边界：选错最大/最小目标（CE28）；候选根本未枚举（CE14）。
- 边界说明：artifact 726 把三元组计数替换成3的倍数个数。
- 支持：60 个 artifact；完整列表见 `codebook.json`。
- 代表案例：artifact `19`（row 13；完整材料见 `results.json`）。

````text
if "7" in str(i):
````

按含7的数计一次，而非统计每次数字7出现。

## CE19 作用域、量词或局部/全局混淆 / SCOPE_QUANTIFIER_OR_GLOBAL_LOCAL_CONFUSION

把存在性当全称、局部窗口当全局集合、逐元素性质当跨元素一致性，或把子序列问题收紧为整串有效性。

- 纳入：局部三字符互异改成全串只有3种字符；存在有效子序列改成整个输入平衡；每个 key 合法误作所有 key 同一大小写。
- 排除与边界：候选列表不完整（CE14）；聚合单位错误（CE18）。
- 边界说明：artifact 519 只验证各键自身大小写合法，未验证全局一致。
- 支持：22 个 artifact；完整列表见 `codebook.json`。
- 代表案例：artifact `2`（row 2；完整材料见 `results.json`）。

````text
if operations[0] < 0: return True
````

递归未携带累计余额，把前缀累计性质降成逐项负号检查。

## CE20 排序键、方向、主次级或排名错误 / SORT_KEY_DIRECTION_OR_RANKING

排序/排名存在，但使用了错误键、方向、主次级关系或仅字典序等不完整复合键。

- 纳入：长度主键遗漏；降序结果应升序；按字符串字典序代替数值；多关键字优先级颠倒。
- 排除与边界：平局规则、稳定性或 distinct 语义（CE21）；优化目标不是排序而是路径/距离时用 CE28。
- 边界说明：artifact 729 只按字典序，遗漏长度主键。
- 支持：26 个 artifact；完整列表见 `codebook.json`。
- 代表案例：artifact `56`（row 42；完整材料见 `results.json`）。

````text
sorted(s.split(), key=lambda x: ''.join(sorted(x)))
````

在词间而非词内排序，破坏词序与空白保真。

## CE21 平局、多重性或等价类错误 / TIE_MULTIPLICITY_OR_EQUIVALENCE

没有正确处理平局、重复值、集合/多重集合、distinct、稳定首现或等价类规范化。

- 纳入：平局未按字典序；set 去重代替删除所有重复；第二小未去重；同值次数约束错；排序后丢失首现映射。
- 排除与边界：一般顺序/位置保持（CE22）；普通筛选遗漏（CE10）。
- 边界说明：artifact 732 排序后无法保留强度平局时的原始首项。
- 支持：37 个 artifact；完整列表见 `codebook.json`。
- 代表案例：artifact `13`（row 10；完整材料见 `results.json`）。

````text
return list(set(numbers))
````

set的去重/无序语义不等于删除所有重复值并保持原序。

## CE22 位置/顺序保持或输入变异错误 / POSITION_ORDER_PRESERVATION_OR_MUTATION

错误重排、删除、复制或修改原位置；未保持非目标元素/原顺序；产生未要求的原地变异。

- 纳入：分区拼接代替原位回填；全局排序破坏受保护位置；输入原地修改；含字母串被反转。
- 排除与边界：排序方向/键本身错误（CE20）；仅输出格式错误（CE23）。
- 边界说明：artifact 739 在含字母情形错误反转字符顺序。
- 支持：52 个 artifact；完整列表见 `codebook.json`。
- 代表案例：artifact `3`（row 3；完整材料见 `results.json`）。

````text
return [delimeter] + [numbers[i] for i in range(len(numbers) - 1)] + [delimeter]
````

分隔符位置、元素保留和空输入结构均不符合协议。

## CE23 输出类型、形状、长度或协议错误 / OUTPUT_TYPE_SHAPE_OR_PROTOCOL

返回内容的容器类型、字段、长度、模板、前后缀、分隔、布尔/字符串协议或结构不符合规格。

- 纳入：返回字典而非众数字母；漏 `0b`；元组字段含义错；列表长度错误；模板替换错误。
- 排除与边界：值本身算法错误但输出结构正确（CE15）；完全缺少返回（CE04）。
- 边界说明：artifact 353 计算值正确但移除了 `0b` 前缀。
- 支持：67 个 artifact；完整列表见 `codebook.json`。
- 代表案例：artifact `3`（row 3；完整材料见 `results.json`）。

````text
return [delimeter] + [numbers[i] for i in range(len(numbers) - 1)] + [delimeter]
````

分隔符位置、元素保留和空输入结构均不符合协议。

## CE24 数值符号、精度、舍入或数值规范化 / NUMERIC_SIGN_PRECISION_OR_ROUNDING

负号语义、浮点稳定性、整数除法、数值字符串规范化或舍入规则处理错误。

- 纳入：先 `abs` 丢失带符号首位；浮点立方根精确相等；银行家舍入不符；真除法破坏整数状态；逗号小数未规范化。
- 排除与边界：一般范围/端点错误（CE13）；类型 API 本身不可用（CE08，可共现）。
- 边界说明：artifact 724 用 `abs` 抹去负号权重。
- 支持：36 个 artifact；完整列表见 `codebook.json`。
- 代表案例：artifact `46`（row 34；完整材料见 `results.json`）。

````text
return a**(1/3) % 1 == 0
````

浮点立方根精确比较不稳健且负数产生复数域问题。

## CE25 字符串大小写、边界、token 或分隔语义 / STRING_CASE_TOKEN_OR_DELIMITER_SEMANTICS

大小写覆盖、逐字符变换、词/句边界、分隔符集合、空白保真或重叠字符串语义处理错误。

- 纳入：只处理小写元音；`I` 前缀过宽；逗号未分隔；用 `str.count` 漏重叠；大小写互换只做单向。
- 排除与边界：输入字段解析的结构性误解（CE07，可共现）；输出分隔协议（CE23）。
- 边界说明：artifact 739 有字母时未逐字符 swapcase。
- 支持：55 个 artifact；完整列表见 `codebook.json`。
- 代表案例：artifact `6`（row 6；完整材料见 `results.json`）。

````text
for x in music_string.split('|')
````

错误拆分音符token，并把无效片段静默映射为默认值。

## CE26 资源、容量或守恒约束错误 / RESOURCE_CAPACITY_OR_CONSERVATION

任务包含库存、容量、供需、可用次数或守恒关系时，没有限制消耗、错误跨组共享资源或更新出非法状态。

- 纳入：库存不足仍消费 need；井之间共享桶容量余量；交换所需奇数与可供偶数未比较。
- 排除与边界：一般资格条件遗漏（CE10）；普通算术公式错误但无资源含义（CE15）。
- 边界说明：artifact 737 产生负库存。
- 支持：11 个 artifact；完整列表见 `codebook.json`。
- 代表案例：artifact `82`（row 65；完整材料见 `results.json`）。

````text
sum(lst1) == sum(lst2) and sum(lst1) % 2 == 0
````

资源供需关系被无关总和条件替代。

## CE27 方向、对称排列或端点规范化 / DIRECTION_SYMMETRY_OR_ENDPOINT_NORMALIZATION

规格对输入排列、两个端点、正反方向或对称角色不敏感，但实现只处理一个方向/排列且未规范化。

- 纳入：a>b 未交换；只把 c 当斜边；只检查一种加法排列；只接受单调递增而不接受递减。
- 排除与边界：编码/解码的逆操作错误（CE16）；排序升降方向错误（CE20）。
- 边界说明：artifact 735 漏掉 a、b 作为斜边的对称情形。
- 支持：15 个 artifact；完整列表见 `codebook.json`。
- 代表案例：artifact `139`（row 110；完整材料见 `results.json`）。

````text
range(a,b+1)
````

未规范化反向端点且候选域错误扩展到多位整数。

## CE28 优化或选择目标错误 / WRONG_OPTIMIZATION_OR_SELECTION_OBJECTIVE

候选已经存在或搜索框架可辨认，但最小/最大、最近/极值、完整词典序/局部代理等目标函数错误。

- 纳入：选最小强度而非最大；最近数对取全局极值；路径只比较末项；最大合格值取首个合格值。
- 排除与边界：候选空间本身缺失（CE14，可共现）；排序键规则（CE20）。
- 边界说明：artifact 732 将强度升序后选择最小值。
- 支持：40 个 artifact；完整列表见 `codebook.json`。
- 代表案例：artifact `9`（row 8；完整材料见 `results.json`）。

````text
numbers.sort()
````

最近数对目标被替换为全局最小值与最大值。

## CE29 处理阶段或变换遗漏 / PIPELINE_STAGE_OR_TRANSFORMATION_OMITTED

多阶段需求中，数据流总体方向可辨认，但跳过了一个核心中间变换、构造或后处理阶段。

- 纳入：直接把 N 转二进制而未先求十进制数位和；只筛选未映射；未构造规定数组即计数；已取得候选却未做最终过滤。
- 排除与边界：整个算法不存在（CE01）；单个资格谓词遗漏（CE10）；只缺返回（CE04）。
- 边界说明：artifact 726 未构造 `a[i]=i*i-i+1`。
- 支持：49 个 artifact；完整列表见 `codebook.json`。
- 代表案例：artifact `54`（row 40；完整材料见 `results.json`）。

````text
return bin(N)[2:]
````

跳过十进制数位求和，直接编码原数。

## 配套文件

- `codebook.json`：结构化定义、成员、计数和代表证据。
- `codebook.csv`：表格化 codebook。
- `assignments.json` / `assignments.csv`：逐 artifact 的代码、理由、阅读摘要、证据和限制。
- `taxonomy.json`：与 GPT6-1 一致的 HOW-style 类别树。
- `results.json`：冻结材料全文与最终类别的逐条组合。
