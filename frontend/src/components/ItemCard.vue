<template>
  <article class="glass-card rounded-card card-pad hover:-translate-y-1 group glass-press">
    <!-- 左右分栏：左侧两组内容上下撑开，右侧三项等距 -->
    <div class="card-body">
      <div class="card-main">
        <!-- 组一：分类标识 + 名称（紧密成组） -->
        <div class="id-group">
          <div class="card-row-top">
            <span class="item-cat truncate">{{ item.category }}</span>
            <span class="card-emoji" aria-hidden="true">{{ item.emoji }}</span>
            <span v-if="isExpired" class="badge-expired ml-auto">已停用</span>
            <span v-else-if="item.expiry_date" class="badge-active ml-auto">使用中</span>
          </div>
          <h3 class="item-name" :title="item.name">{{ item.name }}</h3>
        </div>

        <!-- 组二：均摊成本 -->
        <div class="card-cost" :class="costTone">
          <p class="cost-hero-label">每次使用花费</p>
          <p class="cost-hero-value tnum">
            <span class="cost-hero-unit">¥</span>{{ costDisplay }}
          </p>
        </div>
      </div>

      <!-- 右栏：三项等距，左侧带贯通分割线 -->
      <dl class="card-side">
        <div class="meta-cell">
          <dt class="meta-label">买入价</dt>
          <dd class="meta-value tnum">{{ item.purchase_amount.toLocaleString() }}</dd>
        </div>
        <div class="meta-cell">
          <dt class="meta-label">已使用</dt>
          <!-- 加减按钮与数值同行，不额外占据纵向空间 -->
          <dd class="meta-value tnum usage-row">
            <button
              v-if="canStep"
              class="step-btn"
              :aria-label="`${item.name} 使用次数减一`"
              @click="$emit('record-usage', item.id, 'decrement')"
            >
              <Minus class="w-[11px] h-[11px]" />
            </button>
            <span>{{ totalUsage.toLocaleString() }}<span class="meta-unit">次</span></span>
            <button
              v-if="canStep"
              class="step-btn step-btn-add"
              :aria-label="`${item.name} 使用次数加一`"
              @click="$emit('record-usage', item.id, 'increment')"
            >
              <Plus class="w-[11px] h-[11px]" />
            </button>
          </dd>
        </div>
        <div class="meta-cell">
          <dt class="meta-label">购入于</dt>
          <dd class="meta-value tnum">{{ shortDate }}</dd>
        </div>
      </dl>
    </div>

    <!-- 操作区：悬浮于卡片顶部中央，绝对定位不参与布局计算 -->
    <div v-if="isAuthenticated" class="card-actions">
      <button
        class="act-btn"
        :aria-label="`编辑 ${item.name}`"
        @click="$emit('edit', item)"
      >
        <Edit2 class="w-3.5 h-3.5" />
      </button>
      <button
        class="act-btn act-btn-danger"
        :aria-label="`删除 ${item.name}`"
        @click="$emit('delete', item.id)"
      >
        <Trash2 class="w-3.5 h-3.5" />
      </button>
    </div>
  </article>
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

/* 仅手动计数的物品才显示加减按钮 */
const canStep = computed(() =>
  props.isAuthenticated && props.item.usage_frequency_type === 'manual'
)

const costPerUse = computed(() => {
  if (totalUsage.value === 0) return 0
  const actualCost = props.item.purchase_amount + (props.item.extra_cost || 0) - (props.item.disposal_price || 0)
  return actualCost / totalUsage.value
})

/* 成本档位 → 配色。借鉴地铁线路色：用颜色直接编码「这笔钱花得值不值」，
   让用户扫一眼卡片阵列就能分辨优劣，无需逐个读数。 */
const costTone = computed(() => {
  const cost = costPerUse.value
  if (cost < 10) return 'tone-good'
  if (cost < 50) return 'tone-fair'
  return 'tone-high'
})

/* 大数字优先保证可读：四位数以上省略小数，避免换行或缩字 */
const costDisplay = computed(() => {
  const cost = costPerUse.value
  if (cost >= 1000) return Math.round(cost).toLocaleString()
  return cost.toFixed(2)
})

/* 日期省略年份前两位，节省横向空间：2026-05-22 → 26.05.22 */
const shortDate = computed(() => {
  const parts = props.item.purchase_date?.split('-')
  if (!parts || parts.length < 3) return props.item.purchase_date
  return `${parts[0].slice(2)}.${parts[1]}.${parts[2]}`
})
</script>
