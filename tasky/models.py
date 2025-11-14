import datetime
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    DateTime,
    Text,
    ForeignKey,
)
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

Base = declarative_base()


class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    task_sessions = relationship("TaskSession", back_populates="project")

    def __repr__(self):
        return f"<Project(id={self.id}, name='{self.name}')>"


class TaskSession(Base):
    __tablename__ = "task_sessions"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    start_time = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    end_time = Column(DateTime)
    duration_seconds = Column(Integer, nullable=False, default=0)
    status = Column(String, default="in_progress")  # e.g., "in_progress", "completed", "paused"
    project_id = Column(Integer, ForeignKey("projects.id"))

    project = relationship("Project", back_populates="task_sessions")
    notes = relationship("Note", back_populates="task_session")

    def __repr__(self):
        return f"<TaskSession(id={self.id}, title='{self.title}', status='{self.status}')>"


class Note(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    session_id = Column(Integer, ForeignKey("task_sessions.id"))

    task_session = relationship("TaskSession", back_populates="notes")

    def __repr__(self):
        return f"<Note(id={self.id}, session_id={self.session_id})>"


def get_engine():
    """Returns the SQLAlchemy engine."""
    return create_engine("sqlite:///tasky.db")


def create_tables():
    """Creates the database tables."""
    engine = get_engine()
    Base.metadata.create_all(engine)


def get_session():
    """Returns a new database session."""
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    return Session()

