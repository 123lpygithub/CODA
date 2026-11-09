# Code errors — inductive codebook (GPT6-2)

557 artifacts · 687 source records · 150 tasks · 13 codes · 706 artifact–code assignments.

Each artifact has at least one code. Codes describe distinct observed mechanisms and may co-occur. Case 729 is conditional on an explicitly recorded interpretation of conflicting task requirements. This is a single-assistant source-based analysis, not a human-validated gold codebook.

| Code | Name | Artifacts |
|---|---|---:|
| C01 | Incomplete or nonfunctional implementation | 106 |
| C02 | Unavailable symbol or dependency | 46 |
| C03 | Incompatible operation or API use | 16 |
| C04 | Wrong computational target or unit of analysis | 122 |
| C05 | Omitted requirement or processing step | 93 |
| C06 | Incorrect decision condition | 54 |
| C07 | Incorrect traversal or positional coverage | 40 |
| C08 | Incorrect state evolution or termination | 29 |
| C09 | Incorrect arithmetic or numerical treatment | 32 |
| C10 | Incorrect representation or transformation | 68 |
| C11 | Incorrect ordering or selection priority | 44 |
| C12 | Incorrect result assembly or return contract | 36 |
| C13 | Unhandled boundary or exceptional input | 20 |

## C01 — Incomplete or nonfunctional implementation

实现未完成或缺乏有效处理

The supplied program lacks a completed task-solving path: its body is absent, its source is truncated, its general computation never returns a result, or it substitutes an input-independent placeholder for the requested behavior.

**Include**

- Pass-only or documentation-only bodies; unfinished literals, expressions or blocks.
- Repeated or partial statements without a completed computation and return.
- Constant placeholder output with no substantive implementation of the task.

**Exclude / distinguish**

- A missing local operation in an otherwise substantive algorithm: C05.
- An implemented calculation that solves a different problem: C04.
- A missing symbol used by otherwise interpretable logic: C02; co-code only if lack of a completed result is separate.

**Representative cases**

- Case 1: Function body is pass; no grouping behavior is implemented.
- Case 17: Repeated coefficient manipulation ends in an incomplete comprehension without finding or returning a root.
- Case 77: Returns an empty constant instead of processing nonempty inputs.
- Case 270: Calls undefined count_ones and repeats bit-length updates without returning an ordering.

Supporting artifacts: **106**. Exact source excerpts and all supporting IDs are in `codebook.json`; per-artifact requirements, evidence and caveats are in `assignments.json`.

## C02 — Unavailable symbol or dependency

引用未提供的符号或依赖

The supplied program requires a variable, helper, module or imported name that is not bound in the context provided with the artifact.

**Include**

- Calls to undeclared helpers or unimported modules.
- Misspelled or out-of-scope names needed for execution.

**Exclude / distinguish**

- A present object with an unsupported operation: C03.
- An unfinished token in truncated source, without a separately established dependency: C01.
- Do not assume an external execution harness supplies the missing name; state this context limit.

**Representative cases**

- Case 426: Calls math.floor without importing or defining math in the supplied program.
- Case 79: Calls is_palindrome and is_even without defining or importing them.
- Case 356: Uses undefined c in result construction, lacks a return, and max on empty counts fails the specified empty case.
- Case 138: Calls hashlib.md5 without importing hashlib.

Supporting artifacts: **46**. Exact source excerpts and all supporting IDs are in `codebook.json`; per-artifact requirements, evidence and caveats are in `assignments.json`.

## C03 — Incompatible operation or API use

操作与数据类型或 API 不匹配

An operation, method or API is applied to an object or argument structure that cannot provide the intended behavior under Python's type and API semantics.

**Include**

- Arithmetic on character strings, numeric objects treated as sequences, unsupported container methods.
- Invalid argument or subscript types; list multiplication used where scalar arithmetic is required.

**Exclude / distinguish**

- An undeclared object or function: C02.
- A valid operation with the wrong numeric formula: C09.
- Domain-specific text or numeric representation conversion errors are C10 when that explains the failure without an additional API misuse.

**Representative cases**

- Case 146: Calls mean on individual numeric elements, which do not supply that method.
- Case 435: Applies bitwise XOR directly to character strings.
- Case 208: Treats integer x as a sequence with length and slicing.
- Case 275: Uses a list of indices as a Python list subscript and omits the even-position eligibility condition.

Supporting artifacts: **16**. Exact source excerpts and all supporting IDs are in `codebook.json`; per-artifact requirements, evidence and caveats are in `assignments.json`.

## C04 — Wrong computational target or unit of analysis

计算目标或处理单位偏离要求

The implementation computes a different property, uses the wrong entities or aggregation level, or replaces the required relation with a non-equivalent proxy.

**Include**

- Word length instead of consonant count; whole-number properties instead of digit properties; indices instead of values.
- Whole-collection totals instead of per-group calculations; ordinary factorial instead of product of factorials.
- Checking a different mathematical property, such as parity instead of primality.

**Exclude / distinguish**

- The intended quantity is computed with a wrong local formula: C09.
- A correct target lacks one additional eligibility check: C05.
- A recognizably correct predicate has an incorrect threshold or Boolean relation: C06.
- A ranking objective alone is wrong: C11.

**Representative cases**

- Case 271: Filters by whole-word length rather than number of consonants.
- Case 359: Rounds total pooled water once instead of rounding each well separately before summing.
- Case 114: Computes ordinary factorial rather than the product of factorials.
- Case 593: Uses parity as a substitute for primality.

Supporting artifacts: **122**. Exact source excerpts and all supporting IDs are in `codebook.json`; per-artifact requirements, evidence and caveats are in `assignments.json`.

## C05 — Omitted requirement or processing step

遗漏必要条件、分支或处理步骤

A substantive implementation performs part of the requested task but leaves out a required condition, operation, branch or explicitly stated implementation constraint.

**Include**

- Missing an eligibility filter, required transformation, alternate allowed mode, or part of a conjunction.
- Implementing only some explicitly permitted cases; ignoring a stated no-recursion constraint.
- Dropping the contribution of otherwise valid unmatched elements.

**Exclude / distinguish**

- The whole implementation is absent or a placeholder: C01.
- An existing condition is wrong rather than absent: C06.
- Prefer C07 for traversal coverage, C10 for representation-specific normalization, C11 for tie-breaking, and C13 for exceptional-input guards; do not add C05 again for the same omission.

**Representative cases**

- Case 55: Sums odd-index values without requiring those values to be even.
- Case 83: Returns all character counts without retaining only the maximum-frequency characters.
- Case 137: Omits reversal when the string has no letters.
- Case 721: Drops entries whose indices are multiples of neither three nor four.

Supporting artifacts: **93**. Exact source excerpts and all supporting IDs are in `codebook.json`; per-artifact requirements, evidence and caveats are in `assignments.json`.

## C06 — Incorrect decision condition

判断条件、阈值或分支优先级错误

A condition controlling eligibility, branching or result emission uses an incorrect relation, threshold, logical combination or precedence, although its intended decision can be identified.

**Include**

- Strict versus inclusive comparisons, reversed predicates, tautologies and contradictions.
- Unjustified restrictions and incorrect branch precedence.
- Result emission guarded by a condition unrelated to when that result is required.

**Exclude / distinguish**

- An absent condition: C05, or C13 for exceptional-input handling.
- A predicate for a fundamentally different property: C04.
- A faulty state reset or recurrence: C08; traversal bounds: C07.

**Representative cases**

- Case 151: Appends only when the count of new maxima equals the full length; zero initialization also invalidates negative maxima.
- Case 176: Includes zero despite requiring strictly positive numbers.
- Case 281: Requires strict increase, rejecting the explicitly permitted pair of equal values.
- Case 418: Gives cubing priority at indices divisible by both three and four, reversing the required precedence.

Supporting artifacts: **54**. Exact source excerpts and all supporting IDs are in `codebook.json`; per-artifact requirements, evidence and caveats are in `assignments.json`.

## C07 — Incorrect traversal or positional coverage

遍历范围、位置或候选覆盖错误

Iteration, indexing or candidate enumeration visits the wrong positions, omits required candidates, or accesses positions outside the applicable sequence bounds.

**Include**

- Off-by-one endpoints, incorrect index parity, wrong scan direction or returned neighboring index.
- Considering only adjacent or fixed candidates when arbitrary candidates are required.
- Skipping overlapping matches or forbidding permitted revisits.

**Exclude / distinguish**

- Correctly visited values are ranked incorrectly: C11.
- A failure restricted to an empty, zero-sized or short boundary input requiring a guard: C13.
- Wrong loop state or nontermination: C08; wrong semantic object being traversed: C04.

**Representative cases**

- Case 141: Tests only two fixed pairs and indexes four positions even when the list is shorter.
- Case 165: Advances by substring length and skips possible overlapping or unaligned matches.
- Case 375: Returns i-1 instead of the index i of the descending element.
- Case 368: Uses unimported heapq; globally marks cells visited despite allowed revisits and prioritizes last values rather than whole paths.

Supporting artifacts: **40**. Exact source excerpts and all supporting IDs are in `codebook.json`; per-artifact requirements, evidence and caveats are in `assignments.json`.

## C08 — Incorrect state evolution or termination

状态初始化、更新或终止错误

Stateful or recursive computation uses incorrect seeds, updates, recurrence dependencies or stopping behavior, so intermediate state no longer represents the required computation.

**Include**

- Wrong sequence bases, corrupted rolling state, future-state reads before initialization.
- Recursion with no decreasing argument or unsuccessful-cycle termination.
- Resetting a running aggregate on the wrong sign; losing associations when independently updating linked structures.

**Exclude / distinguish**

- A stateless formula error: C09.
- An output-only container shape problem: C12.
- Wrong loop index bounds without a state-evolution defect: C07.

**Representative cases**

- Case 334: Starts recurrence before all four base states and overwrites the previous d before shifting state.
- Case 81: Recursively rotates until sorted with no unsuccessful-cycle termination; unsortable rotations recurse indefinitely.
- Case 358: Resets negative running sums rather than positive ones when minimizing contiguous sum.
- Case 732: Sorts strength values apart from their names and selects index zero of the sorted scores, losing the score-to-extension association.

Supporting artifacts: **29**. Exact source excerpts and all supporting IDs are in `codebook.json`; per-artifact requirements, evidence and caveats are in `assignments.json`.

## C09 — Incorrect arithmetic or numerical treatment

算式、运算顺序或数值处理错误

The intended quantity is recognizable, but its mathematical expression, numeric operator, rounding, precision treatment or operation order is wrong.

**Include**

- Missing factors or roots, double counting, incorrect inclusion–exclusion formulas.
- True division instead of integer digit extraction, wrong rounding convention, operator precedence ignored.
- Numerical stopping or exactness assumptions that do not ensure the requested numeric result.

**Exclude / distinguish**

- Computing a different quantity altogether: C04.
- Wrong recurrence dependencies or state updates: C08.
- Wrong text encoding, sign representation or alphabet mapping: C10.
- Do not infer numerical instability solely because floating-point arithmetic is used.

**Representative cases**

- Case 485: Returns Heron radicand without taking its square root.
- Case 523: Uses ties-to-even round where halfway values must round away from zero.
- Case 387: Evaluates operators strictly left-to-right instead of respecting algebraic precedence and exponentiation associativity.
- Case 382: Doubles the correctly filtered squared sum without a requested factor of two.

Supporting artifacts: **32**. Exact source excerpts and all supporting IDs are in `codebook.json`; per-artifact requirements, evidence and caveats are in `assignments.json`.

## C10 — Incorrect representation or transformation

表示方式、解析或转换错误

Parsing, normalization, encoding, decoding or symbolic transformation fails to preserve or implement the task's intended meaning.

**Include**

- Wrong delimiters, numeral bases, signed-digit interpretation, character substitutions or case normalization.
- Regex syntax representing the wrong set of strings.
- Incompatible semantic representations such as string digits compared with integer values; failure to normalize interval bounds.

**Exclude / distinguish**

- Only the final message, marker, container or return shape is incorrect: C12.
- Generic unsupported methods or operand types without a representation-specific cause: C03.
- A missing unrelated eligibility filter: C05.

**Representative cases**

- Case 163: Counts case-sensitive characters without required case normalization.
- Case 80: Taking absolute values discards the required negative sign on the leading digit.
- Case 379: Uses a regex character class instead of extension alternatives, admitting invalid extensions and restricting allowed basename characters.
- Case 132: Additive Roman conversion omits required subtractive forms such as iv and ix.

Supporting artifacts: **68**. Exact source excerpts and all supporting IDs are in `codebook.json`; per-artifact requirements, evidence and caveats are in `assignments.json`.

## C11 — Incorrect ordering or selection priority

排序、择优规则或平局处理错误

The program orders values or chooses a preferred candidate using the wrong direction, ranking key, key precedence or tie-breaking rule.

**Include**

- Selecting first, smallest or most frequent when a different optimum is required.
- Ignoring a secondary key, reversing requested output order, comparing only the last component of a lexicographic path.
- Sorting positions that must remain in original order.

**Exclude / distinguish**

- A search never visits required candidates: C07.
- A generic property proxy outside ordering or selection: C04.
- A wrong key caused specifically by signed-digit interpretation: C10, without a redundant C11 label.

**Representative cases**

- Case 157: Sorts ascending by length then returns the shortest entry.
- Case 547: Sorts only by set-bit count and omits the numeric tie-break; prose and reference establish the tie-break despite inconsistent examples.
- Case 361: Returns the largest k elements in descending instead of required increasing order.
- Case 415: Compares only final path values rather than lexicographic sequences.

Supporting artifacts: **44**. Exact source excerpts and all supporting IDs are in `codebook.json`; per-artifact requirements, evidence and caveats are in `assignments.json`.

## C12 — Incorrect result assembly or return contract

结果组装或返回形式不符合要求

The returned result has the wrong structure, components, multiplicity, formatting or object kind, including incorrect placement of values in an assembled result.

**Include**

- Missing separators or markers, malformed message substitution, wrong list/tuple/scalar/function return form.
- Dropped or duplicated output elements, or incorrectly interleaved output components.
- Returning a proxy object rather than the specified result representation.

**Exclude / distinguish**

- No completed return in an unfinished implementation: C01.
- An incorrect numeric value alone: identify its mechanism instead.
- Domain encoding or parsing transformations: C10; output ordering alone: C11.

**Representative cases**

- Case 3: Places delimiters only at endpoints and drops the last original number.
- Case 234: Returns an inner function object rather than an encrypted string.
- Case 84: Interpolates position indices into an incomplete template instead of replacing every i with the odd-digit count.
- Case 494: Omits the trailing db marker and represents zero with no binary digit.

Supporting artifacts: **36**. Exact source excerpts and all supporting IDs are in `codebook.json`; per-artifact requirements, evidence and caveats are in `assignments.json`.

## C13 — Unhandled boundary or exceptional input

边界或异常输入处理缺失

A valid boundary case or an explicitly specified invalid-input case bypasses necessary handling, producing an exception or a result contrary to that case's contract.

**Include**

- Empty or all-filtered collections, zero-sized selection, zero/negative digit enumeration, equal operands.
- Insufficient resources requiring saturation, or malformed inputs for which the contract requires a Boolean/sentinel.
- A boundary guard that checks only the original collection rather than a derived empty collection.

**Exclude / distinguish**

- General indexing mistakes affecting ordinary traversal: C07.
- Wrong recurrence base states: C08.
- Do not assume a required behavior for inputs explicitly excluded by the task; record ambiguity where the domain is unclear.

**Representative cases**

- Case 111: For a zero-only list both filtered groups are empty, but min(positives) is still evaluated.
- Case 551: Selects the smallest k elements; at k=0 returns the original array instead of an empty result.
- Case 737: Consumes need even when stock is smaller, producing negative stock.
- Case 278: Parses malformed dates without guarding conversions or component count, ignores month-specific day limits, and invents a year>=1900 restriction.

Supporting artifacts: **20**. Exact source excerpts and all supporting IDs are in `codebook.json`; per-artifact requirements, evidence and caveats are in `assignments.json`.
