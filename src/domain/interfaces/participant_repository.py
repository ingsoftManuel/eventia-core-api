from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.entities.participant import Participant


class ParticipantRepository(ABC):
    """Interface for participant repository"""
    
    @abstractmethod
    def create(self, participant: Participant) -> Participant:
        """Create a new participant"""
        pass
    
    @abstractmethod
    def get_by_id(self, participant_id: int) -> Optional[Participant]:
        """Get participant by ID"""
        pass
    
    @abstractmethod
    def get_by_email(self, email: str) -> Optional[Participant]:
        """Get participant by email"""
        pass
    
    @abstractmethod
    def get_all(self) -> List[Participant]:
        """Get all participants"""
        pass
    
    @abstractmethod
    def update(self, participant: Participant) -> Participant:
        """Update an existing participant"""
        pass
    
    @abstractmethod
    def delete(self, participant_id: int) -> bool:
        """Delete a participant"""
        pass