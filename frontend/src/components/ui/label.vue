<template>
  <label
    :class="cnWithAttrs('text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70', $attrs.class)"
    v-bind="$attrs"
  >
    <slot />
  </label>
</template>

<script setup lang="ts">
import { cnWithAttrs } from "@/lib/utils"
</script>
