<template>
  <div
    class="flashcard"
    @click="toggleFlip"
    :class="{ flipped: isFlipped }"
  >
    <div class="flashcard-inner">
      <!-- Front (Question) -->
      <div class="flashcard-face flashcard-front">
        <div class="card-label">Question</div>
        <p class="card-text">{{ question }}</p>
        <p class="card-hint">Click to reveal answer</p>
      </div>

      <!-- Back (Answer) -->
      <div class="flashcard-face flashcard-back">
        <div class="card-label">Answer</div>
        <p class="card-text answer">{{ answer }}</p>
        <p class="card-hint">Click to hide answer</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Flashcard',
  props: {
    question: {
      type: String,
      required: true,
    },
    answer: {
      type: String,
      required: true,
    },
    flipped: {
      type: Boolean,
      default: false,
    },
  },
  emits: ['update:flipped'],
  data() {
    return {
      isFlipped: this.flipped,
    };
  },
  watch: {
    flipped(newValue) {
      this.isFlipped = newValue;
    },
  },
  methods: {
    toggleFlip() {
      this.isFlipped = !this.isFlipped;
      this.$emit('update:flipped', this.isFlipped);
    },
  },
};
</script>

<style scoped>
.flashcard {
  perspective: 1000px;
  cursor: pointer;
  min-height: 300px;
  width: 100%;
}

.flashcard-inner {
  position: relative;
  width: 100%;
  height: 100%;
  min-height: 300px;
  transition: transform 0.6s;
  transform-style: preserve-3d;
}

.flashcard.flipped .flashcard-inner {
  transform: rotateY(180deg);
}

.flashcard-face {
  position: absolute;
  width: 100%;
  height: 100%;
  min-height: 300px;
  backface-visibility: hidden;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  background: white;
  border-radius: 0.75rem;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.2s;
}

.flashcard:hover .flashcard-face {
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.15);
}

.flashcard-back {
  transform: rotateY(180deg);
}

.card-label {
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #6b7280;
  margin-bottom: 1rem;
}

.card-text {
  font-size: 1.5rem;
  font-weight: 500;
  color: #1f2937;
  text-align: center;
  margin: 0;
}

.card-text.answer {
  color: #10b981;
}

.card-hint {
  font-size: 0.875rem;
  color: #4f46e5;
  margin-top: 1.5rem;
}

.flashcard-back .card-hint {
  color: #6b7280;
}
</style>
