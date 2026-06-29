import { useState } from 'react'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import {
  createKnowledgeDocument,
  deleteKnowledgeDocument,
  getKnowledgeDocument,
  listKnowledgeDocuments,
  searchKnowledgeDocuments,
  uploadKnowledgeDocument,
} from '@/api/knowledge'
import { Button } from '@/components/ui/Button'
import { Input, Textarea } from '@/components/ui/Input'
import { OWASP_TOP_10 } from '@/lib/owasp'
import type { KnowledgeDocumentSearchResult, KnowledgeDocumentSummary } from '@/api/types'

function hasSnippet(
  doc: KnowledgeDocumentSummary | KnowledgeDocumentSearchResult,
): doc is KnowledgeDocumentSearchResult {
  return 'snippet' in doc
}

export function KnowledgeLibraryPage() {
  const queryClient = useQueryClient()
  const [categoryFilter, setCategoryFilter] = useState<string>('')
  const [searchQuery, setSearchQuery] = useState('')
  const [activeSearch, setActiveSearch] = useState('')
  const [openDocumentId, setOpenDocumentId] = useState<string | null>(null)
  const [showCreateForm, setShowCreateForm] = useState(false)
  const [title, setTitle] = useState('')
  const [content, setContent] = useState('')
  const [categories, setCategories] = useState<string[]>([])
  const [uploadTitle, setUploadTitle] = useState('')
  const [uploadCategories, setUploadCategories] = useState<string[]>([])
  const [uploadFile, setUploadFile] = useState<File | null>(null)

  const { data: documents } = useQuery({
    queryKey: ['knowledge', categoryFilter],
    queryFn: () => listKnowledgeDocuments(categoryFilter || undefined),
    enabled: !activeSearch,
  })

  const { data: searchResults } = useQuery({
    queryKey: ['knowledge', 'search', activeSearch],
    queryFn: () => searchKnowledgeDocuments(activeSearch),
    enabled: !!activeSearch,
  })

  const { data: openDocument } = useQuery({
    queryKey: ['knowledge', 'document', openDocumentId],
    queryFn: () => getKnowledgeDocument(openDocumentId!),
    enabled: !!openDocumentId,
  })

  const invalidateList = () => {
    void queryClient.invalidateQueries({ queryKey: ['knowledge'] })
  }

  const createMutation = useMutation({
    mutationFn: () => createKnowledgeDocument({ title, content, owasp_categories: categories }),
    onSuccess: () => {
      setTitle('')
      setContent('')
      setCategories([])
      setShowCreateForm(false)
      invalidateList()
    },
  })

  const uploadMutation = useMutation({
    mutationFn: () => uploadKnowledgeDocument(uploadTitle, uploadCategories, uploadFile!),
    onSuccess: () => {
      setUploadTitle('')
      setUploadCategories([])
      setUploadFile(null)
      invalidateList()
    },
  })

  const deleteMutation = useMutation({
    mutationFn: (documentId: string) => deleteKnowledgeDocument(documentId),
    onSuccess: () => {
      setOpenDocumentId(null)
      invalidateList()
    },
  })

  const toggleCategory = (
    code: string,
    selected: string[],
    setSelected: (v: string[]) => void,
  ) => {
    setSelected(
      selected.includes(code) ? selected.filter((c) => c !== code) : [...selected, code],
    )
  }

  const visibleDocuments = activeSearch ? searchResults : documents

  return (
    <div className="flex flex-col gap-8">
      <section>
        <div className="mb-4 flex items-center justify-between">
          <h1 className="terminal text-lg text-foreground">biblioteca de conocimiento</h1>
          <Button onClick={() => setShowCreateForm((v) => !v)}>
            {showCreateForm ? 'cancelar' : '+ nuevo documento'}
          </Button>
        </div>

        <form
          className="mb-4 flex gap-2"
          onSubmit={(e) => {
            e.preventDefault()
            setActiveSearch(searchQuery.trim())
          }}
        >
          <Input
            placeholder="buscar en la biblioteca..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
          <Button type="submit">buscar</Button>
          {activeSearch && (
            <Button
              variant="secondary"
              onClick={() => {
                setActiveSearch('')
                setSearchQuery('')
              }}
            >
              limpiar
            </Button>
          )}
        </form>

        {!activeSearch && (
          <div className="mb-4 flex flex-wrap gap-2">
            <Button
              variant={categoryFilter === '' ? 'primary' : 'secondary'}
              onClick={() => setCategoryFilter('')}
            >
              todas
            </Button>
            {OWASP_TOP_10.map((c) => (
              <Button
                key={c.code}
                variant={categoryFilter === c.code ? 'primary' : 'secondary'}
                onClick={() => setCategoryFilter(c.code)}
              >
                {c.code}
              </Button>
            ))}
          </div>
        )}

        {showCreateForm && (
          <form
            className="mb-6 flex flex-col gap-2 rounded-md border border-border bg-surface p-4"
            onSubmit={(e) => {
              e.preventDefault()
              if (title.trim() && content.trim()) createMutation.mutate()
            }}
          >
            <Input placeholder="título" value={title} onChange={(e) => setTitle(e.target.value)} />
            <Textarea
              placeholder="contenido en markdown"
              value={content}
              onChange={(e) => setContent(e.target.value)}
              rows={8}
            />
            <div className="flex flex-wrap gap-2">
              {OWASP_TOP_10.map((c) => (
                <button
                  type="button"
                  key={c.code}
                  onClick={() => toggleCategory(c.code, categories, setCategories)}
                  className={`terminal rounded border px-2 py-1 text-xs ${
                    categories.includes(c.code)
                      ? 'border-accent bg-accent/10 text-accent'
                      : 'border-border bg-surface-elevated text-muted'
                  }`}
                >
                  {c.code}
                </button>
              ))}
            </div>
            <Button type="submit" disabled={createMutation.isPending}>
              guardar
            </Button>
          </form>
        )}

        <div className="mb-6 flex flex-col gap-2 rounded-md border border-border bg-surface p-4">
          <h3 className="terminal text-xs text-accent">subir PDF</h3>
          <Input
            placeholder="título"
            value={uploadTitle}
            onChange={(e) => setUploadTitle(e.target.value)}
          />
          <input
            type="file"
            accept="application/pdf"
            onChange={(e) => setUploadFile(e.target.files?.[0] ?? null)}
            className="terminal text-sm text-muted"
          />
          <div className="flex flex-wrap gap-2">
            {OWASP_TOP_10.map((c) => (
              <button
                type="button"
                key={c.code}
                onClick={() => toggleCategory(c.code, uploadCategories, setUploadCategories)}
                className={`terminal rounded border px-2 py-1 text-xs ${
                  uploadCategories.includes(c.code)
                    ? 'border-accent bg-accent/10 text-accent'
                    : 'border-border bg-surface-elevated text-muted'
                }`}
              >
                {c.code}
              </button>
            ))}
          </div>
          <Button
            onClick={() => uploadTitle.trim() && uploadFile && uploadMutation.mutate()}
            disabled={uploadMutation.isPending || !uploadFile || !uploadTitle.trim()}
          >
            subir
          </Button>
        </div>

        <div className="flex flex-col gap-2">
          {visibleDocuments?.map((doc) => (
            <div key={doc.id} className="rounded-md border border-border bg-surface p-3">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <span className="terminal text-sm text-foreground">{doc.title}</span>
                  <span className="terminal text-xs text-muted">{doc.doc_type}</span>
                  {doc.status !== 'ready' && (
                    <span className="terminal text-xs text-severity-medium">{doc.status}</span>
                  )}
                  {doc.owasp_categories.map((code) => (
                    <span key={code} className="terminal text-xs text-accent">
                      {code}
                    </span>
                  ))}
                </div>
                <div className="flex gap-2">
                  <Button
                    variant="secondary"
                    onClick={() => setOpenDocumentId(openDocumentId === doc.id ? null : doc.id)}
                  >
                    {openDocumentId === doc.id ? 'cerrar' : 'ver'}
                  </Button>
                  {!doc.is_seed && (
                    <Button variant="danger" onClick={() => deleteMutation.mutate(doc.id)}>
                      eliminar
                    </Button>
                  )}
                </div>
              </div>
              {hasSnippet(doc) && doc.snippet && (
                <p
                  className="terminal mt-2 text-xs text-muted"
                  dangerouslySetInnerHTML={{ __html: doc.snippet }}
                />
              )}
              {openDocumentId === doc.id && openDocument?.id === doc.id && (
                <pre className="terminal mt-3 whitespace-pre-wrap rounded-md border border-border bg-background p-3 text-xs text-foreground">
                  {openDocument.content ?? '(sin contenido)'}
                </pre>
              )}
            </div>
          ))}
          {visibleDocuments && visibleDocuments.length === 0 && (
            <p className="text-sm text-muted">No se encontraron documentos.</p>
          )}
        </div>
      </section>
    </div>
  )
}
