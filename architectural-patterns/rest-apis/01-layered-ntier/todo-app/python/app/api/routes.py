from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.schemas import TodoCreate, TodoResponse, TodoUpdate
from app.database import get_db
from app.repositories.todo_repository import TodoRepository
from app.services.todo_service import TodoService

router = APIRouter(prefix="/todos", tags=["Todos"])


def get_todo_service(db: Session = Depends(get_db)) -> TodoService:
    return TodoService(todo_repository=TodoRepository(db=db))


@router.post("/", response_model=TodoResponse, status_code=201)
async def create_todo(
    payload: TodoCreate, service: TodoService = Depends(get_todo_service)
) -> TodoResponse:
    return service.create_todo(payload=payload)


@router.get("/{id}", response_model=TodoResponse, status_code=200)
async def get_todo(
    id: UUID, service: TodoService = Depends(get_todo_service)
) -> TodoResponse:
    return service.get_todo(todo_id=id)


@router.delete("/{id}", status_code=204)
async def delete_todo(id: UUID, service: TodoService = Depends(get_todo_service)):
    service.delete_todo(todo_id=id)


@router.get("/", response_model=list[TodoResponse], status_code=200)
async def get_todos(service: TodoService = Depends(get_todo_service)):
    return service.get_todos()


@router.patch("/{id}", response_model=TodoResponse, status_code=200)
async def update_todo(
    id: UUID, payload: TodoUpdate, service: TodoService = Depends(get_todo_service)
) -> TodoResponse:
    return service.update_todo(todo_id=id, payload=payload)
