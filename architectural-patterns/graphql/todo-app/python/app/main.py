# app/main.py
"""
FastAPI Application Entry Point

This module sets up the FastAPI application with GraphQL support using Strawberry.

Architecture:
- FastAPI: Web framework for handling HTTP requests
- Strawberry: GraphQL library for Python
- SQLAlchemy: ORM for database operations
- DataLoaders: For solving the N+1 query problem

Key Features:
1. Database session management with dependency injection
2. Per-request DataLoader creation for optimal performance
3. GraphQL endpoint at /graphql with GraphiQL interface
"""

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from strawberry.fastapi import GraphQLRouter

from app.core.database import SessionLocal, init_db_with_seed
from app.dataloaders import create_dataloaders
from app.schema import schema

# Initialize database schema and populate with sample seed data
# This runs once at application startup
# WARNING: In production, use proper database migrations (e.g., Alembic)
# instead of recreating the database on each startup
init_db_with_seed()


def get_db():
    """
    Database session dependency for FastAPI.
    
    This function provides a database session for each request and ensures
    proper cleanup after the request is completed.
    
    Yields:
        Session: SQLAlchemy database session
        
    Usage:
        @app.get("/items")
        def read_items(db: Session = Depends(get_db)):
            return db.query(Item).all()
            
    The session is automatically closed after the request, even if an
    exception occurs, thanks to the try/finally block.
    """
    # Create a new database session
    db = SessionLocal()
    try:
        # Yield the session to the request handler
        yield db
    finally:
        # Always close the session after the request is complete
        # This prevents connection leaks and ensures proper resource cleanup
        db.close()


async def get_graphql_context(db: Session = Depends(get_db)):
    """
    GraphQL context factory function.
    
    This function is called for each GraphQL request to create the context
    object that is accessible in all resolvers via info.context.
    
    The context contains:
    1. db: Database session for executing queries
    2. dataloaders: Fresh DataLoader instances for this request
    
    Args:
        db: Database session injected by FastAPI's dependency system
        
    Returns:
        dict: Context dictionary with db session and DataLoaders
        
    CRITICAL: DataLoaders are created per-request, not per-application.
    This prevents:
    - Cache leaks between requests (security issue)
    - Stale data from previous requests
    - Memory leaks from unbounded cache growth
    
    Each request gets its own isolated set of DataLoaders with fresh caches.
    """
    return {
        "db": db,
        "dataloaders": create_dataloaders(db),
    }


# Create GraphQL router with Strawberry
# This router handles all GraphQL requests and provides:
# - GraphQL endpoint for queries/mutations
# - GraphiQL interface for testing (in development)
graphql_app = GraphQLRouter(
    schema=schema,
    context_getter=get_graphql_context,
)

# Create FastAPI application
# title appears in the auto-generated API documentation
app = FastAPI(title="GraphQL DataLoader & Security Engine")

# Mount the GraphQL router at /graphql
# Access the GraphiQL interface at: http://localhost:8000/graphql
# The GraphiQL interface allows you to:
# - Write and test GraphQL queries interactively
# - Explore the schema documentation
# - View query execution results
app.include_router(graphql_app, prefix="/graphql")

# To run the application:
# uvicorn app.main:app --reload
#
# Then visit http://localhost:8000/graphql in your browser
