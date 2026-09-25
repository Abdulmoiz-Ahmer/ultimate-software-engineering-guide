# services/todo_service/app/models.py
"""
Todo Service ORM Models

This module defines the database models for the Todo Service using SQLAlchemy ORM.
Each model class represents a table in the database.
"""

import uuid
from sqlalchemy import Column, String, Boolean
from sqlalchemy.types import UUID
from services.todo_service.app.database import Base


class TodoORM(Base):
    """
    Todo item database model.
    
    Represents a single todo item in the database with fields for
    identification, content, and completion status.
    
    Attributes:
        id: Unique UUID identifier for the todo (auto-generated)
        title: Short title describing the todo task (max 100 chars, required)
        description: Detailed description of the todo task (max 255 chars, optional)
        completed: Boolean flag indicating if the todo is completed (default: False)
    """
    __tablename__ = "todos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    completed = Column(Boolean, default=False)
