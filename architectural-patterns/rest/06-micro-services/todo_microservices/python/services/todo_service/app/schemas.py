"""
Pydantic Schemas for Request/Response Validation

This module defines Pydantic models used for API request validation
and response serialization in the Todo service.

Schemas:
    - CreateTodoRequest: Input validation for creating a new todo
    - TodoResponse: Standard response format for todo items
"""

from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field


class CreateTodoRequest(BaseModel):
    """
    Request schema for creating a new todo item.
    
    This schema validates incoming requests to the POST /todos endpoint.
    
    Attributes:
        title (str): Todo title, required, 1-100 characters
        description (str, optional): Additional details about the todo
    
    Example:
        {
            "title": "Buy groceries",
            "description": "Milk, eggs, bread"
        }
    """
    # Title is required with min/max length validation
    title: str = Field(..., min_length=1, max_length=100)
    
    # Description is optional
    description: str | None = None


class TodoResponse(BaseModel):
    """
    Response schema for todo items.
    
    This schema formats todo items returned by API endpoints.
    Configured to automatically convert ORM models to Pydantic models.
    
    Attributes:
        id (UUID): Unique identifier for the todo
        title (str): Todo title
        description (str, optional): Todo description
        completed (bool): Completion status
    
    Example:
        {
            "id": "123e4567-e89b-12d3-a456-426614174000",
            "title": "Buy groceries",
            "description": "Milk, eggs, bread",
            "completed": false
        }
    """
    # Enable automatic conversion from ORM models
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    description: str | None
    completed: bool
