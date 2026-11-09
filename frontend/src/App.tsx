import {
  BookOpenCheck,
  Bot,
  Check,
  ChevronRight,
  CircleAlert,
  ClipboardList,
  Database,
  Download,
  FileText,
  FolderOpen,
  GitBranch,
  History,
  LoaderCircle,
  Layers3,
  Pause,
  Plus,
  ChevronDown,
  Play,
  RefreshCw,
  Search,
  ShieldCheck,
  Sparkles,
  ScrollText,
  Trash2,
  X,
} from 'lucide-react'
import { startTransition, useDeferredValue, useEffect, useRef, useState, type CSSProperties, type KeyboardEvent as ReactKeyboardEvent, type MouseEvent, type PointerEvent as ReactPointerEvent } from 'react'
import { api } from './api'
import { bootstrapNodeForRun, bootstrapStatusLabelKey, currentNodeForRun } from './workflowProgress'
import ReviewPanel, { type ReviewSubmission } from './ReviewPanel'
import { useLanguage } from './i18n'
import type {
  Code,
  Codebook,
  CodebookChange,
  CodeArtifacts,
  BootstrapInspection,
  BootstrapProgress,
  CodingRecord,
  CurrentArtifactResponse,
  Dataset,
  EvidenceItem,
  ComparisonFinding,
  AnalyticMemo,
  ProvisionalCode,
  ReviewPacket,
  RunArtifacts,
  RunHistory,
  RunSummary,
  ReviewMode,
  RetrospectiveReviewPacket,
  RetrospectiveTask,
  SubmitReviewRequest,
  StageReviewPacket,
  StageReviewRequest,
  CodeInput,
  CodebookChangeInput,
  ContextRequest,
  ExperimentVariant,
} from './types'

type AppView = 'workspace' | 'history' | 'evolution' | 'retrospective' | 'context_requests' | 'bootstrap' | 'logs' | 'codebook'
type LogTab = 'checkpoint' | 'reviews' | 'traces' | 'final_codebook'
type WorkflowStage = 'dataset' | 'initialization' | 'context' | 'coding' | 'comparison' | 'validation' | 'human_review' | 'codebook_update' | 'final'
type OverviewStage = 'familiarization' | 'initial_coding' | 'initial_categorization' | 'iterative_coding' | 'codebook_refinement' | 'stabilization'
type ExecutionNode = {
  id: string
  stage: WorkflowStage
  overview: OverviewStage | null
  label: string
  agent: string
  output: string
  detail: string
}

type WorkspaceDivider = 'left' | 'right'

const WORKSPACE_MIN_WIDTHS = {
  left: 255,
  center: 520,
  right: 260,
} as const

function WorkspaceResizeHandle({
  divider,
  onStart,
  onKeyAdjust,
}: {
  divider: WorkspaceDivider
  onStart: (event: ReactPointerEvent<HTMLButtonElement>, divider: WorkspaceDivider) => void
  onKeyAdjust: (event: ReactKeyboardEvent<HTMLButtonElement>, divider: WorkspaceDivider) => void
}) {
  const { t } = useLanguage()
  const label = divider === 'left' ? t('resizeLeftDivider') : t('resizeRightDivider')
  return (
    <button
      type="button"
      className="workspace-divider"
      role="separator"
      aria-orientation="vertical"
      aria-label={label}
      title={label}
      onPointerDown={(event) => onStart(event, divider)}
      onKeyDown={(event) => onKeyAdjust(event, divider)}
    >
      <span aria-hidden="true" />
    </button>
  )
}

const workflowStages: Array<{ id: WorkflowStage; label: string; group: string; owner: 'system' | 'agent' | 'human'; icon: typeof FileText }> = [
  { id: 'dataset', label: 'workflowDataset', group: 'workflowGroupInput', owner: 'system', icon: Database },
  { id: 'initialization', label: 'workflowInitialization', group: 'workflowGroupInput', owner: 'agent', icon: Sparkles },
  { id: 'context', label: 'workflowContext', group: 'workflowGroupOpenCoding', owner: 'agent', icon: ClipboardList },
  { id: 'coding', label: 'workflowCoding', group: 'workflowGroupOpenCoding', owner: 'agent', icon: Bot },
  { id: 'comparison', label: 'workflowComparison', group: 'workflowGroupComparison', owner: 'agent', icon: GitBranch },
  { id: 'validation', label: 'workflowValidation', group: 'workflowGroupQuality', owner: 'agent', icon: ShieldCheck },
  { id: 'human_review', label: 'workflowHumanReview', group: 'workflowGroupQuality', owner: 'human', icon: BookOpenCheck },
  { id: 'codebook_update', label: 'workflowCodebookUpdate', group: 'workflowGroupOutput', owner: 'system', icon: GitBranch },
  { id: 'final', label: 'workflowFinal', group: 'workflowGroupOutput', owner: 'system', icon: Check },
]

const overviewStages: Array<{
  id: OverviewStage
  label: string
  summary: string
  agent: string
  target: WorkflowStage
  icon: typeof FileText
}> = [
  { id: 'familiarization', label: 'overviewFamiliarization', summary: 'overviewFamiliarizationSummary', agent: 'overviewFamiliarizationAgent', target: 'context', icon: ClipboardList },
  { id: 'initial_coding', label: 'overviewInitialCoding', summary: 'overviewInitialCodingSummary', agent: 'overviewInitialCodingAgent', target: 'coding', icon: Bot },
  { id: 'initial_categorization', label: 'overviewInitialCategorization', summary: 'overviewInitialCategorizationSummary', agent: 'overviewInitialCategorizationAgent', target: 'initialization', icon: Layers3 },
  { id: 'iterative_coding', label: 'overviewIterativeCoding', summary: 'overviewIterativeCodingSummary', agent: 'overviewIterativeCodingAgent', target: 'comparison', icon: GitBranch },
  { id: 'codebook_refinement', label: 'overviewCodebookRefinement', summary: 'overviewCodebookRefinementSummary', agent: 'overviewCodebookRefinementAgent', target: 'comparison', icon: RefreshCw },
  { id: 'stabilization', label: 'overviewStabilization', summary: 'overviewStabilizationSummary', agent: 'overviewStabilizationAgent', target: 'final', icon: Check },
]

const executionNodes: ExecutionNode[] = [
  { id: 'input', stage: 'dataset', overview: null, label: 'workflowDataset', agent: 'workflowResearcherSystem', output: 'workflowDatasetOutput', detail: 'workflowDatasetDescription' },
  { id: 'context', stage: 'context', overview: 'familiarization', label: 'workflowContext', agent: 'agentOverviewContext', output: 'workflowContextOutput', detail: 'workflowContextDescription' },
  { id: 'coding', stage: 'coding', overview: 'initial_coding', label: 'workflowCoding', agent: 'agentOverviewCoders', output: 'workflowCodingOutput', detail: 'workflowCodingDescription' },
  { id: 'induction', stage: 'initialization', overview: 'initial_categorization', label: 'workflowInitialization', agent: 'agentOverviewInduction', output: 'workflowInitializationOutput', detail: 'workflowInitializationDescription' },
  { id: 'initial_validation', stage: 'validation', overview: 'initial_categorization', label: 'workflowValidation', agent: 'agentOverviewValidation', output: 'workflowValidationOutput', detail: 'workflowValidationDescription' },
  { id: 'initial_review', stage: 'human_review', overview: 'initial_categorization', label: 'overviewInitialReview', agent: 'workflowHuman', output: 'workflowHumanReviewOutput', detail: 'overviewInitialReviewSummary' },
  { id: 'iterative_context', stage: 'context', overview: 'iterative_coding', label: 'workflowContext', agent: 'agentOverviewContext', output: 'workflowContextOutput', detail: 'workflowContextDescription' },
  { id: 'iterative_coding', stage: 'coding', overview: 'iterative_coding', label: 'workflowCoding', agent: 'agentOverviewCoders', output: 'workflowCodingOutput', detail: 'workflowCodingDescription' },
  { id: 'comparison', stage: 'comparison', overview: 'iterative_coding', label: 'workflowComparison', agent: 'agentOverviewComparison', output: 'workflowComparisonOutput', detail: 'workflowComparisonDescription' },
  { id: 'validation', stage: 'validation', overview: 'codebook_refinement', label: 'workflowValidation', agent: 'agentOverviewValidation', output: 'workflowValidationOutput', detail: 'workflowValidationDescription' },
  { id: 'triggered_review', stage: 'human_review', overview: 'codebook_refinement', label: 'overviewTriggeredReview', agent: 'workflowHuman', output: 'workflowHumanReviewOutput', detail: 'overviewTriggeredReviewSummary' },
  { id: 'codebook_update', stage: 'codebook_update', overview: 'codebook_refinement', label: 'workflowCodebookUpdate', agent: 'workflowSystem', output: 'workflowCodebookUpdateOutput', detail: 'workflowCodebookUpdateDescription' },
  { id: 'final_review', stage: 'human_review', overview: 'stabilization', label: 'overviewFinalReview', agent: 'workflowHuman', output: 'workflowHumanReviewOutput', detail: 'overviewFinalReviewSummary' },
  { id: 'final', stage: 'final', overview: 'stabilization', label: 'workflowFinal', agent: 'workflowSystem', output: 'workflowFinalOutput', detail: 'workflowFinalDescription' },
]

function WorkflowStatusLabel({ status }: { status: ReturnType<typeof workflowStageStatus> }) {
  const { t } = useLanguage()
  return <span className={`workflow-status ${status}`}>{t(`workflowStatus_${status}`)}</span>
}

function workflowKeyPart(stage: WorkflowStage) {
  return stage.split('_').map((part) => part.charAt(0).toUpperCase() + part.slice(1)).join('')
}

function workflowStageStatus(
  stage: WorkflowStage,
  run: RunSummary | null,
  packet: ReviewPacket | null,
  current: CurrentArtifactResponse | null,
): 'complete' | 'current' | 'waiting' | 'warning' | 'pending' {
  if (!run) return 'pending'
  if (stage === 'dataset') return 'complete'
  if (stage === 'initialization') {
    if (run.bootstrap_status === 'completed' || run.bootstrap_status === 'disabled' || run.bootstrap_status === 'skipped') return 'complete'
    if (run.bootstrap_status === 'failed' || run.bootstrap_status === 'cancelled' || run.bootstrap_status === 'interrupted') return 'warning'
    if (run.bootstrap_status === 'running' || run.bootstrap_status === 'cancelling') return 'current'
    return 'waiting'
  }
  if (stage === 'context') return packet ? 'complete' : current?.artifact ? 'current' : 'pending'
  if (stage === 'coding') return packet?.review_input.evidence_packet.coder_outputs?.length ? 'complete' : 'pending'
  if (stage === 'comparison') return packet?.review_input.evidence_packet.comparison_output || packet?.review_input.evidence_packet.arbitration_output || packet?.review_input.evidence_packet.comparison_findings?.length ? 'complete' : 'pending'
  if (stage === 'validation') {
    if (!packet?.review_input.evidence_packet.validation_output) return 'pending'
    return packet.review_input.evidence_packet.validation_output.human_review_required ? 'warning' : 'complete'
  }
  if (stage === 'human_review') return run.status === 'awaiting_human_review' || run.status === 'awaiting_initial_review' || run.status === 'awaiting_final_review' ? 'current' : run.human_reviewed_artifacts > 0 ? 'complete' : 'pending'
  if (stage === 'codebook_update') return run.codebook_version > 0 && run.reviewed_artifacts > 0 ? 'complete' : 'pending'
  return run.status === 'completed' || run.status === 'stabilized' || run.status === 'completed_with_unresolved' ? 'complete' : 'pending'
}

const selectableDatasetNames = new Set([
  'llm_code_error_semantic',
  'llm_code_error_syntactic',
  'ml_satd_23_shades',
  'personal_data_protection_github',
])

function statusLabel(status: RunSummary['status'], t: (key: string) => string) {
  const labels: Record<RunSummary['status'], string> = {
    not_started: 'Not started', awaiting_initial_review: 'Initial review', in_progress: 'In progress', awaiting_human_review: 'Evidence ready', awaiting_context: 'Waiting for context', awaiting_next_artifact: 'Review recorded', awaiting_final_review: 'Final review', stabilized: 'Stabilized', completed_with_unresolved: 'Completed with unresolved items', resource_limited: 'Resource limited', completed: 'Completed',
  }
  const translated: Record<RunSummary['status'], string> = {
    not_started: t('notStarted'), awaiting_initial_review: t('initialReview'), in_progress: t('inProgress'), awaiting_human_review: t('evidenceReady'), awaiting_context: t('awaitingContext'), awaiting_next_artifact: t('reviewRecorded'), awaiting_final_review: t('finalReview'), stabilized: t('stabilized'), completed_with_unresolved: t('completedWithUnresolved'), resource_limited: t('resourceLimited'), completed: t('completed'),
  }
  return translated[status] || labels[status]
}

function evidenceLabel(index: number) {
  return `E${index + 1}`
}

function codeStatusLabel(value: string, t: ReturnType<typeof useLanguage>['t']) {
  const keys: Record<string, string> = {
    active: 'statusActive', merged: 'statusMerged', split: 'statusSplit', retired: 'statusRetired',
  }
  return keys[value] ? t(keys[value]) : humanize(value)
}

function CodeItem({ code, onSelect }: { code: Code; onSelect: (codeId: string) => void }) {
  const { language, t } = useLanguage()
  const isBootstrap = code.metadata?.origin === 'llm_bootstrap'
  return (
    <button className="code-item" type="button" onClick={() => onSelect(code.code_id)} title={t('viewAssignedArtifacts')}>
      <div className="code-item-heading">
        <span className="code-id">{code.code_id}</span>
        <span className={`status-dot ${code.status}`} title={codeStatusLabel(code.status, t)} />
      </div>
      <h3>{codeLocalized(code, 'name', language)}</h3>
      {isBootstrap && <span className="bootstrap-code-chip">{t('bootstrapProvisional')}</span>}
      <p>{codeLocalized(code, 'definition', language)}</p>
      {code.parent_code_id && <span className="parent-code">{t('parentCode')}: {code.parent_code_id}</span>}
      {code.representative_artifact_ids.length > 0 && (
        <span className="representative-count">
          {code.representative_artifact_ids.length} {t('representativeArtifacts')}
        </span>
      )}
      <span className="code-item-action">{t('viewAssignedArtifacts')}</span>
    </button>
  )
}

function CodeArtifactsView({ data, isLoading }: { data: CodeArtifacts | null; isLoading: boolean }) {
  const { language, t } = useLanguage()
  if (isLoading) return <section className="code-artifacts-detail"><p className="empty-copy">{t('loadingAssignedArtifacts')}</p></section>
  if (!data) return <section className="code-artifacts-detail"><p className="empty-copy">{t('selectCode')}</p></section>
  const warnings = Array.isArray(data.code.metadata?.audit_warnings)
    ? data.code.metadata?.audit_warnings.filter((warning): warning is string => typeof warning === 'string')
    : []
  const warningsZh = Array.isArray(data.code.metadata?.audit_warnings_zh)
    ? data.code.metadata?.audit_warnings_zh.filter((warning): warning is string => typeof warning === 'string')
    : []
  return (
    <section className="code-artifacts-detail">
      <div className="subpanel-heading"><div><p className="section-label">{t('codeAssignment')}</p><h3>{codeLocalized(data.code, 'name', language)}</h3></div><span className="version-chip">{data.artifact_count} {t('artifactsCount')}</span></div>
      <p className="code-detail-definition">{codeLocalized(data.code, 'definition', language)}</p>
      {warnings.length > 0 && <section className="bootstrap-audit"><strong>{t('bootstrapAuditWarnings')}</strong>{localizedList(warnings, warningsZh, language).map((warning) => <p key={warning}>{warning}</p>)}</section>}
      {data.artifacts.length === 0 && <p className="empty-copy">{t('noAssignedArtifacts')}</p>}
      <div className="assigned-artifact-list">
        {data.artifacts.map(({ artifact, review }) => (
          <details key={artifact.artifact_id} className="assigned-artifact">
            <summary><strong>{t('artifact')} {artifact.artifact_id}</strong><span>{review ? decisionLabel(review.decision, t) : t('representativeOnly')}</span></summary>
            <pre>{artifact.content}</pre>
            {review && <p className="detail-meta">{t('reviewedAt', { version: review.codebook_version })} · {review.rationale}</p>}
          </details>
        ))}
      </div>
    </section>
  )
}

function localized(value: unknown, valueZh: unknown, language: 'en' | 'zh', fallback = 'Not recorded') {
  const preferred = language === 'zh' ? valueZh : value
  const secondary = language === 'zh' ? value : valueZh
  if (typeof preferred === 'string' && preferred.trim()) return preferred
  if (typeof secondary === 'string' && secondary.trim()) return secondary
  return fallback
}

function localizedList(value: unknown, valueZh: unknown, language: 'en' | 'zh') {
  const preferred = language === 'zh' ? valueZh : value
  const secondary = language === 'zh' ? value : valueZh
  const list = Array.isArray(preferred) ? preferred : Array.isArray(secondary) ? secondary : []
  return list.filter((item): item is string => typeof item === 'string' && item.trim().length > 0)
}

type LocalizedCodeFields = {
  name: string
  definition: string
  inclusion_criteria: string[]
  exclusion_criteria: string[]
  metadata?: Record<string, unknown>
}

function codeLocalized(
  code: LocalizedCodeFields,
  field: 'name' | 'definition',
  language: 'en' | 'zh',
  fallback = 'Not recorded',
) {
  const zhKey = field === 'name' ? 'name_zh' : 'definition_zh'
  return localized(code[field], code.metadata?.[zhKey], language, fallback)
}

function codeLocalizedList(
  code: LocalizedCodeFields,
  field: 'inclusion_criteria' | 'exclusion_criteria',
  language: 'en' | 'zh',
) {
  const zhKey = field === 'inclusion_criteria' ? 'inclusion_criteria_zh' : 'exclusion_criteria_zh'
  return localizedList(code[field], code.metadata?.[zhKey], language)
}

function confidenceKey(value: unknown) {
  if (value === 'high') return 'confidenceHigh'
  if (value === 'medium') return 'confidenceMedium'
  if (value === 'low') return 'confidenceLow'
  return null
}

function confidenceFactorLabel(value: string, t: ReturnType<typeof useLanguage>['t']) {
  const keys: Record<string, string> = {
    evidence_support: 'factorEvidenceSupport',
    evidence_grounding: 'factorEvidenceGrounding',
    context_sufficiency: 'factorContextSufficiency',
    codebook_fit: 'factorCodebookFit',
    coder_agreement: 'factorCoderAgreement',
    ambiguity: 'factorAmbiguity',
    interpretive_ambiguity: 'factorAmbiguity',
    structural_risk: 'factorStructuralRisk',
    alternative_interpretation: 'factorAlternativeInterpretation',
  }
  return keys[value] ? t(keys[value]) : humanize(value)
}

function normalizedConfidenceFactor(value: unknown) {
  const normalized = String(value ?? '').trim().toLowerCase().replace(/[^a-z0-9]+/g, '_').replace(/^_+|_+$/g, '')
  const aliases: Record<string, string> = {
    strong: 'high',
    sufficient: 'high',
    direct: 'high',
    adequate: 'high',
    moderate: 'medium',
    partial: 'medium',
    mixed: 'medium',
    weak: 'low',
    insufficient: 'low',
    limited: 'low',
    unclear: 'low',
    na: 'not_applicable',
    n_a: 'not_applicable',
    none: 'not_applicable',
  }
  return aliases[normalized] ?? normalized
}

function confidenceFactorValue(value: unknown, t: ReturnType<typeof useLanguage>['t']) {
  const normalized = normalizedConfidenceFactor(value)
  const labels: Record<string, string> = {
    high: 'confidenceHigh',
    medium: 'confidenceMedium',
    low: 'confidenceLow',
    not_applicable: 'confidenceNotApplicable',
  }
  return labels[normalized] ? t(labels[normalized]) : humanize(normalized)
}

function ConfidenceSummary({
  level,
  rationale,
  rationaleZh,
  factors,
}: {
  level: unknown
  rationale?: unknown
  rationaleZh?: unknown
  factors?: Record<string, unknown>
}) {
  const { language, t } = useLanguage()
  const levelKey = confidenceKey(level)
  const factorRows = Object.entries(factors ?? {}).filter(([, value]) => (
    typeof value === 'string' || typeof value === 'number'
  ))
  return (
    <section className={`confidence-summary ${levelKey ? `confidence-${String(level)}` : 'confidence-unknown'}`}>
      <div className="confidence-heading">
        <span className="section-label">{t('confidence')}</span>
        <strong>{levelKey ? t(levelKey) : t('confidenceNotRecorded')}</strong>
      </div>
      {localized(rationale, rationaleZh, language, '') && (
        <p className="confidence-rationale">{t('confidenceRationale')}: {localized(rationale, rationaleZh, language, '')}</p>
      )}
      {factorRows.length > 0 && (
        <dl className="confidence-factors">
          <dt>{t('confidenceFactors')}</dt>
          {factorRows.map(([name, value]) => <dd key={name}><span>{confidenceFactorLabel(name, t)}</span>{confidenceFactorValue(value, t)}</dd>)}
        </dl>
      )}
    </section>
  )
}

function EvidenceList({ items }: { items: EvidenceItem[] }) {
  const { language, t } = useLanguage()
  if (items.length === 0) {
    return <p className="empty-copy">{t('noGroundedExcerpts')}</p>
  }
  return (
    <ol className="evidence-list">
      {items.map((item, index) => (
        <li key={`${item.field_name}-${index}`}>
          <span className="evidence-number">{evidenceLabel(index)}</span>
          <div>
            <span className="field-label">{item.field_name}</span>
            <blockquote>{item.excerpt}</blockquote>
            {item.rationale && <p className="evidence-rationale">{localized(item.rationale, item.rationale_zh, language, '')}</p>}
          </div>
        </li>
      ))}
    </ol>
  )
}

function ProposedCodes({ codes }: { codes: ProvisionalCode[] }) {
  const { language, t } = useLanguage()
  if (codes.length === 0) {
    return <p className="empty-copy">{t('noCandidateCodes')}</p>
  }
  return (
    <div className="candidate-list">
      {codes.map((code, index) => (
        <article className="candidate" key={`${code.code_name}-${index}`}>
          <div className="candidate-heading">
            <h4>{localized(code.code_name, code.code_name_zh, language)}</h4>
            <span className="relationship-tag">{relationshipLabel(code.relationship_to_codebook, t)}</span>
          </div>
          {localized(code.observed_phenomenon, code.observed_phenomenon_zh, language, '') && (
            <p className="observed-phenomenon"><strong>{t('observedPhenomenon')}:</strong> {localized(code.observed_phenomenon, code.observed_phenomenon_zh, language, '')}</p>
          )}
          <p>{localized(code.short_definition, code.short_definition_zh, language)}</p>
          {localized(code.alternative_interpretation, code.alternative_interpretation_zh, language, '') && (
            <p className="alternative">{t('alternative')}: {localized(code.alternative_interpretation, code.alternative_interpretation_zh, language, '')}</p>
          )}
          {localized(code.uncertainty_note, code.uncertainty_note_zh, language, '') && (
            <p className="uncertainty">{t('uncertainty')}: {localized(code.uncertainty_note, code.uncertainty_note_zh, language, '')}</p>
          )}
        </article>
      ))}
    </div>
  )
}

function RoutingDecisionView({ packet }: { packet: ReviewPacket }) {
  const { language, t } = useLanguage()
  const evidencePacket = packet.review_input.evidence_packet
  const routing = evidencePacket.routing_decision
  if (!routing) return null
  const riskSignals = normalizedRoutingSignals(packet)
  const validation = evidencePacket.validation_output
  const routedCriteria = routing.signal_details?.review_criteria ?? []
  const criteria = routedCriteria.length > 0
    ? routedCriteria
    : (validation?.review_criteria ?? [])
  const routedQuestions = language === 'zh'
    ? (routing.signal_details?.review_questions_zh ?? [])
    : (routing.signal_details?.review_questions ?? [])
  const questions = routedQuestions.length > 0
    ? routedQuestions
    : (language === 'zh' ? (validation?.review_questions_zh ?? []) : (validation?.review_questions ?? []))
  return (
    <section className={`routing-banner route-${routing.route}`}>
      <div>
        <p className="section-label">{t('reviewRouting')}</p>
        <strong>{t(`route_${routing.route}`)}</strong>
      </div>
      <ul>{routing.reasons.map((reason, index) => <li key={`${reason}-${index}`}>{routingReasonLabel(reason, t)}</li>)}</ul>
      {riskSignals.length > 0 && <p><span>{t('riskSignals')}:</span> {riskSignals.map((signal) => translatedOrHumanized(`risk_${signal}`, signal, t)).join(' · ')}</p>}
      {criteria.length > 0 && <p><span>{t('reviewCriteria')}:</span> {criteria.map((criterion) => t(`reviewCriterion_${criterion}`)).join(' · ')}</p>}
      {questions.length > 0 && <div><span>{t('reviewQuestions')}:</span><ul className="text-list">{questions.map((question) => <li key={question}>{question}</li>)}</ul></div>}
      <p className="routing-note">{t('confidenceNotRouting')}</p>
      {routing.random_audit && <span className="audit-chip">{t('randomAudit')}</span>}
    </section>
  )
}

function normalizedRoutingSignals(packet: ReviewPacket) {
  const evidencePacket = packet.review_input.evidence_packet
  const routing = evidencePacket.routing_decision
  const signals = new Set(routing?.risk_signals ?? [])
  const validation = evidencePacket.validation_output
  const validationSignals = new Set(validation?.signals.map((item) => item.signal) ?? [])
  const coders = evidencePacket.coder_outputs
  const comparison = evidencePacket.comparison_output ?? evidencePacket.arbitration_output
  const disagreements = comparison?.disagreements ?? []
  const materialValidationSignals = new Set([
    'evidence_insufficient',
    'unsupported_inference',
    'use_case_mismatch',
  ])

  // Compatibility for persisted packets. Confidence is deliberately never
  // used to add or remove a review signal.
  signals.delete('validation_requires_review')
  signals.delete('moderate_independent_judgment_reliability')
  signals.delete('low_independent_judgment_reliability')
  const materialContextGap = coders.some((coder) => coder.insufficient_context)
    || validationSignals.has('context_missing')
  if (!materialContextGap) signals.delete('missing_context')
  if (![...validationSignals].some((signal) => materialValidationSignals.has(signal))) {
    signals.delete('validation_warning')
  }
  if (disagreements.length > 0 && disagreements.every((item) => (
    item.disagreement_type === 'granularity_disagreement'
    || item.disagreement_type === 'codebook_boundary_disagreement'
    || item.disagreement_type === 'output_format_inconsistency'
  ))) {
    signals.delete('substantive_coder_disagreement')
  }

  const preferredOrder = [
    'missing_context',
    'validation_warning',
    'substantive_coder_disagreement',
    'new_or_ambiguous_boundary',
    'new_code_proposal',
    'structural_codebook_change',
    'high_impact_codebook_revision',
    'conflict_with_prior_human_boundary',
  ]
  return [...signals].sort((left, right) => {
    const leftIndex = preferredOrder.indexOf(left)
    const rightIndex = preferredOrder.indexOf(right)
    return (leftIndex < 0 ? preferredOrder.length : leftIndex)
      - (rightIndex < 0 ? preferredOrder.length : rightIndex)
  })
}

function CodebookChangePackets({ packets }: { packets: NonNullable<ReviewPacket['review_input']['evidence_packet']['codebook_change_packets']> }) {
  const { language, t } = useLanguage()
  if (packets.length === 0) return <p className="empty-copy">{t('noCodebookChangePackets')}</p>
  return (
    <section className="change-packet-list">
      <p className="section-label">{t('codebookChangePackets')}</p>
      {packets.map((packet) => (
        <article className="change-packet" key={packet.change_id}>
          <header><span className={`change-action ${packet.action}`}>{changeActionLabel(packet.action, t)}</span><strong>{localized(packet.summary, packet.summary_zh, language)}</strong></header>
          <p>{localized(packet.rationale, packet.rationale_zh, language)}</p>
          <dl>
            <div><dt>{t('beforeCodes')}</dt><dd>{packet.before_codes.map((code) => `${code.code_id}: ${codeLocalized(code, 'name', language)}`).join(' · ') || t('none')}</dd></div>
            <div><dt>{t('proposedCodes')}</dt><dd>{packet.proposed_codes.map((code) => `${code.code_id}: ${codeLocalized(code, 'name', language)}`).join(' · ') || t('none')}</dd></div>
            <div><dt>{t('supportingCases')}</dt><dd>{packet.supporting_artifact_ids.join(', ') || t('none')}</dd></div>
            <div><dt>{t('boundaryCases')}</dt><dd>{packet.boundary_artifact_ids.join(', ') || t('none')}</dd></div>
            <div><dt>{t('affectedCases')}</dt><dd>{packet.affected_artifact_ids.join(', ') || t('none')}</dd></div>
          </dl>
          {packet.validation_warnings.length > 0 && <div className="change-packet-warnings"><CircleAlert size={15} /> {packet.validation_warnings.join(' · ')}</div>}
        </article>
      ))}
    </section>
  )
}

function ComparisonFindings({ findings }: { findings: ComparisonFinding[] }) {
  const { language, t } = useLanguage()
  if (findings.length === 0) return <p className="empty-copy">{t('noComparisonFindings')}</p>
  return (
    <div className="comparison-findings">
      {findings.map((finding) => (
        <article className="comparison-finding" key={finding.comparison_id}>
          <div className="candidate-heading">
            <h4>{t(`comparisonType_${finding.comparison_type}`)}</h4>
            <span className="relationship-tag">{comparisonFindingLabel(finding.finding, t)}</span>
          </div>
          <p>{localized(finding.summary, finding.summary_zh, language)}</p>
          <p className="detail-rationale">{localized(finding.implication, finding.implication_zh, language)}</p>
          {finding.compared_artifact_ids.length > 0 && <small>{t('comparedArtifacts')}: {finding.compared_artifact_ids.join(', ')}</small>}
          {finding.compared_code_ids.length > 0 && <small>{t('comparedCodes')}: {finding.compared_code_ids.join(', ')}</small>}
        </article>
      ))}
    </div>
  )
}

function AnalyticMemos({ memos }: { memos: AnalyticMemo[] }) {
  const { language, t } = useLanguage()
  if (memos.length === 0) return null
  return (
    <section className="analysis-section comparison-memos">
      <p className="section-label">{t('analyticMemos')}</p>
      {memos.map((memo) => (
        <article className="memo-row" key={memo.memo_id}>
          <span className={`status-dot ${memo.status}`} />
          <div>
            <strong>{memoTypeLabel(memo.memo_type, t)}</strong>
            <p>{localized(memo.summary, memo.summary_zh, language)}</p>
          </div>
        </article>
      ))}
    </section>
  )
}

function workflowOwnerLabel(owner: 'system' | 'agent' | 'human', t: ReturnType<typeof useLanguage>['t']) {
  return t(owner === 'agent' ? 'workflowAgent' : owner === 'human' ? 'workflowHuman' : 'workflowSystem')
}

function ReviewSettingSelector({ value, onChange, locked, busy, onContinue, futureOnly = false }: {
  value: ReviewMode
  onChange: (value: ReviewMode) => void
  locked: boolean
  busy: boolean
  onContinue: () => void
  futureOnly?: boolean
}) {
  const { t } = useLanguage()
  return <fieldset className="initial-review-setting" disabled={locked || busy}>
    <legend>{t('codingReviewSettingTitle')}</legend>
    <div className="initial-review-setting-row">
      <div className="review-setting-options" role="radiogroup" aria-label={t('codingReviewSettingTitle')}>
        {(['automatic', 'selective', 'full'] as const).map((setting) => <button type="button" role="radio" aria-checked={value === setting} key={setting} className={`review-setting-option ${value === setting ? 'selected' : ''}`} onClick={() => { if (value !== setting) onChange(setting) }}>{t(`codingReviewSetting_${setting}`)}</button>)}
      </div>
      <p>{t(`codingReviewSettingDescription_${value}`)}</p>
      {value === 'automatic' && !locked && !futureOnly && <button type="button" className="secondary-action compact" onClick={onContinue}>{busy ? <LoaderCircle size={14} className="spin" /> : <Play size={14} />}{t('continueAutomatically')}</button>}
    </div>
    {locked ? <small>{t('codingReviewSettingLocked')}</small> : futureOnly ? <small>{t('reviewSettingFutureOnly')}</small> : null}
  </fieldset>
}

function BatchComparisonSummary({ packet }: { packet: ReviewPacket | null }) {
  const { language } = useLanguage()
  const batch = packet?.review_input.evidence_packet.model_metadata?.batch_execution
  if (!batch) return null
  return <details className="process-output-card">
    <summary>{language === 'zh' ? '本批协调结果' : 'Batch reconciliation'} · {batch.artifact_ids.length} · B{batch.base_version}</summary>
    <p>{language === 'zh'
      ? `本批材料先共同使用 B${batch.base_version} 比较；当前决定已按 B${batch.validated_version} 检查。`
      : `Initial comparisons shared B${batch.base_version}; this decision was checked against B${batch.validated_version}.`}</p>
    <p>{batch.artifact_ids.join(' · ')}</p>
    <p>{localized(batch.reconciled_proposal.agreement_summary, batch.reconciled_proposal.agreement_summary_zh, language)}</p>
    <ProposedCodes codes={batch.reconciled_proposal.recommended_codes} />
  </details>
}

function WorkflowStageContent({
  stage,
  run,
  current,
  packet,
  codebook,
  onOpenArtifact,
  onPrepare,
  isPreparing,
  onHumanReview,
}: {
  stage: WorkflowStage
  run: RunSummary | null
  current: CurrentArtifactResponse | null
  packet: ReviewPacket | null
  codebook: Codebook | null
  onOpenArtifact: () => void
  onPrepare: () => void
  isPreparing: boolean
  onHumanReview: React.ReactNode
}) {
  const { language, t } = useLanguage()
  const artifact = packet?.review_input.artifact ?? current?.artifact ?? null
  const evidence = packet?.review_input.evidence_packet
  const comparison = evidence?.comparison_output ?? evidence?.arbitration_output
  const showArtifact = () => artifact && <section className="process-material-card"><div className="process-card-heading"><span className="section-label">{t('workflowArtifact')} {artifact.artifact_id}</span><button type="button" className="secondary-action compact" onClick={onOpenArtifact}><FileText size={14} /> {t('workflowOpenArtifact')}</button></div><details className="process-source-preview"><summary>{t('originalArtifact')}</summary><p>{artifact.content}</p></details></section>
  if (stage === 'dataset') return <div className="process-stage-body"><div className="process-facts"><div><span>{t('dataset')}</span><strong>{run?.dataset_display_name ?? t('workflowNotAvailable')}</strong></div><div><span>{t('artifacts')}</span><strong>{run ? t('workflowArtifactCount', { processed: run.reviewed_artifacts, total: run.total_artifacts }) : t('workflowNotAvailable')}</strong></div><div><span>{t('workflowOwner')}</span><strong>{workflowOwnerLabel('system', t)}</strong></div></div>{showArtifact()}</div>
  if (stage === 'initialization') return <div className="process-stage-body"><div className="process-facts"><div><span>{t('bootstrapStatus')}</span><strong>{run ? t(`bootstrapPhase${run.bootstrap_status.charAt(0).toUpperCase()}${run.bootstrap_status.slice(1)}`) : t('workflowNotAvailable')}</strong></div><div><span>{t('bootstrapCodes')}</span><strong>{run ? run.bootstrap_code_count : 0}</strong></div><div><span>{t('workflowOwner')}</span><strong>{workflowOwnerLabel('agent', t)}</strong></div></div>{run?.bootstrap_progress && <div className="process-progress"><div><span>{t('initializationProgress')}</span><strong>{run.bootstrap_progress.percent}%</strong></div><progress max={100} value={run.bootstrap_progress.percent} /></div>}</div>
  if (!run) return <p className="process-empty">{t('workflowSelectRun')}</p>
  if (!packet && stage !== 'coding' && stage !== 'human_review' && stage !== 'codebook_update' && stage !== 'final') return <div className="process-stage-body">{showArtifact()}<div className="process-empty"><p>{t('workflowNoEvidence')}</p><button type="button" className="command-button primary" onClick={onPrepare} disabled={isPreparing}>{isPreparing ? t('preparingPacket') : t('prepareEvidence')}</button></div></div>
  if (stage === 'context') return <div className="process-stage-body">{showArtifact()}<section className="process-output-card"><span className="section-label">{t('contextBrief')}</span><p>{evidence ? localized(evidence.context_packet.context_brief, evidence.context_packet.context_brief_zh, language) : t('workflowNoEvidence')}</p>{evidence && <><span className="section-label">{t('workflowMaterials')}</span><EvidenceList items={evidence.context_packet.evidence_items} />{localizedList(evidence.context_packet.missing_context_warnings, evidence.context_packet.missing_context_warnings_zh, language).map((warning) => <p className="warning-block" key={warning}>{warning}</p>)}</>}</section></div>
  if (stage === 'coding') return <div className="process-stage-body">{showArtifact()}{evidence ? <><div className="process-count"><strong>{t('workflowCoderCount', { count: evidence.coder_outputs.length })}</strong></div><div className="coder-grid">{evidence.coder_outputs.map((coder) => <section className="coder-column" key={coder.coder_id}><div className="coder-title"><Bot size={17} /><h3>{translatedOrHumanized(`coderRole_${coder.coder_id}`, coder.coder_id, t)}</h3></div><ConfidenceSummary level={coder.confidence_level} rationale={coder.confidence_rationale} rationaleZh={coder.confidence_rationale_zh} factors={coder.confidence_factors} /><ProposedCodes codes={coder.provisional_codes} />{localized(coder.overall_uncertainty, coder.overall_uncertainty_zh, language, '') && <p className="uncertainty">{localized(coder.overall_uncertainty, coder.overall_uncertainty_zh, language)}</p>}</section>)}</div></> : null}</div>
  if (stage === 'comparison') return <div className="process-stage-body">{showArtifact()}{evidence && <><BatchComparisonSummary packet={packet} /><div className="process-count"><strong>{t('workflowFindingCount', { count: (evidence.comparison_findings ?? comparison?.comparison_findings ?? []).length })}</strong><strong>{t('workflowChangeCount', { count: (evidence.codebook_change_packets ?? evidence.proposed_codebook_changes).length })}</strong></div>{comparison && <section className="process-output-card"><span className="section-label">{t('comparison')}</span><p>{localized(comparison.agreement_summary, comparison.agreement_summary_zh, language)}</p>{localized(comparison.disagreement_summary, comparison.disagreement_summary_zh, language, '') && <p>{localized(comparison.disagreement_summary, comparison.disagreement_summary_zh, language, '')}</p>}</section>}<ComparisonFindings findings={evidence.comparison_findings ?? comparison?.comparison_findings ?? []} /><ProposedCodes codes={comparison?.recommended_codes ?? []} /><CodebookChangePackets packets={evidence.codebook_change_packets ?? []} /><AnalyticMemos memos={evidence.analytic_memos ?? comparison?.analytic_memos ?? []} /></>}</div>
  if (stage === 'validation') return <div className="process-stage-body">{showArtifact()}{evidence?.validation_output ? <section className="process-output-card"><h3>{localized(evidence.validation_output.summary, evidence.validation_output.summary_zh, language)}</h3><ConfidenceSummary level={evidence.validation_output.confidence_level} rationale={evidence.validation_output.confidence_rationale} rationaleZh={evidence.validation_output.confidence_rationale_zh} factors={evidence.validation_output.confidence_factors} />{evidence.validation_output.signals.map((signal) => <div className="validation-signal" key={`${signal.signal}-${signal.summary}`}><span>{signalLabel(signal.signal, t)}</span><p>{localized(signal.summary, signal.summary_zh, language)}</p></div>)}</section> : <p className="process-empty">{t('workflowNotAvailable')}</p>}</div>
  if (stage === 'human_review') return <div className="process-stage-body">{onHumanReview}</div>
  if (stage === 'codebook_update') return <div className="process-stage-body"><div className="process-facts"><div><span>{t('currentVersion')}</span><strong>v{codebook?.version ?? run.codebook_version}</strong></div><div><span>{t('entries')}</span><strong>{codebook?.codes.length ?? run.code_count}</strong></div><div><span>{t('humanRevisions')}</span><strong>{run.human_reviewed_artifacts}</strong></div></div></div>
  return <div className="process-stage-body"><div className="process-facts"><div><span>{t('workflowStatus')}</span><strong>{statusLabel(run.status, t)}</strong></div><div><span>{t('processed')}</span><strong>{run.reviewed_artifacts} / {run.total_artifacts}</strong></div><div><span>{t('codebook')}</span><strong>v{codebook?.version ?? run.codebook_version} · {codebook?.codes.length ?? run.code_count}</strong></div></div></div>
}

function ProcessWorkbench({
  activeNodeId, onSelectNode, run, stageStatus, workspaceRef, workspaceStyle,
  onResizeStart, onResizeKeyAdjust, children, tools, toolActive, humanReview,
  reviewNodeId, showingReview,
}: {
  activeNodeId: string
  onSelectNode: (nodeId: string) => void
  run: RunSummary | null
  stageStatus: (stage: WorkflowStage) => ReturnType<typeof workflowStageStatus>
  workspaceRef: React.RefObject<HTMLElement | null>
  workspaceStyle: CSSProperties
  onResizeStart: (event: ReactPointerEvent<HTMLButtonElement>, divider: WorkspaceDivider) => void
  onResizeKeyAdjust: (event: ReactKeyboardEvent<HTMLButtonElement>, divider: WorkspaceDivider) => void
  children: React.ReactNode
  tools: React.ReactNode
  toolActive: boolean
  humanReview: React.ReactNode
  reviewNodeId: string
  showingReview: boolean
}) {
  const { t } = useLanguage()
  const activeNode = executionNodes.find((node) => node.id === activeNodeId) ?? executionNodes[0]
  const activeOverview = overviewStages.find((phase) => phase.id === activeNode.overview)
  const initialNode = ['context', 'coding', 'induction', 'initial_validation'].includes(activeNode.id)
  const bootstrapPending = Boolean(run && ['not_run', 'running', 'cancelling', 'failed', 'cancelled', 'interrupted'].includes(run.bootstrap_status))
  const nodeStatus = initialNode && run && bootstrapPending
    ? run.bootstrap_status === 'not_run' ? 'pending'
      : bootstrapNodeForRun(run) !== activeNode.id ? 'pending'
        : ['failed', 'cancelled', 'interrupted'].includes(run.bootstrap_status) ? 'warning' : 'current'
    : stageStatus(activeNode.stage)
  const select = (nodeId: string) => onSelectNode(nodeId)
  return (
    <section ref={workspaceRef} className="process-workspace unified-workspace" style={workspaceStyle} aria-label={t('workflowOverview')}>
      <aside className="workflow-sidebar panel">
        <div className="panel-heading"><div><p className="eyebrow">CODA</p><h2>{t('workflowAgentPath')}</h2></div></div>
        <button type="button" className={`overview-input ${!toolActive && activeNodeId === 'input' ? 'active' : ''}`} onClick={() => select('input')}>
          <span>{t('workflowOverviewInput')}</span><strong>{t('workflowOverviewInputText')}</strong>
        </button>
        <details className="workspace-tools" open={toolActive}>
          <summary>{t('recordsAndTools')}</summary>
          {tools}
        </details>
        <nav className="execution-path" aria-label={t('workflowAgentPath')}>
          {overviewStages.map((phase, index) => (
            <section className={`execution-phase ${!toolActive && activeOverview?.id === phase.id ? 'active' : ''}`} key={phase.id}>
              <header><span className="execution-phase-index">{String(index + 1).padStart(2, '0')}</span><strong>{t(phase.label)}</strong></header>
              <div className="execution-phase-nodes">{executionNodes.filter((node) => node.overview === phase.id).map((node) => {
                const Icon = workflowStages.find((stage) => stage.id === node.stage)?.icon ?? FileText
                const selected = !toolActive && activeNodeId === node.id
                const needsReview = node.id === reviewNodeId && Boolean(run && ['awaiting_initial_review', 'awaiting_final_review', 'awaiting_human_review'].includes(run.status))
                return <button type="button" key={node.id} aria-current={selected ? 'step' : undefined} className={`execution-phase-node ${selected ? 'active' : ''} ${needsReview ? 'needs-review' : ''}`} onClick={() => select(node.id)}>
                  <Icon size={14} /><span>{t(node.label)}</span><small>{t(node.agent)}{needsReview ? ` · ${t('pendingAction')}` : ''}</small>
                </button>
              })}</div>
            </section>
          ))}
        </nav>
      </aside>
      <WorkspaceResizeHandle divider="left" onStart={onResizeStart} onKeyAdjust={onResizeKeyAdjust} />
      <section className={`workflow-stage-content panel ${showingReview ? 'workflow-stage-content-review' : ''}`}>
        {!toolActive && !showingReview && <div className="process-stage-heading"><div><p className="eyebrow">{activeOverview ? t(activeOverview.label) : t('workflowOverviewInput')}</p><h2>{t(activeNode.label)}</h2></div><div className="process-stage-meta"><span>{t('workflowAgent')}: {t(activeNode.agent)}</span><WorkflowStatusLabel status={nodeStatus} /></div></div>}
        <div hidden={!showingReview}>{humanReview}</div>
        <div hidden={showingReview}>{children}</div>
      </section>
    </section>
  )
}

// Initial nodes inspect the bootstrap evidence, rather than the current iterative case.
function InitialNodeEvidence({ run, nodeId }: { run: RunSummary; nodeId: string }) {
  const { language, t } = useLanguage()
  const [packet, setPacket] = useState<StageReviewPacket | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [attempt, setAttempt] = useState(0)
  useEffect(() => {
    let cancelled = false
    setPacket(null)
    setError(null)
    api.getStageReview(run.run_id, 'initial', true).then((next) => {
      if (!cancelled) setPacket(next)
    }).catch((reason) => { if (!cancelled) setError(String(reason.message ?? reason)) })
    return () => { cancelled = true }
  }, [run.run_id, run.codebook_version, attempt])
  if (error) return <div className="process-empty" role="alert"><p>{error}</p><button type="button" className="secondary-action" onClick={() => setAttempt((value) => value + 1)}>{t('refresh')}</button></div>
  if (!packet) return <p className="process-empty" role="status"><LoaderCircle size={16} className="spin" /> {t('loadingInitialEvidence')}</p>
  const initial = packet.bootstrap?.initial_codings ?? packet.initial_codings ?? []
  const initialCodebook = packet.bootstrap?.codebook ?? packet.codebook
  return <div className="process-stage-body">
    <p className="history-intro">{t('initialEvidenceScope')}</p>
    {nodeId === 'context' && initial.map((entry) => <article className="process-output-card" key={entry.artifact_id}>
      <h3>{t('artifact')} {entry.artifact_id}</h3><p>{localized(entry.context_packet?.context_brief, entry.context_packet?.context_brief_zh, language)}</p><EvidenceList items={entry.context_packet?.evidence_items ?? []} />
      {packet.sampled_artifacts?.filter((artifact) => artifact.artifact_id === entry.artifact_id).map((artifact) => <details className="source-document" key={artifact.artifact_id}><summary>{t('originalArtifact')}</summary><pre>{artifact.content}</pre></details>)}
    </article>)}
    {nodeId === 'coding' && initial.map((entry) => <article className="process-output-card" key={entry.artifact_id}><h3>{t('artifact')} {entry.artifact_id}</h3><div className="coder-grid">{entry.coder_outputs.map((coder) => <section className="coder-column" key={coder.coder_id}><h3>{translatedOrHumanized(`coderRole_${coder.coder_id}`, coder.coder_id, t)}</h3><ProposedCodes codes={coder.provisional_codes} /></section>)}</div></article>)}
    {nodeId === 'induction' && <><div className="process-facts"><div><span>{t('bootstrapCodeCount')}</span><strong>{initialCodebook.codes.length}</strong></div><div><span>{t('bootstrapAssignmentArtifactCount')}</span><strong>{packet.bootstrap?.assignments.length ?? packet.assignments?.length ?? 0}</strong></div></div>{initialCodebook.codes.map((code) => <article className="process-output-card" key={code.code_id}><span className="code-id">{code.code_id}</span><h3>{codeLocalized(code, 'name', language)}</h3><p>{codeLocalized(code, 'definition', language)}</p><p className="detail-meta">{t('representativeArtifacts')}: {code.representative_artifact_ids.join(', ')}</p></article>)}</>}
    {nodeId === 'initial_validation' && <><section className="process-output-card"><h3>{t('bootstrapAuditWarnings')}</h3><p>{packet.audit?.status ?? packet.bootstrap?.status ?? t('notRecorded')}</p><PersistedList items={localizedList(packet.audit?.warnings ?? packet.bootstrap?.audit_warnings, packet.audit?.warnings_zh ?? packet.bootstrap?.audit_warnings_zh, language)} empty={t('noBootstrapWarnings')} />{packet.audit?.error && <p role="alert">{packet.audit.error}</p>}</section>{(packet.bootstrap?.assignments ?? packet.assignments)?.map((assignment) => <article className="process-output-card" key={assignment.artifact_id}><h3>{t('artifact')} {assignment.artifact_id}</h3><p>{assignment.code_ids.join(' · ')}</p><PersistedList items={assignment.evidence_summary} empty={t('noEvidenceSummary')} /></article>)}</>}
    {['context', 'coding'].includes(nodeId) && initial.length === 0 && <p className="empty-copy">{t('noInitialCoderOutputs')}</p>}
  </div>
}

function humanize(value: string) {
  return value.replaceAll('_', ' ')
}

function comparisonFindingLabel(value: string, t: ReturnType<typeof useLanguage>['t']) {
  const key = `finding_${value}`
  return t(key) === key ? humanize(value) : t(key)
}

function memoTypeLabel(value: string, t: ReturnType<typeof useLanguage>['t']) {
  const key = `memo_${value}`
  return t(key) === key ? humanize(value) : t(key)
}

function translatedOrHumanized(key: string, fallback: string, t: ReturnType<typeof useLanguage>['t']) {
  const translated = t(key)
  return translated === key ? humanize(fallback) : translated
}

function routingReasonLabel(reason: string, t: ReturnType<typeof useLanguage>['t']) {
  const keys: Record<string, string> = {
    'Full Review requires human review for every artifact.': 'reasonFullReview',
    'Selective Review was triggered by risk signals or the frozen random audit.': 'reasonSelectiveReview',
    'Automatic setting preserves risky cases as unresolved instead of claiming human acceptance.': 'reasonAutomaticUnresolved',
    'No configured review trigger was observed.': 'reasonNoTrigger',
    'Automatic accepted a validated category change under R4 without human approval.': 'reasonAutomaticValidatedChange',
    'Selective Review was triggered by one or more applicable R1-R6 criteria.': 'reasonCriterionReview',
    'Selective Review sampled this otherwise unflagged decision under the fixed 10% audit rule.': 'reasonUnflaggedAudit',
  }
  return keys[reason] ? t(keys[reason]) : reason
}

function stabilityReasonLabel(reason: string, t: ReturnType<typeof useLanguage>['t']) {
  const keys: Record<string, string> = {
    'Recent coding still introduced new categories.': 'stabilityRecentNewCodes',
    'Recent coding still changed category meaning or boundaries.': 'stabilityRecentRevisions',
    'Open unresolved cases remain.': 'stabilityOpenUnresolved',
    'Retrospective propagation tasks remain incomplete.': 'stabilityPendingPropagation',
    'No configured instability signal remained.': 'stabilityNoSignals',
  }
  return keys[reason] ? t(keys[reason]) : reason
}

function relationshipLabel(value: string, t: ReturnType<typeof useLanguage>['t']) {
  const keys: Record<string, string> = {
    reuse_existing_code: 'relationshipReuse', new_code: 'relationshipNew', add_parent_code: 'relationshipAddParent',
    refine_existing_code: 'relationshipRefine', merge_existing_codes: 'relationshipMerge',
    split_existing_code: 'relationshipSplit', uncertain: 'relationshipUncertain',
  }
  return keys[value] ? t(keys[value]) : humanize(value)
}

function signalLabel(value: string, t: ReturnType<typeof useLanguage>['t']) {
  const keys: Record<string, string> = {
    valid: 'signalValid', evidence_insufficient: 'signalEvidenceInsufficient',
    unsupported_inference: 'signalUnsupportedInference', use_case_mismatch: 'signalUseCaseMismatch',
    category_overlap: 'signalCategoryOverlap', boundary_unclear: 'signalBoundaryUnclear',
    context_missing: 'signalContextMissing', human_review_required: 'signalHumanReviewRequired',
  }
  return keys[value] ? t(keys[value]) : humanize(value)
}

function changeActionLabel(value: string, t: ReturnType<typeof useLanguage>['t']) {
  const keys: Record<string, string> = {
    add: 'actionAdd', add_parent: 'actionAddParent', refine: 'actionRefine', merge: 'actionMerge',
    split: 'actionSplit', rename: 'actionRename', retire: 'actionRetire', no_change: 'actionNoChange',
  }
  return keys[value] ? t(keys[value]) : humanize(value)
}

function decisionLabel(value: string, t: ReturnType<typeof useLanguage>['t']) {
  const keys = { accept: 'accept', revise: 'revise', reject: 'reject', mark_uncertain: 'uncertain' } as const
  return value in keys ? t(keys[value as keyof typeof keys]) : humanize(value)
}

function ChangeDetails({ change }: { change: CodebookChange }) {
  const { language, t } = useLanguage()
  return (
    <section className="timeline-detail">
      <div className="timeline-heading">
        <span className={`change-action ${change.action}`}>{changeActionLabel(change.action, t)}</span>
        <span className="muted">{t('reviewVersion', { version: change.round_index })}</span>
      </div>
      <p>{localized(change.summary, change.summary_zh, language)}</p>
      {change.rationale && <p className="detail-rationale">{localized(change.rationale, change.rationale_zh, language, '')}</p>}
      {change.target_code_ids.length > 0 && <p className="detail-meta">{t('affected')}: {change.target_code_ids.join(', ')}</p>}
      {change.resulting_code_ids.length > 0 && <p className="detail-meta">{t('resulting')}: {change.resulting_code_ids.join(', ')}</p>}
    </section>
  )
}

function MemoLifecyclePanel({
  memos,
  onUpdate,
  isSaving,
}: {
  memos: AnalyticMemo[]
  onUpdate: (memoId: string, status: 'open' | 'resolved', rationale: string) => Promise<void>
  isSaving: boolean
}) {
  const { language, t } = useLanguage()
  const [rationales, setRationales] = useState<Record<string, string>>({})
  const [validationError, setValidationError] = useState<string | null>(null)

  async function update(memo: AnalyticMemo) {
    const rationale = rationales[memo.memo_id]?.trim() ?? ''
    if (!rationale) {
      setValidationError(t('memoRationaleRequired'))
      return
    }
    setValidationError(null)
    await onUpdate(
      memo.memo_id,
      memo.status === 'open' ? 'resolved' : 'open',
      rationale,
    )
    setRationales((current) => ({ ...current, [memo.memo_id]: '' }))
  }

  return (
    <section className="memo-lifecycle-panel">
      <div className="section-action-heading">
        <p className="section-label">{t('analyticMemos')}</p>
        <span className="version-chip">{memos.filter((memo) => memo.status === 'open').length} {t('memoOpen')}</span>
      </div>
      <p className="history-intro">{t('memoLifecycleIntro')}</p>
      <div className="memo-lifecycle-list">
        {memos.map((memo) => (
          <article key={memo.memo_id} className={`memo-lifecycle-card ${memo.status}`}>
            <header>
              <strong>{memoTypeLabel(memo.memo_type || 'analytic_memo', t)}</strong>
              <span>{memo.status === 'open' ? t('memoOpen') : t('memoResolved')}</span>
            </header>
            <p>{localized(memo.summary, memo.summary_zh, language)}</p>
            {memo.resolution && <small>{t('memoLatestResolution')}: {memo.resolution}</small>}
            <textarea
              rows={2}
              value={rationales[memo.memo_id] ?? ''}
              onChange={(event) => setRationales((current) => ({
                ...current,
                [memo.memo_id]: event.target.value,
              }))}
              placeholder={memo.status === 'open' ? t('memoResolvePlaceholder') : t('memoReopenPlaceholder')}
            />
            <button
              type="button"
              className="secondary-action compact"
              disabled={isSaving}
              onClick={() => void update(memo)}
            >
              {isSaving ? <LoaderCircle size={13} className="spin" /> : memo.status === 'open' ? <Check size={13} /> : <RefreshCw size={13} />}
              {memo.status === 'open' ? t('resolveMemo') : t('reopenMemo')}
            </button>
          </article>
        ))}
        {memos.length === 0 && <p className="empty-copy">{t('noAnalyticMemos')}</p>}
      </div>
      {validationError && <p className="form-error"><CircleAlert size={14} /> {validationError}</p>}
    </section>
  )
}

function ReviewHistoryView({
  history,
  selectedRecordId,
  onSelectRecord,
  onUpdateMemo,
  isSavingMemo,
}: {
  history: RunHistory | null
  selectedRecordId: string | null
  onSelectRecord: (recordId: string) => void
  onUpdateMemo: (memoId: string, status: 'open' | 'resolved', rationale: string) => Promise<void>
  isSavingMemo: boolean
}) {
  const { language, t } = useLanguage()
  const records = history?.coding_records ?? []
  const selected = records.find((record) => record.record_id === selectedRecordId) ?? records[0] ?? null
  const changes = selected
    ? (history?.codebook_revisions ?? []).filter((change) => change.artifact_ids.includes(selected.artifact_id))
    : []
  const hasTrace = selected
    ? (history?.artifact_runs ?? []).some((trace) => trace.artifact_id === selected.artifact_id)
    : false

  return (
    <section className="history-workspace" aria-label={t('reviewHistory')}>
      <aside className="history-list panel">
        <div className="panel-heading"><div><p className="eyebrow">{t('reviewHistory')} · {t('auditTrail')}</p><h2>{t('reviewHistory')}</h2></div><History size={20} className="heading-icon" /></div>
        <p className="history-intro">{t('reviewHistoryIntro')}</p>
        <div className="record-list">
          {records.map((record) => (
            <button key={record.record_id} type="button" className={selected?.record_id === record.record_id ? 'record-row selected' : 'record-row'} onClick={() => onSelectRecord(record.record_id)}>
              <span className={`decision-tag ${record.decision}`}>{decisionLabel(record.decision, t)}</span>
              <strong>{t('artifact')} {record.artifact_id}</strong>
              <small>{t('startedAt', { version: record.codebook_version })}</small>
            </button>
          ))}
          {records.length === 0 && <p className="empty-copy">{t('noHumanReviews')}</p>}
        </div>
        <MemoLifecyclePanel
          memos={history?.analytic_memos ?? []}
          onUpdate={onUpdateMemo}
          isSaving={isSavingMemo}
        />
      </aside>

      <section className="record-detail panel">
        {!selected && <p className="empty-workspace">{t('submitToAudit')}</p>}
        {selected && (
          <>
            <div className="panel-heading"><div><p className="eyebrow">{t('artifactHumanDecision', { id: selected.artifact_id })}</p><h2>{decisionLabel(selected.decision, t)}</h2></div>{hasTrace && <span className="version-chip">{t('agentTraceSaved')}</span>}</div>
            <div className="detail-grid">
              <section><p className="section-label">{t('finalCodes')}</p>{selected.final_code_names.length > 0 ? <ul className="detail-list">{selected.final_code_names.map((name, index) => <li key={`${name}-${index}`}>{name}<span>{selected.final_code_ids[index] ?? ''}</span></li>)}</ul> : <p className="empty-copy">{t('noFinalCode')}</p>}</section>
              <section><p className="section-label">{t('validationSignals')}</p>{selected.validation_signals.length > 0 ? <div className="signal-pills">{selected.validation_signals.map((signal) => <span key={signal}>{signalLabel(signal, t)}</span>)}</div> : <p className="empty-copy">{t('noValidationSignals')}</p>}</section>
            </div>
            <section className="detail-section"><p className="section-label">{t('independentPreRead')}</p><p>{selected.pre_read_memo || t('notRecordedLegacy')}</p></section>
            <section className="detail-section"><p className="section-label">{t('decisionRationale')}</p><p>{selected.rationale}</p></section>
            <section className="detail-section"><p className="section-label">{t('acceptedEvidence')}</p>{selected.evidence_summary.length > 0 ? <ul className="text-list">{selected.evidence_summary.map((item, index) => <li key={`${item}-${index}`}>{item}</li>)}</ul> : <p className="empty-copy">{t('noEvidenceSummary')}</p>}</section>
            {selected.preserved_alternatives.length > 0 && <section className="detail-section"><p className="section-label">{t('preservedAlternatives')}</p><ul className="text-list">{selected.preserved_alternatives.map((item, index) => <li key={`${item}-${index}`}>{item}</li>)}</ul></section>}
            <section className="detail-section"><p className="section-label">{t('recordedChanges')}</p>{changes.length > 0 ? changes.map((change) => <ChangeDetails key={change.change_id} change={change} />) : <p className="empty-copy">{t('noStructuralChange')}</p>}</section>
          </>
        )}
      </section>
    </section>
  )
}

function CodebookEvolutionView({ codebook, history }: { codebook: Codebook | null; history: RunHistory | null }) {
  const { language, t } = useLanguage()
  const revisions = history?.codebook_revisions ?? []
  const versions = history?.codebook_versions?.snapshots ?? []
  const diffs = history?.codebook_versions?.diffs ?? []
  return (
    <section className="evolution-workspace" aria-label={t('codebookEvolution')}>
      <aside className="evolution-summary panel">
        <div className="panel-heading"><div><p className="eyebrow">{t('currentCodebook')}</p><h2>{t('codebookEvolution')}</h2></div><GitBranch size={20} className="heading-icon" /></div>
        <dl className="evolution-facts"><div><dt>{t('currentVersion')}</dt><dd>v{codebook?.version ?? 0}</dd></div><div><dt>{t('entries')}</dt><dd>{codebook?.codes.length ?? 0}</dd></div><div><dt>{t('humanRevisions')}</dt><dd>{revisions.length}</dd></div></dl>
        <p className="history-intro">{t('evolutionIntro')}</p>
        <div className="current-code-list">
          {codebook?.codes.map((code) => <div key={code.code_id}><strong>{codeLocalized(code, 'name', language)}</strong><span>{code.code_id}</span></div>)}
          {codebook?.codes.length === 0 && <p className="empty-copy">{t('codebookStillEmpty')}</p>}
        </div>
      </aside>
      <section className="timeline-panel panel">
        <div className="panel-heading"><div><p className="eyebrow">{t('humanConfirmedRevisions')}</p><h2>{t('changeTimeline')}</h2></div><span className="version-chip">{revisions.length} {t('events')}</span></div>
        <div className="timeline">
          {versions.length > 0 && <section className="version-snapshots"><p className="section-label">{t('immutableSnapshots')}</p><div className="snapshot-strip">{versions.map((snapshot) => <span key={snapshot.version}>v{snapshot.version} · {snapshot.codes.length} {t('entries').toLocaleLowerCase()}</span>)}</div>{diffs.map((diff) => <details key={`${diff.from_version}-${diff.to_version}`} className="version-diff"><summary>v{diff.from_version} → v{diff.to_version}</summary><p>{diff.added.length} {t('added')} · {diff.removed.length} {t('removed')} · {diff.changed.length} {t('changed')}</p>{diff.changed.map((item) => <p key={item.after.code_id} className="detail-meta">{item.after.code_id}: {codeLocalized(item.before, 'name', language)} → {codeLocalized(item.after, 'name', language)}</p>)}</details>)}</section>}
          {revisions.map((change, index) => <div className="timeline-event" key={change.change_id}><span className="timeline-index">{String(index + 1).padStart(2, '0')}</span><ChangeDetails change={change} /><p className="timeline-artifacts">Artifact{change.artifact_ids.length === 1 ? '' : 's'}: {change.artifact_ids.join(', ') || 'not recorded'}</p></div>)}
          {revisions.length === 0 && <p className="empty-workspace">{t('noExplicitChanges')}</p>}
        </div>
      </section>
    </section>
  )
}

function asObject(value: unknown): Record<string, unknown> | null {
  return value !== null && typeof value === 'object' && !Array.isArray(value)
    ? value as Record<string, unknown>
    : null
}

function textValue(value: unknown, fallback = 'Not recorded') {
  return typeof value === 'string' || typeof value === 'number' ? String(value) : fallback
}

function traceContextBrief(trace: Record<string, unknown>, language: 'en' | 'zh') {
  const context = asObject(trace.context_packet)
  return localized(context?.context_brief, context?.context_brief_zh, language, 'No context brief was persisted.')
}

function traceCodeCount(trace: Record<string, unknown>) {
  const outputs = trace.coder_outputs
  return Array.isArray(outputs) ? outputs.length : 0
}

function stringArray(value: unknown) {
  return Array.isArray(value)
    ? value.filter((item): item is string => typeof item === 'string' && item.trim().length > 0)
    : []
}

function objectArray(value: unknown) {
  return Array.isArray(value)
    ? value.filter((item): item is Record<string, unknown> => asObject(item) !== null)
    : []
}

function enrichCodebookTranslations(codebook: Codebook | null, traces: Array<Record<string, unknown>>) {
  if (!codebook || traces.length === 0) return codebook
  const byName = new Map<string, { nameZh: string; definitionZh: string }>()
  const byCodeId = new Map<string, { nameZh: string; definitionZh: string }>()

  const remember = (candidate: Record<string, unknown>) => {
    const name = textValue(candidate.code_name, '').trim()
    const nameZh = textValue(candidate.code_name_zh, '').trim()
    const definitionZh = textValue(candidate.short_definition_zh, '').trim()
    if (!name || (!nameZh && !definitionZh)) return
    const translation = { nameZh, definitionZh }
    byName.set(name.toLocaleLowerCase(), translation)
    if (candidate.relationship_to_codebook === 'reuse_existing_code' || candidate.relationship_to_codebook === 'refine_existing_code') {
      stringArray(candidate.linked_code_ids).forEach((codeId) => byCodeId.set(codeId, translation))
    }
  }

  traces.forEach((trace) => {
    objectArray(trace.coder_outputs).forEach((coder) => {
      objectArray(coder.provisional_codes).forEach(remember)
    })
    const comparison = asObject(trace.comparison_output) ?? asObject(trace.arbitration_output)
    if (!comparison) return
    objectArray(comparison.recommended_codes).forEach(remember)
    objectArray(comparison.preserved_alternatives).forEach(remember)
  })

  return {
    ...codebook,
    codes: codebook.codes.map((code) => {
      const currentNameZh = textValue(code.metadata?.name_zh, '').trim()
      const currentDefinitionZh = textValue(code.metadata?.definition_zh, '').trim()
      if (currentNameZh && currentDefinitionZh) return code
      const translation = byCodeId.get(code.code_id) ?? byName.get(code.name.toLocaleLowerCase())
      if (!translation) return code
      return {
        ...code,
        metadata: {
          ...code.metadata,
          name_zh: currentNameZh || translation.nameZh,
          definition_zh: currentDefinitionZh || translation.definitionZh,
        },
      }
    }),
  }
}

function PersistedList({ items, empty }: { items: string[]; empty: string }) {
  if (items.length === 0) return <p className="empty-copy">{empty}</p>
  return <ul className="text-list">{items.map((item, index) => <li key={`${item}-${index}`}>{item}</li>)}</ul>
}

function PersistedReviewSummary({ review }: { review: Record<string, unknown> }) {
  const { language, t } = useLanguage()
  const finalNames = stringArray(review.final_code_names)
  const finalIds = stringArray(review.final_code_ids)
  const codes = finalNames.map((name, index) => `${name}${finalIds[index] ? ` (${finalIds[index]})` : ''}`)
  const evidence = stringArray(review.evidence_summary)
  const alternatives = stringArray(review.preserved_alternatives)
  const changes = objectArray(review.codebook_changes)
  return (
    <div className="persisted-summary">
      <div className="detail-grid">
        <section><p className="section-label">{t('finalCodes')}</p><PersistedList items={codes} empty={t('noFinalCode')} /></section>
        <section><p className="section-label">{t('codebook')}</p><p className="summary-value">v{textValue(review.codebook_version_after_review)}</p></section>
      </div>
      <section className="detail-section"><p className="section-label">{t('decisionRationale')}</p><p>{textValue(review.rationale)}</p></section>
      <section className="detail-section"><p className="section-label">{t('acceptedEvidence')}</p><PersistedList items={evidence} empty={t('noEvidenceSummary')} /></section>
      {alternatives.length > 0 && <section className="detail-section"><p className="section-label">{t('preservedAlternatives')}</p><PersistedList items={alternatives} empty="" /></section>}
      <section className="detail-section"><p className="section-label">{t('recordedChanges')}</p>{changes.length > 0 ? changes.map((change, index) => <div className="persisted-change" key={`${textValue(change.change_id, 'change')}-${index}`}><strong>{changeActionLabel(textValue(change.action), t)}</strong><p>{localized(change.summary, change.summary_zh, language)}</p>{localized(change.rationale, change.rationale_zh, language, '') && <small>{localized(change.rationale, change.rationale_zh, language, '')}</small>}</div>) : <p className="empty-copy">{t('noStructuralChange')}</p>}</section>
    </div>
  )
}

function PersistedCoderSummary({ coder }: { coder: Record<string, unknown> }) {
  const { language, t } = useLanguage()
  const candidates = objectArray(coder.provisional_codes)
  const coderId = textValue(coder.coder_id, 'coder')
  return (
    <section className="trace-summary-section">
      <div className="trace-summary-heading"><strong>{translatedOrHumanized(`coderRole_${coderId}`, coderId, t)}</strong><span>{candidates.length} {t('candidateCodesLabel')}</span></div>
      {candidates.length === 0 ? <p className="empty-copy">{t('noCandidateCodes')}</p> : <div className="persisted-candidate-list">{candidates.map((candidate, index) => <article className="persisted-candidate" key={`${textValue(candidate.code_name, 'candidate')}-${index}`}><strong>{localized(candidate.code_name, candidate.code_name_zh, language)}</strong><span>{relationshipLabel(textValue(candidate.relationship_to_codebook, 'unknown'), t)}</span><p>{localized(candidate.short_definition, candidate.short_definition_zh, language)}</p>{localized(candidate.uncertainty_note, candidate.uncertainty_note_zh, language, '') && <small>{t('uncertainty')}: {localized(candidate.uncertainty_note, candidate.uncertainty_note_zh, language, '')}</small>}</article>)}</div>}
      <ConfidenceSummary level={coder.confidence_level} rationale={coder.confidence_rationale} rationaleZh={coder.confidence_rationale_zh} factors={asObject(coder.confidence_factors) ?? undefined} />
      {localized(coder.overall_uncertainty, coder.overall_uncertainty_zh, language, '') && <p className="uncertainty">{t('uncertainty')}: {localized(coder.overall_uncertainty, coder.overall_uncertainty_zh, language, '')}</p>}
    </section>
  )
}

function PersistedTraceSummary({ trace }: { trace: Record<string, unknown> }) {
  const { language, t } = useLanguage()
  const context = asObject(trace.context_packet)
  const coders = objectArray(trace.coder_outputs)
  const comparison = asObject(trace.comparison_output) ?? asObject(trace.arbitration_output)
  const validation = asObject(trace.validation_output)
  const recommended = comparison ? objectArray(comparison.recommended_codes) : []
  const signals = validation ? objectArray(validation.signals) : []
  return (
    <div className="persisted-summary trace-summary">
      <section className="detail-section"><p className="section-label">{t('contextBrief')}</p><p>{localized(context?.context_brief, context?.context_brief_zh, language, t('noContextBrief'))}</p></section>
      <section className="detail-section"><p className="section-label">{t('coderOutputs')}</p>{coders.length > 0 ? <div className="trace-summary-list">{coders.map((coder, index) => <PersistedCoderSummary key={`${textValue(coder.coder_id, 'coder')}-${index}`} coder={coder} />)}</div> : <p className="empty-copy">{t('noTrace')}</p>}</section>
      <section className="detail-section"><p className="section-label">{t('comparison')}</p>{comparison ? <><p>{localized(comparison.agreement_summary, comparison.agreement_summary_zh, language, t('notRecorded'))}</p>{localized(comparison.disagreement_summary, comparison.disagreement_summary_zh, language, '') && <p className="detail-rationale">{localized(comparison.disagreement_summary, comparison.disagreement_summary_zh, language, '')}</p>}{recommended.length > 0 && <div className="persisted-candidate-list">{recommended.map((candidate, index) => <article className="persisted-candidate" key={`${textValue(candidate.code_name, 'recommendation')}-${index}`}><strong>{localized(candidate.code_name, candidate.code_name_zh, language)}</strong><p>{localized(candidate.short_definition, candidate.short_definition_zh, language)}</p></article>)}</div>}</> : <p className="empty-copy">{t('notRecorded')}</p>}</section>
      <section className="detail-section"><p className="section-label">{t('validation')}</p>{validation ? <><p>{localized(validation.summary, validation.summary_zh, language, t('notRecorded'))}</p><ConfidenceSummary level={validation.confidence_level} rationale={validation.confidence_rationale} rationaleZh={validation.confidence_rationale_zh} factors={asObject(validation.confidence_factors) ?? undefined} />{signals.length > 0 && <div className="trace-signal-list">{signals.map((signal, index) => <div key={`${textValue(signal.signal, 'signal')}-${index}`}><strong>{signalLabel(textValue(signal.signal), t)}</strong><p>{localized(signal.summary, signal.summary_zh, language)}</p></div>)}</div>}</> : <p className="empty-copy">{t('notRecorded')}</p>}</section>
    </div>
  )
}

function RunArtifactsView({
  data,
  isLoading,
  onRefresh,
}: {
  data: RunArtifacts | null
  isLoading: boolean
  onRefresh: () => Promise<void>
}) {
  const { language, t } = useLanguage()
  const [activeTab, setActiveTab] = useState<LogTab>('checkpoint')
  const [selectedTraceId, setSelectedTraceId] = useState<string | null>(null)
  const traces = data?.artifact_runs ?? []
  const selectedTrace = traces.find((trace) => trace.artifact_id === selectedTraceId) ?? traces[0] ?? null

  if (!data) {
    return (
    <section className="logs-workspace panel" aria-label={t('runArtifacts')}>
        <div className="panel-heading"><div><p className="eyebrow">{t('persistedRecords')}</p><h2>{t('runArtifacts')}</h2></div><ScrollText size={20} className="heading-icon" /></div>
        <div className="empty-workspace"><p>{isLoading ? t('readingFiles') : t('openRunLoad')}</p>{!isLoading && <button type="button" className="command-button primary" onClick={() => void onRefresh()}>{t('loadRunArtifacts')}</button>}</div>
      </section>
    )
  }

  return (
    <section className="logs-workspace panel" aria-label={t('runArtifacts')}>
      <div className="panel-heading"><div><p className="eyebrow">{t('readOnlyRecords')}</p><h2>{t('runArtifacts')}</h2></div><button type="button" className="icon-button" onClick={() => void onRefresh()} disabled={isLoading} title={t('reloadFiles')}><RefreshCw size={16} className={isLoading ? 'spin' : ''} /></button></div>
      <nav className="workspace-tabs logs-tabs" aria-label={t('runArtifactFiles')}>
        <button type="button" className={activeTab === 'checkpoint' ? 'active' : ''} onClick={() => setActiveTab('checkpoint')}>{t('checkpoint')}</button>
        <button type="button" className={activeTab === 'reviews' ? 'active' : ''} onClick={() => setActiveTab('reviews')}>{t('reviewLog')}</button>
        <button type="button" className={activeTab === 'traces' ? 'active' : ''} onClick={() => setActiveTab('traces')}>{t('agentTraces')}</button>
        <button type="button" className={activeTab === 'final_codebook' ? 'active' : ''} onClick={() => setActiveTab('final_codebook')}>{t('finalCodebook')}</button>
      </nav>

      {activeTab === 'checkpoint' && <div className="checkpoint-grid">{Object.entries(data.checkpoint).map(([key, value]) => <div key={key}><span>{humanize(key)}</span><strong>{textValue(value)}</strong></div>)}</div>}
      {activeTab === 'reviews' && <div className="log-records">{data.reviews.map((review, index) => <details key={`${textValue(review.artifact_id, 'artifact')}-${index}`}><summary><span>{t('artifact')} {textValue(review.artifact_id)}</span><em>{decisionLabel(textValue(review.decision), t)}</em></summary><PersistedReviewSummary review={review} /><details className="raw-trace"><summary>{t('viewTechnicalDetails')}</summary><pre>{JSON.stringify(review, null, 2)}</pre></details></details>)}{data.reviews.length === 0 && <p className="empty-workspace">{t('noReviewLog')}</p>}</div>}
      {activeTab === 'final_codebook' && <div className="final-file-view">{data.final_codebook.available && data.final_codebook.snapshot ? <><p className="history-intro">{t('finalFileIntro')}</p><div className="final-code-list-view">{data.final_codebook.snapshot.codes.map((code) => <article key={code.code_id}><span>{code.code_id}</span><strong>{codeLocalized(code, 'name', language)}</strong><p>{codeLocalized(code, 'definition', language)}</p></article>)}</div><details className="raw-trace"><summary>{t('viewFinalFile')}</summary><pre>{JSON.stringify(data.final_codebook.snapshot, null, 2)}</pre></details></> : <p className="empty-workspace">{t('runNotComplete')}</p>}</div>}
    </section>
  )
}

function BootstrapRunView({
  data,
  isLoading,
  onRefresh,
}: {
  data: RunArtifacts | null
  isLoading: boolean
  onRefresh: () => Promise<void>
}) {
  const { language, t } = useLanguage()
  const bootstrap: BootstrapInspection | null = data?.bootstrap ?? null
  if (!data) {
    return <section className="bootstrap-workspace panel"><div className="panel-heading"><div><p className="eyebrow">{t('bootstrapLabel')}</p><h2>{t('bootstrapRecord')}</h2></div><Sparkles size={20} className="heading-icon" /></div><div className="empty-workspace"><p>{isLoading ? t('readingBootstrap') : t('loadBootstrap')}</p>{!isLoading && <button type="button" className="command-button primary" onClick={() => void onRefresh()}>{t('loadBootstrap')}</button>}</div></section>
  }
  if (!bootstrap) {
    return <section className="bootstrap-workspace panel"><div className="panel-heading"><div><p className="eyebrow">{t('bootstrapLabel')}</p><h2>{t('bootstrapRecord')}</h2></div></div><p className="empty-workspace">{t('noBootstrapRecord')}</p></section>
  }
  const protocolRows = [
    ['fraction', 'bootstrapFraction'], ['minimum_size', 'bootstrapMinimum'], ['maximum_size', 'bootstrapMaximum'],
    ['batch_size', 'bootstrapBatchSize'], ['random_seed', 'bootstrapSeed'], ['sampler', 'bootstrapSampler'],
  ] as const
  const initialCodings = bootstrap.initial_codings ?? []
  return (
    <section className="bootstrap-workspace panel" aria-label={t('bootstrapRecord')}>
      <div className="panel-heading"><div><p className="eyebrow">{t('bootstrapLabelB1')}</p><h2>{t('bootstrapRecord')}</h2></div><span className={`bootstrap-run-status ${bootstrap.status}`}>{bootstrapStatusLabel(bootstrap.status, language)}</span></div>
      <p className="history-intro">{bootstrap.status === 'completed' ? t('bootstrapRecordIntro') : t('bootstrapFallbackIntro')}</p>
      {bootstrap.error && <p className="bootstrap-error">{bootstrap.error}</p>}
      <section className="bootstrap-summary-grid">
        <div><span>{t('bootstrapCodeCount')}</span><strong>{bootstrap.codebook.codes.length}</strong></div>
        <div><span>{t('bootstrapAssignmentArtifactCount')}</span><strong>{bootstrap.assignments.length}</strong></div>
      </section>
      <section className="bootstrap-section"><p className="section-label">{t('bootstrapProtocol')}</p><div className="bootstrap-protocol">{protocolRows.map(([key, label]) => <div key={key}><span>{t(label)}</span><strong>{textValue(bootstrap.protocol[key])}</strong></div>)}</div></section>
      <section className="bootstrap-section"><p className="section-label">{t('bootstrapPipeline')}</p><div className="bootstrap-pipeline"><span>{t('bootstrapStageSample')}</span><ChevronRight size={14} /><span>{t('bootstrapStageEvidence')}</span><ChevronRight size={14} /><span>{t('bootstrapStageInitialCoding')}</span><ChevronRight size={14} /><span>{t('bootstrapStageInduction')}</span><ChevronRight size={14} /><span>{t('bootstrapStageAudit')}</span><ChevronRight size={14} /><span>{t('bootstrapStageLabel')}</span></div></section>
      <section className="bootstrap-section"><p className="section-label">{t('bootstrapInitialCoderOutputs')}</p>{initialCodings.length > 0 ? <div className="bootstrap-assignment-list">{initialCodings.map((codingCase) => <details key={codingCase.artifact_id}><summary>{t('artifact')} {codingCase.artifact_id} · {codingCase.coder_outputs.length} {t('coders')}</summary>{codingCase.coder_outputs.map((output) => <article key={`${codingCase.artifact_id}-${output.coder_id}`}><header><strong>{translatedOrHumanized(`coderRole_${output.coder_id}`, output.coder_id, t)}</strong><span>{textValue(output.model_metadata?.model)}</span></header>{output.provisional_codes.map((code, index) => <p key={`${code.code_name}-${index}`}><strong>{localized(code.code_name, code.code_name_zh, language)}</strong>: {localized(code.short_definition, code.short_definition_zh, language)}</p>)}</article>)}</details>)}</div> : <p className="empty-copy">{t('noInitialCoderOutputs')}</p>}</section>
      <section className="bootstrap-section"><p className="section-label">{t('bootstrapInitialCodes')}</p>{bootstrap.codebook.codes.length > 0 ? <div className="bootstrap-code-list">{bootstrap.codebook.codes.map((code) => <article key={code.code_id}><span>{code.code_id}</span><strong>{codeLocalized(code, 'name', language)}</strong><p>{codeLocalized(code, 'definition', language)}</p><small>{code.representative_artifact_ids.join(', ')}</small></article>)}</div> : <p className="empty-copy">{t('noCodesSnapshot')}</p>}</section>
      <section className="bootstrap-section"><p className="section-label">{t('bootstrapAssignments')}</p>{bootstrap.assignments.length > 0 ? <div className="bootstrap-assignment-list">{bootstrap.assignments.map((assignment) => <article key={assignment.artifact_id}><header><strong>{t('artifact')} {assignment.artifact_id}</strong><span>{assignment.status}</span></header><p>{assignment.code_ids.join(' · ') || t('noCodesSnapshot')}</p>{assignment.evidence_summary.length > 0 && <ul>{assignment.evidence_summary.map((evidence, index) => <li key={`${assignment.artifact_id}-${index}`}>{evidence}</li>)}</ul>}</article>)}</div> : <p className="empty-copy">{t('noBootstrapAssignments')}</p>}</section>
      <section className="bootstrap-section"><p className="section-label">{t('bootstrapAuditWarnings')}</p><PersistedList items={localizedList(bootstrap.audit_warnings, bootstrap.audit_warnings_zh, language)} empty={t('noBootstrapWarnings')} /></section>
      <section className="bootstrap-section"><p className="section-label">{t('bootstrapChangeLog')}</p>{bootstrap.change_log.length > 0 ? <div className="bootstrap-changes">{bootstrap.change_log.map((change, index) => <p key={`${change.action ?? 'change'}-${index}`}><strong>{change.action ?? 'change'}</strong> {change.summary ?? ''}</p>)}</div> : <p className="empty-copy">{t('noBootstrapChanges')}</p>}</section>
      <details className="raw-trace"><summary>{t('viewTechnicalDetails')}</summary><pre>{JSON.stringify(bootstrap, null, 2)}</pre></details>
    </section>
  )
}

function bootstrapStatusLabel(status: BootstrapInspection['status'], language: 'en' | 'zh') {
  const labels: Record<BootstrapInspection['status'], Record<'en' | 'zh', string>> = {
    not_run: { en: 'not started', zh: '未开始' },
    running: { en: 'running', zh: '进行中' },
    cancelling: { en: 'stopping', zh: '正在停止' },
    cancelled: { en: 'paused', zh: '已暂停' },
    interrupted: { en: 'interrupted', zh: '已中断' },
    completed: { en: 'completed', zh: '已完成' },
    failed: { en: 'failed', zh: '失败' },
    skipped: { en: 'skipped', zh: '已跳过' },
    disabled: { en: 'disabled', zh: '未启用' },
  }
  return labels[status][language]
}

function bootstrapPhaseLabel(phase: string, t: ReturnType<typeof useLanguage>['t']) {
  const keys: Record<string, string> = {
    pending: 'bootstrapPhasePending',
    starting: 'bootstrapPhaseStarting',
    evidence: 'bootstrapStageEvidence',
    initial_coding: 'bootstrapStageInitialCoding',
    induction: 'bootstrapStageInduction',
    codebook: 'bootstrapStageInduction',
    audit: 'bootstrapStageAudit',
    assignment: 'bootstrapStageLabel',
    reinduction: 'bootstrapStageReinduction',
    reassignment: 'bootstrapStageReassignment',
    revalidation: 'bootstrapStageRevalidation',
    completed: 'bootstrapPhaseCompleted',
    failed: 'bootstrapPhaseFailed',
    cancelling: 'bootstrapPhaseCancelling',
    cancelled: 'bootstrapPhaseCancelled',
    interrupted: 'bootstrapPhaseInterrupted',
    skipped: 'bootstrapPhaseSkipped',
    disabled: 'bootstrapPhaseDisabled',
  }
  return keys[phase] ? t(keys[phase]) : humanize(phase)
}

function BootstrapProgressView({ progress }: { progress?: BootstrapProgress }) {
  const { t } = useLanguage()
  if (!progress) return null
  const total = Math.max(0, Number(progress.total_artifacts) || 0)
  const processed = Math.min(total, Math.max(0, Number(progress.processed_artifacts) || 0))
  const overallPercent = Math.min(100, Math.max(0, Number(progress.percent) || 0))
  const phasePercent = total > 0
    ? Math.round((processed / total) * 100)
    : progress.status === 'completed' ? 100 : 0
  const legacyStageIndex: Record<string, number> = {
    evidence: 1,
    initial_coding: 2,
    induction: 3,
    codebook: 3,
    assignment: 4,
    validation: 5,
    reinduction: 6,
    reassignment: 7,
    revalidation: 8,
    completed: 8,
  }
  const stageIndex = Math.max(
    0,
    Number(progress.stage_index) || legacyStageIndex[progress.phase] || 0,
  )
  const stageTotal = Math.max(0, Number(progress.stage_total) || 8)
  return (
    <section className="bootstrap-progress" aria-live="polite" aria-label={t('initializationProgress')}>
      <div className="bootstrap-progress-heading">
        <div>
          <p className="section-label">{t('currentPhaseProgress')}</p>
          <strong>{processed} / {total} {t('artifacts')}</strong>
        </div>
        <strong className="bootstrap-progress-percent">{phasePercent}%</strong>
      </div>
      <div
        className="bootstrap-progress-track"
        role="progressbar"
        aria-valuemin={0}
        aria-valuemax={100}
        aria-valuenow={phasePercent}
        aria-valuetext={`${processed} / ${total}`}
      >
        <span style={{ width: `${phasePercent}%` }} />
      </div>
      <div className="bootstrap-progress-meta">
        <span>{t('bootstrapPhase')}: {bootstrapPhaseLabel(progress.phase, t)}</span>
        {progress.current_artifact_id && <span>{t('bootstrapCurrentArtifact')}: {progress.current_artifact_id}</span>}
      </div>
      {stageTotal > 0 && (
        <p className="bootstrap-overall-progress">
          {t('overallInitializationProgress')}: {overallPercent}% · {t('currentWorkflowStage')}: {stageIndex} / {stageTotal}
        </p>
      )}
    </section>
  )
}

function TaskSetupView({
  run,
  isInitializing,
  isStopping,
  onInitialize,
  onCancel,
  retry,
}: {
  run: RunSummary
  isInitializing: boolean
  isStopping: boolean
  onInitialize: () => Promise<void>
  onCancel: () => Promise<void>
  retry: boolean
}) {
  const { t } = useLanguage()
  const running = isInitializing || isStopping || run.bootstrap_status === 'running' || run.bootstrap_status === 'cancelling'
  const stopping = isStopping || run.bootstrap_status === 'cancelling'
  const failed = run.bootstrap_status === 'failed'
  const title = stopping ? 'stoppingInitialization' : running ? 'initializationInProgress' : failed ? 'initializationFailed' : retry ? 'initializationPaused' : 'taskCreated'
  return (
    <section className="task-setup-workspace" aria-label={t('taskCreated')}>
      <div className="task-setup-card">
        <Sparkles size={24} className="heading-icon" />
        <p className="eyebrow">{t('initializationProgress')}</p>
        <h2>{t(title)}</h2>
        <p>{stopping ? t('initializationStopHint') : running ? t('initializationInProgressIntro') : failed ? t('initializationFailedIntro') : retry ? t('initializationPausedIntro') : t('taskSetupIntro')}</p>
        <dl className="task-setup-facts">
          <div><dt>{t('activeDataset')}</dt><dd>{run.dataset_display_name}</dd></div>
          <div><dt>{t('inputArtifacts', { count: run.input_artifacts })}</dt><dd>{run.input_artifacts}</dd></div>
          <div><dt>{t('codebook')}</dt><dd>v{run.codebook_version}</dd></div>
        </dl>
        {running && <BootstrapProgressView progress={run.bootstrap_progress} />}
        {running ? (
          <button type="button" className="command-button primary task-initialize-button" onClick={() => void onCancel()} disabled={stopping}>
            {stopping ? <LoaderCircle size={16} className="spin" /> : <X size={16} />}
            {stopping ? t('stoppingInitialization') : t('stopInitialization')}
          </button>
        ) : (
          <button type="button" className="command-button primary task-initialize-button" onClick={() => void onInitialize()}>
            <Sparkles size={16} />
            {retry ? t('resumeInitialization') : t('initializeTask')}
          </button>
        )}
      </div>
    </section>
  )
}

function retrospectiveStatusLabel(status: RetrospectiveTask['status'], t: ReturnType<typeof useLanguage>['t']) {
  const keys: Record<RetrospectiveTask['status'], string> = {
    pending: 'retrospectivePending',
    prepared: 'retrospectivePrepared',
    awaiting_human: 'retrospectiveAwaitingHuman',
    completed: 'retrospectiveCompleted',
    cancelled: 'retrospectiveCancelled',
  }
  return t(keys[status])
}

function contextRequestStatusLabel(status: ContextRequest['status'], t: ReturnType<typeof useLanguage>['t']) {
  const keys: Record<ContextRequest['status'], string> = {
    pending: 'contextRequestPending',
    resolved: 'contextRequestResolved',
    cancelled: 'contextRequestCancelled',
  }
  return t(keys[status])
}

function ContextRequestsView({
  requests,
  onResolve,
  onCancel,
  isSaving,
}: {
  requests: ContextRequest[]
  onResolve: (requestId: string, suppliedContext: string[], resolution: string) => Promise<void>
  onCancel: (requestId: string) => Promise<void>
  isSaving: boolean
}) {
  const { t } = useLanguage()
  const [selectedRequestId, setSelectedRequestId] = useState<string | null>(null)
  const [suppliedContext, setSuppliedContext] = useState('')
  const [resolution, setResolution] = useState('')
  const [validationError, setValidationError] = useState<string | null>(null)
  const selectedRequest = requests.find((request) => request.request_id === selectedRequestId)
    ?? requests.find((request) => request.status === 'pending')
    ?? requests[0]

  useEffect(() => {
    setSelectedRequestId(selectedRequest?.request_id ?? null)
  }, [requests, selectedRequest?.request_id])

  useEffect(() => {
    if (!selectedRequest) {
      setSuppliedContext('')
      setResolution('')
      setValidationError(null)
      return
    }
    setSuppliedContext(selectedRequest.supplied_context.join('\n'))
    setResolution(selectedRequest.resolution)
    setValidationError(null)
  }, [selectedRequest?.request_id])

  async function resolve() {
    if (!selectedRequest) return
    const contextItems = suppliedContext.split('\n').map((item) => item.trim()).filter(Boolean)
    if (contextItems.length === 0) {
      setValidationError(t('contextRequestContextRequired'))
      return
    }
    if (!resolution.trim()) {
      setValidationError(t('contextRequestResolutionRequired'))
      return
    }
    setValidationError(null)
    await onResolve(selectedRequest.request_id, contextItems, resolution.trim())
  }

  return (
    <section className="context-requests-workspace" aria-label={t('contextRequests')}>
      <aside className="context-request-list-panel panel">
        <div className="panel-heading">
          <div><p className="eyebrow">{t('contextRequests')}</p><h2>{t('contextRequestQueue')}</h2></div>
          <CircleAlert size={20} className="heading-icon" />
        </div>
        <p className="history-intro">{t('contextRequestIntro')}</p>
        <div className="context-request-list">
          {requests.map((request) => (
            <button
              key={request.request_id}
              type="button"
              className={request.request_id === selectedRequest?.request_id ? 'context-request-row selected' : 'context-request-row'}
              onClick={() => setSelectedRequestId(request.request_id)}
            >
              <span className="context-request-row-heading"><strong>{request.artifact_id ? `${t('artifact')} ${request.artifact_id}` : t(`contextRequestScope_${request.scope}`)}</strong><em className={request.status}>{contextRequestStatusLabel(request.status, t)}</em></span>
              <span>{request.request_id}</span>
              <small>{request.requested_items.length} {t('contextRequestItems')}</small>
            </button>
          ))}
          {requests.length === 0 && <p className="empty-copy">{t('noContextRequests')}</p>}
        </div>
      </aside>

      <section className="context-request-detail panel">
        {!selectedRequest && <div className="empty-workspace"><p>{t('selectContextRequest')}</p></div>}
        {selectedRequest && (
          <>
            <div className="panel-heading">
              <div><p className="eyebrow">{t('contextRequestDetail')} · {selectedRequest.request_id}</p><h2>{selectedRequest.artifact_id ? `${t('artifact')} ${selectedRequest.artifact_id}` : t(`contextRequestScope_${selectedRequest.scope}`)}</h2></div>
              <span className={`context-request-status ${selectedRequest.status}`}>{contextRequestStatusLabel(selectedRequest.status, t)}</span>
            </div>
            <dl className="context-request-facts">
              <div><dt>{t('contextRequestScope')}</dt><dd>{t(`contextRequestScope_${selectedRequest.scope}`)}</dd></div>
              <div><dt>{t('createdAtCodebook')}</dt><dd>v{selectedRequest.created_at_codebook_version}</dd></div>
              <div><dt>{t('contextRequestArtifact')}</dt><dd>{selectedRequest.artifact_id ?? t('notApplicable')}</dd></div>
            </dl>
            <section className="context-request-section">
              <p className="section-label">{t('contextRequestReason')}</p>
              <p>{selectedRequest.reason}</p>
            </section>
            <section className="context-request-section">
              <p className="section-label">{t('contextRequestRequestedItems')}</p>
              <ul className="text-list">{selectedRequest.requested_items.map((item) => <li key={item}>{item}</li>)}</ul>
            </section>
            <section className="context-request-form">
              <label><span>{t('contextRequestSuppliedContext')}</span><textarea value={suppliedContext} onChange={(event) => setSuppliedContext(event.target.value)} rows={6} disabled={selectedRequest.status !== 'pending'} placeholder={t('contextRequestSuppliedContextPlaceholder')} /></label>
              <label><span>{t('contextRequestResolution')}</span><textarea value={resolution} onChange={(event) => setResolution(event.target.value)} rows={4} disabled={selectedRequest.status !== 'pending'} placeholder={t('contextRequestResolutionPlaceholder')} /></label>
              {selectedRequest.status === 'pending' && <>
                {validationError && <p className="form-error"><CircleAlert size={15} /> {validationError}</p>}
                <div className="context-request-actions">
                  <button type="button" className="command-button primary" onClick={() => void resolve()} disabled={isSaving}><Check size={15} /> {t('resolveContextRequest')}</button>
                  <button type="button" className="secondary-action" onClick={() => void onCancel(selectedRequest.request_id)} disabled={isSaving}><X size={15} /> {t('cancelContextRequest')}</button>
                </div>
              </>}
            </section>
            {selectedRequest.status !== 'pending' && <p className="context-request-closed">{t('contextRequestClosed')}</p>}
          </>
        )}
      </section>
    </section>
  )
}

function RetrospectiveWorkspaceView({
  tasks,
  selectedTaskId,
  packet,
  codebook,
  submitted,
  isPreparing,
  isSubmitting,
  agentAnalysisRevealed,
  onSelectTask,
  onPrepare,
  onSubmit,
  onNext,
  onRevealAgentAnalysis,
  onTimerEvent,
}: {
  tasks: RetrospectiveTask[]
  selectedTaskId: string | null
  packet: RetrospectiveReviewPacket | null
  codebook: Codebook | null
  submitted: boolean
  isPreparing: boolean
  isSubmitting: boolean
  agentAnalysisRevealed: boolean
  onSelectTask: (taskId: string) => void
  onPrepare: () => Promise<void>
  onSubmit: (review: ReviewSubmission) => Promise<void>
  onNext: () => Promise<void>
  onRevealAgentAnalysis: () => void
  onTimerEvent: (action: 'pause' | 'resume') => Promise<void>
}) {
  const { language, t } = useLanguage()
  const selectedTask = tasks.find((task) => task.task_id === selectedTaskId) ?? null
  const artifact = packet?.review_input.artifact ?? null
  const evidencePacket = packet?.review_input.evidence_packet ?? null

  return (
    <section className="retrospective-workspace" aria-label={t('retrospectiveRecoding')}>
      <aside className="retrospective-task-panel panel">
        <div className="panel-heading">
          <div><p className="eyebrow">{t('retrospectiveRecoding')}</p><h2>{t('retrospectiveTasks')}</h2></div>
          <GitBranch size={20} className="heading-icon" />
        </div>
        <p className="history-intro">{t('retrospectiveIntro')}</p>
        <div className="retrospective-task-list">
          {tasks.map((task) => (
            <button
              key={task.task_id}
              type="button"
              className={task.task_id === selectedTaskId ? 'retrospective-task selected' : 'retrospective-task'}
              onClick={() => onSelectTask(task.task_id)}
              disabled={Boolean(packet && !submitted)}
              title={packet && !submitted ? t('finishCurrentRetrospectiveFirst') : undefined}
            >
              <span className="retrospective-task-heading"><strong>{t('artifact')} {task.artifact_id}</strong><em>{retrospectiveStatusLabel(task.status, t)}</em></span>
              <span>{task.trigger_change_id}</span>
              <small>v{task.from_codebook_version} → v{task.target_codebook_version}</small>
            </button>
          ))}
          {tasks.length === 0 && <p className="empty-copy">{t('noRetrospectiveTasks')}</p>}
        </div>
      </aside>

      <section className="retrospective-artifact-panel panel">
        {!selectedTask && <div className="empty-workspace"><p>{t('selectRetrospectiveTask')}</p></div>}
        {selectedTask && (
          <>
            <div className="panel-heading">
              <div><p className="eyebrow">{t('retrospectiveArtifact')} · {selectedTask.task_id}</p><h2>{t('artifact')} {selectedTask.artifact_id}</h2></div>
              <span className={`retrospective-status ${selectedTask.status}`}>{retrospectiveStatusLabel(selectedTask.status, t)}</span>
            </div>
            <dl className="retrospective-facts">
              <div><dt>{t('triggerChange')}</dt><dd>{selectedTask.trigger_change_id}</dd></div>
              <div><dt>{t('sourceVersion')}</dt><dd>v{selectedTask.from_codebook_version}</dd></div>
              <div><dt>{t('targetVersion')}</dt><dd>v{selectedTask.target_codebook_version}</dd></div>
            </dl>
            <section className="retrospective-reason"><p className="section-label">{t('taskReason')}</p><p>{selectedTask.reason}</p></section>
            {!packet && selectedTask.status !== 'completed' && (
              <button type="button" className="command-button primary" onClick={() => void onPrepare()} disabled={isPreparing}>
                {isPreparing ? <LoaderCircle size={16} className="spin" /> : <Sparkles size={16} />}
                {isPreparing ? t('preparingRetrospective') : t('prepareRetrospective')}
              </button>
            )}
            {artifact && (
              <section className="retrospective-document">
                <div className="document-meta"><span><Database size={14} /> {t('originalArtifact')}</span><span>{Object.keys(artifact.raw_fields).length} {t('sourceFields')}</span></div>
                <pre>{artifact.content}</pre>
              </section>
            )}
            {evidencePacket && agentAnalysisRevealed && (
              <section className="retrospective-evidence">
                <p className="section-label">{t('evidencePacket')}</p>
                <p className="context-brief">{localized(evidencePacket.context_packet.context_brief, evidencePacket.context_packet.context_brief_zh, language)}</p>
                <EvidenceList items={evidencePacket.context_packet.evidence_items} />
                <p className="section-label retrospective-evidence-label">{t('coders')}</p>
                {evidencePacket.coder_outputs.map((coder) => <div className="retrospective-coder" key={coder.coder_id}><strong>{translatedOrHumanized(`coderRole_${coder.coder_id}`, coder.coder_id, t)}</strong><ConfidenceSummary level={coder.confidence_level} rationale={coder.confidence_rationale} rationaleZh={coder.confidence_rationale_zh} factors={coder.confidence_factors} /><ProposedCodes codes={coder.provisional_codes} /></div>)}
              </section>
            )}
            {packet && !agentAnalysisRevealed && !submitted && <p className="retrospective-hint">{t('retrospectiveReviewHint')}</p>}
          </>
        )}
      </section>

      <ReviewPanel
        key={`${packet?.task.task_id ?? selectedTaskId ?? 'no-retrospective-task'}-${submitted ? 'submitted' : 'open'}`}
        packet={packet}
        codebook={codebook}
        submitted={submitted}
        isSubmitting={isSubmitting}
        isAdvancing={false}
        agentAnalysisRevealed={agentAnalysisRevealed}
        isRetrospective
        onSubmit={onSubmit}
        onNext={onNext}
        onRevealAgentAnalysis={onRevealAgentAnalysis}
        onTimerEvent={onTimerEvent}
      />
    </section>
  )
}

function StageReviewView({
  packet,
  runId,
  reviewSetting,
  settingLocked,
  isChangingSetting,
  onSettingChange,
  onAutomaticContinue,
  isSubmitting,
  onSubmit,
  onOpenRetrospective,
  onOpenContextRequests,
  onTimerEvent,
}: {
  packet: StageReviewPacket
  runId: string
  reviewSetting: ReviewMode
  settingLocked: boolean
  isChangingSetting: boolean
  onSettingChange: (setting: ReviewMode) => void
  onAutomaticContinue: () => void
  isSubmitting: boolean
  onSubmit: (review: StageReviewRequest) => Promise<void>
  onOpenRetrospective: () => void
  onOpenContextRequests: () => void
  onTimerEvent: (action: 'pause' | 'resume') => Promise<void>
}) {
  const { language, t } = useLanguage()
  const [decision, setDecision] = useState<StageReviewRequest['decision'] | null>(null)
  const [rationale, setRationale] = useState('')
  const [codes, setCodes] = useState<CodeInput[]>([])
  const [stageOperations, setStageOperations] = useState<CodebookChangeInput[]>([])
  const [validationError, setValidationError] = useState<string | null>(null)
  const startedAt = useRef(Date.now())
  const activeSeconds = useRef(0)
  const timerPacketRef = useRef<object | null>(null)
  const [timerPaused, setTimerPaused] = useState(false)
  const readOnly = packet.inspection_only === true
  const isInitial = packet.kind === 'initial'
  const isAutomatic = isInitial && reviewSetting === 'automatic'
  const codebookEditingAllowed = packet.codebook_editing_allowed !== false && !isAutomatic && !readOnly
  const pendingContextRequest = packet.context_requests.some((request) => request.status === 'pending')

  useEffect(() => {
    setDecision(null)
    setRationale('')
    setValidationError(null)
    setCodes(packet.codebook.codes.map((code) => ({ ...code })))
    setStageOperations([])
    startedAt.current = Date.now()
    activeSeconds.current = 0
    setTimerPaused(isAutomatic)
    if (timerPacketRef.current !== packet) {
      timerPacketRef.current = packet
      if (!isAutomatic && !readOnly) void onTimerEvent('resume').catch(() => setValidationError(t('reviewTimerUpdateFailed')))
    }
  }, [runId, packet.kind, packet.codebook.version, readOnly])

  const previousAutomatic = useRef(isAutomatic)
  useEffect(() => {
    if (previousAutomatic.current === isAutomatic) return
    previousAutomatic.current = isAutomatic
    if (isAutomatic) {
      if (!timerPaused) activeSeconds.current += (Date.now() - startedAt.current) / 1000
      setTimerPaused(true)
    } else {
      startedAt.current = Date.now()
      setTimerPaused(false)
    }
  }, [isAutomatic])

  async function toggleTimer() {
    const now = Date.now()
    if (timerPaused) {
      startedAt.current = now
      setTimerPaused(false)
      try {
        await onTimerEvent('resume')
      } catch {
        setTimerPaused(true)
        setValidationError(t('reviewTimerUpdateFailed'))
      }
    } else {
      const addedSeconds = (now - startedAt.current) / 1000
      activeSeconds.current += addedSeconds
      setTimerPaused(true)
      try {
        await onTimerEvent('pause')
      } catch {
        activeSeconds.current -= addedSeconds
        setTimerPaused(false)
        setValidationError(t('reviewTimerUpdateFailed'))
      }
    }
  }

  function activeDurationSeconds() {
    return Math.max(1, Math.round(activeSeconds.current + (timerPaused ? 0 : (Date.now() - startedAt.current) / 1000)))
  }

  async function closeTimerForSubmit(): Promise<number | null> {
    const duration = activeDurationSeconds()
    if (timerPaused) return duration
    const addedSeconds = (Date.now() - startedAt.current) / 1000
    try {
      await onTimerEvent('pause')
    } catch {
      setValidationError(t('reviewTimerUpdateFailed'))
      return null
    }
    activeSeconds.current += addedSeconds
    setTimerPaused(true)
    return duration
  }

  function updateCode(codeId: string, field: 'name' | 'definition' | 'inclusion_criteria' | 'exclusion_criteria' | 'status' | 'parent_code_id', value: string) {
    if (!codebookEditingAllowed) return
    setDecision('revise')
    setCodes((currentCodes) => currentCodes.map((code) => {
      if (code.code_id !== codeId) return code
      if (field === 'inclusion_criteria' || field === 'exclusion_criteria') {
        const items = value.split('\n').map((item) => item.trim()).filter(Boolean)
        if (language === 'zh') {
          const metadata = { ...(code.metadata ?? {}), [`${field}_zh`]: items }
          return { ...code, metadata }
        }
        return { ...code, [field]: items }
      }
      if (field === 'parent_code_id') return { ...code, parent_code_id: value || null }
      if (field === 'name' || field === 'definition') {
        if (language === 'zh') {
          const metadata = { ...(code.metadata ?? {}), [`${field}_zh`]: value }
          // A manually created code still needs the canonical field for API validation.
          return { ...code, [field]: code[field].trim() ? code[field] : value, metadata }
        }
        return { ...code, [field]: value }
      }
      if (field === 'status') return { ...code, status: value as CodeInput['status'] }
      return code
    }))
  }

  function addStageOperation() {
    if (!codebookEditingAllowed) return
    setDecision('revise')
    setStageOperations((items) => [...items, {
      action: 'merge',
      summary: '',
      rationale: '',
      target_code_ids: [],
      resulting_code_ids: [],
      artifact_ids: [],
    }])
  }

  function stageOperationsWithSimpleEdits(): CodebookChangeInput[] {
    const originalById = new Map(packet.codebook.codes.map((code) => [code.code_id, code]))
    const covered = new Set(stageOperations.flatMap((operation) => [...operation.target_code_ids, ...operation.resulting_code_ids]))
    const derived: CodebookChangeInput[] = []
    for (const code of codes) {
      if (covered.has(code.code_id)) continue
      const original = originalById.get(code.code_id)
      if (!original) {
        derived.push({ action: 'add', summary: `Add ${code.name}.`, rationale: rationale.trim(), target_code_ids: [], resulting_code_ids: [code.code_id], artifact_ids: [] })
        continue
      }
      if (JSON.stringify(original) === JSON.stringify(code)) continue
      const renameOnly = JSON.stringify({ ...original, name: code.name }) === JSON.stringify(code)
      const retiring = original.status !== 'retired' && code.status === 'retired'
      derived.push({
        action: retiring ? 'retire' : renameOnly ? 'rename' : 'refine',
        summary: retiring ? `Retire ${original.name}.` : `${renameOnly ? 'Rename' : 'Refine'} ${original.name}.`,
        rationale: rationale.trim(),
        target_code_ids: [code.code_id],
        resulting_code_ids: [code.code_id],
        artifact_ids: [],
      })
    }
    return [...stageOperations, ...derived]
  }

  function addCode() {
    if (!codebookEditingAllowed) return
    setDecision('revise')
    setCodes((currentCodes) => {
      const usedIds = new Set(currentCodes.map((code) => code.code_id))
      let suffix = 1
      while (usedIds.has(`review-code-${suffix}`)) suffix += 1
      return [...currentCodes, {
        code_id: `review-code-${suffix}`,
        name: '',
        definition: '',
        inclusion_criteria: [],
        exclusion_criteria: [],
        boundary_artifact_ids: [],
        counterexample_status: 'not_assessed',
        hypothetical_examples: [],
        parent_code_id: null,
        status: 'active',
        notes: [],
        metadata: {
          origin: `${packet.kind}_human_review`,
          name_zh: '',
          definition_zh: '',
          inclusion_criteria_zh: [],
          exclusion_criteria_zh: [],
        },
      }]
    })
  }

  async function submitStageReview() {
    if (!decision) {
      setValidationError(t('stageReviewDecisionRequired'))
      return
    }
    if (!codebookEditingAllowed && decision === 'revise') {
      setValidationError(t('codebookFrozenStageReview'))
      return
    }
    if (!isInitial && ['accept', 'mark_unresolved'].includes(decision) && (packet.completion_issues?.length ?? 0) > 0) {
      setValidationError(packet.completion_issues!.join(' '))
      return
    }
    if (!isInitial && decision === 'accept' && packet.pending_retrospective_tasks.length > 0) {
      setValidationError(t('completePropagationBeforeAccept'))
      return
    }
    if (!rationale.trim()) {
      setValidationError(t('stageReviewRationaleRequired'))
      return
    }
    const codebookEdited = JSON.stringify(codes) !== JSON.stringify(packet.codebook.codes)
    if (decision !== 'revise' && (codebookEdited || stageOperations.length > 0)) {
      setValidationError(t('stageEditsRequireRevision'))
      return
    }
    if (decision === 'revise') {
      if (codes.length === 0 || codes.some((code) => !code.code_id.trim() || !code.name.trim() || !code.definition.trim())) {
        setValidationError(t('stageReviewCodeFieldsRequired'))
        return
      }
      if (new Set(codes.map((code) => code.code_id.trim())).size !== codes.length) {
        setValidationError(t('validationUniqueIds'))
        return
      }
      if (stageOperations.some((operation) => !operation.summary.trim() || !operation.rationale.trim())) {
        setValidationError(t('stageOperationFieldsRequired'))
        return
      }
    }
    setValidationError(null)
    const duration = await closeTimerForSubmit()
    if (duration === null) return
    await onSubmit({
      decision,
      rationale: rationale.trim(),
      revised_codes: decision === 'revise' ? codes : [],
      change_operations: decision === 'revise' ? stageOperationsWithSimpleEdits() : [],
      duration_seconds: duration,
    })
  }

  const auditWarnings = localizedList(
    packet.audit?.warnings ?? packet.bootstrap?.audit_warnings ?? [],
    packet.audit?.warnings_zh ?? packet.bootstrap?.audit_warnings_zh ?? [],
    language,
  )
  const sampledArtifacts = new Map((packet.sampled_artifacts ?? []).map((artifact) => [artifact.artifact_id, artifact]))
  const assignments = new Map((packet.assignments ?? []).map((assignment) => [assignment.artifact_id, assignment]))
  const crossSourceRecords = new Map((packet.cross_source_audit_records ?? []).map((record) => [record.artifact_id, record]))
  const question = textValue(packet.research_question.question_text, t('notRecorded'))
  const scope = textValue(packet.research_question.analysis_scope, t('notRecorded'))
  const stageDecisions: Array<{ value: StageReviewRequest['decision']; label: string }> = [
    { value: 'accept', label: t('accept') },
    ...(codebookEditingAllowed ? [{ value: 'revise' as const, label: t('revise') }] : []),
    ...(codebookEditingAllowed || isInitial ? [{ value: 'reject' as const, label: t('reject') }] : []),
    { value: 'request_additional_context', label: t('requestAdditionalContext') },
    { value: 'mark_unresolved', label: t('markUnresolved') },
  ]
  const auditSummaryLabels: Record<string, string> = {
    all_sampled_artifact_count: t('allSampledArtifactCount'), sampled_artifact_count: t('sampledArtifactCount'), assignment_count: t('initialAssignmentCount'), all_assignment_count: t('allAssignmentCount'),
    initial_coding_count: t('initialCodingCount'), code_count: t('codeCount'),
    representative_evidence_required: t('representativeEvidenceRequired'),
    input_artifacts: t('auditInputArtifacts'), processed_artifacts: t('auditProcessedArtifacts'), unprocessed_artifact_count: t('unprocessedArtifactCount'),
    coding_record_count: t('codingRecordCount'), stage_review_count: t('stageReviewCount'),
    pending_retrospective_count: t('pendingRetrospectiveCount'), open_unresolved_count: t('openUnresolvedCount'),
    cross_source_audit_status: t('crossSourceAuditStatus'), cross_source_audit_artifact_count: t('crossSourceAuditArtifactCount'),
    final_review_artifact_count: t('finalReviewArtifactCount'), final_review_flagged_count: t('finalReviewFlaggedCount'),
    final_review_unflagged_audit_count: t('finalReviewUnflaggedAuditCount'), low_frequency_code_count: t('lowFrequencyCodeCount'),
    retrospective_recoding_suppressed_count: t('retrospectiveRecodingSuppressedCount'),
  }
  const auditSummaryValue = (key: string, value: string | number | boolean) => {
    if (typeof value === 'boolean') return value ? t('yes') : t('no')
    if (key !== 'cross_source_audit_status') return String(value)
    const statusLabels: Record<string, string> = {
      automatic_validation_coverage: language === 'zh' ? '自动验证覆盖' : 'Automatic validation coverage',
      human_review_completed: language === 'zh' ? '已完成人工审核' : 'Human review completed',
      presented_for_final_review: language === 'zh' ? '已提交最终审核' : 'Presented for final review',
      not_applicable_single_source: language === 'zh' ? '不适用（单一来源）' : 'Not applicable (single source)',
      not_run: language === 'zh' ? '尚未运行' : 'Not run',
    }
    return statusLabels[String(value)] ?? String(value).replace(/_/g, ' ')
  }

  const codebookEditor = (
      <section className="stage-codebook-editor">
        <div className="section-action-heading"><div><p className="section-label">{t('stageCodebookReview')}</p><h3>{t('stageCodebookGuidance')}</h3></div><button type="button" className="secondary-action compact" onClick={addCode} disabled={!codebookEditingAllowed}><Sparkles size={14} /> {t('addManualCode')}</button></div>
        <div className="stage-code-list">
          {codes.map((code) => (
            <article key={code.code_id} className="stage-code-editor">
              <header><span>{code.code_id}</span>{!readOnly && code.status !== 'retired' && <button type="button" className="icon-button subtle" onClick={() => updateCode(code.code_id, 'status', 'retired')} disabled={!codebookEditingAllowed} title={t('retireCode')}><Trash2 size={14} /></button>}</header>
              <label><span>{t('name')}</span><input value={codeLocalized(code, 'name', language, '')} onChange={(event) => updateCode(code.code_id, 'name', event.target.value)} disabled={!codebookEditingAllowed} /></label>
              <label><span>{t('definition')}</span><textarea value={codeLocalized(code, 'definition', language, '')} onChange={(event) => updateCode(code.code_id, 'definition', event.target.value)} rows={3} disabled={!codebookEditingAllowed} /></label>
              <div className="stage-criteria-grid">
                <label><span>{t('inclusionCriteria')}</span><textarea value={codeLocalizedList(code, 'inclusion_criteria', language).join('\n')} onChange={(event) => updateCode(code.code_id, 'inclusion_criteria', event.target.value)} rows={3} disabled={!codebookEditingAllowed} /></label>
                <label><span>{t('exclusionCriteria')}</span><textarea value={codeLocalizedList(code, 'exclusion_criteria', language).join('\n')} onChange={(event) => updateCode(code.code_id, 'exclusion_criteria', event.target.value)} rows={3} disabled={!codebookEditingAllowed} /></label>
              </div>
              <div className="stage-criteria-grid">
                <div className="code-status-readonly"><span>{t('codeStatus')}</span><strong>{codeStatusLabel(code.status, t)}</strong></div>
                <label><span>{t('parentCode')}</span><select value={code.parent_code_id ?? ''} onChange={(event) => updateCode(code.code_id, 'parent_code_id', event.target.value)} disabled={!codebookEditingAllowed}><option value="">{t('none')}</option>{codes.filter((candidate) => candidate.code_id !== code.code_id && candidate.status === 'active').map((candidate) => <option key={candidate.code_id} value={candidate.code_id}>{codeLocalized(candidate, 'name', language, '') || candidate.code_id}</option>)}</select></label>
              </div>
            </article>
          ))}
        </div>
      </section>
  )

  return (
    <section className="stage-review-workspace" aria-label={t(isInitial ? 'initialReview' : 'finalReview')}>
      <header className="stage-review-header">
        <div><p className="eyebrow">{t('humanReview')}</p><h2>{t(isInitial ? 'initialReview' : 'finalReview')}</h2></div>
        <div className="heading-actions">{!isAutomatic && !readOnly && <button type="button" className="icon-button subtle" onClick={() => void toggleTimer()} title={t(timerPaused ? 'resumeReviewTimer' : 'pauseReviewTimer')}>{timerPaused ? <Play size={16} /> : <Pause size={16} />}</button>}<span className="version-chip">v{packet.codebook.version}</span></div>
      </header>

      {isInitial && <ReviewSettingSelector value={reviewSetting} onChange={onSettingChange} locked={settingLocked} futureOnly={readOnly} busy={isChangingSetting || isSubmitting} onContinue={onAutomaticContinue} />}

      <section className="stage-review-position" aria-label={t('reviewWorkflowPosition')}>
        <ol>
          {(isInitial
            ? ['workflowInitialization', 'workflowValidation', 'initialReview', 'reviewNextIteration']
            : ['reviewCodingReassessment', 'reviewFinalValidation', 'finalReview', 'reviewFinalizeAnalysis']
          ).map((label, index) => (
            <li key={label} aria-current={index === 2 ? 'step' : undefined}>
              {index > 0 && <ChevronRight size={14} aria-hidden="true" />}
              <span>{index === 2 && <BookOpenCheck size={14} aria-hidden="true" />}{t(label)}</span>
            </li>
          ))}
        </ol>
        <p>{t(pendingContextRequest || (!isInitial && packet.pending_retrospective_tasks.length > 0)
          ? 'reviewPositionPending'
          : readOnly ? 'reviewPositionInspectionHint' : isAutomatic ? 'reviewPositionAutomaticHint' : isInitial ? 'reviewPositionInitialHint' : 'reviewPositionFinalHint')}</p>
      </section>

      {readOnly && <div className="stage-review-inspection-note"><strong>{t('reviewInspectionTitle')}</strong><p>{packet.review_record ? `${t('stageReviewDecision')}: ${t(packet.review_record.decision === 'request_additional_context' ? 'requestAdditionalContext' : packet.review_record.decision === 'mark_unresolved' ? 'markUnresolved' : packet.review_record.decision)} · ${packet.review_record.rationale}` : t('reviewInspectionNoHumanDecision')}</p></div>}

      {isInitial && codebookEditor}

      <section className="stage-review-context">
        <div><p className="section-label">{t('researchQuestion')}</p><strong>{question}</strong><p>{scope}</p></div>
        <dl>
          <div><dt>{t('artifactUnit')}</dt><dd>{textValue(packet.analysis_protocol.artifact_unit)}</dd></div>
          <div><dt>{t('evidenceUnit')}</dt><dd>{textValue(packet.analysis_protocol.evidence_unit)}</dd></div>
          <div><dt>{t('multipleCoding')}</dt><dd>{packet.analysis_protocol.allow_multiple_codes === false ? t('notAllowed') : t('allowed')}</dd></div>
        </dl>
      </section>

      {packet.review_scope && (
        <section className="stage-review-audit stage-review-scope">
          <div>
            <p className="section-label">{t('reviewScope')}</p>
            <strong>{packet.review_scope.checkpoint === 'initial' ? t('initialReview') : t('finalReview')}</strong>
            <p>{packet.review_scope.purpose}</p>
          </div>
          <div>
            <p className="section-label">{t('requiredChecks')}</p>
            <ul className="text-list">{packet.review_scope.required_checks.map((check) => <li key={check}>{check}</li>)}</ul>
          </div>
        </section>
      )}

      {!readOnly && packet.codebook_editing_allowed === false && (
        <div className="propagation-warning">
          <div>
            <strong>{t('codebookFrozenStageReview')}</strong>
            <p>{t('codebookFrozenStageReviewGuidance')}</p>
          </div>
        </div>
      )}

      {packet.audit_summary && (
        <section className="stage-review-audit">
          <p className="section-label">{t('auditSummary')}</p>
          <dl className="stage-audit-summary">
            {Object.entries(packet.audit_summary).map(([key, value]) => (
              <div key={key}><dt>{auditSummaryLabels[key] ?? key}</dt><dd>{auditSummaryValue(key, value)}</dd></div>
            ))}
          </dl>
        </section>
      )}

      {packet.context_requests.length > 0 && (
        <section className="stage-review-audit">
          <p className="section-label">{t('stageContextRequests')}</p>
          <p className="form-guidance">{t('stageContextRequestsGuidance')}</p>
          <div className="initial-case-list">
            {packet.context_requests.map((request) => (
              <article className="initial-case" key={request.request_id}>
                <header className="context-request-row-heading">
                  <strong>{request.request_id}</strong>
                  <em className={request.status}>{contextRequestStatusLabel(request.status, t)}</em>
                </header>
                <p><strong>{t('contextRequestReason')}:</strong> {request.reason}</p>
                <p><strong>{t('contextRequestRequestedItems')}:</strong> {request.requested_items.join('; ')}</p>
                {request.supplied_context.length > 0 && (
                  <div>
                    <strong>{t('contextRequestSuppliedContext')}:</strong>
                    <ul className="text-list">{request.supplied_context.map((item) => <li key={item}>{item}</li>)}</ul>
                  </div>
                )}
                {request.resolution && <p><strong>{t('contextRequestResolution')}:</strong> {request.resolution}</p>}
              </article>
            ))}
          </div>
          {pendingContextRequest && <div className="propagation-warning"><div><strong>{t('stageContextPending')}</strong></div><button type="button" className="secondary-action" disabled={readOnly} onClick={onOpenContextRequests}><CircleAlert size={15} /> {t('openContextRequests')}</button></div>}
        </section>
      )}

      {isInitial ? (
        <section className="stage-review-audit">
          <div className="stage-facts bootstrap-stage-facts">
            <div><span>{t('bootstrapCodeCount')}</span><strong>{packet.codebook.codes.length}</strong></div>
            <div><span>{t('bootstrapAssignmentArtifactCount')}</span><strong>{packet.assignments?.length ?? 0}</strong></div>
          </div>
          <p className="section-label">{t('bootstrapAuditWarnings')}</p>
          {auditWarnings.length > 0 ? <ul className="text-list">{auditWarnings.map((warning) => <li key={warning}>{warning}</li>)}</ul> : <p className="empty-copy">{t('noBootstrapWarnings')}</p>}
          <details className="initial-review-materials">
            <summary>{t('inspectBootstrapEvidence')}</summary>
            <p className="form-guidance">{t('inspectBootstrapEvidenceGuidance')}</p>
            <div className="initial-case-list">
              {(packet.initial_codings ?? []).map((coding) => {
                const artifact = sampledArtifacts.get(coding.artifact_id)
                const assignment = assignments.get(coding.artifact_id)
                return (
                  <details className="initial-case" key={coding.artifact_id}>
                    <summary>{t('artifact')} {coding.artifact_id}</summary>
                    {artifact && <details className="source-artifact"><summary>{t('originalArtifact')}</summary><pre>{artifact.content}</pre></details>}
                    <div className="initial-context"><strong>{t('context')}</strong><p>{localized(coding.context_packet.context_brief, coding.context_packet.context_brief_zh, language)}</p><EvidenceList items={coding.context_packet.evidence_items} /></div>
                    <div className="initial-coder-grid">
                      {coding.coder_outputs.map((coder) => (
                        <article key={coder.coder_id}>
                          <strong>{translatedOrHumanized(`coderRole_${coder.coder_id}`, coder.coder_id, t)}</strong>
                          <ProposedCodes codes={coder.provisional_codes} />
                        </article>
                      ))}
                    </div>
                    {assignment && <div className="initial-assignment"><strong>{t('bootstrapAssignments')}</strong><p>{assignment.code_ids.join(', ')}</p><ul className="text-list">{assignment.evidence_summary.map((item) => <li key={item}>{item}</li>)}</ul></div>}
                  </details>
                )
              })}
              {(packet.initial_codings?.length ?? 0) === 0 && <p className="empty-copy">{t('noInitialCoderOutputs')}</p>}
            </div>
          </details>
        </section>
      ) : (
        <section className="stage-review-audit">
          <div className="stage-facts">
            <div><span>{t('processed')}</span><strong>{packet.coverage?.processed_artifacts ?? 0} / {packet.coverage?.input_artifacts ?? 0}</strong></div>
            <div><span>{t('bootstrapCoverage')}</span><strong>{packet.coverage?.bootstrap_artifacts ?? 0}</strong></div>
            <div><span>{t('iterativeCoverage')}</span><strong>{packet.coverage?.iterative_artifacts ?? 0}</strong></div>
            <div><span>{t('entries')}</span><strong>{packet.coverage?.code_count ?? packet.codebook.codes.length}</strong></div>
            <div><span>{t('unresolvedCases')}</span><strong>{packet.unresolved_cases.length}</strong></div>
            <div><span>{t('pendingPropagation')}</span><strong>{packet.pending_retrospective_tasks.length}</strong></div>
          </div>
          {packet.stabilization && <div className={`stability-result ${packet.stabilization.stable ? 'stable' : 'unstable'}`}><strong>{packet.stabilization.stable ? t('codingStable') : t('codingNotStable')}</strong><ul>{packet.stabilization.reasons.map((reason) => <li key={reason}>{stabilityReasonLabel(reason, t)}</li>)}</ul></div>}
          {(packet.final_validation_audits ?? []).map((audit) => (
            <details key={audit.audit_id} open={audit.codebook_version === packet.codebook.version}>
              <summary>{t('finalValidationAudit')} · v{audit.codebook_version}</summary>
              <p>{t('finalValidationAuditGuidance')}</p>
              {audit.validation_outputs.map((output) => (
                <article key={output.artifact_id} className="initial-case">
                  <strong>{t('artifact')} {output.artifact_id}</strong>
                  <p>{localized(output.summary, output.summary_zh, language)}</p>
                  <ul className="text-list">{output.signals.map((signal, index) => (
                    <li key={index}>{localized(signal.summary, signal.summary_zh, language)}</li>
                  ))}</ul>
                </article>
              ))}
            </details>
          ))}
          {(packet.final_audit_artifacts?.length ?? 0) > 0 && (
            <details>
              <summary>{t('finalAuditCases')}</summary>
              {packet.final_audit_artifacts?.map((artifact) => {
                const matches = packet.final_audit_records?.filter((item) => item.artifact_id === artifact.artifact_id) ?? []
                const record = matches[matches.length - 1]
                return <details className="initial-case" key={artifact.artifact_id}>
                  <summary>{t('artifact')} {artifact.artifact_id}</summary>
                  <pre>{artifact.content}</pre>
                  <p><strong>{t('finalCodes')}:</strong> {record?.final_code_names.join(', ') || t('none')}</p>
                  <p><strong>{t('decisionRationale')}:</strong> {record?.rationale || t('notRecorded')}</p>
                </details>
              })}
            </details>
          )}
          {packet.pending_retrospective_tasks.length > 0 && <div className="propagation-warning"><div><strong>{t('propagationRequired')}</strong><p>{t('propagationRequiredGuidance')}</p></div><button type="button" className="secondary-action" disabled={readOnly} onClick={onOpenRetrospective}><History size={15} /> {t('openRetrospective')}</button></div>}
          {packet.unresolved_cases.length > 0 && <details><summary>{t('viewUnresolvedCases')}</summary><ul className="text-list">{packet.unresolved_cases.map((item, index) => <li key={`${textValue(item.artifact_id)}-${index}`}><strong>{textValue(item.artifact_id)}</strong>: {textValue(item.reason)}</li>)}</ul></details>}
          {(packet.coverage?.low_frequency_codes.length ?? 0) > 0 && <details><summary>{t('lowFrequencyCodes')}</summary><ul className="text-list">{packet.coverage?.low_frequency_codes.map((code) => <li key={code.code_id}><strong>{codeLocalized(code, 'name', language)}</strong>: {codeLocalized(code, 'definition', language)}</li>)}</ul></details>}
          {(packet.cross_source_audit_artifacts?.length ?? 0) > 0 && (
            <details className="initial-review-materials">
              <summary>{t('crossSourceAudit')}</summary>
              <p className="form-guidance">{t('crossSourceAuditGuidance')}</p>
              <div className="initial-case-list">
                {packet.cross_source_audit_artifacts?.map((artifact) => {
                  const record = crossSourceRecords.get(artifact.artifact_id)
                  return (
                    <details className="initial-case" key={artifact.artifact_id}>
                      <summary>{t('artifact')} {artifact.artifact_id}</summary>
                      <pre>{artifact.content}</pre>
                      <p><strong>{t('finalCodes')}:</strong> {record?.final_code_names.join(', ') || t('none')}</p>
                      <p><strong>{t('decisionRationale')}:</strong> {record?.rationale || t('notRecorded')}</p>
                    </details>
                  )
                })}
              </div>
            </details>
          )}
        </section>
      )}

      {!isInitial && codebookEditor}

      {!readOnly && !isAutomatic && decision === 'revise' && (
        <section className="stage-codebook-editor">
          <div className="section-action-heading"><div><p className="section-label">{t('stageOperations')}</p><h3>{t('stageOperationsGuidance')}</h3></div><button type="button" className="secondary-action compact" onClick={addStageOperation} disabled={!codebookEditingAllowed}><GitBranch size={14} /> {t('addStageOperation')}</button></div>
          <div className="stage-code-list">
            {stageOperations.map((operation, index) => (
              <article className="stage-code-editor" key={`stage-operation-${index}`}>
                <header><span>{t('stageOperation')} {index + 1}</span><button type="button" className="icon-button subtle" onClick={() => setStageOperations((items) => items.filter((_, itemIndex) => itemIndex !== index))} title={t('removeChange')}><Trash2 size={14} /></button></header>
                <label><span>{t('changeType')}</span><select value={operation.action} onChange={(event) => setStageOperations((items) => items.map((item, itemIndex) => itemIndex === index ? { ...item, action: event.target.value as CodebookChangeInput['action'] } : item))}><option value="add">{t('actionAdd')}</option><option value="add_parent">{t('actionAddParent')}</option><option value="refine">{t('actionRefine')}</option><option value="merge">{t('actionMerge')}</option><option value="split">{t('actionSplit')}</option><option value="rename">{t('actionRename')}</option><option value="retire">{t('actionRetire')}</option></select></label>
                <label><span>{t('changeSummary')}</span><input value={operation.summary} onChange={(event) => setStageOperations((items) => items.map((item, itemIndex) => itemIndex === index ? { ...item, summary: event.target.value } : item))} /></label>
                <label><span>{t('affectedCurrentCodes')}</span><input value={operation.target_code_ids.join(', ')} onChange={(event) => setStageOperations((items) => items.map((item, itemIndex) => itemIndex === index ? { ...item, target_code_ids: event.target.value.split(',').map((value) => value.trim()).filter(Boolean) } : item))} placeholder={t('codeIdsCommaSeparated')} /></label>
                <label><span>{t('resultingCodeIds')}</span><input value={operation.resulting_code_ids.join(', ')} onChange={(event) => setStageOperations((items) => items.map((item, itemIndex) => itemIndex === index ? { ...item, resulting_code_ids: event.target.value.split(',').map((value) => value.trim()).filter(Boolean) } : item))} placeholder={t('codeIdsCommaSeparated')} /></label>
                <label><span>{t('reasonForChange')}</span><textarea value={operation.rationale} onChange={(event) => setStageOperations((items) => items.map((item, itemIndex) => itemIndex === index ? { ...item, rationale: event.target.value } : item))} rows={3} /></label>
              </article>
            ))}
            {stageOperations.length === 0 && <p className="empty-copy">{t('simpleStageOperationsAutomatic')}</p>}
          </div>
        </section>
      )}

      {!readOnly && !isAutomatic && <section className="stage-review-decision">
        <p className="section-label">{t('stageReviewDecision')}</p>
        <p>{t(isInitial ? 'initialReviewGuidance' : 'finalReviewGuidance')}</p>
        {!isInitial && (packet.completion_issues?.length ?? 0) > 0 && <div className="form-error"><CircleAlert size={15} /><div>{packet.completion_issues!.map((issue) => <p key={issue}>{issue}</p>)}</div></div>}
        <label><span>{t('stageReviewRationale')}</span><textarea value={rationale} onChange={(event) => setRationale(event.target.value)} rows={4} /></label>
        <div className="stage-decision-grid">{stageDecisions.map((item) => {
          const disabled = pendingContextRequest || (!isInitial && ['accept', 'mark_unresolved'].includes(item.value) && ((packet.completion_issues?.length ?? 0) > 0 || packet.pending_retrospective_tasks.length > 0))
          return <button type="button" disabled={disabled} title={disabled ? (pendingContextRequest ? t('stageContextPending') : t('completePropagationBeforeAccept')) : undefined} className={decision === item.value ? 'selected' : ''} onClick={() => setDecision(item.value)} key={item.value}>{decision === item.value && <Check size={14} />}{item.label}</button>
        })}</div>
        {decision === 'mark_unresolved' && <p className="form-guidance">{t(isInitial ? 'initialMarkUnresolvedGuidance' : 'finalMarkUnresolvedGuidance')}</p>}
        {decision === 'reject' && !isInitial && <p className="form-guidance">{t('finalRejectGuidance')}</p>}
        {validationError && <p className="form-error"><CircleAlert size={15} /> {validationError}</p>}
        <button type="button" className="command-button primary stage-submit" disabled={isSubmitting || pendingContextRequest} onClick={() => void submitStageReview()}>{isSubmitting ? <LoaderCircle size={16} className="spin" /> : <ShieldCheck size={16} />}{isSubmitting ? t('savingReview') : t('submitStageReview')}</button>
      </section>}
    </section>
  )
}

function StageReviewInspector({ run, kind, isChangingSetting, onSettingChange, onOpenRetrospective, onOpenContextRequests }: { run: RunSummary; kind: StageReviewPacket['kind']; isChangingSetting: boolean; onSettingChange: (setting: ReviewMode) => void; onOpenRetrospective: () => void; onOpenContextRequests: () => void }) {
  const { t } = useLanguage()
  const [data, setData] = useState<{ packet: StageReviewPacket | null; error: string | null }>({ packet: null, error: null })
  useEffect(() => {
    let active = true
    setData({ packet: null, error: null })
    void api.getStageReview(run.run_id, kind, true).then(
      (packet) => { if (active) setData({ packet, error: null }) },
      (error) => { if (active) setData({ packet: null, error: error instanceof Error ? error.message : String(error) }) },
    )
    return () => { active = false }
  }, [run.run_id, kind, run.review_setting])
  if (!data.packet) return <section className="stage-review-workspace"><header className="stage-review-header"><h2>{t(kind === 'initial' ? 'initialReview' : 'finalReview')}</h2></header><p className="empty-copy">{data.error ? t(kind === 'initial' ? 'initialReviewNotReady' : 'finalReviewNotReady') : t('loading')}</p>{data.error && <p className="form-guidance">{data.error}</p>}</section>
  return <StageReviewView packet={data.packet} runId={run.run_id} reviewSetting={run.review_setting} settingLocked={Boolean(run.review_setting_locked)} isChangingSetting={isChangingSetting} isSubmitting={false} onSettingChange={onSettingChange} onAutomaticContinue={() => {}} onSubmit={async () => {}} onTimerEvent={async () => {}} onOpenRetrospective={onOpenRetrospective} onOpenContextRequests={onOpenContextRequests} />
}

function SourceDialog({ artifact, onClose }: { artifact: NonNullable<CurrentArtifactResponse['artifact']>; onClose: () => void }) {
  const { t } = useLanguage()
  const dialogRef = useRef<HTMLDialogElement>(null)
  useEffect(() => { const dialog = dialogRef.current; dialog?.showModal(); return () => dialog?.close() }, [])
  return <dialog ref={dialogRef} className="source-dialog" onCancel={onClose} onClick={(event) => { if (event.target === event.currentTarget) onClose() }}>
    <div className="section-action-heading"><div><p className="eyebrow">{t('originalArtifact')}</p><h2>{t('artifact')} {artifact.artifact_id}</h2></div><button type="button" className="icon-button" autoFocus onClick={onClose} aria-label={t('closePanel')}><X size={17} /></button></div>
    <div className="document-view"><pre>{artifact.content}</pre>{artifact.source_refs.length > 0 && <div className="source-row"><span>{t('sources')}</span>{artifact.source_refs.map((source, index) => /^https?:\/\//i.test(source.value) ? <a href={source.value} target="_blank" rel="noreferrer" key={index}>{source.kind}<ChevronRight size={13} /></a> : <span key={index}>{source.kind}: {source.value}</span>)}</div>}</div>
  </dialog>
}

function App() {
  const { language, setLanguage, t } = useLanguage()
  const [datasets, setDatasets] = useState<Dataset[]>([])
  const [runs, setRuns] = useState<RunSummary[]>([])
  const [selectedDataset, setSelectedDataset] = useState('llm_code_error_semantic')
  const [artifactLimit, setArtifactLimit] = useState(2)
  const [iterativeBatchSize, setIterativeBatchSize] = useState(1)
  const [experimentVariant, setExperimentVariant] = useState<ExperimentVariant>('standard')
  const [heldOutEnabled, setHeldOutEnabled] = useState(false)
  const [heldOutSize, setHeldOutSize] = useState(12)
  const [selectedRunId, setSelectedRunId] = useState<string | null>(null)
  const [runPickerOpen, setRunPickerOpen] = useState(false)
  const [runContextMenu, setRunContextMenu] = useState<{ runId: string; x: number; y: number } | null>(null)
  const [deleteRunId, setDeleteRunId] = useState<string | null>(null)
  const [isDeletingRun, setIsDeletingRun] = useState(false)
  const [run, setRun] = useState<RunSummary | null>(null)
  const [current, setCurrent] = useState<CurrentArtifactResponse | null>(null)
  const [packet, setPacket] = useState<ReviewPacket | null>(null)
  const [stageReview, setStageReview] = useState<StageReviewPacket | null>(null)
  const [history, setHistory] = useState<RunHistory | null>(null)
  const [contextRequests, setContextRequests] = useState<ContextRequest[]>([])
  const [retrospectiveTasks, setRetrospectiveTasks] = useState<RetrospectiveTask[]>([])
  const [selectedRetrospectiveTaskId, setSelectedRetrospectiveTaskId] = useState<string | null>(null)
  const [retrospectivePacket, setRetrospectivePacket] = useState<RetrospectiveReviewPacket | null>(null)
  const [retrospectiveSubmittedTaskId, setRetrospectiveSubmittedTaskId] = useState<string | null>(null)
  const [retrospectiveAnalysisRevealed, setRetrospectiveAnalysisRevealed] = useState(false)
  const [runArtifacts, setRunArtifacts] = useState<RunArtifacts | null>(null)
  const [selectedRecordId, setSelectedRecordId] = useState<string | null>(null)
  const [activeNodeId, setActiveNodeId] = useState('input')
  const [newTaskOpen, setNewTaskOpen] = useState(false)
  const [sourceOpen, setSourceOpen] = useState(false)
  const [agentAnalysisRevealed, setAgentAnalysisRevealed] = useState(false)
  const [activeView, setActiveView] = useState<AppView>('workspace')
  const [codeSearch, setCodeSearch] = useState('')
  const deferredCodeSearch = useDeferredValue(codeSearch)
  const [isLoading, setIsLoading] = useState(true)
  const [isCreatingTask, setIsCreatingTask] = useState(false)
  const [isInitializing, setIsInitializing] = useState(false)
  const [isStoppingInitialization, setIsStoppingInitialization] = useState(false)
  const previousWorkflowPosition = useRef<{ runId: string; node: string } | null>(null)
  const [isPreparing, setIsPreparing] = useState(false)
  const [isPreparingRetrospective, setIsPreparingRetrospective] = useState(false)
  const [isAutoProcessing, setIsAutoProcessing] = useState(false)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [isSubmittingStageReview, setIsSubmittingStageReview] = useState(false)
  const [isChangingSetting, setIsChangingSetting] = useState(false)
  const [isSubmittingRetrospective, setIsSubmittingRetrospective] = useState(false)
  const [isSavingContextRequest, setIsSavingContextRequest] = useState(false)
  const [isSavingMemo, setIsSavingMemo] = useState(false)
  const [isAdvancing, setIsAdvancing] = useState(false)
  const [isLoadingArtifacts, setIsLoadingArtifacts] = useState(false)
  const [selectedCodeArtifacts, setSelectedCodeArtifacts] = useState<CodeArtifacts | null>(null)
  const [isLoadingCodeArtifacts, setIsLoadingCodeArtifacts] = useState(false)
  const [isExportingHeldOut, setIsExportingHeldOut] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const workspaceRef = useRef<HTMLElement | null>(null)
  const initializationRequest = useRef<AbortController | null>(null)
  const codeArtifactsRequest = useRef(0)
  const resizeSession = useRef<{
    divider: WorkspaceDivider
    startX: number
    startLeft: number
    startRight: number
  } | null>(null)
  const [workspaceWidths, setWorkspaceWidths] = useState<{ left: number; right: number } | null>(null)
  const [resizingDivider, setResizingDivider] = useState<WorkspaceDivider | null>(null)

  function measureWorkspace() {
    const workspace = workspaceRef.current
    const leftPanel = workspace?.querySelector<HTMLElement>('.codebook-panel, .workflow-sidebar')
    const rightPanel = workspace?.querySelector<HTMLElement>(':scope > .review-panel, :scope > .workflow-inspector')
    const centerPanel = workspace?.querySelector<HTMLElement>('.artifact-panel, .workflow-stage-content')
    if (!workspace || !leftPanel || (!rightPanel && !centerPanel)) return null
    return {
      containerWidth: workspace.clientWidth,
      left: leftPanel.getBoundingClientRect().width,
      right: rightPanel?.getBoundingClientRect().width ?? 0,
    }
  }

  function constrainDividerWidth(
    divider: WorkspaceDivider,
    proposedWidth: number,
    baseWidths: { left: number; right: number },
    containerWidth: number,
  ) {
    const otherWidth = divider === 'left' ? baseWidths.right : baseWidths.left
    const minimum = divider === 'left' ? WORKSPACE_MIN_WIDTHS.left : WORKSPACE_MIN_WIDTHS.right
    const maximum = Math.max(minimum, containerWidth - WORKSPACE_MIN_WIDTHS.center - otherWidth - 16)
    return Math.round(Math.min(maximum, Math.max(minimum, proposedWidth)))
  }

  function applyDividerKeyboardAdjustment(divider: WorkspaceDivider, delta: number) {
    const measured = measureWorkspace()
    if (!measured) return
    const current = workspaceWidths ?? { left: measured.left, right: measured.right }
    const nextWidth = divider === 'left'
      ? constrainDividerWidth(divider, current.left + delta, current, measured.containerWidth)
      : constrainDividerWidth(divider, current.right + delta, current, measured.containerWidth)
    setWorkspaceWidths(divider === 'left'
      ? { left: nextWidth, right: current.right }
      : { left: current.left, right: nextWidth })
  }

  function startWorkspaceResize(event: ReactPointerEvent<HTMLButtonElement>, divider: WorkspaceDivider) {
    if (window.matchMedia('(max-width: 1120px)').matches) return
    const measured = measureWorkspace()
    if (!measured) return
    event.preventDefault()
    resizeSession.current = {
      divider,
      startX: event.clientX,
      startLeft: measured.left,
      startRight: measured.right,
    }
    setWorkspaceWidths({ left: measured.left, right: measured.right })
    setResizingDivider(divider)
  }

  function adjustWorkspaceResize(event: ReactKeyboardEvent<HTMLButtonElement>, divider: WorkspaceDivider) {
    if (window.matchMedia('(max-width: 1120px)').matches) return
    if (event.key !== 'ArrowLeft' && event.key !== 'ArrowRight') return
    event.preventDefault()
    const step = event.shiftKey ? 50 : 16
    const delta = divider === 'left'
      ? (event.key === 'ArrowRight' ? step : -step)
      : (event.key === 'ArrowRight' ? -step : step)
    applyDividerKeyboardAdjustment(divider, delta)
  }

  useEffect(() => {
    if (!resizingDivider) return
    const handlePointerMove = (event: globalThis.PointerEvent) => {
      const session = resizeSession.current
      const measured = measureWorkspace()
      if (!session || !measured) return
      event.preventDefault()
      const delta = event.clientX - session.startX
      const baseWidths = { left: session.startLeft, right: session.startRight }
      const nextWidth = constrainDividerWidth(
        session.divider,
        session.divider === 'left' ? session.startLeft + delta : session.startRight - delta,
        baseWidths,
        measured.containerWidth,
      )
      setWorkspaceWidths(session.divider === 'left'
        ? { left: nextWidth, right: session.startRight }
        : { left: session.startLeft, right: nextWidth })
    }
    const stopResize = () => {
      resizeSession.current = null
      setResizingDivider(null)
    }
    document.body.classList.add('workspace-resizing')
    window.addEventListener('pointermove', handlePointerMove, { passive: false })
    window.addEventListener('pointerup', stopResize)
    window.addEventListener('pointercancel', stopResize)
    return () => {
      document.body.classList.remove('workspace-resizing')
      window.removeEventListener('pointermove', handlePointerMove)
      window.removeEventListener('pointerup', stopResize)
      window.removeEventListener('pointercancel', stopResize)
    }
  }, [resizingDivider])

  async function loadDashboard() {
    setIsLoading(true)
    try {
      const [availableDatasets, availableRuns] = await Promise.all([
        api.listDatasets(),
        api.listRuns(),
      ])
      const selectableDatasets = availableDatasets.filter((dataset) =>
        selectableDatasetNames.has(dataset.dataset_name),
      )
      setDatasets(selectableDatasets)
      setRuns(availableRuns)
      if (selectableDatasets.length > 0 && !selectableDatasets.some((dataset) => dataset.dataset_name === selectedDataset)) {
        setSelectedDataset(selectableDatasets[0].dataset_name)
      }
      if (availableRuns.length > 0) {
        await openRun(availableRuns.some((saved) => saved.run_id === selectedRunId) ? selectedRunId! : availableRuns[0].run_id)
      } else {
        setSelectedRunId(null)
        setRun(null)
        setCurrent(null)
        setPacket(null)
        setStageReview(null)
        setHistory(null)
        setContextRequests([])
        setRetrospectiveTasks([])
        setSelectedRetrospectiveTaskId(null)
        setRetrospectivePacket(null)
        setRetrospectiveSubmittedTaskId(null)
        setRetrospectiveAnalysisRevealed(false)
        setRunArtifacts(null)
      }
    } catch (loadError) {
      setError(loadError instanceof Error ? loadError.message : 'Unable to load the local CODA service.')
    } finally {
      setIsLoading(false)
    }
  }

  async function openRun(runId: string) {
    setError(null)
    try {
      const [nextRun, nextCurrent, nextCodebook, nextHistory, nextContextRequests] = await Promise.all([
        api.getRun(runId),
        api.getCurrentArtifact(runId),
        api.getCodebook(runId),
        api.getHistory(runId),
        api.getContextRequests(runId),
      ])
      const nextStageReview = nextRun.status === 'awaiting_initial_review'
        ? await api.getStageReview(runId, 'initial')
        : nextRun.status === 'awaiting_final_review'
          ? await api.getStageReview(runId, 'final')
          : null
      startTransition(() => {
        setSelectedRunId(runId)
        setSourceOpen(false)
        setRun(nextRun)
        // Keep the setup controls consistent with the saved run being viewed.
        setSelectedDataset(nextRun.dataset_name)
        setArtifactLimit(Math.max(1, nextRun.input_artifacts))
        setCurrent({ ...nextCurrent, codebook: nextCodebook })
        setPacket(null)
        setStageReview(nextStageReview)
        setActiveNodeId(currentNodeForRun(nextRun))
        setAgentAnalysisRevealed(false)
        setActiveView('workspace')
        setHistory(nextHistory)
        setContextRequests(nextContextRequests.requests)
        setRetrospectiveTasks(nextHistory.retrospective_tasks ?? [])
        setSelectedRetrospectiveTaskId(null)
        setRetrospectivePacket(null)
        setRetrospectiveSubmittedTaskId(null)
        setRetrospectiveAnalysisRevealed(false)
        setRunArtifacts(null)
        setSelectedCodeArtifacts(null)
        codeArtifactsRequest.current += 1
        setIsLoadingCodeArtifacts(false)
        setSelectedRecordId(nextHistory.coding_records[0]?.record_id ?? null)
      })
      try {
        const preparedPacket = await api.getReviewPacket(runId)
        setPacket(preparedPacket)
        setAgentAnalysisRevealed(false)
      } catch {
        // A packet is intentionally absent until the agent stages have run.
      }
    } catch (openError) {
      setError(openError instanceof Error ? openError.message : 'Unable to open this run.')
    }
  }

  useEffect(() => {
    void loadDashboard()
  }, [])

  useEffect(() => {
    if (!run) return
    const nextNode = currentNodeForRun(run)
    const previous = previousWorkflowPosition.current
    // Follow live initialization unless the researcher chose another node to inspect.
    if (previous?.runId === run.run_id && previous.node !== nextNode) {
      setActiveNodeId((selected) => selected === previous.node ? nextNode : selected)
    }
    previousWorkflowPosition.current = { runId: run.run_id, node: nextNode }
  }, [run])

  useEffect(() => {
    if (!selectedRunId || !isInitializing) return
    const cancelOnUnload = () => {
      // Closing the workbench must not leave a server-side bootstrap running.
      api.cancelInitializationOnUnload(selectedRunId)
    }
    window.addEventListener('beforeunload', cancelOnUnload)
    return () => window.removeEventListener('beforeunload', cancelOnUnload)
  }, [selectedRunId, isInitializing])

  useEffect(() => {
    const bootstrapStatus = run?.bootstrap_status
    const activeStatuses = new Set(['running', 'cancelling'])
    if (!selectedRunId || (!isInitializing && !isStoppingInitialization && !activeStatuses.has(bootstrapStatus ?? ''))) return
    let stopped = false
    let requestInFlight = false

    const refreshBootstrapProgress = async () => {
      if (stopped || requestInFlight) return
      requestInFlight = true
      try {
        const latest = await api.getRun(selectedRunId)
        if (!stopped) {
          setRun(latest)
          setRuns((existing) => existing.map((savedRun) => (
            savedRun.run_id === latest.run_id ? latest : savedRun
          )))
          if (!activeStatuses.has(latest.bootstrap_status)) {
            setIsInitializing(false)
            setIsStoppingInitialization(false)
            if (!isInitializing && latest.bootstrap_status === 'completed') await openRun(selectedRunId)
          }
        }
      } catch {
        // The initialization request reports its own terminal error. Avoid
        // replacing the visible progress with a transient polling error.
      } finally {
        requestInFlight = false
      }
    }

    void refreshBootstrapProgress()
    const intervalId = window.setInterval(() => void refreshBootstrapProgress(), 1000)
    return () => {
      stopped = true
      window.clearInterval(intervalId)
    }
  }, [selectedRunId, isInitializing, isStoppingInitialization, run?.bootstrap_status])

  useEffect(() => {
    if (!runContextMenu) return
    const closeMenu = () => setRunContextMenu(null)
    window.addEventListener('click', closeMenu)
    window.addEventListener('scroll', closeMenu, true)
    return () => {
      window.removeEventListener('click', closeMenu)
      window.removeEventListener('scroll', closeMenu, true)
    }
  }, [runContextMenu])

  useEffect(() => {
    if (!runPickerOpen) return
    const closePicker = () => setRunPickerOpen(false)
    const closeOnEscape = (event: KeyboardEvent) => {
      if (event.key === 'Escape') closePicker()
    }
    window.addEventListener('click', closePicker)
    window.addEventListener('keydown', closeOnEscape)
    return () => {
      window.removeEventListener('click', closePicker)
      window.removeEventListener('keydown', closeOnEscape)
    }
  }, [runPickerOpen])

  async function createRun() {
    if (operationBusy || isLoading) return
    setError(null)
    setIsLoading(true)
    setIsCreatingTask(true)
    try {
      const newRun = await api.createRun(selectedDataset, artifactLimit, 'selective', experimentVariant, heldOutEnabled, heldOutSize, iterativeBatchSize)
      setRuns((existing) => [newRun, ...existing])
      await openRun(newRun.run_id)
      setNewTaskOpen(false)
    } catch (createError) {
      setError(createError instanceof Error ? createError.message : 'Unable to create a run.')
    } finally {
      setIsLoading(false)
      setIsCreatingTask(false)
    }
  }

  async function exportHeldOutMaterials() {
    if (!selectedRunId) return
    setError(null)
    setIsExportingHeldOut(true)
    try {
      const packet = await api.getHeldOutMaterials(selectedRunId)
      const blob = new Blob([JSON.stringify(packet, null, 2)], { type: 'application/json' })
      const url = URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = `held_out_materials-${selectedRunId}.json`
      document.body.appendChild(link)
      link.click()
      link.remove()
      URL.revokeObjectURL(url)
    } catch (exportError) {
      setError(exportError instanceof Error ? exportError.message : 'Unable to export the held-out packet.')
    } finally {
      setIsExportingHeldOut(false)
    }
  }

  async function initializeTask() {
    if (!selectedRunId) return
    if (run?.bootstrap_status === 'running' || run?.bootstrap_status === 'cancelling') return
    const initializingRunId = selectedRunId
    const controller = new AbortController()
    initializationRequest.current = controller
    setError(null)
    setIsInitializing(true)
    setIsStoppingInitialization(false)
    try {
      const initializedRun = await api.initializeRun(initializingRunId, language, controller.signal)
      setRuns((existing) => existing.map((savedRun) => (
        savedRun.run_id === initializedRun.run_id ? initializedRun : savedRun
      )))
      if (selectedRunId === initializingRunId) await openRun(initializedRun.run_id)
      setRunArtifacts(null)
    } catch (initializeError) {
      if (!(initializeError instanceof DOMException && initializeError.name === 'AbortError')) {
        setError(initializeError instanceof Error ? initializeError.message : 'Unable to initialize this task.')
      }
    } finally {
      if (initializationRequest.current === controller) initializationRequest.current = null
      setIsInitializing(false)
    }
  }

  async function stopInitialization() {
    if (!selectedRunId) return
    const stoppingRunId = selectedRunId
    setError(null)
    setIsStoppingInitialization(true)
    try {
      const latest = await api.cancelInitialization(stoppingRunId)
      initializationRequest.current?.abort()
      setRun((currentRun) => currentRun?.run_id === latest.run_id ? latest : currentRun)
      setRuns((existing) => existing.map((savedRun) => (
        savedRun.run_id === latest.run_id ? latest : savedRun
      )))
      if (latest.bootstrap_status !== 'cancelling') setIsStoppingInitialization(false)
    } catch (stopError) {
      setIsStoppingInitialization(false)
      setError(stopError instanceof Error ? stopError.message : 'Unable to stop initialization.')
    }
  }

  async function confirmDeleteRun() {
    if (!deleteRunId) return
    const removingRunId = deleteRunId
    setIsDeletingRun(true)
    setError(null)
    try {
      await api.deleteRun(removingRunId)
      const remainingRuns = runs.filter((savedRun) => savedRun.run_id !== removingRunId)
      setRuns(remainingRuns)
      setDeleteRunId(null)
      if (selectedRunId === removingRunId) {
        setSelectedRunId(null)
        setRun(null)
        setCurrent(null)
        setPacket(null)
        setStageReview(null)
        setHistory(null)
        setContextRequests([])
        setRetrospectiveTasks([])
        setSelectedRetrospectiveTaskId(null)
        setRetrospectivePacket(null)
        setRetrospectiveSubmittedTaskId(null)
        setRetrospectiveAnalysisRevealed(false)
        setRunArtifacts(null)
        setSelectedCodeArtifacts(null)
        setSourceOpen(false)
        setActiveView('workspace')
        setActiveNodeId('input')
        if (remainingRuns.length > 0) await openRun(remainingRuns[0].run_id)
      }
    } catch (deleteError) {
      setError(deleteError instanceof Error ? deleteError.message : 'Unable to delete the saved run.')
    } finally {
      setIsDeletingRun(false)
    }
  }

  function openRunContextMenu(event: MouseEvent<HTMLElement>, runId = selectedRunId) {
    if (!runId || operationBusy) return
    event.preventDefault()
    event.stopPropagation()
    setRunContextMenu({ runId, x: event.clientX, y: event.clientY })
  }

  async function preparePacket(requestedLanguage = language) {
    if (!selectedRunId) return
    setError(null)
    setIsPreparing(true)
    try {
      const preparedPacket = await api.prepareReview(selectedRunId, requestedLanguage)
      setPacket(preparedPacket)
      setActiveNodeId('triggered_review')
      setActiveView('workspace')
      setAgentAnalysisRevealed(false)
      const [nextRun, nextCurrent] = await Promise.all([
        api.getRun(selectedRunId),
        api.getCurrentArtifact(selectedRunId),
      ])
      setRun(nextRun)
      setRuns((existing) => existing.map((saved) => saved.run_id === nextRun.run_id ? nextRun : saved))
      setCurrent(nextCurrent)
    } catch (prepareError) {
      setError(prepareError instanceof Error ? prepareError.message : 'Unable to prepare the evidence packet.')
    } finally {
      setIsPreparing(false)
    }
  }

  function selectRetrospectiveTask(taskId: string) {
    setSelectedRetrospectiveTaskId(taskId)
    setRetrospectivePacket(null)
    setRetrospectiveSubmittedTaskId(null)
    setRetrospectiveAnalysisRevealed(false)
    setError(null)
  }

  async function prepareRetrospectiveTask() {
    if (!selectedRunId || !selectedRetrospectiveTaskId) return
    setError(null)
    setIsPreparingRetrospective(true)
    try {
      const prepared = await api.prepareRetrospectiveTask(selectedRunId, selectedRetrospectiveTaskId, language)
      if (!('review_kind' in prepared)) {
        setRetrospectivePacket(null)
        setRetrospectiveSubmittedTaskId(prepared.task.task_id)
        await openRun(selectedRunId)
        setActiveView('retrospective')
        return
      }
      setRetrospectivePacket(prepared)
      setRetrospectiveSubmittedTaskId(null)
      setRetrospectiveAnalysisRevealed(false)
    } catch (prepareError) {
      setError(prepareError instanceof Error ? prepareError.message : 'Unable to prepare the retrospective evidence packet.')
    } finally {
      setIsPreparingRetrospective(false)
    }
  }

  async function resolveContextRequest(requestId: string, suppliedContext: string[], resolution: string) {
    if (!selectedRunId) return
    setError(null)
    setIsSavingContextRequest(true)
    try {
      const result = await api.resolveContextRequest(selectedRunId, requestId, suppliedContext, resolution)
      setContextRequests(result.requests)
      setHistory((existing) => existing ? { ...existing, context_requests: result.requests } : existing)
      const runId = selectedRunId
      await openRun(runId)
      setActiveView('context_requests')
    } catch (contextError) {
      setError(contextError instanceof Error ? contextError.message : 'Unable to resolve the context request.')
    } finally {
      setIsSavingContextRequest(false)
    }
  }

  async function cancelContextRequest(requestId: string) {
    if (!selectedRunId) return
    setError(null)
    setIsSavingContextRequest(true)
    try {
      const result = await api.cancelContextRequest(selectedRunId, requestId)
      setContextRequests(result.requests)
      setHistory((existing) => existing ? { ...existing, context_requests: result.requests } : existing)
      await openRun(selectedRunId)
    } catch (contextError) {
      setError(contextError instanceof Error ? contextError.message : 'Unable to cancel the context request.')
    } finally {
      setIsSavingContextRequest(false)
    }
  }

  async function updateAnalyticMemo(
    memoId: string,
    status: 'open' | 'resolved',
    rationale: string,
  ) {
    if (!selectedRunId) return
    setError(null)
    setIsSavingMemo(true)
    try {
      await api.updateAnalyticMemoStatus(selectedRunId, memoId, status, rationale)
      setHistory(await api.getHistory(selectedRunId))
    } catch (memoError) {
      setError(memoError instanceof Error ? memoError.message : 'Unable to update the analytic memo.')
    } finally {
      setIsSavingMemo(false)
    }
  }

  async function processAutomatic() {
    if (!selectedRunId || run?.review_setting === 'full') return
    setError(null)
    setIsAutoProcessing(true)
    try {
      const result = await api.processAutomatic(selectedRunId, language)
      setRun(result.run)
      setRuns((existing) => existing.map((savedRun) => savedRun.run_id === result.run.run_id ? result.run : savedRun))
      setCurrent(result.current)
      setActiveNodeId(currentNodeForRun(result.run))
      setActiveView('workspace')
      setPacket(null)
      if (result.run.status === 'awaiting_final_review') {
        setStageReview(await api.getStageReview(selectedRunId, 'final'))
      } else {
        setStageReview(null)
      }
      if (result.stopped_for_human) {
        setPacket(await api.getReviewPacket(selectedRunId))
        setAgentAnalysisRevealed(false)
      }
    } catch (processError) {
      setError(processError instanceof Error ? processError.message : 'Unable to process automatic passes.')
    } finally {
      setIsAutoProcessing(false)
    }
  }

  async function recordReviewTimer(
    action: 'pause' | 'resume',
    scope: 'artifact' | 'initial' | 'triggered' | 'final' | 'rework',
    artifactId?: string,
  ) {
    if (!selectedRunId) return
    await api.recordReviewTimer(selectedRunId, action, scope, artifactId)
  }

  async function selectReviewSetting(setting: ReviewMode, continueAutomatic = false) {
    if (!selectedRunId || isChangingSetting) return
    setError(null)
    setIsChangingSetting(true)
    try {
      if (stageReview?.kind === 'initial') {
        if (setting === 'automatic') await recordReviewTimer('pause', 'initial')
        else if (run?.review_setting === 'automatic') await recordReviewTimer('resume', 'initial')
      }
      const result = await api.selectInitialReviewSetting(selectedRunId, setting, continueAutomatic)
      setRun(result.run)
      setRuns((existing) => existing.map((saved) => saved.run_id === result.run.run_id ? result.run : saved))
      if (continueAutomatic) {
        await openRun(selectedRunId)
      } else if (stageReview?.kind === 'initial' && !result.packet?.inspection_only) {
        setStageReview(result.packet)
      }
    } catch (settingError) {
      setError(settingError instanceof Error ? settingError.message : 'Unable to save the review setting.')
    } finally {
      setIsChangingSetting(false)
    }
  }

  async function submitStageReview(review: StageReviewRequest) {
    if (!selectedRunId || !stageReview) return
    setError(null)
    setIsSubmittingStageReview(true)
    try {
      await api.submitStageReview(selectedRunId, stageReview.kind, review)
      setRunArtifacts(null)
      setSelectedCodeArtifacts(null)
      await openRun(selectedRunId)
    } catch (stageError) {
      setError(stageError instanceof Error ? stageError.message : 'Unable to save the stage review.')
    } finally {
      setIsSubmittingStageReview(false)
    }
  }

  async function submitReview(review: SubmitReviewRequest) {
    if (!selectedRunId) return
    setError(null)
    setIsSubmitting(true)
    try {
      const result = await api.submitReview(selectedRunId, review)
      const nextHistory = await api.getHistory(selectedRunId)
      setRun(result.run)
      setRuns((existing) => existing.map((savedRun) => savedRun.run_id === result.run.run_id ? result.run : savedRun))
      setCurrent({
        artifact: null,
        message: 'Review saved. Inspect the updated codebook, then explicitly advance to the next artifact.',
        codebook: result.codebook,
      })
      if (review.decision === 'request_additional_context') {
        setPacket(null)
        setAgentAnalysisRevealed(false)
      }
      setHistory(nextHistory)
      setContextRequests(nextHistory.context_requests ?? [])
      setRetrospectiveTasks(nextHistory.retrospective_tasks ?? [])
      setRunArtifacts(null)
      setSelectedCodeArtifacts(null)
      setSelectedRecordId(nextHistory.coding_records.at(-1)?.record_id ?? null)
    } catch (submitError) {
      setError(submitError instanceof Error ? submitError.message : 'Unable to save the human review.')
    } finally {
      setIsSubmitting(false)
    }
  }

  async function submitRetrospectiveReview(review: ReviewSubmission) {
    if (!selectedRunId || !selectedRetrospectiveTaskId) return
    setError(null)
    setIsSubmittingRetrospective(true)
    try {
      const result = await api.submitRetrospectiveReview(selectedRunId, selectedRetrospectiveTaskId, review)
      const nextHistory = await api.getHistory(selectedRunId)
      setRun(result.run)
      setRuns((existing) => existing.map((savedRun) => savedRun.run_id === result.run.run_id ? result.run : savedRun))
      setCurrent((existing) => existing ? { ...existing, codebook: result.codebook } : existing)
      setHistory(nextHistory)
      setRetrospectiveTasks(nextHistory.retrospective_tasks ?? [])
      setContextRequests(nextHistory.context_requests ?? [])
      if (review.decision === 'request_additional_context') {
        setRetrospectivePacket(null)
        setRetrospectiveSubmittedTaskId(null)
        setRetrospectiveAnalysisRevealed(false)
        setActiveView('context_requests')
      } else {
        setRetrospectiveSubmittedTaskId(selectedRetrospectiveTaskId)
      }
      setRunArtifacts(null)
      setSelectedCodeArtifacts(null)
    } catch (submitError) {
      setError(submitError instanceof Error ? submitError.message : 'Unable to save the retrospective review.')
    } finally {
      setIsSubmittingRetrospective(false)
    }
  }

  async function nextRetrospectiveTask() {
    const nextTask = retrospectiveTasks.find((task) => task.status !== 'completed' && task.status !== 'cancelled' && task.task_id !== selectedRetrospectiveTaskId)
    if (nextTask) {
      selectRetrospectiveTask(nextTask.task_id)
      return
    }
    setRetrospectivePacket(null)
    setRetrospectiveSubmittedTaskId(null)
  }

  async function nextArtifact() {
    if (!selectedRunId) return
    setError(null)
    setIsAdvancing(true)
    setAgentAnalysisRevealed(false)
    try {
      let result = await api.nextArtifact(selectedRunId)
      const updateAdvanceResult = (nextResult: typeof result) => {
        setRun(nextResult.run)
        setRuns((existing) => existing.map((savedRun) => savedRun.run_id === nextResult.run.run_id ? nextResult.run : savedRun))
        setCurrent(nextResult.current)
      }
      updateAdvanceResult(result)

      // Automatic and Selective modes persist and return after each artifact.
      // Continue as one researcher action while giving React a render point
      // and retaining a clean retry boundary between LLM requests.
      let lastReviewedCount = -1
      while (result.run.review_mode !== 'full' && result.run.awaiting_next_artifact) {
        if (result.run.reviewed_artifacts <= lastReviewedCount) {
          throw new Error(t('advanceNoProgress'))
        }
        lastReviewedCount = result.run.reviewed_artifacts
        result = await api.nextArtifact(selectedRunId)
        updateAdvanceResult(result)
      }

      if (result.run.review_mode === 'full' && result.run.status === 'in_progress') {
        setPacket(await api.prepareReview(selectedRunId, language))
        const [latestRun, latestCurrent] = await Promise.all([api.getRun(selectedRunId), api.getCurrentArtifact(selectedRunId)])
        result = { ...result, run: latestRun, current: latestCurrent }
        updateAdvanceResult(result)
      } else if (result.run.status === 'awaiting_human_review') {
        setPacket(await api.getReviewPacket(selectedRunId))
      } else {
        setPacket(null)
      }

      setStageReview(result.run.status === 'awaiting_final_review' ? await api.getStageReview(selectedRunId, 'final') : null)
      setActiveNodeId(result.run.review_mode === 'full' && result.run.status === 'in_progress' ? 'triggered_review' : currentNodeForRun(result.run))
      setActiveView('workspace')
    } catch (advanceError) {
      setError(advanceError instanceof Error ? advanceError.message : 'Unable to move to the next artifact.')
    } finally {
      setIsAdvancing(false)
    }
  }

  async function loadRunArtifacts() {
    if (!selectedRunId) return
    setError(null)
    setIsLoadingArtifacts(true)
    try {
      setRunArtifacts(await api.getRunArtifacts(selectedRunId))
    } catch (artifactError) {
      setError(artifactError instanceof Error ? artifactError.message : 'Unable to read persisted run files.')
    } finally {
      setIsLoadingArtifacts(false)
    }
  }

  async function loadCodeArtifacts(codeId: string) {
    if (!selectedRunId) return
    setError(null)
    const requestId = ++codeArtifactsRequest.current
    setIsLoadingCodeArtifacts(true)
    try {
      const result = await api.getCodeArtifacts(selectedRunId, codeId)
      if (requestId === codeArtifactsRequest.current) setSelectedCodeArtifacts(result)
    } catch (codeError) {
      setError(codeError instanceof Error ? codeError.message : 'Unable to load artifacts for this code.')
    } finally {
      if (requestId === codeArtifactsRequest.current) setIsLoadingCodeArtifacts(false)
    }
  }

  const rawCodebook: Codebook | null = current?.codebook ?? packet?.review_input.codebook ?? null
  const codebook = enrichCodebookTranslations(
    rawCodebook,
    (history?.artifact_runs ?? []) as Array<Record<string, unknown>>,
  )
  const shownArtifact = packet?.review_input.artifact ?? current?.artifact ?? null
  const selectedDatasetInfo = datasets.find((dataset) => dataset.dataset_name === selectedDataset)
  const runsByDataset = runs.reduce<Record<string, RunSummary[]>>((groups, savedRun) => {
    const group = groups[savedRun.dataset_name] ?? []
    group.push(savedRun)
    groups[savedRun.dataset_name] = group
    return groups
  }, {})
  const filteredCodes = codebook?.codes.filter((code) => {
    const searchable = `${code.code_id} ${codeLocalized(code, 'name', language)} ${codeLocalized(code, 'definition', language)} ${code.name} ${code.definition}`.toLocaleLowerCase()
    return searchable.includes(deferredCodeSearch.toLocaleLowerCase())
  }) ?? []
  const evidencePacket = packet?.review_input.evidence_packet
  const localizedSelectedCodeArtifacts = selectedCodeArtifacts && codebook
    ? {
        ...selectedCodeArtifacts,
        code: codebook.codes.find((code) => code.code_id === selectedCodeArtifacts.code.code_id)
          ?? selectedCodeArtifacts.code,
      }
    : selectedCodeArtifacts
  const bootstrapNeedsAction = !isStoppingInitialization && ['not_run', 'failed', 'cancelled', 'interrupted'].includes(run?.bootstrap_status ?? '')
  const bootstrapRetry = ['failed', 'cancelled', 'interrupted'].includes(run?.bootstrap_status ?? '')
  const bootstrapInProgress = isInitializing || isStoppingInitialization || run?.bootstrap_status === 'running' || run?.bootstrap_status === 'cancelling'
  const bootstrapSetupVisible = bootstrapNeedsAction || bootstrapInProgress
  const heldOutExportReady = Boolean(
    run?.held_out_artifacts
      && ['completed', 'stabilized', 'completed_with_unresolved'].includes(run.status),
  )
  const workspaceStyle = {
    '--workspace-left-width': workspaceWidths ? `${workspaceWidths.left}px` : '310px',
    '--workspace-right-width': workspaceWidths ? `${workspaceWidths.right}px` : '0.9fr',
  } as CSSProperties

  const operationBusy = isDeletingRun || isCreatingTask || isInitializing || isStoppingInitialization || isAutoProcessing || isPreparing || isAdvancing || isSubmitting || isSubmittingStageReview || isChangingSetting || isSubmittingRetrospective || isPreparingRetrospective || isSavingContextRequest || bootstrapInProgress
  const activeNode = executionNodes.find((node) => node.id === activeNodeId) ?? executionNodes[0]
  const reviewNodeId = stageReview ? (stageReview.kind === 'initial' ? 'initial_review' : 'final_review') : 'triggered_review'
  const showingReview = activeView === 'workspace' && activeNodeId === reviewNodeId && (!bootstrapSetupVisible || Boolean(stageReview))
  const focusCurrent = () => { setActiveView('workspace'); setActiveNodeId(currentNodeForRun(run)) }
  const primaryAction = (() => {
    if (bootstrapInProgress) return { label: t(isStoppingInitialization || run?.bootstrap_status === 'cancelling' ? 'stoppingInitialization' : 'stopInitialization'), onClick: () => void stopInitialization(), disabled: isStoppingInitialization || run?.bootstrap_status === 'cancelling', busy: isStoppingInitialization }
    if (bootstrapNeedsAction) return { label: t(bootstrapRetry ? 'resumeInitialization' : 'initializeTask'), onClick: () => { focusCurrent(); void initializeTask() }, disabled: operationBusy, busy: isInitializing }
    if (stageReview || run?.status === 'awaiting_human_review') return { label: t('goToReview'), onClick: focusCurrent, disabled: operationBusy, busy: operationBusy }
    if (run?.awaiting_context) return { label: t('contextRequests'), onClick: () => setActiveView('context_requests'), disabled: operationBusy, busy: false }
    if (run?.pending_retrospective_task_count) return { label: t('retrospectiveRecoding'), onClick: () => setActiveView('retrospective'), disabled: operationBusy, busy: false }
    if (run?.awaiting_next_artifact) return { label: t('continueWorkflow'), onClick: () => { focusCurrent(); void nextArtifact() }, disabled: operationBusy, busy: isAdvancing }
    if (run && ['completed', 'stabilized', 'completed_with_unresolved'].includes(run.status)) return { label: t('viewFinalAnalysis'), onClick: focusCurrent, disabled: false, busy: false }
    return { label: t(run?.review_setting === 'full' ? 'prepareEvidence' : 'processAutomatic'), onClick: () => { setActiveView('workspace'); void (run?.review_setting === 'full' ? preparePacket() : processAutomatic()) }, disabled: operationBusy || !shownArtifact, busy: isPreparing || isAutoProcessing }
  })()
  const codebookBrowser = <section className="codebook-browser" aria-label={t('codebook')}>
    <div className="panel-heading"><h2>{t('codebook')}</h2><span className="version-chip">v{codebook?.version ?? 0} · {codebook?.codes.length ?? 0} {t('entries')}</span></div>
    <label className="search-box"><Search size={16} /><input value={codeSearch} onChange={(event) => setCodeSearch(event.target.value)} placeholder={t('searchCodes')} aria-label={t('searchCodes')} /></label>
    <div className="codebook-browser-grid"><div className="codebook-list">{filteredCodes.map((code) => <CodeItem key={code.code_id} code={code} onSelect={(id) => void loadCodeArtifacts(id)} />)}{filteredCodes.length === 0 && <p className="empty-copy">{codebook ? t('noCodesSnapshot') : t('selectRunCodebook')}</p>}</div><CodeArtifactsView data={localizedSelectedCodeArtifacts} isLoading={isLoadingCodeArtifacts} /></div>
  </section>
  const toolItems: Array<{ id: AppView; label: string; count?: number }> = [
    { id: 'codebook', label: 'codebook' }, { id: 'history', label: 'reviewHistory' }, { id: 'evolution', label: 'codebookEvolution' },
    { id: 'retrospective', label: 'retrospectiveRecoding', count: retrospectiveTasks.filter((task) => !['completed', 'cancelled'].includes(task.status)).length },
    { id: 'context_requests', label: 'contextRequests', count: contextRequests.filter((request) => request.status === 'pending').length },
    { id: 'bootstrap', label: 'bootstrapRecord' }, { id: 'logs', label: 'runArtifacts' },
  ]
  const tools = <nav aria-label={t('recordsAndTools')}>{toolItems.map((item) => <button key={item.id} type="button" disabled={!run} className={activeView === item.id ? 'active' : ''} aria-current={activeView === item.id ? 'page' : undefined} onClick={() => { setActiveView(item.id); if (item.id === 'bootstrap' || item.id === 'logs') void loadRunArtifacts() }}><span>{t(item.label)}</span>{Boolean(item.count) && <span className="tool-count">{item.count}</span>}</button>)}</nav>
  const caseReviewMaterials = !stageReview && shownArtifact ? <section className="review-materials">
    <div className="section-action-heading"><div><p className="eyebrow">{t('currentArtifact')}</p><h2>{t('artifact')} {shownArtifact.artifact_id}</h2></div><button type="button" className="secondary-action" onClick={() => setSourceOpen(true)}><FileText size={15} />{t('originalArtifact')}</button></div>
    <details className="review-original" open><summary>{t('originalArtifact')}</summary><pre>{shownArtifact.content}</pre></details>
    <details className="review-codebook"><summary>{t('currentCodebook')} · v{codebook?.version ?? 0} · {codebook?.codes.length ?? 0} {t('entries')}</summary>{codebookBrowser}</details>
    {agentAnalysisRevealed && packet && <details className="review-analysis"><summary>{t('evidencePacket')}</summary><p>{localized(evidencePacket?.context_packet.context_brief, evidencePacket?.context_packet.context_brief_zh, language)}</p><EvidenceList items={evidencePacket?.context_packet.evidence_items ?? []} /><div className="coder-grid">{evidencePacket?.coder_outputs.map((coder) => <section className="coder-column" key={coder.coder_id}><h3>{translatedOrHumanized(`coderRole_${coder.coder_id}`, coder.coder_id, t)}</h3><ProposedCodes codes={coder.provisional_codes} /></section>)}</div><ProposedCodes codes={(evidencePacket?.comparison_output ?? evidencePacket?.arbitration_output)?.recommended_codes ?? []} /><CodebookChangePackets packets={evidencePacket?.codebook_change_packets ?? []} /><RoutingDecisionView packet={packet} /></details>}
  </section> : null
  const humanReview = stageReview ? <StageReviewView key={`${selectedRunId}-${stageReview.kind}`} packet={stageReview} runId={selectedRunId ?? ''} reviewSetting={run?.review_setting ?? 'selective'} settingLocked={Boolean(run?.review_setting_locked)} isChangingSetting={isChangingSetting} onSettingChange={(setting) => void selectReviewSetting(setting)} onAutomaticContinue={() => void selectReviewSetting('automatic', true)} isSubmitting={isSubmittingStageReview || isChangingSetting} onSubmit={submitStageReview} onTimerEvent={(action) => recordReviewTimer(action, stageReview.kind === 'initial' ? 'initial' : 'final')} onOpenRetrospective={() => setActiveView('retrospective')} onOpenContextRequests={() => setActiveView('context_requests')} /> : <>{caseReviewMaterials}<ReviewPanel
    key={packet?.artifact_id ?? 'process-review'} packet={packet} codebook={codebook} submitted={run?.awaiting_next_artifact ?? false} contextRequested={run?.awaiting_context ?? false}
    isSubmitting={isSubmitting} isAdvancing={isAdvancing} agentAnalysisRevealed={agentAnalysisRevealed} onSubmit={submitReview} onNext={nextArtifact}
    onRevealAgentAnalysis={() => setAgentAnalysisRevealed(true)} onOpenContextRequests={() => setActiveView('context_requests')} onTimerEvent={(action) => recordReviewTimer(action, 'artifact', packet?.artifact_id)} /></>
  const auxiliaryContent = <>
      {activeView === 'codebook' && codebookBrowser}
      {activeView === 'history' && <ReviewHistoryView history={history} selectedRecordId={selectedRecordId} onSelectRecord={setSelectedRecordId} onUpdateMemo={updateAnalyticMemo} isSavingMemo={isSavingMemo} />}
      {activeView === 'evolution' && <CodebookEvolutionView codebook={codebook} history={history} />}
      <div hidden={activeView !== 'retrospective'}><RetrospectiveWorkspaceView
        tasks={retrospectiveTasks}
        selectedTaskId={selectedRetrospectiveTaskId}
        packet={retrospectivePacket}
        codebook={codebook}
        submitted={retrospectiveSubmittedTaskId === selectedRetrospectiveTaskId && Boolean(selectedRetrospectiveTaskId)}
        isPreparing={isPreparingRetrospective}
        isSubmitting={isSubmittingRetrospective}
        agentAnalysisRevealed={retrospectiveAnalysisRevealed}
        onSelectTask={selectRetrospectiveTask}
        onPrepare={prepareRetrospectiveTask}
        onSubmit={submitRetrospectiveReview}
        onNext={nextRetrospectiveTask}
        onRevealAgentAnalysis={() => setRetrospectiveAnalysisRevealed(true)}
        onTimerEvent={(action) => recordReviewTimer(action, 'rework', retrospectivePacket?.artifact_id)}
      /></div>
      {activeView === 'context_requests' && <ContextRequestsView
        requests={contextRequests}
        onResolve={resolveContextRequest}
        onCancel={cancelContextRequest}
        isSaving={isSavingContextRequest}
      />}
      {activeView === 'bootstrap' && <BootstrapRunView data={runArtifacts} isLoading={isLoadingArtifacts} onRefresh={loadRunArtifacts} />}
      {activeView === 'logs' && <RunArtifactsView data={runArtifacts} isLoading={isLoadingArtifacts} onRefresh={loadRunArtifacts} />}
  </>
  let nodeContent: React.ReactNode
  if (!run) nodeContent = <p className="process-empty">{isLoading ? t('loadingWorkspace') : t('createSmallRun')}</p>
  else if (bootstrapSetupVisible && ['input', 'context', 'coding', 'induction', 'initial_validation'].includes(activeNodeId)) nodeContent = <TaskSetupView run={run} isInitializing={isInitializing} isStopping={isStoppingInitialization} onInitialize={initializeTask} onCancel={stopInitialization} retry={bootstrapRetry} />
  else if (['context', 'coding', 'induction', 'initial_validation'].includes(activeNodeId)) nodeContent = <InitialNodeEvidence run={run} nodeId={activeNodeId} />
  else if (activeNodeId === 'initial_review' || activeNodeId === 'final_review') nodeContent = <StageReviewInspector key={`${run.run_id}-${activeNodeId}`} run={run} kind={activeNodeId === 'initial_review' ? 'initial' : 'final'} isChangingSetting={isChangingSetting} onSettingChange={(setting) => void selectReviewSetting(setting)} onOpenRetrospective={() => setActiveView('retrospective')} onOpenContextRequests={() => setActiveView('context_requests')} />
  else if (activeNodeId === 'triggered_review' && stageReview) nodeContent = <div className="process-empty"><p>{t('noTriggeredReview')}</p><button type="button" className="secondary-action" onClick={focusCurrent}>{t('returnToCurrentStep')}</button></div>
  else if (activeNodeId === 'codebook_update' || activeNodeId === 'final') nodeContent = <><WorkflowStageContent stage={activeNode.stage} run={run} current={current} packet={packet} codebook={codebook} onOpenArtifact={() => setSourceOpen(true)} onPrepare={() => void preparePacket()} isPreparing={isPreparing} onHumanReview={null} />{codebookBrowser}{activeNodeId === 'final' && codebook && <button type="button" className="secondary-action" onClick={() => { const url = URL.createObjectURL(new Blob([JSON.stringify(codebook, null, 2)], { type: 'application/json' })); const link = document.createElement('a'); link.href = url; link.download = `codebook-${run.run_id}.json`; link.click(); URL.revokeObjectURL(url) }}><Download size={15} />{t('downloadCodebook')}</button>}</>
  else nodeContent = <>
    {packet && !agentAnalysisRevealed && !run.awaiting_next_artifact && activeNodeId !== 'input' ? <div className="process-empty"><p>{t('recordPreRead')}</p><button className="secondary-action" type="button" onClick={() => { setActiveNodeId('triggered_review'); setActiveView('workspace') }}>{t('goToReview')}</button></div> : <><WorkflowStageContent stage={activeNode.stage} run={run} current={current} packet={packet} codebook={codebook} onOpenArtifact={() => setSourceOpen(true)} onPrepare={() => void preparePacket()} isPreparing={isPreparing || operationBusy || bootstrapSetupVisible || !shownArtifact || Boolean(stageReview) || Boolean(run.awaiting_next_artifact) || Boolean(run.awaiting_context)} onHumanReview={null} />{activeNodeId === 'validation' && packet && agentAnalysisRevealed && <RoutingDecisionView packet={packet} />}</>}
  </>

  return (
    <main className="app-shell">
      <header className="topbar compact-topbar">
        <div className="brand-block"><div className="brand-mark" aria-hidden="true"><BookOpenCheck size={22} /></div><h1>CODA</h1></div>
        <div
          className="run-selector"
          onContextMenu={openRunContextMenu}
          onClick={(event) => event.stopPropagation()}
        >
          <FolderOpen size={17} />
          <div className="run-picker">
            <button
              type="button"
              className="run-picker-trigger"
              onClick={() => setRunPickerOpen((open) => !open)}
              onContextMenu={openRunContextMenu}
              disabled={runs.length === 0 || operationBusy}
              aria-label={t('selectSavedRun')}
              aria-haspopup="listbox"
              aria-expanded={runPickerOpen}
            >
              <span className="run-picker-value">{selectedRunId ?? t('noSavedRun')}</span>
              {run && <span>{run.reviewed_artifacts}/{run.total_artifacts}</span>}
            </button>
            {runPickerOpen && runs.length > 0 && (
              <div className="run-picker-menu" role="listbox" aria-label={t('selectSavedRun')}>
                {Object.entries(runsByDataset).map(([datasetName, datasetRuns]) => (
                  <div key={datasetName} className="run-picker-group">
                    <p>{datasetRuns[0]?.dataset_display_name ?? datasetName}</p>
                    {datasetRuns.map((savedRun) => (
                      <button
                        key={savedRun.run_id}
                        type="button"
                        role="option"
                        aria-selected={savedRun.run_id === selectedRunId}
                        className={savedRun.run_id === selectedRunId ? 'run-option selected' : 'run-option'}
                        onClick={() => {
                          setRunPickerOpen(false)
                          void openRun(savedRun.run_id)
                        }}
                        onContextMenu={(event) => openRunContextMenu(event, savedRun.run_id)}
                      >
                        <strong>{savedRun.run_id}</strong>
                        <span>{savedRun.reviewed_artifacts}/{savedRun.total_artifacts}</span>
                      </button>
                    ))}
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
        <div className="header-actions">
          <button className="secondary-action" type="button" disabled={operationBusy} onClick={() => setNewTaskOpen((open) => !open)} aria-expanded={newTaskOpen || !run} aria-controls="new-task-panel"><Plus size={16} />{t('newRun')}</button>
          <button className="icon-button" type="button" onClick={() => void loadDashboard()} disabled={isLoading || operationBusy} title={t('refresh')} aria-label={t('refresh')}><RefreshCw size={17} className={isLoading ? 'spin' : ''} /></button>
          <select className="language-select" value={language} onChange={(event) => setLanguage(event.target.value as 'en' | 'zh')} aria-label={t('language')}><option value="en">English</option><option value="zh">中文</option></select>
        </div>
      </header>
      {(newTaskOpen || (!run && !isLoading)) && <section className="new-task-panel" id="new-task-panel"><div className="section-action-heading"><h2>{t('newRun')}</h2>{run && <button type="button" className="icon-button" aria-label={t('closePanel')} onClick={() => setNewTaskOpen(false)}><X size={16} /></button>}</div>
        <form className="run-controls task-form" aria-label={t('runControls')} onSubmit={(event) => { event.preventDefault(); void createRun() }}>
          <fieldset className="task-fields" disabled={operationBusy}>
          <label>
            <span>{t('newRunDataset')}</span>
            <select
              value={selectedDataset}
              onChange={(event) => {
                const nextDataset = datasets.find((dataset) => dataset.dataset_name === event.target.value)
                setSelectedDataset(event.target.value)
                if (nextDataset?.data_available) {
                  const nextLimit = Math.min(Math.max(1, artifactLimit), nextDataset.target_record_count)
                  setArtifactLimit(nextLimit)
                  if (nextLimit < 3) {
                    setHeldOutEnabled(false)
                  } else if (heldOutEnabled) {
                    const recommended = nextLimit <= 100 ? 12 : nextLimit <= 1000 ? 50 : 100
                    const scaled = Math.max(1, Math.round(nextLimit * 0.2))
                    setHeldOutSize((currentSize) => Math.min(currentSize, recommended, scaled, nextLimit - 2))
                  }
                }
              }}
            >
              {datasets.map((dataset) => (
                <option key={dataset.dataset_name} value={dataset.dataset_name} disabled={!dataset.data_available}>
                  {dataset.display_name} · {dataset.target_record_count} {t('artifacts')}{dataset.data_available ? '' : ` · ${t('dataUnavailable')}`}
                </option>
              ))}
            </select>
          </label>
          <label className="limit-control">
            <span>{t('artifacts')}</span>
            <input
              type="number"
              min="1"
              max={selectedDatasetInfo?.target_record_count || undefined}
              value={artifactLimit}
              onChange={(event) => {
                const requested = Math.max(1, Number(event.target.value))
                const nextLimit = selectedDatasetInfo ? Math.min(requested, selectedDatasetInfo.target_record_count) : requested
                setArtifactLimit(nextLimit)
                if (heldOutEnabled) {
                  const recommended = nextLimit <= 100 ? 12 : nextLimit <= 1000 ? 50 : 100
                  const scaled = Math.max(1, Math.round(nextLimit * 0.2))
                  setHeldOutSize((currentSize) => Math.min(currentSize, recommended, scaled, Math.max(1, nextLimit - 2)))
                }
              }}
            />
            {selectedDatasetInfo && <small className="dataset-count-hint">{t('artifactLimitHint', { count: selectedDatasetInfo.target_record_count })}</small>}
          </label>
          <details className="advanced-setup"><summary>{t('advancedSetup')}</summary><div className="advanced-fields">          <label className="limit-control">
            <span>{language === 'zh' ? '每批材料数' : 'Materials per batch'}</span>
            <input type="number" min="1" step="1" value={iterativeBatchSize}
              onChange={(event) => setIterativeBatchSize(Math.max(1, Math.floor(Number(event.target.value) || 1)))} />
            <small className="dataset-count-hint">{language === 'zh'
              ? '同批先统一比较，再逐项审核；已有运行保持原批次。'
              : 'Compare the batch together, then review decisions individually. Existing runs keep their batches.'}</small>
          </label>
          <label>
            <span>{t('experimentVariantLabel')}</span>
            <select value={experimentVariant} onChange={(event) => setExperimentVariant(event.target.value as ExperimentVariant)}>
              <option value="standard">{t('experimentStandard')}</option>
              <option value="freeze_after_initialization">{t('experimentFreezeAfterInitialization')}</option>
              <option value="without_retrospective_recoding">{t('experimentWithoutRetrospectiveRecoding')}</option>
            </select>
          </label>
          <label className="held-out-toggle">
            <span>{t('heldOutEvaluation')}</span>
            <span className="inline-control">
              <input
                type="checkbox"
                checked={heldOutEnabled}
                disabled={artifactLimit < 3}
                onChange={(event) => {
                  setHeldOutEnabled(event.target.checked)
                  if (event.target.checked) {
                    const recommended = artifactLimit <= 100 ? 12 : artifactLimit <= 1000 ? 50 : 100
                    const scaled = Math.max(1, Math.round(artifactLimit * 0.2))
                    setHeldOutSize(Math.min(recommended, scaled, artifactLimit - 2))
                  }
                }}
              />
              {t('heldOutEnable')}
            </span>
            {heldOutEnabled && (
              <input
                className="held-out-size"
                type="number"
                min="1"
                max={Math.max(1, artifactLimit - 2)}
                value={heldOutSize}
                onChange={(event) => {
                  const requested = Math.max(1, Number(event.target.value))
                  setHeldOutSize(Math.min(requested, Math.max(1, artifactLimit - 2)))
                }}
                aria-label={t('heldOutSize')}
              />
            )}
            <small className="dataset-count-hint">
              {artifactLimit < 3 ? t('heldOutMinimumHint') : heldOutEnabled ? t('heldOutHint') : t('heldOutDisabledHint')}
            </small>
          </label>
</div></details>
          <button className="command-button primary" type="submit" disabled={isLoading || operationBusy || datasets.length === 0 || !datasets.find((dataset) => dataset.dataset_name === selectedDataset)?.data_available} title={t('newRun')}>
            <Play size={16} />
            {isCreatingTask ? t('creatingTask') : t('newRun')}
          </button>
          </fieldset>
        </form>
      </section>}

      {error && (
        <div className="error-toast" role="alert" aria-live="assertive">
          <CircleAlert size={17} />
          <span>{error}</span>
          <button className="error-dismiss" type="button" onClick={() => setError(null)} aria-label={language === 'zh' ? '关闭错误提示' : 'Dismiss error'}>
            <X size={15} />
          </button>
        </div>
      )}

      <section className="task-toolbar" aria-label={t('selectedRun')}>
        <div className="task-summary">
          {run ? <><span className={`run-status ${run.status}`}>{bootstrapStatusLabelKey(run) ? t(bootstrapStatusLabelKey(run)!) : statusLabel(run.status, t)}</span><strong className="task-dataset">{run.dataset_display_name}</strong><span className="task-progress">{run.reviewed_artifacts} / {run.total_artifacts} {t('processed')}</span><span className="task-policy">{t(`reviewSetting_${run.review_setting}`)}</span></> : <span className="muted">{isLoading ? t('loadingWorkspace') : t('createSmallRun')}</span>}
        </div>
        <div className="task-actions">
          {run && <details className="task-details"><summary>{t('taskDetails')}<ChevronDown size={13} /></summary><div className="task-details-menu">
            <dl><div><dt>{t('inputArtifacts', { count: run.input_artifacts })}</dt><dd>{run.input_artifacts}</dd></div><div><dt>{t('humanReviewedCount', { count: run.human_reviewed_artifacts })}</dt><dd>{run.human_reviewed_artifacts}</dd></div><div><dt>{t('automaticPassedCount', { count: run.auto_processed_artifacts })}</dt><dd>{run.auto_processed_artifacts}</dd></div><div><dt>{t('codebook')}</dt><dd>v{run.codebook_version} · {run.code_count}</dd></div><div><dt>{t('heldOutEvaluation')}</dt><dd>{run.held_out_artifacts ?? 0}</dd></div><div><dt>{t('experimentVariantLabel')}</dt><dd>{t(`experiment_${run.experiment_variant ?? 'standard'}`)}</dd></div></dl>
            {Boolean(run.held_out_artifacts) && <button className="secondary-action" type="button" onClick={() => void exportHeldOutMaterials()} disabled={!heldOutExportReady || isExportingHeldOut} title={heldOutExportReady ? t('heldOutExport') : t('heldOutExportAfterCompletion')}><Download size={15} />{t('heldOutExport')}</button>}
            <button className="secondary-action danger-text" type="button" onClick={() => setDeleteRunId(run.run_id)} disabled={operationBusy}><Trash2 size={14} />{t('deleteRun')}</button>
          </div></details>}
          {run && <button className="command-button primary" type="button" disabled={primaryAction.disabled} onClick={primaryAction.onClick}>{primaryAction.busy ? <LoaderCircle size={16} className="spin" /> : <Play size={15} />}{primaryAction.label}</button>}
        </div>
      </section>


      {runContextMenu && (
        <div
          className="run-context-menu"
          role="menu"
          style={{ left: runContextMenu.x, top: runContextMenu.y }}
          onContextMenu={(event) => event.preventDefault()}
        >
          <button type="button" role="menuitem" onClick={() => { setDeleteRunId(runContextMenu.runId); setRunContextMenu(null) }}>
            <Trash2 size={14} /> {t('deleteRun')}
          </button>
        </div>
      )}

      {deleteRunId && (
        <div className="modal-backdrop" role="presentation">
          <section className="confirm-dialog" role="dialog" aria-modal="true" aria-labelledby="delete-run-title">
            <p className="eyebrow">{t('deleteRun')}</p>
            <h2 id="delete-run-title">{t('confirmDeleteRun')}</h2>
            <p>{t('deleteRunWarning', { id: deleteRunId })}</p>
            <div className="dialog-actions">
              <button type="button" className="secondary-action" onClick={() => setDeleteRunId(null)} disabled={isDeletingRun}>{t('cancel')}</button>
              <button type="button" className="command-button danger" onClick={() => void confirmDeleteRun()} disabled={isDeletingRun}>
                <Trash2 size={15} /> {isDeletingRun ? t('deletingRun') : t('deleteRun')}
              </button>
            </div>
          </section>
        </div>
      )}

      <ProcessWorkbench activeNodeId={activeNodeId} onSelectNode={(id) => { setActiveNodeId(id); setActiveView('workspace') }} run={run} stageStatus={(stage) => workflowStageStatus(stage, run, packet, current)} workspaceRef={workspaceRef} workspaceStyle={workspaceStyle} onResizeStart={startWorkspaceResize} onResizeKeyAdjust={adjustWorkspaceResize} tools={tools} toolActive={activeView !== 'workspace'} humanReview={humanReview} reviewNodeId={reviewNodeId} showingReview={showingReview}>
        <div hidden={activeView === 'workspace'}><div className="tool-heading"><button type="button" className="secondary-action" onClick={focusCurrent}><ChevronRight size={14} />{t('returnToCurrentStep')}</button><span>{t(toolItems.find((item) => item.id === activeView)?.label ?? 'workspace')}</span></div>{auxiliaryContent}</div>
        {activeView === 'workspace' && !showingReview && nodeContent}
      </ProcessWorkbench>
      {sourceOpen && shownArtifact && <SourceDialog artifact={shownArtifact} onClose={() => setSourceOpen(false)} />}
    </main>
  )
}

export default App
