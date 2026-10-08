from fastapi import FastAPI, APIRouter
from pydantic import BaseModel, Field, model_validator
from datetime import datetime
from fastapi import FastAPI, HTTPException, status, Response

from models.event_model import Event
from schemas.event_schemas import EventCreate, EventUpdate

router = APIRouter()

events = []


@router.post("/events")
def create_event(event: EventCreate):
    new_event = Event(id=len(events)+1, title=event.title,
                description=event.description,
                location=event.location, capacity=event.capacity,
                start=event.start, end=event.end)
    events.append(new_event)
    return new_event

@router.get("/events", response_model=list[Event])
def get_events():
    return events

@router.patch("/events/{event_id}")
def update_event(event_id: int, event_updated: EventUpdate):
    for i, event in enumerate(events):
        if event.id == event_id:

            old_event_data = event.dict()
            event_updated = event_updated.model_dump(exclude_unset=True)
            old_event_data.update(event_updated)

            events[i] = Event(**old_event_data)
            return events[i]
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Event not found")

@router.get("/events/{event_id}", response_model=Event)
def get_event_by_id(event_id: int):
    for event in events:
        if event.id == event_id:
            return event
    raise HTTPException(status_code=404, detail="Event not found")

@router.delete("/events/{event_id}")
def delete_event(event_id: int):
    for i, event in enumerate(events):
        if event.id == event_id:
            events.pop(i)
            return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=404, detail="Event not found")