<script src="../assets/js/views/GroupsView.js"></script>

<template>
  <!-- ===== MAIN CONTENT ===== -->
  <div class="flex-grow-1 w-100 overflow-y-auto">
    <div class="view-container">

      <!-- Page Title & Actions -->
      <div class="view-header">
        <h1 class="h3 text-primary mb-0"><BaseIcon name="people-fill" class="me-2" />My Group</h1>
        <button @click="addGroupModalInstance?.show()" class="btn btn-primary">
          <BaseIcon name="plus-lg" class="me-1" />Create New Group
        </button>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="loading-state">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>

      <!-- Groups Grid -->
      <div v-else class="group-grid row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">

        <!-- Group Cards -->
        <div class="col" v-for="group in groups" :key="group.id">
          <div class="group-card card shadow-sm">
            <div class="group-header card-header bg-white">
              <h2 class="group-title h5 text-primary fw-bold mb-0">
                {{ group.group_name }}
              </h2>
              <button v-if="group.is_creator" @click="openAddMemberModal(group.id)"
                      class="btn btn-outline-primary btn-sm btn-circle-sm" title="Add Member">
                <BaseIcon name="person-plus" />
              </button>
            </div>

            <div class="group-body card-body">
              <h3 class="card-subtitle h6 mb-2 text-muted fw-bold">
                {{ group.course_code }}
              </h3>

              <p class="card-text text-secondary mb-3 small">
                {{ group.course_name }}
              </p>

              <div class="member-section border-top pt-2">
                <small class="member-label text-uppercase text-secondary fw-bold">
                  Members
                </small>

                <ul class="member-list list-unstyled mt-2 mb-0">
                  <li v-for="(member, index) in group.members" :key="index" class="member-item text-secondary">
                      <span class="member-info">
                        <BaseIcon name="person-fill" class="me-2 text-muted" />
                        {{ member.name }}
                        <span class="member-id text-muted">({{ member.student_id }})</span>
                      </span>
                    <button v-if="group.is_creator" @click="deleteMember(member)"
                            class="btn btn-delete-member" title="Remove Member">
                      <BaseIcon name="x-lg" />
                    </button>
                  </li>
                  <li v-if="group.members.length === 0" class="empty-members text-muted fst-italic">
                    No members assigned
                  </li>
                </ul>
              </div>
            </div>

            <div class="group-footer card-footer d-flex justify-content-between align-items-center">
              <small class="creator-info text-muted">
                Created by {{ group.creator_name }}
              </small>
              <button v-if="group.is_creator" @click="deleteGroup(group.id)" class="btn btn-delete-group"
                      title="Delete Group">
                <BaseIcon name="trash" class="me-1" />
              </button>
            </div>
          </div>
        </div>

        <!-- Empty State -->
        <div v-if="groups.length === 0" class="col-12 empty-state">
          <div class="text-muted opacity-50">
            <BaseIcon name="people" size="80" class="opacity-50" />
            <p class="mt-3 fs-5">You are not in any groups.</p>
          </div>
        </div>

      </div> <!-- End Groups Grid -->

      <!-- Back Button -->
      <div class="mt-4 mb-4">
        <router-link to="/dashboard" class="btn btn-secondary">
          <BaseIcon name="arrow-left" class="me-1" />Back to Dashboard
        </router-link>
      </div>

    </div> <!-- End view-container -->
  </div> <!-- End Outer Scrollable Container -->

  <!-- ===== MODALS ===== -->

  <!-- Add Group Modal -->
  <div class="modal fade" id="addGroupModal" tabindex="-1" aria-hidden="true" data-bs-backdrop="static">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h2 class="modal-title h5">Create New Group</h2>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="handleAddGroup">
            <div class="mb-3">
              <label for="groupName" class="form-label">Group Name</label>
              <input type="text" v-model="newGroup.group_name" class="form-control" id="groupName"
                     placeholder="Enter group name"
                     required>
            </div>
            <div class="mb-3">
              <label for="courseId" class="form-label">Associated Course</label>
              <select v-model="newGroup.course_id" class="form-select" id="courseId">
                <option value="">None</option>
                <option v-for="course in courses" :key="course.id" :value="course.id">
                  {{ course.course_code }} - {{ course.name }}
                </option>
              </select>
            </div>
          </form>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
          <button type="button" class="btn btn-primary" @click="handleAddGroup">Create Group</button>
        </div>
      </div>
    </div>
  </div>

  <!-- Add Member Modal -->
  <div class="modal fade" id="addMemberModal" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h2 class="modal-title h5">Add Group Member</h2>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="handleAddMember">
            <div class="mb-3">
              <label for="studentId" class="form-label">Student ID</label>
              <input type="text" v-model="newMember.student_id" class="form-control" id="studentId"
                     placeholder="Max 10 characters"
                     maxlength="10" required>
            </div>
            <div class="mb-3">
              <label for="studentName" class="form-label">Student Name</label>
              <input type="text" v-model="newMember.student_name" class="form-control" id="studentName"
                     placeholder="Max 50 characters"
                     maxlength="50" required>
            </div>
          </form>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
          <button type="button" class="btn btn-primary" @click="handleAddMember">Add Member</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped src="../assets/css/views/GroupsView.css"></style>