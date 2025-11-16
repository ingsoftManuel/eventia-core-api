from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.entities.event import Event


class EventRepository(ABC):
    """Interface for event repository"""
    
    @abstractmethod
    def create(self, event: Event) -> Event:
        """Create a new event"""
        pass
    
    @abstractmethod
    def get_by_id(self, event_id: int) -> Optional[Event]:
        """Get event by ID"""
        pass
    
    @abstractmethod
    def get_all(self) -> List[Event]:
        """Get all events"""
        pass
    
    @abstractmethod
    def update(self, event: Event) -> Event:
        """Update an existing event"""
        pass
    
    @abstractmethod
    def delete(self, event_id: int) -> bool:
        """Delete an event"""
        pass
    
    @abstractmethod
    def get_attendee_count(self, event_id: int) -> int:
        """Get current attendee count for an event"""
        pass