<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <h1 class="text-3xl font-bold">Incidents</h1>
      <Button @click="$router.push('/dashboard/incidents/new')">
        <PlusIcon class="mr-2 h-4 w-4" />
        New Incident
      </Button>
    </div>
    
    <Card>
      <CardHeader>
        <CardTitle>All Incidents</CardTitle>
        <CardDescription>
          View and manage security incidents
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div class="space-y-4">
          <div
            v-for="incident in incidents"
            :key="incident.id"
            class="flex items-center justify-between p-4 border rounded-lg hover:bg-muted/50"
            @click="$router.push(`/dashboard/incidents/${incident.id}`)"
          >
            <div class="flex items-center space-x-4">
              <div class="flex h-8 w-8 items-center justify-center rounded-full bg-primary text-primary-foreground text-sm">
                {{ incident.severity.charAt(0) }}
              </div>
              <div>
                <p class="font-medium">{{ incident.title }}</p>
                <p class="text-sm text-muted-foreground">{{ incident.description }}</p>
              </div>
            </div>
            <div class="flex items-center space-x-4">
              <Badge :variant="getSeverityVariant(incident.severity)">
                {{ incident.severity }}
              </Badge>
              <span class="text-sm text-muted-foreground">
                {{ formatDate(incident.created_at) }}
              </span>
            </div>
          </div>
          
          <div v-if="incidents.length === 0" class="text-center py-8 text-muted-foreground">
            No incidents found
          </div>
        </div>
      </CardContent>
    </Card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import Card from '@/components/ui/card.vue'
import CardHeader from '@/components/ui/card-header.vue'
import CardContent from '@/components/ui/card-content.vue'
import CardTitle from '@/components/ui/card-title.vue'
import CardDescription from '@/components/ui/card-description.vue'
import Button from '@/components/ui/button.vue'
import Badge from '@/components/ui/badge.vue'
import { PlusIcon } from 'lucide-vue-next'

interface Incident {
  id: number
  title: string
  description: string
  severity: 'Low' | 'Medium' | 'High' | 'Critical'
  created_at: string
}

const incidents = ref<Incident[]>([])

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

const fetchIncidents = async () => {
  // TODO: Implement API call to fetch incidents
  // For now, using mock data
  incidents.value = [
    {
      id: 1,
      title: 'Malware Analysis - Trojan.Banker',
      description: 'Suspicious banking trojan detected in user workstation',
      severity: 'High',
      created_at: '2024-01-15T10:30:00Z'
    },
    {
      id: 2,
      title: 'Network Intrusion Investigation',
      description: 'Unauthorized access attempt from external IP',
      severity: 'Medium',
      created_at: '2024-01-14T15:45:00Z'
    },
    {
      id: 3,
      title: 'Data Exfiltration Case',
      description: 'Potential data breach investigation',
      severity: 'Critical',
      created_at: '2024-01-13T09:20:00Z'
    }
  ]
}

onMounted(() => {
  fetchIncidents()
})
</script>