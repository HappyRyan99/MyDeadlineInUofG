import api from '@/js/api'
import * as bootstrap from 'bootstrap'
import DeadlineCard from '@/components/DeadlineCard.vue'
import { getDeadlineColorClass, formatGroupOption } from '@/utils/deadlineUtils'
import { ref, computed, onMounted, onUnmounted } from 'vue'

export default {
  name: 'DashboardView',
  components: {
    DeadlineCard
  },
  emits: ['update-student'],
  setup(props, { emit }) {
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
      { title: 'Within 1 Day', deadlines: deadlines_1_day.value, colorClass: 'text-danger', borderClass: 'border-end' },
      { title: 'Within 3 Days', deadlines: deadlines_3_day.value, colorClass: 'text-orange', borderClass: 'border-end' },
      { title: 'Within 7 Days', deadlines: deadlines_7_day.value, colorClass: 'text-warning', borderClass: '' }
    ])

    const toastTitle = ref('Notification')
    const toastMessage = ref('Msg')
    const toastClass = ref('text-success')

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
    const editingField = ref(null)
    const editTitleValue = ref('')
    const editContentValue = ref('')

    const toastEl = ref(null)
    const addDeadlineModalEl = ref(null)
    const deadlineDetailsModalEl = ref(null)

    let bootstrapToast = null
    let bootstrapAddDeadlineModal = null
    let bootstrapDeadlineDetailsModal = null

    const showToast = (message, isSuccess = true) => {
      toastTitle.value = isSuccess ? 'Success' : 'Error'
      toastMessage.value = message
      toastClass.value = isSuccess ? 'text-success' : 'text-danger'
      if (bootstrapToast) {
        bootstrapToast.show()
      }
    }

    const fetchData = async () => {
      // 1. Fetch Meta Data (Instant)
      try {
        const metaResponse = await api.get('/api/dashboard_meta/')
        if (metaResponse.data.success) {
          const data = metaResponse.data.data
          student.value = data.student
          emit('update-student', student.value)
          groups.value = data.groups
        }
      } catch (error) {
        if (error.response && error.response.status === 401) {
          window.location.href = '/login/'
          return
        }
        console.error('Error fetching meta:', error)
      }

      // 2. Fetch Deadlines Data (Optimized)
      try {
        const deadlinesResponse = await api.get('/api/dashboard_deadlines/')
        if (deadlinesResponse.data.success) {
          const data = deadlinesResponse.data.data
          deadlines.value = data.deadlines
          active_deadlines.value = data.deadlines.filter(t => t.status === '0')
          completed_deadlines.value = data.deadlines.filter(t => t.status === '1')

          // Classification logic (can be handled by backend stats or calculated here)
          deadlines_1_day.value = active_deadlines.value.filter(t => t.hours_until >= 0 && t.hours_until <= 24)
          deadlines_3_day.value = active_deadlines.value.filter(t => t.hours_until > 24 && t.hours_until <= 72)
          deadlines_7_day.value = active_deadlines.value.filter(t => t.hours_until > 72 && t.hours_until <= 168)
        } else {
          showToast(deadlinesResponse.data.error || 'Failed to load deadlines', false)
        }
      } catch (error) {
        console.error('Error fetching deadlines:', error)
        showToast('Error fetching deadlines', false)
      }
    }

    const initBootstrapComponents = () => {
      if (toastEl.value) bootstrapToast = new bootstrap.Toast(toastEl.value)
      if (addDeadlineModalEl.value) bootstrapAddDeadlineModal = new bootstrap.Modal(addDeadlineModalEl.value)

      const detailsModalNode = document.getElementById('deadlineDetailsModal');
      if (detailsModalNode) {
        bootstrapDeadlineDetailsModal = new bootstrap.Modal(detailsModalNode);
        detailsModalNode.addEventListener('hidden.bs.modal', () => {
          selectedDeadline.value = null;
          newLogContent.value = '';
          editingField.value = null;
        });
      }
    }

    onMounted(() => {
      updateTime()
      timerInterval = setInterval(updateTime, 1000)
      fetchData()
      initBootstrapComponents()
    })

    onUnmounted(() => {
      if (timerInterval) clearInterval(timerInterval)
    })

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

      if (hasError) return

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
      bootstrapDeadlineDetailsModal?.show();
    }

    const closeDeadlineDetails = () => {
      bootstrapDeadlineDetailsModal?.hide();
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

      let payload = { deadline_id: selectedDeadline.value.id }

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
          deadlines.value = deadlines.value.filter(t => t.id !== deadlineToDelete.value.id)
          deadlines_1_day.value = deadlines_1_day.value.filter(t => t.id !== deadlineToDelete.value.id)
          deadlines_3_day.value = deadlines_3_day.value.filter(t => t.id !== deadlineToDelete.value.id)
          deadlines_7_day.value = deadlines_7_day.value.filter(t => t.id !== deadlineToDelete.value.id)

          if (selectedDeadline.value && selectedDeadline.value.id === deadlineToDelete.value.id) {
            selectedDeadline.value = null
          }
          closeDeleteModal()
          showToast('Deadline deleted successfully.', true)
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

    return {
      currentTime,
      student,
      deadlines_1_day,
      deadlines_3_day,
      deadlines_7_day,
      deadlines,
      active_deadlines,
      completed_deadlines,
      groups,
      overviewSections,
      toastTitle,
      toastMessage,
      toastClass,
      newDeadline,
      formErrors,
      deadlineToDelete,
      selectedDeadline,
      newLogContent,
      isSubmittingLog,
      deletingDeadlineId,
      editingField,
      editTitleValue,
      editContentValue,
      toastEl,
      addDeadlineModalEl,
      deadlineDetailsModalEl,
      showToast,
      fetchData,
      openAddDeadlineModal,
      closeAddDeadlineModal,
      submitDeadline,
      showDeadlineDetails,
      closeDeadlineDetails,
      startDeadlineEdit,
      cancelDeadlineEdit,
      saveDeadlineEdit,
      showMoreLogsToast,
      submitDeadlineLog,
      toggleDeadlineStatus,
      openDeleteModal,
      closeDeleteModal,
      confirmDeleteDeadlineBtn,
      getDeadlineColorClass,
      formatGroupOption
    }
  }
}
