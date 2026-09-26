# app/core/database.py
"""
Database Configuration and Initialization Module

This module handles:
- SQLAlchemy engine and session configuration
- Database schema initialization
- Sample data seeding for demonstration purposes
"""

import uuid
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, UserORM, TodoORM

# SQLite database URL - creates a file named 'graphql_demo.db' in the project root
SQLALCHEMY_DATABASE_URL = "sqlite:///./graphql_demo.db"

# Create SQLAlchemy engine
# check_same_thread=False is required for SQLite to work with FastAPI's async nature
# Note: In production, use PostgreSQL or MySQL instead of SQLite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# SessionLocal is a factory for creating database sessions
# autocommit=False: Transactions must be explicitly committed
# autoflush=False: Changes aren't automatically flushed to the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db_with_seed():
    """
    Initialize database schema and populate with seed data.
    
    This function:
    1. Drops all existing tables (WARNING: destroys all data!)
    2. Creates fresh tables based on SQLAlchemy models
    3. Seeds the database with sample users and todos
    
    The seed data demonstrates the N+1 query problem and how
    DataLoaders solve it. Creates 3 users, each with 2 todos.
    
    Note: This is called at application startup in main.py
    """
    # Drop all existing tables (fresh start on each run)
    Base.metadata.drop_all(bind=engine)
    
    # Create all tables defined in models.py
    Base.metadata.create_all(bind=engine)

    # Create a database session for seeding
    db = SessionLocal()

    # Create 3 sample users with generated UUIDs
    users = [UserORM(id=uuid.uuid4(), name=f"User {i}") for i in range(1, 4)]
    db.add_all(users)
    db.commit()

    # Create 2 todos per user (6 todos total)
    todos = []
    for user in users:
        # First todo for the user
        todos.append(
            TodoORM(id=uuid.uuid4(), title=f"Task A for {user.name}", user_id=user.id)
        )
        # Second todo for the user
        todos.append(
            TodoORM(id=uuid.uuid4(), title=f"Task B for {user.name}", user_id=user.id)
        )

    # Add all todos to the database
    db.add_all(todos)
    db.commit()
    db.close()
