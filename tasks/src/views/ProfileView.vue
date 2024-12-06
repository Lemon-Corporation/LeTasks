<template>
  <div class="min-h-screen bg-gradient-to-b from-emerald-600 via-teal-800 to-slate-900 p-4 sm:p-6">
    <nav class="bg-black/30 backdrop-blur-xl border border-emerald-500/20 rounded-2xl p-4 mb-6 shadow-lg shadow-emerald-900/20">
      <div class="max-w-7xl mx-auto flex justify-between items-center">
        <h1 class="text-3xl sm:text-4xl font-mono text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 to-teal-300 glitch-text flex items-center">
          <User class="w-8 h-8 mr-2" />
          PROFILE
        </h1>
        <button @click="$router.push('/')" class="text-emerald-400 hover:text-emerald-300 font-mono transition-all duration-300 flex items-center">
          <ArrowLeft class="w-5 h-5 mr-1" />
          Back to Dashboard
        </button>
      </div>
    </nav>

    <div class="max-w-4xl mx-auto bg-black/30 backdrop-blur-xl border border-emerald-500/20 rounded-2xl p-6 shadow-lg shadow-emerald-900/20">
      <h2 class="text-xl font-mono text-emerald-400 mb-6 flex items-center">
        <UserCircle class="w-6 h-6 mr-2" />
        User Profile
      </h2>
      
      <div v-if="loading" class="text-emerald-300 font-mono">Loading...</div>
      
      <div v-else>
        <form @submit.prevent="updateProfile" class="space-y-4">
          <div>
            <label for="username" class="block text-sm font-medium text-emerald-400 mb-1">Username</label>
            <input
              id="username"
              v-model="profile.username"
              type="text"
              class="w-full bg-black/50 border border-emerald-500/30 rounded-xl px-4 py-2 text-emerald-300 font-mono focus:outline-none focus:border-emerald-400 focus:ring-1 focus:ring-emerald-400"
            />
          </div>
          
          <div>
            <label for="email" class="block text-sm font-medium text-emerald-400 mb-1">Email</label>
            <input
              id="email"
              v-model="profile.email"
              type="email"
              class="w-full bg-black/50 border border-emerald-500/30 rounded-xl px-4 py-2 text-emerald-300 font-mono focus:outline-none focus:border-emerald-400 focus:ring-1 focus:ring-emerald-400"
            />
          </div>
          
          <div>
            <label for="avatar" class="block text-sm font-medium text-emerald-400 mb-1">Avatar URL</label>
            <input
              id="avatar"
              v-model="profile.avatar"
              type="text"
              class="w-full bg-black/50 border border-emerald-500/30 rounded-xl px-4 py-2 text-emerald-300 font-mono focus:outline-none focus:border-emerald-400 focus:ring-1 focus:ring-emerald-400"
            />
          </div>
          
          <div>
            <label for="new_password" class="block text-sm font-medium text-emerald-400 mb-1">New Password (leave blank to keep current)</label>
            <input
              id="new_password"
              v-model="newPassword"
              type="password"
              class="w-full bg-black/50 border border-emerald-500/30 rounded-xl px-4 py-2 text-emerald-300 font-mono focus:outline-none focus:border-emerald-400 focus:ring-1 focus:ring-emerald-400"
            />
          </div>
          
          <div>
            <button
              type="submit"
              class="w-full bg-emerald-500/10 hover:bg-emerald-500/20 border border-emerald-500/50 text-emerald-400 font-mono py-2 px-4 rounded-xl transition-all duration-300 flex items-center justify-center"
            >
              <Save class="w-5 h-5 mr-2" />
              Update Profile
            </button>
          </div>
        </form>
        
        <div v-if="message" :class="{'text-green-500': !error, 'text-red-500': error}" class="mt-4 font-mono">
          {{ message }}
        </div>

        <!-- User Statistics -->
        <div class="mt-8">
          <h3 class="text-lg font-mono text-emerald-400 mb-4 flex items-center">
            <ChartBar class="w-5 h-5 mr-2" />
            User Statistics
          </h3>
          <div class="grid grid-cols-2 gap-4">
            <div class="bg-black/50 border border-emerald-500/20 p-4 rounded-xl">
              <p class="text-emerald-300 font-mono">Total Tasks: {{ userStats.totalTasks }}</p>
            </div>
            <div class="bg-black/50 border border-emerald-500/20 p-4 rounded-xl">
              <p class="text-emerald-300 font-mono">Completed Tasks: {{ userStats.completedTasks }}</p>
            </div>
            <div class="bg-black/50 border border-emerald-500/20 p-4 rounded-xl">
              <p class="text-emerald-300 font-mono">Ongoing Tasks: {{ userStats.ongoingTasks }}</p>
            </div>
            <div class="bg-black/50 border border-emerald-500/20 p-4 rounded-xl">
              <p class="text-emerald-300 font-mono">Overdue Tasks: {{ userStats.overdueTasks }}</p>
            </div>
          </div>
        </div>

        <!-- Current Tasks -->
        <div class="mt-8">
          <h3 class="text-lg font-mono text-emerald-400 mb-4 flex items-center">
            <ClipboardList class="w-5 h-5 mr-2" />
            Current Tasks
          </h3>
          <div v-if="currentTasks.length > 0" class="space-y-4">
            <div v-for="task in currentTasks" :key="task.id" class="bg-black/50 border border-emerald-500/20 p-4 rounded-xl">
              <h4 class="text-emerald-300 font-mono font-bold">{{ task.title }}</h4>
              <p class="text-emerald-500 font-mono">Status: {{ task.status }}</p>
              <p classlass="text-emerald-500 font-mono">Due: {{ formatDate(task.due_date) }}</p>
            </div>
          </div>
          <p v-else class="text-emerald-600 font-mono">No current tasks.</p>
        </div>

        <!-- Achievements -->
        <div class="mt-8">
          <h3 class="text-lg font-mono text-emerald-400 mb-4 flex items-center">
            <Award class="w-5 h-5 mr-2" />
            Achievements
          </h3>
          <div v-if="achievements.length > 0" class="grid grid-cols-2 gap-4">
            <div v-for="achievement in achievements" :key="achievement.id" class="bg-black/50 border border-emerald-500/20 p-4 rounded-xl">
              <h4 class="text-emerald-300 font-mono font-bold">{{ achievement.title }}</h4>
              <p class="text-emerald-500 font-mono">{{ achievement.description }}</p>
            </div>
          </div>
          <p v-else class="text-emerald-600 font-mono">No achievements yet.</p>
        </div>

        <!-- Rank -->
        <div class="mt-8">
          <h3 class="text-lg font-mono text-emerald-400 mb-4 flex items-center">
            <Star class="w-5 h-5 mr-2" />
            Rank
          </h3>
          <div class="bg-black/50 border border-emerald-500/20 p-4 rounded-xl">
            <p class="text-emerald-300 font-mono font-bold">{{ profile.rank || 'Employee' }}</p>
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
import { 
  User, ArrowLeft, UserCircle, Save, ChartBar, ClipboardList, Award, Star
} from 'lucide-vue-next'

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
      await store.dispatch('fetchUser')
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