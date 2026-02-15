<template>
  <div class="mode-toggle">
    <div class="label-with-info">
      <label class="label">Learning Mode</label>
      <div class="info-icon-wrapper">
        <svg class="info-icon" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd" />
        </svg>
        <div class="tooltip">
          <strong>Learn:</strong> New cards and ones you're still mastering (confidence below 70%)
          <br><br>
          <strong>Recap:</strong> Cards you know well - review to keep them fresh (confidence 70% or higher)
        </div>
      </div>
    </div>
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

.label-with-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}

.label {
  font-size: 0.875rem;
  font-weight: 500;
  color: #374151;
}

.info-icon-wrapper {
  position: relative;
  display: inline-flex;
  align-items: center;
}

.info-icon {
  width: 1.125rem;
  height: 1.125rem;
  color: #6b7280;
  cursor: help;
  transition: color 0.2s;
  flex-shrink: 0;
}

.info-icon:hover {
  color: #4f46e5;
}

.info-icon-wrapper:hover .tooltip {
  opacity: 1;
  visibility: visible;
}

.tooltip {
  position: absolute;
  left: 1.5rem;
  top: 50%;
  transform: translateY(-50%);
  background-color: #1f2937;
  color: white;
  padding: 0.75rem;
  border-radius: 0.5rem;
  font-size: 0.8125rem;
  line-height: 1.5;
  width: 280px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  opacity: 0;
  visibility: hidden;
  transition: opacity 0.2s, visibility 0.2s;
  z-index: 1000;
  pointer-events: none;
}

.tooltip strong {
  color: #a5b4fc;
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
