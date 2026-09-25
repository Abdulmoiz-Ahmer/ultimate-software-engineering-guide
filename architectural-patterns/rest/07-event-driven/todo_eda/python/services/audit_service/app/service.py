"""
Audit Service Business Logic

This module contains the core business logic for audit operations.
It handles creating and retrieving audit log entries in the database.
"""

from sqlalchemy.orm import Session
from services.audit_service.app.models import AuditLogORM


class AuditService:
    """
    Service class for audit log operations.
    
    Encapsulates the business logic for recording and retrieving
    audit logs from the database.
    
    Attributes:
        db: SQLAlchemy database session for database operations
    """
    
    def __init__(self, db: Session):
        """
        Initialize the AuditService with a database session.
        
        Args:
            db: SQLAlchemy database session
        """
        self.db = db

    def record_event_log(
        self, event_type: str, resource_id: str, message: str
    ) -> AuditLogORM:
        """
        Record a new audit log entry.
        
        Creates an audit log record in the database to track events
        that occur in other services. This is typically called by
        the event subscriber when processing incoming events.
        
        Args:
            event_type: Type of event being audited (e.g., "TODO_CREATED")
            resource_id: Identifier of the resource affected by the event
            message: Human-readable description of the event
        
        Returns:
            AuditLogORM: The newly created audit log entry with generated ID
        
        Side Effects:
            Inserts a new record into the audit_logs table
        """
        log_entry = AuditLogORM(
            event_type=event_type,
            resource_id=resource_id,
            message=message,
        )
        self.db.add(log_entry)
        self.db.commit()
        self.db.refresh(log_entry)
        return log_entry

    def list_logs(self) -> list[AuditLogORM]:
        """
        Retrieve all audit log entries.
        
        Fetches all audit logs from the database, ordered by creation
        time in descending order (most recent first).
        
        Returns:
            list[AuditLogORM]: List of all audit log entries
        
        Note:
            For production use with large datasets, this should implement
            pagination to avoid performance issues.
        """
        return self.db.query(AuditLogORM).order_by(AuditLogORM.created_at.desc()).all()
