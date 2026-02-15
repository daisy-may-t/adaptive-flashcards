<template>
  <div class="create-panel">
    <h2 class="section-title">Create Panel</h2>
    <p class="section-subtitle">Create and manage flashcard decks</p>

    <!-- Toast Notifications (Fixed Position) -->
    <transition name="toast">
      <div v-if="successMessage" class="toast toast-success">
        <span class="toast-icon">✓</span>
        <span class="toast-text">{{ successMessage }}</span>
      </div>
    </transition>
    <transition name="toast">
      <div v-if="errorMessage" class="toast toast-error">
        <span class="toast-icon">⚠</span>
        <span class="toast-text">{{ errorMessage }}</span>
      </div>
    </transition>

    <!-- Create Deck Section -->
    <div class="create-card">
      <h3 class="card-title">Create New Deck</h3>
      <form @submit.prevent="handleCreateDeck" class="form">
        <div class="form-group">
          <label for="deck-title" class="label">Deck Title *</label>
          <input
            id="deck-title"
            v-model="newDeck.title"
            type="text"
            required
            placeholder="e.g., Spanish Basics"
            class="input"
          />
        </div>

        <div class="form-group">
          <label for="deck-description" class="label">Description</label>
          <textarea
            id="deck-description"
            v-model="newDeck.description"
            rows="3"
            placeholder="Optional description of this deck"
            class="input textarea"
          ></textarea>
        </div>

        <button type="submit" :disabled="creating" class="button primary">
          {{ creating ? 'Creating...' : 'Create Deck' }}
        </button>
      </form>
    </div>

    <!-- Add Cards Section -->
    <div class="create-card">
      <h3 class="card-title">Add Cards to Deck</h3>
      
      <!-- Deck Selector -->
      <div class="form-group">
        <label for="target-deck" class="label">Select Deck *</label>
        <select
          id="target-deck"
          v-model="selectedDeckId"
          required
          class="input"
        >
          <option value="">Choose a deck...</option>
          <option v-for="deck in decks" :key="deck.id" :value="deck.id">
            {{ deck.title }}
          </option>
        </select>
      </div>

      <!-- Card Form -->
      <form v-if="selectedDeckId" @submit.prevent="handleAddCard" class="form">
        <div class="form-group">
          <label for="card-question" class="label">Question *</label>
          <textarea
            id="card-question"
            v-model="newCard.question"
            rows="2"
            required
            placeholder="e.g., What is 'hello' in Spanish?"
            class="input textarea"
          ></textarea>
        </div>

        <div class="form-group">
          <label for="card-answer" class="label">Answer *</label>
          <textarea
            id="card-answer"
            v-model="newCard.answer"
            rows="2"
            required
            placeholder="e.g., Hola"
            class="input textarea"
          ></textarea>
        </div>

        <button type="submit" :disabled="addingCard" class="button primary">
          {{ addingCard ? 'Adding...' : 'Add Card' }}
        </button>
      </form>

      <p v-else class="helper-text">Select a deck to start adding cards</p>
    </div>

    <!-- Existing Decks List -->
    <div class="create-card">
      <h3 class="card-title">Existing Decks</h3>
      <div v-if="decks.length === 0" class="empty-state">
        No decks created yet. Create your first deck above!
      </div>
      <div v-else class="decks-list">
        <div 
          v-for="deck in decks" 
          :key="deck.id" 
          class="deck-item"
          @click="goToDeck(deck.id)"
        >
          <div class="deck-info">
            <h4 class="deck-name">{{ deck.title }}</h4>
            <p v-if="deck.description" class="deck-description">
              {{ deck.description }}
            </p>
            <p class="deck-meta">
              Created: {{ formatDate(deck.created_at) }}
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../services/api.js';

export default {
  name: 'CreatePanel',
  emits: ['deck-created', 'navigate-to-deck'],
  data() {
    return {
      decks: [],
      selectedDeckId: '',
      newDeck: {
        title: '',
        description: '',
      },
      newCard: {
        question: '',
        answer: '',
      },
      creating: false,
      addingCard: false,
      successMessage: '',
      errorMessage: '',
    };
  },
  async mounted() {
    await this.loadDecks();
  },
  methods: {
    async loadDecks() {
      try {
        this.decks = await api.getDecks();
      } catch (error) {
        console.error('Error loading decks:', error);
        this.showError('Failed to load decks');
      }
    },

    async handleCreateDeck() {
      if (!this.newDeck.title.trim()) return;

      this.creating = true;
      this.clearMessages();

      try {
        const createdDeck = await api.createDeck(
          this.newDeck.title,
          this.newDeck.description
        );
        
        this.showSuccess(`Deck "${createdDeck.title}" created successfully!`);
        this.newDeck.title = '';
        this.newDeck.description = '';
        
        await this.loadDecks();
      } catch (error) {
        console.error('Error creating deck:', error);
        this.showError('Failed to create deck. Please try again.');
      } finally {
        this.creating = false;
      }
    },

    async handleAddCard() {
      if (!this.newCard.question.trim() || !this.newCard.answer.trim()) return;

      this.addingCard = true;
      this.clearMessages();

      try {
        await api.createCard(
          this.selectedDeckId,
          this.newCard.question,
          this.newCard.answer
        );
        
        this.showSuccess('Card added successfully!');
        this.newCard.question = '';
        this.newCard.answer = '';
      } catch (error) {
        console.error('Error adding card:', error);
        this.showError('Failed to add card. Please try again.');
      } finally {
        this.addingCard = false;
      }
    },

    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString();
    },

    showSuccess(message) {
      this.successMessage = message;
      this.errorMessage = '';
      setTimeout(() => {
        this.successMessage = '';
      }, 5000);
    },

    showError(message) {
      this.errorMessage = message;
      this.successMessage = '';
    },

    clearMessages() {
      this.successMessage = '';
      this.errorMessage = '';
    },

    goToDeck(deckId) {
      this.$emit('navigate-to-deck', deckId);
    },
  },
};
</script>

<style scoped>
.create-panel {
  max-width: 48rem;
  margin: 0 auto;
}

.section-title {
  font-size: 1.875rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 0.5rem;
}

.section-subtitle {
  color: #6b7280;
  margin-bottom: 2rem;
}

/* Toast Notifications */
.toast {
  position: fixed;
  top: 2rem;
  right: 2rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem 1.5rem;
  border-radius: 0.5rem;
  font-weight: 500;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
  z-index: 9999;
  min-width: 300px;
  max-width: 400px;
}

.toast-success {
  background-color: #10b981;
  color: white;
}

.toast-error {
  background-color: #ef4444;
  color: white;
}

.toast-icon {
  font-size: 1.25rem;
  font-weight: bold;
  flex-shrink: 0;
}

.toast-text {
  flex: 1;
}

/* Toast Animation */
.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s ease;
}

.toast-enter-from {
  opacity: 0;
  transform: translateX(100px);
}

.toast-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}

/* Create Cards */
.create-card {
  background: white;
  border-radius: 0.75rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  padding: 1.5rem;
  margin-bottom: 1.5rem;
}

.card-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 1.5rem;
}

/* Forms */
.form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.label {
  font-size: 0.875rem;
  font-weight: 500;
  color: #374151;
  margin-bottom: 0.5rem;
}

.input {
  padding: 0.5rem 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  font-size: 1rem;
  font-family: inherit;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.input:focus {
  outline: none;
  border-color: #4f46e5;
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
}

.input.textarea {
  resize: vertical;
}

.button {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 0.5rem;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.button.primary {
  background-color: #4f46e5;
  color: white;
}

.button.primary:hover:not(:disabled) {
  background-color: #4338ca;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
}

.button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.helper-text {
  color: #6b7280;
  font-size: 0.875rem;
  font-style: italic;
}

/* Decks List */
.empty-state {
  text-align: center;
  padding: 2rem;
  color: #6b7280;
}

.decks-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.deck-item {
  padding: 1rem;
  background-color: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 0.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  transition: all 0.2s;
}

.deck-item:hover {
  background-color: #f3f4f6;
  border-color: #4f46e5;
  transform: translateX(2px);
  box-shadow: 0 2px 8px rgba(79, 70, 229, 0.1);
}

.deck-info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  flex: 1;
}

.deck-arrow {
  color: #9ca3af;
  font-size: 1.25rem;
  transition: all 0.2s;
  margin-left: 1rem;
}

.deck-item:hover .deck-arrow {
  color: #4f46e5;
  transform: translateX(4px);
}

.deck-name {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1f2937;
}

.deck-description {
  color: #6b7280;
  font-size: 0.875rem;
}

.deck-meta {
  font-size: 0.75rem;
  color: #9ca3af;
  margin-top: 0.5rem;
}
</style>
