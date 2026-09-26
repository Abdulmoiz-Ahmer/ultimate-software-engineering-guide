# GraphQL Todo Application with DataLoader & Security

A production-ready GraphQL API demonstration built with FastAPI, Strawberry, and SQLAlchemy that showcases best practices for solving common GraphQL challenges: the **N+1 query problem** and **malicious recursive queries**.

---

## Table of Contents

1. [What is GraphQL?](#what-is-graphql)
2. [Pros and Cons](#pros-and-cons)
3. [When to Use GraphQL](#when-to-use-graphql)
4. [When NOT to Use GraphQL](#when-not-to-use-graphql)
5. [The N+1 Query Problem](#the-n1-query-problem)
6. [Malicious Recursive Queries](#malicious-recursive-queries)
7. [Application Architecture](#application-architecture)
8. [Installation & Setup](#installation--setup)
9. [Usage Examples](#usage-examples)
10. [Project Structure](#project-structure)
11. [Technical Implementation](#technical-implementation)

---

## What is GraphQL?

**GraphQL** is a query language for APIs and a runtime for executing those queries. Created by Facebook in 2012 and open-sourced in 2015, GraphQL provides a complete and understandable description of the data in your API.

### Core Concepts

- **Schema-Driven**: Define your API structure using a strongly-typed schema
- **Client-Specified Queries**: Clients request exactly the data they need, nothing more
- **Single Endpoint**: One endpoint handles all operations (unlike REST's multiple endpoints)
- **Hierarchical Structure**: Queries mirror the shape of the data they return
- **Introspection**: The API is self-documenting and explorable

### How It Works

```graphql
# Client Query (request exactly what you need)
{
  users {
    id
    name
    todos {
      title
    }
  }
}

# Server Response (same shape as query)
{
  "data": {
    "users": [
      {
        "id": "123",
        "name": "Alice",
        "todos": [
          { "title": "Buy groceries" },
          { "title": "Walk the dog" }
        ]
      }
    ]
  }
}
```

---

## Pros and Cons

### ✅ Advantages

1. **Precise Data Fetching**
   - No over-fetching (getting unnecessary data)
   - No under-fetching (making multiple round trips)
   - Clients get exactly what they request

2. **Strong Typing**
   - Schema provides a contract between frontend and backend
   - Compile-time validation and IDE autocomplete
   - Self-documenting API via introspection

3. **Single Endpoint**
   - Simplifies API architecture
   - No need to version endpoints (schema evolution)
   - Easier to maintain and deploy

4. **Efficient for Complex UIs**
   - Reduce network requests by combining multiple resources
   - Perfect for mobile apps with bandwidth constraints
   - Nested queries match component hierarchies

5. **Developer Experience**
   - GraphiQL/Playground for interactive exploration
   - Rich tooling ecosystem (Apollo, Relay, etc.)
   - Strongly typed client generation

6. **Flexibility**
   - Frontend teams can iterate without backend changes
   - Add new fields without breaking existing queries
   - Deprecation system for safe evolution

### ❌ Disadvantages

1. **Complexity**
   - Steeper learning curve than REST
   - Requires careful schema design
   - More complex backend implementation

2. **Caching Challenges**
   - HTTP caching (ETags, Cache-Control) harder to implement
   - Requires specialized caching strategies
   - No standardized caching like REST

3. **Performance Issues**
   - **N+1 query problem** (see detailed section below)
   - Potential for expensive queries if not monitored
   - Query complexity analysis required

4. **Security Concerns**
   - **Recursive queries** can DoS the server
   - Rate limiting more complex than REST
   - Need depth limiting, cost analysis, and query allowlisting

5. **File Upload Complexity**
   - Not natively supported (requires extensions)
   - More complex than multipart/form-data in REST

6. **Monitoring & Debugging**
   - All requests go to one endpoint (harder to monitor)
   - Need specialized tools for query analysis
   - Error handling less standardized than HTTP status codes

7. **Overkill for Simple APIs**
   - REST may be simpler for CRUD operations
   - Additional overhead for straightforward use cases

---

## When to Use GraphQL

GraphQL is an excellent choice for:

### 1. **Complex Frontend Requirements**

- Applications with nested, interconnected data
- UIs that display data from multiple sources
- Dashboards aggregating various data points

### 2. **Mobile Applications**

- Bandwidth-constrained environments
- Need to minimize network requests
- Varying screen sizes require different data

### 3. **Microservices Architecture**

- Unified API gateway over multiple services
- Backend for Frontend (BFF) pattern
- Federated GraphQL for service composition

### 4. **Frequent Frontend Changes**

- Rapidly evolving product requirements
- Multiple client platforms (web, iOS, Android)
- Frontend teams need autonomy

### 5. **Real-Time Applications**

- GraphQL subscriptions for live data
- Collaborative tools (chat, docs, whiteboards)
- Live dashboards and monitoring tools

### 6. **Version-Heavy APIs**

- Avoid the pain of API versioning
- Support multiple client versions simultaneously
- Gradual migration paths

### 7. **Developer Tooling**

- Internal tools requiring flexibility
- Admin dashboards with complex filtering
- Data exploration and analytics platforms

---

## When NOT to Use GraphQL

GraphQL may not be the best choice for:

### 1. **Simple CRUD APIs**

- Straightforward create/read/update/delete operations
- REST is simpler and more direct
- No complex relationships or nesting

### 2. **File Upload/Download Heavy**

- Downloading large files
- Streaming media content
- Binary data transfer (use REST or dedicated services)

### 3. **Caching is Critical**

- Heavily cacheable public data (news sites, blogs)
- CDN caching required
- HTTP-level caching needed

### 4. **Small Team with Limited Experience**

- Lack of GraphQL expertise
- No time for learning curve
- Simple requirements don't justify complexity

### 5. **Public APIs with Unpredictable Load**

- Cannot control client query complexity
- High risk of abuse without proper safeguards
- Rate limiting and monitoring challenges

### 6. **Performance-Critical Systems**

- Ultra-low latency requirements
- Cannot afford resolver overhead
- Simple key-value lookups

### 7. **Legacy System Integration**

- Existing REST APIs work well
- No bandwidth for migration
- Integration complexity not worth benefits

---

## The N+1 Query Problem

### What is the N+1 Problem?

The N+1 query problem occurs when fetching a list of items (1 query) triggers additional queries for related data (N queries), resulting in **N+1 total database queries**.

### Example Scenario

**Query**: Fetch 3 users and their todos

#### ❌ Without DataLoaders (N+1 Problem)

```
1. SELECT * FROM users;                    -- 1 query
2. SELECT * FROM todos WHERE user_id=1;    -- Query for user 1
3. SELECT * FROM todos WHERE user_id=2;    -- Query for user 2
4. SELECT * FROM todos WHERE user_id=3;    -- Query for user 3

Total: 4 queries (1 + N where N=3)
```

If you have 100 users, this becomes **101 queries**! This scales linearly with the number of users and causes severe performance degradation.

### Performance Impact

| Users | Without DataLoader | With DataLoader | Improvement  |
| ----- | ------------------ | --------------- | ------------ |
| 10    | 11 queries         | 2 queries       | 82% faster   |
| 100   | 101 queries        | 2 queries       | 98% faster   |
| 1000  | 1001 queries       | 2 queries       | 99.8% faster |

### ✅ Solution: DataLoaders

**DataLoaders** batch and cache data requests within a single request cycle.

#### How DataLoaders Work

1. **Batching**: Collect multiple `load()` calls
2. **Dedupe**: Remove duplicate IDs
3. **Execute**: Run a single batched query
4. **Cache**: Store results for the request duration
5. **Distribute**: Return data to each caller

#### With DataLoaders (Optimal)

```
1. SELECT * FROM users;                           -- 1 query
2. SELECT * FROM todos WHERE user_id IN (1,2,3);  -- 1 batched query

Total: 2 queries (always!)
```

### Implementation in This Project

```python
# app/dataloaders.py

async def batch_load_todos_by_user_id(keys: list[UUID], db: Session):
    """Batch function that loads todos for multiple users at once"""
    # Single query with WHERE IN clause
    todos = db.query(TodoORM).filter(TodoORM.user_id.in_(keys)).all()

    # Group results by user_id
    user_todos_map = defaultdict(list)
    for todo in todos:
        user_todos_map[todo.user_id].append(todo)

    # Return in the same order as input keys
    return [user_todos_map[user_id] for user_id in keys]

# Create DataLoader instance
todos_loader = DataLoader(load_fn=batch_load_todos_by_user_id)
```

### Key DataLoader Rules

1. **Per-Request Scope**: Create new instances for each request
2. **Never Share**: Sharing causes cache leaks between users
3. **Order Matters**: Return results in the same order as input keys
4. **Handle Missing Data**: Return `None` or empty list for missing items

---

## Malicious Recursive Queries

### What are Recursive Queries?

GraphQL's flexible nature allows clients to create **deeply nested queries** that can overwhelm the server by traversing circular relationships indefinitely.

### The Problem

Consider this malicious query exploiting the User ↔ Todo relationship:

```graphql
{
  users {
    name
    todos {
      title
      author {
        name
        todos {
          title
          author {
            name
            todos {
              # This continues indefinitely!
              # Each level multiplies the data fetched
            }
          }
        }
      }
    }
  }
}
```

### Impact

| Depth | Objects Fetched | Database Queries | Server Load |
| ----- | --------------- | ---------------- | ----------- |
| 3     | ~100            | Moderate         | Acceptable  |
| 5     | ~10,000         | Heavy            | Slow        |
| 10    | ~10M            | Catastrophic     | **Crash**   |

**Result**: Denial of Service (DoS), server crashes, database overload

### Attack Scenarios

1. **Recursive Loops**: User → Todos → Author → Todos → ...
2. **Exponential Expansion**: Fetching related entities at each level
3. **Resource Exhaustion**: Memory overflow, CPU saturation
4. **Distributed DoS**: Multiple clients sending complex queries

### ✅ Solutions

#### 1. Query Depth Limiting (Implemented in This Project)

Reject queries exceeding a maximum nesting depth:

```python
# app/schema.py

from strawberry.extensions import QueryDepthLimiter

schema = strawberry.Schema(
    query=Query,
    extensions=[QueryDepthLimiter(max_depth=3)]
)
```

**How it works**:

- Analyzes query structure before execution
- Counts nesting levels
- Rejects queries exceeding `max_depth`
- Returns error: "Query depth exceeds maximum allowed"

**Example**: With `max_depth=3`:

```graphql
{
  users {        # Depth 1 ✅
    todos {      # Depth 2 ✅
      author {   # Depth 3 ✅
        todos {  # Depth 4 ❌ REJECTED!
        }
      }
    }
  }
}
```

#### 2. Query Complexity Analysis

Assign costs to fields and limit total query cost:

```python
from strawberry.extensions import QueryComplexityLimiter

# Each field has a cost, limit total cost
schema = strawberry.Schema(
    query=Query,
    extensions=[QueryComplexityLimiter(max_complexity=1000)]
)
```

#### 3. Query Cost Calculation

Calculate cost based on arguments (e.g., pagination limits):

```graphql
# Cost = depth × limit
# Cost = 5 × 100 = 500
{
  users(limit: 100) {
    todos(limit: 5) {
      title
    }
  }
}
```

#### 4. Timeout Limits

Set maximum execution time per query:

```python
# Reject queries taking longer than 5 seconds
schema = strawberry.Schema(
    query=Query,
    extensions=[ExecutionTimeoutExtension(max_seconds=5)]
)
```

#### 5. Query Allowlisting (Persisted Queries)

Only allow pre-approved queries:

```python
# Clients send query IDs instead of query strings
allowed_queries = {
    "getUsers": "{ users { name todos { title } } }",
    "getTodos": "{ todos { title author { name } } }"
}

# Reject any query not in the allowlist
```

#### 6. Rate Limiting

Limit requests per user/IP:

```python
from fastapi_limiter import FastAPILimiter

# Max 100 requests per minute per IP
@app.middleware("http")
async def rate_limit_middleware(request, call_next):
    await rate_limiter.check(request.client.host)
    return await call_next(request)
```

### Best Practices

1. **Always implement depth limiting** (minimum protection)
2. **Add complexity analysis** for production
3. **Monitor query patterns** and adjust limits
4. **Combine multiple strategies** for defense in depth
5. **Log and alert** on rejected queries
6. **Educate clients** about query limits

---

## Application Architecture

This application demonstrates a clean, layered architecture for GraphQL APIs.

### Technology Stack

| Layer               | Technology            | Purpose                         |
| ------------------- | --------------------- | ------------------------------- |
| **Web Framework**   | FastAPI               | HTTP server and routing         |
| **GraphQL Library** | Strawberry            | Schema definition and execution |
| **ORM**             | SQLAlchemy            | Database abstraction            |
| **Database**        | SQLite                | Data persistence (demo)         |
| **DataLoader**      | Strawberry DataLoader | N+1 query optimization          |
| **Service Layer**   | TodoService           | Business logic encapsulation    |

### Architecture Layers

```
┌─────────────────────────────────────────────────┐
│           FastAPI Application (main.py)         │
│  - HTTP Server                                  │
│  - Dependency Injection                         │
│  - Request/Response Handling                    │
└─────────────────────┬───────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────┐
│       GraphQL Layer (schema.py)                 │
│  - Type Definitions (UserType, TodoType)        │
│  - Input Types (CreateTodoInput, etc.)          │
│  - Query Resolvers (queries)                    │
│  - Mutation Resolvers (create, update, delete)  │
│  - Query Depth Limiting                         │
└─────────────────────┬───────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────┐
│      Service Layer (services/todo_service.py)   │
│  - Business Logic                               │
│  - Validation                                   │
│  - Database Operations                          │
│  - Transaction Management                       │
└─────────────────────┬───────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────┐
│      DataLoader Layer (dataloaders.py)          │
│  - Batch Loading Functions                      │
│  - Query Optimization                           │
│  - Request-Scoped Caching                       │
└─────────────────────┬───────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────┐
│         ORM Layer (models.py)                   │
│  - UserORM: User entity definition              │
│  - TodoORM: Todo entity definition              │
│  - Relationships: User ↔ Todo                   │
└─────────────────────┬───────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────┐
│      Database Layer (core/database.py)          │
│  - SQLAlchemy Engine                            │
│  - Session Management                           │
│  - Database Initialization                      │
└─────────────────────┬───────────────────────────┘
                      │
                ┌─────▼─────┐
                │  SQLite   │
                │ Database  │
                └───────────┘
```

### Data Flow

#### Read Flow (GraphQL Query)

```
1. Client → FastAPI (/graphql endpoint)
2. FastAPI → GraphQL Router
3. GraphQL Router → Schema Query Resolver
4. Resolver → DataLoader.load() calls
5. DataLoader → Batch function (SQL query)
6. Database → Return results
7. DataLoader → Distribute to resolvers
8. Schema → Construct response object
9. FastAPI → Return JSON to client
```

#### Write Flow (GraphQL Mutation)

```
1. Client → FastAPI (/graphql endpoint with mutation)
2. FastAPI → GraphQL Router
3. GraphQL Router → Schema Mutation Resolver
4. Mutation Resolver → TodoService method
5. TodoService → Validate & execute database operation
6. Database → Execute INSERT/UPDATE/DELETE
7. TodoService → Return updated entity
8. Schema → Convert ORM to GraphQL type
9. FastAPI → Return JSON to client
```

#### Example: Fetching Users with Todos

```graphql
{
  users {
    name
    todos {
      title
    }
  }
}
```

**Execution Steps**:

1. **Query.users** resolver executes
   - `db.query(UserORM).all()` → Fetch all users (1 query)
2. For each user, **UserType.todos** resolver executes
   - Calls `todos_loader.load(user.id)` (doesn't execute yet!)
3. **DataLoader batches** all load calls
   - Collects all user IDs: `[uuid1, uuid2, uuid3]`
4. **Batch function executes**
   - `SELECT * FROM todos WHERE user_id IN (uuid1, uuid2, uuid3)` (1 query)
5. **Results distributed** to each resolver
6. **Response constructed** and returned

**Total Queries**: 2 (optimal!)

### Database Schema

```sql
-- Users Table
CREATE TABLE users (
    id UUID PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);

-- Todos Table
CREATE TABLE todos (
    id UUID PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    user_id UUID NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Relationship: One User → Many Todos
-- Relationship: One Todo → One User (author)
```

### Service Layer Pattern

The application uses the **Service Layer pattern** to separate business logic from GraphQL resolvers:

**Benefits**:

1. **Separation of Concerns**: GraphQL layer handles API, service layer handles logic
2. **Reusability**: Services can be used by multiple resolvers or other services
3. **Testability**: Business logic can be unit tested independently
4. **Maintainability**: Logic centralized in one place, easier to modify

**TodoService Methods**:

- `create_todo()`: Create a new todo item
- `update_todo()`: Update existing todo (partial updates supported)
- `delete_todo()`: Delete a todo by ID

**Example Service Usage**:

```python
# In mutation resolver
@strawberry.mutation
def create_todo(self, info: Info, input: CreateTodoInput) -> TodoType:
    db = info.context["db"]
    # Delegate to service layer
    return TodoService(db).create_todo(
        title=input.title,
        user_id=input.user_id
    )
```

### Security Architecture

1. **Query Depth Limiting**: Max nesting depth = 3
2. **Request Isolation**: Fresh DataLoaders per request
3. **Session Management**: Proper DB connection cleanup
4. **Type Safety**: Strawberry enforces schema contracts

---

## Installation & Setup

### Prerequisites

- **Python**: 3.14+ (specified in pyproject.toml)
- **uv**: Fast Python package manager ([installation guide](https://docs.astral.sh/uv/))

### Installation Steps

1. **Clone the repository**

```bash
git clone <repository-url>
cd todo-app/python
```

2. **Install dependencies with uv**

```bash
# uv automatically creates a virtual environment and installs dependencies
uv sync
```

This installs:

- FastAPI: Web framework
- Strawberry GraphQL: GraphQL library
- SQLAlchemy: ORM
- Uvicorn: ASGI server
- Pydantic: Data validation

3. **Activate the virtual environment**

```bash
source .venv/bin/activate  # On Unix/macOS
# or
.venv\Scripts\activate     # On Windows
```

### Running the Application

```bash
# Development mode with auto-reload
uvicorn app.main:app --reload

# Production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The server starts at: **http://localhost:8000**

### Access GraphiQL Interface

Open your browser and navigate to:

```
http://localhost:8000/graphql
```

GraphiQL provides:

- Interactive query editor with syntax highlighting
- Auto-completion based on schema
- Schema documentation explorer
- Query history

---

## Usage Examples

### Example 1: Fetch All Users

```graphql
{
  users {
    id
    name
  }
}
```

**Response**:

```json
{
  "data": {
    "users": [
      {
        "id": "123e4567-e89b-12d3-a456-426614174000",
        "name": "User 1"
      },
      {
        "id": "223e4567-e89b-12d3-a456-426614174001",
        "name": "User 2"
      },
      {
        "id": "323e4567-e89b-12d3-a456-426614174002",
        "name": "User 3"
      }
    ]
  }
}
```

### Example 2: Users with Their Todos (Demonstrates DataLoader)

```graphql
{
  users {
    name
    todos {
      title
    }
  }
}
```

**Response**:

```json
{
  "data": {
    "users": [
      {
        "name": "User 1",
        "todos": [
          { "title": "Task A for User 1" },
          { "title": "Task B for User 1" }
        ]
      },
      {
        "name": "User 2",
        "todos": [
          { "title": "Task A for User 2" },
          { "title": "Task B for User 2" }
        ]
      },
      {
        "name": "User 3",
        "todos": [
          { "title": "Task A for User 3" },
          { "title": "Task B for User 3" }
        ]
      }
    ]
  }
}
```

**Database Queries**: Only 2!

1. `SELECT * FROM users`
2. `SELECT * FROM todos WHERE user_id IN (...)`

### Example 3: Nested Query with Author Resolution

```graphql
{
  users {
    name
    todos {
      title
      author {
        name
      }
    }
  }
}
```

**Response**:

```json
{
  "data": {
    "users": [
      {
        "name": "User 1",
        "todos": [
          {
            "title": "Task A for User 1",
            "author": { "name": "User 1" }
          },
          {
            "title": "Task B for User 1",
            "author": { "name": "User 1" }
          }
        ]
      }
    ]
  }
}
```

### Example 4: Rejected Query (Too Deep)

```graphql
{
  users {
    todos {
      author {
        todos {
          # Depth 4 - Exceeds max_depth=3
          author {
            name
          }
        }
      }
    }
  }
}
```

**Error Response**:

```json
{
  "errors": [
    {
      "message": "Query depth exceeds maximum allowed depth of 3",
      "extensions": {
        "code": "QUERY_DEPTH_LIMIT_EXCEEDED"
      }
    }
  ]
}
```

### Example 5: Selective Field Fetching

```graphql
{
  users {
    name
    # Only fetch title, not author
    todos {
      title
    }
  }
}
```

This demonstrates GraphQL's precision: fetch only what you need.

### Example 6: Create a New Todo (Mutation)

```graphql
mutation {
  createTodo(
    input: {
      title: "Buy groceries"
      userId: "123e4567-e89b-12d3-a456-426614174000"
    }
  ) {
    id
    title
    completed
    author {
      name
    }
  }
}
```

**Response**:

```json
{
  "data": {
    "createTodo": {
      "id": "456e7890-e89b-12d3-a456-426614174003",
      "title": "Buy groceries",
      "completed": false,
      "author": {
        "name": "User 1"
      }
    }
  }
}
```

### Example 7: Update a Todo (Mutation)

```graphql
mutation {
  updateTodo(
    id: "456e7890-e89b-12d3-a456-426614174003"
    input: { title: "Buy organic groceries", completed: true }
  ) {
    id
    title
    completed
  }
}
```

**Response**:

```json
{
  "data": {
    "updateTodo": {
      "id": "456e7890-e89b-12d3-a456-426614174003",
      "title": "Buy organic groceries",
      "completed": true
    }
  }
}
```

### Example 8: Delete a Todo (Mutation)

```graphql
mutation {
  deleteTodo(id: "456e7890-e89b-12d3-a456-426614174003")
}
```

**Response**:

```json
{
  "data": {
    "deleteTodo": true
  }
}
```

**Note**: Returns `false` if the todo doesn't exist.

---

## Project Structure

```
python/
├── app/
│   ├── __init__.py                 # Package initializer
│   ├── main.py                     # FastAPI app entry point
│   ├── schema.py                   # GraphQL schema & types
│   ├── models.py                   # SQLAlchemy ORM models
│   ├── dataloaders.py              # DataLoader implementations
│   └── core/
│       ├── __init__.py
│       └── database.py             # Database config & seeding
├── pyproject.toml                  # Project dependencies (uv)
├── uv.lock                         # Dependency lock file
├── graphql_demo.db                 # SQLite database (generated)
├── .gitignore                      # Git ignore rules
└── README.md                       # This file
```

### File Descriptions

#### `app/main.py`

- FastAPI application setup
- GraphQL router configuration
- Database session dependency injection
- Context factory for GraphQL resolvers

#### `app/schema.py`

- Strawberry GraphQL schema definition
- Type definitions (`UserType`, `TodoType`)
- Field resolvers with DataLoader integration
- Query depth limiting extension

#### `app/models.py`

- SQLAlchemy ORM models
- `UserORM`: User entity with UUID primary key
- `TodoORM`: Todo entity with foreign key to users
- Bidirectional relationships

#### `app/dataloaders.py`

- DataLoader batch functions
- `batch_load_todos_by_user_id`: Batch load todos
- `batch_load_users_by_id`: Batch load users
- `create_dataloaders`: Factory for per-request loaders

#### `app/core/database.py`

- SQLAlchemy engine configuration
- Session factory
- Database initialization with seed data

---

## Technical Implementation

### DataLoader Implementation Details

#### Creating DataLoaders Per Request

```python
# app/main.py

async def get_graphql_context(db: Session = Depends(get_db)):
    return {
        "db": db,
        "dataloaders": create_dataloaders(db),  # Fresh instances!
    }
```

**Why per-request?**

- Prevents cache leaks between users
- Ensures fresh data for each request
- Avoids memory leaks from unbounded caching

#### Batch Function Requirements

```python
async def batch_load_todos_by_user_id(keys: list[UUID], db: Session):
    # 1. Fetch data with WHERE IN (single query)
    todos = db.query(TodoORM).filter(TodoORM.user_id.in_(keys)).all()

    # 2. Group results
    user_todos_map = defaultdict(list)
    for todo in todos:
        user_todos_map[todo.user_id].append(todo)

    # 3. CRITICAL: Return in the same order as keys!
    return [user_todos_map[user_id] for user_id in keys]
```

**Rules**:

1. Return list of same length as `keys`
2. Same order as `keys`
3. Use `None` or empty list for missing data

### Query Depth Limiting Implementation

```python
# app/schema.py

from strawberry.extensions import QueryDepthLimiter

schema = strawberry.Schema(
    query=Query,
    extensions=[QueryDepthLimiter(max_depth=3)]
)
```

**How it works**:

1. Parser analyzes query AST before execution
2. Counts nesting levels recursively
3. Rejects if depth > `max_depth`
4. Returns error to client

### Type-Safe Resolvers

```python
@strawberry.type
class UserType:
    id: UUID
    name: str

    @strawberry.field
    async def todos(self, info: Info) -> list[TodoType]:
        # Type-safe: returns list of TodoType
        dataloader = info.context["dataloaders"]["todos_by_user_id"]
        return await dataloader.load(self.id)
```

**Benefits**:

- IDE autocomplete
- Compile-time type checking
- Runtime validation

---

## Key Takeaways

### When This Architecture Shines

✅ **Perfect for**:

- Complex, nested data relationships
- Multiple client platforms (web, mobile)
- Microservices aggregation
- Real-time features with subscriptions

### Performance Optimizations

1. **DataLoaders**: Solve N+1 queries
2. **Depth Limiting**: Prevent DoS attacks
3. **Request Scoping**: Isolate user data
4. **Batch Queries**: Single database roundtrips

### Production Considerations

Before deploying to production:

1. **Replace SQLite** with PostgreSQL/MySQL
2. **Add authentication** and authorization
3. **Implement rate limiting** per user/IP
4. **Add query complexity analysis**
5. **Set up monitoring** and logging
6. **Add persisted queries** (query allowlisting)
7. **Configure CORS** properly
8. **Use connection pooling** for databases
9. **Add database migrations** (Alembic)
10. **Implement error tracking** (Sentry)

---

## Resources & Further Learning

### Official Documentation

- [GraphQL Specification](https://spec.graphql.org/)
- [Strawberry GraphQL](https://strawberry.rocks/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)

### DataLoader Resources

- [Facebook DataLoader (original)](https://github.com/graphql/dataloader)
- [DataLoader Pattern Explained](https://github.com/graphql/dataloader#batching)

### Security

- [GraphQL Security Best Practices](https://cheatsheetseries.owasp.org/cheatsheets/GraphQL_Cheat_Sheet.html)
- [Query Complexity Analysis](https://www.apollographql.com/blog/graphql-query-complexity-analysis)

---

## License

This project is provided as an educational example for demonstrating GraphQL best practices, including N+1 query optimization and security implementations.

---

## Contributing

Contributions are welcome! The project already includes:

- [x] Queries for fetching users and todos
- [x] Mutations (create, update, delete)
- [x] Service layer pattern
- [x] DataLoader for N+1 optimization
- [x] Query depth limiting for security

Areas for further improvement:

- [ ] Implement authentication with JWT
- [ ] Add pagination (cursor-based)
- [ ] Add filtering and sorting
- [ ] Implement subscriptions (WebSocket)
- [ ] Add comprehensive test suite
- [ ] Add query complexity analysis
- [ ] Docker containerization
- [ ] CI/CD pipeline
- [ ] Add soft deletes with audit trails

---

**Built with ❤️ to demonstrate GraphQL best practices**
