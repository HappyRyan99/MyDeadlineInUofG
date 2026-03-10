<script setup>
import {ref, onMounted} from 'vue';
import {useRouter} from 'vue-router';
import api from '@/js/api';

const router = useRouter();
const emit = defineEmits(['update-student']);

// State
const student = ref(null);
const groups = ref([]);
const courses = ref([]);
const loading = ref(true);

// Forms State
const newGroup = ref({
  group_name: '',
  course_id: ''
});

const newMember = ref({
  group_id: null,
  student_id: '',
  student_name: ''
});

const showAddGroupModal = ref(false);
const showAddMemberModal = ref(false);

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
      emit('update-student', student.value);
      groups.value = response.data.data.groups;
      courses.value = response.data.data.courses;
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

const handleAddGroup = async () => {
  try {
    const response = await api.post('/api/add_group/', newGroup.value);
    if (response.data.success) {
      showAddGroupModal.value = false;
      newGroup.value = {group_name: '', course_id: ''};
      await fetchData();
    } else {
      alert('Error: ' + response.data.error);
    }
  } catch (error) {
    console.error('Failed to add group:', error);
    alert('Failed to add group');
  }
};

const openAddMemberModal = (groupId) => {
  newMember.value.group_id = groupId;
  showAddMemberModal.value = true;
};

const handleAddMember = async () => {
  try {
    const response = await api.post('/api/add_group_member/', newMember.value);
    if (response.data.success) {
      showAddMemberModal.value = false;
      newMember.value = {group_id: null, student_id: '', student_name: ''};
      await fetchData();
    } else {
      alert('Error: ' + response.data.error);
    }
  } catch (error) {
    console.error('Failed to add member:', error);
    alert('Failed to add member');
  }
};


const deleteMember = async (member) => {
  if (!confirm(`Are you sure you want to remove ${member.name} from this group?`)) {
    return
  }

  try {
    const response = await api.post('/api/delete_group_member/', {
      member_id: member.id
    })

    if (response.data.success) {
      await fetchData() // Refresh list
    } else {
      alert(response.data.error || 'Failed to remove member.')
    }
  } catch (error) {
    console.error('Error:', error)
    alert('An unexpected error occurred.')
  }
}
const deleteGroup = async (groupId) => {
  if (!confirm('Are you sure you want to delete this entire group? All members and associated deadlines will be removed.')) {
    return
  }

  try {
    const response = await api.post('/api/delete_group/', {
      group_id: groupId
    })

    if (response.data.success) {
      await fetchData() // Refresh list
    } else {
      alert(response.data.error || 'Failed to delete group.')
    }
  } catch (error) {
    console.error('Error:', error)
    alert('An unexpected error occurred.')
  }
}
</script>

<template>
    <!-- ===== MAIN CONTENT ===== -->
    <div class="content-container flex-grow-1 overflow-auto w-100">

      <!-- Page Title & Actions -->
      <div class="d-flex justify-content-between align-items-center mb-4 mt-4">
        <h3 class="text-primary mb-0"><i class="bi bi-people-fill me-2"></i>My Group</h3>
        <button @click="showAddGroupModal = true" class="btn btn-primary">
          <i class="bi bi-plus-lg me-1"></i>Create New Group
        </button>
      </div>

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
            <div
                class="card-header bg-white border-bottom-0 pt-3 pb-0 d-flex justify-content-between align-items-start">
              <h5 class="card-title text-primary fw-bold mb-0">
                {{ group.group_name }}
              </h5>
              <button v-if="group.is_creator" @click="openAddMemberModal(group.id)"
                      class="btn btn-outline-primary btn-sm rounded-pill" title="Add Member">
                <i class="bi bi-person-plus"></i>
              </button>
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
                  <li v-for="(member, index) in group.members" :key="index"
                      class="text-secondary d-flex justify-content-between align-items-center mb-1">
                    <span>
                      <i class="bi bi-person-fill me-2 text-muted"></i>
                      {{ member.name }}
                      <span class="text-muted ms-1" style="font-size: 0.65rem;">({{ member.student_id }})</span>
                    </span>
                    <button v-if="group.is_creator" @click="deleteMember(member)"
                            class="btn btn-sm btn-link text-danger p-0 ms-2" title="Remove Member">
                      <i class="bi bi-x-lg" style="font-size: 0.8rem;"></i>
                    </button>
                  </li>
                  <li v-if="group.members.length === 0" class="text-muted fst-italic">
                    No members assigned
                  </li>
                </ul>
              </div>
            </div>

            <div class="card-footer bg-light border-0 d-flex justify-content-between align-items-center py-2">
              <small class="text-muted" style="font-size: 0.75rem;">
                Created by {{ group.creator_name }}
              </small>
              <button v-if="group.is_creator" @click="deleteGroup(group.id)" class="btn btn-sm btn-link text-danger p-0"
                      title="Delete Group">
                <i class="bi bi-trash me-1"></i>
              </button>
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

    <!-- ===== MODALS ===== -->

    <!-- Add Group Modal -->
    <div v-if="showAddGroupModal" class="modal fade show d-block" style="background: rgba(0,0,0,0.5)">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content border-0 shadow-lg">
          <div class="modal-header bg-primary text-white border-0">
            <h5 class="modal-title"><i class="bi bi-people-fill me-2"></i>Create New Group</h5>
            <button type="button" class="btn-close btn-close-white" @click="showAddGroupModal = false"></button>
          </div>
          <div class="modal-body p-4">
            <form @submit.prevent="handleAddGroup">
              <div class="mb-3">
                <label class="form-label fw-bold">Group Name</label>
                <input v-model="newGroup.group_name" type="text" class="form-control" placeholder="Enter group name"
                       required>
              </div>
              <div class="mb-3">
                <label class="form-label fw-bold">Associated Course</label>
                <select v-model="newGroup.course_id" class="form-select">
                  <option value="">None</option>
                  <option v-for="course in courses" :key="course.id" :value="course.id">
                    {{ course.course_code }} - {{ course.name }}
                  </option>
                </select>
              </div>
              <div class="mt-4 d-grid">
                <button type="submit" class="btn btn-primary">Create Group</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>

    <!-- Add Member Modal -->
    <div v-if="showAddMemberModal" class="modal fade show d-block" style="background: rgba(0,0,0,0.5)">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content border-0 shadow-lg">
          <div class="modal-header bg-success text-white border-0">
            <h5 class="modal-title"><i class="bi bi-person-plus-fill me-2"></i>Add Group Member</h5>
            <button type="button" class="btn-close btn-close-white" @click="showAddMemberModal = false"></button>
          </div>
          <div class="modal-body p-4">
            <form @submit.prevent="handleAddMember">
              <div class="mb-3">
                <label class="form-label fw-bold">Student ID</label>
                <input v-model="newMember.student_id" type="text" class="form-control" placeholder="Max 10 characters"
                       maxlength="10" required>
              </div>
              <div class="mb-3">
                <label class="form-label fw-bold">Student Name</label>
                <input v-model="newMember.student_name" type="text" class="form-control" placeholder="Max 50 characters"
                       maxlength="50" required>
              </div>
              <div class="mt-4 d-grid">
                <button type="submit" class="btn btn-success">Add Member</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
</template>

<style scoped>
.content-container {
  max-width: 1080px;
  margin: 0 auto;
  padding: 0 20px;
  width: 100%;
}
</style>