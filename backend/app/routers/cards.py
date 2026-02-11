from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Card, Deck
from app.schemas import CardCreate, CardResponse

router = APIRouter(prefix="/decks", tags=["cards"])

@router.post("/{deck_id}/cards", response_model=CardResponse, status_code=201)
def create_card(deck_id: int, card: CardCreate, db: Session = Depends(get_db)):
    # Verify deck exists
    deck = db.query(Deck).filter(Deck.id == deck_id).first()
    if not deck:
        raise HTTPException(status_code=404, detail="Deck not found")
    
    db_card = Card(deck_id=deck_id, **card.model_dump())
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    return db_card

@router.get("/{deck_id}/cards", response_model=List[CardResponse])
def list_cards(deck_id: int, db: Session = Depends(get_db)):
    # Verify deck exists
    deck = db.query(Deck).filter(Deck.id == deck_id).first()
    if not deck:
        raise HTTPException(status_code=404, detail="Deck not found")
    
    cards = db.query(Card).filter(Card.deck_id == deck_id).all()
    return cards
