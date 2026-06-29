import { apiClient } from '@/lib/api'
import type {
  KnowledgeDocument,
  KnowledgeDocumentInput,
  KnowledgeDocumentSearchResult,
  KnowledgeDocumentSummary,
} from './types'

export async function listKnowledgeDocuments(
  owaspCategory?: string,
): Promise<KnowledgeDocumentSummary[]> {
  const { data } = await apiClient.get<KnowledgeDocumentSummary[]>('/api/knowledge', {
    params: owaspCategory ? { owasp_category: owaspCategory } : undefined,
  })
  return data
}

export async function searchKnowledgeDocuments(
  query: string,
): Promise<KnowledgeDocumentSearchResult[]> {
  const { data } = await apiClient.get<KnowledgeDocumentSearchResult[]>('/api/knowledge/search', {
    params: { q: query },
  })
  return data
}

export async function getKnowledgeDocument(documentId: string): Promise<KnowledgeDocument> {
  const { data } = await apiClient.get<KnowledgeDocument>(`/api/knowledge/${documentId}`)
  return data
}

export async function createKnowledgeDocument(
  payload: KnowledgeDocumentInput,
): Promise<KnowledgeDocument> {
  const { data } = await apiClient.post<KnowledgeDocument>('/api/knowledge', payload)
  return data
}

export async function uploadKnowledgeDocument(
  title: string,
  owaspCategories: string[],
  file: File,
): Promise<KnowledgeDocument> {
  const form = new FormData()
  form.append('title', title)
  form.append('owasp_categories', owaspCategories.join(','))
  form.append('file', file)
  const { data } = await apiClient.post<KnowledgeDocument>('/api/knowledge/upload', form, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
  return data
}

export async function deleteKnowledgeDocument(documentId: string): Promise<void> {
  await apiClient.delete(`/api/knowledge/${documentId}`)
}
