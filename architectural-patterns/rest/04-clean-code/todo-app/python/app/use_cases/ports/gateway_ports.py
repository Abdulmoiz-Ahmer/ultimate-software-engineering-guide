from abc import ABC, abstractmethod
from uuid import UUID
from app.domain.entities import TodoEntity


class ITodoGateway(ABC):
    @abstractmethod
    def save(self, todo: TodoEntity) -> TodoEntity:
        pass

    @abstractmethod
    def get_by_id(self, todo_id: UUID) -> TodoEntity | None:
        pass

    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> list[TodoEntity]:
        pass

    @abstractmethod
    def delete(self, todo_id: UUID) -> bool:
        """Returns True if deleted, False if item was not found."""
        pass
