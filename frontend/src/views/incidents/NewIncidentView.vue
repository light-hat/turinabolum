<template>
  <div class="space-y-6">
    <div>
      <h1 class="text-3xl font-bold tracking-tight">Create New Incident</h1>
      <p class="text-muted-foreground">
        Create a new security incident for investigation
      </p>
    </div>
    
    <Card>
      <CardHeader>
        <CardTitle>Incident Details</CardTitle>
      </CardHeader>
      <CardContent>
        <form @submit.prevent="handleSubmit" class="space-y-6">
          <div class="grid gap-4 md:grid-cols-2">
            <div class="space-y-2">
              <Label for="title">Title *</Label>
              <Input
                id="title"
                v-model="form.title"
                placeholder="Enter incident title"
                required
              />
            </div>
            
            <div class="space-y-2">
              <Label for="severity">Severity *</Label>
              <select
                id="severity"
                v-model="form.severity"
                class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
                required
              >
                <option value="">Select severity</option>
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
                <option value="critical">Critical</option>
              </select>
            </div>
          </div>
          
          <div class="space-y-2">
            <Label for="description">Description *</Label>
            <textarea
              id="description"
              v-model="form.description"
              placeholder="Describe the incident in detail"
              class="flex min-h-[80px] w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
              required
            />
          </div>
          
          <div class="grid gap-4 md:grid-cols-2">
            <div class="space-y-2">
              <Label for="classification">Classification</Label>
              <select
                id="classification"
                v-model="form.classification"
                class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
              >
                <option value="">Select classification</option>
                <option value="malware">Malware</option>
                <option value="phishing">Phishing</option>
                <option value="data_breach">Data Breach</option>
                <option value="network_intrusion">Network Intrusion</option>
                <option value="insider_threat">Insider Threat</option>
                <option value="other">Other</option>
              </select>
            </div>
            
            <div class="space-y-2">
              <Label for="status">Status</Label>
              <select
                id="status"
                v-model="form.status"
                class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
              >
                <option value="open">Open</option>
                <option value="investigating">Investigating</option>
                <option value="resolved">Resolved</option>
                <option value="closed">Closed</option>
              </select>
            </div>
          </div>
          
          <div class="space-y-2">
            <Label for="tags">Tags</Label>
            <Input
              id="tags"
              v-model="form.tags"
              placeholder="Enter tags separated by commas"
            />
            <p class="text-sm text-muted-foreground">
              Separate multiple tags with commas (e.g., malware, banking, trojan)
            </p>
          </div>
          
          <div class="flex items-center gap-4">
            <Button type="submit" :disabled="isSubmitting">
              {{ isSubmitting ? 'Creating...' : 'Create Incident' }}
            </Button>
            <Button type="button" variant="outline" @click="$router.back()">
              Cancel
            </Button>
          </div>
        </form>
      </CardContent>
    </Card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import Card from '@/components/ui/card.vue'
import CardHeader from '@/components/ui/card-header.vue'
import CardContent from '@/components/ui/card-content.vue'
import CardTitle from '@/components/ui/card-title.vue'
import Button from '@/components/ui/button.vue'
import Input from '@/components/ui/input.vue'
import Label from '@/components/ui/label.vue'

const router = useRouter()
const isSubmitting = ref(false)

const form = ref({
  title: '',
  description: '',
  severity: '',
  classification: '',
  status: 'open',
  tags: ''
})

const handleSubmit = async () => {
  isSubmitting.value = true
  
  try {
    // TODO: Implement API call to create incident
    console.log('Creating incident:', form.value)
    
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // Redirect to incidents list
    router.push('/incidents')
  } catch (error) {
    console.error('Error creating incident:', error)
  } finally {
    isSubmitting.value = false
  }
}
</script>
