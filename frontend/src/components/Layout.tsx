import { Link, Outlet, Navigate } from 'react-router-dom'
import { useMutation } from '@tanstack/react-query'
import { useAuth } from '@/context/AuthContext'
import { logout as logoutRequest } from '@/api/auth'
import { Button } from '@/components/ui/Button'

export function Layout() {
  const { status, isLoading, refresh } = useAuth()

  const logoutMutation = useMutation({
    mutationFn: logoutRequest,
    onSuccess: refresh,
  })

  if (isLoading) {
    return <div className="terminal min-h-screen bg-background p-6 text-muted">cargando...</div>
  }

  if (status?.needs_setup || (!status?.auth_disabled && !status?.user)) {
    return <Navigate to="/auth" replace />
  }

  return (
    <div className="min-h-screen bg-background text-foreground">
      <header className="flex items-center justify-between border-b border-border px-6 py-3">
        <Link to="/" className="terminal text-accent text-sm font-semibold">
          cyberswiss
        </Link>
        <div className="flex items-center gap-4 text-sm">
          {status?.user && <span className="text-muted">{status.user.email}</span>}
          {!status?.auth_disabled && (
            <Button variant="ghost" onClick={() => logoutMutation.mutate()}>
              logout
            </Button>
          )}
        </div>
      </header>
      <main className="mx-auto max-w-5xl px-6 py-8">
        <Outlet />
      </main>
    </div>
  )
}
