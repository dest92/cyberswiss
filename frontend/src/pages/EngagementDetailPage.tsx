import { useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { deleteEngagement, getEngagement, updateEngagement } from '@/api/engagements'
import { createScope, deleteScope, listScopes, updateScope } from '@/api/scopes'
import { createNote, deleteNote, listNotes, updateNote } from '@/api/notes'
import { Button } from '@/components/ui/Button'
import { Input, Textarea } from '@/components/ui/Input'
import { StatusBadge } from '@/components/ui/Badge'
import type { EngagementStatus, ScopeType } from '@/api/types'

const SCOPE_TYPES: ScopeType[] = ['domain', 'ip_range', 'url', 'cidr']
const STATUSES: EngagementStatus[] = ['active', 'archived', 'closed']

export function EngagementDetailPage() {
  const { id } = useParams<{ id: string }>()
  const engagementId = id!
  const navigate = useNavigate()
  const queryClient = useQueryClient()

  const { data: engagement } = useQuery({
    queryKey: ['engagements', engagementId],
    queryFn: () => getEngagement(engagementId),
  })

  const { data: scopes } = useQuery({
    queryKey: ['engagements', engagementId, 'scopes'],
    queryFn: () => listScopes(engagementId),
  })

  const { data: notes } = useQuery({
    queryKey: ['engagements', engagementId, 'notes'],
    queryFn: () => listNotes(engagementId),
  })

  const invalidateEngagement = () =>
    queryClient.invalidateQueries({ queryKey: ['engagements', engagementId] })
  const invalidateScopes = () =>
    queryClient.invalidateQueries({ queryKey: ['engagements', engagementId, 'scopes'] })
  const invalidateNotes = () =>
    queryClient.invalidateQueries({ queryKey: ['engagements', engagementId, 'notes'] })

  const statusMutation = useMutation({
    mutationFn: (status: EngagementStatus) => updateEngagement(engagementId, { status }),
    onSuccess: invalidateEngagement,
  })

  const deleteEngagementMutation = useMutation({
    mutationFn: () => deleteEngagement(engagementId),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ['engagements'] })
      navigate('/')
    },
  })

  const [scopeValue, setScopeValue] = useState('')
  const [scopeType, setScopeType] = useState<ScopeType>('domain')
  const addScopeMutation = useMutation({
    mutationFn: () => createScope(engagementId, { type: scopeType, value: scopeValue }),
    onSuccess: () => {
      setScopeValue('')
      invalidateScopes()
    },
  })
  const toggleScopeMutation = useMutation({
    mutationFn: (vars: { scopeId: string; in_scope: boolean }) =>
      updateScope(engagementId, vars.scopeId, { in_scope: vars.in_scope }),
    onSuccess: invalidateScopes,
  })
  const deleteScopeMutation = useMutation({
    mutationFn: (scopeId: string) => deleteScope(engagementId, scopeId),
    onSuccess: invalidateScopes,
  })

  const [noteContent, setNoteContent] = useState('')
  const addNoteMutation = useMutation({
    mutationFn: () => createNote(engagementId, noteContent),
    onSuccess: () => {
      setNoteContent('')
      invalidateNotes()
    },
  })
  const deleteNoteMutation = useMutation({
    mutationFn: (noteId: string) => deleteNote(engagementId, noteId),
    onSuccess: invalidateNotes,
  })
  const [editingNoteId, setEditingNoteId] = useState<string | null>(null)
  const [editingNoteContent, setEditingNoteContent] = useState('')
  const editNoteMutation = useMutation({
    mutationFn: (vars: { noteId: string; content: string }) =>
      updateNote(engagementId, vars.noteId, vars.content),
    onSuccess: () => {
      setEditingNoteId(null)
      invalidateNotes()
    },
  })

  if (!engagement) {
    return <p className="text-sm text-muted">cargando...</p>
  }

  return (
    <div className="flex flex-col gap-8">
      <section>
        <div className="mb-2 flex items-center justify-between">
          <h1 className="terminal text-lg text-foreground">{engagement.name}</h1>
          <div className="flex items-center gap-2">
            <StatusBadge status={engagement.status} />
            <Button
              variant="danger"
              onClick={() => {
                if (confirm('¿Eliminar este engagement y todo su contenido?')) {
                  deleteEngagementMutation.mutate()
                }
              }}
            >
              eliminar
            </Button>
          </div>
        </div>
        {engagement.client_name && (
          <p className="mb-2 text-sm text-muted">cliente: {engagement.client_name}</p>
        )}
        {engagement.authorization_scope_doc && (
          <p className="terminal mb-3 whitespace-pre-wrap rounded-md border border-border bg-surface p-3 text-xs text-foreground">
            {engagement.authorization_scope_doc}
          </p>
        )}
        <div className="flex gap-2">
          {STATUSES.map((s) => (
            <Button
              key={s}
              variant={s === engagement.status ? 'primary' : 'secondary'}
              onClick={() => statusMutation.mutate(s)}
              disabled={statusMutation.isPending}
            >
              {s}
            </Button>
          ))}
        </div>
      </section>

      <section>
        <h2 className="terminal mb-3 text-sm text-accent">scope</h2>
        <form
          className="mb-4 flex gap-2"
          onSubmit={(e) => {
            e.preventDefault()
            if (scopeValue.trim()) addScopeMutation.mutate()
          }}
        >
          <select
            className="terminal rounded-md border border-border bg-surface px-2 py-1.5 text-sm text-foreground"
            value={scopeType}
            onChange={(e) => setScopeType(e.target.value as ScopeType)}
          >
            {SCOPE_TYPES.map((t) => (
              <option key={t} value={t}>
                {t}
              </option>
            ))}
          </select>
          <Input
            placeholder="ej. acme.com, 10.0.0.0/24"
            value={scopeValue}
            onChange={(e) => setScopeValue(e.target.value)}
          />
          <Button type="submit" disabled={addScopeMutation.isPending}>
            agregar
          </Button>
        </form>

        <div className="flex flex-col gap-1.5">
          {scopes?.map((scope) => (
            <div
              key={scope.id}
              className="flex items-center justify-between rounded-md border border-border bg-surface px-3 py-2"
            >
              <div className="flex items-center gap-3">
                <span className="terminal text-xs text-muted">{scope.type}</span>
                <span className="terminal text-sm text-foreground">{scope.value}</span>
                <span
                  className={
                    scope.in_scope
                      ? 'terminal text-xs text-terminal-green'
                      : 'terminal text-xs text-severity-critical'
                  }
                >
                  {scope.in_scope ? 'in-scope' : 'out-of-scope'}
                </span>
              </div>
              <div className="flex gap-2">
                <Button
                  variant="secondary"
                  onClick={() =>
                    toggleScopeMutation.mutate({ scopeId: scope.id, in_scope: !scope.in_scope })
                  }
                >
                  toggle
                </Button>
                <Button variant="danger" onClick={() => deleteScopeMutation.mutate(scope.id)}>
                  eliminar
                </Button>
              </div>
            </div>
          ))}
          {scopes && scopes.length === 0 && (
            <p className="text-sm text-muted">No hay scope definido.</p>
          )}
        </div>
      </section>

      <section>
        <h2 className="terminal mb-3 text-sm text-accent">notas</h2>
        <form
          className="mb-4 flex gap-2"
          onSubmit={(e) => {
            e.preventDefault()
            if (noteContent.trim()) addNoteMutation.mutate()
          }}
        >
          <Textarea
            placeholder="Agregar una nota..."
            value={noteContent}
            onChange={(e) => setNoteContent(e.target.value)}
            rows={2}
          />
          <Button type="submit" disabled={addNoteMutation.isPending}>
            agregar
          </Button>
        </form>

        <div className="flex flex-col gap-2">
          {notes?.map((note) => (
            <div key={note.id} className="rounded-md border border-border bg-surface p-3">
              {editingNoteId === note.id ? (
                <div className="flex flex-col gap-2">
                  <Textarea
                    value={editingNoteContent}
                    onChange={(e) => setEditingNoteContent(e.target.value)}
                    rows={3}
                  />
                  <div className="flex gap-2">
                    <Button
                      onClick={() =>
                        editNoteMutation.mutate({ noteId: note.id, content: editingNoteContent })
                      }
                    >
                      guardar
                    </Button>
                    <Button variant="secondary" onClick={() => setEditingNoteId(null)}>
                      cancelar
                    </Button>
                  </div>
                </div>
              ) : (
                <>
                  <p className="whitespace-pre-wrap text-sm text-foreground">{note.content}</p>
                  <div className="mt-2 flex items-center justify-between">
                    <span className="text-xs text-muted">
                      {new Date(note.created_at).toLocaleString()}
                    </span>
                    <div className="flex gap-2">
                      <Button
                        variant="secondary"
                        onClick={() => {
                          setEditingNoteId(note.id)
                          setEditingNoteContent(note.content)
                        }}
                      >
                        editar
                      </Button>
                      <Button variant="danger" onClick={() => deleteNoteMutation.mutate(note.id)}>
                        eliminar
                      </Button>
                    </div>
                  </div>
                </>
              )}
            </div>
          ))}
          {notes && notes.length === 0 && <p className="text-sm text-muted">Sin notas aún.</p>}
        </div>
      </section>
    </div>
  )
}
