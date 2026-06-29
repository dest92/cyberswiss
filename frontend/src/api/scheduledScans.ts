import { apiClient } from '@/lib/api'
import type { ScheduledScan, ScheduledScanInput } from './types'

export async function listScheduledScans(engagementId: string): Promise<ScheduledScan[]> {
  const { data } = await apiClient.get<ScheduledScan[]>(
    `/api/engagements/${engagementId}/scheduled-scans`,
  )
  return data
}

export async function createScheduledScan(
  engagementId: string,
  payload: ScheduledScanInput,
): Promise<ScheduledScan> {
  const { data } = await apiClient.post<ScheduledScan>(
    `/api/engagements/${engagementId}/scheduled-scans`,
    payload,
  )
  return data
}

export async function toggleScheduledScan(
  engagementId: string,
  scheduledScanId: string,
  enabled: boolean,
): Promise<ScheduledScan> {
  const { data } = await apiClient.patch<ScheduledScan>(
    `/api/engagements/${engagementId}/scheduled-scans/${scheduledScanId}`,
    { enabled },
  )
  return data
}

export async function deleteScheduledScan(
  engagementId: string,
  scheduledScanId: string,
): Promise<void> {
  await apiClient.delete(`/api/engagements/${engagementId}/scheduled-scans/${scheduledScanId}`)
}
