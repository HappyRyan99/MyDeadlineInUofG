<script src="../assets/js/components/HeaderView.js"></script>

<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-white border-bottom shadow-sm flex-shrink-0">
    <div class="container-fluid">
      <router-link to="/dashboard" class="navbar-brand fw-bold d-inline-flex align-items-center">
        <BaseIcon name="clock-history" class="me-2" />MyDeadlineInUofG
      </router-link>

      <div class="d-flex align-items-center">
        <template v-if="student">
          <span class="user-welcome">Welcome, <strong>{{ student.name }}</strong></span>
          <router-link to="/dashboard" class="nav-link-custom">
            <BaseIcon name="speedometer2" />Dashboard
          </router-link>
          <router-link to="/courses" class="nav-link-custom">
            <BaseIcon name="book" />My Course
          </router-link>
          <router-link to="/groups" class="nav-link-custom">
            <BaseIcon name="people" />My Group
          </router-link>
          <a href="/logout/" class="btn logout-btn">
            <BaseIcon name="box-arrow-right" />Logout
          </a>
        </template>
        <template v-else>
          <a href="/login/" class="btn btn-primary btn-sm">Login</a>
        </template>
      </div>
    </div>
  </nav>
</template>

<style scoped src="../assets/css/components/HeaderView.css"></style>
