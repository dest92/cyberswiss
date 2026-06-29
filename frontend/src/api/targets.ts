import { apiClient } from '@/lib/api'
import type { Target } from './types'

export async function listTargets(engagementId: string): Promise<Target[]> {
  const { data } = await apiClient.get<Target[]>(`/api/engagements/${engagementId}/targets`)
  return data
}
