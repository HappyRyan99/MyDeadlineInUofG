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
        <BaseIcon name="clock-history" class="me-2" />MyDeadlineInUofG
      </router-link>

      <div class="d-flex align-items-center">
        <template v-if="student">
          <span class="me-3 text-muted">Welcome, <strong>{{ student.name }}</strong></span>
          <router-link to="/dashboard" class="me-3 text-decoration-none text-dark">
            <BaseIcon name="speedometer2" class="me-1" />Dashboard
          </router-link>
          <router-link to="/courses" class="me-3 text-decoration-none text-dark">
            <BaseIcon name="book" class="me-1" />My Course
          </router-link>
          <router-link to="/groups" class="me-3 text-decoration-none text-dark">
            <BaseIcon name="people" class="me-1" />My Group
          </router-link>
          <a href="/logout/" class="btn btn-outline-danger btn-sm">
            <BaseIcon name="box-arrow-right" class="me-1" />Logout
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
