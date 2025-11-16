from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session
from src.application.controllers.participant_controller import ParticipantController
from src.domain.services.participant_service import ParticipantService
from src.infrastructure.database.repositories.participant_repository_impl import ParticipantRepositoryImpl
from src.infrastructure.database.connection import get_db
from src.application.dtos.participant_dto import (
    ParticipantCreateDTO,
    ParticipantUpdateDTO,
    ParticipantResponseDTO
)

router = APIRouter(prefix="/participants", tags=["Participants"])


def get_participant_controller(db: Session = Depends(get_db)) -> ParticipantController:
    """Dependency injection for participant controller"""
    participant_repository = ParticipantRepositoryImpl(db)
    participant_service = ParticipantService(participant_repository)
    return ParticipantController(participant_service)


@router.post("/", response_model=ParticipantResponseDTO, status_code=201)
def create_participant(
    participant_dto: ParticipantCreateDTO,
    controller: ParticipantController = Depends(get_participant_controller)
):
    """Create a new participant"""
    return controller.create_participant(participant_dto)


@router.get("/{participant_id}", response_model=ParticipantResponseDTO)
def get_participant(
    participant_id: int,
    controller: ParticipantController = Depends(get_participant_controller)
):
    """Get a participant by ID"""
    return controller.get_participant(participant_id)


@router.get("/", response_model=List[ParticipantResponseDTO])
def get_all_participants(
    controller: ParticipantController = Depends(get_participant_controller)
):
    """Get all participants"""
    return controller.get_all_participants()


@router.put("/{participant_id}", response_model=ParticipantResponseDTO)
def update_participant(
    participant_id: int,
    participant_dto: ParticipantUpdateDTO,
    controller: ParticipantController = Depends(get_participant_controller)
):
    """Update an existing participant"""
    return controller.update_participant(participant_id, participant_dto)


@router.delete("/{participant_id}")
def delete_participant(
    participant_id: int,
    controller: ParticipantController = Depends(get_participant_controller)
):
    """Delete a participant"""
    return controller.delete_participant(participant_id)