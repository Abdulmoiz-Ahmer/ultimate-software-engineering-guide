"""
Todo Module - API Router

This module defines the HTTP endpoints (routes) for the Todos domain.
The router layer is responsible for:
- HTTP request/response handling
- Route definitions and URL patterns
- Request validation (via Pydantic schemas)
- Dependency injection
- HTTP status codes

In a modular monolith:
- Each module exposes its own router
- Routers are registered in the main application
- Route handlers delegate business logic to services
"""

from uuid import UUID
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.modules.todos.schemas import CreateTodoRequest, UpdateTodoRequest, TodoResponse
from app.modules.todos.service import TodoService

# Create a router with a prefix and tags for OpenAPI documentation
router = APIRouter(prefix="/todos", tags=["Todos Module"])


def get_service(db: Session = Depends(get_db)) -> TodoService:
    """
    Service dependency factory.
    
    Creates a TodoService instance with the database session.
    This is used for dependency injection in route handlers.
    
    Args:
        db (Session): Database session from get_db dependency
        
    Returns:
        TodoService: Initialized service instance
    """
    return TodoService(db)


@router.post("/", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
def create_todo(
    payload: CreateTodoRequest, service: TodoService = Depends(get_service)
):
    """
    Create a new todo item.
    
    Endpoint: POST /todos/
    
    Args:
        payload (CreateTodoRequest): Todo creation data from request body
        service (TodoService): Injected service instance
        
    Returns:
        TodoResponse: The created todo item
        
    Status Codes:
        201: Todo successfully created
        400: Invalid request data or business rule violation
    """
    return service.create_todo(payload)


@router.get("/{todo_id}", response_model=TodoResponse)
def get_todo(todo_id: UUID, service: TodoService = Depends(get_service)):
    """
    Retrieve a single todo by ID.
    
    Endpoint: GET /todos/{todo_id}
    
    Args:
        todo_id (UUID): Unique identifier from URL path
        service (TodoService): Injected service instance
        
    Returns:
        TodoResponse: The requested todo item
        
    Status Codes:
        200: Todo found and returned
        404: Todo not found
    """
    return service.get_todo(todo_id)


@router.get("/", response_model=list[TodoResponse])
def list_todos(
    skip: int = 0, limit: int = 100, service: TodoService = Depends(get_service)
):
    """
    List todos with pagination.
    
    Endpoint: GET /todos/?skip=0&limit=100
    
    Args:
        skip (int): Number of records to skip (default: 0)
        limit (int): Maximum number of records to return (default: 100)
        service (TodoService): Injected service instance
        
    Returns:
        list[TodoResponse]: List of todo items
        
    Status Codes:
        200: Todos retrieved successfully
    """
    return service.list_todos(skip=skip, limit=limit)


@router.patch("/{todo_id}", response_model=TodoResponse)
def update_todo(
    todo_id: UUID,
    payload: UpdateTodoRequest,
    service: TodoService = Depends(get_service),
):
    """
    Update an existing todo item (partial update).
    
    Endpoint: PATCH /todos/{todo_id}
    
    Supports partial updates - only fields provided in the request
    will be updated.
    
    Args:
        todo_id (UUID): Unique identifier from URL path
        payload (UpdateTodoRequest): Fields to update from request body
        service (TodoService): Injected service instance
        
    Returns:
        TodoResponse: The updated todo item
        
    Status Codes:
        200: Todo updated successfully
        404: Todo not found
    """
    return service.update_todo(todo_id, payload)


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: UUID, service: TodoService = Depends(get_service)):
    """
    Delete a todo item.
    
    Endpoint: DELETE /todos/{todo_id}
    
    Args:
        todo_id (UUID): Unique identifier from URL path
        service (TodoService): Injected service instance
        
    Returns:
        None: 204 No Content response
        
    Status Codes:
        204: Todo deleted successfully
        404: Todo not found
    """
    service.delete_todo(todo_id)
