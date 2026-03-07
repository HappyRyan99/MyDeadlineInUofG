<template>
  <div class="card shadow-sm h-100" 
       :class="{'border-success': isCompleted}" 
       style="cursor: pointer;" 
       @click="$emit('show-details', task)">
    <div class="card-body d-flex flex-column">
      <div class="d-flex justify-content-between align-items-start mb-2">
        <h5 class="card-title mb-0 text-truncate" :title="task.task_title"
            :class="[isCompleted ? 'text-success' : (task.is_past_due ? 'text-danger fw-bold' : '')]">
          <i v-if="isCompleted" class="bi bi-check-circle-fill me-1"></i>
          <span v-else-if="task.is_past_due">[Overdue] </span>
          {{ task.task_title }}
        </h5>
        <span v-if="task.group" class="badge bg-success text-white rounded-pill text-truncate"
              style="max-width: 100px;">Group&nbsp;Work</span>
        <span v-else class="badge bg-primary text-white rounded-pill">Personal</span>
      </div>
      <div v-if="task.group" style="font-size: 12px;" class="text-end">{{ task.group.course_name }}</div>
      <div class="flex-fill mt-2">
        <p style="min-height: 80px;max-height: 100px;overflow: hidden;" 
           :class="{'text-muted': isCompleted}">{{ task.content }}</p>
      </div>
      <p v-if="isCompleted" class="card-text fw-bold mb-auto text-success">
        <i class="bi bi-calendar-check me-1"></i>Completed
      </p>
      <p v-else :class="['card-text fw-bold mb-auto', deadlineColor]">
        <i class="bi bi-calendar-event me-1"></i>
        {{ task.deadline }}
      </p>
    </div>
    <div class="card-footer bg-white text-muted small d-flex justify-content-between align-items-center">
      <div><i class="bi bi-clock me-1"></i>Updated: {{ timeAgo }}</div>
      <button class="btn btn-sm btn-link text-danger p-0" @click.stop="$emit('delete-task', task)"
              title="Delete Task">
        <i class="bi bi-trash"></i>
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { formatTimeAgo, getDeadlineColorClass } from '@/utils/taskUtils'

const props = defineProps({
  task: {
    type: Object,
    required: true
  }
})

defineEmits(['show-details', 'delete-task'])

const isCompleted = computed(() => props.task.status === '1')
const deadlineColor = computed(() => getDeadlineColorClass(props.task))
const timeAgo = computed(() => formatTimeAgo(props.task.update_time))
</script>
