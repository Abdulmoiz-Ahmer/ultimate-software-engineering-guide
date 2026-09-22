# Audit Microservice

## Overview

The Audit Microservice is a centralized logging service that receives and stores audit events from other microservices. It provides a single source of truth for tracking system-wide events, enabling monitoring, debugging, and compliance.

## Architecture

This service follows a layered architecture:

- **API Layer** (`router.py`): HTTP endpoints for receiving and querying logs
- **Service Layer** (`service.py`): Business logic for log management
- **Data Layer** (`models.py`, `database.py`): Database models and persistence
- **Schema Layer** (`schemas.py`): Request/response validation

## Features

- Receive audit events from other microservices
- Store audit logs with timestamps
- Query all audit logs (ordered by newest first)
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

### Create Audit Log
```http
POST /audit/
Content-Type: application/json

{
  "event_type": "TODO_CREATED",
  "resource_id": "123e4567-e89b-12d3-a456-426614174000",
  "message": "Created todo item 'Buy groceries'"
}
```

**Response** (201 Created):
```json
{
  "id": "456e7890-e89b-12d3-a456-426614174000",
  "event_type": "TODO_CREATED",
  "resource_id": "123e4567-e89b-12d3-a456-426614174000",
  "message": "Created todo item 'Buy groceries'",
  "created_at": "2024-01-15T10:30:00Z"
}
```

### List All Audit Logs
```http
GET /audit/
```

**Response** (200 OK):
```json
[
  {
    "id": "789e1234-e89b-12d3-a456-426614174000",
    "event_type": "TODO_DELETED",
    "resource_id": "123e4567-e89b-12d3-a456-426614174000",
    "message": "Deleted todo item ID 123e4567-e89b-12d3-a456-426614174000",
    "created_at": "2024-01-15T11:00:00Z"
  },
  {
    "id": "456e7890-e89b-12d3-a456-426614174000",
    "event_type": "TODO_CREATED",
    "resource_id": "123e4567-e89b-12d3-a456-426614174000",
    "message": "Created todo item 'Buy groceries'",
    "created_at": "2024-01-15T10:30:00Z"
  }
]
```

## Database Schema

### audit_logs Table

| Column      | Type         | Constraints                |
|-------------|--------------|----------------------------|
| id          | UUID         | Primary Key                |
| event_type  | VARCHAR(50)  | NOT NULL                   |
| resource_id | VARCHAR(100) | NOT NULL                   |
| message     | VARCHAR(255) | NOT NULL                   |
| created_at  | TIMESTAMP    | DEFAULT NOW (UTC)          |

## Event Types

Common event types logged by this service:

- **TODO_CREATED**: A new todo item was created
- **TODO_DELETED**: A todo item was deleted
- **TODO_UPDATED**: A todo item was modified (future)
- **USER_LOGIN**: User authentication event (future)
- **USER_LOGOUT**: User logout event (future)

## Setup and Installation

### Prerequisites

- Python 3.14+
- uv package manager

### Installation

```bash
# Navigate to the service directory
cd audit_service

# Install dependencies
uv sync

# Run database migrations (if needed)
uv run alembic upgrade head
```

## Running the Service

### Development Mode

```bash
# Start the service on port 8001
uv run uvicorn audit_service.main:app --reload --port 8001
```

### Production Mode

```bash
# Start with multiple workers
uv run uvicorn audit_service.main:app --host 0.0.0.0 --port 8001 --workers 4
```

## Configuration

### Environment Variables

- `DATABASE_URL`: Database connection string (default: `sqlite:///./audit.db`)

## Testing

```bash
# Create an audit log entry
curl -X POST http://localhost:8001/audit/ \
  -H "Content-Type: application/json" \
  -d '{
    "event_type": "TEST_EVENT",
    "resource_id": "test-123",
    "message": "Testing the audit service"
  }'

# List all audit logs
curl http://localhost:8001/audit/
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
audit_service/
├── app/
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

- **422 Unprocessable Entity**: Invalid input data
- **500 Internal Server Error**: Database or unexpected errors

## Best Practices Demonstrated

1. **Single Responsibility**: Service focuses solely on audit logging
2. **Separation of Concerns**: Clear separation between API, business logic, and data layers
3. **Dependency Injection**: Database sessions injected via FastAPI's `Depends`
4. **Type Safety**: Full type hints for better code quality
5. **Validation**: Pydantic schemas for request/response validation
6. **Database Sessions**: Proper session management with automatic cleanup
7. **UTC Timestamps**: All timestamps stored in UTC for consistency

## Use Cases

### Monitoring
Query audit logs to monitor system activity in real-time.

### Debugging
Trace the sequence of events leading to a bug or issue.

### Compliance
Maintain an immutable audit trail for regulatory compliance.

### Analytics
Analyze usage patterns and user behavior across services.

## Security Considerations

- **Authentication**: Add API key or OAuth2 authentication for production
- **Authorization**: Implement role-based access control
- **Rate Limiting**: Prevent abuse with rate limiting
- **Data Retention**: Implement log rotation and archiving policies
- **Encryption**: Encrypt sensitive data in audit logs

## Performance Considerations

- **Indexing**: Add database indexes on frequently queried columns (event_type, created_at)
- **Pagination**: Implement pagination for the list endpoint
- **Asynchronous Processing**: Use async/await for better throughput
- **Message Queue**: Consider using a message queue (RabbitMQ, Kafka) for high-volume scenarios
- **Read Replicas**: Use database read replicas for query scaling

## Future Enhancements

- [ ] Add filtering by event_type, resource_id, and date range
- [ ] Implement pagination for list endpoint
- [ ] Add search functionality
- [ ] Implement async database operations
- [ ] Add authentication and authorization
- [ ] Use message queue for event ingestion
- [ ] Add comprehensive test suite
- [ ] Add health check endpoint
- [ ] Add metrics and monitoring
- [ ] Implement log retention policies
- [ ] Add data export functionality (CSV, JSON)
