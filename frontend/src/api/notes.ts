import { apiClient } from '@/lib/api'
import type { Note } from './types'

export async function listNotes(engagementId: string): Promise<Note[]> {
  const { data } = await apiClient.get<Note[]>(`/api/engagements/${engagementId}/notes`)
  return data
}

export async function createNote(engagementId: string, content: string): Promise<Note> {
  const { data } = await apiClient.post<Note>(`/api/engagements/${engagementId}/notes`, {
    content,
  })
  return data
}

export async function updateNote(
  engagementId: string,
  noteId: string,
  content: string,
): Promise<Note> {
  const { data } = await apiClient.patch<Note>(
    `/api/engagements/${engagementId}/notes/${noteId}`,
    { content },
  )
  return data
}

export async function deleteNote(engagementId: string, noteId: string): Promise<void> {
  await apiClient.delete(`/api/engagements/${engagementId}/notes/${noteId}`)
}
