import type {
  Codebook,
  CodebookVersions,
  CodeArtifacts,
  CurrentArtifactResponse,
  Dataset,
  ReviewPacket,
  RunSummary,
  HeldOutMaterials,
  SubmitReviewRequest,
  SubmitReviewResponse,
  NextArtifactResponse,
  RunHistory,
  ContextRequest,
  RunArtifacts,
  ReviewMode,
  ExperimentVariant,
  AutomaticProcessResponse,
  RetrospectiveTask,
  RetrospectiveTasksResponse,
  RetrospectiveReviewPacket,
  AutomaticRetrospectiveResult,
  StageReviewPacket,
  StageReviewRequest,
} from './types'

// Vite embeds this public address in the bundle; it must never contain a key.
// An explicit empty string selects a same-origin /api reverse proxy.
const configuredApiUrl = import.meta.env.VITE_API_BASE_URL
const apiBaseUrl = (configuredApiUrl ?? (import.meta.env.DEV ? 'http://127.0.0.1:8003' : '')).trim().replace(/\/+$/, '')

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  let response: Response
  try {
    response = await fetch(`${apiBaseUrl}${path}`, {
      headers: { 'Content-Type': 'application/json', ...options?.headers },
      ...options,
    })
  } catch (error) {
    if (error instanceof DOMException && error.name === 'AbortError') throw error
    const detail = error instanceof Error ? error.message : 'Network request failed.'
    throw new Error(`无法连接 CODA 后端 ${apiBaseUrl || window.location.origin}：${detail}。请检查后端地址、HTTPS、跨域配置及服务状态。`)
  }
  if (!response.ok) {
    const payload = await response.json().catch(() => null)
    throw new Error(payload?.detail ?? `Request failed (${response.status})`)
  }
  return response.json() as Promise<T>
}

export const api = {
  listDatasets: () => request<Dataset[]>('/api/datasets'),
  listRuns: () => request<RunSummary[]>('/api/runs'),
  createRun: (datasetName: string, artifactLimit: number, reviewMode: ReviewMode, experimentVariant: ExperimentVariant, heldOutEnabled: boolean, heldOutSize: number, iterativeBatchSize: number = 1) =>
    request<RunSummary>('/api/runs', {
      method: 'POST',
      body: JSON.stringify({ dataset_name: datasetName, artifact_limit: artifactLimit, iterative_batch_size: iterativeBatchSize, review_mode: reviewMode, experiment_variant: experimentVariant, held_out_enabled: heldOutEnabled, held_out_size: heldOutEnabled ? heldOutSize : null }),
    }),
  initializeRun: (runId: string, language: 'en' | 'zh', signal?: AbortSignal) =>
    request<RunSummary>(`/api/runs/${runId}/initialize?language=${language}`, { method: 'POST', signal }),
  cancelInitialization: (runId: string) =>
    request<RunSummary>(`/api/runs/${runId}/initialize/cancel`, { method: 'POST' }),
  cancelInitializationOnUnload: (runId: string) => {
    if (!navigator.sendBeacon) return false
    return navigator.sendBeacon(`${apiBaseUrl}/api/runs/${runId}/initialize/cancel`, new Blob([], { type: 'application/json' }))
  },
  getStageReview: (runId: string, kind: 'initial' | 'final', inspection = false) =>
    request<StageReviewPacket>(`/api/runs/${runId}/stage-reviews/${kind}${inspection ? '?inspection=true' : ''}`),
  selectInitialReviewSetting: (runId: string, setting: ReviewMode, continueAutomatic = false) =>
    request<{ run: RunSummary; packet: StageReviewPacket | null }>(`/api/runs/${runId}/initial-review-setting`, {
      method: 'POST', body: JSON.stringify({ setting, continue_automatic: continueAutomatic }),
    }),
  submitStageReview: (runId: string, kind: 'initial' | 'final', review: StageReviewRequest) =>
    request<{ review: Record<string, unknown>; run: RunSummary }>(`/api/runs/${runId}/stage-reviews/${kind}`, {
      method: 'POST', body: JSON.stringify(review),
    }),
  recordReviewTimer: (runId: string, action: 'pause' | 'resume', scope: 'artifact' | 'initial' | 'triggered' | 'final' | 'rework', artifactId?: string) =>
    request<{ run: RunSummary; action: string; scope: string; artifact_id?: string }>('/api/runs/' + encodeURIComponent(runId) + '/review-timer', {
      method: 'POST',
      body: JSON.stringify({ action, scope, artifact_id: artifactId ?? null }),
    }),
  getRun: (runId: string) => request<RunSummary>(`/api/runs/${runId}`),
  getHeldOutMaterials: (runId: string) => request<HeldOutMaterials>(`/api/runs/${runId}/held-out-materials`),
  processAutomatic: (runId: string, language: 'en' | 'zh') =>
    request<AutomaticProcessResponse>(`/api/runs/${runId}/process-automatic?language=${language}`, { method: 'POST' }),
  deleteRun: (runId: string) => request<{ run_id: string; deleted: boolean }>(`/api/runs/${runId}`, { method: 'DELETE' }),
  getCurrentArtifact: (runId: string) =>
    request<CurrentArtifactResponse>(`/api/runs/${runId}/current-artifact`),
  prepareReview: (runId: string, language: 'en' | 'zh') =>
    request<ReviewPacket>(`/api/runs/${runId}/prepare-review?language=${language}`, { method: 'POST' }),
  getReviewPacket: (runId: string) =>
    request<ReviewPacket>(`/api/runs/${runId}/review-packet`),
  getCodebook: (runId: string) => request<Codebook>(`/api/runs/${runId}/codebook`),
  getCodebookVersions: (runId: string) => request<CodebookVersions>(`/api/runs/${runId}/codebook/versions`),
  getCodeArtifacts: (runId: string, codeId: string) =>
    request<CodeArtifacts>(`/api/runs/${runId}/codebook/${encodeURIComponent(codeId)}/artifacts`),
  getHistory: (runId: string) => request<RunHistory>(`/api/runs/${runId}/history`),
  updateAnalyticMemoStatus: (runId: string, memoId: string, status: 'open' | 'resolved', rationale: string) =>
    request<{ run_id: string; memo: import('./types').AnalyticMemo }>(`/api/runs/${runId}/analytic-memos/${encodeURIComponent(memoId)}/status`, {
      method: 'POST', body: JSON.stringify({ status, rationale }),
    }),
  getContextRequests: (runId: string) => request<{ run_id: string; requests: ContextRequest[]; pending_count: number }>(`/api/runs/${runId}/context-requests`),
  resolveContextRequest: (runId: string, requestId: string, suppliedContext: string[], resolution: string) =>
    request<{ run_id: string; requests: ContextRequest[]; pending_count: number }>(`/api/runs/${runId}/context-requests/${encodeURIComponent(requestId)}/resolve`, {
      method: 'POST', body: JSON.stringify({ supplied_context: suppliedContext, resolution }),
    }),
  cancelContextRequest: (runId: string, requestId: string) =>
    request<{ run_id: string; requests: ContextRequest[]; pending_count: number }>(`/api/runs/${runId}/context-requests/${encodeURIComponent(requestId)}/cancel`, { method: 'POST' }),
  getRunArtifacts: (runId: string) => request<RunArtifacts>(`/api/runs/${runId}/artifacts`),
  getRetrospectiveTasks: (runId: string) => request<RetrospectiveTasksResponse>(`/api/runs/${runId}/retrospective-tasks`),
  prepareRetrospectiveTask: (runId: string, taskId: string, language: 'en' | 'zh') =>
    request<RetrospectiveReviewPacket | AutomaticRetrospectiveResult>(`/api/runs/${runId}/retrospective-tasks/${encodeURIComponent(taskId)}/prepare?language=${language}`, { method: 'POST' }),
  submitRetrospectiveReview: (runId: string, taskId: string, review: SubmitReviewRequest) =>
    request<{ task: RetrospectiveTask; artifact_id: string; decision: string; codebook: Codebook; run: RunSummary }>(`/api/runs/${runId}/retrospective-tasks/${encodeURIComponent(taskId)}/submit`, {
      method: 'POST', body: JSON.stringify(review),
    }),
  submitReview: (runId: string, review: SubmitReviewRequest) =>
    request<SubmitReviewResponse>(`/api/runs/${runId}/submit-review`, {
      method: 'POST',
      body: JSON.stringify(review),
    }),
  nextArtifact: (runId: string) =>
    request<NextArtifactResponse>(`/api/runs/${runId}/next-artifact`, { method: 'POST' }),
}
