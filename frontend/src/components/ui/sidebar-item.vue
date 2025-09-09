<template>
  <router-link
    :to="to"
    :class="cnWithAttrs(
      `flex items-center gap-3 rounded-lg px-3 py-2 text-sm transition-all hover:text-primary ${isActive ? 'bg-muted text-primary' : 'text-muted-foreground'}`,
      $attrs.class
    )"
    v-bind="$attrs"
  >
    <component :is="icon" class="h-4 w-4" />
    <span>{{ label }}</span>
    <slot />
  </router-link>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { cnWithAttrs } from "@/lib/utils"

interface Props {
  to: string
  label: string
  icon?: any
}

const props = defineProps<Props>()
const route = useRoute()

const isActive = computed(() => route.path === props.to)
</script>
