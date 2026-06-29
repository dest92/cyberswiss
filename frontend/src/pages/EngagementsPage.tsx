import { useState } from 'react'
import { Link } from 'react-router-dom'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { createEngagement, listEngagements } from '@/api/engagements'
import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import { StatusBadge } from '@/components/ui/Badge'

export function EngagementsPage() {
  const queryClient = useQueryClient()
  const [showForm, setShowForm] = useState(false)
  const [name, setName] = useState('')
  const [clientName, setClientName] = useState('')

  const { data: engagements, isLoading } = useQuery({
    queryKey: ['engagements'],
    queryFn: listEngagements,
  })

  const createMutation = useMutation({
    mutationFn: () => createEngagement({ name, client_name: clientName || null }),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ['engagements'] })
      setName('')
      setClientName('')
      setShowForm(false)
    },
  })

  return (
    <div>
      <div className="mb-6 flex items-center justify-between">
        <h1 className="terminal text-lg text-foreground">engagements</h1>
        <Button onClick={() => setShowForm((v) => !v)}>
          {showForm ? 'cancelar' : '+ nuevo engagement'}
        </Button>
      </div>

      {showForm && (
        <form
          className="mb-6 rounded-md border border-border bg-surface p-4"
          onSubmit={(e) => {
            e.preventDefault()
            createMutation.mutate()
          }}
        >
          <div className="mb-3">
            <label className="mb-1 block text-xs text-muted">nombre</label>
            <Input value={name} onChange={(e) => setName(e.target.value)} required autoFocus />
          </div>
          <div className="mb-4">
            <label className="mb-1 block text-xs text-muted">cliente</label>
            <Input value={clientName} onChange={(e) => setClientName(e.target.value)} />
          </div>
          <Button type="submit" disabled={createMutation.isPending}>
            crear
          </Button>
        </form>
      )}

      {isLoading && <p className="text-sm text-muted">cargando...</p>}

      {engagements && engagements.length === 0 && (
        <p className="text-sm text-muted">No hay engagements todavía.</p>
      )}

      <div className="flex flex-col gap-2">
        {engagements?.map((engagement) => (
          <Link
            key={engagement.id}
            to={`/engagements/${engagement.id}`}
            className="flex items-center justify-between rounded-md border border-border bg-surface px-4 py-3 hover:border-accent/50"
          >
            <div>
              <div className="text-sm text-foreground">{engagement.name}</div>
              {engagement.client_name && (
                <div className="text-xs text-muted">{engagement.client_name}</div>
              )}
            </div>
            <StatusBadge status={engagement.status} />
          </Link>
        ))}
      </div>
    </div>
  )
}
