"""
Main application entry point for the Todo API.

This module initializes the FastAPI application and registers all route handlers.
It serves as the top-most layer in the N-tier architecture, orchestrating the
API's startup and configuration.
"""

from fastapi import FastAPI
from app.api.routes import router

# Initialize the FastAPI application with metadata
# This creates the ASGI application that will handle HTTP requests
app = FastAPI(
    title="Todo Using layered architecture",
    description="This is a sample todo application structured using layered architecture",
    version="1.0.0"
)

# Register the todo routes with the application
# The router contains all API endpoints defined in app/api/routes.py
# All routes will be prefixed with "/todos" as defined in the router
app.include_router(router)