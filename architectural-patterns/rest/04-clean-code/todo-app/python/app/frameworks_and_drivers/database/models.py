# app/frameworks_and_drivers/database/models.py
import uuid
from sqlalchemy import Column, String, Boolean
from sqlalchemy.types import UUID
from app.frameworks_and_drivers.database.database import Base


class TodoORM(Base):
    __tablename__ = "todos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    completed = Column(Boolean, default=False)
