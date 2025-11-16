from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime
from src.infrastructure.database.connection import Base


class EventModel(Base):
    """SQLAlchemy model for events table"""
    
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=False)
    date = Column(DateTime, nullable=False, index=True)
    location = Column(String(300), nullable=False)
    capacity = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f"<EventModel(id={self.id}, name='{self.name}')>"