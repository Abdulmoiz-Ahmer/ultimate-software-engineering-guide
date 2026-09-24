# Todo API - Unidirectional Component Architecture

A RESTful Todo API built with FastAPI demonstrating the **Unidirectional Component Architecture** pattern with **CQRS (Command Query Responsibility Segregation)**. This project showcases vertical feature slicing, component isolation, and unidirectional data flow.

## 📋 Table of Contents

- [What is Unidirectional Component Architecture?](#-what-is-unidirectional-component-architecture)
- [Pros and Cons](#-pros-and-cons)
- [When to Use This Architecture](#-when-to-use-this-architecture)
- [Technology Stack](#-technology-stack)
- [Getting Started](#-getting-started)
- [Project Structure](#-project-structure)
- [How It Works](#-how-it-works)
- [API Endpoints](#-api-endpoints)
- [Design Patterns](#-design-patterns)
- [Best Practices](#-best-practices)
- [Database Migrations](#-database-migrations)
- [Contributing](#-contributing)

---

## 🏛️ What is Unidirectional Component Architecture?

**Unidirectional Component Architecture** (also known as **Vertical Slice Architecture** or **Feature-Based Architecture**) is an alternative to traditional layered architecture that organizes code by business features rather than technical layers.

### Core Principle

Instead of spreading a single feature across multiple technical layers (controllers, services, repositories), **all code related to a feature lives together** in a self-contained component with **unidirectional data flow**.

### Visual Comparison

```
Traditional Layered:              Unidirectional Component:
├── controllers/                  ├── components/
│   ├── todo_controller.py        │   ├── todos/              ← Feature 1
│   └── user_controller.py        │   │   ├── router.py       │  (Everything
├── services/                     │   │   ├── handlers.py     │   for todos
│   ├── todo_service.py           │   │   ├── schemas.py      │   in one
│   └── user_service.py           │   │   └── models.py       │   place)
├── repositories/                 │   │
│   ├── todo_repository.py        │   └── users/              ← Feature 2
│   └── user_repository.py        │       ├── router.py       │  (Everything
└── models/                       │       ├── handlers.py     │   for users
    ├── todo.py                   │       ├── schemas.py      │   in one
    └── user.py                   │       └── models.py       │   place)
                                  │
(Feature scattered               └── core/                   ← Shared only
 across 4+ directories)              └── database.py         │  (Infrastructure)
```

### Architecture Diagram

```
┌──────────────────────────────────────────────────────────────┐
│                     Application Core                          │
│           (Shared Infrastructure & Utilities)                 │
│   - Database configuration                                    │
│   - Common middleware                                         │
│   - Cross-cutting concerns (logging, auth, etc.)             │
└──────────────────────────────────────────────────────────────┘
                    ↓                    ↓
┌─────────────────────────┐    ┌─────────────────────────┐
│  Todo Component         │    │  User Component         │
│  (Vertical Slice)       │    │  (Vertical Slice)       │
├─────────────────────────┤    ├─────────────────────────┤
│  ├── router.py          │    │  ├── router.py          │
│  ├── handlers.py        │    │  ├── handlers.py        │
│  ├── schemas.py         │    │  ├── schemas.py         │
│  └── models.py          │    │  └── models.py          │
│                         │    │                         │
│  Self-contained         │    │  Self-contained         │
│  No cross-dependencies  │    │  No cross-dependencies  │
└─────────────────────────┘    └─────────────────────────┘
```

### Unidirectional Data Flow

Data flows in **one direction** through each component:

```
┌─────────────────────────────────────────────────────────────┐
│                    WRITE FLOW (Command)                      │
└─────────────────────────────────────────────────────────────┘

HTTP POST Request
    ↓
Router (validates input → CreateTodoCommand)
    ↓
Handler (business logic → creates TodoModel)
    ↓
Model (ORM saves to database)
    ↓
Database (persists data)
    ↓
Model (returns saved TodoModel)
    ↓
Handler (converts to TodoDTO)
    ↓
Router (returns HTTP response)
    ↓
HTTP Response with TodoDTO


┌─────────────────────────────────────────────────────────────┐
│                     READ FLOW (Query)                        │
└─────────────────────────────────────────────────────────────┘

HTTP GET Request
    ↓
Router (validates query params)
    ↓
Query Handler (fetches data)
    ↓
Model (reads from database)
    ↓
Database (returns data)
    ↓
Query Handler (converts to TodoDTO)
    ↓
Router (returns HTTP response)
    ↓
HTTP Response with TodoDTO
```

**Key Principle**: Each layer only depends on the layer directly below it. No backwards dependencies, no circular references.

---

## ⚖️ Pros and Cons

### ✅ Advantages

#### 1. High Feature Cohesion

- All code for a feature lives in one folder
- Easy to find everything related to a specific feature
- Complete understanding by looking at one component
- No need to jump between 3+ directories

#### 2. Loose Coupling Between Features

- Components don't depend on each other
- Changes to one component don't affect others
- Can add/remove features without side effects
- Easy to refactor individual components

#### 3. Team Scalability

- Teams can own entire features/components
- Parallel development without conflicts
- Less coordination overhead between teams
- Clear boundaries and ownership

#### 4. Microservices-Ready

- Each component is already isolated
- Clear boundaries make extraction straightforward
- Can move components to separate services independently
- Perfect for gradual microservices migration

#### 5. Better for Domain-Driven Design

- Aligns with bounded contexts
- Rich domain models with behavior
- Business logic stays with the domain
- Natural fit for aggregate roots

#### 6. Reduced Merge Conflicts

- Teams work in separate component folders
- No shared service layer to conflict over
- Cleaner Git history per feature
- Faster code reviews

#### 7. Faster Feature Development

- Add new features by creating new components
- No need to modify existing layers
- Clear template to follow
- Reduced cognitive load

#### 8. Independent Evolution

- Features can evolve at their own pace
- Different patterns per component if needed
- Easy to experiment with one feature
- No forced consistency across all features

### ❌ Disadvantages

#### 1. Code Duplication

- Similar logic may exist in multiple components
- No shared service layer to reuse code
- Need to extract common code to core carefully
- Can lead to inconsistencies if not managed

#### 2. More Boilerplate

- Each component needs router, handler, schema, model
- More files to create for simple features
- Can feel like over-engineering for CRUD operations
- Initial setup is heavier

#### 3. Shared Business Logic Challenges

- Hard to implement cross-feature business rules
- No natural place for shared domain logic
- May need to introduce events or domain services
- Can lead to duplicated validation

#### 4. Learning Curve

- Less familiar than traditional layered architecture
- Team needs to understand vertical slicing
- Requires discipline to maintain boundaries
- Harder for junior developers initially

#### 5. Potential for Inconsistency

- Different components may use different patterns
- Without guidelines, each team may do things differently
- Code reviews need to catch architectural drift
- Requires strong architectural governance

#### 6. Overkill for Small Applications

- Too much structure for simple CRUD apps
- More folders and files to navigate
- Added complexity without benefits
- Traditional layering is simpler for small projects

#### 7. Cross-Component Queries

- Harder to implement features spanning multiple components
- May need to call multiple handlers
- Can lead to N+1 query problems
- Need event-driven patterns for complex workflows

#### 8. Testing Challenges

- Integration tests may need to touch multiple components
- Shared test fixtures are harder to manage
- May need to duplicate test utilities
- Database state management across components

---

## 🎯 When to Use This Architecture

### ✅ Use When

#### Large, Feature-Rich Applications

- Application has many independent features (10+ major features)
- Features don't share much business logic
- Each feature is substantial enough to warrant isolation
- Long-term project with ongoing feature development

#### Multiple Teams or Large Teams

- Multiple teams working on the same codebase
- Need clear ownership boundaries
- Want to minimize merge conflicts
- Teams work on different features simultaneously

#### Microservices Migration Path

- Planning to eventually split into microservices
- Want to identify service boundaries early
- Need ability to extract features independently
- Testing service separation without distributed systems complexity

#### Domain-Driven Design (DDD)

- Complex business domain with clear bounded contexts
- Rich domain models with behavior
- Need to model aggregates and entities
- Business logic is feature-specific

#### Features Evolve Independently

- Different features change at different rates
- Need to experiment with new patterns
- Want to refactor one feature without affecting others
- A/B testing or feature flags per component

#### Clear Feature Boundaries

- Business features are well-defined and independent
- Minimal cross-feature business logic
- Each feature has its own data model
- Features can be developed in parallel

#### Long-Term Maintainability Priority

- Code needs to be maintainable for years
- Many developers will work on the project over time
- Need clear navigation and understanding
- Onboarding new developers should be fast

#### Modular Monolith Approach

- Want microservices benefits without distribution
- Need strong boundaries in a monolith
- Plan to keep as monolith but modular
- Want option to split later without rewrite

### ❌ Avoid When

#### Small CRUD Applications

- Simple create, read, update, delete operations
- Less than 5 major features
- Straightforward business logic
- Traditional layered is simpler and faster

#### Heavy Shared Business Logic

- Multiple features share complex business rules
- Central validation logic across all features
- Shared workflows that span features
- Reusable service layer is essential

#### Small Team or Solo Developer

- Single developer or team of 2-3
- No merge conflicts to worry about
- Additional structure provides no benefit
- Overhead outweighs advantages

#### Rapid Prototyping / MVP

- Need to build quickly and iterate fast
- Requirements are unclear
- May throw away and rewrite
- Time to market is critical

#### Tight Cross-Feature Coupling Required

- Features are highly interdependent
- Complex transactions across multiple features
- Shared state management is critical
- Features can't function independently

#### Team Lacks Experience

- Team is unfamiliar with vertical slice architecture
- No time for learning and training
- Existing expertise in layered architecture
- Risk of improper implementation

#### Consistency is Critical

- All features must work exactly the same way
- Standardized patterns across entire application
- Centralized control over all operations
- No deviation allowed between features

#### Simple Data-Centric Applications

- Focus is on data storage and retrieval
- Minimal business logic
- Reports and data views
- Database is the primary concern

### 🆚 Quick Decision Guide

| Factor                | Layered          | Unidirectional Component        |
| --------------------- | ---------------- | ------------------------------- |
| **Team Size**         | 1-5 developers   | 6+ developers or multiple teams |
| **App Size**          | Small to medium  | Large, many features            |
| **Features**          | 3-8 features     | 10+ features                    |
| **Shared Logic**      | Heavy            | Minimal                         |
| **Feature Coupling**  | High             | Low                             |
| **Future Plan**       | Stay monolithic  | May split to microservices      |
| **Development Speed** | Faster initially | Faster long-term                |
| **Complexity**        | Lower            | Higher                          |
| **Maintainability**   | Good for small   | Better for large                |

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

### Installation

```bash
# 1. Navigate to the project directory
cd architectural-patterns/rest/02-vertical-slice-command-handlers/todo-app/python

# 2. Create a virtual environment
python -m venv venv

# 3. Activate the virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt
```

### Database Setup

```bash
# Run database migrations to create tables
alembic upgrade head
```

This creates a `todos.db` SQLite database file with the required schema.

### Run the Application

```bash
# Start the development server
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### Access API Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 📁 Project Structure

```
python/
├── alembic/                          # Database migration files
│   ├── versions/                     # Migration version files
│   │   └── aa099c01e412_initial...   # Initial migration
│   └── env.py                        # Alembic environment config
│
├── app/
│   ├── main.py                       # Application entry point
│   │
│   ├── core/                         # Shared infrastructure
│   │   └── database.py               # Database config & session
│   │
│   └── components/                   # Feature components (vertical slices)
│       └── todos/                    # Todo component (self-contained)
│           ├── router.py             # HTTP routes/endpoints
│           ├── handlers.py           # CQRS handlers (Commands & Queries)
│           ├── schemas.py            # DTOs and Commands (Pydantic)
│           └── models.py             # Database model (SQLAlchemy ORM)
│
├── alembic.ini                       # Alembic configuration
├── requirements.txt                  # Python dependencies
├── todos.db                          # SQLite database (created after migration)
└── README.md                         # This file
```

### Component Anatomy

Each component is organized as a **vertical slice** with all its concerns:

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

---

## ⚙️ How It Works

### Request Flow Example

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

### Key Principles

- **Router knows about HTTP, not business logic**
- **Handler knows about business logic, not HTTP**
- **Data flows in one direction** (no circular dependencies)
- **Each layer has a single, clear responsibility**

---

## 📡 API Endpoints

| Method   | Endpoint      | Description               | Handler/Query       | Response              |
| -------- | ------------- | ------------------------- | ------------------- | --------------------- |
| `POST`   | `/todos/`     | Create a new todo         | `CreateTodoHandler` | `TodoDTO` (201)       |
| `GET`    | `/todos/`     | Get all todos (paginated) | `ListTodosQuery`    | `List[TodoDTO]` (200) |
| `GET`    | `/todos/{id}` | Get a specific todo       | `GetTodoQuery`      | `TodoDTO` (200)       |
| `PATCH`  | `/todos/{id}` | Update a todo (partial)   | `UpdateTodoHandler` | `TodoDTO` (200)       |
| `DELETE` | `/todos/{id}` | Delete a todo             | `DeleteTodoHandler` | No content (204)      |

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

### Testing with HTTPie

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

---

## 🎓 Design Patterns

This application uses several complementary design patterns:

### 1. Unidirectional Component Architecture (Vertical Slices)

**What**: Organize code by business features instead of technical layers

**Benefits**:

- All related code lives together
- Easy to understand a feature by looking at one folder
- Components can be added/removed independently
- Reduces coupling between features
- Teams can own specific components

**Example**:

```
components/todos/          # Everything for todos in one place
  ├── router.py
  ├── handlers.py
  ├── schemas.py
  └── models.py
```

### 2. CQRS (Command Query Responsibility Segregation)

**What**: Separate read operations (Queries) from write operations (Commands)

**Commands** (Write Operations):

- `CreateTodoHandler` - Creates new todos
- `UpdateTodoHandler` - Updates existing todos
- `DeleteTodoHandler` - Deletes todos
- Modify state
- Can be async/queued
- Validation heavy

**Queries** (Read Operations):

- `GetTodoQuery` - Fetches a single todo
- `ListTodosQuery` - Lists todos with pagination
- Read state only
- Never modify data
- Can be cached
- Optimized for speed

**Benefits**:

- Clear separation of reads and writes
- Optimize queries and commands independently
- Different validation rules for each
- Easier to scale (separate read/write databases if needed)

### 3. Handler Pattern (Single Responsibility)

**What**: Each operation has its own handler class with a single `execute()` method

**Benefits**:

- One class = one responsibility
- Easy to test in isolation
- Easy to understand and modify
- Reusable across different contexts

**Example**:

```python
class CreateTodoHandler:
    @staticmethod
    def execute(command: CreateTodoCommand, db: Session) -> TodoDTO:
        # Single responsibility: create a todo
        ...
```

### 4. Data Transfer Object (DTO) Pattern

**What**: Use dedicated objects for data transfer between layers

**Commands** (Input):

- `CreateTodoCommand` - Represents intent to create
- `UpdateTodoCommand` - Represents intent to update

**DTOs** (Output):

- `TodoDTO` - Immutable data for responses

**Benefits**:

- Clear API contracts
- Separate internal models from external API
- Type-safe validation via Pydantic
- Consistent response format

### 5. Dependency Injection

**What**: Inject dependencies (like database sessions) rather than creating them

**Example**:

```python
@router.post("/todos/", status_code=status.HTTP_201_CREATED)
def create_todo(
    command: CreateTodoCommand,
    db: Session = Depends(get_db)  # Injected
) -> TodoDTO:
    return CreateTodoHandler.execute(command, db)
```

**Benefits**:

- Loose coupling between components and infrastructure
- Easy to test with mock dependencies
- Centralized configuration

---

## 💡 Best Practices

### ✅ DO

- **Keep components independent and self-contained**
  - Each component should work on its own
  - Avoid direct dependencies between components

- **Use handlers for all business logic**
  - Keep routers thin (only HTTP concerns)
  - Put all domain logic in handlers

- **Follow CQRS: separate reads from writes**
  - Commands modify state
  - Queries only read state
  - Never mix the two

- **Use DTOs for all API responses**
  - Don't expose database models directly
  - Create explicit contracts with DTOs

- **Name by intent, not implementation**
  - Use `CreateTodoCommand` not `CreateTodoRequest`
  - Use `TodoDTO` not `TodoResponse`

- **Reuse queries in commands**
  - `UpdateTodoHandler` can use `GetTodoQuery`
  - Promotes consistency

### ❌ DON'T

- **Don't create dependencies between components**
  - Todo component shouldn't call User component directly
  - Use events or shared core for cross-component needs

- **Don't put business logic in routers**
  - Routers should only handle HTTP concerns
  - Move logic to handlers

- **Don't mix commands and queries**
  - Queries should never modify data
  - Commands should represent state changes

- **Don't expose database models directly**
  - Always use DTOs for API responses
  - Keeps internal structure flexible

- **Don't create shared service layers**
  - This defeats the purpose of vertical slices
  - Extract truly shared code to core instead

- **Don't use generic names**
  - `TodoDTO` is better than `TodoResponse`
  - `CreateTodoCommand` is better than `TodoInput`

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

## 🔧 Adding a New Component

To add a new component (e.g., "users"), follow these steps:

### 1. Create Component Structure

```bash
# Create component directory
mkdir -p app/components/users

# Create component files
touch app/components/users/__init__.py
touch app/components/users/router.py       # HTTP routes
touch app/components/users/handlers.py     # CQRS handlers
touch app/components/users/schemas.py      # DTOs and commands
touch app/components/users/models.py       # ORM models
```

### 2. Implement Component Files

Follow the same pattern as the `todos` component:

- Define models in `models.py`
- Create DTOs and commands in `schemas.py`
- Implement handlers in `handlers.py`
- Create routes in `router.py`

### 3. Register the Router

```python
# app/main.py
from app.components.todos.router import router as todo_router
from app.components.users.router import router as user_router  # New

app.include_router(todo_router, tags=["todos"])
app.include_router(user_router, tags=["users"])  # New
```

### 4. Create Database Migration

```bash
# Generate migration for new model
alembic revision --autogenerate -m "add users component"

# Apply migration
alembic upgrade head
```

---

## 🤝 Contributing

This is an educational project demonstrating architectural patterns. Feel free to:

- Explore the codebase
- Experiment with modifications
- Add new components following the established patterns
- Share feedback and improvements

### Learning Goals

After working with this project, you should understand:

- How to organize code by features (vertical slices)
- How to implement CQRS pattern
- How to maintain unidirectional data flow
- When to use this architecture vs traditional layered architecture
- How to add new features without affecting existing ones

---

## 📖 Additional Resources

### Architecture Patterns

- **Vertical Slice Architecture**: Features organized by domain, not technology
- **CQRS**: Commands change state, Queries read state
- **Handler Pattern**: Single-responsibility operation handlers
- **DTO Pattern**: Explicit data contracts

### When to Use Different Architectures

**Use Unidirectional Component Architecture for**:

- ✅ Large applications with many features
- ✅ Multiple teams working on the same codebase
- ✅ Features that evolve independently
- ✅ Microservices migration path
- ✅ Domain-Driven Design approach

**Use Traditional Layered Architecture for**:

- ✅ Small, simple CRUD applications
- ✅ Heavy cross-feature business logic
- ✅ Small teams (1-5 developers)
- ✅ Rapid prototyping
- ✅ Traditional enterprise applications

---

## 📝 License

This is a sample educational project for learning software architecture patterns.

---

**Happy Coding!** 🚀
