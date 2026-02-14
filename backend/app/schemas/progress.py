from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional
from app.schemas.card import CardResponse

class ReviewCreate(BaseModel):
    user_id: int
    card_id: int
    confidence: float  # 0.0 to 1.0

class ProgressResponse(BaseModel):
    id: int
    user_id: int
    card_id: int
    confidence_score: float
    review_count: int
    last_reviewed_at: Optional[datetime]
    
    model_config = ConfigDict(from_attributes=True)

class CardWithProgress(BaseModel):
    """Card combined with user's progress on it"""
    card: CardResponse
    progress: Optional[ProgressResponse] = None
    
    model_config = ConfigDict(from_attributes=True)
