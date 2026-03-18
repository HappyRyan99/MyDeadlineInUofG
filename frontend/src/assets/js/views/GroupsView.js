import { ref, onMounted } from 'vue';
import api from '@/js/api';
import * as bootstrap from 'bootstrap';
import ConfirmModal from '@/components/ConfirmModal.vue';

export default {
  name: 'GroupsView',
  components: {
    ConfirmModal
  },
  emits: ['update-student'],
  setup(props, { emit }) {
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

    const formErrors = ref({ group_name: '', course_id: '' });
    const memberFormErrors = ref({ student_id: '', student_name: '' });

    const groupToDelete = ref(null);
    const memberToDelete = ref(null);

    // Lifecycle Hooks
    let addGroupModalInstance = null;
    let addMemberModalInstance = null;
    let toastInstance = null;
    let deleteGroupModalInstance = null;
    let deleteMemberModalInstance = null;

    const toastContent = ref({ title: '', message: '', isSuccess: true });

    const showToast = (message, isSuccess = true) => {
      toastContent.value.title = isSuccess ? 'Success' : 'Error';
      toastContent.value.message = message;
      toastContent.value.isSuccess = isSuccess;
      toastInstance?.show();
    };

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

    onMounted(() => {
      if (document.getElementById('addGroupModal')) {
        addGroupModalInstance = new bootstrap.Modal(document.getElementById('addGroupModal'));
      }
      if (document.getElementById('addMemberModal')) {
        addMemberModalInstance = new bootstrap.Modal(document.getElementById('addMemberModal'));
      }
      if (document.getElementById('deleteGroupModal')) {
        deleteGroupModalInstance = new bootstrap.Modal(document.getElementById('deleteGroupModal'));
      }
      if (document.getElementById('deleteMemberModal')) {
        deleteMemberModalInstance = new bootstrap.Modal(document.getElementById('deleteMemberModal'));
      }
      if (document.getElementById('liveToast')) {
        toastInstance = new bootstrap.Toast(document.getElementById('liveToast'));
      }
      fetchData();
    });

    const openAddGroupModal = () => {
      newGroup.value = { group_name: '', course_id: '' };
      formErrors.value = { group_name: '', course_id: '' };
      addGroupModalInstance?.show();
    };

    const handleAddGroup = async () => {
      formErrors.value = { group_name: '', course_id: '' };
      let hasError = false;

      if (!newGroup.value.group_name.trim()) {
        formErrors.value.group_name = 'Group Name cannot be empty.';
        hasError = true;
      }
      if (!newGroup.value.course_id) {
        formErrors.value.course_id = 'You must select an associated course.';
        hasError = true;
      }

      if (hasError) {
        if (formErrors.value.group_name) document.getElementById('groupName')?.focus();
        else if (formErrors.value.course_id) document.getElementById('courseId')?.focus();
        return;
      }

      try {
        const response = await api.post('/api/add_group/', newGroup.value);
        if (response.data.success) {
          addGroupModalInstance?.hide();
          showToast('Group created successfully.', true);
          await fetchData();
        } else {
          showToast(response.data.error || 'Failed to create group.', false);
        }
      } catch (error) {
        console.error('Failed to add group:', error);
        showToast('An unexpected error occurred.', false);
      }
    };

    const openAddMemberModal = (groupId) => {
      newMember.value.group_id = groupId;
      newMember.value.student_id = '';
      newMember.value.student_name = '';
      memberFormErrors.value = { student_id: '', student_name: '' };
      addMemberModalInstance?.show();
    };

    const handleAddMember = async () => {
      memberFormErrors.value = { student_id: '', student_name: '' };
      let hasError = false;

      if (!newMember.value.student_id.trim()) {
        memberFormErrors.value.student_id = 'Student ID cannot be empty.';
        hasError = true;
      }
      if (!newMember.value.student_name.trim()) {
        memberFormErrors.value.student_name = 'Student Name cannot be empty.';
        hasError = true;
      }

      if (hasError) {
        if (memberFormErrors.value.student_id) document.getElementById('studentId')?.focus();
        else if (memberFormErrors.value.student_name) document.getElementById('studentName')?.focus();
        return;
      }

      try {
        const response = await api.post('/api/add_group_member/', newMember.value);
        if (response.data.success) {
          addMemberModalInstance?.hide();
          showToast('Member added successfully.', true);
          newMember.value = { group_id: null, student_id: '', student_name: '' };
          await fetchData();
        } else {
          showToast(response.data.error || 'Failed to add member.', false);
        }
      } catch (error) {
        console.error('Failed to add member:', error);
        showToast('An unexpected error occurred.', false);
      }
    };

    const confirmDeleteMember = (member) => {
      memberToDelete.value = member;
      deleteMemberModalInstance?.show();
    };

    const confirmDeleteGroup = (group) => {
      groupToDelete.value = group;
      deleteGroupModalInstance?.show();
    };

    const deleteMember = async () => {
      if (!memberToDelete.value) return;

      try {
        const response = await api.post('/api/delete_group_member/', {
          member_id: memberToDelete.value.id
        });

        if (response.data.success) {
          deleteMemberModalInstance?.hide();
          showToast('Member removed successfully.', true);
          memberToDelete.value = null;
          await fetchData();
        } else {
          showToast(response.data.error || 'Failed to remove member.', false);
        }
      } catch (error) {
        console.error('Error:', error);
        showToast('An unexpected error occurred.', false);
      }
    };

    const deleteGroup = async () => {
      if (!groupToDelete.value) return;

      try {
        const response = await api.post('/api/delete_group/', {
          group_id: groupToDelete.value.id
        });

        if (response.data.success) {
          deleteGroupModalInstance?.hide();
          showToast('Group deleted successfully.', true);
          groupToDelete.value = null;
          await fetchData();
        } else {
          showToast(response.data.error || 'Failed to delete group.', false);
        }
      } catch (error) {
        console.error('Error:', error);
        showToast('An unexpected error occurred.', false);
      }
    };

    return {
      student,
      groups,
      courses,
      loading,
      newGroup,
      newMember,
      formErrors,
      memberFormErrors,
      groupToDelete,
      memberToDelete,
      toastContent,
      showToast,
      fetchData,
      openAddGroupModal,
      handleAddGroup,
      openAddMemberModal,
      handleAddMember,
      confirmDeleteMember,
      deleteMember,
      confirmDeleteGroup,
      deleteGroup
    };
  }
}
