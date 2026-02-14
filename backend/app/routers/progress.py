from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timezone
from app.database import get_db
from app.models import Card, User, UserCardProgress, Deck
from app.schemas import ReviewCreate, ProgressResponse, CardWithProgress, CardResponse
from app.config import (
    CONFIDENCE_THRESHOLD_LEARN, 
    CONFIDENCE_THRESHOLD_RECAP,
    REVIEW_WEIGHT_HISTORY,
    REVIEW_WEIGHT_NEW
)

router = APIRouter(tags=["progress"])

@router.get("/users/{user_id}/cards", response_model=List[CardWithProgress])
def get_user_cards(
    user_id: int,
    mode: str = Query(..., pattern="^(learn|recap)$"),
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

@router.post("/reviews", response_model=ProgressResponse, status_code=201)
def record_review(review: ReviewCreate, db: Session = Depends(get_db)):
    """Record a learning/review event and update progress"""
    # Verify user and card exist
    user = db.query(User).filter(User.id == review.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    card = db.query(Card).filter(Card.id == review.card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    
    # Validate confidence
    if not 0.0 <= review.confidence <= 1.0:
        raise HTTPException(status_code=400, detail="Confidence must be between 0.0 and 1.0")
    
    # Find or create progress record
    progress = db.query(UserCardProgress).filter(
        UserCardProgress.user_id == review.user_id,
        UserCardProgress.card_id == review.card_id
    ).first()
    
    if progress:
        # Update existing: weighted average
        progress.confidence_score = (
            REVIEW_WEIGHT_HISTORY * progress.confidence_score + 
            REVIEW_WEIGHT_NEW * review.confidence
        )
        progress.review_count += 1
        progress.last_reviewed_at = datetime.now(timezone.utc)
    else:
        # Create new
        progress = UserCardProgress(
            user_id=review.user_id,
            card_id=review.card_id,
            confidence_score=review.confidence,
            review_count=1,
            last_reviewed_at=datetime.now(timezone.utc)
        )
        db.add(progress)
    
    db.commit()
    db.refresh(progress)
    return progress
