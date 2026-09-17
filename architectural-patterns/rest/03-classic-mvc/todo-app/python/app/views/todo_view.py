"""
View - The "V" in MVC

This module defines the View schemas for the Todo entity. In MVC architecture,
the View is responsible for presentation - how data is displayed to the user.

View Responsibilities in MVC:
┌─────────────────────────────────────────────────────────────┐
│                      View Layer                              │
├─────────────────────────────────────────────────────────────┤
│  ✓ Defines presentation format (JSON schema in REST APIs)   │
│  ✓ Specifies what data is shown to users                    │
│  ✓ Handles data serialization/deserialization               │
│  ✓ Input validation (what user can provide)                 │
│  ✓ Output formatting (what user receives)                   │
│  ✓ Independent of data storage (doesn't know Model details) │
└─────────────────────────────────────────────────────────────┘

View Types in This Module:
1. Input Views (Request Schemas):
   - CreateTodoInputView: What user sends to create a todo
   - UpdateTodoInputView: What user sends to update a todo
   - Validates incoming data before Controller processes it

2. Output Views (Response Schemas):
   - TodoResponseView: How todo data is presented to user
   - Converts Model data to API-friendly format

In Classic MVC (Server-Side Rendering):
- View would be HTML templates (Jinja, ERB, etc.)
- Controller passes Model data to View for rendering
- View generates HTML response

In REST API MVC:
- View is JSON schema (Pydantic models)
- Controller passes Model data to View (Pydantic serialization)
- View generates JSON response

Key Principle: Separation of Concerns
- Model = Data structure (database)
- View = Presentation (API format)
- Controller = Logic (request handling)
"""

from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field


class CreateTodoInputView(BaseModel):
    """
    Input View for creating a new todo.
    
    This View defines what data the user must provide to create a todo.
    It's the "presentation layer" for incoming data, specifying:
    - What fields are required
    - What validation rules apply
    - What constraints exist
    
    In MVC Flow:
    1. User sends JSON matching this schema
    2. Pydantic validates input against this View
    3. Controller receives validated data
    4. Controller creates Model from View data
    
    Attributes:
        title (str): Todo title, 1-100 characters (required)
        description (str | None): Optional description
    """
    
    # Title with validation constraints
    # Field(...) means required
    title: str = Field(..., min_length=1, max_length=100)
    
    # Optional description
    description: str | None = None


class UpdateTodoInputView(BaseModel):
    """
    Input View for updating an existing todo.
    
    This View defines what fields can be updated and their constraints.
    All fields are optional to support partial updates (PATCH semantics).
    
    In MVC Flow:
    1. User sends JSON with fields to update
    2. Pydantic validates input against this View
    3. Controller receives validated data
    4. Controller updates Model with provided fields
    
    Attributes:
        title (str | None): New title (optional)
        description (str | None): New description (optional)
        completed (bool | None): New completion status (optional)
    """
    
    # All fields optional for partial updates
    title: str | None = Field(None, min_length=1, max_length=100)
    description: str | None = None
    completed: bool | None = None


class TodoResponseView(BaseModel):
    """
    Output View for todo responses - The "View" in MVC.
    
    This is the primary View in the MVC pattern - it defines how
    todo data is presented to the user. It's the presentation layer
    that formats Model data into a user-friendly JSON response.
    
    In MVC Flow:
    1. Controller retrieves Model from database
    2. Controller passes Model to View (this schema)
    3. Pydantic serializes Model to JSON using this View
    4. User receives formatted JSON response
    
    View Configuration:
    - from_attributes=True: Allows reading data from ORM models
    - This enables automatic conversion from TodoModel to TodoResponseView
    
    Separation of Concerns:
    - Model (TodoModel): How data is stored (UUID, SQLAlchemy)
    - View (TodoResponseView): How data is presented (JSON, Pydantic)
    - Controller decides which View to use for which response
    
    Attributes:
        id (UUID): Unique identifier
        title (str): Todo title
        description (str | None): Todo description (may be null)
        completed (bool): Completion status
    """
    
    # Configure Pydantic to read from ORM model attributes
    # This is the bridge between Model (data) and View (presentation)
    model_config = ConfigDict(from_attributes=True)

    # All fields included in the response
    # These are "presented" to the user, hence the name "View"
    id: UUID
    title: str
    description: str | None
    completed: bool
