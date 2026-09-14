"""
API Routes - Presentation/API Layer

This module defines the HTTP REST API endpoints for the todo application.
It represents the Presentation Layer (API Layer) in the N-tier architecture,
handling HTTP requests/responses and delegating business logic to the service layer.

Architecture Flow:
1. Client sends HTTP request
2. FastAPI validates request using Pydantic schemas
3. Route handler receives validated data
4. Dependencies inject required services (via Depends)
5. Service layer processes business logic
6. Response is serialized and returned to client

This layer is responsible for:
- HTTP routing and method handling (GET, POST, PATCH, DELETE)
- Request/response serialization
- Dependency injection
- HTTP status codes
- No business logic (delegated to service layer)
"""

from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.schemas import TodoCreate, TodoResponse, TodoUpdate
from app.database import get_db
from app.repositories.todo_repository import TodoRepository
from app.services.todo_service import TodoService

# Create an API router with prefix and tags for organization
# All routes will be prefixed with "/todos" and grouped under "Todos" in OpenAPI docs
router = APIRouter(prefix="/todos", tags=["Todos"])


def get_todo_service(db: Session = Depends(get_db)) -> TodoService:
    """
    Dependency injection function for TodoService.
    
    This function creates a fully initialized TodoService with all its
    dependencies (repository and database session). FastAPI's dependency
    injection system will call this automatically for any route that needs it.
    
    Args:
        db (Session): Database session injected by FastAPI (via get_db)
        
    Returns:
        TodoService: Fully initialized service with repository
        
    Dependency Chain:
        get_db() -> TodoRepository(db) -> TodoService(repository)
    """
    return TodoService(todo_repository=TodoRepository(db=db))


@router.post("/", response_model=TodoResponse, status_code=201)
async def create_todo(
    payload: TodoCreate, service: TodoService = Depends(get_todo_service)
) -> TodoResponse:
    """
    Create a new todo item.
    
    HTTP Method: POST
    Endpoint: /todos/
    Status Code: 201 Created
    
    Request Body:
        {
            "title": "Buy groceries",
            "description": "Milk, eggs, bread"
        }
    
    Response Body:
        {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "title": "Buy groceries",
            "description": "Milk, eggs, bread",
            "completed": false
        }
    
    Args:
        payload (TodoCreate): Validated todo creation data from request body
        service (TodoService): Injected service instance
        
    Returns:
        TodoResponse: The newly created todo with generated ID
    """
    return service.create_todo(payload=payload)


@router.get("/{id}", response_model=TodoResponse, status_code=200)
async def get_todo(
    id: UUID, service: TodoService = Depends(get_todo_service)
) -> TodoResponse:
    """
    Retrieve a single todo by ID.
    
    HTTP Method: GET
    Endpoint: /todos/{id}
    Status Code: 200 OK (or 404 if not found)
    
    Path Parameters:
        id (UUID): The unique identifier of the todo
    
    Response Body:
        {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "title": "Buy groceries",
            "description": "Milk, eggs, bread",
            "completed": false
        }
    
    Args:
        id (UUID): Todo ID from URL path parameter
        service (TodoService): Injected service instance
        
    Returns:
        TodoResponse: The requested todo
        
    Raises:
        HTTPException: 404 if todo not found (raised by service layer)
    """
    return service.get_todo(todo_id=id)


@router.delete("/{id}", status_code=204)
async def delete_todo(id: UUID, service: TodoService = Depends(get_todo_service)):
    """
    Delete a todo item by ID.
    
    HTTP Method: DELETE
    Endpoint: /todos/{id}
    Status Code: 204 No Content (or 404 if not found)
    
    Path Parameters:
        id (UUID): The unique identifier of the todo to delete
    
    Response: No content (empty body)
    
    Args:
        id (UUID): Todo ID from URL path parameter
        service (TodoService): Injected service instance
        
    Returns:
        None (FastAPI returns 204 with empty body)
        
    Raises:
        HTTPException: 404 if todo not found (raised by service layer)
    """
    service.delete_todo(todo_id=id)


@router.get("/", response_model=list[TodoResponse], status_code=200)
async def get_todos(service: TodoService = Depends(get_todo_service)):
    """
    Retrieve all todo items.
    
    HTTP Method: GET
    Endpoint: /todos/
    Status Code: 200 OK
    
    Response Body:
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
    
    Args:
        service (TodoService): Injected service instance
        
    Returns:
        list[TodoResponse]: List of all todos (empty list if none exist)
    """
    return service.get_todos()


@router.patch("/{id}", response_model=TodoResponse, status_code=200)
async def update_todo(
    id: UUID, payload: TodoUpdate, service: TodoService = Depends(get_todo_service)
) -> TodoResponse:
    """
    Update an existing todo item (partial update).
    
    HTTP Method: PATCH
    Endpoint: /todos/{id}
    Status Code: 200 OK (or 404 if not found)
    
    Path Parameters:
        id (UUID): The unique identifier of the todo to update
    
    Request Body (all fields optional):
        {
            "title": "Buy groceries and cook dinner",
            "completed": true
        }
    
    Response Body:
        {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "title": "Buy groceries and cook dinner",
            "description": "Milk, eggs, bread",
            "completed": true
        }
    
    PATCH semantics:
    - Only provided fields are updated
    - Omitted fields remain unchanged
    - Supports partial updates (unlike PUT which requires full replacement)
    
    Args:
        id (UUID): Todo ID from URL path parameter
        payload (TodoUpdate): Validated update data (partial)
        service (TodoService): Injected service instance
        
    Returns:
        TodoResponse: The updated todo with all current values
        
    Raises:
        HTTPException: 404 if todo not found (raised by service layer)
    """
    return service.update_todo(todo_id=id, payload=payload)
