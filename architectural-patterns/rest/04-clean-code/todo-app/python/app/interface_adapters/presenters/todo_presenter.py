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
from app.use_cases.ports.output_ports import IDeleteTodoOutputPort


class CreateTodoPresenter(ICreateTodoOutputPort):
    def __init__(self):
        self.response_data: TodoOutputDTO | None = None
        self.error_message: str | None = None

    def present_success(self, todo: TodoEntity) -> None:
        self.response_data = TodoOutputDTO(
            id=todo.id,
            title=todo.title,
            description=todo.description,
            completed=todo.completed,
        )

    def present_error(self, message: str) -> None:
        self.error_message = message


class ListTodosPresenter(IListTodosOutputPort):
    def __init__(self):
        self.response_data: list[TodoOutputDTO] = []
        self.error_message: str | None = None

    def present_success(self, todos: list[TodoEntity]) -> None:
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
        self.error_message = message


class DeleteTodoPresenter(IDeleteTodoOutputPort):
    def __init__(self):
        self.is_success: bool = False
        self.is_not_found: bool = False
        self.error_message: str | None = None

    def present_success(self) -> None:
        self.is_success = True

    def present_not_found(self, todo_id: UUID) -> None:
        self.is_not_found = True

    def present_error(self, message: str) -> None:
        self.error_message = message


class GetTodoPresenter(IGetTodoOutputPort):
    def __init__(self):
        self.response_data: TodoOutputDTO | None = None
        self.is_not_found: bool = False
        self.error_message: str | None = None

    def present_success(self, todo: TodoEntity) -> None:
        self.response_data = TodoOutputDTO(
            id=todo.id,
            title=todo.title,
            description=todo.description,
            completed=todo.completed,
        )

    def present_not_found(self, todo_id: UUID) -> None:
        self.is_not_found = True

    def present_error(self, message: str) -> None:
        self.error_message = message


class UpdateTodoPresenter(IUpdateTodoOutputPort):
    def __init__(self):
        self.response_data: TodoOutputDTO | None = None
        self.is_not_found: bool = False
        self.error_message: str | None = None

    def present_success(self, todo: TodoEntity) -> None:
        self.response_data = TodoOutputDTO(
            id=todo.id,
            title=todo.title,
            description=todo.description,
            completed=todo.completed,
        )

    def present_not_found(self, todo_id: UUID) -> None:
        self.is_not_found = True

    def present_error(self, message: str) -> None:
        self.error_message = message
