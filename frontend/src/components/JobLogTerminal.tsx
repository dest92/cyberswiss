import { useEffect, useRef } from 'react'
import { useJobLogStream } from '@/hooks/useJobLogStream'

export function JobLogTerminal({ jobId }: { jobId: string }) {
  const { lines, connected } = useJobLogStream(jobId)
  const scrollRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const el = scrollRef.current
    if (el) el.scrollTop = el.scrollHeight
  }, [lines])

  return (
    <div className="rounded-md border border-border bg-black">
      <div className="flex items-center justify-between border-b border-border px-3 py-1.5">
        <span className="terminal text-xs text-muted">job logs</span>
        <span
          className={`terminal text-xs ${connected ? 'text-terminal-green' : 'text-muted'}`}
        >
          {connected ? '● live' : '○ closed'}
        </span>
      </div>
      <div ref={scrollRef} className="terminal h-64 overflow-y-auto p-3 text-xs text-terminal-green">
        {lines.length === 0 && <p className="text-muted">esperando salida...</p>}
        {lines.map((line, i) => (
          <div key={i} className="whitespace-pre-wrap">
            {line}
          </div>
        ))}
      </div>
    </div>
  )
}
