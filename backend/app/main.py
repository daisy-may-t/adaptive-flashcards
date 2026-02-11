from fastapi import FastAPI
from app.database import engine, Base
from app.routers import users, decks, cards

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Adaptive Flashcards API")

app.include_router(users.router)
app.include_router(decks.router)
app.include_router(cards.router)

@app.get("/")
def root():
    return {"message": "Adaptive Flashcards API"}
