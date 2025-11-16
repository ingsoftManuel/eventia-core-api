from datetime import datetime
from typing import Optional


class Attendance:
    """Domain entity representing an attendance registration"""
    
    def __init__(
        self,
        event_id: int,
        participant_id: int,
        attendance_id: Optional[int] = None,
        registration_date: Optional[datetime] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = attendance_id
        self.event_id = event_id
        self.participant_id = participant_id
        self.registration_date = registration_date or datetime.utcnow()
        self.created_at = created_at or datetime.utcnow()
    
    def __repr__(self):
        return f"<Attendance(id={self.id}, event_id={self.event_id}, participant_id={self.participant_id})>"