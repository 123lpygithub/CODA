# CodeErrors / deepseek-1

Schema: `coda.artifact.v1`. Artifacts: **557**; codes: **15**; artifact–code assignments: **735**.

This package uses the common seven-file format. All existing coding decisions, evidence and limitations are preserved. Additional source-specific fields are retained in `extensions`; original codebook text is retained in `codebook.json` metadata extensions and the local pre-conversion backup.

## Scope and method

Single-analyst full-text reading, inductive consolidation, explicit per-artifact mapping and verbatim evidence review

Mechanical format validation does not establish independent semantic accuracy.

## Codes

| Code | Name | Artifacts |
|---|---|---:|
| CE01 | 实质实现未交付 | 81 |
| CE02 | 源码截断或语法不完整 | 31 |
| CE03 | 未定义或未提供的名称 | 35 |
| CE04 | 解析、分词或表示转换错误 | 19 |
| CE05 | 计算目标被替换 | 268 |
| CE06 | 遍历、候选或状态覆盖不足 | 55 |
| CE07 | 条件判断或提前返回错误 | 26 |
| CE08 | 结果组装、顺序或重数错误 | 40 |
| CE09 | 数学公式、递推或数值方法错误 | 85 |
| CE10 | 初始化或状态转移错误 | 9 |
| CE11 | 输入域、类型或边界校验缺失 | 34 |
| CE12 | 对象类型或操作协议不相容 | 20 |
| CE13 | 输出格式或表示契约错误 | 15 |
| CE14 | 字符或大小写规范语义错误 | 17 |
| CE15 | 按提供材料未观察到可归因缺陷 | 0 |

## CE01 — 实质实现未交付

目标函数没有形成可执行的主体实现：pass、仅注释、固定常量或只覆盖示例。

- Include: 空函数体、只有注释、无有效返回、用与输入无关的常量或示例值顶替求解。
- Exclude: 主体逻辑存在但覆盖不全用 CE06；调用未定义名称用 CE03；源码截断用 CE02。
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 81; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "1",
    "field": "content",
    "start_char": 560,
    "end_char": 2519,
    "quote": "from typing import List\n\n\ndef separate_paren_groups(paren_string: str) -> List[str]:\n    \"\"\" Input to this function is a string containing multiple groups of nested parentheses. Your goal is to\n    separate those group into separate strings and return the list of those.\n    Separate groups are balanced (each open brace is properly closed) and not nested within each other\n    Ignore any spaces in the input string.\n    >>> separate_paren_groups('( ) (( )) (( )( ))')\n    ['()', '(())', '(()())']\n    \"\"\"\n    # TODO: Implement this function\n    # pass\n    # return []\n    # stack = []\n    # for i in range(len(paren_string)):\n    #     if paren_string[i] == '(':\n    #         stack.append(paren_string[i])\n    #     elif paren_string[i] == ')':\n    #         stack.pop()\n    #         if len(stack) == 0:\n    #             return [paren_string[:i+1]]\n    # return [paren_string]\n\n    # stack = []\n    # for i in range(len(paren_string)):\n    #     if paren_string[i] == '(':\n    #         stack.append(paren_string[i])\n    #     elif paren_string[i] == ')':\n    #         stack.pop()\n    #         if len(stack) == 0:\n    #             return [paren_string[:i+1]]\n    # return [paren_string]\n\n    # stack = []\n    # for i in range(len(paren_string)):\n    #     if paren_string[i] == '(':\n    #         stack.append(paren_string[i])\n    #     elif paren_string[i] == ')':\n    #         stack.pop()\n    #         if len(stack) == 0:\n    #             return [paren_string[:i+1]]\n    # return [paren_string]\n\n    # stack = []\n    # for i in range(len(paren_string)):\n    #     if paren_string[i] == '(':\n    #         stack.append(paren_string[i])\n    #     elif paren_string[i] == ')':\n    #         stack.pop()\n    #         if len(stack) == 0:\n    #             return [paren_string[:i+1]]\n    # return [paren_string]\n\n    # stack = []\n    # for i in range(len(paren_string)):\n    #     if paren_string[i] == '(':\n    #         stack.append(paren_string[i])",
    "interpretation": "目标函数主体全部为注释，没有可执行实现。"
  }
]
````

## CE02 — 源码截断或语法不完整

冻结源码在 token、表达式、容器或缩进块中途结束，模块无法解析。

- Include: 括号/引号未闭合、缩进块中断、表达式截断、语法错误导致不可导入。
- Exclude: 合法语法但缺 return 用 CE01；运行时类型错误用 CE12。
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 31; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "17",
    "field": "content",
    "start_char": 234,
    "end_char": 2158,
    "quote": "import math\n\n\ndef poly(xs: list, x: float):\n    \"\"\"\n    Evaluates polynomial with coefficients xs at point x.\n    return xs[0] + xs[1] * x + xs[1] * x^2 + .... xs[n] * x^n\n    \"\"\"\n    return sum([coeff * math.pow(x, i) for i, coeff in enumerate(xs)])\n\n\ndef find_zero(xs: list):\n    \"\"\" xs are coefficients of a polynomial.\n    find_zero find x such that poly(x) = 0.\n    find_zero returns only only zero point, even if there are many.\n    Moreover, find_zero only takes list xs having even number of coefficients\n    and largest non zero coefficient as it guarantees\n    a solution.\n    >>> round(find_zero([1, 2]), 2) # f(x) = 1 + 2x\n    -0.5\n    >>> round(find_zero([-6, 11, -6, 1]), 2) # (x - 1) * (x - 2) * (x - 3) = -6 + 11x - 6x^2 + x^3\n    1.0\n    \"\"\"\n    assert len(xs) % 2 == 0, \"xs must have even number of coefficients\"\n    assert max(xs) != 0, \"xs must have largest non zero coefficient\"\n    xs = [x / max(xs) for x in xs]\n    xs.sort(reverse=True)\n    xs = [x * -1 for x in xs]\n    xs.append(0)\n    xs.sort()\n    xs = [x * -1 for x in xs]\n    xs.append(0)\n    xs.sort(reverse=True)\n    xs = [x * -1 for x in xs]\n    xs.append(0)\n    xs.sort()\n    xs = [x * -1 for x in xs]\n    xs.append(0)\n    xs.sort(reverse=True)\n    xs = [x * -1 for x in xs]\n    xs.append(0)\n    xs.sort()\n    xs = [x * -1 for x in xs]\n    xs.append(0)\n    xs.sort(reverse=True)\n    xs = [x * -1 for x in xs]\n    xs.append(0)\n    xs.sort()\n    xs = [x * -1 for x in xs]\n    xs.append(0)\n    xs.sort(reverse=True)\n    xs = [x * -1 for x in xs]\n    xs.append(0)\n    xs.sort()\n    xs = [x * -1 for x in xs]\n    xs.append(0)\n    xs.sort(reverse=True)\n    xs = [x * -1 for x in xs]\n    xs.append(0)\n    xs.sort()\n    xs = [x * -1 for x in xs]\n    xs.append(0)\n    xs.sort(reverse=True)\n    xs = [x * -1 for x in xs]\n    xs.append(0)\n    xs.sort()\n    xs = [x * -1 for x in xs]\n    xs.append(0)\n    xs.sort(reverse=True)\n    xs = [x * -1 for x in",
    "interpretation": "find_zero 在循环表达式中途截断，且可见主体是对系数反复排序而非求解 poly(x)=0。"
  }
]
````

## CE03 — 未定义或未提供的名称

正常路径引用本 artifact 未定义、未导入、任务也未承诺提供的模块、函数或变量。

- Include: 调用未定义 helper、未导入模块、拼错名称、使用未绑定变量。
- Exclude: 对象存在但操作不支持用 CE12；名称在另一段被定义则不算。
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 35; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "5",
    "field": "content",
    "start_char": 143,
    "end_char": 908,
    "quote": "def is_palindrome(string: str) -> bool:\n    \"\"\" Test if given string is a palindrome \"\"\"\n    return string == string[::-1]\n\n\ndef make_palindrome(string: str) -> str:\n    \"\"\" Find the shortest palindrome that begins with a supplied string.\n    Algorithm idea is simple:\n    - Find the longest postfix of supplied string that is a palindrome.\n    - Append to the end of the string reverse of a string prefix that comes before the palindromic suffix.\n    >>> make_palindrome('')\n    ''\n    >>> make_palindrome('cat')\n    'catac'\n    >>> make_palindrome('cata')\n    'catac'\n    \"\"\"\n    if not string:\n        return ''\n    if is_palindrome(string):\n        return string\n    palindrome_prefix = find_palindrome_prefix(string)\n    return palindrome_prefix + string[::-1]",
    "interpretation": "正常路径调用未定义的 find_palindrome_prefix。"
  }
]
````

## CE04 — 解析、分词或表示转换错误

输入被按错误边界或错误表示域解释，或文本/字符/数值/结构表示转换不成立。

- Include: 错误分隔符、错误字段边界、把英文数字直接 int、错误类型转换、分词丢元素。
- Exclude: 解析正确但公式错用 CE09；输出格式不符用 CE13。
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 19; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "6",
    "field": "content",
    "start_char": 587,
    "end_char": 1206,
    "quote": "from typing import List\n\n\ndef parse_music(music_string: str) -> List[int]:\n    \"\"\" Input to this function is a string representing musical notes in a special ASCII format.\n    Your task is to parse this string and return list of integers corresponding to how many beats does each\n    not last.\n\n    Here is a legend:\n    'o' - whole note, lasts four beats\n    'o|' - half note, lasts two beats\n    '.|' - quater note, lasts one beat\n\n    >>> parse_music('o o| .| o| o| .| .| .| .| o o')\n    [4, 2, 1, 2, 2, 1, 1, 1, 1, 4, 4]\n    \"\"\"\n    return [4 if x == 'o' else 2 if x == 'o|' else 1 for x in music_string.split('|')]",
    "interpretation": "用 split('|') 切分音符，把 'o|' 拆成两段，音符边界解析错误。"
  }
]
````

## CE05 — 计算目标被替换

实现计算了可辨识但与契约不同的量、对象、谓词或粒度。

- Include: 求极值代替最近对、按字典序代替数值序、判断偶数代替判素、返回常量目标。
- Exclude: 目标正确但候选/循环覆盖不全用 CE06；目标正确但公式写错用 CE09。
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 268; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "2",
    "field": "content",
    "start_char": 502,
    "end_char": 1083,
    "quote": "from typing import List\n\n\ndef below_zero(operations: List[int]) -> bool:\n    \"\"\" You're given a list of deposit and withdrawal operations on a bank account that starts with\n    zero balance. Your task is to detect if at any point the balance of account fallls below zero, and\n    at that point function should return True. Otherwise it should return False.\n    >>> below_zero([1, 2, 3])\n    False\n    >>> below_zero([1, 2, -4, 5])\n    True\n    \"\"\"\n    if len(operations) == 0:\n        return False\n    if operations[0] < 0:\n        return True\n    return below_zero(operations[1:])",
    "interpretation": "递归只判断当前首项是否为负，从不累计余额；既替换了“任一时点余额”目标，也缺少状态转移。"
  }
]
````

## CE06 — 遍历、候选或状态覆盖不足

目标量正确，但循环边界、候选枚举、状态推进或累积覆盖不完整。

- Include: 少遍历元素、提前停止枚举、漏状态分支、边界少一轮、只检查部分候选。
- Exclude: 完全换掉目标用 CE05；条件写反用 CE07。
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 55; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "11",
    "field": "content",
    "start_char": 224,
    "end_char": 477,
    "quote": "def largest_divisor(n: int) -> int:\n    \"\"\" For a given number n, find the largest number that divides n evenly, smaller than n\n    >>> largest_divisor(15)\n    5\n    \"\"\"\n    divisor = 1\n    while n % divisor != 0:\n        divisor += 1\n    return divisor",
    "interpretation": "从 1 向上递增寻找首个约数并立即返回 1，候选枚举方向与契约要求的“小于 n 的最大约数”相反。"
  }
]
````

## CE07 — 条件判断或提前返回错误

分支条件、终止条件或提前返回使错误路径被选择。

- Include: 比较方向反、and/or 混用、return 位置错误、基线条件错误、循环终止条件错。
- Exclude: 边界输入未校验用 CE11；数学递推公式错用 CE09。
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 26; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "33",
    "field": "content",
    "start_char": 89,
    "end_char": 670,
    "quote": "FIX = \"\"\"\nAdd more test cases.\n\"\"\"\n\ndef vowels_count(s):\n    \"\"\"Write a function vowels_count which takes a string representing\n    a word as input and returns the number of vowels in the string.\n    Vowels in this case are 'a', 'e', 'i', 'o', 'u'. Here, 'y' is also a\n    vowel, but only when it is at the end of the given word.\n\n    Example:\n    >>> vowels_count(\"abcde\")\n    2\n    >>> vowels_count(\"ACEDY\")\n    3\n    \"\"\"\n    vowels = \"aeiou\"\n    count = 0\n    for i in s:\n        if i in vowels:\n            count += 1\n    if s[-1] in vowels:\n        count += 1\n    return count",
    "interpretation": "vowels 只含小写，未处理大写；末位为元音时重复加 1，且未实现“末尾 y 才算元音”的条件。"
  }
]
````

## CE08 — 结果组装、顺序或重数错误

元素、位置、顺序、重复次数或返回结构被错误组装。

- Include: 分隔符位置错、奇偶重排、丢首尾元素、重复添加、嵌套层级/顺序错。
- Exclude: 输出类型/格式契约错用 CE13；计算值本身错用 CE05/CE09。
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 40; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "3",
    "field": "content",
    "start_char": 341,
    "end_char": 712,
    "quote": "from typing import List\n\n\ndef intersperse(numbers: List[int], delimeter: int) -> List[int]:\n    \"\"\" Insert a number 'delimeter' between every two consecutive elements of input list `numbers'\n    >>> intersperse([], 4)\n    []\n    >>> intersperse([1, 2, 3], 4)\n    [1, 4, 2, 4, 3]\n    \"\"\"\n    return [delimeter] + [numbers[i] for i in range(len(numbers) - 1)] + [delimeter]",
    "interpretation": "实现把分隔符放在两端，且只取前 len-1 个元素，结果组装与顺序错误。"
  }
]
````

## CE09 — 数学公式、递推或数值方法错误

目标量正确但公式、递推关系、取整或数值方法本身写错。

- Include: 递推式错、取模/回绕缺失、平均/中位数公式错、二分/筛法方法错、浮点处理错。
- Exclude: 目标量被替换用 CE05；初始化/状态转移错用 CE10。
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 85; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "19",
    "field": "content",
    "start_char": 280,
    "end_char": 658,
    "quote": "def fizz_buzz(n: int):\n    \"\"\"Return the number of times the digit 7 appears in integers less than n which are divisible by 11 or 13.\n    >>> fizz_buzz(50)\n    0\n    >>> fizz_buzz(78)\n    2\n    >>> fizz_buzz(79)\n    3\n    \"\"\"\n    count = 0\n    for i in range(1, n):\n        if i % 11 == 0 or i % 13 == 0:\n            if \"7\" in str(i):\n                count += 1\n    return count",
    "interpretation": "循环从 1 开始漏掉 0，并用成员判断只计“含 7”一次，未统计数字 7 的出现次数。"
  }
]
````

## CE10 — 初始化或状态转移错误

初始值、变量更新或状态转移步骤写错，导致后续计算基于错误状态。

- Include: 累加器初值错、余额未更新、DP 转移错、循环变量更新错。
- Exclude: 循环边界少一轮用 CE06；条件方向错用 CE07。
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 9; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "2",
    "field": "content",
    "start_char": 502,
    "end_char": 1083,
    "quote": "from typing import List\n\n\ndef below_zero(operations: List[int]) -> bool:\n    \"\"\" You're given a list of deposit and withdrawal operations on a bank account that starts with\n    zero balance. Your task is to detect if at any point the balance of account fallls below zero, and\n    at that point function should return True. Otherwise it should return False.\n    >>> below_zero([1, 2, 3])\n    False\n    >>> below_zero([1, 2, -4, 5])\n    True\n    \"\"\"\n    if len(operations) == 0:\n        return False\n    if operations[0] < 0:\n        return True\n    return below_zero(operations[1:])",
    "interpretation": "递归只判断当前首项是否为负，从不累计余额；既替换了“任一时点余额”目标，也缺少状态转移。"
  }
]
````

## CE11 — 输入域、类型或边界校验缺失

未处理契约要求处理的边界值、非法输入或类型差异。

- Include: 空输入、负数、零、单元素、非法日期、越界下标、未捕获转换异常。
- Exclude: 类型不支持所调用操作用 CE12；正常输入上的逻辑错不归 CE11。
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 34; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "40",
    "field": "content",
    "start_char": 472,
    "end_char": 1032,
    "quote": "def triangle_area(a, b, c):\n    '''\n    Given the lengths of the three sides of a triangle. Return the area of\n    the triangle rounded to 2 decimal points if the three sides form a valid triangle. \n    Otherwise return -1\n    Three sides make a valid triangle when the sum of any two sides is greater \n    than the third side.\n    Example:\n    triangle_area(3, 4, 5) == 6.00\n    triangle_area(1, 2, 10) == -1\n    '''\n    # Calculate the area of the triangle\n    s = (a + b + c) / 2\n    area = (s * (s - a) * (s - b) * (s - c)) ** 0.5\n    return round(area, 2)",
    "interpretation": "未先判断三边能否构成三角形，非法输入会返回数值或复数。"
  }
]
````

## CE12 — 对象类型或操作协议不相容

对现有对象施加了其类型不支持的运算或调用，产生运行时错误。

- Include: 字符串索引列表、字符取模、对 None 调用方法、参数结构不符合 API。
- Exclude: 名称未定义用 CE03；合法操作但公式错用 CE09。
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 20; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "76",
    "field": "content",
    "start_char": 391,
    "end_char": 822,
    "quote": "def unique_digits(x):\n    \"\"\"Given a list of positive integers x. return a sorted list of all \n    elements that hasn't any even digit.\n\n    Note: Returned list should be sorted in increasing order.\n    \n    For example:\n    >>> unique_digits([15, 33, 1422, 1])\n    [1, 15, 33]\n    >>> unique_digits([152, 323, 1422, 10])\n    []\n    \"\"\"\n    return sorted(list(filter(lambda x: not any(map(lambda y: y % 2 == 0, list(str(x)))), x)))",
    "interpretation": "对 str 的每个字符执行 y % 2，类型不支持该运算，且判据未先转成整数。"
  }
]
````

## CE13 — 输出格式或表示契约错误

返回值的类型、格式、前缀、大小写或字符串表示不符合任务契约。

- Include: 返回 lambda/元组/列表类型错、缺前缀、连接符错、大小写表示错。
- Exclude: 元素内容本身算错用 CE08；字符级比较规范错用 CE14。
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 15; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "25",
    "field": "content",
    "start_char": 352,
    "end_char": 873,
    "quote": "def change_base(x: int, base: int):\n    \"\"\"Change numerical base of input number x to base.\n    return string representation after the conversion.\n    base numbers are less than 10.\n    >>> change_base(8, 3)\n    '22'\n    >>> change_base(8, 2)\n    '1000'\n    >>> change_base(7, 2)\n    '111'\n    \"\"\"\n    if x == 0:\n        return '0'\n    if base == 10:\n        return str(x)\n    if base == 2:\n        return bin(x)[2:]\n    if base == 8:\n        return oct(x)[2:]\n    if base == 16:\n        return hex(x)[2:]\n    return None",
    "interpretation": "仅对 2/8/10/16 特判，其他 base<10 返回 None；覆盖不足且破坏字符串返回契约。"
  }
]
````

## CE14 — 字符或大小写规范语义错误

字符级比较、大小写或字符集规范被错误应用。

- Include: 大小写不敏感比较、大小写转换范围错、字符集/编码判断错、元音/字母分类错。
- Exclude: 整串解析错误用 CE04；输出格式错用 CE13。
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 17; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "28",
    "field": "content",
    "start_char": 434,
    "end_char": 891,
    "quote": "def remove_vowels(text):\n    \"\"\"\n    remove_vowels is a function that takes string and returns string without vowels.\n    >>> remove_vowels('')\n    ''\n    >>> remove_vowels(\"abcdef\\nghijklm\")\n    'bcdf\\nghjklm'\n    >>> remove_vowels('abcdef')\n    'bcdf'\n    >>> remove_vowels('aaaaa')\n    ''\n    >>> remove_vowels('aaBAA')\n    'B'\n    >>> remove_vowels('zbcd')\n    'zbcd'\n    \"\"\"\n    vowels = 'aeiou'\n    return ''.join([i for i in text if i not in vowels])",
    "interpretation": "vowels 只含小写字符，未处理大写元音，字符分类范围错误。"
  }
]
````

## CE15 — 按提供材料未观察到可归因缺陷

逐条核对任务契约、错误源码与正确源码后，未发现可由现有代码描述的独立失败机制。

- Include: 实现与契约一致，或差异仅是未被材料支持的推测。
- Exclude: 存在不确定或未覆盖输入时，应保留具体边界代码，不应使用 CE15。
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 0; complete membership in `supporting_cases`.

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

# deepseek-1 — Code errors 最终编码本

本轮覆盖 **557 份生成代码、687 条来源记录、150 个任务**。共有 **15 个可分配 code**；分组不是额外编码。允许针对独立缺陷进行多重编码，因此类别覆盖数之和可以超过案例数。

这是单个 AI 编码者的逐条完整阅读与归纳，未使用原始人工类别作为模板，也未经过人工审核。所有案例均已编码，没有未决案例。完整方法与限制见 `METHOD.md`。

## 类别一览

|Code|类别|英文名称|覆盖案例数|
|---|---|---|---:|
|CE01|实质实现未交付|实质实现未交付|81|
|CE02|源码截断或语法不完整|源码截断或语法不完整|31|
|CE03|未定义或未提供的名称|未定义或未提供的名称|35|
|CE04|解析、分词或表示转换错误|解析、分词或表示转换错误|19|
|CE05|计算目标被替换|计算目标被替换|268|
|CE06|遍历、候选或状态覆盖不足|遍历、候选或状态覆盖不足|55|
|CE07|条件判断或提前返回错误|条件判断或提前返回错误|26|
|CE08|结果组装、顺序或重数错误|结果组装、顺序或重数错误|40|
|CE09|数学公式、递推或数值方法错误|数学公式、递推或数值方法错误|85|
|CE10|初始化或状态转移错误|初始化或状态转移错误|9|
|CE11|输入域、类型或边界校验缺失|输入域、类型或边界校验缺失|34|
|CE12|对象类型或操作协议不相容|对象类型或操作协议不相容|20|
|CE13|输出格式或表示契约错误|输出格式或表示契约错误|15|
|CE14|字符或大小写规范语义错误|字符或大小写规范语义错误|17|
|CE15|按提供材料未观察到可归因缺陷|按提供材料未观察到可归因缺陷|0|

## 使用规则

以交付代码中的可观察失败机制为单位，不推断模型的心理原因。优先选择能准确解释证据的具体类别；只有存在不同证据支持的不同缺陷时才多重编码。题目约束优先，参考实现用于理解而非要求相同算法。

## CE01 实质实现未交付

**实质实现未交付**

目标函数没有形成可执行的主体实现：pass、仅注释、固定常量或只覆盖示例。

- 纳入：空函数体、只有注释、无有效返回、用与输入无关的常量或示例值顶替求解。
- 排除与边界：主体逻辑存在但覆盖不全用 CE06；调用未定义名称用 CE03；源码截断用 CE02。
- 支持：81 份代码。完整列表见 `codebook.json` 的 `supporting_case_ids`。
- 代表案例：`1`，字符区间 560:2519。

```text
from typing import List


def separate_paren_groups(paren_string: str) -> List[str]:
    """ Input to this function is a string containing multiple groups of nested parentheses. Your goal is to
    separate those group into separate strings and return the list of those.
    Separate groups are balanced (each open brace is properly closed) and not nested within each other
    Ignore any spaces in the input string.
    >>> separate_paren_groups('( ) (( )) (( )( ))')
    ['()', '(())', '(()())']
    """
    # TODO: Implement this function
    # pass
    # return []
    # stack = []
    # for i in range(len(paren_string)):
    #     if paren_string[i] == '(':
    #         stack.append(paren_string[i])
    #     elif paren_string[i] == ')':
    #         stack.pop()
    #         if len(stack) == 0:
    #             return [paren_string[:i+1]]
    # return [paren_string]

    # stack = []
    # for i in range(len(paren_string)):
    #     if paren_string[i] == '(':
    #         stack.append(paren_string[i])
    #     elif paren_string[i] == ')':
    #         stack.pop()
    #         if len(stack) == 0:
    #             return [paren_string[:i+1]]
    # return [paren_string]

    #
```

目标函数主体全部为注释，没有可执行实现。

## CE02 源码截断或语法不完整

**源码截断或语法不完整**

冻结源码在 token、表达式、容器或缩进块中途结束，模块无法解析。

- 纳入：括号/引号未闭合、缩进块中断、表达式截断、语法错误导致不可导入。
- 排除与边界：合法语法但缺 return 用 CE01；运行时类型错误用 CE12。
- 支持：31 份代码。完整列表见 `codebook.json` 的 `supporting_case_ids`。
- 代表案例：`17`，字符区间 234:2158。

```text
import math


def poly(xs: list, x: float):
    """
    Evaluates polynomial with coefficients xs at point x.
    return xs[0] + xs[1] * x + xs[1] * x^2 + .... xs[n] * x^n
    """
    return sum([coeff * math.pow(x, i) for i, coeff in enumerate(xs)])


def find_zero(xs: list):
    """ xs are coefficients of a polynomial.
    find_zero find x such that poly(x) = 0.
    find_zero returns only only zero point, even if there are many.
    Moreover, find_zero only takes list xs having even number of coefficients
    and largest non zero coefficient as it guarantees
    a solution.
    >>> round(find_zero([1, 2]), 2) # f(x) = 1 + 2x
    -0.5
    >>> round(find_zero([-6, 11, -6, 1]), 2) # (x - 1) * (x - 2) * (x - 3) = -6 + 11x - 6x^2 + x^3
    1.0
    """
    assert len(xs) % 2 == 0, "xs must have even number of coefficients"
    assert max(xs) != 0, "xs must have largest non zero coefficient"
    xs = [x / max(xs) for x in xs]
    xs.sort(reverse=True)
    xs = [x * -1 for x in xs]
    xs.append(0)
    xs.sort()
    xs = [x * -1 for x in xs]
    xs.append(0)
    xs.sort(reverse=True)
    xs = [x * -1 for x in xs]
    xs.append(0)
    xs.sort()
    xs = [x * -1 for x in xs]
    xs.append(
```

find_zero 在循环表达式中途截断，且可见主体是对系数反复排序而非求解 poly(x)=0。

## CE03 未定义或未提供的名称

**未定义或未提供的名称**

正常路径引用本 artifact 未定义、未导入、任务也未承诺提供的模块、函数或变量。

- 纳入：调用未定义 helper、未导入模块、拼错名称、使用未绑定变量。
- 排除与边界：对象存在但操作不支持用 CE12；名称在另一段被定义则不算。
- 支持：35 份代码。完整列表见 `codebook.json` 的 `supporting_case_ids`。
- 代表案例：`5`，字符区间 143:908。

```text
def is_palindrome(string: str) -> bool:
    """ Test if given string is a palindrome """
    return string == string[::-1]


def make_palindrome(string: str) -> str:
    """ Find the shortest palindrome that begins with a supplied string.
    Algorithm idea is simple:
    - Find the longest postfix of supplied string that is a palindrome.
    - Append to the end of the string reverse of a string prefix that comes before the palindromic suffix.
    >>> make_palindrome('')
    ''
    >>> make_palindrome('cat')
    'catac'
    >>> make_palindrome('cata')
    'catac'
    """
    if not string:
        return ''
    if is_palindrome(string):
        return string
    palindrome_prefix = find_palindrome_prefix(string)
    return palindrome_prefix + string[::-1]
```

正常路径调用未定义的 find_palindrome_prefix。

## CE04 解析、分词或表示转换错误

**解析、分词或表示转换错误**

输入被按错误边界或错误表示域解释，或文本/字符/数值/结构表示转换不成立。

- 纳入：错误分隔符、错误字段边界、把英文数字直接 int、错误类型转换、分词丢元素。
- 排除与边界：解析正确但公式错用 CE09；输出格式不符用 CE13。
- 支持：19 份代码。完整列表见 `codebook.json` 的 `supporting_case_ids`。
- 代表案例：`6`，字符区间 587:1206。

```text
from typing import List


def parse_music(music_string: str) -> List[int]:
    """ Input to this function is a string representing musical notes in a special ASCII format.
    Your task is to parse this string and return list of integers corresponding to how many beats does each
    not last.

    Here is a legend:
    'o' - whole note, lasts four beats
    'o|' - half note, lasts two beats
    '.|' - quater note, lasts one beat

    >>> parse_music('o o| .| o| o| .| .| .| .| o o')
    [4, 2, 1, 2, 2, 1, 1, 1, 1, 4, 4]
    """
    return [4 if x == 'o' else 2 if x == 'o|' else 1 for x in music_string.split('|')]
```

用 split('|') 切分音符，把 'o|' 拆成两段，音符边界解析错误。

## CE05 计算目标被替换

**计算目标被替换**

实现计算了可辨识但与契约不同的量、对象、谓词或粒度。

- 纳入：求极值代替最近对、按字典序代替数值序、判断偶数代替判素、返回常量目标。
- 排除与边界：目标正确但候选/循环覆盖不全用 CE06；目标正确但公式写错用 CE09。
- 支持：268 份代码。完整列表见 `codebook.json` 的 `supporting_case_ids`。
- 代表案例：`2`，字符区间 502:1083。

```text
from typing import List


def below_zero(operations: List[int]) -> bool:
    """ You're given a list of deposit and withdrawal operations on a bank account that starts with
    zero balance. Your task is to detect if at any point the balance of account fallls below zero, and
    at that point function should return True. Otherwise it should return False.
    >>> below_zero([1, 2, 3])
    False
    >>> below_zero([1, 2, -4, 5])
    True
    """
    if len(operations) == 0:
        return False
    if operations[0] < 0:
        return True
    return below_zero(operations[1:])
```

递归只判断当前首项是否为负，从不累计余额；既替换了“任一时点余额”目标，也缺少状态转移。

## CE06 遍历、候选或状态覆盖不足

**遍历、候选或状态覆盖不足**

目标量正确，但循环边界、候选枚举、状态推进或累积覆盖不完整。

- 纳入：少遍历元素、提前停止枚举、漏状态分支、边界少一轮、只检查部分候选。
- 排除与边界：完全换掉目标用 CE05；条件写反用 CE07。
- 支持：55 份代码。完整列表见 `codebook.json` 的 `supporting_case_ids`。
- 代表案例：`11`，字符区间 224:477。

```text
def largest_divisor(n: int) -> int:
    """ For a given number n, find the largest number that divides n evenly, smaller than n
    >>> largest_divisor(15)
    5
    """
    divisor = 1
    while n % divisor != 0:
        divisor += 1
    return divisor
```

从 1 向上递增寻找首个约数并立即返回 1，候选枚举方向与契约要求的“小于 n 的最大约数”相反。

## CE07 条件判断或提前返回错误

**条件判断或提前返回错误**

分支条件、终止条件或提前返回使错误路径被选择。

- 纳入：比较方向反、and/or 混用、return 位置错误、基线条件错误、循环终止条件错。
- 排除与边界：边界输入未校验用 CE11；数学递推公式错用 CE09。
- 支持：26 份代码。完整列表见 `codebook.json` 的 `supporting_case_ids`。
- 代表案例：`33`，字符区间 89:670。

```text
FIX = """
Add more test cases.
"""

def vowels_count(s):
    """Write a function vowels_count which takes a string representing
    a word as input and returns the number of vowels in the string.
    Vowels in this case are 'a', 'e', 'i', 'o', 'u'. Here, 'y' is also a
    vowel, but only when it is at the end of the given word.

    Example:
    >>> vowels_count("abcde")
    2
    >>> vowels_count("ACEDY")
    3
    """
    vowels = "aeiou"
    count = 0
    for i in s:
        if i in vowels:
            count += 1
    if s[-1] in vowels:
        count += 1
    return count
```

vowels 只含小写，未处理大写；末位为元音时重复加 1，且未实现“末尾 y 才算元音”的条件。

## CE08 结果组装、顺序或重数错误

**结果组装、顺序或重数错误**

元素、位置、顺序、重复次数或返回结构被错误组装。

- 纳入：分隔符位置错、奇偶重排、丢首尾元素、重复添加、嵌套层级/顺序错。
- 排除与边界：输出类型/格式契约错用 CE13；计算值本身错用 CE05/CE09。
- 支持：40 份代码。完整列表见 `codebook.json` 的 `supporting_case_ids`。
- 代表案例：`3`，字符区间 341:712。

```text
from typing import List


def intersperse(numbers: List[int], delimeter: int) -> List[int]:
    """ Insert a number 'delimeter' between every two consecutive elements of input list `numbers'
    >>> intersperse([], 4)
    []
    >>> intersperse([1, 2, 3], 4)
    [1, 4, 2, 4, 3]
    """
    return [delimeter] + [numbers[i] for i in range(len(numbers) - 1)] + [delimeter]
```

实现把分隔符放在两端，且只取前 len-1 个元素，结果组装与顺序错误。

## CE09 数学公式、递推或数值方法错误

**数学公式、递推或数值方法错误**

目标量正确但公式、递推关系、取整或数值方法本身写错。

- 纳入：递推式错、取模/回绕缺失、平均/中位数公式错、二分/筛法方法错、浮点处理错。
- 排除与边界：目标量被替换用 CE05；初始化/状态转移错用 CE10。
- 支持：85 份代码。完整列表见 `codebook.json` 的 `supporting_case_ids`。
- 代表案例：`19`，字符区间 280:658。

```text
def fizz_buzz(n: int):
    """Return the number of times the digit 7 appears in integers less than n which are divisible by 11 or 13.
    >>> fizz_buzz(50)
    0
    >>> fizz_buzz(78)
    2
    >>> fizz_buzz(79)
    3
    """
    count = 0
    for i in range(1, n):
        if i % 11 == 0 or i % 13 == 0:
            if "7" in str(i):
                count += 1
    return count
```

循环从 1 开始漏掉 0，并用成员判断只计“含 7”一次，未统计数字 7 的出现次数。

## CE10 初始化或状态转移错误

**初始化或状态转移错误**

初始值、变量更新或状态转移步骤写错，导致后续计算基于错误状态。

- 纳入：累加器初值错、余额未更新、DP 转移错、循环变量更新错。
- 排除与边界：循环边界少一轮用 CE06；条件方向错用 CE07。
- 支持：9 份代码。完整列表见 `codebook.json` 的 `supporting_case_ids`。
- 代表案例：`2`，字符区间 502:1083。

```text
from typing import List


def below_zero(operations: List[int]) -> bool:
    """ You're given a list of deposit and withdrawal operations on a bank account that starts with
    zero balance. Your task is to detect if at any point the balance of account fallls below zero, and
    at that point function should return True. Otherwise it should return False.
    >>> below_zero([1, 2, 3])
    False
    >>> below_zero([1, 2, -4, 5])
    True
    """
    if len(operations) == 0:
        return False
    if operations[0] < 0:
        return True
    return below_zero(operations[1:])
```

递归只判断当前首项是否为负，从不累计余额；既替换了“任一时点余额”目标，也缺少状态转移。

## CE11 输入域、类型或边界校验缺失

**输入域、类型或边界校验缺失**

未处理契约要求处理的边界值、非法输入或类型差异。

- 纳入：空输入、负数、零、单元素、非法日期、越界下标、未捕获转换异常。
- 排除与边界：类型不支持所调用操作用 CE12；正常输入上的逻辑错不归 CE11。
- 支持：34 份代码。完整列表见 `codebook.json` 的 `supporting_case_ids`。
- 代表案例：`40`，字符区间 472:1032。

```text
def triangle_area(a, b, c):
    '''
    Given the lengths of the three sides of a triangle. Return the area of
    the triangle rounded to 2 decimal points if the three sides form a valid triangle. 
    Otherwise return -1
    Three sides make a valid triangle when the sum of any two sides is greater 
    than the third side.
    Example:
    triangle_area(3, 4, 5) == 6.00
    triangle_area(1, 2, 10) == -1
    '''
    # Calculate the area of the triangle
    s = (a + b + c) / 2
    area = (s * (s - a) * (s - b) * (s - c)) ** 0.5
    return round(area, 2)
```

未先判断三边能否构成三角形，非法输入会返回数值或复数。

## CE12 对象类型或操作协议不相容

**对象类型或操作协议不相容**

对现有对象施加了其类型不支持的运算或调用，产生运行时错误。

- 纳入：字符串索引列表、字符取模、对 None 调用方法、参数结构不符合 API。
- 排除与边界：名称未定义用 CE03；合法操作但公式错用 CE09。
- 支持：20 份代码。完整列表见 `codebook.json` 的 `supporting_case_ids`。
- 代表案例：`76`，字符区间 391:822。

```text
def unique_digits(x):
    """Given a list of positive integers x. return a sorted list of all 
    elements that hasn't any even digit.

    Note: Returned list should be sorted in increasing order.
    
    For example:
    >>> unique_digits([15, 33, 1422, 1])
    [1, 15, 33]
    >>> unique_digits([152, 323, 1422, 10])
    []
    """
    return sorted(list(filter(lambda x: not any(map(lambda y: y % 2 == 0, list(str(x)))), x)))
```

对 str 的每个字符执行 y % 2，类型不支持该运算，且判据未先转成整数。

## CE13 输出格式或表示契约错误

**输出格式或表示契约错误**

返回值的类型、格式、前缀、大小写或字符串表示不符合任务契约。

- 纳入：返回 lambda/元组/列表类型错、缺前缀、连接符错、大小写表示错。
- 排除与边界：元素内容本身算错用 CE08；字符级比较规范错用 CE14。
- 支持：15 份代码。完整列表见 `codebook.json` 的 `supporting_case_ids`。
- 代表案例：`25`，字符区间 352:873。

```text
def change_base(x: int, base: int):
    """Change numerical base of input number x to base.
    return string representation after the conversion.
    base numbers are less than 10.
    >>> change_base(8, 3)
    '22'
    >>> change_base(8, 2)
    '1000'
    >>> change_base(7, 2)
    '111'
    """
    if x == 0:
        return '0'
    if base == 10:
        return str(x)
    if base == 2:
        return bin(x)[2:]
    if base == 8:
        return oct(x)[2:]
    if base == 16:
        return hex(x)[2:]
    return None
```

仅对 2/8/10/16 特判，其他 base<10 返回 None；覆盖不足且破坏字符串返回契约。

## CE14 字符或大小写规范语义错误

**字符或大小写规范语义错误**

字符级比较、大小写或字符集规范被错误应用。

- 纳入：大小写不敏感比较、大小写转换范围错、字符集/编码判断错、元音/字母分类错。
- 排除与边界：整串解析错误用 CE04；输出格式错用 CE13。
- 支持：17 份代码。完整列表见 `codebook.json` 的 `supporting_case_ids`。
- 代表案例：`28`，字符区间 434:891。

```text
def remove_vowels(text):
    """
    remove_vowels is a function that takes string and returns string without vowels.
    >>> remove_vowels('')
    ''
    >>> remove_vowels("abcdef\nghijklm")
    'bcdf\nghjklm'
    >>> remove_vowels('abcdef')
    'bcdf'
    >>> remove_vowels('aaaaa')
    ''
    >>> remove_vowels('aaBAA')
    'B'
    >>> remove_vowels('zbcd')
    'zbcd'
    """
    vowels = 'aeiou'
    return ''.join([i for i in text if i not in vowels])
```

vowels 只含小写字符，未处理大写元音，字符分类范围错误。

## CE15 按提供材料未观察到可归因缺陷

**按提供材料未观察到可归因缺陷**

逐条核对任务契约、错误源码与正确源码后，未发现可由现有代码描述的独立失败机制。

- 纳入：实现与契约一致，或差异仅是未被材料支持的推测。
- 排除与边界：存在不确定或未覆盖输入时，应保留具体边界代码，不应使用 CE15。
- 支持：0 份代码。完整列表见 `codebook.json` 的 `supporting_case_ids`。

## 随附文件

`taxonomy.json` 是分类树；`results.json` 是 metadata/results 风格结果包；`codebook.json` 保存完整定义、支持案例和代表证据；`assignments.json`/`.csv` 保存逐例编码；`METHOD.md` 记录范围与方法。
