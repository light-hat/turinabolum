<template>
  <div class="space-y-6">
    <div class="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
      <Card>
        <CardHeader class="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle class="text-sm font-medium">Total Incidents</CardTitle>
          <FileTextIcon class="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div class="text-2xl font-bold">{{ stats.totalIncidents }}</div>
          <p class="text-xs text-muted-foreground">
            +{{ stats.newIncidentsThisWeek }} from last week
          </p>
        </CardContent>
      </Card>
      
      <Card>
        <CardHeader class="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle class="text-sm font-medium">Active Cases</CardTitle>
          <ShieldIcon class="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div class="text-2xl font-bold">{{ stats.activeCases }}</div>
          <p class="text-xs text-muted-foreground">
            {{ stats.casesInProgress }} in progress
          </p>
        </CardContent>
      </Card>
      
      <Card>
        <CardHeader class="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle class="text-sm font-medium">Dump Files</CardTitle>
          <UploadIcon class="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div class="text-2xl font-bold">{{ stats.totalDumps }}</div>
          <p class="text-xs text-muted-foreground">
            {{ formatBytes(stats.totalDumpSize) }} total
          </p>
        </CardContent>
      </Card>
      
      <Card>
        <CardHeader class="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle class="text-sm font-medium">IOCs Detected</CardTitle>
          <AlertTriangleIcon class="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div class="text-2xl font-bold">{{ stats.totalIOCs }}</div>
          <p class="text-xs text-muted-foreground">
            {{ stats.newIOCsToday }} new today
          </p>
        </CardContent>
      </Card>
    </div>
    
    <div class="grid gap-4 md:grid-cols-2">
      <Card>
        <CardHeader>
          <CardTitle>Recent Incidents</CardTitle>
        </CardHeader>
        <CardContent>
          <div class="space-y-4">
            <div
              v-for="incident in recentIncidents"
              :key="incident.id"
              class="flex items-center space-x-4"
            >
              <div class="flex-1 space-y-1">
                <p class="text-sm font-medium leading-none">
                  {{ incident.title }}
                </p>
                <p class="text-sm text-muted-foreground">
                  {{ incident.description }}
                </p>
              </div>
              <div class="text-sm text-muted-foreground">
                {{ formatDate(incident.created_at) }}
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
      
      <Card>
        <CardHeader>
          <CardTitle>Quick Actions</CardTitle>
        </CardHeader>
        <CardContent>
          <div class="space-y-2">
            <Button class="w-full justify-start" @click="$router.push('/incidents/new')">
              <PlusIcon class="mr-2 h-4 w-4" />
              Create New Incident
            </Button>
            <Button class="w-full justify-start" variant="outline" @click="$router.push('/dumps')">
              <UploadIcon class="mr-2 h-4 w-4" />
              Upload Dump File
            </Button>
            <Button class="w-full justify-start" variant="outline" @click="$router.push('/graph')">
              <NetworkIcon class="mr-2 h-4 w-4" />
              View Graph Analysis
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import Card from '@/components/ui/card.vue'
import CardHeader from '@/components/ui/card-header.vue'
import CardContent from '@/components/ui/card-content.vue'
import CardTitle from '@/components/ui/card-title.vue'
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
  // TODO: Implement API calls to fetch real data
  // For now, using mock data
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
}

onMounted(() => {
  fetchDashboardData()
})
</script>
