# Todo API - Unidirectional Component Architecture

A RESTful Todo API built with FastAPI demonstrating the **Unidirectional Component Architecture** pattern with **CQRS (Command Query Responsibility Segregation)**. This project showcases vertical feature slicing, component isolation, and unidirectional data flow.

## 🏗️ Architecture Overview

This application implements a **Unidirectional Component Architecture** where each component is a self-contained vertical slice of functionality:

```
┌─────────────────────────────────────────────────────────────┐
│                    Application Core                          │
│                   (app/core/)                                │
│          Shared Infrastructure & Configuration               │
│              - Database configuration                        │
│              - Shared utilities                              │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                 Todo Component (Vertical Slice)              │
│                   (app/components/todos/)                    │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Router (router.py)                                  │   │
│  │  - HTTP endpoints                                    │   │
│  │  - Request/response mapping                          │   │
│  └─────────────────────────────────────────────────────┘   │
│                          ↓                                   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Handlers (handlers.py) - CQRS Pattern              │   │
│  │  - Commands (CreateTodoHandler, UpdateTodoHandler)   │   │
│  │  - Queries (GetTodoQuery, ListTodosQuery)           │   │
│  └─────────────────────────────────────────────────────┘   │
│                          ↓                                   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Schemas (schemas.py)                                │   │
│  │  - Commands (CreateTodoCommand, UpdateTodoCommand)   │   │
│  │  - DTOs (TodoDTO)                                    │   │
│  └─────────────────────────────────────────────────────┘   │
│                          ↓                                   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Model (models.py)                                   │   │
│  │  - TodoModel (ORM)                                   │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### Unidirectional Data Flow

```
HTTP Request → Router → Handler/Query → Model → Database
                 ↓
HTTP Response ← DTO ← Handler/Query ← Model ← Database
```

## 🎯 Key Architectural Concepts

### 1. **Component-Based Organization (Vertical Slices)**

Instead of organizing code by technical layers (controllers, services, repositories), code is organized by **features/components**:

```
Traditional Layered:           Unidirectional Component:
├── controllers/               ├── components/
│   └── todo_controller.py     │   └── todos/              ← Self-contained
├── services/                  │       ├── router.py       ← Routes
│   └── todo_service.py        │       ├── handlers.py     ← Business logic
├── repositories/              │       ├── schemas.py      ← DTOs/Commands
│   └── todo_repository.py     │       └── models.py       ← ORM models
└── models/                    └── core/                   ← Shared
    └── todo.py                    └── database.py         ← Infrastructure
```

**Benefits:**
- ✅ All related code lives together
- ✅ Easy to understand a feature by looking at one folder
- ✅ Components can be added/removed independently
- ✅ Reduces coupling between features
- ✅ Teams can own specific components

### 2. **CQRS Pattern (Command Query Responsibility Segregation)**

Separates read operations (Queries) from write operations (Commands):

```
┌─────────────────────────────────────────────────────────────┐
│                       CQRS Pattern                           │
├─────────────────────────────────────────────────────────────┤
│  Commands (Writes)          |    Queries (Reads)            │
│  ─────────────────          |    ───────────────            │
│  • CreateTodoHandler        |    • GetTodoQuery             │
│  • UpdateTodoHandler        |    • ListTodosQuery           │
│  • DeleteTodoHandler        |                               │
│  ─────────────────          |    ───────────────            │
│  • Modify state             |    • Read state only          │
│  • Return updated data      |    • Never modify             │
│  • Validation heavy         |    • Optimized for speed      │
│  • Can be async/queued      |    • Can be cached            │
└─────────────────────────────────────────────────────────────┘
```

**Benefits:**
- ✅ Clear separation of reads and writes
- ✅ Optimize queries and commands independently
- ✅ Different validation rules for each
- ✅ Easier to scale (separate read/write databases if needed)

### 3. **Handler Pattern (Single Responsibility)**

Each operation has its own handler class with a single `execute()` method:

- **CreateTodoHandler** - Creates new todos
- **GetTodoQuery** - Fetches a single todo
- **ListTodosQuery** - Lists todos with pagination
- **UpdateTodoHandler** - Updates existing todos
- **DeleteTodoHandler** - Deletes todos

**Benefits:**
- ✅ One class = one responsibility
- ✅ Easy to test in isolation
- ✅ Easy to understand and modify
- ✅ Reusable across different contexts

### 4. **Data Transfer Objects (DTOs) and Commands**

- **Commands** (Input): `CreateTodoCommand`, `UpdateTodoCommand` - Represent user intent
- **DTOs** (Output): `TodoDTO` - Immutable data for responses

**Benefits:**
- ✅ Clear API contracts
- ✅ Separate internal models from external API
- ✅ Type-safe validation via Pydantic
- ✅ Consistent response format

## ✨ Key Features

- ✅ **Vertical Slice Architecture**: Features organized by domain, not technology
- ✅ **CQRS Pattern**: Separated read and write operations
- ✅ **Unidirectional Flow**: Predictable data flow from router to database
- ✅ **Component Isolation**: Each component is self-contained
- ✅ **Handler Pattern**: Single-responsibility command/query handlers
- ✅ **Type Safety**: Full type hints with Pydantic validation
- ✅ **UUID Primary Keys**: Globally unique identifiers
- ✅ **RESTful API**: Standard HTTP methods and status codes
- ✅ **Auto-generated Docs**: Interactive API documentation

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
cd architectural-patterns/rest/02-unidirectional-component/todo-app/python

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
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### 4. Access API Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📡 API Endpoints

| Method | Endpoint | Description | Handler/Query | Response |
|--------|----------|-------------|---------------|----------|
| `POST` | `/todos/` | Create a new todo | `CreateTodoHandler` | `TodoDTO` (201) |
| `GET` | `/todos/` | Get all todos (paginated) | `ListTodosQuery` | `List[TodoDTO]` (200) |
| `GET` | `/todos/{id}` | Get a specific todo | `GetTodoQuery` | `TodoDTO` (200) |
| `PATCH` | `/todos/{id}` | Update a todo (partial) | `UpdateTodoHandler` | `TodoDTO` (200) |
| `DELETE` | `/todos/{id}` | Delete a todo | `DeleteTodoHandler` | No content (204) |

### Request/Response Examples

#### Create a Todo (Command)
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

#### Get All Todos (Query)
```bash
curl -X GET "http://localhost:8000/todos/?skip=0&limit=10"
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

#### Update a Todo (Command)
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

#### Delete a Todo (Command)
```bash
curl -X DELETE "http://localhost:8000/todos/550e8400-e29b-41d4-a716-446655440000"
```

**Response:** `204 No Content`

## 📁 Project Structure

```
python/
├── alembic/                          # Database migration files
│   ├── versions/                     # Migration version files
│   └── env.py                        # Alembic environment config
├── app/
│   ├── main.py                       # Application entry point
│   ├── core/                         # Shared infrastructure
│   │   └── database.py               # Database config & session
│   └── components/                   # Feature components (vertical slices)
│       └── todos/                    # Todo component (self-contained)
│           ├── router.py             # HTTP routes/endpoints
│           ├── handlers.py           # CQRS handlers (Commands & Queries)
│           ├── schemas.py            # DTOs and Commands (Pydantic)
│           └── models.py             # Database model (SQLAlchemy ORM)
├── alembic.ini                       # Alembic configuration
├── requirements.txt                  # Python dependencies
└── README.md                         # This file
```

## 🎯 Component Anatomy

Each component is organized as a vertical slice with all its concerns:

```
components/todos/
├── router.py          → HTTP layer (thin adapter)
│   - Defines endpoints
│   - Maps HTTP requests to handlers
│   - Returns HTTP responses
│
├── handlers.py        → Business logic layer (CQRS)
│   - CreateTodoHandler (Command)
│   - UpdateTodoHandler (Command)
│   - DeleteTodoHandler (Command)
│   - GetTodoQuery (Query)
│   - ListTodosQuery (Query)
│
├── schemas.py         → Data contracts layer
│   - CreateTodoCommand (Input)
│   - UpdateTodoCommand (Input)
│   - TodoDTO (Output)
│
└── models.py          → Data persistence layer
    - TodoModel (SQLAlchemy ORM)
```

## 🔄 Request Flow Example

Here's what happens when you create a todo:

```
1. Client sends POST /todos/ with JSON body
   ↓
2. FastAPI validates request against CreateTodoCommand schema
   ↓
3. router.py → create_todo() receives validated command
   ↓
4. CreateTodoHandler.execute() is called
   ↓
5. Handler creates TodoModel and saves to database
   ↓
6. TodoModel is automatically converted to TodoDTO (Pydantic)
   ↓
7. FastAPI serializes TodoDTO to JSON
   ↓
8. Client receives 201 Created with todo data
```

**Key Points:**
- Router knows about HTTP, not business logic
- Handler knows about business logic, not HTTP
- Data flows in one direction (no circular dependencies)
- Each layer has a single, clear responsibility

## 🆚 Comparison with Layered Architecture

| Aspect | Layered (N-Tier) | Unidirectional Component |
|--------|------------------|--------------------------|
| **Organization** | Horizontal layers | Vertical slices |
| **Grouping** | By technical concern | By business feature |
| **Dependencies** | Layer → Layer below | Component → Core only |
| **Cohesion** | Low (spread across layers) | High (all in one folder) |
| **Team Structure** | Teams own layers | Teams own components |
| **Adding Features** | Touch multiple layers | Add one component |
| **Reusability** | Services reused | Components independent |
| **Best For** | Shared business logic | Independent features |

### When to Use Each:

**Layered Architecture:**
- Applications with heavy shared business logic
- Small to medium teams
- Consistent patterns across features
- Traditional enterprise applications

**Unidirectional Component:**
- Large applications with many features
- Microservices-style modularity in a monolith
- Large or distributed teams
- Features that evolve independently
- Domain-Driven Design (DDD) approach

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

# Create a todo (Command)
http POST localhost:8000/todos/ title="Learn CQRS" description="Study command/query separation"

# Get all todos (Query)
http GET localhost:8000/todos/

# Get one todo (Query)
http GET localhost:8000/todos/{id}

# Update a todo (Command)
http PATCH localhost:8000/todos/{id} completed:=true

# Delete a todo (Command)
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

## 🎓 Design Patterns Used

### 1. **Unidirectional Component Architecture**
- Components are vertical slices of functionality
- Each component is self-contained and independent
- Data flows in one direction through the component
- No circular dependencies between components

### 2. **CQRS (Command Query Responsibility Segregation)**
- Commands modify state (CreateTodo, UpdateTodo, DeleteTodo)
- Queries read state (GetTodo, ListTodos)
- Clear separation enables independent optimization
- Different models for reads and writes if needed

### 3. **Handler Pattern**
- Each operation has a dedicated handler class
- Handlers are stateless with static execute() methods
- Single Responsibility Principle (SRP)
- Easy to test and maintain

### 4. **Data Transfer Object (DTO) Pattern**
- Commands represent intent (CreateTodoCommand)
- DTOs represent data (TodoDTO)
- Separation of concerns between internal and external models
- Type-safe contracts via Pydantic

### 5. **Dependency Injection**
- Database sessions injected via FastAPI's Depends()
- Loose coupling between components and infrastructure
- Easy to test with mock dependencies

## 🔧 Adding a New Component

To add a new component (e.g., "users"), follow these steps:

```bash
# 1. Create component directory
mkdir -p app/components/users

# 2. Create component files
touch app/components/users/router.py       # HTTP routes
touch app/components/users/handlers.py     # CQRS handlers
touch app/components/users/schemas.py      # DTOs and commands
touch app/components/users/models.py       # ORM models

# 3. Register the router in app/main.py
```

**Example component registration:**
```python
# app/main.py
from app.components.todos.router import router as todo_router
from app.components.users.router import router as user_router  # New

app.include_router(todo_router)
app.include_router(user_router)  # New
```

## 💡 Best Practices

### ✅ DO:
- Keep components independent and self-contained
- Use handlers for all business logic
- Follow CQRS: separate reads from writes
- Use DTOs for all API responses
- Keep routers thin (only HTTP concerns)
- Name commands by intent (CreateTodoCommand, not CreateTodoRequest)
- Reuse queries in other handlers (e.g., GetTodoQuery in UpdateTodoHandler)

### ❌ DON'T:
- Don't create dependencies between components
- Don't put business logic in routers
- Don't mix commands and queries
- Don't expose database models directly via API
- Don't create shared service layers across components
- Don't use generic names (use TodoDTO, not TodoResponse)

## 🎯 Architecture Benefits

### For Developers:
✅ **Easy to Navigate**: All code for a feature is in one place  
✅ **Easy to Test**: Each handler can be tested independently  
✅ **Easy to Understand**: Clear, unidirectional data flow  
✅ **Easy to Modify**: Changes are localized to one component  

### For Teams:
✅ **Parallel Development**: Teams can work on different components  
✅ **Clear Ownership**: Each team owns specific components  
✅ **Reduced Conflicts**: No shared service layer to conflict over  
✅ **Flexible Scaling**: Can extract components into microservices  

### For Architecture:
✅ **Loose Coupling**: Components don't depend on each other  
✅ **High Cohesion**: Related code stays together  
✅ **Scalable**: Easy to add new features without affecting existing ones  
✅ **Maintainable**: Clear boundaries and responsibilities  

## 📖 Learning Resources

### Understanding the Architecture

**Unidirectional Component Architecture:**
- Organizes by feature, not by technical layer
- Each component is a vertical slice with all its concerns
- Components communicate through DTOs, not direct references
- Core provides shared infrastructure

**CQRS Pattern:**
- Commands change state, Queries read state
- Can have different models for reads and writes
- Enables independent scaling and optimization
- Clear separation of concerns

**When to Use This Architecture:**
- ✅ Large applications with many features
- ✅ Multiple teams working on the same codebase
- ✅ Features that evolve independently
- ✅ Need to extract features into microservices later
- ✅ Domain-Driven Design approach

**When NOT to Use:**
- ❌ Small, simple CRUD applications
- ❌ Heavy cross-feature business logic
- ❌ Single developer/small team
- ❌ Tight coupling required between features

## 🤝 Contributing

Feel free to explore, modify, and experiment with this codebase to better understand unidirectional component architecture and CQRS patterns!

## 📝 License

This is a sample educational project for learning software architecture patterns.

---

**Happy Coding!** 🚀
