<template>
  <div
    :class="cn('px-3 py-2 text-xs font-semibold text-muted-foreground', props.class)"
    v-bind="$attrs"
  >
    <slot />
  </div>
</template>

<script setup lang="ts">
import { cn } from '@/lib/utils'
import type { HTMLAttributes } from 'vue'

const props = withDefaults(defineProps<{
  class?: HTMLAttributes['class']
}>(), {})

defineOptions({
  inheritAttrs: false
})
</script>
