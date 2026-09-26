# app/models.py
"""
SQLAlchemy ORM Models

This module defines the database models for the GraphQL Todo application.
Uses SQLAlchemy's declarative base for ORM mapping.

Models:
- UserORM: Represents users in the system
- TodoORM: Represents todos/tasks associated with users
"""

import uuid
from sqlalchemy import Column, String, ForeignKey, Boolean
from sqlalchemy.types import UUID
from sqlalchemy.orm import declarative_base, relationship

# Base class for all ORM models
Base = declarative_base()


class UserORM(Base):
    """
    User Model
    
    Represents a user in the system. Each user can have multiple todos.
    
    Columns:
        id (UUID): Primary key, auto-generated UUID
        name (str): User's name, max 50 characters, required
        
    Relationships:
        todos: One-to-many relationship with TodoORM
    """
    __tablename__ = "users"

    # Primary key using UUID for distributed system compatibility
    # as_uuid=True ensures Python receives uuid.UUID objects instead of strings
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # User's name - required field with max length of 50 characters
    name = Column(String(50), nullable=False)

    # Relationship: One user can have many todos
    # back_populates creates bidirectional relationship
    todos = relationship("TodoORM", back_populates="author")


class TodoORM(Base):
    """
    Todo/Task Model
    
    Represents a todo item belonging to a user.
    
    Columns:
        id (UUID): Primary key, auto-generated UUID
        title (str): Todo title/description, max 100 characters, required
        completed (bool): Completion status, defaults to False
        user_id (UUID): Foreign key to users table, required
        
    Relationships:
        author: Many-to-one relationship with UserORM
    """
    __tablename__ = "todos"

    # Primary key using UUID
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Todo title/description - required field with max length of 100 characters
    title = Column(String(100), nullable=False)
    
    # Completion status - defaults to False (not completed)
    # nullable=False means this field is required and must have a value
    completed = Column(Boolean, nullable=False, default=False)
    
    # Foreign key linking to the user who owns this todo
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    # Relationship: Many todos belong to one user
    # back_populates creates bidirectional relationship
    author = relationship("UserORM", back_populates="todos")
