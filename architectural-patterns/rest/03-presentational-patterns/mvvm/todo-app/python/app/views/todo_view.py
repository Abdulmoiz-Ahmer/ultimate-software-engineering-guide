from uuid import UUID
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.viewmodels.todo_viewmodel import (
    TodoViewModel,
    CreateTodoItemState,
    UpdateTodoItemState,
    TodoItemViewState,
)

router = APIRouter(prefix="/todos", tags=["MVVM Todos"])


def get_viewmodel(db: Session = Depends(get_db)) -> TodoViewModel:
    return TodoViewModel(db=db)


@router.post("/", response_model=TodoItemViewState, status_code=status.HTTP_201_CREATED)
def create_todo(state: CreateTodoItemState, vm: TodoViewModel = Depends(get_viewmodel)):
    return vm.create_todo(state)


@router.get("/{todo_id}", response_model=TodoItemViewState)
def get_todo(todo_id: UUID, vm: TodoViewModel = Depends(get_viewmodel)):
    return vm.get_todo(todo_id)


@router.get("/", response_model=list[TodoItemViewState])
def list_todos(
    skip: int = 0, limit: int = 100, vm: TodoViewModel = Depends(get_viewmodel)
):
    return vm.list_todos(skip=skip, limit=limit)


@router.patch("/{todo_id}", response_model=TodoItemViewState)
def update_todo(
    todo_id: UUID,
    state: UpdateTodoItemState,
    vm: TodoViewModel = Depends(get_viewmodel),
):
    return vm.update_todo(todo_id, state)


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: UUID, vm: TodoViewModel = Depends(get_viewmodel)):
    vm.delete_todo(todo_id)
