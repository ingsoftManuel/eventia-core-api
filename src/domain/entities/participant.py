from datetime import datetime
from typing import Optional
import re


class Participant:
    """Domain entity representing a participant"""
    
    def __init__(
        self,
        name: str,
        email: str,
        phone: str,
        participant_id: Optional[int] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = participant_id
        self.name = name
        self.email = email
        self.phone = phone
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
        
        self._validate()
    
    def _validate(self):
        """Validate participant data"""
        if not self.name or len(self.name.strip()) == 0:
            raise ValueError("Name cannot be empty")
        
        if not self._is_valid_email(self.email):
            raise ValueError("Invalid email format")
        
        if not self.phone or len(self.phone.strip()) == 0:
            raise ValueError("Phone cannot be empty")
    
    @staticmethod
    def _is_valid_email(email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def __repr__(self):
        return f"<Participant(id={self.id}, name='{self.name}', email='{self.email}')>"