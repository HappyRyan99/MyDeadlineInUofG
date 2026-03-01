<template>
  <router-view>
    <div></div>
  </router-view>
</template>

<script setup>
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
</style>
