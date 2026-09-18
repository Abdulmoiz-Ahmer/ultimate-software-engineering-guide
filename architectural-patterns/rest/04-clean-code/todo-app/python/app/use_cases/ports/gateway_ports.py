"""
Use Cases Layer - Gateway Ports Module

This module defines the gateway interfaces (ports) for data access.
Gateway ports represent the boundary between the use case layer and data persistence.

Following the Dependency Inversion Principle:
- Use cases (high-level policy) define the gateway interfaces they need
- Gateways (low-level details) in the interface adapters layer implement these interfaces

This allows use cases to remain independent of database technology, ORM frameworks,
or any other persistence mechanism.
"""

from abc import ABC, abstractmethod
from uuid import UUID
from app.domain.entities import TodoEntity


class ITodoGateway(ABC):
    """
    Gateway interface for todo data persistence operations.
    
    This interface defines the contract for storing and retrieving todo entities.
    Implementations in the interface adapters layer will handle the actual
    database interactions using specific technologies (SQLAlchemy, MongoDB, etc.).
    
    The use case layer depends only on this interface, not on any concrete implementation.
    """
    
    @abstractmethod
    def save(self, todo: TodoEntity) -> TodoEntity:
        """
        Save (create or update) a todo entity.
        
        If a todo with the same ID already exists, it should be updated.
        Otherwise, a new todo should be created.
        
        Args:
            todo: The todo entity to save
            
        Returns:
            The saved todo entity (may include updated timestamps, etc.)
        """
        pass

    @abstractmethod
    def get_by_id(self, todo_id: UUID) -> TodoEntity | None:
        """
        Retrieve a todo entity by its unique identifier.
        
        Args:
            todo_id: The unique identifier of the todo
            
        Returns:
            The todo entity if found, None otherwise
        """
        pass

    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> list[TodoEntity]:
        """
        Retrieve all todo entities with pagination support.
        
        Args:
            skip: Number of items to skip (for pagination)
            limit: Maximum number of items to return
            
        Returns:
            List of todo entities
        """
        pass

    @abstractmethod
    def delete(self, todo_id: UUID) -> bool:
        """
        Delete a todo entity by its unique identifier.
        
        Args:
            todo_id: The unique identifier of the todo to delete
            
        Returns:
            True if the todo was deleted, False if the todo was not found
        """
        pass
