import { apiClient } from '@/lib/api'
import type { Finding, FindingInput } from './types'

export async function listFindings(engagementId: string): Promise<Finding[]> {
  const { data } = await apiClient.get<Finding[]>(`/api/engagements/${engagementId}/findings`)
  return data
}

export async function createFinding(
  engagementId: string,
  payload: FindingInput,
): Promise<Finding> {
  const { data } = await apiClient.post<Finding>(
    `/api/engagements/${engagementId}/findings`,
    payload,
  )
  return data
}

export async function updateFinding(
  engagementId: string,
  findingId: string,
  payload: Partial<FindingInput>,
): Promise<Finding> {
  const { data } = await apiClient.patch<Finding>(
    `/api/engagements/${engagementId}/findings/${findingId}`,
    payload,
  )
  return data
}

export async function deleteFinding(engagementId: string, findingId: string): Promise<void> {
  await apiClient.delete(`/api/engagements/${engagementId}/findings/${findingId}`)
}
