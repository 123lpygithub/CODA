"""Explicitly authored consolidation after reading the supplied Privacy corpus.

The table is a case-by-case decision record, not a classifier. Integer labels
only abbreviate the authored category identifiers; no text matching is used.
"""
CATEGORIES = [
('P01','Privacy notices and accurate disclosure',
 'Provide accessible, understandable and current explanations of data handling, recipients, purposes and controls, or correct inconsistencies between those explanations and the stated practice.',
 'Policy text, links, localization, permission-purpose explanations, cookie inventories and misleading disclosure wording.',
 'Use P02 for capturing or revisiting a decision, P03 for enforcing it, and P14 for broader organizational readiness rather than notice content.'),
('P02','Explicit choices and durable preference management',
 'Let people make, save, revisit and withdraw purpose-appropriate privacy choices, with a clear distinction between acknowledgement, dismissal and permission.',
 'Accept/reject controls, consent records and versions, preference persistence and scope, re-prompting, and optional communications.',
 'A banner alone is P01. Actual gating of processing is P03; broader telemetry collection/default debates are P04.'),
('P03','Enforcing privacy choices across processing paths',
 'Carry the applicable privacy preference to every relevant processing path and act on it, including initialization, integrations, revocation and state transitions.',
 'Pre-consent script/SDK loading, processing after opt-out, shared consent signals, purpose-specific filtering and inconsistent enforcement between components.',
 'Saving or displaying preferences without evidence about processing is P02. Signal transmission is not assumed to establish downstream compliance.'),
('P04','Telemetry scope, defaults and participation',
 'Decide whether and how operational or usage telemetry is collected, making its scope, defaults, participation controls and diagnostic value explicit.',
 'Default-on versus opt-in analytics, telemetry inventories, identifier choices, inspection of payloads, and deciding to introduce, remove or limit collection.',
 'Ordinary third-party resource loading is P05; a specific sanitizer failure is P08; a concrete failure to honor an established choice additionally belongs to P03.'),
('P05','Control over external services and data destinations',
 'Reduce or make deliberate the disclosure and dependency created by external services, network requests or hosting choices, including local alternatives.',
 'Remote fonts/media/rendering, cloud and DNS endpoints, service-provider trust, self-hosting and documented regional storage concerns.',
 'Encryption of a connection is P12. An external request is not automatically tracking, and provider replacement is not automatically anonymity.'),
('P06','Limiting collection and unnecessary detail',
 'Avoid collecting or exposing more data than the stated function requires, balancing utility with the necessity of fields, precision and identifiers.',
 'Optional personal fields, eliminating unnecessary events, reduced geographic detail, minimal public/session data and rejecting invasive feature proposals.',
 'Transforming existing identifiers is P07; time-based removal is P09; authorization by audience is P10.'),
('P07','De-identification coverage and utility',
 'Remove, mask, replace or coarsen identifying information while preserving the required structure or analytical utility, and examine the limits of that transformation.',
 'Anonymization/pseudonymization tools, metadata stripping, stable mappings, overlooked fields/formats, hash limitations and transformation compatibility.',
 'Log/debug-specific sanitation is P08. Masking is not assumed to erase originals or guarantee resistance to re-identification.'),
('P08','Sensitive information in diagnostics and derived outputs',
 'Prevent diagnostic or derived operational records from disclosing sensitive values, including secondary copies, reconstructed fields and publication workflows.',
 'Logs, crash reports, stack traces, telemetry URLs, metadata in debug profiles, public troubleshooting material and configurable sanitation hooks.',
 'Collection-policy disputes without a specific output concern are P04. General data anonymization is P07 and deletion schedules are P09.'),
('P09','Retention, erasure and residual copies',
 'Control how long information remains and what deletion actually removes across related records, local caches, remote copies and retained historical context.',
 'Account/content deletion, automatic expiration, anonymization as an erasure alternative, log retention, browser history, local persistence and cascade boundaries.',
 'Portable copies for user access are P15. Concealing a view or closing an account is not assumed to erase the underlying data.'),
('P10','Audience boundaries and authorized disclosure',
 'Restrict who can receive, discover or view information and preserve that audience boundary across routes, derived views, identities and state changes.',
 'Private fields/profiles, recipient selection, role restrictions, cross-user leakage, search visibility, sharing safeguards and federation access boundaries.',
 'Inference through otherwise available identifiers or observations is P11. A hidden control or unguessable URL is not assumed to enforce authorization.'),
('P11','Linkability, inference and fingerprinting',
 'Examine or reduce the ability to infer identity, membership, activity or sensitive attributes by linking identifiers, observable behavior or technical characteristics.',
 'Browser/device fingerprints, account enumeration, transaction/vote linkage, activity-status inference and stable identifiers that defeat pseudonymous presentation.',
 'Direct unauthorized content delivery is P10. Randomization, hashes or pseudonyms do not alone establish anonymity.'),
('P12','Confidentiality, credentials and session protection',
 'Protect data and authentication material through suitable encryption, credential handling and session controls while stating the trust boundary those mechanisms protect.',
 'Transport and field encryption, encrypted local storage, key management, cookie security, unattended sessions, passwords and cryptographic protocol choices.',
 'Consent is P02/P03, and encryption is not assumed to prevent an authorized endpoint reading plaintext or to provide erasure.'),
('P13','Usable controls and privacy-related compatibility',
 'Keep privacy choices understandable and operable, and handle functionality affected by privacy controls without silently defeating those controls.',
 'Accessibility, responsive/localized control failures, overlay obstruction, storage and consent integration errors, browser restrictions and safe functional fallbacks.',
 'Notice wording alone is P01; a demonstrated processing bypass is P03. Compatibility symptoms do not establish data leakage.'),
('P14','Privacy requirements and organizational responsibility',
 'Translate privacy obligations and expectations into scoped requirements, responsibilities, review and maintenance work for a product or deployment.',
 'Readiness epics, legal/security assessment, compliance questions, operational guidance, role ownership and regulation-driven distribution requirements.',
 'Specific controls use their corresponding codes; participants legal interpretations and completed checklists are not independent compliance determinations.'),
('P15','User access and portable exports',
 'Provide people with access to usable copies of their data while defining export scope, format, usability and disclosure consequences.',
 'History export, data portability and access/export requirements explicitly distinguished from erasure.',
 'Internal logging is P08 and deletion alone is P09; export success does not establish encrypted or safely shared output.'),
('P16','Capability permissions and controlled execution',
 'Bound the authority of applications, extensions, scripts and device capabilities, explaining or obtaining the permission needed for the intended function.',
 'Sensor and device permissions, privileged extensions, userscript isolation, imported script authority, installation approval and permission-purpose mismatches.',
 'Audience authorization is P10; processing-consent gating is P03. Platform permission, developer delegation and user consent remain distinct.'),
('P17','Evidence-qualified privacy assessment',
 'Assess whether the supplied material establishes a privacy concern, and resolve or retain uncertainty by distinguishing reported claims from source evidence, configuration and actual behavior.',
 'Retracted allegations, disputed scanner findings, unsupported or underspecified reports, corrected causal attribution, support explanations that narrow an initial claim, and maintenance or integrity discussions whose supplied evidence does not establish a privacy defect.',
 'Not a miscellaneous defect code: preserve the concrete subject with another code where supported, and do not turn unresolved evidence into a confirmed vulnerability.'),
('P18','Privacy incident and safe reporting procedures',
 'Prepare for, communicate or respond to privacy/security incidents and arrange reporting channels that avoid unnecessary further exposure.',
 'Incident templates, responsible contact channels, controlled diagnostic sharing and post-compromise response planning.',
 'Routine sanitizer changes are P08 and general compliance planning is P14. Planning a response does not establish an incident occurred.')
]

# Each row: source index : explicitly selected code numbers.
AUTHORED = '''
0:3,16
1:7
2:3
3:13
4:9
5:1
6:8
7:3,13
8:7,9
9:4,11
10:1
11:1,17
12:10
13:3
14:1
15:13
16:12
17:17
18:2,3
19:2,13
20:1
21:2
22:1
23:1
24:10
25:10
26:4,3
27:9
28:10,8
29:13
30:7,13
31:16,17
32:14,9
33:5
34:16
35:10,9
36:9
37:8
38:9,13
39:9
40:12,13
41:9
42:4,2
43:4,3
44:18
45:3,6
46:3
47:4,1
48:1
49:1
50:1,5
51:11
52:12
53:9,10
54:14,9,15
55:6
56:12,13
57:7
58:12
59:1
60:7
61:3
62:7
63:11
64:9
65:16,13
66:4,7
67:10
68:14,3,9
69:1
70:6
71:8
72:4,3
73:6
74:7
75:2,3
76:2,3
77:12
78:7
79:8,3
80:16,17
81:13,17
82:7,3
83:9,1
84:9
85:13
86:1
87:1
88:1
89:10
90:3,16
91:9
92:8
93:17
94:2,3
95:11
96:4,17
97:5,8
98:13
99:6,7
100:1
101:11
102:1,2
103:8,18
104:1,17
105:5
106:7
107:4,1
108:13
109:4
110:1,13
111:6,7
112:2
113:10
114:6
115:13,3
116:3,17
117:10
118:13,17
119:10
120:2
121:1
122:1
123:9
124:5,4
125:13
126:5
127:5
128:2,9
129:8
130:1,17
131:3
132:11
133:14,13
134:14
135:11
136:14
137:2,3
138:9,5
139:4,6
140:14,2,9,15
141:6
142:7
143:4,1
144:8
145:16
146:4
147:2,17
148:1,2
149:7,1
150:9
151:13
152:16
153:9
154:2
155:7,13
156:3,13
157:9
158:12
159:1
160:10,11
161:6,9
162:5
163:2
164:5
165:4,9,1
166:17,12
167:9,17
168:2
169:1
170:13
171:14,1
172:10,15
173:10
174:13
175:14,13
176:2,3
177:14
178:12,17
179:4,3
180:13
181:2,3
182:10
183:1
184:5
185:3,5
186:7
187:9,16
188:1,2
189:9,7
190:3,9
191:17
192:9
193:2,3
194:13
195:9,17
196:15,12
197:1,13
198:2,6
199:5,17
200:13,3
201:3,10
202:5,13
203:12,13
204:5
205:3
206:10
207:10
208:1,2
209:5,6
210:13
211:13,5
212:14,9
213:14,5
214:17,5
215:1
216:1
217:9
218:2
219:13
220:4,1
221:14,6,9
222:7
223:6,4
224:7,10
225:7
226:2,10
227:5,12
228:13
229:1
230:13,2
231:13,17
232:9
233:7
234:7
235:4,14
236:13
237:10,14
238:1,13
239:3
240:7
241:9,13
242:5
243:2,14
244:7
245:4
246:10,17
247:3
248:2
249:5,14
250:1,13
251:2
252:7,13
253:1
254:2
255:7
256:16,17
257:1
258:16,13
259:12,9
260:4
261:1,17
262:1
263:3,5
264:1
265:14,6,9
266:4,1
267:1
268:10,6
269:4
270:2,3
271:5,17
272:12,5
273:1
274:13
275:1,17
276:10
277:12,16
278:4,17
279:7
280:2
281:4
282:11
283:8
284:5,2
285:3,17
286:1,6
287:5
288:6
289:8,17
290:12
291:1,13
292:1
293:7
294:12
295:1,2,3
296:13
297:11,12
298:12
299:7,10
300:1,5
301:5
302:5
303:5,13
304:10
305:9
306:5
307:7
308:1
309:2,17
310:14,9
311:12,9
312:11,7
313:10
314:2
315:13,17
316:10,12
317:7
318:7,10
319:13,12
320:3
321:2
322:8,9
323:9
324:8
325:10,16
326:2,9
327:9,2
328:3,2
329:10,17
330:2
331:9,7
332:10
333:1,4
334:17,6
335:9,1
336:2,13
337:5,17
338:1
339:3,13
340:9,1
341:17
342:1,17
343:2
344:7,1
345:3
346:12,13
347:5,12
348:10
349:8
350:7,14
351:1
352:5,10
353:10
354:13,17
355:9
356:9,10
357:10
358:2
359:10
360:16,6
361:10
362:2
363:1
364:10
365:2
366:3
367:5
368:1
369:11
370:2
371:10
372:2
373:7
374:2,13
375:13,17
376:8
377:12
378:14
379:10
380:1
381:9
382:12
383:2
384:2,1
385:1,10
386:9
387:4,1
388:4,1
389:4
390:4
391:14,17
392:17
393:1,14
394:1
395:14
396:9
397:9
398:10,11
399:7,10
400:9,14
401:15,9
402:11
403:4
404:5,10
405:11
406:3
407:17
408:7
409:1
410:1,2
411:11
412:14
413:9,7
414:5,17
415:14,17
416:5,12
417:4
418:13,3
419:1,5
420:4
421:11,17
422:4,11
423:5,17
424:2
425:1,2
426:5,17
427:10,9
428:12
429:6,13
430:4,3
431:7,11
432:1
433:13
434:1,4
435:7
436:1,7
437:9
438:9
439:13
440:1,14
441:1
442:9,12
443:7
444:2,14
445:11,6
446:17,5
447:13,17
448:8
449:2,3
450:9,13
451:2,1
452:8
453:1,10
454:14,2
455:8,14
456:7,13
457:1,13
458:4
459:13,2
460:17
461:4
462:1
463:2
464:2,1
465:12
466:9
467:5,1
468:5
469:1
470:9,3
471:9
472:10,17
473:13
474:9
475:5,3
476:13,4
477:9
478:2
479:11
480:14,9,15
481:14,17
482:4,3,5
483:16,1
484:4,8
485:9
486:18,12
487:3
488:9
489:4,8
490:13
491:10
492:8,18
493:4,1
494:1,4
495:1,9
496:14,13
497:10,9
498:1
499:12,13
500:1,10
501:5,17
502:13
503:16,13
504:1
505:16,13
506:6,13
507:11,16
508:8,18
509:1
510:12,6
511:6
512:13,2
513:1,10
514:2,13
515:1
516:1,17
517:18,8
518:1
519:4,1
520:16,17
521:12
522:8,10
523:10,13
524:13,3
525:1
526:1
527:2,13
528:7
529:8
530:1,9
531:2
532:10,9
533:7
534:3,2
535:17
536:6,11
537:13,3
538:7
539:1
540:1,11
541:12,13
542:11,6
543:13,17
544:7
545:8
546:3,5
547:13,11
548:3
549:5,3
550:5
551:7,17
552:1
553:14,9
554:1
555:9
556:13
557:3,6
558:7,13
559:14
560:5
561:3,16
562:11,7
563:13,2
564:3
565:1,6
566:14
567:1,5
568:3
569:1
570:1,13
571:8,17
572:10
573:16,1
574:1
575:14
576:9
577:1,4
578:3,4
579:3
580:4
581:2,14
582:2
583:16,1
584:1,2
585:1
586:10,12
587:1,2
588:4,3
589:3
590:8
591:14,13
592:8
593:8,13
594:9
595:7
596:3,4
597:7,8
598:6,17
599:6
600:12,14
601:1,14
602:7,10
603:2
604:18
605:1,12
606:5
607:1,12
608:1
609:6,16
610:2,17
611:17,4
612:10,2
613:5
614:18
615:4
616:9,10
617:12
618:1
619:1,17
620:4,1
621:17,11
622:10,14
623:16,1
624:13
625:12
626:9
627:1
628:9,11
629:8,1
630:9
631:2,3
632:13,10
633:3
634:2,3
635:2
636:8
637:12
638:11
639:7
640:13,17
641:11,14
642:4,2
643:5,1
644:6,9
645:4,17
646:6,14
647:14
648:9
649:2,3
650:10,6
651:2
'''

def decisions():
    result = {}
    for row in AUTHORED.strip().splitlines():
        index, labels = row.split(':')
        index = int(index)
        assert index not in result
        result[index] = [f'P{int(label):02}' for label in labels.split(',')]
    assert set(result) == set(range(652))
    assert all(len(v) == len(set(v)) for v in result.values())
    return result
