# app/use_cases/ports/output_ports.py
from dataclasses import dataclass
from uuid import UUID
from abc import ABC, abstractmethod
from app.domain.entities import TodoEntity


@dataclass
class TodoOutputDTO:
    id: UUID
    title: str
    description: str | None
    completed: bool


class ICreateTodoOutputPort(ABC):
    @abstractmethod
    def present_success(self, todo: TodoEntity) -> None:
        pass

    @abstractmethod
    def present_error(self, message: str) -> None:
        pass


class IListTodosOutputPort(ABC):
    @abstractmethod
    def present_success(self, todos: list[TodoEntity]) -> None:
        pass

    @abstractmethod
    def present_error(self, message: str) -> None:
        pass


class IDeleteTodoOutputPort(ABC):
    @abstractmethod
    def present_success(self) -> None:
        pass

    @abstractmethod
    def present_not_found(self, todo_id: UUID) -> None:
        pass

    @abstractmethod
    def present_error(self, message: str) -> None:
        pass


class IGetTodoOutputPort(ABC):
    @abstractmethod
    def present_success(self, todo: TodoEntity) -> None:
        pass

    @abstractmethod
    def present_not_found(self, todo_id: UUID) -> None:
        pass

    @abstractmethod
    def present_error(self, message: str) -> None:
        pass


# app/use_cases/ports/output_ports.py
class IUpdateTodoOutputPort(ABC):
    @abstractmethod
    def present_success(self, todo: TodoEntity) -> None:
        pass

    @abstractmethod
    def present_not_found(self, todo_id: UUID) -> None:
        pass

    @abstractmethod
    def present_error(self, message: str) -> None:
        pass
