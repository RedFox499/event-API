from fastapi import FastAPI
from pydantic import BaseModel, Field, model_validator
from datetime import datetime
from fastapi import FastAPI, HTTPException, status, Response
from routes.users import router as users_router
from routes.events import router as events_router


app = FastAPI()
app.include_router(users_router)
app.include_router(events_router)




