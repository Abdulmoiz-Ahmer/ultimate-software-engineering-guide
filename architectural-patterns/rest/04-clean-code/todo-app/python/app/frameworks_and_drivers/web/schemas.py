"""
Frameworks and Drivers Layer - Web Schemas Module

This module defines the HTTP request and response schemas using Pydantic.
These schemas are used for:
- Validating incoming HTTP request data
- Serializing outgoing HTTP response data
- Generating OpenAPI documentation

Key points:
- Schemas are framework-specific (Pydantic for FastAPI)
- They represent the HTTP/API contract, not the domain model
- They live in the outermost layer of Clean Architecture
- Changes to API contracts don't affect inner layers (use cases, entities)

The controller layer maps between these HTTP schemas and the domain DTOs
used by the use cases.
"""

from uuid import UUID
from pydantic import BaseModel, Field


class CreateTodoHTTPPayload(BaseModel):
    """
    HTTP request schema for creating a new todo.
    
    This schema defines what data clients must provide when creating a todo.
    Pydantic automatically validates the incoming JSON against these rules.
    
    Attributes:
        title: Todo title (1-100 characters, required)
        description: Optional description
    """
    title: str = Field(..., min_length=1, max_length=100)
    description: str | None = None


class UpdateTodoHTTPPayload(BaseModel):
    """
    HTTP request schema for updating a todo.
    
    All fields are optional to support partial updates (PATCH semantic).
    Clients only need to provide the fields they want to update.
    
    Attributes:
        title: Optional new title (1-100 characters if provided)
        description: Optional new description
        completed: Optional new completion status
    """
    title: str | None = Field(None, min_length=1, max_length=100)
    description: str | None = None
    completed: bool | None = None


class TodoHTTPResponse(BaseModel):
    """
    HTTP response schema for todo items.
    
    This schema defines the structure of todo data returned to clients.
    It's used for both single todos and lists of todos.
    
    Attributes:
        id: Unique identifier (UUID)
        title: Todo title
        description: Optional description
        completed: Completion status
    """
    id: UUID
    title: str
    description: str | None
    completed: bool
