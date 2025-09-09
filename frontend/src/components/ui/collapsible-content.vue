<script setup lang="ts">
import { inject, ref, watch, onMounted, onUnmounted } from 'vue'
import { cn } from '@/lib/utils'

interface CollapsibleContext {
  open: { value: boolean }
  onOpenChange: (open: boolean) => void
}

const context = inject<CollapsibleContext>('collapsible')
const isOpen = ref(false)

const updateOpen = () => {
  if (context) {
    isOpen.value = context.open.value
  }
}

watch(() => context?.open.value, updateOpen, { immediate: true })

onMounted(() => {
  updateOpen()
})

const props = defineProps<{
  class?: string
}>()
</script>

<template>
  <div
    v-show="isOpen"
    :class="cn('overflow-hidden transition-all duration-200', props.class)"
  >
    <slot />
  </div>
</template>
