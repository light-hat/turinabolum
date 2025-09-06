<template>
  <ol :class="cnWithAttrs('flex flex-wrap items-center gap-1.5 break-words text-sm text-muted-foreground sm:gap-2.5', $attrs.class)" v-bind="$attrs">
    <slot />
  </ol>
</template>

<script setup lang="ts">
import { cnWithAttrs } from "@/lib/utils"
</script>
