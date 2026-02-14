# Backend API

REST API for flashcard learning with adaptive card filtering.

## Endpoints

### Users
- `POST /users/` - Create user
- `GET /users/{user_id}` - Get user

### Decks
- `POST /decks/` - Create deck
- `GET /decks/` - List decks (filter by `owner_id`)
- `GET /decks/{deck_id}` - Get deck

### Cards
- `POST /decks/{deck_id}/cards` - Add card
- `GET /decks/{deck_id}/cards` - List cards

### Learning
- `GET /users/{user_id}/cards?mode=learn|recap&deck_id={deck_id}` - Get filtered cards
- `POST /reviews` - Record review and update confidence

## Architecture
```
app/
├── models/          # Database tables (SQLAlchemy)
├── schemas/         # API contracts (Pydantic)
├── routers/         # Endpoints grouped by resource
├── database.py      # DB config
├── config.py        # Constants (thresholds, weights)
└── main.py          # FastAPI app
```

## Learning Logic

**Learn Mode:** Returns cards with `confidence < 0.7` or never reviewed  
**Recap Mode:** Returns cards with `confidence ≥ 0.7`

**Confidence Update:**
```python
new_confidence = 0.7 × old_confidence + 0.3 × review_score
```

Thresholds and weights configurable in `config.py`.

## Development
```bash
# Run server
uvicorn app.main:app --reload

# Run tests
pytest -v

# View API docs
open http://127.0.0.1:8000/docs
```

## Database

- SQLite for local dev (`flashcards.db`)
- Schema designed for PostgreSQL compatibility
- Auto-created on startup via `Base.metadata.create_all()`
