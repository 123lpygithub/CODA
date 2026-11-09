# Privacy — GPT6-1

All **652 artifacts** are included in **708 assignments** to **21 codes**: 20 substantive concern codes and one evidence-qualification code. **14 artifacts** receive the latter because a specific privacy issue is unsupported or corrected in the available record.

Categories were induced from direct reading of issue material. They describe concerns and implementation needs, whether proposed, contested, corrected or reportedly resolved. They do not label every issue as a confirmed privacy violation. One primary code identifies each case’s principal concern; additional codes capture explicitly distinct concerns in broader discussions. No fixed code-count cap or reference human categories were used.

`assignments.json` separates reviewed evidence from retained supplemental context and preserves case rationale, caveats, source locations and provenance. `results.json` retains the full supplied text for every artifact and the reviewed-field list. `taxonomy.json` uses a category/description/layer/children presentation compatible with the requested HOW-style organization; it is not a reproduction of HOW’s generation procedure.

| Code | Category | Primary artifacts | All supporting artifacts |
|---|---|---:|---:|
| P01 | Accurate data-practice disclosure | 61 | 69 |
| P02 | Accessible privacy information and controls | 60 | 62 |
| P03 | Meaningful and purpose-specific choice | 43 | 49 |
| P04 | Reliable consent state and audit trail | 19 | 22 |
| P05 | Consent-aware processing and propagation | 39 | 41 |
| P06 | Bounded and controllable telemetry | 43 | 44 |
| P07 | Data minimization and local persistence | 30 | 31 |
| P08 | Control over external services and requests | 40 | 42 |
| P09 | Effective de-identification | 45 | 47 |
| P10 | Safe diagnostic collection and sharing | 29 | 33 |
| P11 | Complete and usable erasure | 32 | 43 |
| P12 | Bounded retention and expiry | 16 | 21 |
| P13 | Context-appropriate access and visibility | 31 | 35 |
| P14 | Prevention of unintended disclosure | 21 | 21 |
| P15 | Confidentiality and authentication safeguards | 28 | 29 |
| P16 | Appropriate sensitive-resource permissions | 14 | 14 |
| P17 | Resistance to identification and linkability | 14 | 14 |
| P18 | Functionality under privacy constraints | 30 | 30 |
| P19 | Actionable privacy governance | 38 | 39 |
| P20 | Usable personal-data access and export | 5 | 8 |
| P21 | Privacy claim not established by available material | 14 | 14 |

Primary counts sum to 652. Supporting counts overlap where a case has more than one distinct concern. Group headings organize the codebook and are not assigned codes.

## P01 — Accurate data-practice disclosure

Privacy statements and operational documentation must explain actual collection, purposes, recipients, storage, controls and responsibilities.

**Include:** Missing or stale policies, misleading claims, undocumented SDK behavior, and explanations of privacy-related settings or tools.

**Exclude/boundary:** Use B when the content exists but cannot be found or read; C for choosing permission, and S for broader compliance planning.

**Supporting artifacts:** 69; primary in 61. Full IDs are in the structured codebook.

- `privacy-issue-12157`: Documentation reportedly overstated which fields go to Bing Maps; a maintainer says the article was corrected. Scope: Historical event archive may omit discussion; do not infer an actual filter-data disclosure.
- `privacy-issue-3719`: Sharing-count buttons expose IP and page URL through requests; privacy helper is updated after legal consultation. Scope: IP exposure occurs through transport even when not an explicit payload field.
- `privacy-issue-1625`: Matrix notice changes future optional encrypted-key-backup language to present supported behavior and specifies encrypted content. Scope: Statement concerns encrypted messages, not all content; loss of recovery keys remains relevant.

## P02 — Accessible privacy information and controls

Users need to find, read and operate privacy notices and controls across layouts, languages and assistive technologies.

**Include:** Broken links, missing notice placement, translations, clipped or obscured controls, contrast, navigation and responsive-layout failures.

**Exclude/boundary:** Use A for substantive disclosure accuracy, D for stored choice errors, and R for broader application breakage under protection.

**Supporting artifacts:** 62; primary in 60. Full IDs are in the structured codebook.

- `privacy-issue-8890`: A cookie banner blocks NVDA users in Firefox; both maintainer and reporter confirm accessibility after a later change. Scope: Browser-specific accessibility evidence does not establish all consent semantics.
- `privacy-issue-1950`: Privacy-notice footer link fails contrast requirements and is updated with a lighter link color. Scope: Accessibility fix improves notice readability, not data-processing behavior.
- `privacy-issue-1811`: Klaro privacy-policy link appears in a modal but is also needed directly in the initial notice. Scope: Existing modal configuration does not satisfy the requested placement.

## P03 — Meaningful and purpose-specific choice

Data use or publication requires an understandable user choice whose default, granularity, timing and withdrawal match the intended purpose.

**Include:** Opt-in versus opt-out, equal rejection, granular permissions, confirmation before publication, contact preferences and misleading action labels.

**Exclude/boundary:** Use F for telemetry-specific collection decisions; D for state/audit implementation and E for enforcing a choice on processing.

**Supporting artifacts:** 49; primary in 43. Full IDs are in the structured codebook.

- `privacy-issue-8843`: The banner should make decline as easy as accept, default nonessential tracking off, and save selective category preferences. Scope: Historical discussion records iterative designs, not independently verified runtime enforcement.
- `privacy-issue-2421`: Screenshot Save uploads whereas Download remains local, causing accidental disclosure; renaming and upload-disable preference are discussed. Scope: Later Firefox66 report still sees Save, so uniform label rollout is not established; guessing-resistant URLs are not no upload.
- `privacy-issue-18588`: Registration/settings checkbox lets users decide whether event team may use email for tokens and related messages. Scope: Requested UI control does not establish implemented enforcement or versioned consent records.

## P04 — Reliable consent state and audit trail

Consent must be represented, retained, revised and evidenced consistently through navigation, identity changes, scopes and policy revisions.

**Include:** Lost or conflicting consent cookies, repeated prompts, broken persistence, versioned acceptance records and re-consent.

**Exclude/boundary:** Use E for downstream enforcement or vendor/purpose propagation; a required checkbox alone is not an audit record.

**Supporting artifacts:** 22; primary in 19. Full IDs are in the structured codebook.

- `privacy-issue-8876`: Anonymous consent must persist, be revocable, synchronize with backend and transfer appropriately on registration while separating existing-account choices. Scope: Checked implementation tasks coexist with older design questions and a later integration error; notice-only cookies are distinguished from actual consent.
- `privacy-issue-14025`: Checkout stores consent date; discussion requests version/page and repeated acceptance history, with re-consent after updates still outstanding. Scope: Timestamp storage alone does not show complete versioned consent audit.
- `privacy-issue-14234`: MailChimp stores email/IP/time but requester needs exact checkbox wording agreed at that time. Scope: Required checkbox and timestamp do not by themselves preserve consent text history.

## P05 — Consent-aware processing and propagation

Data-processing components must receive and honor applicable permission before and after changes in user choice.

**Include:** Deferred initialization, tracking/script gating, consent strings, vendor and purpose rules, cross-component propagation and withdrawal enforcement.

**Exclude/boundary:** Use D for persistence within a choice store, F for general telemetry policy and R for functionality that breaks because protection is effective.

**Supporting artifacts:** 41; primary in 39. Full IDs are in the structured codebook.

- `privacy-issue-11537`: Privacy flags remove buyeruid but leave other user identifiers; the issue requests consistent removal across LMT/DNT, GDPR, COPPA and CCPA signals. Scope: A maintainer reports completion in Go and Java; no independent execution check.
- `privacy-issue-11653`: AMP adds CCPA remote consent state, opt-out links and region-specific gating alongside GDPR flows; discussion addresses cache synchronization and downstream ad signals. Scope: Dev-channel deployment and a corrected geoOverride configuration are reported; this does not establish every publisher implementation is compliant.
- `privacy-issue-7579`: Server-side mute still transmits microphone audio; client track disabling in 2.2.24 replaces it with silence. Scope: Original default did not record muted audio automatically; continuing silent network traffic after fix is not continuing speech disclosure.

## P06 — Bounded and controllable telemetry

Usage, diagnostic or behavioral measurement needs justified scope, understandable defaults and effective collection controls.

**Include:** Telemetry introduction/removal, opt-in defaults, opt-out ignored, scoped metrics, identifiers and data previews.

**Exclude/boundary:** Use J for sensitive diagnostic payloads or publication, G for nontelemetry minimization, and E for general consent-component plumbing.

**Supporting artifacts:** 44; primary in 43. Full IDs are in the structured codebook.

- `privacy-issue-5472`: The reporter requests analytics disabled by default and no opt-out event; maintainers investigate then close without public resolution details. Scope: Do not interpret closure as compliance or endorse participants' legal conclusions as established law.
- `privacy-issue-14194`: User objects to default-on analytics and absent preview; initial F-Droid-only proposal becomes reported opt-in for everyone in 0.8.9. Scope: Earlier comments misuse opt-in to mean enabled; final release statement supersedes distribution split.
- `privacy-issue-3643`: Default-enabled reporting prompts an audit of embedded trackers and sensitive crash fields. Maintainer testing of v1.5.70 reports no Mixpanel/Google/Doubleclick requests after opt-out; a balena.io static featured-project request remains and offline flashing works. Scope: Earlier v1.5.63 complaint is corrected by its reporter because reporting was still enabled. Analytics opt-out is not a no-network mode; opt-in-default debate is separate.

## P07 — Data minimization and local persistence

Collect or persist only information necessary for the stated function, at the required granularity and location.

**Include:** Unnecessary account fields, preinteraction cookies, localStorage alternatives, behavioral trails, memory-only storage and avoiding needless identifiers.

**Exclude/boundary:** Use L for expiry of already retained data, I for transformation of identifiers, and H for external recipients or services.

**Supporting artifacts:** 31; primary in 30. Full IDs are in the structured codebook.

- `privacy-issue-21382`: Telephone collection should be configurable or conditional on actual delivery/payment needs; participants debate global settings versus extension requirements. Scope: A configurable-field commit is described; legal and service-necessity claims remain participant assertions.
- `privacy-issue-8761`: Chat widget creates conversation tracking cookie before any interaction; proactive messaging and continuity are offered as rationale. Scope: User challenges necessity for never-engaged visitors; closure explicitly leaves requested change unimplemented.
- `privacy-issue-3841`: URL shortener should retain useful aggregates while removing IP, user-agent, referrer and excessive timestamp precision; separate submitter and visitor logs need coverage. Scope: Plugins differ in fields and effects; blanking redirect logs does not clear submitter IPs or old data.

## P08 — Control over external services and requests

Optional integrations, embedded resources and external processing must not create unexamined disclosure or dependence on third parties.

**Include:** Remote fonts, maps, favicons, link previews, updater calls, local/self-hosted alternatives, provider choice and data-region constraints.

**Exclude/boundary:** Use F for intentional telemetry, N for a concrete unintended recipient/content leak, and O for transport encryption itself.

**Supporting artifacts:** 42; primary in 40. Full IDs are in the structured codebook.

- `privacy-issue-21228`: Self-hosted users seek local PDF generation to avoid cloud processing and retain control over customer data; a local renderer solution is reported prepared for release. Scope: External-service legal restrictions are debated and disabling attachments is not equivalent to retaining full invoice workflow.
- `privacy-issue-18769`: Self-hosting fonts is requested to prevent IP disclosure; later reports include Google form and tracking requests despite telemetry disabled. Scope: Fix is reported for v0.104.0; scope should not be expanded to all future network traffic.
- `privacy-issue-15097`: SecureDrop external educational links may expose sources through traffic correlation or hostile sites; shorter internal explanations and removing links are favored. Scope: Some content is removed, with Tor2Web warning treated separately; Tor use does not eliminate every linkage risk.

## P09 — Effective de-identification

Masking, pseudonymization, aggregation or metadata removal must cover relevant fields and representations while preserving necessary utility.

**Include:** Incomplete scrubbing, indirect identifiers, stable mapping, export anonymization, spatial/time coarsening, synthetic replacements and operational failures of scrubbers.

**Exclude/boundary:** Use J for diagnostic-specific redaction, K for erasure, P for resource permission and Q for fingerprint defenses; pseudonymization is not assumed irreversible anonymity.

**Supporting artifacts:** 47; primary in 45. Full IDs are in the structured codebook.

- `privacy-issue-5005`: IP anonymization leaves full addresses in forwarded and real-IP headers; maintainer reports fix for both. Scope: Release is promised for next tag rather than confirmed deployed.
- `privacy-issue-4771`: GoAccess adds output-level IP masking while retaining raw internal distinctions for visitor counts; masking level is version-dependent. Scope: Output masking does not erase raw logs or guarantee anonymity of referrals or other panels.
- `privacy-issue-1019`: A fingerprint processor for anonymization must resist brute-force recovery and preserve stable mappings across distributed nodes. Scope: Ordinary content fingerprinting is explicitly different from anonymization; proposed keyed design is not released in this case.

## P10 — Safe diagnostic collection and sharing

Logs, error reports and support artifacts need sensitive-data filtering, appropriate destinations and review before disclosure.

**Include:** Credentials, identifying URLs or personal data in logs, safe logging defaults, synthetic reproductions and private/pre-upload diagnostic inspection.

**Exclude/boundary:** Use F for whether telemetry is collected, I for non-diagnostic de-identification, and L for retention duration alone.

**Supporting artifacts:** 33; primary in 29. Full IDs are in the structured codebook.

- `privacy-issue-3760`: Profiles expose identifying URLs in network resources, markers and source files; broader removal must preserve useful diagnostics. Scope: The issue describes remaining exposure despite an initial safeguard, not completed universal anonymization.
- `privacy-issue-4844`: Avatar troubleshooting exposes incomplete anonymisation of LDAP password and sensitive vCards/logs, prompting safer export request. Scope: Primary privacy phenomenon is diagnostic disclosure, separate from avatar failure; repetitive diagnostics inspected selectively, not every line.
- `privacy-issue-14156`: Linked patch moves sensitive authority, client, scope and error details into PII-designated logging calls, separates generic messages, and disables logcat by default. Scope: Patch is source evidence for logging classification/default changes, not a runtime audit of every possible sensitive field.

## P11 — Complete and usable erasure

Removing data requires an accessible request/action and coverage of related, derived, cached or distributed records within the supported scope.

**Include:** Account deletion, forgotten uploads, residual indexes/history, deletion versus deactivation, identity unlinking and erasure propagation.

**Exclude/boundary:** Use L for automatic age limits, I for retaining transformed records, T for access/export; local erasure does not prove removal of external copies.

**Supporting artifacts:** 43; primary in 32. Full IDs are in the structured codebook.

- `privacy-issue-11364`: Previously deleted repositories and account data remain indexed by a third-party service; a comment reports removal. Scope: Removal is asserted for requested records, not a general synchronization fix.
- `privacy-issue-6881`: Offline cache survives account changes and backend rules do not secure locally persisted records; users request safe clearing with pending-write/multitab handling. Scope: clearPersistence released6.2.0; GC5.7.0 is separate; manual schema edits unsafe and logout clearing does not fully secure shared OS accounts.
- `privacy-issue-5452`: Forum post purge leaves uploads; implementation checklist adds deletion and preservation option while account deletion already purges content. Scope: Orphan cleanup and account deletion have different scopes; historical orphan remediation not established.

## P12 — Bounded retention and expiry

Stored data needs an appropriate lifetime and cleanup process that respects operational and evidentiary constraints.

**Include:** Timed log/cache/post deletion, inactive-account cleanup, retention configuration and preserving necessary audit or transaction records.

**Exclude/boundary:** Use K for specific erasure actions and their completeness; use A when only retention wording changes.

**Supporting artifacts:** 21; primary in 16. Full IDs are in the structured codebook.

- `privacy-issue-3873`: The request proposes automatic expiry of load-balancer and CDN logs containing IP addresses after about fourteen days. Scope: Requested duration is not a confirmed operational policy.
- `privacy-issue-20535`: Request argues maxEntries alone permits indefinite cached personal data and proposes required or capped maxAgeSeconds. Scope: Developer legal assumptions and proposed numerical caps are not verified legal requirements or implementation.
- `privacy-issue-18336`: Mastodon users request timed post deletion to reduce footprint, balanced against moderation and UI complexity. Scope: Federated remote copies and screenshots cannot be guaranteed erased; duplicate closure leaves per-post scope disputed.

## P13 — Context-appropriate access and visibility

Who can discover, view or act on information must match role, account, tenant, audience and contextual sharing boundaries.

**Include:** Private profiles, role permissions, enumeration, search/index visibility, contextual enrollment and identity-sensitive audience selection.

**Exclude/boundary:** Use N for concrete wrong-recipient or unintended-output incidents, C for user agreement itself, and O for credential/cryptographic mechanisms.

**Supporting artifacts:** 35; primary in 31. Full IDs are in the structured codebook.

- `privacy-issue-21349`: Group-member names should be suppressed for ordinary members when the privacy flag is set while administrators retain access. Scope: A requested FERPA-related feature, not proof of legal compliance or implementation.
- `privacy-issue-13435`: Replay account identifiers could reveal players who disabled match-data sharing; maintainers intentionally avoid exploiting the alternate source. Scope: Technical availability does not imply permission to reconstruct withheld identities.
- `privacy-issue-14262`: Multi-journal submission should let users select roles while preserving journal-specific data boundaries and privacy notices; revised flow is reported merged. Scope: Shared installation/domain does not imply shared controllers or automatic authorization to enroll others.

## P14 — Prevention of unintended disclosure

Information must not escape through an unintended recipient, context, surface or inherited state.

**Include:** Wrong-recipient messages, cross-account collisions, exposed private URL/data, notification contents, shared-screen traces and accidental secret publication.

**Exclude/boundary:** Use M for general audience/access design, J for diagnostic payloads and H for intentional external-service architecture.

**Supporting artifacts:** 21; primary in 21. Full IDs are in the structured codebook.

- `privacy-issue-12057`: Browser copy/share uses a previous tab URL after opening another; reports, workarounds, reproduction attempts and a planned fix appear in the thread. Scope: Later non-reproduction is reported but no universal verified resolution is established.
- `privacy-issue-12109`: A mail builder retains recipients after an exception and can send the next customer's order to a previous recipient; finally/reset addresses state cleanup. Scope: Source-level fix and maintainer closure are reported; reporter did not perform an end-to-end retest.
- `privacy-issue-18411`: Password auto-type follows changed application focus and enters credentials into Slack; window-title revalidation is proposed. Scope: Proposal is not demonstrated deployed fix; target verification must precede typing.

## P15 — Confidentiality and authentication safeguards

Encryption, key handling, secure transport and authentication mechanisms must protect sensitive content and credentials under the relevant threat model.

**Include:** Field/database encryption, TLS, key exchange, credential storage/reveal, session protection and account recovery.

**Exclude/boundary:** Use M for authorization/audience policies; general integrity work without a privacy connection belongs in U.

**Supporting artifacts:** 29; primary in 28. Full IDs are in the structured codebook.

- `privacy-issue-3871`: Field-level encryption is implemented with migration of existing values and encrypted search restrictions. Scope: Advanced key management and rotation are not established as complete.
- `privacy-issue-7032`: Short-code file transfer's bespoke exchange requires human key verification; discussion leads to PAKE implementation in croc3.0. Scope: Reported PAKE adoption does not prove cryptographic audit or Wormhole wire compatibility; earlier claim public keys alone prevent MITM is contested.
- `privacy-issue-6858`: Database credentials use readily reversible encryption in CE; secure storage/master-password or OS authentication are debated for password reveal. Scope: Not literal plaintext as initially alleged; final verified comment does not describe what was verified.

## P16 — Appropriate sensitive-resource permissions

Access to device/browser capabilities must be necessary, correctly declared and understandable, with deliberate activation and suitable scope.

**Include:** Microphone, camera, contacts, location, sensor or privacy-settings permissions, least privilege and platform declaration failures.

**Exclude/boundary:** Use C for non-platform consent, Q for fingerprinting, and E where a privacy action fails to stop transmission.

**Supporting artifacts:** 14; primary in 14. Full IDs are in the structured codebook.

- `privacy-issue-15163`: XR policy naming raises whether broad access would implicitly authorize sensitive future capabilities; the discussion keeps core xr and contemplates separate policies for new sensitive features. Scope: Hypothetical eye-tracking policies are examples, not implemented features; closure requires no immediate spec edit.
- `privacy-issue-7659`: An iOS audio app crashes for privacy violation; the response directs enabling microphone permission in the exporter. Scope: A missing permission declaration is not evidence of unauthorized recording.
- `privacy-issue-18429`: Background photo upload uses platform location wakeups, prompting privacy and battery concerns and requests for clearer explanation. Scope: Coarse cell/WiFi location and GPS differ; discussion does not independently audit tracking absence or later battery regressions.

## P17 — Resistance to identification and linkability

Observable identifiers, timing or platform behavior must not unintentionally allow identification or correlation beyond the intended scope.

**Include:** Browser/API fingerprinting, identifying headers, anonymous transaction sets, cross-context identifiers and privacy-preserving linkage designs.

**Exclude/boundary:** Use I for data-set de-identification, M for directory enumeration and H for third-party network architecture.

**Supporting artifacts:** 14; primary in 14. Full IDs are in the structured codebook.

- `privacy-issue-4346`: Diagnosis keys can potentially be linked to patient identity if central parties collude; blind signatures are proposed to reduce reliance on organizational separation. Scope: Threat models differ and hashed/transient links limit some attacks; closure redirects discussion rather than confirms deployment or an actual attack.
- `privacy-issue-15180`: Modified canvas APIs expose distinctive exceptions and function behavior; fixes reduce technical leaks but known-pixel detection remains inherent to the discussed faking approach. Scope: Closure and newer-browser improvement do not mean universal undetectability.
- `privacy-issue-15248`: Audio API perturbation must cover sampled values and derived hashes while preserving performance and media playback. Scope: Multiple alpha limitations and later video regression are reported; release and follow-up fix do not prove universal resistance.

## P18 — Functionality under privacy constraints

Software must handle restricted storage, blocked tracking, masked environment information or privacy-oriented dependencies without breaking required functionality.

**Include:** Tracking protection compatibility, blocked-cookie authentication, masked timezone/OS, privacy component performance and privacy-related API/provider migration.

**Exclude/boundary:** Use B for notice/control layout, D for consent-state bugs, and E for failing to enforce rather than tolerate a restriction.

**Supporting artifacts:** 30; primary in 30. Full IDs are in the structured codebook.

- `privacy-issue-302`: Third-party cookie restrictions break embedded Shopify sessions; v16 adds storage-access flow, with manual cookie-enabling fallback where browsers still fail. Scope: HMAC query configuration and later missing shop parameter are distinct causes; release does not resolve all Safari failures.
- `privacy-issue-15131`: Fingerprint resistance reports UTC, causing calendar display mismatch; explicit timezone selection is proposed. Scope: Server timezone is not necessarily the user's timezone; automatic detection cannot recover deliberately withheld context.
- `privacy-issue-2102`: Email clients block tracking pixels; Gophish infers opened event when a link click occurs. Scope: An inferred open is not a directly observed pixel load, and missing open events do not mean unread mail.

## P19 — Actionable privacy governance

Teams translate privacy obligations and risks into scoped requirements, reviews, ownership, operational procedures or incident-response support.

**Include:** Compliance readiness, data inventory, children/jurisdiction requirements, processor review, standards alignment, breach templates and private reporting channels.

**Exclude/boundary:** Do not treat participant legal claims or checklists as certification; use a specific technical code when that is the principal concern.

**Supporting artifacts:** 39; primary in 38. Full IDs are in the structured codebook.

- `privacy-issue-12039`: The team collects templates to help application teams report security/privacy incidents; a comment reports collection and storage. Scope: Operational readiness, not a reported breach.
- `privacy-issue-5602`: Federated-service discussion covers disclosure, export, erasure, logs, retention and operator responsibilities; software features alone cannot cover external infrastructure. Scope: Participants contradict one another on jurisdiction and personal data; retain as compliance design discussion rather than legal conclusions.
- `privacy-issue-3856`: Provider-data project checks relevant standards and recognizes that some provider records contain PII despite initial assumption. Scope: Response favors access controls and guidelines; absence of identified mandate does not imply data is nonsensitive.

## P20 — Usable personal-data access and export

Users or operators need appropriately scoped access, copies or portable records of personal data and associated requests.

**Include:** Readable chat/data export, access requests, portability, authorized submission receipts and distinguishing access from erasure.

**Exclude/boundary:** Use I for privacy transformation of exports, M for access restrictions and K for erasure.

**Supporting artifacts:** 8; primary in 5. Full IDs are in the structured codebook.

- `privacy-issue-12177`: Users need confirmation of prior submissions without exposing a public applicant list; emailed copies are selected before broader authenticated access. Scope: Matching emails may identify candidate duplicates, not establish that applications are interchangeable.
- `privacy-issue-14015`: Users seek scoped readable chat exports for access, search and backup; a web/desktop export reaches development release, then discussion raises optional encryption/warnings. Scope: One-time export differs from continuous logging, mobile support and enforceable prevention of copying; those are not delivered by this issue.
- `privacy-issue-5489`: Standard wording using OR conflates two different user rights; discussion distinguishes UI features from operational procedures. Scope: Proposal/requirements discussion, not proof every application needs a specific UI or universal legal obligation.

## P21 — Privacy claim not established by available material

The supplied record does not substantiate a specific privacy issue, or explicitly corrects an initial privacy allegation.

**Include:** Vague complaints, irrelevant privacy mentions, withdrawn accusations, false-positive alerts and ordinary technical behavior with no demonstrated privacy mechanism.

**Exclude/boundary:** Use substantive concern codes for supported requests even if unimplemented; this category retains the case without manufacturing a privacy defect.

**Supporting artifacts:** 14; primary in 14. Full IDs are in the structured codebook.

- `privacy-issue-3700`: An automated IP-anonymization warning is explicitly dismissed as a bot failure. Scope: Do not code this as a confirmed identifying-data leak.
- `privacy-issue-7594`: iOS crash includes camera access; DeviceKit maintainer explains camera capabilities are hardcoded and require no camera access. Scope: Reporter accepts clarification; crash source remains unlocated and should not be attributed to DeviceKit. The pinned source excerpt confirms a hard-coded camera-capability lookup without camera access in that excerpt.
- `privacy-issue-7595`: Analytics allegation is retracted after reporter realizes inspector targeted documentation site, not library-consuming app. Scope: Dev dependency in repository is not proof of shipped runtime tracking.

## Method and limits

All 652 artifact records are coded. Available primary titles, bodies and discussions were reviewed; repetitive diagnostic blocks were inspected selectively where noted. Selected linked source excerpts were checked. Other supplemental material is retained but not claimed to have been read. Images referenced by Markdown were not independently visually inspected.

- Current retrievable discussions may include later changes and are not the original study historical snapshot; GH Archive records can be incomplete or contain conflicting context.
- Codes describe supported concerns, requests or discussions, not confirmed defects, legal determinations or independently verified remediation.
- P21 explicitly retains records whose supplied evidence does not establish a specific privacy issue. Full coding coverage is not equivalent to every artifact establishing a substantive defect.
- Quoted source contains participant claims; inclusion as evidence does not endorse those claims. Source patches are not runtime verification.
- This is one assistant analysis without an external LLM API or independent human validation. No human reference codebook or fixed category cap was used.

Coverage, source-text equality and references are checked programmatically. These checks do not constitute independent semantic review. Process notes and audits are stored outside Artifact under experiments/codebook-construction/direct-analysis/Privacy.
