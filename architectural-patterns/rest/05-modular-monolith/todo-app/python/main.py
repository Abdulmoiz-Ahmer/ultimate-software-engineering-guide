"""
Main Application Entry Point

This module serves as the entry point for the Modular Monolith Todo API.
It initializes the FastAPI application and registers all module routers.

In a modular monolith architecture, the application is organized into independent
modules (domain contexts) that are deployed together as a single unit. Each module
has clear boundaries and can be developed and maintained independently.
"""

from fastapi import FastAPI
from app.modules.todos.router import router as todos_router

# Initialize the FastAPI application with metadata
app = FastAPI(
    title="Modular Monolith Todo API",
    description="A modular monolith application isolating domain contexts in Python",
    version="1.0.0",
)

# Mount module routers independently
# Each module exposes its functionality through a dedicated router
# This allows modules to be plugged in and out easily
app.include_router(todos_router)
