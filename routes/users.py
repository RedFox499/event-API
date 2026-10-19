from fastapi import APIRouter, HTTPException, status, Response, Depends

from schemas.user import UserCreate, UserResponse
from services.user_store import UserStore, user_store

from models.user import User
from models.user_model import User

from sqlalchemy.orm import Session
from sqlalchemy import select
from database import get_db

router = APIRouter()

@router.post("/users", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.scalar(
        select(User).where(User.email == user.email)
    )
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Email already registered")
    new_user = User(name=user.name, email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/users", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    users = db.scalars(
        select(User)).all()
    return users

@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    existing_user = db.scalar(
        select(User).where(User.id == user_id)
    )
    if existing_user:
        return existing_user
    raise HTTPException(status_code=404, detail="User not found")

@router.delete("/users/{user_id}", response_model=UserResponse)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    existing_user = db.scalar(
        select(User).where(User.id == user_id)
    )
    if existing_user:
        db.delete(existing_user)
        db.commit()
        return existing_user
    raise HTTPException(status_code=404, detail="User not found")

@router.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.scalar(
        select(User).where(User.id == user_id)
    )
    if existing_user:
        find_existing_email = db.scalar(
            select(User).where(User.email == user.email,
                               User.id != existing_user.id)
        )
        if find_existing_email:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="Email already registered")
        existing_user.name = user.name
        existing_user.email = user.email
        db.commit()
        return existing_user
    raise HTTPException(status_code=404, detail="User not found")


