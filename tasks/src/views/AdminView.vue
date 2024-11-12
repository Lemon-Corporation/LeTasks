<template>
    <div class="min-h-screen bg-black p-4 sm:p-6">
      <nav class="bg-gray-900/50 backdrop-blur-sm border border-yellow-600/20 rounded-lg p-4 mb-6">
        <div class="max-w-7xl mx-auto flex justify-between items-center">
          <h1 class="text-2xl font-mono text-white">Le Tasks -> PANEL</h1>
          <button @click="logout" class="text-yellow-500 hover:text-yellow-400">Logout</button>
        </div>
      </nav>
  
      <div class="max-w-4xl mx-auto space-y-8">
        <!-- Projects Section -->
        <div class="bg-gray-900/50 backdrop-blur-sm border border-yellow-600/20 rounded-lg p-6">
          <h2 class="text-xl font-mono text-yellow-500 mb-4">Projects</h2>
          <div class="flex space-x-4 mb-4">
            <input
              v-model="newProjectName"
              type="text"
              placeholder="New Project Name"
              class="flex-grow bg-black border border-yellow-600/30 rounded px-4 py-2 text-white font-mono focus:outline-none focus:border-yellow-500 placeholder-gray-600"
            />
            <button
              @click="createProject"
              class="bg-yellow-600/20 hover:bg-yellow-600/30 border border-yellow-600/50 text-yellow-500 font-mono px-4 py-2 rounded transition-all duration-300"
            >
              Create Project
            </button>
          </div>
          <div v-if="projects.length" class="space-y-4">
            <div v-for="project in projects" :key="project.id" class="bg-gray-800/50 p-4 rounded-lg">
              <h3 class="text-lg font-mono text-white mb-2">{{ project.name }}</h3>
              <div class="flex space-x-2 mb-2">
                <select
                  v-model="selectedUsers[project.id]"
                  class="bg-black border border-yellow-600/30 rounded px-2 py-1 text-white font-mono focus:outline-none focus:border-yellow-500"
                >
                  <option value="">Select User</option>
                  <option v-for="user in getAvailableUsers(project)" :key="user.id" :value="user.id">
                    {{ user.username }}
                  </option>
                </select>
                <button
                  @click="addUserToProject(project.id)"
                  class="bg-yellow-600/20 hover:bg-yellow-600/30 border border-yellow-600/50 text-yellow-500 font-mono px-3 py-1 rounded transition-all duration-300"
                >
                  Add User
                </button>
              </div>
              <div v-if="project.users && project.users.length" class="space-y-2">
                <div v-for="user in project.users" :key="user.id" class="flex justify-between items-center bg-gray-700/50 p-2 rounded">
                  <span class="text-white font-mono">{{ user.username }}</span>
                  <button
                    @click="removeUserFromProject(project.id, user.id)"
                    class="text-red-500 hover:text-red-400 font-mono"
                  >
                    Remove
                  </button>
                </div>
              </div>
              <p v-else class="text-gray-500 font-mono">No users assigned to this project.</p>
            </div>
          </div>
          <p v-else class="text-gray-500 font-mono">No projects found.</p>
        </div>
  
        <!-- Users Section -->
        <div class="bg-gray-900/50 backdrop-blur-sm border border-yellow-600/20 rounded-lg p-6">
          <h2 class="text-xl font-mono text-yellow-500 mb-4">Users</h2>
          <div v-if="users.length" class="space-y-2">
            <div v-for="user in users" :key="user.id" class="bg-gray-800/50 p-3 rounded-lg">
              <span class="text-white font-mono">{{ user.username }} ({{ user.email }})</span>
            </div>
          </div>
          <p v-else class="text-gray-500 font-mono">No users found.</p>
        </div>
      </div>
  
      <!-- Create Task Modal -->
      <div v-if="showModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
        <div class="bg-gray-900 border border-yellow-600/20 rounded-lg p-6 w-full max-w-md">
          <h3 class="text-xl font-mono text-yellow-500 mb-4">Create Task for User</h3>
          <form @submit.prevent="createTask" class="space-y-4">
            <input
              v-model="newTask.title"
              type="text"
              placeholder="Task Title"
              required
              class="w-full bg-black border border-yellow-600/30 rounded px-4 py-2 text-white font-mono focus:outline-none focus:border-yellow-500 placeholder-gray-600"
            />
            <textarea
              v-model="newTask.description"
              placeholder="Task Description"
              class="w-full bg-black border border-yellow-600/30 rounded px-4 py-2 text-white font-mono focus:outline-none focus:border-yellow-500 placeholder-gray-600"
            ></textarea>
            <select
              v-model="newTask.status"
              required
              class="w-full bg-black border border-yellow-600/30 rounded px-4 py-2 text-white font-mono focus:outline-none focus:border-yellow-500"
            >
              <option value="To Do">To Do</option>
              <option value="In Progress">In Progress</option>
              <option value="Done">Done</option>
            </select>
            <select
              v-model="newTask.priority"
              required
              class="w-full bg-black border border-yellow-600/30 rounded px-4 py-2 text-white font-mono focus:outline-none focus:border-yellow-500"
            >
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
            </select>
            <input
              v-model="newTask.due_date"
              type="date"
              required
              class="w-full bg-black border border-yellow-600/30 rounded px-4 py-2 text-white font-mono focus:outline-none focus:border-yellow-500"
            />
            <select
              v-model="newTask.project_id"
              required
              class="w-full bg-black border border-yellow-600/30 rounded px-4 py-2 text-white font-mono focus:outline-none focus:border-yellow-500"
            >
              <option v-for="project in projects" :key="project.id" :value="project.id">
                {{ project.name }}
              </option>
            </select>
            <div class="flex justify-end space-x-2">
              <button
                type="button"
                @click="showModal = false"
                class="bg-gray-600/20 hover:bg-gray-600/30 border border-gray-600/50 text-gray-300 font-mono px-4 py-2 rounded transition-all duration-300"
              >
                Cancel
              </button>
              <button
                type="submit"
                class="bg-yellow-600/20 hover:bg-yellow-600/30 border border-yellow-600/50 text-yellow-500 font-mono px-4 py-2 rounded transition-all duration-300"
              >
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
    if (user != "admin"){
      router.push('/')
    }
    await fetchUsers()
    await fetchProjects()
  })
  
  async function fetchUsers() {
    try {
      const response = await fetch('http://localhost:8000/api/admin/users', {
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
      const response = await fetch('http://localhost:8000/api/projects/', {
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
      const response = await fetch('http://localhost:8000/api/projects/', {
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
      const response = await fetch('http://localhost:8000/api/admin/assign-project', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${store.state.token}`
        },
        body: JSON.stringify({ user_id: userId, project_id: projectId })
      })
      if (response.ok) {
        alert('User added to project successfully')
        await fetchProjects() // Refresh projects to update the UI
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
      const response = await fetch('http://localhost:8000/api/admin/remove-user-from-project', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${store.state.token}`
        },
        body: JSON.stringify({ user_id: userId, project_id: projectId })
      })
      if (response.ok) {
        alert('User removed from project successfully')
        await fetchProjects() // Refresh projects to update the UI
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
      const response = await fetch('http://localhost:8000/api/admin/create-task-for-user', {
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