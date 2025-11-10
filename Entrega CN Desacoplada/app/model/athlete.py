from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Literal
from datetime import datetime
import uuid

class Athlete(BaseModel):
    athlete_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    Name: str = Field(..., min_length=1, max_length=255)
    Surname: str = Field(..., min_length=1, max_length=255)
    trial: List[Literal['sprint', 'hurdles', 'weight', 'javelin', 'disc']] = ['sprint']
    distance: Optional[str] = None
    Phase: Literal['Qualifiers', 'Semi-Final', 'Final'] = 'Qualifiers'
    Number: int = 0
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    
    def update_timestamp(self):
        self.updated_at = datetime.utcnow().isoformat()