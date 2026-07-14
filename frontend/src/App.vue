<script setup>
import { RouterLink, RouterView } from 'vue-router'
import ChatbotWidget from './components/ChatbotWidget.vue'
</script>

<template>
  <div class="app-shell">
    <header class="app-header">
      <RouterLink to="/" class="app-logo">LocalHub</RouterLink>
      <span class="app-header-caption">서울시 전체</span>
    </header>
    <main class="app-main">
      <RouterView />
    </main>
    <ChatbotWidget />
  </div>
</template>

<style scoped>
.app-shell {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.app-header {
  display: flex;
  align-items: center;
  gap: var(--space-md);
  height: 56px;
  padding: 0 var(--space-xl);
  background: var(--color-canvas);
  border-bottom: 1px solid var(--color-border);
}

.app-logo {
  font-size: 20px;
  font-weight: 700;
  color: var(--color-primary);
  text-decoration: none;
}

.app-header-caption {
  font-size: 14px;
  color: var(--color-muted);
}

.app-main {
  flex: 1;
  display: flex;
  flex-direction: column;
}
</style>
