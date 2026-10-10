import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'items',
    component: () => import('@/views/ItemsView.vue')
  },
  {
    path: '/subscription',
    name: 'subscription',
    component: () => import('@/views/SubscriptionView.vue')
  },
  {
    path: '/shopping-list',
    name: 'shopping-list',
    component: () => import('@/views/ShoppingListView.vue')
  },
  {
    // 管理入口：任意未匹配路径都落到这里，由服务端判定是否为后台入口。
    // 真实路径不存在于前端代码中，无法通过阅读 JS 推断。
    path: '/:gate(.*)',
    name: 'gate',
    component: () => import('@/views/GateView.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
