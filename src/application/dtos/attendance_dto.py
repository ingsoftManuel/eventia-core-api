from pydantic import BaseModel, Field
from datetime import datetime


class AttendanceCreateDTO(BaseModel):
    """DTO for creating an attendance registration"""
    event_id: int = Field(..., gt=0)
    participant_id: int = Field(..., gt=0)


class AttendanceResponseDTO(BaseModel):
    """DTO for attendance response"""
    id: int
    event_id: int
    participant_id: int
    registration_date: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True