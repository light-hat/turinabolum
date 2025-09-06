<template>
  <div class="w-full h-screen flex items-center justify-center px-4">
    <Card class="mx-auto max-w-sm">
      <CardHeader>
        <CardTitle class="text-2xl">Login</CardTitle>
        <CardDescription>
          Enter your username below to login to your account
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form @submit.prevent="handleLogin" class="grid gap-4">
          <div class="grid gap-2">
            <Label for="username">Username</Label>
            <input
              id="username"
              v-model="form.username"
              type="text"
              placeholder="admin"
              autocomplete="username"
              required
              :disabled="authStore.isLoading"
              class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
            />
          </div>
          
          <div class="grid gap-2">
            <div class="flex items-center">
              <Label for="password">Password</Label>
              <a href="#" class="ml-auto inline-block text-sm underline">
                Forgot your password?
              </a>
            </div>
            <input
              id="password"
              v-model="form.password"
              type="password"
              autocomplete="current-password"
              required
              :disabled="authStore.isLoading"
              class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
            />
          </div>
          
          <div v-if="authStore.error" class="text-sm text-destructive">
            {{ authStore.error }}
          </div>
          
          <Button
            type="submit"
            class="w-full"
            :disabled="authStore.isLoading"
          >
            {{ authStore.isLoading ? 'Signing in...' : 'Login' }}
          </Button>
          
          <Button variant="outline" class="w-full" type="button">
            Login with Google
          </Button>
        </form>
        
        <div class="mt-4 text-center text-sm">
          Don't have an account?
          <router-link to="/register" class="underline">
            Sign up
          </router-link>
        </div>
      </CardContent>
    </Card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import Card from '@/components/ui/card.vue'
import CardHeader from '@/components/ui/card-header.vue'
import CardContent from '@/components/ui/card-content.vue'
import CardTitle from '@/components/ui/card-title.vue'
import CardDescription from '@/components/ui/card-description.vue'
import Button from '@/components/ui/button.vue'
import Input from '@/components/ui/input.vue'
import Label from '@/components/ui/label.vue'

const router = useRouter()
const authStore = useAuthStore()

const form = ref({
  username: '',
  password: ''
})

const handleLogin = async () => {
  console.log('Form data before login:', form.value)
  console.log('Form data keys:', Object.keys(form.value))
  console.log('Username value:', form.value.username)
  console.log('Password value:', form.value.password)
  
  const result = await authStore.login(form.value)
  if (result.success) {
    router.push('/dashboard')
  }
}

onMounted(() => {
  // Redirect if already authenticated
  if (authStore.isAuthenticated) {
    router.push('/dashboard')
  }
})
</script>
