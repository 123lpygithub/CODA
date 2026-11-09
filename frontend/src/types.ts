export type RunStatus =
  | 'not_started'
  | 'awaiting_initial_review'
  | 'in_progress'
  | 'awaiting_human_review'
  | 'awaiting_context'
  | 'awaiting_next_artifact'
  | 'awaiting_final_review'
  | 'stabilized'
  | 'completed_with_unresolved'
  | 'resource_limited'
  | 'completed'

export type ReviewMode = 'automatic' | 'selective' | 'full'
export type ExperimentVariant = 'standard' | 'freeze_after_initialization' | 'without_retrospective_recoding'

export interface Dataset {
  dataset_name: string
  display_name: string
  target_record_count: number
  artifact_unit: string
  task_family: string
  data_available: boolean
  availability_message: string | null
}

export type BootstrapProgressStatus =
  | 'not_run'
  | 'running'
  | 'cancelling'
  | 'cancelled'
  | 'interrupted'
  | 'completed'
  | 'failed'
  | 'skipped'
  | 'disabled'

export interface BootstrapProgress {
  status: BootstrapProgressStatus
  phase: string
  processed_artifacts: number
  total_artifacts: number
  overall_completed: number
  overall_total: number
  stage_index?: number
  stage_total?: number
  percent: number
  current_artifact_id: string | null
  error?: string | null
}

export interface RunSummary {
  run_id: string
  dataset_name: string
  dataset_display_name: string
  status: RunStatus
  run_dir: string
  reviewed_artifacts: number
  input_artifacts: number
  human_review_artifacts: number
  selected_artifacts?: number
  coding_pool_artifacts?: number
  held_out_artifacts?: number
  total_selected_artifacts?: number
  human_reviewed_artifacts: number
  auto_processed_artifacts: number
  total_artifacts: number
  codebook_version: number
  code_count: number
  bootstrap_enabled: boolean
  bootstrap_status: BootstrapProgressStatus
  bootstrap_artifacts: number
  bootstrap_code_count: number
  bootstrap_protocol: Record<string, unknown>
  bootstrap_progress: BootstrapProgress
  awaiting_next_artifact: boolean
  awaiting_context: boolean
  pending_context_request_count?: number
  review_mode: ReviewMode
  review_setting: ReviewMode
  review_setting_locked?: boolean
  experiment_variant?: ExperimentVariant
  experiment_protocol?: Record<string, unknown>
  open_unresolved_count?: number
  initial_review?: StageReviewRecord | null
  final_review?: StageReviewRecord | null
  stabilization?: StabilizationCheck | null
  retrospective_task_count?: number
  pending_retrospective_task_count?: number
}

export interface HeldOutMaterials {
  format: string
  format_version: number
  run_id: string
  dataset_name: string
  main_run_status: RunStatus
  codebook_version: number
  codebook: Codebook
  artifacts: Artifact[]
  protocol: Record<string, unknown>
  reference_data_included: false
  application_instructions: string[]
  judgment_schema: Record<string, unknown>
}

export interface Code {
  code_id: string
  name: string
  definition: string
  inclusion_criteria: string[]
  exclusion_criteria: string[]
  representative_artifact_ids: string[]
  boundary_artifact_ids: string[]
  counterexample_status: 'not_assessed' | 'no_observed_counterexample' | 'observed_counterexample'
  hypothetical_examples: string[]
  parent_code_id: string | null
  status: 'active' | 'merged' | 'split' | 'retired'
  notes: string[]
  metadata?: Record<string, unknown>
}

export interface Codebook {
  dataset_name: string
  version: number
  codes: Code[]
  sensitizing_concepts: string[]
  revisions: CodebookChange[]
  notes: string[]
}

export interface CodebookDiff {
  from_version: number
  to_version: number
  added: Code[]
  removed: Code[]
  changed: Array<{ before: Code; after: Code }>
}

export interface CodebookVersions {
  snapshots: Codebook[]
  diffs: CodebookDiff[]
}

export interface CodeArtifacts {
  codebook_version: number
  code: Code
  artifact_count: number
  artifacts: Array<{
    artifact: Artifact
    review: CodingRecord | null
  }>
}

export interface CodebookChange {
  change_id: string
  action: 'add' | 'add_parent' | 'refine' | 'merge' | 'split' | 'rename' | 'retire' | 'no_change'
  round_index: number
  summary: string
  summary_zh?: string
  rationale: string
  rationale_zh?: string
  target_code_ids: string[]
  resulting_code_ids: string[]
  artifact_ids: string[]
}

export interface Artifact {
  artifact_id: string
  content: string
  raw_fields: Record<string, unknown>
  source_refs: SourceRef[]
  metadata: Record<string, unknown>
}

export interface SourceRef {
  kind: string
  value: string
  ref_id?: string
  field?: string
}

export interface EvidenceItem {
  field_name: string
  excerpt: string
  locator?: {
    start?: number | null
    end?: number | null
    line_start?: number | null
    line_end?: number | null
  } | null
  rationale: string
  rationale_zh?: string
  claim_type?: 'reported' | 'observed' | 'inferred'
  revision?: string | null
}

export interface ProvisionalCode {
  code_name: string
  code_name_zh?: string
  short_definition: string
  short_definition_zh?: string
  inclusion_criteria?: string[]
  exclusion_criteria?: string[]
  inclusion_criteria_zh?: string[]
  exclusion_criteria_zh?: string[]
  observed_phenomenon?: string
  observed_phenomenon_zh?: string
  supporting_evidence: EvidenceItem[]
  relationship_to_codebook: string
  linked_code_ids: string[]
  alternative_interpretation: string
  alternative_interpretation_zh?: string
  uncertainty_note: string
  uncertainty_note_zh?: string
  proposed_codebook_action: string
}

export interface CoderOutput {
  artifact_id: string
  coder_id: string
  provisional_codes: ProvisionalCode[]
  insufficient_context: boolean
  overall_uncertainty: string
  overall_uncertainty_zh?: string
  /** Optional because traces written before confidence was introduced still exist. */
  confidence_level?: 'high' | 'medium' | 'low'
  confidence_rationale?: string
  confidence_rationale_zh?: string
  confidence_factors?: Record<string, string>
  notes: string[]
  notes_zh?: string[]
  model_metadata?: Record<string, unknown>
}

export interface ComparisonOutput {
  agreement_summary: string
  agreement_summary_zh?: string
  disagreement_summary: string
  disagreement_summary_zh?: string
  recommended_codes: ProvisionalCode[]
  preserved_alternatives: ProvisionalCode[]
  disagreements?: Array<{
    disagreement_type: string
    summary: string
    summary_zh?: string
  }>
  possible_codebook_changes: CodebookChange[]
  comparison_findings?: ComparisonFinding[]
  analytic_memos?: AnalyticMemo[]
}

/** @deprecated Read-only alias for historical run files. */
export type ArbitrationOutput = ComparisonOutput

export interface ComparisonFinding {
  comparison_id: string
  comparison_type: 'case_to_case' | 'case_to_code' | 'code_to_code'
  finding: string
  summary: string
  summary_zh?: string
  current_artifact_id?: string
  compared_artifact_ids: string[]
  compared_code_ids: string[]
  evidence_items: EvidenceItem[]
  implication: string
  implication_zh?: string
}

export interface AnalyticMemo {
  memo_id: string
  memo_type: string
  summary: string
  summary_zh?: string
  artifact_ids: string[]
  code_ids: string[]
  status: 'open' | 'resolved'
  resolution?: string
  updated_by?: string
  status_history?: Array<{
    from?: string
    status: 'open' | 'resolved'
    source?: string
    rationale?: string
    codebook_version?: number
  }>
}

export interface ValidationSignal {
  signal: string
  issue_scope?: 'none' | 'evidence' | 'assignment' | 'codebook' | 'context'
  summary: string
  summary_zh?: string
  related_code_names: string[]
  evidence_items: EvidenceItem[]
}

export interface ValidationOutput {
  signals: ValidationSignal[]
  human_review_required: boolean
  summary: string
  summary_zh?: string
  /** Optional for backwards-compatible rendering of older persisted traces. */
  confidence_level?: 'high' | 'medium' | 'low'
  confidence_rationale?: string
  confidence_rationale_zh?: string
  confidence_factors?: Record<string, string>
  review_criteria?: Array<'R1' | 'R2' | 'R3' | 'R4' | 'R5' | 'R6'>
  review_questions?: string[]
  review_questions_zh?: string[]
  notes: string[]
  notes_zh?: string[]
}

export interface ReviewPacket {
  artifact_id: string
  codebook_version: number
  review_input: {
    artifact: Artifact
    evidence_packet: {
      context_packet: {
        context_brief: string
        context_brief_zh?: string
        evidence_items: EvidenceItem[]
        missing_context_warnings: string[]
        missing_context_warnings_zh?: string[]
        distracting_information: string[]
        distracting_information_zh?: string[]
      }
      coder_outputs: CoderOutput[]
      candidate_definitions: string[]
      candidate_definitions_zh?: string[]
      alternative_interpretations: string[]
      alternative_interpretations_zh?: string[]
      comparison_output?: ComparisonOutput | null
      arbitration_output?: ArbitrationOutput | null
      validation_output: ValidationOutput | null
      proposed_codebook_changes: CodebookChange[]
      codebook_change_packets?: CodebookChangePacket[]
      routing_decision?: ReviewRoutingDecision | null
      comparison_findings?: ComparisonFinding[]
      analytic_memos?: AnalyticMemo[]
      model_metadata?: {
        batch_execution?: {
          batch_id: string
          artifact_ids: string[]
          base_version: number
          validated_version: number
          reconciled_proposal: ComparisonOutput
        }
      }
    }
    codebook: Codebook
    history: { coding_records: unknown[] }
  }
}

export interface CodebookChangePacket {
  change_id: string
  action: CodebookChange['action']
  summary: string
  summary_zh?: string
  rationale: string
  rationale_zh?: string
  before_codes: Code[]
  proposed_codes: Code[]
  supporting_artifact_ids: string[]
  boundary_artifact_ids: string[]
  affected_artifact_ids: string[]
  validation_warnings: string[]
}

export interface ReviewRoutingDecision {
  artifact_id: string
  setting: ReviewMode
  route: 'automatic_accept' | 'human_review' | 'unresolved'
  reasons: string[]
  risk_signals: string[]
  random_audit: boolean
  signal_details?: {
    review_criteria?: Array<'R1' | 'R2' | 'R3' | 'R4' | 'R5' | 'R6'>
    review_questions?: string[]
    review_questions_zh?: string[]
    [key: string]: unknown
  }
}

export interface StageReviewRecord {
  review_id: string
  kind: 'initial' | 'final'
  decision: string
  rationale: string
  codebook_version_before: number
  codebook_version_after: number
  metadata?: Record<string, unknown>
}

export interface StabilizationCheck {
  check_id: string
  codebook_version: number
  processed_artifacts: number
  remaining_artifacts: number
  open_unresolved_count: number
  pending_retrospective_count: number
  recent_new_code_count: number
  recent_substantive_revision_count: number
  window_size: number
  stable: boolean
  consecutive_stable_batches: number
  cross_source_audit_status: string
  cross_source_audit_artifact_ids: string[]
  reasons: string[]
  metadata?: Record<string, unknown>
}

export interface BootstrapAssignmentRecord {
  artifact_id: string
  code_ids: string[]
  evidence_summary: string[]
  status: string
}

export interface InitialCodingRecord {
  artifact_id: string
  context_packet: {
    context_brief: string
    context_brief_zh?: string
    evidence_items: EvidenceItem[]
    missing_context_warnings?: string[]
    missing_context_warnings_zh?: string[]
  }
  coder_outputs: CoderOutput[]
}

export interface StageReviewPacket {
  completion_issues?: string[]
  kind: 'initial' | 'final'
  inspection_only?: boolean
  review_record?: StageReviewRecord | null
  experiment_variant?: ExperimentVariant
  codebook_editing_allowed?: boolean
  research_question: Record<string, unknown>
  analysis_protocol: Record<string, unknown>
  codebook: Codebook
  context_requests: ContextRequest[]
  unresolved_cases: Array<Record<string, unknown>>
  pending_retrospective_tasks: RetrospectiveTask[]
  bootstrap?: BootstrapInspection | null
  audit?: { status?: string; warnings?: string[]; warnings_zh?: string[]; error?: string | null } | null
  sampled_artifacts?: Artifact[]
  cross_source_audit_artifacts?: Artifact[]
  cross_source_audit_records?: CodingRecord[]
  final_audit_artifacts?: Artifact[]
  final_audit_records?: CodingRecord[]
  final_validation_audits?: Array<{
    audit_id: string
    codebook_version: number
    status: string
    unprocessed_artifact_ids: string[]
    validation_outputs: Array<ValidationOutput & { artifact_id: string }>
  }>
  assignments?: BootstrapAssignmentRecord[]
  initial_codings?: InitialCodingRecord[]
  stabilization?: StabilizationCheck | null
  review_scope?: { checkpoint: string; purpose: string; required_checks: string[] }
  audit_summary?: Record<string, string | number | boolean>
  coverage?: {
    processed_artifacts: number
    bootstrap_artifacts: number
    iterative_artifacts: number
    input_artifacts: number
    code_count: number
    low_frequency_codes: Code[]
  }
}

export interface StageReviewRequest {
  decision: 'accept' | 'revise' | 'reject' | 'request_additional_context' | 'mark_unresolved'
  rationale: string
  revised_codes: CodeInput[]
  change_operations: CodebookChangeInput[]
  duration_seconds?: number
}

export interface CurrentArtifactResponse {
  artifact: Artifact | null
  batch_id?: string
  batch_index?: number
  batch_size?: number
  batch_position?: number
  batch_preparation?: string | null
  message?: string
  codebook: Codebook
}

export type HumanDecision =
  | 'accept'
  | 'revise'
  | 'reject'
  | 'mark_uncertain'
  | 'request_additional_context'

export type CodebookAction = CodebookChange['action']

export interface CodeInput {
  code_id: string
  name: string
  definition: string
  inclusion_criteria: string[]
  exclusion_criteria: string[]
  boundary_artifact_ids: string[]
  counterexample_status: Code['counterexample_status']
  hypothetical_examples: string[]
  parent_code_id: string | null
  status: Code['status']
  notes: string[]
  metadata?: Record<string, unknown>
}

export interface CodebookChangeInput {
  action: CodebookAction
  summary: string
  rationale: string
  target_code_ids: string[]
  resulting_code_ids: string[]
  artifact_ids: string[]
  metadata?: Record<string, unknown>
}

export interface SubmitReviewRequest {
  artifact_id: string
  decision: HumanDecision
  pre_read_memo: string
  final_codes: CodeInput[]
  rationale: string
  evidence_summary: string[]
  confirmed_evidence: EvidenceItem[]
  preserved_alternatives: string[]
  codebook_changes: CodebookChangeInput[]
  notes: string[]
  duration_seconds?: number
}

export interface SubmitReviewResponse {
  artifact_id: string
  decision: HumanDecision
  codebook: Codebook
  run: RunSummary
}

export interface AutomaticProcessResponse {
  run: RunSummary
  current: CurrentArtifactResponse
  auto_processed: number
  auto_processed_artifact_ids: string[]
  stopped_for_human: boolean
}

export interface NextArtifactResponse {
  run: RunSummary
  current: CurrentArtifactResponse
}

export interface CodingRecord {
  record_id: string
  artifact_id: string
  dataset_name: string
  batch_index: number
  codebook_version: number
  decision: HumanDecision
  pre_read_memo: string
  final_code_ids: string[]
  final_code_names: string[]
  rationale: string
  evidence_summary: string[]
  preserved_alternatives: string[]
  validation_signals: string[]
  notes: string[]
  metadata: Record<string, unknown>
}

export interface ArtifactRunTrace {
  artifact_id: string
  codebook_version_after_review?: number
  [key: string]: unknown
}

export interface RunHistory {
  coding_records: CodingRecord[]
  codebook_revisions: CodebookChange[]
  notes: string[]
  artifact_runs: ArtifactRunTrace[]
  codebook_versions: CodebookVersions
  retrospective_tasks: RetrospectiveTask[]
  context_requests?: ContextRequest[]
  analytic_memos?: AnalyticMemo[]
}

export type ContextRequestStatus = 'pending' | 'resolved' | 'cancelled'

export interface ContextRequest {
  request_id: string
  scope: 'artifact' | 'initial' | 'final'
  reason: string
  requested_items: string[]
  created_at_codebook_version: number
  artifact_id?: string | null
  status: ContextRequestStatus
  resolution: string
  supplied_context: string[]
  metadata: Record<string, unknown>
}

export type RetrospectiveTaskStatus = 'pending' | 'prepared' | 'awaiting_human' | 'completed' | 'cancelled'

export interface RetrospectiveTask {
  task_id: string
  artifact_id: string
  trigger_change_id: string
  from_codebook_version: number
  target_codebook_version: number
  status: RetrospectiveTaskStatus
  reason: string
  attempt_count: number
  metadata: Record<string, unknown>
}

export interface RetrospectiveTasksResponse {
  run_id: string
  tasks: RetrospectiveTask[]
  pending_count: number
}

export interface RetrospectiveReviewPacket extends ReviewPacket {
  review_kind: 'retrospective'
  task: RetrospectiveTask
}

export interface AutomaticRetrospectiveResult {
  auto_processed: true
  task: RetrospectiveTask
  artifact_id: string
  decision: string
  routing_decision: ReviewRoutingDecision
  codebook: Codebook
  run: RunSummary
}

export interface CheckpointOverview {
  format: string
  format_version: number
  run_id: string
  dataset_name: string
  status: RunStatus
  current_batch_index: number
  coding_batch_count: number
  review_count: number
  codebook_version: number
  code_count: number
}

export interface FinalCodebookFile {
  available: boolean
  snapshot: Codebook | null
}

export interface RunArtifacts {
  checkpoint: CheckpointOverview
  reviews: Array<Record<string, unknown>>
  artifact_runs: ArtifactRunTrace[]
  final_codebook: FinalCodebookFile
  bootstrap: BootstrapInspection | null
}

export interface BootstrapInspection {
  status: BootstrapProgressStatus
  error: string | null
  artifact_ids: string[]
  assignments: Array<{
    artifact_id: string
    code_ids: string[]
    evidence_summary: string[]
    status: string
  }>
  initial_codings?: InitialCodingRecord[]
  codebook: Codebook
  change_log: Array<{ action?: string; summary?: string }>
  analytic_memos?: Array<Record<string, unknown>>
  audit_warnings: string[]
  audit_warnings_zh?: string[]
  protocol: Record<string, unknown>
  progress?: BootstrapProgress
}
