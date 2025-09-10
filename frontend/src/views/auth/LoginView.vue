<template>
    <div class="min-h-screen flex items-center justify-center">
        <Card class="w-full max-w-sm">
            <CardHeader>
                <CardTitle class="text-2xl">
                    Login
                </CardTitle>
                <CardDescription>
                    Enter your email below to login to your account.
                </CardDescription>
            </CardHeader>
            <CardContent class="grid gap-4">
                <div class="grid gap-2">
                    <Label for="email">Email</Label>
                    <Input id="email" type="email" placeholder="m@example.com" required />
                </div>
                <div class="grid gap-2">
                    <Label for="password">Password</Label>
                    <Input id="password" type="password" required />
                </div>
            </CardContent>


            <CardContent class="grid gap-4">
                <form @submit.prevent="handleLogin" class="grid gap-4">
                <div class="grid gap-2">
                    <Label for="username">Username</Label>
                    <Input 
                    id="username" 
                    v-model="form.username"
                    type="text" 
                    placeholder="Enter your username" 
                    autocomplete="username"
                    required 
                    :disabled="authStore.isLoading"
                    class="h-11 "
                    />
                </div>
                <div class="grid gap-2">
                    <Label for="password">Password</Label>
                    <Input 
                    id="password" 
                    v-model="form.password"
                    type="password" 
                    placeholder="Enter your password"
                    autocomplete="current-password"
                    required 
                    :disabled="authStore.isLoading"
                    class="h-11 "
                    />
                </div>

                <div v-if="authStore.error" class="p-3 text-sm text-red-600 dark:text-red-400 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-md ">
                {{ authStore.error }}
                </div>
                </form>
            </CardContent>


            <CardFooter>
                <Button 
                class="w-full"
                type="submit"
                @click="handleLogin"
                :disabled="authStore.isLoading">
                    Sign in
                </Button>
            </CardFooter>
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
import CardFooter from '@/components/ui/card-footer.vue'
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

