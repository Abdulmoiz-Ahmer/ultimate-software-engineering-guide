"""
Todo Component - Command Handlers and Query Handlers

This module implements the business logic for the Todo component using
the Command/Query Responsibility Segregation (CQRS) pattern.

CQRS Pattern:
┌─────────────────────────────────────────────────────────────┐
│                    CQRS Architecture                         │
├─────────────────────────────────────────────────────────────┤
│  Commands (Write)          |    Queries (Read)              │
│  - Modify state            |    - Read state                │
│  - Return result           |    - Never modify              │
│  - Can be async            |    - Fast reads                │
│  - Validation heavy        |    - Optimized queries         │
└─────────────────────────────────────────────────────────────┘

Handler Responsibilities:
1. Receive validated input (Command/Query)
2. Execute business logic
3. Interact with database (Model)
4. Return standardized output (DTO)

Key Principles:
- Each handler has a single responsibility (SRP)
- Handlers are stateless (static methods)
- Unidirectional data flow: Input → Logic → Output
- No cross-handler dependencies (loose coupling)
- Database operations encapsulated within handlers

Benefits:
✓ Easy to test (each handler is isolated)
✓ Easy to understand (one handler = one operation)
✓ Easy to modify (changes are localized)
✓ Easy to optimize (queries vs commands separately)
"""

from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.components.todos.models import TodoModel
from app.components.todos.schemas import CreateTodoCommand, TodoDTO


class CreateTodoHandler:
    """
    Command Handler for creating a new todo.
    
    Responsibility: Handle the creation of a new todo item
    Input: CreateTodoCommand (validated by Pydantic)
    Output: TodoDTO (newly created todo)
    
    Flow:
    1. Receive validated command
    2. Create new TodoModel instance
    3. Persist to database
    4. Return DTO representation
    """
    
    @staticmethod
    def execute(db: Session, command: CreateTodoCommand) -> TodoDTO:
        """
        Execute the create todo command.
        
        Args:
            db (Session): Database session
            command (CreateTodoCommand): Validated creation command
            
        Returns:
            TodoDTO: The newly created todo
            
        Business Rules:
        - Title is required (enforced by schema)
        - Completed defaults to False
        - ID is auto-generated (UUID)
        """
        # Create new todo model from command
        todo = TodoModel(
            title=command.title, 
            description=command.description, 
            completed=False
        )
        
        # Persist to database
        db.add(todo)
        db.commit()
        db.refresh(todo)  # Get database-generated values
        
        # Return as DTO (Pydantic converts automatically)
        return todo


class GetTodoQuery:
    """
    Query Handler for retrieving a single todo by ID.
    
    Responsibility: Fetch a specific todo item
    Input: todo_id (UUID)
    Output: TodoDTO (the requested todo)
    
    Flow:
    1. Query database by ID
    2. Raise 404 if not found
    3. Return DTO representation
    """
    
    @staticmethod
    def execute(db: Session, todo_id: str) -> TodoDTO:
        """
        Execute the get todo query.
        
        Args:
            db (Session): Database session
            todo_id (str): UUID of the todo to retrieve
            
        Returns:
            TodoDTO: The requested todo
            
        Raises:
            HTTPException: 404 if todo not found
            
        Business Rules:
        - Must return exact match by ID
        - Non-existent IDs result in 404 error
        """
        # Query database for todo
        todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
        
        # Business rule: Todo must exist
        if not todo:
            raise HTTPException(
                status_code=404, 
                detail=f"Todo with id {todo_id} not found"
            )
        
        # Return as DTO
        return todo


class ListTodosQuery:
    """
    Query Handler for retrieving a list of todos.
    
    Responsibility: Fetch multiple todos with pagination
    Input: skip (offset), limit (page size)
    Output: list[TodoDTO] (list of todos)
    
    Flow:
    1. Query database with pagination
    2. Return list of DTOs
    
    Note: This is a read-only operation that never modifies state.
    """
    
    @staticmethod
    def execute(db: Session, skip: int = 0, limit: int = 100) -> list[TodoDTO]:
        """
        Execute the list todos query.
        
        Args:
            db (Session): Database session
            skip (int): Number of records to skip (offset)
            limit (int): Maximum number of records to return
            
        Returns:
            list[TodoDTO]: List of todos (may be empty)
            
        Business Rules:
        - Supports pagination via skip/limit
        - Default limit prevents excessive data transfer
        - Returns empty list if no todos exist
        """
        # Query with pagination
        return db.query(TodoModel).offset(skip).limit(limit).all()


class UpdateTodoHandler:
    """
    Command Handler for updating an existing todo.
    
    Responsibility: Handle partial updates to a todo item
    Input: todo_id (UUID), UpdateTodoCommand (fields to update)
    Output: TodoDTO (updated todo)
    
    Flow:
    1. Verify todo exists (via GetTodoQuery)
    2. Apply updates to model
    3. Persist changes
    4. Return updated DTO
    """
    
    @staticmethod
    def execute(db: Session, todo_id: str, command: CreateTodoCommand) -> TodoDTO:
        """
        Execute the update todo command.
        
        Args:
            db (Session): Database session
            todo_id (str): UUID of the todo to update
            command (CreateTodoCommand): Update command with new values
            
        Returns:
            TodoDTO: The updated todo
            
        Raises:
            HTTPException: 404 if todo not found
            
        Business Rules:
        - Todo must exist (reuses GetTodoQuery)
        - Supports partial updates (only provided fields)
        - Unset fields remain unchanged
        """
        # First verify todo exists (will raise 404 if not found)
        todo = GetTodoQuery.execute(db, todo_id)
        
        # Extract only the fields that were provided
        # exclude_unset=True means only include explicitly set fields
        update_data = command.model_dump(exclude_unset=True)
        
        # Apply updates to the model
        for field, value in update_data.items():
            setattr(todo, field, value)
        
        # Persist changes
        db.commit()
        db.refresh(todo)
        
        # Return updated DTO
        return todo


class DeleteTodoHandler:
    """
    Command Handler for deleting a todo.
    
    Responsibility: Handle deletion of a todo item
    Input: todo_id (UUID)
    Output: None (no content on success)
    
    Flow:
    1. Verify todo exists (via GetTodoQuery)
    2. Delete from database
    3. Commit transaction
    """
    
    @staticmethod
    def execute(db: Session, todo_id: str) -> None:
        """
        Execute the delete todo command.
        
        Args:
            db (Session): Database session
            todo_id (str): UUID of the todo to delete
            
        Returns:
            None
            
        Raises:
            HTTPException: 404 if todo not found
            
        Business Rules:
        - Todo must exist before deletion (reuses GetTodoQuery)
        - Deletion is permanent (no soft delete)
        - Returns nothing on success (204 No Content)
        """
        # First verify todo exists (will raise 404 if not found)
        todo = GetTodoQuery.execute(db, todo_id)
        
        # Delete from database
        db.delete(todo)
        db.commit()
