from typing import List
from fastapi import HTTPException
from src.domain.services.participant_service import ParticipantService
from src.domain.entities.participant import Participant
from src.application.dtos.participant_dto import (
    ParticipantCreateDTO,
    ParticipantUpdateDTO,
    ParticipantResponseDTO
)


class ParticipantController:
    """Controller for handling participant-related HTTP requests"""
    
    def __init__(self, participant_service: ParticipantService):
        self.participant_service = participant_service
    
    def create_participant(self, participant_dto: ParticipantCreateDTO) -> ParticipantResponseDTO:
        """Create a new participant"""
        try:
            participant = Participant(
                name=participant_dto.name,
                email=participant_dto.email,
                phone=participant_dto.phone
            )
            
            created_participant = self.participant_service.create_participant(participant)
            
            return ParticipantResponseDTO(
                id=created_participant.id,
                name=created_participant.name,
                email=created_participant.email,
                phone=created_participant.phone,
                created_at=created_participant.created_at,
                updated_at=created_participant.updated_at
            )
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    
    def get_participant(self, participant_id: int) -> ParticipantResponseDTO:
        """Get a participant by ID"""
        try:
            participant = self.participant_service.get_participant_by_id(participant_id)
            if not participant:
                raise HTTPException(
                    status_code=404,
                    detail=f"Participant with id {participant_id} not found"
                )
            
            return ParticipantResponseDTO(
                id=participant.id,
                name=participant.name,
                email=participant.email,
                phone=participant.phone,
                created_at=participant.created_at,
                updated_at=participant.updated_at
            )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    
    def get_all_participants(self) -> List[ParticipantResponseDTO]:
        """Get all participants"""
        try:
            participants = self.participant_service.get_all_participants()
            return [
                ParticipantResponseDTO(
                    id=p.id,
                    name=p.name,
                    email=p.email,
                    phone=p.phone,
                    created_at=p.created_at,
                    updated_at=p.updated_at
                )
                for p in participants
            ]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    
    def update_participant(
        self,
        participant_id: int,
        participant_dto: ParticipantUpdateDTO
    ) -> ParticipantResponseDTO:
        """Update an existing participant"""
        try:
            participant = Participant(
                participant_id=participant_id,
                name=participant_dto.name,
                email=participant_dto.email,
                phone=participant_dto.phone
            )
            
            updated_participant = self.participant_service.update_participant(participant)
            
            return ParticipantResponseDTO(
                id=updated_participant.id,
                name=updated_participant.name,
                email=updated_participant.email,
                phone=updated_participant.phone,
                created_at=updated_participant.created_at,
                updated_at=updated_participant.updated_at
            )
        except ValueError as e:
            status_code = 404 if "not found" in str(e).lower() else 400
            raise HTTPException(status_code=status_code, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    
    def delete_participant(self, participant_id: int) -> dict:
        """Delete a participant"""
        try:
            result = self.participant_service.delete_participant(participant_id)
            if not result:
                raise HTTPException(
                    status_code=404,
                    detail=f"Participant with id {participant_id} not found"
                )
            
            return {"message": f"Participant {participant_id} deleted successfully"}
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")