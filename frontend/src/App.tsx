import { useQuery } from '@tanstack/react-query'
import { apiClient } from '@/lib/api'

function useHealth() {
  return useQuery({
    queryKey: ['health'],
    queryFn: async () => {
      const { data } = await apiClient.get<{ status: string }>('/health')
      return data
    },
    retry: false,
  })
}

function App() {
  const { data, isLoading, isError } = useHealth()

  const backendStatus = isLoading
    ? 'checking...'
    : isError
      ? 'unreachable'
      : data?.status ?? 'unknown'

  const statusColor = isError
    ? 'text-severity-critical'
    : data?.status === 'ok'
      ? 'text-terminal-green'
      : 'text-muted'

  return (
    <div className="flex min-h-screen flex-col items-center justify-center gap-6 bg-background px-6 text-foreground">
      <pre className="terminal text-accent text-sm leading-tight">
{`  ____      _                                _
 / ___|   _| |__   ___ _ __ _____      _(_)___ ___
| |  | | | | '_ \\ / _ \\ '__/ _ \\ \\ /\\ / / / __/ __|
| |__| |_| | |_) |  __/ | |  __/\\ V  V /| \\__ \\__ \\
 \\____\\__, |_.__/ \\___|_|  \\___| \\_/\\_/ |_|___/___/
      |___/                                              `}
      </pre>

      <div className="terminal rounded-md border border-border bg-surface px-6 py-4 text-sm">
        <span className="text-muted">$ </span>
        <span>curl {`{`}backend{`}`}/health</span>
        <div className="mt-2">
          backend:{' '}
          <span className={statusColor}>{backendStatus}</span>
        </div>
      </div>

      <p className="terminal max-w-md text-center text-xs text-muted">
        Suite de pentesting / red team self-hosted. Fase 0 — bootstrap completo.
      </p>
    </div>
  )
}

export default App
