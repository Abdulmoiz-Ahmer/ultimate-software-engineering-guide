"""
Todo Module - Pydantic Schemas

This module defines the data transfer objects (DTOs) using Pydantic models.
Schemas define the structure of data that flows in and out of the API,
providing validation and serialization.

Key Principles:
- Request schemas validate incoming data
- Response schemas structure outgoing data
- Schemas decouple the API contract from internal models
- They enforce validation rules and data constraints
"""

from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field


class CreateTodoRequest(BaseModel):
    """
    Schema for creating a new todo item.
    
    This schema validates the data required to create a new todo.
    It enforces business rules like minimum/maximum length constraints.
    
    Attributes:
        title (str): Title of the todo (1-100 characters, required)
        description (str, optional): Detailed description of the todo
    """
    title: str = Field(..., min_length=1, max_length=100)
    description: str | None = None


class UpdateTodoRequest(BaseModel):
    """
    Schema for updating an existing todo item.
    
    All fields are optional to support partial updates (PATCH semantics).
    Only fields provided in the request will be updated.
    
    Attributes:
        title (str, optional): New title for the todo (1-100 characters)
        description (str, optional): New description for the todo
        completed (bool, optional): New completion status
    """
    title: str | None = Field(None, min_length=1, max_length=100)
    description: str | None = None
    completed: bool | None = None


class TodoResponse(BaseModel):
    """
    Schema for todo item responses.
    
    This schema represents a todo item in API responses. It uses Pydantic's
    from_attributes configuration to automatically convert ORM models to
    response schemas.
    
    Attributes:
        id (UUID): Unique identifier of the todo
        title (str): Title of the todo
        description (str, optional): Description of the todo
        completed (bool): Completion status
    
    Configuration:
        from_attributes=True: Enables conversion from ORM models (SQLAlchemy)
    """
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    description: str | None
    completed: bool
