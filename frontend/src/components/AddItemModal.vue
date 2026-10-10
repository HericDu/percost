<template>
  <div
    class="fixed inset-0 z-50 flex items-end sm:items-center justify-center bg-ink-900/25 backdrop-blur-sm sm:p-4"
    role="dialog"
    aria-modal="true"
  >
    <div class="lg rounded-t-modal sm:rounded-modal w-full sm:max-w-2xl max-h-[92vh] sm:max-h-[88vh] overflow-hidden modal-in">
      <div class="p-5 sm:p-6 overflow-y-auto max-h-[92vh] sm:max-h-[88vh]">
        <!-- 标题栏 -->
        <div class="flex items-center justify-between mb-5">
          <h2 class="text-[17px] font-bold text-ink-900 tracking-tight">
            {{ item ? '编辑物品' : '添加物品' }}
          </h2>
          <button
            @click="$emit('close')"
            aria-label="关闭"
            class="glass-button w-8 h-8 rounded-pill flex items-center justify-center shrink-0"
          >
            <X class="w-4 h-4 text-ink-500" />
          </button>
        </div>

        <form @submit.prevent="handleSubmit" class="space-y-4">
          <!-- 图标选择器 -->
          <div>
            <label class="field-label">
              图标 *
            </label>
            <div class="flex items-center gap-3 mb-2.5">
              <button
                type="button"
                class="w-11 h-11 rounded-ctl glass-button flex items-center justify-center text-[22px] shrink-0"
                :aria-expanded="showEmojiPicker"
                @click="showEmojiPicker = !showEmojiPicker"
              >
                {{ form.emoji || '📦' }}
              </button>
              <span class="text-[12px] text-ink-400">点击选择图标</span>
            </div>
            <div v-if="showEmojiPicker" class="emoji-panel rounded-card p-3">
              <!-- 分类标签 -->
              <div class="flex gap-1.5 mb-3 overflow-x-auto pb-1 -mx-1 px-1 scrollbar-hide">
                <button
                  v-for="cat in emojiCategories"
                  :key="cat.name"
                  type="button"
                  @click="activeCategory = cat.name"
                  class="chip"
                  :class="activeCategory === cat.name ? 'chip-active' : ''"
                >
                  {{ cat.name }}
                </button>
              </div>
              <!-- Emoji 网格 -->
              <div class="grid grid-cols-4 sm:grid-cols-6 gap-1.5 max-h-52 overflow-y-auto pr-1">
                <button
                  v-for="item in currentEmojis"
                  :key="item.icon"
                  type="button"
                  @click="selectEmoji(item.icon)"
                  class="emoji-tile"
                  :class="form.emoji === item.icon ? 'emoji-tile-active' : ''"
                >
                  <span class="text-[22px] leading-none">{{ item.icon }}</span>
                  <span class="text-[10px] text-ink-400 leading-tight truncate w-full text-center">{{ item.label }}</span>
                </button>
              </div>
            </div>
          </div>

          <!-- 物品名称 -->
          <div>
            <label class="field-label">
              物品名称 *
            </label>
            <input
              v-model="form.name"
              type="text"
              required
              maxlength="200"
              class="field-input"
              placeholder="MacBook Pro"
            />
          </div>

          <!-- 分类 -->
          <div>
            <label class="field-label">
              分类 *
            </label>
            <select
              v-model="form.category"
              required
              class="field-input"
            >
              <option value="">请选择分类</option>
              <option v-for="cat in categories" :key="cat" :value="cat">{{ cat }}</option>
            </select>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <!-- 购买金额 -->
            <div>
              <label class="field-label">
                购买金额 (元) *
              </label>
              <input
                type="number"
                required
                min="0"
                class="field-input"
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
              <label class="field-label">
                购买日期 *
              </label>
              <input
                v-model="form.purchase_date"
                type="date"
                required
                class="field-input"
              />
            </div>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <!-- 额外成本 -->
            <div>
              <label class="field-label">
                额外成本 (元)
              </label>
              <input
                type="number"
                min="0"
                class="field-input"
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
              <label class="field-label">
                处置价格 (元)
              </label>
              <input
                type="number"
                min="0"
                class="field-input"
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
            <label class="field-label">
              使用频率
            </label>
            <div class="grid grid-cols-2 gap-3">
              <select
                v-model="form.usage_frequency_type"
                class="field-input"
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
                class="field-input"
                placeholder="次数"
              />
            </div>
          </div>

          <!-- 使用截止日期 -->
          <div>
            <label class="field-label">
              使用截止日期
              <span class="field-hint">不填则视为使用中</span>
            </label>
            <input
              v-model="form.expiry_date"
              type="date"
              class="field-input"
            />
          </div>

          <!-- 备注 -->
          <div>
            <label class="field-label">
              备注
            </label>
            <textarea
              v-model="form.remark"
              rows="3"
              class="field-input"
              placeholder="其他备注信息"
            />
          </div>

          <!-- 按钮 -->
          <div class="flex gap-2.5 pt-2">
            <button
              type="button"
              @click="$emit('close')"
              class="flex-1 py-3 rounded-pill glass-button text-sm font-medium text-ink-500"
            >
              取消
            </button>
            <button
              type="submit"
              class="flex-1 py-3 rounded-pill text-sm font-semibold text-white btn-solid"
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
      class="fixed inset-0 bg-ink-900/25 backdrop-blur-sm flex items-center justify-center z-[60] p-4"
      role="alertdialog"
      aria-modal="true"
      @click.self="validationError = ''"
    >
      <div class="lg rounded-modal p-6 w-full max-w-[20rem] modal-in">
        <h3 class="text-base font-bold text-ink-900 mb-2 text-center">还差一点</h3>
        <p class="text-[13px] text-ink-500 mb-6 text-center leading-relaxed">{{ validationError }}</p>
        <button
          @click="validationError = ''"
          class="w-full py-2.5 rounded-pill text-sm font-semibold text-white btn-solid"
        >
          知道了
        </button>
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
