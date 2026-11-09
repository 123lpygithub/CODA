import {
  ArrowRight,
  Check,
  CircleAlert,
  FilePenLine,
  ListChecks,
  LoaderCircle,
  Pause,
  Play,
  Plus,
  Send,
  Trash2,
} from 'lucide-react'
import { useEffect, useId, useRef, useState } from 'react'
import type {
  Code,
  Codebook,
  CodebookAction,
  CodebookChangePacket,
  CodebookChangeInput,
  EvidenceItem,
  HumanDecision,
  ProvisionalCode,
  ReviewPacket,
} from './types'
import { useLanguage } from './i18n'

interface DraftCode {
  localId: string
  code_id: string
  name: string
  definition: string
  inclusion_criteria: string[]
  exclusion_criteria: string[]
  representative_artifact_ids: string[]
  boundary_artifact_ids: string[]
  counterexample_status: Code['counterexample_status']
  hypothetical_examples: string[]
  parent_code_id: string | null
  status: Code['status']
  notes: string[]
  metadata: Record<string, unknown>
}

interface DraftChange {
  localId: string
  action: CodebookAction
  summary: string
  rationale: string
  targetCodeIds: string[]
  resultingCodeIds: string
  affectedHistoricalArtifactIds: string
  sourceFinalCodeLocalId?: string
  sourceSuggestionId?: string
  autoSummary?: boolean
}

interface DraftEvidence {
  localId: string
  field_name: string
  excerpt: string
  rationale: string
}

interface CandidateOption {
  id: string
  source: string
  code: ProvisionalCode
  existingCode: Code | null
}

export interface ReviewSubmission {
  artifact_id: string
  decision: HumanDecision
  pre_read_memo: string
  final_codes: Array<Omit<DraftCode, 'localId' | 'representative_artifact_ids'>>
  rationale: string
  evidence_summary: string[]
  confirmed_evidence: EvidenceItem[]
  preserved_alternatives: string[]
  codebook_changes: CodebookChangeInput[]
  notes: string[]
  duration_seconds?: number
}

interface ReviewPanelProps {
  packet: ReviewPacket | null
  codebook: Codebook | null
  submitted: boolean
  contextRequested?: boolean
  isSubmitting: boolean
  isAdvancing: boolean
  agentAnalysisRevealed: boolean
  onSubmit: (review: ReviewSubmission) => Promise<void>
  onNext: () => Promise<void>
  onRevealAgentAnalysis: () => void
  onOpenContextRequests?: () => void
  onTimerEvent?: (action: 'pause' | 'resume') => Promise<void> | void
  isRetrospective?: boolean
}

const decisions: Array<{ value: HumanDecision; key: 'accept' | 'revise' | 'reject' | 'uncertain' | 'requestAdditionalContext' }> = [
  { value: 'accept', key: 'accept' }, { value: 'revise', key: 'revise' }, { value: 'reject', key: 'reject' }, { value: 'mark_uncertain', key: 'uncertain' }, { value: 'request_additional_context', key: 'requestAdditionalContext' },
]

function slugify(value: string) {
  const normalized = value
    .toLocaleLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '')
  return normalized || 'new-concept'
}

function unique<T>(values: T[]) {
  return [...new Set(values)]
}

function splitLines(value: string) {
  return value.split('\n').map((item) => item.trim()).filter(Boolean)
}

function evidenceKey(item: EvidenceItem, index: number) {
  return `${index}:${item.field_name}:${item.excerpt}`
}

function localized(value: string, valueZh: string | undefined, language: 'en' | 'zh') {
  if (language === 'zh' && valueZh?.trim()) return valueZh
  return value
}

function draftCodeId(code: DraftCode) {
  return code.code_id.trim() || `code-${slugify(code.name)}`
}

function addChangeSummary(code: DraftCode, language: 'en' | 'zh') {
  const codeId = draftCodeId(code)
  return language === 'zh'
    ? `新增编码“${code.name}”（${codeId}）：${code.definition}`
    : `Add code "${code.name}" (${codeId}): ${code.definition}`
}

function suggestedCodeName(code: Code, language: 'en' | 'zh') {
  const translated = code.metadata?.name_zh
  return language === 'zh' && typeof translated === 'string' && translated.trim()
    ? translated
    : code.name
}

function suggestedCodeDefinition(code: Code, language: 'en' | 'zh') {
  const translated = code.metadata?.definition_zh
  return language === 'zh' && typeof translated === 'string' && translated.trim()
    ? translated
    : code.definition
}

function mapsToExistingCode(code: ProvisionalCode) {
  return code.relationship_to_codebook === 'reuse_existing_code'
    || code.relationship_to_codebook === 'refine_existing_code'
}

function candidateOptions(packet: ReviewPacket, codebook: Codebook): CandidateOption[] {
  const options: CandidateOption[] = []
  const activeCodes = codebook.codes.filter((code) => code.status === 'active')
  const findExistingCode = (code: ProvisionalCode) => {
    // New candidates may link neighboring codes solely for boundary comparison.
    // Only an explicit reuse/refine relationship maps the candidate itself to
    // an existing codebook entry.
    if (!mapsToExistingCode(code)) return null
    return code.linked_code_ids
      .map((codeId) => activeCodes.find((item) => item.code_id === codeId))
      .find((item): item is Code => Boolean(item))
      ?? null
  }
  const append = (source: string, codes: ProvisionalCode[]) => {
    codes.forEach((code, index) => {
      const duplicate = options.some((candidate) =>
        candidate.code.code_name === code.code_name
        && candidate.code.short_definition === code.short_definition,
      )
      if (!duplicate) options.push({
        id: `${source}-${index}-${code.code_name}`,
        source,
        code,
        existingCode: findExistingCode(code),
      })
    })
  }
  packet.review_input.evidence_packet.coder_outputs.forEach((coder) => {
    append(coder.coder_id, coder.provisional_codes)
  })
  const comparison = packet.review_input.evidence_packet.comparison_output
    ?? packet.review_input.evidence_packet.arbitration_output
  append('comparison', comparison?.recommended_codes ?? [])
  return options
}

function materializeCandidate(
  candidate: CandidateOption,
  codebook: Codebook,
  artifactId: string,
): DraftCode {
  const activeCodes = codebook.codes.filter((code) => code.status === 'active')
  const linked = candidate.code.linked_code_ids
    .map((codeId) => activeCodes.find((code) => code.code_id === codeId))
    .find((code): code is Code => Boolean(code))
  const existing = mapsToExistingCode(candidate.code) ? linked : undefined
  if (existing) {
    return {
      localId: candidate.id,
      ...existing,
      metadata: {
        ...existing.metadata,
        name_zh: existing.metadata?.name_zh || candidate.code.code_name_zh || '',
        definition_zh: existing.metadata?.definition_zh || candidate.code.short_definition_zh || '',
      },
      representative_artifact_ids: unique([
        ...existing.representative_artifact_ids,
        artifactId,
      ]),
    }
  }
  const baseCodeId = `code-${slugify(candidate.code.code_name)}`
  let codeId = baseCodeId
  let suffix = 2
  while (codebook.codes.some((code) => code.code_id === codeId)) {
    codeId = `${baseCodeId}-${suffix}`
    suffix += 1
  }
  return {
    localId: candidate.id,
    code_id: codeId,
    name: candidate.code.code_name,
    definition: candidate.code.short_definition,
    inclusion_criteria: [],
    exclusion_criteria: [],
    representative_artifact_ids: [artifactId],
    boundary_artifact_ids: [],
    counterexample_status: 'not_assessed',
    hypothetical_examples: [],
    parent_code_id: null,
    status: 'active',
    notes: [],
    metadata: {
      name_zh: candidate.code.code_name_zh ?? '',
      definition_zh: candidate.code.short_definition_zh ?? '',
      inclusion_criteria_zh: [],
      exclusion_criteria_zh: [],
    },
  }
}

function ChangeEditor({
  change,
  codebook,
  onChange,
  onDelete,
}: {
  change: DraftChange
  codebook: Codebook
  onChange: (next: DraftChange) => void
  onDelete: () => void
}) {
  const { t } = useLanguage()
  const actionGuidance: Record<CodebookAction, string> = {
    add: t('guidanceAdd'), add_parent: t('guidanceAddParent'), refine: t('guidanceRefine'), merge: t('guidanceMerge'), split: t('guidanceSplit'), rename: t('guidanceRename'), retire: t('actionRetire'), no_change: t('guidanceNoChange'),
  }
  return (
    <fieldset className="change-editor">
      <div className="inline-control-row">
        <label>
          <span>{t('changeType')}</span>
          <select value={change.action} onChange={(event) => onChange({ ...change, action: event.target.value as CodebookAction, targetCodeIds: event.target.value === 'add' ? [] : change.targetCodeIds, resultingCodeIds: event.target.value === 'refine' || event.target.value === 'rename' ? '' : change.resultingCodeIds })}>
            <option value="add">{t('actionAdd')}</option>
            <option value="add_parent">{t('actionAddParent')}</option>
            <option value="refine">{t('actionRefine')}</option>
            <option value="merge">{t('actionMerge')}</option>
            <option value="split">{t('actionSplit')}</option>
            <option value="rename">{t('actionRename')}</option>
          </select>
        </label>
        <button type="button" className="icon-button subtle" onClick={onDelete} title={t('removeChange')}>
          <Trash2 size={15} />
        </button>
      </div>
      <p className="form-guidance">{actionGuidance[change.action]}</p>
      <label>
        <span>{t('changeSummary')}</span>
        <textarea value={change.summary} onChange={(event) => onChange({ ...change, summary: event.target.value, autoSummary: false })} placeholder={t('changeSummaryPlaceholder')} rows={3} />
      </label>
      {codebook.codes.length > 0 && change.action !== 'add' && (
        <div className="target-picker">
          <span>{t('affectedCurrentCodes')}</span>
          {change.action === 'add_parent' && <p className="form-guidance">{t('addParentTargetGuidance')}</p>}
          {codebook.codes.filter((code) => code.status === 'active').map((code) => (
            <label key={code.code_id} className="check-line">
              <input
                type="checkbox"
                checked={change.targetCodeIds.includes(code.code_id)}
                onChange={(event) => onChange({
                  ...change,
                  targetCodeIds: event.target.checked
                    ? [...change.targetCodeIds, code.code_id]
                    : change.targetCodeIds.filter((codeId) => codeId !== code.code_id),
                })}
              />
              <span>{code.name}</span>
              <em>{code.code_id}</em>
            </label>
          ))}
        </div>
      )}
      {change.action === 'merge' || change.action === 'split' || change.action === 'add' || change.action === 'add_parent' ? (
            <label>
              <span>{change.action === 'add_parent' ? t('newParentCodeId') : t('resultingCodeIds')}</span>
          <input value={change.resultingCodeIds} onChange={(event) => onChange({ ...change, resultingCodeIds: event.target.value })} placeholder={t('resultingCodeIdsPlaceholder')} />
        </label>
      ) : null}
      {change.action === 'add' && (
        <label>
          <span>{t('affectedHistoricalArtifacts')}</span>
          <input
            value={change.affectedHistoricalArtifactIds}
            onChange={(event) => onChange({ ...change, affectedHistoricalArtifactIds: event.target.value })}
            placeholder={t('affectedHistoricalArtifactsPlaceholder')}
          />
          <small className="field-hint">{t('affectedHistoricalArtifactsHint')}</small>
        </label>
      )}
      <label>
        <span>{t('reasonForChange')}</span>
        <textarea value={change.rationale} onChange={(event) => onChange({ ...change, rationale: event.target.value })} placeholder={t('reasonForChangePlaceholder')} rows={2} />
      </label>
    </fieldset>
  )
}

export default function ReviewPanel({
  packet,
  codebook,
  submitted,
  contextRequested = false,
  isSubmitting,
  isAdvancing,
  agentAnalysisRevealed,
  onSubmit,
  onNext,
  onRevealAgentAnalysis,
  onOpenContextRequests,
  onTimerEvent,
  isRetrospective = false,
}: ReviewPanelProps) {
  const { language, t } = useLanguage()
  const reviewerId = useId()
  const [decision, setDecision] = useState<HumanDecision | null>(null)
  const [preReadMemo, setPreReadMemo] = useState('')
  const [selectedCandidates, setSelectedCandidates] = useState<string[]>([])
  const [finalCodes, setFinalCodes] = useState<DraftCode[]>([])
  const [rationale, setRationale] = useState('')
  const [evidenceSummary, setEvidenceSummary] = useState('')
  const [selectedEvidenceKeys, setSelectedEvidenceKeys] = useState<string[]>([])
  const [customEvidence, setCustomEvidence] = useState<DraftEvidence[]>([])
  const [alternatives, setAlternatives] = useState('')
  const [requestedContext, setRequestedContext] = useState('')
  const [changes, setChanges] = useState<DraftChange[]>([])
  const [validationError, setValidationError] = useState<string | null>(null)
  const startedAt = useRef(Date.now())
  const activeSeconds = useRef(0)
  const timerPacketRef = useRef<object | null>(null)
  const [timerPaused, setTimerPaused] = useState(false)

  const packetEvidence = packet?.review_input.evidence_packet.context_packet.evidence_items ?? []
  useEffect(() => {
    if (!packet) return
    // A newly prepared packet may belong to the same artifact after a context
    // request. Reset the whole form so an earlier decision cannot be reused.
    setDecision(null)
    setPreReadMemo('')
    setSelectedCandidates([])
    setFinalCodes([])
    setRationale('')
    setEvidenceSummary('')
    setSelectedEvidenceKeys([])
    setCustomEvidence([])
    setAlternatives('')
    setRequestedContext('')
    setChanges([])
    setValidationError(null)
    startedAt.current = Date.now()
    activeSeconds.current = 0
    setTimerPaused(false)
    if (timerPacketRef.current !== packet) {
      timerPacketRef.current = packet
      void (onTimerEvent?.('resume') ?? Promise.resolve()).catch(() => setValidationError(t('reviewTimerUpdateFailed')))
    }
    // Agent-selected excerpts are review candidates, not human-confirmed evidence.
  }, [packet])

  if ((!packet || !codebook) && !contextRequested) {
    return (
      <aside className="review-panel panel">
        <div className="panel-heading">
          <div><p className="eyebrow">{t(isRetrospective ? 'retrospectiveReview' : 'humanReview')}</p><h2>{t('review')}</h2></div>
          <FilePenLine size={20} className="heading-icon" />
        </div>
        <section className="review-state">
          <span className="review-state-marker" />
          <div><p className="section-label">{t('currentState')}</p><strong>{t('awaitingEvidence')}</strong></div>
        </section>
        <p className="empty-copy review-empty">{t('prepareBeforeReview')}</p>
      </aside>
    )
  }

  if (contextRequested) {
    return (
      <aside className="review-panel panel">
        <div className="panel-heading">
          <div><p className="eyebrow">{t('humanReview')}</p><h2>{t('contextReviewPaused')}</h2></div>
          <FilePenLine size={20} className="heading-icon" />
        </div>
        <section className="review-state">
          <span className="review-state-marker" />
          <div><p className="section-label">{t('contextRequestPending')}</p><strong>{t('contextReviewPausedGuidance')}</strong></div>
        </section>
        <button type="button" className="command-button primary next-button" onClick={onOpenContextRequests}>
          {t('openContextRequests')}
        </button>
      </aside>
    )
  }

  // TypeScript cannot infer that the context-paused branch above returned.
  // Keep the runtime guard explicit so the review form never dereferences a
  // missing packet or codebook during a status refresh.
  if (!packet || !codebook) return null

  const artifactId = packet.artifact_id
  const activeCodebook = codebook
  const candidates = candidateOptions(packet, activeCodebook)
  const suggestedChanges = packet.review_input.evidence_packet.codebook_change_packets ?? []
  const confirmedEvidence = [
    ...packetEvidence.filter((item, index) =>
      selectedEvidenceKeys.includes(evidenceKey(item, index)),
    ),
    ...customEvidence
      .filter((item) => item.excerpt.trim() && item.rationale.trim())
      .map(({ localId: _localId, ...item }) => ({
        ...item,
        field_name: item.field_name.trim() || 'content',
        excerpt: item.excerpt.trim(),
        rationale: item.rationale.trim(),
      })),
  ]

  function addCustomEvidence() {
    setCustomEvidence((items) => [
      ...items,
      {
        localId: `evidence-${Date.now()}-${items.length}`,
        field_name: 'content',
        excerpt: '',
        rationale: '',
      },
    ])
  }

  function updateCode(localId: string, key: keyof DraftCode, value: string) {
    const current = finalCodes.find((code) => code.localId === localId)
    if (!current) return
    const next = { ...current, [key]: value }
    setFinalCodes((codes) => codes.map((code) => code.localId === localId ? next : code))
    setChanges((items) => items.filter((change) => {
      if (change.sourceFinalCodeLocalId !== localId || change.action !== 'add') return true
      return !activeCodebook.codes.some((code) => code.code_id === draftCodeId(next))
    }).map((change) => {
      if (change.sourceFinalCodeLocalId !== localId || change.action !== 'add') return change
      return {
        ...change,
        resultingCodeIds: draftCodeId(next),
        summary: change.autoSummary ? addChangeSummary(next, language) : change.summary,
      }
    }))
  }

  function isExistingCode(code: DraftCode) {
    return activeCodebook.codes.some((item) => item.code_id === draftCodeId(code))
  }

  function hasQuickAddChange(code: DraftCode) {
    const id = draftCodeId(code)
    return changes.some((change) =>
      change.action === 'add'
      && (change.sourceFinalCodeLocalId === code.localId || change.resultingCodeIds.split(',').map((item) => item.trim()).includes(id)),
    )
  }

  function addFinalCodeToCodebook(code: DraftCode) {
    if (isExistingCode(code) || hasQuickAddChange(code)) return
    setChanges((items) => [
      ...items,
      {
        localId: `change-${Date.now()}-${items.length}`,
        action: 'add',
        summary: addChangeSummary(code, language),
        rationale: '',
        targetCodeIds: [],
        resultingCodeIds: draftCodeId(code),
        affectedHistoricalArtifactIds: '',
        sourceFinalCodeLocalId: code.localId,
        autoSummary: true,
      },
    ])
  }

  function toggleCandidate(candidate: CandidateOption) {
    const isSelected = selectedCandidates.includes(candidate.id)
    if (isSelected) {
      const nextSelected = selectedCandidates.filter((item) => item !== candidate.id)
      const candidateCodeId = materializeCandidate(candidate, activeCodebook, artifactId).code_id
      const hasEquivalentSelection = candidates
        .filter((item) => nextSelected.includes(item.id))
        .some((item) => materializeCandidate(item, activeCodebook, artifactId).code_id === candidateCodeId)
      setSelectedCandidates(nextSelected)
      if (!hasEquivalentSelection) {
        setFinalCodes((codes) => codes.filter((code) =>
          code.localId.startsWith('manual-') || code.code_id !== candidateCodeId,
        ))
      }
      return
    }
    const code = materializeCandidate(candidate, activeCodebook, artifactId)
    setSelectedCandidates((items) => [...items, candidate.id])
    setFinalCodes((codes) => {
      const duplicate = codes.find((item) => item.code_id === code.code_id)
      if (!duplicate) return [...codes, code]
      return codes.map((item) => item.code_id === code.code_id
        ? { ...item, representative_artifact_ids: unique([...item.representative_artifact_ids, artifactId]) }
        : item)
    })
  }

  function addManualCode() {
    setFinalCodes((codes) => [
      ...codes,
      {
        localId: `manual-${Date.now()}-${codes.length}`,
        code_id: '',
        name: '',
        definition: '',
        inclusion_criteria: [],
        exclusion_criteria: [],
        representative_artifact_ids: [artifactId],
        boundary_artifact_ids: [],
        counterexample_status: 'not_assessed',
        hypothetical_examples: [],
        parent_code_id: null,
        status: 'active',
        notes: [],
        metadata: {
          name_zh: '',
          definition_zh: '',
          inclusion_criteria_zh: [],
          exclusion_criteria_zh: [],
        },
      },
    ])
  }

  function addChange() {
    setChanges((items) => [
      ...items,
      {
        localId: `change-${Date.now()}-${items.length}`,
        action: 'add',
        summary: '',
        rationale: '',
        targetCodeIds: [],
        resultingCodeIds: '',
        affectedHistoricalArtifactIds: '',
      },
    ])
  }

  function canAdoptSuggestion(suggestion: CodebookChangePacket) {
    const proposedCount = suggestion.proposed_codes.length
    const targetCount = suggestion.before_codes.length
    if (suggestion.action === 'add') return proposedCount >= 1
    if (suggestion.action === 'add_parent') return targetCount >= 2 && proposedCount === 1
    if (suggestion.action === 'refine' || suggestion.action === 'rename') {
      return targetCount === 1 && proposedCount >= 1
    }
    if (suggestion.action === 'merge') return targetCount >= 2 && proposedCount === 1
    if (suggestion.action === 'split') return targetCount === 1 && proposedCount >= 2
    return false
  }

  function adoptSuggestion(suggestion: CodebookChangePacket) {
    if (!canAdoptSuggestion(suggestion)) return
    const currentIds = new Set(activeCodebook.codes.map((code) => code.code_id))
    const reservedIds = new Set([
      ...currentIds,
      ...finalCodes.map((code) => draftCodeId(code)),
    ])
    const targetIds = suggestion.before_codes.map((code) => code.code_id)
    const proposedDrafts = suggestion.proposed_codes.map((code, index): DraftCode => {
      const sameNameExisting = activeCodebook.codes.find((item) => (
        item.status === 'active'
        && item.name.trim().toLocaleLowerCase() === code.name.trim().toLocaleLowerCase()
      ))
      let codeId = ''
      if ((suggestion.action === 'refine' || suggestion.action === 'rename') && targetIds[index]) {
        codeId = targetIds[index]
      } else if (suggestion.action === 'merge' && sameNameExisting && targetIds.includes(sameNameExisting.code_id)) {
        codeId = sameNameExisting.code_id
      } else {
        const baseId = `code-${slugify(code.name)}`
        codeId = baseId
        let suffix = 2
        while (reservedIds.has(codeId)) {
          codeId = `${baseId}-${suffix}`
          suffix += 1
        }
      }
      reservedIds.add(codeId)
      const existing = activeCodebook.codes.find((item) => item.code_id === codeId)
      return {
        localId: `suggestion-${suggestion.change_id}-${index}`,
        code_id: codeId,
        name: code.name,
        definition: code.definition,
        inclusion_criteria: existing?.inclusion_criteria ?? code.inclusion_criteria,
        exclusion_criteria: existing?.exclusion_criteria ?? code.exclusion_criteria,
        representative_artifact_ids: unique([
          ...(existing?.representative_artifact_ids ?? code.representative_artifact_ids),
          artifactId,
        ]),
        boundary_artifact_ids: unique([
          ...(existing?.boundary_artifact_ids ?? code.boundary_artifact_ids),
          ...suggestion.boundary_artifact_ids,
        ]),
        counterexample_status: existing?.counterexample_status ?? code.counterexample_status,
        hypothetical_examples: existing?.hypothetical_examples ?? code.hypothetical_examples,
        parent_code_id: existing?.parent_code_id ?? code.parent_code_id,
        status: 'active',
        notes: existing?.notes ?? code.notes,
        metadata: {
          ...(code.metadata ?? {}),
          ...(existing?.metadata ?? {}),
        },
      }
    })
    setFinalCodes((items) => {
      const next = [...items]
      proposedDrafts.forEach((draft) => {
        const existingIndex = next.findIndex((item) => draftCodeId(item) === draft.code_id)
        if (existingIndex >= 0) next[existingIndex] = draft
        else next.push(draft)
      })
      return next
    })
    const resultIds = suggestion.action === 'refine' || suggestion.action === 'rename'
      ? ''
      : proposedDrafts.map((code) => draftCodeId(code)).join(', ')
    setChanges((items) => [
      ...items.filter((item) => item.sourceSuggestionId !== suggestion.change_id),
      {
        localId: `suggested-change-${suggestion.change_id}`,
        action: suggestion.action,
        summary: localized(suggestion.summary, suggestion.summary_zh, language),
        rationale: localized(suggestion.rationale, suggestion.rationale_zh, language),
        targetCodeIds: targetIds,
        resultingCodeIds: resultIds,
        affectedHistoricalArtifactIds: suggestion.affected_artifact_ids.join(', '),
        sourceSuggestionId: suggestion.change_id,
      },
    ])
  }

  async function submit() {
    if (!preReadMemo.trim()) {
      setValidationError(t('validationMemo'))
      return
    }
    if (!agentAnalysisRevealed) {
      setValidationError(t('validationReveal'))
      return
    }
    if (!decision) {
      setValidationError(t('validationDecision'))
      return
    }
    if (!rationale.trim()) {
      setValidationError(t('validationRationale'))
      return
    }
    const normalizedCodes = finalCodes.map((code) => ({
      ...code,
      code_id: code.code_id.trim() || `code-${slugify(code.name)}`,
      name: code.name.trim(),
      definition: code.definition.trim(),
    }))
    if (normalizedCodes.some((code) => !code.name || !code.definition)) {
      setValidationError(t('validationCodeFields'))
      return
    }
    const codeIds = normalizedCodes.map((code) => code.code_id)
    if (new Set(codeIds).size !== codeIds.length) {
      setValidationError(t('validationUniqueIds'))
      return
    }
    if ((decision === 'reject' || decision === 'mark_uncertain' || decision === 'request_additional_context') && (normalizedCodes.length > 0 || changes.length > 0)) {
      setValidationError(t('validationRejectCodes'))
      return
    }
    if (normalizedCodes.length > 0 && confirmedEvidence.length === 0) {
      setValidationError(t('validationEvidence'))
      return
    }
    if (changes.some((change) => !change.summary.trim())) {
      setValidationError(t('validationChangeSummary'))
      return
    }
    if (changes.some((change) => !change.rationale.trim())) {
      setValidationError(t('validationChangeReason'))
      return
    }
    if (decision === 'request_additional_context' && !requestedContext.trim()) {
      setValidationError(t('validationRequestedContext'))
      return
    }
    const finalCodeIds = new Set(normalizedCodes.map((code) => code.code_id))
    const currentCodeIds = new Set(activeCodebook.codes.map((code) => code.code_id))
    for (const change of changes) {
      const resultIds = change.resultingCodeIds.split(',').map((item) => item.trim()).filter(Boolean)
      if (change.action === 'add' && (change.targetCodeIds.length > 0 || resultIds.length === 0 || resultIds.some((id) => !finalCodeIds.has(id) || currentCodeIds.has(id)))) {
        setValidationError(t('validationAdd'))
        return
      }
      if (change.action === 'add_parent' && (change.targetCodeIds.length < 2 || resultIds.length !== 1 || !finalCodeIds.has(resultIds[0]) || currentCodeIds.has(resultIds[0]))) {
        setValidationError(t('validationAddParent'))
        return
      }
      if ((change.action === 'refine' || change.action === 'rename') && (change.targetCodeIds.length !== 1 || !finalCodeIds.has(change.targetCodeIds[0]))) {
        setValidationError(t('validationRefine', { action: change.action === 'refine' ? t('actionRefine') : t('actionRename') }))
        return
      }
      if (change.action === 'merge' && (change.targetCodeIds.length < 2 || resultIds.length !== 1 || (!finalCodeIds.has(resultIds[0]) && !currentCodeIds.has(resultIds[0])))) {
        setValidationError(t('validationMerge'))
        return
      }
      if (change.action === 'split' && (change.targetCodeIds.length !== 1 || resultIds.length < 2 || resultIds.some((id) => !finalCodeIds.has(id)) || resultIds.includes(change.targetCodeIds[0]))) {
        setValidationError(t('validationSplit'))
        return
      }
    }
    setValidationError(null)
    const duration = await closeTimerForSubmit()
    if (duration === null) return
    await onSubmit({
      artifact_id: artifactId,
      decision,
      pre_read_memo: preReadMemo.trim(),
      final_codes: normalizedCodes.map(({ localId: _localId, representative_artifact_ids: _representatives, ...code }) => code),
      rationale: rationale.trim(),
      evidence_summary: splitLines(evidenceSummary),
      confirmed_evidence: confirmedEvidence,
      preserved_alternatives: splitLines(alternatives),
      codebook_changes: changes.map((change) => ({
        action: change.action,
        summary: change.summary.trim(),
        rationale: change.rationale.trim(),
        target_code_ids: change.targetCodeIds,
        resulting_code_ids: change.resultingCodeIds.split(',').map((item) => item.trim()).filter(Boolean),
        artifact_ids: [artifactId],
        metadata: change.affectedHistoricalArtifactIds.split(',').map((item) => item.trim()).filter(Boolean).length > 0
          ? {
              affected_historical_artifact_ids: change.affectedHistoricalArtifactIds
                .split(',')
                .map((item) => item.trim())
                .filter(Boolean),
            }
          : {},
      })),
      notes: splitLines(requestedContext),
      duration_seconds: duration,
    })
  }

  if (submitted) {
    return (
      <aside className="review-panel panel">
        <div className="panel-heading">
          <div><p className="eyebrow">{t(isRetrospective ? 'retrospectiveReview' : 'reviewRecorded')}</p><h2>{t(isRetrospective ? 'retrospectiveReviewComplete' : 'reviewComplete')}</h2></div>
          <Check size={20} className="heading-icon success-icon" />
        </div>
        <section className="review-state complete-state">
          <span className="review-state-marker ready" />
          <div><p className="section-label">{t('codebookUpdated')}</p><strong>{t(isRetrospective ? 'retrospectiveSaved' : 'reviewSaved', { id: artifactId })}</strong></div>
        </section>
        <p className="post-submit-copy">{t('inspectBeforeMoving')}</p>
        <button type="button" className="command-button primary next-button" onClick={() => void onNext()} disabled={isAdvancing}>
          {isAdvancing ? <LoaderCircle size={16} className="spin" /> : <ArrowRight size={16} />}
          {isAdvancing ? t(isRetrospective ? 'openingNextRetrospective' : 'openingNext') : t(isRetrospective ? 'nextRetrospectiveTask' : 'nextArtifact')}
        </button>
      </aside>
    )
  }

  async function toggleTimer() {
    const now = Date.now()
    if (timerPaused) {
      startedAt.current = now
      setTimerPaused(false)
      try {
        await onTimerEvent?.('resume')
      } catch {
        setTimerPaused(true)
        setValidationError(t('reviewTimerUpdateFailed'))
      }
    } else {
      const addedSeconds = (now - startedAt.current) / 1000
      activeSeconds.current += addedSeconds
      setTimerPaused(true)
      try {
        await onTimerEvent?.('pause')
      } catch {
        activeSeconds.current -= addedSeconds
        setTimerPaused(false)
        setValidationError(t('reviewTimerUpdateFailed'))
      }
    }
  }

  function activeDurationSeconds() {
    return Math.max(
      1,
      Math.round(
        activeSeconds.current
          + (timerPaused ? 0 : (Date.now() - startedAt.current) / 1000),
      ),
    )
  }

  async function closeTimerForSubmit(): Promise<number | null> {
    const duration = activeDurationSeconds()
    if (timerPaused) return duration
    const addedSeconds = (Date.now() - startedAt.current) / 1000
    try {
      await onTimerEvent?.('pause')
    } catch {
      setValidationError(t('reviewTimerUpdateFailed'))
      return null
    }
    activeSeconds.current += addedSeconds
    setTimerPaused(true)
    return duration
  }

  return (
    <aside className="review-panel panel">
      <div className="panel-heading">
        <div><p className="eyebrow">{t('humanReview')}</p><h2>{t('reviewDecision')}</h2></div>
        <div className="heading-actions">
          <button type="button" className="icon-button subtle" onClick={() => void toggleTimer()} title={t(timerPaused ? 'resumeReviewTimer' : 'pauseReviewTimer')}>
            {timerPaused ? <Play size={16} /> : <Pause size={16} />}
          </button>
          <FilePenLine size={20} className="heading-icon" />
        </div>
      </div>
      <form className="review-form" onSubmit={(event) => { event.preventDefault(); void submit() }}>
        <section className="form-section">
          <p className="section-label">1. {t('independentPreRead')}</p>
          <p className="form-guidance">{t('preReadGuidance')}</p>
          <label><span>{t('initialMemo')}</span><textarea value={preReadMemo} onChange={(event) => setPreReadMemo(event.target.value)} placeholder={t('initialMemoPlaceholder')} rows={5} required /></label>
          {!agentAnalysisRevealed && <button type="button" className="secondary-action" onClick={onRevealAgentAnalysis} disabled={!preReadMemo.trim()}><ArrowRight size={15} /> {t('revealEvidence')}</button>}
        </section>

        {agentAnalysisRevealed && <>
          <section className="form-section">
            <p className="section-label">2. {t('evidenceAudit')}</p>
            <p className="form-guidance">{t('evidenceAuditGuidance')}</p>
            <div className="evidence-confirmation-list">
              {packetEvidence.map((item, index) => {
                const key = evidenceKey(item, index)
                const selected = selectedEvidenceKeys.includes(key)
                return (
                  <label className={`evidence-confirmation ${selected ? 'selected' : ''}`} key={key}>
                    <input
                      type="checkbox"
                      checked={selected}
                      onChange={() => setSelectedEvidenceKeys((current) => (
                        selected
                          ? current.filter((value) => value !== key)
                          : [...current, key]
                      ))}
                    />
                    <span><strong>{item.field_name}</strong><small>{item.excerpt}</small></span>
                  </label>
                )
              })}
              {packetEvidence.length === 0 && <p className="empty-copy">{t('noEvidenceSummary')}</p>}
            </div>
            <div className="section-action-heading">
              <p className="form-guidance">{t('manualEvidenceGuidance')}</p>
              <button type="button" className="secondary-action compact" onClick={addCustomEvidence}><Plus size={14} /> {t('addManualEvidence')}</button>
            </div>
            {customEvidence.map((item) => (
              <fieldset className="change-editor" key={item.localId}>
                <button type="button" className="icon-button danger" title={t('removeManualEvidence')} onClick={() => setCustomEvidence((items) => items.filter((candidate) => candidate.localId !== item.localId))}><Trash2 size={14} /></button>
                <label><span>{t('evidenceFieldName')}</span><input value={item.field_name} onChange={(event) => setCustomEvidence((items) => items.map((candidate) => candidate.localId === item.localId ? { ...candidate, field_name: event.target.value } : candidate))} placeholder="content" /></label>
                <label><span>{t('verbatimEvidenceExcerpt')}</span><textarea value={item.excerpt} onChange={(event) => setCustomEvidence((items) => items.map((candidate) => candidate.localId === item.localId ? { ...candidate, excerpt: event.target.value } : candidate))} rows={3} /></label>
                <label><span>{t('evidenceRationale')}</span><textarea value={item.rationale} onChange={(event) => setCustomEvidence((items) => items.map((candidate) => candidate.localId === item.localId ? { ...candidate, rationale: event.target.value } : candidate))} rows={2} /></label>
              </fieldset>
            ))}
            <label><span>{t('humanConfirmedEvidence')}</span><textarea value={evidenceSummary} onChange={(event) => setEvidenceSummary(event.target.value)} placeholder={t('evidencePlaceholder')} rows={4} /></label>
          </section>

          <section className="form-section">
            <p className="section-label">3. {t('candidateComparison')}</p>
            <p className="form-guidance">{t('candidateGuidance')}</p>
            <div className="candidate-picker">
              {candidates.map((candidate) => (
                <label className={`candidate-choice ${candidate.existingCode ? 'existing' : 'new'}`} key={candidate.id}>
                  <input type="checkbox" checked={selectedCandidates.includes(candidate.id)} onChange={() => toggleCandidate(candidate)} />
                  <span>
                    <strong>{localized(candidate.code.code_name, candidate.code.code_name_zh, language)}</strong>
                    <span className={`candidate-status ${candidate.existingCode ? 'existing' : 'new'}`}>
                      {candidate.existingCode ? t('existingCode') : t('newCandidateCode')}
                    </span>
                    <em>{candidate.source.startsWith('coder-') ? t(`coderRole_${candidate.source}`) : candidate.source}</em>
                    <small>{localized(candidate.code.short_definition, candidate.code.short_definition_zh, language)}</small>
                    {candidate.existingCode && <small className="candidate-code-id">{candidate.existingCode.code_id}</small>}
                  </span>
                </label>
              ))}
              {candidates.length === 0 && <p className="empty-copy">{t('noCandidatesManual')}</p>}
            </div>
            <div className="final-code-list">
              {finalCodes.map((code) => (
                <fieldset className="final-code-editor" key={code.localId}>
                  <div className="inline-control-row">
                    <span className="field-label">
                      {t('finalCode')}
                      <span className={`final-code-status ${isExistingCode(code) ? 'existing' : 'new'}`}>
                        {isExistingCode(code) ? t('existingCode') : t('newCandidateCode')}
                      </span>
                    </span>
                    {!isExistingCode(code) && (
                      <button
                        type="button"
                        className="secondary-action compact"
                        onClick={() => addFinalCodeToCodebook(code)}
                        disabled={hasQuickAddChange(code) || !code.name.trim() || !code.definition.trim()}
                        title={!code.name.trim() || !code.definition.trim() ? t('completeCodeBeforeAdd') : undefined}
                      >
                        <Plus size={13} />
                        {hasQuickAddChange(code) ? t('codeAddedToCodebook') : t('addNewCodeToCodebook')}
                      </button>
                    )}
                    <button type="button" className="icon-button subtle" onClick={() => {
                      setFinalCodes((codes) => codes.filter((item) => item.localId !== code.localId))
                      setChanges((items) => items.filter((change) => change.sourceFinalCodeLocalId !== code.localId))
                    }} title={t('removeFinalCode')}><Trash2 size={15} /></button>
                  </div>
                  <label><span>{t('codeId')}</span><input value={code.code_id} onChange={(event) => updateCode(code.localId, 'code_id', event.target.value)} placeholder={code.name ? `code-${slugify(code.name)}` : t('autoFromName')} /></label>
                  <label><span>{t('name')}</span><input value={code.name} onChange={(event) => updateCode(code.localId, 'name', event.target.value)} placeholder={t('conceptName')} /></label>
                  <label><span>{t('definition')}</span><textarea value={code.definition} onChange={(event) => updateCode(code.localId, 'definition', event.target.value)} placeholder={t('definitionPlaceholder')} rows={3} /></label>
                </fieldset>
              ))}
            </div>
            <button type="button" className="secondary-action" onClick={addManualCode}><Plus size={15} /> {t('addManualCode')}</button>
            <label><span>{t('preservedAlternatives')}</span><textarea value={alternatives} onChange={(event) => setAlternatives(event.target.value)} placeholder={t('alternativesPlaceholder')} rows={3} /></label>
          </section>

          <section className="form-section">
            <div className="section-action-heading"><p className="section-label">4. {t('codebookImpact')}</p><button type="button" className="secondary-action compact" onClick={addChange}><Plus size={14} /> {t('recordChange')}</button></div>
            <p className="form-guidance">{t('codebookImpactGuidance')}</p>
            {suggestedChanges.length > 0 && (
              <div className="review-suggestion-list">
                <p className="field-label">{t('agentChangeSuggestions')}</p>
                <p className="form-guidance">{t('agentChangeSuggestionsGuidance')}</p>
                {suggestedChanges.map((suggestion) => {
                  const adopted = changes.some((change) => change.sourceSuggestionId === suggestion.change_id)
                  const adoptable = canAdoptSuggestion(suggestion)
                  return (
                    <article className={`review-suggestion ${adopted ? 'adopted' : ''}`} key={suggestion.change_id}>
                      <header>
                        <span className={`change-action ${suggestion.action}`}>{t(`action${suggestion.action === 'add_parent' ? 'AddParent' : suggestion.action.charAt(0).toUpperCase() + suggestion.action.slice(1)}`)}</span>
                        <strong>{localized(suggestion.summary, suggestion.summary_zh, language)}</strong>
                      </header>
                      <p>{localized(suggestion.rationale, suggestion.rationale_zh, language)}</p>
                      <dl>
                        <div><dt>{t('affectedCurrentCodes')}</dt><dd>{suggestion.before_codes.map((code) => suggestedCodeName(code, language)).join(' · ') || t('none')}</dd></div>
                        <div><dt>{t('proposedCodes')}</dt><dd>{suggestion.proposed_codes.map((code) => suggestedCodeName(code, language)).join(' · ') || t('none')}</dd></div>
                      </dl>
                      <button type="button" className="secondary-action compact" disabled={adopted || !adoptable} onClick={() => adoptSuggestion(suggestion)}>
                        <Check size={13} />
                        {adopted ? t('suggestionLoaded') : adoptable ? t('adoptSuggestion') : t('suggestionIncomplete')}
                      </button>
                    </article>
                  )
                })}
              </div>
            )}
            {changes.map((change) => <ChangeEditor key={change.localId} change={change} codebook={activeCodebook} onChange={(next) => setChanges((items) => items.map((item) => item.localId === next.localId ? { ...next, sourceFinalCodeLocalId: next.action === 'add' ? next.sourceFinalCodeLocalId : undefined } : item))} onDelete={() => setChanges((items) => items.filter((item) => item.localId !== change.localId))} />)}
            {changes.length === 0 && <p className="empty-copy">{t('noStructuralChange')}</p>}
          </section>

          <section className="form-section">
            <p className="section-label">5. {t('finalDisposition')}</p>
            <label><span>{t('finalRationale')}</span><textarea value={rationale} onChange={(event) => setRationale(event.target.value)} placeholder={t('finalRationalePlaceholder')} rows={5} required /></label>
            <p className="form-guidance">{t('decisionGuidance')}</p>
            <div className="decision-grid" role="radiogroup" aria-label={t('finalDisposition')}>
              {decisions.map((item) => (
                <label key={item.value} className={decision === item.value ? 'selected' : ''}>
                  <input type="radio" name={reviewerId} checked={decision === item.value} onChange={() => setDecision(item.value)} />
                  {t(item.key)}
                </label>
              ))}
            </div>
            {decision === 'request_additional_context' && (
              <label><span>{t('requestedContext')}</span><textarea value={requestedContext} onChange={(event) => setRequestedContext(event.target.value)} placeholder={t('requestedContextPlaceholder')} rows={3} required /></label>
            )}
          </section>
        </>}

        {validationError && <p className="form-error"><CircleAlert size={15} /> {validationError}</p>}
        <button type="submit" className="command-button primary submit-review" disabled={isSubmitting || !agentAnalysisRevealed}>
          {isSubmitting ? <LoaderCircle size={16} className="spin" /> : <Send size={16} />}
          {isSubmitting ? t('savingReview') : t('submitReview')}
        </button>
        <p className="submission-note"><ListChecks size={14} /> {t('submissionNote')}</p>
      </form>
    </aside>
  )
}
