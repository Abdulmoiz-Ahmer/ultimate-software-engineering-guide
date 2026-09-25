# services/audit_service/app/models.py
"""
Audit Service ORM Models

This module defines the database models for the Audit Service using SQLAlchemy ORM.
Each model class represents a table in the database for storing audit logs.
"""

import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime
from sqlalchemy.types import UUID
from services.audit_service.app.database import Base


class AuditLogORM(Base):
    """
    Audit log database model.
    
    Represents a single audit log entry in the database, capturing
    events that occur in other services for compliance, debugging,
    and monitoring purposes.
    
    Attributes:
        id: Unique UUID identifier for the audit log entry (auto-generated)
        event_type: Type of event being audited (e.g., "TODO_CREATED", "TODO_DELETED")
        resource_id: Identifier of the resource affected by the event
        message: Human-readable description of the audited event
        created_at: UTC timestamp when the audit log was created (auto-generated)
    """
    __tablename__ = "audit_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_type = Column(String(50), nullable=False)
    resource_id = Column(String(100), nullable=False)
    message = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
