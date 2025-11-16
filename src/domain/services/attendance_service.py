from typing import List, Optional
from src.domain.entities.attendance import Attendance
from src.domain.interfaces.attendance_repository import AttendanceRepository
from src.domain.interfaces.event_repository import EventRepository
from src.domain.interfaces.participant_repository import ParticipantRepository
from src.infrastructure.cache.cache_client import cache_client


class AttendanceService:
    """Service containing business logic for attendance registrations"""
    
    def __init__(
        self,
        attendance_repository: AttendanceRepository,
        event_repository: EventRepository,
        participant_repository: ParticipantRepository
    ):
        self.attendance_repository = attendance_repository
        self.event_repository = event_repository
        self.participant_repository = participant_repository
    
    def register_attendance(self, attendance: Attendance) -> Attendance:
        """Register a participant to an event with business rules validation"""
        # 1. Validate event exists
        event = self.event_repository.get_by_id(attendance.event_id)
        if not event:
            raise ValueError(f"Event with id {attendance.event_id} not found")
        
        # 2. Validate participant exists
        participant = self.participant_repository.get_by_id(attendance.participant_id)
        if not participant:
            raise ValueError(f"Participant with id {attendance.participant_id} not found")
        
        # 3. Check for duplicate registration
        existing = self.attendance_repository.get_by_event_and_participant(
            attendance.event_id,
            attendance.participant_id
        )
        if existing:
            raise ValueError(
                f"Participant {attendance.participant_id} is already registered to event {attendance.event_id}"
            )
        
        # 4. Check event capacity
        current_attendees = self.attendance_repository.count_by_event(attendance.event_id)
        if not event.has_capacity(current_attendees):
            raise ValueError(f"Event {attendance.event_id} has reached maximum capacity")
        
        # 5. Validate event is in the future
        if not event.is_future_event():
            raise ValueError(f"Cannot register to past event {attendance.event_id}")
        
        # Create the attendance
        created_attendance = self.attendance_repository.create(attendance)
        
        # Invalidate relevant caches
        cache_client.delete(f"event:stats:{attendance.event_id}")
        cache_client.delete(f"attendances:event:{attendance.event_id}")
        cache_client.delete(f"attendances:participant:{attendance.participant_id}")
        
        return created_attendance
    
    def get_attendance_by_id(self, attendance_id: int) -> Optional[Attendance]:
        """Get attendance by ID"""
        return self.attendance_repository.get_by_id(attendance_id)
    
    def get_attendances_by_event(self, event_id: int) -> List[Attendance]:
        """Get all attendances for an event with caching"""
        # Try cache first
        cache_key = f"attendances:event:{event_id}"
        cached_data = cache_client.get(cache_key)
        
        if cached_data:
            return [
                Attendance(
                    attendance_id=a["id"],
                    event_id=a["event_id"],
                    participant_id=a["participant_id"]
                )
                for a in cached_data
            ]
        
        # Get from database
        attendances = self.attendance_repository.get_by_event(event_id)
        
        # Cache results for 2 minutes
        if attendances:
            cache_data = [
                {
                    "id": a.id,
                    "event_id": a.event_id,
                    "participant_id": a.participant_id
                }
                for a in attendances
            ]
            cache_client.set(cache_key, cache_data, expiration=120)
        
        return attendances
    
    def get_attendances_by_participant(self, participant_id: int) -> List[Attendance]:
        """Get all attendances for a participant with caching"""
        # Try cache first
        cache_key = f"attendances:participant:{participant_id}"
        cached_data = cache_client.get(cache_key)
        
        if cached_data:
            return [
                Attendance(
                    attendance_id=a["id"],
                    event_id=a["event_id"],
                    participant_id=a["participant_id"]
                )
                for a in cached_data
            ]
        
        # Get from database
        attendances = self.attendance_repository.get_by_participant(participant_id)
        
        # Cache results for 2 minutes
        if attendances:
            cache_data = [
                {
                    "id": a.id,
                    "event_id": a.event_id,
                    "participant_id": a.participant_id
                }
                for a in attendances
            ]
            cache_client.set(cache_key, cache_data, expiration=120)
        
        return attendances
    
    def cancel_attendance(self, attendance_id: int) -> bool:
        """Cancel an attendance registration"""
        # Get attendance to invalidate related caches
        attendance = self.attendance_repository.get_by_id(attendance_id)
        
        if not attendance:
            return False
        
        # Delete attendance
        result = self.attendance_repository.delete(attendance_id)
        
        if result:
            # Invalidate caches
            cache_client.delete(f"event:stats:{attendance.event_id}")
            cache_client.delete(f"attendances:event:{attendance.event_id}")
            cache_client.delete(f"attendances:participant:{attendance.participant_id}")
        
        return result