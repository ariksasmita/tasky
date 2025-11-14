from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base

DATABASE_URL = "sqlite:///tasky.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """
    Initializes the database and creates tables if they don't exist.
    """
    Base.metadata.create_all(bind=engine)

def get_db():
    """
    Returns a new database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

