import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.api.main import app
from src.infrastructure.database.connection import Base, get_db

# Test database URL (usando SQLite en memoria para pruebas)
TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override database dependency for testing"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def test_db():
    """Create test database tables"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(test_db):
    """Create test client"""
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def sample_event_data():
    """Sample event data for testing"""
    return {
        "name": "Test Event",
        "description": "This is a test event",
        "date": "2025-12-31T10:00:00",
        "location": "Test Location",
        "capacity": 50
    }


@pytest.fixture
def sample_participant_data():
    """Sample participant data for testing"""
    return {
        "name": "Test Participant",
        "email": "test@example.com",
        "phone": "1234567890"
    }