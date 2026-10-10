from pydantic import BaseModel, Field, model_validator, EmailStr


class UserCreate(BaseModel):
    name: str
    email: EmailStr

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr