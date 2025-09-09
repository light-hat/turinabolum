<template>
  <textarea
    :class="cnWithAttrs('flex min-h-[80px] w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50', $attrs.class)"
    :value="modelValue"
    @input="$emit('update:modelValue', ($event.target as HTMLTextAreaElement).value)"
    v-bind="$attrs"
  />
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
