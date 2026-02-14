import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000';

// Hardcoded user ID for demo purposes
// In production, this would come from authentication
const DEMO_USER_ID = 1;

class FlashcardAPI {
  constructor(baseURL = API_BASE_URL) {
    this.client = axios.create({
      baseURL,
      headers: {
        'Content-Type': 'application/json',
      },
    });
  }

  /**
   * Fetch all decks
   * @returns {Promise<Array>} List of decks
   */
  async getDecks() {
    const response = await this.client.get('/decks/');
    return response.data;
  }

  /**
   * Fetch a specific deck by ID
   * @param {number} deckId - The deck ID
   * @returns {Promise<Object>} Deck object
   */
  async getDeck(deckId) {
    const response = await this.client.get(`/decks/${deckId}`);
    return response.data;
  }

  /**
   * Fetch cards for a user in a specific mode
   * @param {string} mode - 'learn' or 'recap'
   * @param {number} deckId - The deck ID
   * @returns {Promise<Array>} List of cards with progress
   */
  async getCards(mode, deckId) {
    const response = await this.client.get(`/users/${DEMO_USER_ID}/cards`, {
      params: { mode, deck_id: deckId },
    });
    return response.data;
  }

  /**
   * Submit a review for a card
   * @param {number} cardId - The card ID
   * @param {number} confidence - Confidence score (0-1 scale)
   * @returns {Promise<Object>} Updated progress object
   */
  async submitReview(cardId, confidence) {
    const response = await this.client.post('/reviews', {
      user_id: DEMO_USER_ID,
      card_id: cardId,
      confidence,
    });
    return response.data;
  }

  /**
   * Create a new user (for initial setup)
   * @param {string} username - Username
   * @param {string} email - Email address
   * @returns {Promise<Object>} Created user object
   */
  async createUser(username, email) {
    const response = await this.client.post('/users/', {
      username,
      email,
    });
    return response.data;
  }

  /**
   * Create a new deck
   * @param {string} title - Deck title
   * @param {string} description - Deck description
   * @returns {Promise<Object>} Created deck object
   */
  async createDeck(title, description = '') {
    const response = await this.client.post('/decks/', {
      title,
      description,
      owner_id: DEMO_USER_ID,
    });
    return response.data;
  }

  /**
   * Add a card to a deck
   * @param {number} deckId - The deck ID
   * @param {string} question - Card question
   * @param {string} answer - Card answer
   * @returns {Promise<Object>} Created card object
   */
  async createCard(deckId, question, answer) {
    const response = await this.client.post(`/decks/${deckId}/cards`, {
      question,
      answer,
    });
    return response.data;
  }
}

// Export a singleton instance
export default new FlashcardAPI();
