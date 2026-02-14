# Adaptive Flashcards

A flashcard learning API with confidence tracking and adaptive filtering (learn vs. recap modes).

## Tech Stack
- Backend: Python (FastAPI)
- Database: PostgreSQL (SQLite locally)
- Frontend: Minimal
- Tooling: Git, pytest

## Quick Start
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Visit `http://127.0.0.1:8000/docs` for interactive API documentation.

## Example Usage
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

## How It Works

**Learn Mode** (`mode=learn`): Shows new cards or cards with confidence < 0.7  
**Recap Mode** (`mode=recap`): Shows cards with confidence ≥ 0.7

Confidence updates use weighted average: `new = 0.7 × old + 0.3 × review`

## Project Structure
```
backend/
├── app/
│   ├── models/      # SQLAlchemy ORM
│   ├── schemas/     # Pydantic models
│   ├── routers/     # API endpoints
│   ├── config.py    # Constants
│   └── main.py      # FastAPI app
└── tests/           # pytest tests
```

## Run Tests
```bash
cd backend
pytest -v
```

## Future Ideas
- Spaced repetition (SM-2 algorithm)
- AI-generated flashcards
- Progress analytics
- Cloud deployment

## Scope
This project focuses on core backend architecture and API design. Additional concerns such as authentication, advanced scheduling, and deployment are considered out of scope for the initial version.

## Future Improvements
- Spaced repetition algorithms
- AI-assisted flashcard generation from user notes or learning materials
- User authentication
- Frontend learning interface
- GCP deployment
