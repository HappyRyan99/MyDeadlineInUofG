<script src="../assets/js/views/CoursesView.js"></script>

<template>
    <!-- Main Content -->
    <div class="flex-grow-1 w-100 overflow-y-auto">
      <div class="view-container">
        <div class="view-header">
          <h1 class="h3 text-primary mb-0"><BaseIcon name="journal-text" class="me-2" />My Course</h1>
          <button type="button" class="btn btn-primary" @click="openAddCourseModal">
            <BaseIcon name="plus-lg" class="me-1" />Add Course
          </button>
        </div>

        <div class="course-table-card card shadow-sm">
          <div class="card-body p-0">
            <table class="course-table table table-hover table-striped mb-0">
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
                  <td class="action-column text-end pe-4">
                    <button class="btn btn-outline-primary btn-sm btn-circle-sm me-1" @click="openEditModal(course)">
                      <BaseIcon name="pencil" />
                    </button>
                    <button class="btn btn-outline-danger btn-sm btn-circle-sm" @click="confirmDeleteModal(course)">
                      <BaseIcon name="trash" />
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <div class="mt-4 mb-4">
          <router-link to="/dashboard" class="btn btn-secondary">
            <BaseIcon name="arrow-left" class="me-1" />Back to Dashboard
          </router-link>
        </div>
      </div> <!-- End view-container -->
    </div> <!-- End Main Content -->
    <div class="modal fade" id="addCourseModal" tabindex="-1" aria-hidden="true" data-bs-backdrop="static">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h2 class="modal-title h5">Add New Course</h2>
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
            <h2 class="modal-title h5">Edit Course</h2>
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
    <ConfirmModal 
      modalId="deleteCourseModal"
      title="Confirm Deletion"
      confirmText="Delete Course"
      @confirm="handleDeleteCourse">
      <template #message>
        Are you sure you want to delete <strong v-if="courseToDelete">{{ courseToDelete.course_code }}</strong>?
      </template>
    </ConfirmModal>

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
</template>

<style scoped src="../assets/css/views/CoursesView.css"></style>