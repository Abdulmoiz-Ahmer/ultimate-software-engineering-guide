# Todo API - Model-View-Controller (MVC) Architecture

A RESTful Todo API built with FastAPI demonstrating the classic **Model-View-Controller (MVC)** architectural pattern. This project showcases the separation of concerns between data (Model), presentation (View), and business logic (Controller).

---

## Table of Contents

1. [What is MVC?](#-what-is-mvc)
2. [Pros of MVC](#-pros-of-mvc)
3. [Cons of MVC](#-cons-of-mvc)
4. [When to Use MVC](#-when-to-use-mvc)
5. [When NOT to Use MVC](#-when-not-to-use-mvc)
6. [Getting Started](#-getting-started)
7. [Architecture Overview](#️-architecture-overview)
8. [API Documentation](#-api-endpoints)
9. [Project Structure](#-project-structure)
10. [Best Practices](#-best-practices)
11. [Evolution Path](#-evolution-path)

---

## 🎯 What is MVC?

**Model-View-Controller (MVC)** is a software architectural pattern that separates an application into three interconnected components:

- **Model**: The data layer - manages the application's data, business rules, and logic for accessing data
- **View**: The presentation layer - handles the display and formatting of data for the user
- **Controller**: The orchestration layer - receives user input, processes it (often using the Model), and returns output via the View

**Core Philosophy**: Separate what you see (View) from what you store (Model), with business logic (Controller) acting as the coordinator between them.

### Key Characteristics

1. **Separation of Concerns**: Each component has a distinct responsibility
2. **Model Independence**: The Model layer doesn't know about Views or Controllers
3. **Controller as Orchestrator**: The Controller coordinates between Model and View
4. **View as Presentation**: Views only handle formatting and display logic
5. **Unidirectional Dependencies**: Model ← Controller → View (Controller knows both, but Model and View are isolated)

### Origins & Evolution

MVC was invented in 1979 by Trygve Reenskaug for Smalltalk at Xerox PARC. Originally designed for desktop GUI applications, it evolved to become one of the most popular patterns for web development:

- **1979**: Original MVC for desktop GUI applications
- **1996**: Adapted for web applications (server-side rendering)
- **2000s**: Ruby on Rails popularizes MVC for web
- **2010s**: REST APIs adapt MVC (Views become JSON schemas)
- **Today**: Still widely used, especially for CRUD applications

---

## ✅ Pros of MVC

### 1. **Clear Separation of Concerns**

Each component has a well-defined, singular responsibility, making code organization intuitive:

```
Model      → "What is the data?"
View       → "How should data be displayed?"
Controller → "What should happen with the data?"
```

### 2. **Parallel Development**

Teams can work simultaneously on different components:

- Frontend developers work on Views
- Backend developers work on Models
- Full-stack developers coordinate in Controllers

### 3. **Easy to Understand**

The pattern is:

- **Well-documented** with decades of literature
- **Widely adopted** across frameworks (Django, Rails, Laravel, Spring MVC)
- **Industry standard** that most developers recognize
- **Simple mental model** that maps to real-world organization

### 4. **Testability**

Each layer can be tested independently:

```python
# Test Model in isolation
def test_todo_model():
    todo = TodoModel(title="Test")
    assert todo.title == "Test"

# Test View validation
def test_view_validation():
    with pytest.raises(ValidationError):
        CreateTodoInputView(title="")

# Test Controller logic
def test_controller(mock_db):
    result = create_todo(payload, mock_db)
    assert result.id is not None
```

### 5. **Code Reusability**

- Models can be used by multiple Controllers
- Views can be shared across different endpoints
- Controllers can be split and reorganized without changing Models

### 6. **Maintainability**

Changes are localized:

- Database schema changes? → Update Model
- API response format changes? → Update View
- Business logic changes? → Update Controller

### 7. **Framework Support**

Most web frameworks provide MVC out of the box:

- Built-in routing, ORM, validation
- Convention over configuration
- Scaffolding tools for rapid development

---

## ❌ Cons of MVC

### 1. **Controller Bloat (Fat Controllers)**

As applications grow, Controllers tend to accumulate too much logic:

```python
# Controller becomes a "god object"
@router.post("/todos/")
def create_todo(payload, db):
    # Validation logic
    if not payload.title:
        raise HTTPException(400, "Title required")

    # Business logic
    if len(payload.title) > 100:
        raise HTTPException(400, "Title too long")

    # Authorization logic
    if not user.can_create_todos():
        raise HTTPException(403, "Forbidden")

    # Email logic
    send_notification_email(user.email)

    # Logging logic
    log_todo_creation(user.id, payload)

    # Database logic
    todo = TodoModel(**payload.dict())
    db.add(todo)
    db.commit()
    # ... 100 more lines
```

### 2. **Anemic Domain Model**

MVC often leads to Models that are just data containers with no behavior:

```python
# Anemic Model - just a data structure
class TodoModel(Base):
    id = Column(UUID)
    title = Column(String)
    completed = Column(Boolean)
    # No methods, no behavior, no business logic
```

**Problem**: Business logic ends up scattered across Controllers instead of being encapsulated in the domain.

### 3. **Limited Scalability for Complex Logic**

MVC doesn't provide guidance for:

- Complex business workflows
- Multi-step transactions
- Domain-driven design patterns
- Cross-cutting concerns (logging, caching, auth)

### 4. **View-Model Tight Coupling**

While Models don't "know" about Views, Views must match Model structure closely:

```python
# View must mirror Model fields
class TodoResponseView(BaseModel):
    id: UUID           # Must match TodoModel.id type
    title: str         # Must match TodoModel.title type
    completed: bool    # Must match TodoModel.completed type
```

**Problem**: Changing the Model often forces View changes.

### 5. **No Service Layer**

MVC doesn't define where to put:

- External API calls
- Complex calculations
- Business orchestration logic
- Reusable operations

This forces developers to either bloat Controllers or create ad-hoc solutions.

### 6. **Testing Dependencies**

Controllers often become tightly coupled to:

- Database sessions
- HTTP frameworks
- Multiple Models and Views

Making comprehensive testing complex:

```python
# Testing a Controller requires mocking many dependencies
def test_create_todo(mock_db, mock_email, mock_logger, mock_cache):
    result = create_todo(payload, mock_db)
    # Must verify interactions with all dependencies
```

### 7. **Not Suitable for Modern Frontend Patterns**

MVC was designed for server-side rendering. With modern SPAs:

- Frontend has its own MVC/MVVM
- Backend serves JSON APIs
- "View" becomes just a serialization schema
- The pattern feels awkward and outdated

---

## 🎯 When to Use MVC

### ✅ Perfect Use Cases

#### 1. **Simple CRUD Applications**

When your application primarily creates, reads, updates, and deletes data with minimal business logic:

```
Examples:
- Todo list APIs
- Contact management systems
- Blog platforms
- Content management systems (CMS)
- Admin panels
```

#### 2. **Rapid Prototyping**

When you need to build and iterate quickly:

- MVC frameworks provide scaffolding
- Clear structure accelerates development
- Easy to understand for stakeholders

#### 3. **Small to Medium Applications**

When your application has:

- Fewer than 20-30 entities
- Straightforward workflows
- Limited business complexity
- Small team (1-5 developers)

#### 4. **Database-Centric Applications**

When the database is the core of your application:

- Most operations are data persistence
- Business logic is mostly validation
- CRUD operations dominate

#### 5. **RESTful APIs Without Complex Business Logic**

When building REST APIs where:

- Endpoints map to database operations
- Limited inter-entity relationships
- Minimal state management
- Simple request/response flows

#### 6. **Educational Projects**

When learning web development:

- Well-documented pattern
- Lots of tutorials and resources
- Supported by major frameworks
- Good foundation for understanding architecture

#### 7. **Teams with MVC Experience**

When your team:

- Already knows MVC frameworks
- Has established MVC conventions
- Needs to onboard developers quickly

### ✅ Good Indicators for MVC

- Most features are "list, create, edit, delete" operations
- Business rules fit in simple validation checks
- User workflows are straightforward
- Data relationships are simple (few joins)
- You need to ship quickly with limited resources

---

## 🚫 When NOT to Use MVC

### ❌ Avoid MVC For:

#### 1. **Complex Business Logic**

When you have:

```
- Multi-step workflows (order processing, approval chains)
- Complex validation rules that span entities
- Domain-specific business rules
- Rich domain models with behavior
- Intricate state machines
```

**Use Instead**: Layered Architecture with Service layer, Domain-Driven Design

#### 2. **Microservices Architecture**

When building distributed systems:

```
- Services need clear boundaries
- Domain logic must be encapsulated
- Inter-service communication is complex
- Need independent scalability
```

**Use Instead**: Domain-Driven Design, Hexagonal Architecture, Clean Architecture

#### 3. **Event-Driven Systems**

When your application:

```
- Processes events asynchronously
- Uses message queues (RabbitMQ, Kafka)
- Needs eventual consistency
- Has decoupled components communicating via events
```

**Use Instead**: Event Sourcing, CQRS, Event-Driven Architecture

#### 4. **High-Performance Applications**

When you need:

```
- Optimized read/write patterns
- Command and Query separation
- Denormalized views
- Caching strategies
- Database-specific optimizations
```

**Use Instead**: CQRS (Command Query Responsibility Segregation)

#### 5. **Large Enterprise Applications**

When your application has:

```
- 50+ entities
- Multiple bounded contexts
- Complex domain logic
- Large development teams (10+ developers)
- Long-term evolution requirements
```

**Use Instead**: Domain-Driven Design, Hexagonal Architecture, Modular Monolith

#### 6. **Real-Time Collaborative Systems**

When building:

```
- Real-time chat applications
- Collaborative editing tools
- Live dashboards
- Multi-player games
- Streaming applications
```

**Use Instead**: Actor Model, Reactive Architecture, WebSocket-based patterns

#### 7. **Applications Requiring Complex Testing**

When you need:

```
- Comprehensive unit test coverage
- Easy mocking and stubbing
- Testable business logic in isolation
- Test-driven development (TDD)
```

**Use Instead**: Hexagonal Architecture, Clean Architecture (better dependency management)

#### 8. **API Gateway / Backend for Frontend (BFF)**

When building:

```
- API aggregation layers
- Multiple frontend-specific APIs
- Complex data transformation
- External API orchestration
```

**Use Instead**: API Gateway pattern, BFF pattern with Service layer

### ❌ Red Flags Against MVC

- Controllers exceed 200-300 lines
- Repeated logic across Controllers
- Difficulty writing unit tests without database
- Models have no methods (pure data bags)
- Need for transaction management across operations
- Complex authorization requirements
- Frequent need for rollbacks or sagas

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)

### 1. Installation

```bash
# Navigate to the project directory
cd architectural-patterns/rest/03-presentational-patterns/mvc/todo-app/python

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

## 🏗️ Architecture Overview

This application implements the **MVC (Model-View-Controller)** pattern:

```
┌─────────────────────────────────────────────────────────────┐
│                    MVC Architecture                          │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                    Controller                         │  │
│  │              (todo_controller.py)                     │  │
│  │  • Receives HTTP requests                            │  │
│  │  • Validates business rules                          │  │
│  │  • Orchestrates Model and View                       │  │
│  │  • Returns HTTP responses                            │  │
│  └────────┬──────────────────────────────┬──────────────┘  │
│           │                               │                  │
│           ▼                               ▼                  │
│  ┌────────────────┐            ┌─────────────────────────┐ │
│  │     Model      │            │         View            │ │
│  │   (todo.py)    │            │   (todo_view.py)        │ │
│  │ • Data schema  │            │ • Request schemas       │ │
│  │ • ORM mapping  │            │ • Response schemas      │ │
│  │ • Persistence  │            │ • Serialization         │ │
│  └────────────────┘            └─────────────────────────┘ │
│         ▲                                                    │
│         │                                                    │
│         ▼                                                    │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                    Database                           │  │
│  │                  (SQLite/SQLAlchemy)                  │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### MVC Components

#### Model (The "M") - `app/models/todo.py`

The Model represents **what the data is**:

```python
class TodoModel(Base):
    """The Model - represents data structure"""
    __tablename__ = "todos"
    id = Column(UUID, primary_key=True)
    title = Column(String(100))
    description = Column(String(255))
    completed = Column(Boolean, default=False)
```

**Responsibilities:**

- Defining data structure (database schema)
- Encapsulating data access (ORM)
- Representing domain entities
- Being independent of presentation and HTTP concerns

#### View (The "V") - `app/views/todo_view.py`

The View represents **how the data is presented**:

```python
class TodoResponseView(BaseModel):
    """The View - defines presentation format"""
    id: UUID
    title: str
    description: str | None
    completed: bool
```

**Responsibilities:**

- Defining presentation format (JSON schemas)
- Input validation (request schemas)
- Output serialization (response schemas)
- Being independent of data storage details

#### Controller (The "C") - `app/controllers/todo_controller.py`

The Controller represents **how the data is processed**:

```python
@router.post("/", response_model=TodoResponseView)
def create_todo(payload: CreateTodoInputView, db: Session):
    """The Controller - orchestrates Model and View"""
    # Business logic
    if "forbidden" in payload.title.lower():
        raise HTTPException(400, "Invalid title")

    # Manipulate Model
    todo = TodoModel(title=payload.title, ...)
    db.add(todo)
    db.commit()

    # Return View
    return todo  # Auto-converted to TodoResponseView
```

**Responsibilities:**

- Handling HTTP requests
- Implementing business logic
- Coordinating Model and View
- Error handling and workflow orchestration

### Request Lifecycle

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Client sends HTTP request                                 │
│    POST /todos/ {"title": "Task"}                           │
└────────────────────┬────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────────┐
│ 2. FastAPI routes request to Controller                      │
│    @router.post("/") → create_todo()                        │
└────────────────────┬────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────────┐
│ 3. Input View validates request data                         │
│    CreateTodoInputView checks constraints                    │
└────────────────────┬────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────────┐
│ 4. Controller applies business logic                         │
│    Validates title, checks business rules                    │
└────────────────────┬────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────────┐
│ 5. Controller creates and saves Model                        │
│    TodoModel instantiated, added to DB, committed            │
└────────────────────┬────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────────┐
│ 6. Output View formats Model data                            │
│    TodoResponseView converts Model to JSON                   │
└────────────────────┬────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────────┐
│ 7. Controller returns HTTP response                          │
│    201 Created with JSON body                                │
└─────────────────────────────────────────────────────────────┘
```

### Separation of Concerns

| Component      | Concern                        | Independence                       |
| -------------- | ------------------------------ | ---------------------------------- |
| **Model**      | Data structure & persistence   | Independent of View and Controller |
| **View**       | Presentation & formatting      | Independent of Model details       |
| **Controller** | Business logic & orchestration | Knows about both Model and View    |

### Responsibilities Matrix

| Task               | Model | View | Controller     |
| ------------------ | ----- | ---- | -------------- |
| Define data schema | ✅    | ❌   | ❌             |
| Database queries   | ✅    | ❌   | ✅ (initiates) |
| Validate input     | ❌    | ✅   | ✅ (checks)    |
| Business rules     | ❌    | ❌   | ✅             |
| Format responses   | ❌    | ✅   | ❌             |
| Handle HTTP        | ❌    | ❌   | ✅             |
| Error handling     | ❌    | ❌   | ✅             |

---

## 📡 API Endpoints

| Method   | Endpoint      | Description         | Controller Action | Response View                  |
| -------- | ------------- | ------------------- | ----------------- | ------------------------------ |
| `POST`   | `/todos/`     | Create a new todo   | `create_todo()`   | `TodoResponseView` (201)       |
| `GET`    | `/todos/`     | Get all todos       | `list_todos()`    | `List[TodoResponseView]` (200) |
| `GET`    | `/todos/{id}` | Get a specific todo | `get_todo()`      | `TodoResponseView` (200)       |
| `PATCH`  | `/todos/{id}` | Update a todo       | `update_todo()`   | `TodoResponseView` (200)       |
| `DELETE` | `/todos/{id}` | Delete a todo       | `delete_todo()`   | No content (204)               |

### Example Requests

#### Create a Todo

```bash
curl -X POST "http://localhost:8000/todos/" \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy groceries", "description": "Milk, eggs, bread"}'
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
curl -X GET "http://localhost:8000/todos/?skip=0&limit=10"
```

#### Update a Todo

```bash
curl -X PATCH "http://localhost:8000/todos/550e8400-e29b-41d4-a716-446655440000" \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'
```

#### Delete a Todo

```bash
curl -X DELETE "http://localhost:8000/todos/550e8400-e29b-41d4-a716-446655440000"
```

### Testing the API

You can test the API using:

- **Swagger UI**: http://localhost:8000/docs (recommended)
- **curl** (command line)
- **Postman** (GUI)
- **HTTPie** (command line)
- **Thunder Client** (VS Code extension)

---

## 📁 Project Structure

```
python/
├── alembic/                          # Database migrations
│   ├── versions/                     # Migration version files
│   └── env.py                        # Alembic configuration
├── app/
│   ├── controllers/                  # Controller Layer (The "C")
│   │   └── todo_controller.py        # HTTP request handlers, business logic
│   ├── models/                       # Model Layer (The "M")
│   │   └── todo.py                   # Database models (ORM entities)
│   ├── views/                        # View Layer (The "V")
│   │   └── todo_view.py              # Request/response schemas
│   └── database.py                   # Database configuration
├── main.py                           # Application entry point
├── alembic.ini                       # Alembic configuration
├── requirements.txt                  # Python dependencies
└── README.md                         # This file
```

### Technology Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) - Modern, high-performance web framework
- **ORM**: [SQLAlchemy](https://www.sqlalchemy.org/) - SQL toolkit and Object-Relational Mapping
- **Database**: SQLite (easily swappable to PostgreSQL, MySQL, etc.)
- **Migrations**: [Alembic](https://alembic.sqlalchemy.org/) - Database migration tool
- **Validation**: [Pydantic](https://docs.pydantic.dev/) - Data validation using Python type hints
- **Server**: [Uvicorn](https://www.uvicorn.org/) - ASGI server implementation

---

## 💡 Best Practices

### ✅ DO:

**Models:**

- Keep models focused on data structure
- Use ORM features (relationships, constraints)
- Make models independent of HTTP concerns
- Use meaningful field names and types

**Views:**

- Create separate input and output views
- Use Pydantic for automatic validation
- Keep views focused on presentation
- Use descriptive view names (TodoResponseView, not TodoDTO)

**Controllers:**

- Put business logic in controllers
- Keep controllers thin (delegate to services if needed)
- Handle all error cases
- Use dependency injection for database sessions
- Return appropriate HTTP status codes

### ❌ DON'T:

- Don't put business logic in Models
- Don't put HTTP concerns in Models
- Don't access Models directly from Views
- Don't skip input validation
- Don't mix concerns between M-V-C
- Don't expose internal Model structure in Views

### Design Principles

1. **Separation of Concerns**: Each component has a single, well-defined responsibility
2. **Loose Coupling**: Model doesn't know about View or Controller
3. **Single Responsibility Principle (SRP)**: Model = Data, View = Presentation, Controller = Logic
4. **Don't Repeat Yourself (DRY)**: Reuse Models and Views across Controllers

---

## 🔄 Evolution Path

### Signs You've Outgrown MVC

1. Controllers are becoming unmanageable (>500 lines)
2. Duplicated logic across Controllers
3. Complex business rules scattered everywhere
4. Difficulty testing without full database
5. Need for transaction scripts across entities
6. Models are anemic (no behavior)
7. Team struggles to locate business logic

### Migration Strategies

#### Phase 1: Introduce Service Layer

```python
# Extract logic from Controller to Service
class TodoService:
    def create_todo(self, payload: CreateTodoInputView) -> TodoModel:
        # Business logic here
        if "forbidden" in payload.title:
            raise BusinessRuleViolation()
        return TodoModel(**payload.dict())

# Controller becomes thin
@router.post("/")
def create_todo(payload: CreateTodoInputView, db: Session):
    service = TodoService()
    todo = service.create_todo(payload)
    db.add(todo)
    db.commit()
    return todo
```

#### Phase 2: Introduce Repository Pattern

```python
# Abstract data access
class TodoRepository:
    def add(self, todo: TodoModel):
        # Data access logic

    def find_by_id(self, id: UUID) -> TodoModel:
        # Query logic
```

#### Phase 3: Move to Layered Architecture

```
Controller → Service → Repository → Model
(API)      → (Business) → (Data)  → (Domain)
```

#### Phase 4: Consider Domain-Driven Design

For large, complex applications with rich domain logic.

---

## 🆚 MVC vs Other Patterns

### MVC vs Layered Architecture

| Aspect             | MVC                   | Layered (N-Tier)                  |
| ------------------ | --------------------- | --------------------------------- |
| **Organization**   | Model-View-Controller | Presentation-Business-Data        |
| **Focus**          | Presentation pattern  | Architectural pattern             |
| **Layers**         | 3 (M-V-C)             | 4+ (API-Service-Repository-Model) |
| **Business Logic** | In Controller         | In Service Layer                  |
| **Complexity**     | Simple, flat          | More abstraction layers           |
| **Best For**       | Simple CRUD apps      | Complex business logic            |

### MVC vs Component Architecture

| Aspect           | MVC                        | Unidirectional Component       |
| ---------------- | -------------------------- | ------------------------------ |
| **Organization** | By concern (M/V/C)         | By feature (components)        |
| **Files**        | Grouped by type            | Grouped by feature             |
| **Coupling**     | Controller couples M & V   | Components independent         |
| **Scalability**  | Horizontal (add more MVCs) | Vertical (add more components) |
| **Best For**     | Traditional apps           | Large feature sets             |

---

## 📚 Additional Resources

### Database Migrations

**Create a New Migration:**

```bash
alembic revision --autogenerate -m "description of changes"
```

**Apply Migrations:**

```bash
alembic upgrade head
```

**Rollback Migrations:**

```bash
alembic downgrade -1
```

### Extending the Application

To add a new entity (e.g., Users):

1. Create Model in `app/models/user.py`
2. Create Views in `app/views/user_view.py`
3. Create Controller in `app/controllers/user_controller.py`
4. Register Controller in `main.py`

---

## 🤝 Contributing

Feel free to explore, modify, and experiment with this codebase to better understand the MVC architectural pattern!

## 📝 License

This is a sample educational project for learning software architecture patterns.

---

**Happy Coding!** 🚀
