# services/todo_service/main.py
"""
Todo Service Main Application Entry Point

This module initializes the Todo Producer Service using FastAPI.
The service handles todo item operations (create, delete) and publishes
events to a message broker for consumption by other services.
"""

from fastapi import FastAPI
from services.todo_service.app.router import router as todo_router

# Initialize FastAPI application with service metadata
app = FastAPI(title="Todo Producer Service", version="1.0.0")

# Register the todo router to handle all todo-related API endpoints
app.include_router(todo_router)
