<template>
  <div class="mode-toggle">
    <label class="label">Learning Mode</label>
    <div class="button-group">
      <button
        @click="selectMode('learn')"
        :class="['mode-button', { active: modelValue === 'learn', learn: true }]"
      >
        📚 Learn
      </button>
      <button
        @click="selectMode('recap')"
        :class="['mode-button', { active: modelValue === 'recap', recap: true }]"
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

.button-group {
  display: flex;
  gap: 0.5rem;
}

.mode-button {
  flex: 1;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 0.5rem;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  background-color: #e5e7eb;
  color: #374151;
}

.mode-button:hover {
  opacity: 0.9;
  transform: translateY(-1px);
}

.mode-button.active.learn {
  background-color: #4f46e5;
  color: white;
}

.mode-button.active.recap {
  background-color: #10b981;
  color: white;
}

.mode-button:focus {
  outline: none;
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.2);
}
</style>
