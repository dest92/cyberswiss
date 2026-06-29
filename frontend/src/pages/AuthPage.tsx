import { useState } from 'react'
import { Navigate } from 'react-router-dom'
import { useMutation } from '@tanstack/react-query'
import { useAuth } from '@/context/AuthContext'
import { setup, login } from '@/api/auth'
import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'

export function AuthPage() {
  const { status, isLoading, refresh } = useAuth()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')

  const mutation = useMutation({
    mutationFn: () => (status?.needs_setup ? setup(email, password) : login(email, password)),
    onSuccess: refresh,
  })

  if (isLoading) {
    return <div className="terminal min-h-screen bg-background p-6 text-muted">cargando...</div>
  }

  if (status?.auth_disabled || status?.user) {
    return <Navigate to="/" replace />
  }

  const isSetup = status?.needs_setup

  return (
    <div className="flex min-h-screen items-center justify-center bg-background px-6">
      <form
        className="w-full max-w-sm rounded-md border border-border bg-surface p-6"
        onSubmit={(e) => {
          e.preventDefault()
          mutation.mutate()
        }}
      >
        <h1 className="terminal mb-1 text-accent text-lg">cyberswiss</h1>
        <p className="mb-6 text-sm text-muted">
          {isSetup ? 'Crear el usuario único de esta instancia.' : 'Iniciar sesión.'}
        </p>

        <div className="mb-3">
          <label className="mb-1 block text-xs text-muted">email</label>
          <Input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            autoFocus
          />
        </div>
        <div className="mb-4">
          <label className="mb-1 block text-xs text-muted">password</label>
          <Input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            minLength={8}
          />
        </div>

        {mutation.isError && (
          <p className="mb-3 text-xs text-severity-critical">
            {isSetup ? 'No se pudo crear el usuario.' : 'Credenciales inválidas.'}
          </p>
        )}

        <Button type="submit" className="w-full" disabled={mutation.isPending}>
          {isSetup ? 'crear usuario' : 'entrar'}
        </Button>
      </form>
    </div>
  )
}
