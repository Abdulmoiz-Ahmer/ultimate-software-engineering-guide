# services/todo_service/app/database.py
"""
Todo Service Database Configuration

This module configures the SQLAlchemy database connection for the Todo Service.
It uses SQLite as the database backend and provides a session factory
and dependency injection function for database access.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# SQLite database URL - creates/connects to todos.db in the current directory
SQLALCHEMY_DATABASE_URL = "sqlite:///./todos.db"

# Create SQLAlchemy engine with SQLite-specific configuration
# check_same_thread=False allows the engine to be used across multiple threads
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Session factory for creating database sessions
# autocommit=False: Requires explicit commit() calls for transactions
# autoflush=False: Prevents automatic flush before queries
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all ORM models in this service
Base = declarative_base()


def get_db():
    """
    Database session dependency for FastAPI.
    
    Creates a new database session for each request and ensures
    it's properly closed after the request is completed.
    
    Yields:
        Session: SQLAlchemy database session
    
    Usage:
        Use with FastAPI's Depends() in route handlers:
        @app.get("/")
        def read_items(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
