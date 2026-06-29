import { cn } from '@/lib/utils'
import type { EngagementStatus } from '@/api/types'

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
