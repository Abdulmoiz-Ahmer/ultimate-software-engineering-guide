"""
Use Cases Layer - Interactors Module

This module contains the actual use case implementations (interactors).
Interactors orchestrate the flow of data and business logic to accomplish specific use cases.

Each interactor:
1. Implements an input port interface (defining what it does)
2. Uses a gateway port (for data access)
3. Uses an output port (for presenting results)

Interactors contain application-specific business rules and coordinate between
the domain layer (entities) and the interface adapters layer (gateways and presenters).
"""

from app.use_cases.ports.gateway_ports import ITodoGateway
from app.use_cases.ports.input_ports import (
    DeleteTodoInputDTO,
    GetTodoInputDTO,
    ICreateTodoInputPort,
    IDeleteTodoInputPort,
    IGetTodoInputPort,
    IListTodosInputPort,
    CreateTodoInputDTO,
    IUpdateTodoInputPort,
    ListTodosInputDTO,
    UpdateTodoInputDTO,
)
from app.use_cases.ports.output_ports import (
    ICreateTodoOutputPort,
    IDeleteTodoOutputPort,
    IListTodosOutputPort,
    IGetTodoOutputPort,
    IUpdateTodoOutputPort,
)
from app.domain.entities import TodoEntity


class CreateTodoInteractor(ICreateTodoInputPort):
    """
    Use case interactor for creating a new todo item.
    
    This interactor orchestrates the create todo use case:
    1. Validates business rules (e.g., forbidden words in title)
    2. Creates a new todo entity
    3. Persists it via the gateway
    4. Presents the result via the output port
    """
    
    def __init__(self, gateway: ITodoGateway, output_port: ICreateTodoOutputPort):
        """
        Initialize the interactor with its dependencies.
        
        Args:
            gateway: Data access interface for persisting todos
            output_port: Presentation interface for delivering results
        """
        self.gateway = gateway
        self.output_port = output_port

    def execute(self, input_dto: CreateTodoInputDTO) -> None:
        """
        Execute the create todo use case.
        
        Business Rules:
        - Title cannot contain the word "forbidden" (case-insensitive)
        
        Args:
            input_dto: Contains the data needed to create a new todo
        """
        # Application-specific business rule validation
        if "forbidden" in input_dto.title.lower():
            self.output_port.present_error("Title contains disallowed words.")
            return

        # Create the domain entity
        todo = TodoEntity(title=input_dto.title, description=input_dto.description)
        
        # Persist via gateway
        saved_todo = self.gateway.save(todo)
        
        # Present the result
        self.output_port.present_success(saved_todo)


class ListTodosInteractor(IListTodosInputPort):
    """
    Use case interactor for listing all todo items.
    
    This interactor retrieves all todos with pagination support
    and handles any errors that occur during retrieval.
    """
    
    def __init__(self, gateway: ITodoGateway, output_port: IListTodosOutputPort):
        """
        Initialize the interactor with its dependencies.
        
        Args:
            gateway: Data access interface for retrieving todos
            output_port: Presentation interface for delivering results
        """
        self.gateway = gateway
        self.output_port = output_port

    def execute(self, input_dto: ListTodosInputDTO) -> None:
        """
        Execute the list todos use case.
        
        Args:
            input_dto: Contains pagination parameters (skip and limit)
        """
        try:
            # Retrieve todos from the gateway
            todos = self.gateway.get_all(skip=input_dto.skip, limit=input_dto.limit)
            
            # Present the successful result
            self.output_port.present_success(todos)
        except Exception as err:
            # Handle any errors during retrieval
            self.output_port.present_error(f"Failed to retrieve todos: {str(err)}")


class DeleteTodoInteractor(IDeleteTodoInputPort):
    """
    Use case interactor for deleting a todo item.
    
    This interactor handles the deletion of a todo and manages
    different outcomes (success, not found, error).
    """
    
    def __init__(self, gateway: ITodoGateway, output_port: IDeleteTodoOutputPort):
        """
        Initialize the interactor with its dependencies.
        
        Args:
            gateway: Data access interface for deleting todos
            output_port: Presentation interface for delivering results
        """
        self.gateway = gateway
        self.output_port = output_port

    def execute(self, input_dto: DeleteTodoInputDTO) -> None:
        """
        Execute the delete todo use case.
        
        Args:
            input_dto: Contains the ID of the todo to delete
        """
        try:
            # Attempt to delete the todo
            success = self.gateway.delete(input_dto.todo_id)
            
            if not success:
                # Todo was not found
                self.output_port.present_not_found(input_dto.todo_id)
                return
                
            # Present successful deletion
            self.output_port.present_success()
        except Exception as err:
            # Handle any errors during deletion
            self.output_port.present_error(f"Failed to delete todo: {str(err)}")


class GetTodoInteractor(IGetTodoInputPort):
    """
    Use case interactor for retrieving a single todo item.
    
    This interactor fetches a specific todo by ID and handles
    cases where the todo might not exist.
    """
    
    def __init__(self, gateway: ITodoGateway, output_port: IGetTodoOutputPort):
        """
        Initialize the interactor with its dependencies.
        
        Args:
            gateway: Data access interface for retrieving todos
            output_port: Presentation interface for delivering results
        """
        self.gateway = gateway
        self.output_port = output_port

    def execute(self, input_dto: GetTodoInputDTO) -> None:
        """
        Execute the get todo use case.
        
        Args:
            input_dto: Contains the ID of the todo to retrieve
        """
        try:
            # Retrieve the todo from the gateway
            todo = self.gateway.get_by_id(input_dto.todo_id)
            
            if not todo:
                # Todo was not found
                self.output_port.present_not_found(input_dto.todo_id)
                return
                
            # Present the successful result
            self.output_port.present_success(todo)
        except Exception as err:
            # Handle any errors during retrieval
            self.output_port.present_error(f"Failed to fetch todo: {str(err)}")


class UpdateTodoInteractor(IUpdateTodoInputPort):
    """
    Use case interactor for updating a todo item.
    
    This interactor handles partial updates to a todo, allowing clients
    to update only specific fields without affecting others.
    """
    
    def __init__(self, gateway: ITodoGateway, output_port: IUpdateTodoOutputPort):
        """
        Initialize the interactor with its dependencies.
        
        Args:
            gateway: Data access interface for updating todos
            output_port: Presentation interface for delivering results
        """
        self.gateway = gateway
        self.output_port = output_port

    def execute(self, input_dto: UpdateTodoInputDTO) -> None:
        """
        Execute the update todo use case.
        
        This method supports partial updates - only provided fields are updated.
        
        Business Rules:
        - Title cannot contain the word "forbidden" (case-insensitive)
        - Title cannot be empty (enforced by the entity)
        
        Args:
            input_dto: Contains the ID and fields to update
        """
        try:
            # First, retrieve the existing todo
            todo = self.gateway.get_by_id(input_dto.todo_id)
            
            if not todo:
                # Todo was not found
                self.output_port.present_not_found(input_dto.todo_id)
                return

            # Update title if provided
            if input_dto.title is not None:
                # Validate business rule
                if "forbidden" in input_dto.title.lower():
                    self.output_port.present_error("Title contains disallowed words.")
                    return
                # Use domain entity method to update (enforces entity rules)
                todo.update_title(input_dto.title)

            # Update description if provided
            if input_dto.description is not None:
                todo.description = input_dto.description

            # Mark as completed if requested
            if input_dto.completed is True:
                todo.mark_completed()

            # Persist the updated todo
            updated_todo = self.gateway.save(todo)
            
            # Present the successful result
            self.output_port.present_success(updated_todo)
            
        except ValueError as err:
            # Handle domain validation errors (e.g., empty title)
            self.output_port.present_error(str(err))
        except Exception as err:
            # Handle any other errors during update
            self.output_port.present_error(f"Failed to update todo: {str(err)}")
