import { apiClient } from '@/lib/api'
import type { AuthStatus, User } from './types'

export async function fetchAuthStatus(): Promise<AuthStatus> {
  const { data } = await apiClient.get<AuthStatus>('/api/auth/status')
  return data
}

export async function setup(email: string, password: string): Promise<User> {
  const { data } = await apiClient.post<User>('/api/auth/setup', { email, password })
  return data
}

export async function login(email: string, password: string): Promise<User> {
  const { data } = await apiClient.post<User>('/api/auth/login', { email, password })
  return data
}

export async function logout(): Promise<void> {
  await apiClient.post('/api/auth/logout')
}
