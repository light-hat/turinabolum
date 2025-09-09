<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-3xl font-bold">{{ incident?.title || 'Incident Details' }}</h1>
        <p class="text-muted-foreground">Incident ID: {{ $route.params.id }}</p>
      </div>
      <Button variant="outline" @click="$router.back()">
        <ArrowLeftIcon class="mr-2 h-4 w-4" />
        Back
      </Button>
    </div>
    
    <div v-if="incident" class="grid gap-6 md:grid-cols-2">
      <Card>
        <CardHeader>
          <CardTitle>Incident Information</CardTitle>
        </CardHeader>
        <CardContent class="space-y-4">
          <div>
            <Label class="text-sm font-medium">Title</Label>
            <p class="text-sm text-muted-foreground">{{ incident.title }}</p>
          </div>
          <div>
            <Label class="text-sm font-medium">Description</Label>
            <p class="text-sm text-muted-foreground">{{ incident.description }}</p>
          </div>
          <div>
            <Label class="text-sm font-medium">Severity</Label>
            <Badge :variant="getSeverityVariant(incident.severity)">
              {{ incident.severity }}
            </Badge>
          </div>
          <div>
            <Label class="text-sm font-medium">Created</Label>
            <p class="text-sm text-muted-foreground">{{ formatDate(incident.created_at) }}</p>
          </div>
        </CardContent>
      </Card>
      
      <Card>
        <CardHeader>
          <CardTitle>Investigation Details</CardTitle>
        </CardHeader>
        <CardContent class="space-y-4">
          <div>
            <Label class="text-sm font-medium">Status</Label>
            <Badge variant="outline">{{ incident.status }}</Badge>
          </div>
          <div>
            <Label class="text-sm font-medium">Assigned To</Label>
            <p class="text-sm text-muted-foreground">{{ incident.assigned_to || 'Unassigned' }}</p>
          </div>
          <div>
            <Label class="text-sm font-medium">Last Updated</Label>
            <p class="text-sm text-muted-foreground">{{ formatDate(incident.updated_at) }}</p>
          </div>
        </CardContent>
      </Card>
    </div>
    
    <Card v-else>
      <CardContent class="text-center py-8">
        <p class="text-muted-foreground">Loading incident details...</p>
      </CardContent>
    </Card>
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
import Badge from '@/components/ui/badge.vue'
import { ArrowLeftIcon } from 'lucide-vue-next'

const route = useRoute()

interface Incident {
  id: number
  title: string
  description: string
  severity: 'Low' | 'Medium' | 'High' | 'Critical'
  status: 'Open' | 'In Progress' | 'Closed'
  assigned_to?: string
  created_at: string
  updated_at: string
}

const incident = ref<Incident | null>(null)

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString()
}

const getSeverityVariant = (severity: string) => {
  switch (severity) {
    case 'Critical': return 'destructive'
    case 'High': return 'destructive'
    case 'Medium': return 'default'
    case 'Low': return 'secondary'
    default: return 'default'
  }
}

const fetchIncident = async () => {
  const incidentId = route.params.id
  
  try {
    // TODO: Implement API call to fetch incident details
    // For now, using mock data
    incident.value = {
      id: Number(incidentId),
      title: 'Malware Analysis - Trojan.Banker',
      description: 'Suspicious banking trojan detected in user workstation. The malware appears to be targeting financial information and credentials.',
      severity: 'High',
      status: 'In Progress',
      assigned_to: 'John Doe',
      created_at: '2024-01-15T10:30:00Z',
      updated_at: '2024-01-15T14:20:00Z'
    }
  } catch (error) {
    console.error('Error fetching incident:', error)
  }
}

onMounted(() => {
  fetchIncident()
})
</script>