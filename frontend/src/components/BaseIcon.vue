<template>
  <svg
    xmlns="http://www.w3.org/2000/svg"
    fill="currentColor"
    class="base-icon"
    :style="iconStyle"
    viewBox="0 0 16 16"
    aria-hidden="true"
    v-html="iconContent"
  >
  </svg>
</template>

<script setup>
import { computed } from 'vue';
import { icons } from '@/assets/icons';

const props = defineProps({
  name: {
    type: String,
    required: true
  },
  size: {
    type: [String, Number],
    default: 16
  }
});

const iconContent = computed(() => {
  const content = icons[props.name];
  if (!content) {
    console.warn(`Icon "${props.name}" not found in icons.js`);
    return '';
  }
  return content;
});

const iconStyle = computed(() => ({
  width: `${props.size}px`,
  height: `${props.size}px`
}));
</script>

<style scoped>
.base-icon {
  display: inline-block;
  vertical-align: middle;
  flex-shrink: 0;
  position: relative;
  top: -1px; /* Subtle adjustment for optical alignment with text */
}
</style>
