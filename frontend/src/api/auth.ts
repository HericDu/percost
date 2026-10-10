import api from './request'
import type { LoginRequest, LoginResponse } from '@/types'

export const authApi = {
  // 校验是否为管理后台入口路径（真实路径仅存在于服务端）
  gate(path: string): Promise<{ ok: boolean }> {
    return api.post('/auth/gate', { path })
  },

  // 用户登录
  login(data: LoginRequest): Promise<LoginResponse> {
    return api.post('/auth/login', data)
  },

  // 用户登出
  logout(): Promise<{ message: string }> {
    return api.post('/auth/logout')
  },

  // 验证 Token
  verify(): Promise<{ valid: boolean; user?: any }> {
    return api.get('/auth/verify')
  },

  // 获取当前用户信息
  getUser(): Promise<{ user: any }> {
    return api.get('/auth/user')
  }
}
