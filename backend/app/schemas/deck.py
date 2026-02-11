from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class DeckCreate(BaseModel):
    title: str
    description: Optional[str] = None
    owner_id: int

class DeckResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    owner_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
        