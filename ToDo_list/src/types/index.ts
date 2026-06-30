export interface User {
  id: number
  username: string
  email: string
}

export interface Task {
  id: number
  title: string
  description: string
  status: 'todo' | 'in_progress' | 'completed'
  priority: 'low' | 'medium' | 'high'
  tags: string[]
  due_date: string | null
  created_at: string
  updated_at: string
}

export interface LoginRequest {
  username: string
  password: string
}

export interface LoginResponse {
  access_token: string
  token_type: string
  user: User
}

export interface CreateTaskRequest {
  title: string
  description?: string
  priority?: 'low' | 'medium' | 'high'
  tags?: string[]
  due_date?: string
  status?: 'todo' | 'in_progress' | 'completed'
}

export interface UpdateTaskRequest {
  title?: string
  description?: string
  status?: 'todo' | 'in_progress' | 'completed'
  priority?: 'low' | 'medium' | 'high'
  tags?: string[]
  due_date?: string
}
