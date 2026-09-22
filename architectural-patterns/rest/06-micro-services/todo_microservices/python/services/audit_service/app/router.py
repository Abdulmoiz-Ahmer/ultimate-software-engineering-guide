"""
API Routes for Audit Service

This module defines the FastAPI router and HTTP endpoints for the Audit service.
It handles incoming HTTP requests for logging and retrieving audit events.

Endpoints:
    - POST /audit/: Record a new audit log entry
    - GET /audit/: Retrieve all audit logs (newest first)

Database initialization happens on module load.
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from audit_service.app.database import get_db, Base, engine
from audit_service.app.schemas import CreateAuditLogPayload, AuditLogResponse
from audit_service.app.service import AuditService

# Auto-create SQLite table on startup
# This ensures the audit_logs table exists before handling requests
Base.metadata.create_all(bind=engine)

# Create API router with common prefix and tags
router = APIRouter(prefix="/audit", tags=["Audit Microservice"])


@router.post("/", response_model=AuditLogResponse, status_code=status.HTTP_201_CREATED)
def create_log(payload: CreateAuditLogPayload, db: Session = Depends(get_db)):
    """
    Record a new audit log entry.
    
    This endpoint receives audit events from other microservices
    (like the Todo service) and persists them to the database.
    
    Args:
        payload (CreateAuditLogPayload): Audit event data containing
            event_type, resource_id, and message
        db (Session): Database session (injected dependency)
    
    Returns:
        AuditLogResponse: The created audit log with generated ID and timestamp
    
    Status Codes:
        - 201: Audit log created successfully
        - 422: Validation error (invalid payload)
    
    Example Request:
        POST /audit/
        {
            "event_type": "TODO_CREATED",
            "resource_id": "123e4567-e89b-12d3-a456-426614174000",
            "message": "Created todo item 'Buy groceries'"
        }
    
    Example Response:
        {
            "id": "456e7890-e89b-12d3-a456-426614174000",
            "event_type": "TODO_CREATED",
            "resource_id": "123e4567-e89b-12d3-a456-426614174000",
            "message": "Created todo item 'Buy groceries'",
            "created_at": "2024-01-15T10:30:00Z"
        }
    """
    return AuditService(db).record_log(payload)


@router.get("/", response_model=list[AuditLogResponse])
def list_logs(db: Session = Depends(get_db)):
    """
    Retrieve all audit logs.
    
    This endpoint returns all audit log entries stored in the database,
    ordered by creation time (newest first). Useful for monitoring and
    debugging system activity.
    
    Args:
        db (Session): Database session (injected dependency)
    
    Returns:
        list[AuditLogResponse]: List of all audit logs, newest first
    
    Status Codes:
        - 200: Successfully retrieved audit logs
    
    Example Request:
        GET /audit/
    
    Example Response:
        [
            {
                "id": "456e7890-e89b-12d3-a456-426614174000",
                "event_type": "TODO_DELETED",
                "resource_id": "123e4567-e89b-12d3-a456-426614174000",
                "message": "Deleted todo item ID 123e4567-e89b-12d3-a456-426614174000",
                "created_at": "2024-01-15T11:00:00Z"
            },
            {
                "id": "789e1234-e89b-12d3-a456-426614174000",
                "event_type": "TODO_CREATED",
                "resource_id": "123e4567-e89b-12d3-a456-426614174000",
                "message": "Created todo item 'Buy groceries'",
                "created_at": "2024-01-15T10:30:00Z"
            }
        ]
    """
    return AuditService(db).list_logs()
