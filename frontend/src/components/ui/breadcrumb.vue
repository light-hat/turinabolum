<template>
  <nav :class="cnWithAttrs('flex', $attrs.class)" v-bind="$attrs">
    <slot />
  </nav>
</template>

<script setup lang="ts">
import { cnWithAttrs } from "@/lib/utils"
</script>
