"""
Use Cases Layer - Output Ports Module

This module defines the output boundaries (ports) for the application's use cases.
Output ports represent how use cases communicate their results back to the outside world.

Key concepts:
- Output DTOs: Data Transfer Objects that carry data from use cases to presenters
- Output Ports: Interfaces that define how use cases present their results

Following the Dependency Inversion Principle, use cases define these output interfaces,
and presenters (in the interface adapters layer) implement them. This keeps use cases
independent of presentation details.
"""

from dataclasses import dataclass
from uuid import UUID
from abc import ABC, abstractmethod
from app.domain.entities import TodoEntity


@dataclass
class TodoOutputDTO:
    """
    Data Transfer Object for representing a todo item in the output.
    
    This DTO is used to transfer todo data from the use case layer
    to the presentation layer, keeping the domain entity isolated.
    
    Attributes:
        id: Unique identifier of the todo item
        title: Title of the todo item
        description: Optional description
        completed: Completion status
    """
    id: UUID
    title: str
    description: str | None
    completed: bool


class ICreateTodoOutputPort(ABC):
    """
    Output port interface for the Create Todo use case.
    
    Defines how the create todo use case presents its results.
    Presenters implement this interface to format and deliver the response.
    """
    @abstractmethod
    def present_success(self, todo: TodoEntity) -> None:
        """
        Present a successful todo creation.
        
        Args:
            todo: The newly created todo entity
        """
        pass

    @abstractmethod
    def present_error(self, message: str) -> None:
        """
        Present an error that occurred during todo creation.
        
        Args:
            message: Human-readable error message
        """
        pass


class IListTodosOutputPort(ABC):
    """
    Output port interface for the List Todos use case.
    
    Defines how the list todos use case presents its results.
    """
    @abstractmethod
    def present_success(self, todos: list[TodoEntity]) -> None:
        """
        Present a successful list of todos.
        
        Args:
            todos: List of todo entities retrieved from the system
        """
        pass

    @abstractmethod
    def present_error(self, message: str) -> None:
        """
        Present an error that occurred during todo retrieval.
        
        Args:
            message: Human-readable error message
        """
        pass


class IDeleteTodoOutputPort(ABC):
    """
    Output port interface for the Delete Todo use case.
    
    Defines how the delete todo use case presents its results.
    """
    @abstractmethod
    def present_success(self) -> None:
        """
        Present a successful todo deletion.
        
        No data is returned for a successful deletion, just confirmation.
        """
        pass

    @abstractmethod
    def present_not_found(self, todo_id: UUID) -> None:
        """
        Present a "not found" error when the todo doesn't exist.
        
        Args:
            todo_id: The ID of the todo that was not found
        """
        pass

    @abstractmethod
    def present_error(self, message: str) -> None:
        """
        Present an error that occurred during todo deletion.
        
        Args:
            message: Human-readable error message
        """
        pass


class IGetTodoOutputPort(ABC):
    """
    Output port interface for the Get Todo use case.
    
    Defines how the get todo use case presents its results.
    """
    @abstractmethod
    def present_success(self, todo: TodoEntity) -> None:
        """
        Present a successfully retrieved todo.
        
        Args:
            todo: The todo entity that was retrieved
        """
        pass

    @abstractmethod
    def present_not_found(self, todo_id: UUID) -> None:
        """
        Present a "not found" error when the todo doesn't exist.
        
        Args:
            todo_id: The ID of the todo that was not found
        """
        pass

    @abstractmethod
    def present_error(self, message: str) -> None:
        """
        Present an error that occurred during todo retrieval.
        
        Args:
            message: Human-readable error message
        """
        pass


class IUpdateTodoOutputPort(ABC):
    """
    Output port interface for the Update Todo use case.
    
    Defines how the update todo use case presents its results.
    """
    @abstractmethod
    def present_success(self, todo: TodoEntity) -> None:
        """
        Present a successfully updated todo.
        
        Args:
            todo: The updated todo entity
        """
        pass

    @abstractmethod
    def present_not_found(self, todo_id: UUID) -> None:
        """
        Present a "not found" error when the todo doesn't exist.
        
        Args:
            todo_id: The ID of the todo that was not found
        """
        pass

    @abstractmethod
    def present_error(self, message: str) -> None:
        """
        Present an error that occurred during todo update.
        
        Args:
            message: Human-readable error message
        """
        pass
