"""
ORM Models for Audit Service

This module defines the database models (ORM) for the Audit service.
Each model represents a table in the SQLite database.

Models:
    - AuditLogORM: Represents an audit log entry for tracking system events
"""

import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime
from sqlalchemy.types import UUID
from audit_service.app.database import Base


class AuditLogORM(Base):
    """
    Audit log database model.
    
    This model stores audit events received from other microservices.
    Each log entry captures what happened, when it happened, and which
    resource was affected.
    
    Attributes:
        id (UUID): Primary key, automatically generated UUID
        event_type (str): Type of event (e.g., "TODO_CREATED"), max 50 chars
        resource_id (str): ID of the affected resource, max 100 chars
        message (str): Human-readable event description, max 255 chars
        created_at (datetime): Timestamp when the log was created (UTC)
    
    Table:
        audit_logs
    
    Example Entry:
        {
            "id": "456e7890-e89b-12d3-a456-426614174000",
            "event_type": "TODO_CREATED",
            "resource_id": "123e4567-e89b-12d3-a456-426614174000",
            "message": "Created todo item 'Buy groceries'",
            "created_at": "2024-01-15T10:30:00Z"
        }
    """
    __tablename__ = "audit_logs"

    # Primary key with auto-generated UUID
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Type of event being logged (e.g., CREATE, UPDATE, DELETE)
    event_type = Column(String(50), nullable=False)
    
    # ID of the resource that was affected
    resource_id = Column(String(100), nullable=False)
    
    # Human-readable description of what happened
    message = Column(String(255), nullable=False)
    
    # Timestamp when the event occurred (automatically set to current UTC time)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
