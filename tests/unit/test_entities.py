import pytest
from datetime import datetime, timedelta
from src.domain.entities.event import Event
from src.domain.entities.participant import Participant
from src.domain.entities.attendance import Attendance


@pytest.mark.unit
class TestEventEntity:
    """Unit tests for Event entity"""
    
    def test_event_creation(self):
        """Test event can be created with valid data"""
        event = Event(
            name="Test Event",
            description="Test Description",
            date=datetime.now() + timedelta(days=1),
            location="Test Location",
            capacity=100
        )
        assert event.name == "Test Event"
        assert event.capacity == 100
    
    def test_event_has_capacity(self):
        """Test event capacity check"""
        event = Event(
            name="Test Event",
            description="Test",
            date=datetime.now() + timedelta(days=1),
            location="Test",
            capacity=10
        )
        assert event.has_capacity(5) is True
        assert event.has_capacity(10) is False
        assert event.has_capacity(15) is False
    
    def test_event_is_future(self):
        """Test future event detection"""
        future_event = Event(
            name="Future Event",
            description="Test",
            date=datetime.now() + timedelta(days=1),
            location="Test",
            capacity=10
        )
        assert future_event.is_future_event() is True
        
        past_event = Event(
            name="Past Event",
            description="Test",
            date=datetime.now() - timedelta(days=1),
            location="Test",
            capacity=10
        )
        assert past_event.is_future_event() is False


@pytest.mark.unit
class TestParticipantEntity:
    """Unit tests for Participant entity"""
    
    def test_participant_creation(self):
        """Test participant can be created with valid data"""
        participant = Participant(
            name="John Doe",
            email="john@example.com",
            phone="1234567890"
        )
        assert participant.name == "John Doe"
        assert participant.email == "john@example.com"
    
    def test_participant_invalid_email(self):
        """Test participant validation with invalid email"""
        with pytest.raises(ValueError, match="Invalid email format"):
            Participant(
                name="John Doe",
                email="invalid-email",
                phone="1234567890"
            )
    
    def test_participant_empty_name(self):
        """Test participant validation with empty name"""
        with pytest.raises(ValueError, match="Name cannot be empty"):
            Participant(
                name="",
                email="john@example.com",
                phone="1234567890"
            )


@pytest.mark.unit
class TestAttendanceEntity:
    """Unit tests for Attendance entity"""
    
    def test_attendance_creation(self):
        """Test attendance can be created"""
        attendance = Attendance(
            event_id=1,
            participant_id=1
        )
        assert attendance.event_id == 1
        assert attendance.participant_id == 1
        assert attendance.registration_date is not None