# Todo API - Layered (N-Tier) Architecture

A RESTful Todo API built with FastAPI demonstrating the **Layered (N-Tier) Architecture** pattern. This project showcases clean separation of concerns across distinct layers, making the codebase maintainable, testable, and scalable.

## 🏗️ Architecture Overview

This application implements a classic **4-layer N-tier architecture**:

```
┌─────────────────────────────────────────┐
│     Presentation Layer (API Layer)      │
│         app/api/routes.py                │
│    - HTTP endpoints & routing            │
│    - Request/response handling           │
│    - Dependency injection                │
└─────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│      Business Logic Layer (Service)      │
│       app/services/todo_service.py       │
│    - Business rules & validation         │
│    - Orchestration logic                 │
│    - Error handling                      │
└─────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│    Data Access Layer (Repository)        │
│   app/repositories/todo_repository.py    │
│    - Database CRUD operations            │
│    - Query abstraction                   │
│    - Data persistence                    │
└─────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│         Data Model Layer (ORM)           │
│        app/models/todo.py                │
│    - Database schema definition          │
│    - SQLAlchemy models                   │
└─────────────────────────────────────────┘
```

### Layer Responsibilities

| Layer | Purpose | Key Files |
|-------|---------|-----------|
| **API Layer** | Handles HTTP requests/responses, routing, and serialization | `app/api/routes.py`, `app/api/schemas.py` |
| **Service Layer** | Implements business logic and orchestrates operations | `app/services/todo_service.py` |
| **Repository Layer** | Abstracts data access and database operations | `app/repositories/todo_repository.py` |
| **Model Layer** | Defines data structures and database schema | `app/models/todo.py` |

## ✨ Key Features

- ✅ **Clean Architecture**: Clear separation of concerns across layers
- ✅ **RESTful API**: Standard HTTP methods (GET, POST, PATCH, DELETE)
- ✅ **UUID Primary Keys**: Globally unique identifiers for security
- ✅ **Dependency Injection**: Loose coupling via FastAPI's DI system
- ✅ **Repository Pattern**: Abstracted data access layer
- ✅ **Type Safety**: Full type hints with Pydantic validation
- ✅ **Database Migrations**: Version-controlled schema with Alembic
- ✅ **Auto-generated Documentation**: Interactive API docs via OpenAPI/Swagger

## 🛠️ Technology Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) - Modern, high-performance web framework
- **ORM**: [SQLAlchemy](https://www.sqlalchemy.org/) - SQL toolkit and Object-Relational Mapping
- **Database**: SQLite (easily swappable to PostgreSQL, MySQL, etc.)
- **Migrations**: [Alembic](https://alembic.sqlalchemy.org/) - Database migration tool
- **Validation**: [Pydantic](https://docs.pydantic.dev/) - Data validation using Python type hints
- **Server**: [Uvicorn](https://www.uvicorn.org/) - ASGI server implementation

## 📋 Prerequisites

- Python 3.10 or higher
- pip (Python package manager)

## 🚀 Getting Started

### 1. Installation

```bash
# Navigate to the project directory
cd architectural-patterns/rest/01-layered-ntier/todo-app/python

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Database Setup

```bash
# Run database migrations to create tables
alembic upgrade head
```

This creates a `todos.db` SQLite database file with the required schema.

### 3. Run the Application

```bash
# Start the development server
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### 4. Access API Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📡 API Endpoints

| Method | Endpoint | Description | Request Body | Response |
|--------|----------|-------------|--------------|----------|
| `POST` | `/todos/` | Create a new todo | `TodoCreate` | `TodoResponse` (201) |
| `GET` | `/todos/` | Get all todos | - | `List[TodoResponse]` (200) |
| `GET` | `/todos/{id}` | Get a specific todo | - | `TodoResponse` (200) |
| `PATCH` | `/todos/{id}` | Update a todo (partial) | `TodoUpdate` | `TodoResponse` (200) |
| `DELETE` | `/todos/{id}` | Delete a todo | - | No content (204) |

### Request/Response Examples

#### Create a Todo
```bash
curl -X POST "http://localhost:8000/todos/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Buy groceries",
    "description": "Milk, eggs, bread"
  }'
```

**Response (201 Created):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false
}
```

#### Get All Todos
```bash
curl -X GET "http://localhost:8000/todos/"
```

**Response (200 OK):**
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "completed": false
  }
]
```

#### Update a Todo
```bash
curl -X PATCH "http://localhost:8000/todos/550e8400-e29b-41d4-a716-446655440000" \
  -H "Content-Type: application/json" \
  -d '{
    "completed": true
  }'
```

**Response (200 OK):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": true
}
```

#### Delete a Todo
```bash
curl -X DELETE "http://localhost:8000/todos/550e8400-e29b-41d4-a716-446655440000"
```

**Response:** `204 No Content`

## 📁 Project Structure

```
python/
├── alembic/                      # Database migration files
│   ├── versions/                 # Migration version files
│   │   └── 6034f17cd7d6_create_initial_todos_table.py
│   └── env.py                    # Alembic environment configuration
├── app/
│   ├── api/                      # API/Presentation Layer
│   │   ├── routes.py             # HTTP route handlers
│   │   └── schemas.py            # Pydantic request/response models
│   ├── services/                 # Business Logic Layer
│   │   └── todo_service.py       # Todo business logic
│   ├── repositories/             # Data Access Layer
│   │   └── todo_repository.py    # Todo data access operations
│   ├── models/                   # Data Model Layer
│   │   └── todo.py               # SQLAlchemy ORM models
│   └── database.py               # Database configuration & session
├── main.py                       # Application entry point
├── alembic.ini                   # Alembic configuration
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## 🎯 Design Patterns Used

### 1. **Layered Architecture (N-Tier)**
- Clear separation of concerns across horizontal layers
- Each layer has a specific responsibility and depends only on layers below it
- Changes in one layer have minimal impact on others

### 2. **Repository Pattern**
- Abstracts data access logic from business logic
- Provides a collection-like interface for accessing domain objects
- Makes the codebase more testable (can mock repositories)

### 3. **Dependency Injection**
- FastAPI's `Depends()` system injects dependencies automatically
- Promotes loose coupling and testability
- Dependencies flow from outer layers to inner layers

### 4. **Data Transfer Objects (DTO)**
- Pydantic schemas (`TodoCreate`, `TodoUpdate`, `TodoResponse`) act as DTOs
- Separate internal models from external API contracts
- Automatic validation and serialization

## 🔄 Request Flow Example

Here's what happens when you create a todo:

```
1. Client sends POST /todos/ with JSON body
   ↓
2. FastAPI validates request against TodoCreate schema
   ↓
3. routes.py → create_todo() receives validated data
   ↓
4. FastAPI injects TodoService (with TodoRepository and DB session)
   ↓
5. TodoService.create_todo() processes business logic
   ↓
6. TodoRepository.createOne() performs database INSERT
   ↓
7. SQLAlchemy commits transaction and returns TodoModel
   ↓
8. TodoModel is converted to TodoResponse (Pydantic)
   ↓
9. FastAPI serializes TodoResponse to JSON
   ↓
10. Client receives 201 Created with todo data
```

## 🧪 Testing the API

You can test the API using the interactive documentation at `http://localhost:8000/docs` or use tools like:

- **curl** (command line)
- **Postman** (GUI)
- **HTTPie** (command line)
- **Thunder Client** (VS Code extension)

### Example with HTTPie:
```bash
# Install httpie
pip install httpie

# Create a todo
http POST localhost:8000/todos/ title="Learn FastAPI" description="Study layered architecture"

# Get all todos
http GET localhost:8000/todos/

# Update a todo
http PATCH localhost:8000/todos/{id} completed:=true

# Delete a todo
http DELETE localhost:8000/todos/{id}
```

## 📚 Database Migrations

### Create a New Migration
```bash
# Auto-generate migration from model changes
alembic revision --autogenerate -m "description of changes"
```

### Apply Migrations
```bash
# Upgrade to latest version
alembic upgrade head

# Upgrade one version
alembic upgrade +1

# Upgrade to specific version
alembic upgrade <revision_id>
```

### Rollback Migrations
```bash
# Downgrade one version
alembic downgrade -1

# Downgrade to specific version
alembic downgrade <revision_id>

# Downgrade to base (empty database)
alembic downgrade base
```

### View Migration History
```bash
# Show current version
alembic current

# Show migration history
alembic history
```

## 🔧 Configuration

### Database Configuration
The database URL is configured in `app/database.py`:
```python
SQLALCHEMY_DATABASE_URL = "sqlite:///./todos.db"
```

To use PostgreSQL instead:
```python
SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost/dbname"
```

Don't forget to update `alembic.ini` as well and install the appropriate database driver (`psycopg2` for PostgreSQL).

## 🎓 Learning Resources

### Understanding Layered Architecture
- Each layer has a single responsibility
- Dependencies flow downward (upper layers depend on lower layers)
- Lower layers should not depend on upper layers
- Enables easier testing, maintenance, and scalability

### Benefits of This Architecture
✅ **Maintainability**: Changes are localized to specific layers  
✅ **Testability**: Each layer can be tested independently  
✅ **Scalability**: Layers can be scaled independently  
✅ **Flexibility**: Easy to swap implementations (e.g., change database)  
✅ **Team Collaboration**: Teams can work on different layers simultaneously  

### When to Use Layered Architecture
- Medium to large applications
- Applications with complex business logic
- Projects requiring high maintainability
- Systems that need to support multiple clients (web, mobile, etc.)

### Trade-offs
- **Overhead**: More files and abstractions than a simple flat structure
- **Learning Curve**: Requires understanding of architectural patterns
- **Boilerplate**: More code compared to monolithic approaches

For simple CRUD applications with minimal business logic, a simpler architecture might be more appropriate.

## 🤝 Contributing

Feel free to explore, modify, and experiment with this codebase to better understand layered architecture patterns!

## 📝 License

This is a sample educational project for learning software architecture patterns.

---

**Happy Coding!** 🚀
