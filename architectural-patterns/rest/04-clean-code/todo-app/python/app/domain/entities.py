"""
Domain Layer - Entities Module

This module defines the core business entities of the application.
Entities represent the business objects and encapsulate the enterprise business rules.
They are independent of any frameworks, databases, or external systems.

According to Clean Architecture principles, entities are at the center and should not
depend on anything else in the system.
"""

from dataclasses import dataclass, field
import uuid
from uuid import UUID


@dataclass
class TodoEntity:
    """
    TodoEntity represents a todo item in the domain model.
    
    This is a pure business object that encapsulates the core todo business logic.
    It contains no knowledge of databases, HTTP, or any external frameworks.
    
    Attributes:
        title: The title of the todo item (required)
        description: Optional detailed description of the todo
        completed: Boolean flag indicating if the todo is completed
        id: Unique identifier (UUID) for the todo item
    """
    title: str
    description: str | None = None
    completed: bool = False
    id: UUID = field(default_factory=uuid.uuid4)

    def mark_completed(self) -> None:
        """
        Mark this todo item as completed.
        
        This method encapsulates the business rule for completing a todo.
        """
        self.completed = True

    def update_title(self, new_title: str) -> None:
        """
        Update the title of this todo item.
        
        Args:
            new_title: The new title to set
            
        Raises:
            ValueError: If the new title is empty or contains only whitespace
            
        Business Rule: A todo must always have a non-empty title.
        """
        if not new_title.strip():
            raise ValueError("Title cannot be empty.")
        self.title = new_title
