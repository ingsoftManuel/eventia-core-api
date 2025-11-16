from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


class ParticipantCreateDTO(BaseModel):
    """DTO for creating a participant"""
    name: str = Field(..., min_length=1, max_length=200)
    email: EmailStr
    phone: str = Field(..., min_length=1, max_length=20)


class ParticipantUpdateDTO(BaseModel):
    """DTO for updating a participant"""
    name: str = Field(..., min_length=1, max_length=200)
    email: EmailStr
    phone: str = Field(..., min_length=1, max_length=20)


class ParticipantResponseDTO(BaseModel):
    """DTO for participant response"""
    id: int
    name: str
    email: str
    phone: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True