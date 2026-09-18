"""
Main application entry point for the Clean Architecture Todo API.

This module bootstraps the FastAPI application and registers the todo router.
It serves as the composition root where all the application components come together.
"""

from fastapi import FastAPI
from app.frameworks_and_drivers.web.routes import router as todo_router

# Initialize the FastAPI application with metadata
app = FastAPI(
    title="Uncle Bob Clean Architecture Todo API",
    description="Decoupled application built with FastAPI, SQLAlchemy, and SQLite",
    version="1.0.0",
)

# Register the todo router to handle all /todos endpoints
app.include_router(todo_router)
