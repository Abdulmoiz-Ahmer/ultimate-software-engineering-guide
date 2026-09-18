from app.use_cases.ports.gateway_ports import ITodoGateway
from app.use_cases.ports.input_ports import (
    DeleteTodoInputDTO,
    GetTodoInputDTO,
    ICreateTodoInputPort,
    IDeleteTodoInputPort,
    IGetTodoInputPort,
    IListTodosInputPort,
    CreateTodoInputDTO,
    IUpdateTodoInputPort,
    ListTodosInputDTO,
    UpdateTodoInputDTO,
)
from app.use_cases.ports.output_ports import (
    ICreateTodoOutputPort,
    IDeleteTodoOutputPort,
    IListTodosOutputPort,
    IGetTodoOutputPort,
    IUpdateTodoOutputPort,
)
from app.domain.entities import TodoEntity


class CreateTodoInteractor(ICreateTodoInputPort):
    def __init__(self, gateway: ITodoGateway, output_port: ICreateTodoOutputPort):
        self.gateway = gateway
        self.output_port = output_port

    def execute(self, input_dto: CreateTodoInputDTO) -> None:
        if "forbidden" in input_dto.title.lower():
            self.output_port.present_error("Title contains disallowed words.")
            return

        todo = TodoEntity(title=input_dto.title, description=input_dto.description)
        saved_todo = self.gateway.save(todo)
        self.output_port.present_success(saved_todo)


class ListTodosInteractor(IListTodosInputPort):
    def __init__(self, gateway: ITodoGateway, output_port: IListTodosOutputPort):
        self.gateway = gateway
        self.output_port = output_port

    def execute(self, input_dto: ListTodosInputDTO) -> None:
        try:
            todos = self.gateway.get_all(skip=input_dto.skip, limit=input_dto.limit)
            self.output_port.present_success(todos)
        except Exception as err:
            self.output_port.present_error(f"Failed to retrieve todos: {str(err)}")


class DeleteTodoInteractor(IDeleteTodoInputPort):
    def __init__(self, gateway: ITodoGateway, output_port: IDeleteTodoOutputPort):
        self.gateway = gateway
        self.output_port = output_port

    def execute(self, input_dto: DeleteTodoInputDTO) -> None:
        try:
            success = self.gateway.delete(input_dto.todo_id)
            if not success:
                self.output_port.present_not_found(input_dto.todo_id)
                return
            self.output_port.present_success()
        except Exception as err:
            self.output_port.present_error(f"Failed to delete todo: {str(err)}")


class GetTodoInteractor(IGetTodoInputPort):
    def __init__(self, gateway: ITodoGateway, output_port: IGetTodoOutputPort):
        self.gateway = gateway
        self.output_port = output_port

    def execute(self, input_dto: GetTodoInputDTO) -> None:
        try:
            todo = self.gateway.get_by_id(input_dto.todo_id)
            if not todo:
                self.output_port.present_not_found(input_dto.todo_id)
                return
            self.output_port.present_success(todo)
        except Exception as err:
            self.output_port.present_error(f"Failed to fetch todo: {str(err)}")


class UpdateTodoInteractor(IUpdateTodoInputPort):
    def __init__(self, gateway: ITodoGateway, output_port: IUpdateTodoOutputPort):
        self.gateway = gateway
        self.output_port = output_port

    def execute(self, input_dto: UpdateTodoInputDTO) -> None:
        try:
            todo = self.gateway.get_by_id(input_dto.todo_id)
            if not todo:
                self.output_port.present_not_found(input_dto.todo_id)
                return

            if input_dto.title is not None:
                if "forbidden" in input_dto.title.lower():
                    self.output_port.present_error("Title contains disallowed words.")
                    return
                todo.update_title(input_dto.title)

            if input_dto.description is not None:
                todo.description = input_dto.description

            if input_dto.completed is True:
                todo.mark_completed()

            updated_todo = self.gateway.save(todo)
            self.output_port.present_success(updated_todo)
        except ValueError as err:
            self.output_port.present_error(str(err))
        except Exception as err:
            self.output_port.present_error(f"Failed to update todo: {str(err)}")
