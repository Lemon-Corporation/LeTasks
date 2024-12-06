<template>
  <div class="min-h-screen bg-gradient-to-b from-emerald-600 via-teal-800 to-slate-900 p-2 sm:p-4 md:p-6">
    <!-- Navbar with frosted glass effect -->
    <nav class="bg-black/30 backdrop-blur-xl border border-emerald-500/20 rounded-2xl p-4 mb-6 shadow-lg shadow-emerald-900/20">
      <div class="max-w-7xl mx-auto flex flex-col sm:flex-row justify-between items-center">
        <h1 class="text-3xl sm:text-4xl font-mono text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 to-teal-300 mb-4 sm:mb-0 glitch-text flex items-center">
          <ClipboardList class="w-8 h-8 mr-2" />
          Le Tasks
        </h1>
        <div class="flex flex-col sm:flex-row items-center space-y-4 sm:space-y-0 sm:space-x-4">
          <select
            v-model="selectedProject"
            @change="changeProject"
            class="w-full sm:w-auto bg-black/50 border border-emerald-500/30 rounded-xl px-4 py-2 text-emerald-300 font-mono focus:outline-none focus:border-emerald-400 focus:ring-1 focus:ring-emerald-400 mb-2 sm:mb-0 transition-all duration-300"
          >
            <option value="">All Projects</option>
            <option v-for="project in projects" :key="project.id" :value="project.id">{{ project.name }}</option>
          </select>
          <div v-if="user" class="flex items-center space-x-4">
            <a href="/profile" class="flex items-center space-x-3 bg-black/30 rounded-xl px-4 py-2 border border-emerald-500/20 hover:border-emerald-500/40 transition-all duration-300">
              <img :src="user.avatar" alt="User Avatar" class="w-8 h-8 rounded-lg border border-emerald-500/30">
              <span class="text-emerald-300 font-mono">{{ user.username }}</span>
            </a>
            <button 
              @click="logout" 
              class="text-emerald-400 hover:text-emerald-300 font-mono transition-all duration-300 flex items-center"
            >
              <LogOut class="w-5 h-5 mr-1" />
              [ LOGOUT ]
            </button>
          </div>
          <button
            v-else
            @click="$router.push('/auth/sign-in')"
            class="w-full sm:w-auto bg-emerald-500/10 hover:bg-emerald-500/20 border border-emerald-500/50 text-emerald-400 font-mono px-6 py-2 rounded-xl transition-all duration-300 hover:shadow-lg hover:shadow-emerald-500/20 flex items-center justify-center"
          >
            <LogIn class="w-5 h-5 mr-2" />
            [ LOGIN ]
          </button>
        </div>
      </div>
    </nav>
  
    <div class="max-w-6xl mx-auto">
      <!-- Task Input Section -->
      <div class="bg-black/30 backdrop-blur-xl border border-emerald-500/20 rounded-2xl p-4 sm:p-6 mb-6 shadow-lg shadow-emerald-900/20">
        <form @submit.prevent="addTask" class="space-y-4">
          <div class="flex flex-col sm:flex-row gap-4">
            <div class="relative flex-grow">
              <input
                v-model="newTask.title"
                type="text"
                placeholder="INITIALIZE NEW TASK"
                required
                class="w-full bg-black/50 border border-emerald-500/30 rounded-xl pl-10 pr-4 py-3 text-emerald-300 font-mono focus:outline-none focus:border-emerald-400 focus:ring-1 focus:ring-emerald-400 placeholder-emerald-700 transition-all duration-300"
              />
              <PlusCircle class="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-emerald-500" />
            </div>
            <select
              v-model="newTask.priority"
              required
              class="w-full sm:w-auto bg-black/50 border border-emerald-500/30 rounded-xl px-4 py-3 text-emerald-300 font-mono focus:outline-none focus:border-emerald-400 focus:ring-1 focus:ring-emerald-400 transition-all duration-300"
            >
              <option value="low">LOW PRIORITY</option>
              <option value="medium">MEDIUM PRIORITY</option>
              <option value="high">HIGH PRIORITY</option>
            </select>
          </div>
          <div class="flex flex-col sm:flex-row gap-4">
            <div class="relative flex-grow">
              <input
                v-model="newTask.due_date"
                type="text"
                placeholder="DD.MM"
                required
                class="w-full sm:w-auto bg-black/50 border border-emerald-500/30 rounded-xl pl-10 pr-4 py-3 text-emerald-300 font-mono focus:outline-none focus:border-emerald-400 focus:ring-1 focus:ring-emerald-400 placeholder-emerald-700 transition-all duration-300"
              />
              <Calendar class="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-emerald-500" />
            </div>
            <div class="relative flex-grow">
              <select
                v-model="newTask.assignee"
                class="w-full bg-black/50 border border-emerald-500/30 rounded-xl pl-10 pr-4 py-3 text-emerald-300 font-mono focus:outline-none focus:border-emerald-400 focus:ring-1 focus:ring-emerald-400 transition-all duration-300"
                :disabled="!selectedProject"
              >
                <option value="">Select User</option>
                <option v-for="user in projectUsers" :key="user.id" :value="user.username">
                  {{ user.username }}
                </option>
              </select>
              <User class="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-emerald-500" />
            </div>
          </div>
          <div class="relative">
            <textarea
              v-model="newTask.description"
              placeholder="Task description"
              rows="3"
              class="w-full bg-black/50 border border-emerald-500/30 rounded-xl pl-10 pr-4 py-3 text-emerald-300 font-mono focus:outline-none focus:border-emerald-400 focus:ring-1 focus:ring-emerald-400 placeholder-emerald-700 transition-all duration-300"
            ></textarea>
            <AlignLeft class="absolute left-3 top-3 w-5 h-5 text-emerald-500" />
          </div>
          <button
            type="submit"
            class="w-full bg-emerald-500/10 hover:bg-emerald-500/20 border border-emerald-500/50 text-emerald-400 font-mono py-3 rounded-xl transition-all duration-300 hover:shadow-lg hover:shadow-emerald-500/20 relative overflow-hidden group flex items-center justify-center"
          >
            <span class="relative z-10 flex items-center">
              <Send class="w-5 h-5 mr-2" />
              [ INITIALIZE TASK ]
            </span>
            <div class="absolute inset-0 bg-gradient-to-r from-emerald-500/0 via-emerald-500/10 to-emerald-500/0 transform translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-1000"></div>
          </button>
        </form>
      </div>
  
      <!-- Stats Grid -->
      <div class="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-6">
        <div class="bg-black/30 backdrop-blur-xl border border-emerald-500/20 rounded-2xl p-4 shadow-lg shadow-emerald-900/20 hover:border-emerald-500/40 transition-all duration-300">
          <div class="text-emerald-500 font-mono text-sm mb-2 flex items-center">
            <ListTodo class="w-4 h-4 mr-2" />
            TOTAL TASKS
          </div>
          <div class="text-emerald-300 font-mono text-2xl sm:text-3xl">{{ filteredTasks.length }}</div>
        </div>
        <div class="bg-black/30 backdrop-blur-xl border border-emerald-500/20 rounded-2xl p-4 shadow-lg shadow-emerald-900/20 hover:border-emerald-500/40 transition-all duration-300">
          <div class="text-emerald-500 font-mono text-sm mb-2 flex items-center">
            <CheckSquare class="w-4 h-4 mr-2" />
            COMPLETED
          </div>
          <div class="text-emerald-300 font-mono text-2xl sm:text-3xl">{{ completedTasks }}</div>
        </div>
        <div class="bg-black/30 backdrop-blur-xl border border-emerald-500/20 rounded-2xl p-4 shadow-lg shadow-emerald-900/20 hover:border-emerald-500/40 transition-all duration-300">
          <div class="text-emerald-500 font-mono text-sm mb-2 flex items-center">
            <TrendingUp class="w-4 h-4 mr-2" />
            EFFICIENCY
          </div>
          <div class="text-emerald-300 font-mono text-2xl sm:text-3xl">{{ efficiency }}%</div>
        </div>
        <div class="bg-black/30 backdrop-blur-xl border border-emerald-500/20 rounded-2xl p-4 shadow-lg shadow-emerald-900/20 hover:border-emerald-500/40 transition-all duration-300">
          <div class="text-emerald-500 font-mono text-sm mb-2 flex items-center">
            <AlertTriangle class="w-4 h-4 mr-2" />
            OVERDUE
          </div>
          <div class="text-emerald-300 font-mono text-2xl sm:text-3xl">{{ overdueTasks }}</div>
        </div>
      </div>
  
      <!-- Kanban Board -->
      <div class="space-y-6 md:space-y-0 md:grid md:grid-cols-3 md:gap-6">
        <div 
          v-for="status in ['To Do', 'In Progress', 'Done']" 
          :key="status" 
          class="bg-black/30 backdrop-blur-xl border border-emerald-500/20 rounded-2xl p-4 sm:p-6 shadow-lg shadow-emerald-900/20"
          @drop="onDrop($event, status)"
          @dragover.prevent
          @dragenter.prevent
        >
          <h2 class="text-lg font-mono text-emerald-400 mb-4 sm:mb-6 flex items-center">
            <component :is="getStatusIcon(status)" class="w-5 h-5 mr-2" />
            {{ status }}
          </h2>
          <div class="space-y-4">
            <div
              v-for="task in getTasksByStatus(status)"
              :key="task.id"
              class="group bg-black/50 border border-emerald-500/20 rounded-xl p-4 cursor-move hover:border-emerald-500/40 transition-all duration-300"
              draggable="true"
              @dragstart="startDrag($event, task)"
              @click="openTaskDetails(task)"
            >
              <div class="flex items-center justify-between mb-3">
                <span class="font-mono text-emerald-300 text-sm sm:text-base" :class="{ 'line-through': task.completed }">{{ task.title }}</span>
                <span
                  class="px-2 py-1 rounded-lg text-xs font-mono flex items-center"
                  :class="{
                    'bg-red-500/20 text-red-400 border border-red-500/30': task.priority === 'high',
                    'bg-yellow-500/20 text-yellow-400 border border-yellow-500/30': task.priority === 'medium',
                    'bg-blue-500/20 text-blue-400 border border-blue-500/30': task.priority === 'low'
                  }"
                >
                  <component :is="getPriorityIcon(task.priority)" class="w-3 h-3 mr-1" />
                  {{ task.priority.toUpperCase() }}
                </span>
              </div>
              <div class="flex items-center justify-between text-xs sm:text-sm">
                <span class="text-emerald-600 font-mono flex items-center">
                  <Calendar class="w-3 h-3 mr-1" />
                  {{ formatDate(task.due_date) }}
                </span>
                <span class="text-emerald-400 font-mono flex items-center">
                  <User class="w-3 h-3 mr-1" />
                  {{ task.assignee ? task.assignee.username : 'Unassigned' }}
                </span>
              </div>
              <div v-if="task.description" class="mt-3 text-emerald-500/80 text-xs sm:text-sm truncate">
                {{ task.description }}
              </div>
              <div class="mt-4 flex flex-wrap justify-end gap-2 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                <button
                  v-if="task.status !== 'In Progress'"
                  @click.stop="moveToInProgress(task)"
                  class="bg-emerald-500/10 hover:bg-emerald-500/20 border border-emerald-500/50 text-emerald-400 font-mono px-2 py-1 rounded-lg text-xs transition-all duration-300 flex items-center"
                >
                  <Play class="w-3 h-3 mr-1" />
                  Start
                </button>
                <button
                  v-if="!task.completed"
                  @click.stop="toggleTaskStatus(task)"
                  class="bg-green-500/10 hover:bg-green-500/20 border border-green-500/50 text-green-400 font-mono px-2 py-1 rounded-lg text-xs transition-all duration-300 flex items-center"
                >
                  <CheckCircle class="w-3 h-3 mr-1" />
                  Complete
                </button>
                <button
                  v-else
                  @click.stop="toggleTaskStatus(task)"
                  class="bg-emerald-500/10 hover:bg-emerald-500/20 border border-emerald-500/50 text-emerald-400 font-mono px-2 py-1 rounded-lg text-xs transition-all duration-300 flex items-center"
                >
                  <RefreshCw class="w-3 h-3 mr-1" />
                  Reopen
                </button>
                <button
                  v-if="task.completed"
                  @click.stop="deleteTask(task.id)"
                  class="bg-red-500/10 hover:bg-red-500/20 border border-red-500/50 text-red-400 font-mono px-2 py-1 rounded-lg text-xs transition-all duration-300 flex items-center"
                >
                  <Trash2 class="w-3 h-3 mr-1" />
                  Delete
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Task Details Modal -->
      <div v-if="selectedTask" class="fixed inset-0 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4 z-50">
        <div class="bg-black/90 border border-emerald-500/20 rounded-2xl p-6 w-full max-w-md shadow-2xl shadow-emerald-900/20">
          <h2 class="text-xl sm:text-2xl font-mono text-emerald-400 mb-4 flex items-center">
            <ClipboardList class="w-6 h-6 mr-2" />
            {{ selectedTask.title }}
          </h2>
          <div class="mb-4">
            <label class="block text-emerald-500 font-mono mb-2 flex items-center">
              <AlignLeft class="w-4 h-4 mr-2" />
              Description
            </label>
            <textarea
              v-model="selectedTask.description"
              class="w-full bg-black/50 border border-emerald-500/30 rounded-xl px-4 py-3 text-emerald-300 font-mono focus:outline-none focus:border-emerald-400 focus:ring-1 focus:ring-emerald-400"
              rows="4"
            ></textarea>
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-4">
            <div>
              <label class="block text-emerald-500 font-mono mb-2 flex items-center">
                <ListTodo class="w-4 h-4 mr-2" />
                Status
              </label>
              <select 
                v-model="selectedTask.status" 
                class="w-full bg-black/50 border border-emerald-500/30 rounded-xl px-4 py-3 text-emerald-300 font-mono focus:outline-none focus:border-emerald-400 focus:ring-1 focus:ring-emerald-400"
              >
                <option value="To Do">To Do</option>
                <option value="In Progress">In Progress</option>
                <option value="Done">Done</option>
              </select>
            </div>
            <div>
              <label class="block text-emerald-500 font-mono mb-2 flex items-center">
                <Flag class="w-4 h-4 mr-2" />
                Priority
              </label>
              <select 
                v-model="selectedTask.priority" 
                class="w-full bg-black/50 border border-emerald-500/30 rounded-xl px-4 py-3 text-emerald-300 font-mono focus:outline-none focus:border-emerald-400 focus:ring-1 focus:ring-emerald-400"
              >
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
              </select>
            </div>
          </div>
          <div class="mb-4">
            <label class="block text-emerald-500 font-mono mb-2 flex items-center">
              <User class="w-4 h-4 mr-2" />
              Assignee
            </label>
            <select 
              v-model="selectedTask.assignee" 
              class="w-full bg-black/50 border border-emerald-500/30 rounded-xl px-4 py-3 text-emerald-300 font-mono focus:outline-none focus:border-emerald-400 focus:ring-1 focus:ring-emerald-400"
            >
              <option value="">Unassigned</option>
              <option v-for="user in projectUsers" :key="user.id" :value="user.username">
                {{ user.username }}
              </option>
            </select>
          </div>
          <div class="mb-6">
            <label class="block text-emerald-500 font-mono mb-2 flex items-center">
              <Calendar class="w-4 h-4 mr-2" />
              Due Date (DD.MM)
            </label>
            <input
              v-model="selectedTask.due_date"
              type="text"
              placeholder="DD.MM"
              class="w-full bg-black/50 border border-emerald-500/30 rounded-xl px-4 py-3 text-emerald-300 font-mono focus:outline-none focus:border-emerald-400 focus:ring-1 focus:ring-emerald-400"
            />
          </div>
          <div class="flex flex-wrap justify-end gap-4">
            <button 
              @click="closeTaskDetails" 
              class="bg-gray-800 hover:bg-gray-700 text-gray-300 px-4 py-2 rounded-xl font-mono transition-all duration-300 flex items-center"
            >
              <X class="w-4 h-4 mr-2" />
              Close
            </button>
            <button 
              @click="saveTaskDetails" 
              class="bg-emerald-500/20 hover:bg-emerald-500/30 border border-emerald-500/50 text-emerald-400 px-4 py-2 rounded-xl font-mono transition-all duration-300 flex items-center"
            >
              <Save class="w-4 h-4 mr-2" />
              Save
            </button>
            <button
              v-if="selectedTask.completed"
              @click="deleteTask(selectedTask.id)"
              class="bg-red-500/20 hover:bg-red-500/30 border border-red-500/50 text-red-400 px-4 py-2 rounded-xl font-mono transition-all duration-300 flex items-center"
            >
              <Trash2 class="w-4 h-4 mr-2" />
              Delete
            </button>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div 
        v-if="filteredTasks.length === 0" 
        class="text-center py-12 sm:py-16 border border-emerald-500/20 rounded-2xl mt-6 sm:mt-8 bg-black/30 backdrop-blur-xl"
      >
        <Inbox class="w-12 h-12 mx-auto mb-4 text-emerald-500" />
        <div class="text-emerald-400 font-mono mb-3 text-lg sm:text-xl">/ / SYSTEM IDLE / /</div>
        <div class="text-emerald-600 font-mono text-sm">NO ACTIVE TASKS DETECTED</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { 
  ClipboardList, LogOut, LogIn, PlusCircle, Calendar, User, AlignLeft, Send,
  ListTodo, CheckSquare, TrendingUp, AlertTriangle, Play, CheckCircle, RefreshCw,
  Trash2, Flag, X, Save, Inbox
} from 'lucide-vue-next'

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
      //router.push('/auth/sign-in')
    }
  } else {
    //router.push('/auth/sign-in')
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
   // router.push('/auth/sign-in')
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
  const taskID = evt.dataTransfer.getData('taskID');
  if (!taskID) {
    console.error("Task ID not found in dataTransfer");
    return;
  }

  const task = tasks.value.find(task => task.id === parseInt(taskID));

  if (task && task.status !== newStatus) {
    try {
      const updatedTask = {
        status: newStatus,
        completed: newStatus === 'Done',
        assignee: task.assignee ? task.assignee.username : null, // Отправляем только имя пользователя
        project_id: task.project.id, // Отправляем только ID проекта
      };
      console.log("Updating task with data:", updatedTask);
      await store.dispatch('updateTask', updatedTask);
      console.log("Task updated to new status:", newStatus);
      await store.dispatch('fetchTasks', selectedProject.value);
    } catch (error) {
      console.error('Failed to update task status:', error);
    }
  }
};

const moveToInProgress = async (task) => {
  await store.dispatch('updateTask', {
    ...task,
    status: 'In Progress'
  })
  await store.dispatch('fetchTasks', selectedProject.value)
}

const getStatusIcon = (status) => {
  switch (status) {
    case 'To Do':
      return ListTodo
    case 'In Progress':
      return Play
    case 'Done':
      return CheckSquare
    default:
      return ListTodo
  }
}

const getPriorityIcon = (priority) => {
  switch (priority) {
    case 'high':
      return AlertTriangle
    case 'medium':
      return Flag
    case 'low':
      return TrendingUp
    default:
      return Flag
  }
}
</script>

<style scoped>
@keyframes glitch {
  0% {
    text-shadow: 
      0.05em 0 0 rgba(0, 255, 0, 0.75),
      -0.05em -0.025em 0 rgba(0, 255, 0, 0.75),
      -0.025em 0.05em 0 rgba(0, 255, 0, 0.75);
  }
  15% {
    text-shadow: 
      -0.05em -0.025em 0 rgba(0, 255, 0, 0.75),
      0.025em 0.025em 0 rgba(0, 255, 0, 0.75),
      -0.05em -0.05em 0 rgba(0, 255, 0, 0.75);
  }
  50% {
    text-shadow: 
      0.025em 0.05em 0 rgba(0, 255, 0, 0.75),
      0.05em 0 0 rgba(0, 255, 0, 0.75),
      0 -0.05em 0 rgba(0, 255, 0, 0.75);
  }
  100% {
    text-shadow: 
      0.05em 0 0 rgba(0, 255, 0, 0.75),
      -0.05em -0.025em 0 rgba(0, 255, 0, 0.75),
      -0.025em 0.05em 0 rgba(0, 255, 0, 0.75);
  }
}
</style>