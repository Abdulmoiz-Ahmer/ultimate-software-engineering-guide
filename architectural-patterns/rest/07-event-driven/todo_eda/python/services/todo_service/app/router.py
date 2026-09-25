# services/todo_service/app/router.py
"""
Todo Service API Routes

This module defines the REST API endpoints for the Todo Service.
It handles HTTP requests and delegates business logic to the TodoService.
"""

from uuid import UUID
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from services.todo_service.app.database import get_db, Base, engine
from services.todo_service.app.schemas import CreateTodoRequest, TodoResponse
from services.todo_service.app.service import TodoService

# Ensure all database tables are created on module import
Base.metadata.create_all(bind=engine)

# Initialize API router with common prefix and tags for OpenAPI documentation
router = APIRouter(prefix="/todos", tags=["Todos Producer"])


@router.post("/", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
async def create_todo(payload: CreateTodoRequest, db: Session = Depends(get_db)):
    """
    Create a new todo item.
    
    Creates a todo with the provided title and optional description.
    Upon successful creation, publishes a TodoCreatedEvent for consumption
    by subscriber services.
    
    Args:
        payload: CreateTodoRequest containing todo data
        db: Database session (injected dependency)
    
    Returns:
        TodoResponse: The created todo with all fields including generated ID
    
    Status Codes:
        201: Todo successfully created
        422: Validation error in request payload
    """
    return await TodoService(db).create_todo(payload)


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(todo_id: UUID, db: Session = Depends(get_db)):
    """
    Delete an existing todo item.
    
    Removes the todo with the specified ID from the database.
    Upon successful deletion, publishes a TodoDeletedEvent for consumption
    by subscriber services.
    
    Args:
        todo_id: UUID of the todo to delete
        db: Database session (injected dependency)
    
    Returns:
        None (204 No Content on success)
    
    Status Codes:
        204: Todo successfully deleted
        404: Todo with specified ID not found
        422: Invalid UUID format
    """
    await TodoService(db).delete_todo(todo_id)
