from typing import List, Optional
from src.domain.entities.participant import Participant
from src.domain.interfaces.participant_repository import ParticipantRepository
from src.infrastructure.cache.cache_client import cache_client


class ParticipantService:
    """Service containing business logic for participants"""
    
    def __init__(self, participant_repository: ParticipantRepository):
        self.participant_repository = participant_repository
    
    def create_participant(self, participant: Participant) -> Participant:
        """Create a new participant with validation"""
        # Check if email already exists
        existing = self.participant_repository.get_by_email(participant.email)
        if existing:
            raise ValueError(f"Participant with email {participant.email} already exists")
        
        # Create participant (validation happens in entity constructor)
        created_participant = self.participant_repository.create(participant)
        
        # Invalidate cache
        cache_client.delete("participants:all")
        
        return created_participant
    
    def get_participant_by_id(self, participant_id: int) -> Optional[Participant]:
        """Get participant by ID with caching"""
        # Try cache first
        cache_key = f"participant:{participant_id}"
        cached_data = cache_client.get(cache_key)
        
        if cached_data:
            return Participant(
                participant_id=cached_data["id"],
                name=cached_data["name"],
                email=cached_data["email"],
                phone=cached_data["phone"]
            )
        
        # Get from database
        participant = self.participant_repository.get_by_id(participant_id)
        
        if participant:
            # Cache for 5 minutes
            cache_data = {
                "id": participant.id,
                "name": participant.name,
                "email": participant.email,
                "phone": participant.phone
            }
            cache_client.set(cache_key, cache_data, expiration=300)
        
        return participant
    
    def get_all_participants(self) -> List[Participant]:
        """Get all participants with caching"""
        # Try cache first
        cache_key = "participants:all"
        cached_data = cache_client.get(cache_key)
        
        if cached_data:
            return [
                Participant(
                    participant_id=p["id"],
                    name=p["name"],
                    email=p["email"],
                    phone=p["phone"]
                )
                for p in cached_data
            ]
        
        # Get from database
        participants = self.participant_repository.get_all()
        
        # Cache results
        if participants:
            cache_data = [
                {
                    "id": p.id,
                    "name": p.name,
                    "email": p.email,
                    "phone": p.phone
                }
                for p in participants
            ]
            cache_client.set(cache_key, cache_data, expiration=300)
        
        return participants
    
    def update_participant(self, participant: Participant) -> Participant:
        """Update a participant with validation"""
        # Validate participant exists
        existing = self.participant_repository.get_by_id(participant.id)
        if not existing:
            raise ValueError(f"Participant with id {participant.id} not found")
        
        # Check if new email conflicts with another participant
        email_check = self.participant_repository.get_by_email(participant.email)
        if email_check and email_check.id != participant.id:
            raise ValueError(f"Email {participant.email} is already in use by another participant")
        
        # Update participant
        updated_participant = self.participant_repository.update(participant)
        
        # Invalidate cache
        cache_client.delete(f"participant:{participant.id}")
        cache_client.delete("participants:all")
        
        return updated_participant
    
    def delete_participant(self, participant_id: int) -> bool:
        """Delete a participant"""
        result = self.participant_repository.delete(participant_id)
        
        if result:
            # Invalidate cache
            cache_client.delete(f"participant:{participant_id}")
            cache_client.delete("participants:all")
        
        return result