<template>
  <div class="h-full flex flex-col">
    <div class="flex items-center justify-between p-4 border-b">
      <div>
        <h1 class="text-2xl font-bold">Graph Analysis</h1>
        <p class="text-muted-foreground">Visualize relationships between incidents, cases, and evidence</p>
      </div>
      <div class="flex items-center gap-2">
        <Button @click="addRandomNode" variant="outline">
          <PlusIcon class="mr-2 h-4 w-4" />
          Add Node
        </Button>
        <Button @click="resetGraph" variant="outline">
          <RefreshCwIcon class="mr-2 h-4 w-4" />
          Reset
        </Button>
        <Button @click="fitView" variant="outline">
          <MaximizeIcon class="mr-2 h-4 w-4" />
          Fit View
        </Button>
      </div>
    </div>
    
    <div class="flex-1 relative">
      <VueFlow
        v-model="elements"
        :default-viewport="{ zoom: 1 }"
        :min-zoom="0.2"
        :max-zoom="4"
        :snap-to-grid="true"
        :snap-grid="[15, 15]"
        class="bg-background"
        @node-click="onNodeClick"
        @edge-click="onEdgeClick"
      >
        <Background :gap="20" :size="1" />
        <Controls />
        <MiniMap />
        
        <!-- Custom Node Types -->
        <template #node-incident="nodeProps">
          <div class="px-4 py-2 bg-red-100 border-2 border-red-300 rounded-lg shadow-sm">
            <div class="font-semibold text-red-800">{{ nodeProps.data.label }}</div>
            <div class="text-sm text-red-600">{{ nodeProps.data.type }}</div>
          </div>
        </template>
        
        <template #node-case="nodeProps">
          <div class="px-4 py-2 bg-blue-100 border-2 border-blue-300 rounded-lg shadow-sm">
            <div class="font-semibold text-blue-800">{{ nodeProps.data.label }}</div>
            <div class="text-sm text-blue-600">{{ nodeProps.data.type }}</div>
          </div>
        </template>
        
        <template #node-evidence="nodeProps">
          <div class="px-4 py-2 bg-green-100 border-2 border-green-300 rounded-lg shadow-sm">
            <div class="font-semibold text-green-800">{{ nodeProps.data.label }}</div>
            <div class="text-sm text-green-600">{{ nodeProps.data.type }}</div>
          </div>
        </template>
        
        <template #node-ioc="nodeProps">
          <div class="px-4 py-2 bg-yellow-100 border-2 border-yellow-300 rounded-lg shadow-sm">
            <div class="font-semibold text-yellow-800">{{ nodeProps.data.label }}</div>
            <div class="text-sm text-yellow-600">{{ nodeProps.data.type }}</div>
          </div>
        </template>
      </VueFlow>
    </div>
    
    <!-- Node Details Panel -->
    <div v-if="selectedNode" class="border-t p-4 bg-muted/50">
      <div class="flex items-center justify-between">
        <div>
          <h3 class="font-semibold">{{ selectedNode.data.label }}</h3>
          <p class="text-sm text-muted-foreground">{{ selectedNode.data.type }}</p>
        </div>
        <Button @click="selectedNode = null" variant="ghost" size="icon">
          <XIcon class="h-4 w-4" />
        </Button>
      </div>
      <div v-if="selectedNode.data.description" class="mt-2 text-sm">
        {{ selectedNode.data.description }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { VueFlow } from '@vue-flow/core'
import { Background } from '@vue-flow/background'
import { Controls } from '@vue-flow/controls'
import { MiniMap } from '@vue-flow/minimap'
import '@vue-flow/core/dist/style.css'
import '@vue-flow/core/dist/theme-default.css'
import Button from '@/components/ui/button.vue'
import { PlusIcon, RefreshCwIcon, MaximizeIcon, XIcon } from 'lucide-vue-next'

interface NodeData {
  label: string
  type: string
  description?: string
}

interface Node {
  id: string
  type: string
  position: { x: number; y: number }
  data: NodeData
}

interface Edge {
  id: string
  source: string
  target: string
  label?: string
  type?: string
}

type Element = Node | Edge

const elements = ref<Element[]>([])
const selectedNode = ref<Node | null>(null)

const nodeTypes = ['incident', 'case', 'evidence', 'ioc']
const nodeLabels = {
  incident: ['Malware Analysis', 'Network Intrusion', 'Data Breach', 'Phishing Attack'],
  case: ['Investigation Case #1', 'Forensic Analysis', 'Threat Hunting', 'Incident Response'],
  evidence: ['Memory Dump', 'Network Logs', 'File Artifact', 'Registry Key'],
  ioc: ['Suspicious IP', 'Malicious Domain', 'File Hash', 'Email Address']
}

const addRandomNode = () => {
  const type = nodeTypes[Math.floor(Math.random() * nodeTypes.length)]
  const labels = nodeLabels[type as keyof typeof nodeLabels]
  const label = labels[Math.floor(Math.random() * labels.length)]
  
  const newNode: Node = {
    id: `node-${Date.now()}`,
    type,
    position: {
      x: Math.random() * 800,
      y: Math.random() * 600
    },
    data: {
      label,
      type: type.toUpperCase(),
      description: `This is a ${type} node with additional information about the investigation.`
    }
  }
  
  elements.value.push(newNode)
  
  // Add random connections to existing nodes
  if (elements.value.length > 1) {
    const existingNodes = elements.value.filter(el => 'type' in el && el.type !== 'default')
    if (existingNodes.length > 0) {
      const randomTarget = existingNodes[Math.floor(Math.random() * existingNodes.length)]
      const newEdge: Edge = {
        id: `edge-${Date.now()}`,
        source: newNode.id,
        target: randomTarget.id,
        label: 'related to',
        type: 'default'
      }
      elements.value.push(newEdge)
    }
  }
}

const resetGraph = () => {
  elements.value = []
  selectedNode.value = null
}

const fitView = () => {
  // VueFlow will handle this automatically when elements change
  // This is a placeholder for custom fit view logic
}

const onNodeClick = (event: any) => {
  selectedNode.value = event.node
}

const onEdgeClick = (event: any) => {
  console.log('Edge clicked:', event.edge)
}

const initializeGraph = () => {
  // Add some initial nodes for demonstration
  const initialNodes: Node[] = [
    {
      id: 'incident-1',
      type: 'incident',
      position: { x: 100, y: 100 },
      data: {
        label: 'Malware Analysis',
        type: 'INCIDENT',
        description: 'Investigation of banking trojan detected in user workstation'
      }
    },
    {
      id: 'case-1',
      type: 'case',
      position: { x: 300, y: 100 },
      data: {
        label: 'Case #2024-001',
        type: 'CASE',
        description: 'Forensic analysis case for malware investigation'
      }
    },
    {
      id: 'evidence-1',
      type: 'evidence',
      position: { x: 200, y: 250 },
      data: {
        label: 'Memory Dump',
        type: 'EVIDENCE',
        description: 'Memory dump from infected workstation (8GB)'
      }
    },
    {
      id: 'ioc-1',
      type: 'ioc',
      position: { x: 400, y: 250 },
      data: {
        label: '192.168.1.100',
        type: 'IOC',
        description: 'Suspicious IP address involved in the attack'
      }
    }
  ]
  
  const initialEdges: Edge[] = [
    {
      id: 'edge-1',
      source: 'incident-1',
      target: 'case-1',
      label: 'investigated by',
      type: 'default'
    },
    {
      id: 'edge-2',
      source: 'case-1',
      target: 'evidence-1',
      label: 'contains',
      type: 'default'
    },
    {
      id: 'edge-3',
      source: 'evidence-1',
      target: 'ioc-1',
      label: 'reveals',
      type: 'default'
    }
  ]
  
  elements.value = [...initialNodes, ...initialEdges]
}

onMounted(() => {
  initializeGraph()
})
</script>
