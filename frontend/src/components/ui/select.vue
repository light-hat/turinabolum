<template>
  <div class="relative">
    <select
      :class="cnWithAttrs('flex h-10 w-full items-center justify-between rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50', $attrs.class)"
      :value="modelValue"
      @change="$emit('update:modelValue', ($event.target as HTMLSelectElement).value)"
      v-bind="$attrs"
    >
      <slot />
    </select>
  </div>
</template>

<script setup lang="ts">
import { cnWithAttrs } from "@/lib/utils"

defineOptions({
  inheritAttrs: false
})

defineProps<{
  modelValue?: string
}>()

defineEmits<{
  'update:modelValue': [value: string]
}>()
</script>
