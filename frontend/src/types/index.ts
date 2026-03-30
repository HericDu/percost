// 类型定义文件

export interface User {
  id: number
  username: string
  created_at: string
}

export interface ItemImage {
  id: number
  item_id: number
  image_data: string
  image_order: number
  created_at: string
}

export interface Item {
  id: number
  emoji: string
  name: string
  category: string
  purchase_amount: number
  purchase_date: string
  extra_cost: number
  disposal_price: number
  remark: string
  usage_frequency_type: string
  usage_frequency_value: number
  expiry_date: string | null
  manual_usage_count: number
  created_at: string
  updated_at: string
  images: ItemImage[]
}

export interface LoginRequest {
  username: string
  password: string
}

export interface LoginResponse {
  message: string
  token: string
  user: User
}

export interface ApiResponse<T = any> {
  message?: string
  error?: string
  errors?: string[]
  data?: T
}

export type Category = 
  | '电子产品'
  | '家用电器'
  | '生活用品'
  | '服饰鞋包'
  | '运动健康'
  | '休闲娱乐'
  | '学习办公'
  | '软件服务'
  | '其他'

export type UsageFrequencyType = 
  | 'daily'
  | 'weekly'
  | 'monthly'
  | 'yearly'
  | 'manual'
