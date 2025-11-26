
from sqlalchemy.orm import Session
from typing import Generator

from app.core.database import SessionLocal

def get_db() -> Generator[Session, None, None]:
    """
    Dependency function to get a database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
