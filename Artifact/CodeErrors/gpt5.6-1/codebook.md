# CodeErrors / gpt5.6-1

Schema: `coda.artifact.v1`. Artifacts: **557**; codes: **14**; artifact–code assignments: **946**.

This package uses the common seven-file format. All existing coding decisions, evidence and limitations are preserved. Additional source-specific fields are retained in `extensions`; original codebook text is retained in `codebook.json` metadata extensions and the local pre-conversion backup.

## Scope and method

逐条完整阅读、开放编码、持续比较、逐条人工 assignment、code-to-artifact 反向复核；程序仅转换格式和验证。

单一 AI 编码；机械一致性检查不构成人工复核。Privacy 的 metadata-only 材料只按可用标题和元数据作最小判断。

## Codes

| Code | Name | Artifacts |
|---|---|---:|
| CE01 | 实质实现未交付 | 81 |
| CE02 | 源码截断或语法不完整 | 26 |
| CE03 | 未提供的依赖或名称 | 48 |
| CE04 | 解析、分词或表示转换错误 | 58 |
| CE05 | 计算目标被替换 | 187 |
| CE06 | 状态、递归或迭代推进错误 | 50 |
| CE07 | 搜索空间或候选覆盖不足 | 79 |
| CE08 | 输出组装、位置、顺序或重数错误 | 77 |
| CE09 | 控制流条件或提前返回错误 | 28 |
| CE10 | 数学公式、递推或数值方法错误 | 86 |
| CE11 | 输出格式或表示契约错误 | 37 |
| CE12 | 条件、类型或输入域验证不完整 | 150 |
| CE13 | 大小写或字符规范语义错误 | 22 |
| CE14 | 运行时对象协议或操作类型不相容 | 17 |

## CE01 — 实质实现未交付

目标函数没有完成足以形成契约结果的可执行实现。

- Include: `pass`；只有文档字符串或注释；固定占位常量；实现片段结束后没有任何结果返回；只硬编码少量示例、一般输入仍未交付。
- Exclude: 源码因未闭合 token 无法解析用 CE02；已有完整可执行算法但计算错误用相应机制类别；仅缺 import 或 helper 用 CE03。
- Boundary/examples: row 30（artifact 42）是纯 `pass`；row 344（artifact 459）只硬编码前五个示例且一般输入返回空值，也属于未交付一般实现。
- Supporting artifacts: 81; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "42",
    "row": 30,
    "field": "incorrect_code",
    "quote": "    # TODO: Write your code here\n    pass",
    "interpretation": "函数体为 pass，核心实现未交付。"
  }
]
````

## CE02 — 源码截断或语法不完整

冻结源码在 token、字符串、表达式、容器、条件或缩进块中间结束，使模块无法解析或函数文本明显未闭合。

- Include: 未闭合字符串/列表/调用/推导式；裸 `if`；条件后缺少缩进块；赋值号后中断。
- Exclude: 以合法表达式结束但没有 `return` 用 CE01；合法语法中的未定义名称用 CE03。
- Boundary/examples: row 140（artifact 182）在字符串和推导式中途结束；row 406（artifact 546）的末行 `max_` 是合法名称表达式，因此不使用 CE02。
- Supporting artifacts: 26; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "182",
    "row": 140,
    "field": "incorrect_code",
    "quote": "    groups = [group[1:] + group[0] for group in s.split(\"",
    "interpretation": "解码源码在字符串和推导式中途截断。"
  }
]
````

## CE03 — 未提供的依赖或名称

正常路径引用当前 artifact 未定义、未导入、任务也未承诺提供的模块、函数、变量或 helper。

- Include: 缺少 `re`、`math`、`hashlib`、`reduce`；拼错函数名；未定义的 helper、数组或局部名称。
- Exclude: 对象存在但其类型不支持所调用操作用 CE14；输入表示转换错误用 CE04；源码 token 未闭合用 CE02。
- Boundary/examples: row 109（artifact 138）缺少 `hashlib`；row 325（artifact 435）中的字符串对象存在但不支持异或，归 CE14 而非 CE03。
- Supporting artifacts: 48; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "138",
    "row": 109,
    "field": "incorrect_code",
    "quote": "    return hashlib.md5(text.encode('utf-8')).hexdigest()",
    "interpretation": "缺少 hashlib 依赖。"
  }
]
````

## CE04 — 解析、分词或表示转换错误

输入被按错误边界、错误 token 位置或错误表示域解释，或文本、字符、数字和结构表示之间的转换不成立。

- Include: 分隔符错误；把标签词转整数；英文数字词直接 `int()`；负号当数字；十六进制按十进制解析；把整串、整行或端点集合误作另一表示。
- Exclude: 表示已正确解析但公式错误用 CE10；缺失名称用 CE03；对象类型不支持操作用 CE14；纯输出前缀/布局用 CE11。
- Boundary/examples: row 25（artifact 36）读取了错误 token；row 325（artifact 435）同时需要 CE04（未转整数）和 CE14（字符串不支持异或）。
- Supporting artifacts: 58; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "36",
    "row": 25,
    "field": "incorrect_code",
    "quote": "    return n - int(s.split()[0]) - int(s.split()[1])",
    "interpretation": "读取标签 token 并尝试转整数，漏读正确位置。"
  }
]
````

## CE05 — 计算目标被替换

实现计算了一个可辨识但与任务契约不同的量、对象、谓词、粒度或优化目标。

- Include: 累计余额换成单项正负；最近点对换成全局极值；字符集合换成字符串长度；最大素数换成列表最大值；词内排序换成词间排序；逐字符计数换成整数级计数。
- Exclude: 目标仍正确但候选只检查一部分用 CE07；目标量正确但公式错误用 CE10；仅输出位置或重数错误用 CE08。
- Boundary/examples: row 8（artifact 9）同时使用 CE05（目标变成极值）和 CE07（未比较候选差值）；row 334（artifact 446）目标仍是归一化，只是公式漏减最小值，因此只用 CE10。
- Supporting artifacts: 187; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "9",
    "row": 8,
    "field": "incorrect_code",
    "quote": "    numbers.sort()\n    return (numbers[0], numbers[-1])",
    "interpretation": "选择目标变成全局极值，且未比较完整候选差值。"
  }
]
````

## CE06 — 状态、递归或迭代推进错误

算法需要跨步骤保存或推进状态，但实现丢失状态、混淆状态角色、沿错误方向更新、无终止条件或非同步覆盖旧状态。

- Include: 递归不传余额；递归参数向上发散；解码继续沿编码方向；容量跨井不重置；递推窗口更新顺序错误；状态不前进造成无限循环。
- Exclude: 循环根本不进入或 `return` 位置错误用 CE09；递推关系数值本身错误可同时用 CE10；只是候选范围不足用 CE07。
- Boundary/examples: row 64（artifact 81）循环一整圈后没有失败终止状态；row 259（artifact 334）既有状态窗口更新错误 CE06，也有递推基础/公式错误 CE10。
- Supporting artifacts: 50; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "81",
    "row": 64,
    "field": "incorrect_code",
    "quote": "        arr.append(arr.pop(0))\n        return move_one_ball(arr)",
    "interpretation": "失败候选循环一圈后仍无终止状态，导致无限递归。"
  }
]
````

## CE07 — 搜索空间或候选覆盖不足

任务要求枚举、比较或搜索多个候选，实施只检查固定位置、首个候选、端点、连续窗口、有限硬编码或不完整候选集合。

- Include: 只看首个合格项；只检查端点；只硬编码少数输入；非重叠计数跳过重叠起点；未枚举全部旋转、元素对、组合或因子重数。
- Exclude: 候选覆盖完整但优化指标/谓词换了用 CE05；公式错误用 CE10；循环控制使搜索完全跳过可同时用 CE09。
- Boundary/examples: row 331（artifact 443）使用非重叠接口而漏起点；row 299（artifact 400）仅是平局分支错误，不属于候选覆盖，归 CE09。
- Supporting artifacts: 79; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "443",
    "row": 331,
    "field": "incorrect_code",
    "quote": "    return string.count(substring)",
    "interpretation": "非重叠计数接口跳过重叠起点候选。"
  }
]
````

## CE08 — 输出组装、位置、顺序或重数错误

实现得到或接近得到所需元素/值，但重建结果时破坏了位置、主次排序键、交替结构、长度、重复次数或原序。

- Include: 集合去重破坏重数和顺序；分组拼接代替原位交织；返回前驱索引；遗漏/增加前缀项；选中最大项后以错误方向排列；重复计同一镜像对。
- Exclude: 最终外部文本格式或类型错误用 CE11；元素本身选择目标错误用 CE05；候选未搜索完整用 CE07。
- Boundary/examples: row 264（artifact 346）两次全局排序颠倒主次键；row 270（artifact 353）只丢失二进制前缀，归 CE11 而非 CE08。
- Supporting artifacts: 77; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "346",
    "row": 264,
    "field": "incorrect_code",
    "quote": "    result.sort(key=lambda x: x[0])\n    result.sort(key=lambda x: x[1], reverse=True)",
    "interpretation": "两次全局排序颠倒主次键并打散行分组。"
  }
]
````

## CE09 — 控制流条件或提前返回错误

分支条件、循环初始化/继续条件、分支优先级或 `return` 位置使必要路径被跳过、反转或过早终止。

- Include: 循环首次不进入；首项即返回；有效输入分支反向；重叠条件优先级错误；边界值落入错误分支；应有特殊分支但无条件走同一路径。
- Exclude: 谓词本身遗漏复合条件用 CE12；数学比较/公式错误用 CE10；跨步骤状态不推进用 CE06。
- Boundary/examples: row 9（artifact 11）初始化使搜索完全跳过；row 372（artifact 498）严格阈值被写成含等号，边界值走错分支。
- Supporting artifacts: 28; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "11",
    "row": 9,
    "field": "incorrect_code",
    "quote": "    divisor = 1\n    while n % divisor != 0:\n        divisor += 1\n    return divisor",
    "interpretation": "循环初始化使搜索不执行，并返回最小而非最大真因数。"
  }
]
````

## CE10 — 数学公式、递推或数值方法错误

计算目标仍可辨认，但采用的代数式、计数式、递推关系、舍入规则、数值方法或运算顺序不成立。

- Include: 错误容斥；错误递推；公式漏平方根；运算符优先级错误；银行家舍入替代远离零；归一化漏平移；二分法丢端点根；带符号数字和公式错误。
- Exclude: 计算的是完全不同目标用 CE05；只漏某类输入/条件用 CE12；状态传递错误可同时用 CE06。
- Boundary/examples: row 362（artifact 485）海伦公式漏平方根；row 390（artifact 523）使用错误的中点舍入规则。
- Supporting artifacts: 86; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "485",
    "row": 362,
    "field": "incorrect_code",
    "quote": "        return round(s * (s - a) * (s - b) * (s - c), 2)",
    "interpretation": "海伦公式遗漏平方根。"
  }
]
````

## CE11 — 输出格式或表示契约错误

语义值接近、部分可得或另有机制已描述内容错误，但外部输出的类型、前缀、分隔、文本模板、空白布局或表示形式不符合契约。

- Include: 删除 `0b` 前缀；英文词输出成数字字符；模板替换位置错误；返回函数对象、标量或嵌套列表而非指定形状；折叠必须保留的空白。
- Exclude: 序列内部位置/顺序/重数用 CE08；输入解析用 CE04；只因没有任何实现而隐式 `None` 用 CE01。
- Boundary/examples: row 270（artifact 353）只错误删除 `0b`；row 277（artifact 361）内容已选对但顺序错误，归 CE08。
- Supporting artifacts: 37; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "353",
    "row": 270,
    "field": "incorrect_code",
    "quote": "    return bin(avg)[2:]",
    "interpretation": "错误删除要求保留的二进制前缀。"
  }
]
````

## CE12 — 条件、类型或输入域验证不完整

遗漏、反向或无依据增加任务明确规定的类型、范围、复合谓词、边界、有效性或特殊输入条件。

- Include: 遗漏三角形不等式；不验整数类型；漏复合筛选项；把 1 当素数；空输入越界；错误增加年份/长度限制；把允许重复两次收窄为禁止重复。
- Exclude: 核心目标被替换用 CE05；核心数学关系错误用 CE10；控制路径位置/优先级错误用 CE09；专门的大小写规则用 CE13。
- Boundary/examples: row 47（artifact 63）只遗漏整数类型约束；row 248（artifact 318）核心勾股公式被替换，归 CE10，不把它泛化成验证遗漏。
- Supporting artifacts: 150; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "63",
    "row": 47,
    "field": "incorrect_code",
    "quote": "    if x == y + z or y == x + z or z == x + y:\n        return True",
    "interpretation": "遗漏所有参数必须为整数的复合条件。"
  }
]
````

## CE13 — 大小写或字符规范语义错误

错误忽略、统一、交换或遗漏大小写，使任务明确区分或合并的字符集合与字符变换语义被改变。

- Include: 只列小写元音；统一转大写后抹除原大写条件；双向 swapcase 写成单向转换；大小写不敏感计数未归一化；元音变换前未先交换大小写。
- Exclude: 英文数词等语义映射用 CE04；一般输出文本格式用 CE11；字符内容的非大小写复合条件用 CE12。
- Boundary/examples: row 53（artifact 69）统一转大写抹除原字符状态；row 125（artifact 163）遗漏大小写不敏感归一化。
- Supporting artifacts: 22; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "69",
    "row": 53,
    "field": "incorrect_code",
    "quote": "        if i % 2 == 0 and s[i].upper() in 'AEIOU':",
    "interpretation": "统一转大写抹除了原字符必须为大写的语义。"
  }
]
````

## CE14 — 运行时对象协议或操作类型不相容

所需对象或值已经存在，但实现把它当成另一种对象协议，调用该类型不支持的方法、运算、索引或调用约定，导致正常路径上的 `TypeError`、`AttributeError` 等。

- Include: 对字典调用列表 `.sort()`；在标量上调用集合均值方法；把整数当可切片序列；对字符串字符做按位异或/取模；把 Python 列表当数组布尔掩码；用索引列表直接索引 Python 列表。
- Exclude: 名称或 import 根本不存在用 CE03；文本/数值表示转换缺失用 CE04；只是没有验证输入类型用 CE12。
- Boundary/examples: row 249（artifact 319）对字典调用不存在的 `.sort()`；row 348（artifact 464）既把目标换成十进制原样返回 CE05，也在备用分支把整数传给字符串解析接口 CE14。
- Supporting artifacts: 17; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "319",
    "row": 249,
    "field": "incorrect_code",
    "quote": "    words = set(words)\n    word_count = {}\n    for word in words:\n        word_count[word] = word_count.get(word, 0) + 1\n    word_count.sort(key=word_count.get, reverse=True)\n    return word_count[0]",
    "interpretation": "把词内字符数换成词频，未比较候选且对字典调用不支持的方法。"
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

# gpt5.6-1 — CodeErrors 最终编码本

本轮覆盖 **557 个 artifact**，形成 **14 个可分配 code**，共记录 **946 个 artifact–code assignment**。全部 557 个 artifact 均已编码，未决 0 个。允许在存在彼此独立证据时进行多重编码，因此类别覆盖数之和可以超过 artifact 数。

本 codebook 来自逐条完整阅读、开放编码、持续比较和反向成员复核；不继承旧 assignment 或 codebook。关键词、正则、聚类和脚本没有用于决定类别，脚本只将已经人工确认的决定转换为 GPT6-1 的发布表现形式并检查一致性。

## 类别一览

|Code|类别|覆盖 artifact 数|
|---|---|---:|
|CE01|实质实现未交付|81|
|CE02|源码截断或语法不完整|26|
|CE03|未提供的依赖或名称|48|
|CE04|解析、分词或表示转换错误|58|
|CE05|计算目标被替换|187|
|CE06|状态、递归或迭代推进错误|50|
|CE07|搜索空间或候选覆盖不足|79|
|CE08|输出组装、位置、顺序或重数错误|77|
|CE09|控制流条件或提前返回错误|28|
|CE10|数学公式、递推或数值方法错误|86|
|CE11|输出格式或表示契约错误|37|
|CE12|条件、类型或输入域验证不完整|150|
|CE13|大小写或字符规范语义错误|22|
|CE14|运行时对象协议或操作类型不相容|17|

## 使用规则

- 按失败机制编码，不按题目领域、函数名或最终错误结果命名。
- “答案不正确”“会报错”不能单独成为代码；必须回到造成该结果的具体机制。
- 同一现象不重复贴近义标签；只有不同机制并存时才多标签。
- 性能问题、输入突变或异常类型只有在任务契约明确相关时才编码。
- `closed`、测试结果或题目领域不参与本数据集分类；判断只基于冻结任务说明与错误实现。

## CE01 实质实现未交付

目标函数没有完成足以形成契约结果的可执行实现。

- 纳入：`pass`；只有文档字符串或注释；固定占位常量；实现片段结束后没有任何结果返回；只硬编码少量示例、一般输入仍未交付。
- 排除与边界：源码因未闭合 token 无法解析用 CE02；已有完整可执行算法但计算错误用相应机制类别；仅缺 import 或 helper 用 CE03。
- 支持：81 个 artifact。完整列表见 `codebook.json` 的 `supporting_cases`。
- 边界案例：row 30（artifact 42）是纯 `pass`；row 344（artifact 459）只硬编码前五个示例且一般输入返回空值，也属于未交付一般实现。
- 代表案例：artifact `42`（row 30；完整材料见 `results.json`）。

````text
    # TODO: Write your code here
    pass
````

函数体为 pass，核心实现未交付。

## CE02 源码截断或语法不完整

冻结源码在 token、字符串、表达式、容器、条件或缩进块中间结束，使模块无法解析或函数文本明显未闭合。

- 纳入：未闭合字符串/列表/调用/推导式；裸 `if`；条件后缺少缩进块；赋值号后中断。
- 排除与边界：以合法表达式结束但没有 `return` 用 CE01；合法语法中的未定义名称用 CE03。
- 支持：26 个 artifact。完整列表见 `codebook.json` 的 `supporting_cases`。
- 边界案例：row 140（artifact 182）在字符串和推导式中途结束；row 406（artifact 546）的末行 `max_` 是合法名称表达式，因此不使用 CE02。
- 代表案例：artifact `182`（row 140；完整材料见 `results.json`）。

````text
    groups = [group[1:] + group[0] for group in s.split("
````

解码源码在字符串和推导式中途截断。

## CE03 未提供的依赖或名称

正常路径引用当前 artifact 未定义、未导入、任务也未承诺提供的模块、函数、变量或 helper。

- 纳入：缺少 `re`、`math`、`hashlib`、`reduce`；拼错函数名；未定义的 helper、数组或局部名称。
- 排除与边界：对象存在但其类型不支持所调用操作用 CE14；输入表示转换错误用 CE04；源码 token 未闭合用 CE02。
- 支持：48 个 artifact。完整列表见 `codebook.json` 的 `supporting_cases`。
- 边界案例：row 109（artifact 138）缺少 `hashlib`；row 325（artifact 435）中的字符串对象存在但不支持异或，归 CE14 而非 CE03。
- 代表案例：artifact `138`（row 109；完整材料见 `results.json`）。

````text
    return hashlib.md5(text.encode('utf-8')).hexdigest()
````

缺少 hashlib 依赖。

## CE04 解析、分词或表示转换错误

输入被按错误边界、错误 token 位置或错误表示域解释，或文本、字符、数字和结构表示之间的转换不成立。

- 纳入：分隔符错误；把标签词转整数；英文数字词直接 `int()`；负号当数字；十六进制按十进制解析；把整串、整行或端点集合误作另一表示。
- 排除与边界：表示已正确解析但公式错误用 CE10；缺失名称用 CE03；对象类型不支持操作用 CE14；纯输出前缀/布局用 CE11。
- 支持：58 个 artifact。完整列表见 `codebook.json` 的 `supporting_cases`。
- 边界案例：row 25（artifact 36）读取了错误 token；row 325（artifact 435）同时需要 CE04（未转整数）和 CE14（字符串不支持异或）。
- 代表案例：artifact `36`（row 25；完整材料见 `results.json`）。

````text
    return n - int(s.split()[0]) - int(s.split()[1])
````

读取标签 token 并尝试转整数，漏读正确位置。

## CE05 计算目标被替换

实现计算了一个可辨识但与任务契约不同的量、对象、谓词、粒度或优化目标。

- 纳入：累计余额换成单项正负；最近点对换成全局极值；字符集合换成字符串长度；最大素数换成列表最大值；词内排序换成词间排序；逐字符计数换成整数级计数。
- 排除与边界：目标仍正确但候选只检查一部分用 CE07；目标量正确但公式错误用 CE10；仅输出位置或重数错误用 CE08。
- 支持：187 个 artifact。完整列表见 `codebook.json` 的 `supporting_cases`。
- 边界案例：row 8（artifact 9）同时使用 CE05（目标变成极值）和 CE07（未比较候选差值）；row 334（artifact 446）目标仍是归一化，只是公式漏减最小值，因此只用 CE10。
- 代表案例：artifact `9`（row 8；完整材料见 `results.json`）。

````text
    numbers.sort()
    return (numbers[0], numbers[-1])
````

选择目标变成全局极值，且未比较完整候选差值。

## CE06 状态、递归或迭代推进错误

算法需要跨步骤保存或推进状态，但实现丢失状态、混淆状态角色、沿错误方向更新、无终止条件或非同步覆盖旧状态。

- 纳入：递归不传余额；递归参数向上发散；解码继续沿编码方向；容量跨井不重置；递推窗口更新顺序错误；状态不前进造成无限循环。
- 排除与边界：循环根本不进入或 `return` 位置错误用 CE09；递推关系数值本身错误可同时用 CE10；只是候选范围不足用 CE07。
- 支持：50 个 artifact。完整列表见 `codebook.json` 的 `supporting_cases`。
- 边界案例：row 64（artifact 81）循环一整圈后没有失败终止状态；row 259（artifact 334）既有状态窗口更新错误 CE06，也有递推基础/公式错误 CE10。
- 代表案例：artifact `81`（row 64；完整材料见 `results.json`）。

````text
        arr.append(arr.pop(0))
        return move_one_ball(arr)
````

失败候选循环一圈后仍无终止状态，导致无限递归。

## CE07 搜索空间或候选覆盖不足

任务要求枚举、比较或搜索多个候选，实施只检查固定位置、首个候选、端点、连续窗口、有限硬编码或不完整候选集合。

- 纳入：只看首个合格项；只检查端点；只硬编码少数输入；非重叠计数跳过重叠起点；未枚举全部旋转、元素对、组合或因子重数。
- 排除与边界：候选覆盖完整但优化指标/谓词换了用 CE05；公式错误用 CE10；循环控制使搜索完全跳过可同时用 CE09。
- 支持：79 个 artifact。完整列表见 `codebook.json` 的 `supporting_cases`。
- 边界案例：row 331（artifact 443）使用非重叠接口而漏起点；row 299（artifact 400）仅是平局分支错误，不属于候选覆盖，归 CE09。
- 代表案例：artifact `443`（row 331；完整材料见 `results.json`）。

````text
    return string.count(substring)
````

非重叠计数接口跳过重叠起点候选。

## CE08 输出组装、位置、顺序或重数错误

实现得到或接近得到所需元素/值，但重建结果时破坏了位置、主次排序键、交替结构、长度、重复次数或原序。

- 纳入：集合去重破坏重数和顺序；分组拼接代替原位交织；返回前驱索引；遗漏/增加前缀项；选中最大项后以错误方向排列；重复计同一镜像对。
- 排除与边界：最终外部文本格式或类型错误用 CE11；元素本身选择目标错误用 CE05；候选未搜索完整用 CE07。
- 支持：77 个 artifact。完整列表见 `codebook.json` 的 `supporting_cases`。
- 边界案例：row 264（artifact 346）两次全局排序颠倒主次键；row 270（artifact 353）只丢失二进制前缀，归 CE11 而非 CE08。
- 代表案例：artifact `346`（row 264；完整材料见 `results.json`）。

````text
    result.sort(key=lambda x: x[0])
    result.sort(key=lambda x: x[1], reverse=True)
````

两次全局排序颠倒主次键并打散行分组。

## CE09 控制流条件或提前返回错误

分支条件、循环初始化/继续条件、分支优先级或 `return` 位置使必要路径被跳过、反转或过早终止。

- 纳入：循环首次不进入；首项即返回；有效输入分支反向；重叠条件优先级错误；边界值落入错误分支；应有特殊分支但无条件走同一路径。
- 排除与边界：谓词本身遗漏复合条件用 CE12；数学比较/公式错误用 CE10；跨步骤状态不推进用 CE06。
- 支持：28 个 artifact。完整列表见 `codebook.json` 的 `supporting_cases`。
- 边界案例：row 9（artifact 11）初始化使搜索完全跳过；row 372（artifact 498）严格阈值被写成含等号，边界值走错分支。
- 代表案例：artifact `11`（row 9；完整材料见 `results.json`）。

````text
    divisor = 1
    while n % divisor != 0:
        divisor += 1
    return divisor
````

循环初始化使搜索不执行，并返回最小而非最大真因数。

## CE10 数学公式、递推或数值方法错误

计算目标仍可辨认，但采用的代数式、计数式、递推关系、舍入规则、数值方法或运算顺序不成立。

- 纳入：错误容斥；错误递推；公式漏平方根；运算符优先级错误；银行家舍入替代远离零；归一化漏平移；二分法丢端点根；带符号数字和公式错误。
- 排除与边界：计算的是完全不同目标用 CE05；只漏某类输入/条件用 CE12；状态传递错误可同时用 CE06。
- 支持：86 个 artifact。完整列表见 `codebook.json` 的 `supporting_cases`。
- 边界案例：row 362（artifact 485）海伦公式漏平方根；row 390（artifact 523）使用错误的中点舍入规则。
- 代表案例：artifact `485`（row 362；完整材料见 `results.json`）。

````text
        return round(s * (s - a) * (s - b) * (s - c), 2)
````

海伦公式遗漏平方根。

## CE11 输出格式或表示契约错误

语义值接近、部分可得或另有机制已描述内容错误，但外部输出的类型、前缀、分隔、文本模板、空白布局或表示形式不符合契约。

- 纳入：删除 `0b` 前缀；英文词输出成数字字符；模板替换位置错误；返回函数对象、标量或嵌套列表而非指定形状；折叠必须保留的空白。
- 排除与边界：序列内部位置/顺序/重数用 CE08；输入解析用 CE04；只因没有任何实现而隐式 `None` 用 CE01。
- 支持：37 个 artifact。完整列表见 `codebook.json` 的 `supporting_cases`。
- 边界案例：row 270（artifact 353）只错误删除 `0b`；row 277（artifact 361）内容已选对但顺序错误，归 CE08。
- 代表案例：artifact `353`（row 270；完整材料见 `results.json`）。

````text
    return bin(avg)[2:]
````

错误删除要求保留的二进制前缀。

## CE12 条件、类型或输入域验证不完整

遗漏、反向或无依据增加任务明确规定的类型、范围、复合谓词、边界、有效性或特殊输入条件。

- 纳入：遗漏三角形不等式；不验整数类型；漏复合筛选项；把 1 当素数；空输入越界；错误增加年份/长度限制；把允许重复两次收窄为禁止重复。
- 排除与边界：核心目标被替换用 CE05；核心数学关系错误用 CE10；控制路径位置/优先级错误用 CE09；专门的大小写规则用 CE13。
- 支持：150 个 artifact。完整列表见 `codebook.json` 的 `supporting_cases`。
- 边界案例：row 47（artifact 63）只遗漏整数类型约束；row 248（artifact 318）核心勾股公式被替换，归 CE10，不把它泛化成验证遗漏。
- 代表案例：artifact `63`（row 47；完整材料见 `results.json`）。

````text
    if x == y + z or y == x + z or z == x + y:
        return True
````

遗漏所有参数必须为整数的复合条件。

## CE13 大小写或字符规范语义错误

错误忽略、统一、交换或遗漏大小写，使任务明确区分或合并的字符集合与字符变换语义被改变。

- 纳入：只列小写元音；统一转大写后抹除原大写条件；双向 swapcase 写成单向转换；大小写不敏感计数未归一化；元音变换前未先交换大小写。
- 排除与边界：英文数词等语义映射用 CE04；一般输出文本格式用 CE11；字符内容的非大小写复合条件用 CE12。
- 支持：22 个 artifact。完整列表见 `codebook.json` 的 `supporting_cases`。
- 边界案例：row 53（artifact 69）统一转大写抹除原字符状态；row 125（artifact 163）遗漏大小写不敏感归一化。
- 代表案例：artifact `69`（row 53；完整材料见 `results.json`）。

````text
        if i % 2 == 0 and s[i].upper() in 'AEIOU':
````

统一转大写抹除了原字符必须为大写的语义。

## CE14 运行时对象协议或操作类型不相容

所需对象或值已经存在，但实现把它当成另一种对象协议，调用该类型不支持的方法、运算、索引或调用约定，导致正常路径上的 `TypeError`、`AttributeError` 等。

- 纳入：对字典调用列表 `.sort()`；在标量上调用集合均值方法；把整数当可切片序列；对字符串字符做按位异或/取模；把 Python 列表当数组布尔掩码；用索引列表直接索引 Python 列表。
- 排除与边界：名称或 import 根本不存在用 CE03；文本/数值表示转换缺失用 CE04；只是没有验证输入类型用 CE12。
- 支持：17 个 artifact。完整列表见 `codebook.json` 的 `supporting_cases`。
- 边界案例：row 249（artifact 319）对字典调用不存在的 `.sort()`；row 348（artifact 464）既把目标换成十进制原样返回 CE05，也在备用分支把整数传给字符串解析接口 CE14。
- 代表案例：artifact `319`（row 249；完整材料见 `results.json`）。

````text
    words = set(words)
    word_count = {}
    for word in words:
        word_count[word] = word_count.get(word, 0) + 1
    word_count.sort(key=word_count.get, reverse=True)
    return word_count[0]
````

把词内字符数换成词频，未比较候选且对字典调用不支持的方法。

## 冻结边界与多标签规则

- CE03 + CE05：依赖缺失，同时即使补齐依赖，计算目标仍错误。
- CE04 + CE14：先遗漏必要表示转换，随后对错误类型执行不支持操作。
- CE05 + CE07：既换了比较/优化目标，又只覆盖了部分候选。
- CE06 + CE10：状态窗口推进错误与递推关系/基础值错误并存。
- CE08 + CE11：只有在内部序列结构和外部表示分别有独立错误时同时使用；不能为同一格式现象重复贴码。
- CE09 + CE12：控制流位置/优先级错误与独立的条件覆盖遗漏并存时才同时使用。

## 配套文件

- `codebook.json`：结构化定义、支持案例、计数、代表证据和方法元数据。
- `codebook.csv`：表格化 codebook。
- `assignments.json` / `assignments.csv`：每个 artifact 的 code、理由、逐字证据与证据限制。
- `taxonomy.json`：与 GPT6-1 一致的 HOW-style 类别树。
- `results.json`：冻结材料正文与最终类别的逐条组合。
