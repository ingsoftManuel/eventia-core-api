import pytest
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.infrastructure.database.connection import Base
from src.infrastructure.database.repositories.event_repository_impl import EventRepositoryImpl
from src.infrastructure.database.repositories.participant_repository_impl import ParticipantRepositoryImpl
from src.domain.entities.event import Event
from src.domain.entities.participant import Participant

# Test database
TEST_DB_URL = "sqlite:///./test_integration.db"
engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
TestSessionLocal = sessionmaker(bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Create test database session"""
    Base.metadata.create_all(bind=engine)
    session = TestSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)


@pytest.mark.integration
class TestEventRepository:
    """Integration tests for EventRepository"""
    
    def test_create_event(self, db_session):
        """Test creating an event in database"""
        repo = EventRepositoryImpl(db_session)
        event = Event(
            name="Integration Test Event",
            description="Test Description",
            date=datetime.now() + timedelta(days=1),
            location="Test Location",
            capacity=50
        )
        
        created_event = repo.create(event)
        
        assert created_event.id is not None
        assert created_event.name == "Integration Test Event"
    
    def test_get_event_by_id(self, db_session):
        """Test retrieving event by ID"""
        repo = EventRepositoryImpl(db_session)
        event = Event(
            name="Test Event",
            description="Test",
            date=datetime.now() + timedelta(days=1),
            location="Test",
            capacity=50
        )
        
        created = repo.create(event)
        retrieved = repo.get_by_id(created.id)
        
        assert retrieved is not None
        assert retrieved.id == created.id
        assert retrieved.name == "Test Event"
    
    def test_update_event(self, db_session):
        """Test updating an event"""
        repo = EventRepositoryImpl(db_session)
        event = Event(
            name="Original Name",
            description="Test",
            date=datetime.now() + timedelta(days=1),
            location="Test",
            capacity=50
        )
        
        created = repo.create(event)
        created.name = "Updated Name"
        updated = repo.update(created)
        
        assert updated.name == "Updated Name"
    
    def test_delete_event(self, db_session):
        """Test deleting an event"""
        repo = EventRepositoryImpl(db_session)
        event = Event(
            name="To Delete",
            description="Test",
            date=datetime.now() + timedelta(days=1),
            location="Test",
            capacity=50
        )
        
        created = repo.create(event)
        result = repo.delete(created.id)
        
        assert result is True
        assert repo.get_by_id(created.id) is None


@pytest.mark.integration
class TestParticipantRepository:
    """Integration tests for ParticipantRepository"""
    
    def test_create_participant(self, db_session):
        """Test creating a participant in database"""
        repo = ParticipantRepositoryImpl(db_session)
        participant = Participant(
            name="Test User",
            email="testuser@example.com",
            phone="1234567890"
        )
        
        created = repo.create(participant)
        
        assert created.id is not None
        assert created.email == "testuser@example.com"
    
    def test_get_participant_by_email(self, db_session):
        """Test retrieving participant by email"""
        repo = ParticipantRepositoryImpl(db_session)
        participant = Participant(
            name="Test User",
            email="unique@example.com",
            phone="1234567890"
        )
        
        repo.create(participant)
        retrieved = repo.get_by_email("unique@example.com")
        
        assert retrieved is not None
        assert retrieved.email == "unique@example.com"