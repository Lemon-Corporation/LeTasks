import { createStore } from 'vuex'
import axios from 'axios'
import Cookies from 'js-cookie'

const store = createStore({
  state: {
    user: null,
    token: Cookies.get('token') || null,
    tasks: [],
    projects: []
  },
  mutations: {
    setUser(state, user) {
      state.user = user
    },
    setToken(state, token) {
      state.token = token
      Cookies.set('token', token, { expires: 7 }) // Token expires in 7 days
    },
    clearUserData(state) {
      state.user = null
      state.token = null
      Cookies.remove('token')
    },
    setTasks(state, tasks) {
      state.tasks = tasks
    },
    setProjects(state, projects) {
      state.projects = projects
    }
  },
  actions: {
    async login({ commit, dispatch }, credentials) {
      try {
        const formData = new FormData()
        formData.append('username', credentials.username)
        formData.append('password', credentials.password)

        const response = await axios.post('/api/token', formData, {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
          }
        })
        commit('setToken', response.data.access_token)
        await dispatch('fetchUser')
      } catch (error) {
        console.error('Login failed:', error)
        throw error
      }
    },
    async register({ dispatch }, userData) {
      try {
        await axios.post('/api/users/', userData)
        await dispatch('login', { username: userData.username, password: userData.password })
      } catch (error) {
        console.error('Registration failed:', error)
        throw error
      }
    },
    async fetchUser({ commit, state }) {
      if (!state.token) {
        console.warn('No token found, user is not authenticated')
        return
      }
      try {
        const response = await axios.get('/api/users/me', {
          headers: { Authorization: `Bearer ${state.token}` }
        })
        commit('setUser', response.data)
      } catch (error) {
        console.error('Failed to fetch user:', error)
        if (error.response && error.response.status === 401) {
          commit('clearUserData')
        }
        throw error
      }
    },
    logout({ commit }) {
      commit('clearUserData')
    },
    async fetchTasks({ commit, state }, projectId = null) {
      if (!state.token) {
        console.warn('No token found, user is not authenticated')
        return
      }
      try {
        let url = '/api/tasks/'
        if (projectId) {
          url += `?project_id=${projectId}`
        }
        const response = await axios.get(url, {
          headers: { Authorization: `Bearer ${state.token}` }
        })
        commit('setTasks', response.data)
      } catch (error) {
        console.error('Failed to fetch tasks:', error)
        if (error.response && error.response.status === 401) {
          commit('clearUserData')
        }
        throw error
      }
    },
    async addTask({ commit, state }, task) {
      try {
        console.log('Sending task to server:', task); // Log the task data
        const response = await axios.post('/api/tasks/', task, {
          headers: { 
            Authorization: `Bearer ${state.token}`,
            'Content-Type': 'application/json'
          }
        });
        console.log('Server response:', response.data); // Log the server response
        commit('addTask', response.data);
      } catch (error) {
        console.error('Failed to add task:', error);
        if (error.response) {
          console.error('Server error response:', error.response.data);
        }
        throw error;
      }
    },
    async updateTask({ dispatch, state }, task) {
      try {
        console.log('Updating task:', task); // Добавим лог для отладки
        const response = await axios.put(`/api/tasks/${task.id}`, task, {
          headers: { 
            Authorization: `Bearer ${state.token}`,
            'Content-Type': 'application/json'
          }
        });
        console.log('Server response:', response.data); // Добавим лог для отладки
        await dispatch('fetchTasks');
      } catch (error) {
        console.error('Failed to update task:', error);
        if (error.response) {
          console.error('Error response:', error.response.data);
        }
        throw error;
      }
    },
    async deleteTask({ dispatch, state }, taskId) {
      try {
        await axios.delete(`/api/tasks/${taskId}`, {
          headers: { Authorization: `Bearer ${state.token}` }
        });
        await dispatch('fetchTasks');
      } catch (error) {
        console.error('Failed to delete task:', error);
        throw error;
      }
    },
    async fetchProjects({ commit, state }) {
      try {
        const response = await axios.get('/api/projects/', {
          headers: { Authorization: `Bearer ${state.token}` }
        })
        commit('setProjects', response.data)
      } catch (error) {
        console.error('Failed to fetch projects:', error)
        throw error
      }
    }
  },
  getters: {
    isAuthenticated: state => !!state.token,
    getUser: state => state.user,
    getTasks: state => state.tasks,
    getProjects: state => state.projects
  }
})

axios.interceptors.request.use(config => {
  const token = store.state.token
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
}, error => {
  return Promise.reject(error)
})

// Add this interceptor to handle 401 errors globally
axios.interceptors.response.use(response => response, error => {
  if (error.response && error.response.status === 401) {
    store.commit('clearUserData')
  }
  return Promise.reject(error)
})

export default store