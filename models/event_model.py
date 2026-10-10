from pydantic import BaseModel, Field, model_validator
from datetime import datetime

class Event(BaseModel):
    id: int
    title: str
    description: str
    location: str
    capacity: int
    start: datetime
    end: datetime
