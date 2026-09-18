"""
Interface Adapters Layer - Todo Gateway Module

This module implements the gateway interface for todo data persistence.
The gateway acts as an adapter between the use case layer and the database layer,
translating between domain entities and database models.

Key responsibilities:
- Implement the ITodoGateway interface defined by the use case layer
- Convert between TodoEntity (domain) and TodoORM (database model)
- Execute database operations using SQLAlchemy

This follows the Adapter pattern - adapting the SQLAlchemy API to match
the interface expected by the use cases.
"""

from uuid import UUID
from sqlalchemy.orm import Session
from app.domain.entities import TodoEntity
from app.use_cases.ports.gateway_ports import ITodoGateway
from app.frameworks_and_drivers.database.models import TodoORM


class SqlAlchemyTodoGateway(ITodoGateway):
    """
    SQLAlchemy implementation of the todo gateway.
    
    This class adapts the SQLAlchemy ORM to implement the ITodoGateway interface.
    It handles the conversion between domain entities (TodoEntity) and
    database models (TodoORM).
    
    Attributes:
        db: SQLAlchemy database session for executing queries
    """
    
    def __init__(self, db: Session):
        """
        Initialize the gateway with a database session.
        
        Args:
            db: SQLAlchemy session for database operations
        """
        self.db = db

    def _to_entity(self, orm: TodoORM) -> TodoEntity:
        """
        Convert a database model (ORM) to a domain entity.
        
        This private method isolates the conversion logic, keeping the domain
        layer independent of database concerns.
        
        Args:
            orm: TodoORM instance from the database
            
        Returns:
            TodoEntity with data from the ORM model
        """
        return TodoEntity(
            id=orm.id,
            title=orm.title,
            description=orm.description,
            completed=orm.completed,
        )

    def save(self, todo: TodoEntity) -> TodoEntity:
        """
        Save (create or update) a todo entity in the database.
        
        If a todo with the same ID exists, it updates the existing record.
        Otherwise, it creates a new record.
        
        Args:
            todo: The todo entity to save
            
        Returns:
            The saved todo entity (with any database-generated values)
        """
        # Check if the todo already exists
        orm_item = self.db.query(TodoORM).filter(TodoORM.id == todo.id).first()
        
        if orm_item:
            # Update existing record
            orm_item.title = todo.title
            orm_item.description = todo.description
            orm_item.completed = todo.completed
        else:
            # Create new record
            orm_item = TodoORM(
                id=todo.id,
                title=todo.title,
                description=todo.description,
                completed=todo.completed,
            )
            self.db.add(orm_item)
        
        # Commit the transaction
        self.db.commit()
        # Refresh to get any database-generated values
        self.db.refresh(orm_item)
        
        # Convert back to entity and return
        return self._to_entity(orm_item)

    def get_all(self, skip: int = 0, limit: int = 100) -> list[TodoEntity]:
        """
        Retrieve all todo entities with pagination.
        
        Args:
            skip: Number of records to skip (for pagination)
            limit: Maximum number of records to return
            
        Returns:
            List of todo entities
        """
        # Query with pagination
        orm_items = self.db.query(TodoORM).offset(skip).limit(limit).all()
        
        # Convert all ORM models to entities
        return [self._to_entity(item) for item in orm_items]

    def get_by_id(self, todo_id: UUID) -> TodoEntity | None:
        """
        Retrieve a single todo entity by its ID.
        
        Args:
            todo_id: The unique identifier of the todo
            
        Returns:
            The todo entity if found, None otherwise
        """
        # Query by ID
        orm_item = self.db.query(TodoORM).filter(TodoORM.id == todo_id).first()
        
        # Convert to entity if found, otherwise return None
        return self._to_entity(orm_item) if orm_item else None

    def delete(self, todo_id: UUID) -> bool:
        """
        Delete a todo entity by its ID.
        
        Args:
            todo_id: The unique identifier of the todo to delete
            
        Returns:
            True if the todo was deleted, False if it was not found
        """
        # Find the todo to delete
        orm_item = self.db.query(TodoORM).filter(TodoORM.id == todo_id).first()
        
        if not orm_item:
            # Todo not found
            return False

        # Delete the todo
        self.db.delete(orm_item)
        self.db.commit()
        
        return True
