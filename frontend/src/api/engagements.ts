import { apiClient } from '@/lib/api'
import type { Engagement, EngagementInput } from './types'

export async function listEngagements(): Promise<Engagement[]> {
  const { data } = await apiClient.get<Engagement[]>('/api/engagements')
  return data
}

export async function getEngagement(id: string): Promise<Engagement> {
  const { data } = await apiClient.get<Engagement>(`/api/engagements/${id}`)
  return data
}

export async function createEngagement(payload: EngagementInput): Promise<Engagement> {
  const { data } = await apiClient.post<Engagement>('/api/engagements', payload)
  return data
}

export async function updateEngagement(
  id: string,
  payload: Partial<EngagementInput>,
): Promise<Engagement> {
  const { data } = await apiClient.patch<Engagement>(`/api/engagements/${id}`, payload)
  return data
}

export async function deleteEngagement(id: string): Promise<void> {
  await apiClient.delete(`/api/engagements/${id}`)
}
