# Modular Monolith Todo API

A Python-based Todo application demonstrating the **Modular Monolith** architectural pattern using FastAPI, SQLAlchemy, and Alembic.

## 📋 Table of Contents

- [What is a Modular Monolith?](#what-is-a-modular-monolith)
  - [Core Characteristics](#core-characteristics)
  - [How It Works](#how-it-works)
  - [The Modular Monolith Philosophy](#the-modular-monolith-philosophy)
  - [Pros of Modular Monolith](#pros-of-modular-monolith)
  - [Cons of Modular Monolith](#cons-of-modular-monolith)
  - [When to Use Modular Monolith](#when-to-use-modular-monolith)
  - [When NOT to Use Modular Monolith](#when-not-to-use-modular-monolith)
  - [Practical Decision Framework](#practical-decision-framework)
  - [Migration Path](#migration-path)
- [Architecture Overview](#architecture-overview)
  - [Layer Responsibilities](#layer-responsibilities)
- [Project Structure](#project-structure)
  - [Module Organization](#module-organization)
- [Key Principles](#key-principles)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [API Endpoints](#api-endpoints)
  - [Todos Module](#todos-module)
  - [Example Requests](#example-requests)
- [Database Migrations](#database-migrations)
  - [Common Commands](#common-commands)
  - [Important Notes](#important-notes)
- [Adding New Modules](#adding-new-modules)
- [Technology Stack](#technology-stack)
- [Best Practices](#best-practices)
- [Further Reading](#further-reading)

## 🏗️ What is a Modular Monolith?

A **Modular Monolith** is an architectural pattern that structures an application as a collection of loosely-coupled, highly-cohesive modules within a single deployable unit. It combines the operational simplicity of monolithic architecture with the organizational and maintainability benefits of microservices.

### Core Characteristics

- **Single Deployment Unit**: The entire application is built and deployed as one artifact
- **Module Boundaries**: Logical separation between business domains/capabilities
- **Shared Process Space**: All modules run in the same process (no network calls between modules)
- **Enforced Encapsulation**: Modules communicate through well-defined public interfaces
- **Shared Infrastructure**: Common database, logging, configuration, and cross-cutting concerns

### How It Works

Each module represents a bounded context or business capability:

```
┌──────────────────────────────────────────┐
│         Modular Monolith                 │
│                                          │
│  ┌────────┐  ┌────────┐  ┌────────┐   │
│  │ User   │  │ Order  │  │Payment │   │
│  │Module  │  │ Module │  │ Module │   │
│  └───┬────┘  └───┬────┘  └───┬────┘   │
│      │           │            │         │
│      └───────────┴────────────┘         │
│              │                           │
│      ┌───────▼────────┐                │
│      │ Shared Database │                │
│      └─────────────────┘                │
└──────────────────────────────────────────┘
         Single Process
```

### The Modular Monolith Philosophy

**Key Idea**: "Start simple, organize well, split when necessary."

The Modular Monolith acknowledges that:

1. Most systems don't need the complexity of microservices initially
2. Clear module boundaries provide organizational benefits without operational overhead
3. Well-structured modules can be extracted to separate services if scaling demands it
4. Premature distribution is a costly mistake

### Pros of Modular Monolith

#### ✅ Advantages

1. **Operational Simplicity**
   - Single application to build, test, and deploy
   - One server/container to monitor and maintain
   - No complex orchestration (no Kubernetes required initially)
   - Simplified CI/CD pipeline with fewer moving parts

2. **Development Speed**
   - No network latency between modules (in-process calls)
   - Shared transactions across modules (ACID guarantees)
   - Easier to refactor across module boundaries
   - Faster iteration cycles without service coordination

3. **Debugging & Observability**
   - Single process to debug and profile
   - Stack traces span the entire request
   - Easier to reproduce issues locally
   - Simplified logging and tracing (no distributed tracing complexity)

4. **Consistent Data**
   - Shared database enables JOIN queries across modules
   - Referential integrity across boundaries
   - Single source of truth
   - No eventual consistency challenges

5. **Lower Infrastructure Costs**
   - Single deployment reduces server/container costs
   - No service mesh or API gateway required
   - Less complex networking and security setup
   - Reduced operational overhead

6. **Team Productivity**
   - Developers can work across modules easily
   - No service boundary friction for small teams
   - Shared code review and testing practices
   - Lower cognitive load than distributed systems

7. **Flexibility for Growth**
   - Module boundaries provide extraction points for microservices
   - Can gradually extract hot modules as needed
   - Proven module boundaries before distribution
   - Reversible architectural decisions

8. **Testability**
   - Integration tests run fast (no network I/O)
   - Easy to test interactions between modules
   - Single test database setup
   - Simplified test environment

### Cons of Modular Monolith

#### ❌ Disadvantages

1. **Scaling Limitations**
   - Cannot scale individual modules independently
   - Must scale the entire application vertically or horizontally
   - Resource-intensive modules affect the whole system
   - Limited granularity in resource allocation

2. **Technology Lock-In**
   - All modules must use the same programming language/runtime
   - Cannot mix technologies per module (Python + Go, etc.)
   - Framework choice affects entire system
   - Difficult to adopt new technology stacks incrementally

3. **Deployment Coupling**
   - One module's bug can bring down the entire application
   - Must redeploy everything for any change
   - Increased blast radius for deployments
   - Longer deployment times as system grows

4. **Build Time Overhead**
   - Entire application must be rebuilt for any change
   - CI/CD times grow with codebase size
   - No incremental builds across modules (typically)
   - Can slow down development as project grows

5. **Database Contention**
   - Shared database can become a bottleneck
   - Conflicting schema change requirements
   - Difficult to optimize for different access patterns
   - Lock contention in high-traffic scenarios

6. **Boundary Enforcement Challenges**
   - Requires discipline to maintain module boundaries
   - Easy to accidentally create tight coupling
   - No physical boundary preventing direct imports
   - Code reviews must enforce architectural rules

7. **Limited Team Autonomy**
   - Teams cannot deploy independently
   - Coordination required for releases
   - Shared codebase can lead to merge conflicts
   - Harder to establish ownership boundaries

8. **Testing Blast Radius**
   - Changes anywhere require testing the whole system
   - Integration test suites can become slow
   - No isolation of module test failures
   - Difficult to parallelize testing across modules

9. **Single Point of Failure**
   - Memory leak in one module affects all
   - CPU-intensive module impacts entire system
   - No fault isolation between modules
   - Difficult to implement module-specific resilience patterns

10. **Organizational Scaling**
    - Becomes challenging with >20 developers
    - Code ownership becomes unclear
    - Coordination overhead increases
    - Conway's Law eventually pushes toward microservices

### When to Use Modular Monolith

✅ **Use Modular Monolith when:**

1. **Starting a New Project**
   - Requirements are still evolving
   - Business domain is not fully understood
   - Need to validate product-market fit quickly
   - Want to defer architectural complexity

2. **Small to Medium Teams**
   - Team size is 2-20 developers
   - Single team can understand entire codebase
   - Coordination overhead is manageable
   - Team prefers collective code ownership

3. **Moderate Traffic Levels**
   - System handles <100 requests/second
   - Vertical scaling is sufficient
   - No extreme scaling requirements
   - Traffic patterns are relatively predictable

4. **Shared Business Logic**
   - Modules have significant overlapping concerns
   - Business rules span multiple domains
   - Transactions frequently cross boundaries
   - Strong consistency requirements

5. **Limited Operational Resources**
   - Small DevOps team or no dedicated SRE
   - Simple infrastructure is preferred
   - Cost optimization is important
   - Don't want to manage distributed systems complexity

6. **Uncertain Future Direction**
   - May need to extract microservices later
   - Want clear module boundaries for future flexibility
   - Need to learn domain boundaries first
   - Want to keep options open

7. **Development Speed Priority**
   - Time to market is critical
   - Need rapid iteration cycles
   - Feature velocity matters more than scale
   - Simplicity > premature optimization

8. **B2B Enterprise Applications**
   - Internal tools and admin systems
   - ERP, CRM, HR systems
   - Applications with moderate user bases
   - Systems where reliability > massive scale

9. **Educational or Portfolio Projects**
   - Learning production architecture
   - Demonstrating good design principles
   - Balancing simplicity and structure
   - Want to showcase modular thinking

### When NOT to Use Modular Monolith

❌ **Avoid Modular Monolith when:**

1. **Massive Scale Requirements**
   - Need to handle >10,000 requests/second
   - Individual components need independent scaling
   - Traffic patterns are highly variable across features
   - **Better Alternative**: Microservices with service mesh

2. **Large, Distributed Teams**
   - > 50 developers working simultaneously
   - Multiple teams in different time zones
   - Teams need full deployment autonomy
   - **Better Alternative**: Microservices with team ownership

3. **Multi-Technology Requirements**
   - Different modules need different languages (Python + Go + Java)
   - Need to leverage specialized technology per module
   - Want to use best tool for each job
   - **Better Alternative**: Polyglot microservices

4. **Extreme Fault Isolation Needed**
   - One module failure cannot affect others
   - Critical systems requiring 99.99% uptime per component
   - Regulatory requirements for isolation
   - **Better Alternative**: Microservices with circuit breakers

5. **Highly Independent Domains**
   - Modules have zero shared business logic
   - No transactions spanning modules
   - Completely different teams and release cycles
   - **Better Alternative**: Microservices or separate applications

6. **Regulatory/Compliance Boundaries**
   - Different security clearance levels per module
   - Data residency requirements differ by region
   - Audit trails need physical separation
   - **Better Alternative**: Separate services with compliance boundaries

7. **Very Simple Applications**
   - Basic CRUD with 2-3 database tables
   - No complex business logic
   - Single developer maintaining
   - **Better Alternative**: Simple layered monolith or MVC

8. **Performance-Critical Components**
   - Need to optimize different modules with different languages
   - CPU-intensive module affects user-facing features
   - Real-time processing mixed with standard web requests
   - **Better Alternative**: Extract performance-critical modules as services

9. **Already Facing Monolith Problems**
   - Existing monolith with severe coupling issues
   - Deployment frequency limited by conflicts
   - Teams blocked by code ownership conflicts
   - **Better Alternative**: Break into microservices (strangler pattern)

10. **Serverless/FaaS Architecture**
    - Event-driven, highly granular functions
    - Need automatic scaling to zero
    - Pay-per-invocation model preferred
    - **Better Alternative**: AWS Lambda, Azure Functions, etc.

### Practical Decision Framework

Use this decision tree to determine if Modular Monolith is right:

```
START
  ↓
Is this a greenfield project? ─NO→ Consider strangler pattern to microservices
  ↓ YES
  ↓
Is your team < 20 developers? ─NO→ Consider microservices
  ↓ YES
  ↓
Do you need independent module scaling? ─YES→ Consider microservices
  ↓ NO
  ↓
Is operational simplicity important? ─YES→ ✅ USE MODULAR MONOLITH
  ↓ NO
  ↓
Do you have strong DevOps/SRE capability? ─NO→ ✅ USE MODULAR MONOLITH
  ↓ YES
  ↓
Is development speed critical? ─YES→ ✅ USE MODULAR MONOLITH
  ↓ NO
  ↓
Consider microservices or hybrid approach
```

### Migration Path

**From Monolith → Modular Monolith → Microservices**

1. **Phase 1**: Organize existing code into logical modules
2. **Phase 2**: Enforce module boundaries via code review/linting
3. **Phase 3**: Introduce public interfaces between modules
4. **Phase 4**: Monitor module performance and coupling
5. **Phase 5**: Extract performance bottleneck modules to services
6. **Phase 6**: Gradually extract other modules as needed

**Key Principle**: Modular Monolith is not a permanent destination—it's a pragmatic starting point that preserves your options.

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

---

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

- **`models.py`** - Database models (internal to module)
- **`schemas.py`** - API request/response models
- **`service.py`** - Business logic layer
- **`router.py`** - HTTP endpoints
- **`public.py`** - Public interface for inter-module communication

---

## 🔑 Key Principles

This project follows these core principles for maintainable modular architecture:

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

---

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

---

## 📡 API Endpoints

### Todos Module

| Method | Endpoint      | Description                      |
| ------ | ------------- | -------------------------------- |
| POST   | `/todos/`     | Create a new todo                |
| GET    | `/todos/`     | List all todos (with pagination) |
| GET    | `/todos/{id}` | Get a specific todo              |
| PATCH  | `/todos/{id}` | Update a todo (partial)          |
| DELETE | `/todos/{id}` | Delete a todo                    |

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

---

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

---

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
