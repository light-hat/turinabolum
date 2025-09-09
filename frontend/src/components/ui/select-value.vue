<template>
  <span :class="cn('block truncate', props.class)">
    <slot />
  </span>
</template>

<script setup lang="ts">
import { cn } from '@/lib/utils'
import type { HTMLAttributes } from 'vue'

const props = defineProps<{
  placeholder?: string
  class?: HTMLAttributes['class']
}>()
</script>
