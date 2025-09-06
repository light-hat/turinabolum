<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-3xl font-bold tracking-tight">Incidents</h1>
        <p class="text-muted-foreground">
          Manage and track security incidents
        </p>
      </div>
      <Button @click="$router.push('/incidents/new')">
        <PlusIcon class="mr-2 h-4 w-4" />
        New Incident
      </Button>
    </div>
    
    <!-- Filters -->
    <Card>
      <CardHeader>
        <CardTitle>Filters</CardTitle>
      </CardHeader>
      <CardContent>
        <div class="grid gap-4 md:grid-cols-4">
          <div class="space-y-2">
            <Label for="status">Status</Label>
            <select
              id="status"
              v-model="filters.status"
              class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
            >
              <option value="">All Statuses</option>
              <option value="open">Open</option>
              <option value="investigating">Investigating</option>
              <option value="resolved">Resolved</option>
              <option value="closed">Closed</option>
            </select>
          </div>
          
          <div class="space-y-2">
            <Label for="severity">Severity</Label>
            <select
              id="severity"
              v-model="filters.severity"
              class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
            >
              <option value="">All Severities</option>
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
              <option value="critical">Critical</option>
            </select>
          </div>
          
          <div class="space-y-2">
            <Label for="search">Search</Label>
            <Input
              id="search"
              v-model="filters.search"
              placeholder="Search incidents..."
            />
          </div>
          
          <div class="flex items-end">
            <Button @click="applyFilters" class="w-full">
              Apply Filters
            </Button>
          </div>
        </div>
      </CardContent>
    </Card>
    
    <!-- Incidents List -->
    <div class="space-y-4">
      <Card v-for="incident in filteredIncidents" :key="incident.id" class="cursor-pointer hover:shadow-md transition-shadow" @click="$router.push(`/incidents/${incident.id}`)">
        <CardContent class="p-6">
          <div class="flex items-start justify-between">
            <div class="space-y-2">
              <div class="flex items-center gap-2">
                <h3 class="text-lg font-semibold">{{ incident.title }}</h3>
                <span :class="getSeverityBadgeClass(incident.severity)">
                  {{ incident.severity.toUpperCase() }}
                </span>
                <span :class="getStatusBadgeClass(incident.status)">
                  {{ incident.status.toUpperCase() }}
                </span>
              </div>
              <p class="text-muted-foreground">{{ incident.description }}</p>
              <div class="flex items-center gap-4 text-sm text-muted-foreground">
                <span>Created: {{ formatDate(incident.created_at) }}</span>
                <span>Updated: {{ formatDate(incident.updated_at) }}</span>
                <span v-if="incident.cases_count">Cases: {{ incident.cases_count }}</span>
              </div>
            </div>
            <div class="flex items-center gap-2">
              <Button variant="ghost" size="icon">
                <EyeIcon class="h-4 w-4" />
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
    
    <!-- Pagination -->
    <div class="flex items-center justify-between">
      <p class="text-sm text-muted-foreground">
        Showing {{ filteredIncidents.length }} of {{ incidents.length }} incidents
      </p>
      <div class="flex items-center gap-2">
        <Button variant="outline" size="sm" :disabled="currentPage === 1" @click="currentPage--">
          Previous
        </Button>
        <span class="text-sm">Page {{ currentPage }} of {{ totalPages }}</span>
        <Button variant="outline" size="sm" :disabled="currentPage === totalPages" @click="currentPage++">
          Next
        </Button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import Card from '@/components/ui/card.vue'
import CardHeader from '@/components/ui/card-header.vue'
import CardContent from '@/components/ui/card-content.vue'
import CardTitle from '@/components/ui/card-title.vue'
import Button from '@/components/ui/button.vue'
import Input from '@/components/ui/input.vue'
import Label from '@/components/ui/label.vue'
import { PlusIcon, EyeIcon } from 'lucide-vue-next'

interface Incident {
  id: number
  title: string
  description: string
  status: 'open' | 'investigating' | 'resolved' | 'closed'
  severity: 'low' | 'medium' | 'high' | 'critical'
  created_at: string
  updated_at: string
  cases_count?: number
}

const incidents = ref<Incident[]>([])
const currentPage = ref(1)
const itemsPerPage = 10

const filters = ref({
  status: '',
  severity: '',
  search: ''
})

const filteredIncidents = computed(() => {
  let filtered = incidents.value

  if (filters.value.status) {
    filtered = filtered.filter(incident => incident.status === filters.value.status)
  }

  if (filters.value.severity) {
    filtered = filtered.filter(incident => incident.severity === filters.value.severity)
  }

  if (filters.value.search) {
    const search = filters.value.search.toLowerCase()
    filtered = filtered.filter(incident => 
      incident.title.toLowerCase().includes(search) ||
      incident.description.toLowerCase().includes(search)
    )
  }

  return filtered
})

const totalPages = computed(() => {
  return Math.ceil(filteredIncidents.value.length / itemsPerPage)
})

const getSeverityBadgeClass = (severity: string) => {
  const classes = {
    low: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300',
    medium: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300',
    high: 'bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-300',
    critical: 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300'
  }
  return `px-2 py-1 rounded-full text-xs font-medium ${classes[severity as keyof typeof classes]}`
}

const getStatusBadgeClass = (status: string) => {
  const classes = {
    open: 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300',
    investigating: 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-300',
    resolved: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300',
    closed: 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-300'
  }
  return `px-2 py-1 rounded-full text-xs font-medium ${classes[status as keyof typeof classes]}`
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString()
}

const applyFilters = () => {
  currentPage.value = 1
  // Filters are applied reactively through computed property
}

const fetchIncidents = async () => {
  // TODO: Implement API call to fetch incidents
  // For now, using mock data
  incidents.value = [
    {
      id: 1,
      title: 'Malware Analysis - Trojan.Banker',
      description: 'Suspicious banking trojan detected in user workstation',
      status: 'investigating',
      severity: 'high',
      created_at: '2024-01-15T10:30:00Z',
      updated_at: '2024-01-15T14:20:00Z',
      cases_count: 3
    },
    {
      id: 2,
      title: 'Network Intrusion Investigation',
      description: 'Unauthorized access attempt from external IP',
      status: 'open',
      severity: 'medium',
      created_at: '2024-01-14T15:45:00Z',
      updated_at: '2024-01-14T16:30:00Z',
      cases_count: 1
    },
    {
      id: 3,
      title: 'Data Exfiltration Case',
      description: 'Potential data breach investigation',
      status: 'resolved',
      severity: 'critical',
      created_at: '2024-01-13T09:20:00Z',
      updated_at: '2024-01-14T11:15:00Z',
      cases_count: 5
    }
  ]
}

onMounted(() => {
  fetchIncidents()
})
</script>
