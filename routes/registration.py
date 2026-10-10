from fastapi import APIRouter, HTTPException, status, Response

from models.registration import Registration
from schemas.registration import RegistrationCreate, RegistrationResponse
from services.registration_store import RegistrationStore, registration_store
from routes.users import user_store
from services.event_store import event_store


router = APIRouter()



@router.post("/registrations", response_model=RegistrationResponse)
def create_registration(registration: RegistrationCreate):
    user_exists = any(registration.user_id == user.id for user in user_store.get_users())

    if not user_exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found")

    event_exists = any(registration.event_id == event.id for event in event_store.get_events())

    if not event_exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Event not found" )

    if any(registration_check.event_id == registration.event_id and
           registration_check.user_id == registration.user_id
           for registration_check in registration_store.get_registrations()
           ):

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Registration already registered"
            )

    registeredcounter = sum(
        1 for registr in registration_store.get_registrations()
        if registr.event_id == registration.event_id
    )

    for event in event_store.get_events():
        if event.id == registration.event_id:
            if registeredcounter >= event.capacity:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Event is full"
                )
            break

    return registration_store.add_registration(user_id=registration.user_id,
                                               event_id=registration.event_id)

@router.get("/registrations", response_model=list[RegistrationResponse])
def get_registrations():
    return registration_store.get_registrations()

@router.get("/registrations/{registration_id}", response_model=RegistrationResponse)
def get_registration(registration_id: int):
    for registration in registration_store.get_registrations():
        if registration.id == registration_id:
            return registration
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Registration not found")

@router.delete("/registrations/{registration_id}", response_model=RegistrationResponse)
def delete_registration(registration_id: int):
    for i, registration in enumerate(registration_store.get_registrations()):

        if registration.id == registration_id:
            return registration_store.delete_registration(i)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Registration not found"
        )

@router.get("/events/{event_id}/registrations", response_model=list[RegistrationResponse])
def get_registrations_by_event(event_id: int):
    event_exists = any(event_id == event.id for event in event_store.get_events())
    if not event_exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Event not found")

    registered = []
    for registration in registration_store.get_registrations():
        if registration.event_id == event_id:
            registered.append(registration)
    return registered

@router.get("/users/{user_id}/registrations", response_model=list[RegistrationResponse])
def get_registrations_by_user(user_id: int):
    user_exists = any(user_id == user.id for user in user_store.get_users())
    if not user_exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found")

    registered = []
    for registration in registration_store.get_registrations():
        if registration.user_id == user_id:
            registered.append(registration)
    return registered

