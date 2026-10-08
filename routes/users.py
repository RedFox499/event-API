from fastapi import FastAPI, APIRouter
from pydantic import BaseModel, Field, model_validator
from datetime import datetime
from fastapi import FastAPI, HTTPException, status, Response
from models.user import User
from schemas.user import UserCreate, UserResponse


router = APIRouter()

class UserStore:

    def __init__(self):
        self.users = []
        self.next_user_id = 1

    def get_users(self):
        return self.users


    def add_user(self, name, email):
        user = User(id=self.next_user_id, name=name, email=email)
        self.users.append(user)
        self.next_user_id += 1
        return user

    def delete_user(self, id):
        return self.users.pop(id)



user_store = UserStore()


@router.post("/users", response_model=UserResponse)
def create_user(user: UserCreate):
    for user_check in user_store.get_users():
        if user.email == user_check.email:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="Email already registered")

    return user_store.add_user(user.name, user.email)

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


