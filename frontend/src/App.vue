<template>
  <div id="app">
    <!-- Header -->
    <header class="header">
      <div class="container">
        <h1 class="title">Adaptive Flashcards</h1>
        <p class="subtitle">Learn smarter, not harder</p>
        
        <!-- Navigation Tabs -->
        <div class="nav-tabs">
          <button
            @click="currentView = 'learn'"
            :class="['nav-tab', { active: currentView === 'learn' }]"
          >
            📚 Learn
          </button>
          <button
            @click="currentView = 'admin'"
            :class="['nav-tab', { active: currentView === 'admin' }]"
          >
            ⚙️ Admin
          </button>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="main">
      <div class="container">
        <!-- Learn View -->
        <div v-if="currentView === 'learn'">
        <!-- Controls -->
        <div class="controls-card">
          <div class="controls-grid">
            <DeckSelector v-model="selectedDeckId" :decks="decks" />
            <ModeToggle v-model="mode" />
          </div>
        </div>

        <!-- Loading State -->
        <div v-if="loading" class="state-card">
          <div class="loader"></div>
          <p class="state-text">Loading cards...</p>
        </div>

        <!-- Error State -->
        <div v-else-if="error" class="state-card error">
          <div class="error-icon">⚠️</div>
          <p class="state-text">{{ error }}</p>
          <button @click="retryLoad" class="retry-button">Retry</button>
        </div>

        <!-- No Deck Selected -->
        <div v-else-if="!selectedDeckId" class="state-card">
          <div class="state-icon">👆</div>
          <p class="state-text">Select a deck to get started</p>
        </div>

        <!-- No Cards -->
        <div v-else-if="cards.length === 0" class="state-card">
          <div class="state-icon">🎉</div>
          <p class="state-text">
            {{ mode === 'learn' ? 'No cards to learn!' : 'No cards to recap!' }}
          </p>
          <p class="state-subtext">
            {{ mode === 'learn' 
              ? 'Try switching to Recap mode to review what you know.' 
              : 'Try switching to Learn mode to practice new material.' 
            }}
          </p>
        </div>

        <!-- Card Display -->
        <div v-else class="card-section">
          <!-- Progress Bar -->
          <div class="progress-card">
            <ProgressBar :current-index="currentCardIndex" :total="cards.length" />
          </div>

          <!-- Flashcard -->
          <Flashcard
            :question="currentCard.card.question"
            :answer="currentCard.card.answer"
            v-model:flipped="flipped"
          />

          <!-- Confidence Slider (shown when flipped) -->
          <div v-if="flipped" class="confidence-card">
            <ConfidenceSlider
              v-model="confidence"
              :disabled="submitting"
              :button-text="submitting ? 'Submitting...' : 'Submit Review & Next Card'"
              @submit="handleSubmitReview"
            />
          </div>

          <!-- Progress Info -->
          <div v-if="currentCard.progress" class="info-card">
            <p class="info-text">
              <strong>Previous confidence:</strong> 
              {{ (currentCard.progress.confidence_score * 10).toFixed(1) }}/10
            </p>
            <p class="info-text">
              <strong>Times reviewed:</strong> 
              {{ currentCard.progress.review_count }}
            </p>
          </div>
        </div>
        </div>

        <!-- Admin View -->
        <AdminPanel v-else @deck-created="loadDecks" />
      </div>
    </main>
  </div>
</template>

<script>
import DeckSelector from './components/DeckSelector.vue';
import ModeToggle from './components/ModeToggle.vue';
import ProgressBar from './components/ProgressBar.vue';
import Flashcard from './components/Flashcard.vue';
import ConfidenceSlider from './components/ConfidenceSlider.vue';
import AdminPanel from './components/AdminPanel.vue';
import api from './services/api.js';

export default {
  name: 'App',
  components: {
    DeckSelector,
    ModeToggle,
    ProgressBar,
    Flashcard,
    ConfidenceSlider,
    AdminPanel,
  },
  data() {
    return {
      currentView: 'learn',
      decks: [],
      selectedDeckId: '',
      mode: 'learn',
      cards: [],
      currentCardIndex: 0,
      flipped: false,
      confidence: 5,
      loading: false,
      submitting: false,
      error: null,
    };
  },
  computed: {
    currentCard() {
      return this.cards[this.currentCardIndex] || null;
    },
  },
  watch: {
    selectedDeckId() {
      this.loadCards();
      this.updatePageTitle();
    },
    mode() {
      this.loadCards();
      this.updatePageTitle();
    },
    currentView(newView) {
      if (newView === 'learn') {
        this.loadDecks();
      }
    },
  },
  async mounted() {
    await this.loadDecks();
  },
  methods: {
    async loadDecks() {
      try {
        this.decks = await api.getDecks();
        this.updatePageTitle();
      } catch (error) {
        console.error('Error loading decks:', error);
        this.error = 'Failed to load decks. Make sure the backend is running.';
      }
    },

    async loadCards() {
      if (!this.selectedDeckId) return;

      this.loading = true;
      this.error = null;
      this.currentCardIndex = 0;
      this.flipped = false;

      try {
        this.cards = await api.getCards(this.mode, this.selectedDeckId);
      } catch (error) {
        console.error('Error loading cards:', error);
        this.error = 'Failed to load cards. Please try again.';
      } finally {
        this.loading = false;
      }
    },

    async handleSubmitReview() {
      this.submitting = true;

      try {
        // Convert 0-10 scale to 0-1 for backend
        const confidenceScore = this.confidence / 10;

        await api.submitReview(this.currentCard.card.id, confidenceScore);

        // Move to next card or reload if finished
        if (this.currentCardIndex < this.cards.length - 1) {
          this.currentCardIndex++;
          this.flipped = false;
          this.confidence = 5; // Reset to middle
        } else {
          // Finished all cards, reload to see updated filtering
          await this.loadCards();
        }
      } catch (error) {
        console.error('Error submitting review:', error);
        this.error = 'Failed to submit review. Please try again.';
      } finally {
        this.submitting = false;
      }
    },

    retryLoad() {
      this.error = null;
      if (this.selectedDeckId) {
        this.loadCards();
      } else {
        this.loadDecks();
      }
    },

    updatePageTitle() {
      if (!this.selectedDeckId) {
        document.title = 'Adaptive Flashcards';
        return;
      }
      
      const deck = this.decks.find(d => d.id === this.selectedDeckId);
      if (deck) {
        const modeText = this.mode === 'learn' ? 'Learn' : 'Recap';
        document.title = `${deck.title} - ${modeText} | Adaptive Flashcards`;
      }
    },
  },
};
</script>

<style>
/* Global Styles */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  background-color: #f3f4f6;
  min-height: 100vh;
}

#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* Header */
.header {
  background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
  color: white;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.container {
  max-width: 56rem;
  margin: 0 auto;
  padding: 0 1.5rem;
}

.header .container {
  padding-top: 1.5rem;
  padding-bottom: 1.5rem;
}

.title {
  font-size: 1.875rem;
  font-weight: 700;
  margin-bottom: 0.25rem;
}

.subtitle {
  color: rgba(255, 255, 255, 0.9);
  font-size: 0.875rem;
}

/* Navigation Tabs */
.nav-tabs {
  display: flex;
  gap: 0.5rem;
  margin-top: 1rem;
}

.nav-tab {
  padding: 0.5rem 1.5rem;
  background-color: rgba(255, 255, 255, 0.2);
  color: white;
  border: none;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.nav-tab:hover {
  background-color: rgba(255, 255, 255, 0.3);
}

.nav-tab.active {
  background-color: white;
  color: #4f46e5;
}

/* Main Content */
.main {
  flex: 1;
  padding: 2rem 0;
}

/* Cards */
.controls-card,
.state-card,
.progress-card,
.confidence-card,
.info-card {
  background: white;
  border-radius: 0.75rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  padding: 1.5rem;
  margin-bottom: 1.5rem;
}

.controls-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
}

@media (min-width: 768px) {
  .controls-grid {
    grid-template-columns: 1fr 1fr;
  }
}

/* State Cards */
.state-card {
  text-align: center;
  padding: 3rem 1.5rem;
}

.state-card.error {
  background-color: #fef2f2;
  border: 1px solid #fecaca;
}

.state-icon,
.error-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.state-text {
  font-size: 1.125rem;
  font-weight: 500;
  color: #374151;
  margin-bottom: 0.5rem;
}

.state-subtext {
  color: #6b7280;
  font-size: 0.875rem;
}

.loader {
  display: inline-block;
  width: 3rem;
  height: 3rem;
  border: 4px solid #e5e7eb;
  border-top-color: #4f46e5;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.retry-button {
  margin-top: 1rem;
  padding: 0.5rem 1.5rem;
  background-color: #4f46e5;
  color: white;
  border: none;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
}

.retry-button:hover {
  background-color: #4338ca;
}

/* Card Section */
.card-section {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* Info Card */
.info-card {
  background-color: #f9fafb;
  border: 1px solid #e5e7eb;
}

.info-text {
  font-size: 0.875rem;
  color: #6b7280;
  margin-bottom: 0.5rem;
}

.info-text:last-child {
  margin-bottom: 0;
}
</style>
