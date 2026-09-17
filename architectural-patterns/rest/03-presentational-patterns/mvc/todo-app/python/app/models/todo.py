"""
Model - The "M" in MVC

This module defines the data Model for the Todo entity. In MVC architecture,
the Model represents the data structure and business domain objects.

Model Responsibilities in MVC:
┌─────────────────────────────────────────────────────────────┐
│                      Model Layer                             │
├─────────────────────────────────────────────────────────────┤
│  ✓ Represents data structure (database schema)              │
│  ✓ Encapsulates data access and storage                     │
│  ✓ Defines domain objects (entities)                        │
│  ✓ Independent of presentation (doesn't know about Views)   │
│  ✓ Independent of HTTP (doesn't know about Controllers)     │
└─────────────────────────────────────────────────────────────┘

Key Principles:
- Model is the single source of truth for data structure
- Model can be accessed by Controller but never by View directly
- Model contains no presentation logic or HTTP concerns
- Model uses ORM (SQLAlchemy) to map to database tables

In classic MVC (server-side rendering):
- Model often includes business logic
- Model can notify Views of changes (Observer pattern)

In REST API MVC:
- Model is primarily data structure (ORM entity)
- Business logic often lives in Controller
- No direct Model-View connection (Controller mediates)
"""

import uuid
from sqlalchemy import Column, String, Boolean
from sqlalchemy.types import UUID
from app.database import Base


class TodoModel(Base):
    """
    Todo Model - Represents the data structure for a todo item.
    
    This is the "M" (Model) in MVC. It defines the shape of todo data
    and maps to the database table. The Model is concerned only with
    data structure and persistence, not with how data is presented
    (that's the View's job) or how requests are handled (Controller's job).
    
    In MVC Pattern:
    - Controller manipulates the Model (CRUD operations)
    - Controller selects appropriate View for Model data
    - View formats Model data for presentation
    - Model remains independent of both Controller and View
    
    Attributes:
        id (UUID): Unique identifier for the todo item
        title (str): Todo title (required, max 100 chars)
        description (str): Todo description (optional, max 255 chars)
        completed (bool): Completion status (defaults to False)
    """
    
    # Table name in the database
    __tablename__ = "todos"

    # Primary key using UUID for global uniqueness
    # UUIDs are preferred over auto-incrementing integers for:
    # - Global uniqueness (no collision across databases)
    # - Security (prevent enumeration attacks)
    # - Distributed systems (can be generated anywhere)
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Title is required (nullable=False)
    # Max length enforced at database level
    title = Column(String(100), nullable=False)
    
    # Description is optional (nullable defaults to True)
    description = Column(String(255), nullable=True)
    
    # Completed status defaults to False for new todos
    # Represents the domain concept of task completion
    completed = Column(Boolean, default=False)
