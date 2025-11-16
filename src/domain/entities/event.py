from datetime import datetime
from typing import Optional


class Event:
    """Domain entity representing an event"""
    
    def __init__(
        self,
        name: str,
        description: str,
        date: datetime,
        location: str,
        capacity: int,
        event_id: Optional[int] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = event_id
        self.name = name
        self.description = description
        self.date = date
        self.location = location
        self.capacity = capacity
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
    
    def has_capacity(self, current_attendees: int) -> bool:
        """Check if event has available capacity"""
        return current_attendees < self.capacity
    
    def is_future_event(self) -> bool:
        """Check if event is in the future"""
        return self.date > datetime.utcnow()
    
    def __repr__(self):
        return f"<Event(id={self.id}, name='{self.name}', date={self.date})>"