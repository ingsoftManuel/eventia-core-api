from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session
from src.application.controllers.event_controller import EventController
from src.domain.services.event_service import EventService
from src.infrastructure.database.repositories.event_repository_impl import EventRepositoryImpl
from src.infrastructure.database.connection import get_db
from src.application.dtos.event_dto import (
    EventCreateDTO,
    EventUpdateDTO,
    EventResponseDTO,
    EventStatisticsDTO
)

router = APIRouter(prefix="/events", tags=["Events"])


def get_event_controller(db: Session = Depends(get_db)) -> EventController:
    """Dependency injection for event controller"""
    event_repository = EventRepositoryImpl(db)
    event_service = EventService(event_repository)
    return EventController(event_service)


@router.post("/", response_model=EventResponseDTO, status_code=201)
def create_event(
    event_dto: EventCreateDTO,
    controller: EventController = Depends(get_event_controller)
):
    """Create a new event"""
    return controller.create_event(event_dto)


@router.get("/{event_id}", response_model=EventResponseDTO)
def get_event(
    event_id: int,
    controller: EventController = Depends(get_event_controller)
):
    """Get an event by ID"""
    return controller.get_event(event_id)


@router.get("/", response_model=List[EventResponseDTO])
def get_all_events(
    controller: EventController = Depends(get_event_controller)
):
    """Get all events"""
    return controller.get_all_events()


@router.put("/{event_id}", response_model=EventResponseDTO)
def update_event(
    event_id: int,
    event_dto: EventUpdateDTO,
    controller: EventController = Depends(get_event_controller)
):
    """Update an existing event"""
    return controller.update_event(event_id, event_dto)


@router.delete("/{event_id}")
def delete_event(
    event_id: int,
    controller: EventController = Depends(get_event_controller)
):
    """Delete an event"""
    return controller.delete_event(event_id)


@router.get("/{event_id}/statistics", response_model=EventStatisticsDTO)
def get_event_statistics(
    event_id: int,
    controller: EventController = Depends(get_event_controller)
):
    """Get event statistics (capacity, attendees, etc.)"""
    return controller.get_event_statistics(event_id)