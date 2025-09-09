<script setup lang="ts">
import { cn } from '@/lib/utils'
import type { HTMLAttributes } from 'vue'

const props = defineProps<{
  class?: HTMLAttributes['class']
}>()
</script>

<template>
  <ul :class="cn('grid w-full gap-1 px-2', props.class)">
    <slot />
  </ul>
</template>
