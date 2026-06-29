import { useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { deleteEngagement, getEngagement, updateEngagement } from '@/api/engagements'
import { createScope, deleteScope, listScopes, updateScope } from '@/api/scopes'
import { createNote, deleteNote, listNotes, updateNote } from '@/api/notes'
import { createJob, listJobs, listTools } from '@/api/jobs'
import { listTargets } from '@/api/targets'
import { createPipelineRun, listPipelineDefinitions, listPipelineRuns } from '@/api/pipelines'
import { Button } from '@/components/ui/Button'
import { Input, Textarea } from '@/components/ui/Input'
import { StatusBadge, JobStatusBadge, PipelineRunStatusBadge } from '@/components/ui/Badge'
import { JobLogTerminal } from '@/components/JobLogTerminal'
import type { EngagementStatus, ScopeType } from '@/api/types'

const SCOPE_TYPES: ScopeType[] = ['domain', 'ip_range', 'url', 'cidr']
const STATUSES: EngagementStatus[] = ['active', 'archived', 'closed']
const ACTIVE_JOB_STATUSES = new Set(['queued', 'running'])
const ACTIVE_RUN_STATUSES = new Set(['queued', 'running'])
const PIPELINE_PARAM_KEY: Record<string, string> = { recon_chain: 'domain', web_audit: 'url' }

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

  const { data: tools } = useQuery({ queryKey: ['tools'], queryFn: listTools })

  const { data: jobs } = useQuery({
    queryKey: ['engagements', engagementId, 'jobs'],
    queryFn: () => listJobs(engagementId),
    refetchInterval: (query) => {
      const data = query.state.data
      return data?.some((job) => ACTIVE_JOB_STATUSES.has(job.status)) ? 2000 : false
    },
  })

  const { data: targets } = useQuery({
    queryKey: ['engagements', engagementId, 'targets'],
    queryFn: () => listTargets(engagementId),
  })

  const invalidateJobs = () =>
    queryClient.invalidateQueries({ queryKey: ['engagements', engagementId, 'jobs'] })
  const invalidateTargets = () =>
    queryClient.invalidateQueries({ queryKey: ['engagements', engagementId, 'targets'] })

  const [selectedTool, setSelectedTool] = useState('')
  const [toolInput, setToolInput] = useState('')
  const [activeJobId, setActiveJobId] = useState<string | null>(null)
  const launchJobMutation = useMutation({
    mutationFn: () => {
      const tool = selectedTool || tools?.[0] || ''
      const params =
        tool === 'subfinder' ? { domain: toolInput.trim() } : { targets: toolInput.split('\n').map((l) => l.trim()).filter(Boolean) }
      return createJob(engagementId, { tool_name: tool, params })
    },
    onSuccess: (job) => {
      setToolInput('')
      setActiveJobId(job.id)
      invalidateJobs()
      invalidateTargets()
    },
  })

  const { data: pipelineDefinitions } = useQuery({
    queryKey: ['pipelines'],
    queryFn: listPipelineDefinitions,
  })

  const { data: pipelineRuns } = useQuery({
    queryKey: ['engagements', engagementId, 'pipeline-runs'],
    queryFn: () => listPipelineRuns(engagementId),
    refetchInterval: (query) => {
      const data = query.state.data
      return data?.some((run) => ACTIVE_RUN_STATUSES.has(run.status)) ? 2000 : false
    },
  })

  const invalidatePipelineRuns = () =>
    queryClient.invalidateQueries({ queryKey: ['engagements', engagementId, 'pipeline-runs'] })

  const [selectedPipeline, setSelectedPipeline] = useState('')
  const [pipelineInput, setPipelineInput] = useState('')
  const [expandedRunId, setExpandedRunId] = useState<string | null>(null)
  const launchPipelineMutation = useMutation({
    mutationFn: () => {
      const pipelineName = selectedPipeline || pipelineDefinitions?.[0] || ''
      const paramKey = PIPELINE_PARAM_KEY[pipelineName] ?? 'domain'
      return createPipelineRun(engagementId, {
        pipeline_name: pipelineName,
        params: { [paramKey]: pipelineInput.trim() },
      })
    },
    onSuccess: (run) => {
      setPipelineInput('')
      setExpandedRunId(run.id)
      invalidatePipelineRuns()
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

      <section>
        <h2 className="terminal mb-3 text-sm text-accent">escaneos</h2>
        <form
          className="mb-4 flex gap-2"
          onSubmit={(e) => {
            e.preventDefault()
            if (toolInput.trim()) launchJobMutation.mutate()
          }}
        >
          <select
            className="terminal rounded-md border border-border bg-surface px-2 py-1.5 text-sm text-foreground"
            value={selectedTool || tools?.[0] || ''}
            onChange={(e) => setSelectedTool(e.target.value)}
          >
            {tools?.map((t) => (
              <option key={t} value={t}>
                {t}
              </option>
            ))}
          </select>
          <Input
            placeholder={
              (selectedTool || tools?.[0]) === 'subfinder'
                ? 'dominio, ej. example.com'
                : 'targets (uno por línea), ej. https://example.com'
            }
            value={toolInput}
            onChange={(e) => setToolInput(e.target.value)}
          />
          <Button type="submit" disabled={launchJobMutation.isPending || !tools?.length}>
            lanzar
          </Button>
        </form>

        <div className="flex flex-col gap-2">
          {jobs?.map((job) => (
            <div key={job.id} className="rounded-md border border-border bg-surface p-3">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <span className="terminal text-sm text-foreground">{job.tool_name}</span>
                  <JobStatusBadge status={job.status} />
                  <span className="text-xs text-muted">
                    {new Date(job.created_at).toLocaleString()}
                  </span>
                </div>
                <Button
                  variant="secondary"
                  onClick={() => setActiveJobId(activeJobId === job.id ? null : job.id)}
                >
                  {activeJobId === job.id ? 'ocultar logs' : 'ver logs'}
                </Button>
              </div>
              {job.error_message && (
                <p className="terminal mt-2 text-xs text-severity-critical">
                  {job.error_message}
                </p>
              )}
              {activeJobId === job.id && (
                <div className="mt-3">
                  <JobLogTerminal jobId={job.id} />
                </div>
              )}
            </div>
          ))}
          {jobs && jobs.length === 0 && (
            <p className="text-sm text-muted">No se han lanzado escaneos aún.</p>
          )}
        </div>
      </section>

      <section>
        <h2 className="terminal mb-3 text-sm text-accent">pipelines</h2>
        <form
          className="mb-4 flex gap-2"
          onSubmit={(e) => {
            e.preventDefault()
            if (pipelineInput.trim()) launchPipelineMutation.mutate()
          }}
        >
          <select
            className="terminal rounded-md border border-border bg-surface px-2 py-1.5 text-sm text-foreground"
            value={selectedPipeline || pipelineDefinitions?.[0] || ''}
            onChange={(e) => setSelectedPipeline(e.target.value)}
          >
            {pipelineDefinitions?.map((p) => (
              <option key={p} value={p}>
                {p}
              </option>
            ))}
          </select>
          <Input
            placeholder={
              PIPELINE_PARAM_KEY[selectedPipeline || pipelineDefinitions?.[0] || ''] === 'url'
                ? 'url, ej. https://example.com'
                : 'dominio, ej. example.com'
            }
            value={pipelineInput}
            onChange={(e) => setPipelineInput(e.target.value)}
          />
          <Button type="submit" disabled={launchPipelineMutation.isPending || !pipelineDefinitions?.length}>
            lanzar
          </Button>
        </form>

        <div className="flex flex-col gap-2">
          {pipelineRuns?.map((run) => (
            <div key={run.id} className="rounded-md border border-border bg-surface p-3">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <span className="terminal text-sm text-foreground">{run.pipeline_name}</span>
                  <PipelineRunStatusBadge status={run.status} />
                  <span className="text-xs text-muted">
                    {new Date(run.created_at).toLocaleString()}
                  </span>
                </div>
                <Button
                  variant="secondary"
                  onClick={() => setExpandedRunId(expandedRunId === run.id ? null : run.id)}
                >
                  {expandedRunId === run.id ? 'ocultar pasos' : 'ver pasos'}
                </Button>
              </div>
              {run.error_message && (
                <p className="terminal mt-2 text-xs text-severity-critical">
                  {run.error_message}
                </p>
              )}
              {expandedRunId === run.id && (
                <div className="mt-3 flex flex-col gap-2 border-l border-border pl-3">
                  {run.jobs.map((job) => (
                    <div key={job.id}>
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-3">
                          <span className="terminal text-xs text-muted">
                            paso {job.step_index}
                          </span>
                          <span className="terminal text-sm text-foreground">
                            {job.tool_name}
                          </span>
                          <JobStatusBadge status={job.status} />
                        </div>
                        <Button
                          variant="secondary"
                          onClick={() => setActiveJobId(activeJobId === job.id ? null : job.id)}
                        >
                          {activeJobId === job.id ? 'ocultar logs' : 'ver logs'}
                        </Button>
                      </div>
                      {job.error_message && (
                        <p className="terminal mt-1 text-xs text-severity-critical">
                          {job.error_message}
                        </p>
                      )}
                      {activeJobId === job.id && (
                        <div className="mt-2">
                          <JobLogTerminal jobId={job.id} />
                        </div>
                      )}
                    </div>
                  ))}
                  {run.jobs.length === 0 && (
                    <p className="text-sm text-muted">Aún no hay pasos ejecutados.</p>
                  )}
                </div>
              )}
            </div>
          ))}
          {pipelineRuns && pipelineRuns.length === 0 && (
            <p className="text-sm text-muted">No se han lanzado pipelines aún.</p>
          )}
        </div>
      </section>

      <section>
        <h2 className="terminal mb-3 text-sm text-accent">targets descubiertos</h2>
        <div className="flex flex-col gap-1.5">
          {targets?.map((target) => (
            <div
              key={target.id}
              className="flex items-center gap-3 rounded-md border border-border bg-surface px-3 py-2"
            >
              <span className="terminal text-xs text-muted">{target.type}</span>
              <span className="terminal text-sm text-foreground">{target.value}</span>
            </div>
          ))}
          {targets && targets.length === 0 && (
            <p className="text-sm text-muted">Sin targets descubiertos aún.</p>
          )}
        </div>
      </section>
    </div>
  )
}
