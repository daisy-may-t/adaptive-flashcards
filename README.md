# Adaptive Flashcards

A flashcard learning application with confidence tracking and adaptive filtering, featuring a Vue 3 frontend and FastAPI backend.

**Note:** This project was developed with the assistance of AI tools (Claude) to accelerate development.

## Tech Stack
- **Backend:** Python 3.13, FastAPI, SQLAlchemy
- **Database:** SQLite locally (PostgreSQL-compatible schema)
- **Frontend:** Vue 3, Vite, Axios
- **Testing:** pytest (backend), Vitest (frontend)

## Quick Start

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Backend runs on `http://127.0.0.1:8000`

**API Documentation:** `http://127.0.0.1:8000/docs`

### Frontend
```bash
cd frontend
npm install
npm run dev
```
Frontend runs on `http://localhost:5173`

### Run Tests
```bash
# Backend
cd backend
pytest -v

# Frontend
cd frontend
npm run test
```

## How It Works

**Learn Mode** (`mode=learn`): Shows new cards or cards with confidence < 70%  
**Recap Mode** (`mode=recap`): Shows cards with confidence ≥ 70%

**Current Confidence Calculation:**
```python
# First review
confidence = user_rating / 10  # 0-10 scale converted to 0-1

# Subsequent reviews (weighted average)
new_confidence = (0.7 × old_confidence) + (0.3 × new_rating / 10)
```

## Project Structure
```
adaptive-flashcards/
├── backend/
│   ├── app/
│   │   ├── models/      # SQLAlchemy ORM models
│   │   ├── schemas/     # Pydantic request/response models
│   │   ├── routers/     # API endpoints
│   │   ├── config.py    # Configuration constants
│   │   └── main.py      # FastAPI application
│   └── tests/           # pytest unit tests
├── frontend/
│   ├── src/
│   │   ├── components/  # Vue components
│   │   ├── services/    # API service layer
│   │   └── App.vue      # Root component
│   └── tests/           # Vitest component tests
└── README.md
```

## API Examples
```bash
# Create user
curl -X POST "http://127.0.0.1:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{"username": "alice", "email": "alice@example.com"}'

# Create deck
curl -X POST "http://127.0.0.1:8000/decks/" \
  -H "Content-Type: application/json" \
  -d '{"title": "Spanish Basics", "owner_id": 1}'

# Add card
curl -X POST "http://127.0.0.1:8000/decks/1/cards" \
  -H "Content-Type: application/json" \
  -d '{"question": "Hello in Spanish?", "answer": "Hola"}'

# Get cards to learn
curl "http://127.0.0.1:8000/users/1/cards?mode=learn&deck_id=1"

# Record review
curl -X POST "http://127.0.0.1:8000/reviews" \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "card_id": 1, "confidence": 0.8}'
```

## Future Enhancements

- **Update and Delete** - Ability to edit and delete cards and decks
- **Spaced Repetition** - Schedule cards based on confidence and time, e.g.,
  - Low confidence: daily review
  - Medium confidence: weekly review
  - High confidence: monthly review
- **User Authentication** - JWT-based auth with protected endpoints
- **Progress Analytics** - Charts and statistics
- **Rich Card Content** - Markdown, images, code blocks
- **Bulk Card Generation** - Easy way to add many cards at once, e.g.,
  - Deck Import/Export - Share decks as JSON
  - AI-Generated Cards - Create flashcards from notes/documents/articles/exam boards
- **Mobile App** - Native iOS/Android
- **Collaborative Decks** - Have public and private decks with the ability to share and fork public decks
- **Offline Support** - Ability to download decks for offline use
