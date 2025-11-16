from typing import List
from fastapi import HTTPException
from src.domain.services.attendance_service import AttendanceService
from src.domain.entities.attendance import Attendance
from src.application.dtos.attendance_dto import (
    AttendanceCreateDTO,
    AttendanceResponseDTO
)


class AttendanceController:
    """Controller for handling attendance-related HTTP requests"""
    
    def __init__(self, attendance_service: AttendanceService):
        self.attendance_service = attendance_service
    
    def register_attendance(self, attendance_dto: AttendanceCreateDTO) -> AttendanceResponseDTO:
        """Register a participant to an event"""
        try:
            attendance = Attendance(
                event_id=attendance_dto.event_id,
                participant_id=attendance_dto.participant_id
            )
            
            created_attendance = self.attendance_service.register_attendance(attendance)
            
            return AttendanceResponseDTO(
                id=created_attendance.id,
                event_id=created_attendance.event_id,
                participant_id=created_attendance.participant_id,
                registration_date=created_attendance.registration_date,
                created_at=created_attendance.created_at
            )
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    
    def get_attendance(self, attendance_id: int) -> AttendanceResponseDTO:
        """Get an attendance by ID"""
        try:
            attendance = self.attendance_service.get_attendance_by_id(attendance_id)
            if not attendance:
                raise HTTPException(
                    status_code=404,
                    detail=f"Attendance with id {attendance_id} not found"
                )
            
            return AttendanceResponseDTO(
                id=attendance.id,
                event_id=attendance.event_id,
                participant_id=attendance.participant_id,
                registration_date=attendance.registration_date,
                created_at=attendance.created_at
            )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    
    def get_attendances_by_event(self, event_id: int) -> List[AttendanceResponseDTO]:
        """Get all attendances for a specific event"""
        try:
            attendances = self.attendance_service.get_attendances_by_event(event_id)
            return [
                AttendanceResponseDTO(
                    id=a.id,
                    event_id=a.event_id,
                    participant_id=a.participant_id,
                    registration_date=a.registration_date,
                    created_at=a.created_at
                )
                for a in attendances
            ]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    
    def get_attendances_by_participant(self, participant_id: int) -> List[AttendanceResponseDTO]:
        """Get all attendances for a specific participant"""
        try:
            attendances = self.attendance_service.get_attendances_by_participant(participant_id)
            return [
                AttendanceResponseDTO(
                    id=a.id,
                    event_id=a.event_id,
                    participant_id=a.participant_id,
                    registration_date=a.registration_date,
                    created_at=a.created_at
                )
                for a in attendances
            ]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    
    def cancel_attendance(self, attendance_id: int) -> dict:
        """Cancel an attendance registration"""
        try:
            result = self.attendance_service.cancel_attendance(attendance_id)
            if not result:
                raise HTTPException(
                    status_code=404,
                    detail=f"Attendance with id {attendance_id} not found"
                )
            
            return {"message": f"Attendance {attendance_id} cancelled successfully"}
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")