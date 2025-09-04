<template>
  <div :class="cnWithAttrs('p-6 pt-0', $attrs.class)" v-bind="$attrs">
    <slot />
  </div>
</template>

<script setup lang="ts">
import { cnWithAttrs } from "@/lib/utils"
</script>
