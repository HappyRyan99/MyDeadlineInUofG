<template>
  <div class="min-vh-100 d-flex flex-column bg-light">
    <!-- Top Section (Navbar) -->
    <nav class="navbar navbar-expand-lg navbar-light bg-white border-bottom shadow-sm">
      <div class="container-fluid">
        <a class="navbar-brand fw-bold" href="#">
          <i class="bi bi-clock-history me-2"></i>MyDeadlineInUofG
        </a>

        <div class="d-flex align-items-center">
          <template v-if="student">
            <span class="me-3 text-muted">Welcome, <strong>{{ student.name }}</strong></span>
            <router-link to="/courses" class="me-3 text-decoration-none text-dark"><i class="bi bi-book me-1"></i>My Course</router-link>
            <router-link to="/groups" class="me-3 text-decoration-none text-dark"><i class="bi bi-people me-1"></i>My Group</router-link>
            <a href="/logout" class="btn btn-outline-danger btn-sm">
              <i class="bi bi-box-arrow-right me-1"></i>Logout
            </a>
          </template>
        </div>
      </div>
    </nav>

    <!-- Middle Section -->
    <div class="flex-grow-1 p-4 overflow-y-auto">
      <div class="container" style="max-width: 1080px;">
        <template v-if="student">
          <!-- Student Info Card -->
          <div class="card mb-4 shadow-sm">
            <div class="card-header bg-primary text-white">
              <h5 class="mb-0"><i class="bi bi-person-circle me-2"></i>Student Information</h5>
            </div>
            <div class="card-body">
              <div class="row">
                <div class="col-md-4">
                  <p class="mb-1 text-muted">Name</p>
                  <p class="fw-bold">{{ student.name }}</p>
                </div>
                <div class="col-md-4">
                  <p class="mb-1 text-muted">Student ID</p>
                  <p class="fw-bold">{{ student.student_id }}</p>
                </div>
                <div class="col-md-4">
                  <p class="mb-1 text-muted">Email</p>
                  <p class="fw-bold">{{ student.email }}</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Deadline Overview Card -->
          <div class="card mb-4 shadow-sm">
            <div class="card-body">
              <div class="d-flex justify-content-between align-items-center mb-3">
                <h5 class="card-title text-primary mb-0"><i class="bi bi-calendar3 me-2"></i>Deadline Overview</h5>
                <button class="btn btn-sm btn-primary" @click="openAddTaskModal"><i class="bi bi-plus-lg me-1"></i>Add Deadline</button>
              </div>
              <div class="row text-center">
                <div class="col-4 border-end">
                  <h5 class="fw-bold mb-3 text-danger">Within 1 Day</h5>
                  <ul v-if="tasks_1_day.length > 0" class="list-unstyled mb-0 text-start small">
                    <li v-for="task in tasks_1_day" :key="task.id" class="text-truncate ps-3"><i class="bi bi-dot"></i>{{ task.task_title }}</li>
                  </ul>
                  <span v-else class="text-muted small fst-italic">No deadlines</span>
                </div>
                <div class="col-4 border-end">
                  <h5 class="fw-bold mb-3" style="color: #fd7e14;">Within 3 Days</h5>
                  <ul v-if="tasks_3_day.length > 0" class="list-unstyled mb-0 text-start small">
                    <li v-for="task in tasks_3_day" :key="task.id" class="text-truncate ps-3"><i class="bi bi-dot"></i>{{ task.task_title }}</li>
                  </ul>
                  <span v-else class="text-muted small fst-italic">No deadlines</span>
                </div>
                <div class="col-4">
                  <h5 class="fw-bold mb-3 text-warning">Within 7 Days</h5>
                  <ul v-if="tasks_7_day.length > 0" class="list-unstyled mb-0 text-start small">
                    <li v-for="task in tasks_7_day" :key="task.id" class="text-truncate ps-3"><i class="bi bi-dot"></i>{{ task.task_title }}</li>
                  </ul>
                  <span v-else class="text-muted small fst-italic">No deadlines</span>
                </div>
              </div>
            </div>
          </div>

          <h3 class="mb-3 border-bottom pb-2">Upcoming Deadlines</h3>
          <div class="row row-cols-1 row-cols-md-3 g-4">
            <div v-for="task in tasks" :key="task.id" class="col">
              <div class="card shadow-sm h-100 placeholder-wave" style="cursor: pointer; transition: transform 0.2s, box-shadow 0.2s;" onmouseover="this.classList.replace('shadow-sm', 'shadow')" onmouseout="this.classList.replace('shadow', 'shadow-sm')" @click="showTaskDetails(task)">
                <div class="card-body d-flex flex-column">
                  <div class="d-flex justify-content-between align-items-start mb-2">
                    <h5 class="card-title mb-0 text-truncate" :title="task.task_title">{{ task.task_title }}</h5>
                    <span v-if="task.group" class="badge bg-secondary text-truncate" style="max-width: 100px;">Group&nbsp;Work</span>
                    <span v-else class="badge bg-success">Personal</span>
                  </div>
                  <div v-if="task.group" style="font-size: 12px;" class="text-end">{{ task.course_name }}</div>
                  <div class="flex-fill mt-2">
                    <p style="min-height: 80px;max-height: 100px;overflow: hidden;">{{ task.content }}</p>
                  </div>
                  <p :class="['card-text fw-bold mb-auto', getDeadlineColorClass(task)]">
                    <i class="bi bi-calendar-event me-1"></i>
                    {{ task.deadline }}
                  </p>
                </div>
                <div class="card-footer bg-white text-muted small d-flex justify-content-between align-items-center">
                  <div><i class="bi bi-clock me-1"></i>Updated: {{ task.update_time_display || 'recently' }}</div>
                  <button class="btn btn-sm btn-link text-danger p-0" @click.stop="openDeleteModal(task)" title="Delete Task">
                    <i class="bi bi-trash"></i>
                  </button>
                </div>
              </div>
            </div>

            <div class="col" v-if="tasks.length === 0">
              <!-- Add New (Empty State) -->
              <div class="card p-3 mb-3 bg-light d-flex align-items-center justify-content-center text-muted" style="height: 100px; cursor: pointer; border: 2px dashed #dee2e6;" @click="openAddTaskModal">
                <div class="text-center">
                  <i class="bi bi-plus-circle fs-4 mb-1"></i>
                  <div>Add Deadline</div>
                </div>
              </div>
            </div>
          </div>

        </template>
        <template v-else>
          <div class="alert alert-warning text-center" role="alert">
            Please <router-link to="/login" class="alert-link">log in</router-link> to view your dashboard.
          </div>
        </template>
      </div>
    </div>

    <!-- Bottom Section -->
    <footer class="bg-dark text-white text-center py-3 mt-auto">
      <div class="container">
        <small>2026 MyDeadlineInUofG</small>
      </div>
    </footer>

    <!-- Toast Container -->
    <div class="toast-container position-fixed top-0 end-0 p-3" style="z-index: 11">
      <div id="liveToast" class="toast" role="alert" aria-live="assertive" aria-atomic="true" ref="toastEl">
        <div class="toast-header">
          <strong class="me-auto" id="toastTitle">{{ toastTitle }}</strong>
          <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
        <div :class="['toast-body', toastClass]" id="toastBody">
          {{ toastMessage }}
        </div>
      </div>
    </div>

    <!-- Add Task Modal -->
    <div class="modal fade" id="addTaskModal" tabindex="-1" aria-labelledby="addTaskModalLabel" aria-hidden="true" ref="addTaskModalEl">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="addTaskModalLabel">Add New Task</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" @click="closeAddTaskModal"></button>
          </div>
          <div class="modal-body">
            <form id="addTaskForm" @submit.prevent="submitTask">
              <div class="mb-3">
                <label for="taskTitle" class="form-label">Task Title</label>
                <input type="text" class="form-control" id="taskTitle" v-model="newTask.task_title" required>
              </div>
              <div class="mb-3">
                <label for="taskContent" class="form-label">Content</label>
                <textarea class="form-control" id="taskContent" rows="3" v-model="newTask.content" required></textarea>
              </div>
              <div class="mb-3">
                <label for="taskDeadline" class="form-label">Deadline</label>
                <input type="datetime-local" max="2100-01-01T00:00" class="form-control" id="taskDeadline" v-model="newTask.deadline" required>
              </div>
              <div class="mb-3">
                <label for="taskGroup" class="form-label">Group</label>
                <select class="form-select" id="taskGroup" v-model="newTask.group_id">
                  <option value="" selected>Personal (No Group)</option>
                  <option v-for="group in groups" :key="group.id" :value="group.id">{{group.course_code}}-{{ group.group_name }}</option>
                </select>
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" @click="closeAddTaskModal">Close</button>
            <button type="button" class="btn btn-primary" @click="submitTask">Save Task</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div class="modal fade" id="deleteTaskModal" tabindex="-1" aria-labelledby="deleteTaskModalLabel" aria-hidden="true" ref="deleteTaskModalEl">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="deleteTaskModalLabel">Confirm Delete</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" @click="closeDeleteModal"></button>
          </div>
          <div class="modal-body">
            Are you sure you want to delete the task "<span>{{ taskToDelete?.task_title }}</span>"?
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" @click="closeDeleteModal">Cancel</button>
            <button type="button" class="btn btn-danger" @click="confirmDeleteTaskBtn">Delete</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Task Details Modal -->
    <div class="modal fade" id="taskDetailsModal" tabindex="-1" aria-labelledby="taskDetailsModalLabel" aria-hidden="true" ref="taskDetailsModalEl">
      <div class="modal-dialog modal-dialog-centered" style="min-width: 800px; max-width: 1000px;">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="taskDetailsModalLabel">Task Details</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" @click="closeTaskDetails"></button>
          </div>
          <div class="modal-body" v-if="selectedTask">
            <div class="mb-3">
              <small class="text-muted d-block">Title</small>
              <h5 class="fw-bold">{{ selectedTask.task_title }}</h5>
            </div>
            <div class="mb-3">
              <small class="text-muted d-block">Course</small>
              <h5 class="text-primary">
                <span class="fw-bold me-2">{{ selectedTask.course_code }}</span>
                <span class="fw-normal text-dark">{{ selectedTask.course_name }}</span>
                <span class="fw-normal me-2">{{ selectedTask.group_name }}</span>
              </h5>
            </div>
            <div class="mb-3">
              <small class="text-muted d-block">Deadline</small>
              <p class="fs-5 text-danger fw-bold"><i class="bi bi-calendar-event me-2"></i><span>{{ selectedTask.deadline }}</span></p>
            </div>
            <div class="mb-3">
              <small class="text-muted d-block">Content</small>
              <div class="p-3 bg-light rounded border" style="white-space: pre-wrap;">{{ selectedTask.content }}</div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" @click="closeTaskDetails">Close</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

// --- Mock Data or state for static structure ---
const student = ref({
  name: 'Test Student',
  student_id: '12345678',
  email: 'test@student.gla.ac.uk'
})

const tasks_1_day = ref([])
const tasks_3_day = ref([])
const tasks_7_day = ref([])
const tasks = ref([])
const groups = ref([])

// Toast State
const toastTitle = ref('Notification')
const toastMessage = ref('Msg')
const toastClass = ref('text-success')

// Modals State
const newTask = ref({
  task_title: '123',
  content: '123',
  deadline: '123',
  group_id: '123'
})
const taskToDelete = ref(null)
const selectedTask = ref(null)

// DOM Refs for Bootstrap modals
const toastEl = ref(null)
const addTaskModalEl = ref(null)
const deleteTaskModalEl = ref(null)
const taskDetailsModalEl = ref(null)

let bootstrapToast = null
let bootstrapAddTaskModal = null
let bootstrapDeleteModal = null
let bootstrapDetailsModal = null

// --- Methods that were requested to be kept temporarily empty/with method names ---

onMounted(() => {
  // Initialization, like fetching data or initializing bootstrap modals
  fetchData()
  initBootstrapComponents()
})

const initBootstrapComponents = () => {
  // Initialize standard Bootstrap modals/toasts if bootstrap is available in window
  if (window.bootstrap) {
    if (toastEl.value) bootstrapToast = new window.bootstrap.Toast(toastEl.value)
    if (addTaskModalEl.value) bootstrapAddTaskModal = new window.bootstrap.Modal(addTaskModalEl.value)
    if (deleteTaskModalEl.value) bootstrapDeleteModal = new window.bootstrap.Modal(deleteTaskModalEl.value)
    if (taskDetailsModalEl.value) bootstrapDetailsModal = new window.bootstrap.Modal(taskDetailsModalEl.value)
  }
}

const fetchData = () => {
  // TODO: fetch dashboard data and populate student, tasks, groups, etc.
}

const getDeadlineColorClass = (task) => {
  // TODO: implement logic to return correct class based on task deadline
  // classes: text-danger, text-warning, text-dark, or style color
  return 'text-dark'
}

const showToast = (message, isSuccess = true) => {
  toastTitle.value = isSuccess ? 'Success' : 'Error'
  toastMessage.value = message
  toastClass.value = isSuccess ? 'text-success' : 'text-danger'
  if (bootstrapToast) {
    bootstrapToast.show()
  }
}

const openAddTaskModal = () => {
  if (bootstrapAddTaskModal) bootstrapAddTaskModal.show()
}

const closeAddTaskModal = () => {
  if (bootstrapAddTaskModal) bootstrapAddTaskModal.hide()
}

const submitTask = () => {
  // TODO: Save Task Logic
  // fetch POST to add_task
}

const showTaskDetails = (task) => {
  selectedTask.value = task
  if (bootstrapDetailsModal) bootstrapDetailsModal.show()
}

const closeTaskDetails = () => {
  if (bootstrapDetailsModal) bootstrapDetailsModal.hide()
}

const openDeleteModal = (task) => {
  taskToDelete.value = task
  if (bootstrapDeleteModal) bootstrapDeleteModal.show()
}

const closeDeleteModal = () => {
  if (bootstrapDeleteModal) bootstrapDeleteModal.hide()
}

const confirmDeleteTaskBtn = () => {
  // TODO: Confirm Delete Task Logic
  // fetch POST to delete_task
}
</script>


