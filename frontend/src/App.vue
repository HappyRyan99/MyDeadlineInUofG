<template>
  <div class="vh-100 d-flex flex-column bg-light overflow-hidden">
    <header role="banner">
      <HeaderView :student="student" />
    </header>
    <main class="flex-grow-1 overflow-hidden d-flex flex-column" role="main">
      <router-view @update-student="student = $event" />
    </main>
    <FooterView />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import HeaderView from '@/components/HeaderView.vue'
import FooterView from '@/components/FooterView.vue'

const student = ref(null)
</script>

<style scoped>
/* App-specific local styles (if any) could go here */
</style>
