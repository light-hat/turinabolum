<template>
  <div class="space-y-6">
    <div>
      <h1 class="text-3xl font-bold tracking-tight">Profile Settings</h1>
      <p class="text-muted-foreground">
        Manage your account settings and preferences
      </p>
    </div>
    
    <div class="grid gap-6 md:grid-cols-2">
      <!-- Profile Information -->
      <Card>
        <CardHeader>
          <CardTitle>Profile Information</CardTitle>
        </CardHeader>
        <CardContent>
          <form @submit.prevent="handleProfileUpdate" class="space-y-4">
            <div class="space-y-2">
              <Label for="username">Username</Label>
              <Input
                id="username"
                v-model="profileForm.username"
                :disabled="authStore.isLoading"
              />
            </div>
            
            <div class="space-y-2">
              <Label for="email">Email</Label>
              <Input
                id="email"
                v-model="profileForm.email"
                type="email"
                :disabled="authStore.isLoading"
              />
            </div>
            
            <div class="grid gap-4 md:grid-cols-2">
              <div class="space-y-2">
                <Label for="first_name">First Name</Label>
                <Input
                  id="first_name"
                  v-model="profileForm.first_name"
                  :disabled="authStore.isLoading"
                />
              </div>
              
              <div class="space-y-2">
                <Label for="last_name">Last Name</Label>
                <Input
                  id="last_name"
                  v-model="profileForm.last_name"
                  :disabled="authStore.isLoading"
                />
              </div>
            </div>
            
            <Button type="submit" :disabled="authStore.isLoading">
              {{ authStore.isLoading ? 'Updating...' : 'Update Profile' }}
            </Button>
          </form>
        </CardContent>
      </Card>
      
      <!-- Password Change -->
      <Card>
        <CardHeader>
          <CardTitle>Change Password</CardTitle>
        </CardHeader>
        <CardContent>
          <form @submit.prevent="handlePasswordChange" class="space-y-4">
            <div class="space-y-2">
              <Label for="current_password">Current Password</Label>
              <Input
                id="current_password"
                v-model="passwordForm.current_password"
                type="password"
                :disabled="authStore.isLoading"
              />
            </div>
            
            <div class="space-y-2">
              <Label for="new_password">New Password</Label>
              <Input
                id="new_password"
                v-model="passwordForm.new_password"
                type="password"
                :disabled="authStore.isLoading"
              />
            </div>
            
            <div class="space-y-2">
              <Label for="confirm_password">Confirm New Password</Label>
              <Input
                id="confirm_password"
                v-model="passwordForm.confirm_password"
                type="password"
                :disabled="authStore.isLoading"
              />
            </div>
            
            <Button type="submit" :disabled="authStore.isLoading || !passwordsMatch">
              {{ authStore.isLoading ? 'Changing...' : 'Change Password' }}
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
    
    <!-- Theme Settings -->
    <Card>
      <CardHeader>
        <CardTitle>Appearance</CardTitle>
      </CardHeader>
      <CardContent>
        <div class="space-y-4">
          <div class="space-y-2">
            <Label>Theme</Label>
            <div class="flex items-center gap-4">
              <Button
                v-for="theme in themes"
                :key="theme.value"
                :variant="themeStore.theme === theme.value ? 'default' : 'outline'"
                @click="themeStore.setTheme(theme.value)"
              >
                <component :is="theme.icon" class="mr-2 h-4 w-4" />
                {{ theme.label }}
              </Button>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
    
    <!-- Account Actions -->
    <Card>
      <CardHeader>
        <CardTitle>Account Actions</CardTitle>
      </CardHeader>
      <CardContent>
        <div class="space-y-4">
          <div class="flex items-center justify-between">
            <div>
              <h4 class="font-medium">Delete Account</h4>
              <p class="text-sm text-muted-foreground">
                Permanently delete your account and all associated data
              </p>
            </div>
            <Button variant="destructive" @click="showDeleteDialog = true">
              Delete Account
            </Button>
          </div>
        </div>
      </CardContent>
    </Card>
    
    <!-- Delete Confirmation Dialog -->
    <div v-if="showDeleteDialog" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <Card class="w-full max-w-md">
        <CardHeader>
          <CardTitle class="text-destructive">Delete Account</CardTitle>
        </CardHeader>
        <CardContent>
          <p class="text-sm text-muted-foreground mb-4">
            Are you sure you want to delete your account? This action cannot be undone.
          </p>
          <div class="flex items-center gap-4">
            <Button variant="destructive" @click="handleDeleteAccount">
              Yes, Delete Account
            </Button>
            <Button variant="outline" @click="showDeleteDialog = false">
              Cancel
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useThemeStore } from '@/stores/theme'
import Card from '@/components/ui/card.vue'
import CardHeader from '@/components/ui/card-header.vue'
import CardContent from '@/components/ui/card-content.vue'
import CardTitle from '@/components/ui/card-title.vue'
import Button from '@/components/ui/button.vue'
import Input from '@/components/ui/input.vue'
import Label from '@/components/ui/label.vue'
import { SunIcon, MoonIcon, MonitorIcon } from 'lucide-vue-next'

const router = useRouter()
const authStore = useAuthStore()
const themeStore = useThemeStore()

const showDeleteDialog = ref(false)

const profileForm = ref({
  username: '',
  email: '',
  first_name: '',
  last_name: ''
})

const passwordForm = ref({
  current_password: '',
  new_password: '',
  confirm_password: ''
})

const themes: Array<{ value: 'light' | 'dark' | 'system', label: string, icon: any }> = [
  { value: 'light', label: 'Light', icon: SunIcon },
  { value: 'dark', label: 'Dark', icon: MoonIcon },
  { value: 'system', label: 'System', icon: MonitorIcon }
]

const passwordsMatch = computed(() => {
  return passwordForm.value.new_password === passwordForm.value.confirm_password &&
         passwordForm.value.new_password.length > 0
})

const handleProfileUpdate = async () => {
  const result = await authStore.updateProfile(profileForm.value)
  if (result.success) {
    // Profile updated successfully
    console.log('Profile updated')
  }
}

const handlePasswordChange = async () => {
  if (!passwordsMatch.value) {
    return
  }
  
  const result = await authStore.changePassword(
    passwordForm.value.current_password,
    passwordForm.value.new_password
  )
  
  if (result.success) {
    passwordForm.value = {
      current_password: '',
      new_password: '',
      confirm_password: ''
    }
    console.log('Password changed successfully')
  }
}

const handleDeleteAccount = async () => {
  // TODO: Implement account deletion
  console.log('Account deletion requested')
  showDeleteDialog.value = false
}

const loadUserData = () => {
  if (authStore.user) {
    profileForm.value = {
      username: authStore.user.username,
      email: authStore.user.email,
      first_name: authStore.user.first_name || '',
      last_name: authStore.user.last_name || ''
    }
  }
}

onMounted(() => {
  loadUserData()
})
</script>
