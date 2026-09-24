# Clean Architecture Todo API

A RESTful Todo API implementation following **Uncle Bob's Clean Architecture** principles. This project demonstrates how to build a decoupled, testable, and maintainable application using **FastAPI**, **SQLAlchemy**, and **SQLite**.

## 📋 Table of Contents

- [What is Clean Architecture?](#what-is-clean-architecture)
- [When to Use Clean Architecture](#when-to-use-clean-architecture)
- [When NOT to Use Clean Architecture](#when-not-to-use-clean-architecture)
- [Pros and Cons](#pros-and-cons)
- [Project Overview](#project-overview)
- [Architecture Layers](#architecture-layers)
- [Project Structure](#project-structure)
- [Core Concepts](#core-concepts)
- [Getting Started](#getting-started)
- [API Endpoints](#api-endpoints)
- [Design Patterns](#design-patterns)
- [Testing Strategy](#testing-strategy)
- [Further Reading](#further-reading)

---

## 🎓 What is Clean Architecture?

**Clean Architecture** is a software design philosophy introduced by **Robert C. Martin (Uncle Bob)** in 2012. It's an approach to organizing code that emphasizes **separation of concerns** and **independence from frameworks, databases, and external systems**.

### Core Philosophy

The fundamental idea is to structure your application in **concentric layers**, where each layer has a specific responsibility and dependencies flow in one direction: **from the outside in**.

```
External World → Frameworks → Interface Adapters → Use Cases → Entities
```

### The Dependency Rule

> **"Source code dependencies must point only inward, toward higher-level policies."**

This means:

- Inner layers know **nothing** about outer layers
- Outer layers depend on inner layers, never the reverse
- Business logic is independent of UI, databases, and frameworks

### Key Principles

1. **Independent of Frameworks** - Your business logic doesn't depend on FastAPI, Django, or any framework
2. **Testable** - Business rules can be tested without UI, database, or external services
3. **Independent of UI** - The UI can change without affecting business logic
4. **Independent of Database** - Business rules don't know if you use PostgreSQL, MongoDB, or files
5. **Independent of External Systems** - Business logic doesn't know about APIs, message queues, or any external agency

### The Four Layers

**1. Entities (Enterprise Business Rules)**

- Pure business objects
- No framework dependencies
- Contains core business logic
- Most stable layer

**2. Use Cases (Application Business Rules)**

- Application-specific business rules
- Orchestrates data flow between entities and external systems
- Defines interfaces (ports) for external systems
- Independent of delivery mechanisms

**3. Interface Adapters**

- Converts data between use cases and external systems
- Controllers, Presenters, Gateways
- Implements the interfaces defined by use cases
- Adapts external formats to internal formats

**4. Frameworks & Drivers**

- Web frameworks (FastAPI, Flask, Django)
- Database ORMs (SQLAlchemy, Django ORM)
- External APIs, message queues
- Most volatile layer

---

## ✅ When to Use Clean Architecture

Clean Architecture is **ideal** for:

### 1. **Long-Lived Enterprise Applications**

- Applications expected to live for 5+ years
- Projects where business rules are complex and evolve over time
- Systems where maintainability is critical

### 2. **Complex Business Logic**

- Applications with intricate business rules
- Systems where business logic needs protection from external changes
- Projects where domain knowledge is the core value

### 3. **Large Teams**

- Multiple teams working on different parts of the application
- Need for clear boundaries and contracts between components
- Onboarding new developers who need clear structure

### 4. **Evolving Requirements**

- Uncertain about which frameworks or databases to use
- Expecting to migrate frameworks or databases in the future
- Need flexibility to add new delivery mechanisms (REST, GraphQL, gRPC)

### 5. **High Testability Requirements**

- Need to test business logic in isolation
- Strict testing and code coverage requirements
- Applications where bugs are costly (finance, healthcare, critical systems)

### 6. **Microservices Architecture**

- Each service needs clear boundaries
- Services may use different frameworks or databases
- Business logic needs to be portable across services

### 7. **Projects with Regulatory Requirements**

- Need clear audit trails
- Business rules must be easily verifiable
- Compliance-driven development

---

## ❌ When NOT to Use Clean Architecture

Clean Architecture may be **overkill** for:

### 1. **Simple CRUD Applications**

- Basic create-read-update-delete operations
- Minimal business logic
- Straightforward data persistence
- **Alternative:** Use a simpler layered architecture or MVC

### 2. **Prototypes and MVPs**

- Time-to-market is critical
- Validating ideas quickly
- Short-lived proof-of-concepts
- **Alternative:** Use framework defaults, monolithic structure

### 3. **Small Projects or Scripts**

- Single-file applications
- Internal tools with 1-2 developers
- Scripts or automation tasks
- **Alternative:** Simple procedural or basic OOP structure

### 4. **Projects with Stable, Simple Requirements**

- No expectation of framework changes
- No complex business rules
- UI-centric applications (admin panels, dashboards)
- **Alternative:** Framework-driven architecture (Rails, Django patterns)

### 5. **Very Small Teams (1-2 developers)**

- Overhead of maintaining layers may not be worth it
- Context switching cost is higher than benefits
- **Alternative:** Simplified layered architecture

### 6. **When You Lack Experience**

- Team unfamiliar with architectural patterns
- No senior developers to guide implementation
- Risk of over-engineering or incorrect implementation
- **Better:** Start with simpler patterns, evolve as needed

### 7. **Highly Framework-Specific Applications**

- Applications deeply integrated with framework features
- CMS systems, admin interfaces
- When the framework IS the product
- **Alternative:** Embrace the framework's conventions

---

## ⚖️ Pros and Cons

### Pros

#### ✅ **1. Testability**

- Business logic can be tested without frameworks, databases, or UI
- Easy to write unit tests with mocked dependencies
- High test coverage achievable

#### ✅ **2. Flexibility**

- Swap frameworks without changing business logic
- Change databases without affecting use cases
- Add new delivery mechanisms (REST, GraphQL, CLI) easily

#### ✅ **3. Maintainability**

- Clear separation of concerns
- Easy to locate and modify code
- Reduced cognitive load when working on specific areas

#### ✅ **4. Scalability**

- Team scalability - clear boundaries for parallel work
- Code scalability - easy to add features without breaking existing code

#### ✅ **5. Framework Independence**

- Not locked into a specific technology
- Migrate gradually without full rewrites
- Business logic survives framework deprecation

#### ✅ **6. Business Logic Protection**

- Core business rules isolated and protected
- Changes to external systems don't affect business logic
- Domain knowledge preserved and explicit

#### ✅ **7. Parallel Development**

- Multiple teams can work independently
- Clear interfaces enable contract-first development
- Easier code reviews with defined boundaries

### Cons

#### ❌ **1. Complexity and Overhead**

- More files, classes, and interfaces to manage
- Steeper learning curve for developers
- Can feel over-engineered for simple applications

#### ❌ **2. Initial Development Time**

- Slower initial development compared to framework-driven approach
- More boilerplate code to write
- Setup time for layers and dependencies

#### ❌ **3. Duplication Across Layers**

- Multiple DTOs for the same concept (Entity, InputDTO, OutputDTO, HTTP Schema)
- Data mapping between layers adds code
- Can feel repetitive

#### ❌ **4. Team Knowledge Required**

- Requires understanding of SOLID principles
- Team needs experience with dependency inversion
- Risk of inconsistent implementation without guidance

#### ❌ **5. Overkill for Simple Projects**

- Unnecessary complexity for CRUD apps
- Maintenance burden for small projects
- Not cost-effective for short-lived applications

#### ❌ **6. Debugging Complexity**

- More layers to trace through
- Dependency injection can obscure execution flow
- Requires better tooling and logging

#### ❌ **7. Potential for Incorrect Implementation**

- Easy to violate dependency rules without discipline
- Can end up with "Clean Architecture in name only"
- Requires architectural reviews and vigilance

---

## 🎯 Project Overview

This project is an **educational implementation** showcasing Clean Architecture principles in a real-world Python web application. It provides a fully functional Todo API with CRUD operations while maintaining strict architectural boundaries.

### Key Features

- ✅ **Clean Architecture** - Follows Uncle Bob's layered architecture
- ✅ **SOLID Principles** - Demonstrates all five SOLID principles
- ✅ **Dependency Inversion** - High-level policies don't depend on low-level details
- ✅ **Testability** - Business logic isolated from frameworks
- ✅ **Framework Independence** - Core logic doesn't know about FastAPI or SQLAlchemy
- ✅ **Database Independence** - Easy to swap SQLite for PostgreSQL, MongoDB, etc.

---

## 🏗️ Architecture Layers

The application follows Clean Architecture with four distinct layers:

```
┌─────────────────────────────────────────────────────────────────┐
│                   Frameworks & Drivers                          │
│           (FastAPI Routes, SQLAlchemy Models)                   │
│                     - Web Framework                             │
│                     - Database ORM                              │
│                     - External Services                         │
└─────────────────────────────────────────────────────────────────┘
                            ↓ depends on
┌─────────────────────────────────────────────────────────────────┐
│                   Interface Adapters                            │
│        (Controllers, Gateways, Presenters)                      │
│                     - Convert data formats                      │
│                     - Implement ports                           │
│                     - Adapt external interfaces                 │
└─────────────────────────────────────────────────────────────────┘
                            ↓ depends on
┌─────────────────────────────────────────────────────────────────┐
│                   Use Cases (Application Business Rules)        │
│          (Interactors, Input/Output Ports)                      │
│                     - Application-specific logic                │
│                     - Orchestrate entity operations             │
│                     - Define interfaces (ports)                 │
└─────────────────────────────────────────────────────────────────┘
                            ↓ depends on
┌─────────────────────────────────────────────────────────────────┐
│                   Entities (Enterprise Business Rules)          │
│                  (Domain Models, Value Objects)                 │
│                     - Core business logic                       │
│                     - No external dependencies                  │
│                     - Most stable layer                         │
└─────────────────────────────────────────────────────────────────┘
```

### Dependency Rule

**Dependencies only point inward.** Outer layers can depend on inner layers, but inner layers never depend on outer layers. This is achieved through:

- **Interfaces (Ports)** - Inner layers define interfaces
- **Implementations (Adapters)** - Outer layers implement those interfaces
- **Dependency Injection** - Dependencies are injected at runtime

---

## 📁 Project Structure

```
todo-app/python/
│
├── main.py                          # Application entry point
│
├── app/
│   ├── domain/                      # 🟢 Layer 1: Entities
│   │   └── entities.py              # TodoEntity - Core business model
│   │
│   ├── use_cases/                   # 🔵 Layer 2: Use Cases
│   │   ├── interactors.py           # Use case implementations
│   │   └── ports/
│   │       ├── input_ports.py       # Input boundaries (DTOs + Interfaces)
│   │       ├── output_ports.py      # Output boundaries (DTOs + Interfaces)
│   │       └── gateway_ports.py     # Data access boundaries
│   │
│   ├── interface_adapters/          # 🟡 Layer 3: Interface Adapters
│   │   ├── controllers/
│   │   │   └── todo_controller.py   # HTTP request orchestration
│   │   ├── presenters/
│   │   │   └── todo_presenter.py    # Output formatting
│   │   └── gateways/
│   │       └── todo_gateway.py      # Data persistence implementation
│   │
│   └── frameworks_and_drivers/      # 🔴 Layer 4: Frameworks & Drivers
│       ├── web/
│       │   ├── routes.py            # FastAPI route definitions
│       │   └── schemas.py           # Pydantic HTTP schemas
│       └── database/
│           ├── database.py          # SQLAlchemy configuration
│           └── models.py            # ORM models
│
├── alembic/                         # Database migrations
├── alembic.ini                      # Alembic configuration
├── todos.db                         # SQLite database file
└── .gitignore
```

---

## 💡 Core Concepts

### 1. Entities (Domain Layer)

**Location:** `app/domain/entities.py`

The innermost layer containing enterprise business rules. Entities are pure business objects with no dependencies.

```python
@dataclass
class TodoEntity:
    """Pure domain model - no framework dependencies"""
    title: str
    description: str | None = None
    completed: bool = False
    id: UUID = field(default_factory=uuid.uuid4)

    def mark_completed(self) -> None:
        """Business logic lives in entities"""
        self.completed = True
```

**Characteristics:**

- Framework-independent
- Contains business rules
- Most stable (rarely changes)

---

### 2. Use Cases (Application Business Rules)

**Location:** `app/use_cases/`

Use cases orchestrate the flow of data between entities and external systems. They contain application-specific business rules.

#### Input Ports (Input Boundaries)

Define what the system can do. Controllers depend on these interfaces.

```python
class ICreateTodoInputPort(ABC):
    """Interface defining the contract for creating todos"""
    @abstractmethod
    def execute(self, input_dto: CreateTodoInputDTO) -> None:
        pass
```

#### Output Ports (Output Boundaries)

Define how results are presented. Use cases call these to deliver results.

```python
class ICreateTodoOutputPort(ABC):
    """Interface for presenting creation results"""
    @abstractmethod
    def present_success(self, todo: TodoEntity) -> None:
        pass

    @abstractmethod
    def present_error(self, message: str) -> None:
        pass
```

#### Gateway Ports

Define data access interfaces. Use cases use these to persist data.

```python
class ITodoGateway(ABC):
    """Interface for data persistence"""
    @abstractmethod
    def save(self, todo: TodoEntity) -> TodoEntity:
        pass
```

#### Interactors

Implement use cases by orchestrating entities, gateways, and presenters.

```python
class CreateTodoInteractor(ICreateTodoInputPort):
    def __init__(self, gateway: ITodoGateway, output_port: ICreateTodoOutputPort):
        self.gateway = gateway
        self.output_port = output_port

    def execute(self, input_dto: CreateTodoInputDTO) -> None:
        # 1. Validate business rules
        # 2. Create entity
        # 3. Persist via gateway
        # 4. Present result
```

---

### 3. Interface Adapters

**Location:** `app/interface_adapters/`

This layer converts data between the format most convenient for use cases and entities, and the format needed by external systems.

#### Controllers

Receive requests, create presenters, execute use cases, and handle HTTP concerns.

```python
class TodoController:
    def create_todo(self, title: str, description: str | None):
        presenter = CreateTodoPresenter()
        interactor = self.create_interactor_factory(presenter)
        interactor.execute(CreateTodoInputDTO(title, description))

        if presenter.error_message:
            raise HTTPException(400, presenter.error_message)
        return presenter.response_data
```

#### Presenters

Implement output ports to format data for presentation.

```python
class CreateTodoPresenter(ICreateTodoOutputPort):
    def __init__(self):
        self.response_data = None
        self.error_message = None

    def present_success(self, todo: TodoEntity):
        self.response_data = TodoOutputDTO(...)
```

#### Gateways

Implement gateway ports to access databases.

```python
class SqlAlchemyTodoGateway(ITodoGateway):
    def save(self, todo: TodoEntity) -> TodoEntity:
        # Convert entity → ORM model
        # Save to database
        # Convert ORM model → entity
```

---

### 4. Frameworks & Drivers

**Location:** `app/frameworks_and_drivers/`

The outermost layer containing framework-specific code.

#### Web Layer

- **Routes** - FastAPI endpoint definitions
- **Schemas** - Pydantic request/response models

#### Database Layer

- **Database** - SQLAlchemy engine and session configuration
- **Models** - ORM models for database tables

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- pip or uv

### Installation

1. **Navigate to the project directory:**

   ```bash
   cd architectural-patterns/rest/04-clean-code/todo-app/python
   ```

2. **Create and activate a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
   pip install fastapi uvicorn sqlalchemy alembic python-dotenv
   ```

4. **Initialize the database:**

   ```bash
   alembic upgrade head
   ```

5. **Run the application:**

   ```bash
   uvicorn main:app --reload
   ```

6. **Access the API:**
   - API: `http://localhost:8000/todos`
   - Interactive docs: `http://localhost:8000/docs`
   - OpenAPI schema: `http://localhost:8000/openapi.json`

---

## 🌐 API Endpoints

### Create Todo

```http
POST /todos/
Content-Type: application/json

{
  "title": "Learn Clean Architecture",
  "description": "Study Uncle Bob's principles"
}
```

**Response:** `201 Created`

```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "title": "Learn Clean Architecture",
  "description": "Study Uncle Bob's principles",
  "completed": false
}
```

### List Todos

```http
GET /todos/?skip=0&limit=100
```

**Response:** `200 OK`

```json
[
  {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "title": "Learn Clean Architecture",
    "description": "Study Uncle Bob's principles",
    "completed": false
  }
]
```

### Get Todo

```http
GET /todos/{todo_id}
```

**Response:** `200 OK` or `404 Not Found`

### Update Todo

```http
PATCH /todos/{todo_id}
Content-Type: application/json

{
  "completed": true
}
```

**Response:** `200 OK` or `404 Not Found`

### Delete Todo

```http
DELETE /todos/{todo_id}
```

**Response:** `204 No Content` or `404 Not Found`

---

## 🎨 Design Patterns

### Ports and Adapters (Hexagonal Architecture)

- **Ports** - Interfaces defined by use cases
- **Adapters** - Implementations in outer layers

### Dependency Injection

All dependencies are injected, making the system highly testable.

```python
def get_controller(db: Session = Depends(get_db)) -> TodoController:
    gateway = SqlAlchemyTodoGateway(db)
    # Create interactor factories
    # Return controller with injected dependencies
```

### Factory Pattern

Interactor factories allow each request to have its own presenter instance.

```python
def create_interactor_factory(presenter):
    return CreateTodoInteractor(gateway=gateway, output_port=presenter)
```

### Data Transfer Objects (DTOs)

Decouple layers by using DTOs instead of passing entities or ORM models across boundaries.

- `CreateTodoInputDTO` - Input to use case
- `TodoOutputDTO` - Output from use case
- `CreateTodoHTTPPayload` - HTTP request body
- `TodoHTTPResponse` - HTTP response body

---

## ✅ Benefits of This Implementation

This Todo API implementation demonstrates the key advantages of Clean Architecture in practice:

### 1. **Testability**

Business logic can be tested without frameworks:

```python
def test_create_todo():
    gateway = InMemoryTodoGateway()  # Test double
    presenter = CreateTodoPresenter()
    interactor = CreateTodoInteractor(gateway, presenter)

    interactor.execute(CreateTodoInputDTO("Test"))

    assert presenter.response_data.title == "Test"
```

### 2. **Framework Independence**

Core business logic has no dependencies on FastAPI or SQLAlchemy. You could swap to:

- Flask, Django, or any web framework
- PostgreSQL, MongoDB, or any database
- Without changing entities or use cases

### 3. **Maintainability**

Clear separation of concerns makes code easier to:

- Understand
- Modify
- Extend
- Debug

### 4. **Flexibility**

Add new features without affecting existing code:

- Add GraphQL alongside REST
- Add Redis caching
- Add event sourcing
- Implement CQRS

### 5. **Business Logic Protection**

Business rules are isolated and protected from framework changes and external dependencies.

---

## 🧪 Testing Strategy

### Unit Tests

**Entities** - Test business logic in isolation

```python
def test_mark_completed():
    todo = TodoEntity(title="Test")
    todo.mark_completed()
    assert todo.completed == True
```

**Use Cases** - Test with mocked dependencies

```python
def test_create_todo_with_forbidden_word():
    gateway = MockGateway()
    presenter = CreateTodoPresenter()
    interactor = CreateTodoInteractor(gateway, presenter)

    interactor.execute(CreateTodoInputDTO("forbidden word"))

    assert presenter.error_message == "Title contains disallowed words."
```

### Integration Tests

Test adapters with real frameworks:

```python
def test_gateway_saves_todo():
    db = TestSessionLocal()
    gateway = SqlAlchemyTodoGateway(db)
    todo = TodoEntity(title="Test")

    saved = gateway.save(todo)

    assert saved.id == todo.id
```

### End-to-End Tests

Test the full application:

```python
def test_create_todo_endpoint():
    response = client.post("/todos/", json={"title": "Test"})
    assert response.status_code == 201
    assert response.json()["title"] == "Test"
```

---

## 📚 Further Reading

### Books

- **Clean Architecture** by Robert C. Martin (Uncle Bob)
- **Clean Code** by Robert C. Martin
- **Domain-Driven Design** by Eric Evans

### Articles

- [The Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Ports and Adapters Pattern](https://alistair.cockburn.us/hexagonal-architecture/)

### Related Patterns

- Hexagonal Architecture (Ports and Adapters)
- Onion Architecture
- Domain-Driven Design (DDD)
- CQRS (Command Query Responsibility Segregation)

---

## 🤝 Contributing

This is an educational project. Feel free to:

- Add more use cases
- Implement additional adapters
- Add comprehensive tests
- Improve documentation

---

## 📝 License

This project is part of an educational guide and is available for learning purposes.

---

## 🙏 Acknowledgments

- Robert C. Martin (Uncle Bob) for Clean Architecture principles
- The FastAPI and SQLAlchemy communities
- All contributors to SOLID principles and design patterns

---

**Happy Learning! 🚀**
