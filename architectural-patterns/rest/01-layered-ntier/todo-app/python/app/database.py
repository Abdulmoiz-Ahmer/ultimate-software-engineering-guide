"""
Database configuration and session management module.

This module sets up the SQLAlchemy engine, base model class, and session factory
for database operations. It implements the Data Access Layer foundation in the
N-tier architecture.

Key Components:
- Database engine: Manages connection to SQLite database
- Base: Declarative base class for all ORM models
- SessionLocal: Factory for creating database sessions
- get_db: Dependency injection function for FastAPI routes
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# SQLite database connection string
# "sqlite:///./todos.db" creates a file-based SQLite database in the current directory
SQLALCHEMY_DATABASE_URL = "sqlite:///./todos.db"

# Create the SQLAlchemy engine
# connect_args={"check_same_thread": False} is required for SQLite to work with FastAPI
# (SQLite by default only allows one thread to access the database)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Base class for all ORM models
# All models will inherit from this to be tracked by SQLAlchemy
Base = declarative_base()

# Session factory for creating database sessions
# autocommit=False: Transactions must be explicitly committed
# autoflush=False: Changes are not automatically flushed to the database
# bind=engine: Sessions are bound to the engine we created
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    Database session dependency for FastAPI routes.
    
    This generator function provides a database session to route handlers
    and ensures proper cleanup after each request. It follows the
    dependency injection pattern used by FastAPI.
    
    Yields:
        Session: A SQLAlchemy database session
        
    Usage:
        @router.get("/example")
        def example_route(db: Session = Depends(get_db)):
            # Use db session here
            pass
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        # Always close the session when done, even if an exception occurs
        db.close()
