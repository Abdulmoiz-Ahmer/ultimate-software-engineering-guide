from uuid import UUID
from sqlalchemy.orm import Session
from app.domain.entities import TodoEntity
from app.use_cases.ports.gateway_ports import ITodoGateway
from app.frameworks_and_drivers.database.models import TodoORM


class SqlAlchemyTodoGateway(ITodoGateway):
    def __init__(self, db: Session):
        self.db = db

    def _to_entity(self, orm: TodoORM) -> TodoEntity:
        return TodoEntity(
            id=orm.id,
            title=orm.title,
            description=orm.description,
            completed=orm.completed,
        )

    def save(self, todo: TodoEntity) -> TodoEntity:
        orm_item = self.db.query(TodoORM).filter(TodoORM.id == todo.id).first()
        if orm_item:
            orm_item.title = todo.title
            orm_item.description = todo.description
            orm_item.completed = todo.completed
        else:
            orm_item = TodoORM(
                id=todo.id,
                title=todo.title,
                description=todo.description,
                completed=todo.completed,
            )
            self.db.add(orm_item)
        
        self.db.commit()
        self.db.refresh(orm_item)
        return self._to_entity(orm_item)

    def get_all(self, skip: int = 0, limit: int = 100) -> list[TodoEntity]:
        orm_items = self.db.query(TodoORM).offset(skip).limit(limit).all()
        return [self._to_entity(item) for item in orm_items]

    def get_by_id(self, todo_id: UUID) -> TodoEntity | None:
        orm_item = self.db.query(TodoORM).filter(TodoORM.id == todo_id).first()
        return self._to_entity(orm_item) if orm_item else None

    def delete(self, todo_id: UUID) -> bool:
        orm_item = self.db.query(TodoORM).filter(TodoORM.id == todo_id).first()
        if not orm_item:
            return False

        self.db.delete(orm_item)
        self.db.commit()
        return True
