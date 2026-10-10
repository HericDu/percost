<template>
  <div class="min-h-screen flex flex-col items-center justify-center px-4 py-10">
    <div class="w-full max-w-[26rem]">
      <div class="lg rounded-modal p-7 sm:p-8 modal-in">
        <header class="text-center mb-7">
          <h1 class="brand-wordmark">Percost</h1>
          <p class="text-[12.5px] text-ink-400 mt-2.5">算清每件东西的真实成本</p>
        </header>

        <form @submit.prevent="handleLogin" class="space-y-4">
          <div>
            <label for="username" class="field-label">用户名</label>
            <input
              id="username"
              v-model="username"
              type="text"
              required
              autocomplete="username"
              class="field-input"
              placeholder="请输入用户名"
            />
          </div>

          <div>
            <label for="password" class="field-label">密码</label>
            <input
              id="password"
              v-model="password"
              type="password"
              required
              autocomplete="current-password"
              class="field-input"
              placeholder="请输入密码"
            />
          </div>

          <p v-if="error" class="form-error" role="alert">{{ error }}</p>

          <button
            type="submit"
            :disabled="loading"
            class="w-full py-3 rounded-pill text-sm font-semibold text-white btn-solid disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {{ loading ? '登录中…' : '登录' }}
          </button>
        </form>

        <div class="mt-6 text-center">
          <router-link
            to="/"
            class="text-[12.5px] text-ink-400 hover:text-indigo-500 transition-colors"
          >
            不登录，先去看看
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
