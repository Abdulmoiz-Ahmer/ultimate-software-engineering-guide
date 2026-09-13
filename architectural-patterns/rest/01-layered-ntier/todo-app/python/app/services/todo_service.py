import uuid

from fastapi import HTTPException
from app.repositories.todo_repository import TodoRepository
from app.api.schemas import TodoCreate, TodoResponse, TodoUpdate


class TodoService:
    def __init__(self, todo_repository: TodoRepository):
        self.repository = todo_repository

    def create_todo(self, payload: TodoCreate) -> TodoResponse:
        todo = self.repository.createOne(
            title=payload.title, description=payload.description
        )
        return todo

    def get_todo(self, todo_id: uuid.UUID) -> TodoResponse | None:
        todo = self.repository.fetchOne(todo_id)
        if not todo:
            raise HTTPException(status_code=404, detail="Todo not found")
        return todo

    def get_todos(self) -> list[TodoResponse]:
        todos = self.repository.fetchAll()
        return todos

    def delete_todo(self, todo_id: uuid.UUID) -> None:
        todo = self.get_todo(todo_id)
        self.repository.deleteOne(todo)

    def update_todo(self, todo_id: uuid.UUID, payload: TodoUpdate) -> TodoResponse:
        todo = self.get_todo(todo_id)
        update_data = payload.model_dump(exclude_unset=True)
        result = self.repository.updateOne(todo, update_data)
        return result
