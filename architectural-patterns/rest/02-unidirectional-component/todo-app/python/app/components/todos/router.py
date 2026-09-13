from uuid import UUID
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.components.todos.schemas import CreateTodoCommand, UpdateTodoCommand, TodoDTO
from app.components.todos.handlers import (
    CreateTodoHandler,
    GetTodoQuery,
    ListTodosQuery,
    UpdateTodoHandler,
    DeleteTodoHandler,
)

router = APIRouter(prefix="/todos", tags=["Todos Component"])


@router.post("/", response_model=TodoDTO, status_code=status.HTTP_201_CREATED)
def create_todo(command: CreateTodoCommand, db: Session = Depends(get_db)):
    return CreateTodoHandler.execute(db, command)


@router.get("/{todo_id}", response_model=TodoDTO)
def get_todo(todo_id: UUID, db: Session = Depends(get_db)):
    return GetTodoQuery.execute(db, todo_id)


@router.get("/", response_model=list[TodoDTO])
def list_todos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return ListTodosQuery.execute(db, skip=skip, limit=limit)


@router.patch("/{todo_id}", response_model=TodoDTO)
def update_todo(
    todo_id: UUID, command: UpdateTodoCommand, db: Session = Depends(get_db)
):
    return UpdateTodoHandler.execute(db, todo_id, command)


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: UUID, db: Session = Depends(get_db)):
    DeleteTodoHandler.execute(db, todo_id)
