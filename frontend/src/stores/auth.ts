import { defineStore } from 'pinia'
import { ref } from 'vue'
import { authApi } from '@/api/auth'
import { getToken, setToken, removeToken } from '@/utils/token'
import type { User, LoginRequest } from '@/types'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const token = ref<string | null>(getToken())
  const isAuthenticated = ref(false)

  // 登录
  async function login(credentials: LoginRequest) {
    const response = await authApi.login(credentials)
    user.value = response.user
    token.value = response.token
    isAuthenticated.value = true
    setToken(response.token)
    return response
  }

  // 登出
  async function logout() {
    try {
      await authApi.logout()
    } finally {
      user.value = null
      token.value = null
      isAuthenticated.value = false
      removeToken()
    }
  }

  // 检查认证状态
  async function checkAuth() {
    const savedToken = getToken()
    if (!savedToken) {
      isAuthenticated.value = false
      return false
    }

    try {
      const response = await authApi.verify()
      if (response.valid && response.user) {
        user.value = response.user
        isAuthenticated.value = true
        return true
      }
    } catch (error) {
      console.error('Auth check failed:', error)
      removeToken()
    }

    isAuthenticated.value = false
    return false
  }

  return {
    user,
    token,
    isAuthenticated,
    login,
    logout,
    checkAuth
  }
})
