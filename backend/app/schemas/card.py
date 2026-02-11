from pydantic import BaseModel
from datetime import datetime

class CardCreate(BaseModel):
    question: str
    answer: str

class CardResponse(BaseModel):
    id: int
    deck_id: int
    question: str
    answer: str
    created_at: datetime
    
    class Config:
        from_attributes = True
        