<template>
  <div class="flex flex-1 flex-col gap-6">
      <!-- Header -->
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-3xl font-bold text-slate-900 dark:text-slate-100 ">Dashboard</h1>
          <p class="text-slate-600 dark:text-slate-400 ">Welcome to Turinabolum Digital Forensics Platform</p>
        </div>
        <div class="flex items-center gap-2">
          <Button @click="refreshData" :disabled="isLoading" class=" bg-white/80 dark:bg-slate-800/80 backdrop-blur-sm border-0 shadow-lg">
            <svg v-if="isLoading" class="animate-spin -ml-1 mr-2 h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            Refresh
          </Button>
        </div>
      </div>

      <!-- Stats Grid -->
      <div class="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
        <Card class="p-6 bg-white/80 dark:bg-slate-800/80 backdrop-blur-sm border-0 shadow-xl">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-slate-600 dark:text-slate-400 ">Total Incidents</p>
              <p class="text-2xl font-bold text-slate-900 dark:text-slate-100 ">{{ stats.totalIncidents }}</p>
            </div>
            <div class="h-12 w-12 rounded-lg bg-red-100 dark:bg-red-900/20 flex items-center justify-center">
              <AlertTriangleIcon class="h-6 w-6 text-red-600 dark:text-red-400" />
            </div>
          </div>
          <div class="mt-4 flex items-center text-sm text-slate-600 dark:text-slate-400">
            <span class="">{{ stats.newIncidentsThisWeek }} new this week</span>
          </div>
        </Card>

        <Card class="p-6 bg-white/80 dark:bg-slate-800/80 backdrop-blur-sm border-0 shadow-xl">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-slate-600 dark:text-slate-400 ">Active Cases</p>
              <p class="text-2xl font-bold text-slate-900 dark:text-slate-100 ">{{ stats.activeCases }}</p>
            </div>
            <div class="h-12 w-12 rounded-lg bg-blue-100 dark:bg-blue-900/20 flex items-center justify-center">
              <ShieldIcon class="h-6 w-6 text-blue-600 dark:text-blue-400" />
            </div>
          </div>
          <div class="mt-4 flex items-center text-sm text-slate-600 dark:text-slate-400">
            <span class="">{{ stats.casesInProgress }} in progress</span>
          </div>
        </Card>

        <Card class="p-6 bg-white/80 dark:bg-slate-800/80 backdrop-blur-sm border-0 shadow-xl">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-slate-600 dark:text-slate-400 ">Total Dumps</p>
              <p class="text-2xl font-bold text-slate-900 dark:text-slate-100 ">{{ stats.totalDumps }}</p>
            </div>
            <div class="h-12 w-12 rounded-lg bg-green-100 dark:bg-green-900/20 flex items-center justify-center">
              <UploadIcon class="h-6 w-6 text-green-600 dark:text-green-400" />
            </div>
          </div>
          <div class="mt-4 flex items-center text-sm text-slate-600 dark:text-slate-400">
            <span class="">{{ formatBytes(stats.totalDumpSize) }} total size</span>
          </div>
        </Card>

        <Card class="p-6 bg-white/80 dark:bg-slate-800/80 backdrop-blur-sm border-0 shadow-xl">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-slate-600 dark:text-slate-400 ">IOCs</p>
              <p class="text-2xl font-bold text-slate-900 dark:text-slate-100 ">{{ stats.totalIOCs }}</p>
            </div>
            <div class="h-12 w-12 rounded-lg bg-purple-100 dark:bg-purple-900/20 flex items-center justify-center">
              <NetworkIcon class="h-6 w-6 text-purple-600 dark:text-purple-400" />
            </div>
          </div>
          <div class="mt-4 flex items-center text-sm text-slate-600 dark:text-slate-400">
            <span class="">{{ stats.newIOCsToday }} new today</span>
          </div>
        </Card>
      </div>

      <!-- Recent Incidents -->
      <div class="grid gap-6 lg:grid-cols-2">
        <Card class="p-6 bg-white/80 dark:bg-slate-800/80 backdrop-blur-sm border-0 shadow-xl">
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-lg font-semibold text-slate-900 dark:text-slate-100 ">Recent Incidents</h3>
            <Button variant="outline" size="sm" class=" bg-white/50 dark:bg-slate-700/50 backdrop-blur-sm border-0 shadow-lg">
              View All
            </Button>
          </div>
          <div class="space-y-4">
            <div v-for="incident in recentIncidents" :key="incident.id" class="flex items-start space-x-3 p-3 rounded-lg hover:bg-slate-50/50 dark:hover:bg-slate-700/50 transition-colors backdrop-blur-sm">
              <div class="h-2 w-2 rounded-full bg-red-500 mt-2"></div>
              <div class="flex-1 min-w-0">
                <p class="text-sm font-medium text-slate-900 dark:text-slate-100 ">{{ incident.title }}</p>
                <p class="text-sm text-slate-600 dark:text-slate-400 ">{{ incident.description }}</p>
                <p class="text-xs text-slate-500 dark:text-slate-500 ">{{ formatDate(incident.created_at) }}</p>
              </div>
            </div>
          </div>
        </Card>

        <Card class="p-6 bg-white/80 dark:bg-slate-800/80 backdrop-blur-sm border-0 shadow-xl">
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-lg font-semibold text-slate-900 dark:text-slate-100 ">Quick Actions</h3>
          </div>
          <div class="space-y-3">
            <Button class="w-full justify-start  bg-white/50 dark:bg-slate-700/50 backdrop-blur-sm border-0 shadow-lg hover:bg-white/70 dark:hover:bg-slate-600/70" variant="outline">
              <PlusIcon class="mr-2 h-4 w-4" />
              Create New Incident
            </Button>
            <Button class="w-full justify-start  bg-white/50 dark:bg-slate-700/50 backdrop-blur-sm border-0 shadow-lg hover:bg-white/70 dark:hover:bg-slate-600/70" variant="outline">
              <UploadIcon class="mr-2 h-4 w-4" />
              Upload Dump File
            </Button>
            <Button class="w-full justify-start  bg-white/50 dark:bg-slate-700/50 backdrop-blur-sm border-0 shadow-lg hover:bg-white/70 dark:hover:bg-slate-600/70" variant="outline">
              <FileTextIcon class="mr-2 h-4 w-4" />
              Generate Report
            </Button>
          </div>
        </Card>
      </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import Card from '@/components/ui/card.vue'
import Button from '@/components/ui/button.vue'
import {
  FileTextIcon,
  ShieldIcon,
  UploadIcon,
  AlertTriangleIcon,
  PlusIcon,
  NetworkIcon
} from 'lucide-vue-next'

interface Incident {
  id: number
  title: string
  description: string
  created_at: string
}

const router = useRouter()
const isLoading = ref(false)

const stats = ref({
  totalIncidents: 0,
  newIncidentsThisWeek: 0,
  activeCases: 0,
  casesInProgress: 0,
  totalDumps: 0,
  totalDumpSize: 0,
  totalIOCs: 0,
  newIOCsToday: 0
})

const recentIncidents = ref<Incident[]>([])

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString()
}

const formatBytes = (bytes: number) => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

const fetchDashboardData = async () => {
  isLoading.value = true
  try {
    // TODO: Implement API calls to fetch real data
    // For now, using mock data
    await new Promise(resolve => setTimeout(resolve, 1000)) // Simulate API call
    
    stats.value = {
      totalIncidents: 24,
      newIncidentsThisWeek: 3,
      activeCases: 8,
      casesInProgress: 5,
      totalDumps: 156,
      totalDumpSize: 2048576000, // ~2GB
      totalIOCs: 89,
      newIOCsToday: 12
    }
    
    recentIncidents.value = [
      {
        id: 1,
        title: 'Malware Analysis - Trojan.Banker',
        description: 'Suspicious banking trojan detected in user workstation',
        created_at: '2024-01-15T10:30:00Z'
      },
      {
        id: 2,
        title: 'Network Intrusion Investigation',
        description: 'Unauthorized access attempt from external IP',
        created_at: '2024-01-14T15:45:00Z'
      },
      {
        id: 3,
        title: 'Data Exfiltration Case',
        description: 'Potential data breach investigation',
        created_at: '2024-01-13T09:20:00Z'
      }
    ]
  } finally {
    isLoading.value = false
  }
}

const refreshData = () => {
  fetchDashboardData()
}

onMounted(() => {
  fetchDashboardData()
})
</script>
