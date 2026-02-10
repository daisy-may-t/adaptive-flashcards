# Backend

The backend provides a REST API for managing users, decks, cards, and tracking learning progress.

## Responsibilities
- Persist learner progress and confidence scores
- Serve card sets for different learning modes
- Provide a foundation for adaptive learning logic

## Planned Endpoints

### Users
- POST   /users
- GET    /users/{user_id}

### Decks
- POST   /decks
- GET    /decks
- GET    /decks/{deck_id}

### Cards
- POST   /decks/{deck_id}/cards
- GET    /decks/{deck_id}/cards

### Learning / Progress
- POST   /reviews
- GET    /users/{user_id}/cards?mode=learn|recap&deck_id={deck_id}
