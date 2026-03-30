<template>
  <div class="fixed inset-0 z-50 flex items-end sm:items-center justify-center bg-black/30 backdrop-blur-sm">
    <div class="bg-white/90 backdrop-blur-2xl rounded-t-[2rem] sm:rounded-[2rem] w-full sm:max-w-2xl max-h-[92vh] sm:max-h-[90vh] overflow-hidden border border-white/50 shadow-2xl">
      <div class="p-5 sm:p-6 overflow-y-auto max-h-[92vh] sm:max-h-[90vh]">
        <!-- 标题栏 -->
        <div class="flex items-center justify-between mb-5">
          <h2 class="text-lg font-bold text-gray-900">
            {{ item ? '编辑物品' : '添加物品' }}
          </h2>
          <button @click="$emit('close')" class="glass-button p-2 rounded-2xl flex items-center justify-center">
            <X class="w-5 h-5 text-gray-500" />
          </button>
        </div>

        <form @submit.prevent="handleSubmit" class="space-y-4">
          <!-- 图标选择器 -->
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">
              图标 *
            </label>
            <div class="flex items-center gap-3 mb-2">
              <div class="w-12 h-12 rounded-2xl glass-card flex items-center justify-center text-2xl cursor-pointer" @click="showEmojiPicker = !showEmojiPicker">
                {{ form.emoji || '📦' }}
              </div>
              <span class="text-xs text-gray-400">点击选择图标</span>
            </div>
            <div v-if="showEmojiPicker" class="bg-white/80 backdrop-blur-xl rounded-3xl p-3 border border-white/40 shadow-lg">
              <!-- 分类标签 -->
              <div class="flex gap-1.5 mb-3 overflow-x-auto pb-1 -mx-1 px-1 scrollbar-hide">
                <button
                  v-for="cat in emojiCategories"
                  :key="cat.name"
                  type="button"
                  @click="activeCategory = cat.name"
                  class="px-3 py-1.5 rounded-full text-xs whitespace-nowrap font-medium transition-all duration-200"
                  :class="activeCategory === cat.name
                    ? 'bg-indigo-500 text-white shadow-sm'
                    : 'bg-gray-100 text-gray-500 hover:bg-gray-200'"
                >
                  {{ cat.name }}
                </button>
              </div>
              <!-- Emoji 网格 -->
              <div class="grid grid-cols-4 sm:grid-cols-6 gap-2 max-h-52 overflow-y-auto pr-1">
                <button
                  v-for="item in currentEmojis"
                  :key="item.icon"
                  type="button"
                  @click="selectEmoji(item.icon)"
                  class="flex flex-col items-center justify-center gap-1 py-2 rounded-2xl hover:bg-indigo-50 transition-colors glass-press"
                  :class="form.emoji === item.icon ? 'bg-indigo-100 ring-2 ring-indigo-400/40' : ''"
                >
                  <span class="text-2xl leading-none">{{ item.icon }}</span>
                  <span class="text-[10px] text-gray-400 leading-tight truncate w-full text-center">{{ item.label }}</span>
                </button>
              </div>
            </div>
          </div>

          <!-- 物品名称 -->
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">
              物品名称 *
            </label>
            <input
              v-model="form.name"
              type="text"
              required
              maxlength="200"
              class="glass-input w-full px-4 py-2.5 rounded-2xl text-sm"
              placeholder="MacBook Pro"
            />
          </div>

          <!-- 分类 -->
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">
              分类 *
            </label>
            <select
              v-model="form.category"
              required
              class="glass-input w-full px-4 py-2.5 rounded-2xl text-sm"
            >
              <option value="">请选择分类</option>
              <option v-for="cat in categories" :key="cat" :value="cat">{{ cat }}</option>
            </select>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <!-- 购买金额 -->
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">
                购买金额 (元) *
              </label>
              <input
                type="number"
                required
                min="0"
                class="glass-input w-full px-4 py-2.5 rounded-2xl text-sm"
                :class="{ 'amount-placeholder': !isPurchaseFocused && form.purchase_amount === 0 }"
                :value="form.purchase_amount === 0 && !isPurchaseFocused ? '' : form.purchase_amount"
                @focus="onAmountFocus('purchase')"
                @blur="onAmountBlur('purchase')"
                @input="form.purchase_amount = Number(($event.target as HTMLInputElement).value) || 0"
                placeholder="0"
              />
            </div>

            <!-- 购买日期 -->
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">
                购买日期 *
              </label>
              <input
                v-model="form.purchase_date"
                type="date"
                required
                class="glass-input w-full px-4 py-2.5 rounded-2xl text-sm"
              />
            </div>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <!-- 额外成本 -->
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">
                额外成本 (元)
              </label>
              <input
                type="number"
                min="0"
                class="glass-input w-full px-4 py-2.5 rounded-2xl text-sm"
                :class="{ 'amount-placeholder': !isExtraFocused && form.extra_cost === 0 }"
                :value="form.extra_cost === 0 && !isExtraFocused ? '' : form.extra_cost"
                @focus="onAmountFocus('extra')"
                @blur="onAmountBlur('extra')"
                @input="form.extra_cost = Number(($event.target as HTMLInputElement).value) || 0"
                placeholder="0"
              />
            </div>

            <!-- 处置价格 -->
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">
                处置价格 (元)
              </label>
              <input
                type="number"
                min="0"
                class="glass-input w-full px-4 py-2.5 rounded-2xl text-sm"
                :class="{ 'amount-placeholder': !isDisposalFocused && form.disposal_price === 0 }"
                :value="form.disposal_price === 0 && !isDisposalFocused ? '' : form.disposal_price"
                @focus="onAmountFocus('disposal')"
                @blur="onAmountBlur('disposal')"
                @input="form.disposal_price = Number(($event.target as HTMLInputElement).value) || 0"
                placeholder="0"
              />
            </div>
          </div>

          <!-- 使用频率 -->
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">
              使用频率
            </label>
            <div class="grid grid-cols-2 gap-3">
              <select
                v-model="form.usage_frequency_type"
                class="glass-input px-4 py-2.5 rounded-2xl text-sm"
              >
                <option value="daily">每天</option>
                <option value="weekly">每周</option>
                <option value="monthly">每月</option>
                <option value="yearly">每年</option>
                <option value="manual">手动录入</option>
              </select>
              <input
                v-model.number="form.usage_frequency_value"
                type="number"
                min="1"
                class="glass-input px-4 py-2.5 rounded-2xl text-sm"
                placeholder="次数"
              />
            </div>
          </div>

          <!-- 使用截止日期 -->
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">
              使用截止日期
              <span class="text-xs text-gray-400 font-normal ml-1">不填则视为使用中</span>
            </label>
            <input
              v-model="form.expiry_date"
              type="date"
              class="glass-input w-full px-4 py-2.5 rounded-2xl text-sm"
            />
          </div>

          <!-- 备注 -->
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">
              备注
            </label>
            <textarea
              v-model="form.remark"
              rows="3"
              class="glass-input w-full px-4 py-2.5 rounded-2xl text-sm resize-none"
              placeholder="其他备注信息"
            />
          </div>

          <!-- 按钮 -->
          <div class="flex gap-3 pt-2">
            <button
              type="button"
              @click="$emit('close')"
              class="flex-1 py-3 rounded-2xl glass-button text-sm font-medium text-gray-500 flex items-center justify-center"
            >
              取消
            </button>
            <button
              type="submit"
              class="flex-1 py-3 rounded-2xl bg-gradient-to-r from-indigo-500 to-purple-600 text-white text-sm font-semibold shadow-lg shadow-indigo-500/20 hover:shadow-xl hover:shadow-indigo-500/30 active:scale-[0.98] transition-all duration-200 flex items-center justify-center"
            >
              {{ item ? '更新' : '保存' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- 验证错误弹窗 -->
    <div
      v-if="validationError"
      class="fixed inset-0 bg-black/30 backdrop-blur-sm flex items-center justify-center z-[60]"
      @click.self="validationError = ''"
    >
      <div class="bg-white/90 backdrop-blur-2xl rounded-3xl p-6 w-80 shadow-xl border border-white/50">
        <h3 class="text-lg font-bold text-gray-900 mb-2 text-center">提示</h3>
        <p class="text-sm text-gray-500 mb-6 text-center">{{ validationError }}</p>
        <div class="flex gap-3">
          <button
            @click="validationError = ''"
            class="flex-1 py-2.5 rounded-2xl text-sm font-semibold text-white bg-gradient-to-r from-indigo-500 to-purple-600 shadow-lg shadow-indigo-500/20 hover:shadow-xl hover:shadow-indigo-500/30 active:scale-[0.98] transition-all duration-200 flex items-center justify-center"
          >
            我知道了
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, computed, onMounted } from 'vue'
import { X } from 'lucide-vue-next'
import type { Item } from '@/types'
import { emojiCategories } from '@/data/emojiCategories'

interface Props {
  item?: Item | null
}

const props = defineProps<Props>()

const emit = defineEmits<{
  close: []
  save: [data: any]
}>()

const categories = [
  '电子产品', '家用电器', '生活用品', '服饰鞋包',
  '运动健康', '休闲娱乐', '学习办公', '软件服务', '其他'
]

const showEmojiPicker = ref(false)
const activeCategory = ref('电子产品')
const validationError = ref('')

const currentEmojis = computed(() => {
  const cat = emojiCategories.find(c => c.name === activeCategory.value)
  return cat ? cat.emojis : emojiCategories[0].emojis
})

const form = reactive({
  emoji: '',
  name: '',
  category: '',
  purchase_amount: 0,
  purchase_date: new Date().toISOString().split('T')[0],
  extra_cost: 0,
  disposal_price: 0,
  remark: '',
  usage_frequency_type: 'daily',
  usage_frequency_value: 1,
  expiry_date: '' as string
})

const isPurchaseFocused = ref(false)
const isExtraFocused = ref(false)
const isDisposalFocused = ref(false)

function onAmountFocus(field: string) {
  if (field === 'purchase') isPurchaseFocused.value = true
  if (field === 'extra') isExtraFocused.value = true
  if (field === 'disposal') isDisposalFocused.value = true
}

function onAmountBlur(field: string) {
  if (field === 'purchase') isPurchaseFocused.value = false
  if (field === 'extra') isExtraFocused.value = false
  if (field === 'disposal') isDisposalFocused.value = false
}

function selectEmoji(emoji: string) {
  form.emoji = emoji
  showEmojiPicker.value = false
}

onMounted(() => {
  if (props.item) {
    Object.assign(form, {
      emoji: props.item.emoji,
      name: props.item.name,
      category: props.item.category,
      purchase_amount: props.item.purchase_amount,
      purchase_date: props.item.purchase_date,
      extra_cost: props.item.extra_cost || 0,
      disposal_price: props.item.disposal_price || 0,
      remark: props.item.remark || '',
      usage_frequency_type: props.item.usage_frequency_type || 'daily',
      usage_frequency_value: props.item.usage_frequency_value || 1,
      expiry_date: props.item.expiry_date || ''
    })
  }
})

function handleSubmit() {
  const errors: string[] = []
  if (!form.emoji) errors.push('图标')
  if (!form.name) errors.push('物品名称')
  if (!form.category) errors.push('分类')
  if (!form.purchase_amount) errors.push('购买金额')
  if (!form.purchase_date) errors.push('购买日期')

  if (errors.length > 0) {
    validationError.value = errors.join('、') + '未填写'
    return
  }

  const data = {
    emoji: form.emoji,
    name: form.name,
    category: form.category,
    purchase_amount: Math.floor(form.purchase_amount),
    purchase_date: form.purchase_date,
    extra_cost: Math.floor(form.extra_cost || 0),
    disposal_price: Math.floor(form.disposal_price || 0),
    remark: form.remark,
    usage_frequency_type: form.usage_frequency_type,
    usage_frequency_value: form.usage_frequency_value,
    expiry_date: form.expiry_date || null
  }

  emit('save', data)
}
</script>
