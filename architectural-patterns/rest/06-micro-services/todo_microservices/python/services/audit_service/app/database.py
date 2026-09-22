"""
Database Configuration and Session Management

This module configures the SQLAlchemy database connection and provides
dependency injection for database sessions in the Audit service.

Database: SQLite (audit.db)
Pattern: Session-per-request using FastAPI's Depends
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# SQLite database connection string for audit logs
# The database file will be created in the current working directory
SQLALCHEMY_DATABASE_URL = "sqlite:///./audit.db"

# Create SQLAlchemy engine
# check_same_thread=False is required for SQLite to work with FastAPI
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# SessionLocal class will be used to create database sessions
# autocommit=False: transactions must be explicitly committed
# autoflush=False: changes are not automatically flushed to DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all ORM models
Base = declarative_base()


def get_db():
    """
    Dependency injection function that provides a database session.
    
    Yields:
        Session: SQLAlchemy database session
        
    Usage:
        @router.post("/")
        def create_log(db: Session = Depends(get_db)):
            # Use db session here
            pass
    
    The session is automatically closed after the request completes,
    ensuring proper resource management and preventing connection leaks.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
