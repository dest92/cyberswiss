import { apiClient } from '@/lib/api'
import type { Scope, ScopeInput } from './types'

export async function listScopes(engagementId: string): Promise<Scope[]> {
  const { data } = await apiClient.get<Scope[]>(`/api/engagements/${engagementId}/scopes`)
  return data
}

export async function createScope(engagementId: string, payload: ScopeInput): Promise<Scope> {
  const { data } = await apiClient.post<Scope>(`/api/engagements/${engagementId}/scopes`, payload)
  return data
}

export async function updateScope(
  engagementId: string,
  scopeId: string,
  payload: Partial<ScopeInput>,
): Promise<Scope> {
  const { data } = await apiClient.patch<Scope>(
    `/api/engagements/${engagementId}/scopes/${scopeId}`,
    payload,
  )
  return data
}

export async function deleteScope(engagementId: string, scopeId: string): Promise<void> {
  await apiClient.delete(`/api/engagements/${engagementId}/scopes/${scopeId}`)
}
