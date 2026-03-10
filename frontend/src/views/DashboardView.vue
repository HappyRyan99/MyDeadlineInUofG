<template>
  <div class="vh-100 d-flex flex-column bg-light overflow-hidden">
    <!-- Top Section (Navbar) -->
    <HeaderView :student="student" />

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
                <button class="btn btn-sm btn-primary" @click="openAddDeadlineModal"><i class="bi bi-plus-lg me-1"></i>Add
                  Deadline
                </button>
              </div>

              <!-- Real-time Clock Display -->
              <div class="d-flex justify-content-center mb-4">
                <div
                    class="h5 fw-bold text-dark px-4 py-2 bg-light border rounded shadow-sm d-flex align-items-center bg-white mb-0">
                  <i class="bi bi-clock-fill text-primary me-2"></i>{{ currentTime }}
                </div>
              </div>

              <div class="row text-center">
                <div v-for="(section, index) in overviewSections" :key="index" :class="['col-4', section.borderClass]">
                  <h5 class="fw-bold mb-3" :class="section.colorClass">{{ section.title }}</h5>
                  <ul v-if="section.deadlines.length > 0" class="list-unstyled mb-0 text-start"
                      :class="section.colorClass">
                    <li v-for="deadline in section.deadlines" :key="deadline.id"
                        class="text-truncate ps-3 overview-deadline-item"
                        @click="showDeadlineDetails(deadline)">
                      <i class="bi bi-dot"></i>{{ deadline.deadline_title }}
                    </li>
                  </ul>
                  <span v-else class="text-muted fst-italic">No deadlines</span>
                </div>
              </div>
            </div>
          </div>

          <h3 class="mb-3 border-bottom pb-2">
            <i class="bi bi-card-checklist me-2 text-primary"></i>Upcoming Deadlines
          </h3>
          <div class="row row-cols-1 row-cols-md-3 g-4">
            <div v-for="deadline in active_deadlines" :key="deadline.id" class="col">
              <DeadlineCard :deadline="deadline" @show-details="showDeadlineDetails"
                            @delete-deadline="openDeleteModal"/>
            </div>

            <div class="col" v-if="active_deadlines.length === 0">
              <!-- Add New (Empty State) -->
              <div
                  class="card p-4 mb-3 border-dashed border-2 bg-white d-flex align-items-center justify-content-center text-muted empty-state-card"
                  style="min-height: 180px; cursor: pointer;" @click="openAddDeadlineModal">
                <div class="text-center">
                  <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
                       stroke-linecap="round" stroke-linejoin="round" class="mb-2 text-secondary" style="opacity: 0.7;">
                    <line x1="12" y1="5" x2="12" y2="19"></line>
                    <line x1="5" y1="12" x2="19" y2="12"></line>
                  </svg>
                  <div class="fw-medium">Add Deadline</div>
                </div>
              </div>
            </div>
          </div>

          <!-- Completed Deadlines Section -->
          <template v-if="completed_deadlines.length > 0">
            <h3 class="mb-3 border-bottom pb-2 mt-5 text-success">
              <i class="bi bi-check2-circle me-2"></i>Completed Deadlines
            </h3>
            <div class="row row-cols-1 row-cols-md-3 g-4 opacity-75">
              <div v-for="deadline in completed_deadlines" :key="deadline.id" class="col">
                <DeadlineCard :deadline="deadline" @show-details="showDeadlineDetails"
                              @delete-deadline="openDeleteModal"/>
              </div>
            </div>
          </template>

        </template>
        <template v-else>
          <div class="alert alert-warning text-center" role="alert">
            Please
            <router-link to="/login" class="alert-link">log in</router-link>
            to view your dashboard.
          </div>
        </template>
      </div>
    </div>

    <!-- Bottom Section -->
    <FooterView/>

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

    <!-- Add Deadline Modal -->
    <div class="modal fade" id="addDeadlineModal" tabindex="-1" aria-labelledby="addDeadlineModalLabel"
         aria-hidden="true"
         data-bs-backdrop="static" data-bs-keyboard="false" ref="addDeadlineModalEl">
      <div class="modal-dialog" style="max-width: 550px;">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="addDeadlineModalLabel">Add New Deadline</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"
                    @click="closeAddDeadlineModal"></button>
          </div>
          <div class="modal-body">
            <form id="addDeadlineForm" @submit.prevent="submitDeadline" novalidate>
              <div class="mb-3">
                <label for="deadlineTitle" class="form-label">Deadline Title</label>
                <input type="text" class="form-control" :class="{ 'is-invalid': formErrors.deadline_title }"
                       id="deadlineTitle" v-model="newDeadline.deadline_title" required
                       aria-describedby="deadlineTitleFeedback">
                <div id="deadlineTitleFeedback" class="invalid-feedback">
                  Please provide a deadline title.
                </div>
              </div>
              <div class="mb-3">
                <label for="deadlineContent" class="form-label">Content</label>
                <textarea class="form-control" :class="{ 'is-invalid': formErrors.content }" id="deadlineContent"
                          rows="3" v-model="newDeadline.content" required
                          aria-describedby="deadlineContentFeedback"></textarea>
                <div id="deadlineContentFeedback" class="invalid-feedback">
                  Please provide a description or content.
                </div>
              </div>
              <div class="mb-3">
                <label for="deadlineDate" class="form-label">Deadline</label>
                <input type="datetime-local" max="2100-01-01T00:00" class="form-control"
                       :class="{ 'is-invalid': formErrors.deadline }" id="deadlineDate"
                       v-model="newDeadline.deadline" required aria-describedby="deadlineDateFeedback">
                <div id="deadlineDateFeedback" class="invalid-feedback">
                  Please provide a valid date and time for the deadline.
                </div>
              </div>
              <div class="mb-3">
                <label for="deadlineGroup" class="form-label">Group</label>
                <select class="form-select" id="deadlineGroup" v-model="newDeadline.group_id" style="max-width: 100%;">
                  <option value="" selected>Personal (Individual)</option>
                  <option v-for="group in groups" :key="group.id" :value="group.id"
                          :title="group.course_code + ' - ' + group.course_name + ' (' + group.group_name + ')'">
                    {{ formatGroupOption(group) }}
                  </option>
                </select>
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" @click="closeAddDeadlineModal">Close
            </button>
            <button type="button" class="btn btn-primary" @click="submitDeadline">Save Deadline</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Deadline Details Modal -->
    <div v-if="selectedDeadline" class="modal fade show d-block" tabindex="-1"
         style="background-color: rgba(0,0,0,0.5); z-index: 1055;">
      <div class="modal-dialog modal-dialog-centered modal-lg modal-dialog-scrollable fade-in-up">
        <div class="modal-content border-0 shadow-lg rounded-4 bg-white bg-opacity-90 blur-backdrop">
          <div class="modal-header border-bottom-0 pb-0 align-items-start">
            <h3 class="modal-title fw-bold text-dark h4 mb-0 text-break pe-3 w-100 d-flex align-items-center"
                :class="{'text-danger': selectedDeadline.status === '0' && selectedDeadline.is_past_due}">
              <i v-if="selectedDeadline.status === '1'" class="bi bi-check-circle-fill text-success me-2"></i>
              <span v-if="selectedDeadline.status === '0' && selectedDeadline.is_past_due">[Overdue] </span>

              <!-- Title Edit Mode -->
              <div v-if="editingField === 'title'" class="d-flex w-100 align-items-center">
                <input type="text" class="form-control me-2" v-model="editTitleValue"
                       @keyup.enter="saveDeadlineEdit('title')" @keyup.esc="cancelDeadlineEdit" autofocus>
                <button class="btn btn-sm btn-success me-1 px-2" @click="saveDeadlineEdit('title')"><i
                    class="bi bi-check-lg"></i></button>
                <button class="btn btn-sm btn-secondary px-2" @click="cancelDeadlineEdit"><i class="bi bi-x-lg"></i>
                </button>
              </div>
              <!-- Title Display Mode -->
              <div v-else class="d-flex align-items-center">
                <span>{{ selectedDeadline.deadline_title }}</span>
                <button v-if="selectedDeadline.can_edit" class="btn btn-sm btn-link text-secondary p-0 ms-2"
                        @click="startDeadlineEdit('title')" title="Edit Title">
                  <i class="bi bi-pencil"></i>
                </button>
              </div>
            </h3>
            <button type="button" class="btn-close mt-1 flex-shrink-0" @click="closeDeadlineDetails"
                    aria-label="Close"></button>
          </div>
          <div class="modal-body py-4">

            <div class="row g-3 mb-4">
              <div class="col-sm-6 text-sm">
                <span class="text-secondary fw-bold text-uppercase d-block mb-1"
                      style="font-size: 0.75rem;">Deadline</span>
                <span :class="['fw-bold', getDeadlineColorClass(selectedDeadline)]">
                  {{ selectedDeadline.deadline }}
                </span>
              </div>
              <div class="col-sm-6 text-sm">
                <span class="text-secondary fw-bold text-uppercase d-block mb-1" style="font-size: 0.75rem;">Type</span>
                <span :class="['badge text-white rounded-pill', selectedDeadline.group ? 'bg-success' : 'bg-primary']">
                  {{ selectedDeadline.group ? 'Group Work' : 'Personal' }}
                </span>
              </div>
              <div class="col-sm-6 text-sm" v-if="selectedDeadline.group">
                <span class="text-secondary fw-bold text-uppercase d-block mb-1"
                      style="font-size: 0.75rem;">Course</span>
                <span class="fw-medium text-dark">{{
                    selectedDeadline.group.course_code
                  }} - {{ selectedDeadline.group.course_name }}</span>
              </div>
              <div class="col-sm-6 text-sm" v-if="selectedDeadline.group">
                <span class="text-secondary fw-bold text-uppercase d-block mb-1"
                      style="font-size: 0.75rem;">Group</span>
                <span class="fw-medium text-dark">{{ selectedDeadline.group.group_name }}</span>
              </div>
            </div>

            <div class="bg-light bg-opacity-50 rounded-3 p-4 border border-1">
              <div class="d-flex justify-content-between align-items-center mb-3">
                <h4 class="h6 fw-bold text-dark mb-0">Description</h4>
                <button v-if="selectedDeadline.can_edit && editingField !== 'content'"
                        class="btn btn-sm btn-link text-secondary p-0" @click="startDeadlineEdit('content')"
                        title="Edit Description">
                  <i class="bi bi-pencil"></i>
                </button>
              </div>

              <!-- Content Edit Mode -->
              <div v-if="editingField === 'content'">
                <textarea class="form-control mb-2" rows="4" v-model="editContentValue" @keyup.esc="cancelDeadlineEdit"
                          autofocus></textarea>
                <div class="d-flex justify-content-end">
                  <button class="btn btn-sm btn-secondary me-2" @click="cancelDeadlineEdit">Cancel</button>
                  <button class="btn btn-sm btn-success" @click="saveDeadlineEdit('content')">Save</button>
                </div>
              </div>
              <!-- Content Display Mode -->
              <p v-else class="mb-0 text-secondary" style="line-height: 1.6; white-space: pre-wrap;">{{
                  selectedDeadline.content
                }}</p>
            </div>

            <div class="mt-4">
              <h4 class="h6 fw-bold text-dark mb-3">Latest 3 Updates / Logs</h4>

              <!-- Logs List -->
              <div v-if="selectedDeadline.logs && selectedDeadline.logs.length > 0" class="mb-3">
                <div v-for="log in selectedDeadline.logs.slice(0, 3)" :key="log.id"
                     class="card mb-2 border-0 shadow-sm bg-light">
                  <div class="card-body p-3">
                    <p class="mb-1 text-dark fw-bold" style="white-space: pre-wrap; font-size: 1.15rem;">{{
                        log.content
                      }}</p>
                    <small class="text-muted"><i class="bi bi-clock me-1"></i>{{ log.create_time }}</small>
                  </div>
                </div>
                <div class="text-end mt-2" v-if="selectedDeadline.logs.length > 3">
                  <span class="more-logs-btn" @click="showMoreLogsToast">More</span>
                </div>
              </div>
              <div v-else class="text-muted text-center mb-3 fst-italic small">No updates yet.</div>

              <!-- Add Log Form -->
              <div class="card border-0 shadow-sm" v-if="selectedDeadline.status === '0'">
                <div class="card-body p-3">
                  <textarea class="form-control mb-2" rows="2" placeholder="Write an update (max 280 chars)..."
                            v-model="newLogContent" maxlength="280"></textarea>
                  <div class="d-flex justify-content-between align-items-center">
                    <small class="text-muted">{{ 280 - (newLogContent ? newLogContent.length : 0) }} chars left</small>
                    <button class="btn btn-sm btn-primary" @click="submitDeadlineLog"
                            :disabled="!newLogContent.trim() || isSubmittingLog">
                      <span v-if="isSubmittingLog" class="spinner-border spinner-border-sm me-1" role="status"
                            aria-hidden="true"></span>
                      Add Update
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="modal-footer border-top-0 pt-0 d-flex justify-content-between align-items-center">
            <!-- Completion Switch -->
            <div v-if="selectedDeadline && selectedDeadline.is_creator" class="d-flex align-items-center">
              <div v-if="selectedDeadline.status === '0'"
                   class="form-check form-switch m-0 p-0 d-flex align-items-center">
                <input class="form-check-input m-0 me-2 cursor-pointer" type="checkbox" role="switch"
                       id="completeDeadlineSwitch"
                       :checked="false" @change="toggleDeadlineStatus" style="width: 2.25em; height: 1.15em;">
                <label class="form-check-label fw-bold cursor-pointer text-primary m-0" for="completeDeadlineSwitch"
                       style="font-size: 1.1rem; line-height: 1;">Done</label>
              </div>
              <div v-else class="text-success fw-bold d-flex align-items-center" style="font-size: 1rem;">
                <i class="bi bi-check2-all me-1"></i>Completed
              </div>
            </div>
            <div v-else-if="selectedDeadline" class="d-flex align-items-center">
              <span v-if="selectedDeadline.status === '1'" class="text-success fw-bold"><i
                  class="bi bi-check2-all me-1"></i>Completed</span>
              <span v-else class="text-muted fst-italic">In Progress</span>
            </div>

            <div class="d-flex gap-2">
              <button type="button" class="btn btn-secondary" @click="closeDeadlineDetails">Close</button>
              <button type="button" class="btn btn-danger" v-if="selectedDeadline.is_creator && !deletingDeadlineId"
                      @click="openDeleteModal(selectedDeadline)">Delete Deadline
              </button>
              <button type="button" class="btn btn-danger disabled"
                      v-if="selectedDeadline.is_creator && deletingDeadlineId === selectedDeadline.id">
                <span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                Deleting...
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Custom Confirm Delete Modal -->
    <div v-if="deadlineToDelete" class="modal fade show d-block" tabindex="-1"
         style="background-color: rgba(0,0,0,0.5); z-index: 1060;" @click.self="closeDeleteModal">
      <div class="modal-dialog modal-dialog-centered modal-sm fade-in-up">
        <div class="modal-content border-0 shadow-lg rounded-4 bg-white text-center p-4">
          <div class="text-danger mb-3">
            <i class="bi bi-exclamation-circle text-danger" style="font-size: 3rem;"></i>
          </div>
          <h3 class="h4 fw-bold text-dark mb-2">Confirm Delete</h3>
          <p class="text-secondary mb-4">Are you sure you want to delete <br/>"<strong>{{
              deadlineToDelete.deadline_title
            }}</strong>"?</p>
          <div class="d-flex justify-content-center gap-3">
            <button type="button" class="btn btn-light px-4" @click="closeDeleteModal">Cancel</button>
            <button type="button" class="btn btn-danger px-4" @click="confirmDeleteDeadlineBtn">Yes, Delete</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import {ref, computed, onMounted, onUnmounted} from 'vue'
import api from '@/js/api'
import * as bootstrap from 'bootstrap'
import DeadlineCard from '@/components/DeadlineCard.vue'
import {getDeadlineColorClass, formatGroupOption} from '@/utils/deadlineUtils'
import HeaderView from "@/components/HeaderView.vue";
import FooterView from "@/components/FooterView.vue";

const currentTime = ref('')
let timerInterval = null

const updateTime = () => {
  const now = new Date()
  const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
  const yyyy = now.getFullYear()
  const MMM = monthNames[now.getMonth()]
  const dd = String(now.getDate()).padStart(2, '0')
  const HH = String(now.getHours()).padStart(2, '0')
  const mm = String(now.getMinutes()).padStart(2, '0')
  const ss = String(now.getSeconds()).padStart(2, '0')
  currentTime.value = `${dd} ${MMM} ${yyyy} ${HH}:${mm}:${ss}`
}

const student = ref(null)

const deadlines_1_day = ref([])
const deadlines_3_day = ref([])
const deadlines_7_day = ref([])
const deadlines = ref([])
const active_deadlines = ref([])
const completed_deadlines = ref([])
const groups = ref([])

const overviewSections = computed(() => [
  {title: 'Within 1 Day', deadlines: deadlines_1_day.value, colorClass: 'text-danger', borderClass: 'border-end'},
  {title: 'Within 3 Days', deadlines: deadlines_3_day.value, colorClass: 'text-orange', borderClass: 'border-end'},
  {title: 'Within 7 Days', deadlines: deadlines_7_day.value, colorClass: 'text-warning', borderClass: ''}
])

// Toast State
const toastTitle = ref('Notification')
const toastMessage = ref('Msg')
const toastClass = ref('text-success')

// Modals State
const newDeadline = ref({
  deadline_title: '',
  content: '',
  deadline: '',
  group_id: ''
})

const formErrors = ref({
  deadline_title: false,
  content: false,
  deadline: false
})

const resetFormErrors = () => {
  formErrors.value = {
    deadline_title: false,
    content: false,
    deadline: false
  }
}
const deadlineToDelete = ref(null)
const selectedDeadline = ref(null)

const newLogContent = ref('')
const isSubmittingLog = ref(false)

const deletingDeadlineId = ref(null)

// Edit Deadline State
const editingField = ref(null) // 'title' or 'content'
const editTitleValue = ref('')
const editContentValue = ref('')

// DOM Refs for Bootstrap modals
const toastEl = ref(null)
const addDeadlineModalEl = ref(null)

let bootstrapToast = null
let bootstrapAddDeadlineModal = null


onMounted(() => {
  // Start clock
  updateTime()
  timerInterval = setInterval(updateTime, 1000)

  // Initialization, like fetching data or initializing bootstrap modals
  fetchData()
  initBootstrapComponents()
})

onUnmounted(() => {
  if (timerInterval) {
    clearInterval(timerInterval)
  }
})

const initBootstrapComponents = () => {
  // Initialize standard Bootstrap modals/toasts using imported bootstrap module
  if (toastEl.value) bootstrapToast = new bootstrap.Toast(toastEl.value)
  if (addDeadlineModalEl.value) bootstrapAddDeadlineModal = new bootstrap.Modal(addDeadlineModalEl.value)
}

const fetchData = async () => {
  try {
    const response = await api.get('/api/dashboard_data/')
    if (response.data.success) {
      const data = response.data.data
      student.value = data.student
      groups.value = data.groups
      deadlines.value = data.deadlines
      active_deadlines.value = data.deadlines.filter(t => t.status === '0')
      completed_deadlines.value = data.deadlines.filter(t => t.status === '1')

      deadlines_1_day.value = active_deadlines.value.filter(t => t.hours_until >= 0 && t.hours_until <= 24)
      deadlines_3_day.value = active_deadlines.value.filter(t => t.hours_until > 24 && t.hours_until <= 72)
      deadlines_7_day.value = active_deadlines.value.filter(t => t.hours_until > 72 && t.hours_until <= 168)
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


const showToast = (message, isSuccess = true) => {
  toastTitle.value = isSuccess ? 'Success' : 'Error'
  toastMessage.value = message
  toastClass.value = isSuccess ? 'text-success' : 'text-danger'
  if (bootstrapToast) {
    bootstrapToast.show()
  }
}

const openAddDeadlineModal = () => {
  if (bootstrapAddDeadlineModal) bootstrapAddDeadlineModal.show()
}

const closeAddDeadlineModal = () => {
  if (bootstrapAddDeadlineModal) bootstrapAddDeadlineModal.hide()
  resetFormErrors()
}

const submitDeadline = async () => {
  resetFormErrors()
  let hasError = false

  if (!newDeadline.value.deadline_title || !newDeadline.value.deadline_title.trim()) {
    formErrors.value.deadline_title = true
    hasError = true
  }
  if (!newDeadline.value.content || !newDeadline.value.content.trim()) {
    formErrors.value.content = true
    hasError = true
  }
  if (!newDeadline.value.deadline) {
    formErrors.value.deadline = true
    hasError = true
  }

  if (hasError) {
    return
  }

  const formattedDeadline = newDeadline.value.deadline.replace('T', ' ')

  try {
    const response = await api.post('/add_deadline/', {
      deadline_title: newDeadline.value.deadline_title,
      content: newDeadline.value.content,
      deadline: formattedDeadline,
      group_id: newDeadline.value.group_id
    })

    if (response.data.success) {
      closeAddDeadlineModal()
      showToast('Deadline added successfully! Reloading...', true)
      setTimeout(() => {
        window.location.reload()
      }, 1000)
    } else {
      showToast(response.data.error || 'Failed to add deadline.', false)
    }
  } catch (error) {
    console.error('Error:', error)
    closeAddDeadlineModal()
    showToast('An unexpected error occurred.', false)
  }
}

const showDeadlineDetails = (deadline) => {
  selectedDeadline.value = deadline
}

const closeDeadlineDetails = () => {
  selectedDeadline.value = null
  newLogContent.value = ''
  editingField.value = null
}

const startDeadlineEdit = (field) => {
  editingField.value = field
  if (field === 'title') {
    editTitleValue.value = selectedDeadline.value.deadline_title
  } else if (field === 'content') {
    editContentValue.value = selectedDeadline.value.content
  }
}

const cancelDeadlineEdit = () => {
  editingField.value = null
}

const saveDeadlineEdit = async (field) => {
  if (!selectedDeadline.value) return

  let payload = {deadline_id: selectedDeadline.value.id}

  if (field === 'title') {
    if (!editTitleValue.value.trim()) {
      showToast('Title cannot be empty', false)
      return
    }
    payload.deadline_title = editTitleValue.value.trim()
  } else if (field === 'content') {
    if (!editContentValue.value.trim()) {
      showToast('Description cannot be empty', false)
      return
    }
    payload.content = editContentValue.value.trim()
  }

  try {
    const response = await api.post('/edit_deadline/', payload)

    if (response.data.success) {
      if (field === 'title') {
        selectedDeadline.value.deadline_title = payload.deadline_title
      } else if (field === 'content') {
        selectedDeadline.value.content = payload.content
      }

      const updateList = (list) => {
        const index = list.findIndex(t => t.id === selectedDeadline.value.id)
        if (index !== -1) {
          if (field === 'title') list[index].deadline_title = payload.deadline_title
          if (field === 'content') list[index].content = payload.content
        }
      }
      updateList(deadlines.value)
      updateList(active_deadlines.value)
      updateList(completed_deadlines.value)
      updateList(deadlines_1_day.value)
      updateList(deadlines_3_day.value)
      updateList(deadlines_7_day.value)

      showToast('Deadline updated successfully', true)
      editingField.value = null
    } else {
      showToast(response.data.error || 'Failed to update deadline', false)
    }
  } catch (error) {
    console.error('Error updating deadline:', error)
    showToast('Failed to connect to the server', false)
  }
}

const showMoreLogsToast = () => {
  showToast('Implementation in the future', true)
}

const submitDeadlineLog = async () => {
  if (!newLogContent.value.trim() || !selectedDeadline.value) return

  isSubmittingLog.value = true
  try {
    const response = await api.post('/add_deadline_log/', {
      deadline_id: selectedDeadline.value.id,
      content: newLogContent.value.trim()
    })

    if (response.data.success) {
      showToast('Update added successfully.', true)
      newLogContent.value = ''
      await fetchData()
      const updatedDeadline = deadlines.value.find(t => t.id === selectedDeadline.value.id)
      if (updatedDeadline) {
        selectedDeadline.value = updatedDeadline
      }
    } else {
      showToast(response.data.error || 'Failed to add update.', false)
    }
  } catch (error) {
    console.error('Error:', error)
    showToast('An unexpected error occurred.', false)
  } finally {
    isSubmittingLog.value = false
  }
}

const toggleDeadlineStatus = async () => {
  if (!selectedDeadline.value) return

  try {
    const response = await api.post('/update_deadline_status/', {
      id: selectedDeadline.value.id,
      status: selectedDeadline.value.status === '0' ? '1' : '0'
    })

    if (response.data.success) {
      showToast('Deadline marked as completed! Reloading...', true)
      closeDeadlineDetails()
      setTimeout(() => {
        window.location.reload()
      }, 700)
    } else {
      showToast(response.data.error || 'Failed to update deadline status.', false)
    }
  } catch (error) {
    console.error('Error updating status:', error)
    showToast('Failed to connect to the server.', false)
  }
}

const openDeleteModal = (deadline) => {
  deadlineToDelete.value = deadline
}

const closeDeleteModal = () => {
  deadlineToDelete.value = null
}

const confirmDeleteDeadlineBtn = async () => {
  if (!deadlineToDelete.value) return
  deletingDeadlineId.value = deadlineToDelete.value.id

  try {
    const response = await api.post('/delete_deadline/', {
      id: deadlineToDelete.value.id
    })
    if (response.data.success) {
      // Remove deadline seamlessly from UI
      deadlines.value = deadlines.value.filter(t => t.id !== deadlineToDelete.value.id)
      deadlines_1_day.value = deadlines_1_day.value.filter(t => t.id !== deadlineToDelete.value.id)
      deadlines_3_day.value = deadlines_3_day.value.filter(t => t.id !== deadlineToDelete.value.id)
      deadlines_7_day.value = deadlines_7_day.value.filter(t => t.id !== deadlineToDelete.value.id)

      if (selectedDeadline.value && selectedDeadline.value.id === deadlineToDelete.value.id) {
        selectedDeadline.value = null
      }
      closeDeleteModal()
      showToast('Deadline deleted successfully.', true)
      // Refetch data passively to ensure stats are 100% correct if needed
      fetchData()
    } else {
      showToast(response.data.error || 'Failed to delete deadline.', false)
    }
  } catch (error) {
    console.error('Error:', error)
    showToast('An unexpected error occurred.', false)
  } finally {
    deletingDeadlineId.value = null
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

.overview-deadline-item {
  cursor: pointer;
}

.overview-deadline-item:hover {
  text-decoration: underline;
}

.more-logs-btn {
  cursor: pointer;
  color: #6c757d;
}

.more-logs-btn:hover {
  text-decoration: underline;
}

.cursor-pointer {
  cursor: pointer;
}
</style>


