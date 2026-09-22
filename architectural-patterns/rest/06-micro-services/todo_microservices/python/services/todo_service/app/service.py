"""
Business Logic for Todo Service

This module contains the business logic layer for managing todo items.
It handles database operations and coordinates with the Audit service
to log events.

Classes:
    - TodoService: Core service class for todo operations
"""

from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from todo_service.app.models import TodoORM
from todo_service.app.schemas import CreateTodoRequest
from todo_service.app.clients.audit_client import AuditServiceClient


class TodoService:
    """
    Service layer for Todo operations.
    
    This class encapsulates the business logic for managing todo items,
    including database operations and inter-service communication.
    
    Attributes:
        db (Session): SQLAlchemy database session
    """
    
    def __init__(self, db: Session):
        """
        Initialize the TodoService with a database session.
        
        Args:
            db (Session): SQLAlchemy database session for data persistence
        """
        self.db = db

    def create_todo(self, payload: CreateTodoRequest) -> TodoORM:
        """
        Create a new todo item and log the event.
        
        This method:
        1. Creates a new todo item in the database
        2. Sends an audit event to the Audit microservice
        
        Args:
            payload (CreateTodoRequest): Todo creation data (title, description)
        
        Returns:
            TodoORM: The created todo item with generated ID
        
        Example:
            service = TodoService(db)
            todo = service.create_todo(CreateTodoRequest(
                title="Buy milk",
                description="From the grocery store"
            ))
        """
        # Create new todo ORM instance
        todo = TodoORM(title=payload.title, description=payload.description)
        
        # Persist to database
        self.db.add(todo)
        self.db.commit()
        self.db.refresh(todo)  # Refresh to get generated ID

        # Trigger network call to Audit microservice
        # This demonstrates inter-service communication in microservices architecture
        AuditServiceClient.send_audit_event(
            event_type="TODO_CREATED",
            resource_id=str(todo.id),
            message=f"Created todo item '{todo.title}'",
        )
        return todo

    def delete_todo(self, todo_id: UUID) -> None:
        """
        Delete a todo item by ID and log the event.
        
        This method:
        1. Finds the todo by ID
        2. Deletes it from the database
        3. Sends an audit event to the Audit microservice
        
        Args:
            todo_id (UUID): The unique identifier of the todo to delete
        
        Raises:
            HTTPException: 404 if todo with given ID is not found
        
        Example:
            service = TodoService(db)
            service.delete_todo(uuid.UUID("123e4567-e89b-12d3-a456-426614174000"))
        """
        # Query for the todo item
        todo = self.db.query(TodoORM).filter(TodoORM.id == todo_id).first()
        
        # Raise 404 if not found
        if not todo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found."
            )

        # Delete from database
        self.db.delete(todo)
        self.db.commit()

        # Trigger network call to Audit microservice
        AuditServiceClient.send_audit_event(
            event_type="TODO_DELETED",
            resource_id=str(todo_id),
            message=f"Deleted todo item ID {todo_id}",
        )
