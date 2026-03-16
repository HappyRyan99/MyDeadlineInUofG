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

<style scoped>
/* App-specific local styles (if any) could go here */
</style>
