"""
Frameworks and Drivers Layer - Web Routes Module

This module defines the FastAPI routes (HTTP endpoints) for the todo API.
It's the entry point for HTTP requests and serves as the composition root
where all dependencies are wired together.

Key responsibilities:
- Define HTTP endpoints (routes) and their request/response contracts
- Wire together all the layers: database, gateway, interactors, controller
- Handle dependency injection via FastAPI's Depends()
- Map HTTP requests to controller methods
- Convert controller responses to HTTP responses

This is the outermost layer in Clean Architecture - it depends on everything
else but nothing depends on it. Changing from FastAPI to another web framework
would only require changes in this layer.
"""

from fastapi import APIRouter, Depends, status
from uuid import UUID
from sqlalchemy.orm import Session
from app.frameworks_and_drivers.database.database import get_db
from app.frameworks_and_drivers.web.schemas import (
    CreateTodoHTTPPayload,
    TodoHTTPResponse,
    UpdateTodoHTTPPayload,
)
from app.interface_adapters.gateways.todo_gateway import SqlAlchemyTodoGateway
from app.interface_adapters.controllers.todo_controller import TodoController
from app.use_cases.interactors import (
    CreateTodoInteractor,
    DeleteTodoInteractor,
    GetTodoInteractor,
    ListTodosInteractor,
    UpdateTodoInteractor,
)

# Create an API router for todo endpoints
# All routes will be prefixed with /todos
router = APIRouter(prefix="/todos", tags=["Clean Architecture Todos"])


def get_controller(db: Session = Depends(get_db)) -> TodoController:
    """
    Dependency injection function for creating a configured TodoController.
    
    This function serves as the composition root - it wires together all the
    dependencies needed for the application to run:
    1. Creates a gateway with the database session
    2. Creates factory functions for each interactor
    3. Creates and returns a controller with all the factories
    
    This approach ensures:
    - Each request gets its own gateway (tied to a DB session)
    - Each use case execution gets its own interactor (with a unique presenter)
    - All dependencies follow the Dependency Inversion Principle
    
    Args:
        db: Database session (injected by FastAPI)
        
    Returns:
        TodoController configured with all necessary dependencies
    """
    # Create the gateway (data access layer)
    gateway = SqlAlchemyTodoGateway(db)

    # Define factory functions for creating interactors
    # Each factory takes a presenter and returns an interactor
    # This allows each request to have its own presenter instance
    
    def create_interactor_factory(presenter):
        """Factory for creating CreateTodoInteractor with the given presenter."""
        return CreateTodoInteractor(gateway=gateway, output_port=presenter)

    def get_interactor_factory(presenter):
        """Factory for creating GetTodoInteractor with the given presenter."""
        return GetTodoInteractor(gateway=gateway, output_port=presenter)

    def list_interactor_factory(presenter):
        """Factory for creating ListTodosInteractor with the given presenter."""
        return ListTodosInteractor(gateway=gateway, output_port=presenter)

    def update_interactor_factory(presenter):
        """Factory for creating UpdateTodoInteractor with the given presenter."""
        return UpdateTodoInteractor(gateway=gateway, output_port=presenter)

    def delete_interactor_factory(presenter):
        """Factory for creating DeleteTodoInteractor with the given presenter."""
        return DeleteTodoInteractor(gateway=gateway, output_port=presenter)

    # Create and return the controller with all the factories
    return TodoController(
        create_interactor_factory=create_interactor_factory,
        get_interactor_factory=get_interactor_factory,
        list_interactor_factory=list_interactor_factory,
        update_interactor_factory=update_interactor_factory,
        delete_interactor_factory=delete_interactor_factory,
    )


@router.post("/", response_model=TodoHTTPResponse, status_code=status.HTTP_201_CREATED)
def create_todo(
    payload: CreateTodoHTTPPayload,
    controller: TodoController = Depends(get_controller),
):
    """
    Create a new todo item.
    
    HTTP Method: POST
    Endpoint: /todos/
    Status Code: 201 Created (on success)
    
    Args:
        payload: Request body containing title and optional description
        controller: Injected TodoController instance
        
    Returns:
        The newly created todo item
        
    Raises:
        HTTPException 400: If validation fails (e.g., forbidden words in title)
    """
    return controller.create_todo(title=payload.title, description=payload.description)


@router.get("/", response_model=list[TodoHTTPResponse])
def list_todos(
    skip: int = 0,
    limit: int = 100,
    controller: TodoController = Depends(get_controller),
):
    """
    List all todo items with pagination.
    
    HTTP Method: GET
    Endpoint: /todos/?skip=0&limit=100
    
    Query Parameters:
        skip: Number of items to skip (default: 0)
        limit: Maximum number of items to return (default: 100)
        
    Args:
        skip: Pagination offset
        limit: Pagination limit
        controller: Injected TodoController instance
        
    Returns:
        List of todo items
        
    Raises:
        HTTPException 500: If an error occurs during retrieval
    """
    return controller.list_todos(skip=skip, limit=limit)


@router.get("/{todo_id}", response_model=TodoHTTPResponse)
def get_todo(
    todo_id: UUID,
    controller: TodoController = Depends(get_controller),
):
    """
    Retrieve a single todo item by ID.
    
    HTTP Method: GET
    Endpoint: /todos/{todo_id}
    
    Path Parameters:
        todo_id: UUID of the todo to retrieve
        
    Args:
        todo_id: The unique identifier of the todo
        controller: Injected TodoController instance
        
    Returns:
        The requested todo item
        
    Raises:
        HTTPException 404: If the todo is not found
        HTTPException 500: If an error occurs during retrieval
    """
    return controller.get_todo(todo_id=todo_id)


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(
    todo_id: UUID,
    controller: TodoController = Depends(get_controller),
):
    """
    Delete a todo item by ID.
    
    HTTP Method: DELETE
    Endpoint: /todos/{todo_id}
    Status Code: 204 No Content (on success)
    
    Path Parameters:
        todo_id: UUID of the todo to delete
        
    Args:
        todo_id: The unique identifier of the todo
        controller: Injected TodoController instance
        
    Returns:
        No content (empty response body)
        
    Raises:
        HTTPException 404: If the todo is not found
        HTTPException 500: If an error occurs during deletion
    """
    controller.delete_todo(todo_id=todo_id)


@router.patch("/{todo_id}", response_model=TodoHTTPResponse)
def update_todo(
    todo_id: UUID,
    payload: UpdateTodoHTTPPayload,
    controller: TodoController = Depends(get_controller),
):
    """
    Update a todo item (supports partial updates).
    
    HTTP Method: PATCH
    Endpoint: /todos/{todo_id}
    
    Path Parameters:
        todo_id: UUID of the todo to update
        
    Request Body (all fields optional):
        title: New title for the todo
        description: New description for the todo
        completed: New completion status
        
    Args:
        todo_id: The unique identifier of the todo
        payload: Request body containing fields to update
        controller: Injected TodoController instance
        
    Returns:
        The updated todo item
        
    Raises:
        HTTPException 400: If validation fails (e.g., empty title)
        HTTPException 404: If the todo is not found
    """
    return controller.update_todo(
        todo_id=todo_id,
        title=payload.title,
        description=payload.description,
        completed=payload.completed,
    )
