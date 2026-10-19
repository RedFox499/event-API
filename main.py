from fastapi import FastAPI, HTTPException, status, Response
from routes.users import router as users_router
from routes.events import router as events_router
from routes.registration import router as registration_router
from models.base import Base
from models.user_model import User
from models.event_model import Event
from models.registration import Registration
from database import engine


app = FastAPI()
app.include_router(users_router)
app.include_router(events_router)
app.include_router(registration_router)


Base.metadata.create_all(bind=engine)




