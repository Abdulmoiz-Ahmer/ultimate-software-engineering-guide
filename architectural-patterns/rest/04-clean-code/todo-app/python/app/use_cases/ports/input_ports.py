"""
Use Cases Layer - Input Ports Module

This module defines the input boundaries (ports) for the application's use cases.
Input ports represent the entry points into the use case layer, defining what
actions can be performed on the system.

Key concepts:
- Input DTOs: Data Transfer Objects that carry data from the controller to the use case
- Input Ports: Interfaces that define the contract for executing use cases

These ports follow the Dependency Inversion Principle - high-level use cases
define the interfaces, and low-level details (controllers) depend on them.
"""

from dataclasses import dataclass
from abc import ABC, abstractmethod
from uuid import UUID


@dataclass
class CreateTodoInputDTO:
    """
    Data Transfer Object for creating a new todo item.
    
    Attributes:
        title: The title of the new todo item
        description: Optional description for the todo item
    """
    title: str
    description: str | None = None


class ICreateTodoInputPort(ABC):
    """
    Interface defining the contract for creating a new todo item.
    
    This port represents the input boundary for the "Create Todo" use case.
    Controllers will depend on this interface to trigger the use case.
    """
    @abstractmethod
    def execute(self, input_dto: CreateTodoInputDTO) -> None:
        """
        Execute the create todo use case.
        
        Args:
            input_dto: The data needed to create a new todo item
        """
        pass


@dataclass
class ListTodosInputDTO:
    """
    Data Transfer Object for listing todo items with pagination.
    
    Attributes:
        skip: Number of items to skip (for pagination)
        limit: Maximum number of items to return
    """
    skip: int = 0
    limit: int = 100


class IListTodosInputPort(ABC):
    """
    Interface defining the contract for listing all todo items.
    
    This port represents the input boundary for the "List Todos" use case.
    """
    @abstractmethod
    def execute(self, input_dto: ListTodosInputDTO) -> None:
        """
        Execute the list todos use case.
        
        Args:
            input_dto: Pagination parameters for listing todos
        """
        pass


@dataclass
class DeleteTodoInputDTO:
    """
    Data Transfer Object for deleting a todo item.
    
    Attributes:
        todo_id: The unique identifier of the todo item to delete
    """
    todo_id: UUID


class IDeleteTodoInputPort(ABC):
    """
    Interface defining the contract for deleting a todo item.
    
    This port represents the input boundary for the "Delete Todo" use case.
    """
    @abstractmethod
    def execute(self, input_dto: DeleteTodoInputDTO) -> None:
        """
        Execute the delete todo use case.
        
        Args:
            input_dto: Contains the ID of the todo item to delete
        """
        pass


@dataclass
class GetTodoInputDTO:
    """
    Data Transfer Object for retrieving a single todo item.
    
    Attributes:
        todo_id: The unique identifier of the todo item to retrieve
    """
    todo_id: UUID


class IGetTodoInputPort(ABC):
    """
    Interface defining the contract for retrieving a single todo item.
    
    This port represents the input boundary for the "Get Todo" use case.
    """
    @abstractmethod
    def execute(self, input_dto: GetTodoInputDTO) -> None:
        """
        Execute the get todo use case.
        
        Args:
            input_dto: Contains the ID of the todo item to retrieve
        """
        pass


@dataclass
class UpdateTodoInputDTO:
    """
    Data Transfer Object for updating a todo item.
    
    All fields except todo_id are optional to support partial updates.
    
    Attributes:
        todo_id: The unique identifier of the todo item to update
        title: Optional new title for the todo item
        description: Optional new description for the todo item
        completed: Optional new completion status
    """
    todo_id: UUID
    title: str | None = None
    description: str | None = None
    completed: bool | None = None


class IUpdateTodoInputPort(ABC):
    """
    Interface defining the contract for updating a todo item.
    
    This port represents the input boundary for the "Update Todo" use case.
    Supports partial updates - only provided fields will be updated.
    """
    @abstractmethod
    def execute(self, input_dto: UpdateTodoInputDTO) -> None:
        """
        Execute the update todo use case.
        
        Args:
            input_dto: Contains the ID and fields to update for the todo item
        """
        pass
