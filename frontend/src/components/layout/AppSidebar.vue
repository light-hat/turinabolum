<template>
  <Sidebar collapsible="icon">
    <SidebarHeader>
      <div class="flex h-16 items-center border-b px-6">
        <div class="flex items-center space-x-2">
          <div class="w-8 h-8 bg-primary rounded-md flex items-center justify-center">
            <span class="text-primary-foreground font-bold text-sm">T</span>
          </div>
          <div>
            <h2 class="text-lg font-semibold">Turinabolum</h2>
            <p class="text-xs text-muted-foreground">v1.0.0</p>
          </div>
        </div>
      </div>
    </SidebarHeader>
    
    <SidebarContent>
      <!-- Search Bar -->
      <div class="p-4 border-b">
        <div class="relative">
          <SearchIcon class="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <input
            type="text"
            placeholder="Search incidents..."
            class="w-full pl-10 pr-4 py-2 bg-background border border-input rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-ring"
          />
        </div>
      </div>
      
      <nav class="space-y-1 px-3 py-4">
        <SidebarItem
          to="/dashboard"
          label="Dashboard"
          :icon="HomeIcon"
        />
        
        <div class="space-y-1">
          <button
            @click="toggleIncidentsDropdown"
            class="flex w-full items-center gap-3 rounded-lg px-3 py-2 text-sm text-muted-foreground hover:text-primary"
          >
            <FileTextIcon class="h-4 w-4" />
            <span>Incidents</span>
            <ChevronDownIcon 
              :class="cn('ml-auto h-4 w-4 transition-transform', incidentsDropdownOpen && 'rotate-180')"
            />
          </button>
          
          <div v-if="incidentsDropdownOpen" class="ml-6 space-y-1">
            <SidebarItem
              to="/incidents"
              label="All Incidents"
              :icon="ListIcon"
            />
            <SidebarItem
              to="/incidents/new"
              label="New Incident"
              :icon="PlusIcon"
            />
          </div>
        </div>
        
        <SidebarItem
          to="/dumps"
          label="Dump Uploads"
          :icon="UploadIcon"
        />
        
        <SidebarItem
          to="/graph"
          label="Graph View"
          :icon="NetworkIcon"
        />
        
        <SidebarItem
          to="/profile"
          label="Profile"
          :icon="UserIcon"
        />
      </nav>
    </SidebarContent>
    
    <SidebarFooter>
      <div class="flex items-center gap-3">
        <div class="flex h-8 w-8 items-center justify-center rounded-full bg-primary text-primary-foreground text-sm">
          {{ userInitials }}
        </div>
        <div class="flex-1 min-w-0">
          <p class="text-sm font-medium truncate">{{ authStore.user?.username }}</p>
          <p class="text-xs text-muted-foreground truncate">{{ authStore.user?.email }}</p>
        </div>
        <Button
          variant="ghost"
          size="icon"
          @click="handleLogout"
          class="h-8 w-8"
        >
          <LogOutIcon class="h-4 w-4" />
        </Button>
      </div>
    </SidebarFooter>
    
    <SidebarRail />
  </Sidebar>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import Sidebar from '@/components/ui/sidebar.vue'
import SidebarHeader from '@/components/ui/sidebar-header.vue'
import SidebarContent from '@/components/ui/sidebar-content.vue'
import SidebarFooter from '@/components/ui/sidebar-footer.vue'
import SidebarRail from '@/components/ui/sidebar-rail.vue'
import SidebarItem from '@/components/ui/sidebar-item.vue'
import Button from '@/components/ui/button.vue'
import { cn } from '@/lib/utils'
import {
  HomeIcon,
  FileTextIcon,
  ListIcon,
  PlusIcon,
  UploadIcon,
  NetworkIcon,
  UserIcon,
  LogOutIcon,
  ChevronDownIcon,
  SearchIcon
} from 'lucide-vue-next'

const router = useRouter()
const authStore = useAuthStore()

const incidentsDropdownOpen = ref(false)

const userInitials = computed(() => {
  if (!authStore.user) return 'U'
  const firstName = authStore.user.first_name || ''
  const lastName = authStore.user.last_name || ''
  if (firstName && lastName) {
    return `${firstName[0]}${lastName[0]}`.toUpperCase()
  }
  return authStore.user.username[0].toUpperCase()
})

const toggleIncidentsDropdown = () => {
  incidentsDropdownOpen.value = !incidentsDropdownOpen.value
}

const handleLogout = async () => {
  await authStore.logout()
  router.push('/login')
}
</script>
