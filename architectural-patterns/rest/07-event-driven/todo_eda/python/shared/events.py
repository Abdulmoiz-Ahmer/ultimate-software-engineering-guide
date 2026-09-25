"""
Shared Event Definitions

This module defines all event types used in the event-driven architecture.
Events are published by producer services and consumed by subscriber services
to enable loose coupling and asynchronous communication between services.

All events inherit from BaseEvent and use Pydantic for data validation.
"""

from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field


class BaseEvent(BaseModel):
    """
    Base class for all events in the system.
    
    Provides common fields that all events should have, including
    the event type identifier and timestamp of occurrence.
    
    Attributes:
        event_type: String identifier for the type of event
        occurred_at: ISO-formatted timestamp when the event occurred
    """

    event_type: str
    occurred_at: str = Field(
        default_factory=lambda: datetime.now().isoformat(),
        description="The timestamp when the event occurred.",
    )


class TodoCreatedEvent(BaseEvent):
    """
    Event representing the creation of a new todo item.
    
    Published when a new todo is successfully created in the system.
    Subscribers can use this event to perform actions like auditing,
    notifications, or syncing to other systems.
    
    Attributes:
        event_type: Always set to "TODO_CREATED"
        todo_id: Unique identifier of the created todo
        title: Title of the todo item
        description: Optional description of the todo item
    """

    event_type: str = Field(default="TODO_CREATED")
    todo_id: UUID
    title: str
    description: str | None = None


class TodoDeletedEvent(BaseEvent):
    """
    Event representing the deletion of a todo item.
    
    Published when a todo is successfully removed from the system.
    Subscribers can use this event to perform cleanup actions,
    auditing, or cascade deletions in related systems.
    
    Attributes:
        event_type: Always set to "TODO_DELETED"
        todo_id: Unique identifier of the deleted todo
    """

    event_type: str = Field(default="TODO_DELETED")
    todo_id: UUID
