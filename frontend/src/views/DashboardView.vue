<script src="../assets/js/views/DashboardView.js"></script>

<template>
  <!-- Middle Section -->
  <div class="flex-grow-1 overflow-y-auto w-100">
    <div class="view-container">
      <template v-if="student">
        <!-- Student Info Card -->
        <div class="student-info-card card mb-4 shadow-sm">
          <div class="card-header bg-primary text-white">
            <h5 class="mb-0 d-flex align-items-center"><BaseIcon name="person-circle" class="me-2" />Student Information</h5>
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
        <div class="overview-card card mb-4 shadow-sm">
          <div class="card-body">
            <div class="overview-header d-flex justify-content-between align-items-center mb-3">
              <h5 class="card-title text-primary mb-0 d-flex align-items-center"><BaseIcon name="calendar3" class="me-2" />Deadline Overview</h5>
              <button class="btn btn-sm btn-primary" @click="openAddDeadlineModal"><BaseIcon name="plus-lg" class="me-1" />Add
                Deadline
              </button>
            </div>

            <!-- Real-time Clock Display -->
            <div class="clock-container d-flex justify-content-center mb-4">
              <div class="clock-display">
                <BaseIcon name="clock-fill" class="text-primary me-2" />{{ currentTime }}
              </div>
            </div>

            <div class="row text-center">
              <div v-for="(section, index) in overviewSections" :key="index" :class="['col-4', section.borderClass]">
                <h5 class="fw-bold mb-3" :class="section.colorClass">{{ section.title }}</h5>
                <ul v-if="section.deadlines.length > 0" class="overview-list list-unstyled mb-0 text-start"
                    :class="section.colorClass">
                  <li v-for="deadline in section.deadlines" :key="deadline.id"
                      class="text-truncate ps-3 overview-item"
                      @click="showDeadlineDetails(deadline)">
                    <BaseIcon name="dot" />{{ deadline.deadline_title }}
                  </li>
                </ul>
                <span v-else class="text-muted fst-italic">No deadlines</span>
              </div>
            </div>
          </div>
        </div>

        <h3 class="deadline-section-title mb-3 border-bottom pb-2 d-flex align-items-center">
          <BaseIcon name="card-checklist" class="me-2 text-primary" />Upcoming Deadlines
        </h3>
        <div class="deadline-grid row row-cols-1 row-cols-md-3 g-4">
          <div v-for="deadline in active_deadlines" :key="deadline.id" class="col">
            <DeadlineCard :deadline="deadline" @show-details="showDeadlineDetails"
                          @delete-deadline="openDeleteModal"/>
          </div>

          <div class="col" v-if="active_deadlines.length === 0">
            <!-- Add New (Empty State) -->
            <div class="empty-deadline-action" @click="openAddDeadlineModal">
              <div class="text-center">
                <BaseIcon name="plus-lg" size="48" class="mb-2 text-secondary opacity-75" />
                <div class="fw-medium">Add Deadline</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Completed Deadlines Section -->
        <template v-if="completed_deadlines.length > 0">
          <h3 class="deadline-section-title completed-title mb-3 border-bottom pb-2 mt-5 text-success d-flex align-items-center">
            <BaseIcon name="check2-circle" class="me-2" />Completed Deadlines
          </h3>
          <div class="deadline-grid completed-grid row row-cols-1 row-cols-md-3 g-4 opacity-75">
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
       data-bs-backdrop="static" aria-hidden="true" ref="addDeadlineModalEl">
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
            <div class="mb-3">
              <label for="deadlineContent" class="form-label">Content</label>
              <textarea class="form-control" :class="{ 'is-invalid': formErrors.content }" id="deadlineContent"
                        rows="3" v-model="newDeadline.content" required
                        aria-describedby="deadlineContentFeedback"></textarea>
              <div id="deadlineContentFeedback" class="invalid-feedback">
                Please provide a description or content.
              </div>
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
  <div class="modal fade" id="deadlineDetailsModal" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered modal-lg modal-dialog-scrollable">
      <div class="modal-content border-0 shadow-lg rounded-4 bg-white bg-opacity-90 blur-backdrop"
           v-if="selectedDeadline">
        <div class="modal-header border-bottom-0 pb-0 align-items-start">
          <h3 class="modal-title fw-bold text-dark h4 mb-0 text-break pe-3 w-100 d-flex align-items-center"
              :class="{'text-danger': selectedDeadline.status === '0' && selectedDeadline.is_past_due}">
            <BaseIcon v-if="selectedDeadline.status === '1'" name="check-circle-fill" class="text-success me-2" />
            <span v-if="selectedDeadline.status === '0' && selectedDeadline.is_past_due">[Overdue] </span>

            <!-- Title Edit Mode -->
            <div v-if="editingField === 'title'" class="d-flex w-100 align-items-center">
              <input type="text" class="form-control me-2" v-model="editTitleValue"
                     @keyup.enter="saveDeadlineEdit('title')" @keyup.esc="cancelDeadlineEdit" autofocus>
              <button class="btn btn-sm btn-success me-1 px-2" @click="saveDeadlineEdit('title')"><BaseIcon
                  name="check-lg" /></button>
              <button class="btn btn-sm btn-secondary px-2" @click="cancelDeadlineEdit"><BaseIcon name="x-lg" />
              </button>
            </div>
            <!-- Title Display Mode -->
            <div v-else class="d-flex align-items-center">
              <span>{{ selectedDeadline.deadline_title }}</span>
              <button v-if="selectedDeadline.can_edit" class="btn btn-sm btn-link text-secondary p-0 ms-2"
                      @click="startDeadlineEdit('title')" title="Edit Title">
                <BaseIcon name="pencil" />
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
                <BaseIcon name="pencil" />
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
                  <small class="text-muted"><BaseIcon name="clock" class="me-1" />{{ log.create_time }}</small>
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
              <BaseIcon name="check2-all" class="me-1" />Completed
            </div>
          </div>
          <div v-else-if="selectedDeadline" class="d-flex align-items-center">
              <span v-if="selectedDeadline.status === '1'" class="text-success fw-bold"><i
                  name="check2-all" class="me-1" />Completed</span>
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
          <BaseIcon name="exclamation-circle" size="48" class="text-danger" />
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
</template>

<style scoped src="../assets/css/views/DashboardView.css"></style>
