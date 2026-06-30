import axios from 'axios'
import router from '../router'
import type { LoginRequest, LoginResponse, Task, CreateTaskRequest, UpdateTaskRequest } from '../types'

const api = axios.create({
  baseURL: '/api',
  timeout: 5000
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      router.push('/login')
    }
    return Promise.reject(error)
  }
)

export const login = (data: LoginRequest): Promise<LoginResponse> => {
  return api.post('/auth/login', data).then((res) => res.data)
}

export const getTasks = (search?: string): Promise<Task[]> => {
  const params = search ? { search } : {}
  return api.get('/tasks', { params }).then((res) => res.data)
}

export const getTask = (id: number): Promise<Task> => {
  return api.get(`/tasks/${id}`).then((res) => res.data)
}

export const createTask = (data: CreateTaskRequest): Promise<Task> => {
  return api.post('/tasks', data).then((res) => res.data)
}

export const updateTask = (id: number, data: UpdateTaskRequest): Promise<Task> => {
  return api.put(`/tasks/${id}`, data).then((res) => res.data)
}

export const deleteTask = (id: number): Promise<void> => {
  return api.delete(`/tasks/${id}`).then((res) => res.data)
}
