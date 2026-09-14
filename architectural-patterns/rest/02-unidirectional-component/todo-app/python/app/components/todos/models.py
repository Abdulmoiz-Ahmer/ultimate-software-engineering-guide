"""
Todo Component - Data Models

This module defines the database model for the Todo component.
In unidirectional component architecture, each component owns its models
and they live alongside the component's other files.

Component Ownership:
- Models are scoped to the component (not shared)
- Changes to this model only affect the Todo component
- Component encapsulates its data structure
- No cross-component model dependencies

This contrasts with layered architecture where all models live in
a shared models/ directory and can be accessed by any layer.
"""

import uuid
from sqlalchemy import Column, String, Boolean
from sqlalchemy.types import UUID
from app.core.database import Base


class TodoModel(Base):
    """
    SQLAlchemy ORM model for Todo items.
    
    This model belongs exclusively to the Todo component and represents
    the database table structure for storing todo items. It uses UUID
    for primary keys to ensure global uniqueness.
    
    Attributes:
        id (UUID): Unique identifier, auto-generated
        title (str): Todo title (required, max 100 chars)
        description (str): Todo description (optional, max 255 chars)
        completed (bool): Completion status (defaults to False)
    """
    
    # Table name in the database
    __tablename__ = "todos"

    # Primary key using UUID for global uniqueness and security
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Title is required
    title = Column(String(100), nullable=False, index=True)
    
    # Description is optional
    description = Column(String(255), nullable=True, index=True)
    
    # Completed status defaults to False for new todos
    completed = Column(Boolean, default=False)
