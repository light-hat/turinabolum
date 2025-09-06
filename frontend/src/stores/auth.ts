import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { api } from '@/lib/api'

export interface User {
  id: number
  username: string
  email: string
  first_name?: string
  last_name?: string
}

export interface LoginCredentials {
  username: string
  password: string
}

export interface RegisterData {
  username: string
  email: string
  password: string
  first_name?: string
  last_name?: string
}

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const token = ref<string | null>(localStorage.getItem('access_token'))
  const refreshToken = ref<string | null>(localStorage.getItem('refresh_token'))
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  const isAuthenticated = computed(() => !!token.value && !!user.value)

  // Set auth headers for API requests
  const setAuthHeaders = () => {
    if (token.value) {
      api.defaults.headers.common['Authorization'] = `Bearer ${token.value}`
    }
  }

  // Clear auth headers
  const clearAuthHeaders = () => {
    delete api.defaults.headers.common['Authorization']
  }

  // Initialize auth state
  const init = async () => {
    if (token.value) {
      setAuthHeaders()
      try {
        await fetchUser()
      } catch (error) {
        // Token might be expired, try to refresh
        if (refreshToken.value) {
          try {
            await refreshAccessToken()
          } catch (refreshError) {
            logout()
          }
        } else {
          logout()
        }
      }
    }
  }

  // Login
  const login = async (credentials: LoginCredentials) => {
    isLoading.value = true
    error.value = null
    
    try {
      console.log('Attempting login with credentials:', credentials)
      console.log('API base URL:', api.defaults.baseURL)
      const response = await api.post('/auth/jwt/create/', credentials)
      console.log('Login response:', response.data)
      const { access, refresh } = response.data
      
      token.value = access
      refreshToken.value = refresh
      
      localStorage.setItem('access_token', access)
      localStorage.setItem('refresh_token', refresh)
      
      setAuthHeaders()
      await fetchUser()
      
      return { success: true }
    } catch (err: any) {
      console.error('Login error:', err)
      console.error('Error response:', err.response)
      error.value = err.response?.data?.detail || err.response?.data?.error || 'Login failed'
      return { success: false, error: error.value }
    } finally {
      isLoading.value = false
    }
  }

  // Register
  const register = async (data: RegisterData) => {
    isLoading.value = true
    error.value = null
    
    try {
      const response = await api.post('/auth/users/', data)
      // After registration, automatically log in
      return await login({ username: data.username, password: data.password })
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Registration failed'
      return { success: false, error: error.value }
    } finally {
      isLoading.value = false
    }
  }

  // Fetch current user
  const fetchUser = async () => {
    try {
      const response = await api.get('/auth/users/me/')
      user.value = response.data
    } catch (err) {
      throw err
    }
  }

  // Refresh access token
  const refreshAccessToken = async () => {
    if (!refreshToken.value) {
      throw new Error('No refresh token available')
    }
    
    try {
      const response = await api.post('/auth/jwt/refresh/', {
        refresh: refreshToken.value
      })
      
      const { access } = response.data
      token.value = access
      localStorage.setItem('access_token', access)
      setAuthHeaders()
    } catch (err) {
      throw err
    }
  }

  // Update user profile
  const updateProfile = async (data: Partial<User>) => {
    isLoading.value = true
    error.value = null
    
    try {
      const response = await api.patch('/auth/users/me/', data)
      user.value = response.data
      return { success: true }
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Update failed'
      return { success: false, error: error.value }
    } finally {
      isLoading.value = false
    }
  }

  // Change password
  const changePassword = async (currentPassword: string, newPassword: string) => {
    isLoading.value = true
    error.value = null
    
    try {
      await api.post('/auth/users/set_password/', {
        current_password: currentPassword,
        new_password: newPassword
      })
      return { success: true }
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Password change failed'
      return { success: false, error: error.value }
    } finally {
      isLoading.value = false
    }
  }

  // Logout
  const logout = async () => {
    if (refreshToken.value) {
      try {
        await api.post('/auth/jwt/logout/', {
          refresh: refreshToken.value
        })
      } catch (err) {
        // Ignore logout errors
      }
    }
    
    user.value = null
    token.value = null
    refreshToken.value = null
    error.value = null
    
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    
    clearAuthHeaders()
  }

  return {
    user,
    token,
    refreshToken,
    isLoading,
    error,
    isAuthenticated,
    init,
    login,
    register,
    fetchUser,
    updateProfile,
    changePassword,
    logout
  }
})
