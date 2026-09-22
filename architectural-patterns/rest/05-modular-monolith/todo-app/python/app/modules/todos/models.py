"""
Todo Module - Database Models

This module defines the ORM (Object-Relational Mapping) models for the Todos domain.
Models represent the database schema and provide the data persistence layer.

In a modular monolith:
- Each module owns its own tables
- Table names are prefixed with the module name to prevent collisions
- Models are not directly exposed to other modules (see public.py for inter-module communication)
"""

import uuid
from sqlalchemy import Column, String, Boolean
from sqlalchemy.types import UUID
from app.core.database import Base


class TodoORM(Base):
    """
    Todo ORM Model
    
    Represents a todo item in the database. This model encapsulates all
    database-related operations for todos.
    
    Attributes:
        id (UUID): Unique identifier for the todo item
        title (str): Title of the todo (max 100 characters)
        description (str, optional): Detailed description of the todo (max 255 characters)
        completed (bool): Completion status of the todo
    
    Table Design:
        - Table name is prefixed with 'todos_' to indicate module ownership
        - This prevents naming conflicts when multiple modules have similar entities
    """
    __tablename__ = "todos_todo"  # Prefixed by module name to prevent table collisions

    # Primary key: UUID provides globally unique identifiers across distributed systems
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Title: Required field with a maximum length constraint
    title = Column(String(100), nullable=False)
    
    # Description: Optional field for additional details
    description = Column(String(255), nullable=True)
    
    # Completed: Boolean flag indicating completion status, defaults to False
    completed = Column(Boolean, default=False)
