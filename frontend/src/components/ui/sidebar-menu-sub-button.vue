<script setup lang="ts">
import { cn } from '@/lib/utils'
import type { HTMLAttributes } from 'vue'

const props = withDefaults(defineProps<{
  asChild?: boolean
  isActive?: boolean
  class?: HTMLAttributes['class']
}>(), {
  asChild: false,
  isActive: false
})
</script>

<template>
  <component
    :is="asChild ? 'slot' : 'button'"
    :class="cn(
      'flex w-full items-center gap-3 overflow-hidden rounded-md px-3 py-2 text-left text-sm outline-none ring-sidebar-ring transition-[width,height,padding] hover:bg-sidebar-accent hover:text-sidebar-accent-foreground focus-visible:ring-2 active:bg-sidebar-accent active:text-sidebar-accent-foreground disabled:pointer-events-none disabled:opacity-50 group-has-[[data-sidebar=menu-action]]/menu-item:pr-8 aria-disabled:pointer-events-none aria-disabled:opacity-50 data-[active=true]:bg-sidebar-accent data-[active=true]:font-medium data-[active=true]:text-sidebar-accent-foreground data-[state=open]:hover:bg-sidebar-accent data-[state=open]:hover:text-sidebar-accent-foreground group-data-[collapsible=icon]:!size-8 group-data-[collapsible=icon]:!p-2 [&>svg]:size-4 [&>svg]:shrink-0',
      isActive && 'bg-sidebar-accent font-medium text-sidebar-accent-foreground',
      props.class
    )"
  >
    <slot />
  </component>
</template>
