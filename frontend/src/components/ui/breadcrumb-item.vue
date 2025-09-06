<template>
  <li :class="cnWithAttrs('inline-flex items-center gap-1.5', $attrs.class)" v-bind="$attrs">
    <slot />
  </li>
</template>

<script setup lang="ts">
import { cnWithAttrs } from "@/lib/utils"
</script>
