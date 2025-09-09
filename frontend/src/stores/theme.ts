import { defineStore } from 'pinia'
import { ref, watch } from 'vue'

export const useThemeStore = defineStore('theme', () => {
  const theme = ref<'light' | 'dark' | 'system'>(
    (localStorage.getItem('theme') as 'light' | 'dark' | 'system') || 'dark'
  )

  const isDark = ref(false)

  const setTheme = (newTheme: 'light' | 'dark' | 'system') => {
    theme.value = newTheme
    localStorage.setItem('theme', newTheme)
    applyTheme()
  }

  const applyTheme = () => {
    const root = document.documentElement
    
    if (theme.value === 'system') {
      const systemTheme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
      isDark.value = systemTheme === 'dark'
      root.classList.toggle('dark', systemTheme === 'dark')
    } else {
      isDark.value = theme.value === 'dark'
      root.classList.toggle('dark', theme.value === 'dark')
    }
  }

  const toggleTheme = () => {
    if (theme.value === 'light') {
      setTheme('dark')
    } else if (theme.value === 'dark') {
      setTheme('system')
    } else {
      setTheme('light')
    }
  }

  // Watch for system theme changes
  const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
  mediaQuery.addEventListener('change', () => {
    if (theme.value === 'system') {
      applyTheme()
    }
  })

  // Initialize theme on store creation
  applyTheme()

  // Watch for theme changes and apply them
  watch(theme, () => {
    applyTheme()
  })

  return {
    theme,
    isDark,
    setTheme,
    toggleTheme
  }
})
