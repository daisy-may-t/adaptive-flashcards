from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models import Card, User, UserCardProgress, Deck
from app.schemas import ProgressResponse, CardWithProgress, CardResponse
from app.config import (
    CONFIDENCE_THRESHOLD_LEARN, 
    CONFIDENCE_THRESHOLD_RECAP,
)

router = APIRouter(tags=["progress"])

@router.get("/users/{user_id}/cards", response_model=List[CardWithProgress])
def get_user_cards(
    user_id: int,
    mode: str = Query(..., regex="^(learn|recap)$"),
    deck_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    Get cards for a user based on mode:
    - learn: Cards never seen or low confidence
    - recap: Cards with sufficient confidence for review
    """
    # Verify user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Build base query
    query = db.query(Card)
    if deck_id:
        deck = db.query(Deck).filter(Deck.id == deck_id).first()
        if not deck:
            raise HTTPException(status_code=404, detail="Deck not found")
        query = query.filter(Card.deck_id == deck_id)
    
    cards = query.all()
    
    # Get progress for all cards
    card_ids = [card.id for card in cards]
    progress_records = db.query(UserCardProgress).filter(
        UserCardProgress.user_id == user_id,
        UserCardProgress.card_id.in_(card_ids)
    ).all()
    progress_map = {progress.card_id: progress for progress in progress_records}
    
    # Filter based on mode
    result = []
    for card in cards:
        progress = progress_map.get(card.id)
        
        if mode == "learn":
            if progress is None or progress.confidence_score < CONFIDENCE_THRESHOLD_LEARN:
                result.append(CardWithProgress(
                    card=CardResponse.model_validate(card),
                    progress=ProgressResponse.model_validate(progress) if progress else None
                ))
        
        elif mode == "recap":
            if progress and progress.confidence_score >= CONFIDENCE_THRESHOLD_RECAP:
                result.append(CardWithProgress(
                    card=CardResponse.model_validate(card),
                    progress=ProgressResponse.model_validate(progress)
                ))
    
    return result
