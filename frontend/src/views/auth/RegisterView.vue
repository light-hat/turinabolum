<template>
  <div class="w-full h-screen flex items-center justify-center px-4">
    <Card class="mx-auto max-w-sm">
      <CardHeader>
        <CardTitle class="text-xl">Sign Up</CardTitle>
        <CardDescription>
          Enter your information to create an account
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form @submit.prevent="handleRegister" class="grid gap-4">
          <div class="grid grid-cols-2 gap-4">
            <div class="grid gap-2">
              <Label for="first_name">First name</Label>
              <Input
                id="first_name"
                v-model="form.first_name"
                type="text"
                placeholder="Max"
                :disabled="authStore.isLoading"
              />
            </div>
            <div class="grid gap-2">
              <Label for="last_name">Last name</Label>
              <Input
                id="last_name"
                v-model="form.last_name"
                type="text"
                placeholder="Robinson"
                :disabled="authStore.isLoading"
              />
            </div>
          </div>
          
          <div class="grid gap-2">
            <Label for="email">Email</Label>
            <Input
              id="email"
              v-model="form.email"
              type="email"
              placeholder="m@example.com"
              required
              :disabled="authStore.isLoading"
            />
          </div>
          
          <div class="grid gap-2">
            <Label for="password">Password</Label>
            <Input
              id="password"
              v-model="form.password"
              type="password"
              required
              :disabled="authStore.isLoading"
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
            {{ authStore.isLoading ? 'Creating account...' : 'Create an account' }}
          </Button>
          
          <Button variant="outline" class="w-full" type="button">
            Sign up with GitHub
          </Button>
        </form>
        
        <div class="mt-4 text-center text-sm">
          Already have an account?
          <router-link to="/login" class="underline">
            Sign in
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
  email: '',
  first_name: '',
  last_name: '',
  password: ''
})

const handleRegister = async () => {
  const result = await authStore.register(form.value)
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
