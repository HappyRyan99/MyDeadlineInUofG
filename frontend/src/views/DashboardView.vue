<template>
  <div class="vh-100 d-flex flex-column bg-light overflow-hidden">
    <!-- Top Section (Navbar) -->
    <nav class="navbar navbar-expand-lg navbar-light bg-white border-bottom shadow-sm flex-shrink-0">
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
                  <ul v-if="tasks_1_day.length > 0" class="list-unstyled mb-0 text-start text-danger">
                    <li v-for="task in tasks_1_day" :key="task.id" class="text-truncate ps-3 overview-task-item" @click="showTaskDetails(task)">
                      <i class="bi bi-dot"></i>{{ task.task_title }}
                    </li>
                  </ul>
                  <span v-else class="text-muted fst-italic">No deadlines</span>
                </div>
                <div class="col-4 border-end">
                  <h5 class="fw-bold mb-3" style="color: #fd7e14;">Within 3 Days</h5>
                  <ul v-if="tasks_3_day.length > 0" class="list-unstyled mb-0 text-start text-orange">
                    <li v-for="task in tasks_3_day" :key="task.id" class="text-truncate ps-3 overview-task-item" @click="showTaskDetails(task)">
                      <i class="bi bi-dot"></i>{{ task.task_title }}
                    </li>
                  </ul>
                  <span v-else class="text-muted fst-italic">No deadlines</span>
                </div>
                <div class="col-4">
                  <h5 class="fw-bold mb-3 text-warning">Within 7 Days</h5>
                  <ul v-if="tasks_7_day.length > 0" class="list-unstyled mb-0 text-start text-warning">
                    <li v-for="task in tasks_7_day" :key="task.id" class="text-truncate ps-3 overview-task-item" @click="showTaskDetails(task)">
                      <i class="bi bi-dot"></i>{{ task.task_title }}
                    </li>
                  </ul>
                  <span v-else class="text-muted fst-italic">No deadlines</span>
                </div>
              </div>
            </div>
          </div>

          <h3 class="mb-3 border-bottom pb-2">Upcoming Deadlines</h3>
          <div class="row row-cols-1 row-cols-md-3 g-4">
            <div v-for="task in tasks" :key="task.id" class="col">
              <div class="card shadow-sm h-100" style="cursor: pointer;" @click="showTaskDetails(task)">
                <div class="card-body d-flex flex-column">
                  <div class="d-flex justify-content-between align-items-start mb-2">
                    <h5 class="card-title mb-0 text-truncate" :title="task.task_title">{{ task.task_title }}</h5>
                    <span v-if="task.group" class="badge bg-success text-white rounded-pill text-truncate" style="max-width: 100px;">Group&nbsp;Work</span>
                    <span v-else class="badge bg-primary text-white rounded-pill">Personal</span>
                  </div>
                  <div v-if="task.group" style="font-size: 12px;" class="text-end">{{ task.group.course_name }}</div>
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
              <div class="card p-4 mb-3 border-dashed border-2 bg-white d-flex align-items-center justify-content-center text-muted empty-state-card" style="min-height: 180px; cursor: pointer;" @click="openAddTaskModal">
                <div class="text-center">
                  <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mb-2 text-secondary" style="opacity: 0.7;">
                    <line x1="12" y1="5" x2="12" y2="19"></line>
                    <line x1="5" y1="12" x2="19" y2="12"></line>
                  </svg>
                  <div class="fw-medium">Add Deadline</div>
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
    <footer class="bg-dark text-white text-center py-3 mt-auto flex-shrink-0">
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
    <div class="modal fade" id="addTaskModal" tabindex="-1" aria-labelledby="addTaskModalLabel" aria-hidden="true" data-bs-backdrop="static" data-bs-keyboard="false" ref="addTaskModalEl">
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

    <!-- Task Details Modal (from DashboardViewNew) -->
    <div v-if="selectedTask" class="modal fade show d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.5); z-index: 1055;" @click.self="closeTaskDetails">
      <div class="modal-dialog modal-dialog-centered modal-lg modal-dialog-scrollable fade-in-up">
        <div class="modal-content border-0 shadow-lg rounded-4 bg-white bg-opacity-90 blur-backdrop">
          <div class="modal-header border-bottom-0 pb-0">
            <h3 class="modal-title fw-bold text-dark h4">{{ selectedTask.task_title }}</h3>
            <button type="button" class="btn-close" @click="closeTaskDetails" aria-label="Close"></button>
          </div>
          <div class="modal-body py-4">          
            <div class="row g-3 mb-4">
              <div class="col-sm-6 text-sm">
                <span class="text-secondary fw-bold text-uppercase d-block mb-1" style="font-size: 0.75rem;">Deadline</span>
                <span :class="['fw-bold', getDeadlineColorClass(selectedTask)]">
                  {{ selectedTask.deadline }}
                </span>
              </div>
              <div class="col-sm-6 text-sm">
                <span class="text-secondary fw-bold text-uppercase d-block mb-1" style="font-size: 0.75rem;">Type</span>
                <span :class="['badge text-white rounded-pill', selectedTask.group ? 'bg-success' : 'bg-primary']">
                  {{ selectedTask.group ? 'Group Work' : 'Personal' }}
                </span>
              </div>
              <div class="col-sm-6 text-sm" v-if="selectedTask.group">
                <span class="text-secondary fw-bold text-uppercase d-block mb-1" style="font-size: 0.75rem;">Course</span>
                <span class="fw-medium text-dark">{{ selectedTask.group.course_code }} - {{ selectedTask.group.course_name }}</span>
              </div>
              <div class="col-sm-6 text-sm" v-if="selectedTask.group">
                <span class="text-secondary fw-bold text-uppercase d-block mb-1" style="font-size: 0.75rem;">Group</span>
                <span class="fw-medium text-dark">{{ selectedTask.group.group_name }}</span>
              </div>
            </div>
            
            <div class="bg-light bg-opacity-50 rounded-3 p-4 border border-1">
              <h4 class="h6 fw-bold text-dark mb-3">Description</h4>
              <p class="mb-0 text-secondary" style="line-height: 1.6; white-space: pre-wrap;">{{ selectedTask.content }}</p>
            </div>
          </div>
          <div class="modal-footer border-top-0 pt-0">
            <button type="button" class="btn btn-secondary" @click="closeTaskDetails">Close</button>
            <button type="button" class="btn btn-danger" v-if="!deletingTaskId" @click="openDeleteModal(selectedTask)">Delete Task</button>
            <button type="button" class="btn btn-danger disabled" v-if="deletingTaskId === selectedTask.id">
               <span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
               Deleting...
            </button>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Custom Confirm Delete Modal -->
    <div v-if="taskToDelete" class="modal fade show d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.5); z-index: 1060;" @click.self="closeDeleteModal">
      <div class="modal-dialog modal-dialog-centered modal-sm fade-in-up">
        <div class="modal-content border-0 shadow-lg rounded-4 bg-white text-center p-4">
          <div class="text-danger mb-3">
            <i class="bi bi-exclamation-circle text-danger" style="font-size: 3rem;"></i>
          </div>
          <h3 class="h4 fw-bold text-dark mb-2">Confirm Delete</h3>
          <p class="text-secondary mb-4">Are you sure you want to delete <br/>"<strong>{{ taskToDelete.task_title }}</strong>"?</p>
          <div class="d-flex justify-content-center gap-3">
            <button type="button" class="btn btn-light px-4" @click="closeDeleteModal">Cancel</button>
            <button type="button" class="btn btn-danger px-4" @click="confirmDeleteTaskBtn">Yes, Delete</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/js/api'
import * as bootstrap from 'bootstrap'


const student = ref(null)

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
  task_title: '',
  content: '',
  deadline: '',
  group_id: ''
})
const taskToDelete = ref(null)
const selectedTask = ref(null)

const deletingTaskId = ref(null)

// DOM Refs for Bootstrap modals
const toastEl = ref(null)
const addTaskModalEl = ref(null)

let bootstrapToast = null
let bootstrapAddTaskModal = null


onMounted(() => {
  // Initialization, like fetching data or initializing bootstrap modals
  fetchData()
  initBootstrapComponents()
})

const initBootstrapComponents = () => {
  // Initialize standard Bootstrap modals/toasts using imported bootstrap module
  if (toastEl.value) bootstrapToast = new bootstrap.Toast(toastEl.value)
  if (addTaskModalEl.value) bootstrapAddTaskModal = new bootstrap.Modal(addTaskModalEl.value)
}

const fetchData = async () => {
  try {
    const response = await api.get('/api/dashboard_data/')
    if (response.data.success) {
      const data = response.data.data
      student.value = data.student
      groups.value = data.groups
      tasks.value = data.tasks
      
      tasks_1_day.value = data.tasks.filter(t => t.hours_until >= 0 && t.hours_until <= 24)
      tasks_3_day.value = data.tasks.filter(t => t.hours_until > 24 && t.hours_until <= 72)
      tasks_7_day.value = data.tasks.filter(t => t.hours_until > 72 && t.hours_until <= 168)
    } else {
      showToast(response.data.error || 'Failed to load data', false)
    }
  } catch (error) {
    if (error.response && error.response.status === 401) {
       window.location.href = '/login/'
    } else {
       showToast('Error fetching data', false)
    }
  }
}

const getDeadlineColorClass = (task) => {
  if (task.is_past_due || task.hours_until <= 24) return 'text-danger'
  if (task.hours_until <= 72) return 'text-orange'
  if (task.hours_until <= 168) return 'text-warning'
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

const submitTask = async () => {
  if (!newTask.value.task_title || !newTask.value.content || !newTask.value.deadline) {
    showToast('Please fill in all required fields.', false)
    return
  }

  const formattedDeadline = newTask.value.deadline.replace('T', ' ')

  try {
    const response = await api.post('/add_task/', {
      task_title: newTask.value.task_title,
      content: newTask.value.content,
      deadline: formattedDeadline,
      group_id: newTask.value.group_id
    })
    
    if (response.data.success) {
      closeAddTaskModal()
      showToast('Task added successfully! Reloading...', true)
      setTimeout(() => {
        window.location.reload()
      }, 1000)
    } else {
      showToast(response.data.error || 'Failed to add task.', false)
    }
  } catch (error) {
    console.error('Error:', error)
    closeAddTaskModal()
    showToast('An unexpected error occurred.', false)
  }
}

const showTaskDetails = (task) => {
  selectedTask.value = task
}

const closeTaskDetails = () => {
  selectedTask.value = null
}

const openDeleteModal = (task) => {
  taskToDelete.value = task
}

const closeDeleteModal = () => {
  taskToDelete.value = null
}

const confirmDeleteTaskBtn = async () => {
  if (!taskToDelete.value) return
  deletingTaskId.value = taskToDelete.value.id

  try {
    const response = await api.post('/delete_task/', {
      id: taskToDelete.value.id
    })
    if (response.data.success) {
      // Remove task seamlessly from UI
      tasks.value = tasks.value.filter(t => t.id !== taskToDelete.value.id)
      tasks_1_day.value = tasks_1_day.value.filter(t => t.id !== taskToDelete.value.id)
      tasks_3_day.value = tasks_3_day.value.filter(t => t.id !== taskToDelete.value.id)
      tasks_7_day.value = tasks_7_day.value.filter(t => t.id !== taskToDelete.value.id)

      if (selectedTask.value && selectedTask.value.id === taskToDelete.value.id) {
        selectedTask.value = null
      }
      closeDeleteModal()
      showToast('Task deleted successfully.', true)
      // Refetch data passively to ensure stats are 100% correct if needed
      fetchData()
    } else {
      showToast(response.data.error || 'Failed to delete task.', false)
    }
  } catch (error) {
    console.error('Error:', error)
    showToast('An unexpected error occurred.', false)
  } finally {
    deletingTaskId.value = null
    closeDeleteModal()
  }
}
</script>

<style scoped>
.blur-backdrop {
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
}
.fade-in-up {
  animation: fadeInUp 0.4s cubic-bezier(0.16, 1, 0.3, 1) forwards;
  opacity: 0;
  transform: translateY(20px);
}
@keyframes fadeInUp {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.border-dashed {
  border-style: dashed !important;
}

.empty-state-card {
  transition: all 0.2s ease-in-out;
  border-color: #dee2e6 !important;
}
.empty-state-card:hover {
  background-color: #f1f3f5 !important;
  border-color: #adb5bd !important;
  color: #495057 !important;
  transform: translateY(-2px);
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075) !important;
}

.overview-task-item {
  cursor: pointer;
}
.overview-task-item:hover {
  text-decoration: underline;
}

.text-orange { color: #fd7e14 !important; }
</style>


