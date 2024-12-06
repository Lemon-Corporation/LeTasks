<template>
  <div class="min-h-screen bg-gradient-to-b from-emerald-600 via-teal-800 to-slate-900 p-2 sm:p-4 md:p-6">
    <nav class="bg-black/30 backdrop-blur-xl border border-emerald-500/20 rounded-2xl p-4 mb-6 shadow-lg shadow-emerald-900/20">
      <div class="max-w-7xl mx-auto flex justify-between items-center">
        <h1 class="text-3xl sm:text-4xl font-mono text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 to-teal-300 glitch-text flex items-center">
          <ClipboardList class="w-8 h-8 mr-2" />
          Le Tasks -> PANEL
        </h1>
        <button @click="logout" class="text-emerald-400 hover:text-emerald-300 font-mono transition-all duration-300 flex items-center">
          <LogOut class="w-5 h-5 mr-1" />
          [ LOGOUT ]
        </button>
      </div>
    </nav>

    <div class="max-w-6xl mx-auto space-y-8">
      <!-- Projects Section -->
      <div class="bg-black/30 backdrop-blur-xl border border-emerald-500/20 rounded-2xl p-6 shadow-lg shadow-emerald-900/20">
        <h2 class="text-xl font-mono text-emerald-400 mb-4 flex items-center">
          <Folder class="w-5 h-5 mr-2" />
          Projects
        </h2>
        <div class="flex space-x-4 mb-4">
          <input
            v-model="newProjectName"
            type="text"
            placeholder="New Project Name"
            class="flex-grow bg-black/50 border border-emerald-500/30 rounded-xl px-4 py-2 text-emerald-300 font-mono focus:outline-none focus:border-emerald-400 focus:ring-1 focus:ring-emerald-400 placeholder-emerald-700"
          />
          <button
            @click="createProject"
            class="bg-emerald-500/10 hover:bg-emerald-500/20 border border-emerald-500/50 text-emerald-400 font-mono px-4 py-2 rounded-xl transition-all duration-300 flex items-center"
          >
            <PlusCircle class="w-5 h-5 mr-2" />
            Create Project
          </button>
        </div>
        <div v-if="projects.length" class="space-y-4">
          <div v-for="project in projects" :key="project.id" class="bg-black/50 border border-emerald-500/20 rounded-xl p-4">
            <h3 class="text-lg font-mono text-emerald-300 mb-2">{{ project.name }}</h3>
            <div class="flex space-x-2 mb-2">
              <select
                v-model="selectedUsers[project.id]"
                class="bg-black/50 border border-emerald-500/30 rounded-xl px-4 py-2 text-emerald-300 font-mono focus:outline-none focus:border-emerald-400 focus:ring-1 focus:ring-emerald-400"
              >
                <option value="">Select User</option>
                <option v-for="user in getAvailableUsers(project)" :key="user.id" :value="user.id">
                  {{ user.username }}
                </option>
              </select>
              <button
                @click="addUserToProject(project.id)"
                class="bg-emerald-500/10 hover:bg-emerald-500/20 border border-emerald-500/50 text-emerald-400 font-mono px-3 py-1 rounded-xl transition-all duration-300 flex items-center"
              >
                <UserPlus class="w-4 h-4 mr-1" />
                Add User
              </button>
            </div>
            <div v-if="project.users && project.users.length" class="space-y-2">
              <div v-for="user in project.users" :key="user.id" class="flex justify-between items-center bg-black/50 p-2 rounded-xl">
                <span class="text-emerald-300 font-mono">{{ user.username }}</span>
                <button
                  @click="removeUserFromProject(project.id, user.id)"
                  class="text-red-400 hover:text-red-300 font-mono flex items-center"
                >
                  <UserMinus class="w-4 h-4 mr-1" />
                  Remove
                </button>
              </div>
            </div>
            <p v-else class="text-emerald-600 font-mono">No users assigned to this project.</p>
          </div>
        </div>
        <p v-else class="text-emerald-600 font-mono">No projects found.</p>
      </div>

      <!-- Users Section -->
      <div class="bg-black/30 backdrop-blur-xl border border-emerald-500/20 rounded-2xl p-6 shadow-lg shadow-emerald-900/20">
        <h2 class="text-xl font-mono text-emerald-400 mb-4 flex items-center">
          <Users class="w-5 h-5 mr-2" />
          Users
        </h2>
        <div v-if="users.length" class="space-y-2">
          <div v-for="user in users" :key="user.id" class="bg-black/50 border border-emerald-500/20 p-3 rounded-xl">
            <span class="text-emerald-300 font-mono">{{ user.username }} ({{ user.email }})</span>
          </div>
        </div>
        <p v-else class="text-emerald-600 font-mono">No users found.</p>
      </div>
    </div>

    <!-- Create Task Modal -->
    <div v-if="showModal" class="fixed inset-0 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4 z-50">
      <div class="bg-black/90 border border-emerald-500/20 rounded-2xl p-6 w-full max-w-md shadow-2xl shadow-emerald-900/20">
        <h3 class="text-xl font-mono text-emerald-400 mb-4 flex items-center">
          <PlusCircle class="w-5 h-5 mr-2" />
          Create Task for User
        </h3>
        <form @submit.prevent="createTask" class="space-y-4">
          <input
            v-model="newTask.title"
            type="text"
            placeholder="Task Title"
            required
            class="w-full bg-black/50 border border-emerald-500/30 rounded-xl px-4 py-2 text-emerald-300 font-mono focus:outline-none focus:border-emerald-400 focus:ring-1 focus:ring-emerald-400 placeholder-emerald-700"
          />
          <textarea
            v-model="newTask.description"
            placeholder="Task Description"
            class="w-full bg-black/50 border border-emerald-500/30 rounded-xl px-4 py-2 text-emerald-300 font-mono focus:outline-none focus:border-emerald-400 focus:ring-1 focus:ring-emerald-400 placeholder-emerald-700"
          ></textarea>
          <select
            v-model="newTask.status"
            required
            class="w-full bg-black/50 border border-emerald-500/30 rounded-xl px-4 py-2 text-emerald-300 font-mono focus:outline-none focus:border-emerald-400 focus:ring-1 focus:ring-emerald-400"
          >
            <option value="To Do">To Do</option>
            <option value="In Progress">In Progress</option>
            <option value="Done">Done</option>
          </select>
          <select
            v-model="newTask.priority"
            required
            class="w-full bg-black/50 border border-emerald-500/30 rounded-xl px-4 py-2 text-emerald-300 font-mono focus:outline-none focus:border-emerald-400 focus:ring-1 focus:ring-emerald-400"
          >
            <option value="low">Low</option>
            <option value="medium">Medium</option>
            <option value="high">High</option>
          </select>
          <input
            v-model="newTask.due_date"
            type="date"
            required
            class="w-full bg-black/50 border border-emerald-500/30 rounded-xl px-4 py-2 text-emerald-300 font-mono focus:outline-none focus:border-emerald-400 focus:ring-1 focus:ring-emerald-400"
          />
          <select
            v-model="newTask.project_id"
            required
            class="w-full bg-black/50 border border-emerald-500/30 rounded-xl px-4 py-2 text-emerald-300 font-mono focus:outline-none focus:border-emerald-400 focus:ring-1 focus:ring-emerald-400"
          >
            <option v-for="project in projects" :key="project.id" :value="project.id">
              {{ project.name }}
            </option>
          </select>
          <div class="flex justify-end space-x-2">
            <button
              type="button"
              @click="showModal = false"
              class="bg-gray-600/20 hover:bg-gray-600/30 border border-gray-600/50 text-gray-300 font-mono px-4 py-2 rounded-xl transition-all duration-300 flex items-center"
            >
              <X class="w-4 h-4 mr-1" />
              Cancel
            </button>
            <button
              type="submit"
              class="bg-emerald-500/20 hover:bg-emerald-500/30 border border-emerald-500/50 text-emerald-400 font-mono px-4 py-2 rounded-xl transition-all duration-300 flex items-center"
            >
              <Check class="w-4 h-4 mr-1" />
              Create Task
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import { 
  ClipboardList, LogOut, Folder, PlusCircle, UserPlus, UserMinus, Users,
  Check, X
} from 'lucide-vue-next'

const store = useStore()
const router = useRouter()

const users = ref([])
const projects = ref([])
const selectedUsers = ref({})
const newProjectName = ref('')
const showModal = ref(false)
const selectedUserId = ref(null)
const newTask = ref({
  title: '',
  description: '',
  status: 'To Do',
  priority: 'medium',
  due_date: '',
  project_id: null
})

const user = computed(() => store.state.user)

onMounted(async () => {
  await fetchUsers()
  await fetchProjects()
})

async function fetchUsers() {
  try {
    const response = await fetch('/api/admin/users', {
      headers: { Authorization: `Bearer ${store.state.token}` }
    })
    if (response.ok) {
      users.value = await response.json()
    } else {
      console.error('Failed to fetch users')
    }
  } catch (error) {
    console.error('Error fetching users:', error)
  }
}

async function fetchProjects() {
  try {
    const response = await fetch('/api/projects/', {
      headers: { Authorization: `Bearer ${store.state.token}` }
    })
    if (response.ok) {
      projects.value = await response.json()
    } else {
      console.error('Failed to fetch projects')
    }
  } catch (error) {
    console.error('Error fetching projects:', error)
  }
}

async function createProject() {
  if (!newProjectName.value.trim()) return

  try {
    const response = await fetch('/api/projects/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${store.state.token}`
      },
      body: JSON.stringify({ name: newProjectName.value.trim() })
    })
    if (response.ok) {
      const newProject = await response.json()
      projects.value.push(newProject)
      newProjectName.value = ''
    } else {
      console.error('Failed to create project')
    }
  } catch (error) {
    console.error('Error creating project:', error)
  }
}

function getAvailableUsers(project) {
  return users.value.filter(user => !project.users || !project.users.some(projectUser => projectUser.id === user.id))
}

async function addUserToProject(projectId) {
  const userId = selectedUsers.value[projectId]
  if (!userId) return

  try {
    console.log("Assigning user to project", { user_id: userId, project_id: projectId });
    const response = await fetch('/api/admin/assign-project', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${store.state.token}`
      },
      body: JSON.stringify({ user_id: userId, project_id: projectId })
    })
    if (response.ok) {
      alert('User added to project successfully')
      await fetchProjects()
      selectedUsers.value[projectId] = ''
    } else {
      console.error('Failed to add user to project')
    }
  } catch (error) {
    console.error('Error adding user to project:', error)
  }
}

async function removeUserFromProject(projectId, userId) {
  try {
    const response = await fetch('/api/admin/remove-user-from-project', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${store.state.token}`
      },
      body: JSON.stringify({ user_id: userId, project_id: projectId })
    })
    if (response.ok) {
      alert('User removed from project successfully')
      await fetchProjects()
    } else {
      console.error('Failed to remove user from project')
    }
  } catch (error) {
    console.error('Error removing user from project:', error)
  }
}

function showCreateTaskModal(userId) {
  selectedUserId.value = userId
  showModal.value = true
}

async function createTask() {
  if (!selectedUserId.value) return

  try {
    const response = await fetch('/api/admin/create-task-for-user', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${store.state.token}`
      },
      body: JSON.stringify({ ...newTask.value, assignee_id: selectedUserId.value })
    })
    if (response.ok) {
      alert('Task created successfully')
      showModal.value = false
      newTask.value = {
        title: '',
        description: '',
        status: 'To Do',
        priority: 'medium',
        due_date: '',
        project_id: null
      }
    } else {
      console.error('Failed to create task')
    }
  } catch (error) {
    console.error('Error creating task:', error)
  }
}

function logout() {
  store.dispatch('logout')
  router.push('/auth/sign-in')
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