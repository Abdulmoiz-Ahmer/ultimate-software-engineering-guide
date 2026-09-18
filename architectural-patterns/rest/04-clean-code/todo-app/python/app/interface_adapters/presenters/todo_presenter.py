"""
Interface Adapters Layer - Todo Presenters Module

This module implements the output port interfaces for presenting use case results.
Presenters are responsible for formatting data from use cases into a form suitable
for delivery (e.g., HTTP responses, CLI output, etc.).

Key responsibilities:
- Implement output port interfaces defined by use cases
- Convert domain entities to output DTOs
- Store presentation state (success data, error messages, not found flags)
- Remain independent of specific delivery mechanisms (HTTP, GraphQL, etc.)

Presenters follow the Single Responsibility Principle - they only format data,
they don't handle HTTP status codes or response delivery (that's the controller's job).
"""

from app.domain.entities import TodoEntity
from app.use_cases.ports.output_ports import (
    ICreateTodoOutputPort,
    IDeleteTodoOutputPort,
    IGetTodoOutputPort,
    IListTodosOutputPort,
    IUpdateTodoOutputPort,
    TodoOutputDTO,
)
from uuid import UUID


class CreateTodoPresenter(ICreateTodoOutputPort):
    """
    Presenter for the Create Todo use case.
    
    Formats the result of creating a todo for presentation.
    Stores the response data or error message for the controller to retrieve.
    """
    
    def __init__(self):
        """Initialize the presenter with empty state."""
        self.response_data: TodoOutputDTO | None = None
        self.error_message: str | None = None

    def present_success(self, todo: TodoEntity) -> None:
        """
        Format a successful todo creation for presentation.
        
        Converts the domain entity to a presentation DTO.
        
        Args:
            todo: The newly created todo entity
        """
        self.response_data = TodoOutputDTO(
            id=todo.id,
            title=todo.title,
            description=todo.description,
            completed=todo.completed,
        )

    def present_error(self, message: str) -> None:
        """
        Store an error message for presentation.
        
        Args:
            message: Human-readable error message
        """
        self.error_message = message


class ListTodosPresenter(IListTodosOutputPort):
    """
    Presenter for the List Todos use case.
    
    Formats a list of todos for presentation.
    """
    
    def __init__(self):
        """Initialize the presenter with empty state."""
        self.response_data: list[TodoOutputDTO] = []
        self.error_message: str | None = None

    def present_success(self, todos: list[TodoEntity]) -> None:
        """
        Format a successful todo list for presentation.
        
        Converts a list of domain entities to presentation DTOs.
        
        Args:
            todos: List of todo entities to present
        """
        self.response_data = [
            TodoOutputDTO(
                id=todo.id,
                title=todo.title,
                description=todo.description,
                completed=todo.completed,
            )
            for todo in todos
        ]

    def present_error(self, message: str) -> None:
        """
        Store an error message for presentation.
        
        Args:
            message: Human-readable error message
        """
        self.error_message = message


class DeleteTodoPresenter(IDeleteTodoOutputPort):
    """
    Presenter for the Delete Todo use case.
    
    Tracks the outcome of a delete operation (success, not found, or error).
    """
    
    def __init__(self):
        """Initialize the presenter with empty state."""
        self.is_success: bool = False
        self.is_not_found: bool = False
        self.error_message: str | None = None

    def present_success(self) -> None:
        """
        Mark the delete operation as successful.
        
        No data needs to be returned for a successful deletion.
        """
        self.is_success = True

    def present_not_found(self, todo_id: UUID) -> None:
        """
        Mark the todo as not found.
        
        Args:
            todo_id: The ID of the todo that was not found
        """
        self.is_not_found = True

    def present_error(self, message: str) -> None:
        """
        Store an error message for presentation.
        
        Args:
            message: Human-readable error message
        """
        self.error_message = message


class GetTodoPresenter(IGetTodoOutputPort):
    """
    Presenter for the Get Todo use case.
    
    Formats a single todo for presentation and handles not found cases.
    """
    
    def __init__(self):
        """Initialize the presenter with empty state."""
        self.response_data: TodoOutputDTO | None = None
        self.is_not_found: bool = False
        self.error_message: str | None = None

    def present_success(self, todo: TodoEntity) -> None:
        """
        Format a successfully retrieved todo for presentation.
        
        Converts the domain entity to a presentation DTO.
        
        Args:
            todo: The retrieved todo entity
        """
        self.response_data = TodoOutputDTO(
            id=todo.id,
            title=todo.title,
            description=todo.description,
            completed=todo.completed,
        )

    def present_not_found(self, todo_id: UUID) -> None:
        """
        Mark the todo as not found.
        
        Args:
            todo_id: The ID of the todo that was not found
        """
        self.is_not_found = True

    def present_error(self, message: str) -> None:
        """
        Store an error message for presentation.
        
        Args:
            message: Human-readable error message
        """
        self.error_message = message


class UpdateTodoPresenter(IUpdateTodoOutputPort):
    """
    Presenter for the Update Todo use case.
    
    Formats the updated todo for presentation and handles not found cases.
    """
    
    def __init__(self):
        """Initialize the presenter with empty state."""
        self.response_data: TodoOutputDTO | None = None
        self.is_not_found: bool = False
        self.error_message: str | None = None

    def present_success(self, todo: TodoEntity) -> None:
        """
        Format a successfully updated todo for presentation.
        
        Converts the domain entity to a presentation DTO.
        
        Args:
            todo: The updated todo entity
        """
        self.response_data = TodoOutputDTO(
            id=todo.id,
            title=todo.title,
            description=todo.description,
            completed=todo.completed,
        )

    def present_not_found(self, todo_id: UUID) -> None:
        """
        Mark the todo as not found.
        
        Args:
            todo_id: The ID of the todo that was not found
        """
        self.is_not_found = True

    def present_error(self, message: str) -> None:
        """
        Store an error message for presentation.
        
        Args:
            message: Human-readable error message
        """
        self.error_message = message
