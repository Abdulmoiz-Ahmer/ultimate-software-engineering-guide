"""
Todo Service - Business Logic Layer

This module implements the Service layer (Business Logic Layer) in the N-tier
architecture. It orchestrates business operations, enforces business rules,
and coordinates between the API layer and data access layer.

Key Responsibilities:
- Implements business logic and validation rules
- Coordinates between API schemas and repository operations
- Handles error scenarios and business rule violations
- Provides a clean API for the presentation layer (routes)

The service layer is independent of HTTP concerns (request/response)
and database details (SQL/ORM), making it easily testable and reusable.
"""

import uuid

from fastapi import HTTPException
from app.repositories.todo_repository import TodoRepository
from app.api.schemas import TodoCreate, TodoResponse, TodoUpdate


class TodoService:
    """
    Service class for todo business operations.
    
    This class encapsulates all business logic related to todos,
    delegating data access to the TodoRepository. It acts as the
    coordinator between the API layer and data layer.
    
    Attributes:
        repository (TodoRepository): Data access layer for todos
    """
    
    def __init__(self, todo_repository: TodoRepository):
        """
        Initialize the service with a repository dependency.
        
        Args:
            todo_repository (TodoRepository): Repository for data access
        """
        self.repository = todo_repository

    def create_todo(self, payload: TodoCreate) -> TodoResponse:
        """
        Create a new todo item.
        
        Business logic:
        - Validates payload via Pydantic schema (done automatically)
        - Delegates creation to repository
        - Returns the created todo
        
        Args:
            payload (TodoCreate): Validated todo creation data
            
        Returns:
            TodoResponse: The newly created todo
        """
        # Delegate to repository for database operation
        todo = self.repository.createOne(
            title=payload.title, description=payload.description
        )
        # Return type is TodoResponse, Pydantic handles conversion
        return todo

    def get_todo(self, todo_id: uuid.UUID) -> TodoResponse | None:
        """
        Retrieve a single todo by ID.
        
        Business logic:
        - Fetches todo from repository
        - Raises 404 error if not found (business rule)
        
        Args:
            todo_id (UUID): The unique identifier of the todo
            
        Returns:
            TodoResponse: The requested todo
            
        Raises:
            HTTPException: 404 error if todo doesn't exist
        """
        # Fetch from repository
        todo = self.repository.fetchOne(todo_id)
        
        # Business rule: Non-existent todos should return 404
        if not todo:
            raise HTTPException(status_code=404, detail="Todo not found")
        
        return todo

    def get_todos(self) -> list[TodoResponse]:
        """
        Retrieve all todo items.
        
        Returns:
            list[TodoResponse]: List of all todos
        """
        # Fetch all todos from repository
        todos = self.repository.fetchAll()
        return todos

    def delete_todo(self, todo_id: uuid.UUID) -> None:
        """
        Delete a todo item by ID.
        
        Business logic:
        - Verifies todo exists (via get_todo)
        - Delegates deletion to repository
        
        Args:
            todo_id (UUID): The unique identifier of the todo to delete
            
        Returns:
            None
            
        Raises:
            HTTPException: 404 error if todo doesn't exist
        """
        # First verify the todo exists (will raise 404 if not found)
        todo = self.get_todo(todo_id)
        
        # Delegate deletion to repository
        self.repository.deleteOne(todo)

    def update_todo(self, todo_id: uuid.UUID, payload: TodoUpdate) -> TodoResponse:
        """
        Update an existing todo item.
        
        Business logic:
        - Verifies todo exists (via get_todo)
        - Extracts only provided fields (partial update support)
        - Delegates update to repository
        
        Args:
            todo_id (UUID): The unique identifier of the todo to update
            payload (TodoUpdate): Validated update data (partial)
            
        Returns:
            TodoResponse: The updated todo
            
        Raises:
            HTTPException: 404 error if todo doesn't exist
        """
        # Verify todo exists (will raise 404 if not found)
        todo = self.get_todo(todo_id)
        
        # Extract only the fields that were provided in the request
        # exclude_unset=True means only include fields explicitly set by client
        update_data = payload.model_dump(exclude_unset=True)
        
        # Delegate update to repository
        result = self.repository.updateOne(todo, update_data)
        
        return result
