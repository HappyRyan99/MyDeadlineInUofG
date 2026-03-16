<template>
  <div class="vh-100 d-flex flex-column bg-light overflow-hidden">
    <HeaderView :student="student" />
    <router-view @update-student="student = $event" />
    <FooterView />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import HeaderView from '@/components/HeaderView.vue'
import FooterView from '@/components/FooterView.vue'

const student = ref(null)
</script>

<style>
/* Reset and Base Styles */
:root {
  --primary-color: #4f46e5;
  --secondary-color: #3b82f6;
  --bg-color: #f3f4f6;
  --card-bg: #ffffff;
  --text-primary: #111827;
  --text-secondary: #6b7280;
  --danger-color: #ef4444;
  --warning-color: #f59e0b;
  --success-color: #10b981;
}

body {
  margin: 0;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  background-color: var(--bg-color);
  color: var(--text-primary);
  height: 100vh;
  -webkit-font-smoothing: antialiased;
}

* {
  box-sizing: border-box;
}

button {
  cursor: pointer;
}

/* Global utility classes */
.btn-circle-sm {
  width: 32px;
  height: 32px;
  padding: 0;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 50% !important;
  line-height: 1;
}

.btn-circle-xs {
  width: 24px;
  height: 24px;
  padding: 0;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 50% !important;
  line-height: 1;
}

.align-middle-icon {
  display: inline-flex;
  align-items: center;
}
</style>
