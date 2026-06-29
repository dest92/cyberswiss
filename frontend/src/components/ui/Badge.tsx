import { cn } from '@/lib/utils'
import type { EngagementStatus, JobStatus } from '@/api/types'

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
