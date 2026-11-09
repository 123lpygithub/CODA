# CodeErrors / deepseek-2

Schema: `coda.artifact.v1`. Artifacts: **557**; codes: **28**; artifact–code assignments: **1228**.

This package uses the common seven-file format. All existing coding decisions, evidence and limitations are preserved. Additional source-specific fields are retained in `extensions`; original codebook text is retained in `codebook.json` metadata extensions and the local pre-conversion backup.

## Scope and method

逐条完整阅读冻结材料，记录逐篇 memo 与开放编码，归纳 codebook 后再逐条复核并指派 code；脚本仅做格式转换、重复复核裁定和机械一致性校验，不按关键词分类。

覆盖范围限于冻结材料中的文本；链接页面、附件和图片未读时明确保留限制。
单一 AI 编码；机械一致性检查不构成人工复核或独立双编码。
编码表示材料支持的主题或证据状态，不等于确认违规、缺陷已复现或修复已完成。

## Codes

| Code | Name | Artifacts |
|---|---|---:|
| CE01 | stub, placeholder, or no computed result | 103 |
| CE02 | missing return path or abandoned accumulator | 35 |
| CE03 | premature or first-match selection before full scan | 15 |
| CE04 | wrong task, substituted procedure, or spec read at wrong granularity | 201 |
| CE05 | required conjunct, predicate, filter, or transformation stage dropped | 137 |
| CE06 | wrong recursive structure, base, or termination | 22 |
| CE07 | undefined name, phantom helper, or missing import | 48 |
| CE08 | wrong tokenization, operand extraction, or unit of analysis | 30 |
| CE09 | presence vs multiplicity counting or wrong dedup rule | 38 |
| CE10 | wrong scan position, order, stride, direction, or index scope | 46 |
| CE11 | wrong sort key, direction, extremum, or selection representation | 32 |
| CE12 | wrong operator, formula, metric, or comparison operand in a branch | 63 |
| CE13 | hardcoded cases, literal parameters, fixed/fallback result, or overfit to examples | 35 |
| CE14 | missing or wrong boundary/edge guard or invented precondition | 59 |
| CE15 | wrong constant domain, character set, or case handling | 19 |
| CE16 | boundary comparison off at equality or seed value | 22 |
| CE17 | missing modular, sign, or rotation normalization | 14 |
| CE18 | missing secondary sort or tie-break rule | 10 |
| CE19 | violated stated constraint, efficiency rule, or unfaithful validation | 8 |
| CE20 | container/API contract runtime failure or ignored parameter | 17 |
| CE21 | inverted, tautological, or wrong-polarity condition | 47 |
| CE22 | type, conversion, or representational level confusion | 33 |
| CE23 | wrong return format, shape, or destructive input mutation | 48 |
| CE24 | missing word/neighbor boundary or single regex cannot express contract | 25 |
| CE25 | under-specified equality, wrong predicate rule, or one-sided predicate | 29 |
| CE26 | incomplete permutation/rotation coverage or unnormalized comparison | 8 |
| CE27 | docstring example or spec contradicts code | 78 |
| CE28 | no verifiable defect or implementation is correct | 6 |

## CE01 — stub, placeholder, or no computed result

Body produces no meaningful task computation: pass/TODO, docstring-only, unused/missing return, constant placeholder, tautological predicate, commented draft, or truncation.

- Include: pass/TODO; no return; constant 0/None/True; parameter never read; trimmed body.
- Exclude: Real computation with wrong value; hardcoded lookup answering some inputs; identity transform.
- Boundary/examples: Distinguish absence of computation from committed but wrong logic.
- Supporting artifacts: 103; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "1",
    "field": "incorrect_code",
    "quote": "    # TODO: Implement this function",
    "interpretation": "The entire function body is a TODO comment followed by multiple commented-out draft attempts; no executable computation remains, so calling the function yields None rather than a list of groups."
  }
]
````

## CE02 — missing return path or abandoned accumulator

Execution falls off the end, or an initialized result/counter/seed is never returned, or only a dead/partial branch returns, so required output is absent.

- Include: Body ends without return; only false branch returns; initialized notes discarded; seed never collected.
- Exclude: Explicit placeholder constant; wrong-shaped but returned value.
- Boundary/examples: Return exists somewhere but not reachable/complete for required value.
- Supporting artifacts: 35; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "4",
    "field": "incorrect_code",
    "quote": "# Use a list to keep track of the deepest level of",
    "interpretation": "The function is cut off mid-comment with no return path at all; execution would fall off the end and implicitly return None, so the required output list is absent. There is no reachable branch that returns any value."
  }
]
````

## CE03 — premature or first-match selection before full scan

A terminal return/index fires on first or local hit where extremal, last-occurrence, full-scan, or tie-aware selection is required; later candidates never examined.

- Include: return inside loop on local hit; sorted[1] for second smallest; branch returns x before testing larger y.
- Exclude: Correct first-match by spec; single candidate tested once.
- Boundary/examples: Selection semantics differ between extremal and first-match tasks.
- Supporting artifacts: 15; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "9",
    "field": "incorrect_code",
    "quote": "numbers.sort()",
    "interpretation": "By returning numbers[0] and numbers[-1] immediately after sorting, the code performs a local/first-and-last selection without scanning adjacent pairs to find the minimal difference. No candidate pairs are examined to establish which are closest, so the terminal selection fires before the needed full scan over adjacent differences."
  }
]
````

## CE04 — wrong task, substituted procedure, or spec read at wrong granularity

Coherent algorithm for a different task, substituted goal, or spec term read at wrong granularity/domain/composition, giving semantically unrelated output.

- Include: Primality vs triple-prime; bit-sum for digit-sum; character startswith where word required; set cardinality for window distinctness.
- Exclude: Correct shape with one wrong operator/constant; missing conjunct; placeholder.
- Boundary/examples: Whole goal or reading wrong, not one branch.
- Supporting artifacts: 201; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "2",
    "field": "incorrect_code",
    "quote": "    if operations[0] < 0:\n        return True",
    "interpretation": "The task requires tracking the running balance across all operations and detecting when the cumulative sum goes below zero, but the code instead checks whether any individual operation is negative. That is a different question (any withdrawal vs. running balance below zero)."
  }
]
````

## CE05 — required conjunct, predicate, filter, or transformation stage dropped

Correct skeleton omits a required scope predicate/conjunct, guard, parity/domain filter, or processing/reconstruction stage, silently solving a simpler or raw problem.

- Include: Sum without parity filter; dropped integer/positive guard; no sorted()/replace/sqrt; palindrome on raw s; frequency dict returned without max.
- Exclude: Whole algorithm substituted; one branch operator wrong; output shape only.
- Boundary/examples: Structure present; step or condition missing.
- Supporting artifacts: 137; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "2",
    "field": "incorrect_code",
    "quote": "    if operations[0] < 0:\n        return True",
    "interpretation": "The required accumulation/conjunct step—summing operations into a balance before comparing to zero—is dropped entirely; only the raw sign of the first element is examined, solving a simpler problem."
  }
]
````

## CE06 — wrong recursive structure, base, or termination

Recursive/iterative definition models wrong ordering/nesting, or base value, termination test, argument shrinking, or call direction is wrong, producing wrong results or nontermination.

- Include: Symmetric minima instead of alternating extremes; wrong empty termination; n+1 recursion; wrong-end shrink.
- Exclude: No recurrence attempted; iterative substitute; missing single branch.
- Boundary/examples: Recurrence skeleton exists; control/base is wrong.
- Supporting artifacts: 22; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "27",
    "field": "incorrect_code",
    "quote": "elif n % 2 == 0:\n        return modp(n // 2, p) ** 2 % p\n    else:\n        return (modp(n - 1, p) ** 2 * 2) % p",
    "interpretation": "The recursive decomposition is structurally present, but the odd-branch recursion reuses modp(n-1,p) and then squares it, which does not match the correct recurrence for exponentiation. This wrong recursion structure produces incorrect values."
  }
]
````

## CE07 — undefined name, phantom helper, or missing import

References a name/helper/module/data shape never defined or imported, or invents an API, guaranteeing NameError or fabricated-field failure independent of algorithm.

- Include: Undefined is_prime/find_palindrome_prefix; set.count(); reduce without functools; fabricated planets dict; invented nested offsets.
- Exclude: Resolved API with wrong semantics; helper defined elsewhere; unused local.
- Boundary/examples: Failure is resolution-time, not value-logic.
- Supporting artifacts: 48; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "5",
    "field": "incorrect_code",
    "quote": "palindrome_prefix = find_palindrome_prefix(string)",
    "interpretation": "The incorrect make_palindrome calls find_palindrome_prefix, a function that is never defined or imported anywhere in the artifact. This guarantees a NameError at runtime for any non-empty non-palindrome input, independent of algorithm correctness."
  }
]
````

## CE08 — wrong tokenization, operand extraction, or unit of analysis

Parses with wrong delimiter/type/index, splits on wrong composite boundary, or treats surface tokens where semantic entities are defined, so the unit of analysis is wrong before computation.

- Include: int() on word numbers; split('|') on spaces; literal ', ' failing bare commas; lexical sort of number words; '' join instead of ' '.
- Exclude: Correct tokens with wrong output delimiter; correct parse with wrong relation.
- Boundary/examples: Breakdown happens at parsing/segmentation.
- Supporting artifacts: 30; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "6",
    "field": "incorrect_code",
    "quote": "return [4 if x == 'o' else 2 if x == 'o|' else 1 for x in music_string.split('|')]",
    "interpretation": "The incorrect code splits the input on the pipe character '|', which is part of the note tokens themselves (e.g., 'o|', '.|'), rather than splitting on spaces as the token boundaries require. This produces fragments like 'o o', ' .', etc., so the unit of analysis is wrong before any mapping occurs."
  }
]
````

## CE09 — presence vs multiplicity counting or wrong dedup rule

Counts each item once where multiplicity matters, deduplicates by set where frequency-aware removal/singleton filtering required, or relies on non-overlapping str.count/set equality.

- Include: x in y where per-char count needed; list(set(..)) as answer; str.count non-overlap; set equality for multiset.
- Exclude: Distinct counting where distinct specified; correct frequency with off-by-one; delimiter errors.
- Boundary/examples: Question is how repeated items contribute.
- Supporting artifacts: 38; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "13",
    "field": "incorrect_code",
    "quote": "return list(set(numbers))",
    "interpretation": "The task requires removing all elements that occur more than once (multiplicity-aware), but the code deduplicates via a set, counting each item once and thus keeping duplicates while dropping order. The set operation ignores frequency entirely."
  }
]
````

## CE10 — wrong scan position, order, stride, direction, or index scope

Loop range, slice bound, start index, stride, or traversal direction is misaligned: first vs last, wrong span, overlapping skipped, positions not interleaved, or local window where prefix aggregate required.

- Include: range(len(xs)-1) loses last; i+=len(sub) skips overlaps; evens-then-odds extend; window at index 1.
- Exclude: Comparison strictness; missing modulo; correct scope wrong predicate.
- Boundary/examples: Where/how the scan walks is wrong.
- Supporting artifacts: 46; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "2",
    "field": "incorrect_code",
    "quote": "    return below_zero(operations[1:])",
    "interpretation": "By recursing with operations[1:] and testing only operations[0] as a sign, the scan never accumulates prior operations; the traversal discards the prefix aggregate that the running-balance check requires, examining only a local element at each step."
  }
]
````

## CE11 — wrong sort key, direction, extremum, or selection representation

Sorts/compares wrong collection, uses wrong key or fixed direction where condition-dependent, selects wrong extremum, or returns wrong representation of sorted data.

- Include: sorted(s.split()) sorts words; unconditional ascending where parity decides; min where max needed; sorts converted digits.
- Exclude: Correct sort with boundary bug; wrong membership/filter; off-by-one bounds.
- Boundary/examples: Ordering/selection semantics wrong, membership right.
- Supporting artifacts: 32; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "9",
    "field": "incorrect_code",
    "quote": "return (numbers[0], numbers[-1])",
    "interpretation": "The code selects the wrong extremum representation: it takes the first and last sorted elements (the extremes) where the task requires the pair with minimum adjacent difference. Ordering is computed correctly, but the selection of which elements to represent the answer is wrong."
  }
]
````

## CE12 — wrong operator, formula, metric, or comparison operand in a branch

Recognizable strategy mostly correct, but one branch operator/multiplier/formula or chosen quantity/operand is wrong, systematically breaking that case.

- Include: Odd-branch squaring gives 2n-1; a==b+c instead of sum; divisor init 1; length vs summed lengths; x%3 vs i%3.
- Exclude: Coherent different task; missing branch; comparison strictness only.
- Boundary/examples: Local arithmetic/quantity substitution in otherwise correct plan.
- Supporting artifacts: 63; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "11",
    "field": "incorrect_code",
    "quote": "while n % divisor != 0:",
    "interpretation": "The strategy direction is inverted: it increments divisor from 1 upward looking for the first divisor instead of returning n // i for the smallest divisor found, so it yields the smallest divisor (1) rather than the largest proper divisor."
  }
]
````

## CE13 — hardcoded cases, literal parameters, fixed/fallback result, or overfit to examples

Branches on small input set, reassigns parameters to literals, returns fixed/degenerate value, or matches a doctest/sample rather than the general rule, masking defects.

- Include: bases 2/8/16 with None fallback; lst=[0,3,2,1]; constant return matching False doctest; index-3 coincidence; nested hardcoded tables.
- Exclude: General loop with edge-case miss; legitimate small vocabulary dict; whole-body stub.
- Boundary/examples: Generalization replaced by enumeration or sample-fitting.
- Supporting artifacts: 35; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "25",
    "field": "incorrect_code",
    "quote": "if base == 2:\n        return bin(x)[2:]",
    "interpretation": "The implementation does not perform general base conversion. Instead it enumerates specific bases (2, 8, 16, 10) with hardcoded builtins and falls back to returning None for any other base. This is a hardcoded/fallback approach that masks the missing general algorithm."
  }
]
````

## CE14 — missing or wrong boundary/edge guard or invented precondition

Boundary input (empty, singleton, k==0, no letters, zero, a==b) lacks a branch/length guard causing crash or invalid result, or an unstated precondition rejects valid inputs.

- Include: No n==3; no empty guard before txt[-1]; n=1 treated prime; year>=1900 gate; equal-length precondition.
- Exclude: Guard present but operator wrong; quiet catch-all fallback; wrong core algorithm.
- Boundary/examples: Degenerate-input handling missing or over-restrictive.
- Supporting artifacts: 59; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "3",
    "field": "incorrect_code",
    "quote": ">>> intersperse([], 4)",
    "interpretation": "The empty-list boundary is mishandled: the expression always adds the delimiter at both ends regardless of input length, so intersperse([], 4) returns [4] instead of the required []. No guard exists for the empty or singleton case."
  }
]
````

## CE15 — wrong constant domain, character set, or case handling

Lookup/filter mechanism sound but embedded constant set is incomplete/misdefined, or handles only one case where both required, so required characters/inputs mishandled.

- Include: Vowel set 'aeiou' only; lowercase-only literals with uppercase doctest; wrong special member; A-Z shift only lowercase.
- Exclude: Wrong algorithm shape; correct constant with wrong operand; wrong formula secondary to case gap.
- Boundary/examples: Defect is contents of the set/table.
- Supporting artifacts: 19; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "28",
    "field": "incorrect_code",
    "quote": "vowels = 'aeiou'",
    "interpretation": "The filter mechanism is sound but the constant vowel set only includes lowercase 'aeiou', omitting uppercase 'AEIOU'. Uppercase vowels therefore pass through, breaking the 'aaBAA' example that requires apostrophe B only."
  }
]
````

## CE16 — boundary comparison off at equality or seed value

Relational guard uses wrong comparison at equality, or exact half-way/inclusive/singleton/tie/seed rule implemented via truncation or one-directional fallback.

- Include: >= vs > routing equality; int() truncation instead of rounding; strict x<y for singleton; fib4(1) returns 1 not 0.
- Exclude: Wholly missing guard; missing modulo; loop-bound off-by-one.
- Boundary/examples: Discrete equality/tie/seed boundary specifically.
- Supporting artifacts: 22; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "35",
    "field": "incorrect_code",
    "quote": "if shift >= len(s):\n        return s[::-1]",
    "interpretation": "The branch guard uses shift >= len(s) where the spec (and ground truth) use shift > len(s). When shift equals the digit length, the correct result is the unchanged string but the code takes the reverse branch, an equality-boundary comparison error in the guard."
  }
]
````

## CE17 — missing modular, sign, or rotation normalization

Raw shift/offset/sign used without required modulo, wraparound, or sign normalization, or residue constants misplaced, so cyclic/alphabet-boundary/negative inputs come out wrong.

- Include: Rotation lacks % len; ord('a') inside modulo; missing +26 before %; missing abs for negatives.
- Exclude: Wrong rotation direction with correct arithmetic; wrong character set; missing cast.
- Boundary/examples: Numeric normalization step wrong or omitted.
- Supporting artifacts: 14; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "35",
    "field": "incorrect_code",
    "quote": "return s[-shift:] + s[:-shift]",
    "interpretation": "The rotation uses raw shift indexing s[-shift:] + s[:-shift] without normalizing shift modulo the digit length, and the correct code adds 'shift %= len(s)'. Missing modular normalization is the mechanism, though here it manifests at the equality boundary."
  }
]
````

## CE18 — missing secondary sort or tie-break rule

Primary filtering/ordering correct, but specified secondary ordering (alphabetical among equal lengths) or index tie-break omitted; stable sort masks the omission.

- Include: key=len only where alphabetical tie-break required; no comparator; ties depend on input order.
- Exclude: Primary-order errors; reversed primary direction; absent whole sort.
- Boundary/examples: Primary correct; only tie-break absent.
- Supporting artifacts: 10; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "125",
    "field": "incorrect_code",
    "quote": "If two words have the same length, sort the list alphabetically.",
    "interpretation": "The code keeps only even-length words and sorts by length, but it omits the required alphabetical secondary tie-break among equal lengths. The spec explicitly requires alphabetical ordering for equal-length words, and sorted with key=len does not provide that."
  }
]
````

## CE19 — violated stated constraint, efficiency rule, or unfaithful validation

Violates explicit non-functional constraint/efficiency requirement, or validates format with unanchored/wrong-class pattern or missing length/count check, accepting malformed or rejecting valid input.

- Include: Self-recursion despite ban; exponential without memo; re.match without ^/$; no len(date)==10; no count before unpack.
- Exclude: Correct iterative solution; intentional fixed-domain table; over-strict invented precondition.
- Boundary/examples: Spec's stated constraint or validation fidelity violated.
- Supporting artifacts: 8; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "81",
    "field": "incorrect_code",
    "quote": "move_one_ball([3, 5, 4, 1, 2])==>False",
    "interpretation": "The docstring notes the list has unique elements and the task implies a finite check over N rotations, but the recursive implementation re-rotates indefinitely for unsorted arrays that never become sorted. For input [3,5,4,1,2], which must return False, the recursion never terminates, violating the implicit constraint of termination rather than iterating over the at most N distinct rotations."
  }
]
````

## CE20 — container/API contract runtime failure or ignored parameter

Assumes a container/API contract that fails at runtime (mask on list, most_common on array, sort on tuple, int on empty), or a capacity/state parameter is unused, shadowed, or rebound.

- Include: Boolean list as index; most_common on array; interval1.sort() on tuple; capacity never checked; comprehension shadows n; lambda param shadows target.
- Exclude: Undefined names; parameter used with wrong formula; harmless misleading names.
- Boundary/examples: Runtime contract break or logically inert binding.
- Supporting artifacts: 17; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "101",
    "field": "incorrect_code",
    "quote": "if dp[i][j] == dp[i - 1][j] + grid[i][j]:",
    "interpretation": "The code reads dp[i-1][j] and dp[i][j-1] at i=j=0 and at row 0 / column 0 where those indices wrap to negative or out-of-range positions, and it never bounds-checks; also `paths[i-1][j] + paths[i][j-1]` adds tuples, breaking the container contract at runtime."
  }
]
````

## CE21 — inverted, tautological, or wrong-polarity condition

Condition flipped, always true/false, imposes no constraint, tests complement/inverse of specified relation, or routes branches wrongly, yielding anti-correct behaviour.

- Include: Variable compared to itself; always-true modulo; identical if/else arms; x is y instead of x==y+z; i%3!=0; missing else.
- Exclude: Wrong threshold same side; missing condition entirely; wrong aggregate.
- Boundary/examples: Condition exists; polarity/logic is wrong.
- Supporting artifacts: 47; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "46",
    "field": "incorrect_code",
    "quote": "return a**(1/3) % 1 == 0",
    "interpretation": "The condition `a**(1/3) % 1 == 0` does not implement the cube check reliably; for negative inputs Python's fractional power of a negative number yields a complex number and `% 1` on complex raises, and for non-perfect cubes floating point gives wrong polarity. The predicate as constructed does not test integer-ness of a real cube root correctly."
  }
]
````

## CE22 — type, conversion, or representational level confusion

Operands/types/levels conflated or required casts omitted: strings used as numbers/chars, list vs scalar arithmetic, multi-char strings treated as single chars, numeric strings not normalized.

- Include: str with ^; missing int()/str(); recurrence over lists; '+' concatenation vs numeric; '-' in str int; char % 2.
- Exclude: Correct conversion with wrong API semantics; wrong metric alone; correct level wrong range.
- Boundary/examples: Conversion/level of the value wrong, not the operation.
- Supporting artifacts: 33; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "8",
    "field": "incorrect_code",
    "quote": "numbers = [int(i) for i in numbers]",
    "interpretation": "The implementation conflates the level of representation: the spec's values are words that must be mapped through a name-to-int dictionary, but the code treats the word strings as directly numeric. The required conversion between word and integer levels is wrong, causing a type/value confusion rather than a wrong ordering operator."
  }
]
````

## CE23 — wrong return format, shape, or destructive input mutation

Value computed but returned in wrong type/length/tuple packing/delimiter/scale, or function mutates/normalizes input destructively, losing order, case, sign, or multiplicity later needed.

- Include: List where int; swapped tuple slots; bin()[2:] drops '0b'; list.sort() on parameter; lower() before case swap; set() drops duplicates; abs() discards sign.
- Exclude: Missing return (falls off); wrong-valued but correctly shaped; mutation explicitly allowed.
- Boundary/examples: Output representation or input-integrity damaged after computation.
- Supporting artifacts: 48; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "49",
    "field": "incorrect_code",
    "quote": "        if len(s) == 3:\n            return True\n        else:\n            return False",
    "interpretation": "The output logic returns True solely when the set size equals 3, i.e., the result is derived from the wrong representation (set cardinality) of the input rather than window tests, so 'abcd' has set size 4 and returns False even though it should be True."
  }
]
````

## CE24 — missing word/neighbor boundary or single regex cannot express contract

Tests a single element where relation to neighbor/delimiter required (bare startswith, last char alone), or chosen control structure/single regex cannot represent per-side, tiered, nested conditions.

- Include: startswith('I') without space; only last char isalpha; never inspects neighbor; one regex for nesting depth; if/elif forcing single side.
- Exclude: Neighbor tested with wrong operator/direction; missing conjunct; correct regex for regular sub-property.
- Boundary/examples: Local-only test or inexpressible structure for contextual contract.
- Supporting artifacts: 25; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "61",
    "field": "incorrect_code",
    "quote": "return sum(1 for word in S.split() if word.startswith('I'))",
    "interpretation": "The implementation checks each whitespace-separated word with startswith('I') without verifying a sentence boundary or word boundary (the required 'I' at the start of a sentence followed by a space). A local-only test can match any word beginning with 'I', not only the first word of a sentence, so contextual neighbor/delimiter information is never inspected."
  }
]
````

## CE25 — under-specified equality, wrong predicate rule, or one-sided predicate

Tests weaker pairwise/per-item property instead of exact equality/global uniformity, or uses wrong parity/digit/bound predicate, so mixed or one-sided cases wrongly accepted/counted.

- Include: All-three-equal vs pairwise distinct; startswith vs exact 'I'; isalpha and not isalnum; count non-zero digits where odd required; both endpoints where only upper bound.
- Exclude: Missing neighborhood context; omitted conjunct; crash from empty indexing.
- Boundary/examples: Predicate present but too weak or wrong rule.
- Supporting artifacts: 29; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "33",
    "field": "incorrect_code",
    "quote": "if s[-1] in vowels:\n        count += 1",
    "interpretation": "The trailing-'y' rule is implemented with the wrong predicate: the code tests whether the last character is in 'aeiou' instead of testing for 'y'/'Y'. This is a predicate rule error (wrong character class for the special end-of-word vowel), not merely a missing conjunct."
  }
]
````

## CE26 — incomplete permutation/rotation coverage or unnormalized comparison

Checks only truncated subset of symmetric orientations (one rotation, one hypotenuse assignment, reversed args) or compares unnormalized operands, so other orientations or numeric-string inputs fail.

- Include: Hardcoded one-of-N ordering; missing permutation loop; a>b on comma-separated numeric strings.
- Exclude: Full permutations with wrong predicate; pure off-by-one; missing conjunct.
- Boundary/examples: Coverage of symmetric cases or normalization before compare.
- Supporting artifacts: 8; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "318",
    "field": "incorrect_code",
    "quote": "return abs(a - b) <= abs(c - a) <= abs(c - b)",
    "interpretation": "A correct solution would need to cover all three orientations (which side is the hypotenuse). The incorrect code never enumerates any orientation assignment and only compares differences, so no permutation/hypotenuse coverage exists at all, making all orientations fail."
  }
]
````

## CE27 — docstring example or spec contradicts code

Retained doctest/example or docstring is inconsistent with what code returns or raises, or spec internally inconsistent, showing examples not reconciled with implementation.

- Include: Code yields 24 where doctest says 288; stub with numeric-root doctest; non-negative claim with negative example.
- Exclude: Examples consistent but code overfits to them; examples absent; cosmetic scaffold.
- Boundary/examples: Explicit example text contradicts behavior.
- Supporting artifacts: 78; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "17",
    "field": "incorrect_code",
    "quote": ">>> round(find_zero([1, 2]), 2) # f(x) = 1 + 2x\n    -0.5",
    "interpretation": "The retained doctests specify concrete outputs (-0.5 and 1.0), but the implemented body performs meaningless sort/negate cycles and returns nothing, so the documented examples are irreconcilable with the actual behavior."
  }
]
````

## CE28 — no verifiable defect or implementation is correct

The incorrect implementation cannot be shown to be defective from the supplied material: it matches the ground truth in behaviour, the task itself is contradictory or under-specified, or the difference is only stylistic. Used only after comparing task, implementation and ground truth.

- Include: Behaviourally equivalent code; only cosmetic/comment differences; task statement contradicts its own examples so no implementation can satisfy it; defect cannot be attributed without execution that the material does not permit.
- Exclude: Any concrete wrong value, crash, missing step or violated constraint, even if it also differs cosmetically. Do not use merely because the mechanism is hard to name.
- Boundary/examples: Requires an explicit equivalence/contradiction argument; otherwise choose the most specific defect code that the evidence supports.
- Supporting artifacts: 6; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "111",
    "field": "incorrect_code",
    "quote": "if len(negatives) == 0:\n            return (None, min(positives))",
    "interpretation": "The incorrect implementation builds separate negative and positive lists, handles empties of each, and returns max(negatives)/min(positives) with None fallbacks. This matches the ground truth behavior for the examples and for arbitrary lists, including zero (ignored) and empty list. The logic is a different but behaviorally equivalent formulation of the same presentive filter/order operations. No concrete wrong value, crash, or missing step can be demonstrated."
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

# deepseek-2 — CodeErrors 最终编码本

本轮覆盖 **557 个 去重后的错误代码 artifact**，形成 **28 个可分配 code**，共记录 **1228 个 artifact–code assignment**。全部 557 个 artifact 均已编码，未决 0 个。允许在存在彼此独立证据时进行多重编码，因此类别覆盖数之和可以超过 artifact 数。

本 codebook 来自逐条完整阅读冻结材料、逐篇 memo、开放编码、持续比较和逐条 assignment 复核。关键词、正则、聚类和脚本没有用于决定类别；脚本只做格式转换、重复复核裁定和一致性校验。

## 范围与限制

- 覆盖范围是冻结材料中的全部文本；未读取的外链、附件和图片不作推断。
- 单一 AI 编码，未经人工审核，也不构成独立双编码。
- code 表示材料支持的主题、机制或证据状态，不等于确认违规、缺陷已复现或修复已完成。

## 类别一览

| Code | 名称 | Artifacts |
|---|---|---:|
| CE01 | stub, placeholder, or no computed result | 103 |
| CE02 | missing return path or abandoned accumulator | 35 |
| CE03 | premature or first-match selection before full scan | 15 |
| CE04 | wrong task, substituted procedure, or spec read at wrong granularity | 201 |
| CE05 | required conjunct, predicate, filter, or transformation stage dropped | 137 |
| CE06 | wrong recursive structure, base, or termination | 22 |
| CE07 | undefined name, phantom helper, or missing import | 48 |
| CE08 | wrong tokenization, operand extraction, or unit of analysis | 30 |
| CE09 | presence vs multiplicity counting or wrong dedup rule | 38 |
| CE10 | wrong scan position, order, stride, direction, or index scope | 46 |
| CE11 | wrong sort key, direction, extremum, or selection representation | 32 |
| CE12 | wrong operator, formula, metric, or comparison operand in a branch | 63 |
| CE13 | hardcoded cases, literal parameters, fixed/fallback result, or overfit to examples | 35 |
| CE14 | missing or wrong boundary/edge guard or invented precondition | 59 |
| CE15 | wrong constant domain, character set, or case handling | 19 |
| CE16 | boundary comparison off at equality or seed value | 22 |
| CE17 | missing modular, sign, or rotation normalization | 14 |
| CE18 | missing secondary sort or tie-break rule | 10 |
| CE19 | violated stated constraint, efficiency rule, or unfaithful validation | 8 |
| CE20 | container/API contract runtime failure or ignored parameter | 17 |
| CE21 | inverted, tautological, or wrong-polarity condition | 47 |
| CE22 | type, conversion, or representational level confusion | 33 |
| CE23 | wrong return format, shape, or destructive input mutation | 48 |
| CE24 | missing word/neighbor boundary or single regex cannot express contract | 25 |
| CE25 | under-specified equality, wrong predicate rule, or one-sided predicate | 29 |
| CE26 | incomplete permutation/rotation coverage or unnormalized comparison | 8 |
| CE27 | docstring example or spec contradicts code | 78 |
| CE28 | no verifiable defect or implementation is correct | 6 |

## 使用规则

- 以交付代码中的可观察失败机制为单位，不推断模型的心理原因。
- 优先选择能准确解释证据的具体 code；一个缺陷不同时归到泛化类别与具体类别。
- 只有存在不同证据支持的不同缺陷时才多重编码。
- 题目约束优先；参考实现用于理解而非要求相同算法。

## CE01 — stub, placeholder, or no computed result

Body produces no meaningful task computation: pass/TODO, docstring-only, unused/missing return, constant placeholder, tautological predicate, commented draft, or truncation.

**Include:** pass/TODO; no return; constant 0/None/True; parameter never read; trimmed body.

**Exclude:** Real computation with wrong value; hardcoded lookup answering some inputs; identity transform.

**Support:** 103 artifact(s). 完整列表见 `codebook.json`。

**Boundary:** Distinguish absence of computation from committed but wrong logic.

**Example:** `1` — The entire function body is a TODO comment followed by multiple commented-out draft attempts; no executable computation remains, so calling the function yields None rather than a list of groups.

````text
    # TODO: Implement this function
````


## CE02 — missing return path or abandoned accumulator

Execution falls off the end, or an initialized result/counter/seed is never returned, or only a dead/partial branch returns, so required output is absent.

**Include:** Body ends without return; only false branch returns; initialized notes discarded; seed never collected.

**Exclude:** Explicit placeholder constant; wrong-shaped but returned value.

**Support:** 35 artifact(s). 完整列表见 `codebook.json`。

**Boundary:** Return exists somewhere but not reachable/complete for required value.

**Example:** `4` — The function is cut off mid-comment with no return path at all; execution would fall off the end and implicitly return None, so the required output list is absent. There is no reachable branch that returns any value.

````text
# Use a list to keep track of the deepest level of
````


## CE03 — premature or first-match selection before full scan

A terminal return/index fires on first or local hit where extremal, last-occurrence, full-scan, or tie-aware selection is required; later candidates never examined.

**Include:** return inside loop on local hit; sorted[1] for second smallest; branch returns x before testing larger y.

**Exclude:** Correct first-match by spec; single candidate tested once.

**Support:** 15 artifact(s). 完整列表见 `codebook.json`。

**Boundary:** Selection semantics differ between extremal and first-match tasks.

**Example:** `9` — By returning numbers[0] and numbers[-1] immediately after sorting, the code performs a local/first-and-last selection without scanning adjacent pairs to find the minimal difference. No candidate pairs are examined to establish which are closest, so the terminal selection fires before the needed full scan over adjacent differences.

````text
numbers.sort()
````


## CE04 — wrong task, substituted procedure, or spec read at wrong granularity

Coherent algorithm for a different task, substituted goal, or spec term read at wrong granularity/domain/composition, giving semantically unrelated output.

**Include:** Primality vs triple-prime; bit-sum for digit-sum; character startswith where word required; set cardinality for window distinctness.

**Exclude:** Correct shape with one wrong operator/constant; missing conjunct; placeholder.

**Support:** 201 artifact(s). 完整列表见 `codebook.json`。

**Boundary:** Whole goal or reading wrong, not one branch.

**Example:** `2` — The task requires tracking the running balance across all operations and detecting when the cumulative sum goes below zero, but the code instead checks whether any individual operation is negative. That is a different question (any withdrawal vs. running balance below zero).

````text
    if operations[0] < 0:
        return True
````


## CE05 — required conjunct, predicate, filter, or transformation stage dropped

Correct skeleton omits a required scope predicate/conjunct, guard, parity/domain filter, or processing/reconstruction stage, silently solving a simpler or raw problem.

**Include:** Sum without parity filter; dropped integer/positive guard; no sorted()/replace/sqrt; palindrome on raw s; frequency dict returned without max.

**Exclude:** Whole algorithm substituted; one branch operator wrong; output shape only.

**Support:** 137 artifact(s). 完整列表见 `codebook.json`。

**Boundary:** Structure present; step or condition missing.

**Example:** `2` — The required accumulation/conjunct step—summing operations into a balance before comparing to zero—is dropped entirely; only the raw sign of the first element is examined, solving a simpler problem.

````text
    if operations[0] < 0:
        return True
````


## CE06 — wrong recursive structure, base, or termination

Recursive/iterative definition models wrong ordering/nesting, or base value, termination test, argument shrinking, or call direction is wrong, producing wrong results or nontermination.

**Include:** Symmetric minima instead of alternating extremes; wrong empty termination; n+1 recursion; wrong-end shrink.

**Exclude:** No recurrence attempted; iterative substitute; missing single branch.

**Support:** 22 artifact(s). 完整列表见 `codebook.json`。

**Boundary:** Recurrence skeleton exists; control/base is wrong.

**Example:** `27` — The recursive decomposition is structurally present, but the odd-branch recursion reuses modp(n-1,p) and then squares it, which does not match the correct recurrence for exponentiation. This wrong recursion structure produces incorrect values.

````text
elif n % 2 == 0:
        return modp(n // 2, p) ** 2 % p
    else:
        return (modp(n - 1, p) ** 2 * 2) % p
````


## CE07 — undefined name, phantom helper, or missing import

References a name/helper/module/data shape never defined or imported, or invents an API, guaranteeing NameError or fabricated-field failure independent of algorithm.

**Include:** Undefined is_prime/find_palindrome_prefix; set.count(); reduce without functools; fabricated planets dict; invented nested offsets.

**Exclude:** Resolved API with wrong semantics; helper defined elsewhere; unused local.

**Support:** 48 artifact(s). 完整列表见 `codebook.json`。

**Boundary:** Failure is resolution-time, not value-logic.

**Example:** `5` — The incorrect make_palindrome calls find_palindrome_prefix, a function that is never defined or imported anywhere in the artifact. This guarantees a NameError at runtime for any non-empty non-palindrome input, independent of algorithm correctness.

````text
palindrome_prefix = find_palindrome_prefix(string)
````


## CE08 — wrong tokenization, operand extraction, or unit of analysis

Parses with wrong delimiter/type/index, splits on wrong composite boundary, or treats surface tokens where semantic entities are defined, so the unit of analysis is wrong before computation.

**Include:** int() on word numbers; split('|') on spaces; literal ', ' failing bare commas; lexical sort of number words; '' join instead of ' '.

**Exclude:** Correct tokens with wrong output delimiter; correct parse with wrong relation.

**Support:** 30 artifact(s). 完整列表见 `codebook.json`。

**Boundary:** Breakdown happens at parsing/segmentation.

**Example:** `6` — The incorrect code splits the input on the pipe character '|', which is part of the note tokens themselves (e.g., 'o|', '.|'), rather than splitting on spaces as the token boundaries require. This produces fragments like 'o o', ' .', etc., so the unit of analysis is wrong before any mapping occurs.

````text
return [4 if x == 'o' else 2 if x == 'o|' else 1 for x in music_string.split('|')]
````


## CE09 — presence vs multiplicity counting or wrong dedup rule

Counts each item once where multiplicity matters, deduplicates by set where frequency-aware removal/singleton filtering required, or relies on non-overlapping str.count/set equality.

**Include:** x in y where per-char count needed; list(set(..)) as answer; str.count non-overlap; set equality for multiset.

**Exclude:** Distinct counting where distinct specified; correct frequency with off-by-one; delimiter errors.

**Support:** 38 artifact(s). 完整列表见 `codebook.json`。

**Boundary:** Question is how repeated items contribute.

**Example:** `13` — The task requires removing all elements that occur more than once (multiplicity-aware), but the code deduplicates via a set, counting each item once and thus keeping duplicates while dropping order. The set operation ignores frequency entirely.

````text
return list(set(numbers))
````


## CE10 — wrong scan position, order, stride, direction, or index scope

Loop range, slice bound, start index, stride, or traversal direction is misaligned: first vs last, wrong span, overlapping skipped, positions not interleaved, or local window where prefix aggregate required.

**Include:** range(len(xs)-1) loses last; i+=len(sub) skips overlaps; evens-then-odds extend; window at index 1.

**Exclude:** Comparison strictness; missing modulo; correct scope wrong predicate.

**Support:** 46 artifact(s). 完整列表见 `codebook.json`。

**Boundary:** Where/how the scan walks is wrong.

**Example:** `2` — By recursing with operations[1:] and testing only operations[0] as a sign, the scan never accumulates prior operations; the traversal discards the prefix aggregate that the running-balance check requires, examining only a local element at each step.

````text
    return below_zero(operations[1:])
````


## CE11 — wrong sort key, direction, extremum, or selection representation

Sorts/compares wrong collection, uses wrong key or fixed direction where condition-dependent, selects wrong extremum, or returns wrong representation of sorted data.

**Include:** sorted(s.split()) sorts words; unconditional ascending where parity decides; min where max needed; sorts converted digits.

**Exclude:** Correct sort with boundary bug; wrong membership/filter; off-by-one bounds.

**Support:** 32 artifact(s). 完整列表见 `codebook.json`。

**Boundary:** Ordering/selection semantics wrong, membership right.

**Example:** `9` — The code selects the wrong extremum representation: it takes the first and last sorted elements (the extremes) where the task requires the pair with minimum adjacent difference. Ordering is computed correctly, but the selection of which elements to represent the answer is wrong.

````text
return (numbers[0], numbers[-1])
````


## CE12 — wrong operator, formula, metric, or comparison operand in a branch

Recognizable strategy mostly correct, but one branch operator/multiplier/formula or chosen quantity/operand is wrong, systematically breaking that case.

**Include:** Odd-branch squaring gives 2n-1; a==b+c instead of sum; divisor init 1; length vs summed lengths; x%3 vs i%3.

**Exclude:** Coherent different task; missing branch; comparison strictness only.

**Support:** 63 artifact(s). 完整列表见 `codebook.json`。

**Boundary:** Local arithmetic/quantity substitution in otherwise correct plan.

**Example:** `11` — The strategy direction is inverted: it increments divisor from 1 upward looking for the first divisor instead of returning n // i for the smallest divisor found, so it yields the smallest divisor (1) rather than the largest proper divisor.

````text
while n % divisor != 0:
````


## CE13 — hardcoded cases, literal parameters, fixed/fallback result, or overfit to examples

Branches on small input set, reassigns parameters to literals, returns fixed/degenerate value, or matches a doctest/sample rather than the general rule, masking defects.

**Include:** bases 2/8/16 with None fallback; lst=[0,3,2,1]; constant return matching False doctest; index-3 coincidence; nested hardcoded tables.

**Exclude:** General loop with edge-case miss; legitimate small vocabulary dict; whole-body stub.

**Support:** 35 artifact(s). 完整列表见 `codebook.json`。

**Boundary:** Generalization replaced by enumeration or sample-fitting.

**Example:** `25` — The implementation does not perform general base conversion. Instead it enumerates specific bases (2, 8, 16, 10) with hardcoded builtins and falls back to returning None for any other base. This is a hardcoded/fallback approach that masks the missing general algorithm.

````text
if base == 2:
        return bin(x)[2:]
````


## CE14 — missing or wrong boundary/edge guard or invented precondition

Boundary input (empty, singleton, k==0, no letters, zero, a==b) lacks a branch/length guard causing crash or invalid result, or an unstated precondition rejects valid inputs.

**Include:** No n==3; no empty guard before txt[-1]; n=1 treated prime; year>=1900 gate; equal-length precondition.

**Exclude:** Guard present but operator wrong; quiet catch-all fallback; wrong core algorithm.

**Support:** 59 artifact(s). 完整列表见 `codebook.json`。

**Boundary:** Degenerate-input handling missing or over-restrictive.

**Example:** `3` — The empty-list boundary is mishandled: the expression always adds the delimiter at both ends regardless of input length, so intersperse([], 4) returns [4] instead of the required []. No guard exists for the empty or singleton case.

````text
>>> intersperse([], 4)
````


## CE15 — wrong constant domain, character set, or case handling

Lookup/filter mechanism sound but embedded constant set is incomplete/misdefined, or handles only one case where both required, so required characters/inputs mishandled.

**Include:** Vowel set 'aeiou' only; lowercase-only literals with uppercase doctest; wrong special member; A-Z shift only lowercase.

**Exclude:** Wrong algorithm shape; correct constant with wrong operand; wrong formula secondary to case gap.

**Support:** 19 artifact(s). 完整列表见 `codebook.json`。

**Boundary:** Defect is contents of the set/table.

**Example:** `28` — The filter mechanism is sound but the constant vowel set only includes lowercase 'aeiou', omitting uppercase 'AEIOU'. Uppercase vowels therefore pass through, breaking the 'aaBAA' example that requires apostrophe B only.

````text
vowels = 'aeiou'
````


## CE16 — boundary comparison off at equality or seed value

Relational guard uses wrong comparison at equality, or exact half-way/inclusive/singleton/tie/seed rule implemented via truncation or one-directional fallback.

**Include:** >= vs > routing equality; int() truncation instead of rounding; strict x<y for singleton; fib4(1) returns 1 not 0.

**Exclude:** Wholly missing guard; missing modulo; loop-bound off-by-one.

**Support:** 22 artifact(s). 完整列表见 `codebook.json`。

**Boundary:** Discrete equality/tie/seed boundary specifically.

**Example:** `35` — The branch guard uses shift >= len(s) where the spec (and ground truth) use shift > len(s). When shift equals the digit length, the correct result is the unchanged string but the code takes the reverse branch, an equality-boundary comparison error in the guard.

````text
if shift >= len(s):
        return s[::-1]
````


## CE17 — missing modular, sign, or rotation normalization

Raw shift/offset/sign used without required modulo, wraparound, or sign normalization, or residue constants misplaced, so cyclic/alphabet-boundary/negative inputs come out wrong.

**Include:** Rotation lacks % len; ord('a') inside modulo; missing +26 before %; missing abs for negatives.

**Exclude:** Wrong rotation direction with correct arithmetic; wrong character set; missing cast.

**Support:** 14 artifact(s). 完整列表见 `codebook.json`。

**Boundary:** Numeric normalization step wrong or omitted.

**Example:** `35` — The rotation uses raw shift indexing s[-shift:] + s[:-shift] without normalizing shift modulo the digit length, and the correct code adds 'shift %= len(s)'. Missing modular normalization is the mechanism, though here it manifests at the equality boundary.

````text
return s[-shift:] + s[:-shift]
````


## CE18 — missing secondary sort or tie-break rule

Primary filtering/ordering correct, but specified secondary ordering (alphabetical among equal lengths) or index tie-break omitted; stable sort masks the omission.

**Include:** key=len only where alphabetical tie-break required; no comparator; ties depend on input order.

**Exclude:** Primary-order errors; reversed primary direction; absent whole sort.

**Support:** 10 artifact(s). 完整列表见 `codebook.json`。

**Boundary:** Primary correct; only tie-break absent.

**Example:** `125` — The code keeps only even-length words and sorts by length, but it omits the required alphabetical secondary tie-break among equal lengths. The spec explicitly requires alphabetical ordering for equal-length words, and sorted with key=len does not provide that.

````text
If two words have the same length, sort the list alphabetically.
````


## CE19 — violated stated constraint, efficiency rule, or unfaithful validation

Violates explicit non-functional constraint/efficiency requirement, or validates format with unanchored/wrong-class pattern or missing length/count check, accepting malformed or rejecting valid input.

**Include:** Self-recursion despite ban; exponential without memo; re.match without ^/$; no len(date)==10; no count before unpack.

**Exclude:** Correct iterative solution; intentional fixed-domain table; over-strict invented precondition.

**Support:** 8 artifact(s). 完整列表见 `codebook.json`。

**Boundary:** Spec's stated constraint or validation fidelity violated.

**Example:** `81` — The docstring notes the list has unique elements and the task implies a finite check over N rotations, but the recursive implementation re-rotates indefinitely for unsorted arrays that never become sorted. For input [3,5,4,1,2], which must return False, the recursion never terminates, violating the implicit constraint of termination rather than iterating over the at most N distinct rotations.

````text
move_one_ball([3, 5, 4, 1, 2])==>False
````


## CE20 — container/API contract runtime failure or ignored parameter

Assumes a container/API contract that fails at runtime (mask on list, most_common on array, sort on tuple, int on empty), or a capacity/state parameter is unused, shadowed, or rebound.

**Include:** Boolean list as index; most_common on array; interval1.sort() on tuple; capacity never checked; comprehension shadows n; lambda param shadows target.

**Exclude:** Undefined names; parameter used with wrong formula; harmless misleading names.

**Support:** 17 artifact(s). 完整列表见 `codebook.json`。

**Boundary:** Runtime contract break or logically inert binding.

**Example:** `101` — The code reads dp[i-1][j] and dp[i][j-1] at i=j=0 and at row 0 / column 0 where those indices wrap to negative or out-of-range positions, and it never bounds-checks; also `paths[i-1][j] + paths[i][j-1]` adds tuples, breaking the container contract at runtime.

````text
if dp[i][j] == dp[i - 1][j] + grid[i][j]:
````


## CE21 — inverted, tautological, or wrong-polarity condition

Condition flipped, always true/false, imposes no constraint, tests complement/inverse of specified relation, or routes branches wrongly, yielding anti-correct behaviour.

**Include:** Variable compared to itself; always-true modulo; identical if/else arms; x is y instead of x==y+z; i%3!=0; missing else.

**Exclude:** Wrong threshold same side; missing condition entirely; wrong aggregate.

**Support:** 47 artifact(s). 完整列表见 `codebook.json`。

**Boundary:** Condition exists; polarity/logic is wrong.

**Example:** `46` — The condition `a**(1/3) % 1 == 0` does not implement the cube check reliably; for negative inputs Python's fractional power of a negative number yields a complex number and `% 1` on complex raises, and for non-perfect cubes floating point gives wrong polarity. The predicate as constructed does not test integer-ness of a real cube root correctly.

````text
return a**(1/3) % 1 == 0
````


## CE22 — type, conversion, or representational level confusion

Operands/types/levels conflated or required casts omitted: strings used as numbers/chars, list vs scalar arithmetic, multi-char strings treated as single chars, numeric strings not normalized.

**Include:** str with ^; missing int()/str(); recurrence over lists; '+' concatenation vs numeric; '-' in str int; char % 2.

**Exclude:** Correct conversion with wrong API semantics; wrong metric alone; correct level wrong range.

**Support:** 33 artifact(s). 完整列表见 `codebook.json`。

**Boundary:** Conversion/level of the value wrong, not the operation.

**Example:** `8` — The implementation conflates the level of representation: the spec's values are words that must be mapped through a name-to-int dictionary, but the code treats the word strings as directly numeric. The required conversion between word and integer levels is wrong, causing a type/value confusion rather than a wrong ordering operator.

````text
numbers = [int(i) for i in numbers]
````


## CE23 — wrong return format, shape, or destructive input mutation

Value computed but returned in wrong type/length/tuple packing/delimiter/scale, or function mutates/normalizes input destructively, losing order, case, sign, or multiplicity later needed.

**Include:** List where int; swapped tuple slots; bin()[2:] drops '0b'; list.sort() on parameter; lower() before case swap; set() drops duplicates; abs() discards sign.

**Exclude:** Missing return (falls off); wrong-valued but correctly shaped; mutation explicitly allowed.

**Support:** 48 artifact(s). 完整列表见 `codebook.json`。

**Boundary:** Output representation or input-integrity damaged after computation.

**Example:** `49` — The output logic returns True solely when the set size equals 3, i.e., the result is derived from the wrong representation (set cardinality) of the input rather than window tests, so 'abcd' has set size 4 and returns False even though it should be True.

````text
        if len(s) == 3:
            return True
        else:
            return False
````


## CE24 — missing word/neighbor boundary or single regex cannot express contract

Tests a single element where relation to neighbor/delimiter required (bare startswith, last char alone), or chosen control structure/single regex cannot represent per-side, tiered, nested conditions.

**Include:** startswith('I') without space; only last char isalpha; never inspects neighbor; one regex for nesting depth; if/elif forcing single side.

**Exclude:** Neighbor tested with wrong operator/direction; missing conjunct; correct regex for regular sub-property.

**Support:** 25 artifact(s). 完整列表见 `codebook.json`。

**Boundary:** Local-only test or inexpressible structure for contextual contract.

**Example:** `61` — The implementation checks each whitespace-separated word with startswith('I') without verifying a sentence boundary or word boundary (the required 'I' at the start of a sentence followed by a space). A local-only test can match any word beginning with 'I', not only the first word of a sentence, so contextual neighbor/delimiter information is never inspected.

````text
return sum(1 for word in S.split() if word.startswith('I'))
````


## CE25 — under-specified equality, wrong predicate rule, or one-sided predicate

Tests weaker pairwise/per-item property instead of exact equality/global uniformity, or uses wrong parity/digit/bound predicate, so mixed or one-sided cases wrongly accepted/counted.

**Include:** All-three-equal vs pairwise distinct; startswith vs exact 'I'; isalpha and not isalnum; count non-zero digits where odd required; both endpoints where only upper bound.

**Exclude:** Missing neighborhood context; omitted conjunct; crash from empty indexing.

**Support:** 29 artifact(s). 完整列表见 `codebook.json`。

**Boundary:** Predicate present but too weak or wrong rule.

**Example:** `33` — The trailing-'y' rule is implemented with the wrong predicate: the code tests whether the last character is in 'aeiou' instead of testing for 'y'/'Y'. This is a predicate rule error (wrong character class for the special end-of-word vowel), not merely a missing conjunct.

````text
if s[-1] in vowels:
        count += 1
````


## CE26 — incomplete permutation/rotation coverage or unnormalized comparison

Checks only truncated subset of symmetric orientations (one rotation, one hypotenuse assignment, reversed args) or compares unnormalized operands, so other orientations or numeric-string inputs fail.

**Include:** Hardcoded one-of-N ordering; missing permutation loop; a>b on comma-separated numeric strings.

**Exclude:** Full permutations with wrong predicate; pure off-by-one; missing conjunct.

**Support:** 8 artifact(s). 完整列表见 `codebook.json`。

**Boundary:** Coverage of symmetric cases or normalization before compare.

**Example:** `318` — A correct solution would need to cover all three orientations (which side is the hypotenuse). The incorrect code never enumerates any orientation assignment and only compares differences, so no permutation/hypotenuse coverage exists at all, making all orientations fail.

````text
return abs(a - b) <= abs(c - a) <= abs(c - b)
````


## CE27 — docstring example or spec contradicts code

Retained doctest/example or docstring is inconsistent with what code returns or raises, or spec internally inconsistent, showing examples not reconciled with implementation.

**Include:** Code yields 24 where doctest says 288; stub with numeric-root doctest; non-negative claim with negative example.

**Exclude:** Examples consistent but code overfits to them; examples absent; cosmetic scaffold.

**Support:** 78 artifact(s). 完整列表见 `codebook.json`。

**Boundary:** Explicit example text contradicts behavior.

**Example:** `17` — The retained doctests specify concrete outputs (-0.5 and 1.0), but the implemented body performs meaningless sort/negate cycles and returns nothing, so the documented examples are irreconcilable with the actual behavior.

````text
>>> round(find_zero([1, 2]), 2) # f(x) = 1 + 2x
    -0.5
````


## CE28 — no verifiable defect or implementation is correct

The incorrect implementation cannot be shown to be defective from the supplied material: it matches the ground truth in behaviour, the task itself is contradictory or under-specified, or the difference is only stylistic. Used only after comparing task, implementation and ground truth.

**Include:** Behaviourally equivalent code; only cosmetic/comment differences; task statement contradicts its own examples so no implementation can satisfy it; defect cannot be attributed without execution that the material does not permit.

**Exclude:** Any concrete wrong value, crash, missing step or violated constraint, even if it also differs cosmetically. Do not use merely because the mechanism is hard to name.

**Support:** 6 artifact(s). 完整列表见 `codebook.json`。

**Boundary:** Requires an explicit equivalence/contradiction argument; otherwise choose the most specific defect code that the evidence supports.

**Example:** `111` — The incorrect implementation builds separate negative and positive lists, handles empties of each, and returns max(negatives)/min(positives) with None fallbacks. This matches the ground truth behavior for the examples and for arbitrary lists, including zero (ignored) and empty list. The logic is a different but behaviorally equivalent formulation of the same presentive filter/order operations. No concrete wrong value, crash, or missing step can be demonstrated.

````text
if len(negatives) == 0:
            return (None, min(positives))
````

## 配套文件

- `codebook.json`：结构化定义、支持案例、计数、代表证据和方法元数据。
- `codebook.csv`：表格化 codebook。
- `assignments.json` / `assignments.csv`：每个 artifact 的 code、理由、逐字证据、来源与证据限制。
- `taxonomy.json`：HOW-style 类别树。
- `results.json`：冻结材料正文与最终编码的逐条组合。
