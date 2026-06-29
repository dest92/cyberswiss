export interface User {
  id: string
  email: string
  created_at: string
}

export interface AuthStatus {
  auth_disabled: boolean
  needs_setup: boolean
  user: User | null
}

export type EngagementStatus = 'active' | 'archived' | 'closed'

export interface Engagement {
  id: string
  name: string
  client_name: string | null
  status: EngagementStatus
  authorization_scope_doc: string | null
  start_date: string | null
  end_date: string | null
  created_at: string
  updated_at: string
}

export interface EngagementInput {
  name: string
  client_name?: string | null
  status?: EngagementStatus
  authorization_scope_doc?: string | null
  start_date?: string | null
  end_date?: string | null
}

export type ScopeType = 'domain' | 'ip_range' | 'url' | 'cidr'

export interface Scope {
  id: string
  engagement_id: string
  type: ScopeType
  value: string
  in_scope: boolean
}

export interface ScopeInput {
  type: ScopeType
  value: string
  in_scope?: boolean
}

export interface Note {
  id: string
  engagement_id: string
  content: string
  created_at: string
  updated_at: string
}
