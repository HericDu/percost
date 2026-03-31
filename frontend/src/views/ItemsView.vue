<template>
  <div class="min-h-screen flex flex-col">
    <!-- 主要内容 -->
    <main class="flex-1 px-4 sm:px-8 lg:px-16 max-w-7xl mx-auto w-full pb-4">
      <!-- 统计卡片 -->
      <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 sm:gap-4 mb-5 pt-6">
        <div class="glass-card rounded-3xl p-4 sm:p-5 hover:-translate-y-0.5 transition-transform duration-300 flex flex-col justify-center">
          <div class="flex items-center gap-2.5 mb-2.5">
            <div class="w-10 h-10 rounded-2xl bg-indigo-100 flex items-center justify-center flex-shrink-0">
              <Package class="w-5 h-5 text-indigo-500" />
            </div>
            <span class="text-sm font-semibold text-gray-700">总物品数</span>
          </div>
          <div class="text-2xl sm:text-3xl font-bold text-gray-900 text-left">{{ stats.total }}</div>
        </div>
        <div class="glass-card rounded-3xl p-4 sm:p-5 hover:-translate-y-0.5 transition-transform duration-300 flex flex-col justify-center">
          <div class="flex items-center gap-2.5 mb-2.5">
            <div class="w-10 h-10 rounded-2xl bg-purple-100 flex items-center justify-center flex-shrink-0">
              <Wallet class="w-5 h-5 text-purple-500" />
            </div>
            <span class="text-sm font-semibold text-gray-700">总投资</span>
          </div>
          <div class="text-2xl sm:text-3xl font-bold text-gray-900 text-left">{{ formatAmount(stats.totalAmount) }}</div>
        </div>
        <div class="glass-card rounded-3xl p-4 sm:p-5 hover:-translate-y-0.5 transition-transform duration-300 flex flex-col justify-center">
          <div class="flex items-center gap-2.5 mb-2.5">
            <div class="w-10 h-10 rounded-2xl bg-blue-100 flex items-center justify-center flex-shrink-0">
              <Calculator class="w-5 h-5 text-blue-500" />
            </div>
            <span class="text-sm font-semibold text-gray-700">平均每次成本</span>
          </div>
          <div class="text-2xl sm:text-3xl font-bold text-gray-900 text-left">¥{{ stats.avgCost.toFixed(2) }}</div>
        </div>
        <div class="glass-card rounded-3xl p-4 sm:p-5 hover:-translate-y-0.5 transition-transform duration-300 flex flex-col justify-center">
          <div class="flex items-center gap-2.5 mb-2.5">
            <div class="w-10 h-10 rounded-2xl bg-emerald-100 flex items-center justify-center flex-shrink-0">
              <CheckCircle class="w-5 h-5 text-emerald-500" />
            </div>
            <span class="text-sm font-semibold text-gray-700">使用中</span>
          </div>
          <div class="text-2xl sm:text-3xl font-bold text-gray-900 text-left">{{ stats.inUse }}</div>
        </div>
      </div>

      <!-- 搜索、筛选、排序 -->
      <div class="glass-card rounded-3xl p-3 sm:p-4 mb-5">
        <div class="flex flex-wrap items-center gap-2 sm:gap-3">
          <div class="relative flex-1 min-w-[140px] sm:min-w-[180px]">
            <Search class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
            <input
              v-model="searchQuery"
              type="text"
              placeholder="搜索物品..."
              class="glass-input w-full pl-9 pr-4 py-2.5 rounded-2xl text-sm"
            />
          </div>
          <select
            v-model="selectedCategory"
            class="glass-input px-3 py-2.5 rounded-2xl text-sm min-w-[100px]"
          >
            <option value="">全部分类</option>
            <option v-for="cat in categories" :key="cat" :value="cat">{{ cat }}</option>
          </select>
          <select
            v-model="sortBy"
            class="glass-input px-3 py-2.5 rounded-2xl text-sm min-w-[100px]"
          >
            <option value="">默认排序</option>
            <option value="cost_asc">每次成本 低→高</option>
            <option value="cost_desc">每次成本 高→低</option>
            <option value="price_asc">购买价格 低→高</option>
            <option value="price_desc">购买价格 高→低</option>
            <option value="usage_asc">使用次数 低→高</option>
            <option value="usage_desc">使用次数 高→低</option>
            <option value="date_asc">购买日期 早→晚</option>
            <option value="date_desc">购买日期 晚→早</option>
          </select>
          <button
            @click="resetFilters"
            class="glass-button px-3 py-2.5 rounded-2xl text-sm text-gray-500 flex items-center gap-1.5"
          >
            <RotateCcw class="w-3.5 h-3.5" />
            <span>重置</span>
          </button>
        </div>
      </div>

      <!-- 物品网格 -->
      <div v-if="filteredItems.length === 0" class="text-center py-16">
        <div class="text-4xl mb-3">📦</div>
        <p class="text-gray-400 text-sm">暂无物品数据</p>
        <button
          @click="handleAddClick"
          class="mt-4 glass-button px-6 py-2.5 rounded-2xl text-sm font-medium text-indigo-600"
        >
          添加第一个物品
        </button>
      </div>

      <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        <ItemCard
          v-for="item in filteredItems"
          :key="item.id"
          :item="item"
          :is-authenticated="authStore.isAuthenticated"
          @edit="editItem"
          @delete="deleteItem"
          @record-usage="recordUsage"
        />
      </div>
    </main>

    <!-- 右下角操作区 -->
    <div class="fixed bottom-6 right-6 sm:bottom-8 sm:right-8 flex flex-col items-center gap-3 z-50">
      <!-- 已登录：退出按钮（与添加按钮同样式） -->
      <button
        v-if="authStore.isAuthenticated"
        @click="handleLogout"
        class="w-14 h-14 rounded-2xl bg-gradient-to-br from-rose-400 to-red-500 text-white shadow-lg shadow-rose-500/25 hover:shadow-xl hover:shadow-rose-500/30 transform hover:scale-105 active:scale-95 transition-all duration-200 flex items-center justify-center"
        title="退出登录"
      >
        <LogOut class="w-6 h-6" />
      </button>

      <!-- 添加按钮 -->
      <button
        @click="handleAddClick"
        class="w-14 h-14 rounded-2xl bg-gradient-to-br from-indigo-500 to-purple-600 text-white shadow-lg shadow-indigo-500/25 hover:shadow-xl hover:shadow-indigo-500/30 transform hover:scale-105 active:scale-95 transition-all duration-200 flex items-center justify-center"
      >
        <Plus class="w-6 h-6" />
      </button>
    </div>

    <!-- 退出确认弹窗 -->
    <div
      v-if="showLogoutConfirm"
      class="fixed inset-0 bg-black/30 backdrop-blur-sm flex items-center justify-center z-[60]"
      @click.self="showLogoutConfirm = false"
    >
      <div class="bg-white/90 backdrop-blur-2xl rounded-3xl p-6 w-80 shadow-xl border border-white/50">
        <h3 class="text-lg font-bold text-gray-900 mb-2 text-center">确认退出</h3>
        <p class="text-sm text-gray-500 mb-6 text-center">
          当前用户为 <span class="font-semibold text-gray-700">{{ authStore.user?.username }}</span>，确认退出登录吗？
        </p>
        <div class="flex gap-3">
          <button
            @click="showLogoutConfirm = false"
            class="flex-1 py-2.5 rounded-2xl glass-button text-sm font-medium text-gray-500 flex items-center justify-center"
          >
            取消
          </button>
          <button
            @click="confirmLogout"
            class="flex-1 py-2.5 rounded-2xl text-sm font-semibold text-white bg-gradient-to-r from-indigo-500 to-purple-600 shadow-lg shadow-indigo-500/20 hover:shadow-xl hover:shadow-indigo-500/30 active:scale-[0.98] transition-all duration-200 flex items-center justify-center"
          >
            确认退出
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

    <!-- 底部信息 -->
    <footer class="text-center py-8 px-4 space-y-1.5 flex-shrink-0">
      <p class="text-xs text-gray-400">&copy;2025 - 2027 By HericDu</p>
      <p class="text-xs text-gray-300">powered by codebuddy</p>
      <p class="text-xs text-gray-300">蜀ICP备2023020875号</p>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Plus, Package, Wallet, Calculator, CheckCircle, Search, RotateCcw, LogOut } from 'lucide-vue-next'
import { useAuthStore } from '@/stores/auth'
import { itemsApi } from '@/api/items'
import type { Item } from '@/types'
import ItemCard from '@/components/ItemCard.vue'
import AddItemModal from '@/components/AddItemModal.vue'

const router = useRouter()
const authStore = useAuthStore()

const items = ref<Item[]>([])
const loading = ref(true)
const searchQuery = ref('')
const selectedCategory = ref('')
const sortBy = ref('purchase_date_desc')
const showAddModal = ref(false)
const editingItem = ref<Item | null>(null)
const showLogoutConfirm = ref(false)

const categories = [
  '电子产品', '家用电器', '生活用品', '服饰鞋包',
  '运动健康', '休闲娱乐', '学习办公', '软件服务', '其他'
]

function handleAddClick() {
  if (!authStore.isAuthenticated) {
    router.push('/login')
    return
  }
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

function formatAmount(amount: number) {
  if (amount >= 10000) {
    return `¥${(amount / 10000).toFixed(2)}万`
  }
  return `¥${amount.toLocaleString()}`
}

function resetFilters() {
  searchQuery.value = ''
  selectedCategory.value = ''
  sortBy.value = 'purchase_date_desc'
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

async function deleteItem(id: number) {
  if (!confirm('确定要删除这件物品吗？')) return

  try {
    await itemsApi.deleteItem(id)
    items.value = items.value.filter(item => item.id !== id)
  } catch (error) {
    console.error('Failed to delete item:', error)
    alert('删除失败')
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
