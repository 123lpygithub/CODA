"""Assistant-authored categories and explicit case decisions; no text classifier."""
# Read all individual source-reading notes before writing these decisions.
# Codes express admitted work/limitations, not independent proof of an executed bug.
CATEGORIES = [
('IMP','Unfinished functionality','A named operation, workflow step, or output is absent, stubbed, disabled, or explicitly awaiting implementation.','Include pass/NotImplementedError, inactive drafts, or a concrete missing step.','Exclude extension of a functioning operation to additional input/backend combinations (EXT); absent tests (TST).'),
('EXT','Restricted supported cases','An implemented operation does not cover a stated input type, shape, backend, format, model family, or execution mode.','Include an explicit unsupported combination or requested generalization.','Exclude an entirely missing operation (IMP) and merely questioning whether an unspecified extension is needed (DES).'),
('REP','Incomplete or mismatched information representation','A data representation, interface contract, conversion, or persistence path loses information or cannot express the intended semantics.','Include omitted metadata, incompatible shapes/contracts, lossy reduction, and mismatched producer/consumer granularity.','Exclude changes motivated only by clearer organization (ARC) or naming (NAM); do not infer actual loss when only potential loss is documented.'),
('ALG','Behavioral or analytical correctness concern','The material identifies a specific discrepancy, faulty assumption, numerical hazard, or methodological problem in implemented computation or evaluation.','Include source-visible contradictions and explicitly reported incorrect behavior; retain conditionality and lack of execution evidence.','Exclude open-ended choices without a concrete discrepancy (DES), and missing precondition checks (VAL).'),
('VAL','Incomplete validation or failure handling','Required input, state, consistency, authorization, or failure conditions are insufficiently checked or handled.','Include omitted checks, overbroad exception handling, and missing recovery/error policy.','Exclude an unsupported input explicitly rejected by design (EXT); message clarity alone belongs to OBS.'),
('DES','Unresolved design or interpretation choice','The developer has not settled whether an algorithm, parameter policy, representation, or architectural alternative is appropriate.','Include genuine questions about meaning, necessity, tradeoffs, and correctness where no definite defect is established.','Exclude a concrete prescribed refactoring (ARC), a visible discrepancy (ALG), and a marker with no interpretable requested change (UNC).'),
('ARC','Structural simplification and responsibility placement','Existing behavior needs clearer abstraction, consolidation, decomposition, dependency separation, or placement.','Include duplicated logic, ad hoc wrappers, private-API coupling, circular dependencies, obsolete code cleanup, and moving responsibilities.','Exclude mere renaming (NAM), dependency-version migrations (DEP), and a new missing behavior (IMP).'),
('NAM','Unclear or inconsistent interface naming','Names, aliases, parameter terminology, or exposed method names inadequately communicate their role or differ across related interfaces.','Include renaming, constants/enums replacing magic identifiers, and ambiguous terminology.','Exclude substantive representation changes (REP) or an unsettled behavior rather than naming (DES).'),
('CFG','Inflexible configuration or defaults','A meaningful option, default, path, threshold, or resource setting is hardcoded, inaccessible, or disconnected from configuration.','Include exposing controls and replacing personal paths or architecture-specific constants with derived settings.','Exclude an unresolved choice of the right value without a request for configuration (DES); missing combinations belong to EXT.'),
('PER','Avoidable computation or memory cost','The material identifies redundant computation, costly representations, unnecessary transfers, or opportunities for parallelism, reuse, or reduced memory.','Include proposed optimizations without claiming a measured improvement.','Exclude resource correctness/lifecycle problems (RES) and replacing code solely for organization (ARC).'),
('TST','Insufficient verification coverage','Tests, assertions, examples used for verification, or checks of an implementation remain missing, disabled, weak, or unreliable.','Include untested paths, loose tolerances, broken fixtures, and required test expansion.','Exclude production validation (VAL) and scheduled retirement of a still-useful compatibility test (DEP).'),
('DOC','Incomplete documentation or examples','Explanations, API documentation, tutorials, usage examples, or instructions are missing, outdated, or inconsistent with the shown behavior.','Include module/docstring placeholders and proposed explanatory examples.','Exclude runtime diagnostics (OBS) and missing functional output (OUT).'),
('DEP','Dependency and version adaptation','Behavior relies on a compatibility workaround, historical dependency constraint, or planned version/API migration.','Include temporary aliases, legacy loaders, upstream limitations, and deferred cleanup after minimum-version changes.','Exclude generic coupling without version/dependency constraints (ARC); retain whether a workaround already functions.'),
('OUT','Incomplete result delivery or traceability','Computed results or their provenance are not adequately saved, exposed, visualized, or reported.','Include missing model/checkpoint persistence, evaluation exports, metadata lineage, and result visualization.','Exclude runtime warnings/logging (OBS), documentation (DOC), or a proposed data structure change with no delivery concern (REP).'),
('RES','Resource lifecycle and concurrent-state coordination','State ownership, cleanup, shutdown, asynchronous result routing, or concurrent access needs explicit coordination.','Include races, retained resources, thread-local state, and uncertain reference ownership.','Exclude solely performance-motivated allocation reductions without a lifecycle issue (PER).'),
('OBS','Insufficient or intrusive operational diagnostics','Warnings, errors, status messages, logging, or debug output inadequately support operation or require cleanup.','Include missing/incorrect messages, overly generic exception types, and temporary debug prints.','Exclude validation logic itself (VAL), analytical result reporting (OUT), or explanatory documentation (DOC).'),
('UNC','Unspecified remaining work','A supplied TODO or similar marker does not identify enough remaining behavior to support a more specific work category.','Use only when surrounding source still leaves the intended change indeterminate; retain the concrete context in the case rationale.','Exclude interpretable alternatives (DES), named missing functionality (IMP), or explanatory comments without outstanding work (EXPL).'),
('EXPL','Implemented behavior without established remaining work','The selected comment describes an implemented safeguard, constraint, transformation, or educational instruction, without establishing outstanding maintenance work in the supplied context.','Include explanatory XXX/maybe comments, implemented requested-looking operations, and explicit teaching scaffolds.','Exclude active compatibility debt with a stated migration/removal dependency (DEP) and unknown TODO intent (UNC).'),
]

# Each row names its first corpus index, then one explicit judgment per artifact.
# Plus joins distinct supported concerns. This is not keyword matching.
DECISIONS = '''
0 ARC DES IMP EXPL ALG ARC EXT EXT PER IMP
10 IMP IMP ARC DES EXPL IMP CFG CFG TST NAM
20 TST EXT REP PER IMP DEP DEP ARC DES DEP
30 UNC DES DES OBS DOC DES DES DOC OBS DES
40 ARC ARC EXT IMP IMP REP TST TST REP IMP
50 UNC CFG DEP TST DOC DES DES EXT IMP REP
60 EXPL UNC ARC IMP ARC DEP DES VAL IMP DES
70 EXT ARC+TST DES ARC REP NAM TST IMP+DOC IMP+DOC EXT
80 DES CFG ARC DES ARC PER EXPL DEP CFG IMP
90 TST PER DES EXT ARC TST DES ARC DES DES
100 VAL EXT ARC VAL EXT EXT EXT DES ARC CFG
110 DES ARC EXT VAL IMP PER EXPL EXT DES EXT
120 REP RES IMP DEP DEP ARC TST TST OUT DES
130 DES ALG ARC TST PER EXT ARC OUT ARC DOC
140 OUT NAM DEP IMP ALG CFG EXPL IMP OBS IMP
150 RES DES TST EXT DOC DEP EXT ARC EXT DES
160 CFG EXT OBS EXT EXT DES EXPL EXT DES DES
170 CFG IMP TST ARC UNC DES DES PER IMP+VAL EXT
180 DES IMP UNC IMP DES DEP VAL DES DES OBS
190 DEP ARC DES UNC REP CFG ARC EXT DES TST
200 PER ALG EXT DEP ARC NAM VAL VAL VAL DES
210 DES DES CFG IMP IMP ARC NAM REP RES CFG
220 ARC DES EXT DEP DES ARC DES UNC ARC DES
230 DES ARC DES DES IMP PER ARC DES CFG EXT
240 EXT IMP REP DES DEP DEP DOC IMP IMP DES
250 IMP DEP OBS DOC REP OUT UNC DES PER EXT
260 EXT EXT NAM EXT IMP ARC DES ARC REP EXT
270 ARC IMP DOC ALG EXPL DES OUT RES ARC EXT
280 DEP CFG EXT IMP EXT DEP DES CFG EXT CFG
290 PER EXPL PER DEP ARC IMP VAL EXPL DES REP
300 OUT EXPL ALG EXPL ARC DES TST ARC DEP IMP
310 ARC ARC ARC+TST ARC NAM RES RES REP DES EXPL
320 REP UNC EXT IMP+VAL RES ARC CFG IMP TST EXT
330 EXT REP IMP DES EXT VAL PER REP DES PER
340 DOC ARC VAL EXT EXT NAM ALG UNC IMP ARC
350 CFG EXT EXT PER DEP OBS REP DES IMP DES
360 EXT TST CFG DOC PER DEP ARC TST DEP ARC
370 ARC REP REP ALG ARC EXT ALG IMP REP IMP
380 IMP OUT IMP EXT VAL DES DES REP ALG PER
390 EXPL DES TST IMP DEP EXT DEP IMP DES DEP
400 ARC TST EXT ARC REP TST DEP EXPL UNC IMP
410 OUT DES OUT EXPL DEP ALG DEP PER DEP DEP
420 PER CFG REP DES EXT DES NAM EXPL DES DES
430 EXT DES IMP EXT IMP DES DES DES REP UNC
440 DES OBS OBS DES DES UNC ARC VAL IMP ARC
450 UNC IMP EXT DEP EXPL DES DEP DES EXT UNC
460 DES TST DES PER VAL EXT ARC ALG EXT UNC
470 DES TST DEP IMP DEP DOC EXT ALG DEP DEP
480 ARC CFG ARC IMP PER REP DES OUT ARC ALG
490 TST ARC ALG OUT ARC DEP OUT NAM DES EXT
500 REP DES RES NAM DES IMP DES EXT ALG IMP
510 NAM EXT ARC ARC TST ARC EXPL NAM EXT EXPL
520 EXT VAL NAM ARC DES DOC PER EXT ARC PER
530 REP ARC TST RES REP ARC DES DES DEP EXT
540 UNC DEP EXPL OUT IMP ARC PER DES DES TST
550 DEP DES OUT CFG ALG EXPL ARC ARC CFG DES
560 OUT ALG CFG ARC TST TST EXT DEP PER RES
570 PER PER ARC TST ALG IMP EXT IMP TST DEP
580 TST PER ALG IMP DES EXT EXT ALG DES DEP
590 EXT EXT OUT EXT EXT EXT VAL DES REP REP
600 NAM ARC ARC DEP PER NAM DES IMP DES ARC
610 REP CFG UNC TST DEP ALG PER VAL ARC IMP+DOC
620 REP RES DEP REP TST VAL OBS TST EXPL UNC
630 IMP EXT ALG DES REP ARC TST CFG EXT+TST EXPL
640 DES IMP OUT OBS ALG DEP TST DES DES TST
650 UNC REP UNC IMP DEP ARC PER PER ARC TST
660 PER DEP TST DES EXT EXT ALG EXT TST ARC
670 DEP REP EXT TST VAL DES EXPL ARC PER ARC
680 IMP DEP DOC TST EXPL DEP OUT TST REP DES
690 OBS IMP EXT ARC ALG DOC PER DES DES EXPL
700 ALG ARC ARC ARC VAL ARC DES TST TST ARC
710 EXT ARC TST DEP DES EXT PER VAL NAM ARC
720 VAL EXPL OUT EXT REP UNC ARC ARC ARC TST
730 TST IMP VAL ARC EXT DES DES DES PER EXT
740 ARC DES ARC DOC DEP NAM OUT EXT NAM PER
750 NAM EXPL REP EXT NAM EXT+PER PER DES IMP REP
760 ARC EXPL ARC DES PER EXT IMP TST CFG DEP
770 ARC EXT CFG ARC IMP NAM ALG EXT NAM UNC
780 DES DES IMP PER EXT EXT IMP DES EXT DEP
790 OUT EXPL NAM DES EXT PER OUT IMP UNC ARC
800 EXPL PER REP TST EXT ALG TST EXT ARC DES
810 ALG IMP VAL TST EXPL OBS OBS ARC ARC NAM
820 EXT TST EXT EXT IMP TST DEP DES DEP DES
830 ARC DES ARC PER EXT RES TST EXPL DES DES
840 ALG EXT EXT REP ALG OUT EXT ARC VAL ALG
850 DES PER EXT IMP REP EXT
'''

def decisions():
    result = {}
    for line in DECISIONS.strip().splitlines():
        start, *codes = line.split()
        for offset, code in enumerate(codes):
            index = int(start) + offset
            assert index not in result, index
            result[index] = code.split('+')
    # Explicit corrections after reading each displayed assignment beside its note.
    corrections = {
        8:'REP+PER',9:'PER',105:'DEP',124:'ARC',125:'DEP',126:'ARC',128:'TST',129:'OUT',
        141:'REP',167:'EXPL',168:'EXT',174:'ARC',175:'UNC',207:'DES',219:'ARC',232:'ARC',
        261:'NAM',262:'EXT',315:'RES',326:'EXT',327:'CFG',328:'IMP',329:'TST',
        367:'ARC',368:'TST',369:'ALG',377:'DES',378:'IMP+ALG',379:'REP',428:'ARC',
        485:'EXPL',515:'EXT+ARC',530:'REP',569:'TST',653:'EXT',665:'EXT',
        772:'CFG+REP',776:'DOC',792:'DES',839:'NAM',853:'IMP'
    }
    for index, codes in corrections.items():
        result[index] = codes.split('+')
    assert set(result) == set(range(856))
    allowed = {row[0] for row in CATEGORIES}
    assert all(set(codes) <= allowed for codes in result.values())
    return result
