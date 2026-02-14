from pydantic import BaseModel, ConfigDict
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
    
    model_config = ConfigDict(from_attributes=True)
