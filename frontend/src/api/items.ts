import api from './request'
import type { Item } from '@/types'

export interface CreateItemData {
  emoji: string
  name: string
  category: string
  purchase_amount: number
  purchase_date: string
  extra_cost?: number
  disposal_price?: number
  remark?: string
  usage_frequency_type?: string
  usage_frequency_value?: number
  expiry_date?: string
}

export interface UpdateItemData extends CreateItemData {
  id: number
}

export const itemsApi = {
  // 获取所有物品
  getItems(params?: {
    search?: string
    category?: string
    status?: string
    sort_by?: string
    sort_order?: string
  }): Promise<{ items: Item[]; total: number }> {
    return api.get('/items', { params })
  },

  // 获取单个物品
  getItem(id: number): Promise<{ item: Item }> {
    return api.get(`/items/${id}`)
  },

  // 创建物品
  createItem(data: CreateItemData): Promise<{ message: string; item: Item }> {
    return api.post('/items', data)
  },

  // 更新物品
  updateItem(id: number, data: Partial<CreateItemData>): Promise<{ message: string; item: Item }> {
    return api.put(`/items/${id}`, data)
  },

  // 删除物品
  deleteItem(id: number): Promise<{ message: string }> {
    return api.delete(`/items/${id}`)
  },

  // 上传图片
  uploadImage(itemId: number, image_data: string): Promise<{ message: string; image: any }> {
    return api.post(`/items/${itemId}/images`, { image_data })
  },

  // 删除图片
  deleteImage(imageId: number): Promise<{ message: string }> {
    return api.delete(`/images/${imageId}`)
  },

  // 记录使用次数
  recordUsage(itemId: number, action: 'increment' | 'decrement' = 'increment'): Promise<{ message: string; manual_usage_count: number }> {
    return api.post(`/items/${itemId}/usage`, { action })
  }
}
