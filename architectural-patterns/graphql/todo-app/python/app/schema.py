# app/schema.py
"""
GraphQL Schema Definition Module

This module defines the GraphQL schema using Strawberry, including:
- GraphQL types (TodoType, UserType)
- Field resolvers with DataLoader integration
- Query root
- Security extensions (Query Depth Limiter)

The schema demonstrates best practices for:
1. Solving the N+1 query problem with DataLoaders
2. Preventing malicious recursive queries with depth limiting
"""

import strawberry
from uuid import UUID
from typing import TYPE_CHECKING
from strawberry.types import Info
from strawberry.extensions import QueryDepthLimiter
from app.models import UserORM
from app.services.todo_service import TodoService

# TYPE_CHECKING is True only during static type checking (mypy, pyright)
# This avoids circular import issues while maintaining type hints
if TYPE_CHECKING:
    from app.schema import UserType


@strawberry.type
class TodoType:
    """
    GraphQL Type for Todo items

    Fields:
        id: Unique identifier (UUID)
        title: Todo description
        completed: Completion status (boolean)
        user_id: ID of the user who owns this todo
        author: The user who created this todo (resolved via DataLoader)
    """

    id: UUID
    title: str
    completed: bool
    user_id: UUID

    @strawberry.field
    async def author(self, info: Info) -> "UserType":
        """
        Resolves the author (user) of this todo.

        This field resolver uses DataLoader to avoid the N+1 query problem.

        Without DataLoader:
            - Fetching 10 todos would trigger 10 separate user queries

        With DataLoader:
            - All user IDs are collected and fetched in a single batched query

        Args:
            info: Strawberry Info object containing request context

        Returns:
            UserType: The user who created this todo

        Note: The dataloader.load() call doesn't execute immediately.
        DataLoader collects all load() calls and batches them together.
        """
        # Access the user_by_id DataLoader from the request context
        dataloader = info.context["dataloaders"]["user_by_id"]

        # .load() returns a Promise that DataLoader resolves asynchronously
        # Multiple .load() calls are automatically batched into one query
        return await dataloader.load(self.user_id)


@strawberry.type
class UserType:
    """
    GraphQL Type for User

    Fields:
        id: Unique identifier (UUID)
        name: User's name
        todos: List of todos belonging to this user (resolved via DataLoader)
    """

    id: UUID
    name: str

    @strawberry.field
    async def todos(self, info: Info) -> list[TodoType]:
        """
        Resolves all todos for this user.

        This field resolver uses DataLoader to batch todo queries.

        Example Query:
            {
              users {
                name
                todos {
                  title
                }
              }
            }

        Without DataLoader:
            - 1 query for users
            - N queries for todos (one per user)
            - Total: N+1 queries

        With DataLoader:
            - 1 query for users
            - 1 batched query for all todos
            - Total: 2 queries

        Args:
            info: Strawberry Info object containing request context

        Returns:
            list[TodoType]: All todos belonging to this user
        """
        # Access the todos_by_user_id DataLoader from the request context
        dataloader = info.context["dataloaders"]["todos_by_user_id"]

        # DataLoader batches this load with others and executes a single query
        return await dataloader.load(self.id)


@strawberry.input
class CreateTodoInput:
    """
    Input type for creating a new Todo.
    
    GraphQL Input types are used for mutation arguments to group
    related fields together, improving API organization.
    
    Fields:
        title: The todo description/title (required)
        user_id: The ID of the user who owns this todo (required)
    
    Example Usage:
        mutation {
          createTodo(input: {
            title: "Buy groceries"
            userId: "123e4567-e89b-12d3-a456-426614174000"
          }) {
            id
            title
          }
        }
    """
    title: str
    user_id: UUID


@strawberry.input
class UpdateTodoInput:
    """
    Input type for updating an existing Todo.
    
    All fields are optional, allowing partial updates.
    Only provided fields will be updated on the Todo.
    
    Fields:
        title: New title for the todo (optional)
        completed: Completion status (optional)
    
    Example Usage:
        mutation {
          updateTodo(
            id: "123e4567-e89b-12d3-a456-426614174000"
            input: { completed: true }
          ) {
            id
            title
            completed
          }
        }
    """
    title: str | None = None
    completed: bool | None = None


@strawberry.type
class Query:
    """
    Root Query Type

    Defines the entry points for GraphQL queries.
    """

    @strawberry.field
    def users(self, info: Info) -> list[UserType]:
        """
        Root query: Fetch all users.

        Example Query:
            {
              users {
                id
                name
                todos {
                  title
                  author {
                    name
                  }
                }
              }
            }

        Args:
            info: Strawberry Info object containing request context

        Returns:
            list[UserType]: All users in the database
        """
        # Access the database session from the request context
        db = info.context["db"]

        # Fetch all users using SQLAlchemy
        return db.query(UserORM).all()


@strawberry.type
class Mutation:
    """
    Root Mutation Type
    
    Defines the entry points for GraphQL mutations (write operations).
    Mutations allow clients to modify data on the server.
    
    Best Practices:
    - Use service layer (TodoService) for business logic
    - Keep resolvers thin (delegate to services)
    - Return updated objects for optimistic UI updates
    - Use input types for grouping related arguments
    """

    @strawberry.mutation
    def create_todo(self, info: Info, input: CreateTodoInput) -> TodoType:
        """
        Create a new Todo item.
        
        This mutation creates a todo and associates it with a user.
        The service layer handles database operations and validation.
        
        Args:
            info: Strawberry Info object containing request context
            input: CreateTodoInput with title and user_id
            
        Returns:
            TodoType: The newly created todo with generated ID
            
        Example Mutation:
            mutation {
              createTodo(input: {
                title: "Buy groceries"
                userId: "123e4567-e89b-12d3-a456-426614174000"
              }) {
                id
                title
                author {
                  name
                }
              }
            }
            
        Raises:
            ValueError: If user_id doesn't exist in the database
        """
        # Access the database session from the request context
        db = info.context["db"]
        
        # Delegate business logic to the service layer
        # Services encapsulate database operations and validation
        return TodoService(db).create_todo(title=input.title, user_id=input.user_id)

    @strawberry.mutation
    def update_todo(self, info: Info, id: UUID, input: UpdateTodoInput) -> TodoType:
        """
        Update an existing Todo item.
        
        Supports partial updates - only provided fields are modified.
        The service layer handles validation and database updates.
        
        Args:
            info: Strawberry Info object containing request context
            id: UUID of the todo to update
            input: UpdateTodoInput with optional title and completed fields
            
        Returns:
            TodoType: The updated todo with all current values
            
        Example Mutation:
            mutation {
              updateTodo(
                id: "123e4567-e89b-12d3-a456-426614174000"
                input: {
                  title: "Buy organic groceries"
                  completed: true
                }
              ) {
                id
                title
                completed
              }
            }
            
        Raises:
            ValueError: If todo with given ID doesn't exist
        """
        # Access the database session from the request context
        db = info.context["db"]
        
        # Delegate to service layer for update logic
        return TodoService(db).update_todo(
            id=id, title=input.title, completed=input.completed
        )

    @strawberry.mutation
    def delete_todo(self, info: Info, id: UUID) -> bool:
        """
        Delete a Todo item by ID.
        
        Permanently removes a todo from the database.
        Returns boolean indicating success or failure.
        
        Args:
            info: Strawberry Info object containing request context
            id: UUID of the todo to delete
            
        Returns:
            bool: True if deleted successfully, False if todo not found
            
        Example Mutation:
            mutation {
              deleteTodo(id: "123e4567-e89b-12d3-a456-426614174000")
            }
            
        Note: This operation is destructive and cannot be undone.
        Consider implementing soft deletes for production applications.
        """
        # Access the database session from the request context
        db = info.context["db"]
        
        # Delegate to service layer for deletion logic
        return TodoService(db).delete_todo(id=id)


# Register Schema with Security Extensions
#
# QueryDepthLimiter prevents malicious recursive queries that could
# cause server overload or denial of service attacks.
#
# Example of a malicious query (depth = 6):
#   {
#     users {           # depth 1
#       todos {         # depth 2
#         author {      # depth 3
#           todos {     # depth 4
#             author {  # depth 5
#               todos { # depth 6 - REJECTED!
#                 ...
#               }
#             }
#           }
#         }
#       }
#     }
#   }
#
# With max_depth=3, the above query is rejected before execution,
# preventing resource exhaustion.
schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    extensions=[QueryDepthLimiter(max_depth=3)],  # Max allowed nesting = 3
)
