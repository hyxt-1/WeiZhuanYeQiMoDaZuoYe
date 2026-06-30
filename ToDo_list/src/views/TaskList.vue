<template>
  <div class="min-h-screen bg-gray-100">
    <header class="bg-white shadow-sm">
      <div class="max-w-6xl mx-auto px-4 py-4">
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-3">
            <span class="text-3xl">📋</span>
            <h1 class="text-xl font-bold text-gray-800">待办事项</h1>
          </div>
          <button
            @click="handleLogout"
            class="text-gray-500 hover:text-gray-700 flex items-center space-x-2"
          >
            <span>退出登录</span>
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path>
            </svg>
          </button>
        </div>
      </div>
    </header>
    
    <main class="max-w-6xl mx-auto px-4 py-6">
      <div class="bg-white rounded-xl shadow-sm p-4 mb-6">
        <div class="flex flex-col sm:flex-row gap-4">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="搜索任务..."
            class="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
          />
          <button
            @click="handleSearch"
            class="px-6 py-3 bg-blue-500 hover:bg-blue-600 text-white font-semibold rounded-lg transition-colors"
          >
            搜索
          </button>
          <button
            @click="showAddModal = true"
            class="px-6 py-3 bg-green-500 hover:bg-green-600 text-white font-semibold rounded-lg transition-colors flex items-center justify-center space-x-2"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
            </svg>
            <span>新建任务</span>
          </button>
        </div>
      </div>
      
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div class="bg-white rounded-xl shadow-sm p-4">
          <div class="flex items-center justify-between mb-4">
            <h2 class="font-semibold text-gray-700">待完成</h2>
            <span class="px-3 py-1 bg-yellow-100 text-yellow-600 text-sm rounded-full">{{ pendingTasks.length }}</span>
          </div>
          <div class="space-y-3">
            <div
              v-for="task in pendingTasks"
              :key="task.id"
              @click="handleViewTask(task.id)"
              class="p-4 bg-gray-50 rounded-lg hover:bg-gray-100 cursor-pointer transition-colors"
            >
              <div class="flex items-start justify-between">
                <h3 class="font-medium text-gray-800">{{ task.title }}</h3>
                <div class="flex items-center space-x-2">
                  <button
                    @click.stop="changeTaskStatus(task.id, 'in_progress')"
                    class="text-blue-400 hover:text-blue-600"
                    title="开始进行"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z"></path>
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                    </svg>
                  </button>
                  <button
                    @click.stop="handleDeleteTask(task.id)"
                    class="text-red-400 hover:text-red-600"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                    </svg>
                  </button>
                </div>
              </div>
              <p v-if="task.description" class="text-sm text-gray-500 mt-2 line-clamp-2">{{ task.description }}</p>
              <div v-if="task.tags.length > 0" class="flex flex-wrap gap-1 mt-2">
                <span v-for="tag in task.tags" :key="tag" class="px-2 py-0.5 bg-blue-100 text-blue-600 text-xs rounded">{{ tag }}</span>
              </div>
              <div v-if="task.due_date" class="flex items-center text-sm text-gray-400 mt-2">
                <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                </svg>
                {{ formatDate(task.due_date) }}
              </div>
            </div>
            <div v-if="pendingTasks.length === 0" class="text-center py-8 text-gray-400">
              暂无待完成任务
            </div>
          </div>
        </div>
        
        <div class="bg-white rounded-xl shadow-sm p-4">
          <div class="flex items-center justify-between mb-4">
            <h2 class="font-semibold text-gray-700">进行中</h2>
            <span class="px-3 py-1 bg-blue-100 text-blue-600 text-sm rounded-full">{{ inProgressTasks.length }}</span>
          </div>
          <div class="space-y-3">
            <div
              v-for="task in inProgressTasks"
              :key="task.id"
              @click="handleViewTask(task.id)"
              class="p-4 bg-gray-50 rounded-lg hover:bg-gray-100 cursor-pointer transition-colors"
            >
              <div class="flex items-start justify-between">
                <h3 class="font-medium text-gray-800">{{ task.title }}</h3>
                <div class="flex items-center space-x-2">
                  <button
                    @click.stop="changeTaskStatus(task.id, 'todo')"
                    class="text-yellow-400 hover:text-yellow-600"
                    title="移回待完成"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path>
                    </svg>
                  </button>
                  <button
                    @click.stop="changeTaskStatus(task.id, 'completed')"
                    class="text-green-400 hover:text-green-600"
                    title="完成任务"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                    </svg>
                  </button>
                  <button
                    @click.stop="handleDeleteTask(task.id)"
                    class="text-red-400 hover:text-red-600"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                    </svg>
                  </button>
                </div>
              </div>
              <p v-if="task.description" class="text-sm text-gray-500 mt-2 line-clamp-2">{{ task.description }}</p>
              <div v-if="task.tags.length > 0" class="flex flex-wrap gap-1 mt-2">
                <span v-for="tag in task.tags" :key="tag" class="px-2 py-0.5 bg-blue-100 text-blue-600 text-xs rounded">{{ tag }}</span>
              </div>
            </div>
            <div v-if="inProgressTasks.length === 0" class="text-center py-8 text-gray-400">
              暂无进行中任务
            </div>
          </div>
        </div>
        
        <div class="bg-white rounded-xl shadow-sm p-4">
          <div class="flex items-center justify-between mb-4">
            <h2 class="font-semibold text-gray-700">已完成</h2>
            <span class="px-3 py-1 bg-green-100 text-green-600 text-sm rounded-full">{{ completedTasks.length }}</span>
          </div>
          <div class="space-y-3">
            <div
              v-for="task in completedTasks"
              :key="task.id"
              @click="handleViewTask(task.id)"
              class="p-4 bg-gray-50 rounded-lg hover:bg-gray-100 cursor-pointer transition-colors opacity-70"
            >
              <div class="flex items-start justify-between">
                <h3 class="font-medium text-gray-500 line-through">{{ task.title }}</h3>
                <div class="flex items-center space-x-2">
                  <button
                    @click.stop="changeTaskStatus(task.id, 'in_progress')"
                    class="text-blue-400 hover:text-blue-600"
                    title="重新开始"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
                    </svg>
                  </button>
                  <button
                    @click.stop="handleDeleteTask(task.id)"
                    class="text-red-400 hover:text-red-600"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                    </svg>
                  </button>
                </div>
              </div>
              <p v-if="task.description" class="text-sm text-gray-400 mt-2 line-clamp-2">{{ task.description }}</p>
            </div>
            <div v-if="completedTasks.length === 0" class="text-center py-8 text-gray-400">
              暂无已完成任务
            </div>
          </div>
        </div>
      </div>
    </main>
    
    <div v-if="showAddModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-xl shadow-2xl p-6 w-full max-w-md">
        <h2 class="text-xl font-bold text-gray-800 mb-4">新建任务</h2>
        <form @submit.prevent="handleCreateTask" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">任务标题</label>
            <input
              v-model="newTask.title"
              type="text"
              placeholder="请输入任务标题"
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
              required
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">任务描述</label>
            <textarea
              v-model="newTask.description"
              rows="3"
              placeholder="请输入任务描述"
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none resize-none"
            ></textarea>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">优先级</label>
            <select
              v-model="newTask.priority"
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
            >
              <option value="low">低</option>
              <option value="medium">中</option>
              <option value="high">高</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">截止时间</label>
            <input
              v-model="newTask.due_date"
              type="date"
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
            />
          </div>
          <div class="flex gap-4">
            <button
              type="button"
              @click="showAddModal = false"
              class="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
            >
              取消
            </button>
            <button
              type="submit"
              class="flex-1 px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
            >
              创建
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getTasks, createTask, deleteTask } from '../api'
import type { Task } from '../types'

const router = useRouter()
const tasks = ref<Task[]>([])
const searchQuery = ref('')
const showAddModal = ref(false)

const newTask = reactive({
  title: '',
  description: '',
  priority: 'medium' as 'low' | 'medium' | 'high',
  due_date: ''
})

const filteredTasks = computed(() => {
  if (!searchQuery.value) return tasks.value
  const query = searchQuery.value.toLowerCase()
  return tasks.value.filter(task =>
    task.title.toLowerCase().includes(query) ||
    task.description.toLowerCase().includes(query) ||
    task.tags.some(tag => tag.toLowerCase().includes(query))
  )
})

const pendingTasks = computed(() => filteredTasks.value.filter(t => t.status === 'todo'))
const inProgressTasks = computed(() => filteredTasks.value.filter(t => t.status === 'in_progress'))
const completedTasks = computed(() => filteredTasks.value.filter(t => t.status === 'completed'))

const priorityClass = (priority: string) => {
  switch (priority) {
    case 'high': return 'bg-red-100 text-red-600'
    case 'medium': return 'bg-yellow-100 text-yellow-600'
    case 'low': return 'bg-green-100 text-green-600'
    default: return 'bg-gray-100 text-gray-600'
  }
}

const priorityText = (priority: string) => {
  switch (priority) {
    case 'high': return '高'
    case 'medium': return '中'
    case 'low': return '低'
    default: return priority
  }
}

const formatDate = (date: string) => {
  const d = new Date(date)
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
}

const loadTasks = async () => {
  try {
    tasks.value = await getTasks(searchQuery.value)
  } catch (err) {
    console.error('Failed to load tasks:', err)
  }
}

const handleSearch = () => {
  loadTasks()
}

const handleViewTask = (id: number) => {
  router.push(`/tasks/${id}`)
}

const handleCreateTask = async () => {
  try {
    await createTask(newTask)
    showAddModal.value = false
    newTask.title = ''
    newTask.description = ''
    newTask.priority = 'medium'
    newTask.due_date = ''
    loadTasks()
  } catch (err) {
    console.error('Failed to create task:', err)
  }
}

const changeTaskStatus = async (id: number, status: 'todo' | 'in_progress' | 'completed') => {
  try {
    await updateTask(id, { status })
    loadTasks()
  } catch (err) {
    console.error('Failed to change task status:', err)
  }
}

const handleDeleteTask = async (id: number) => {
  if (confirm('确定要删除这个任务吗？')) {
    try {
      await deleteTask(id)
      loadTasks()
    } catch (err) {
      console.error('Failed to delete task:', err)
    }
  }
}

const handleLogout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('user')
  router.push('/login')
}

onMounted(() => {
  loadTasks()
})
</script>
