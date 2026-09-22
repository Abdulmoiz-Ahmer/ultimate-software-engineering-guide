"""
HTTP Client for Audit Service Communication

This module provides an HTTP client for communicating with the Audit microservice.
It demonstrates inter-service communication in a microservices architecture.

Classes:
    - AuditServiceClient: Static client for sending audit events
"""

import httpx

# Base URL for the Audit microservice
# In production, this should be configurable via environment variables
AUDIT_SERVICE_URL = "http://localhost:8001/audit/"


class AuditServiceClient:
    """
    Client for sending audit events to the Audit microservice.
    
    This client demonstrates the microservices pattern where services
    communicate over HTTP. The Todo service uses this client to log
    events to the Audit service asynchronously.
    
    Note: This implementation uses synchronous HTTP calls. In production,
    consider using async/await or message queues for better scalability.
    """
    
    @staticmethod
    def send_audit_event(event_type: str, resource_id: str, message: str) -> None:
        """
        Send an audit event to the Audit microservice.
        
        This method makes an HTTP POST request to the Audit service to log
        an event. It implements a fail-safe pattern where audit failures
        don't prevent the main operation from succeeding.
        
        Args:
            event_type (str): Type of event (e.g., "TODO_CREATED", "TODO_DELETED")
            resource_id (str): ID of the affected resource (e.g., todo UUID)
            message (str): Human-readable description of the event
        
        Example:
            AuditServiceClient.send_audit_event(
                event_type="TODO_CREATED",
                resource_id="123e4567-e89b-12d3-a456-426614174000",
                message="Created todo 'Buy milk'"
            )
        
        Error Handling:
            If the Audit service is unavailable or times out, the error is logged
            but not propagated. This ensures that audit logging failures don't
            break the main todo operations (fail-safe pattern).
        """
        # Prepare the audit event payload
        payload = {
            "event_type": event_type,
            "resource_id": resource_id,
            "message": message,
        }
        
        try:
            # Send POST request to Audit service with 3-second timeout
            with httpx.Client(timeout=3.0) as client:
                client.post(AUDIT_SERVICE_URL, json=payload)
        except httpx.RequestError as err:
            # Fallback error handling: log network failure without stopping todo execution
            # In production, consider using a proper logging framework
            print(f"[WARNING] Could not reach Audit Microservice: {err}")
