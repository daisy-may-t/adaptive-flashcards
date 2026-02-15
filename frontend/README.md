# Frontend

Modern Vue 3 flashcard interface with adaptive filtering and fullscreen study mode.

## Tech Stack

- Vue 3 + Vite
- Axios for API calls
- Vitest + Vue Test Utils for testing

## Quick Start

```bash
npm install
npm run dev        # Start dev server (localhost:5173)
npm run test       # Run unit tests
```

**Note:** Backend must be running on `http://127.0.0.1:8000`

## Project Structure

```
src/
├── components/           # Vue components
│   ├── CreatePanel.vue   # Create decks and cards
│   ├── Flashcard.vue    # Card with flip animation
│   ├── FullscreenFlashcard.vue  # Immersive study mode
│   └── ...
├── services/
│   └── api.js          # All backend API calls
├── App.vue             # Root component with navigation
└── main.js

tests/
└── components/         # Component unit tests
```

## Features

- **Study Mode** - Learn new cards (confidence < 70%) or recap known cards (≥ 70%)
- **Create Panel** - Create decks and add cards through UI
- **Fullscreen Mode** - Distraction-free study experience
- **Confidence Tracking** - 0-10 rating scale with visual tick marks
