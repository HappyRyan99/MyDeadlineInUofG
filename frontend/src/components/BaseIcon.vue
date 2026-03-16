<template>
  <svg
    xmlns="http://www.w3.org/2000/svg"
    :width="size"
    :height="size"
    fill="currentColor"
    class="base-icon"
    viewBox="0 0 16 16"
    aria-hidden="true"
  >
    <path
      v-for="(path, index) in paths"
      :key="index"
      :d="path"
    />
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

const paths = computed(() => {
  const iconPaths = icons[props.name];
  if (!iconPaths) {
    console.warn(`Icon "${props.name}" not found in icons.js`);
    return [];
  }
  return Array.isArray(iconPaths) ? iconPaths : [iconPaths];
});
</script>

<style scoped>
.base-icon {
  display: inline-block;
  vertical-align: -0.125em;
  flex-shrink: 0;
}
</style>
