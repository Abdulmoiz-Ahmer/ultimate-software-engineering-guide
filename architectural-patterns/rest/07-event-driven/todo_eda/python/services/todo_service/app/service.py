# services/todo_service/app/service.py
"""
Todo Service Business Logic

This module contains the core business logic for todo operations.
It handles database transactions and publishes events to the message broker
when todos are created or deleted.
"""

from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from services.todo_service.app.models import TodoORM
from services.todo_service.app.schemas import CreateTodoRequest
from services.todo_service.app.broker.publisher import EventPublisher
from shared.events import TodoCreatedEvent, TodoDeletedEvent


class TodoService:
    """
    Service class for todo operations.
    
    Encapsulates the business logic for creating and deleting todos,
    including database operations and event publishing.
    
    Attributes:
        db: SQLAlchemy database session for database operations
    """
    
    def __init__(self, db: Session):
        """
        Initialize the TodoService with a database session.
        
        Args:
            db: SQLAlchemy database session
        """
        self.db = db

    async def create_todo(self, payload: CreateTodoRequest) -> TodoORM:
        """
        Create a new todo item.
        
        Creates a todo in the database and publishes a TodoCreatedEvent
        to notify other services of the creation.
        
        Args:
            payload: CreateTodoRequest containing todo title and description
        
        Returns:
            TodoORM: The newly created todo object with generated ID
        
        Side Effects:
            - Inserts a new record into the todos table
            - Publishes a TodoCreatedEvent to the message broker
        """
        # Create new todo instance and persist to database
        todo = TodoORM(title=payload.title, description=payload.description)
        self.db.add(todo)
        self.db.commit()
        self.db.refresh(todo)

        # Emit TodoCreatedEvent asynchronously to the message broker
        event = TodoCreatedEvent(
            todo_id=todo.id,
            title=todo.title,
            description=todo.description,
        )
        await EventPublisher.publish(event)
        return todo

    async def delete_todo(self, todo_id: UUID) -> None:
        """
        Delete an existing todo item.
        
        Removes a todo from the database and publishes a TodoDeletedEvent
        to notify other services of the deletion.
        
        Args:
            todo_id: UUID of the todo to delete
        
        Raises:
            HTTPException: 404 error if the todo with given ID is not found
        
        Side Effects:
            - Deletes the record from the todos table
            - Publishes a TodoDeletedEvent to the message broker
        """
        # Query for the todo item
        todo = self.db.query(TodoORM).filter(TodoORM.id == todo_id).first()
        if not todo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found."
            )

        # Delete the todo from database
        self.db.delete(todo)
        self.db.commit()

        # Emit TodoDeletedEvent asynchronously to the message broker
        event = TodoDeletedEvent(todo_id=todo_id)
        await EventPublisher.publish(event)
