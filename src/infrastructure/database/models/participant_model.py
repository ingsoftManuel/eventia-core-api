from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from src.infrastructure.database.connection import Base


class ParticipantModel(Base):
    """SQLAlchemy model for participants table"""
    
    __tablename__ = "participants"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    email = Column(String(200), nullable=False, unique=True, index=True)
    phone = Column(String(20), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f"<ParticipantModel(id={self.id}, email='{self.email}')>"