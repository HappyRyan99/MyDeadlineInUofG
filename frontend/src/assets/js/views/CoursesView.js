import { ref, onMounted } from 'vue';
import api from '@/js/api';
import * as bootstrap from 'bootstrap';
import ConfirmModal from '@/components/ConfirmModal.vue';

export default {
  name: 'CoursesView',
  components: {
    ConfirmModal
  },
  emits: ['update-student'],
  setup(props, { emit }) {
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
          emit('update-student', student.value);
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
        const response = await api.post('/add_course/', newCourse.value)
        
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

    return {
      student,
      courses,
      loading,
      addCourseError,
      newCourse,
      editCourseData,
      courseToDelete,
      toastContent,
      showToast,
      fetchData,
      openAddCourseModal,
      handleAddCourse,
      openEditModal,
      handleEditCourse,
      confirmDeleteModal,
      handleDeleteCourse
    };
  }
}
