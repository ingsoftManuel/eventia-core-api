from typing import List
from fastapi import HTTPException
from src.domain.services.event_service import EventService
from src.domain.entities.event import Event
from src.application.dtos.event_dto import (
    EventCreateDTO,
    EventUpdateDTO,
    EventResponseDTO,
    EventStatisticsDTO
)


class EventController:
    """Controller for handling event-related HTTP requests"""
    
    def __init__(self, event_service: EventService):
        self.event_service = event_service
    
    def create_event(self, event_dto: EventCreateDTO) -> EventResponseDTO:
        """Create a new event"""
        try:
            # Convert DTO to domain entity
            event = Event(
                name=event_dto.name,
                description=event_dto.description,
                date=event_dto.date,
                location=event_dto.location,
                capacity=event_dto.capacity
            )
            
            # Call service
            created_event = self.event_service.create_event(event)
            
            # Convert entity to response DTO
            return EventResponseDTO(
                id=created_event.id,
                name=created_event.name,
                description=created_event.description,
                date=created_event.date,
                location=created_event.location,
                capacity=created_event.capacity,
                created_at=created_event.created_at,
                updated_at=created_event.updated_at
            )
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    
    def get_event(self, event_id: int) -> EventResponseDTO:
        """Get an event by ID"""
        try:
            event = self.event_service.get_event_by_id(event_id)
            if not event:
                raise HTTPException(status_code=404, detail=f"Event with id {event_id} not found")
            
            return EventResponseDTO(
                id=event.id,
                name=event.name,
                description=event.description,
                date=event.date,
                location=event.location,
                capacity=event.capacity,
                created_at=event.created_at,
                updated_at=event.updated_at
            )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    
    def get_all_events(self) -> List[EventResponseDTO]:
        """Get all events"""
        try:
            events = self.event_service.get_all_events()
            return [
                EventResponseDTO(
                    id=e.id,
                    name=e.name,
                    description=e.description,
                    date=e.date,
                    location=e.location,
                    capacity=e.capacity,
                    created_at=e.created_at,
                    updated_at=e.updated_at
                )
                for e in events
            ]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    
    def update_event(self, event_id: int, event_dto: EventUpdateDTO) -> EventResponseDTO:
        """Update an existing event"""
        try:
            event = Event(
                event_id=event_id,
                name=event_dto.name,
                description=event_dto.description,
                date=event_dto.date,
                location=event_dto.location,
                capacity=event_dto.capacity
            )
            
            updated_event = self.event_service.update_event(event)
            
            return EventResponseDTO(
                id=updated_event.id,
                name=updated_event.name,
                description=updated_event.description,
                date=updated_event.date,
                location=updated_event.location,
                capacity=updated_event.capacity,
                created_at=updated_event.created_at,
                updated_at=updated_event.updated_at
            )
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    
    def delete_event(self, event_id: int) -> dict:
        """Delete an event"""
        try:
            result = self.event_service.delete_event(event_id)
            if not result:
                raise HTTPException(status_code=404, detail=f"Event with id {event_id} not found")
            
            return {"message": f"Event {event_id} deleted successfully"}
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    
    def get_event_statistics(self, event_id: int) -> EventStatisticsDTO:
        """Get event statistics"""
        try:
            stats = self.event_service.get_event_statistics(event_id)
            return EventStatisticsDTO(**stats)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")