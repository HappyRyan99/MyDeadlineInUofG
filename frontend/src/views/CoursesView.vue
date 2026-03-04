<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import api from '@/js/api';
import * as bootstrap from 'bootstrap';

const router = useRouter();

// State
const student = ref(null);
const courses = ref([]);
const loading = ref(true);

// Error states
const addCourseError = ref('');

// Form states
const newCourse = ref({ course_code: '', name: '' });
const editCourseData = ref({ id: '', course_code: '', name: '' });
const courseToDelete = ref(null);

// Modal instances
let addCourseModalInstance = null;
let editCourseModalInstance = null;
let deleteCourseModalInstance = null;
let toastInstance = null;

const toastContent = ref({ title: '', message: '', isSuccess: true });

onMounted(() => {
  if (document.getElementById('addCourseModal')) {
    addCourseModalInstance = new bootstrap.Modal(document.getElementById('addCourseModal'));
  }
  if (document.getElementById('editCourseModal')) {
    editCourseModalInstance = new bootstrap.Modal(document.getElementById('editCourseModal'));
  }
  if (document.getElementById('deleteCourseModal')) {
    deleteCourseModalInstance = new bootstrap.Modal(document.getElementById('deleteCourseModal'));
  }
  if (document.getElementById('liveToast')) {
    toastInstance = new bootstrap.Toast(document.getElementById('liveToast'));
  }
  
  fetchData();
});

const showToast = (message, isSuccess = true) => {
  toastContent.value.title = isSuccess ? 'Success' : 'Error';
  toastContent.value.message = message;
  toastContent.value.isSuccess = isSuccess;
  toastInstance?.show();
};

const fetchData = async () => {
  try {
    const response = await api.get('/api/courses_data/');
    if (response.data.success) {
        student.value = response.data.data.student;
        courses.value = response.data.data.courses;
    } else {
        showToast(response.data.error || 'Failed to load course data.', false);
    }
  } catch (error) {
    console.error('Failed to load courses data:', error);
    if (error.response && error.response.status === 401) {
      window.location.href = '/login/';
    } else {
      showToast('Failed to load course data.', false);
    }
  } finally {
    loading.value = false;
  }
};

const handleLogout = () => {
  window.location.href = '/logout/';
};

const openAddCourseModal = () => {
  newCourse.value = { course_code: '', name: '' };
  addCourseError.value = '';
  addCourseModalInstance?.show();
};

const handleAddCourse = async () => {
  if (!newCourse.value.course_code || !newCourse.value.name) {
      addCourseError.value = 'Both Course Code and Name are required.';
      return;
  }
  
  try {
    const formData = new FormData();
    formData.append('course_code', newCourse.value.course_code);
    formData.append('name', newCourse.value.name);
      
    const response = await api.post('/add_course/', formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    });
    
    if (response.data.success) {
      addCourseModalInstance?.hide();
      showToast('Course added successfully!', true);
      fetchData();
    } else {
        addCourseError.value = response.data.error || 'An error occurred';
    }
  } catch (error) {
    console.error('Failed to add course:', error);
    addCourseError.value = 'An unexpected error occurred.';
  }
};

const openEditModal = (course) => {
  editCourseData.value = { 
    id: course.id, 
    course_code: course.course_code, 
    name: course.name 
  };
  editCourseModalInstance?.show();
};

const handleEditCourse = async () => {
    if (!editCourseData.value.name.trim()) {
        showToast('Course name cannot be empty.', false);
        return;
    }

    try {
        const response = await api.post('/edit_course/', {
            course_id: editCourseData.value.id,
            name: editCourseData.value.name
        });

        if (response.data.success) {
            editCourseModalInstance?.hide();
            showToast('Course updated successfully.', true);
            const courseIndex = courses.value.findIndex(c => c.id === editCourseData.value.id);
            if (courseIndex !== -1) {
                courses.value[courseIndex].name = editCourseData.value.name;
            }
        } else {
            showToast(response.data.error || 'Failed to update course.', false);
        }
    } catch (error) {
        console.error('Failed to update course:', error);
        editCourseModalInstance?.hide();
        showToast('An unexpected error occurred.', false);
    }
};

const confirmDeleteModal = (course) => {
  courseToDelete.value = course;
  deleteCourseModalInstance?.show();
};

const handleDeleteCourse = async () => {
  if (!courseToDelete.value) return;

  try {
    const response = await api.post('/delete_course/', {
       course_id: courseToDelete.value.id
    });
    
    if (response.data.success) {
      deleteCourseModalInstance?.hide();
      showToast('Course deleted successfully.', true);
      courses.value = courses.value.filter(c => c.id !== courseToDelete.value.id);
      courseToDelete.value = null;
    } else {
      showToast(response.data.error || 'Failed to delete course.', false);
    }
  } catch (error) {
    console.error('Failed to delete course:', error);
    deleteCourseModalInstance?.hide();
    showToast('An unexpected error occurred.', false);
  }
};
</script>

<template>
  <div class="vh-100 d-flex flex-column bg-light overflow-hidden">
    <!-- Navbar -->
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
            <button @click="handleLogout" class="btn btn-outline-danger btn-sm">
              <i class="bi bi-box-arrow-right me-1"></i>Logout
            </button>
          </template>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <div class="content-container flex-grow-1 overflow-auto">
      <div class="d-flex justify-content-between align-items-center mb-4 mt-4">
        <h3 class="text-primary mb-0"><i class="bi bi-journal-text me-2"></i>My Course</h3>
        <button type="button" class="btn btn-success" @click="openAddCourseModal">
          <i class="bi bi-plus-lg me-1"></i>Add Course
        </button>
      </div>

      <div class="card shadow-sm">
        <div class="card-body p-0">
          <table class="table table-hover table-striped mb-0">
            <thead class="table-light">
              <tr>
                <th scope="col" class="ps-4">Course Code</th>
                <th scope="col">Course Name</th>
                <th scope="col" class="text-end pe-4">Action</th>
              </tr>
            </thead>
            <tbody>
              <!-- Loading State -->
              <tr v-if="loading">
                  <td colspan="3" class="text-center py-4 text-muted">
                     <div class="spinner-border spinner-border-sm me-2" role="status"></div>
                     Loading courses...
                  </td>
              </tr>
              <!-- Empty State -->
              <tr v-else-if="courses.length === 0">
                <td colspan="3" class="text-center py-4 text-muted">No courses found.</td>
              </tr>
              <!-- Data Rows -->
              <tr v-for="course in courses" :key="course.id" v-else>
                <td class="ps-4 fw-bold align-middle">{{ course.course_code }}</td>
                <td class="align-middle">{{ course.name }}</td>
                <td class="text-end pe-4">
                  <button class="btn btn-outline-primary btn-sm me-1" @click="openEditModal(course)">
                    <i class="bi bi-pencil"></i>
                  </button>
                  <button class="btn btn-outline-danger btn-sm" @click="confirmDeleteModal(course)">
                    <i class="bi bi-trash"></i>
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div class="mt-4 mb-4">
        <router-link to="/dashboard" class="btn btn-secondary">
          <i class="bi bi-arrow-left me-1"></i>Back to Dashboard
        </router-link>
      </div>
    </div> <!-- End Main Content -->

    <!-- Footer -->
    <footer class="bg-dark text-white text-center py-3 mt-auto flex-shrink-0">
      <div class="container">
        <p class="mb-0">&copy; 2026 MyDeadlineInUofG. All rights reserved.</p>
      </div>
    </footer>

    <!-- Add Course Modal -->
    <div class="modal fade" id="addCourseModal" tabindex="-1" aria-hidden="true" data-bs-backdrop="static">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Add New Course</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="handleAddCourse">
              <div class="mb-3">
                <label for="courseCode" class="form-label">Course Code</label>
                <input type="text" v-model="newCourse.course_code" class="form-control" id="courseCode" placeholder="e.g., COMPSCI1001" required>
              </div>
              <div class="mb-3">
                <label for="courseName" class="form-label">Course Name</label>
                <input type="text" v-model="newCourse.name" class="form-control" id="courseName" placeholder="e.g., Intro to CS" required>
              </div>
              <div class="alert alert-danger" v-if="addCourseError">{{ addCourseError }}</div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
            <button type="button" class="btn btn-primary" @click="handleAddCourse">Save Course</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Edit Course Modal -->
    <div class="modal fade" id="editCourseModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Edit Course</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="handleEditCourse">
              <div class="mb-3">
                <label class="form-label">Course Code</label>
                <input type="text" :value="editCourseData.course_code" class="form-control" disabled>
                <div class="form-text">Course code cannot be modified.</div>
              </div>
              <div class="mb-3">
                <label class="form-label">Course Name</label>
                <input type="text" v-model="editCourseData.name" class="form-control" required>
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
            <button type="button" class="btn btn-primary" @click="handleEditCourse">Save Changes</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Delete Course Modal -->
    <div class="modal fade" id="deleteCourseModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Confirm Deletion</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <p>Are you sure you want to delete <strong v-if="courseToDelete">{{ courseToDelete.course_code }}</strong>?</p>
            <p class="text-danger small mb-0"><i class="bi bi-exclamation-triangle me-1"></i>This action cannot be undone.</p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
            <button type="button" class="btn btn-danger" @click="handleDeleteCourse">Delete Course</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Toast Container -->
    <div class="toast-container position-fixed top-0 end-0 p-3" style="z-index: 1100">
      <div id="liveToast" class="toast" role="alert" aria-live="assertive" aria-atomic="true">
        <div class="toast-header">
          <strong class="me-auto">{{ toastContent.title }}</strong>
          <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
        <div :class="['toast-body', toastContent.isSuccess ? 'text-success' : 'text-danger']">
          {{ toastContent.message }}
        </div>
      </div>
    </div>

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