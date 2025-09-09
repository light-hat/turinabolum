<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <h1 class="text-3xl font-bold">New Incident</h1>
      <Button variant="outline" @click="$router.back()">
        <ArrowLeftIcon class="mr-2 h-4 w-4" />
        Back
      </Button>
    </div>
    
    <Card>
      <CardHeader>
        <CardTitle>Create New Incident</CardTitle>
        <CardDescription>
          Fill in the details to create a new security incident
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form @submit.prevent="handleSubmit" class="space-y-4">
          <div class="grid gap-4 md:grid-cols-2">
            <div class="space-y-2">
              <Label for="title">Title</Label>
              <Input
                id="title"
                v-model="form.title"
                placeholder="Enter incident title"
                required
              />
            </div>
            <div class="space-y-2">
              <Label for="severity">Severity</Label>
              <Select v-model="form.severity">
                <SelectTrigger>
                  <SelectValue placeholder="Select severity" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="Low">Low</SelectItem>
                  <SelectItem value="Medium">Medium</SelectItem>
                  <SelectItem value="High">High</SelectItem>
                  <SelectItem value="Critical">Critical</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
          
          <div class="space-y-2">
            <Label for="description">Description</Label>
            <Textarea
              id="description"
              v-model="form.description"
              placeholder="Enter incident description"
              rows="4"
              required
            />
          </div>
          
          <div class="flex justify-end space-x-2">
            <Button type="button" variant="outline" @click="$router.back()">
              Cancel
            </Button>
            <Button type="submit" :disabled="isSubmitting">
              {{ isSubmitting ? 'Creating...' : 'Create Incident' }}
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
import CardDescription from '@/components/ui/card-description.vue'
import Button from '@/components/ui/button.vue'
import Input from '@/components/ui/input.vue'
import Label from '@/components/ui/label.vue'
import Textarea from '@/components/ui/textarea.vue'
import Select from '@/components/ui/select.vue'
import SelectContent from '@/components/ui/select-content.vue'
import SelectItem from '@/components/ui/select-item.vue'
import SelectTrigger from '@/components/ui/select-trigger.vue'
import SelectValue from '@/components/ui/select-value.vue'
import { ArrowLeftIcon } from 'lucide-vue-next'

const router = useRouter()

const form = ref({
  title: '',
  description: '',
  severity: 'Medium'
})

const isSubmitting = ref(false)

const handleSubmit = async () => {
  isSubmitting.value = true
  
  try {
    // TODO: Implement API call to create incident
    console.log('Creating incident:', form.value)
    
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // Redirect to incidents list
    router.push('/dashboard/incidents')
  } catch (error) {
    console.error('Error creating incident:', error)
  } finally {
    isSubmitting.value = false
  }
}
</script>