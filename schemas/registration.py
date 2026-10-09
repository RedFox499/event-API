from pydantic import BaseModel, Field, model_validator, EmailStr

class RegistrationCreate(BaseModel):
    event_id: int
    user_id: int

class RegistrationResponse(BaseModel):
    id: int
    event_id: int
    user_id: int