<template>
  <div class="mode-toggle">
    <label class="label">Learning Mode</label>
    <div class="tab-group">
      <button
        @click="selectMode('learn')"
        :class="['tab', { active: modelValue === 'learn' }]"
      >
        📚 Learn
      </button>
      <button
        @click="selectMode('recap')"
        :class="['tab', { active: modelValue === 'recap' }]"
      >
        ✅ Recap
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ModeToggle',
  props: {
    modelValue: {
      type: String,
      required: true,
      validator: (value) => ['learn', 'recap'].includes(value),
    },
  },
  emits: ['update:modelValue'],
  methods: {
    selectMode(mode) {
      this.$emit('update:modelValue', mode);
    },
  },
};
</script>

<style scoped>
.mode-toggle {
  width: 100%;
}

.label {
  display: block;
  font-size: 0.875rem;
  font-weight: 500;
  color: #374151;
  margin-bottom: 0.5rem;
}

.tab-group {
  display: inline-flex;
  background-color: #f3f4f6;
  border-radius: 0.5rem;
  padding: 0.25rem;
  gap: 0.25rem;
}

.tab {
  flex: 1;
  padding: 0.5rem 1.5rem;
  border: none;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  background-color: transparent;
  color: #6b7280;
  white-space: nowrap;
}

.tab:hover:not(.active) {
  color: #374151;
  background-color: rgba(255, 255, 255, 0.5);
}

.tab.active {
  background-color: white;
  color: #4f46e5;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.tab:focus {
  outline: none;
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
}
</style>
