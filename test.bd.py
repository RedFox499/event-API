from database import SessionLocal
from models.user_model import User


db = SessionLocal()

try:
    user = User(name="Alex", email="Alex@example.com")
    db.add(user)
    db.commit()
finally:
    db.close()
