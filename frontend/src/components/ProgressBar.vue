<template>
  <div class="progress-container">
    <div class="progress-info">
      <span class="progress-text">
        Card {{ currentIndex + 1 }} of {{ total }}
      </span>
      <span class="remaining-text">
        {{ remaining }} remaining
      </span>
    </div>
    <div class="progress-bar-track">
      <div
        class="progress-bar-fill"
        :style="{ width: progressPercentage + '%' }"
      ></div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ProgressBar',
  props: {
    currentIndex: {
      type: Number,
      required: true,
    },
    total: {
      type: Number,
      required: true,
    },
  },
  computed: {
    progressPercentage() {
      if (this.total === 0) return 0;
      return ((this.currentIndex + 1) / this.total) * 100;
    },
    remaining() {
      return this.total - this.currentIndex - 1;
    },
  },
};
</script>

<style scoped>
.progress-container {
  width: 100%;
}

.progress-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.progress-text {
  font-weight: 500;
  color: #374151;
}

.remaining-text {
  font-size: 0.875rem;
  color: #6b7280;
}

.progress-bar-track {
  height: 0.5rem;
  background-color: #e5e7eb;
  border-radius: 9999px;
  overflow: hidden;
}

.progress-bar-fill {
  height: 100%;
  background-color: #4f46e5;
  border-radius: 9999px;
  transition: width 0.3s ease;
}
</style>
