from uuid import UUID

from fastapi import HTTPException, status
from app.use_cases.ports.input_ports import (
    CreateTodoInputDTO,
    DeleteTodoInputDTO,
    GetTodoInputDTO,
    ListTodosInputDTO,
    UpdateTodoInputDTO,
)
from app.use_cases.ports.output_ports import TodoOutputDTO
from app.interface_adapters.presenters.todo_presenter import (
    CreateTodoPresenter,
    DeleteTodoPresenter,
    GetTodoPresenter,
    ListTodosPresenter,
    UpdateTodoPresenter,
)


class TodoController:
    def __init__(
        self,
        create_interactor_factory,
        get_interactor_factory,
        list_interactor_factory,
        update_interactor_factory,
        delete_interactor_factory,
    ):
        self.create_interactor_factory = create_interactor_factory
        self.get_interactor_factory = get_interactor_factory
        self.list_interactor_factory = list_interactor_factory
        self.update_interactor_factory = update_interactor_factory
        self.delete_interactor_factory = delete_interactor_factory

    def list_todos(self, skip: int = 0, limit: int = 100) -> list[TodoOutputDTO]:
        presenter = ListTodosPresenter()
        interactor = self.list_interactor_factory(presenter)

        interactor.execute(ListTodosInputDTO(skip=skip, limit=limit))

        if presenter.error_message:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=presenter.error_message,
            )
        return presenter.response_data

    def create_todo(self, title: str, description: str | None) -> TodoOutputDTO:
        presenter = CreateTodoPresenter()
        interactor = self.create_interactor_factory(presenter)

        input_dto = CreateTodoInputDTO(title=title, description=description)
        interactor.execute(input_dto)

        if presenter.error_message:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=presenter.error_message
            )
        return presenter.response_data

    def delete_todo(self, todo_id: UUID) -> None:
        presenter = DeleteTodoPresenter()
        interactor = self.delete_interactor_factory(presenter)

        interactor.execute(DeleteTodoInputDTO(todo_id=todo_id))

        if presenter.is_not_found:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Todo item with ID '{todo_id}' was not found.",
            )
        if presenter.error_message:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=presenter.error_message,
            )

    def get_todo(self, todo_id: UUID) -> TodoOutputDTO:
        presenter = GetTodoPresenter()
        interactor = self.get_interactor_factory(presenter)

        interactor.execute(GetTodoInputDTO(todo_id=todo_id))

        if presenter.is_not_found:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Todo item with ID '{todo_id}' was not found.",
            )
        if presenter.error_message:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=presenter.error_message,
            )
        return presenter.response_data

    def update_todo(
        self,
        todo_id: UUID,
        title: str | None,
        description: str | None,
        completed: bool | None,
    ) -> TodoOutputDTO:
        presenter = UpdateTodoPresenter()
        interactor = self.update_interactor_factory(presenter)

        input_dto = UpdateTodoInputDTO(
            todo_id=todo_id, title=title, description=description, completed=completed
        )
        interactor.execute(input_dto)

        if presenter.is_not_found:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Todo item with ID '{todo_id}' was not found.",
            )
        if presenter.error_message:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=presenter.error_message,
            )
        return presenter.response_data
