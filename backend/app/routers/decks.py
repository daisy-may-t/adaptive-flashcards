from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models import Deck, User
from app.schemas import DeckCreate, DeckResponse

router = APIRouter(prefix="/decks", tags=["decks"])

@router.post("/", response_model=DeckResponse, status_code=201)
def create_deck(deck: DeckCreate, db: Session = Depends(get_db)):
    # Verify owner exists
    owner = db.query(User).filter(User.id == deck.owner_id).first()
    if not owner:
        raise HTTPException(status_code=404, detail="Owner not found")
    
    db_deck = Deck(**deck.model_dump())
    db.add(db_deck)
    db.commit()
    db.refresh(db_deck)
    return db_deck

@router.get("/", response_model=List[DeckResponse])
def list_decks(owner_id: Optional[int] = None, db: Session = Depends(get_db)):
    query = db.query(Deck)
    if owner_id:
        query = query.filter(Deck.owner_id == owner_id)
    return query.all()

@router.get("/{deck_id}", response_model=DeckResponse)
def get_deck(deck_id: int, db: Session = Depends(get_db)):
    deck = db.query(Deck).filter(Deck.id == deck_id).first()
    if not deck:
        raise HTTPException(status_code=404, detail="Deck not found")
    return deck
