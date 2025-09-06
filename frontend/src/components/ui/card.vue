<template>
  <div :class="cnWithAttrs('rounded-lg border bg-card text-card-foreground shadow-sm', $attrs.class)" v-bind="$attrs">
    <slot />
  </div>
</template>

<script setup lang="ts">
import { cnWithAttrs } from "@/lib/utils"
</script>
