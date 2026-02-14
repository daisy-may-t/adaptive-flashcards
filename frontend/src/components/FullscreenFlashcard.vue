<template>
  <div v-if="isVisible" class="fullscreen-overlay" @click="handleOverlayClick">
    <div class="fullscreen-container">
      <!-- Close Button -->
      <button @click="close" class="close-button" aria-label="Exit fullscreen">
        ✕
      </button>

      <!-- Progress Indicator -->
      <div class="fullscreen-progress">
        <span class="progress-text">{{ currentIndex + 1 }} / {{ total }}</span>
        <div class="progress-bar-track">
          <div
            class="progress-bar-fill"
            :style="{ width: progressPercentage + '%' }"
          ></div>
        </div>
      </div>

      <!-- Flashcard -->
      <div
        class="fullscreen-card"
        @click.stop="toggleFlip"
        :class="{ flipped: isFlipped }"
      >
        <div class="fullscreen-card-inner">
          <!-- Front (Question) -->
          <div class="fullscreen-card-face fullscreen-card-front">
            <div class="card-label">Question</div>
            <p class="card-content">{{ question }}</p>
            <p class="card-hint">Tap to reveal answer</p>
          </div>

          <!-- Back (Answer) -->
          <div class="fullscreen-card-face fullscreen-card-back">
            <div class="card-label">Answer</div>
            <p class="card-content answer">{{ answer }}</p>
            <p class="card-hint">Tap to hide answer</p>
          </div>
        </div>
      </div>

      <!-- Confidence Controls (when flipped) -->
      <div v-if="isFlipped" class="fullscreen-controls">
        <div class="confidence-label">How confident? ({{ confidence }}/10)</div>
        <div class="slider-wrapper">
          <input
            type="range"
            v-model.number="confidence"
            min="0"
            max="10"
            step="1"
            class="fullscreen-slider"
            @click.stop
          />
          <div class="slider-ticks">
            <span v-for="i in 11" :key="i" class="tick"></span>
          </div>
        </div>
        <div class="slider-labels">
          <span>Not confident</span>
          <span>Very confident</span>
        </div>
        <button @click.stop="submitAndNext" class="submit-button">
          {{ isLastCard ? 'Finish' : 'Next Card' }}
        </button>
      </div>

      <!-- Navigation Hint -->
      <div v-if="!isFlipped" class="navigation-hint">
        Press ESC to exit fullscreen
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'FullscreenFlashcard',
  props: {
    isVisible: {
      type: Boolean,
      required: true,
    },
    question: {
      type: String,
      required: true,
    },
    answer: {
      type: String,
      required: true,
    },
    currentIndex: {
      type: Number,
      required: true,
    },
    total: {
      type: Number,
      required: true,
    },
  },
  emits: ['close', 'submit'],
  data() {
    return {
      isFlipped: false,
      confidence: 5,
    };
  },
  computed: {
    progressPercentage() {
      if (this.total === 0) return 0;
      return ((this.currentIndex + 1) / this.total) * 100;
    },
    isLastCard() {
      return this.currentIndex >= this.total - 1;
    },
  },
  watch: {
    isVisible(newValue) {
      if (newValue) {
        this.resetCard();
        this.addKeyboardListener();
        this.lockOrientation();
      } else {
        this.removeKeyboardListener();
        this.unlockOrientation();
      }
    },
    currentIndex() {
      this.resetCard();
    },
  },
  methods: {
    toggleFlip() {
      this.isFlipped = !this.isFlipped;
    },

    submitAndNext() {
      const confidenceScore = this.confidence / 10;
      this.$emit('submit', confidenceScore);
      this.resetCard();
    },

    resetCard() {
      this.isFlipped = false;
      this.confidence = 5;
    },

    close() {
      this.$emit('close');
    },

    handleOverlayClick(event) {
      // Close if clicking the overlay background (not the card)
      if (event.target === event.currentTarget) {
        this.close();
      }
    },

    handleKeydown(event) {
      if (event.key === 'Escape') {
        this.close();
      } else if (event.key === ' ' || event.key === 'Enter') {
        event.preventDefault();
        this.toggleFlip();
      }
    },

    addKeyboardListener() {
      document.addEventListener('keydown', this.handleKeydown);
    },

    removeKeyboardListener() {
      document.removeEventListener('keydown', this.handleKeydown);
    },

    async lockOrientation() {
      // Try to lock to landscape on mobile devices
      if (screen.orientation && screen.orientation.lock) {
        try {
          await screen.orientation.lock('landscape');
        } catch (error) {
          // Orientation lock not supported or denied
          console.log('Orientation lock not available');
        }
      }
    },

    unlockOrientation() {
      if (screen.orientation && screen.orientation.unlock) {
        screen.orientation.unlock();
      }
    },
  },
  beforeUnmount() {
    this.removeKeyboardListener();
    this.unlockOrientation();
  },
};
</script>

<style scoped>
.fullscreen-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.95);
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
}

.fullscreen-container {
  position: relative;
  width: 100%;
  max-width: 800px;
  height: 100%;
  display: flex;
  flex-direction: column;
  padding-top: 4rem;
  padding-bottom: 2rem;
}

/* Close Button */
.close-button {
  position: absolute;
  top: 1rem;
  right: 1rem;
  width: 2.5rem;
  height: 2.5rem;
  background-color: rgba(255, 255, 255, 0.1);
  color: white;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  font-size: 1.5rem;
  cursor: pointer;
  transition: all 0.2s;
  z-index: 10;
}

.close-button:hover {
  background-color: rgba(255, 255, 255, 0.2);
  transform: scale(1.1);
}

/* Progress */
.fullscreen-progress {
  position: absolute;
  top: 1rem;
  left: 1rem;
  right: 5rem;
  color: white;
  z-index: 5;
}

.progress-text {
  font-size: 0.875rem;
  font-weight: 500;
  margin-bottom: 0.5rem;
  display: block;
}

.progress-bar-track {
  height: 0.25rem;
  background-color: rgba(255, 255, 255, 0.2);
  border-radius: 9999px;
  overflow: hidden;
}

.progress-bar-fill {
  height: 100%;
  background-color: #4f46e5;
  border-radius: 9999px;
  transition: width 0.3s ease;
}

/* Flashcard */
.fullscreen-card {
  perspective: 1000px;
  cursor: pointer;
  width: 100%;
  flex: 1;
  max-height: 450px;
  min-height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.fullscreen-card-inner {
  position: relative;
  width: 100%;
  height: 100%;
  transition: transform 0.6s;
  transform-style: preserve-3d;
}

.fullscreen-card.flipped .fullscreen-card-inner {
  transform: rotateY(180deg);
}

.fullscreen-card-face {
  position: absolute;
  width: 100%;
  height: 100%;
  backface-visibility: hidden;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem;
  background: white;
  border-radius: 1rem;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
}

.fullscreen-card-back {
  transform: rotateY(180deg);
}

.card-label {
  font-size: 0.875rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: #6b7280;
  margin-bottom: 2rem;
}

.card-content {
  font-size: 2rem;
  font-weight: 600;
  color: #1f2937;
  text-align: center;
  margin: 0;
  line-height: 1.4;
}

.card-content.answer {
  color: #10b981;
}

.card-hint {
  font-size: 1rem;
  color: #9ca3af;
  margin-top: 2rem;
}

/* Controls */
.fullscreen-controls {
  margin-top: 2rem;
  width: 100%;
  max-width: 400px;
  padding: 1.5rem;
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: 0.75rem;
  backdrop-filter: blur(10px);
  align-self: center;
}

.confidence-label {
  color: white;
  font-weight: 500;
  margin-bottom: 1rem;
  text-align: center;
}

.slider-wrapper {
  position: relative;
  width: 100%;
  margin-bottom: 0.5rem;
}

.fullscreen-slider {
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
  padding: 0 0.125rem;
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

.fullscreen-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 1.5rem;
  height: 1.5rem;
  border-radius: 50%;
  background: white;
  border: 3px solid #4f46e5;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
  position: relative;
  z-index: 20;
}

.fullscreen-slider::-moz-range-thumb {
  width: 1.5rem;
  height: 1.5rem;
  border-radius: 50%;
  background: white;
  border: 3px solid #4f46e5;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
  position: relative;
  z-index: 20;
}

.slider-labels {
  display: flex;
  justify-content: space-between;
  font-size: 0.75rem;
  color: rgba(255, 255, 255, 0.7);
  margin-bottom: 1rem;
}

.submit-button {
  width: 100%;
  padding: 0.75rem;
  background-color: #4f46e5;
  color: white;
  border: none;
  border-radius: 0.5rem;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.submit-button:hover {
  background-color: #4338ca;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(79, 70, 229, 0.4);
}

/* Navigation Hint */
.navigation-hint {
  position: absolute;
  bottom: 1rem;
  color: rgba(255, 255, 255, 0.5);
  font-size: 0.875rem;
}

/* Mobile Landscape Optimization */
@media (max-width: 768px) and (orientation: landscape) {
  .fullscreen-container {
    max-height: 100vh;
  }

  .fullscreen-card {
    max-height: 60vh;
  }

  .card-content {
    font-size: 1.5rem;
  }

  .fullscreen-controls {
    padding: 1rem;
    margin-top: 1rem;
  }
}

/* Mobile Portrait */
@media (max-width: 768px) and (orientation: portrait) {
  .card-content {
    font-size: 1.5rem;
  }

  .fullscreen-card-face {
    padding: 2rem;
  }
}
</style>
