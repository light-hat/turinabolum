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
        if (refreshToken.value === 'cookie') {
          try {
            await refreshAccessToken()
            await fetchUser()
          } catch (refreshError) {
            console.log('Token refresh failed, logging out')
            logout()
          }
        } else {
          console.log('No refresh token available, logging out')
          logout()
        }
      }
    } else {
      // No access token found - this is normal for first-time visitors
      // console.log('No access token found')
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
      const { access, user } = response.data
      
      token.value = access
      // Refresh token is set as HttpOnly cookie, so we don't store it in localStorage
      refreshToken.value = 'cookie' // Placeholder to indicate we have a refresh token
      
      localStorage.setItem('access_token', access)
      // Don't store refresh token in localStorage as it's HttpOnly
      
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
      console.log('Fetching user data...')
      const response = await api.get('/auth/users/me/')
      user.value = response.data
      console.log('User data fetched successfully:', response.data)
    } catch (err: any) {
      console.error('Error fetching user:', err)
      throw err
    }
  }

  // Refresh access token
  const refreshAccessToken = async () => {
    try {
      console.log('Refreshing access token...')
      const response = await api.post('/auth/jwt/refresh/', {})
      
      const { access } = response.data
      token.value = access
      localStorage.setItem('access_token', access)
      setAuthHeaders()
      console.log('Access token refreshed successfully')
    } catch (err: any) {
      console.error('Error refreshing token:', err)
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
    try {
      // Try to logout from server if we have a refresh token
      if (refreshToken.value && refreshToken.value !== 'cookie') {
        await api.post('/auth/jwt/logout/', {
          refresh: refreshToken.value
        })
      }
    } catch (err) {
      // Ignore logout errors - we still want to clear local state
      console.log('Logout API call failed, but continuing with local logout')
    }
    
    // Clear all local state
    user.value = null
    token.value = null
    refreshToken.value = null
    error.value = null
    
    // Clear localStorage
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    
    // Clear auth headers
    clearAuthHeaders()
    
    // Redirect to login page
    window.location.href = '/login'
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
