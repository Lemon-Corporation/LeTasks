<template>
  <div class="min-h-screen bg-black p-4 sm:p-6">
    <nav class="bg-gray-900/50 backdrop-blur-sm border border-yellow-600/20 rounded-lg p-4 mb-6">
      <div class="max-w-7xl mx-auto flex justify-between items-center">
        <h1 class="text-2xl font-mono text-white">PROFILE</h1>
        <button @click="$router.push('/')" class="text-yellow-500 hover:text-yellow-400">Back to Dashboard</button>
      </div>
    </nav>

    <div class="max-w-2xl mx-auto bg-gray-900/50 backdrop-blur-sm border border-yellow-600/20 rounded-lg p-6">
      <h2 class="text-xl font-mono text-yellow-500 mb-6">User Profile</h2>
      
      <div v-if="loading" class="text-white font-mono">Loading...</div>
      
      <div v-else>
        <form @submit.prevent="updateProfile" class="space-y-4">
          <div>
            <label for="username" class="block text-sm font-medium text-gray-400">Username</label>
            <input
              id="username"
              v-model="profile.username"
              type="text"
              class="mt-1 block w-full bg-black border border-yellow-600/30 rounded-md shadow-sm py-2 px-3 text-white font-mono focus:outline-none focus:ring-yellow-500 focus:border-yellow-500"
            />
          </div>
          
          <div>
            <label for="email" class="block text-sm font-medium text-gray-400">Email</label>
            <input
              id="email"
              v-model="profile.email"
              type="email"
              class="mt-1 block w-full bg-black border border-yellow-600/30 rounded-md shadow-sm py-2 px-3 text-white font-mono focus:outline-none focus:ring-yellow-500 focus:border-yellow-500"
            />
          </div>
          
          <div>
            <label for="avatar" class="block text-sm font-medium text-gray-400">Avatar URL</label>
            <input
              id="avatar"
              v-model="profile.avatar"
              type="text"
              class="mt-1 block w-full bg-black border border-yellow-600/30 rounded-md shadow-sm py-2 px-3 text-white font-mono focus:outline-none focus:ring-yellow-500 focus:border-yellow-500"
            />
          </div>
          
          <div>
            <label for="new_password" class="block text-sm font-medium text-gray-400">New Password (leave blank to keep current)</label>
            <input
              id="new_password"
              v-model="newPassword"
              type="password"
              class="mt-1 block w-full bg-black border border-yellow-600/30 rounded-md shadow-sm py-2 px-3 text-white font-mono focus:outline-none focus:ring-yellow-500 focus:border-yellow-500"
            />
          </div>
          
          <div>
            <button
              type="submit"
              class="w-full bg-yellow-600/20 hover:bg-yellow-600/30 border border-yellow-600/50 text-yellow-500 font-mono py-2 px-4 rounded transition-all duration-300"
            >
              Update Profile
            </button>
          </div>
        </form>
        
        <div v-if="message" :class="{'text-green-500': !error, 'text-red-500': error}" class="mt-4 font-mono">
          {{ message }}
        </div>

        <!-- User Statistics -->
        <div class="mt-8">
          <h3 class="text-lg font-mono text-yellow-500 mb-4">User Statistics</h3>
          <div class="grid grid-cols-2 gap-4">
            <div class="bg-gray-800/50 p-4 rounded-lg">
              <p class="text-white font-mono">Total Tasks: {{ userStats.totalTasks }}</p>
            </div>
            <div class="bg-gray-800/50 p-4 rounded-lg">
              <p class="text-white font-mono">Completed Tasks: {{ userStats.completedTasks }}</p>
            </div>
            <div class="bg-gray-800/50 p-4 rounded-lg">
              <p class="text-white font-mono">Ongoing Tasks: {{ userStats.ongoingTasks }}</p>
            </div>
            <div class="bg-gray-800/50 p-4 rounded-lg">
              <p class="text-white font-mono">Overdue Tasks: {{ userStats.overdueTasks }}</p>
            </div>
          </div>
        </div>

        <!-- Current Tasks -->
        <div class="mt-8">
          <h3 class="text-lg font-mono text-yellow-500 mb-4">Current Tasks</h3>
          <div v-if="currentTasks.length > 0" class="space-y-4">
            <div v-for="task in currentTasks" :key="task.id" class="bg-gray-800/50 p-4 rounded-lg">
              <h4 class="text-white font-mono font-bold">{{ task.title }}</h4>
              <p class="text-gray-400 font-mono">Status: {{ task.status }}</p>
              <p class="text-gray-400 font-mono">Due: {{ formatDate(task.due_date) }}</p>
            </div>
          </div>
          <p v-else class="text-gray-400 font-mono">No current tasks.</p>
        </div>

        <!-- Achievements -->
        <div class="mt-8">
          <h3 class="text-lg font-mono text-yellow-500 mb-4">Achievements</h3>
          <div v-if="achievements.length > 0" class="grid grid-cols-2 gap-4">
            <div v-for="achievement in achievements" :key="achievement.id" class="bg-gray-800/50 p-4 rounded-lg">
              <h4 class="text-white font-mono font-bold">{{ achievement.title }}</h4>
              <p class="text-gray-400 font-mono">{{ achievement.description }}</p>
            </div>
          </div>
          <p v-else class="text-gray-400 font-mono">No achievements yet.</p>
        </div>

        <!-- Rank -->
        <div class="mt-8">
          <h3 class="text-lg font-mono text-yellow-500 mb-4">Rank</h3>
          <div class="bg-gray-800/50 p-4 rounded-lg">
            <p class="text-white font-mono font-bold">{{ profile.rank || 'Employee' }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

const store = useStore()
const router = useRouter()

const profile = ref({
  username: '',
  email: '',
  avatar: '',
  rank: 'Employee'
})
const newPassword = ref('')
const loading = ref(true)
const message = ref('')
const error = ref(false)
const userStats = ref({
  totalTasks: 0,
  completedTasks: 0,
  ongoingTasks: 0,
  overdueTasks: 0
})
const currentTasks = ref([])
const achievements = ref([])

onMounted(async () => {
  if (!store.getters.isAuthenticated) {
    router.push('/auth/sign-in')
    return
  }
  await fetchProfile()
  await fetchUserStats()
  await fetchCurrentTasks()
  await fetchAchievements()
})

async function fetchProfile() {
  try {
    const response = await fetch('/api/users/me', {
      headers: { Authorization: `Bearer ${store.state.token}` }
    })
    if (response.ok) {
      const data = await response.json()
      profile.value = {
        username: data.username,
        email: data.email,
        avatar: data.avatar || '',
        rank: data.rank || 'Employee'
      }
    } else {
      throw new Error('Failed to fetch profile')
    }
  } catch (err) {
    console.error('Error fetching profile:', err)
    message.value = 'Failed to load profile. Please try again.'
    error.value = true
  } finally {
    loading.value = false
  }
}

async function updateProfile() {
  try {
    const updateData = { ...profile.value }
    if (newPassword.value) {
      updateData.password = newPassword.value
    }

    const response = await fetch('/api/users/me', {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${store.state.token}`
      },
      body: JSON.stringify(updateData)
    })

    if (response.ok) {
      message.value = 'Profile updated successfully'
      error.value = false
      newPassword.value = ''
      await store.dispatch('fetchUser') // Update user data in Vuex store
    } else {
      throw new Error('Failed to update profile')
    }
  } catch (err) {
    console.error('Error updating profile:', err)
    message.value = 'Failed to update profile. Please try again.'
    error.value = true
  }
}

async function fetchUserStats() {
  try {
    const response = await fetch('/api/users/me/stats', {
      headers: { Authorization: `Bearer ${store.state.token}` }
    })
    if (response.ok) {
      userStats.value = await response.json()
    } else {
      throw new Error('Failed to fetch user stats')
    }
  } catch (err) {
    console.error('Error fetching user stats:', err)
  }
}

async function fetchCurrentTasks() {
  try {
    const response = await fetch('/api/users/me/tasks', {
      headers: { Authorization: `Bearer ${store.state.token}` }
    })
    if (response.ok) {
      currentTasks.value = await response.json()
    } else {
      throw new Error('Failed to fetch current tasks')
    }
  } catch (err) {
    console.error('Error fetching current tasks:', err)
  }
}

async function fetchAchievements() {
  try {
    const response = await fetch('/api/users/me/achievements', {
      headers: { Authorization: `Bearer ${store.state.token}` }
    })
    if (response.ok) {
      achievements.value = await response.json()
    } else {
      throw new Error('Failed to fetch achievements')
    }
  } catch (err) {
    console.error('Error fetching achievements:', err)
  }
}

function formatDate(dateString) {
  const options = { year: 'numeric', month: 'long', day: 'numeric' }
  return new Date(dateString).toLocaleDateString(undefined, options)
}
</script>