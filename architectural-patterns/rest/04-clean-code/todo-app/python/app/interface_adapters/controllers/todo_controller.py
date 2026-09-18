"""
Interface Adapters Layer - Todo Controller Module

This module implements the controller for handling todo operations.
The controller acts as the entry point for incoming requests, coordinating
between the web layer, use cases, and presenters.

Key responsibilities:
- Receive input from the web layer (routes)
- Create presenters for capturing use case output
- Execute use cases via interactors
- Interpret presenter state and translate to HTTP exceptions
- Return formatted responses

The controller follows the Controller pattern in Clean Architecture,
sitting in the interface adapters layer and orchestrating the flow of
data between the outer layers (web) and inner layers (use cases).
"""

from uuid import UUID

from fastapi import HTTPException, status
from app.use_cases.ports.input_ports import (
    CreateTodoInputDTO,
    DeleteTodoInputDTO,
    GetTodoInputDTO,
    ListTodosInputDTO,
    UpdateTodoInputDTO,
)
from app.use_cases.ports.output_ports import TodoOutputDTO
from app.interface_adapters.presenters.todo_presenter import (
    CreateTodoPresenter,
    DeleteTodoPresenter,
    GetTodoPresenter,
    ListTodosPresenter,
    UpdateTodoPresenter,
)


class TodoController:
    """
    Controller for coordinating todo operations.
    
    This controller receives requests from the web layer, executes use cases,
    and translates presentation state into HTTP responses/exceptions.
    
    The controller uses factory functions to create interactors because each
    request needs its own presenter instance to capture the output.
    
    Attributes:
        create_interactor_factory: Factory function for creating CreateTodoInteractor
        get_interactor_factory: Factory function for creating GetTodoInteractor
        list_interactor_factory: Factory function for creating ListTodosInteractor
        update_interactor_factory: Factory function for creating UpdateTodoInteractor
        delete_interactor_factory: Factory function for creating DeleteTodoInteractor
    """
    
    def __init__(
        self,
        create_interactor_factory,
        get_interactor_factory,
        list_interactor_factory,
        update_interactor_factory,
        delete_interactor_factory,
    ):
        """
        Initialize the controller with interactor factories.
        
        Args:
            create_interactor_factory: Callable that takes a presenter and returns a CreateTodoInteractor
            get_interactor_factory: Callable that takes a presenter and returns a GetTodoInteractor
            list_interactor_factory: Callable that takes a presenter and returns a ListTodosInteractor
            update_interactor_factory: Callable that takes a presenter and returns an UpdateTodoInteractor
            delete_interactor_factory: Callable that takes a presenter and returns a DeleteTodoInteractor
        """
        self.create_interactor_factory = create_interactor_factory
        self.get_interactor_factory = get_interactor_factory
        self.list_interactor_factory = list_interactor_factory
        self.update_interactor_factory = update_interactor_factory
        self.delete_interactor_factory = delete_interactor_factory

    def list_todos(self, skip: int = 0, limit: int = 100) -> list[TodoOutputDTO]:
        """
        List all todo items with pagination.
        
        Args:
            skip: Number of items to skip (for pagination)
            limit: Maximum number of items to return
            
        Returns:
            List of todo output DTOs
            
        Raises:
            HTTPException: If an error occurs during retrieval (500)
        """
        # Create a presenter to capture the output
        presenter = ListTodosPresenter()
        
        # Create an interactor with the presenter
        interactor = self.list_interactor_factory(presenter)

        # Execute the use case
        interactor.execute(ListTodosInputDTO(skip=skip, limit=limit))

        # Interpret the presenter state and handle errors
        if presenter.error_message:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=presenter.error_message,
            )
            
        # Return the successful response data
        return presenter.response_data

    def create_todo(self, title: str, description: str | None) -> TodoOutputDTO:
        """
        Create a new todo item.
        
        Args:
            title: Title of the new todo
            description: Optional description
            
        Returns:
            The created todo as an output DTO
            
        Raises:
            HTTPException: If validation fails or an error occurs (400)
        """
        # Create a presenter to capture the output
        presenter = CreateTodoPresenter()
        
        # Create an interactor with the presenter
        interactor = self.create_interactor_factory(presenter)

        # Create input DTO and execute the use case
        input_dto = CreateTodoInputDTO(title=title, description=description)
        interactor.execute(input_dto)

        # Interpret the presenter state and handle errors
        if presenter.error_message:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=presenter.error_message
            )
            
        # Return the successful response data
        return presenter.response_data

    def delete_todo(self, todo_id: UUID) -> None:
        """
        Delete a todo item by ID.
        
        Args:
            todo_id: The unique identifier of the todo to delete
            
        Raises:
            HTTPException: If todo not found (404) or an error occurs (500)
        """
        # Create a presenter to capture the output
        presenter = DeleteTodoPresenter()
        
        # Create an interactor with the presenter
        interactor = self.delete_interactor_factory(presenter)

        # Execute the use case
        interactor.execute(DeleteTodoInputDTO(todo_id=todo_id))

        # Interpret the presenter state and handle different outcomes
        if presenter.is_not_found:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Todo item with ID '{todo_id}' was not found.",
            )
        if presenter.error_message:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=presenter.error_message,
            )
        
        # Success - no return value for delete operations

    def get_todo(self, todo_id: UUID) -> TodoOutputDTO:
        """
        Retrieve a single todo item by ID.
        
        Args:
            todo_id: The unique identifier of the todo to retrieve
            
        Returns:
            The todo as an output DTO
            
        Raises:
            HTTPException: If todo not found (404) or an error occurs (500)
        """
        # Create a presenter to capture the output
        presenter = GetTodoPresenter()
        
        # Create an interactor with the presenter
        interactor = self.get_interactor_factory(presenter)

        # Execute the use case
        interactor.execute(GetTodoInputDTO(todo_id=todo_id))

        # Interpret the presenter state and handle different outcomes
        if presenter.is_not_found:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Todo item with ID '{todo_id}' was not found.",
            )
        if presenter.error_message:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=presenter.error_message,
            )
            
        # Return the successful response data
        return presenter.response_data

    def update_todo(
        self,
        todo_id: UUID,
        title: str | None,
        description: str | None,
        completed: bool | None,
    ) -> TodoOutputDTO:
        """
        Update a todo item (supports partial updates).
        
        Args:
            todo_id: The unique identifier of the todo to update
            title: Optional new title
            description: Optional new description
            completed: Optional new completion status
            
        Returns:
            The updated todo as an output DTO
            
        Raises:
            HTTPException: If todo not found (404), validation fails (400),
                          or an error occurs (500)
        """
        # Create a presenter to capture the output
        presenter = UpdateTodoPresenter()
        
        # Create an interactor with the presenter
        interactor = self.update_interactor_factory(presenter)

        # Create input DTO and execute the use case
        input_dto = UpdateTodoInputDTO(
            todo_id=todo_id, title=title, description=description, completed=completed
        )
        interactor.execute(input_dto)

        # Interpret the presenter state and handle different outcomes
        if presenter.is_not_found:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Todo item with ID '{todo_id}' was not found.",
            )
        if presenter.error_message:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=presenter.error_message,
            )
            
        # Return the successful response data
        return presenter.response_data
