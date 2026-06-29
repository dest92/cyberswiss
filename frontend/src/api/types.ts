export interface User {
  id: string
  email: string
  created_at: string
}

export interface AuthStatus {
  auth_disabled: boolean
  needs_setup: boolean
  user: User | null
}

export type EngagementStatus = 'active' | 'archived' | 'closed'

export interface Engagement {
  id: string
  name: string
  client_name: string | null
  status: EngagementStatus
  authorization_scope_doc: string | null
  start_date: string | null
  end_date: string | null
  created_at: string
  updated_at: string
}

export interface EngagementInput {
  name: string
  client_name?: string | null
  status?: EngagementStatus
  authorization_scope_doc?: string | null
  start_date?: string | null
  end_date?: string | null
}

export type ScopeType = 'domain' | 'ip_range' | 'url' | 'cidr'

export interface Scope {
  id: string
  engagement_id: string
  type: ScopeType
  value: string
  in_scope: boolean
}

export interface ScopeInput {
  type: ScopeType
  value: string
  in_scope?: boolean
}

export interface Note {
  id: string
  engagement_id: string
  content: string
  created_at: string
  updated_at: string
}

export type JobStatus = 'queued' | 'running' | 'success' | 'failed' | 'timeout'

export interface Job {
  id: string
  engagement_id: string
  pipeline_run_id: string | null
  step_index: number | null
  tool_name: string
  status: JobStatus
  params: Record<string, unknown>
  raw_output: string | null
  parsed_results: unknown[] | null
  container_id: string | null
  error_message: string | null
  created_at: string
  started_at: string | null
  finished_at: string | null
}

export interface JobInput {
  tool_name: string
  params: Record<string, unknown>
}

export type PipelineRunStatus = 'queued' | 'running' | 'success' | 'failed'

export interface PipelineRun {
  id: string
  engagement_id: string
  pipeline_name: string
  status: PipelineRunStatus
  params: Record<string, unknown>
  error_message: string | null
  created_at: string
  started_at: string | null
  finished_at: string | null
  jobs: Job[]
}

export interface PipelineRunInput {
  pipeline_name: string
  params: Record<string, unknown>
}

export type TargetType = 'host' | 'url'

export interface Target {
  id: string
  engagement_id: string
  type: TargetType
  value: string
  source_job_id: string | null
  discovered_at: string
}

export type FindingSeverity = 'critical' | 'high' | 'medium' | 'low' | 'info'
export type FindingStatus = 'open' | 'confirmed' | 'fixed' | 'false_positive'

export interface Finding {
  id: string
  engagement_id: string
  source_job_id: string | null
  title: string
  description: string | null
  owasp_category: string
  mitre_techniques: string[]
  severity: FindingSeverity
  cvss_score: number | null
  status: FindingStatus
  created_at: string
  updated_at: string
}

export interface FindingInput {
  title: string
  description?: string | null
  owasp_category: string
  mitre_techniques?: string[]
  severity: FindingSeverity
  cvss_score?: number | null
  status?: FindingStatus
  source_job_id?: string | null
}

export type KnowledgeDocumentType = 'markdown' | 'pdf'
export type KnowledgeDocumentStatus = 'ready' | 'processing' | 'failed'

export interface KnowledgeDocumentSummary {
  id: string
  title: string
  doc_type: KnowledgeDocumentType
  status: KnowledgeDocumentStatus
  owasp_categories: string[]
  is_seed: boolean
  created_at: string
  updated_at: string
}

export interface KnowledgeDocument extends KnowledgeDocumentSummary {
  content: string | null
  file_path: string | null
  error_message: string | null
}

export interface KnowledgeDocumentSearchResult extends KnowledgeDocumentSummary {
  snippet: string | null
  rank: number | null
}

export interface KnowledgeDocumentInput {
  title: string
  content: string
  owasp_categories: string[]
}

export type ReportFormat = 'markdown' | 'pdf'

export interface Report {
  id: string
  engagement_id: string
  format: ReportFormat
  created_at: string
}

export interface EngagementSummary {
  findings_by_severity: Record<string, number>
  findings_by_owasp_category: Record<string, number>
  jobs_by_status: Record<string, number>
  total_scopes: number
  total_targets: number
  total_notes: number
  total_reports: number
}

export interface ScheduledScan {
  id: string
  engagement_id: string
  tool_name: string
  params: Record<string, unknown>
  interval_minutes: number
  enabled: boolean
  next_run_at: string
  last_run_at: string | null
  created_at: string
}

export interface ScheduledScanInput {
  tool_name: string
  params: Record<string, unknown>
  interval_minutes: number
}
