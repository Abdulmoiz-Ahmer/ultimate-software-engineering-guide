"""
Todo Component - API Router

This module defines the HTTP API endpoints for the Todo component.
It represents the entry point for all todo-related HTTP requests and
implements the routing layer of the component.

Component Architecture:
┌─────────────────────────────────────────────────────────────┐
│                    Todo Component                            │
├─────────────────────────────────────────────────────────────┤
│  router.py (this file)     → HTTP layer (routes)            │
│  handlers.py               → Business logic (CQRS)          │
│  schemas.py                → Data contracts (DTOs/Commands)  │
│  models.py                 → Database models (ORM)          │
└─────────────────────────────────────────────────────────────┘

Unidirectional Data Flow:
  HTTP Request → Router → Handler/Query → Model → Database
                    ↓
  HTTP Response ← DTO ← Handler/Query ← Model ← Database

Router Responsibilities:
- Define HTTP endpoints and methods
- Handle request/response serialization
- Inject dependencies (database session)
- Delegate business logic to handlers
- Map HTTP status codes to outcomes
- NO business logic (thin routing layer)

Key Principles:
- Routes are thin adapters between HTTP and domain logic
- All business logic lives in handlers
- Routes only know about HTTP concerns
- Handlers don't know about HTTP concerns
"""

from uuid import UUID
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.components.todos.schemas import CreateTodoCommand, UpdateTodoCommand, TodoDTO
from app.components.todos.handlers import (
    CreateTodoHandler,
    GetTodoQuery,
    ListTodosQuery,
    UpdateTodoHandler,
    DeleteTodoHandler,
)

# Create component-specific router
# All routes are prefixed with "/todos" and tagged for API documentation
router = APIRouter(prefix="/todos", tags=["Todos Component"])


@router.post("/", response_model=TodoDTO, status_code=status.HTTP_201_CREATED)
def create_todo(command: CreateTodoCommand, db: Session = Depends(get_db)):
    """
    Create a new todo item.
    
    HTTP Method: POST
    Endpoint: /todos/
    Status: 201 Created
    
    This endpoint receives a CreateTodoCommand, validates it via Pydantic,
    and delegates the creation logic to CreateTodoHandler.
    
    Args:
        command (CreateTodoCommand): Validated todo creation data
        db (Session): Database session injected by FastAPI
        
    Returns:
        TodoDTO: The newly created todo with generated ID
        
    Request Body Example:
        {
            "title": "Buy groceries",
            "description": "Milk, eggs, bread"
        }
        
    Response Example:
        {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "title": "Buy groceries",
            "description": "Milk, eggs, bread",
            "completed": false
        }
    """
    return CreateTodoHandler.execute(db, command)


@router.get("/{todo_id}", response_model=TodoDTO)
def get_todo(todo_id: UUID, db: Session = Depends(get_db)):
    """
    Retrieve a single todo by ID.
    
    HTTP Method: GET
    Endpoint: /todos/{todo_id}
    Status: 200 OK (or 404 Not Found)
    
    This endpoint fetches a specific todo using its UUID identifier.
    If the todo doesn't exist, the handler raises a 404 error.
    
    Args:
        todo_id (UUID): The unique identifier of the todo
        db (Session): Database session injected by FastAPI
        
    Returns:
        TodoDTO: The requested todo
        
    Raises:
        HTTPException: 404 if todo not found
        
    Response Example:
        {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "title": "Buy groceries",
            "description": "Milk, eggs, bread",
            "completed": false
        }
    """
    return GetTodoQuery.execute(db, todo_id)


@router.get("/", response_model=list[TodoDTO])
def list_todos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve a paginated list of todos.
    
    HTTP Method: GET
    Endpoint: /todos/
    Status: 200 OK
    
    This endpoint supports pagination through skip and limit query parameters.
    It delegates to ListTodosQuery which handles the database query.
    
    Args:
        skip (int): Number of records to skip (default: 0)
        limit (int): Maximum records to return (default: 100)
        db (Session): Database session injected by FastAPI
        
    Returns:
        list[TodoDTO]: List of todos (may be empty)
        
    Query Parameters:
        ?skip=0&limit=10
        
    Response Example:
        [
            {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "title": "Buy groceries",
                "description": "Milk, eggs, bread",
                "completed": false
            },
            {
                "id": "550e8400-e29b-41d4-a716-446655440001",
                "title": "Write code",
                "description": null,
                "completed": true
            }
        ]
    """
    return ListTodosQuery.execute(db, skip=skip, limit=limit)


@router.patch("/{todo_id}", response_model=TodoDTO)
def update_todo(
    todo_id: UUID, command: UpdateTodoCommand, db: Session = Depends(get_db)
):
    """
    Update an existing todo (partial update).
    
    HTTP Method: PATCH
    Endpoint: /todos/{todo_id}
    Status: 200 OK (or 404 Not Found)
    
    This endpoint supports partial updates using PATCH semantics.
    Only fields provided in the request body are updated; others remain unchanged.
    The handler validates that the todo exists before attempting updates.
    
    Args:
        todo_id (UUID): The unique identifier of the todo to update
        command (UpdateTodoCommand): Partial update data (all fields optional)
        db (Session): Database session injected by FastAPI
        
    Returns:
        TodoDTO: The updated todo with all current values
        
    Raises:
        HTTPException: 404 if todo not found
        
    Request Body Example (partial update):
        {
            "completed": true
        }
        
    Response Example:
        {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "title": "Buy groceries",
            "description": "Milk, eggs, bread",
            "completed": true
        }
    """
    return UpdateTodoHandler.execute(db, todo_id, command)


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: UUID, db: Session = Depends(get_db)):
    """
    Delete a todo item.
    
    HTTP Method: DELETE
    Endpoint: /todos/{todo_id}
    Status: 204 No Content (or 404 Not Found)
    
    This endpoint permanently deletes a todo. The handler first verifies
    the todo exists before attempting deletion. On success, returns no content.
    
    Args:
        todo_id (UUID): The unique identifier of the todo to delete
        db (Session): Database session injected by FastAPI
        
    Returns:
        None (204 No Content status code)
        
    Raises:
        HTTPException: 404 if todo not found
        
    Response: Empty body with 204 status
    """
    DeleteTodoHandler.execute(db, todo_id)
