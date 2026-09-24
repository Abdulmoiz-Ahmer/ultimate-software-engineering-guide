# Todo API - Layered (N-Tier) Architecture

A RESTful Todo API built with FastAPI demonstrating the **Layered (N-Tier) Architecture** pattern. This project showcases clean separation of concerns across distinct layers, making the codebase maintainable, testable, and scalable.

---

## Table of Contents

- [Understanding Layered Architecture](#-understanding-layered-architecture)
- [This Project's Architecture](#-this-projects-architecture)
- [Technology Stack](#️-technology-stack)
- [Getting Started](#-getting-started)
- [API Reference](#-api-reference)
- [Project Structure](#-project-structure)
- [Design Patterns](#-design-patterns)
- [Database Migrations](#-database-migrations)
- [Configuration](#-configuration)
- [Additional Resources](#-additional-resources)

---

## 🎯 Understanding Layered Architecture

### What is Layered (N-Tier) Architecture?

**Layered Architecture**, also known as **N-Tier Architecture**, is one of the most common and fundamental architectural patterns in software engineering. It organizes code into horizontal layers, where each layer has a specific responsibility and communicates only with adjacent layers.

### Core Principles

1. **Separation of Concerns**: Each layer handles a distinct aspect of the application (presentation, business logic, data access, etc.)
2. **Unidirectional Dependencies**: Layers depend only on the layers directly below them, never above
3. **Abstraction**: Each layer hides implementation details from the layers above it
4. **Loose Coupling**: Layers interact through well-defined interfaces, making components interchangeable

### Common Layer Structure

Most layered architectures follow a 3-4 tier pattern:

- **Presentation/API Layer**: Handles user interface or API requests/responses
- **Business Logic/Service Layer**: Implements business rules and application workflows
- **Data Access/Repository Layer**: Manages data persistence and retrieval
- **Data/Model Layer**: Defines data structures and database schemas

### ✅ Advantages

| Advantage                  | Description                                                                                  |
| -------------------------- | -------------------------------------------------------------------------------------------- |
| **Easy to Understand**     | Intuitive structure that mirrors how teams naturally think about applications                |
| **Maintainability**        | Changes are isolated to specific layers, reducing ripple effects                             |
| **Testability**            | Each layer can be tested independently with mocked dependencies                              |
| **Team Collaboration**     | Multiple teams can work on different layers simultaneously                                   |
| **Reusability**            | Business logic can be reused across different presentation layers (web, mobile, API)         |
| **Technology Flexibility** | Layers can use different technologies (e.g., swap databases without touching business logic) |
| **Clear Responsibilities** | Well-defined boundaries make it clear where new code belongs                                 |
| **Gradual Learning Curve** | New developers can focus on one layer at a time                                              |

### ❌ Disadvantages

| Disadvantage                  | Description                                                                          |
| ----------------------------- | ------------------------------------------------------------------------------------ |
| **Boilerplate Code**          | Requires more files and abstractions than simpler architectures                      |
| **Performance Overhead**      | Data must pass through multiple layers, potentially impacting performance            |
| **Rigidity**                  | Strict layer separation can lead to unnecessary complexity for simple operations     |
| **Over-Engineering Risk**     | Easy to create too many layers or abstractions for small applications                |
| **Deployment Coupling**       | Typically deployed as a monolith, making independent scaling harder                  |
| **Cross-Cutting Concerns**    | Features like logging, authentication span multiple layers, causing duplication      |
| **False Sense of Modularity** | Layers are organizational, not true architectural boundaries                         |
| **Database-Centric**          | Often leads to designs that revolve around the database rather than business domains |

### When to Use This Pattern

#### ✅ Good Use Cases

- **Medium to Large Enterprise Applications** where maintainability and team collaboration are critical
- **Applications with Complex Business Logic** that needs to be tested and maintained independently
- **Projects with Long Lifecycles** that will be maintained and extended over many years
- **Multi-Client Applications** where business logic needs to serve web, mobile, and API clients
- **Team Structure Alignment** when you have specialized teams (frontend, backend, database)
- **Regulated Industries** where clear separation helps with compliance and auditing
- **Stable, Well-Understood Domains** where requirements are clear and change gradually
- **CRUD-Heavy Applications** with standard create, read, update, delete operations

#### ❌ When NOT to Use

- **Simple CRUD Applications** with minimal business logic (consider simpler frameworks or serverless)
- **Microservices** where domain-driven design or hexagonal architecture may be more appropriate
- **High-Performance Systems** where the overhead of passing through layers is prohibitive
- **Rapidly Changing Startups** where flexibility and speed matter more than structure
- **Prototypes and MVPs** where you need to validate ideas quickly without overhead
- **Event-Driven Systems** where events and messaging patterns are central (consider event-driven architecture)
- **Small Teams or Solo Projects** where the overhead outweighs the organizational benefits
- **Domain-Complex Applications** where business domains should be the primary organizational principle (consider DDD)

#### 💡 Consider These Alternatives

| Scenario                                  | Better Alternative                              |
| ----------------------------------------- | ----------------------------------------------- |
| Need independent deployment of features   | **Microservices Architecture**                  |
| Domain complexity > technical complexity  | **Domain-Driven Design (DDD)**                  |
| Need to isolate business logic completely | **Hexagonal/Ports & Adapters Architecture**     |
| Event-driven or async workflows           | **Event-Driven Architecture**                   |
| Simple data operations                    | **Transaction Script or Active Record Pattern** |
| Real-time collaboration or streaming      | **CQRS or Event Sourcing**                      |

---

## 🏗️ This Project's Architecture

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

| Layer                | Purpose                                                     | Key Files                                 |
| -------------------- | ----------------------------------------------------------- | ----------------------------------------- |
| **API Layer**        | Handles HTTP requests/responses, routing, and serialization | `app/api/routes.py`, `app/api/schemas.py` |
| **Service Layer**    | Implements business logic and orchestrates operations       | `app/services/todo_service.py`            |
| **Repository Layer** | Abstracts data access and database operations               | `app/repositories/todo_repository.py`     |
| **Model Layer**      | Defines data structures and database schema                 | `app/models/todo.py`                      |

### Request Flow Example

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

### Key Features

- ✅ **Clean Architecture**: Clear separation of concerns across layers
- ✅ **RESTful API**: Standard HTTP methods (GET, POST, PATCH, DELETE)
- ✅ **UUID Primary Keys**: Globally unique identifiers for security
- ✅ **Dependency Injection**: Loose coupling via FastAPI's DI system
- ✅ **Repository Pattern**: Abstracted data access layer
- ✅ **Type Safety**: Full type hints with Pydantic validation
- ✅ **Database Migrations**: Version-controlled schema with Alembic
- ✅ **Auto-generated Documentation**: Interactive API docs via OpenAPI/Swagger

---

## 🛠️ Technology Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) - Modern, high-performance web framework
- **ORM**: [SQLAlchemy](https://www.sqlalchemy.org/) - SQL toolkit and Object-Relational Mapping
- **Database**: SQLite (easily swappable to PostgreSQL, MySQL, etc.)
- **Migrations**: [Alembic](https://alembic.sqlalchemy.org/) - Database migration tool
- **Validation**: [Pydantic](https://docs.pydantic.dev/) - Data validation using Python type hints
- **Server**: [Uvicorn](https://www.uvicorn.org/) - ASGI server implementation

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)

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

---

## 📡 API Reference

### Endpoints

| Method   | Endpoint      | Description             | Request Body | Response                   |
| -------- | ------------- | ----------------------- | ------------ | -------------------------- |
| `POST`   | `/todos/`     | Create a new todo       | `TodoCreate` | `TodoResponse` (201)       |
| `GET`    | `/todos/`     | Get all todos           | -            | `List[TodoResponse]` (200) |
| `GET`    | `/todos/{id}` | Get a specific todo     | -            | `TodoResponse` (200)       |
| `PATCH`  | `/todos/{id}` | Update a todo (partial) | `TodoUpdate` | `TodoResponse` (200)       |
| `DELETE` | `/todos/{id}` | Delete a todo           | -            | No content (204)           |

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

### Testing the API

You can test the API using the interactive documentation at `http://localhost:8000/docs` or use tools like:

- **curl** (command line)
- **Postman** (GUI)
- **HTTPie** (command line)
- **Thunder Client** (VS Code extension)

#### Example with HTTPie:

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

---

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

---

## 🎯 Design Patterns

This project demonstrates several design patterns working together:

### 1. Layered Architecture (N-Tier)

- Clear separation of concerns across horizontal layers
- Each layer has a specific responsibility and depends only on layers below it
- Changes in one layer have minimal impact on others

### 2. Repository Pattern

- Abstracts data access logic from business logic
- Provides a collection-like interface for accessing domain objects
- Makes the codebase more testable (can mock repositories)

### 3. Dependency Injection

- FastAPI's `Depends()` system injects dependencies automatically
- Promotes loose coupling and testability
- Dependencies flow from outer layers to inner layers

### 4. Data Transfer Objects (DTO)

- Pydantic schemas (`TodoCreate`, `TodoUpdate`, `TodoResponse`) act as DTOs
- Separate internal models from external API contracts
- Automatic validation and serialization

---

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

---

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

---

## 📖 Additional Resources

### Key Takeaways

- Each layer has a single responsibility
- Dependencies flow downward (upper layers depend on lower layers)
- Lower layers should not depend on upper layers
- Enables easier testing, maintenance, and scalability

### When This Architecture Shines

✅ **Maintainability**: Changes are localized to specific layers  
✅ **Testability**: Each layer can be tested independently  
✅ **Team Collaboration**: Teams can work on different layers simultaneously  
✅ **Flexibility**: Easy to swap implementations (e.g., change database)

### Trade-offs to Consider

⚠️ **Overhead**: More files and abstractions than a simple flat structure  
⚠️ **Learning Curve**: Requires understanding of architectural patterns  
⚠️ **Boilerplate**: More code compared to simpler approaches

> **Note**: For simple CRUD applications with minimal business logic, a simpler architecture might be more appropriate. Choose the right tool for the job based on your project's needs.

---

## 🤝 Contributing

Feel free to explore, modify, and experiment with this codebase to better understand layered architecture patterns!

## 📝 License

This is a sample educational project for learning software architecture patterns.

---

**Happy Coding!** 🚀
