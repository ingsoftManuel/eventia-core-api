from typing import List, Optional
from sqlalchemy.orm import Session
from src.domain.interfaces.attendance_repository import AttendanceRepository
from src.domain.entities.attendance import Attendance
from src.infrastructure.database.models.attendance_model import AttendanceModel


class AttendanceRepositoryImpl(AttendanceRepository):
    """SQLAlchemy implementation of AttendanceRepository"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, attendance: Attendance) -> Attendance:
        """Create a new attendance registration"""
        db_attendance = AttendanceModel(
            event_id=attendance.event_id,
            participant_id=attendance.participant_id,
            registration_date=attendance.registration_date
        )
        self.db.add(db_attendance)
        self.db.commit()
        self.db.refresh(db_attendance)
        return self._to_entity(db_attendance)
    
    def get_by_id(self, attendance_id: int) -> Optional[Attendance]:
        """Get attendance by ID"""
        db_attendance = self.db.query(AttendanceModel).filter(
            AttendanceModel.id == attendance_id
        ).first()
        return self._to_entity(db_attendance) if db_attendance else None
    
    def get_by_event_and_participant(
        self, 
        event_id: int, 
        participant_id: int
    ) -> Optional[Attendance]:
        """Check if participant is already registered to event"""
        db_attendance = self.db.query(AttendanceModel).filter(
            AttendanceModel.event_id == event_id,
            AttendanceModel.participant_id == participant_id
        ).first()
        return self._to_entity(db_attendance) if db_attendance else None
    
    def get_by_event(self, event_id: int) -> List[Attendance]:
        """Get all attendances for an event"""
        db_attendances = self.db.query(AttendanceModel).filter(
            AttendanceModel.event_id == event_id
        ).all()
        return [self._to_entity(a) for a in db_attendances]
    
    def get_by_participant(self, participant_id: int) -> List[Attendance]:
        """Get all attendances for a participant"""
        db_attendances = self.db.query(AttendanceModel).filter(
            AttendanceModel.participant_id == participant_id
        ).all()
        return [self._to_entity(a) for a in db_attendances]
    
    def delete(self, attendance_id: int) -> bool:
        """Delete an attendance registration"""
        db_attendance = self.db.query(AttendanceModel).filter(
            AttendanceModel.id == attendance_id
        ).first()
        if not db_attendance:
            return False
        
        self.db.delete(db_attendance)
        self.db.commit()
        return True
    
    def count_by_event(self, event_id: int) -> int:
        """Count attendees for an event"""
        return self.db.query(AttendanceModel).filter(
            AttendanceModel.event_id == event_id
        ).count()
    
    def _to_entity(self, model: AttendanceModel) -> Attendance:
        """Convert database model to domain entity"""
        return Attendance(
            attendance_id=model.id,
            event_id=model.event_id,
            participant_id=model.participant_id,
            registration_date=model.registration_date,
            created_at=model.created_at
        )