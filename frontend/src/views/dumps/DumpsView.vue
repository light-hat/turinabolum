<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <h1 class="text-3xl font-bold">Dump Uploads</h1>
      <Button @click="showUploadDialog = true">
        <UploadIcon class="mr-2 h-4 w-4" />
        Upload Dump
      </Button>
    </div>
    
    <Card>
      <CardHeader>
        <CardTitle>Uploaded Dumps</CardTitle>
        <CardDescription>
          Manage and analyze uploaded dump files
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div class="space-y-4">
          <div
            v-for="dump in dumps"
            :key="dump.id"
            class="flex items-center justify-between p-4 border rounded-lg"
          >
            <div class="flex items-center space-x-4">
              <FileIcon class="h-8 w-8 text-muted-foreground" />
              <div>
                <p class="font-medium">{{ dump.filename }}</p>
                <p class="text-sm text-muted-foreground">
                  {{ formatBytes(dump.file_size) }} • {{ formatDate(dump.uploaded_at) }}
                </p>
              </div>
            </div>
            <div class="flex items-center space-x-2">
              <Button variant="outline" size="sm">
                <DownloadIcon class="h-4 w-4" />
              </Button>
              <Button variant="outline" size="sm">
                <TrashIcon class="h-4 w-4" />
              </Button>
            </div>
          </div>
          
          <div v-if="dumps.length === 0" class="text-center py-8 text-muted-foreground">
            No dump files uploaded yet
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
import {
  UploadIcon,
  FileIcon,
  DownloadIcon,
  TrashIcon
} from 'lucide-vue-next'

interface DumpFile {
  id: number
  filename: string
  file_size: number
  uploaded_at: string
}

const dumps = ref<DumpFile[]>([])
const showUploadDialog = ref(false)

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

const fetchDumps = async () => {
  // TODO: Implement API call to fetch dumps
  // For now, using mock data
  dumps.value = [
    {
      id: 1,
      filename: 'malware_sample_001.dmp',
      file_size: 52428800, // 50MB
      uploaded_at: '2024-01-15T10:30:00Z'
    },
    {
      id: 2,
      filename: 'network_capture_002.pcap',
      file_size: 104857600, // 100MB
      uploaded_at: '2024-01-14T15:45:00Z'
    }
  ]
}

onMounted(() => {
  fetchDumps()
})
</script>