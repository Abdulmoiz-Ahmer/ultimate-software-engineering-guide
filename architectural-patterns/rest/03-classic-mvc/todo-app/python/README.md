# Todo API - Model-View-Controller (MVC) Architecture

A RESTful Todo API built with FastAPI demonstrating the classic **Model-View-Controller (MVC)** architectural pattern. This project showcases the separation of concerns between data (Model), presentation (View), and business logic (Controller).

## 🏗️ Architecture Overview

This application implements the **MVC (Model-View-Controller)** pattern, one of the most established architectural patterns for building web applications:

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

### MVC Data Flow

```
1. HTTP Request (JSON)
        ↓
2. Controller receives request
        ↓
3. Input View validates data
        ↓
4. Controller applies business logic
        ↓
5. Controller manipulates Model (database)
        ↓
6. Output View formats Model data
        ↓
7. Controller returns HTTP Response (JSON)
```

## 🎯 MVC Components Explained

### Model (The "M")
**Location:** `app/models/todo.py`

The Model represents **what the data is**. It's responsible for:
- Defining data structure (database schema)
- Encapsulating data access (ORM)
- Representing domain entities
- Being independent of presentation and HTTP concerns

```python
class TodoModel(Base):
    """The Model - represents data structure"""
    __tablename__ = "todos"
    id = Column(UUID, primary_key=True)
    title = Column(String(100))
    description = Column(String(255))
    completed = Column(Boolean, default=False)
```

### View (The "V")
**Location:** `app/views/todo_view.py`

The View represents **how the data is presented**. It's responsible for:
- Defining presentation format (JSON schemas)
- Input validation (request schemas)
- Output serialization (response schemas)
- Being independent of data storage details

```python
class TodoResponseView(BaseModel):
    """The View - defines presentation format"""
    id: UUID
    title: str
    description: str | None
    completed: bool
```

### Controller (The "C")
**Location:** `app/controllers/todo_controller.py`

The Controller represents **how the data is processed**. It's responsible for:
- Handling HTTP requests
- Implementing business logic
- Coordinating Model and View
- Error handling and workflow orchestration

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

## ✨ Key Features

- ✅ **Classic MVC Pattern**: Clean separation of Model, View, and Controller
- ✅ **RESTful API**: Standard HTTP methods and status codes
- ✅ **Input Validation**: Pydantic schemas validate incoming data
- ✅ **Output Formatting**: Consistent JSON response format via Views
- ✅ **Business Logic in Controller**: Validation rules and workflow orchestration
- ✅ **UUID Primary Keys**: Globally unique identifiers for security
- ✅ **Type Safety**: Full type hints with Pydantic validation
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

## 📡 API Endpoints

| Method | Endpoint | Description | Controller Action | Response View |
|--------|----------|-------------|-------------------|---------------|
| `POST` | `/todos/` | Create a new todo | `create_todo()` | `TodoResponseView` (201) |
| `GET` | `/todos/` | Get all todos | `list_todos()` | `List[TodoResponseView]` (200) |
| `GET` | `/todos/{id}` | Get a specific todo | `get_todo()` | `TodoResponseView` (200) |
| `PATCH` | `/todos/{id}` | Update a todo | `update_todo()` | `TodoResponseView` (200) |
| `DELETE` | `/todos/{id}` | Delete a todo | `delete_todo()` | No content (204) |

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

## 🎯 MVC Pattern Deep Dive

### Separation of Concerns

The MVC pattern enforces **separation of concerns** through three distinct layers:

| Component | Concern | Independence |
|-----------|---------|--------------|
| **Model** | Data structure & persistence | Independent of View and Controller |
| **View** | Presentation & formatting | Independent of Model details |
| **Controller** | Business logic & orchestration | Knows about both Model and View |

### Responsibilities Matrix

| Task | Model | View | Controller |
|------|-------|------|------------|
| Define data schema | ✅ | ❌ | ❌ |
| Database queries | ✅ | ❌ | ✅ (initiates) |
| Validate input | ❌ | ✅ | ✅ (checks) |
| Business rules | ❌ | ❌ | ✅ |
| Format responses | ❌ | ✅ | ❌ |
| Handle HTTP | ❌ | ❌ | ✅ |
| Error handling | ❌ | ❌ | ✅ |

### MVC in Action: Create Todo Flow

Let's trace what happens when you create a todo:

```python
# 1. HTTP Request arrives
POST /todos/
{
  "title": "Learn MVC",
  "description": "Study the pattern"
}

# 2. FastAPI routes to Controller
@router.post("/", response_model=TodoResponseView)
def create_todo(payload: CreateTodoInputView, db: Session):
    
    # 3. Input View validates data
    # CreateTodoInputView ensures title is 1-100 chars
    # Pydantic raises error if validation fails
    
    # 4. Controller applies business logic
    if "forbidden" in payload.title.lower():
        raise HTTPException(400, "Invalid title")
    
    # 5. Controller creates Model
    todo = TodoModel(
        title=payload.title,
        description=payload.description
    )
    
    # 6. Controller persists Model
    db.add(todo)
    db.commit()
    db.refresh(todo)
    
    # 7. Controller returns Model
    # FastAPI converts TodoModel to TodoResponseView
    return todo

# 8. Output View formats response
# TodoResponseView serializes Model to JSON
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Learn MVC",
  "description": "Study the pattern",
  "completed": false
}
```

## 🆚 MVC vs Other Patterns

### MVC vs Layered Architecture

| Aspect | MVC | Layered (N-Tier) |
|--------|-----|------------------|
| **Organization** | Model-View-Controller | Presentation-Business-Data |
| **Focus** | Presentation pattern | Architectural pattern |
| **Layers** | 3 (M-V-C) | 4+ (API-Service-Repository-Model) |
| **Business Logic** | In Controller | In Service Layer |
| **Complexity** | Simple, flat | More abstraction layers |
| **Best For** | Simple CRUD apps | Complex business logic |

### MVC vs Component Architecture

| Aspect | MVC | Unidirectional Component |
|--------|-----|--------------------------|
| **Organization** | By concern (M/V/C) | By feature (components) |
| **Files** | Grouped by type | Grouped by feature |
| **Coupling** | Controller couples M & V | Components independent |
| **Scalability** | Horizontal (add more MVCs) | Vertical (add more components) |
| **Best For** | Traditional apps | Large feature sets |

## 🔄 Request Lifecycle

Understanding the complete request lifecycle in MVC:

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
http POST localhost:8000/todos/ title="Learn MVC" description="Study pattern"

# Get all todos
http GET localhost:8000/todos/

# Get one todo
http GET localhost:8000/todos/{id}

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
```

### Rollback Migrations
```bash
# Downgrade one version
alembic downgrade -1

# Downgrade to base
alembic downgrade base
```

## 🎓 Design Principles

### 1. **Separation of Concerns**
Each component has a single, well-defined responsibility:
- **Model**: "I know what the data is"
- **View**: "I know how the data looks"
- **Controller**: "I know what to do with the data"

### 2. **Loose Coupling**
- Model doesn't know about View or Controller
- View doesn't know about Model structure details
- Controller coordinates but doesn't tightly bind M and V

### 3. **Single Responsibility Principle (SRP)**
Each MVC component focuses on one aspect:
- Model = Data
- View = Presentation
- Controller = Logic

### 4. **Don't Repeat Yourself (DRY)**
- Models define schema once (used by all controllers)
- Views define format once (used across all responses)
- Controllers reuse Models and Views

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

## 🎯 When to Use MVC

### ✅ MVC is Great For:

- **Simple CRUD applications** - Straightforward create/read/update/delete
- **Rapid prototyping** - Quick to set up and understand
- **Small to medium apps** - Not overly complex
- **Traditional web apps** - Originally designed for web
- **RESTful APIs** - Clean mapping to HTTP methods
- **Learning architectures** - Classic, well-documented pattern

### ❌ Consider Alternatives When:

- **Complex business logic** - Use Layered Architecture with Service layer
- **Many independent features** - Use Component Architecture
- **Event-driven systems** - Use Event Sourcing or CQRS
- **Microservices** - Use Domain-Driven Design
- **Real-time updates** - Consider Observer pattern or WebSockets

## 🔧 Extending the Application

### Adding a New Entity (e.g., Users)

1. **Create Model** (`app/models/user.py`):
```python
class UserModel(Base):
    __tablename__ = "users"
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    name = Column(String(100))
    email = Column(String(255))
```

2. **Create Views** (`app/views/user_view.py`):
```python
class CreateUserInputView(BaseModel):
    name: str
    email: str

class UserResponseView(BaseModel):
    id: UUID
    name: str
    email: str
```

3. **Create Controller** (`app/controllers/user_controller.py`):
```python
router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserResponseView)
def create_user(payload: CreateUserInputView, db: Session):
    user = UserModel(name=payload.name, email=payload.email)
    db.add(user)
    db.commit()
    return user
```

4. **Register in main.py**:
```python
from app.controllers.user_controller import router as user_router
app.include_router(user_router)
```

## 🎯 Architecture Benefits

### For Developers:
✅ **Easy to Learn**: Classic, well-documented pattern  
✅ **Easy to Navigate**: Clear folder structure (models/views/controllers)  
✅ **Easy to Test**: Each component testable independently  
✅ **Familiar**: Used by many frameworks (Django, Rails, Laravel)  

### For Projects:
✅ **Quick Setup**: Straightforward structure for CRUD apps  
✅ **Clear Responsibilities**: No confusion about where code goes  
✅ **Maintainable**: Changes are localized to one component  
✅ **Scalable**: Can grow to service-based architecture if needed  

### For Teams:
✅ **Easy Onboarding**: New developers understand it quickly  
✅ **Parallel Work**: Different devs can work on M/V/C  
✅ **Code Reviews**: Clear structure makes reviews easier  
✅ **Standardized**: Industry-standard pattern  

## 📖 History & Context

### Origins of MVC

MVC was invented in 1979 by Trygve Reenskaug for Smalltalk at Xerox PARC. It was designed to separate concerns in graphical user interfaces.

### Evolution

- **1979**: Original MVC for desktop GUI applications
- **1996**: Adapted for web applications (server-side rendering)
- **2000s**: Ruby on Rails popularizes MVC for web
- **2010s**: REST APIs adapt MVC (Views become JSON schemas)
- **Today**: Still widely used, especially for CRUD applications

### Modern Adaptations

In REST APIs (like this project):
- **Model** remains similar (data structure)
- **View** becomes JSON schemas (Pydantic models)
- **Controller** handles HTTP instead of GUI events

## 🤝 Contributing

Feel free to explore, modify, and experiment with this codebase to better understand the MVC architectural pattern!

## 📝 License

This is a sample educational project for learning software architecture patterns.

---

**Happy Coding!** 🚀
