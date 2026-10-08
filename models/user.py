from fastapi import FastAPI
from pydantic import BaseModel, Field, model_validator, EmailStr
from datetime import datetime
from fastapi import FastAPI, HTTPException, status, Response


class User:
    def __init__(self, name: str, email: str, id: int):
        self.id = id
        self.name = name
        self.email = email
