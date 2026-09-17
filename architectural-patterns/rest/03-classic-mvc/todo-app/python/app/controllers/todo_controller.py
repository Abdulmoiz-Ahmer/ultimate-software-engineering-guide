"""
Controller - The "C" in MVC

This module implements the Controller for the Todo entity. In MVC architecture,
the Controller is the orchestrator that handles user requests, coordinates
between Model and View, and contains application logic.

Controller Responsibilities in MVC:
┌─────────────────────────────────────────────────────────────┐
│                    Controller Layer                          │
├─────────────────────────────────────────────────────────────┤
│  ✓ Handles HTTP requests (routing)                          │
│  ✓ Validates input (via Input Views)                        │
│  ✓ Implements business logic and rules                      │
│  ✓ Manipulates Models (CRUD operations)                     │
│  ✓ Selects appropriate View for response                    │
│  ✓ Handles errors and edge cases                            │
│  ✓ Orchestrates workflow between Model and View             │
└─────────────────────────────────────────────────────────────┘

MVC Flow in This Controller:
┌─────────────────────────────────────────────────────────────┐
│  HTTP Request                                                │
│       ↓                                                      │
│  Controller receives request                                 │
│       ↓                                                      │
│  Input View validates data                                   │
│       ↓                                                      │
│  Controller applies business logic                           │
│       ↓                                                      │
│  Controller manipulates Model (database)                     │
│       ↓                                                      │
│  Controller uses Output View to format response              │
│       ↓                                                      │
│  HTTP Response (JSON)                                        │
└─────────────────────────────────────────────────────────────┘

Key Principles:
- Controller knows about both Model and View
- Controller contains application/business logic
- Model and View remain independent of each other
- Controller is the "glue" that connects everything

In Classic MVC:
- Controller receives user input (form submissions, button clicks)
- Controller updates Model based on input
- Controller selects View template to render
- View displays updated Model data

In REST API MVC:
- Controller receives HTTP requests (JSON payloads)
- Controller updates Model (database operations)
- Controller uses View schemas for response serialization
- View (Pydantic) formats Model data as JSON
"""

from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.todo import TodoModel
from app.views.todo_view import (
    CreateTodoInputView,
    UpdateTodoInputView,
    TodoResponseView,
)

# Create API router for todo endpoints
# This router groups all todo-related controller actions
router = APIRouter(prefix="/todos", tags=["MVC Todos"])


@router.post("/", response_model=TodoResponseView, status_code=status.HTTP_201_CREATED)
def create_todo(payload: CreateTodoInputView, db: Session = Depends(get_db)):
    """
    Controller action to create a new todo.
    
    MVC Flow:
    1. [View] CreateTodoInputView validates incoming request
    2. [Controller] This function receives validated input
    3. [Controller] Applies business rules (validation logic)
    4. [Model] Creates and saves TodoModel to database
    5. [View] TodoResponseView formats the response
    
    Business Logic Example:
    - Validates that title doesn't contain forbidden words
    - This is application logic that belongs in Controller
    - Model handles data structure, View handles presentation
    - Controller handles the rules and workflow
    
    Args:
        payload (CreateTodoInputView): Validated input from user
        db (Session): Database session for Model operations
        
    Returns:
        TodoResponseView: The newly created todo (Model formatted as View)
        
    Raises:
        HTTPException: 400 if title contains forbidden words
        
    Controller Responsibilities Here:
    - Input validation (business rules)
    - Model creation and persistence
    - Response formatting (automatic via response_model)
    """
    # Business logic: Validate title content
    # This is controller logic, not Model or View concern
    if "forbidden" in payload.title.lower():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Title contains disallowed words.",
        )

    # Create Model from Input View data
    # Controller bridges View (input) and Model (storage)
    todo = TodoModel(title=payload.title, description=payload.description)
    
    # Persist Model to database
    db.add(todo)
    db.commit()
    db.refresh(todo)  # Get database-generated values
    
    # Return Model (Pydantic auto-converts to TodoResponseView)
    # Controller selects the Output View (response_model)
    return todo


@router.get("/{todo_id}", response_model=TodoResponseView)
def get_todo(todo_id: UUID, db: Session = Depends(get_db)):
    """
    Controller action to retrieve a single todo.
    
    MVC Flow:
    1. [Controller] Receives todo_id from URL path
    2. [Model] Queries database for TodoModel
    3. [Controller] Handles not found case (business logic)
    4. [View] TodoResponseView formats the response
    
    Args:
        todo_id (UUID): Unique identifier of the todo
        db (Session): Database session for Model query
        
    Returns:
        TodoResponseView: The requested todo (Model as View)
        
    Raises:
        HTTPException: 404 if todo not found
        
    Controller Responsibilities:
    - Coordinate Model retrieval
    - Handle error cases (404)
    - Select appropriate View for response
    """
    # Query Model from database
    todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
    
    # Business logic: Handle not found case
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo item not found."
        )
    
    # Return Model (formatted as TodoResponseView)
    return todo


@router.get("/", response_model=list[TodoResponseView])
def list_todos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Controller action to list todos with pagination.
    
    MVC Flow:
    1. [Controller] Receives pagination parameters
    2. [Model] Queries database with filters
    3. [View] List of TodoResponseView formats the response
    
    Args:
        skip (int): Number of records to skip (pagination offset)
        limit (int): Maximum records to return (page size)
        db (Session): Database session for Model query
        
    Returns:
        list[TodoResponseView]: List of todos (Models as Views)
        
    Controller Responsibilities:
    - Handle pagination parameters
    - Coordinate Model query
    - Select list View for response
    """
    # Query Models with pagination
    # Controller coordinates the query, Model handles data access
    return db.query(TodoModel).offset(skip).limit(limit).all()


@router.patch("/{todo_id}", response_model=TodoResponseView)
def update_todo(
    todo_id: UUID, payload: UpdateTodoInputView, db: Session = Depends(get_db)
):
    """
    Controller action to update an existing todo.
    
    MVC Flow:
    1. [View] UpdateTodoInputView validates incoming changes
    2. [Controller] Retrieves Model from database
    3. [Controller] Applies business logic (partial update)
    4. [Model] Updates database record
    5. [View] TodoResponseView formats updated todo
    
    Args:
        todo_id (UUID): Unique identifier of the todo to update
        payload (UpdateTodoInputView): Validated update data
        db (Session): Database session for Model operations
        
    Returns:
        TodoResponseView: The updated todo (Model as View)
        
    Raises:
        HTTPException: 404 if todo not found
        
    Controller Responsibilities:
    - Verify todo exists
    - Apply partial update logic (only update provided fields)
    - Persist changes to Model
    - Handle errors
    """
    # Query Model from database
    todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
    
    # Business logic: Handle not found case
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo item not found."
        )

    # Extract only provided fields from Input View
    # exclude_unset=True enables partial updates (PATCH semantics)
    # This is controller logic for handling updates
    update_data = payload.model_dump(exclude_unset=True)
    
    # Apply updates to Model
    # Controller coordinates the update process
    for key, value in update_data.items():
        setattr(todo, key, value)

    # Persist changes to database
    db.commit()
    db.refresh(todo)
    
    # Return updated Model (formatted as TodoResponseView)
    return todo


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: UUID, db: Session = Depends(get_db)):
    """
    Controller action to delete a todo.
    
    MVC Flow:
    1. [Controller] Receives todo_id to delete
    2. [Controller] Verifies Model exists
    3. [Model] Deletes from database
    4. [No View] 204 No Content response
    
    Args:
        todo_id (UUID): Unique identifier of the todo to delete
        db (Session): Database session for Model operations
        
    Returns:
        None (204 No Content status)
        
    Raises:
        HTTPException: 404 if todo not found
        
    Controller Responsibilities:
    - Verify todo exists before deletion
    - Coordinate Model deletion
    - Handle error cases
    - Return appropriate status code
    """
    # Query Model from database
    todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
    
    # Business logic: Handle not found case
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo item not found."
        )

    # Delete Model from database
    # Controller orchestrates the deletion
    db.delete(todo)
    db.commit()
    
    # No View needed for delete (204 No Content)
    # Controller decides not to return any data
