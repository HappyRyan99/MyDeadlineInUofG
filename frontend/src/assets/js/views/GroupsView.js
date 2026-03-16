import { ref, onMounted } from 'vue';
import api from '@/js/api';
import * as bootstrap from 'bootstrap';

export default {
  name: 'GroupsView',
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

    // Lifecycle Hooks
    let addGroupModalInstance = null;
    let addMemberModalInstance = null;

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
      fetchData();
    });

    const handleAddGroup = async () => {
      try {
        const response = await api.post('/api/add_group/', newGroup.value);
        if (response.data.success) {
          addGroupModalInstance?.hide();
          newGroup.value = { group_name: '', course_id: '' };
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
      addMemberModalInstance?.show();
    };

    const handleAddMember = async () => {
      try {
        const response = await api.post('/api/add_group_member/', newMember.value);
        if (response.data.success) {
          addMemberModalInstance?.hide();
          newMember.value = { group_id: null, student_id: '', student_name: '' };
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
        return;
      }

      try {
        const response = await api.post('/api/delete_group_member/', {
          member_id: member.id
        });

        if (response.data.success) {
          await fetchData();
        } else {
          alert(response.data.error || 'Failed to remove member.');
        }
      } catch (error) {
        console.error('Error:', error);
        alert('An unexpected error occurred.');
      }
    };

    const deleteGroup = async (groupId) => {
      if (!confirm('Are you sure you want to delete this entire group? All members and associated deadlines will be removed.')) {
        return;
      }

      try {
        const response = await api.post('/api/delete_group/', {
          group_id: groupId
        });

        if (response.data.success) {
          await fetchData();
        } else {
          alert(response.data.error || 'Failed to delete group.');
        }
      } catch (error) {
        console.error('Error:', error);
        alert('An unexpected error occurred.');
      }
    };

    return {
      student,
      groups,
      courses,
      loading,
      newGroup,
      newMember,
      addGroupModalInstance,
      addMemberModalInstance,
      fetchData,
      handleAddGroup,
      openAddMemberModal,
      handleAddMember,
      deleteMember,
      deleteGroup
    };
  }
}
