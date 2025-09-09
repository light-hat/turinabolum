<script setup lang="ts">
import { Search } from "lucide-vue-next"
import Label from "@/components/ui/label.vue"
import SidebarGroup from "@/components/ui/sidebar-group.vue"
import SidebarGroupContent from "@/components/ui/sidebar-group-content.vue"
import SidebarInput from "@/components/ui/sidebar-input.vue"
</script>

<template>
  <form>
    <SidebarGroup class="py-0">
      <SidebarGroupContent class="relative">
        <Label for="search" class="sr-only">
          Search
        </Label>
        <SidebarInput
          id="search"
          placeholder="Search incidents..."
          class="pl-9 w-full h-9 bg-background/50 border-border/50 focus:bg-background focus:border-border transition-all duration-200"
        />
        <Search class="pointer-events-none absolute left-3 top-1/2 size-4 -translate-y-1/2 select-none text-muted-foreground" />
      </SidebarGroupContent>
    </SidebarGroup>
  </form>
</template>
