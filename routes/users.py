from fastapi import APIRouter, HTTPException, status, Response, Depends
from models.user import User
from schemas.user import UserCreate, UserResponse
from services.user_store import UserStore, user_store
from sqlalchemy.orm import Session
from sqlalchemy import select
from database import get_db
from models.user_model import User

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
def get_users():
    return user_store.get_users()

@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    for user in user_store.get_users():
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

@router.delete("/users/{user_id}", response_model=UserResponse)
def delete_user(user_id: int):
    for i, user in enumerate(user_store.get_users()):
        if user.id == user_id:
            return user_store.delete_user(i)

    raise HTTPException(status_code=404, detail="User not found")

@router.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserCreate):

    for current_user in user_store.get_users():
        if current_user.id == user_id:

            for user_check in user_store.get_users():
                if user_check.email == user.email and user_check.id != current_user.id:
                    raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                        detail="Email already registered")
            current_user.name = user.name
            current_user.email = user.email
            return current_user
    raise HTTPException(status_code=404, detail="User not found")


