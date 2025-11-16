from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session
from src.application.controllers.attendance_controller import AttendanceController
from src.domain.services.attendance_service import AttendanceService
from src.infrastructure.database.repositories.attendance_repository_impl import AttendanceRepositoryImpl
from src.infrastructure.database.repositories.event_repository_impl import EventRepositoryImpl
from src.infrastructure.database.repositories.participant_repository_impl import ParticipantRepositoryImpl
from src.infrastructure.database.connection import get_db
from src.application.dtos.attendance_dto import (
    AttendanceCreateDTO,
    AttendanceResponseDTO
)

router = APIRouter(prefix="/attendances", tags=["Attendances"])


def get_attendance_controller(db: Session = Depends(get_db)) -> AttendanceController:
    """Dependency injection for attendance controller"""
    attendance_repository = AttendanceRepositoryImpl(db)
    event_repository = EventRepositoryImpl(db)
    participant_repository = ParticipantRepositoryImpl(db)
    
    attendance_service = AttendanceService(
        attendance_repository,
        event_repository,
        participant_repository
    )
    return AttendanceController(attendance_service)


@router.post("/", response_model=AttendanceResponseDTO, status_code=201)
def register_attendance(
    attendance_dto: AttendanceCreateDTO,
    controller: AttendanceController = Depends(get_attendance_controller)
):
    """Register a participant to an event"""
    return controller.register_attendance(attendance_dto)


@router.get("/{attendance_id}", response_model=AttendanceResponseDTO)
def get_attendance(
    attendance_id: int,
    controller: AttendanceController = Depends(get_attendance_controller)
):
    """Get an attendance by ID"""
    return controller.get_attendance(attendance_id)


@router.get("/event/{event_id}", response_model=List[AttendanceResponseDTO])
def get_attendances_by_event(
    event_id: int,
    controller: AttendanceController = Depends(get_attendance_controller)
):
    """Get all attendances for a specific event"""
    return controller.get_attendances_by_event(event_id)


@router.get("/participant/{participant_id}", response_model=List[AttendanceResponseDTO])
def get_attendances_by_participant(
    participant_id: int,
    controller: AttendanceController = Depends(get_attendance_controller)
):
    """Get all attendances for a specific participant"""
    return controller.get_attendances_by_participant(participant_id)


@router.delete("/{attendance_id}")
def cancel_attendance(
    attendance_id: int,
    controller: AttendanceController = Depends(get_attendance_controller)
):
    """Cancel an attendance registration"""
    return controller.cancel_attendance(attendance_id)