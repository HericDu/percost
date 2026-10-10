<template>
  <!-- 校验中：不渲染任何内容，避免登录表单一闪而过暴露入口存在 -->
  <div v-if="state === 'checking'" class="min-h-screen" />

  <!-- 校验通过：显示登录表单 -->
  <LoginView v-else-if="state === 'granted'" />

  <!-- 校验失败：与真实 404 完全一致，不透露此处是否存在后台 -->
  <div v-else class="min-h-screen flex items-center justify-center px-4 py-10">
    <div class="w-full max-w-[26rem] text-center">
      <p class="text-[64px] leading-none font-bold text-ink-200 tnum tracking-tight">404</p>
      <h1 class="text-base font-semibold text-ink-800 mt-5 mb-2">页面不存在</h1>
      <p class="text-[13px] text-ink-500 leading-relaxed">
        这个地址没有对应的内容，可能已被移除或链接有误。
      </p>
      <router-link to="/" class="inline-block mt-7 px-6 py-2.5 rounded-pill text-sm font-semibold text-white btn-solid">
        回到首页
      </router-link>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { authApi } from '@/api/auth'
import LoginView from '@/views/LoginView.vue'

const route = useRoute()
const state = ref<'checking' | 'granted' | 'denied'>('checking')

onMounted(async () => {
  const candidate = String(route.params.gate || '')

  // 空路径或含层级的路径一律视为无效，减少无谓的服务端请求
  if (!candidate || candidate.includes('/')) {
    state.value = 'denied'
    return
  }

  try {
    const { ok } = await authApi.gate(candidate)
    state.value = ok ? 'granted' : 'denied'
  } catch {
    // 包含 404（路径错误）与 429（触发限流），一律按不存在处理
    state.value = 'denied'
  }
})
</script>
