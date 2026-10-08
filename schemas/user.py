from fastapi import FastAPI
from pydantic import BaseModel, Field, model_validator, EmailStr
from datetime import datetime
from fastapi import FastAPI, HTTPException, status, Response

class UserCreate(BaseModel):
    name: str
    email: EmailStr

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr