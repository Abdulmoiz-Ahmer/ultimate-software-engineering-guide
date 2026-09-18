# app/use_cases/ports/input_ports.py
from dataclasses import dataclass
from abc import ABC, abstractmethod
from uuid import UUID


@dataclass
class CreateTodoInputDTO:
    title: str
    description: str | None = None


class ICreateTodoInputPort(ABC):
    @abstractmethod
    def execute(self, input_dto: CreateTodoInputDTO) -> None:
        pass


@dataclass
class ListTodosInputDTO:
    skip: int = 0
    limit: int = 100


class IListTodosInputPort(ABC):
    @abstractmethod
    def execute(self, input_dto: ListTodosInputDTO) -> None:
        pass


@dataclass
class DeleteTodoInputDTO:
    todo_id: UUID


class IDeleteTodoInputPort(ABC):
    @abstractmethod
    def execute(self, input_dto: DeleteTodoInputDTO) -> None:
        pass


@dataclass
class GetTodoInputDTO:
    todo_id: UUID


class IGetTodoInputPort(ABC):
    @abstractmethod
    def execute(self, input_dto: GetTodoInputDTO) -> None:
        pass


# app/use_cases/ports/input_ports.py
@dataclass
class UpdateTodoInputDTO:
    todo_id: UUID
    title: str | None = None
    description: str | None = None
    completed: bool | None = None


class IUpdateTodoInputPort(ABC):
    @abstractmethod
    def execute(self, input_dto: UpdateTodoInputDTO) -> None:
        pass
