from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import users, decks, cards, progress

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Adaptive Flashcards API")

app.add_middleware(
       CORSMiddleware,
       allow_origins=["http://localhost:5173"],  # Vite dev server
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )

app.include_router(users.router)
app.include_router(decks.router)
app.include_router(cards.router)
app.include_router(progress.router)

@app.get("/")
def root():
    return {"message": "Adaptive Flashcards API"}
