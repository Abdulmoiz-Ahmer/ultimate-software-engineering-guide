# Event-Driven Architecture: Todo Management System

A microservices-based Todo application demonstrating Event-Driven Architecture (EDA) using Python, FastAPI, Redis Pub/Sub, and SQLAlchemy.

## Table of Contents

- [Overview](#overview)
- [What are Microservices?](#what-are-microservices)
- [What is Event-Driven Architecture?](#what-is-event-driven-architecture)
- [Pros and Cons](#pros-and-cons)
- [When to Use EDA](#when-to-use-eda)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Implementation Details](#implementation-details)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Testing the System](#testing-the-system)

## Overview

This project implements a Todo management system using microservices and event-driven architecture. It consists of two independent services:

1. **Todo Service (Producer)** - Manages todo items (create, delete) and publishes events
2. **Audit Service (Consumer)** - Subscribes to events and maintains an audit log

The services communicate asynchronously through Redis Pub/Sub, demonstrating loose coupling and independent scalability.

## What are Microservices?

**Microservices** is an architectural style that structures an application as a collection of small, autonomous services modeled around a business domain. Each service:

- Runs in its own process
- Communicates through well-defined APIs
- Can be deployed independently
- Owns its own database (database per service pattern)
- Can be written in different programming languages
- Is organized around business capabilities

### Key Characteristics

- **Single Responsibility**: Each service does one thing well
- **Autonomous**: Services can be developed, deployed, and scaled independently
- **Decentralized**: No central control; services make their own decisions
- **Resilient**: Failure in one service doesn't cascade to others
- **Observable**: Services expose metrics and logs for monitoring

## What is Event-Driven Architecture?

**Event-Driven Architecture (EDA)** is a software design pattern where services communicate by producing and consuming events. An event represents a significant change in state.

### Core Concepts

1. **Event**: A record of something that happened (e.g., "Todo Created", "Todo Deleted")
2. **Event Producer**: Service that publishes events when state changes occur
3. **Event Consumer**: Service that subscribes to and processes events
4. **Message Broker**: Intermediary that routes events from producers to consumers
5. **Asynchronous Communication**: Producers don't wait for consumers to process events

### Communication Pattern

```
[Producer Service] ---> [Message Broker] ---> [Consumer Service(s)]
                         (Redis Pub/Sub)
```

## How Microservices and EDA Fit Together

Microservices and Event-Driven Architecture are complementary patterns that work exceptionally well together, though neither requires the other. Understanding their relationship is key to building scalable, maintainable distributed systems.

### The Natural Synergy

**Microservices** solve the problem of **organizing code and teams**, while **Event-Driven Architecture** solves the problem of **service communication**.

```
┌─────────────────────────────────────────────────────────────────┐
│                     MICROSERVICES ARCHITECTURE                   │
│  (How to structure and organize your application)                │
│                                                                   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │  Service A  │  │  Service B  │  │  Service C  │             │
│  │  (Auth)     │  │  (Orders)   │  │  (Payment)  │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
│         │                 │                 │                    │
│         └─────────────────┼─────────────────┘                   │
│                           │                                      │
│                  How do they communicate?                        │
│                           │                                      │
│         ┌─────────────────▼─────────────────┐                   │
│         │   EVENT-DRIVEN ARCHITECTURE       │                   │
│         │   (How services communicate)      │                   │
│         │                                   │                   │
│         │     ┌─────────────────┐           │                   │
│         │     │ Message Broker  │           │                   │
│         │     │  (Event Bus)    │           │                   │
│         │     └─────────────────┘           │                   │
│         └───────────────────────────────────┘                   │
└─────────────────────────────────────────────────────────────────┘
```

### Communication Patterns in Microservices

When you adopt microservices, services need to communicate. You have several options:

#### 1. **Synchronous Communication (Request-Response)**

**Pattern**: Direct API calls using REST or gRPC

```
Service A ──HTTP/gRPC──> Service B
          <──Response───
```

**Characteristics**:

- ✅ Simple to understand and implement
- ✅ Immediate response and error handling
- ❌ Tight coupling - Service A must know about Service B
- ❌ Service A blocks waiting for Service B
- ❌ If Service B is down, Service A fails
- ❌ Cascading failures - problems propagate

**Example**:

```python
# Order Service directly calls Payment Service
response = await payment_service_client.post(
    "http://payment-service:8080/charge",
    json={"amount": 100, "user_id": 123}
)
if response.status_code == 200:
    # Continue with order...
```

#### 2. **Asynchronous Communication (Event-Driven)**

**Pattern**: Services communicate through events via a message broker

```
Service A ──Publish Event──> Message Broker ──Subscribe──> Service B
                                           └──Subscribe──> Service C
```

**Characteristics**:

- ✅ Loose coupling - Services don't know about each other
- ✅ Non-blocking - Service A continues immediately
- ✅ Multiple consumers can react to same event
- ✅ Service B can be down; events queue up
- ✅ Easy to add new consumers
- ❌ More complex infrastructure
- ❌ Eventual consistency
- ❌ Harder to debug

**Example**:

```python
# Order Service publishes event
await event_bus.publish(OrderCreatedEvent(
    order_id=order.id,
    user_id=123,
    amount=100
))
# Service continues immediately

# Payment Service (separate microservice) subscribes
@event_handler("ORDER_CREATED")
async def process_payment(event: OrderCreatedEvent):
    # Process payment asynchronously
```

### Why EDA is Ideal for Microservices

#### 1. **Decoupling Services**

**Without EDA** (Direct API Calls):

```
Order Service ──knows about──> Payment Service
              ──knows about──> Inventory Service
              ──knows about──> Notification Service
              ──knows about──> Analytics Service
```

If you add a new service (e.g., Fraud Detection), you must **modify Order Service**.

**With EDA** (Events):

```
Order Service ──publishes──> "OrderCreated" Event
                                    │
                    ┌───────────────┼───────────────┬──────────────┐
                    │               │               │              │
            Payment Service   Inventory      Notification    Analytics
                            Service         Service         Service
```

Adding Fraud Detection Service just means subscribing to "OrderCreated" - **no changes to Order Service**.

#### 2. **Independent Scaling**

Each microservice can scale independently based on its load:

```
Order Service (1 instance) ──> Event Bus ──> Payment Service (5 instances)
                                        └──> Email Service (2 instances)
```

Payment processing might need more resources than email sending. With EDA, scale only what you need.

#### 3. **Temporal Decoupling**

Services don't need to be online simultaneously:

- Order Service publishes "OrderCreated" at 2 PM
- Payment Service comes online at 2:30 PM
- Payment Service processes the queued event (if using persistent queue)

This is impossible with synchronous REST calls.

#### 4. **Failure Isolation**

**Synchronous**:

```
Order Service → Payment Service (DOWN) → ❌ Order fails
```

**Event-Driven**:

```
Order Service → Event Bus → ✅ Order succeeds
                         → Payment Service (DOWN)
                         → Event queued, processed later
```

### When to Combine Both Patterns

A mature microservices architecture often uses **both** patterns strategically:

#### Use **Synchronous (REST/gRPC)** for:

1. **Queries**: Getting current data

   ```python
   user = await user_service.get_user(user_id)  # Need result now
   ```

2. **Commands requiring immediate feedback**:

   ```python
   result = await payment_service.charge(card_info)
   if result.success:
       show_success_message()
   else:
       show_error_message()  # User needs to know NOW
   ```

3. **Services that must succeed together** (Distributed Transaction):
   ```python
   # Reserve inventory and charge payment atomically
   # Use 2-phase commit or Saga pattern
   ```

#### Use **Asynchronous (EDA)** for:

1. **Fire-and-forget operations**:

   ```python
   # Send welcome email - don't wait
   await events.publish(UserRegisteredEvent(user_id=user.id))
   ```

2. **Fan-out scenarios** (one event, many reactions):

   ```python
   # Order created → inventory, payment, shipping, analytics
   await events.publish(OrderCreatedEvent(...))
   ```

3. **Cross-boundary communications**:

   ```python
   # Between different bounded contexts or teams
   await events.publish(InvoiceGeneratedEvent(...))
   ```

4. **Long-running workflows**:
   ```python
   # Saga pattern for multi-step processes
   # Step 1: Reserve inventory (event)
   # Step 2: Charge payment (event)
   # Step 3: Ship order (event)
   ```

### Real-World Example: E-commerce Order

**Hybrid Approach** (Synchronous + Asynchronous):

```python
@app.post("/orders")
async def create_order(order_data: OrderCreate):
    # 1. Synchronous: Check inventory (need immediate answer)
    inventory = await inventory_service.check_availability(order_data.items)
    if not inventory.available:
        raise HTTPException(400, "Items not available")

    # 2. Synchronous: Validate payment method (need immediate answer)
    payment_valid = await payment_service.validate_payment_method(
        order_data.payment_info
    )
    if not payment_valid:
        raise HTTPException(400, "Invalid payment method")

    # 3. Create order in database
    order = await db.create_order(order_data)

    # 4. Asynchronous: Publish event (don't wait for these)
    await event_bus.publish(OrderCreatedEvent(
        order_id=order.id,
        user_id=order_data.user_id,
        items=order_data.items,
        amount=order.total_amount
    ))

    # 5. Return immediately to user
    return {"order_id": order.id, "status": "processing"}

# Separate microservices react asynchronously:

# Payment Service
@subscribe("ORDER_CREATED")
async def charge_payment(event: OrderCreatedEvent):
    await process_payment(event.order_id, event.amount)

# Inventory Service
@subscribe("ORDER_CREATED")
async def reserve_inventory(event: OrderCreatedEvent):
    await reserve_items(event.items)

# Notification Service
@subscribe("ORDER_CREATED")
async def send_confirmation(event: OrderCreatedEvent):
    await send_email(event.user_id, "Order confirmed")

# Analytics Service
@subscribe("ORDER_CREATED")
async def track_order(event: OrderCreatedEvent):
    await record_analytics(event)
```

### The Spectrum: Choosing Your Approach

```
Monolith ──────> Microservices ──────> Microservices + EDA
                 (Sync REST)           (Async Events)

Simple          Medium                 High
Complexity      Complexity             Complexity

Low             Medium                 High
Scalability     Scalability            Scalability

Tight           Some                   Loose
Coupling        Coupling               Coupling

Best for        Best for               Best for
Small Teams     Medium Systems         Large, Complex Systems
```

### Key Takeaway

**Microservices** answer: "How should I organize my application?"

- Break it into small, independent services

**EDA** answers: "How should my services communicate?"

- Use events for loose coupling and scalability

**Together** they provide:

- Organizational independence (microservices)
- Technical independence (EDA)
- Team autonomy (both)
- Scalability (both)
- Resilience (both)

You can have microservices without EDA (using REST), and you can have EDA in a monolith (internal event bus), but combining them gives you the most flexibility for building large-scale distributed systems.

## Pros and Cons

### Advantages ✅

#### Event-Driven Architecture

1. **Loose Coupling**: Services don't need to know about each other
2. **Scalability**: Consumers can be scaled independently based on load
3. **Flexibility**: Easy to add new consumers without modifying producers
4. **Resilience**: If a consumer fails, events can be queued or replayed
5. **Real-time Processing**: Events are processed as they happen
6. **Audit Trail**: Events naturally create a log of all system changes
7. **Temporal Decoupling**: Producers and consumers don't need to be online simultaneously

#### Microservices

1. **Independent Deployment**: Deploy services without affecting others
2. **Technology Diversity**: Use the best tool for each job
3. **Team Autonomy**: Teams can work independently on different services
4. **Fault Isolation**: Failures are contained to individual services
5. **Scalability**: Scale only the services that need it

### Disadvantages ❌

#### Event-Driven Architecture

1. **Complexity**: More moving parts to manage and monitor
2. **Eventual Consistency**: Data may be temporarily inconsistent across services
3. **Debugging Difficulty**: Harder to trace request flows across services
4. **Message Broker Dependency**: Broker becomes a critical point of failure
5. **Event Schema Evolution**: Changes to event structure require coordination
6. **Duplicate Processing**: Requires idempotency to handle message redelivery
7. **No Immediate Response**: Asynchronous nature means no instant feedback

#### Microservices

1. **Operational Overhead**: More services to deploy, monitor, and maintain
2. **Network Latency**: Inter-service communication over network is slower
3. **Data Consistency**: Distributed transactions are complex
4. **Testing Complexity**: Integration testing requires multiple services
5. **Deployment Coordination**: Changes spanning multiple services need orchestration

## When to Use EDA

### ✅ Good Use Cases

1. **Event Sourcing Requirements**: Need to maintain a complete audit log
2. **Multiple Independent Reactions**: Many services need to react to the same event
3. **High Scalability Needs**: Need to scale different parts independently
4. **Real-time Notifications**: Users need immediate updates (via WebSocket consumers)
5. **Integration with External Systems**: Third-party services need event notifications
6. **Complex Workflows**: Multi-step processes where steps can fail independently
7. **Analytics and Reporting**: Separate service processes events for analytics
8. **Decoupled Services**: Services should not have direct dependencies

### Example Scenarios

- **E-commerce**: Order created → Inventory service, Payment service, Shipping service all react
- **Social Media**: Post created → Notification service, Feed service, Analytics service react
- **IoT Systems**: Sensor data → Multiple services process data independently
- **Financial Systems**: Transaction occurred → Fraud detection, Accounting, Reporting services react

### ❌ When NOT to Use EDA

1. **Simple CRUD Applications**: Direct API calls are simpler and sufficient
2. **Strong Consistency Required**: Financial transactions needing immediate consistency
3. **Low Latency Critical**: Real-time gaming where milliseconds matter
4. **Small Team/Project**: Overhead outweighs benefits for simple applications
5. **Limited Resources**: Insufficient infrastructure for message brokers and monitoring
6. **Simple Linear Workflows**: When A calls B calls C in a straightforward sequence
7. **Tight Coupling Acceptable**: Internal monolith modules that change together

### Better Alternatives

- **Monolithic Architecture**: For simple applications or small teams
- **Synchronous REST/gRPC**: When immediate responses are needed
- **Request-Response Pattern**: When operations are sequential and dependent
- **Direct Database Access**: For tightly coupled components in a monolith

## Architecture

### System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        Client/User                           │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ HTTP Requests
                         │
         ┌───────────────▼──────────────┐
         │   Todo Service (Producer)     │
         │   Port: 8000                  │
         │                               │
         │  ┌─────────────────────────┐  │
         │  │  REST API Endpoints     │  │
         │  │  POST /todos/           │  │
         │  │  DELETE /todos/{id}     │  │
         │  └─────────────────────────┘  │
         │                               │
         │  ┌─────────────────────────┐  │
         │  │  Business Logic         │  │
         │  │  - Create Todo          │  │
         │  │  - Delete Todo          │  │
         │  └─────────────────────────┘  │
         │                               │
         │  ┌─────────────────────────┐  │
         │  │  Event Publisher        │  │
         │  │  - TodoCreatedEvent     │  │
         │  │  - TodoDeletedEvent     │  │
         │  └─────────────────────────┘  │
         │                               │
         │  ┌─────────────────────────┐  │
         │  │  Database: todos.db     │  │
         │  │  (SQLite)               │  │
         │  └─────────────────────────┘  │
         └───────────────┬───────────────┘
                         │
                         │ Publish Events
                         │
         ┌───────────────▼───────────────┐
         │   Redis Pub/Sub Broker        │
         │   Channel: "todo_events"      │
         │   Port: 6379                  │
         └───────────────┬───────────────┘
                         │
                         │ Subscribe to Events
                         │
         ┌───────────────▼──────────────┐
         │   Audit Service (Consumer)    │
         │   Port: 8001                  │
         │                               │
         │  ┌─────────────────────────┐  │
         │  │  Event Subscriber       │  │
         │  │  (Background Task)      │  │
         │  │  - Listen for Events    │  │
         │  └─────────────────────────┘  │
         │                               │
         │  ┌─────────────────────────┐  │
         │  │  Business Logic         │  │
         │  │  - Record Audit Log     │  │
         │  └─────────────────────────┘  │
         │                               │
         │  ┌─────────────────────────┐  │
         │  │  REST API Endpoints     │  │
         │  │  GET /audit/            │  │
         │  └─────────────────────────┘  │
         │                               │
         │  ┌─────────────────────────┐  │
         │  │  Database: audit.db     │  │
         │  │  (SQLite)               │  │
         │  └─────────────────────────┘  │
         └───────────────────────────────┘
```

### Event Flow

1. **Client** sends HTTP POST request to create a todo
2. **Todo Service** validates and stores the todo in its database
3. **Todo Service** publishes a `TodoCreatedEvent` to Redis
4. **Redis** broadcasts the event to all subscribers
5. **Audit Service** receives the event through its subscriber
6. **Audit Service** creates an audit log entry in its database
7. **Client** can query audit logs via GET /audit/

### Key Design Patterns

- **Database Per Service**: Each service has its own database
- **Event Sourcing**: Changes are captured as events
- **Saga Pattern**: Distributed transactions through events (implicit)
- **CQRS (Command Query Responsibility Segregation)**: Separate write (Todo) and read (Audit) models

## Project Structure

```
python/
├── services/
│   ├── todo_service/              # Producer Service
│   │   ├── app/
│   │   │   ├── broker/
│   │   │   │   └── publisher.py   # Publishes events to Redis
│   │   │   ├── database.py        # Database configuration
│   │   │   ├── models.py          # SQLAlchemy ORM models
│   │   │   ├── router.py          # FastAPI route handlers
│   │   │   ├── schemas.py         # Pydantic request/response models
│   │   │   └── service.py         # Business logic
│   │   └── main.py                # Application entry point
│   │
│   └── audit_service/             # Consumer Service
│       ├── app/
│       │   ├── broker/
│       │   │   └── subscriber.py  # Subscribes to Redis events
│       │   ├── database.py        # Database configuration
│       │   ├── models.py          # SQLAlchemy ORM models
│       │   └── service.py         # Business logic
│       └── main.py                # Application entry point
│
├── shared/
│   └── events.py                  # Shared event definitions
│
├── pyproject.toml                 # Python dependencies
├── todos.db                       # Todo Service database
└── audit.db                       # Audit Service database
```

## Implementation Details

### 1. Event Definitions (`shared/events.py`)

All events inherit from `BaseEvent` and use Pydantic for validation:

```python
class TodoCreatedEvent(BaseEvent):
    event_type: str = "TODO_CREATED"
    todo_id: UUID
    title: str
    description: str | None = None
```

### 2. Event Publisher (`todo_service/app/broker/publisher.py`)

The Todo Service publishes events to Redis Pub/Sub:

```python
class EventPublisher:
    @staticmethod
    async def publish(event: BaseEvent) -> None:
        client = await aioredis.from_url(REDIS_URL)
        await client.publish(CHANNEL_NAME, event.model_dump_json())
        await client.aclose()
```

**Design Decisions:**

- Uses async Redis client for non-blocking I/O
- Serializes events to JSON for interoperability
- Creates new connection per publish (suitable for low throughput)
- Error handling prevents service disruption

### 3. Event Subscriber (`audit_service/app/broker/subscriber.py`)

The Audit Service runs a background task that continuously listens for events:

```python
async def start_event_subscriber():
    client = aioredis.from_url(REDIS_URL)
    pubsub = client.pubsub()
    await pubsub.subscribe(CHANNEL_NAME)

    async for message in pubsub.listen():
        # Process event and create audit log
```

**Design Decisions:**

- Runs as a FastAPI lifespan task
- Creates isolated database session per event (transaction per message)
- Graceful shutdown on cancellation
- Prints processing status for observability

### 4. Service Independence

Each service:

- Has its own database (SQLite for simplicity)
- Can be deployed independently
- Has no direct dependency on the other service
- Uses shared event definitions only

### 5. Database Per Service Pattern

- **Todo Service**: `todos.db` - Stores todo items
- **Audit Service**: `audit.db` - Stores audit logs

This ensures:

- Data isolation
- Independent scaling
- Service autonomy
- No shared database bottlenecks

## Prerequisites

- **Python**: 3.14 or higher
- **Redis**: Running instance (default port 6379)
- **Package Manager**: uv, pip, or poetry

## Installation

### 1. Install Dependencies

Using `uv` (recommended):

```bash
uv sync
```

Using `pip`:

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install fastapi uvicorn sqlalchemy redis pydantic httpx
```

### 2. Start Redis

**Using Docker:**

```bash
docker run -d -p 6379:6379 redis:latest
```

**Using Homebrew (macOS):**

```bash
brew install redis
brew services start redis
```

**Using apt (Ubuntu/Debian):**

```bash
sudo apt update
sudo apt install redis-server
sudo systemctl start redis
```

Verify Redis is running:

```bash
redis-cli ping
# Should return: PONG
```

## Running the Application

### Option 1: Run Services in Separate Terminals

**Terminal 1 - Todo Service (Producer):**

```bash
uvicorn services.todo_service.main:app --reload --port 8000
```

**Terminal 2 - Audit Service (Consumer):**

```bash
uvicorn services.audit_service.main:app --reload --port 8001
```

### Option 2: Run with Background Processes

```bash
# Start Todo Service
uvicorn services.todo_service.main:app --port 8000 &

# Start Audit Service
uvicorn services.audit_service.main:app --port 8001 &
```

### Verify Services are Running

```bash
# Check Todo Service
curl http://localhost:8000/docs

# Check Audit Service
curl http://localhost:8001/docs
```

## API Documentation

### Todo Service (Port 8000)

#### Create Todo

```http
POST /todos/
Content-Type: application/json

{
  "title": "Learn Event-Driven Architecture",
  "description": "Study EDA patterns and implementations"
}
```

**Response (201 Created):**

```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "title": "Learn Event-Driven Architecture",
  "description": "Study EDA patterns and implementations",
  "completed": false
}
```

#### Delete Todo

```http
DELETE /todos/{todo_id}
```

**Response: 204 No Content**

### Audit Service (Port 8001)

#### List All Audit Logs

```http
GET /audit/
```

**Response (200 OK):**

```json
[
  {
    "id": "789e4567-e89b-12d3-a456-426614174000",
    "event_type": "TODO_CREATED",
    "resource_id": "123e4567-e89b-12d3-a456-426614174000",
    "message": "New Todo created: 'Learn Event-Driven Architecture'",
    "created_at": "2026-09-25T10:30:00.000Z"
  },
  {
    "id": "456e4567-e89b-12d3-a456-426614174000",
    "event_type": "TODO_DELETED",
    "resource_id": "123e4567-e89b-12d3-a456-426614174000",
    "message": "Todo item deleted: ID 123e4567-e89b-12d3-a456-426614174000",
    "created_at": "2026-09-25T10:35:00.000Z"
  }
]
```

### Interactive API Documentation

- **Todo Service**: http://localhost:8000/docs
- **Audit Service**: http://localhost:8001/docs

## Testing the System

### 1. Create a Todo

```bash
curl -X POST http://localhost:8000/todos/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Todo",
    "description": "Testing EDA implementation"
  }'
```

Expected output:

```json
{
  "id": "abc123...",
  "title": "Test Todo",
  "description": "Testing EDA implementation",
  "completed": false
}
```

### 2. Check Audit Logs

```bash
curl http://localhost:8001/audit/
```

You should see an audit entry for the created todo:

```json
[
  {
    "event_type": "TODO_CREATED",
    "resource_id": "abc123...",
    "message": "New Todo created: 'Test Todo'",
    ...
  }
]
```

### 3. Delete the Todo

```bash
curl -X DELETE http://localhost:8000/todos/abc123...
```

### 4. Verify Audit Log Updated

```bash
curl http://localhost:8001/audit/
```

You should now see both CREATE and DELETE audit entries.

### 5. Monitor Event Processing

Watch the Audit Service terminal to see real-time event consumption:

```
[*] Audit Service worker subscribed to 'todo_events'...
[EVENT CONSUMED] Created Audit record for Todo ID abc123...
[EVENT CONSUMED] Created Audit record for deleted Todo ID abc123...
```

## Key Learning Points

1. **Asynchronous Communication**: Todo Service doesn't wait for Audit Service
2. **Loose Coupling**: Services communicate through events, not direct API calls
3. **Service Independence**: Each service can be deployed and scaled separately
4. **Event as Source of Truth**: Events capture what happened in the system
5. **Eventual Consistency**: Audit logs are eventually consistent with todo operations
6. **Resilience**: If Audit Service is down, Todo Service continues operating
7. **Extensibility**: Easy to add new consumers (e.g., Notification Service) without changing producers

## Production Considerations

### What's Missing for Production

1. **Message Durability**: Use Redis Streams or RabbitMQ/Kafka for guaranteed delivery
2. **Error Handling**: Dead letter queues for failed event processing
3. **Idempotency**: Handle duplicate events gracefully
4. **Monitoring**: Add metrics, tracing, and structured logging
5. **Authentication**: Add API authentication and authorization
6. **Rate Limiting**: Protect services from overload
7. **Health Checks**: Implement readiness and liveness probes
8. **Connection Pooling**: Reuse Redis connections instead of creating per publish
9. **Schema Registry**: Version and validate event schemas
10. **Testing**: Unit tests, integration tests, and contract tests

### Recommended Improvements

```python
# Use Redis connection pool
class EventPublisher:
    _pool = None

    @classmethod
    async def get_pool(cls):
        if cls._pool is None:
            cls._pool = aioredis.ConnectionPool.from_url(REDIS_URL)
        return cls._pool
```

```python
# Add idempotency for event processing
def process_event(event_id, event_data):
    if already_processed(event_id):
        return  # Skip duplicate
    # Process event...
    mark_as_processed(event_id)
```

## Troubleshooting

### Redis Connection Error

**Error**: `ConnectionRefusedError: [Errno 111] Connection refused`

**Solution**: Ensure Redis is running:

```bash
redis-cli ping
```

### Events Not Being Consumed

**Check**:

1. Both services are running
2. Services are connected to the same Redis instance
3. Check Audit Service logs for errors
4. Verify channel name matches in both services

### Port Already in Use

**Error**: `OSError: [Errno 48] Address already in use`

**Solution**: Use different ports or kill existing process:

```bash
lsof -ti:8000 | xargs kill -9
lsof -ti:8001 | xargs kill -9
```

## Further Reading

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Redis Pub/Sub](https://redis.io/docs/manual/pubsub/)
- [Event-Driven Architecture Patterns](https://martinfowler.com/articles/201701-event-driven.html)
- [Microservices Patterns](https://microservices.io/patterns/index.html)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/en/20/orm/)

## License

MIT License - Feel free to use this for learning and experimentation.

## Contributing

This is an educational project. Feel free to fork and experiment with:

- Adding new event types
- Implementing new consumer services (e.g., Notification Service)
- Adding retry mechanisms
- Implementing event sourcing patterns
- Converting to use Kafka or RabbitMQ

---

**Happy Learning! 🚀**
