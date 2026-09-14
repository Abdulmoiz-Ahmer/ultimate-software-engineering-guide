"""
Main Application Entry Point - Unidirectional Component Architecture

This module initializes the FastAPI application using the Unidirectional Component
Architecture pattern. In this architecture:

- Components are self-contained, vertical slices of functionality
- Each component owns its routes, handlers, models, and schemas
- Data flow is unidirectional: Router → Handler/Query → Model → Database
- Components communicate through well-defined interfaces (DTOs)
- Shared infrastructure (database, config) lives in the core module

Key Differences from Layered Architecture:
┌─────────────────────────────────────────────────────────────┐
│ Layered (N-Tier)          vs   Unidirectional Component     │
├─────────────────────────────────────────────────────────────┤
│ Horizontal layers              Vertical feature slices      │
│ Layer dependencies             Component independence        │
│ Cross-cutting concerns         Self-contained components    │
│ API → Service → Repo           Router → Handler → Model     │
└─────────────────────────────────────────────────────────────┘

Architecture Benefits:
- Feature isolation: Each component is independent
- Easier to understand: Related code stays together
- Scalable teams: Different teams own different components
- Flexible: Easy to add/remove features without affecting others
"""

from fastapi import FastAPI
from app.components.todos.router import router as todo_router

# Initialize FastAPI application with metadata
app = FastAPI(
    title="Todo Using Unidirectional Component Architecture",
    description="This is a sample todo application structured using unidirectional component architecture",
    version="1.0.0",
)

# Register component routers
# Each component exposes its own router that handles all its endpoints
# Components are independent and can be added/removed easily
app.include_router(todo_router)
