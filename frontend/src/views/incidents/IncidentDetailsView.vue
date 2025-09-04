<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-3xl font-bold tracking-tight">{{ incident?.title || 'Incident Details' }}</h1>
        <p class="text-muted-foreground">
          Detailed information about the incident
        </p>
      </div>
      <div class="flex items-center gap-2">
        <Button variant="outline" @click="$router.back()">
          Back to Incidents
        </Button>
        <Button>
          Edit Incident
        </Button>
      </div>
    </div>
    
    <div v-if="incident" class="grid gap-6 md:grid-cols-3">
      <!-- Main Content -->
      <div class="md:col-span-2 space-y-6">
        <Card>
          <CardHeader>
            <CardTitle>Description</CardTitle>
          </CardHeader>
          <CardContent>
            <p>{{ incident.description }}</p>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader>
            <CardTitle>Associated Cases</CardTitle>
          </CardHeader>
          <CardContent>
            <div v-if="cases.length > 0" class="space-y-4">
              <div v-for="caseItem in cases" :key="caseItem.id" class="border rounded-lg p-4">
                <h4 class="font-semibold">{{ caseItem.title }}</h4>
                <p class="text-sm text-muted-foreground">{{ caseItem.description }}</p>
                <div class="flex items-center gap-2 mt-2">
                  <span :class="getStatusBadgeClass(caseItem.status)">
                    {{ caseItem.status.toUpperCase() }}
                  </span>
                  <span class="text-sm text-muted-foreground">
                    Created: {{ formatDate(caseItem.created_at) }}
                  </span>
                </div>
              </div>
            </div>
            <div v-else class="text-center py-8 text-muted-foreground">
              No cases associated with this incident
            </div>
          </CardContent>
        </Card>
      </div>
      
      <!-- Sidebar -->
      <div class="space-y-6">
        <Card>
          <CardHeader>
            <CardTitle>Incident Information</CardTitle>
          </CardHeader>
          <CardContent class="space-y-4">
            <div>
              <Label class="text-sm font-medium">Status</Label>
              <div class="mt-1">
                <span :class="getStatusBadgeClass(incident.status)">
                  {{ incident.status.toUpperCase() }}
                </span>
              </div>
            </div>
            
            <div>
              <Label class="text-sm font-medium">Severity</Label>
              <div class="mt-1">
                <span :class="getSeverityBadgeClass(incident.severity)">
                  {{ incident.severity.toUpperCase() }}
                </span>
              </div>
            </div>
            
            <div>
              <Label class="text-sm font-medium">Classification</Label>
              <p class="text-sm">{{ incident.classification || 'Not specified' }}</p>
            </div>
            
            <div>
              <Label class="text-sm font-medium">Created</Label>
              <p class="text-sm">{{ formatDate(incident.created_at) }}</p>
            </div>
            
            <div>
              <Label class="text-sm font-medium">Last Updated</Label>
              <p class="text-sm">{{ formatDate(incident.updated_at) }}</p>
            </div>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader>
            <CardTitle>Quick Actions</CardTitle>
          </CardHeader>
          <CardContent class="space-y-2">
            <Button class="w-full justify-start" variant="outline">
              <PlusIcon class="mr-2 h-4 w-4" />
              Add Case
            </Button>
            <Button class="w-full justify-start" variant="outline">
              <UploadIcon class="mr-2 h-4 w-4" />
              Upload Evidence
            </Button>
            <Button class="w-full justify-start" variant="outline">
              <NetworkIcon class="mr-2 h-4 w-4" />
              View in Graph
            </Button>
          </CardContent>
        </Card>
      </div>
    </div>
    
    <div v-else class="text-center py-12">
      <p class="text-muted-foreground">Loading incident details...</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import Card from '@/components/ui/card.vue'
import CardHeader from '@/components/ui/card-header.vue'
import CardContent from '@/components/ui/card-content.vue'
import CardTitle from '@/components/ui/card-title.vue'
import Button from '@/components/ui/button.vue'
import Label from '@/components/ui/label.vue'
import { PlusIcon, UploadIcon, NetworkIcon } from 'lucide-vue-next'

interface Incident {
  id: number
  title: string
  description: string
  status: 'open' | 'investigating' | 'resolved' | 'closed'
  severity: 'low' | 'medium' | 'high' | 'critical'
  classification?: string
  created_at: string
  updated_at: string
}

interface Case {
  id: number
  title: string
  description: string
  status: string
  created_at: string
}

const route = useRoute()
const incident = ref<Incident | null>(null)
const cases = ref<Case[]>([])

const getStatusBadgeClass = (status: string) => {
  const classes = {
    open: 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300',
    investigating: 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-300',
    resolved: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300',
    closed: 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-300'
  }
  return `px-2 py-1 rounded-full text-xs font-medium ${classes[status as keyof typeof classes]}`
}

const getSeverityBadgeClass = (severity: string) => {
  const classes = {
    low: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300',
    medium: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300',
    high: 'bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-300',
    critical: 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300'
  }
  return `px-2 py-1 rounded-full text-xs font-medium ${classes[severity as keyof typeof classes]}`
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString()
}

const fetchIncident = async () => {
  const incidentId = route.params.id
  // TODO: Implement API call to fetch incident details
  // For now, using mock data
  incident.value = {
    id: Number(incidentId),
    title: 'Malware Analysis - Trojan.Banker',
    description: 'Suspicious banking trojan detected in user workstation. The malware appears to be targeting financial information and credentials.',
    status: 'investigating',
    severity: 'high',
    classification: 'malware',
    created_at: '2024-01-15T10:30:00Z',
    updated_at: '2024-01-15T14:20:00Z'
  }
}

const fetchCases = async () => {
  // TODO: Implement API call to fetch associated cases
  // For now, using mock data
  cases.value = [
    {
      id: 1,
      title: 'Forensic Analysis Case #1',
      description: 'Memory dump analysis and malware reverse engineering',
      status: 'in_progress',
      created_at: '2024-01-15T11:00:00Z'
    },
    {
      id: 2,
      title: 'Network Traffic Analysis',
      description: 'Analysis of network communications during the incident',
      status: 'completed',
      created_at: '2024-01-15T12:00:00Z'
    }
  ]
}

onMounted(() => {
  fetchIncident()
  fetchCases()
})
</script>
