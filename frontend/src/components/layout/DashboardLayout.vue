<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800">
    <SidebarProvider>
      <AppSidebar />
      <SidebarInset>
        <header class="flex h-16 shrink-0 items-center gap-4 border-b border-border bg-white/80 dark:bg-slate-800/80 backdrop-blur supports-[backdrop-filter]:bg-white/60 dark:supports-[backdrop-filter]:bg-slate-800/60 px-6">
          <Breadcrumb>
            <BreadcrumbList>
              <BreadcrumbItem class="hidden md:block">
                <BreadcrumbLink href="#" class="text-sm font-medium text-muted-foreground hover:text-foreground transition-colors font-serif">
                  Turinabolum Platform
                </BreadcrumbLink>
              </BreadcrumbItem>
              <BreadcrumbSeparator class="hidden md:block" />
              <BreadcrumbItem>
                <BreadcrumbPage class="text-sm font-semibold font-serif">{{ pageTitle }}</BreadcrumbPage>
              </BreadcrumbItem>
            </BreadcrumbList>
          </Breadcrumb>
          
          <div class="ml-auto flex items-center gap-3">
            <Button
              variant="ghost"
              size="icon"
              @click="themeStore.toggleTheme()"
              class="h-9 w-9 hover:bg-slate-100/50 dark:hover:bg-slate-700/50 backdrop-blur-sm"
            >
              <SunIcon v-if="themeStore.isDark" class="h-4 w-4" />
              <MoonIcon v-else class="h-4 w-4" />
            </Button>
            <Button
              variant="ghost"
              size="icon"
              @click="authStore.logout()"
              class="h-9 w-9 hover:bg-slate-100/50 dark:hover:bg-slate-700/50 backdrop-blur-sm"
              title="Logout"
            >
              <LogOut class="h-4 w-4" />
            </Button>
          </div>
        </header>
        <main class="flex flex-1 flex-col gap-6 p-6">
          <slot />
        </main>
      </SidebarInset>
    </SidebarProvider>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useThemeStore } from '@/stores/theme'
import AppSidebar from '@/components/layout/AppSidebar.vue'
import SidebarProvider from '@/components/ui/sidebar-provider.vue'
import SidebarInset from '@/components/ui/sidebar-inset.vue'
import Breadcrumb from '@/components/ui/breadcrumb.vue'
import BreadcrumbList from '@/components/ui/breadcrumb-list.vue'
import BreadcrumbItem from '@/components/ui/breadcrumb-item.vue'
import BreadcrumbLink from '@/components/ui/breadcrumb-link.vue'
import BreadcrumbSeparator from '@/components/ui/breadcrumb-separator.vue'
import BreadcrumbPage from '@/components/ui/breadcrumb-page.vue'
import Button from '@/components/ui/button.vue'
import { SunIcon, MoonIcon, LogOut } from 'lucide-vue-next'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()
const themeStore = useThemeStore()

const pageTitle = computed(() => {
  const path = route.path
  if (path === '/dashboard') return 'Dashboard'
  if (path === '/incidents') return 'Incidents'
  if (path === '/incidents/new') return 'New Incident'
  if (path === '/dumps') return 'Dump Uploads'
  if (path === '/graph') return 'Graph View'
  if (path === '/profile') return 'Profile'
  return 'Turinabolum'
})

onMounted(() => {
  if (!authStore.isAuthenticated) {
    router.push('/login')
  }
})
</script>
