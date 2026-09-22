"""
Todo Service - Main Application Entry Point

This module serves as the entry point for the Todo microservice.
It initializes the FastAPI application and registers the todo router.

The Todo service is responsible for managing todo items (CRUD operations)
and communicating with the Audit service to log events.

Port: 8000 (default)
"""

from fastapi import FastAPI
from todo_service.app.router import router as todo_router

# Initialize FastAPI application with metadata
app = FastAPI(title="Todo Microservice", version="1.0.0")

# Register the todo router to handle all /todos endpoints
app.include_router(todo_router)
