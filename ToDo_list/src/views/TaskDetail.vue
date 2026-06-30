<template>
  <div class="min-h-screen bg-gray-100">
    <header class="bg-white shadow-sm">
      <div class="max-w-4xl mx-auto px-4 py-4">
        <button
          @click="handleBack"
          class="flex items-center text-gray-600 hover:text-gray-800 transition-colors"
        >
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path>
          </svg>
          返回任务列表
        </button>
      </div>
    </header>
    
    <main class="max-w-4xl mx-auto px-4 py-6">
      <div v-if="task" class="bg-white rounded-xl shadow-sm p-6">
        <div class="flex items-start justify-between mb-6">
          <div>
            <input
              v-model="task.title"
              class="text-2xl font-bold text-gray-800 border-none outline-none bg-transparent"
            />
            <div class="flex items-center gap-2 mt-2">
              <select
                v-model="task.status"
                class="px-3 py-1 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
              >
                <option value="todo">待完成</option>
                <option value="in_progress">进行中</option>
                <option value="completed">已完成</option>
              </select>
              <span :class="statusClass(task.status)" class="px-2 py-0.5 text-sm rounded">
                {{ statusText(task.status) }}
              </span>
            </div>
          </div>
          <button
            @click="handleSave"
            class="px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white font-semibold rounded-lg transition-colors"
          >
            保存
          </button>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">任务描述</label>
            <textarea
              v-model="task.description"
              rows="6"
              placeholder="请输入任务描述"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none resize-none"
            ></textarea>
          </div>
          
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">优先级</label>
              <select
                v-model="task.priority"
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
                v-model="task.due_date"
                type="date"
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
              />
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">标签</label>
              <div class="flex flex-wrap gap-2 mb-2">
                <span
                  v-for="(tag, index) in task.tags"
                  :key="tag"
                  class="px-3 py-1 bg-blue-100 text-blue-600 rounded-full text-sm flex items-center"
                >
                  {{ tag }}
                  <button
                    @click="removeTag(index)"
                    class="ml-1 hover:text-blue-800"
                  >
                    ×
                  </button>
                </span>
              </div>
              <div class="flex gap-2">
                <input
                  v-model="newTag"
                  type="text"
                  placeholder="输入标签"
                  class="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
                  @keyup.enter="addTag"
                />
                <button
                  @click="addTag"
                  class="px-4 py-2 bg-gray-500 hover:bg-gray-600 text-white rounded-lg transition-colors"
                >
                  添加
                </button>
              </div>
            </div>
          </div>
        </div>
        
        <div class="mt-6 pt-6 border-t border-gray-200">
          <div class="flex items-center justify-between text-sm text-gray-400">
            <span>创建时间: {{ formatDate(task.created_at) }}</span>
            <span>更新时间: {{ formatDate(task.updated_at) }}</span>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getTask, updateTask } from '../api'
import type { Task } from '../types'

const route = useRoute()
const router = useRouter()
const task = ref<Task | null>(null)
const newTag = ref('')

const formatDate = (date: string) => {
  const d = new Date(date)
  return d.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const loadTask = async () => {
  const id = Number(route.params.id)
  try {
    task.value = await getTask(id)
  } catch (err) {
    console.error('Failed to load task:', err)
    router.push('/tasks')
  }
}

const statusClass = (status: string) => {
  switch (status) {
    case 'completed': return 'bg-green-100 text-green-600'
    case 'in_progress': return 'bg-blue-100 text-blue-600'
    case 'todo': return 'bg-yellow-100 text-yellow-600'
    default: return 'bg-gray-100 text-gray-600'
  }
}

const statusText = (status: string) => {
  switch (status) {
    case 'completed': return '已完成'
    case 'in_progress': return '进行中'
    case 'todo': return '待完成'
    default: return status
  }
}

const addTag = () => {
  if (newTag.value.trim() && task.value) {
    task.value.tags.push(newTag.value.trim())
    newTag.value = ''
  }
}

const removeTag = (index: number) => {
  if (task.value) {
    task.value.tags.splice(index, 1)
  }
}

const handleSave = async () => {
  if (task.value) {
    try {
      await updateTask(task.value.id, task.value)
    } catch (err) {
      console.error('Failed to update task:', err)
    }
  }
}

const handleBack = () => {
  router.push('/tasks')
}

onMounted(() => {
  loadTask()
})
</script>
