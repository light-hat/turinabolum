<script setup lang="ts">
import { provide, ref, type Ref } from 'vue'
import { cn } from '@/lib/utils'

interface CollapsibleContext {
  open: Ref<boolean>
  onOpenChange: (open: boolean) => void
}

const props = withDefaults(defineProps<{
  defaultOpen?: boolean
  open?: boolean
  disabled?: boolean
  class?: string
}>(), {
  defaultOpen: false,
  disabled: false
})

const emit = defineEmits<{
  'update:open': [open: boolean]
}>()

const open = ref(props.open ?? props.defaultOpen)

const onOpenChange = (value: boolean) => {
  open.value = value
  emit('update:open', value)
}

provide<CollapsibleContext>('collapsible', {
  open,
  onOpenChange
})
</script>

<template>
  <div :class="cn('group/collapsible', props.class)">
    <slot />
  </div>
</template>
