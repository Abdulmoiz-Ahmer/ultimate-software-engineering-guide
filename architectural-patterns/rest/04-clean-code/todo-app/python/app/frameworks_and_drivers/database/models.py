"""
Frameworks and Drivers Layer - Database Models Module

This module defines the ORM (Object-Relational Mapping) models for database tables.
These models are SQLAlchemy-specific and represent how data is stored in the database.

Key points:
- ORM models are framework-specific (SQLAlchemy) and live in the outermost layer
- They are separate from domain entities (which are framework-independent)
- The gateway layer translates between ORM models and domain entities
- Changing the ORM or database technology only requires changes in this layer

This separation keeps the business logic (entities, use cases) independent
of database implementation details.
"""

import uuid
from sqlalchemy import Column, String, Boolean
from sqlalchemy.types import UUID
from app.frameworks_and_drivers.database.database import Base


class TodoORM(Base):
    """
    SQLAlchemy ORM model for the todos table.
    
    This class defines the schema and mapping for storing todos in the database.
    It's completely separate from the TodoEntity in the domain layer.
    
    Attributes:
        id: Primary key, UUID type, auto-generated
        title: Todo title, string up to 100 characters, required
        description: Todo description, string up to 255 characters, optional
        completed: Completion status, boolean, defaults to False
        
    Table name: todos
    """
    
    __tablename__ = "todos"

    # Primary key column with UUID type
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Title column - required field
    title = Column(String(100), nullable=False)
    
    # Description column - optional field
    description = Column(String(255), nullable=True)
    
    # Completed status - defaults to False
    completed = Column(Boolean, default=False)
