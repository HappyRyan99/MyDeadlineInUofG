<script setup>
defineProps({
  student: {
    type: Object,
    default: null
  }
})
</script>

<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-white border-bottom shadow-sm flex-shrink-0">
    <div class="container-fluid">
      <router-link to="/dashboard" class="navbar-brand fw-bold">
        <i class="bi bi-clock-history me-2"></i>MyDeadlineInUofG
      </router-link>

      <div class="d-flex align-items-center">
        <template v-if="student">
          <span class="me-3 text-muted">Welcome, <strong>{{ student.name }}</strong></span>
          <router-link to="/dashboard" class="me-3 text-decoration-none text-dark">
            <i class="bi bi-speedometer2 me-1"></i>Dashboard
          </router-link>
          <router-link to="/courses" class="me-3 text-decoration-none text-dark">
            <i class="bi bi-book me-1"></i>My Course
          </router-link>
          <router-link to="/groups" class="me-3 text-decoration-none text-dark">
            <i class="bi bi-people me-1"></i>My Group
          </router-link>
          <a href="/logout/" class="btn btn-outline-danger btn-sm">
            <i class="bi bi-box-arrow-right me-1"></i>Logout
          </a>
        </template>
        <template v-else>
          <a href="/login/" class="btn btn-primary btn-sm">Login</a>
        </template>
      </div>
    </div>
  </nav>
</template>

<style scoped>

</style>
