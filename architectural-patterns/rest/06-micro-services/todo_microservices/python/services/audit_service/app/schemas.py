"""
Pydantic Schemas for Request/Response Validation

This module defines Pydantic models used for API request validation
and response serialization in the Audit service.

Schemas:
    - CreateAuditLogPayload: Input validation for receiving audit events
    - AuditLogResponse: Standard response format for audit log entries
"""

from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class CreateAuditLogPayload(BaseModel):
    """
    Request schema for creating an audit log entry.
    
    This schema validates incoming audit events from other microservices.
    
    Attributes:
        event_type (str): Type of event (e.g., "TODO_CREATED", "TODO_DELETED")
        resource_id (str): Unique identifier of the affected resource
        message (str): Human-readable description of the event
    
    Example:
        {
            "event_type": "TODO_CREATED",
            "resource_id": "123e4567-e89b-12d3-a456-426614174000",
            "message": "Created todo item 'Buy groceries'"
        }
    """
    event_type: str
    resource_id: str
    message: str


class AuditLogResponse(BaseModel):
    """
    Response schema for audit log entries.
    
    This schema formats audit logs returned by API endpoints.
    Configured to automatically convert ORM models to Pydantic models.
    
    Attributes:
        id (UUID): Unique identifier for the audit log entry
        event_type (str): Type of event that was logged
        resource_id (str): ID of the resource that was affected
        message (str): Description of what happened
        created_at (datetime): When the event was logged (UTC)
    
    Example:
        {
            "id": "456e7890-e89b-12d3-a456-426614174000",
            "event_type": "TODO_CREATED",
            "resource_id": "123e4567-e89b-12d3-a456-426614174000",
            "message": "Created todo item 'Buy groceries'",
            "created_at": "2024-01-15T10:30:00Z"
        }
    """
    # Enable automatic conversion from ORM models
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    event_type: str
    resource_id: str
    message: str
    created_at: datetime
