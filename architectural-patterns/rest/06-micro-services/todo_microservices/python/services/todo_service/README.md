# Todo Microservice

## Overview

The Todo Microservice is a RESTful API service responsible for managing todo items. It demonstrates core microservices patterns including service independence, inter-service communication, and separation of concerns.

## Architecture

This service follows a layered architecture:

- **API Layer** (`router.py`): HTTP endpoints and request/response handling
- **Service Layer** (`service.py`): Business logic and orchestration
- **Data Layer** (`models.py`, `database.py`): Database models and persistence
- **Integration Layer** (`clients/`): Communication with other microservices
- **Schema Layer** (`schemas.py`): Request/response validation

## Features

- Create todo items with title and description
- Delete todo items by UUID
- Automatic audit logging via Audit microservice
- SQLite database with SQLAlchemy ORM
- Automatic database schema creation
- Input validation with Pydantic

## Technology Stack

- **Framework**: FastAPI 0.141.1+
- **Database**: SQLite with SQLAlchemy 2.0.54+
- **Migration**: Alembic 1.20.0+
- **Validation**: Pydantic 2.13.5+
- **HTTP Client**: httpx 0.28.1+
- **Server**: Uvicorn 0.53.0+

## API Endpoints

### Create Todo
```http
POST /todos/
Content-Type: application/json

{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread"
}
```

**Response** (201 Created):
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false
}
```

### Delete Todo
```http
DELETE /todos/{todo_id}
```

**Response**: 204 No Content

## Database Schema

### todos Table

| Column      | Type         | Constraints                |
|-------------|--------------|----------------------------|
| id          | UUID         | Primary Key                |
| title       | VARCHAR(100) | NOT NULL                   |
| description | VARCHAR(255) | NULL                       |
| completed   | BOOLEAN      | DEFAULT FALSE              |

## Inter-Service Communication

This service communicates with the **Audit Microservice** to log events:

- **TODO_CREATED**: Logged when a new todo is created
- **TODO_DELETED**: Logged when a todo is deleted

The communication uses HTTP POST requests with a fail-safe pattern - if the Audit service is unavailable, the todo operation still succeeds.

## Setup and Installation

### Prerequisites

- Python 3.14+
- uv package manager

### Installation

```bash
# Navigate to the service directory
cd todo_service

# Install dependencies
uv sync

# Run database migrations (if needed)
uv run alembic upgrade head
```

## Running the Service

### Development Mode

```bash
# Start the service on port 8000
uv run uvicorn todo_service.main:app --reload --port 8000
```

### Production Mode

```bash
# Start with multiple workers
uv run uvicorn todo_service.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## Configuration

### Environment Variables

- `DATABASE_URL`: Database connection string (default: `sqlite:///./todos.db`)
- `AUDIT_SERVICE_URL`: Audit service endpoint (default: `http://localhost:8001/audit/`)

## Testing

```bash
# Run with curl
curl -X POST http://localhost:8000/todos/ \
  -H "Content-Type: application/json" \
  -d '{"title":"Test Todo","description":"Testing the API"}'

# List todos (not implemented in this version)
# Delete a todo
curl -X DELETE http://localhost:8000/todos/{todo-id}
```

## Database Migrations

This service uses Alembic for database migrations:

```bash
# Create a new migration
uv run alembic revision --autogenerate -m "Description of changes"

# Apply migrations
uv run alembic upgrade head

# Rollback one migration
uv run alembic downgrade -1
```

## Project Structure

```
todo_service/
├── app/
│   ├── clients/
│   │   └── audit_client.py    # HTTP client for Audit service
│   ├── database.py             # Database configuration
│   ├── models.py               # SQLAlchemy ORM models
│   ├── router.py               # API endpoints
│   ├── schemas.py              # Pydantic validation schemas
│   └── service.py              # Business logic
├── alembic/                    # Database migrations
├── main.py                     # Application entry point
├── pyproject.toml              # Project dependencies
└── README.md                   # This file
```

## Error Handling

- **404 Not Found**: Todo with specified ID doesn't exist
- **422 Unprocessable Entity**: Invalid input data
- **500 Internal Server Error**: Database or unexpected errors

## Best Practices Demonstrated

1. **Separation of Concerns**: Clear separation between API, business logic, and data layers
2. **Dependency Injection**: Database sessions injected via FastAPI's `Depends`
3. **Fail-Safe Pattern**: Audit logging failures don't break main operations
4. **Type Safety**: Full type hints for better code quality
5. **Validation**: Pydantic schemas for request/response validation
6. **Database Sessions**: Proper session management with automatic cleanup

## Future Enhancements

- [ ] Add GET endpoint to list all todos
- [ ] Add PUT/PATCH endpoint to update todos
- [ ] Add filtering and pagination
- [ ] Implement async database operations
- [ ] Add authentication and authorization
- [ ] Use message queue for audit events
- [ ] Add comprehensive test suite
- [ ] Add health check endpoint
- [ ] Add metrics and monitoring
