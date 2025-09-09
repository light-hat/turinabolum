<template>
  <a
    :class="cnWithAttrs('transition-colors hover:text-foreground', $attrs.class)"
    v-bind="$attrs"
  >
    <slot />
  </a>
</template>

<script setup lang="ts">
import { cnWithAttrs } from "@/lib/utils"
</script>
