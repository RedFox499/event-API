from fastapi import FastAPI
from pydantic import BaseModel, Field, model_validator
from datetime import datetime
from fastapi import FastAPI, HTTPException, status, Response


class EventCreate(BaseModel):
    title: str
    description: str
    location: str
    capacity: int = Field(gt=0)
    start: datetime
    end: datetime

    @model_validator(mode="after")
    def check_dates(self):
        if self.end <= self.start:
            raise ValueError("End time must be after start time")
        return self


class EventUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    location: str | None = None
    capacity: int | None = None
    start: datetime | None = None
    end: datetime | None = None

class EventResponse(BaseModel):
    id: int
    title: str
    description: str
    location: str
    capacity: int
    start: datetime
    end: datetime
