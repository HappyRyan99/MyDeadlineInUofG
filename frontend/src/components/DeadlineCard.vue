<script src="../assets/js/components/DeadlineCard.js"></script>

<template>
  <div class="deadline-card card shadow-sm" 
       :class="{'border-success': isCompleted}" 
       @click="$emit('show-details', deadline)">
    <div class="card-body d-flex flex-column">
      <div class="d-flex justify-content-between align-items-start mb-2">
        <h3 class="card-title h5 mb-0 text-truncate" :title="deadline.deadline_title"
            :class="[isCompleted ? 'text-success' : (deadline.is_past_due ? 'text-danger fw-bold' : '')]">
          <BaseIcon v-if="isCompleted" name="check-circle-fill" class="me-1" />
          <span v-else-if="deadline.is_past_due">[Overdue] </span>
          {{ deadline.deadline_title }}
        </h3>
        <span v-if="deadline.group" class="badge bg-success text-white rounded-pill text-truncate"
              style="max-width: 100px;">Group&nbsp;Work</span>
        <span v-else class="badge bg-primary text-white rounded-pill">Personal</span>
      </div>
      <div v-if="deadline.group" style="font-size: 12px;" class="text-end">{{ deadline.group.course_name }}</div>
      <div class="flex-fill mt-2">
        <p style="min-height: 80px;max-height: 100px;overflow: hidden;" 
           :class="{'text-muted': isCompleted}">{{ deadline.content }}</p>
      </div>
      <div class="mt-auto">
        <p v-if="isCompleted" class="card-text fw-bold mb-0 text-success">
          <BaseIcon name="calendar-check" class="me-1" />Completed
        </p>
        <p v-else :class="['card-text fw-bold mb-0', deadlineColor]">
          <BaseIcon name="calendar-event" class="me-1" />
          {{ deadline.deadline }}
        </p>
      </div>
    </div>
    <div class="card-footer bg-white text-muted small d-flex justify-content-between align-items-center">
      <div><BaseIcon name="clock" class="me-1" />Updated: {{ timeAgo }}</div>
      <button v-if="deadline.is_creator" class="btn btn-sm btn-link text-danger p-0" @click.stop="$emit('delete-deadline', deadline)"
              title="Delete Deadline">
        <BaseIcon name="trash" />
      </button>
    </div>
  </div>
</template>

<style scoped src="../assets/css/components/DeadlineCard.css"></style>
