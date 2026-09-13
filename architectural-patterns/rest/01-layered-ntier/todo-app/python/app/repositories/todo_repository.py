from sqlalchemy.orm import Session
from starlette.exceptions import HTTPException
from app.models.todo import TodoModel
from uuid import UUID


class TodoRepository:
    def __init__(self, db: Session):
        self.db = db

    def createOne(self, title: str, description: str | None) -> TodoModel:
        todo = TodoModel(title=title, description=description)
        self.db.add(todo)
        self.db.commit()
        self.db.refresh(todo)
        return todo

    def fetchOne(self, todo_id: UUID) -> TodoModel | None:
        todo = self.db.query(TodoModel).filter(TodoModel.id == todo_id).first()
        return todo
    
    def updateOne(self, todo: TodoModel, update_data: dict) -> TodoModel:
        for key, value in update_data.items():
            setattr(todo, key, value)
        self.db.commit()
        self.db.refresh(todo)
        return todo

    def fetchAll(self) -> list[TodoModel]:
        todos = self.db.query(TodoModel).all()
        return todos

    def deleteOne(self, todo: TodoModel) -> None:
        self.db.delete(todo)
        self.db.commit()
