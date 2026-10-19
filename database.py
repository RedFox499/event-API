from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)

if __name__ == "__main__":
    with engine.connect() as connection:
        print("PostgreSQL connected.")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()