"""
Main Application Entry Point - MVC Architecture

This module initializes the FastAPI application using the Model-View-Controller
(MVC) architectural pattern. MVC is a classic presentation pattern that separates
concerns into three distinct components:

┌─────────────────────────────────────────────────────────────┐
│                    MVC Architecture                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────┐      ┌──────────────┐      ┌──────────────┐ │
│  │  Model   │◄─────│  Controller  │─────►│     View     │ │
│  │ (Data)   │      │   (Logic)    │      │ (Response)   │ │
│  └──────────┘      └──────────────┘      └──────────────┘ │
│       ▲                   ▲                      │          │
│       │                   │                      │          │
│       └───────────────────┴──────────────────────┘          │
│                    Database                                  │
└─────────────────────────────────────────────────────────────┘

MVC Components:
- Model: Represents data structure (TodoModel - database entity)
- View: Represents presentation (TodoResponseView - HTTP response format)
- Controller: Handles requests and coordinates Model/View (todo_controller.py)

This pattern originated for web applications with server-side rendering,
but adapts well to REST APIs where Views become response schemas.
"""

from fastapi import FastAPI
from app.controllers.todo_controller import router as todo_router

# Initialize FastAPI application with MVC architecture metadata
app = FastAPI(
    title="MVC Architecture Todo API",
    description="A clean REST API organized around Model-View-Controller principles",
    version="1.0.0",
)

# Register the todo controller router
# In MVC, controllers handle all HTTP routing and business logic
app.include_router(todo_router)
