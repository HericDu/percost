import { ref, onMounted, onUnmounted, readonly } from 'vue'

/**
 * 按视窗尺寸推算每页卡片数。
 *
 * 列数与 ItemsView 网格断点保持一致；行数取「首屏能完整容纳的行数 + 1」——
 * 多出的一行会露出半截，既让版面更饱满，也暗示下方还有内容可滚动。
 */

// 与 grid 的 sm/lg/xl 断点一一对应
const COLUMN_BREAKPOINTS: Array<[number, number]> = [
  [640, 1],   // < 640px  → 1 列
  [1024, 2],  // < 1024px → 2 列
  [1280, 3],  // < 1280px → 3 列
  [Infinity, 4],
]

const CARD_HEIGHT = 225      // 实测卡片高度 207 + 行间距 18
const CHROME_HEIGHT = 162    // 顶部 Dock 126 + 上下外边距 36（分页器在文档流中，不占首屏）
const MIN_ROWS = 2
const MAX_ROWS = 8
const MIN_SIZE = 4
const MAX_SIZE = 48

/* 在「首屏完整容纳的行数」基础上多排一行，让版面更饱满 */
const EXTRA_ROWS = 1

function columnsFor(width: number): number {
  return COLUMN_BREAKPOINTS.find(([max]) => width < max)![1]
}

function computeSize(): { size: number; columns: number } {
  if (typeof window === 'undefined') return { size: 12, columns: 4 }

  const columns = columnsFor(window.innerWidth)
  const usable = window.innerHeight - CHROME_HEIGHT
  // 首屏能完整放下的行数
  const fullRows = Math.max(1, Math.floor(usable / CARD_HEIGHT))
  const rows = Math.min(MAX_ROWS, Math.max(MIN_ROWS, fullRows + EXTRA_ROWS))

  return {
    size: Math.min(MAX_SIZE, Math.max(MIN_SIZE, columns * rows)),
    columns,
  }
}

export function useResponsivePageSize() {
  const autoSize = ref(computeSize().size)
  const columns = ref(computeSize().columns)

  let frame = 0
  function update() {
    cancelAnimationFrame(frame)
    frame = requestAnimationFrame(() => {
      const next = computeSize()
      autoSize.value = next.size
      columns.value = next.columns
    })
  }

  onMounted(() => {
    update()
    window.addEventListener('resize', update, { passive: true })
    window.addEventListener('orientationchange', update, { passive: true })
  })

  onUnmounted(() => {
    cancelAnimationFrame(frame)
    window.removeEventListener('resize', update)
    window.removeEventListener('orientationchange', update)
  })

  return {
    autoSize: readonly(autoSize),
    columns: readonly(columns),
  }
}

/**
 * 生成带省略号的页码序列，两端各保留 1 页、当前页左右各 1 页。
 * 例：1 … 5 6 7 … 20
 */
export function buildPageRange(current: number, total: number): Array<number | '...'> {
  if (total <= 7) return Array.from({ length: total }, (_, i) => i + 1)

  const pages = new Set<number>([1, total, current])
  if (current - 1 > 1) pages.add(current - 1)
  if (current + 1 < total) pages.add(current + 1)
  if (current <= 3) pages.add(2).add(3).add(4)
  if (current >= total - 2) pages.add(total - 1).add(total - 2).add(total - 3)

  const sorted = [...pages].filter(p => p >= 1 && p <= total).sort((a, b) => a - b)

  const result: Array<number | '...'> = []
  let prev = 0
  for (const page of sorted) {
    if (prev && page - prev > 1) result.push('...')
    result.push(page)
    prev = page
  }
  return result
}
