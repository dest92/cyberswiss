import { apiClient } from '@/lib/api'
import type { Report, ReportFormat } from './types'

export async function listReports(engagementId: string): Promise<Report[]> {
  const { data } = await apiClient.get<Report[]>(`/api/engagements/${engagementId}/reports`)
  return data
}

export async function createReport(engagementId: string, format: ReportFormat): Promise<Report> {
  const { data } = await apiClient.post<Report>(`/api/engagements/${engagementId}/reports`, {
    format,
  })
  return data
}

export async function deleteReport(engagementId: string, reportId: string): Promise<void> {
  await apiClient.delete(`/api/engagements/${engagementId}/reports/${reportId}`)
}

export async function downloadReport(
  engagementId: string,
  report: Report,
): Promise<void> {
  const { data } = await apiClient.get<Blob>(
    `/api/engagements/${engagementId}/reports/${report.id}/download`,
    { responseType: 'blob' },
  )
  const extension = report.format === 'markdown' ? 'md' : 'pdf'
  const url = window.URL.createObjectURL(data)
  const link = document.createElement('a')
  link.href = url
  link.download = `reporte-${engagementId}.${extension}`
  document.body.appendChild(link)
  link.click()
  link.remove()
  window.URL.revokeObjectURL(url)
}
