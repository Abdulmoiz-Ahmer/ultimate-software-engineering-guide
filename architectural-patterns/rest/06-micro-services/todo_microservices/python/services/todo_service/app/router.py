"""
API Routes for Todo Service

This module defines the FastAPI router and HTTP endpoints for the Todo service.
It handles incoming HTTP requests and delegates business logic to the service layer.

Endpoints:
    - POST /todos/: Create a new todo item
    - DELETE /todos/{todo_id}: Delete a todo by ID

Database initialization happens on module load.
"""

from uuid import UUID
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from todo_service.app.database import get_db, Base, engine
from todo_service.app.schemas import CreateTodoRequest, TodoResponse
from todo_service.app.service import TodoService

# Auto-create database tables on startup
# This ensures the todos table exists before handling requests
Base.metadata.create_all(bind=engine)

# Create API router with common prefix and tags
router = APIRouter(prefix="/todos", tags=["Todos Microservice"])


@router.post("/", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
def create_todo(payload: CreateTodoRequest, db: Session = Depends(get_db)):
    """
    Create a new todo item.
    
    This endpoint:
    1. Validates the incoming request payload
    2. Creates a new todo in the database
    3. Sends an audit event to the Audit service
    4. Returns the created todo with generated ID
    
    Args:
        payload (CreateTodoRequest): Todo data (title and optional description)
        db (Session): Database session (injected dependency)
    
    Returns:
        TodoResponse: The created todo item with all fields
    
    Status Codes:
        - 201: Todo created successfully
        - 422: Validation error (invalid payload)
    
    Example Request:
        POST /todos/
        {
            "title": "Learn microservices",
            "description": "Study inter-service communication patterns"
        }
    
    Example Response:
        {
            "id": "123e4567-e89b-12d3-a456-426614174000",
            "title": "Learn microservices",
            "description": "Study inter-service communication patterns",
            "completed": false
        }
    """
    return TodoService(db).create_todo(payload)


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: UUID, db: Session = Depends(get_db)):
    """
    Delete a todo item by ID.
    
    This endpoint:
    1. Validates the UUID format
    2. Finds the todo in the database
    3. Deletes it if found
    4. Sends an audit event to the Audit service
    
    Args:
        todo_id (UUID): Unique identifier of the todo to delete
        db (Session): Database session (injected dependency)
    
    Returns:
        None (204 No Content on success)
    
    Status Codes:
        - 204: Todo deleted successfully
        - 404: Todo not found
        - 422: Invalid UUID format
    
    Example Request:
        DELETE /todos/123e4567-e89b-12d3-a456-426614174000
    """
    TodoService(db).delete_todo(todo_id)
