"""
Todo Component - Data Transfer Objects (DTOs) and Commands

This module defines the data contracts for the Todo component using Pydantic.
It implements the Command/Query Responsibility Segregation (CQRS) pattern
through distinct input commands and output DTOs.

Key Concepts:

1. Commands (Inputs):
   - CreateTodoCommand: Intent to create a new todo
   - UpdateTodoCommand: Intent to modify an existing todo
   - Represents write operations (mutations)
   - Named with "Command" suffix to indicate intent

2. Queries (Outputs):
   - TodoDTO: Read-only representation of a todo
   - Used for all read operations
   - Immutable data transfer object
   - Named with "DTO" suffix (Data Transfer Object)

CQRS Benefits:
- Clear separation between reads and writes
- Different validation rules for inputs vs outputs
- Optimized models for different use cases
- Better security (output can hide sensitive fields)

Unidirectional Flow:
  Command/Query → Handler → Model → Database → DTO
"""

from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field


class CreateTodoCommand(BaseModel):
    """
    Command for creating a new todo item.
    
    This represents the user's intent to create a todo. It only contains
    fields that the user can provide - system-generated fields (id, completed)
    are handled by the handler.
    
    Attributes:
        title (str): Todo title, 1-100 characters (required)
        description (str | None): Optional description
        
    Usage:
        POST /todos/
        {
            "title": "Buy groceries",
            "description": "Milk, eggs, bread"
        }
    """
    
    # Title with validation constraints
    title: str = Field(..., min_length=1, max_length=100)
    
    # Optional description
    description: str | None = None


class UpdateTodoCommand(BaseModel):
    """
    Command for updating an existing todo item.
    
    Supports partial updates (PATCH semantics) - all fields are optional.
    Only fields provided in the request will be updated.
    
    Attributes:
        title (str | None): New title (optional)
        description (str | None): New description (optional)
        completed (bool | None): New completion status (optional)
        
    Usage:
        PATCH /todos/{id}
        {
            "completed": true
        }
    """
    
    # All fields optional for partial updates
    title: str | None = Field(None, min_length=1, max_length=100)
    description: str | None = None
    completed: bool | None = None


class TodoDTO(BaseModel):
    """
    Data Transfer Object for Todo representation.
    
    This is the immutable output format returned by all queries and commands.
    It represents the current state of a todo item after it has been
    persisted to the database.
    
    The DTO is separate from the command/query to:
    - Provide a stable API contract
    - Include system-generated fields (id, timestamps)
    - Prevent modification of output data
    - Allow different internal vs external representations
    
    Attributes:
        id (UUID): Unique identifier
        title (str): Todo title
        description (str | None): Todo description
        completed (bool): Completion status
        
    Usage:
        Returned by all Todo endpoints:
        - POST /todos/ (create)
        - GET /todos/{id} (read one)
        - GET /todos/ (read many)
        - PATCH /todos/{id} (update)
    """
    
    # Configure Pydantic to read data from ORM model attributes
    # This allows automatic conversion from TodoModel to TodoDTO
    model_config = ConfigDict(from_attributes=True)

    # All fields included in the output
    id: UUID
    title: str
    description: str | None
    completed: bool
