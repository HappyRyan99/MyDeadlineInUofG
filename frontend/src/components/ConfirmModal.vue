<template>
  <div class="modal fade" :id="modalId" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h2 class="modal-title h5">{{ title }}</h2>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <p><slot name="message">{{ message }}</slot></p>
          <p class="text-danger small mb-0" v-if="warning">
            <BaseIcon name="exclamation-triangle" class="me-1" v-if="showWarningIcon" />
            <slot name="warning">{{ warning }}</slot>
          </p>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
          <button type="button" class="btn btn-danger" @click="$emit('confirm')">{{ confirmText }}</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ConfirmModal',
  props: {
    modalId: {
      type: String,
      required: true
    },
    title: {
      type: String,
      default: 'Confirm Deletion'
    },
    message: {
      type: String,
      default: 'Are you sure you want to proceed?'
    },
    warning: {
      type: String,
      default: 'This action cannot be undone.'
    },
    showWarningIcon: {
      type: Boolean,
      default: true
    },
    confirmText: {
      type: String,
      default: 'Delete'
    }
  },
  emits: ['confirm']
}
</script>
