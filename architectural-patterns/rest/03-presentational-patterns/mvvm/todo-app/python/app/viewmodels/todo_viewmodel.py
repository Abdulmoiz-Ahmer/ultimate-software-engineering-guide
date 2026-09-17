from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.todo import TodoModel

# View State DTOs
class CreateTodoItemState(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: str | None = None

class UpdateTodoItemState(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=100)
    description: str | None = None
    completed: bool | None = None

class TodoItemViewState(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    description: str | None
    completed: bool
    display_title: str  # Computed view property

    @classmethod
    def from_model(cls, model: TodoModel) -> "TodoItemViewState":
        """Transforms a DB Model into a View State presentation object."""
        status_tag = "[DONE]" if model.completed else "[PENDING]"
        return cls(
            id=model.id,
            title=model.title,
            description=model.description,
            completed=model.completed,
            display_title=f"{status_tag} {model.title}"
        )


# ViewModel Execution Class
class TodoViewModel:
    def __init__(self, db: Session):
        self.db = db

    def create_todo(self, state: CreateTodoItemState) -> TodoItemViewState:
        if "forbidden" in state.title.lower():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Title contains disallowed words."
            )

        todo = TodoModel(title=state.title, description=state.description)
        self.db.add(todo)
        self.db.commit()
        self.db.refresh(todo)
        return TodoItemViewState.from_model(todo)

    def get_todo(self, todo_id: UUID) -> TodoItemViewState:
        todo = self.db.query(TodoModel).filter(TodoModel.id == todo_id).first()
        if not todo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Todo item not found."
            )
        return TodoItemViewState.from_model(todo)

    def list_todos(self, skip: int = 0, limit: int = 100) -> list[TodoItemViewState]:
        todos = self.db.query(TodoModel).offset(skip).limit(limit).all()
        return [TodoItemViewState.from_model(item) for item in todos]

    def update_todo(self, todo_id: UUID, state: UpdateTodoItemState) -> TodoItemViewState:
        todo = self.db.query(TodoModel).filter(TodoModel.id == todo_id).first()
        if not todo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Todo item not found."
            )

        update_data = state.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(todo, key, value)

        self.db.commit()
        self.db.refresh(todo)
        return TodoItemViewState.from_model(todo)

    def delete_todo(self, todo_id: UUID) -> None:
        todo = self.db.query(TodoModel).filter(TodoModel.id == todo_id).first()
        if not todo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Todo item not found."
            )
        self.db.delete(todo)
        self.db.commit()