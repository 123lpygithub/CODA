# Privacy / S1-2

Schema: `coda.artifact.v1`. Artifacts: **652**; codes: **31**; artifact–code assignments: **2841**.

This package uses the common seven-file format. All existing coding decisions, evidence and limitations are preserved. Additional source-specific fields are retained in `extensions`; original codebook text is retained in `codebook.json` metadata extensions and the local pre-conversion backup.

## Scope and method

逐条完整阅读冻结材料，记录逐篇 memo 与开放编码，归纳 codebook 后再逐条复核并指派 code；脚本仅做格式转换、重复复核裁定和机械一致性校验，不按关键词分类。

覆盖范围限于冻结材料中的文本；链接页面、附件和图片未读时明确保留限制。
单一 AI 编码；机械一致性检查不构成人工复核或独立双编码。
编码表示材料支持的主题或证据状态，不等于确认违规、缺陷已复现或修复已完成。

## Codes

| Code | Name | Artifacts |
|---|---|---:|
| PR01 | consent capture, gating, and lifecycle enforcement | 132 |
| PR02 | consent recordkeeping and audit trail | 28 |
| PR03 | consent control defeated by timing, persistence, or removal | 49 |
| PR04 | privacy notice and consent interface defects | 96 |
| PR05 | default-on collection and opt-in/opt-out model | 86 |
| PR06 | notice presence, reachability, accuracy, and maintenance | 124 |
| PR07 | transparency, purpose disclosure, and documented trust assumptions | 145 |
| PR08 | jurisdiction scope, cross-border transfer, and legal-authority compliance | 227 |
| PR09 | data inventory, retention, purpose limitation, and minimization | 104 |
| PR10 | right-to-erasure requests, deletion scope, and portability | 66 |
| PR11 | erasure semantics, tooling failure, and residual stores | 29 |
| PR12 | anonymization technique, coverage, re-identification, and media redaction | 99 |
| PR13 | location precision, spatial generalization, encryption, and aggregation safeguards | 17 |
| PR14 | third-party analytics, embeds, and processor exposure | 137 |
| PR15 | data minimization, local-first processing, and configuration suppression | 71 |
| PR16 | credential, secret exposure, and cryptographic/key protection | 28 |
| PR17 | access control integrity, field visibility, and tenant scoping | 50 |
| PR18 | user control over stored state, telemetry settings, and analytics opt-out | 91 |
| PR19 | logging, output, and harvested identifiers as disclosure channel | 37 |
| PR20 | telemetry payload exposure, server-log access, and retention | 16 |
| PR21 | sensitive-context amplification, vulnerable groups, and public-interest tradeoff | 56 |
| PR22 | privacy versus product, security, or platform constraint tradeoff | 113 |
| PR23 | execution of untrusted code and cross-site session exposure | 6 |
| PR24 | responsibility boundary, policy ownership, and dismissal/deferral | 230 |
| PR25 | closure quality, stale/deferred status, and scanner or unreproducible disputes | 120 |
| PR26 | consent implementation tradeoffs, deadline pressure, and monetization | 26 |
| PR27 | restricted data redistribution, license-driven design, and remote uninstall purge | 6 |
| EV01 | evidence: complete body and discussion | 531 |
| EV02 | evidence: partial snapshot | 4 |
| EV03 | evidence: metadata only | 117 |
| EV04 | evidence: title or keyword only, content unreadable | 0 |

## PR01 — consent capture, gating, and lifecycle enforcement

Affirmative choice, granular categories, withdrawal, runtime/state propagation, pre-consent blocking, and honoring recorded consent across components, iframes, SDKs, and permissions.

- Include: Before-consent blocking; opt-in defaults; granular/revocable consent; consent flags across components; SDK consent gates; permission-scope delegation; downstream enforcement failures.
- Exclude: Consent evidence/audit records; notice wording defects; erasure after withdrawal; pure default-on telemetry.
- Boundary/examples: Distinct from consent-recordkeeping and from notice-interface defects; this code owns the working mechanism.
- Supporting artifacts: 132; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "privacy-issue-310",
    "field": "body",
    "quote": "But for that to work, we would have to grant the `cookies` permission, that'll prompt the extension users to re-approve the extension, but given that most users are tech savvy, I think that'd be fine.",
    "interpretation": "The implementation requires granting the `cookies` permission, which triggers a browser-level permission re-approval prompt for existing users. This is an affirmative permission-scope delegation and propagation concern tied to the consent gate for the new capability."
  }
]
````

## PR02 — consent recordkeeping and audit trail

Evidence and accountability for consent: storing exact wording, timestamp, version, identity/IP, withdrawal logs, audit trails, or disputing whether a checkbox alone suffices.

- Include: Consent logs; audit trails; exact statement/timestamp; withdrawal logging; DPO reminders; no record of checked boxes.
- Exclude: Obtaining consent; propagating consent state; notice text/UI; erasure of account data.
- Boundary/examples: Only evidence of consent, not obtaining or enforcing it.
- Supporting artifacts: 28; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "privacy-issue-1770",
    "field": "discussion",
    "quote": "the confirmation has to be saved with the data privacy statement, ideally in a printable form to be archived locally",
    "interpretation": "Participant 1 relays the DPO's requirement that the consent confirmation be stored together with the exact privacy statement version, in an archivable printable form, establishing an audit-evidence mechanism for consent."
  }
]
````

## PR03 — consent control defeated by timing, persistence, or removal

A privacy control is undermined because collection occurs before the user can act, a setting does not survive restart, a widget fails, or exit controls are removed, distorted, or mandatory.

- Include: Analytics before settings reachable; toggle lost on restart; widget error; short consent table; mandatory field; no unsubscribe; member removes group; consent later reused as default.
- Exclude: General unverified-toggle complaints; absent notice text; checkboxes working as designed.
- Boundary/examples: Failure modes of an existing control rather than its design.
- Supporting artifacts: 49; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "privacy-issue-450",
    "field": "body",
    "quote": "if the user reloads the page without clicking anything on the custom prompt, a cookie is planted and on all subsequent loads the prompt does not appear",
    "interpretation": "The control (the prompt) is defeated because a persistence artifact (cookie) is set before the user can act, so the consent control does not survive proper user interaction and is undermined by timing/persistence. This is precisely a failure mode of an existing control rather than its design."
  }
]
````

## PR04 — privacy notice and consent interface defects

Presence, legibility, wording, dismissal, locale, accessibility, or geo-scoping of privacy notices and consent banners at collection, including misleading opt-out instructions and a link substituted for a working mechanism.

- Include: Missing/broken/illegible policy link; banner cannot dismiss; hardcoded strings; NVDA cannot read; hidden controls; stale unsubscribe; CCPA settings row; EEA-only prompting.
- Exclude: Consent capture/gating; consent proof; enforcement failures; policy drafting.
- Boundary/examples: UI-level defects of notices/banners, not their content accuracy.
- Supporting artifacts: 96; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "privacy-issue-1665",
    "field": "body",
    "quote": "The “Privacy Notice” label link is displayed in English, regardless of the user language",
    "interpretation": "The defect is a localized label on a privacy-notice link rendered in English regardless of the user's locale, a UI-level locale/wording defect of the notice interface rather than a capture or enforcement failure. The reporter explicitly frames it as the label link not being translated while the actual notice page works in the user language."
  }
]
````

## PR05 — default-on collection and opt-in/opt-out model

Data practices active unless the user opts out, or debate over opt-in versus opt-out models, covering analytics, telemetry, upload, or persistence enabled by default without an affirmative act.

- Include: Preselected upload checkboxes; cookie set on widget load; persisted accountID enabling later uploads; mandatory email; calls to flip a default; continued use as acceptance.
- Exclude: Banner that fails to persist; pure transparency notices; proposed explicit consent mechanics.
- Boundary/examples: Concerns the default state, not the consent UI mechanics.
- Supporting artifacts: 86; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "privacy-issue-450",
    "field": "body",
    "quote": "a cookie is planted and on all subsequent loads the prompt does not appear",
    "interpretation": "The cookie is set on load and persists by default without any affirmative opt-in act, embodying a default-on collection/acceptance model. The reporter's proposal is effectively to flip the default so the prompt only stops once the user takes an affirmative action."
  }
]
````

## PR06 — notice presence, reachability, accuracy, and maintenance

Whether a privacy notice, policy page, or transparency document exists, is reachable, correctly linked, and accurately reflects practice, including editing, translating, recovering redirects, or documenting configuration.

- Include: Missing policy page; broken links/redirects; policy for app store; stale wording; missing third-party links; localization; rename; deploy legal docs; config attributes documented wrong.
- Exclude: Substantive missing disclosure of collection or recipients; consent capture; banner not rendering.
- Boundary/examples: Object is the document itself; interface rendering defects go elsewhere.
- Supporting artifacts: 124; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "privacy-issue-21460",
    "field": "body",
    "quote": "[French Ts&Cs](https://notification.alpha.canada.ca/features/terms) contain this line:",
    "interpretation": "The issue is about the privacy/terms document itself: a French translation is missing and English legal-term formatting (title case, italicization) is wrong, so the document's accuracy/maintenance in both locales is at stake. This is a defect of the policy document's wording and localization, not of a banner rendering or consent capture."
  }
]
````

## PR07 — transparency, purpose disclosure, and documented trust assumptions

Remedy is to explain purposes, permissions, retention, or residual risk more clearly, or document and warn users about a trust assumption, rather than change the underlying practice.

- Include: In-app location rationale; footer privacy link; FAQ on retention; documenting log retention; docs stating users must trust admins; self-host warning; preview logs; translated notice docs; spec warnings.
- Exclude: Consent checkboxes; actual deletion or anonymization; compliance self-assessment asserting lawfulness.
- Boundary/examples: Disclosure-in-place remedy, not fixing the practice.
- Supporting artifacts: 145; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "privacy-issue-1765",
    "field": "discussion",
    "quote": "crates.io logs IP addresses of all requests as part of standard logging, and these logs are currently retained for a year",
    "interpretation": "The maintainers' remedy-in-place is disclosure: they enumerate informally what is logged, what is stored and for how long, so users can understand the practice, without changing the underlying collection. The reporter's demand is likewise for information about processing rather than cessation, and the retention facts are presented as things to be explained."
  }
]
````

## PR08 — jurisdiction scope, cross-border transfer, and legal-authority compliance

Geography or named law scopes a notice or data flow (EU vs non-EU, CCPA/GDPR, IP-as-PII by region) or the request, refusal, or deferral rests on external legal duty, regulator, DPO, or compliance assertion.

- Include: Extend notice to all visitors; EU/EEA but not UK; German law forbids non-EU client data; uploads to foreign destinations; CCPA/GDPR citations; legal review; vendor TOS; app-store rejection; generic checklist.
- Exclude: TOS-driven license redesign without privacy; notice merely not rendered; purely ethical refusal.
- Boundary/examples: Owns statutory/geographic scoping, including legal review deferrals.
- Supporting artifacts: 227; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "privacy-issue-21460",
    "field": "body",
    "quote": "Follow Canadian law with regard to the privacy act when using this software.",
    "interpretation": "The text names an external statute (the Canadian Privacy Act) as the legal authority governing use of the software, and the requested clause references the Loi sur la protection des renseignements personnels. The scoping rests on a named law rather than a generic transparency request."
  }
]
````

## PR09 — data inventory, retention, purpose limitation, and minimization

Enumerates personal data stored or logged and specifies retention, expiry, overruns, or purpose; includes debate over whether data is processed at all (transient vs stored) versus unbounded retention, and field-level minimization.

- Include: Lists of PII fields; logs retained too long; TTL/expiry; 30-day IP retention; audit tables; scrubbing usernames; dropping fields; stop saving IP/email; country vs province.
- Exclude: Recipient identity or third-party sharing; legal basis; consent design; erasure-request workflows.
- Boundary/examples: Owns retention duration and field-level minimization, not anonymization technique.
- Supporting artifacts: 104; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "privacy-issue-1765",
    "field": "discussion",
    "quote": "Logs are stored for 1 year.",
    "interpretation": "A formal PII audit enumerates fields held (email, GitHub username/full name/avatar), states retention durations and admits logs are kept longer than intended. The thread also records an intent to log additional per-upload data, so field-level inventory, purpose and retention overruns are directly debated."
  }
]
````

## PR10 — right-to-erasure requests, deletion scope, and portability

Data-subject requests for deletion, right-to-be-forgotten, export/portability, or rights scoping, including no self-service path, admin stop-gaps, over-broad clear/delete actions, and conflicts with audit trails, legal hold, shared organizations, or downstream packages.

- Include: No way to delete account; users cannot delete uploads; right-to-be-forgotten; support-email procedure; admin stop-gap; export own data; withdrawal logging; GDPR Art.17 vs audit trail; clear action removing too much.
- Exclude: Tooling failure before erasure; anonymization within retained records; pure retention windows.
- Boundary/examples: Request/capability and scope of deletion, not whether the tool ran.
- Supporting artifacts: 66; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "privacy-issue-21543",
    "field": "discussion",
    "quote": "You can manually verify an user on the database by changing the `verification_token` row on `ticket` table to `NULL`.",
    "interpretation": "The thread describes a stop-gap procedure (manually changing the verification token in the database or resetting a password) used when a user cannot recover access, which is an administrative workaround in the absence of a proper self-service capability."
  }
]
````

## PR11 — erasure semantics, tooling failure, and residual stores

Disputes whether a privacy operation deletes or anonymizes records, conflicts erasure with mandated retention, or documents an eraser aborting on config/schema errors or leaving PII in logs and secondary stores.

- Include: 'Deleted' corrected to 'anonymize'; ten-year order retention with anonymized fields; config from wrong dir; missing-table SQL error; PII in logs; files left on disk.
- Exclude: Tool running but leaving primary-field data; no deletion path at all; pure retention timeouts.
- Boundary/examples: Execution and semantic outcome of deletion, separated from requesting it.
- Supporting artifacts: 29; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "privacy-issue-2958",
    "field": "discussion",
    "quote": "we should not remove the postal code itself (as you say, other users depend on it) but we should remove the deleted user's **reference** to the code.",
    "interpretation": "The thread disputes the semantic of deletion at the postal-code level: whether to delete the record or merely strip the deleted user's reference to a shared Position record, and clarifies via the checkin model's encrypted_user_id attribute. This is a debate over delete-versus-de-reference and what residual store remains after erasure."
  }
]
````

## PR12 — anonymization technique, coverage, re-identification, and media redaction

Masking, hashing, truncation, redaction, substitution, or blurring; reports identifiers surviving in headers, free text, logs, or export boundaries; or documents pseudonymization reversible, linkable, recomputable, or defeated at a role boundary.

- Include: AnonymizeIP options; mask admin emails; hashes are pseudonymization; MESSAGE_ not scrubbed; X-Forwarded-For; stable hash vs random UUID; secret salt; face/plate blurring; statistical de-anonymization.
- Exclude: Wholesale field removal; deletion cascade; unguessable URLs as access control; pure fingerprinting resistance.
- Boundary/examples: Technique adequacy, not location generalization or key-destruction aggregation.
- Supporting artifacts: 99; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "privacy-issue-943",
    "field": "body",
    "quote": "especially include the pseudonymisation logic because this was already identified as a huge bottleneck",
    "interpretation": "The artifact treats pseudonymisation as a processing step whose performance is under analysis and whose selective skipping is proposed, which is a discussion of pseudonymisation technique/coverage even though the motivation is efficiency. The follow-up ideas about per-entity field caches and skipping entities that will not be pseudonymised concern the scope and implementation of pseudonymisation itself."
  }
]
````

## PR13 — location precision, spatial generalization, encryption, and aggregation safeguards

Reducing location granularity so it cannot pinpoint a person (coordinate precision, geoblocks, snapping, adaptive radii) or technical safeguards so released data cannot decrypt or re-identify: key destruction, decryption thresholds, minimum cohort counts.

- Include: Exact coords obfuscated; grid-snapping; density-adaptive radii; geoblocks; delete private key before publishing; trustees with majority threshold; minimum trip counts; suppression of low-count cells.
- Exclude: Location permission rationale only; UI anonymization toggles; export-time hash without key destruction; generic minimization.
- Boundary/examples: Spatial/aggregate safeguards, distinct from field-level masking.
- Supporting artifacts: 17; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "privacy-issue-2904",
    "field": "discussion",
    "quote": "Here's an example of aggregated data:",
    "interpretation": "Aggregation safeguards are invoked: data is aggregated across servers and small deployments below a minimum cohort of five devices are dropped, avoiding pinpointing individuals/small installations. This is a minimum-count aggregation safeguard."
  }
]
````

## PR14 — third-party analytics, embeds, and processor exposure

Named external analytics, trackers, CDNs, relays, ads, fonts, webhooks, or bundled tracker SDKs receive or can access personal data, with anonymization, pre-hashing, proxying, opt-out, removal, or stripped builds framed as remedy, including transfer without consent.

- Include: Anonymize before GTM; cookie from widget embed; Google Fonts CDN; HIBP prehashing; geocoding to Google; Crashlytics at startup; Exodus/F-Droid tracker lists; sending user info to Google without consent; provider substitution.
- Exclude: Internal logs or on-device retention with no external recipient; unknown-recipient breaches; destination-country only.
- Boundary/examples: Combines exposure and transfer; consent-violation framing included.
- Supporting artifacts: 137; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "privacy-issue-1545",
    "field": "discussion",
    "quote": "No the app itself does not, only Twitch collects information. https://www.twitch.tv/p/en/legal/privacy-notice/",
    "interpretation": "The discussion attributes data collection to Twitch, an external platform that users must log into, and directs readers to Twitch's privacy notice. This evidences a third-party service receiving or accessing user data rather than an in-app collection practice."
  }
]
````

## PR15 — data minimization, local-first processing, and configuration suppression

Collect, request, or retain less personal data, keep data local or on-device unless explicitly sent, or argue a rule does not apply because a service is configured to suppress cookies, fingerprints, or IPs.

- Include: Drop mandatory email; local screenshot rendering vs cloud; offline capture; GDPR not applying because data never sent; analytics non-cookie mode; false fingerprints; per-request IP anonymization cited to avoid notice.
- Exclude: Anonymization of already-collected data; efficiency arguments; pure retention timeouts; access control.
- Boundary/examples: Minimization by avoidance rather than transformation.
- Supporting artifacts: 71; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "privacy-issue-943",
    "field": "body",
    "quote": "Skip pseudonymisation completely for entites that we know will not be pseudonymised based on the user's user rights",
    "interpretation": "The concrete proposal is to avoid performing the pseudonymisation transformation at all for cases where it is unnecessary, i.e. reduce processing work by suppression conditioned on configuration/rights rather than transform more data. The per-entity field cache idea similarly aims to request/process less per call, framing minimization-of-processing as the remedy."
  }
]
````

## PR16 — credential, secret exposure, and cryptographic/key protection

Secret material (keys, tokens, share secrets, passwords) appears in an unintended channel such as public repo, analytics dashboard, P2P share, or observability store, or is stored unencrypted/verbatim; includes weak password storage and key-management redesign requests.

- Include: Secret tokens in dashboard URLs; private keys kept out of VCS; master-password persistence; password field plaintext; LDAP password in shared paste; secrets in logs; asymmetric encryption requests.
- Exclude: Non-secret identifying metadata; server-side keychain trust; exposed URL that is not a secret.
- Boundary/examples: Merges secret-in-logs with credential protection; key policy for server ops stays separate.
- Supporting artifacts: 28; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "privacy-issue-21543",
    "field": "body",
    "quote": "I will try from the database anyway but this is not a good solution right now.",
    "interpretation": "The body of the request concerns password handling: the reporter resorts to editing the stored bcrypt hash directly in the database to change a user's password, which exposes the credential-storage channel and key/password protection question."
  }
]
````

## PR17 — access control integrity, field visibility, and tenant scoping

Limiting who can view or operate on personal data via roles, per-field/record visibility, identity-binding proof, tenant filters, and admin operations, and failures where settings, tabs, unguessable URLs, or secret links substitute for real access control or desynchronize.

- Include: Private accounts; follow requests; per-audience visibility; missing WHERE/tenant filter; concurrent ID collision resolving to another subject; admins setting passwords; hiding tabs instead of auth; unguessable URLs.
- Exclude: End-user consent toggles; third-party transfer; retention duration; statistical re-identification.
- Boundary/examples: Structural authorization boundaries, not on-device storage.
- Supporting artifacts: 50; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "privacy-issue-21543",
    "field": "discussion",
    "quote": "This is a well established method and you should not be able to interfere with the user passwords yourelf.",
    "interpretation": "The discussion is fundamentally about whether an administrator may change or assume a user's password/account, i.e. whether such an authorization capability should exist at all and how it undermines the user's own control over their credential; the maintainers argue admins should not be able to interfere with user passwords."
  }
]
````

## PR18 — user control over stored state, telemetry settings, and analytics opt-out

User-facing control over stored state or data egress: deleting cookies/local data, disabling remote pushes, in-memory store choice, discovering telemetry settings, opting out of analytics, or optional/configurable invasive features, plus DNT signaling.

- Include: Cookie-removal command/UI; regex bulk deletion; injectable in-memory store; disable_remote; private fields interim; telemetry-setting links; make live-typing optional; navigator.doNotTrack.
- Exclude: Consent before cookies are set; notice publication; administrative account deletion; default-on model debate.
- Boundary/examples: User-initiated post-collection controls, distinct from pre-consent gating.
- Supporting artifacts: 91; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "privacy-issue-310",
    "field": "body",
    "quote": "I find myself having to go to cookie management page to remove cookies from a specific domain or from multiple domains. I would love to have this feature added to SurfingKeys.",
    "interpretation": "The proposal adds a user-initiated command to remove cookies by domain regex, giving the user direct control over stored browser state after collection. It is a post-collection control mechanism rather than pre-consent gating or a notice."
  }
]
````

## PR19 — logging, output, and harvested identifiers as disclosure channel

Diagnostic logs, error messages, generated output, or automatically harvested metadata (git-log contacts, POM emails, contributor lists) are unintended channels for sensitive data, with masking, redaction, immutable-history caveats, or log expiry proposed.

- Include: Audits of logs for sensitive data; mask fields; replace CN with serial and Pod IP with Pod UID; retroactive redaction; auto-extracting git-log contacts; emails in Maven POM; cannot remove from history; auto-expiry policies; storing non-app API requests by user ID; scrubbing runner diagnostic logs.
- Exclude: Deliberate third-party analytics transmission; access control over stored databases; user-invoked deletion; spatial generalization.
- Boundary/examples: Log/output as channel plus retention of user-linked logs; server log access policy stays separate.
- Supporting artifacts: 37; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "privacy-issue-1770",
    "field": "discussion",
    "quote": "maybe there are some \"hidden\" logs such as revisions with name and time which may be connected to [Issue #924]",
    "interpretation": "The discussion turns on logs as a disclosure channel: nginx access logs storing IP with timestamps, revision history linking names and times to users, and the request to enumerate hidden logs for the privacy statement. Mitigation framing is documenting/scrubbing what the logs contain."
  }
]
````

## PR20 — telemetry payload exposure, server-log access, and retention

What server/platform logs, telemetry payloads, diagnostics, stack traces, breadcrumbs, or debug details collect; who can access them; how long they are kept; PII content; public debug disclosure; and missing redaction hooks.

- Include: Server-side logs; infra sees visitor IPs; unknown retention; PII in stack traces; sensitive debug logs; missing built-in redaction.
- Exclude: Default-on telemetry opt-out; local device history; third-party analytics; consent gating.
- Boundary/examples: Server/infra-side view and access, distinct from client log output.
- Supporting artifacts: 16; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "privacy-issue-1765",
    "field": "discussion",
    "quote": "IP address and user agent header",
    "interpretation": "Server-side logs are described as recording IP address and user-agent per request, with an explicit retention window and a claim about non-associability with account identity. This is about what the platform's logs collect and retain on the infrastructure side, distinct from client output."
  }
]
````

## PR21 — sensitive-context amplification, vulnerable groups, and public-interest tradeoff

Privacy harm amplified by sensitive domain or vulnerable population (minors, Tor/marginalized users, harassment targets), sector-specific sensitive data such as financial or legal records, or explicit balancing against public health, funder reporting, or functionality.

- Include: Medical app data to Facebook; last-online stalking; empty result infers private data; asylum/abortion records; vulnerable groups as rationale; age-gating/COPPA-adjacent; financial ledger sync; public-health vs privacy; legal/court/tax context.
- Exclude: Generic personal data; ordinary content disclosure; access-control desync; identifier collision.
- Boundary/examples: Stakes framing via domain, group, or tradeoff—not a mechanism.
- Supporting artifacts: 56; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "privacy-issue-975",
    "field": "body",
    "quote": "check persons and their respective entities outside the users jurisdiction",
    "interpretation": "The artifact is set in a public-health/epidemiological surveillance application (SORMAS) where person records include sensitive case and contact data. The disclosure of identifiable persons outside a community officer's jurisdiction is amplified harm in a sensitive health context, which the code frames as stakes rather than mechanism."
  }
]
````

## PR22 — privacy versus product, security, or platform constraint tradeoff

Reasoned opposition to a privacy request because the practice serves security, anti-abuse, or core product function, granular controls complicate API consistency, or OS/browser/upstream requirements make it unavoidable (including custom crypto instead of standards).

- Include: Email verification as anti-spam; messaging continuity justifying cookie; grid snapping for marker stability; Safari cookie cap; Apple location services required; upstream library behavior; SHA256 exchange instead of PAKE; Chrome dependency demands.
- Exclude: Bare closure notes with no rationale; generic effort rejections; standards-body decisions awaited.
- Boundary/examples: Requires a stated countervailing rationale, not mere deferral.
- Supporting artifacts: 113; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "privacy-issue-21543",
    "field": "discussion",
    "quote": "Email verification it's still necessary because we need to very the authenticity of the email",
    "interpretation": "The closing rationale weighs a security/anti-abuse account-integrity position (email verification, self-service reset, not encouraging admin override) against the requested product feature, providing a reasoned countervailing rationale rather than a bare rejection."
  }
]
````

## PR23 — execution of untrusted code and cross-site session exposure

External or user-supplied scripts run in a page context with access to credentials, cookies, or DOM data, or an injection flaw renders untrusted data unescaped, allowing script execution that reads session tokens.

- Include: Refusing unsafe-eval because it permits third-party code; crafted pages loading eval code; userscripts from third-party sites; stored XSS via html_safe reading document.cookie; escaping before autolinking.
- Exclude: General network transmission concerns; permission scoping not about code execution; policy text about encryption.
- Boundary/examples: Script injection/execution vector, not data-at-rest exposure.
- Supporting artifacts: 6; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "privacy-issue-352",
    "field": "body",
    "quote": "Errbit's `notices/_user_attributes` partial executes XSS",
    "interpretation": "The issue describes user-supplied exception attribute data being rendered through html_safe in a view partial, enabling stored XSS that executes in the page context and reads document.cookie. The discussion remedy is to escape input before autolinking, directly addressing the script-injection vector."
  }
]
````

## PR24 — responsibility boundary, policy ownership, and dismissal/deferral

Raises where a privacy obligation or policy decision should sit (library vs downstream developer, instance admin, DB layer, standards body), or dismisses/postpones a concern as false positive, expected behavior, another issue, plugin, vendor, or user responsibility without substantive investigation.

- Include: Whether gem or developers anonymize IPs; encryption belongs to DB layer; instance admins decide email; deferral to IAB guidance; contact sales; support-email deflection; duplicate closure; 'use a VPN'; false-positive trust.
- Exclude: Internal task-division disputes within one team; tool config errors with obvious owner; reasoned security tradeoffs.
- Boundary/examples: Ownership deflection and uncontested dismissal; reasoned tradeoffs are separate.
- Supporting artifacts: 230; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "privacy-issue-8387",
    "field": "discussion",
    "quote": "we have set up a team for GDPR enhancements of DNN",
    "interpretation": "Responsibility for the mechanism is pushed to a separate team/initiative and, ultimately, to a successor issue/PR rather than being resolved here. The concern is deferred to other ownership channels without substantive investigation in this thread."
  }
]
````

## PR25 — closure quality, stale/deferred status, and scanner or unreproducible disputes

Resolution quality is contested: closure by roadmap promise, stale-bot, wontfix, duplicate redirect, private unverified outcome, vague report, or contested scanner evidence without diff, test, or reporter confirmation; also shipped fixes disputed as incomplete, and lifecycle metadata like severity/priority conflicts.

- Include: Closed zero comments; stale automation; duplicate redirect; 'pretty sure but not confirmed'; Fortify/Sovy/Tenable sole evidence; attacker-model disputes; vague allegation; cannot reproduce; 'blocker' with 'wontfix'; revisit-on-upgrade notes.
- Exclude: Closure with linked commit; reasoned deferral with consequences; uncontested delivered outcome; reporter confirms.
- Boundary/examples: Triage/lifecycle and evidence-sufficiency signals; independent confirmation is separate.
- Supporting artifacts: 120; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "privacy-issue-21543",
    "field": "discussion",
    "quote": "The real fix to this issue is to make sure that the \"forgot my password\" functionality works as expected, so I will be closing this issue",
    "interpretation": "The issue is closed by arguing the actual defect lies elsewhere (the password-recovery flow) and redirecting related reports, a resolution whose sufficiency rests on the maintainer's assertion rather than a delivered fix; a later commenter reopens the underlying question."
  }
]
````

## PR26 — consent implementation tradeoffs, deadline pressure, and monetization

Tradeoffs prioritizing visual parity, MVP scope, Storybook-only integration, performance, or a statutory date over completing the privacy mechanism, or delivering compliance as a separately priced add-on.

- Include: Drop settings icons in MVP; banner only in Storybook; lazy-load IP getters; CCPA Jan 1 2020 and GDPR May 25 deadlines; one amp-consent instance; compliance as separate priced extension.
- Exclude: Abstract regulation with no concrete deadline/architecture constraint; performance as main point with compliance incidental.
- Boundary/examples: Implementation compromise under schedule/scope pressure, not product-function defense.
- Supporting artifacts: 26; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "privacy-issue-1285",
    "field": "discussion",
    "quote": "Think this is done for the first release of the MVP.",
    "interpretation": "The resolution explicitly scopes the notice guidance to the first MVP release, showing the privacy-related work being settled against release-scope pressure rather than fully resolved. The completion comment frames the instruction work as sufficient 'for the first release of the MVP.'"
  }
]
````

## PR27 — restricted data redistribution, license-driven design, and remote uninstall purge

An externally imposed license, EULA, or distribution restriction on a data source forces redesign of how data is obtained, consented to, or refreshed, or app/account removal hides rather than deletes stored data requiring a lifecycle purge hook.

- Include: MaxMind GeoLite2 developer distribution key; client EULA acceptance; periodic updates after a CCPA change; uninstall hides tabs that reappear; app-removal hook to clean third-party data.
- Exclude: First-party collection/minimization; consent flows for first-party data; standing opt-out persistence.
- Boundary/examples: External redistribution terms and lifecycle purge, distinct from statutory scope.
- Supporting artifacts: 6; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "privacy-issue-21474",
    "field": "body",
    "quote": "Hello, can we use db-ip.com instead of maxmind.com?",
    "interpretation": "The request is to replace MaxMind GeoLite2 with db-ip.com because an externally imposed license/account-key restriction was placed on the data source; the maintainer frames the change as working around a vendor redistribution restriction rather than a first-party collection choice."
  }
]
````

## EV01 — evidence: complete body and discussion

The artifact carries a current-snapshot issue body and all retrievable comments, so proposal, discussion and any recorded outcome can be assessed directly.

- Include: Use when evidence_status is complete and the relevant text is present.
- Exclude: Do not use for partial or metadata-only records, or when the body is empty and there are no comments.
- Boundary/examples: Exactly one state code per artifact; state is about evidence availability, not about whether the issue was resolved.
- Supporting artifacts: 531; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "privacy-issue-310",
    "field": "content",
    "quote": "Evidence availability: complete",
    "interpretation": "The artifact contains the full current issue body and the retrieval explicitly records zero comments out of zero, so the proposal and its discussion state are fully available for assessment."
  }
]
````

## EV02 — evidence: partial snapshot

Some body or discussion text is retrievable but comments, attachments or edited content are known to be missing, so conclusions about discussion or outcome are limited.

- Include: Use when evidence_status is partial or retrieved comments are fewer than expected.
- Exclude: Do not use for complete snapshots or for records with no body/comment text at all.
- Boundary/examples: State, not a theme; note which parts are missing.
- Supporting artifacts: 4; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "privacy-issue-21474",
    "field": "content",
    "quote": "Evidence availability: partial",
    "interpretation": "The artifact is a partial retrieval snapshot: 3 of 4 comments were retrieved and linked pages/attachments were not fetched, limiting conclusions about the full discussion and outcome."
  }
]
````

## EV03 — evidence: metadata only

Only released metadata (title, labels, counts, dates, matched keywords) is available; no body or comment text can be read.

- Include: Use when evidence_status is metadata_only or the snapshot is unavailable.
- Exclude: Do not use when any body or comment text is retrievable.
- Boundary/examples: Themes may still be assigned only at the most cautious, title-supported level; no discussion or outcome may be inferred.
- Supporting artifacts: 117; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": "privacy-issue-4216",
    "field": "content",
    "quote": "Evidence availability: metadata_only",
    "interpretation": "The snapshot supplies only released metadata — title, project, status, dates, label list, comment count — and explicitly states no body or discussion text was retrieved. No concrete privacy mechanism can be inferred from the bare title \"Conflicting documentation\" beyond a lexical match on 'privacy controls'."
  }
]
````

## EV04 — evidence: title or keyword only, content unreadable

A title or matched keyword is the only semantic signal, and even metadata-level context is insufficient to support a concrete privacy mechanism.

- Include: Use when the artifact text cannot support any theme beyond a bare topic mention.
- Exclude: Do not use when the title names a specific mechanism that a theme can defensibly capture.
- Boundary/examples: Distinguish from EV03: EV03 has usable metadata context, EV04 has only a lexical signal.
- Supporting artifacts: 0; complete membership in `supporting_cases`.

````json
[
  {
    "case_id": null,
    "field": null,
    "quote": null,
    "interpretation": ""
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

# deepseek-2 — Privacy 最终编码本

本轮覆盖 **652 个 隐私相关 GitHub issue artifact**，形成 **31 个可分配 code**，共记录 **2841 个 artifact–code assignment**。全部 652 个 artifact 均已编码，未决 0 个。允许在存在彼此独立证据时进行多重编码，因此类别覆盖数之和可以超过 artifact 数。

本 codebook 来自逐条完整阅读冻结材料、逐篇 memo、开放编码、持续比较和逐条 assignment 复核。关键词、正则、聚类和脚本没有用于决定类别；脚本只做格式转换、重复复核裁定和一致性校验。

## 范围与限制

- 覆盖范围是冻结材料中的全部文本；未读取的外链、附件和图片不作推断。
- 单一 AI 编码，未经人工审核，也不构成独立双编码。
- code 表示材料支持的主题、机制或证据状态，不等于确认违规、缺陷已复现或修复已完成。
- Privacy 每个 artifact 至少 1 个隐私主题 code，并恰好 1 个证据状态 code（EV01–EV04）。
- 11 个 artifact 有两次完整复核；发布较晚的一版，全部版本保留在 `assignments.json` 的 `review_history`。

## 类别一览

| Code | 名称 | Artifacts |
|---|---|---:|
| PR01 | consent capture, gating, and lifecycle enforcement | 132 |
| PR02 | consent recordkeeping and audit trail | 28 |
| PR03 | consent control defeated by timing, persistence, or removal | 49 |
| PR04 | privacy notice and consent interface defects | 96 |
| PR05 | default-on collection and opt-in/opt-out model | 86 |
| PR06 | notice presence, reachability, accuracy, and maintenance | 124 |
| PR07 | transparency, purpose disclosure, and documented trust assumptions | 145 |
| PR08 | jurisdiction scope, cross-border transfer, and legal-authority compliance | 227 |
| PR09 | data inventory, retention, purpose limitation, and minimization | 104 |
| PR10 | right-to-erasure requests, deletion scope, and portability | 66 |
| PR11 | erasure semantics, tooling failure, and residual stores | 29 |
| PR12 | anonymization technique, coverage, re-identification, and media redaction | 99 |
| PR13 | location precision, spatial generalization, encryption, and aggregation safeguards | 17 |
| PR14 | third-party analytics, embeds, and processor exposure | 137 |
| PR15 | data minimization, local-first processing, and configuration suppression | 71 |
| PR16 | credential, secret exposure, and cryptographic/key protection | 28 |
| PR17 | access control integrity, field visibility, and tenant scoping | 50 |
| PR18 | user control over stored state, telemetry settings, and analytics opt-out | 91 |
| PR19 | logging, output, and harvested identifiers as disclosure channel | 37 |
| PR20 | telemetry payload exposure, server-log access, and retention | 16 |
| PR21 | sensitive-context amplification, vulnerable groups, and public-interest tradeoff | 56 |
| PR22 | privacy versus product, security, or platform constraint tradeoff | 113 |
| PR23 | execution of untrusted code and cross-site session exposure | 6 |
| PR24 | responsibility boundary, policy ownership, and dismissal/deferral | 230 |
| PR25 | closure quality, stale/deferred status, and scanner or unreproducible disputes | 120 |
| PR26 | consent implementation tradeoffs, deadline pressure, and monetization | 26 |
| PR27 | restricted data redistribution, license-driven design, and remote uninstall purge | 6 |
| EV01 | evidence: complete body and discussion | 531 |
| EV02 | evidence: partial snapshot | 4 |
| EV03 | evidence: metadata only | 117 |
| EV04 | evidence: title or keyword only, content unreadable | 0 |

## 使用规则

- 隐私主题 code 记录材料直接支持的机制、边界或风险；不把报告者主张自动当作已确认事实。
- 证据状态 code 单独记录材料可用性；EV03/EV04 下的主题只作最谨慎的标题或元数据级判断。
- 允许多重主题编码；同一 artifact 恰好一个证据状态 code。

## PR01 — consent capture, gating, and lifecycle enforcement

Affirmative choice, granular categories, withdrawal, runtime/state propagation, pre-consent blocking, and honoring recorded consent across components, iframes, SDKs, and permissions.

**Include:** Before-consent blocking; opt-in defaults; granular/revocable consent; consent flags across components; SDK consent gates; permission-scope delegation; downstream enforcement failures.

**Exclude:** Consent evidence/audit records; notice wording defects; erasure after withdrawal; pure default-on telemetry.

**Support:** 132 artifact(s). 完整列表见 `codebook.json`。

**Boundary:** Distinct from consent-recordkeeping and from notice-interface defects; this code owns the working mechanism.

**Example:** `privacy-issue-310` — The implementation requires granting the `cookies` permission, which triggers a browser-level permission re-approval prompt for existing users. This is an affirmative permission-scope delegation and propagation concern tied to the consent gate for the new capability.

````text
But for that to work, we would have to grant the `cookies` permission, that'll prompt the extension users to re-approve the extension, but given that most users are tech savvy, I think that'd be fine.
````


## PR02 — consent recordkeeping and audit trail

Evidence and accountability for consent: storing exact wording, timestamp, version, identity/IP, withdrawal logs, audit trails, or disputing whether a checkbox alone suffices.

**Include:** Consent logs; audit trails; exact statement/timestamp; withdrawal logging; DPO reminders; no record of checked boxes.

**Exclude:** Obtaining consent; propagating consent state; notice text/UI; erasure of account data.

**Support:** 28 artifact(s). 完整列表见 `codebook.json`。

**Boundary:** Only evidence of consent, not obtaining or enforcing it.

**Example:** `privacy-issue-1770` — Participant 1 relays the DPO's requirement that the consent confirmation be stored together with the exact privacy statement version, in an archivable printable form, establishing an audit-evidence mechanism for consent.

````text
the confirmation has to be saved with the data privacy statement, ideally in a printable form to be archived locally
````


## PR03 — consent control defeated by timing, persistence, or removal

A privacy control is undermined because collection occurs before the user can act, a setting does not survive restart, a widget fails, or exit controls are removed, distorted, or mandatory.

**Include:** Analytics before settings reachable; toggle lost on restart; widget error; short consent table; mandatory field; no unsubscribe; member removes group; consent later reused as default.

**Exclude:** General unverified-toggle complaints; absent notice text; checkboxes working as designed.

**Support:** 49 artifact(s). 完整列表见 `codebook.json`。

**Boundary:** Failure modes of an existing control rather than its design.

**Example:** `privacy-issue-450` — The control (the prompt) is defeated because a persistence artifact (cookie) is set before the user can act, so the consent control does not survive proper user interaction and is undermined by timing/persistence. This is precisely a failure mode of an existing control rather than its design.

````text
if the user reloads the page without clicking anything on the custom prompt, a cookie is planted and on all subsequent loads the prompt does not appear
````


## PR04 — privacy notice and consent interface defects

Presence, legibility, wording, dismissal, locale, accessibility, or geo-scoping of privacy notices and consent banners at collection, including misleading opt-out instructions and a link substituted for a working mechanism.

**Include:** Missing/broken/illegible policy link; banner cannot dismiss; hardcoded strings; NVDA cannot read; hidden controls; stale unsubscribe; CCPA settings row; EEA-only prompting.

**Exclude:** Consent capture/gating; consent proof; enforcement failures; policy drafting.

**Support:** 96 artifact(s). 完整列表见 `codebook.json`。

**Boundary:** UI-level defects of notices/banners, not their content accuracy.

**Example:** `privacy-issue-1665` — The defect is a localized label on a privacy-notice link rendered in English regardless of the user's locale, a UI-level locale/wording defect of the notice interface rather than a capture or enforcement failure. The reporter explicitly frames it as the label link not being translated while the actual notice page works in the user language.

````text
The “Privacy Notice” label link is displayed in English, regardless of the user language
````


## PR05 — default-on collection and opt-in/opt-out model

Data practices active unless the user opts out, or debate over opt-in versus opt-out models, covering analytics, telemetry, upload, or persistence enabled by default without an affirmative act.

**Include:** Preselected upload checkboxes; cookie set on widget load; persisted accountID enabling later uploads; mandatory email; calls to flip a default; continued use as acceptance.

**Exclude:** Banner that fails to persist; pure transparency notices; proposed explicit consent mechanics.

**Support:** 86 artifact(s). 完整列表见 `codebook.json`。

**Boundary:** Concerns the default state, not the consent UI mechanics.

**Example:** `privacy-issue-450` — The cookie is set on load and persists by default without any affirmative opt-in act, embodying a default-on collection/acceptance model. The reporter's proposal is effectively to flip the default so the prompt only stops once the user takes an affirmative action.

````text
a cookie is planted and on all subsequent loads the prompt does not appear
````


## PR06 — notice presence, reachability, accuracy, and maintenance

Whether a privacy notice, policy page, or transparency document exists, is reachable, correctly linked, and accurately reflects practice, including editing, translating, recovering redirects, or documenting configuration.

**Include:** Missing policy page; broken links/redirects; policy for app store; stale wording; missing third-party links; localization; rename; deploy legal docs; config attributes documented wrong.

**Exclude:** Substantive missing disclosure of collection or recipients; consent capture; banner not rendering.

**Support:** 124 artifact(s). 完整列表见 `codebook.json`。

**Boundary:** Object is the document itself; interface rendering defects go elsewhere.

**Example:** `privacy-issue-21460` — The issue is about the privacy/terms document itself: a French translation is missing and English legal-term formatting (title case, italicization) is wrong, so the document's accuracy/maintenance in both locales is at stake. This is a defect of the policy document's wording and localization, not of a banner rendering or consent capture.

````text
[French Ts&Cs](https://notification.alpha.canada.ca/features/terms) contain this line:
````


## PR07 — transparency, purpose disclosure, and documented trust assumptions

Remedy is to explain purposes, permissions, retention, or residual risk more clearly, or document and warn users about a trust assumption, rather than change the underlying practice.

**Include:** In-app location rationale; footer privacy link; FAQ on retention; documenting log retention; docs stating users must trust admins; self-host warning; preview logs; translated notice docs; spec warnings.

**Exclude:** Consent checkboxes; actual deletion or anonymization; compliance self-assessment asserting lawfulness.

**Support:** 145 artifact(s). 完整列表见 `codebook.json`。

**Boundary:** Disclosure-in-place remedy, not fixing the practice.

**Example:** `privacy-issue-1765` — The maintainers' remedy-in-place is disclosure: they enumerate informally what is logged, what is stored and for how long, so users can understand the practice, without changing the underlying collection. The reporter's demand is likewise for information about processing rather than cessation, and the retention facts are presented as things to be explained.

````text
crates.io logs IP addresses of all requests as part of standard logging, and these logs are currently retained for a year
````


## PR08 — jurisdiction scope, cross-border transfer, and legal-authority compliance

Geography or named law scopes a notice or data flow (EU vs non-EU, CCPA/GDPR, IP-as-PII by region) or the request, refusal, or deferral rests on external legal duty, regulator, DPO, or compliance assertion.

**Include:** Extend notice to all visitors; EU/EEA but not UK; German law forbids non-EU client data; uploads to foreign destinations; CCPA/GDPR citations; legal review; vendor TOS; app-store rejection; generic checklist.

**Exclude:** TOS-driven license redesign without privacy; notice merely not rendered; purely ethical refusal.

**Support:** 227 artifact(s). 完整列表见 `codebook.json`。

**Boundary:** Owns statutory/geographic scoping, including legal review deferrals.

**Example:** `privacy-issue-21460` — The text names an external statute (the Canadian Privacy Act) as the legal authority governing use of the software, and the requested clause references the Loi sur la protection des renseignements personnels. The scoping rests on a named law rather than a generic transparency request.

````text
Follow Canadian law with regard to the privacy act when using this software.
````


## PR09 — data inventory, retention, purpose limitation, and minimization

Enumerates personal data stored or logged and specifies retention, expiry, overruns, or purpose; includes debate over whether data is processed at all (transient vs stored) versus unbounded retention, and field-level minimization.

**Include:** Lists of PII fields; logs retained too long; TTL/expiry; 30-day IP retention; audit tables; scrubbing usernames; dropping fields; stop saving IP/email; country vs province.

**Exclude:** Recipient identity or third-party sharing; legal basis; consent design; erasure-request workflows.

**Support:** 104 artifact(s). 完整列表见 `codebook.json`。

**Boundary:** Owns retention duration and field-level minimization, not anonymization technique.

**Example:** `privacy-issue-1765` — A formal PII audit enumerates fields held (email, GitHub username/full name/avatar), states retention durations and admits logs are kept longer than intended. The thread also records an intent to log additional per-upload data, so field-level inventory, purpose and retention overruns are directly debated.

````text
Logs are stored for 1 year.
````


## PR10 — right-to-erasure requests, deletion scope, and portability

Data-subject requests for deletion, right-to-be-forgotten, export/portability, or rights scoping, including no self-service path, admin stop-gaps, over-broad clear/delete actions, and conflicts with audit trails, legal hold, shared organizations, or downstream packages.

**Include:** No way to delete account; users cannot delete uploads; right-to-be-forgotten; support-email procedure; admin stop-gap; export own data; withdrawal logging; GDPR Art.17 vs audit trail; clear action removing too much.

**Exclude:** Tooling failure before erasure; anonymization within retained records; pure retention windows.

**Support:** 66 artifact(s). 完整列表见 `codebook.json`。

**Boundary:** Request/capability and scope of deletion, not whether the tool ran.

**Example:** `privacy-issue-21543` — The thread describes a stop-gap procedure (manually changing the verification token in the database or resetting a password) used when a user cannot recover access, which is an administrative workaround in the absence of a proper self-service capability.

````text
You can manually verify an user on the database by changing the `verification_token` row on `ticket` table to `NULL`.
````


## PR11 — erasure semantics, tooling failure, and residual stores

Disputes whether a privacy operation deletes or anonymizes records, conflicts erasure with mandated retention, or documents an eraser aborting on config/schema errors or leaving PII in logs and secondary stores.

**Include:** 'Deleted' corrected to 'anonymize'; ten-year order retention with anonymized fields; config from wrong dir; missing-table SQL error; PII in logs; files left on disk.

**Exclude:** Tool running but leaving primary-field data; no deletion path at all; pure retention timeouts.

**Support:** 29 artifact(s). 完整列表见 `codebook.json`。

**Boundary:** Execution and semantic outcome of deletion, separated from requesting it.

**Example:** `privacy-issue-2958` — The thread disputes the semantic of deletion at the postal-code level: whether to delete the record or merely strip the deleted user's reference to a shared Position record, and clarifies via the checkin model's encrypted_user_id attribute. This is a debate over delete-versus-de-reference and what residual store remains after erasure.

````text
we should not remove the postal code itself (as you say, other users depend on it) but we should remove the deleted user's **reference** to the code.
````


## PR12 — anonymization technique, coverage, re-identification, and media redaction

Masking, hashing, truncation, redaction, substitution, or blurring; reports identifiers surviving in headers, free text, logs, or export boundaries; or documents pseudonymization reversible, linkable, recomputable, or defeated at a role boundary.

**Include:** AnonymizeIP options; mask admin emails; hashes are pseudonymization; MESSAGE_ not scrubbed; X-Forwarded-For; stable hash vs random UUID; secret salt; face/plate blurring; statistical de-anonymization.

**Exclude:** Wholesale field removal; deletion cascade; unguessable URLs as access control; pure fingerprinting resistance.

**Support:** 99 artifact(s). 完整列表见 `codebook.json`。

**Boundary:** Technique adequacy, not location generalization or key-destruction aggregation.

**Example:** `privacy-issue-943` — The artifact treats pseudonymisation as a processing step whose performance is under analysis and whose selective skipping is proposed, which is a discussion of pseudonymisation technique/coverage even though the motivation is efficiency. The follow-up ideas about per-entity field caches and skipping entities that will not be pseudonymised concern the scope and implementation of pseudonymisation itself.

````text
especially include the pseudonymisation logic because this was already identified as a huge bottleneck
````


## PR13 — location precision, spatial generalization, encryption, and aggregation safeguards

Reducing location granularity so it cannot pinpoint a person (coordinate precision, geoblocks, snapping, adaptive radii) or technical safeguards so released data cannot decrypt or re-identify: key destruction, decryption thresholds, minimum cohort counts.

**Include:** Exact coords obfuscated; grid-snapping; density-adaptive radii; geoblocks; delete private key before publishing; trustees with majority threshold; minimum trip counts; suppression of low-count cells.

**Exclude:** Location permission rationale only; UI anonymization toggles; export-time hash without key destruction; generic minimization.

**Support:** 17 artifact(s). 完整列表见 `codebook.json`。

**Boundary:** Spatial/aggregate safeguards, distinct from field-level masking.

**Example:** `privacy-issue-2904` — Aggregation safeguards are invoked: data is aggregated across servers and small deployments below a minimum cohort of five devices are dropped, avoiding pinpointing individuals/small installations. This is a minimum-count aggregation safeguard.

````text
Here's an example of aggregated data:
````


## PR14 — third-party analytics, embeds, and processor exposure

Named external analytics, trackers, CDNs, relays, ads, fonts, webhooks, or bundled tracker SDKs receive or can access personal data, with anonymization, pre-hashing, proxying, opt-out, removal, or stripped builds framed as remedy, including transfer without consent.

**Include:** Anonymize before GTM; cookie from widget embed; Google Fonts CDN; HIBP prehashing; geocoding to Google; Crashlytics at startup; Exodus/F-Droid tracker lists; sending user info to Google without consent; provider substitution.

**Exclude:** Internal logs or on-device retention with no external recipient; unknown-recipient breaches; destination-country only.

**Support:** 137 artifact(s). 完整列表见 `codebook.json`。

**Boundary:** Combines exposure and transfer; consent-violation framing included.

**Example:** `privacy-issue-1545` — The discussion attributes data collection to Twitch, an external platform that users must log into, and directs readers to Twitch's privacy notice. This evidences a third-party service receiving or accessing user data rather than an in-app collection practice.

````text
No the app itself does not, only Twitch collects information. https://www.twitch.tv/p/en/legal/privacy-notice/
````


## PR15 — data minimization, local-first processing, and configuration suppression

Collect, request, or retain less personal data, keep data local or on-device unless explicitly sent, or argue a rule does not apply because a service is configured to suppress cookies, fingerprints, or IPs.

**Include:** Drop mandatory email; local screenshot rendering vs cloud; offline capture; GDPR not applying because data never sent; analytics non-cookie mode; false fingerprints; per-request IP anonymization cited to avoid notice.

**Exclude:** Anonymization of already-collected data; efficiency arguments; pure retention timeouts; access control.

**Support:** 71 artifact(s). 完整列表见 `codebook.json`。

**Boundary:** Minimization by avoidance rather than transformation.

**Example:** `privacy-issue-943` — The concrete proposal is to avoid performing the pseudonymisation transformation at all for cases where it is unnecessary, i.e. reduce processing work by suppression conditioned on configuration/rights rather than transform more data. The per-entity field cache idea similarly aims to request/process less per call, framing minimization-of-processing as the remedy.

````text
Skip pseudonymisation completely for entites that we know will not be pseudonymised based on the user's user rights
````


## PR16 — credential, secret exposure, and cryptographic/key protection

Secret material (keys, tokens, share secrets, passwords) appears in an unintended channel such as public repo, analytics dashboard, P2P share, or observability store, or is stored unencrypted/verbatim; includes weak password storage and key-management redesign requests.

**Include:** Secret tokens in dashboard URLs; private keys kept out of VCS; master-password persistence; password field plaintext; LDAP password in shared paste; secrets in logs; asymmetric encryption requests.

**Exclude:** Non-secret identifying metadata; server-side keychain trust; exposed URL that is not a secret.

**Support:** 28 artifact(s). 完整列表见 `codebook.json`。

**Boundary:** Merges secret-in-logs with credential protection; key policy for server ops stays separate.

**Example:** `privacy-issue-21543` — The body of the request concerns password handling: the reporter resorts to editing the stored bcrypt hash directly in the database to change a user's password, which exposes the credential-storage channel and key/password protection question.

````text
I will try from the database anyway but this is not a good solution right now.
````


## PR17 — access control integrity, field visibility, and tenant scoping

Limiting who can view or operate on personal data via roles, per-field/record visibility, identity-binding proof, tenant filters, and admin operations, and failures where settings, tabs, unguessable URLs, or secret links substitute for real access control or desynchronize.

**Include:** Private accounts; follow requests; per-audience visibility; missing WHERE/tenant filter; concurrent ID collision resolving to another subject; admins setting passwords; hiding tabs instead of auth; unguessable URLs.

**Exclude:** End-user consent toggles; third-party transfer; retention duration; statistical re-identification.

**Support:** 50 artifact(s). 完整列表见 `codebook.json`。

**Boundary:** Structural authorization boundaries, not on-device storage.

**Example:** `privacy-issue-21543` — The discussion is fundamentally about whether an administrator may change or assume a user's password/account, i.e. whether such an authorization capability should exist at all and how it undermines the user's own control over their credential; the maintainers argue admins should not be able to interfere with user passwords.

````text
This is a well established method and you should not be able to interfere with the user passwords yourelf.
````


## PR18 — user control over stored state, telemetry settings, and analytics opt-out

User-facing control over stored state or data egress: deleting cookies/local data, disabling remote pushes, in-memory store choice, discovering telemetry settings, opting out of analytics, or optional/configurable invasive features, plus DNT signaling.

**Include:** Cookie-removal command/UI; regex bulk deletion; injectable in-memory store; disable_remote; private fields interim; telemetry-setting links; make live-typing optional; navigator.doNotTrack.

**Exclude:** Consent before cookies are set; notice publication; administrative account deletion; default-on model debate.

**Support:** 91 artifact(s). 完整列表见 `codebook.json`。

**Boundary:** User-initiated post-collection controls, distinct from pre-consent gating.

**Example:** `privacy-issue-310` — The proposal adds a user-initiated command to remove cookies by domain regex, giving the user direct control over stored browser state after collection. It is a post-collection control mechanism rather than pre-consent gating or a notice.

````text
I find myself having to go to cookie management page to remove cookies from a specific domain or from multiple domains. I would love to have this feature added to SurfingKeys.
````


## PR19 — logging, output, and harvested identifiers as disclosure channel

Diagnostic logs, error messages, generated output, or automatically harvested metadata (git-log contacts, POM emails, contributor lists) are unintended channels for sensitive data, with masking, redaction, immutable-history caveats, or log expiry proposed.

**Include:** Audits of logs for sensitive data; mask fields; replace CN with serial and Pod IP with Pod UID; retroactive redaction; auto-extracting git-log contacts; emails in Maven POM; cannot remove from history; auto-expiry policies; storing non-app API requests by user ID; scrubbing runner diagnostic logs.

**Exclude:** Deliberate third-party analytics transmission; access control over stored databases; user-invoked deletion; spatial generalization.

**Support:** 37 artifact(s). 完整列表见 `codebook.json`。

**Boundary:** Log/output as channel plus retention of user-linked logs; server log access policy stays separate.

**Example:** `privacy-issue-1770` — The discussion turns on logs as a disclosure channel: nginx access logs storing IP with timestamps, revision history linking names and times to users, and the request to enumerate hidden logs for the privacy statement. Mitigation framing is documenting/scrubbing what the logs contain.

````text
maybe there are some "hidden" logs such as revisions with name and time which may be connected to [Issue #924]
````


## PR20 — telemetry payload exposure, server-log access, and retention

What server/platform logs, telemetry payloads, diagnostics, stack traces, breadcrumbs, or debug details collect; who can access them; how long they are kept; PII content; public debug disclosure; and missing redaction hooks.

**Include:** Server-side logs; infra sees visitor IPs; unknown retention; PII in stack traces; sensitive debug logs; missing built-in redaction.

**Exclude:** Default-on telemetry opt-out; local device history; third-party analytics; consent gating.

**Support:** 16 artifact(s). 完整列表见 `codebook.json`。

**Boundary:** Server/infra-side view and access, distinct from client log output.

**Example:** `privacy-issue-1765` — Server-side logs are described as recording IP address and user-agent per request, with an explicit retention window and a claim about non-associability with account identity. This is about what the platform's logs collect and retain on the infrastructure side, distinct from client output.

````text
IP address and user agent header
````


## PR21 — sensitive-context amplification, vulnerable groups, and public-interest tradeoff

Privacy harm amplified by sensitive domain or vulnerable population (minors, Tor/marginalized users, harassment targets), sector-specific sensitive data such as financial or legal records, or explicit balancing against public health, funder reporting, or functionality.

**Include:** Medical app data to Facebook; last-online stalking; empty result infers private data; asylum/abortion records; vulnerable groups as rationale; age-gating/COPPA-adjacent; financial ledger sync; public-health vs privacy; legal/court/tax context.

**Exclude:** Generic personal data; ordinary content disclosure; access-control desync; identifier collision.

**Support:** 56 artifact(s). 完整列表见 `codebook.json`。

**Boundary:** Stakes framing via domain, group, or tradeoff—not a mechanism.

**Example:** `privacy-issue-975` — The artifact is set in a public-health/epidemiological surveillance application (SORMAS) where person records include sensitive case and contact data. The disclosure of identifiable persons outside a community officer's jurisdiction is amplified harm in a sensitive health context, which the code frames as stakes rather than mechanism.

````text
check persons and their respective entities outside the users jurisdiction
````


## PR22 — privacy versus product, security, or platform constraint tradeoff

Reasoned opposition to a privacy request because the practice serves security, anti-abuse, or core product function, granular controls complicate API consistency, or OS/browser/upstream requirements make it unavoidable (including custom crypto instead of standards).

**Include:** Email verification as anti-spam; messaging continuity justifying cookie; grid snapping for marker stability; Safari cookie cap; Apple location services required; upstream library behavior; SHA256 exchange instead of PAKE; Chrome dependency demands.

**Exclude:** Bare closure notes with no rationale; generic effort rejections; standards-body decisions awaited.

**Support:** 113 artifact(s). 完整列表见 `codebook.json`。

**Boundary:** Requires a stated countervailing rationale, not mere deferral.

**Example:** `privacy-issue-21543` — The closing rationale weighs a security/anti-abuse account-integrity position (email verification, self-service reset, not encouraging admin override) against the requested product feature, providing a reasoned countervailing rationale rather than a bare rejection.

````text
Email verification it's still necessary because we need to very the authenticity of the email
````


## PR23 — execution of untrusted code and cross-site session exposure

External or user-supplied scripts run in a page context with access to credentials, cookies, or DOM data, or an injection flaw renders untrusted data unescaped, allowing script execution that reads session tokens.

**Include:** Refusing unsafe-eval because it permits third-party code; crafted pages loading eval code; userscripts from third-party sites; stored XSS via html_safe reading document.cookie; escaping before autolinking.

**Exclude:** General network transmission concerns; permission scoping not about code execution; policy text about encryption.

**Support:** 6 artifact(s). 完整列表见 `codebook.json`。

**Boundary:** Script injection/execution vector, not data-at-rest exposure.

**Example:** `privacy-issue-352` — The issue describes user-supplied exception attribute data being rendered through html_safe in a view partial, enabling stored XSS that executes in the page context and reads document.cookie. The discussion remedy is to escape input before autolinking, directly addressing the script-injection vector.

````text
Errbit's `notices/_user_attributes` partial executes XSS
````


## PR24 — responsibility boundary, policy ownership, and dismissal/deferral

Raises where a privacy obligation or policy decision should sit (library vs downstream developer, instance admin, DB layer, standards body), or dismisses/postpones a concern as false positive, expected behavior, another issue, plugin, vendor, or user responsibility without substantive investigation.

**Include:** Whether gem or developers anonymize IPs; encryption belongs to DB layer; instance admins decide email; deferral to IAB guidance; contact sales; support-email deflection; duplicate closure; 'use a VPN'; false-positive trust.

**Exclude:** Internal task-division disputes within one team; tool config errors with obvious owner; reasoned security tradeoffs.

**Support:** 230 artifact(s). 完整列表见 `codebook.json`。

**Boundary:** Ownership deflection and uncontested dismissal; reasoned tradeoffs are separate.

**Example:** `privacy-issue-8387` — Responsibility for the mechanism is pushed to a separate team/initiative and, ultimately, to a successor issue/PR rather than being resolved here. The concern is deferred to other ownership channels without substantive investigation in this thread.

````text
we have set up a team for GDPR enhancements of DNN
````


## PR25 — closure quality, stale/deferred status, and scanner or unreproducible disputes

Resolution quality is contested: closure by roadmap promise, stale-bot, wontfix, duplicate redirect, private unverified outcome, vague report, or contested scanner evidence without diff, test, or reporter confirmation; also shipped fixes disputed as incomplete, and lifecycle metadata like severity/priority conflicts.

**Include:** Closed zero comments; stale automation; duplicate redirect; 'pretty sure but not confirmed'; Fortify/Sovy/Tenable sole evidence; attacker-model disputes; vague allegation; cannot reproduce; 'blocker' with 'wontfix'; revisit-on-upgrade notes.

**Exclude:** Closure with linked commit; reasoned deferral with consequences; uncontested delivered outcome; reporter confirms.

**Support:** 120 artifact(s). 完整列表见 `codebook.json`。

**Boundary:** Triage/lifecycle and evidence-sufficiency signals; independent confirmation is separate.

**Example:** `privacy-issue-21543` — The issue is closed by arguing the actual defect lies elsewhere (the password-recovery flow) and redirecting related reports, a resolution whose sufficiency rests on the maintainer's assertion rather than a delivered fix; a later commenter reopens the underlying question.

````text
The real fix to this issue is to make sure that the "forgot my password" functionality works as expected, so I will be closing this issue
````


## PR26 — consent implementation tradeoffs, deadline pressure, and monetization

Tradeoffs prioritizing visual parity, MVP scope, Storybook-only integration, performance, or a statutory date over completing the privacy mechanism, or delivering compliance as a separately priced add-on.

**Include:** Drop settings icons in MVP; banner only in Storybook; lazy-load IP getters; CCPA Jan 1 2020 and GDPR May 25 deadlines; one amp-consent instance; compliance as separate priced extension.

**Exclude:** Abstract regulation with no concrete deadline/architecture constraint; performance as main point with compliance incidental.

**Support:** 26 artifact(s). 完整列表见 `codebook.json`。

**Boundary:** Implementation compromise under schedule/scope pressure, not product-function defense.

**Example:** `privacy-issue-1285` — The resolution explicitly scopes the notice guidance to the first MVP release, showing the privacy-related work being settled against release-scope pressure rather than fully resolved. The completion comment frames the instruction work as sufficient 'for the first release of the MVP.'

````text
Think this is done for the first release of the MVP.
````


## PR27 — restricted data redistribution, license-driven design, and remote uninstall purge

An externally imposed license, EULA, or distribution restriction on a data source forces redesign of how data is obtained, consented to, or refreshed, or app/account removal hides rather than deletes stored data requiring a lifecycle purge hook.

**Include:** MaxMind GeoLite2 developer distribution key; client EULA acceptance; periodic updates after a CCPA change; uninstall hides tabs that reappear; app-removal hook to clean third-party data.

**Exclude:** First-party collection/minimization; consent flows for first-party data; standing opt-out persistence.

**Support:** 6 artifact(s). 完整列表见 `codebook.json`。

**Boundary:** External redistribution terms and lifecycle purge, distinct from statutory scope.

**Example:** `privacy-issue-21474` — The request is to replace MaxMind GeoLite2 with db-ip.com because an externally imposed license/account-key restriction was placed on the data source; the maintainer frames the change as working around a vendor redistribution restriction rather than a first-party collection choice.

````text
Hello, can we use db-ip.com instead of maxmind.com?
````


## EV01 — evidence: complete body and discussion

The artifact carries a current-snapshot issue body and all retrievable comments, so proposal, discussion and any recorded outcome can be assessed directly.

**Include:** Use when evidence_status is complete and the relevant text is present.

**Exclude:** Do not use for partial or metadata-only records, or when the body is empty and there are no comments.

**Support:** 531 artifact(s). 完整列表见 `codebook.json`。

**Boundary:** Exactly one state code per artifact; state is about evidence availability, not about whether the issue was resolved.

**Example:** `privacy-issue-310` — The artifact contains the full current issue body and the retrieval explicitly records zero comments out of zero, so the proposal and its discussion state are fully available for assessment.

````text
Evidence availability: complete
````


## EV02 — evidence: partial snapshot

Some body or discussion text is retrievable but comments, attachments or edited content are known to be missing, so conclusions about discussion or outcome are limited.

**Include:** Use when evidence_status is partial or retrieved comments are fewer than expected.

**Exclude:** Do not use for complete snapshots or for records with no body/comment text at all.

**Support:** 4 artifact(s). 完整列表见 `codebook.json`。

**Boundary:** State, not a theme; note which parts are missing.

**Example:** `privacy-issue-21474` — The artifact is a partial retrieval snapshot: 3 of 4 comments were retrieved and linked pages/attachments were not fetched, limiting conclusions about the full discussion and outcome.

````text
Evidence availability: partial
````


## EV03 — evidence: metadata only

Only released metadata (title, labels, counts, dates, matched keywords) is available; no body or comment text can be read.

**Include:** Use when evidence_status is metadata_only or the snapshot is unavailable.

**Exclude:** Do not use when any body or comment text is retrievable.

**Support:** 117 artifact(s). 完整列表见 `codebook.json`。

**Boundary:** Themes may still be assigned only at the most cautious, title-supported level; no discussion or outcome may be inferred.

**Example:** `privacy-issue-4216` — The snapshot supplies only released metadata — title, project, status, dates, label list, comment count — and explicitly states no body or discussion text was retrieved. No concrete privacy mechanism can be inferred from the bare title "Conflicting documentation" beyond a lexical match on 'privacy controls'.

````text
Evidence availability: metadata_only
````


## EV04 — evidence: title or keyword only, content unreadable

A title or matched keyword is the only semantic signal, and even metadata-level context is insufficient to support a concrete privacy mechanism.

**Include:** Use when the artifact text cannot support any theme beyond a bare topic mention.

**Exclude:** Do not use when the title names a specific mechanism that a theme can defensibly capture.

**Support:** 0 artifact(s). 完整列表见 `codebook.json`。

**Boundary:** Distinguish from EV03: EV03 has usable metadata context, EV04 has only a lexical signal.

## 配套文件

- `codebook.json`：结构化定义、支持案例、计数、代表证据和方法元数据。
- `codebook.csv`：表格化 codebook。
- `assignments.json` / `assignments.csv`：每个 artifact 的 code、理由、逐字证据、来源与证据限制。
- `taxonomy.json`：HOW-style 类别树。
- `results.json`：冻结材料正文与最终编码的逐条组合。
