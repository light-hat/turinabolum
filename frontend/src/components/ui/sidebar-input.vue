<template>
  <input
    :class="cnWithAttrs('h-8 w-full bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50', $attrs.class)"
    v-bind="$attrs"
  />
</template>

<script setup lang="ts">
import { cnWithAttrs } from "@/lib/utils"

defineOptions({
  inheritAttrs: false
})
</script>
