import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'items',
    component: () => import('@/views/ItemsView.vue')
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('@/views/LoginView.vue')
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
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
