<script setup lang="ts">
import { inject } from 'vue'
import { cn } from '@/lib/utils'

interface CollapsibleContext {
  open: { value: boolean }
  onOpenChange: (open: boolean) => void
}

const context = inject<CollapsibleContext>('collapsible')

const toggle = () => {
  if (context) {
    context.onOpenChange(!context.open.value)
  }
}

const props = defineProps<{
  asChild?: boolean
  class?: string
}>()
</script>

<template>
  <button
    :class="cn('w-full', props.class)"
    @click="toggle"
  >
    <slot />
  </button>
</template>
