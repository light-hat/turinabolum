<template>
  <SidebarProvider>
    <AppSidebar />
    <SidebarInset>
      <header class="flex h-16 shrink-0 items-center gap-2 border-b px-4">
        <SidebarTrigger class="-ml-1" />
        <Separator orientation="vertical" class="mr-2 h-4" />
        <Breadcrumb>
          <BreadcrumbList>
            <BreadcrumbItem class="hidden md:block">
              <BreadcrumbLink href="#">
                Turinabolum
              </BreadcrumbLink>
            </BreadcrumbItem>
            <BreadcrumbSeparator class="hidden md:block" />
            <BreadcrumbItem>
              <BreadcrumbPage>{{ pageTitle }}</BreadcrumbPage>
            </BreadcrumbItem>
          </BreadcrumbList>
        </Breadcrumb>
        
        <div class="ml-auto flex items-center gap-4">
          <Button
            variant="ghost"
            size="icon"
            @click="themeStore.toggleTheme()"
          >
            <SunIcon v-if="themeStore.isDark" class="h-4 w-4" />
            <MoonIcon v-else class="h-4 w-4" />
          </Button>
        </div>
      </header>
      
      <div class="flex flex-1 flex-col gap-4 p-4">
        <slot />
      </div>
    </SidebarInset>
  </SidebarProvider>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useThemeStore } from '@/stores/theme'
import AppSidebar from '@/components/layout/AppSidebar.vue'
import SidebarProvider from '@/components/ui/sidebar-provider.vue'
import SidebarInset from '@/components/ui/sidebar-inset.vue'
import SidebarTrigger from '@/components/ui/sidebar-trigger.vue'
import Breadcrumb from '@/components/ui/breadcrumb.vue'
import BreadcrumbList from '@/components/ui/breadcrumb-list.vue'
import BreadcrumbItem from '@/components/ui/breadcrumb-item.vue'
import BreadcrumbLink from '@/components/ui/breadcrumb-link.vue'
import BreadcrumbSeparator from '@/components/ui/breadcrumb-separator.vue'
import BreadcrumbPage from '@/components/ui/breadcrumb-page.vue'
import Separator from '@/components/ui/separator.vue'
import Button from '@/components/ui/button.vue'
import { SunIcon, MoonIcon } from 'lucide-vue-next'

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
