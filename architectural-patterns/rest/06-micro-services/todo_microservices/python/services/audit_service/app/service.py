"""
Business Logic for Audit Service

This module contains the business logic layer for managing audit logs.
It handles database operations for recording and retrieving audit events.

Classes:
    - AuditService: Core service class for audit log operations
"""

from sqlalchemy.orm import Session
from audit_service.app.models import AuditLogORM
from audit_service.app.schemas import CreateAuditLogPayload


class AuditService:
    """
    Service layer for Audit operations.
    
    This class encapsulates the business logic for managing audit logs,
    including persisting events and querying historical logs.
    
    Attributes:
        db (Session): SQLAlchemy database session
    """
    
    def __init__(self, db: Session):
        """
        Initialize the AuditService with a database session.
        
        Args:
            db (Session): SQLAlchemy database session for data persistence
        """
        self.db = db

    def record_log(self, payload: CreateAuditLogPayload) -> AuditLogORM:
        """
        Record a new audit log entry.
        
        This method creates and persists a new audit log entry in the database.
        The timestamp is automatically set to the current UTC time.
        
        Args:
            payload (CreateAuditLogPayload): Audit event data containing
                event_type, resource_id, and message
        
        Returns:
            AuditLogORM: The created audit log entry with generated ID and timestamp
        
        Example:
            service = AuditService(db)
            log = service.record_log(CreateAuditLogPayload(
                event_type="TODO_CREATED",
                resource_id="123e4567-e89b-12d3-a456-426614174000",
                message="Created todo item 'Buy milk'"
            ))
        """
        # Create new audit log ORM instance
        log_entry = AuditLogORM(
            event_type=payload.event_type,
            resource_id=payload.resource_id,
            message=payload.message,
        )
        
        # Persist to database
        self.db.add(log_entry)
        self.db.commit()
        self.db.refresh(log_entry)  # Refresh to get generated ID and timestamp
        
        return log_entry

    def list_logs(self) -> list[AuditLogORM]:
        """
        Retrieve all audit logs ordered by creation time (newest first).
        
        This method queries all audit log entries from the database
        and returns them in descending chronological order.
        
        Returns:
            list[AuditLogORM]: List of all audit log entries, newest first
        
        Example:
            service = AuditService(db)
            logs = service.list_logs()
            for log in logs:
                print(f"{log.created_at}: {log.message}")
        """
        return self.db.query(AuditLogORM).order_by(AuditLogORM.created_at.desc()).all()
