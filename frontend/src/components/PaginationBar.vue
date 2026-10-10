<template>
  <nav
    v-if="totalItems > 0"
    class="lg rounded-pill pl-3.5 pr-2 py-1.5 flex items-center gap-2 sm:gap-3 max-w-[calc(100vw-2rem)]"
    aria-label="物品列表分页"
  >
    <!-- 区间说明：补上「第…件」的量词，避免裸数字区间产生歧义 -->
    <p class="text-[11.5px] text-ink-500 tnum whitespace-nowrap shrink-0">
      第 <span class="text-ink-800 font-semibold">{{ rangeStart }}–{{ rangeEnd }}</span> 件
      <span class="text-ink-300 mx-0.5">·</span>
      共 <span class="text-ink-800 font-semibold">{{ totalItems }}</span> 件
    </p>

    <span
      v-if="totalPages > 1"
      class="w-px h-5 bg-gradient-to-b from-transparent via-ink-300/40 to-transparent shrink-0"
      aria-hidden="true"
    />

    <!-- 页码：overflow-x 会连带裁切垂直方向的投影，故用负边距外扩可视区 -->
    <div v-if="totalPages > 1" class="page-track flex items-center gap-0.5 min-w-0 overflow-x-auto scrollbar-hide">
      <button
        class="page-btn shrink-0"
        :disabled="current === 1"
        aria-label="上一页"
        @click="go(current - 1)"
      >
        <ChevronLeft class="w-3.5 h-3.5" />
      </button>

      <template v-for="(page, i) in pageRange" :key="`${page}-${i}`">
        <span v-if="page === '...'" class="page-ellipsis shrink-0" aria-hidden="true">···</span>
        <button
          v-else
          class="page-btn shrink-0"
          :class="{ 'is-active': page === current }"
          :aria-label="`第 ${page} 页`"
          :aria-current="page === current ? 'page' : undefined"
          @click="go(page as number)"
        >
          {{ page }}
        </button>
      </template>

      <button
        class="page-btn shrink-0"
        :disabled="current === totalPages"
        aria-label="下一页"
        @click="go(current + 1)"
      >
        <ChevronRight class="w-3.5 h-3.5" />
      </button>
    </div>

  </nav>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { ChevronLeft, ChevronRight } from 'lucide-vue-next'
import { buildPageRange } from '@/composables/useResponsivePageSize'

const props = defineProps<{
  current: number
  totalItems: number
  /** 每页数量，由视窗自适应算出 */
  effectiveSize: number
}>()

const emit = defineEmits<{
  'update:current': [page: number]
}>()

const totalPages = computed(() =>
  Math.max(1, Math.ceil(props.totalItems / props.effectiveSize))
)

const rangeStart = computed(() =>
  props.totalItems === 0 ? 0 : (props.current - 1) * props.effectiveSize + 1
)

const rangeEnd = computed(() =>
  Math.min(props.current * props.effectiveSize, props.totalItems)
)

const pageRange = computed(() => buildPageRange(props.current, totalPages.value))

function go(page: number) {
  if (page < 1 || page > totalPages.value || page === props.current) return
  emit('update:current', page)
}
</script>
