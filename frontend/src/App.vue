<template>
  <div class="app-shell min-h-screen">
    <!-- 动态光斑背景层 -->
    <div class="orb-field" aria-hidden="true">
      <div v-for="n in 6" :key="n" class="orb" :class="`orb-${n}`" />
    </div>
    <router-view />
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

onMounted(async () => {
  await authStore.checkAuth()
})
</script>
