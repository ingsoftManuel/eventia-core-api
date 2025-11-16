from typing import List, Optional
from sqlalchemy.orm import Session
from src.domain.interfaces.participant_repository import ParticipantRepository
from src.domain.entities.participant import Participant
from src.infrastructure.database.models.participant_model import ParticipantModel


class ParticipantRepositoryImpl(ParticipantRepository):
    """SQLAlchemy implementation of ParticipantRepository"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, participant: Participant) -> Participant:
        """Create a new participant"""
        db_participant = ParticipantModel(
            name=participant.name,
            email=participant.email,
            phone=participant.phone
        )
        self.db.add(db_participant)
        self.db.commit()
        self.db.refresh(db_participant)
        return self._to_entity(db_participant)
    
    def get_by_id(self, participant_id: int) -> Optional[Participant]:
        """Get participant by ID"""
        db_participant = self.db.query(ParticipantModel).filter(
            ParticipantModel.id == participant_id
        ).first()
        return self._to_entity(db_participant) if db_participant else None
    
    def get_by_email(self, email: str) -> Optional[Participant]:
        """Get participant by email"""
        db_participant = self.db.query(ParticipantModel).filter(
            ParticipantModel.email == email
        ).first()
        return self._to_entity(db_participant) if db_participant else None
    
    def get_all(self) -> List[Participant]:
        """Get all participants"""
        db_participants = self.db.query(ParticipantModel).all()
        return [self._to_entity(p) for p in db_participants]
    
    def update(self, participant: Participant) -> Participant:
        """Update an existing participant"""
        db_participant = self.db.query(ParticipantModel).filter(
            ParticipantModel.id == participant.id
        ).first()
        if not db_participant:
            raise ValueError(f"Participant with id {participant.id} not found")
        
        db_participant.name = participant.name
        db_participant.email = participant.email
        db_participant.phone = participant.phone
        
        self.db.commit()
        self.db.refresh(db_participant)
        return self._to_entity(db_participant)
    
    def delete(self, participant_id: int) -> bool:
        """Delete a participant"""
        db_participant = self.db.query(ParticipantModel).filter(
            ParticipantModel.id == participant_id
        ).first()
        if not db_participant:
            return False
        
        self.db.delete(db_participant)
        self.db.commit()
        return True
    
    def _to_entity(self, model: ParticipantModel) -> Participant:
        """Convert database model to domain entity"""
        return Participant(
            participant_id=model.id,
            name=model.name,
            email=model.email,
            phone=model.phone,
            created_at=model.created_at,
            updated_at=model.updated_at
        )