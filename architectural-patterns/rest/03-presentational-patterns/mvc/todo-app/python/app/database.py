"""
Database Configuration Module

This module provides database connection and session management that is
shared across the application. It's infrastructure code that supports
the MVC pattern but isn't part of Model, View, or Controller itself.

In MVC Architecture:
- This module provides the persistence layer foundation
- Models use the Base class to define database tables
- Controllers use get_db() to obtain database sessions
- Views remain independent of database concerns
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# SQLite database connection string
# In production, this would typically come from environment variables
SQLALCHEMY_DATABASE_URL = "sqlite:///./todos.db"

# Create SQLAlchemy engine
# connect_args needed for SQLite thread safety with FastAPI
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Session factory for creating database sessions
# Each request will get its own session via dependency injection
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all ORM models
# All Models in MVC will inherit from this
Base = declarative_base()


def get_db():
    """
    Database session dependency for FastAPI routes.
    
    This function provides a database session to controller endpoints
    via FastAPI's dependency injection system. It ensures proper
    session lifecycle management with automatic cleanup.
    
    Yields:
        Session: SQLAlchemy database session
        
    Usage in Controller:
        @router.get("/example")
        def example(db: Session = Depends(get_db)):
            # Use db session here
            pass
    """
    db = SessionLocal()
    try:
        # Yield session for use in the request
        yield db
    finally:
        # Always close session when request completes
        db.close()
