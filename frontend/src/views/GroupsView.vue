<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import api from '@/js/api';

const router = useRouter();

// State
const student = ref(null);
const groups = ref([]);
const loading = ref(true);

// Lifecycle Hooks
onMounted(() => {
  fetchData();
});

// Methods
const fetchData = async () => {
  try {
    const response = await api.get('/api/groups_data/');
    if (response.data.success) {
        student.value = response.data.data.student;
        groups.value = response.data.data.groups;
    }
  } catch (error) {
    console.error('Failed to load groups data:', error);
    if (error.response && error.response.status === 401) {
      window.location.href = '/login/';
    }
  } finally {
    loading.value = false;
  }
};

const handleLogout = () => {
  window.location.href = '/logout/';
};
</script>

<template>
  <div class="vh-100 d-flex flex-column bg-light overflow-hidden">
    <!-- ===== NAVBAR ===== -->
    <nav class="navbar navbar-expand-lg navbar-light bg-white border-bottom shadow-sm flex-shrink-0">
      <div class="container-fluid">
        <router-link to="/dashboard" class="navbar-brand fw-bold">
          <i class="bi bi-clock-history me-2"></i>MyDeadlineInUofG
        </router-link>

        <div class="d-flex align-items-center">
          <template v-if="student">
            <span class="me-3 text-muted">
              Welcome, <strong>{{ student.name }}</strong>
            </span>
            <router-link to="/dashboard" class="me-3 text-decoration-none text-dark">
              <i class="bi bi-speedometer2 me-1"></i>Dashboard
            </router-link>
            <router-link to="/courses" class="me-3 text-decoration-none text-dark">
              <i class="bi bi-book me-1"></i>My Course
            </router-link>
            <router-link to="/groups" class="me-3 text-decoration-none text-dark">
              <i class="bi bi-people me-1"></i>My Group
            </router-link>
            <button @click="handleLogout" class="btn btn-outline-danger btn-sm">
              <i class="bi bi-box-arrow-right me-1"></i>Logout
            </button>
          </template>
          <template v-else>
            <a href="/login/" class="btn btn-primary btn-sm">Login</a>
          </template>
        </div>
      </div>
    </nav>

    <!-- ===== MAIN CONTENT ===== -->
    <div class="content-container flex-grow-1 overflow-auto">
      
      <!-- Page Title -->
      <h3 class="mb-4 mt-4 text-primary"><i class="bi bi-people-fill me-2"></i>My Group</h3>

      <!-- Loading State -->
      <div v-if="loading" class="text-center py-5">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>

      <!-- Groups Grid -->
      <div v-else class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
        
        <!-- Group Cards -->
        <div class="col" v-for="group in groups" :key="group.id">
          <div class="card h-100 shadow-sm border-0">
            <div class="card-header bg-white border-bottom-0 pt-3 pb-0">
              <h5 class="card-title text-primary fw-bold mb-0">
                {{ group.group_name }}
              </h5>
            </div>

            <div class="card-body">
              <h6 class="card-subtitle mb-2 text-muted fw-bold">
                {{ group.course_code }}
              </h6>

              <p class="card-text text-secondary mb-3 small">
                {{ group.course_name }}
              </p>

              <div class="border-top pt-2">
                <small class="text-uppercase text-secondary fw-bold" style="font-size: 0.7rem;">
                  Members
                </small>

                <ul class="list-unstyled mt-2 mb-0 small">
                  <li v-for="(member, index) in group.members" :key="index" class="text-secondary d-flex align-items-center mb-1">
                    <i class="bi bi-person-fill me-2 text-muted"></i>
                    {{ member.name }}
                  </li>
                  <li v-if="group.members.length === 0" class="text-muted fst-italic">
                    No members assigned
                  </li>
                </ul>
              </div>
            </div>

            <div class="card-footer bg-light border-0 text-end py-2">
              <small class="text-muted" style="font-size: 0.75rem;">
                Created by {{ group.creator_name }}
              </small>
            </div>
          </div>
        </div>

        <!-- Empty State -->
        <div v-if="groups.length === 0" class="col-12 text-center py-5">
          <div class="text-muted opacity-50">
            <i class="bi bi-people display-1"></i>
            <p class="mt-3 fs-5">You are not in any groups.</p>
          </div>
        </div>
        
      </div> <!-- End Groups Grid -->

      <!-- Back Button -->
      <div class="mt-4 mb-4">
        <router-link to="/dashboard" class="btn btn-secondary">
          <i class="bi bi-arrow-left me-1"></i>Back to Dashboard
        </router-link>
      </div>

    </div> <!-- End Main Content -->

    <!-- ===== FOOTER ===== -->
    <footer class="bg-dark text-white text-center py-3 mt-auto flex-shrink-0">
      <div class="container">
        <p class="mb-0">&copy; 2026 MyDeadlineInUofG. All rights reserved.</p>
      </div>
    </footer>

  </div> <!-- End root wrapper -->
</template>

<style scoped>
.content-container {
  max-width: 1080px;
  margin: 0 auto;
  padding: 0 20px;
  width: 100%;
}
</style>