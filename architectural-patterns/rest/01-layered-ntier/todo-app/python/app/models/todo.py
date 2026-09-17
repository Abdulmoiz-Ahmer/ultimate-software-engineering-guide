"""
Todo Model - Data Model Layer

This module defines the Todo database model using SQLAlchemy ORM.
It represents the structure of the 'todos' table in the database
and is part of the Data Model layer in the N-tier architecture.

The model uses UUID for primary keys to ensure globally unique identifiers
and prevent enumeration attacks common with auto-incrementing integers.
"""

import uuid
from sqlalchemy import Column, String, Boolean
from sqlalchemy.types import UUID
from app.database import Base


class TodoModel(Base):
    """
    Todo ORM Model representing a task/todo item.
    
    This model maps to the 'todos' table in the database and defines
    the schema for todo items with UUID-based identification.
    
    Attributes:
        id (UUID): Unique identifier for the todo item, auto-generated
        title (str): The todo item's title/summary (max 100 chars, required)
        description (str, optional): Detailed description (max 255 chars)
        completed (bool): Completion status, defaults to False
    """
    
    # Table name in the database
    __tablename__ = "todos"

    # Primary key using UUID for global uniqueness
    # as_uuid=True ensures Python receives UUID objects, not strings
    # default=uuid.uuid4 automatically generates a new UUID for each record
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Title is required (nullable=False) with a max length constraint
    title = Column(String(100), nullable=False, index=True)
    
    # Description is optional (nullable=True by default)
    description = Column(String(255), nullable=True, index=True)
    
    # Completed status defaults to False for new todos
    completed = Column(Boolean, default=False)
