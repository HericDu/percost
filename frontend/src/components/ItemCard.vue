<template>
  <div class="glass-card rounded-3xl p-5 hover:-translate-y-1 hover:shadow-xl transition-all duration-300 ease-out group glass-press">
    <div class="flex items-center justify-between mb-3 min-h-[44px]">
      <div class="flex items-center gap-3 min-w-0">
        <span class="text-3xl leading-none flex-shrink-0">{{ item.emoji }}</span>
        <h3 class="font-extrabold text-gray-900 text-lg leading-tight truncate">{{ item.name }}</h3>
      </div>
      <div class="flex items-center gap-1.5 flex-shrink-0 ml-2">
        <div class="flex gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
          <button
            v-if="isAuthenticated"
            @click="$emit('edit', item)"
            class="glass-button p-1.5 rounded-xl flex items-center justify-center"
          >
            <Edit2 class="w-3.5 h-3.5 text-gray-400" />
          </button>
          <button
            v-if="isAuthenticated"
            @click="$emit('delete', item.id)"
            class="glass-button p-1.5 rounded-xl flex items-center justify-center"
          >
            <Trash2 class="w-3.5 h-3.5 text-red-400" />
          </button>
        </div>
      </div>
    </div>

    <div class="space-y-2.5 text-[13px]">
      <div class="flex justify-between items-center">
        <span class="text-gray-400">分类</span>
        <span class="text-gray-500 text-right">{{ item.category }}</span>
      </div>
      <div class="flex justify-between items-center">
        <span class="text-gray-400">购买金额</span>
        <span class="font-semibold text-gray-800 text-right">¥{{ item.purchase_amount.toLocaleString() }}</span>
      </div>
      <div class="flex justify-between items-center">
        <span class="text-gray-400">购买日期</span>
        <span class="text-gray-500 text-right">{{ item.purchase_date }}</span>
      </div>
      <div class="flex justify-between items-center">
        <span class="text-gray-400">每次成本</span>
        <div class="flex items-center gap-2">
          <span
            v-if="isExpired"
            class="badge-expired inline-block whitespace-nowrap"
          >已到期</span>
          <span
            v-else-if="item.expiry_date"
            class="badge-active inline-block whitespace-nowrap"
          >使用中</span>
          <span
            class="px-2.5 py-0.5 rounded-full text-xs font-semibold"
            :class="costClass"
          >
            ¥{{ costPerUse.toFixed(2) }}
          </span>
        </div>
      </div>
      <div class="flex justify-between items-center">
        <span class="text-gray-400">使用次数</span>
        <div class="flex items-center gap-1.5">
          <span class="text-gray-800 font-semibold">{{ totalUsage }}</span>
          <div v-if="isAuthenticated && item.usage_frequency_type === 'manual'" class="flex gap-0.5">
            <button
              @click="$emit('record-usage', item.id, 'decrement')"
              class="glass-button p-1 rounded-xl flex items-center justify-center"
            >
              <Minus class="w-3 h-3 text-red-400" />
            </button>
            <button
              @click="$emit('record-usage', item.id, 'increment')"
              class="glass-button p-1 rounded-xl flex items-center justify-center"
            >
              <Plus class="w-3 h-3 text-emerald-500" />
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { Edit2, Trash2, Plus, Minus } from 'lucide-vue-next'
import type { Item } from '@/types'

interface Props {
  item: Item
  isAuthenticated: boolean
}

const props = defineProps<Props>()

defineEmits<{
  edit: [item: Item]
  delete: [id: number]
  'record-usage': [id: number, action: 'increment' | 'decrement']
}>()

const isExpired = computed(() => {
  if (!props.item.expiry_date) return false
  return new Date(props.item.expiry_date) <= new Date()
})

const daysOwned = computed(() => {
  const purchaseDate = new Date(props.item.purchase_date)
  const referenceDate = isExpired.value && props.item.expiry_date
    ? new Date(props.item.expiry_date)
    : new Date()
  const diff = Math.floor((referenceDate.getTime() - purchaseDate.getTime()) / (1000 * 60 * 60 * 24))
  return Math.max(0, diff)
})

const totalUsage = computed(() => {
  const type = props.item.usage_frequency_type
  const value = props.item.usage_frequency_value || 1

  switch (type) {
    case 'daily':
      return daysOwned.value * value
    case 'weekly':
      return Math.floor(daysOwned.value / 7) * value
    case 'monthly':
      return Math.floor(daysOwned.value / 30) * value
    case 'yearly':
      return Math.floor(daysOwned.value / 365) * value
    case 'manual':
      return props.item.manual_usage_count || 0
    default:
      return daysOwned.value
  }
})

const costPerUse = computed(() => {
  if (totalUsage.value === 0) return 0
  const actualCost = props.item.purchase_amount + (props.item.extra_cost || 0) - (props.item.disposal_price || 0)
  return actualCost / totalUsage.value
})

const costClass = computed(() => {
  const cost = costPerUse.value
  if (cost < 10) return 'bg-emerald-100 text-emerald-600'
  if (cost < 50) return 'bg-amber-100 text-amber-600'
  return 'bg-red-100 text-red-600'
})
</script>
