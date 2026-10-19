from fastapi import APIRouter, HTTPException, status, Response, Depends

from services.event_store import event_store
from models.user_model import User
from models.event_model import Event
from models.registration import Registration

from schemas.event_schemas import EventCreate, EventUpdate, EventResponse
from services.registration_store import registration_store

from sqlalchemy.orm import Session
from sqlalchemy import select, func
from database import get_db

router = APIRouter()

@router.post("/events", response_model=EventResponse )
def create_event(event: EventCreate, db: Session = Depends(get_db)):
    new_event = Event(title=event.title, description=event.description, location=event.location, capacity=event.capacity, start=event.start, end=event.end)
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return new_event

@router.get("/events", response_model=list[EventResponse])
def get_events(db: Session = Depends(get_db)):
    events_list = db.scalars(select(Event)).all()
    return events_list

@router.get("/events/{event_id}", response_model=EventResponse)
def get_event_by_id(event_id: int, db: Session = Depends(get_db)):
    event_exist = db.scalar(
        select(Event).where(Event.id == event_id)
    )
    if event_exist:
        return event_exist
    raise HTTPException(status_code=404, detail="Event not found")

@router.patch("/events/{event_id}", response_model=EventResponse)
def update_event(event_id: int, event_updated: EventUpdate, db: Session = Depends(get_db)):
    event_exist = db.scalar(
        select(Event).where(Event.id == event_id)
    )
    if event_exist is None:
        raise HTTPException(status_code=404, detail="Event not found")

    updated_data = event_updated.model_dump(exclude_unset=True)
    new_start = updated_data.get("start", event_exist.start)
    new_end = updated_data.get("end", event_exist.end)

    if new_start > new_end:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="end time cannot be before start time"
        )
    registered_counter = db.scalar(
        select(func.count()).select_from(Registration).where(
            Registration.event_id == event_id
        )
    )

    if 'capacity' in updated_data and updated_data['capacity'] < registered_counter:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Capacity less than registered"
        )

    for key, value in updated_data.items():
        setattr(event_exist, key, value)
    db.commit()
    return event_exist

@router.delete("/events/{event_id}", response_model=EventResponse)
def delete_event(event_id: int, db: Session = Depends(get_db)):
    event_exist = db.scalar(
        select(Event).where(Event.id == event_id)
    )
    if event_exist is not None:
        db.delete(event_exist)
        db.commit()
        return event_exist
    raise HTTPException(status_code=404, detail="Event not found")