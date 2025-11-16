from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class EventCreateDTO(BaseModel):
    """DTO for creating an event"""
    name: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1)
    date: datetime
    location: str = Field(..., min_length=1, max_length=300)
    capacity: int = Field(..., gt=0)


class EventUpdateDTO(BaseModel):
    """DTO for updating an event"""
    name: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1)
    date: datetime
    location: str = Field(..., min_length=1, max_length=300)
    capacity: int = Field(..., gt=0)


class EventResponseDTO(BaseModel):
    """DTO for event response"""
    id: int
    name: str
    description: str
    date: datetime
    location: str
    capacity: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class EventStatisticsDTO(BaseModel):
    """DTO for event statistics"""
    event_id: int
    event_name: str
    total_capacity: int
    registered_attendees: int
    available_spots: int
    occupancy_percentage: float