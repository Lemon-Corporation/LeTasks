<template>
  <div class="min-h-screen bg-gradient-to-b from-emerald-600 via-teal-800 to-slate-900 flex items-center justify-center p-4 sm:p-6">
    <div class="w-full max-w-md">
      <div class="bg-black/30 backdrop-blur-xl border border-emerald-500/20 rounded-2xl p-8 shadow-lg shadow-emerald-900/20">
        <h2 class="text-3xl font-bold text-center text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 to-teal-300 mb-6 lex items-center justify-center">
          <UserPlus class="w-8 h-8 mr-2" />
          REGISTER
        </h2>
        <form @submit.prevent="register" class="space-y-6">
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
            <label for="email" class="block text-sm font-medium text-emerald-400 mb-1">EMAIL</label>
            <div class="relative">
              <input
                v-model="email"
                id="email"
                type="email"
                required
                class="w-full bg-black/50 border border-emerald-500/30 rounded-xl pl-10 pr-4 py-2 text-emerald-300 font-mono focus:outline-none focus:border-emerald-400 focus:ring-1 focus:ring-emerald-400"
              />
              <Mail class="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-emerald-500" />
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
            <label for="confirmPassword" class="block text-sm font-medium text-emerald-400 mb-1">CONFIRM PASSWORD</label>
            <div class="relative">
              <input
                v-model="confirmPassword"
                id="confirmPassword"
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
              <UserPlus class="w-5 h-5 mr-2" />
              [ CREATE ACCOUNT ]
            </button>
          </div>
        </form>
        <div class="mt-4 text-center">
          <router-link to="/auth/sign-in" class="text-emerald-400 hover:text-emerald-300 font-mono transition-all duration-300">
            [ ALREADY HAVE AN ACCOUNT? LOGIN ]
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
import { UserPlus, User, Mail, Lock } from 'lucide-vue-next'

const store = useStore()
const router = useRouter()

const username = ref('')
const email = ref('')
const password = ref('')
const confirmPassword = ref('')
  
  const register = async () => {
    if (password.value !== confirmPassword.value) {
      console.error('Passwords do not match')
      // Here you could set an error message to display to the user
      return
    }
  
    try {
      await store.dispatch('register', {
        username: username.value,
        email: email.value,
        password: password.value
      })
      router.push('/')
    } catch (error) {
      console.error('Registration failed:', error)
      // Here you could set an error message to display to the user
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