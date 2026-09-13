from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.components.todos.models import TodoModel
from app.components.todos.schemas import CreateTodoCommand, TodoDTO


class CreateTodoHandler:
    @staticmethod
    def execute(db: Session, command: CreateTodoCommand) -> TodoDTO:
        todo = TodoModel(
            title=command.title, description=command.description, completed=False
        )
        db.add(todo)
        db.commit()
        db.refresh(todo)
        return todo


class GetTodoQuery:
    @staticmethod
    def execute(db: Session, todo_id: str) -> TodoDTO:
        todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
        if not todo:
            raise HTTPException(
                status_code=404, detail=f"Todo with id {todo_id} not found"
            )
        return todo


class ListTodosQuery:
    @staticmethod
    def execute(db: Session, skip: int = 0, limit: int = 100) -> list[TodoDTO]:
        return db.query(TodoModel).offset(skip).limit(limit).all()


class UpdateTodoHandler:
    @staticmethod
    def execute(db: Session, todo_id: str, command: CreateTodoCommand) -> TodoDTO:
        todo = GetTodoQuery.execute(db, todo_id)
        update_data = command.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(todo, field, value)
        db.commit()
        db.refresh(todo)
        return todo


class DeleteTodoHandler:
    @staticmethod
    def execute(db: Session, todo_id: str) -> None:
        todo = GetTodoQuery.execute(db, todo_id)
        db.delete(todo)
        db.commit()
