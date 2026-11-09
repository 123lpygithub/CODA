# Privacy consolidation decisions

The case-specific observations were consolidated into 18 categories after reading the supplied corpus. `consolidation.py` records every index-to-code choice explicitly; it does not infer categories from text. The number 18 was an outcome of consolidation, not a preset ceiling.

## Merges and retained distinctions

- Cookie, policy, localization and disclosure issues share P01 when they concern what people are told. P02 concerns making and retaining a decision; P03 concerns whether processing honors it. This preserves a distinction between a visible notice, a saved choice and an effective control.
- Telemetry participation and default-policy debates share P04. Specific data leaks in diagnostics belong to P08, and a demonstrated opt-out bypass can also receive P03.
- External fonts, hosted services, network endpoints and local alternatives share P05. Encryption remains P12 because secure transport does not eliminate disclosure to the receiving service.
- General anonymization and transformation coverage share P07. Collection minimization (P06), retention/erasure (P09), audience authorization (P10) and inferential linkage (P11) remain separate mechanisms.
- Device and extension capabilities share P16. Platform permissions are not interchangeable with processing consent or audience authorization.
- Accessibility and integration failures share P13 when the evidence concerns usability or compatibility. Mere breakage does not establish data leakage.
- P17 records the evidential assessment of disputed, retracted, underspecified or non-privacy reports. It is not an additional confirmed defect. Where supported, a substantive category accompanies it; some records support only a narrowed or unresolved assessment.
- Organizational obligations and responsibility (P14), user exports (P15), and safe incident reporting (P18) remain separate because they concern different actions even when infrequent.

## Boundary checks

The explicit assignments retain reported versus implemented behavior and historical differences. Records 247 and 633 preserve the abandoned purpose-4 identifier-removal proposal rather than treating it as the final policy. Record 470 supports default-disabled local persistence without claiming deletion of old data. Record 196 distinguishes export functionality from protection of exported plaintext. Record 503 distinguishes hiding or accepting cookie notices from refusing tracking. Dependency-lock patches for 247, 451, 470 and 633 were subsequently read and do not justify additional privacy categories.

All 652 artifacts receive at least one code, yielding 980 artifact–code pairs. Counts are not mutually exclusive. Quotations and case-specific qualifications remain in assignments.json. This consolidation and its review were authored within the same assistant conversation; package integrity checks are not independent qualitative validation.
