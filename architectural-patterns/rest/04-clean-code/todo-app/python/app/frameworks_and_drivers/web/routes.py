# app/frameworks_and_drivers/web/routes.py
from fastapi import APIRouter, Depends, status
from uuid import UUID
from sqlalchemy.orm import Session
from app.frameworks_and_drivers.database.database import get_db
from app.frameworks_and_drivers.web.schemas import (
    CreateTodoHTTPPayload,
    TodoHTTPResponse,
    UpdateTodoHTTPPayload,
)
from app.interface_adapters.gateways.todo_gateway import SqlAlchemyTodoGateway
from app.interface_adapters.controllers.todo_controller import TodoController
from app.use_cases.interactors import (
    CreateTodoInteractor,
    DeleteTodoInteractor,
    GetTodoInteractor,
    ListTodosInteractor,
    UpdateTodoInteractor,
)

router = APIRouter(prefix="/todos", tags=["Clean Architecture Todos"])


def get_controller(db: Session = Depends(get_db)) -> TodoController:
    gateway = SqlAlchemyTodoGateway(db)

    def create_interactor_factory(presenter):
        return CreateTodoInteractor(gateway=gateway, output_port=presenter)

    def get_interactor_factory(presenter):
        return GetTodoInteractor(gateway=gateway, output_port=presenter)

    def list_interactor_factory(presenter):
        return ListTodosInteractor(gateway=gateway, output_port=presenter)

    def update_interactor_factory(presenter):
        return UpdateTodoInteractor(gateway=gateway, output_port=presenter)

    def delete_interactor_factory(presenter):
        return DeleteTodoInteractor(gateway=gateway, output_port=presenter)

    return TodoController(
        create_interactor_factory=create_interactor_factory,
        get_interactor_factory=get_interactor_factory,
        list_interactor_factory=list_interactor_factory,
        update_interactor_factory=update_interactor_factory,
        delete_interactor_factory=delete_interactor_factory,
    )


@router.post("/", response_model=TodoHTTPResponse, status_code=status.HTTP_201_CREATED)
def create_todo(
    payload: CreateTodoHTTPPayload,
    controller: TodoController = Depends(get_controller),
):
    return controller.create_todo(title=payload.title, description=payload.description)


@router.get("/", response_model=list[TodoHTTPResponse])
def list_todos(
    skip: int = 0,
    limit: int = 100,
    controller: TodoController = Depends(get_controller),
):
    return controller.list_todos(skip=skip, limit=limit)


@router.get("/{todo_id}", response_model=TodoHTTPResponse)
def get_todo(
    todo_id: UUID,
    controller: TodoController = Depends(get_controller),
):
    return controller.get_todo(todo_id=todo_id)


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(
    todo_id: UUID,
    controller: TodoController = Depends(get_controller),
):
    controller.delete_todo(todo_id=todo_id)


@router.patch("/{todo_id}", response_model=TodoHTTPResponse)
def update_todo(
    todo_id: UUID,
    payload: UpdateTodoHTTPPayload,
    controller: TodoController = Depends(get_controller),
):
    return controller.update_todo(
        todo_id=todo_id,
        title=payload.title,
        description=payload.description,
        completed=payload.completed,
    )
