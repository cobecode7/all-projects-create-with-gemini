import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'

export const useAuthStore = defineStore('auth', () => {
  // State
  const user = ref(null)
  const token = ref(localStorage.getItem('token') || '')

  // Getters
  const isAuthenticated = computed(() => !!token.value)

  // Actions
  const login = async (credentials) => {
    try {
      const response = await axios.post('/api/auth/login', credentials)

      if (response.data.token) {
        token.value = response.data.token
        user.value = response.data.user
        localStorage.setItem('token', token.value)

        // Set default auth header for all future requests
        axios.defaults.headers.common['Authorization'] = `Bearer ${token.value}`

        return response.data
      }

      throw new Error('Invalid login response')
    } catch (error) {
      console.error('Login error:', error)
      throw error
    }
  }

  const register = async (userData) => {
    try {
      const response = await axios.post('/api/auth/register', userData)
      return response.data
    } catch (error) {
      console.error('Registration error:', error)
      throw error
    }
  }

  const logout = async () => {
    try {
      // Call logout endpoint if it exists
      await axios.post('/api/auth/logout')
    } catch (error) {
      console.error('Logout error:', error)
    } finally {
      // Always clear local data regardless of API call success
      token.value = ''
      user.value = null
      localStorage.removeItem('token')

      // Remove auth header
      delete axios.defaults.headers.common['Authorization']
    }
  }

  const checkAuth = async () => {
    if (!token.value) return false

    try {
      // Set auth header for this request
      axios.defaults.headers.common['Authorization'] = `Bearer ${token.value}`

      const response = await axios.get('/api/profile')
      user.value = response.data.user
      return true
    } catch (error) {
      console.error('Auth check error:', error)

      // Token is invalid, clear it
      token.value = ''
      user.value = null
      localStorage.removeItem('token')
      delete axios.defaults.headers.common['Authorization']

      return false
    }
  }

  const updateProfile = async (profileData) => {
    try {
      const response = await axios.put('/api/profile', profileData)
      user.value = response.data.user
      return response.data
    } catch (error) {
      console.error('Profile update error:', error)
      throw error
    }
  }

  return {
    user,
    token,
    isAuthenticated,
    login,
    register,
    logout,
    checkAuth,
    updateProfile
  }
})
