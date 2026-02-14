<template>
  <div class="confidence-slider">
    <label class="label">
      How confident are you? ({{ modelValue }}/10)
    </label>

    <div class="slider-container">
      <input
        type="range"
        v-model.number="localValue"
        @input="handleInput"
        min="0"
        max="10"
        step="1"
        class="slider"
      />
      <div class="slider-ticks">
        <span v-for="i in 11" :key="i" class="tick"></span>
      </div>
    </div>

    <div class="scale-labels">
      <span class="scale-label">0 - Not confident</span>
      <span class="scale-label">5 - Somewhat</span>
      <span class="scale-label">10 - Very confident</span>
    </div>

    <button
      @click="handleSubmit"
      :disabled="disabled"
      class="submit-button"
      :class="{ disabled }"
    >
      {{ buttonText }}
    </button>
  </div>
</template>

<script>
export default {
  name: 'ConfidenceSlider',
  props: {
    modelValue: {
      type: Number,
      default: 5,
      validator: (value) => value >= 0 && value <= 10,
    },
    disabled: {
      type: Boolean,
      default: false,
    },
    buttonText: {
      type: String,
      default: 'Submit Review & Next Card',
    },
  },
  emits: ['update:modelValue', 'submit'],
  data() {
    return {
      localValue: this.modelValue,
    };
  },
  watch: {
    modelValue(newValue) {
      this.localValue = newValue;
    },
  },
  methods: {
    handleInput() {
      this.$emit('update:modelValue', this.localValue);
    },
    handleSubmit() {
      if (!this.disabled) {
        this.$emit('submit', this.localValue);
      }
    },
  },
};
</script>

<style scoped>
.confidence-slider {
  width: 100%;
}

.label {
  display: block;
  font-size: 0.875rem;
  font-weight: 500;
  color: #374151;
  margin-bottom: 0.75rem;
}

.slider-container {
  position: relative;
  width: 100%;
  margin-bottom: 0.5rem;
}

.slider {
  position: relative;
  width: 100%;
  height: 0.75rem;
  border-radius: 0.5rem;
  background: linear-gradient(to right, #ef4444, #f59e0b, #10b981);
  outline: none;
  cursor: pointer;
  -webkit-appearance: none;
  appearance: none;
}

.slider-ticks {
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  transform: translateY(-50%);
  display: flex;
  justify-content: space-between;
  padding: 0 0.75rem;
  pointer-events: none;
  z-index: 10;
}

.tick {
  width: 0.5rem;
  height: 0.5rem;
  background-color: rgba(255, 255, 255, 0.9);
  border: 1px solid rgba(0, 0, 0, 0.2);
  border-radius: 50%;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
}

.slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 1.5rem;
  height: 1.5rem;
  border-radius: 50%;
  background: white;
  border: 3px solid #4f46e5;
  cursor: pointer;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
  transition: transform 0.2s;
  position: relative;
  z-index: 20;
}

.slider::-webkit-slider-thumb:hover {
  transform: scale(1.1);
}

.slider::-moz-range-thumb {
  width: 1.5rem;
  height: 1.5rem;
  border-radius: 50%;
  background: white;
  border: 3px solid #4f46e5;
  cursor: pointer;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
  transition: transform 0.2s;
  position: relative;
  z-index: 20;
}

.slider::-moz-range-thumb:hover {
  transform: scale(1.1);
}

.scale-labels {
  display: flex;
  justify-content: space-between;
  margin-top: 0.5rem;
  margin-bottom: 1rem;
}

.scale-label {
  font-size: 0.75rem;
  color: #6b7280;
}

.submit-button {
  width: 100%;
  padding: 0.75rem 1.5rem;
  background-color: #4f46e5;
  color: white;
  border: none;
  border-radius: 0.5rem;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.submit-button:hover:not(.disabled) {
  background-color: #4338ca;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
}

.submit-button:active:not(.disabled) {
  transform: translateY(0);
}

.submit-button.disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.submit-button:focus {
  outline: none;
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.3);
}
</style>
