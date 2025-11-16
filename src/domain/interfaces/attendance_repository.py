from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.entities.attendance import Attendance


class AttendanceRepository(ABC):
    """Interface for attendance repository"""
    
    @abstractmethod
    def create(self, attendance: Attendance) -> Attendance:
        """Create a new attendance registration"""
        pass
    
    @abstractmethod
    def get_by_id(self, attendance_id: int) -> Optional[Attendance]:
        """Get attendance by ID"""
        pass
    
    @abstractmethod
    def get_by_event_and_participant(
        self, 
        event_id: int, 
        participant_id: int
    ) -> Optional[Attendance]:
        """Check if participant is already registered to event"""
        pass
    
    @abstractmethod
    def get_by_event(self, event_id: int) -> List[Attendance]:
        """Get all attendances for an event"""
        pass
    
    @abstractmethod
    def get_by_participant(self, participant_id: int) -> List[Attendance]:
        """Get all attendances for a participant"""
        pass
    
    @abstractmethod
    def delete(self, attendance_id: int) -> bool:
        """Delete an attendance registration"""
        pass
    
    @abstractmethod
    def count_by_event(self, event_id: int) -> int:
        """Count attendees for an event"""
        pass