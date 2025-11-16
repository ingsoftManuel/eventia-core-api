import pytest


@pytest.mark.system
class TestEventEndpoints:
    """System tests for Event API endpoints"""
    
    def test_create_event(self, client, sample_event_data):
        """Test POST /events/ endpoint"""
        response = client.post("/events/", json=sample_event_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == sample_event_data["name"]
        assert "id" in data
    
    def test_get_all_events(self, client, sample_event_data):
        """Test GET /events/ endpoint"""
        # Create an event first
        client.post("/events/", json=sample_event_data)
        
        # Get all events
        response = client.get("/events/")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
    
    def test_get_event_by_id(self, client, sample_event_data):
        """Test GET /events/{id} endpoint"""
        # Create event
        create_response = client.post("/events/", json=sample_event_data)
        event_id = create_response.json()["id"]
        
        # Get event
        response = client.get(f"/events/{event_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == event_id
    
    def test_update_event(self, client, sample_event_data):
        """Test PUT /events/{id} endpoint"""
        # Create event
        create_response = client.post("/events/", json=sample_event_data)
        event_id = create_response.json()["id"]
        
        # Update event
        updated_data = sample_event_data.copy()
        updated_data["name"] = "Updated Event Name"
        response = client.put(f"/events/{event_id}", json=updated_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Event Name"
    
    def test_delete_event(self, client, sample_event_data):
        """Test DELETE /events/{id} endpoint"""
        # Create event
        create_response = client.post("/events/", json=sample_event_data)
        event_id = create_response.json()["id"]
        
        # Delete event
        response = client.delete(f"/events/{event_id}")
        
        assert response.status_code == 200
        
        # Verify deletion
        get_response = client.get(f"/events/{event_id}")
        assert get_response.status_code == 404
    
    def test_get_event_statistics(self, client, sample_event_data):
        """Test GET /events/{id}/statistics endpoint"""
        # Create event
        create_response = client.post("/events/", json=sample_event_data)
        event_id = create_response.json()["id"]
        
        # Get statistics
        response = client.get(f"/events/{event_id}/statistics")
        
        assert response.status_code == 200
        data = response.json()
        assert "total_capacity" in data
        assert "registered_attendees" in data
        assert "available_spots" in data


@pytest.mark.system
class TestParticipantEndpoints:
    """System tests for Participant API endpoints"""
    
    def test_create_participant(self, client, sample_participant_data):
        """Test POST /participants/ endpoint"""
        response = client.post("/participants/", json=sample_participant_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == sample_participant_data["email"]
        assert "id" in data
    
    def test_get_all_participants(self, client, sample_participant_data):
        """Test GET /participants/ endpoint"""
        # Create participant
        client.post("/participants/", json=sample_participant_data)
        
        # Get all
        response = client.get("/participants/")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_duplicate_email_validation(self, client, sample_participant_data):
        """Test that duplicate emails are rejected"""
        # Create first participant
        client.post("/participants/", json=sample_participant_data)
        
        # Try to create duplicate
        response = client.post("/participants/", json=sample_participant_data)
        
        assert response.status_code == 400


@pytest.mark.system
class TestAttendanceEndpoints:
    """System tests for Attendance API endpoints"""
    
    def test_register_attendance(self, client, sample_event_data, sample_participant_data):
        """Test POST /attendances/ endpoint"""
        # Create event and participant
        event_response = client.post("/events/", json=sample_event_data)
        event_id = event_response.json()["id"]
        
        participant_response = client.post("/participants/", json=sample_participant_data)
        participant_id = participant_response.json()["id"]
        
        # Register attendance
        attendance_data = {
            "event_id": event_id,
            "participant_id": participant_id
        }
        response = client.post("/attendances/", json=attendance_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["event_id"] == event_id
        assert data["participant_id"] == participant_id
    
    def test_duplicate_registration_prevention(self, client, sample_event_data, sample_participant_data):
        """Test that duplicate registrations are prevented"""
        # Create event and participant
        event_response = client.post("/events/", json=sample_event_data)
        event_id = event_response.json()["id"]
        
        participant_response = client.post("/participants/", json=sample_participant_data)
        participant_id = participant_response.json()["id"]
        
        # Register attendance
        attendance_data = {
            "event_id": event_id,
            "participant_id": participant_id
        }
        client.post("/attendances/", json=attendance_data)
        
        # Try duplicate registration
        response = client.post("/attendances/", json=attendance_data)
        
        assert response.status_code == 400
    
    def test_capacity_validation(self, client, sample_participant_data):
        """Test that event capacity is enforced"""
        # Create event with capacity of 1
        event_data = {
            "name": "Small Event",
            "description": "Test",
            "date": "2025-12-31T10:00:00",
            "location": "Test",
            "capacity": 1
        }
        event_response = client.post("/events/", json=event_data)
        event_id = event_response.json()["id"]
        
        # Create two participants
        p1_data = sample_participant_data.copy()
        p1_data["email"] = "p1@example.com"
        p1_response = client.post("/participants/", json=p1_data)
        p1_id = p1_response.json()["id"]
        
        p2_data = sample_participant_data.copy()
        p2_data["email"] = "p2@example.com"
        p2_response = client.post("/participants/", json=p2_data)
        p2_id = p2_response.json()["id"]
        
        # Register first participant (should succeed)
        client.post("/attendances/", json={"event_id": event_id, "participant_id": p1_id})
        
        # Try to register second participant (should fail - capacity reached)
        response = client.post("/attendances/", json={"event_id": event_id, "participant_id": p2_id})
        
        assert response.status_code == 400
        assert "capacity" in response.json()["detail"].lower()