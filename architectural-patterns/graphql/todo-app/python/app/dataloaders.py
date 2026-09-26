# app/dataloaders.py
"""
DataLoader Implementation Module

This module implements Facebook's DataLoader pattern to solve the N+1 query problem
in GraphQL. DataLoaders batch and cache database requests within a single request.

Key Concepts:
- Batching: Multiple individual loads are collected and executed as a single query
- Caching: Results are cached per-request to avoid duplicate queries
- Per-Request: New DataLoader instances are created for each HTTP request

The N+1 Problem Without DataLoaders:
    Query: Get 3 users and their todos
    - 1 query to fetch all users
    - 3 queries to fetch todos (one per user)
    Total: 4 queries (N+1 where N=3)

With DataLoaders:
    - 1 query to fetch all users
    - 1 batched query to fetch all todos for all users
    Total: 2 queries
"""

from uuid import UUID
from collections import defaultdict
from strawberry.dataloader import DataLoader
from sqlalchemy.orm import Session
from app.models import TodoORM, UserORM


async def batch_load_todos_by_user_id(
    keys: list[UUID], db: Session
) -> list[list[TodoORM]]:
    """
    Batch function for loading todos by user IDs.
    
    This function is called by the DataLoader when multiple todos.load(user_id)
    calls are batched together.
    
    Args:
        keys: List of user IDs that need their todos loaded
        db: SQLAlchemy database session
        
    Returns:
        List of todo lists, one for each key, in the EXACT same order as keys
        
    CRITICAL RULE: The returned list MUST match the exact order and length
    of the input 'keys' list! DataLoader depends on this positional mapping.
    
    Example:
        keys = [uuid1, uuid2, uuid3]
        returns = [
            [todo1, todo2],  # todos for uuid1
            [],              # no todos for uuid2
            [todo3]          # one todo for uuid3
        ]
    """
    # Execute a SINGLE query with WHERE IN clause instead of N separate queries
    # This is the key to solving the N+1 problem
    todos = db.query(TodoORM).filter(TodoORM.user_id.in_(keys)).all()

    # Group todos by their user_id using a defaultdict
    # defaultdict returns an empty list for missing keys
    user_todos_map = defaultdict(list)
    for todo in todos:
        user_todos_map[todo.user_id].append(todo)

    # Return lists in the exact order requested by 'keys'
    # If a user has no todos, returns an empty list
    return [user_todos_map[user_id] for user_id in keys]


async def batch_load_users_by_id(keys: list[UUID], db: Session) -> list[UserORM | None]:
    """
    Batch function for loading users by primary keys.
    
    This function is called by the DataLoader when multiple user.load(id)
    calls are batched together.
    
    Args:
        keys: List of user IDs to load
        db: SQLAlchemy database session
        
    Returns:
        List of User objects (or None for missing users), in the same order as keys
        
    Note: Returns None for keys that don't correspond to existing users.
    DataLoader handles None values gracefully.
    """
    # Single query to fetch all requested users
    users = db.query(UserORM).filter(UserORM.id.in_(keys)).all()
    
    # Create a dictionary for O(1) lookup by user ID
    user_map = {user.id: user for user in users}

    # Return users in the exact order of the input keys
    # Returns None if a user ID doesn't exist
    return [user_map.get(user_id) for user_id in keys]


def create_dataloaders(db: Session) -> dict[str, DataLoader]:
    """
    Factory function to instantiate fresh DataLoaders PER REQUEST.
    
    This function is called by the GraphQL context getter for each HTTP request.
    
    Args:
        db: SQLAlchemy database session for this request
        
    Returns:
        Dictionary of DataLoader instances keyed by name
        
    WARNING: Never share DataLoader instances across requests!
    Reasons:
    1. Cache Leaks: User A could see cached data from User B's request
    2. Stale Data: Cached data from previous requests may be outdated
    3. Memory Leaks: Caches would grow indefinitely across all requests
    
    DataLoaders are designed to be request-scoped, not application-scoped.
    """
    return {
        # DataLoader for fetching todos by user ID
        # Used by UserType.todos field resolver
        "todos_by_user_id": DataLoader(
            load_fn=lambda keys: batch_load_todos_by_user_id(keys, db)
        ),
        
        # DataLoader for fetching users by ID
        # Used by TodoType.author field resolver
        "user_by_id": DataLoader(load_fn=lambda keys: batch_load_users_by_id(keys, db)),
    }
