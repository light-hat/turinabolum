<template>
  <Sidebar v-bind="props" class="border-r border-sidebar-border bg-white/80 dark:bg-slate-800/80 backdrop-blur-sm">
    <SidebarHeader class="p-4 border-b border-sidebar-border">
      <SidebarMenu>
        <SidebarMenuItem>
          <SidebarMenuButton size="lg" as-child class="h-12 px-3">
            <a href="#" class="flex items-center gap-3">
              <div class="flex aspect-square size-10 items-center justify-center rounded-xl bg-sidebar-primary text-sidebar-primary-foreground shadow-sm">
                <GalleryVerticalEnd class="size-5" />
              </div>
              <div class="flex flex-col gap-0.5 leading-none min-w-0">
                <span class="font-bold text-base">Turinabolum</span>
                <span class="text-xs text-muted-foreground font-medium">v1.0.0</span>
              </div>
            </a>
          </SidebarMenuButton>
        </SidebarMenuItem>
      </SidebarMenu>
      <div class="mt-4">
        <SearchForm />
      </div>
    </SidebarHeader>
    <SidebarContent class="p-2">
      <SidebarGroup>
        <SidebarGroupLabel class="px-3 py-2 text-xs font-semibold text-muted-foreground">Platform</SidebarGroupLabel>
        <SidebarMenu class="space-y-1">
          <Collapsible
            v-for="(item, index) in data.navMain"
            :key="item.title"
            :default-open="index === 0"
            class="group/collapsible"
          >
            <SidebarMenuItem>
              <CollapsibleTrigger as-child v-if="item.items.length">
                <SidebarMenuButton class="h-10 px-3 font-medium text-sm hover:bg-sidebar-accent/50 transition-colors font-serif">
                  {{ item.title }}
                </SidebarMenuButton>
              </CollapsibleTrigger>
              <SidebarMenuButton v-else as-child class="h-10 px-3 font-medium text-sm hover:bg-sidebar-accent/50 transition-colors font-serif">
                <router-link :to="item.url" class="block w-full">{{ item.title }}</router-link>
              </SidebarMenuButton>
              <CollapsibleContent v-if="item.items.length" class="overflow-hidden transition-all duration-200">
                <SidebarMenuSub class="mt-1 space-y-1">
                  <SidebarMenuSubItem v-for="childItem in item.items" :key="childItem.title">
                    <SidebarMenuSubButton
                      as-child
                      :is-active="childItem.isActive || false"
                      class="h-9 px-3 text-sm hover:bg-sidebar-accent/50 transition-colors font-serif"
                    >
                      <router-link :to="childItem.url" class="block w-full">{{ childItem.title }}</router-link>
                    </SidebarMenuSubButton>
                  </SidebarMenuSubItem>
                </SidebarMenuSub>
              </CollapsibleContent>
            </SidebarMenuItem>
          </Collapsible>
        </SidebarMenu>
      </SidebarGroup>
    </SidebarContent>
    <SidebarRail />
  </Sidebar>
</template>

<script setup lang="ts">
import { GalleryVerticalEnd } from "lucide-vue-next"
import SearchForm from "@/components/layout/SearchForm.vue"
import Collapsible from "@/components/ui/collapsible.vue"
import CollapsibleContent from "@/components/ui/collapsible-content.vue"
import CollapsibleTrigger from "@/components/ui/collapsible-trigger.vue"
import Sidebar from "@/components/ui/sidebar.vue"
import SidebarContent from "@/components/ui/sidebar-content.vue"
import SidebarGroup from "@/components/ui/sidebar-group.vue"
import SidebarGroupLabel from "@/components/ui/sidebar-group-label.vue"
import SidebarHeader from "@/components/ui/sidebar-header.vue"
import SidebarMenu from "@/components/ui/sidebar-menu.vue"
import SidebarMenuButton from "@/components/ui/sidebar-menu-button.vue"
import SidebarMenuItem from "@/components/ui/sidebar-menu-item.vue"
import SidebarMenuSub from "@/components/ui/sidebar-menu-sub.vue"
import SidebarMenuSubButton from "@/components/ui/sidebar-menu-sub-button.vue"
import SidebarMenuSubItem from "@/components/ui/sidebar-menu-sub-item.vue"
import SidebarRail from "@/components/ui/sidebar-rail.vue"

interface SidebarProps {
  collapsible?: 'offcanvas' | 'icon' | 'none'
  class?: string
}

const props = withDefaults(defineProps<SidebarProps>(), {
  collapsible: "icon",
})

// Navigation data for Turinabolum
const data = {
  navMain: [
    {
      title: "Dashboard",
      url: "/dashboard",
      items: [],
    },
    {
      title: "Incidents",
      url: "/incidents",
      items: [
        {
          title: "All Incidents",
          url: "/incidents",
          isActive: false,
        },
        {
          title: "New Incident",
          url: "/incidents/new",
          isActive: false,
        },
      ],
    },
    {
      title: "Dumps",
      url: "/dumps",
      items: [],
    },
    {
      title: "Graph",
      url: "/graph",
      items: [],
    },
  ],
  projects: [],
}
</script>
