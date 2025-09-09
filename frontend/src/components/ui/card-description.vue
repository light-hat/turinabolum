<template>
  <p :class="cnWithAttrs('text-sm text-muted-foreground', $attrs.class)" v-bind="$attrs">
    <slot />
  </p>
</template>

<script setup lang="ts">
import { cnWithAttrs } from "@/lib/utils"
</script>
