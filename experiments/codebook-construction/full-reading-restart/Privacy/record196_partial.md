# Privacy index 196 — partial reading, not a completed note

Main issue and linked_1 were fully read before this continuation. linked_2 (32-commit Seshat patch) and linked_3/linked_4 are now fully read. linked_5 duplicates the main issue body and all 118 comments exactly: see record196_linked5_duplicates.json. linked_6 fully read. linked_7 read through character 168000 of 4331929, with an overlapping re-read at 79000–108000 to recover a truncated display. External_1 remains unread.

## Additional observations

- Seshat patch 06 fixes delete-case fallthrough; patch 09 actually enables encryption using a literal DEFAULT_PASSPHRASE. This is not evidence of a securely managed secret. Patch 10 removes per-user scope; patch 11 distinguishes close/null from directory deletion; do not mistake intermediate changes for current deployed behavior.
- Later Seshat documentation says official releases will build native modules from source but release integration is still pending and native features are disabled by default. Search/indexing in encrypted rooms is distinct from end-user export.
- linked_3 reports full room history download available within export; linked_6 reports JSON event export fixed, without supplying that fix here.
- Seshat historical JS file exposes database encryption as optional passphrase config, deletion/shutdown, passphrase change, indexing/recovery and loadFileEvents. It does not alone prove a general chat export UI or the case-time version.
- linked_7 patches 1–22 build HTML export, reply links, attachments/decryption, media support, sanitization, Firefox stream polyfill and export classes. Early HTML interpolation and reply handling change over time; do not characterize the final implementation before reading later patches.
- Patch 23 replaces custom HTML with existing React event components, suppresses live interactions/read receipts/URL previews, and starts using original source URLs for media. Its old exporter deletion has been read. New exporter has been read through the opening of exportCSS.ts, where the next chunk begins inside minified CSS. Full patch history remains unfinished.

## Interpretation to retain when finalizing

Usable, selectable per-room/date/format data export, with accessibility barriers to external tools and client resource constraints. Exported plaintext confidentiality and user warnings are a separate concern. The requester withdraws blocking/enforcement of export but retains optional encryption/warning. Discussion closure and a user report of development-build success do not establish universal release/platform availability or legal compliance.

## Further continuation

External_1 fully read: modern MDN File System API snapshot, secure contexts, user-permitted filesystem handles, OPFS distinction, asynchronous writable streams and dedicated-worker sync handles. Do not infer 2021 browser support from 2026 documentation.

linked_7 additional range 589794–645794 read (patches 24–31 and start of 32); the initial minified CSS remains mostly unread. Exact-reconstructable CSS fragment map saved, unique-fragment display read 0–26000 only. Patches 25–29 add local media/avatars and encrypted voice/non-media attachment handling after earlier remote URLs. Patch30 uses attachment names/timestamps and exports icons. These remain intermediate revisions.

Patches32–91: replies/media/redaction, room/exporter metadata, backward pagination and decryption, text/JSON/HTML formats, streaming ZIP (not encryption), cancellation, right-panel export controls. Attachments default false, 100 messages,8MB; UI choices differ from internal start-date capability. JSON uses decrypted content. No execution or deployment verification. Next patch92 warning modal. Non-CSS blocks view read229051–512051; patches32–39 covered by alternate view146430–182430.

Non-CSS patches through176 fully read. Patch92 warning is cancellation, not confidentiality.113 fixes JSON via JSON.stringify.139 replaces streaming ZIP with JSZip+file-saver;143 size maximum2000MB;147 comments out startDate;148 corrects MB/byte comparison.152 corrects Blob construction.168 renders text DOM for linkification with listener gating;170 HTML chunks1000events.172 uses light theme and lazy JSZip. Tests are supplied, not executed. CSS diffs remain unread.
