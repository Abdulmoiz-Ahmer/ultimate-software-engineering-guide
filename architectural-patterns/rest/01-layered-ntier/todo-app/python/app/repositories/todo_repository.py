"""
Todo Repository - Data Access Layer

This module implements the Repository pattern, providing an abstraction layer
between the business logic and data access. It encapsulates all database
operations for Todo entities, allowing the service layer to work with
domain objects without knowing SQL or ORM details.

Benefits of Repository Pattern:
- Separates data access logic from business logic
- Makes it easier to test business logic (can mock repository)
- Centralizes data access code for easier maintenance
- Provides a clean API for data operations
"""

from sqlalchemy.orm import Session
from starlette.exceptions import HTTPException
from app.models.todo import TodoModel
from uuid import UUID


class TodoRepository:
    """
    Repository for Todo data access operations.
    
    This class handles all database CRUD operations for todos,
    providing a clean interface for the service layer. It follows
    the Repository pattern to abstract database details.
    
    Attributes:
        db (Session): SQLAlchemy database session
    """
    
    def __init__(self, db: Session):
        """
        Initialize the repository with a database session.
        
        Args:
            db (Session): SQLAlchemy session for database operations
        """
        self.db = db

    def createOne(self, title: str, description: str | None) -> TodoModel:
        """
        Create a new todo item in the database.
        
        This method creates a new TodoModel instance, adds it to the session,
        commits the transaction, and refreshes the object to get database-generated
        values (like the UUID).
        
        Args:
            title (str): The todo item's title
            description (str | None): Optional description
            
        Returns:
            TodoModel: The newly created todo with all fields populated
        """
        # Create a new TodoModel instance (id and completed are auto-generated)
        todo = TodoModel(title=title, description=description)
        
        # Add to session (stages the insert)
        self.db.add(todo)
        
        # Commit transaction (executes the INSERT)
        self.db.commit()
        
        # Refresh to get database-generated values (UUID, defaults)
        self.db.refresh(todo)
        
        return todo

    def fetchOne(self, todo_id: UUID) -> TodoModel | None:
        """
        Fetch a single todo by its ID.
        
        Args:
            todo_id (UUID): The unique identifier of the todo
            
        Returns:
            TodoModel | None: The todo if found, None otherwise
        """
        # Query the database for a todo with the given ID
        # .first() returns the first result or None if not found
        todo = self.db.query(TodoModel).filter(TodoModel.id == todo_id).first()
        return todo
    
    def updateOne(self, todo: TodoModel, update_data: dict) -> TodoModel:
        """
        Update an existing todo item with new data.
        
        This method uses setattr to dynamically update only the fields
        present in update_data, enabling partial updates (PATCH semantics).
        
        Args:
            todo (TodoModel): The todo instance to update
            update_data (dict): Dictionary of field names and new values
            
        Returns:
            TodoModel: The updated todo with changes persisted to database
        """
        # Iterate through update_data and set each attribute on the model
        for key, value in update_data.items():
            setattr(todo, key, value)
        
        # Commit the changes to database
        self.db.commit()
        
        # Refresh to get any database-level changes
        self.db.refresh(todo)
        
        return todo

    def fetchAll(self) -> list[TodoModel]:
        """
        Fetch all todo items from the database.
        
        Returns:
            list[TodoModel]: List of all todos in the database
        """
        # Query all todos without any filter
        todos = self.db.query(TodoModel).all()
        return todos

    def deleteOne(self, todo: TodoModel) -> None:
        """
        Delete a todo item from the database.
        
        Args:
            todo (TodoModel): The todo instance to delete
            
        Returns:
            None
        """
        # Mark the todo for deletion
        self.db.delete(todo)
        
        # Commit to execute the DELETE statement
        self.db.commit()
