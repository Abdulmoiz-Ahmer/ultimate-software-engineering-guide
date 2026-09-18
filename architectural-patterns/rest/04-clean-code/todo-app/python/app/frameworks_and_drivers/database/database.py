"""
Frameworks and Drivers Layer - Database Configuration Module

This module configures the SQLAlchemy database connection and session management.
It's part of the outermost layer in Clean Architecture, containing framework-specific
and infrastructure code.

Key responsibilities:
- Configure the database engine (SQLite in this case)
- Set up the session factory for creating database sessions
- Provide the declarative base for ORM models
- Provide a dependency injection function for FastAPI routes

This layer can be easily replaced with a different database (PostgreSQL, MySQL, etc.)
without affecting the inner layers (use cases, entities).
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# SQLite database URL (file-based database)
SQLALCHEMY_DATABASE_URL = "sqlite:///./todos.db"

# Create the database engine
# check_same_thread=False is needed for SQLite to work with FastAPI
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create a session factory
# Sessions are used to interact with the database
# autocommit=False means we explicitly control transactions
# autoflush=False means we manually trigger flushes
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarative base class for ORM models
# All ORM models will inherit from this base
Base = declarative_base()


def get_db():
    """
    Dependency injection function for database sessions.
    
    This function is used with FastAPI's Depends() to inject a database
    session into route handlers. It ensures proper session lifecycle:
    - Creates a new session for each request
    - Yields the session to the route handler
    - Closes the session after the request completes
    
    Yields:
        Session: SQLAlchemy database session
        
    Example usage in a route:
        @router.get("/todos")
        def get_todos(db: Session = Depends(get_db)):
            # Use db session here
            pass
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
