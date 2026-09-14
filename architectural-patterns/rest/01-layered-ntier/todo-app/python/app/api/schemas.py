"""
API Schemas - Presentation Layer

This module defines Pydantic models for request/response validation and serialization.
These schemas act as data transfer objects (DTOs) in the presentation layer,
ensuring type safety and automatic validation of API inputs/outputs.

Pydantic provides:
- Automatic validation of incoming data
- Type conversion and coercion
- Clear API documentation via OpenAPI/Swagger
- Serialization of response objects
"""

from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field


class TodoCreate(BaseModel):
    """
    Schema for creating a new todo item.
    
    Used in POST /todos/ endpoint to validate incoming todo data.
    Only accepts title and optional description; id and completed
    status are set automatically.
    
    Attributes:
        title (str): Todo title, 1-100 characters (required)
        description (str, optional): Todo description (optional)
    """
    
    # Title is required with length validation
    # Field(...) means required, with constraints
    title: str = Field(..., min_length=1, max_length=100)
    
    # Description is optional (can be None)
    description: str | None = None


class TodoUpdate(BaseModel):
    """
    Schema for updating an existing todo item.
    
    Used in PATCH /todos/{id} endpoint for partial updates.
    All fields are optional, allowing clients to update only
    specific fields without providing the entire object.
    
    Attributes:
        title (str, optional): New title, 1-100 characters
        description (str, optional): New description or None
        completed (bool, optional): New completion status
    """
    
    # All fields are optional (None by default) for partial updates
    title: str = Field(None, min_length=1, max_length=100)
    description: str | None = None
    completed: bool | None = None


class TodoResponse(BaseModel):
    """
    Schema for todo item responses.
    
    Used in all response bodies to serialize TodoModel objects
    into JSON format. The from_attributes config allows Pydantic
    to automatically convert SQLAlchemy models to this schema.
    
    Attributes:
        id (UUID): Unique identifier of the todo
        title (str): Todo title
        description (str, optional): Todo description
        completed (bool): Completion status
    """
    
    # Configure Pydantic to read data from ORM model attributes
    # (previously known as orm_mode in Pydantic v1)
    model_config = ConfigDict(from_attributes=True)

    # All fields are required in responses
    id: UUID
    title: str
    description: str | None
    completed: bool
