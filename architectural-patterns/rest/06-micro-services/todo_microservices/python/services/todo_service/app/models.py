"""
ORM Models for Todo Service

This module defines the database models (ORM) for the Todo service.
Each model represents a table in the SQLite database.

Models:
    - TodoORM: Represents a todo item with title, description, and completion status
"""

import uuid
from sqlalchemy import Column, String, Boolean
from sqlalchemy.types import UUID
from todo_service.app.database import Base


class TodoORM(Base):
    """
    Todo item database model.
    
    This model represents a single todo item in the database.
    Each todo has a unique UUID identifier, title, optional description,
    and completion status.
    
    Attributes:
        id (UUID): Primary key, automatically generated UUID
        title (str): Todo title, required, max 100 characters
        description (str, optional): Detailed description, max 255 characters
        completed (bool): Completion status, defaults to False
    
    Table:
        todos
    """
    __tablename__ = "todos"

    # Primary key with auto-generated UUID
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Todo title is required and limited to 100 characters
    title = Column(String(100), nullable=False)
    
    # Optional description field for additional details
    description = Column(String(255), nullable=True)
    
    # Completion status, defaults to False (incomplete)
    completed = Column(Boolean, default=False)
