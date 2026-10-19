from fastapi import APIRouter, HTTPException, status, Response, Depends

from models.registration import Registration
from routes.users import user_store
from services.event_store import event_store

from models.event_model import Event
from models.user_model import User

from schemas.registration import RegistrationCreate, RegistrationResponse
from services.registration_store import RegistrationStore, registration_store

from sqlalchemy.orm import Session
from sqlalchemy import select, func
from database import get_db



router = APIRouter()



@router.post("/registrations", response_model=RegistrationResponse)
def create_registration(registration: RegistrationCreate, db: Session = Depends(get_db)):
    existing_user = db.scalar(
        select(User).where(User.id == registration.user_id)
    )

    if not existing_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found")

    event_existing = db.scalar(
        select(Event).where(Event.id == registration.event_id)
    )

    if not event_existing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Event not found" )

    existing_registration = db.scalar(
        select(Registration).where(
            Registration.user_id == registration.user_id,
                        Registration.event_id == registration.event_id
        )
    )

    if existing_registration:

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Registration already registered"
            )

    registration_counter = db.scalar(
        select(func.count()).select_from(Registration).where(
            Registration.event_id == registration.event_id
        )
    )
    if registration_counter >= event_existing.capacity:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Event is full"
        )

    new_registration = Registration(event_id=registration.event_id, user_id=registration.user_id)
    db.add(new_registration)
    db.commit()
    db.refresh(new_registration)
    return new_registration


@router.get("/registrations", response_model=list[RegistrationResponse])
def get_registrations(db: Session = Depends(get_db)):
    registrations_list = db.scalars(select(Registration)).all()
    return registrations_list

@router.get("/registrations/{registration_id}", response_model=RegistrationResponse)
def get_registration(registration_id: int, db: Session = Depends(get_db)):
    registration_exist = db.scalar(
        select(Registration).where(Registration.id == registration_id)
    )
    if registration_exist:
        return registration_exist
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Registration not found")

@router.delete("/registrations/{registration_id}", response_model=RegistrationResponse)
def delete_registration(registration_id: int, db: Session = Depends(get_db)):
    registration_exist = db.scalar(
        select(Registration).where(Registration.id == registration_id)
    )
    if registration_exist:
        db.delete(registration_exist)
        db.commit()
        return registration_exist
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Registration not found"
        )

@router.get("/events/{event_id}/registrations", response_model=list[RegistrationResponse])
def get_registrations_by_event(event_id: int, db: Session = Depends(get_db)):
    event_existing = db.scalar(
        select(Event).where(Event.id == event_id)
    )
    if not event_existing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Event not found")

    registered = db.scalars(select(Registration).where(Registration.event_id == event_id)).all()
    return registered

@router.get("/users/{user_id}/registrations", response_model=list[RegistrationResponse])
def get_registrations_by_user(user_id: int,  db: Session = Depends(get_db)):
    existing_user = db.scalar(
        select(User).where(User.id == user_id)
    )
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found")

    registered = db.scalars(select(Registration).where(Registration.user_id == user_id)).all()
    return registered

