<template>
  <div class="min-h-screen bg-gradient-to-b from-emerald-600 via-teal-800 to-slate-900 flex items-center justify-center p-4 sm:p-6">
    <div class="w-full max-w-md">
      <div class="bg-black/30 backdrop-blur-xl border border-emerald-500/20 rounded-2xl p-8 shadow-lg shadow-emerald-900/20">
        <h2 class="text-3xl font-bold text-center text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 to-teal-300 mb-6 lex items-center justify-center">
          <UserPlus class="w-8 h-8 mr-2" />
          LOGIN
        </h2>
        <form @submit.prevent="login" class="space-y-6">
          <div>
            <label for="username" class="block text-sm font-medium text-emerald-400 mb-1">USERNAME</label>
            <div class="relative">
              <input
                v-model="username"
                id="username"
                type="text"
                required
                class="w-full bg-black/50 border border-emerald-500/30 rounded-xl pl-10 pr-4 py-2 text-emerald-300 font-mono focus:outline-none focus:border-emerald-400 focus:ring-1 focus:ring-emerald-400"
              />
              <User class="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-emerald-500" />
            </div>
          </div>
          <div>
            <label for="password" class="block text-sm font-medium text-emerald-400 mb-1">PASSWORD</label>
            <div class="relative">
              <input
                v-model="password"
                id="password"
                type="password"
                required
                class="w-full bg-black/50 border border-emerald-500/30 rounded-xl pl-10 pr-4 py-2 text-emerald-300 font-mono focus:outline-none focus:border-emerald-400 focus:ring-1 focus:ring-emerald-400"
              />
              <Lock class="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-emerald-500" />
            </div>
          </div>
          <div>
            <button
              type="submit"
              class="w-full bg-emerald-500/10 hover:bg-emerald-500/20 border border-emerald-500/50 text-emerald-400 font-bold py-2 px-4 rounded-xl focus:outline-none focus:shadow-outline transition-all duration-300 flex items-center justify-center"
            >
              <LogIn class="w-5 h-5 mr-2" />
              [ AUTHENTICATE ]
            </button>
          </div>
        </form>
        <div class="mt-4 text-center">
          <router-link to="/auth/sign-up" class="text-emerald-400 hover:text-emerald-300 font-mono transition-all duration-300">
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
import { LogIn, User, Lock } from 'lucide-vue-next'

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
    // Here you can add logic to display an error message to the user
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