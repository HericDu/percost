<template>
  <div class="min-h-screen flex items-center justify-center px-4">
    <div class="max-w-md w-full">
      <div class="bg-white/80 backdrop-blur-2xl rounded-[1.75rem] p-8 border border-white/50 shadow-2xl">
        <div class="text-center mb-8">
          <h1 class="text-3xl font-bold bg-gradient-to-r from-indigo-500 to-purple-600 bg-clip-text text-transparent">
            Percost
          </h1>
          <p class="text-gray-400 mt-2 text-sm">智能物品成本管理</p>
        </div>

        <form @submit.prevent="handleLogin" class="space-y-5">
          <div>
            <label for="username" class="block text-sm font-semibold text-gray-700 mb-2">
              用户名
            </label>
            <input
              id="username"
              v-model="username"
              type="text"
              required
              class="glass-input w-full px-4 py-3 rounded-2xl text-sm"
              placeholder="请输入用户名"
            />
          </div>

          <div>
            <label for="password" class="block text-sm font-semibold text-gray-700 mb-2">
              密码
            </label>
            <input
              id="password"
              v-model="password"
              type="password"
              required
              class="glass-input w-full px-4 py-3 rounded-2xl text-sm"
              placeholder="请输入密码"
            />
          </div>

          <div v-if="error" class="text-red-500 text-sm text-center font-medium">
            {{ error }}
          </div>

          <button
            type="submit"
            :disabled="loading"
            class="w-full py-3 px-4 rounded-2xl bg-gradient-to-r from-indigo-500 to-purple-600 text-white text-sm font-semibold shadow-lg shadow-indigo-500/20 hover:shadow-xl hover:shadow-indigo-500/30 active:scale-[0.98] transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {{ loading ? '登录中...' : '登录' }}
          </button>
        </form>

        <div class="mt-6 text-center">
          <router-link to="/" class="text-sm text-gray-400 hover:text-indigo-500 transition-colors">
            返回首页浏览
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const username = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

async function handleLogin() {
  loading.value = true
  error.value = ''

  try {
    await authStore.login({
      username: username.value,
      password: password.value
    })
    router.push('/')
  } catch (err: any) {
    error.value = err.response?.data?.error || '登录失败，请稍后重试'
  } finally {
    loading.value = false
  }
}
</script>
