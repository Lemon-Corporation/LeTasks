<template>
  <div class="min-h-screen bg-black flex items-center justify-center p-4 sm:p-6">
    <div class="w-full max-w-md">
      <div class="bg-gray-900/50 backdrop-blur-sm border border-yellow-600/20 rounded-lg p-8">
        <h2 class="text-3xl font-bold text-center text-yellow-500 mb-6">LOGIN</h2>
        <form @submit.prevent="login" class="space-y-6">
          <div>
            <label for="username" class="block text-sm font-medium text-yellow-500 mb-1">USERNAME</label>
            <input
              v-model="username"
              id="username"
              type="text"
              required
              class="w-full bg-black border border-yellow-600/30 rounded px-3 py-2 text-white focus:outline-none focus:border-yellow-500"
            />
          </div>
          <div>
            <label for="password" class="block text-sm font-medium text-yellow-500 mb-1">PASSWORD</label>
            <input
              v-model="password"
              id="password"
              type="password"
              required
              class="w-full bg-black border border-yellow-600/30 rounded px-3 py-2 text-white focus:outline-none focus:border-yellow-500"
            />
          </div>
          <div>
            <button
              type="submit"
              class="w-full bg-yellow-600/20 hover:bg-yellow-600/30 border border-yellow-600/50 text-yellow-500 font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline transition-all duration-300"
            >
              [ AUTHENTICATE ]
            </button>
          </div>
        </form>
        <div class="mt-4 text-center">
          <router-link to="/auth/sign-up" class="text-yellow-500 hover:text-yellow-400">
            [ CREATE NEW ACCOUNT ]
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

const store = useStore()
const router = useRouter()

const username = ref('')
const password = ref('')

const login = async () => {
  try {
    await store.dispatch('login', { username: username.value, password: password.value })
    router.push('/')
  } catch (error) {
    console.error('Login failed:', error)
    // Здесь вы можете добавить логику для отображения ошибки пользователю
  }
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
    text-shadow: 
      0.025em 0.05em 0 rgba(255, 255, 0, 0.75),
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