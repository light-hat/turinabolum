<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-3xl font-bold tracking-tight">Dump Uploads</h1>
        <p class="text-muted-foreground">
          Upload and manage memory dumps for investigation
        </p>
      </div>
      <Button @click="showUploadDialog = true">
        <UploadIcon class="mr-2 h-4 w-4" />
        Upload Dump
      </Button>
    </div>
    
    <!-- Upload Dialog -->
    <div v-if="showUploadDialog" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <Card class="w-full max-w-md">
        <CardHeader>
          <CardTitle>Upload Dump File</CardTitle>
        </CardHeader>
        <CardContent>
          <form @submit.prevent="handleUpload" class="space-y-4">
            <div class="space-y-2">
              <Label for="file">Select File</Label>
              <Input
                id="file"
                type="file"
                @change="handleFileSelect"
                accept=".dmp,.raw,.img,.vmem"
                required
              />
              <p class="text-sm text-muted-foreground">
                Supported formats: .dmp, .raw, .img, .vmem
              </p>
            </div>
            
            <div class="space-y-2">
              <Label for="description">Description</Label>
              <textarea
                id="description"
                v-model="uploadForm.description"
                placeholder="Describe the dump file"
                class="flex min-h-[80px] w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
              />
            </div>
            
            <div class="space-y-2">
              <Label for="case">Associated Case</Label>
              <select
                id="case"
                v-model="uploadForm.case_id"
                class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
              >
                <option value="">Select a case (optional)</option>
                <option v-for="caseItem in cases" :key="caseItem.id" :value="caseItem.id">
                  {{ caseItem.title }}
                </option>
              </select>
            </div>
            
            <div class="flex items-center gap-4">
              <Button type="submit" :disabled="isUploading || !selectedFile">
                {{ isUploading ? 'Uploading...' : 'Upload' }}
              </Button>
              <Button type="button" variant="outline" @click="showUploadDialog = false">
                Cancel
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
    
    <!-- Dumps List -->
    <div class="space-y-4">
      <Card v-for="dump in dumps" :key="dump.id">
        <CardContent class="p-6">
          <div class="flex items-start justify-between">
            <div class="space-y-2">
              <div class="flex items-center gap-2">
                <h3 class="text-lg font-semibold">{{ dump.filename }}</h3>
                <span class="px-2 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300">
                  {{ dump.file_type?.toUpperCase() || 'UNKNOWN' }}
                </span>
              </div>
              <p class="text-muted-foreground">{{ dump.description || 'No description provided' }}</p>
              <div class="flex items-center gap-4 text-sm text-muted-foreground">
                <span>Size: {{ formatBytes(dump.file_size) }}</span>
                <span>Uploaded: {{ formatDate(dump.created_at) }}</span>
                <span v-if="dump.case">Case: {{ dump.case.title }}</span>
              </div>
              <div v-if="dump.md5_hash || dump.sha1_hash || dump.sha256_hash" class="flex items-center gap-4 text-xs text-muted-foreground">
                <span v-if="dump.md5_hash">MD5: {{ dump.md5_hash }}</span>
                <span v-if="dump.sha1_hash">SHA1: {{ dump.sha1_hash }}</span>
                <span v-if="dump.sha256_hash">SHA256: {{ dump.sha256_hash }}</span>
              </div>
            </div>
            <div class="flex items-center gap-2">
              <Button variant="ghost" size="icon" @click="downloadDump(dump)">
                <DownloadIcon class="h-4 w-4" />
              </Button>
              <Button variant="ghost" size="icon" @click="deleteDump(dump.id)">
                <TrashIcon class="h-4 w-4" />
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
    
    <!-- Empty State -->
    <div v-if="dumps.length === 0" class="text-center py-12">
      <UploadIcon class="mx-auto h-12 w-12 text-muted-foreground" />
      <h3 class="mt-4 text-lg font-semibold">No dump files uploaded</h3>
      <p class="text-muted-foreground">Get started by uploading your first memory dump.</p>
      <Button class="mt-4" @click="showUploadDialog = true">
        <UploadIcon class="mr-2 h-4 w-4" />
        Upload Dump
      </Button>
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
import Input from '@/components/ui/input.vue'
import Label from '@/components/ui/label.vue'
import { UploadIcon, DownloadIcon, TrashIcon } from 'lucide-vue-next'

interface DumpUpload {
  id: number
  filename: string
  file_size: number
  file_type?: string
  description?: string
  md5_hash?: string
  sha1_hash?: string
  sha256_hash?: string
  created_at: string
  case?: {
    id: number
    title: string
  }
}

interface Case {
  id: number
  title: string
}

const dumps = ref<DumpUpload[]>([])
const cases = ref<Case[]>([])
const showUploadDialog = ref(false)
const isUploading = ref(false)
const selectedFile = ref<File | null>(null)

const uploadForm = ref({
  description: '',
  case_id: ''
})

const formatBytes = (bytes: number) => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString()
}

const handleFileSelect = (event: Event) => {
  const target = event.target as HTMLInputElement
  if (target.files && target.files[0]) {
    selectedFile.value = target.files[0]
  }
}

const handleUpload = async () => {
  if (!selectedFile.value) return
  
  isUploading.value = true
  
  try {
    const formData = new FormData()
    formData.append('file', selectedFile.value)
    formData.append('description', uploadForm.value.description)
    if (uploadForm.value.case_id) {
      formData.append('case', uploadForm.value.case_id)
    }
    
    // TODO: Implement API call to upload dump
    console.log('Uploading dump:', formData)
    
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    // Reset form and close dialog
    uploadForm.value = { description: '', case_id: '' }
    selectedFile.value = null
    showUploadDialog.value = false
    
    // Refresh dumps list
    await fetchDumps()
  } catch (error) {
    console.error('Error uploading dump:', error)
  } finally {
    isUploading.value = false
  }
}

const downloadDump = (dump: DumpUpload) => {
  // TODO: Implement download functionality
  console.log('Downloading dump:', dump)
}

const deleteDump = async (dumpId: number) => {
  if (!confirm('Are you sure you want to delete this dump file?')) return
  
  try {
    // TODO: Implement API call to delete dump
    console.log('Deleting dump:', dumpId)
    
    // Remove from local list
    dumps.value = dumps.value.filter(dump => dump.id !== dumpId)
  } catch (error) {
    console.error('Error deleting dump:', error)
  }
}

const fetchDumps = async () => {
  // TODO: Implement API call to fetch dumps
  // For now, using mock data
  dumps.value = [
    {
      id: 1,
      filename: 'workstation_memory.dmp',
      file_size: 8589934592, // 8GB
      file_type: 'dmp',
      description: 'Memory dump from infected workstation',
      md5_hash: 'a1b2c3d4e5f6789012345678901234567',
      sha1_hash: '1234567890abcdef1234567890abcdef12345678',
      sha256_hash: 'abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890',
      created_at: '2024-01-15T10:30:00Z',
      case: {
        id: 1,
        title: 'Malware Analysis - Trojan.Banker'
      }
    },
    {
      id: 2,
      filename: 'server_crash.raw',
      file_size: 4294967296, // 4GB
      file_type: 'raw',
      description: 'Server crash dump for analysis',
      md5_hash: 'b2c3d4e5f67890123456789012345678',
      sha1_hash: '234567890abcdef1234567890abcdef123456789',
      sha256_hash: 'bcdef1234567890abcdef1234567890abcdef1234567890abcdef12345678901',
      created_at: '2024-01-14T15:45:00Z'
    }
  ]
}

const fetchCases = async () => {
  // TODO: Implement API call to fetch cases
  // For now, using mock data
  cases.value = [
    { id: 1, title: 'Malware Analysis - Trojan.Banker' },
    { id: 2, title: 'Network Intrusion Investigation' },
    { id: 3, title: 'Data Exfiltration Case' }
  ]
}

onMounted(() => {
  fetchDumps()
  fetchCases()
})
</script>
