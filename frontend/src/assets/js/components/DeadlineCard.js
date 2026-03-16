import { computed } from 'vue'
import { formatTimeAgo, getDeadlineColorClass } from '@/utils/deadlineUtils'

export default {
  name: 'DeadlineCard',
  props: {
    deadline: {
      type: Object,
      required: true
    }
  },
  emits: ['show-details', 'delete-deadline'],
  setup(props) {
    const isCompleted = computed(() => props.deadline.status === '1')
    const deadlineColor = computed(() => getDeadlineColorClass(props.deadline))
    const timeAgo = computed(() => formatTimeAgo(props.deadline.update_time))

    return {
      isCompleted,
      deadlineColor,
      timeAgo
    }
  }
}
