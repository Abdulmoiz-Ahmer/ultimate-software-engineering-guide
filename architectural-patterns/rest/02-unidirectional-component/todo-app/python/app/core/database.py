"""
Core Database Module - Shared Infrastructure

This module provides database configuration and session management that is
shared across all components. It's part of the 'core' infrastructure layer
that components depend on but don't implement themselves.

Core Module Purpose:
- Provides cross-cutting concerns (database, config, logging, etc.)
- Shared by all components but owned by no specific component
- Infrastructure code that doesn't contain business logic
- Keeps components focused on their domain logic

In Unidirectional Component Architecture:
- Core provides foundation/infrastructure
- Components provide business features
- Components use core but don't modify it
- Core remains stable while components evolve
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# SQLite database connection string
# In production, this would come from environment variables
SQLALCHEMY_DATABASE_URL = "sqlite:///./todos.db"

# Create SQLAlchemy engine
# connect_args for SQLite thread safety with FastAPI
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Session factory for creating database sessions
# Each request gets its own session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all ORM models across all components
# All component models inherit from this
Base = declarative_base()


def get_db():
    """
    Database session dependency injection.
    
    Provides a database session to request handlers and ensures
    proper cleanup. This is used by all component routers via
    FastAPI's Depends() system.
    
    Yields:
        Session: SQLAlchemy database session
        
    Usage:
        @router.get("/example")
        def example(db: Session = Depends(get_db)):
            # Use db here
            pass
    """
    db = SessionLocal()
    try:
        # Yield session for use in the request
        yield db
    finally:
        # Always close session after request completes
        db.close()
