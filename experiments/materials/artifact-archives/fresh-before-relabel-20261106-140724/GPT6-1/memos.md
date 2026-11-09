# Consolidation and boundary memos

## From observations to codes

The analysis recorded 557 artifact observations (468 grouped observation rows where several artifacts support the same interpretation), then manually mapped every artifact to the consolidated definitions. Categories were not generated from label keywords, task names, published human categories, or the earlier codebook. Thirteen reusable mechanisms were retained after comparing task-specific observations. No target category count or maximum was imposed. The flat taxonomy avoids adding organizational parent labels that would be mistaken for additional coding decisions.

## Consolidations

- Pass bodies, constant placeholders, truncated generation and repeated unfinished statements share the absence of a completed task-solving path (C01). Their different manifestations remain in case rationales rather than becoming separate task-specific categories.
- Undefined helpers, missing imports and out-of-scope local names share a missing binding (C02). This differs from calling a nonexistent method on an available object (C03).
- Confusing words with characters, numbers with digits, indices with values, or whole-corpus totals with per-group calculations changes the computational target or unit (C04). An ordinary factorial substituted for a product of factorials is also a target substitution.
- Rounding conventions, omitted factors, square roots and algebraic precedence belong to arithmetic treatment (C09). Character shifts, delimiters, signed-digit interpretation and numeral systems belong to representation and transformation (C10).
- Ordering direction, primary and secondary sort keys, tie-breaking and selection priorities share C11. No separate category is introduced for each sorting task.

## Avoiding redundant labels

C05 is not a generic label attached to every defect: it applies when a recognizable implementation lacks a distinct requirement. Missing tie-breaking is only C11; missing case normalization is only C10; a missing empty-input guard is only C13. A wrong existing predicate is C06. Wrong visitation or index bounds are C07. Wrong recurrence state is C08. Multiple labels denote separate observations, not both a parent and a child description of the same defect.

For example, case 151 has an output guard tied to the number of new maxima rather than the required per-position output (C06), plus a separate zero seed that invalidates negative maxima (C08). The output omission is not additionally coded as C05 or C12. Case 359 rounds a pooled water total instead of separate wells (C04); the use of ceiling itself is valid, so it is not additionally C09. Case 531 compares string members with integer members (C10) and separately removes duplicates (C12).

## Execution and source scope

The artifact includes the generated source, canonical task text and supplied reference. Generated code is never repaired before diagnostic execution, and no imports are injected. A missing dependency therefore means absent from the supplied standalone context; the original generation/test harness may have had other context that is not provided here. Truncation is a property of the supplied artifact, without attributing its cause to the generator or data extraction. Python parsing is checked for all 557 sources; 26 do not parse, all assigned C01.

An exception can mask a later defect. Local semantic observations behind that exception remain static findings; they are not represented as multiple observed runtime failures. This distinction applies, for example, to case 368's missing heapq binding and separately visible path-selection logic.

## Focused difficult cases

- **393:** The canonical task field supplies only the polynomial helper, while the generated source also contains the root-finding requirements. On coefficients `[100, 1]`, the unchanged program returns approximately `99.99999925494194` although the root is `-100`. Its strict sign test discards a root already at the left endpoint. This directly supports C06. C09 separately records that interval-width termination does not in general guarantee a small polynomial residual; that second observation is static.
- **729:** The task says to sort by length then alphabetically, but also says all words have the same length. The supplied examples and reference permit different lengths. Under the length-first interpretation, `['zz', 'aaaa']` should remain in that order; the program reverses it. Under equal-length inputs, lexical sorting suffices, as the diagnostic `['zz', 'aa']` confirms. The artifact receives C11 with status `coded_conditional_on_specification`. It is included in coverage, but is not an unconditionally proven bug. This preserves all-artifact coding without inventing evidence.
- **357:** The generated docstring changes example outputs. The canonical task text and reference require every letter `i` in the template to be replaced. The C12 interpretation follows the canonical contract, and records the embedded-documentation conflict.
- **547:** Examples conflict with bit-count ordering, but the prose explicitly requires a numeric tie-break. Input `[2, 1]` independently exposes the missing tie-break without relying on a disputed example.
- **188:** The positive example `(8, 3)` demonstrates true division corrupting digit extraction. Its zero-input empty result is separately scoped to ordinary positional notation; reference behavior is not assumed to establish correctness on every boundary input.

## Evidence and interpretation limits

Thirty diagnostic inputs cover 26 selected artifacts. They are not an official test suite or a random sample for estimating accuracy. All 557 programs were analyzed statically; not all were dynamically tested. Assertions in the export audit establish coverage, consistent IDs, evidence quotation accuracy and schema integrity. They do not establish that every interpretation is correct. The current conversation contains prior information, so this is not a blinded independent replication and no inter-coder agreement is claimed. Human code categories were excluded from the analysis input. The GPT6-1 directory is a result label, not verification of an API model name.
