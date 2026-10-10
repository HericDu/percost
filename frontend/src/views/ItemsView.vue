<template>
  <div class="min-h-screen flex flex-col">
    <!-- 主要内容 -->
    <main class="flex-1 px-4 sm:px-6 lg:px-10 xl:px-14 max-w-[1600px] mx-auto w-full">
      <!-- 顶部单行 Dock：左侧指标摘要 + 右侧搜索筛选 -->
      <div class="lg rounded-card px-4 py-[18px] sm:px-5 sm:py-[22px] mt-4 mb-[var(--gap-section)]">
        <!-- 始终左右分割，不换行：左侧指标 ~60%，右侧筛选 ~40% -->
        <div class="dock-row">
          <!-- 指标条：占据左侧主导空间，溢出时横向滚动 -->
          <div class="metric-rail flex items-center overflow-x-auto scrollbar-hide">
            <div
              v-for="(metric, i) in metrics"
              :key="metric.label"
              class="stat-cell shrink-0"
              :class="[metric.tone, { 'stat-divided': i > 0 }]"
            >
              <div class="stat-value tnum">
                <span v-if="metric.unit" class="stat-unit">{{ metric.unit }}</span>{{ metric.value
                }}<span v-if="metric.suffix" class="stat-suffix">{{ metric.suffix }}</span>
              </div>
              <div class="stat-label">{{ metric.label }}</div>
            </div>
          </div>

          <!-- 搜索与筛选：压缩到右侧，所有控件统一 36px 高、药丸圆角 -->
          <div class="dock-tools">
            <div class="relative flex-1 min-w-0 xl:flex-none xl:w-[150px]">
              <Search class="absolute left-3 top-1/2 -translate-y-1/2 w-[14px] h-[14px] text-ink-400 pointer-events-none" />
              <input
                v-model="searchQuery"
                type="search"
                placeholder="搜索"
                aria-label="搜索物品名称"
                class="ctl ctl-input w-full pl-8"
              />
            </div>
            <!-- 窄屏收为图标：select 透明覆盖在图标上，仍触发系统原生选择器，
                 功能不丢失，只是省掉当前值的文字展示 -->
            <div class="ctl-compact shrink-0">
              <Tag class="ctl-compact-icon" aria-hidden="true" />
              <select v-model="selectedCategory" aria-label="按分类筛选物品" class="ctl ctl-select">
                <option value="">所有分类</option>
                <option v-for="cat in categories" :key="cat" :value="cat">{{ cat }}</option>
              </select>
            </div>
            <!-- 排序项用自然语言描述结果，而非「字段 + 箭头」的抽象表达 -->
            <div class="ctl-compact shrink-0">
              <ArrowUpDown class="ctl-compact-icon" aria-hidden="true" />
              <select v-model="sortBy" aria-label="选择列表排序方式" class="ctl ctl-select">
                <option value="date_desc">最近买的在前</option>
                <option value="date_asc">最早买的在前</option>
                <option value="cost_asc">最划算的在前</option>
                <option value="cost_desc">最不划算的在前</option>
                <option value="price_asc">买得最便宜的在前</option>
                <option value="price_desc">买得最贵的在前</option>
                <option value="usage_asc">用得最少的在前</option>
                <option value="usage_desc">用得最多的在前</option>
              </select>
            </div>
            <button
              v-if="hasActiveFilters"
              @click="resetFilters"
              aria-label="清除搜索与筛选，恢复默认列表"
              title="清除筛选"
              class="ctl ctl-icon shrink-0"
            >
              <RotateCcw class="w-[14px] h-[14px]" />
            </button>
          </div>
        </div>
      </div>

      <!-- 加载骨架 -->
      <div
        v-if="loading"
        class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-[var(--gap-grid)]"
      >
        <div
          v-for="n in 8"
          :key="n"
          class="glass-card rounded-card p-5 h-[212px] animate-pulse"
          aria-hidden="true"
        >
          <div class="flex items-center gap-3 mb-5">
            <div class="w-9 h-9 rounded-pill bg-ink-200/50" />
            <div class="h-4 w-2/5 rounded-pill bg-ink-200/50" />
          </div>
          <div class="space-y-3">
            <div v-for="i in 5" :key="i" class="h-3 rounded-pill bg-ink-100/70" :style="{ width: `${90 - i * 9}%` }" />
          </div>
        </div>
      </div>

      <!-- 空状态 -->
      <div v-else-if="filteredItems.length === 0" class="lg rounded-card text-center px-6 py-16">
        <template v-if="items.length === 0">
          <div class="text-5xl mb-4">🧮</div>
          <h2 class="text-base font-semibold text-ink-800 mb-1.5">还没有记录任何物品</h2>
          <p class="text-[13px] text-ink-500 max-w-sm mx-auto leading-relaxed">
            记下买入价和使用频率，Percost 会算出每次使用的真实成本，
            帮你判断一件东西到底值不值。
          </p>
          <!-- 仅登录后可见：未登录时不暴露任何通往后台的入口 -->
          <button
            v-if="authStore.isAuthenticated"
            @click="handleAddClick"
            class="mt-6 px-6 py-2.5 rounded-pill text-sm font-semibold text-white btn-solid"
          >
            记录第一件物品
          </button>
        </template>
        <template v-else>
          <div class="text-5xl mb-4">🔍</div>
          <h2 class="text-base font-semibold text-ink-800 mb-1.5">没有匹配的物品</h2>
          <p class="text-[13px] text-ink-500">
            换个关键词，或
            <button @click="resetFilters" class="text-indigo-600 font-medium hover:underline underline-offset-2">
              清除筛选条件
            </button>
          </p>
        </template>
      </div>

      <!-- 物品网格 -->
      <template v-else>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-[var(--gap-grid)]">
          <ItemCard
            v-for="(item, i) in pagedItems"
            :key="item.id"
            :item="item"
            :is-authenticated="authStore.isAuthenticated"
            class="card-enter"
            :style="{ animationDelay: `${Math.min(i, 11) * 22}ms` }"
            @edit="editItem"
            @delete="askDelete"
            @record-usage="recordUsage"
          />
        </div>

        <!-- 分页：置于列表末尾的文档流中，随内容自然下落 -->
        <div class="flex justify-center mt-5">
          <PaginationBar
            :current="currentPage"
            :total-items="filteredItems.length"
            :effective-size="effectivePageSize"
            @update:current="goToPage"
          />
        </div>
      </template>
    </main>

    <!-- 右下角操作区：仅登录后出现。
         未登录时整块不渲染，页面上不存在任何指向后台的线索 -->
    <div
      v-if="authStore.isAuthenticated"
      class="fixed bottom-4 right-4 sm:bottom-6 sm:right-6 flex flex-col items-center gap-2.5 z-50"
    >
      <button @click="handleLogout" class="fab fab-ghost" aria-label="退出登录">
        <LogOut class="w-[18px] h-[18px]" />
      </button>

      <button @click="handleAddClick" class="fab fab-primary" aria-label="添加物品">
        <Plus class="w-6 h-6" />
      </button>
    </div>

    <!-- 退出确认弹窗 -->
    <div
      v-if="showLogoutConfirm"
      class="fixed inset-0 bg-ink-900/25 backdrop-blur-sm flex items-center justify-center z-[60] p-4"
      role="dialog"
      aria-modal="true"
      @click.self="showLogoutConfirm = false"
    >
      <div class="lg rounded-modal p-6 w-full max-w-[20rem] modal-in">
        <h3 class="text-base font-bold text-ink-900 mb-2 text-center">确认退出</h3>
        <p class="text-[13px] text-ink-500 mb-6 text-center leading-relaxed">
          当前登录 <span class="font-semibold text-ink-700">{{ authStore.user?.username }}</span>，退出后将无法编辑数据。
        </p>
        <div class="flex gap-2.5">
          <button
            @click="showLogoutConfirm = false"
            class="flex-1 py-2.5 rounded-pill glass-button text-sm font-medium text-ink-500"
          >
            取消
          </button>
          <button
            @click="confirmLogout"
            class="flex-1 py-2.5 rounded-pill text-sm font-semibold text-white btn-solid"
          >
            退出登录
          </button>
        </div>
      </div>
    </div>

    <!-- 删除确认弹窗 -->
    <div
      v-if="pendingDelete"
      class="fixed inset-0 bg-ink-900/25 backdrop-blur-sm flex items-center justify-center z-[60] p-4"
      role="dialog"
      aria-modal="true"
      @click.self="pendingDelete = null"
    >
      <div class="lg rounded-modal p-6 w-full max-w-[20rem] modal-in">
        <h3 class="text-base font-bold text-ink-900 mb-2 text-center">删除这件物品？</h3>
        <p class="text-[13px] text-ink-500 mb-6 text-center leading-relaxed">
          <span class="font-semibold text-ink-700">{{ pendingDelete.emoji }} {{ pendingDelete.name }}</span>
          的成本记录将被永久移除，无法恢复。
        </p>
        <div class="flex gap-2.5">
          <button
            @click="pendingDelete = null"
            class="flex-1 py-2.5 rounded-pill glass-button text-sm font-medium text-ink-500"
          >
            取消
          </button>
          <button
            @click="confirmDelete"
            class="flex-1 py-2.5 rounded-pill text-sm font-semibold text-white btn-danger"
          >
            删除
          </button>
        </div>
      </div>
    </div>

    <!-- 添加/编辑物品弹窗 -->
    <AddItemModal
      v-if="showAddModal"
      :item="editingItem"
      @close="closeModal"
      @save="saveItem"
    />

    <!-- 底部信息：三行居中，右侧留出 FAB 的空间 -->
    <footer class="text-center pl-4 pr-20 sm:px-4 pt-6 pb-6 flex-shrink-0 space-y-1.5">
      <p class="text-[11px] text-ink-400">&copy;2025 - 2027 By HericDu</p>
      <p class="text-[11px] text-ink-300">powered by codebuddy</p>
      <p class="text-[11px] text-ink-300">蜀ICP备2023020875号</p>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Plus, Search, RotateCcw, LogOut, Tag, ArrowUpDown } from 'lucide-vue-next'
import { useAuthStore } from '@/stores/auth'
import { itemsApi } from '@/api/items'
import type { Item } from '@/types'
import ItemCard from '@/components/ItemCard.vue'
import AddItemModal from '@/components/AddItemModal.vue'
import PaginationBar from '@/components/PaginationBar.vue'
import { useResponsivePageSize } from '@/composables/useResponsivePageSize'

const router = useRouter()
const authStore = useAuthStore()

const items = ref<Item[]>([])
const loading = ref(true)
const searchQuery = ref('')
const selectedCategory = ref('')
const sortBy = ref('date_desc')
const showAddModal = ref(false)
const editingItem = ref<Item | null>(null)
const showLogoutConfirm = ref(false)
const pendingDelete = ref<Item | null>(null)

const categories = [
  '电子产品', '家用电器', '生活用品', '服饰鞋包',
  '运动健康', '休闲娱乐', '学习办公', '软件服务', '其他'
]

function handleAddClick() {
  // 入口本身仅登录后渲染，此处再兜一层，避免未授权状态打开弹窗
  if (!authStore.isAuthenticated) return
  showAddModal.value = true
}

function getItemCostPerUse(item: Item): number {
  const purchaseDate = new Date(item.purchase_date)
  const now = new Date()
  let daysOwned = Math.max(0, Math.floor((now.getTime() - purchaseDate.getTime()) / (1000 * 60 * 60 * 24)))

  const type = item.usage_frequency_type
  const value = item.usage_frequency_value || 1

  let totalUsage = 0
  switch (type) {
    case 'daily':
      totalUsage = daysOwned * value
      break
    case 'weekly':
      totalUsage = Math.floor(daysOwned / 7) * value
      break
    case 'monthly':
      totalUsage = Math.floor(daysOwned / 30) * value
      break
    case 'yearly':
      totalUsage = Math.floor(daysOwned / 365) * value
      break
    case 'manual':
      totalUsage = item.manual_usage_count || 0
      break
    default:
      totalUsage = daysOwned
  }

  if (totalUsage === 0) return 0
  const actualCost = item.purchase_amount + (item.extra_cost || 0) - (item.disposal_price || 0)
  return actualCost / totalUsage
}

const filteredItems = computed(() => {
  let result = [...items.value]

  if (searchQuery.value) {
    result = result.filter(item =>
      item.name.toLowerCase().includes(searchQuery.value.toLowerCase())
    )
  }

  if (selectedCategory.value) {
    result = result.filter(item => item.category === selectedCategory.value)
  }

  if (sortBy.value) {
    result.sort((a, b) => {
      const direction = sortBy.value!.endsWith('_asc') ? 1 : -1
      const field = sortBy.value!.replace(/_(asc|desc)$/, '')
      let cmp = 0
      switch (field) {
        case 'cost':
          cmp = getItemCostPerUse(a) - getItemCostPerUse(b)
          break
        case 'price':
          cmp = a.purchase_amount - b.purchase_amount
          break
        case 'usage': {
          const ua = getItemCostPerUse(a)
          const ub = getItemCostPerUse(b)
          const ca = ua === 0 ? 0 : (a.purchase_amount + (a.extra_cost || 0) - (a.disposal_price || 0)) / ua
          const cb = ub === 0 ? 0 : (b.purchase_amount + (b.extra_cost || 0) - (b.disposal_price || 0)) / ub
          cmp = ca - cb
          break
        }
        case 'date':
          cmp = new Date(a.purchase_date).getTime() - new Date(b.purchase_date).getTime()
          break
      }
      return cmp * direction
    })
  }

  return result
})

/* ---------- 分页 ----------
   必须定义在 filteredItems 之后：下方 watch 的 getter 会在 setup 同步阶段
   立即求值一次以取得初始值，提前引用会命中 const 的暂时性死区。 */

// 每页数量完全跟随视窗，不提供手动选择
const { autoSize: effectivePageSize } = useResponsivePageSize()
const currentPage = ref(1)

const pagedItems = computed(() => {
  const start = (currentPage.value - 1) * effectivePageSize.value
  return filteredItems.value.slice(start, start + effectivePageSize.value)
})

function goToPage(page: number) {
  currentPage.value = page
  // 翻页后回到列表顶部，避免停留在上一页底部
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

// 筛选条件变化或页数缩减时，把越界的页码拉回有效范围
watch([() => filteredItems.value.length, effectivePageSize], ([total, size]) => {
  const maxPage = Math.max(1, Math.ceil(total / size))
  if (currentPage.value > maxPage) currentPage.value = maxPage
})

watch([searchQuery, selectedCategory, sortBy], () => {
  currentPage.value = 1
})

const stats = computed(() => {
  const total = items.value.length
  const totalAmount = items.value.reduce((sum, item) => sum + item.purchase_amount, 0)
  const avgCost = total > 0 ? totalAmount / total : 0
  const inUse = items.value.filter(item => {
    if (!item.expiry_date) return true
    const expiry = new Date(item.expiry_date)
    return expiry > new Date()
  }).length

  return { total, totalAmount, avgCost, inUse }
})

/* 指标拆成「单位 / 数值 / 后缀」三段，便于让数值独占最大字号，
   单位与后缀降级 —— 导向标识里数字永远是主体。 */
const metrics = computed(() => {
  const amount = stats.value.totalAmount
  const isWan = amount >= 10000
  return [
    { label: '记录物品', value: String(stats.value.total), suffix: '件', tone: 'metric-1' },
    {
      label: '累计花费',
      unit: '¥',
      value: isWan ? (amount / 10000).toFixed(1) : amount.toLocaleString(),
      suffix: isWan ? '万' : '',
      tone: 'metric-2',
    },
    { label: '件均价格', unit: '¥', value: Math.round(stats.value.avgCost).toLocaleString(), tone: 'metric-3' },
    { label: '仍在使用', value: String(stats.value.inUse), suffix: '件', tone: 'metric-4' },
  ]
})

const hasActiveFilters = computed(() =>
  Boolean(searchQuery.value || selectedCategory.value) || sortBy.value !== 'date_desc'
)

function formatAmount(amount: number) {
  if (amount >= 10000) {
    return `¥${(amount / 10000).toFixed(2)}万`
  }
  return `¥${amount.toLocaleString()}`
}

function resetFilters() {
  searchQuery.value = ''
  selectedCategory.value = ''
  sortBy.value = 'date_desc'
}

async function fetchItems() {
  try {
    const response = await itemsApi.getItems()
    items.value = response.items
  } catch (error) {
    console.error('Failed to fetch items:', error)
  } finally {
    loading.value = false
  }
}

function handleLogout() {
  showLogoutConfirm.value = true
}

async function confirmLogout() {
  showLogoutConfirm.value = false
  await authStore.logout()
  router.push('/')
}

function editItem(item: Item) {
  editingItem.value = item
  showAddModal.value = true
}

function askDelete(id: number) {
  pendingDelete.value = items.value.find(item => item.id === id) || null
}

async function confirmDelete() {
  const target = pendingDelete.value
  if (!target) return
  pendingDelete.value = null

  try {
    await itemsApi.deleteItem(target.id)
    items.value = items.value.filter(item => item.id !== target.id)
  } catch (error) {
    console.error('Failed to delete item:', error)
    alert('删除失败，请稍后重试')
  }
}

async function recordUsage(itemId: number, action: 'increment' | 'decrement') {
  try {
    const response = await itemsApi.recordUsage(itemId, action)
    const item = items.value.find(i => i.id === itemId)
    if (item) {
      item.manual_usage_count = response.manual_usage_count
    }
  } catch (error) {
    console.error('Failed to record usage:', error)
  }
}

function closeModal() {
  showAddModal.value = false
  editingItem.value = null
}

async function saveItem(data: any) {
  try {
    if (editingItem.value) {
      const response = await itemsApi.updateItem(editingItem.value.id, data)
      const index = items.value.findIndex(i => i.id === editingItem.value!.id)
      if (index !== -1) {
        items.value[index] = response.item
      }
    } else {
      const response = await itemsApi.createItem(data)
      items.value.unshift(response.item)
    }
    closeModal()
  } catch (error) {
    console.error('Failed to save item:', error)
    alert('保存失败')
  }
}

onMounted(() => {
  fetchItems()
})
</script>
