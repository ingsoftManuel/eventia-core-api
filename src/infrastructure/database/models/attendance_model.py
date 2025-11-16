from sqlalchemy import Column, Integer, DateTime, ForeignKey, UniqueConstraint
from datetime import datetime
from src.infrastructure.database.connection import Base


class AttendanceModel(Base):
    """SQLAlchemy model for attendance table"""
    
    __tablename__ = "attendances"
    
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id", ondelete="CASCADE"), nullable=False, index=True)
    participant_id = Column(Integer, ForeignKey("participants.id", ondelete="CASCADE"), nullable=False, index=True)
    registration_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Ensure a participant can only register once per event
    __table_args__ = (
        UniqueConstraint('event_id', 'participant_id', name='unique_event_participant'),
    )
    
    def __repr__(self):
        return f"<AttendanceModel(id={self.id}, event_id={self.event_id}, participant_id={self.participant_id})>"