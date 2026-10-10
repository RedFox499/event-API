from fastapi import APIRouter, HTTPException, status, Response

from models.event_model import Event
from schemas.event_schemas import EventCreate, EventUpdate, EventResponse
from services.registration_store import registration_store
from services.event_store import event_store

router = APIRouter()


@router.post("/events", response_model=EventResponse)
def create_event(event: EventCreate):
    return event_store.add_event(event.title, event.description, event.location, event.capacity, event.start, event.end)

@router.get("/events", response_model=list[Event])
def get_events():
    return event_store.get_events()

@router.patch("/events/{event_id}")
def update_event(event_id: int, event_updated: EventUpdate):
    for i, event in enumerate(event_store.get_events()):
        if event.id == event_id:

            old_event_data = event.dict()
            event_updated = event_updated.model_dump(exclude_unset=True)
            old_event_data.update(event_updated)

            if old_event_data['start'] > event_updated['end']:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                    detail="end time cannot be before start time"
                )

            registered_counter = sum(
                1 for registr in registration_store.get_registrations()
                if registr.event_id == event_id
            )
            if 'capacity' in event_updated and event_updated['capacity'] < registered_counter:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Capacity less than registered"
                )

            event_store.events[i] = Event(**old_event_data)
            return event_store.events[i]

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Event not found")

@router.get("/events/{event_id}", response_model=Event)
def get_event_by_id(event_id: int):
    for event in event_store.get_events():
        if event.id == event_id:
            return event

    raise HTTPException(status_code=404, detail="Event not found")

@router.delete("/events/{event_id}")
def delete_event(event_id: int):
    for i, event in enumerate(event_store.get_events()):
        if event.id == event_id:
            return event_store.delete_event(i)

    raise HTTPException(status_code=404, detail="Event not found")