from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from typing import Union
import datetime
from .models import Base, Project, TaskSession

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

def add_project(project_name: str) -> Union[Project, None]:
    """
    Adds a new project to the database.
    Returns the new Project object if successful, None if project name already exists.
    """
    with SessionLocal() as session:
        existing_project = session.query(Project).filter_by(name=project_name).first()
        if existing_project:
            return None # Project with this name already exists

        new_project = Project(name=project_name)
        session.add(new_project)
        try:
            session.commit()
            session.refresh(new_project)
            return new_project
        except IntegrityError:
            session.rollback()
            return None # Should not happen if check above is correct, but good for safety

def get_all_projects() -> list[Project]:
    """
    Retrieves all projects from the database.
    """
    with SessionLocal() as session:
        return session.query(Project).order_by(Project.name).all()

def create_task_session(title: str, description: str, project_id: int) -> TaskSession:
    """
    Creates a new task session in the database.
    """
    with SessionLocal() as session:
        new_session = TaskSession(
            title=title,
            description=description,
            project_id=project_id,
            start_time=datetime.datetime.utcnow(),
            status="in_progress"
        )
        session.add(new_session)
        session.commit()
        session.refresh(new_session)
        return new_session

def update_task_session(session_id: int, end_time: datetime.datetime, duration_seconds: int, status: str) -> Union[TaskSession, None]:
    """
    Updates an existing task session in the database.
    """
    with SessionLocal() as session:
        task_session = session.query(TaskSession).filter_by(id=session_id).first()
        if task_session:
            task_session.end_time = end_time
            task_session.duration_seconds = duration_seconds
            task_session.status = status
            session.commit()
            session.refresh(task_session)
            return task_session
        return None

