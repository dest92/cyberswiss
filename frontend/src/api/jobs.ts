import { apiClient } from '@/lib/api'
import type { Job, JobInput } from './types'

export async function listJobs(engagementId: string): Promise<Job[]> {
  const { data } = await apiClient.get<Job[]>(`/api/engagements/${engagementId}/jobs`)
  return data
}

export async function getJob(engagementId: string, jobId: string): Promise<Job> {
  const { data } = await apiClient.get<Job>(`/api/engagements/${engagementId}/jobs/${jobId}`)
  return data
}

export async function createJob(engagementId: string, payload: JobInput): Promise<Job> {
  const { data } = await apiClient.post<Job>(`/api/engagements/${engagementId}/jobs`, payload)
  return data
}

export async function listTools(): Promise<string[]> {
  const { data } = await apiClient.get<string[]>('/api/tools')
  return data
}
