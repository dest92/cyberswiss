import { apiClient } from '@/lib/api'
import type { PipelineRun, PipelineRunInput } from './types'

export async function listPipelineDefinitions(): Promise<string[]> {
  const { data } = await apiClient.get<string[]>('/api/pipelines')
  return data
}

export async function listPipelineRuns(engagementId: string): Promise<PipelineRun[]> {
  const { data } = await apiClient.get<PipelineRun[]>(
    `/api/engagements/${engagementId}/pipeline-runs`,
  )
  return data
}

export async function createPipelineRun(
  engagementId: string,
  payload: PipelineRunInput,
): Promise<PipelineRun> {
  const { data } = await apiClient.post<PipelineRun>(
    `/api/engagements/${engagementId}/pipeline-runs`,
    payload,
  )
  return data
}
