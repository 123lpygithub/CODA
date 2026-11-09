# Privacy — GPT6-1

652 artifacts; 18 codes; 980 artifact–code assignments.

Inductive consolidation of individually authored full supplied-text reading notes, followed by explicit per-artifact assignment review. No keyword classifier, external model API, or prior codebook assignments were used for consolidation.

Every supplied artifact has an assignment. Codes describe the observed work, concern, or evidence status; they do not establish that a defect was reproduced. Refer to `assignments.json` for individual reasoning, qualifications, source references and evidence.

## Scope

- Coverage refers to all supplied textual sections, not all content ever linked on the web.
- Source revision ambiguity, inaccessible context, tentative proposals and absence of execution evidence remain in individual scope notes.
- Coding is assistant-authored; it is not published human annotation, independently validated ground truth, or an experimental system run.
- All artifacts are included. Reports, proposals, disputed or retracted claims, implementation evidence and missing context remain distinct; coding a concern does not confirm a violation or a completed fix.
- Exact duplicate supplemental text was read once with reconstruction maps. Long CSS and dependency metadata used reversible lexical views; integrity digests were retained as opaque literals, not verified. Linked images or external pages not inspected are explicitly qualified; runtime behavior was not reproduced.

Reconstruction within the same conversation; not a blinded independent replicate.

## Codebook

| Code | Name | Artifacts |
|---|---|---:|
| P01 | Privacy notices and accurate disclosure | 131 |
| P02 | Explicit choices and durable preference management | 82 |
| P03 | Enforcing privacy choices across processing paths | 70 |
| P04 | Telemetry scope, defaults and participation | 55 |
| P05 | Control over external services and data destinations | 56 |
| P06 | Limiting collection and unnecessary detail | 35 |
| P07 | De-identification coverage and utility | 57 |
| P08 | Sensitive information in diagnostics and derived outputs | 34 |
| P09 | Retention, erasure and residual copies | 84 |
| P10 | Audience boundaries and authorized disclosure | 64 |
| P11 | Linkability, inference and fingerprinting | 31 |
| P12 | Confidentiality, credentials and session protection | 42 |
| P13 | Usable controls and privacy-related compatibility | 91 |
| P14 | Privacy requirements and organizational responsibility | 46 |
| P15 | User access and portable exports | 6 |
| P16 | Capability permissions and controlled execution | 24 |
| P17 | Evidence-qualified privacy assessment | 64 |
| P18 | Privacy incident and safe reporting procedures | 8 |

## P01 — Privacy notices and accurate disclosure

Provide accessible, understandable and current explanations of data handling, recipients, purposes and controls, or correct inconsistencies between those explanations and the stated practice.

**Include:** Policy text, links, localization, permission-purpose explanations, cookie inventories and misleading disclosure wording.

**Exclude:** Use P02 for capturing or revisiting a decision, P03 for enforcing it, and P14 for broader organizational readiness rather than notice content.

**Examples:**

- `privacy-issue-20664`: A cookie-warning request for the project's website was initially interpreted as forcing a warning into the authentication library. The author clarifies the scope is ember-simple-auth.com, so the objection about application-level design control addresses a different scope. Qualification: A participant's legal supposition is not an independent determination. No implemented warning is shown. The linked legal-information page has not yet been read in this reconstruction.
- `privacy-issue-8840`: Parabol asks to verify absence of cookies or provide a policy/banner if present. The closing discussion explicitly distinguishes existing marketing-site work from application work not yet performed. Qualification: Neither no-cookie status nor application GDPR compliance is established. Closed/stale status is not completion evidence.

## P02 — Explicit choices and durable preference management

Let people make, save, revisit and withdraw purpose-appropriate privacy choices, with a clear distinction between acknowledgement, dismissal and permission.

**Include:** Accept/reject controls, consent records and versions, preference persistence and scope, re-prompting, and optional communications.

**Exclude:** A banner alone is P01. Actual gating of processing is P03; broader telemetry collection/default debates are P04.

**Examples:**

- `privacy-issue-17245`: A cookie-consent feature starts with a proposed end-to-end flow from editable categories/notice text through a Next.js consent component and Django request middleware. The final reply abandons the in-house path in favor of third-party services. Qualification: The corpus has no body field. Planned components are not proof they were all shipped; the final closure represents a change in approach, not completion of the proposed internal implementation or proof of EU-law compliance.
- `privacy-issue-8812`: GOV.UK requests progressively enhanced cookie-banner examples: hide with JavaScript after consent, reload without JavaScript, and show how essential-only services behave on client and server. The related guidance issue coordinates examples, technical/content review and privacy review. Qualification: Current issue checklists report completion, while the dated comment describes an earlier release dependency. This supports reported documentation/example work, not runtime proof that every adopting service enforces consent correctly.

## P03 — Enforcing privacy choices across processing paths

Carry the applicable privacy preference to every relevant processing path and act on it, including initialization, integrations, revocation and state transitions.

**Include:** Pre-consent script/SDK loading, processing after opt-out, shared consent signals, purpose-specific filtering and inconsistent enforcement between components.

**Exclude:** Saving or displaying preferences without evidence about processing is P02. Signal transmission is not assumed to establish downstream compliance.

**Examples:**

- `privacy-issue-12607`: Bookmarks Organizer 2.0 took control of Firefox tracking protection to avoid false broken-bookmark reports, leaving the native privacy controls unavailable. The maintainer first proposed opt-in, later reported reverting the change in 2.0.1, and in 2023 abandoned reintroduction in favor of an explanatory notice. Qualification: Closure and current changelog cannot establish when a fix deployed; the rollback is a maintainer report. Opt-in was an abandoned proposal, not the recorded final implementation. The linked changelog is retrieval-time master, not a frozen 2018 snapshot.
- `privacy-issue-20518`: WP Rocket needs compatibility with the WeePie plugin's mechanism for blocking content until cookies are approved. Qualification: The request does not document an actual bypass, precise integration mechanism, or completed fix; closed status alone does not supply those facts.

## P04 — Telemetry scope, defaults and participation

Decide whether and how operational or usage telemetry is collected, making its scope, defaults, participation controls and diagnostic value explicit.

**Include:** Default-on versus opt-in analytics, telemetry inventories, identifier choices, inspection of payloads, and deciding to introduce, remove or limit collection.

**Exclude:** Ordinary third-party resource loading is P05; a specific sanitizer failure is P08; a concrete failure to honor an established choice additionally belongs to P03.

**Examples:**

- `privacy-issue-18575`: A Syncthing user proposes randomized reporting to hide individual usage details and hopes stronger guarantees would increase opt-in participation. Maintainers dispute its necessity, note existing opt-out and claimed lack of user linkage, and judge the added complexity excessive. The proposer accepts that it is an optional improvement. Qualification: The thread does not establish existing re-identification, mathematical privacy guarantees of an implemented design, or improved representativeness. Randomization alone does not remove participation bias. External RAPPOR and differential-privacy explanations remain to be read.
- `privacy-issue-5472`: The reporter challenges default-enabled Flutter CLI analytics and transmission of an opt-out event, proposing explicit opt-in, a first-run choice and no analytics transmissions when disabled. Discussion contests the applicability of the supplied legal references and quotes regulator guidance. Maintainers acknowledge investigation and later close the public issue while explicitly saying review continues and public updates will stop. Qualification: Legal violations are participant claims, not established findings. The issue is closed without a stated technical fix; the comment about repeated events after configuration resets is a report, not a reproduced trace. External legal documents and product comparisons were not independently verified.

## P05 — Control over external services and data destinations

Reduce or make deliberate the disclosure and dependency created by external services, network requests or hosting choices, including local alternatives.

**Include:** Remote fonts/media/rendering, cloud and DNS endpoints, service-provider trust, self-hosting and documented regional storage concerns.

**Exclude:** Encryption of a connection is P12. An external request is not automatically tracking, and provider replacement is not automatically anonymity.

**Examples:**

- `privacy-issue-18638`: The reporter wants a standalone configurator to avoid Chrome privacy concerns. Discussion establishes existing CLI and Chromium options; the request evolves into documenting Chromium rather than requiring a new GUI. Maintainers initially close for lack of a proposed replacement, and later agree alternatives should be mentioned. The linked CLI document was read in full, including backup/restore and parameter tables; it describes serial configuration independent of the Chrome app. Qualification: Chrome insecurity and Chromium privacy guarantees are participant opinions, not verified findings. No specific collection or leak is demonstrated. The master-branch CLI document was retrieved in 2026, not pinned to the discussion revision; its flight telemetry parameters are not evidence of browser analytics.
- `privacy-issue-18693`: A developer quotes a store enforcement notice about an embedded messaging SDK collecting PII without disclosure, with remediation through disclosure or removing collection. Response redirects to private support. Qualification: This is a reported enforcement notice; neither SDK payload nor resolution independently established, and support exchange unavailable.

## P06 — Limiting collection and unnecessary detail

Avoid collecting or exposing more data than the stated function requires, balancing utility with the necessity of fields, precision and identifiers.

**Include:** Optional personal fields, eliminating unnecessary events, reduced geographic detail, minimal public/session data and rejecting invasive feature proposals.

**Exclude:** Transforming existing identifiers is P07; time-based removal is P09; authorization by audience is P10.

**Examples:**

- `privacy-issue-11537`: Privacy flags already remove buyer identifiers but miss IDs in other request fields. The request extends removal consistently across advertising opt-out, GDPR, child-protection and sale opt-out signals; maintainer reports completion in Go and Java. Qualification: Implementation reported by maintainer; no patch or independent runtime verification supplied. Duplicate stale notices represented as aliases.
- `privacy-issue-21382`: A hard-required telephone field prompts a request for configurable display and requiredness to avoid collecting unneeded personal data. Discussion distinguishes store-wide policy from provider-specific checkout needs and recognizes template/controller consistency. Maintainer promises settings and subsequent comments describe the commit enabling both controls. Qualification: All44comments, pinned template excerpt and both supplied legal pages read. Template marks telephone row required but alone does not establish backend enforcement. Legal applicability and penalty assertions remain participants’ claims; no complete fix diff/runtime test supplied.

## P07 — De-identification coverage and utility

Remove, mask, replace or coarsen identifying information while preserving the required structure or analytical utility, and examine the limits of that transformation.

**Include:** Anonymization/pseudonymization tools, metadata stripping, stable mappings, overlooked fields/formats, hash limitations and transformation compatibility.

**Exclude:** Log/debug-specific sanitation is P08. Masking is not assumed to erase originals or guarantee resistance to re-identification.

**Examples:**

- `privacy-issue-4824`: The issue requests handling private fields during anonymization or a Neurinfo-specific solution. The sole later reply reports completion by one developer while explicitly awaiting final validation. Qualification: The fields, anonymization transformation and validation outcome are not described. Do not infer a particular medical identifier or independently successful anonymization.
- `privacy-issue-4956`: The LMS requests an administrator action that anonymizes user data while preserving the user record, distinct from deleting the user. A later reply states the feature was implemented. Qualification: No list of transformed fields or resistance to re-identification is supplied; implementation status is reported rather than inspected.

## P08 — Sensitive information in diagnostics and derived outputs

Prevent diagnostic or derived operational records from disclosing sensitive values, including secondary copies, reconstructed fields and publication workflows.

**Include:** Logs, crash reports, stack traces, telemetry URLs, metadata in debug profiles, public troubleshooting material and configurable sanitation hooks.

**Exclude:** Collection-policy disputes without a specific output concern are P04. General data anonymization is P07 and deletion schedules are P09.

**Examples:**

- `privacy-issue-5536`: The runner issue asks which personal data in diagnostic logs should be scrubbed to support expected certification needs. A later maintainer reply says scrubbing work was already done and asks for specific residual issues. Qualification: The discussion supplies no log samples, patch or audit covering every field. Completion is reported, not independently verified, and certification is a motivating expectation rather than established status.
- `privacy-issue-12223`: Staging exposes links to internal delegate documents. Discussion identifies that URLs are also in public source, so hiding links is insufficient: access must be restricted at the document host. A separate concern is pending identity-claim information in developer database dumps, with a privacy-versus-representative-test-data tradeoff. A participant reports forms now require WCA sign-in and the issue later cites a fixing PR. Qualification: Read all eight comments and the pinned template excerpt. The screenshot shows document and claim links, not the contents or access-control enforcement. No evidence establishes that database-dump sanitization was accepted or implemented; reported form restrictions must not be extended to every concern.

## P09 — Retention, erasure and residual copies

Control how long information remains and what deletion actually removes across related records, local caches, remote copies and retained historical context.

**Include:** Account/content deletion, automatic expiration, anonymization as an erasure alternative, log retention, browser history, local persistence and cascade boundaries.

**Exclude:** Portable copies for user access are P15. Concealing a view or closing an account is not assumed to erase the underlying data.

**Examples:**

- `privacy-issue-5616`: A user reports that deleting a forum user violates a nonnegative post-count database constraint, obstructing the requested removal. The maintainer suggests deleting related topics/posts/profile and reports that direct deletion also works in their own test. Qualification: The conflict between report and maintainer test is unresolved in the supplied discussion; do not claim a confirmed fix or legal noncompliance. The reporter deleted topics/profile but does not show separately deleting every ForumPost.
- `privacy-issue-4956`: The LMS requests an administrator action that anonymizes user data while preserving the user record, distinct from deleting the user. A later reply states the feature was implemented. Qualification: No list of transformed fields or resistance to re-identification is supplied; implementation status is reported rather than inspected.

## P10 — Audience boundaries and authorized disclosure

Restrict who can receive, discover or view information and preserve that audience boundary across routes, derived views, identities and state changes.

**Include:** Private fields/profiles, recipient selection, role restrictions, cross-user leakage, search visibility, sharing safeguards and federation access boundaries.

**Exclude:** Inference through otherwise available identifiers or observations is P11. A hidden control or unguessable URL is not assumed to enforce authorization.

**Examples:**

- `privacy-issue-12057`: Firefox users report copying or sharing a previous tab’s URL instead of the selected tab after opening external links. Reproduction varies by build and context; a maintainer eventually reproduces with custom tabs and says a fix is available, followed by a reporter no longer reproducing it. Qualification: Users report sharing wrong links; credential/secret-URL exposure is a possible consequence, not a documented exposure of particular credentials. Patch deployment is not verified. Jira source is unavailable; switching tabs is a reported workaround.
- `privacy-issue-21349`: A proposed default-false FERPA profile flag suppresses protected member names for ordinary members while retaining administrator visibility. Discussion corrects the acronym and changes the placeholder from Suppressed to asterisks. Annotated screenshots additionally specify that members must not see UIN or email, while administrators see all details. Qualification: These are requested rules and annotated interface designs, not proof of implemented backend authorization or FERPA compliance. Screenshots distinguish name suppression from broader restrictions on email and UIN.

## P11 — Linkability, inference and fingerprinting

Examine or reduce the ability to infer identity, membership, activity or sensitive attributes by linking identifiers, observable behavior or technical characteristics.

**Include:** Browser/device fingerprints, account enumeration, transaction/vote linkage, activity-status inference and stable identifiers that defeat pseudonymous presentation.

**Exclude:** Direct unauthorized content delivery is P10. Randomization, hashes or pseudonyms do not alone establish anonymity.

**Examples:**

- `privacy-issue-18575`: A Syncthing user proposes randomized reporting to hide individual usage details and hopes stronger guarantees would increase opt-in participation. Maintainers dispute its necessity, note existing opt-out and claimed lack of user linkage, and judge the added complexity excessive. The proposer accepts that it is an optional improvement. Qualification: The thread does not establish existing re-identification, mathematical privacy guarantees of an implemented design, or improved representativeness. Randomization alone does not remove participation bias. External RAPPOR and differential-privacy explanations remain to be read.
- `privacy-issue-2824`: Advertisers seek attribution-window accuracy despite delayed reports; discussion identifies inference of browser inactivity and timing-based linkage, distinguishes event and aggregate reporting, and weighs noise against utility and delivery. Later follow-up favors scheduled report time without substantial random delay. Linked PCM debate explains how ordering and conversion bits can reconstruct identifiers. Qualification: Full supplied linked PCM thread read including the truncated span reread separately. Different privacy models must not be conflated; proposed noise is not a proven deployed mitigation, and final follow-up differs from early proposals.

## P12 — Confidentiality, credentials and session protection

Protect data and authentication material through suitable encryption, credential handling and session controls while stating the trust boundary those mechanisms protect.

**Include:** Transport and field encryption, encrypted local storage, key management, cookie security, unattended sessions, passwords and cryptographic protocol choices.

**Exclude:** Consent is P02/P03, and encryption is not assumed to prevent an authorized endpoint reading plaintext or to provide erasure.

**Examples:**

- `privacy-issue-2628`: A proposal to prevent HTTP browsing/posting exposure evolves into a redirect-to-HTTPS option. Initially intended off by default and possibly combined with archive encryption, it is later kept separate; the final reply reports the redirect option added and enabled by default. Qualification: The final default differs from the original proposal. The issue reports implementation but supplies no patch/runtime test; no actual interception event is established.
- `privacy-issue-17579`: A requester wants Secure-cookie defaults inferred from server TLS to avoid cookies failing over HTTP. Maintainers explain TLS termination at upstream proxies makes local HTTP insufficient to infer browser transport, and retain the secure default. Qualification: A configuration/usability disagreement, not demonstrated leakage. Six comments read, including lock notice.

## P13 — Usable controls and privacy-related compatibility

Keep privacy choices understandable and operable, and handle functionality affected by privacy controls without silently defeating those controls.

**Include:** Accessibility, responsive/localized control failures, overlay obstruction, storage and consent integration errors, browser restrictions and safe functional fallbacks.

**Exclude:** Notice wording alone is P01; a demonstrated processing bypass is P03. Compatibility symptoms do not establish data leakage.

**Examples:**

- `privacy-issue-18374`: French Signal settings truncate privacy, notification and advanced-setting labels on an iPhone SE with enlarged system text, making the choices difficult to understand. The discussion proposes multiline labels and dynamic cell heights rather than simply reducing text size. Qualification: All four linked screenshots were downloaded and visually inspected. They support label truncation, not failure of the underlying privacy toggles. A stale-bot comment is the final reply; the proposed layout change is not shown implemented.
- `privacy-issue-20525`: AMP integration with iubenda's cookie solution is requested; the reply says the third-party plugin already supports AMPforWP and points to configuration and integration instructions. Qualification: Support is reported in a reply; the screenshot, support conversation and external guides still require follow-up. No deployed site's consent enforcement has been observed.

## P14 — Privacy requirements and organizational responsibility

Translate privacy obligations and expectations into scoped requirements, responsibilities, review and maintenance work for a product or deployment.

**Include:** Readiness epics, legal/security assessment, compliance questions, operational guidance, role ownership and regulation-driven distribution requirements.

**Exclude:** Specific controls use their corresponding codes; participants legal interpretations and completed checklists are not independent compliance determinations.

**Examples:**

- `privacy-issue-4960`: A GDPR readiness issue groups consent to or refusal of personal-data storage, information, deletion, cookie disclosure and legal acceptance controls. The current checklist marks these complete but leaves Google opt-out unchecked. A comment additionally recommends readable policy, data export, self-service deletion, anonymization of unnecessary personal data and security maintenance. Qualification: Checklist completion is reported task status, not proof of legal compliance or verified enforcement. Export and anonymization recommendations in the comment are not demonstrated implemented. Linked child issues and whitepaper are not included in supplied content.
- `privacy-issue-14142`: An umbrella GDPR request develops into data inventory, customer access/export, erasure or anonymization with transaction-retention constraints, evidence of agreement, and extension-wide integration. Early third-party add-on work gives way to WordPress core integration; final comments report EDD2.9.2/2.9.3 release of initial functionality. Qualification: Read all71 primary comments. linked_1 is the same issue: title/body and all71 comment bodies compared exactly equal, with no differences; external_1 exactly equals the previously read record47 page. Cross-referenced rather than reread duplicates. Legal claims, purported anonymity and full compliance are not independently established. Images not inspected; textual updates support the interpretation.

## P15 — User access and portable exports

Provide people with access to usable copies of their data while defining export scope, format, usability and disclosure consequences.

**Include:** History export, data portability and access/export requirements explicitly distinguished from erasure.

**Exclude:** Internal logging is P08 and deletion alone is P09; export success does not establish encrypted or safely shared output.

**Examples:**

- `privacy-issue-14142`: An umbrella GDPR request develops into data inventory, customer access/export, erasure or anonymization with transaction-retention constraints, evidence of agreement, and extension-wide integration. Early third-party add-on work gives way to WordPress core integration; final comments report EDD2.9.2/2.9.3 release of initial functionality. Qualification: Read all71 primary comments. linked_1 is the same issue: title/body and all71 comment bodies compared exactly equal, with no differences; external_1 exactly equals the previously read record47 page. Cross-referenced rather than reread duplicates. Legal claims, purported anonymity and full compliance are not independently established. Images not inspected; textual updates support the interpretation.
- `privacy-issue-5577`: A GDPR epic groups portability, erasure, versioned policy acceptance, unbundled registration consent and opt-in newsletters into actionable feature proposals. Qualification: Checked tasks record tracker state, not independently verified compliance or implementation; closure includes a stale notice.

## P16 — Capability permissions and controlled execution

Bound the authority of applications, extensions, scripts and device capabilities, explaining or obtaining the permission needed for the intended function.

**Include:** Sensor and device permissions, privileged extensions, userscript isolation, imported script authority, installation approval and permission-purpose mismatches.

**Exclude:** Audience authorization is P10; processing-consent gating is P03. Platform permission, developer delegation and user consent remain distinct.

**Examples:**

- `privacy-issue-12607`: Bookmarks Organizer 2.0 took control of Firefox tracking protection to avoid false broken-bookmark reports, leaving the native privacy controls unavailable. The maintainer first proposed opt-in, later reported reverting the change in 2.0.1, and in 2023 abandoned reintroduction in favor of an explanatory notice. Qualification: Closure and current changelog cannot establish when a fix deployed; the rollback is a maintainer report. Opt-in was an abandoned proposal, not the recorded final implementation. The linked changelog is retrieval-time master, not a frozen 2018 snapshot.
- `privacy-issue-18585`: An image-loading library upgrade coincides with App Store rejection for missing photo-library usage description. A maintainer proposes changing the cache directory from Library to Library/Caches and later reports successful deployments, but a subsequent reporter still sees rejection after upgrading and suspects another library. Qualification: The warning does not prove actual photo access. The cache-path diagnosis is a maintainer attribution, not a verified common cause for the later report; the final comment prevents coding the entire thread as conclusively resolved.

## P17 — Evidence-qualified privacy assessment

Assess whether the supplied material establishes a privacy concern, and resolve or retain uncertainty by distinguishing reported claims from source evidence, configuration and actual behavior.

**Include:** Retracted allegations, disputed scanner findings, unsupported or underspecified reports, corrected causal attribution, support explanations that narrow an initial claim, and maintenance or integrity discussions whose supplied evidence does not establish a privacy defect.

**Exclude:** Not a miscellaneous defect code: preserve the concrete subject with another code where supported, and do not turn unresolved evidence into a confirmed vulnerability.

**Examples:**

- `privacy-issue-12157`: A reporter disputes documentation claiming filter-bucket information is sent to Bing Maps, and the documentation team reports updating the article. The later retrieved documentation distinguishes map types and excludes Size and Legend data from transmission. Qualification: GHArchive coverage is partial. The linked GitHub document is unavailable. The current external article was updated in 2026 and does not verify 2020 runtime behavior; its map-type conditions also qualify the reporter’s broad description. No actual filter-data leak is established.
- `privacy-issue-7666`: A user reports confusing add-on navigation, then alleges account/data misuse across several applications. Maintainers ask for specific locations and evidence and ultimately close the report as unclear and apparently unrelated to AMO. Qualification: Include the artifact without turning unsupported allegations into confirmed account compromise or data leakage. The primary body/comments have migrated addons URLs different from the original issue provenance; preserve both. No clear reproducible privacy mechanism is established.

## P18 — Privacy incident and safe reporting procedures

Prepare for, communicate or respond to privacy/security incidents and arrange reporting channels that avoid unnecessary further exposure.

**Include:** Incident templates, responsible contact channels, controlled diagnostic sharing and post-compromise response planning.

**Exclude:** Routine sanitizer changes are P08 and general compliance planning is P14. Planning a response does not establish an incident occurred.

**Examples:**

- `privacy-issue-12039`: The team gathers incident-response templates from government peers for application teams to use quickly during security/privacy incidents; completion comment reports related information stored in Compliance. Qualification: Preparation and reported collection, not an actual breach or proof the planned login-page form exists.
- `privacy-issue-21604`: Jupiter debugging raises disagreement about sharing real thesis metadata on public GitHub. Participants distinguish publicly licensed bibliographic metadata from account identifiers and email, report redacting data, and propose team guidance for external tools. Redaction can also remove the exact metadata needed to diagnose migration defects. Qualification: All19comments and linked509 read. License and FOIP claims are participant interpretations, not independent legal determinations. Linked509 documents visibility mapping problems and an unchecked post-migration audit; closure alone does not prove complete remediation. Internal issue unavailable; reported exposure there not independently verified.
