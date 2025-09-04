<template>
  <div
    data-slot="sidebar-rail"
    :class="cn('absolute inset-y-0 z-20 hidden w-2 -translate-x-full transition-transform duration-200 ease-linear group-data-[side=left]:-left-2 group-data-[side=right]:left-full group-data-[collapsible=offcanvas]:translate-x-0 group-data-[collapsible=icon]:translate-x-0', props.class)"
    v-bind="$attrs"
  >
    <button
      class="absolute inset-y-0 z-10 w-full focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sidebar-ring focus-visible:ring-offset-2 focus-visible:ring-offset-sidebar"
      @click="toggleSidebar"
    >
      <span class="sr-only">Toggle Sidebar</span>
    </button>
  </div>
</template>

<script setup lang="ts">
import type { HTMLAttributes } from "vue"
import { cn } from "@/lib/utils"
import { useSidebar } from "@/lib/sidebar-utils"

const props = defineProps<{
  class?: HTMLAttributes["class"]
}>()

const { toggleSidebar } = useSidebar()
</script>
