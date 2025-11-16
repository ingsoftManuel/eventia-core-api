from typing import List, Optional
from sqlalchemy.orm import Session
from src.domain.interfaces.event_repository import EventRepository
from src.domain.entities.event import Event
from src.infrastructure.database.models.event_model import EventModel
from src.infrastructure.database.models.attendance_model import AttendanceModel


class EventRepositoryImpl(EventRepository):
    """SQLAlchemy implementation of EventRepository"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, event: Event) -> Event:
        """Create a new event"""
        db_event = EventModel(
            name=event.name,
            description=event.description,
            date=event.date,
            location=event.location,
            capacity=event.capacity
        )
        self.db.add(db_event)
        self.db.commit()
        self.db.refresh(db_event)
        return self._to_entity(db_event)
    
    def get_by_id(self, event_id: int) -> Optional[Event]:
        """Get event by ID"""
        db_event = self.db.query(EventModel).filter(EventModel.id == event_id).first()
        return self._to_entity(db_event) if db_event else None
    
    def get_all(self) -> List[Event]:
        """Get all events"""
        db_events = self.db.query(EventModel).all()
        return [self._to_entity(e) for e in db_events]
    
    def update(self, event: Event) -> Event:
        """Update an existing event"""
        db_event = self.db.query(EventModel).filter(EventModel.id == event.id).first()
        if not db_event:
            raise ValueError(f"Event with id {event.id} not found")
        
        db_event.name = event.name
        db_event.description = event.description
        db_event.date = event.date
        db_event.location = event.location
        db_event.capacity = event.capacity
        
        self.db.commit()
        self.db.refresh(db_event)
        return self._to_entity(db_event)
    
    def delete(self, event_id: int) -> bool:
        """Delete an event"""
        db_event = self.db.query(EventModel).filter(EventModel.id == event_id).first()
        if not db_event:
            return False
        
        self.db.delete(db_event)
        self.db.commit()
        return True
    
    def get_attendee_count(self, event_id: int) -> int:
        """Get current attendee count for an event"""
        count = self.db.query(AttendanceModel).filter(
            AttendanceModel.event_id == event_id
        ).count()
        return count
    
    def _to_entity(self, model: EventModel) -> Event:
        """Convert database model to domain entity"""
        return Event(
            event_id=model.id,
            name=model.name,
            description=model.description,
            date=model.date,
            location=model.location,
            capacity=model.capacity,
            created_at=model.created_at,
            updated_at=model.updated_at
        )