"""
Audit Service - Main Application Entry Point

This module serves as the entry point for the Audit microservice.
It initializes the FastAPI application and registers the audit router.

The Audit service is responsible for receiving and storing audit logs
from other microservices (like the Todo service). It provides a centralized
logging mechanism for tracking events across the system.

Port: 8001 (default)
"""

from fastapi import FastAPI
from audit_service.app.router import router as audit_router

# Initialize FastAPI application with metadata
app = FastAPI(title="Audit Microservice", version="1.0.0")

# Register the audit router to handle all /audit endpoints
app.include_router(audit_router)
