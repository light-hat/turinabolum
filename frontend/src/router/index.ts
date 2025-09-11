import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/dashboard'
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/auth/LoginView.vue'),
      meta: { requiresGuest: true }
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('@/views/auth/RegisterView.vue'),
      meta: { requiresGuest: true }
    },
    // {
    //   path: '/dashboard',
    //   name: 'dashboard',
    //   component: () => import('@/components/layout/DashboardLayout.vue'),
    //   meta: { requiresAuth: true },
    //   children: [
    //     {
    //       path: '',
    //       name: 'dashboard-home',
    //       component: () => import('@/views/dashboard/DashboardView.vue')
    //     },
    //     {
    //       path: 'incidents',
    //       name: 'incidents',
    //       component: () => import('@/views/incidents/IncidentsView.vue')
    //     },
    //     {
    //       path: 'incidents/new',
    //       name: 'new-incident',
    //       component: () => import('@/views/incidents/NewIncidentView.vue')
    //     },
    //     {
    //       path: 'incidents/:id',
    //       name: 'incident-details',
    //       component: () => import('@/views/incidents/IncidentDetailsView.vue'),
    //       props: true
    //     },
    //     {
    //       path: 'dumps',
    //       name: 'dumps',
    //       component: () => import('@/views/dumps/DumpsView.vue')
    //     },
    //     {
    //       path: 'graph',
    //       name: 'graph',
    //       component: () => import('@/views/graph/GraphView.vue')
    //     },
    //     {
    //       path: 'profile',
    //       name: 'profile',
    //       component: () => import('@/views/ProfileView.vue')
    //     }
    //   ]
    // }
  ]
})

// Navigation guards
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()
  
  // Initialize auth store if not already done
  if (!authStore.isAuthenticated && localStorage.getItem('access_token')) {
    await authStore.init()
  }
  
  // Check if route requires authentication
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
    return
  }
  
  // Check if route requires guest (not authenticated)
  if (to.meta.requiresGuest && authStore.isAuthenticated) {
    next('/dashboard')
    return
  }
  
  next()
})

export default router