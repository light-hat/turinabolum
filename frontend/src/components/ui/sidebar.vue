<script setup lang="ts">
import type { HTMLAttributes } from "vue"
import { cn } from "@/lib/utils"
import { useSidebar } from "@/lib/sidebar-utils"

export interface SidebarProps {
  side?: "left" | "right"
  variant?: "sidebar" | "floating" | "inset"
  collapsible?: "offcanvas" | "icon" | "none"
  class?: HTMLAttributes["class"]
}

defineOptions({
  inheritAttrs: false,
})

const props = withDefaults(defineProps<SidebarProps>(), {
  side: "left",
  variant: "sidebar",
  collapsible: "offcanvas",
})

const { isMobile, state, openMobile, setOpenMobile } = useSidebar()
</script>

<template>
  <div
    v-if="collapsible === 'none'"
    data-slot="sidebar"
    :class="cn('bg-sidebar text-sidebar-foreground flex h-full w-80 flex-col', props.class)"
    v-bind="$attrs"
  >
    <slot />
  </div>

  <!-- Mobile sidebar -->
  <div
    v-else-if="isMobile"
    :class="cn('fixed inset-y-0 z-50 w-80 bg-sidebar text-sidebar-foreground', 
               side === 'left' ? 'left-0' : 'right-0',
               openMobile ? 'translate-x-0' : side === 'left' ? '-translate-x-full' : 'translate-x-full',
               'transition-transform duration-200 ease-in-out')"
    v-bind="$attrs"
  >
    <div class="flex h-full w-full flex-col">
      <slot />
    </div>
  </div>

  <!-- Desktop sidebar -->
  <div
    v-else
    class="group peer text-sidebar-foreground hidden md:block"
    data-slot="sidebar"
    :data-state="state"
    :data-collapsible="state === 'collapsed' ? collapsible : ''"
    :data-variant="variant"
    :data-side="side"
  >
    <!-- This is what handles the sidebar gap on desktop  -->
    <div
      :class="cn(
        'relative w-80 bg-transparent transition-[width] duration-200 ease-linear',
        'group-data-[collapsible=offcanvas]:w-0',
        'group-data-[side=right]:rotate-180',
        variant === 'floating' || variant === 'inset'
          ? 'group-data-[collapsible=icon]:w-16'
          : 'group-data-[collapsible=icon]:w-12',
      )"
    />
    <div
      :class="cn(
        'fixed inset-y-0 z-10 hidden h-svh w-80 transition-[left,right,width] duration-200 ease-linear md:flex',
        side === 'left'
          ? 'left-0 group-data-[collapsible=offcanvas]:-left-80'
          : 'right-0 group-data-[collapsible=offcanvas]:-right-80',
        // Adjust the padding for floating and inset variants.
        variant === 'floating' || variant === 'inset'
          ? 'p-2 group-data-[collapsible=icon]:w-16'
          : 'group-data-[collapsible=icon]:w-12 group-data-[side=left]:border-r group-data-[side=right]:border-l',
        props.class,
      )"
      v-bind="$attrs"
    >
      <div
        data-sidebar="sidebar"
        class="bg-sidebar group-data-[variant=floating]:border-sidebar-border flex h-full w-full flex-col group-data-[variant=floating]:rounded-lg group-data-[variant=floating]:border group-data-[variant=floating]:shadow-sm"
      >
        <slot />
      </div>
    </div>
  </div>
</template>