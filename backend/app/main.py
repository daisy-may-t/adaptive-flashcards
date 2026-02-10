from fastapi import FastAPI
from app.database import engine, Base
from app.routers import users

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Adaptive Flashcards API")

app.include_router(users.router)

@app.get("/")
def root():
    return {"message": "Adaptive Flashcards API"}
