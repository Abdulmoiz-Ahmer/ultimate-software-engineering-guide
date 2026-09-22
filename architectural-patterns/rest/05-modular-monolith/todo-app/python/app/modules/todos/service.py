"""
Todo Module - Business Logic Service

This module contains the business logic layer for the Todos domain.
The service layer encapsulates all business rules, validations, and
data access operations.

Service Layer Responsibilities:
- Business logic and validation
- Database operations through ORM
- Exception handling and error messages
- Transaction management

In a modular monolith, services:
- Are the primary interface for business operations
- Keep business logic separate from HTTP concerns
- Can be reused by other modules through the public interface
"""

from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.modules.todos.models import TodoORM
from app.modules.todos.schemas import CreateTodoRequest, UpdateTodoRequest


class TodoService:
    """
    Todo Service Class
    
    Encapsulates all business logic for managing todo items.
    This service is injected into route handlers via dependency injection.
    
    Attributes:
        db (Session): SQLAlchemy database session
    """
    
    def __init__(self, db: Session):
        """
        Initialize the service with a database session.
        
        Args:
            db (Session): SQLAlchemy database session
        """
        self.db = db

    def create_todo(self, payload: CreateTodoRequest) -> TodoORM:
        """
        Create a new todo item.
        
        Business rules:
        - Title cannot contain the word "forbidden"
        - Title and description are validated by the schema
        
        Args:
            payload (CreateTodoRequest): Todo creation data
            
        Returns:
            TodoORM: The created todo item
            
        Raises:
            HTTPException: If title contains disallowed words
        """
        # Business validation: check for forbidden words
        if "forbidden" in payload.title.lower():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Title contains disallowed words.",
            )
        
        # Create new todo instance
        todo = TodoORM(title=payload.title, description=payload.description)
        
        # Persist to database
        self.db.add(todo)
        self.db.commit()
        self.db.refresh(todo)  # Refresh to get generated fields like ID
        
        return todo

    def get_todo(self, todo_id: UUID) -> TodoORM:
        """
        Retrieve a single todo by ID.
        
        Args:
            todo_id (UUID): Unique identifier of the todo
            
        Returns:
            TodoORM: The requested todo item
            
        Raises:
            HTTPException: If todo is not found (404)
        """
        todo = self.db.query(TodoORM).filter(TodoORM.id == todo_id).first()
        
        if not todo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Todo item not found."
            )
        
        return todo

    def list_todos(self, skip: int = 0, limit: int = 100) -> list[TodoORM]:
        """
        List todos with pagination.
        
        Supports pagination through skip and limit parameters to handle
        large datasets efficiently.
        
        Args:
            skip (int): Number of records to skip (for pagination)
            limit (int): Maximum number of records to return
            
        Returns:
            list[TodoORM]: List of todo items
        """
        return self.db.query(TodoORM).offset(skip).limit(limit).all()

    def update_todo(self, todo_id: UUID, payload: UpdateTodoRequest) -> TodoORM:
        """
        Update an existing todo item.
        
        Supports partial updates - only fields provided in the payload
        will be updated. Uses Pydantic's exclude_unset to ignore fields
        that weren't provided in the request.
        
        Args:
            todo_id (UUID): Unique identifier of the todo to update
            payload (UpdateTodoRequest): Fields to update
            
        Returns:
            TodoORM: The updated todo item
            
        Raises:
            HTTPException: If todo is not found (404)
        """
        # Retrieve existing todo (raises 404 if not found)
        todo = self.get_todo(todo_id)
        
        # Get only the fields that were explicitly set in the request
        update_data = payload.model_dump(exclude_unset=True)
        
        # Apply updates to the model
        for key, value in update_data.items():
            setattr(todo, key, value)
        
        # Commit changes to database
        self.db.commit()
        self.db.refresh(todo)
        
        return todo

    def delete_todo(self, todo_id: UUID) -> None:
        """
        Delete a todo item.
        
        Args:
            todo_id (UUID): Unique identifier of the todo to delete
            
        Raises:
            HTTPException: If todo is not found (404)
        """
        # Retrieve existing todo (raises 404 if not found)
        todo = self.get_todo(todo_id)
        
        # Delete from database
        self.db.delete(todo)
        self.db.commit()
