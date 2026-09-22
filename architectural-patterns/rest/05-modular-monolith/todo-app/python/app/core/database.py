"""
Database Configuration and Session Management

This module provides centralized database configuration for the entire application.
It sets up the SQLAlchemy engine, session factory, and declarative base that all
modules will inherit from.

Key Components:
- engine: SQLAlchemy engine connected to the database
- SessionLocal: Session factory for creating database sessions
- Base: Declarative base class that all ORM models inherit from
- get_db: Dependency injection function for FastAPI routes
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Database connection URL
# Using SQLite for simplicity, but can be replaced with PostgreSQL, MySQL, etc.
SQLALCHEMY_DATABASE_URL = "sqlite:///./todos.db"

# Create the SQLAlchemy engine
# connect_args={"check_same_thread": False} is required only for SQLite
# to allow multiple threads to access the database
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# SessionLocal is a factory for creating database sessions
# autocommit=False: Transactions must be explicitly committed
# autoflush=False: Changes are not automatically flushed to the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base is the declarative base class for all ORM models
# All models across all modules inherit from this base
Base = declarative_base()


def get_db():
    """
    Database session dependency for FastAPI routes.
    
    This function creates a new database session for each request and ensures
    proper cleanup after the request is complete. It's used as a FastAPI
    dependency to inject database sessions into route handlers.
    
    Yields:
        Session: A SQLAlchemy database session
    
    Example:
        @router.get("/items")
        def get_items(db: Session = Depends(get_db)):
            return db.query(Item).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
