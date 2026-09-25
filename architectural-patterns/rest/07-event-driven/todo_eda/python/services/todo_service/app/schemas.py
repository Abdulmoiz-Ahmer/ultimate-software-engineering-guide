# services/todo_service/app/schemas.py
"""
Todo Service Pydantic Schemas

This module defines the request and response schemas for the Todo Service API.
These schemas are used for data validation and serialization/deserialization
of API payloads.
"""

from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field


class CreateTodoRequest(BaseModel):
    """
    Request schema for creating a new todo item.
    
    Validates incoming data when a client creates a new todo.
    
    Attributes:
        title: Todo title (1-100 characters, required)
        description: Optional detailed description of the todo
    """
    title: str = Field(..., min_length=1, max_length=100)
    description: str | None = None


class TodoResponse(BaseModel):
    """
    Response schema for todo item data.
    
    Used when returning todo information to clients.
    The from_attributes configuration allows this schema to be
    created directly from SQLAlchemy ORM models.
    
    Attributes:
        id: Unique identifier for the todo
        title: Todo title
        description: Optional todo description
        completed: Whether the todo is marked as complete
    """
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    description: str | None
    completed: bool
