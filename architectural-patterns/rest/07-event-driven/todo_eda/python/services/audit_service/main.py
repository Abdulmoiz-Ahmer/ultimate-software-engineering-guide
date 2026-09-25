"""
Audit Service Main Application Entry Point

This module initializes the Audit Consumer Service using FastAPI.
The service consumes events from a message broker, stores audit logs,
and provides an API endpoint to retrieve audit history.

The service runs a background task that continuously listens for events
published by other services (e.g., Todo Service).
"""

import asyncio
from contextlib import asynccontextmanager
from uuid import UUID
from datetime import datetime
from fastapi import FastAPI, Depends
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from services.audit_service.app.database import get_db, Base, engine
from services.audit_service.app.broker.subscriber import start_event_subscriber
from services.audit_service.app.service import AuditService

# Create database tables on application startup
Base.metadata.create_all(bind=engine)


class AuditLogResponse(BaseModel):
    """
    Response model for audit log entries.
    
    Attributes:
        id: Unique identifier for the audit log entry
        event_type: Type of event that was audited (e.g., TODO_CREATED, TODO_DELETED)
        resource_id: ID of the resource that was affected
        message: Human-readable description of the audited event
        created_at: Timestamp when the audit log was created
    """
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    event_type: str
    resource_id: str
    message: str
    created_at: datetime


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan context manager.
    
    Manages the lifecycle of background tasks:
    - On startup: Launches the event subscriber task to consume messages
    - On shutdown: Gracefully cancels the subscriber task
    
    Args:
        app: The FastAPI application instance
    
    Yields:
        Control back to the application during its runtime
    """
    # Startup: Spin up background event consumer loop
    subscriber_task = asyncio.create_task(start_event_subscriber())
    yield
    # Shutdown: Cleanly cancel background worker
    subscriber_task.cancel()


# Initialize FastAPI application with lifespan management
app = FastAPI(title="Audit Consumer Service", version="1.0.0", lifespan=lifespan)


@app.get("/audit/", response_model=list[AuditLogResponse])
def list_audit_logs(db: Session = Depends(get_db)):
    """
    Retrieve all audit logs.
    
    Returns a list of all audit log entries sorted by creation time
    in descending order (most recent first).
    
    Args:
        db: Database session injected by FastAPI dependency
    
    Returns:
        List of AuditLogResponse objects containing all audit logs
    """
    return AuditService(db).list_logs()
