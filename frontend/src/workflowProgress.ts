import type { RunSummary } from './types'

export function bootstrapNodeForRun(run: RunSummary) {
  const progress = run.bootstrap_progress
  const nodes: Record<string, string> = {
    evidence: 'context',
    initial_coding: 'coding',
    induction: 'induction',
    codebook: 'induction',
    assignment: 'induction',
    validation: 'initial_validation',
    audit: 'initial_validation',
    reinduction: 'induction',
    reassignment: 'induction',
    revalidation: 'initial_validation',
  }
  if (run.bootstrap_status === 'not_run') return 'context'
  if (nodes[progress?.phase]) return nodes[progress.phase]
  // Pausing or failing replaces the phase name, but retains the stage index.
  const stage = progress?.stage_index ?? 0
  if (stage === 2) return 'coding'
  if ([3, 4, 6, 7].includes(stage)) return 'induction'
  if ([5, 8].includes(stage)) return 'initial_validation'
  return 'context'
}

export function currentNodeForRun(run: RunSummary | null) {
  if (!run) return 'input'
  if (['not_run', 'running', 'cancelling', 'failed', 'cancelled', 'interrupted'].includes(run.bootstrap_status)) return bootstrapNodeForRun(run)
  if (run.status === 'awaiting_initial_review') return 'initial_review'
  if (run.status === 'awaiting_final_review') return 'final_review'
  if (run.status === 'awaiting_human_review' || run.awaiting_next_artifact || run.awaiting_context) return 'triggered_review'
  if (['completed', 'stabilized', 'completed_with_unresolved'].includes(run.status)) return 'final'
  return 'iterative_context'
}

export function bootstrapStatusLabelKey(run: RunSummary | null): string | null {
  switch (run?.bootstrap_status) {
    case 'running': return 'initializingTask'
    case 'cancelling': return 'stoppingInitialization'
    case 'cancelled': return 'bootstrapPhaseCancelled'
    case 'interrupted': return 'bootstrapPhaseInterrupted'
    case 'failed': return 'bootstrapPhaseFailed'
    default: return null
  }
}
