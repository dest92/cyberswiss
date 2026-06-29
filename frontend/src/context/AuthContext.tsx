import { createContext, useContext, type ReactNode } from 'react'
import { useQuery, useQueryClient } from '@tanstack/react-query'
import { fetchAuthStatus } from '@/api/auth'
import type { AuthStatus } from '@/api/types'

interface AuthContextValue {
  status: AuthStatus | undefined
  isLoading: boolean
  refresh: () => void
}

const AuthContext = createContext<AuthContextValue | null>(null)

export function AuthProvider({ children }: { children: ReactNode }) {
  const queryClient = useQueryClient()
  const { data, isLoading } = useQuery({
    queryKey: ['auth-status'],
    queryFn: fetchAuthStatus,
  })

  const refresh = () => {
    void queryClient.invalidateQueries({ queryKey: ['auth-status'] })
  }

  return (
    <AuthContext.Provider value={{ status: data, isLoading, refresh }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth debe usarse dentro de AuthProvider')
  return ctx
}
