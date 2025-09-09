<template>
  <div
    :class="cnWithAttrs(
      `shrink-0 bg-border ${orientation === 'horizontal' ? 'h-[1px] w-full' : 'h-full w-[1px]'}`,
      $attrs.class
    )"
    v-bind="$attrs"
  />
</template>

<script setup lang="ts">
import { cnWithAttrs } from "@/lib/utils"

interface Props {
  orientation?: 'horizontal' | 'vertical'
}

withDefaults(defineProps<Props>(), {
  orientation: 'horizontal'
})
</script>
