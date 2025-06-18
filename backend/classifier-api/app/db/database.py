from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from dotenv import load_dotenv
import os
from typing import Generator

# Load env variables
load_dotenv()

# Get desired env variables
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Base class for models
Base = declarative_base()

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()