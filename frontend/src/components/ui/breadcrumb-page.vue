<template>
  <span :class="cnWithAttrs('font-normal text-foreground', $attrs.class)" v-bind="$attrs">
    <slot />
  </span>
</template>

<script setup lang="ts">
import { cnWithAttrs } from "@/lib/utils"
</script>
