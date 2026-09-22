# Modular Monolith Todo API

A Python-based Todo application demonstrating the **Modular Monolith** architectural pattern using FastAPI, SQLAlchemy, and Alembic.

## 📋 Table of Contents

- [What is a Modular Monolith?](#what-is-a-modular-monolith)
- [Architecture Overview](#architecture-overview)
- [Project Structure](#project-structure)
- [Key Principles](#key-principles)
- [Getting Started](#getting-started)
- [API Endpoints](#api-endpoints)
- [Database Migrations](#database-migrations)
- [Adding New Modules](#adding-new-modules)
- [Technology Stack](#technology-stack)

## 🏗️ What is a Modular Monolith?

A **Modular Monolith** is an architectural pattern that combines the simplicity of a monolithic deployment with the organizational benefits of microservices. The application is structured as independent, loosely-coupled modules within a single deployable unit.

### Benefits

- ✅ **Simple Deployment**: Single application to deploy and manage
- ✅ **Module Isolation**: Clear boundaries between business domains
- ✅ **Easier Refactoring**: Modules can be extracted to microservices later if needed
- ✅ **Shared Infrastructure**: Database, logging, and configuration in one place
- ✅ **Better than a Big Ball of Mud**: Enforced module boundaries prevent coupling
- ✅ **Faster Development**: No network overhead between modules during development

### When to Use

- Starting a new project where requirements are still evolving
- Team size is small to medium (< 20 developers)
- Performance requirements don't justify distributed complexity
- You want the option to extract microservices later

## 🎯 Architecture Overview

This application follows a layered architecture within each module:

```
┌─────────────────────────────────────────────┐
│           FastAPI Application               │
│                 (main.py)                   │
└──────────────────┬──────────────────────────┘
                   │
        ┌──────────┴──────────┐
        │                     │
   ┌────▼─────┐        ┌─────▼────┐
   │  Todos   │        │  Future  │
   │  Module  │        │  Modules │
   └────┬─────┘        └──────────┘
        │
        │
   ┌────▼─────────────────────┐
   │  Module Layers:          │
   │                          │
   │  ┌──────────────────┐   │
   │  │   Router Layer   │   │  ← HTTP endpoints
   │  └────────┬─────────┘   │
   │           │              │
   │  ┌────────▼─────────┐   │
   │  │  Service Layer   │   │  ← Business logic
   │  └────────┬─────────┘   │
   │           │              │
   │  ┌────────▼─────────┐   │
   │  │   Data Layer     │   │  ← Database access
   │  │   (Models/ORM)   │   │
   │  └──────────────────┘   │
   └──────────────────────────┘
                   │
        ┌──────────▼──────────┐
        │  Shared Database    │
        │     (SQLite)        │
        └─────────────────────┘
```

### Layer Responsibilities

1. **Router Layer** (`router.py`)
   - HTTP request/response handling
   - Route definitions
   - Dependency injection
   - Input validation (via Pydantic schemas)

2. **Service Layer** (`service.py`)
   - Business logic and rules
   - Transaction management
   - Error handling
   - Coordination between repositories

3. **Data Layer** (`models.py`)
   - ORM models
   - Database schema definition
   - Data persistence

4. **Schemas** (`schemas.py`)
   - Request/response DTOs
   - Data validation
   - API contract definition

5. **Public Interface** (`public.py`)
   - Inter-module communication
   - Exposes module functionality to other modules
   - Maintains encapsulation

## 📁 Project Structure

```
.
├── alembic/                      # Database migrations
│   ├── versions/                 # Migration files
│   │   └── e893d74119ac_*.py    # Initial schema migration
│   ├── env.py                   # Alembic environment config
│   └── script.py.mako           # Migration template
├── app/                         # Application code
│   ├── core/                    # Shared core components
│   │   └── database.py          # Database configuration
│   └── modules/                 # Domain modules
│       └── todos/               # Todo module
│           ├── models.py        # ORM models (TodoORM)
│           ├── schemas.py       # Pydantic schemas
│           ├── service.py       # Business logic
│           ├── router.py        # API endpoints
│           └── public.py        # Public interface for other modules
├── alembic.ini                  # Alembic configuration
├── main.py                      # Application entry point
├── todos.db                     # SQLite database (generated)
├── .gitignore                   # Git ignore rules
└── README.md                    # This file
```

### Module Organization

Each module follows a consistent structure:

- `models.py` - Database models (internal to module)
- `schemas.py` - API request/response models
- `service.py` - Business logic layer
- `router.py` - HTTP endpoints
- `public.py` - Public interface for inter-module communication

## 🔑 Key Principles

### 1. Module Isolation

Each module is self-contained with clear boundaries:

```python
# ✅ GOOD: Using public interface
from app.modules.todos.public import get_todo_for_notification

# ❌ BAD: Direct access to internal components
from app.modules.todos.service import TodoService
from app.modules.todos.models import TodoORM
```

### 2. Table Name Prefixing

Prevent naming collisions by prefixing table names with module names:

```python
class TodoORM(Base):
    __tablename__ = "todos_todo"  # Prefixed with module name
```

### 3. Dependency Injection

Use FastAPI's dependency injection for clean, testable code:

```python
@router.get("/todos")
def list_todos(service: TodoService = Depends(get_service)):
    return service.list_todos()
```

### 4. Separation of Concerns

- **Routers** handle HTTP concerns
- **Services** contain business logic
- **Models** manage data persistence
- **Schemas** define data contracts

## 🚀 Getting Started

### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository** (or navigate to this directory)

2. **Create a virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install fastapi uvicorn sqlalchemy alembic pydantic
   ```

4. **Run database migrations**:
   ```bash
   alembic upgrade head
   ```

5. **Start the development server**:
   ```bash
   uvicorn main:app --reload
   ```

6. **Access the API**:
   - API: http://localhost:8000
   - Interactive docs (Swagger): http://localhost:8000/docs
   - Alternative docs (ReDoc): http://localhost:8000/redoc

## 📡 API Endpoints

### Todos Module

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/todos/` | Create a new todo |
| GET | `/todos/` | List all todos (with pagination) |
| GET | `/todos/{id}` | Get a specific todo |
| PATCH | `/todos/{id}` | Update a todo (partial) |
| DELETE | `/todos/{id}` | Delete a todo |

### Example Requests

**Create a Todo**:
```bash
curl -X POST "http://localhost:8000/todos/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Learn Modular Monolith",
    "description": "Study the architecture pattern"
  }'
```

**List Todos**:
```bash
curl "http://localhost:8000/todos/?skip=0&limit=10"
```

**Update a Todo**:
```bash
curl -X PATCH "http://localhost:8000/todos/{todo_id}" \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'
```

**Delete a Todo**:
```bash
curl -X DELETE "http://localhost:8000/todos/{todo_id}"
```

## 🗄️ Database Migrations

This project uses Alembic for database schema management.

### Common Commands

**Create a new migration**:
```bash
alembic revision --autogenerate -m "Description of changes"
```

**Apply migrations**:
```bash
alembic upgrade head
```

**Rollback one migration**:
```bash
alembic downgrade -1
```

**View migration history**:
```bash
alembic history
```

### Important Notes

- Always import new ORM models in `alembic/env.py` for autogenerate to work
- Review generated migrations before applying them
- Test migrations on a copy of production data before deploying

## ➕ Adding New Modules

To add a new module to the application:

1. **Create module directory structure**:
   ```bash
   mkdir -p app/modules/new_module
   touch app/modules/new_module/{models.py,schemas.py,service.py,router.py,public.py}
   ```

2. **Define ORM models** (`models.py`):
   ```python
   from app.core.database import Base
   from sqlalchemy import Column, String
   
   class NewModuleORM(Base):
       __tablename__ = "newmodule_entity"  # Use module prefix!
       # ... define columns
   ```

3. **Create Pydantic schemas** (`schemas.py`):
   ```python
   from pydantic import BaseModel
   
   class CreateRequest(BaseModel):
       # ... define fields
   
   class Response(BaseModel):
       # ... define fields
   ```

4. **Implement business logic** (`service.py`):
   ```python
   class NewModuleService:
       def __init__(self, db: Session):
           self.db = db
       # ... implement methods
   ```

5. **Create API router** (`router.py`):
   ```python
   from fastapi import APIRouter
   
   router = APIRouter(prefix="/new-module", tags=["New Module"])
   # ... define endpoints
   ```

6. **Register router in main.py**:
   ```python
   from app.modules.new_module.router import router as new_module_router
   app.include_router(new_module_router)
   ```

7. **Import models in Alembic** (`alembic/env.py`):
   ```python
   from app.modules.new_module.models import NewModuleORM
   ```

8. **Generate and apply migration**:
   ```bash
   alembic revision --autogenerate -m "Add new module"
   alembic upgrade head
   ```

## 🛠️ Technology Stack

- **FastAPI** - Modern, fast web framework for building APIs
- **SQLAlchemy** - SQL toolkit and ORM
- **Alembic** - Database migration tool
- **Pydantic** - Data validation using Python type annotations
- **SQLite** - Lightweight database (easily replaceable with PostgreSQL, MySQL, etc.)
- **Uvicorn** - ASGI server for running the application

## 🧪 Best Practices

1. **Keep modules independent** - Avoid direct dependencies between modules
2. **Use the public interface** - Expose only what's necessary through `public.py`
3. **Prefix table names** - Prevent naming collisions with `modulename_tablename`
4. **Write migrations** - Never modify the database schema manually
5. **Validate input** - Use Pydantic schemas for all API requests
6. **Handle errors gracefully** - Raise appropriate HTTP exceptions
7. **Test module boundaries** - Ensure modules can be tested in isolation

## 📚 Further Reading

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Alembic Tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html)
- [Modular Monolith Architecture](https://www.kamilgrzybek.com/design/modular-monolith-primer/)

## 📄 License

This is a sample project for educational purposes.

---

**Happy Coding!** 🚀
