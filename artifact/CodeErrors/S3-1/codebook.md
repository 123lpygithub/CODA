# CodeErrors / S3-1

Schema: `coda.artifact.v1`. Artifacts: **557**; codes: **17**; artifact–code assignments: **729**.

This package uses the common seven-file format. All existing coding decisions, evidence and limitations are preserved. Additional source-specific fields are retained in `extensions`; original codebook text is retained in `codebook.json` metadata extensions and the local pre-conversion backup.

## Scope and method

Assistant-led source reading, inductive consolidation, explicit case mapping and focused execution checks

Mechanical format validation does not establish independent semantic accuracy.

## Codes

| Code | Name | Artifacts |
|---|---|---:|
| C01 | Absent substantive implementation | 67 |
| C02 | Unfinished or degenerate implementation | 39 |
| C03 | Unresolved program dependency | 45 |
| C04 | Incompatible type or API operation | 21 |
| C05 | Substituted computational objective | 67 |
| C06 | Missing required operation or constraint | 90 |
| C07 | Wrong operand or semantic scope | 57 |
| C08 | Incorrect decision predicate | 68 |
| C09 | Incomplete traversal or candidate coverage | 36 |
| C10 | Incorrect initialization or state transition | 21 |
| C11 | Invalid progress or execution strategy | 7 |
| C12 | Incorrect parsing or normalization | 41 |
| C13 | Incorrect multiplicity or aggregation unit | 24 |
| C14 | Incorrect ordering or selection priority | 40 |
| C15 | Incorrect arithmetic or numerical transformation | 37 |
| C16 | Incorrect result construction or delivery | 36 |
| C17 | Unhandled valid boundary or special input | 33 |

## C01 — Absent substantive implementation

The delivered function contains no substantive algorithm for the requested behavior, using only a stub, constant answer, identity return, or unrelated setup.

- Include: pass、仅文档/注释、固定默认答案、原样返回输入，或只有准备工作而没有主体计算。
- Exclude: 已有清晰算法但缺一个局部步骤用 C06；展开到一半的重复或截断过程用 C02。
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 67; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "609",
    "field": "incorrect_code",
    "line_start": 12,
    "quote": "    pass",
    "interpretation": "Pass-only body returns None instead of groups."
  }
]
````

## C02 — Unfinished or degenerate implementation

A started implementation ends in incomplete syntax, an unfinished computation, or repetitive expansions without a usable completion.

- Include: 半截表达式/字符串/分支，或重复展开的处理一直没有完成任务或交付结果；只描述交付代码状态，不推断截断原因。
- Exclude: 仅短小空壳用 C01；已完成计算却返回错误对象或漏 return 用 C16；独立算法错误可另行编码。
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 39; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "182",
    "field": "incorrect_code",
    "line_start": 17,
    "quote": "    groups = [group[1:] + group[0] for group in s.split(\"",
    "interpretation": "Truncated string/comprehension; cannot parse."
  }
]
````

## C03 — Unresolved program dependency

The supplied program references a required name, helper, module, or API entry that is neither defined nor imported in the available program.

- Include: 缺少导入、未实现 helper、未绑定变量；结论限定于交付的完整片段，不假设隐藏的预加载环境。
- Exclude: 名称存在但类型/方法契约用错归 C04；算法内部状态初始化错误归 C10。
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 45; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "426",
    "field": "incorrect_code",
    "line_start": 10,
    "quote": "    return number - math.floor(number)",
    "interpretation": "math.floor referenced without math import in supplied program."
  }
]
````

## C04 — Incompatible type or API operation

An operation assumes a representation or API capability unsupported by the actual operand or container type.

- Include: 字符串直接做数值运算、list 当向量化数组、dict.sort、对不适合的字符串使用 int、递归传参改变类型后仍调用原方法。
- Exclude: 模块或 helper 不存在用 C03；可执行但转换的语义不符合要求用 C12。
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 21; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "435",
    "field": "incorrect_code",
    "line_start": 10,
    "quote": "    return ''.join(map(lambda x, y: str(x ^ y), a, b))",
    "interpretation": "Applies XOR to character strings without integer conversion."
  }
]
````

## C05 — Substituted computational objective

The implementation solves a different problem or uses a proxy property that does not establish the requested relation.

- Include: 用元素数量代替零和存在性、用素数测试代替三个素数乘积、求总和最短路代替字典序路径等。
- Exclude: 目标保留但作用对象/范围错用 C07；局部可定位错误优先用相应类别，不把 C05 当兜底类。
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 67; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "184",
    "field": "incorrect_code",
    "line_start": 18,
    "quote": "    return len(set(l)) >= 3",
    "interpretation": "Distinct-value count substituted for existence of zero-sum triple."
  }
]
````

## C06 — Missing required operation or constraint

A recognizable solution omits an explicitly required transformation, filter, validity check, or alternative behavior.

- Include: 缺少数位求和、类型/奇偶过滤、回退分支、三角形合法性检查等独立要求。
- Exclude: 若缺失对应独立的表示处理 C12、输出格式 C16 或有效边界输入 C17，则优先使用具体类别，不重复标同一缺陷。
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 90; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "54",
    "field": "incorrect_code",
    "line_start": 15,
    "quote": "    return bin(N)[2:]",
    "interpretation": "Converts N directly to binary without summing decimal digits."
  }
]
````

## C07 — Wrong operand or semantic scope

The computation targets the wrong operand, level, positional unit, grouping scope, or temporal extent.

- Include: 值与索引混淆、整体与子对象混淆、局部窗口代替累计前缀、以错误字段或前后状态作比较。
- Exclude: 重复/计数单位的显式问题用 C13；其他问题整体替代目标用 C05。
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 57; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "427",
    "field": "incorrect_code",
    "line_start": 13,
    "quote": "    return any(operation < 0 for operation in operations)",
    "interpretation": "Tests individual negativity rather than prefix balance."
  }
]
````

## C08 — Incorrect decision predicate

A comparison, boolean combination, branch priority, or guard accepts or suppresses behavior under the wrong condition.

- Include: 比较方向/严格性错误、and/or 错误、自比较恒真、错误条件控制输出、凭空增加限制。
- Exclude: 条件完全不存在用 C06；错误搜索位置或遍历区间用 C09；极值/并列优先级用 C14。
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 68; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "151",
    "field": "incorrect_code",
    "line_start": 17,
    "quote": "        if rolling_max_index == len(numbers):",
    "interpretation": "Emits only when count of record maxima equals sequence length; zero seed also invalid for negative-only input."
  }
]
````

## C09 — Incomplete traversal or candidate coverage

The traversal, search space, or enumeration boundaries omit required candidates or include invalid positions.

- Include: 只检查固定若干元素、漏排列/旋转、off-by-one、过早返回导致不完整搜索、硬编码有限输入范围。
- Exclude: 边界输入绕过原本合理的主体计算用 C17；排序后选错方向用 C14。
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 36; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "141",
    "field": "incorrect_code",
    "line_start": 12,
    "quote": "    close = abs(numbers[0] - numbers[1]) < threshold",
    "interpretation": "Only fixed pairs 0/1 and 2/3 checked; short lists index out of range and other close pairs missed."
  }
]
````

## C10 — Incorrect initialization or state transition

Seeds, stored intermediate values, recursive composition, or update order fail to preserve the required computational state.

- Include: 递推基础值缺失/错误、先覆盖再移动旧状态、更新方向错、累积状态重置错、关联被破坏。
- Exclude: 不前进/不终止或违背明确执行方式用 C11；单个无状态数式错误用 C15。
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 21; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "334",
    "field": "incorrect_code",
    "line_start": 23,
    "quote": "            d = a + b + c + d",
    "interpretation": "Starts recurrence too early and overwrites d before shifting old state."
  }
]
````

## C11 — Invalid progress or execution strategy

Iteration or recursion lacks a valid completion/progress rule, or contradicts an explicit required execution strategy.

- Include: 循环旋转无耗尽判断、递归参数增长、无进展调用；题目明确禁止递归却使用递归。
- Exclude: 不因“递归”本身判错；没有实际性能证据不声称超时；基础状态数值错误另用 C10。
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 7; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "81",
    "field": "incorrect_code",
    "line_start": 40,
    "quote": "        return move_one_ball(arr)",
    "interpretation": "Repeats rotations recursively with no exhaustion detection for unsortable cycle."
  }
]
````

## C12 — Incorrect parsing or normalization

Input interpretation, token boundaries, case/sign handling, or normalization changes the meaning required by the contract.

- Include: 错误分隔符、遗漏大小写等价处理、误删符号/空白、混淆二进制文本与十进制值、未规范化区间顺序。
- Exclude: 类型操作本身不合法用 C04；只影响最终输出形态用 C16；数值运算公式用 C15。
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 41; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "163",
    "field": "incorrect_code",
    "line_start": 8,
    "quote": "    return len(set(string))",
    "interpretation": "Case normalization missing before counting distinct characters."
  }
]
````

## C13 — Incorrect multiplicity or aggregation unit

Counting or aggregation uses the wrong unit, drops required repetitions, retains forbidden repetitions, or combines groups that must remain separate.

- Include: 去重与删除所有重复项混淆、重叠计数缺失、镜像对重复计数、先合并再取整导致逐组语义丢失。
- Exclude: 普通范围遗漏用 C09；只比较错误对象而无聚合单位问题用 C07。
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 24; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "359",
    "field": "incorrect_code",
    "line_start": 9,
    "quote": "    num_buckets = math.ceil(total_water / bucket_capacity)",
    "interpretation": "Rounds after pooling all wells instead of separately per well."
  }
]
````

## C14 — Incorrect ordering or selection priority

A sort key, direction, extremum choice, stable ordering, or tie-break fails to implement the requested selection/order.

- Include: 选最短代替最长、漏次级键、主次排序反转、返回降序而要求升序、并列时选错对象。
- Exclude: 完全换成另一个任务用 C05；输出容器/标点格式用 C16。
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 40; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "547",
    "field": "incorrect_code",
    "line_start": 12,
    "quote": "    return sorted(arr, key=lambda x: bin(x).count('1'))",
    "interpretation": "Missing secondary numeric sort key for equal bit counts; task examples conflict with verbal bitcount order, reference supports verbal rule."
  }
]
````

## C15 — Incorrect arithmetic or numerical transformation

An expression uses incorrect arithmetic, precedence, scaling, direction of transformation, numeric representation, or rounding semantics.

- Include: 整数除法误用浮点除法、公式遗漏项、运算优先级、模环绕、四舍五入/银行家舍入混淆、正反变换错误。
- Exclude: 状态演化问题用 C10；目标整体变化用 C05；输入分词/大小写转换用 C12。
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 37; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "387",
    "field": "incorrect_code",
    "line_start": 33,
    "quote": "            result *= operand[i+1]",
    "interpretation": "Evaluates left-to-right, ignoring precedence and exponent associativity."
  }
]
````

## C16 — Incorrect result construction or delivery

The returned value has the wrong container, components, formatting, placement, or delivery despite identifiable output-producing work.

- Include: 返回函数对象、漏输出前后缀、标点/模板错误、间隔符位置错误、计算了结果却没有 return。
- Exclude: 空函数用 C01；退化展开未完成用 C02；输出遗漏由条件/遍历所致优先 C08/C09。
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 36; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "353",
    "field": "incorrect_code",
    "line_start": 5,
    "quote": "    return bin(avg)[2:]",
    "interpretation": "Removes required 0b prefix."
  }
]
````

## C17 — Unhandled valid boundary or special input

An otherwise identifiable algorithm fails on a documented or reference-supported empty, zero, singleton, negative, or absent-candidate case.

- Include: 空集合取极值、零输入跳过输出构造、短列表索引越界、负输入符号路径失效。
- Exclude: 范围外输入不编码；递推基础状态用 C10；普通比较等号错误用 C08。
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 33; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "520",
    "field": "incorrect_code",
    "line_start": 13,
    "quote": "    primes[0] = False",
    "interpretation": "Unconditionally initializes indices 0 and 1; n=0/1 raises IndexError."
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

# GPT6-1 — Code errors 最终编码本

本轮覆盖 **557 份生成代码、687 条来源记录、150 个任务**。共有 **17 个可分配 code**，组织在 4 个导航分组下；分组不是额外编码。已归类 557 份，未决 0 份。允许针对独立缺陷进行多重编码，因此类别覆盖数之和可以超过案例数。

这是同一助手会话中的第 1 轮完整阅读与归纳，未使用原始人工类别作为模板，也未经过人工审核。本目录保留第一轮归纳的 17 个类别，并按补充证据完成 393、729 两个原未决案例的编码；补充决策单独留痕。完整方法见 [README](../../../experiments/codebook-construction/CodeErrors/README.md)。

## 类别一览

|Code|类别|英文名称|覆盖案例数|
|---|---|---|---:|
|C01|实质实现缺失|Absent substantive implementation|67|
|C02|实现未完成或退化重复|Unfinished or degenerate implementation|39|
|C03|程序依赖未定义|Unresolved program dependency|45|
|C04|类型或 API 操作不相容|Incompatible type or API operation|21|
|C05|计算目标被替换|Substituted computational objective|67|
|C06|必要步骤或约束遗漏|Missing required operation or constraint|90|
|C07|操作对象或语义范围错误|Wrong operand or semantic scope|57|
|C08|条件判断错误|Incorrect decision predicate|68|
|C09|遍历或候选覆盖不完整|Incomplete traversal or candidate coverage|36|
|C10|初始化或状态转移错误|Incorrect initialization or state transition|21|
|C11|推进或执行策略不成立|Invalid progress or execution strategy|7|
|C12|解析或规范化错误|Incorrect parsing or normalization|41|
|C13|重数或聚合单位错误|Incorrect multiplicity or aggregation unit|24|
|C14|排序或选择优先级错误|Incorrect ordering or selection priority|40|
|C15|算术或数值变换错误|Incorrect arithmetic or numerical transformation|37|
|C16|结果构造或交付错误|Incorrect result construction or delivery|36|
|C17|有效边界或特殊输入未处理|Unhandled valid boundary or special input|33|

## 使用规则

以交付代码中的可观察失败机制为单位，不推断模型的心理原因。优先选择能准确解释证据的具体类别；一个缺陷不同时归到泛化类别与具体类别。只有存在不同证据支持的不同缺陷时才多重编码。题目约束优先，参考实现用于理解而非要求相同算法；材料冲突进入未决记录。

## C01 实质实现缺失

**Absent substantive implementation**

The delivered function contains no substantive algorithm for the requested behavior, using only a stub, constant answer, identity return, or unrelated setup.

- 纳入：pass、仅文档/注释、固定默认答案、原样返回输入，或只有准备工作而没有主体计算。
- 排除与边界：已有清晰算法但缺一个局部步骤用 C06；展开到一半的重复或截断过程用 C02。
- 支持：67 份代码。完整列表见 codebook.json 的 supporting_case_ids。
- 代表案例：[Error ID 609](../../../experiments/codebook-construction/CodeErrors/shared/cases/609.txt)，生成代码第 12 行。

```python
    pass
```

Pass-only body returns None instead of groups.

## C02 实现未完成或退化重复

**Unfinished or degenerate implementation**

A started implementation ends in incomplete syntax, an unfinished computation, or repetitive expansions without a usable completion.

- 纳入：半截表达式/字符串/分支，或重复展开的处理一直没有完成任务或交付结果；只描述交付代码状态，不推断截断原因。
- 排除与边界：仅短小空壳用 C01；已完成计算却返回错误对象或漏 return 用 C16；独立算法错误可另行编码。
- 支持：39 份代码。完整列表见 codebook.json 的 supporting_case_ids。
- 代表案例：[Error ID 182](../../../experiments/codebook-construction/CodeErrors/shared/cases/182.txt)，生成代码第 17 行。

```python
    groups = [group[1:] + group[0] for group in s.split("
```

Truncated string/comprehension; cannot parse.

## C03 程序依赖未定义

**Unresolved program dependency**

The supplied program references a required name, helper, module, or API entry that is neither defined nor imported in the available program.

- 纳入：缺少导入、未实现 helper、未绑定变量；结论限定于交付的完整片段，不假设隐藏的预加载环境。
- 排除与边界：名称存在但类型/方法契约用错归 C04；算法内部状态初始化错误归 C10。
- 支持：45 份代码。完整列表见 codebook.json 的 supporting_case_ids。
- 代表案例：[Error ID 426](../../../experiments/codebook-construction/CodeErrors/shared/cases/426.txt)，生成代码第 10 行。

```python
    return number - math.floor(number)
```

math.floor referenced without math import in supplied program.

## C04 类型或 API 操作不相容

**Incompatible type or API operation**

An operation assumes a representation or API capability unsupported by the actual operand or container type.

- 纳入：字符串直接做数值运算、list 当向量化数组、dict.sort、对不适合的字符串使用 int、递归传参改变类型后仍调用原方法。
- 排除与边界：模块或 helper 不存在用 C03；可执行但转换的语义不符合要求用 C12。
- 支持：21 份代码。完整列表见 codebook.json 的 supporting_case_ids。
- 代表案例：[Error ID 435](../../../experiments/codebook-construction/CodeErrors/shared/cases/435.txt)，生成代码第 10 行。

```python
    return ''.join(map(lambda x, y: str(x ^ y), a, b))
```

Applies XOR to character strings without integer conversion.

## C05 计算目标被替换

**Substituted computational objective**

The implementation solves a different problem or uses a proxy property that does not establish the requested relation.

- 纳入：用元素数量代替零和存在性、用素数测试代替三个素数乘积、求总和最短路代替字典序路径等。
- 排除与边界：目标保留但作用对象/范围错用 C07；局部可定位错误优先用相应类别，不把 C05 当兜底类。
- 支持：67 份代码。完整列表见 codebook.json 的 supporting_case_ids。
- 代表案例：[Error ID 184](../../../experiments/codebook-construction/CodeErrors/shared/cases/184.txt)，生成代码第 18 行。

```python
    return len(set(l)) >= 3
```

Distinct-value count substituted for existence of zero-sum triple.

## C06 必要步骤或约束遗漏

**Missing required operation or constraint**

A recognizable solution omits an explicitly required transformation, filter, validity check, or alternative behavior.

- 纳入：缺少数位求和、类型/奇偶过滤、回退分支、三角形合法性检查等独立要求。
- 排除与边界：若缺失对应独立的表示处理 C12、输出格式 C16 或有效边界输入 C17，则优先使用具体类别，不重复标同一缺陷。
- 支持：90 份代码。完整列表见 codebook.json 的 supporting_case_ids。
- 代表案例：[Error ID 54](../../../experiments/codebook-construction/CodeErrors/shared/cases/54.txt)，生成代码第 15 行。

```python
    return bin(N)[2:]
```

Converts N directly to binary without summing decimal digits.

## C07 操作对象或语义范围错误

**Wrong operand or semantic scope**

The computation targets the wrong operand, level, positional unit, grouping scope, or temporal extent.

- 纳入：值与索引混淆、整体与子对象混淆、局部窗口代替累计前缀、以错误字段或前后状态作比较。
- 排除与边界：重复/计数单位的显式问题用 C13；其他问题整体替代目标用 C05。
- 支持：57 份代码。完整列表见 codebook.json 的 supporting_case_ids。
- 代表案例：[Error ID 427](../../../experiments/codebook-construction/CodeErrors/shared/cases/427.txt)，生成代码第 13 行。

```python
    return any(operation < 0 for operation in operations)
```

Tests individual negativity rather than prefix balance.

## C08 条件判断错误

**Incorrect decision predicate**

A comparison, boolean combination, branch priority, or guard accepts or suppresses behavior under the wrong condition.

- 纳入：比较方向/严格性错误、and/or 错误、自比较恒真、错误条件控制输出、凭空增加限制。
- 排除与边界：条件完全不存在用 C06；错误搜索位置或遍历区间用 C09；极值/并列优先级用 C14。
- 支持：68 份代码。完整列表见 codebook.json 的 supporting_case_ids。
- 代表案例：[Error ID 151](../../../experiments/codebook-construction/CodeErrors/shared/cases/151.txt)，生成代码第 17 行。

```python
        if rolling_max_index == len(numbers):
```

Emits only when count of record maxima equals sequence length; zero seed also invalid for negative-only input.

## C09 遍历或候选覆盖不完整

**Incomplete traversal or candidate coverage**

The traversal, search space, or enumeration boundaries omit required candidates or include invalid positions.

- 纳入：只检查固定若干元素、漏排列/旋转、off-by-one、过早返回导致不完整搜索、硬编码有限输入范围。
- 排除与边界：边界输入绕过原本合理的主体计算用 C17；排序后选错方向用 C14。
- 支持：36 份代码。完整列表见 codebook.json 的 supporting_case_ids。
- 代表案例：[Error ID 141](../../../experiments/codebook-construction/CodeErrors/shared/cases/141.txt)，生成代码第 12 行。

```python
    close = abs(numbers[0] - numbers[1]) < threshold
```

Only fixed pairs 0/1 and 2/3 checked; short lists index out of range and other close pairs missed.

## C10 初始化或状态转移错误

**Incorrect initialization or state transition**

Seeds, stored intermediate values, recursive composition, or update order fail to preserve the required computational state.

- 纳入：递推基础值缺失/错误、先覆盖再移动旧状态、更新方向错、累积状态重置错、关联被破坏。
- 排除与边界：不前进/不终止或违背明确执行方式用 C11；单个无状态数式错误用 C15。
- 支持：21 份代码。完整列表见 codebook.json 的 supporting_case_ids。
- 代表案例：[Error ID 334](../../../experiments/codebook-construction/CodeErrors/shared/cases/334.txt)，生成代码第 23 行。

```python
            d = a + b + c + d
```

Starts recurrence too early and overwrites d before shifting old state.

## C11 推进或执行策略不成立

**Invalid progress or execution strategy**

Iteration or recursion lacks a valid completion/progress rule, or contradicts an explicit required execution strategy.

- 纳入：循环旋转无耗尽判断、递归参数增长、无进展调用；题目明确禁止递归却使用递归。
- 排除与边界：不因“递归”本身判错；没有实际性能证据不声称超时；基础状态数值错误另用 C10。
- 支持：7 份代码。完整列表见 codebook.json 的 supporting_case_ids。
- 代表案例：[Error ID 81](../../../experiments/codebook-construction/CodeErrors/shared/cases/81.txt)，生成代码第 40 行。

```python
        return move_one_ball(arr)
```

Repeats rotations recursively with no exhaustion detection for unsortable cycle.

## C12 解析或规范化错误

**Incorrect parsing or normalization**

Input interpretation, token boundaries, case/sign handling, or normalization changes the meaning required by the contract.

- 纳入：错误分隔符、遗漏大小写等价处理、误删符号/空白、混淆二进制文本与十进制值、未规范化区间顺序。
- 排除与边界：类型操作本身不合法用 C04；只影响最终输出形态用 C16；数值运算公式用 C15。
- 支持：41 份代码。完整列表见 codebook.json 的 supporting_case_ids。
- 代表案例：[Error ID 163](../../../experiments/codebook-construction/CodeErrors/shared/cases/163.txt)，生成代码第 8 行。

```python
    return len(set(string))
```

Case normalization missing before counting distinct characters.

## C13 重数或聚合单位错误

**Incorrect multiplicity or aggregation unit**

Counting or aggregation uses the wrong unit, drops required repetitions, retains forbidden repetitions, or combines groups that must remain separate.

- 纳入：去重与删除所有重复项混淆、重叠计数缺失、镜像对重复计数、先合并再取整导致逐组语义丢失。
- 排除与边界：普通范围遗漏用 C09；只比较错误对象而无聚合单位问题用 C07。
- 支持：24 份代码。完整列表见 codebook.json 的 supporting_case_ids。
- 代表案例：[Error ID 359](../../../experiments/codebook-construction/CodeErrors/shared/cases/359.txt)，生成代码第 9 行。

```python
    num_buckets = math.ceil(total_water / bucket_capacity)
```

Rounds after pooling all wells instead of separately per well.

## C14 排序或选择优先级错误

**Incorrect ordering or selection priority**

A sort key, direction, extremum choice, stable ordering, or tie-break fails to implement the requested selection/order.

- 纳入：选最短代替最长、漏次级键、主次排序反转、返回降序而要求升序、并列时选错对象。
- 排除与边界：完全换成另一个任务用 C05；输出容器/标点格式用 C16。
- 支持：40 份代码。完整列表见 codebook.json 的 supporting_case_ids。
- 代表案例：[Error ID 547](../../../experiments/codebook-construction/CodeErrors/shared/cases/547.txt)，生成代码第 12 行。

```python
    return sorted(arr, key=lambda x: bin(x).count('1'))
```

Missing secondary numeric sort key for equal bit counts; task examples conflict with verbal bitcount order, reference supports verbal rule.

## C15 算术或数值变换错误

**Incorrect arithmetic or numerical transformation**

An expression uses incorrect arithmetic, precedence, scaling, direction of transformation, numeric representation, or rounding semantics.

- 纳入：整数除法误用浮点除法、公式遗漏项、运算优先级、模环绕、四舍五入/银行家舍入混淆、正反变换错误。
- 排除与边界：状态演化问题用 C10；目标整体变化用 C05；输入分词/大小写转换用 C12。
- 支持：37 份代码。完整列表见 codebook.json 的 supporting_case_ids。
- 代表案例：[Error ID 387](../../../experiments/codebook-construction/CodeErrors/shared/cases/387.txt)，生成代码第 33 行。

```python
            result *= operand[i+1]
```

Evaluates left-to-right, ignoring precedence and exponent associativity.

## C16 结果构造或交付错误

**Incorrect result construction or delivery**

The returned value has the wrong container, components, formatting, placement, or delivery despite identifiable output-producing work.

- 纳入：返回函数对象、漏输出前后缀、标点/模板错误、间隔符位置错误、计算了结果却没有 return。
- 排除与边界：空函数用 C01；退化展开未完成用 C02；输出遗漏由条件/遍历所致优先 C08/C09。
- 支持：36 份代码。完整列表见 codebook.json 的 supporting_case_ids。
- 代表案例：[Error ID 353](../../../experiments/codebook-construction/CodeErrors/shared/cases/353.txt)，生成代码第 5 行。

```python
    return bin(avg)[2:]
```

Removes required 0b prefix.

## C17 有效边界或特殊输入未处理

**Unhandled valid boundary or special input**

An otherwise identifiable algorithm fails on a documented or reference-supported empty, zero, singleton, negative, or absent-candidate case.

- 纳入：空集合取极值、零输入跳过输出构造、短列表索引越界、负输入符号路径失效。
- 排除与边界：范围外输入不编码；递推基础状态用 C10；普通比较等号错误用 C08。
- 支持：33 份代码。完整列表见 codebook.json 的 supporting_case_ids。
- 代表案例：[Error ID 520](../../../experiments/codebook-construction/CodeErrors/shared/cases/520.txt)，生成代码第 13 行。

```python
    primes[0] = False
```

Unconditionally initializes indices 0 and 1; n=0/1 raises IndexError.

## 未决记录

全部 557 个 artifact 均已编码，无未决案例。393 和 729 的补充判断见 [材料核查说明](../../../experiments/codebook-construction/CodeErrors/DATA_NOTES.md)。

## 随附文件

`taxonomy.json` 是 HOW 风格分类树；`results.json` 是其 metadata/results 风格结果包；`codebook.json` 保存完整定义和边界；`assignments.json`/`.csv` 保存逐例编码；[metadata.json](../../../experiments/codebook-construction/CodeErrors/GPT6-1/metadata.json) 记录本轮范围与方法。所有执行见证集中保存在 `../../../experiments/codebook-construction/CodeErrors/shared/witness_results.json`。
