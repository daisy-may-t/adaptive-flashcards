<template>
  <div class="deck-selector">
    <label for="deck-select" class="label">Select Deck</label>
    <select
      id="deck-select"
      v-model="selectedDeckId"
      @change="handleChange"
      class="select"
    >
      <option value="">Choose a deck...</option>
      <option v-for="deck in decks" :key="deck.id" :value="deck.id">
        {{ deck.title }}
      </option>
    </select>
  </div>
</template>

<script>
export default {
  name: 'DeckSelector',
  props: {
    decks: {
      type: Array,
      required: true,
    },
    modelValue: {
      type: [String, Number],
      default: '',
    },
  },
  emits: ['update:modelValue'],
  data() {
    return {
      selectedDeckId: this.modelValue,
    };
  },
  watch: {
    modelValue(newValue) {
      this.selectedDeckId = newValue;
    },
  },
  methods: {
    handleChange() {
      this.$emit('update:modelValue', this.selectedDeckId);
    },
  },
};
</script>

<style scoped>
.deck-selector {
  width: 100%;
}

.label {
  display: block;
  font-size: 0.875rem;
  font-weight: 500;
  color: #374151;
  margin-bottom: 0.5rem;
}

.select {
  width: 100%;
  padding: 0.5rem 1rem;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  font-size: 1rem;
  background-color: white;
  cursor: pointer;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.select:focus {
  outline: none;
  border-color: #4f46e5;
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
}

.select:hover {
  border-color: #9ca3af;
}
</style>
