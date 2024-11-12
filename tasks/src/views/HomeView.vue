<template>
  <div class="min-h-screen bg-black p-4 sm:p-6">
    <!-- Navbar -->
    <nav class="bg-gray-900/50 backdrop-blur-sm border border-yellow-600/20 rounded-lg p-4 mb-6">
      <div class="max-w-7xl mx-auto flex flex-col sm:flex-row justify-between items-center">
        <h1 class="text-2xl font-mono text-white mb-4 sm:mb-0">Le Tasks</h1>
        <div class="flex flex-col sm:flex-row items-center space-y-4 sm:space-y-0 sm:space-x-4">
          <select
            v-model="selectedProject"
            @change="changeProject"
            class="w-full sm:w-auto bg-black border border-yellow-600/30 rounded px-3 py-1 text-white font-mono focus:outline-none focus:border-yellow-500 mb-2 sm:mb-0"
          >
            <option value="">All Projects</option>
            <option v-for="project in projects" :key="project.id" :value="project.id">{{ project.name }}</option>
          </select>
          <div v-if="user" class="flex items-center space-x-2">
            <a href="/profile" class="flex items-center space-x-2">
              <img :src="user.avatar" alt="User Avatar" class="w-8 h-8 rounded-full">
              <span class="text-white font-mono">{{ user.username }}</span>
            </a>
            <button @click="logout" class="text-yellow-500 hover:text-yellow-400">Logout</button>
          </div>
          <button
            v-else
            @click="$router.push('/auth/sign-in')"
            class="w-full sm:w-auto bg-yellow-600/20 hover:bg-yellow-600/30 border border-yellow-600/50 text-yellow-500 font-mono px-4 py-1 rounded transition-all duration-300"
          >
            [ LOGIN ]
          </button>
        </div>
      </div>
    </nav>
  
    <div class="max-w-4xl mx-auto">
      <!-- Task Input Section -->
      <div class="bg-gray-900/50 backdrop-blur-sm border border-yellow-600/20 rounded-lg p-4 sm:p-6 mb-8">
        <form @submit.prevent="addTask" class="space-y-4">
          <div class="flex flex-col sm:flex-row gap-4">
            <input
              v-model="newTask.title"
              type="text"
              placeholder="ENTER NEW TASK"
              required
              class="w-full bg-black border border-yellow-600/30 rounded px-4 py-2 text-white font-mono focus:outline-none focus:border-yellow-500 placeholder-gray-600"
            />
            <select
              v-model="newTask.priority"
              required
              class="w-full sm:w-auto bg-black border border-yellow-600/30 rounded px-4 py-2 text-white font-mono focus:outline-none focus:border-yellow-500"
            >
              <option value="low">LOW PRIORITY</option>
              <option value="medium">MEDIUM PRIORITY</option>
              <option value="high">HIGH PRIORITY</option>
            </select>
          </div>
          <div class="flex flex-col sm:flex-row gap-4">
            <input
              v-model="newTask.due_date"
              type="text"
              placeholder="DD.MM"
              required
              class="w-full sm:w-auto bg-black border border-yellow-600/30 rounded px-4 py-2 text-white font-mono focus:outline-none focus:border-yellow-500"
            />
            <select
              v-model="newTask.assignee"
              class="w-full bg-black border border-yellow-600/30 rounded px-4 py-2 text-white font-mono focus:outline-none focus:border-yellow-500"
              :disabled="!selectedProject"
            >
              <option value="">Select User</option>
              <option v-for="user in projectUsers" :key="user.id" :value="user.username">
                {{ user.username }}
              </option>
            </select>
          </div>
          <textarea
            v-model="newTask.description"
            placeholder="Task description"
            rows="3"
            class="w-full bg-black border border-yellow-600/30 rounded px-4 py-2 text-white font-mono focus:outline-none focus:border-yellow-500 placeholder-gray-600"
          ></textarea>
          <button
            type="submit"
            class="w-full bg-yellow-600/20 hover:bg-yellow-600/30 border border-yellow-600/50 text-yellow-500 font-mono py-2 rounded transition-all duration-300"
          >
            [ INITIALIZE TASK ]
          </button>
        </form>
      </div>
  
      <!-- Stats Grid -->
      <div class="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-8">
        <div class="bg-gray-900/50 border border-yellow-600/20 rounded-lg p-4">
          <div class="text-gray-500 font-mono text-sm mb-1">TOTAL TASKS</div>
          <div class="text-white font-mono text-2xl">{{ filteredTasks.length }}</div>
        </div>
        <div class="bg-gray-900/50 border border-yellow-600/20 rounded-lg p-4">
          <div class="text-gray-500 font-mono text-sm mb-1">COMPLETED</div>
          <div class="text-white font-mono text-2xl">{{ completedTasks }}</div>
        </div>
        <div class="bg-gray-900/50 border border-yellow-600/20 rounded-lg p-4">
          <div class="text-gray-500 font-mono text-sm mb-1">EFFICIENCY</div>
          <div class="text-white font-mono text-2xl">{{ efficiency }}%</div>
        </div>
        <div class="bg-gray-900/50 border border-yellow-600/20 rounded-lg p-4">
          <div class="text-gray-500 font-mono text-sm mb-1">OVERDUE</div>
          <div class="text-white font-mono text-2xl">{{ overdueTasks }}</div>
        </div>
      </div>
  
      <!-- Kanban Board -->
      <div class="space-y-6 md:space-y-0 md:grid md:grid-cols-3 md:gap-6">
        <div 
          v-for="status in ['To Do', 'In Progress', 'Done']" 
          :key="status" 
          class="bg-gray-900/50 border border-yellow-600/20 rounded-lg p-4"
          @drop="onDrop($event, status)"
          @dragover.prevent
          @dragenter.prevent
        >
          <h2 class="text-lg font-semibold text-yellow-400 mb-4">{{ status }}</h2>
          <div class="space-y-4">
            <div
              v-for="task in getTasksByStatus(status)"
              :key="task.id"
              class="bg-gray-800/50 border border-yellow-600/20 rounded-lg p-4 cursor-move"
              draggable="true"
              @dragstart="startDrag($event, task)"
              @click="openTaskDetails(task)"
            >
              <div class="flex items-center justify-between mb-2">
                <span class="font-mono text-white" :class="{ 'line-through': task.completed }">{{ task.title }}</span>
                <span
                  class="px-2 py-1 rounded text-xs font-mono"
                  :class="{
                    'bg-red-500/20 text-red-500': task.priority === 'high',
                    'bg-yellow-500/20 text-yellow-500': task.priority === 'medium',
                    'bg-blue-500/20 text-blue-500': task.priority === 'low'
                  }"
                >{{ task.priority.toUpperCase() }}</span>
              </div>
              <div class="flex items-center justify-between text-sm">
                <span class="text-gray-500 font-mono">{{ formatDate(task.due_date) }}</span>
                <span class="text-yellow-500 font-mono">{{ task.assignee ? task.assignee.username : 'Unassigned' }}</span>
              </div>
              <div v-if="task.description" class="mt-2 text-gray-400 text-sm truncate">
                {{ task.description }}
              </div>
              <div class="mt-2 flex flex-wrap justify-end gap-2">
                <button
                  v-if="task.status !== 'In Progress'"
                  @click.stop="moveToInProgress(task)"
                  class="bg-yellow-600/20 hover:bg-yellow-600/30 border border-yellow-600/50 text-yellow-500 font-mono px-2 py-1 rounded text-xs"
                >
                  Move to In Progress
                </button>
                <button
                  v-if="!task.completed"
                  @click.stop="toggleTaskStatus(task)"
                  class="bg-green-600/20 hover:bg-green-600/30 border border-green-600/50 text-green-500 font-mono px-2 py-1 rounded text-xs"
                >
                  Complete
                </button>
                <button
                  v-else
                  @click.stop="toggleTaskStatus(task)"
                  class="bg-yellow-600/20 hover:bg-yellow-600/30 border border-yellow-600/50 text-yellow-500 font-mono px-2 py-1 rounded text-xs"
                >
                  Reopen
                </button>
                <button
                  v-if="task.completed"
                  @click.stop="deleteTask(task.id)"
                  class="bg-red-600/20 hover:bg-red-600/30 border border-red-600/50 text-red-500 font-mono px-2 py-1 rounded text-xs"
                >
                  Delete
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Task Details Modal -->
      <div v-if="selectedTask" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
        <div class="bg-gray-900 border border-yellow-600/20 rounded-lg p-6 w-full max-w-md">
          <h2 class="text-2xl font-bold text-white mb-4">{{ selectedTask.title }}</h2>
          <div class="mb-4">
            <label class="block text-yellow-500 font-mono mb-2">Description</label>
            <textarea
              v-model="selectedTask.description"
              class="w-full bg-gray-800 text-white rounded p-2"
              rows="4"
            ></textarea>
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-4">
            <div>
              <label class="block text-yellow-500 font-mono mb-2">Status</label>
              <select v-model="selectedTask.status" class="w-full bg-gray-800 text-white rounded p-2">
                <option value="To Do">To Do</option>
                <option value="In Progress">In Progress</option>
                <option value="Done">Done</option>
              </select>
            </div>
            <div>
              <label class="block text-yellow-500 font-mono mb-2">Priority</label>
              <select v-model="selectedTask.priority" class="w-full bg-gray-800 text-white rounded p-2">
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
              </select>
            </div>
          </div>
          <div class="mb-4">
            <label class="block text-yellow-500 font-mono mb-2">Assignee</label>
            <select v-model="selectedTask.assignee" class="w-full bg-gray-800 text-white rounded p-2">
              <option value="">Unassigned</option>
              <option v-for="user in projectUsers" :key="user.id" :value="user.username">
                {{ user.username }}
              </option>
            </select>
          </div>
          <div class="mb-4">
            <label class="block text-yellow-500 font-mono mb-2">Due Date (DD.MM)</label>
            <input
              v-model="selectedTask.due_date"
              type="text"
              placeholder="DD.MM"
              class="w-full bg-gray-800 text-white rounded p-2"
            />
          </div>
          <div class="flex flex-wrap justify-end gap-4">
            <button @click="closeTaskDetails" class="bg-gray-700 text-white px-4 py-2 rounded">Close</button>
            <button @click="saveTaskDetails" class="bg-yellow-600 text-white px-4 py-2 rounded">Save</button>
            <button
              v-if="selectedTask.completed"
              @click="deleteTask(selectedTask.id)"
              class="bg-red-600 text-white px-4 py-2 rounded"
            >
              Delete
            </button>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-if="filteredTasks.length === 0" class="text-center py-12 border border-yellow-600/20 rounded-lg mt-8">
        <div class="text-yellow-500 font-mono mb-2">/ / SYSTEM IDLE / /</div>
        <div class="text-gray-500 font-mono text-sm">NO ACTIVE TASKS DETECTED</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import axios from 'axios'

const store = useStore()
const router = useRouter()

const user = computed(() => store.state.user)
const projects = computed(() => store.state.projects)
const tasks = computed(() => store.state.tasks)
const selectedProject = ref('')
const selectedTask = ref(null)
const projectUsers = ref([])
const intervalId = ref(null)

const newTask = ref({
  title: '',
  description: '',
  priority: 'medium',
  due_date: '',
  assignee: '',
  status: 'To Do'
})

onMounted(async () => {
  if (store.getters.isAuthenticated) {
    try {
      await store.dispatch('fetchUser')
      await store.dispatch('fetchProjects')
      await store.dispatch('fetchTasks', selectedProject.value)
    } catch (error) {
      console.error('Failed to fetch initial data:', error)
      router.push('/auth/sign-in')
    }
  } else {
    router.push('/auth/sign-in')
  }
  intervalId.value = setInterval(() => {
    store.dispatch('fetchTasks', selectedProject.value)
  }, 300000)
})

const fetchProjectUsers = async (projectId) => {
  if (!projectId) {
    projectUsers.value = []
    return
  }
  try {
    const response = await axios.get(`/api/projects/${projectId}/users`, {
      headers: { Authorization: `Bearer ${store.state.token}` }
    })
    projectUsers.value = response.data
    console.log('Fetched users:', projectUsers.value)
  } catch (error) {
    console.error('Failed to fetch project users:', error)
    projectUsers.value = []
  }
}

const changeProject = async () => {
  await store.dispatch('fetchTasks', selectedProject.value)
  await fetchProjectUsers(selectedProject.value)
}

const addTask = async () => {
  const taskData = {
    title: newTask.value.title,
    description: newTask.value.description,
    priority: newTask.value.priority,
    due_date: formatDateForBackend(newTask.value.due_date),
    status: newTask.value.status,
    project_id: parseInt(selectedProject.value),
    assignee: newTask.value.assignee
  }

  console.log('Sending task data:', taskData)

  try {
    await store.dispatch('addTask', taskData)
    console.log('Task added successfully')
    newTask.value = {
      title: '',
      description: '',
      priority: 'medium',
      due_date: '',
      assignee: '',
      status: 'To Do'
    }
    await store.dispatch('fetchTasks', selectedProject.value)
  } catch (error) {
    console.error("Failed to add task:", error)
    if (error.response) {
      console.error("Server response:", error.response.data)
    }
  }
}

watch(selectedProject, async (newValue) => {
  if (newValue) {
    await fetchProjectUsers(newValue)
  } else {
    projectUsers.value = []
  }
})

watch(() => store.getters.isAuthenticated, (isAuthenticated) => {
  if (!isAuthenticated) {
    router.push('/auth/sign-in')
  }
})

const formatDate = (dateString) => {
  if (!dateString) return ''
  const [year, month, day] = dateString.split('-')
  return `${day}.${month}`
}

const formatDateForBackend = (dateString) => {
  if (!dateString) return ''
  const [day, month] = dateString.split('.')
  const year = new Date().getFullYear()
  return `${year}-${month.padStart(2, '0')}-${day.padStart(2, '0')}`
}

const openTaskDetails = (task) => {
  selectedTask.value = { ...task, due_date: formatDate(task.due_date) }
}

const closeTaskDetails = () => {
  selectedTask.value = null
}

const saveTaskDetails = async () => {
  try {
    const updatedTask = {
      ...selectedTask.value,
      due_date: formatDateForBackend(selectedTask.value.due_date)
    }
    await store.dispatch('updateTask', updatedTask)
    closeTaskDetails()
    await store.dispatch('fetchTasks', selectedProject.value)
  } catch (error) {
    console.error('Failed to update task:', error)
  }
}

const toggleTaskStatus = async (task) => {
  await store.dispatch('updateTask', {
    ...task,
    completed: !task.completed,
    status: !task.completed ? 'Done' : 'To Do'
  })
  await store.dispatch('fetchTasks', selectedProject.value)
}

const deleteTask = async (id) => {
  try {
    await store.dispatch('deleteTask', id)
    if (selectedTask.value && selectedTask.value.id === id) {
      closeTaskDetails()
    }
    await store.dispatch('fetchTasks', selectedProject.value)
  } catch (error) {
    console.error('Failed to delete task:', error)
  }
}

const filteredTasks = computed(() => {
  return tasks.value.filter(task => 
    !selectedProject.value || task.project.id === parseInt(selectedProject.value)
  )
})

const getTasksByStatus = (status) => {
  return filteredTasks.value.filter(task => 
    (status === 'Done' && task.completed) ||
    (status === 'To Do' && !task.completed && task.status === 'To Do') ||
    (status === 'In Progress' && !task.completed && task.status === 'In Progress')
  )
}

const completedTasks = computed(() => {
  return filteredTasks.value.filter(task => task.completed).length
})

const efficiency = computed(() => {
  if (filteredTasks.value.length === 0) return 0
  return Math.round((completedTasks.value / filteredTasks.value.length) * 100)
})

const overdueTasks = computed(() => {
  const today = new Date()
  return filteredTasks.value.filter(task => 
    !task.completed && new Date(task.due_date) < today
  ).length
})

const logout = () => {
  store.dispatch('logout')
  router.push('/auth/sign-in')
}

const startDrag = (evt, task) => {
  evt.dataTransfer.effectAllowed = 'move'
  evt.dataTransfer.setData('taskID', task.id.toString())
}

const onDrop = async (evt, newStatus) => {
  const taskID = evt.dataTransfer.getData('taskID')
  if (!taskID) {
    console.error("Task ID not found in dataTransfer")
    return
  }

  const task = tasks.value.find(task => task.id === parseInt(taskID))

  if (task && task.status !== newStatus) {
    try {
      await store.dispatch('updateTask', {
        ...task,
        status: newStatus,
        completed: newStatus === 'Done'
      })
      console.log("Task updated to new status:", newStatus)
      await store.dispatch('fetchTasks', selectedProject.value)
    } catch (error) {
      console.error('Failed to update task status:', error)
    }
  }
}

const moveToInProgress = async (task) => {
  await store.dispatch('updateTask', {
    ...task,
    status: 'In Progress'
  })
  await store.dispatch('fetchTasks', selectedProject.value)
}
</script>

<style scoped>
@keyframes glitch {
  0% {
    text-shadow: 
      0.05em 0 0 rgba(255, 255, 0, 0.75),
      -0.05em -0.025em 0 rgba(255, 255, 0, 0.75),
      -0.025em 0.05em 0 rgba(255, 255, 0, 0.75);
  }
  14% {
    text-shadow: 
      0.05em 0 0 rgba(255, 255, 0, 0.75),
      -0.05em -0.025em 0 rgba(255, 255, 0, 0.75),
      -0.025em 0.05em 0 rgba(255, 255, 0, 0.75);
  }
  15% {
    text-shadow: 
      -0.05em -0.025em 0 rgba(255, 255, 0, 0.75),
      0.025em 0.025em 0 rgba(255, 255, 0, 0.75),
      -0.05em -0.05em 0 rgba(255, 255, 0, 0.75);
  }
  49% {
    text-shadow: 
      -0.05em -0.025em 0 rgba(255, 255, 0, 0.75),
      0.025em 0.025em 0 rgba(255, 255, 0, 0.75),
      -0.05em -0.05em 0 rgba(255, 255, 0, 0.75);
  }
  50% {
    text-shadow: 0.025em 0.05em 0 rgba(255, 255, 0, 0.75),
      0.05em 0 0 rgba(255, 255, 0, 0.75),
      0 -0.05em 0 rgba(255, 255, 0, 0.75);
  }
  99% {
    text-shadow: 
      0.025em 0.05em 0 rgba(255, 255, 0, 0.75),
      0.05em 0 0 rgba(255, 255, 0, 0.75),
      0 -0.05em 0 rgba(255, 255, 0, 0.75);
  }
  100% {
    text-shadow: 
      -0.025em 0 0 rgba(255, 255, 0, 0.75),
      -0.025em -0.025em 0 rgba(255, 255, 0, 0.75),
      -0.025em -0.05em 0 rgba(255, 255, 0, 0.75);
  }
}
</style>