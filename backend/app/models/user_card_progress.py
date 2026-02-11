from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base

class UserCardProgress(Base):
    __tablename__ = "user_card_progress"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    card_id = Column(Integer, ForeignKey("cards.id"), nullable=False)
    confidence_score = Column(Float, default=0.0)  # 0.0 to 1.0
    review_count = Column(Integer, default=0)
    last_reviewed_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", backref="card_progress")
    card = relationship("Card", backref="user_progress")
