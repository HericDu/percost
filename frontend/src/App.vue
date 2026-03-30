<template>
  <div class="min-h-screen bg-gradient-to-br from-indigo-50/80 via-purple-30/60 to-blue-50/70 dark:from-gray-950 dark:via-gray-900 dark:to-indigo-950/50">
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
