<script setup lang="ts">
import { cnWithAttrs } from '@/lib/utils'

defineOptions({
  inheritAttrs: false
})
</script>

<template>
  <div 
    :class="cnWithAttrs('flex items-center p-6 pt-0', $attrs.class)"
    v-bind="$attrs"
  >
    <slot />
  </div>
</template>
