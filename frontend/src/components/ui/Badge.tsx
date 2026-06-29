import { cn } from '@/lib/utils'
import type {
  EngagementStatus,
  FindingSeverity,
  FindingStatus,
  JobStatus,
  PipelineRunStatus,
} from '@/api/types'

const statusClasses: Record<EngagementStatus, string> = {
  active: 'text-terminal-green border-terminal-green/40 bg-terminal-green/10',
  archived: 'text-severity-medium border-severity-medium/40 bg-severity-medium/10',
  closed: 'text-muted border-border bg-surface-elevated',
}

export function StatusBadge({ status }: { status: EngagementStatus }) {
  return (
    <span
      className={cn(
        'terminal rounded border px-2 py-0.5 text-xs uppercase tracking-wide',
        statusClasses[status],
      )}
    >
      {status}
    </span>
  )
}

const jobStatusClasses: Record<JobStatus, string> = {
  queued: 'text-muted border-border bg-surface-elevated',
  running: 'text-accent border-accent/40 bg-accent/10',
  success: 'text-terminal-green border-terminal-green/40 bg-terminal-green/10',
  failed: 'text-severity-critical border-severity-critical/40 bg-severity-critical/10',
  timeout: 'text-severity-medium border-severity-medium/40 bg-severity-medium/10',
}

export function JobStatusBadge({ status }: { status: JobStatus }) {
  return (
    <span
      className={cn(
        'terminal rounded border px-2 py-0.5 text-xs uppercase tracking-wide',
        jobStatusClasses[status],
      )}
    >
      {status}
    </span>
  )
}

const pipelineRunStatusClasses: Record<PipelineRunStatus, string> = {
  queued: 'text-muted border-border bg-surface-elevated',
  running: 'text-accent border-accent/40 bg-accent/10',
  success: 'text-terminal-green border-terminal-green/40 bg-terminal-green/10',
  failed: 'text-severity-critical border-severity-critical/40 bg-severity-critical/10',
}

export function PipelineRunStatusBadge({ status }: { status: PipelineRunStatus }) {
  return (
    <span
      className={cn(
        'terminal rounded border px-2 py-0.5 text-xs uppercase tracking-wide',
        pipelineRunStatusClasses[status],
      )}
    >
      {status}
    </span>
  )
}

const severityClasses: Record<FindingSeverity, string> = {
  critical: 'text-severity-critical border-severity-critical/40 bg-severity-critical/10',
  high: 'text-severity-high border-severity-high/40 bg-severity-high/10',
  medium: 'text-severity-medium border-severity-medium/40 bg-severity-medium/10',
  low: 'text-severity-low border-severity-low/40 bg-severity-low/10',
  info: 'text-severity-info border-severity-info/40 bg-severity-info/10',
}

export function SeverityBadge({ severity }: { severity: FindingSeverity }) {
  return (
    <span
      className={cn(
        'terminal rounded border px-2 py-0.5 text-xs uppercase tracking-wide',
        severityClasses[severity],
      )}
    >
      {severity}
    </span>
  )
}

const findingStatusClasses: Record<FindingStatus, string> = {
  open: 'text-accent border-accent/40 bg-accent/10',
  confirmed: 'text-severity-high border-severity-high/40 bg-severity-high/10',
  fixed: 'text-terminal-green border-terminal-green/40 bg-terminal-green/10',
  false_positive: 'text-muted border-border bg-surface-elevated',
}

export function FindingStatusBadge({ status }: { status: FindingStatus }) {
  return (
    <span
      className={cn(
        'terminal rounded border px-2 py-0.5 text-xs uppercase tracking-wide',
        findingStatusClasses[status],
      )}
    >
      {status.replace('_', ' ')}
    </span>
  )
}
