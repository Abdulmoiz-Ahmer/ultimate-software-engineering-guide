# Todo Microservices - Python Implementation

## What Are Microservices?

**Microservices** is an architectural pattern where an application is structured as a collection of loosely coupled, independently deployable services. Each service:

- Focuses on a single business capability
- Runs in its own process
- Communicates via well-defined APIs (typically HTTP/REST or message queues)
- Can be developed, deployed, and scaled independently
- May use different technology stacks

### Microservices vs Monolithic Architecture

| Aspect | Monolithic | Microservices |
|--------|-----------|---------------|
| **Structure** | Single codebase | Multiple services |
| **Deployment** | Deploy entire application | Deploy services independently |
| **Scaling** | Scale entire application | Scale individual services |
| **Technology** | Single stack | Polyglot (multiple stacks) |
| **Development** | Single team or coordinated teams | Autonomous teams per service |
| **Failure Impact** | Entire app goes down | Only affected service fails |
| **Complexity** | Simpler initially | Higher operational complexity |

## When to Use Microservices?

### ✅ Good Fit For:

- **Large applications** with distinct business domains
- **High-traffic systems** requiring independent scaling
- **Teams** wanting autonomy and parallel development
- **Applications** with varying technology requirements
- **Systems** needing resilience to partial failures
- **Organizations** practicing DevOps and CI/CD

### ❌ Not Ideal For:

- Small applications with simple requirements
- Startups in early MVP stage
- Teams without strong DevOps culture
- Projects with tight coupling between features
- Organizations without container/orchestration infrastructure

## How This Example Works

This repository demonstrates a simple microservices architecture with two services:

### 1. Todo Service (Port 8000)
**Responsibility**: Manage todo items

- Create new todos
- Delete todos
- Store todo data in its own database

### 2. Audit Service (Port 8001)
**Responsibility**: Centralized audit logging

- Receive audit events from other services
- Store audit logs with timestamps
- Provide audit history

### Communication Flow

```
┌──────────────┐         ┌──────────────┐
│              │         │              │
│    Client    │────────▶│ Todo Service │
│              │  HTTP   │  (Port 8000) │
└──────────────┘         └──────┬───────┘
                                │
                                │ HTTP POST
                                │ (Audit Event)
                                ▼
                         ┌──────────────┐
                         │              │
                         │Audit Service │
                         │ (Port 8001)  │
                         └──────────────┘

Each service has its own database:
- Todo Service → todos.db
- Audit Service → audit.db
```

## Key Microservices Patterns Demonstrated

### 1. Service Independence
Each service has its own:
- Codebase and repository structure
- Database (separate SQLite files)
- API endpoints
- Dependencies and configuration

### 2. Inter-Service Communication
Services communicate via HTTP REST APIs:
- **Synchronous**: Todo service directly calls Audit service
- **Fail-Safe**: If Audit service is down, Todo operations still succeed

### 3. Database Per Service
Each service owns its data:
- Todo service: `todos.db`
- Audit service: `audit.db`
- No direct database sharing between services

### 4. API Gateway Pattern (Not Implemented Yet)
In production, you'd typically add:
- API Gateway as single entry point
- Authentication/Authorization
- Rate limiting
- Request routing

### 5. Event-Driven Architecture (Future Enhancement)
Current: Synchronous HTTP calls
Better: Asynchronous message queue (RabbitMQ, Kafka)

## Project Structure

```
services/
├── todo_service/              # Todo management microservice
│   ├── app/
│   │   ├── clients/
│   │   │   └── audit_client.py    # HTTP client for Audit service
│   │   ├── database.py            # Database configuration
│   │   ├── models.py              # ORM models
│   │   ├── router.py              # API endpoints
│   │   ├── schemas.py             # Request/response schemas
│   │   └── service.py             # Business logic
│   ├── alembic/                   # Database migrations
│   ├── main.py                    # Entry point
│   ├── pyproject.toml             # Dependencies
│   ├── todos.db                   # SQLite database
│   └── README.md                  # Service documentation
│
├── audit_service/             # Audit logging microservice
│   ├── app/
│   │   ├── database.py            # Database configuration
│   │   ├── models.py              # ORM models
│   │   ├── router.py              # API endpoints
│   │   ├── schemas.py             # Request/response schemas
│   │   └── service.py             # Business logic
│   ├── alembic/                   # Database migrations
│   ├── main.py                    # Entry point
│   ├── pyproject.toml             # Dependencies
│   ├── audit.db                   # SQLite database
│   └── README.md                  # Service documentation
│
└── README.md                  # This file
```

## Getting Started

### Prerequisites

- Python 3.14+
- uv package manager ([installation guide](https://docs.astral.sh/uv/))

### Installation

```bash
# Install dependencies for both services
cd todo_service && uv sync && cd ..
cd audit_service && uv sync && cd ..
```

### Running the Services

Open **two terminal windows**:

**Terminal 1 - Audit Service:**
```bash
cd audit_service
uv run uvicorn audit_service.main:app --reload --port 8001
```

**Terminal 2 - Todo Service:**
```bash
cd todo_service
uv run uvicorn todo_service.main:app --reload --port 8000
```

### Testing the System

```bash
# 1. Create a todo (this will also create an audit log)
curl -X POST http://localhost:8000/todos/ \
  -H "Content-Type: application/json" \
  -d '{"title":"Buy groceries","description":"Milk, eggs, bread"}'

# Response will include the todo ID, e.g., "id": "123e4567-..."

# 2. View audit logs
curl http://localhost:8001/audit/

# 3. Delete the todo (this will also create an audit log)
curl -X DELETE http://localhost:8000/todos/{todo-id}

# 4. View audit logs again to see both events
curl http://localhost:8001/audit/
```

## Advantages of This Architecture

### 1. **Independent Deployment**
- Deploy Todo service without touching Audit service
- Roll back individual services if issues arise
- Zero-downtime deployments per service

### 2. **Independent Scaling**
- Scale Todo service horizontally if it receives more traffic
- Keep Audit service at minimal resources if log volume is low
- Optimize resources based on actual usage

### 3. **Technology Freedom**
- Todo service uses FastAPI (Python)
- Future services could use Node.js, Go, Java, etc.
- Choose the best tool for each job

### 4. **Fault Isolation**
- If Audit service crashes, todos still work
- Failures are contained to individual services
- System remains partially operational

### 5. **Team Autonomy**
- Separate teams can own separate services
- Parallel development without merge conflicts
- Clear ownership and responsibility

### 6. **Easier Understanding**
- Each service is smaller and focused
- New developers can understand one service at a time
- Reduced cognitive load

## Challenges and Considerations

### 1. **Increased Complexity**
- **Challenge**: More moving parts to manage
- **Solution**: Use container orchestration (Docker, Kubernetes)

### 2. **Network Latency**
- **Challenge**: Inter-service calls over network
- **Solution**: Async messaging, caching, service mesh

### 3. **Data Consistency**
- **Challenge**: No ACID transactions across services
- **Solution**: Eventual consistency, saga pattern

### 4. **Debugging Difficulty**
- **Challenge**: Tracing requests across services
- **Solution**: Distributed tracing (Jaeger, Zipkin)

### 5. **Deployment Overhead**
- **Challenge**: Managing multiple deployments
- **Solution**: CI/CD pipelines, infrastructure as code

### 6. **Testing Complexity**
- **Challenge**: Integration testing across services
- **Solution**: Contract testing, service virtualization

## Best Practices Applied

### 1. **Single Responsibility**
Each service has one clear purpose:
- Todo service: Manage todos
- Audit service: Log events

### 2. **Database Per Service**
No shared databases:
- `todos.db` for Todo service
- `audit.db` for Audit service

### 3. **API Versioning**
Prepare for breaking changes:
- Use `/v1/todos/` for version 1
- Maintain backwards compatibility

### 4. **Health Checks**
Monitor service availability:
- Implement `/health` endpoints
- Use for load balancer routing

### 5. **Graceful Degradation**
Handle service failures:
- Todo service works even if Audit is down
- Log warnings instead of throwing errors

### 6. **Configuration Management**
Externalize configuration:
- Use environment variables
- Separate dev/staging/prod configs

## Evolution Path

### Phase 1: Current Implementation ✅
- Two services with HTTP communication
- Synchronous calls
- SQLite databases

### Phase 2: Production Ready
- [ ] Add API Gateway (Kong, Nginx)
- [ ] Implement authentication/authorization
- [ ] Add health check endpoints
- [ ] Set up logging and monitoring
- [ ] Use PostgreSQL instead of SQLite

### Phase 3: Advanced Patterns
- [ ] Replace HTTP with message queue (RabbitMQ/Kafka)
- [ ] Implement event sourcing
- [ ] Add service mesh (Istio, Linkerd)
- [ ] Implement circuit breakers
- [ ] Add distributed tracing

### Phase 4: Cloud Native
- [ ] Containerize with Docker
- [ ] Orchestrate with Kubernetes
- [ ] Auto-scaling based on metrics
- [ ] Multi-region deployment
- [ ] Disaster recovery

## Related Patterns

### Service Mesh
Network layer for service-to-service communication:
- Traffic management
- Security (mTLS)
- Observability
- **Examples**: Istio, Linkerd, Consul

### Circuit Breaker
Prevent cascading failures:
- Fast fail when service is down
- Automatic recovery detection
- **Libraries**: Hystrix, resilience4j

### API Gateway
Single entry point for clients:
- Request routing
- Authentication
- Rate limiting
- **Examples**: Kong, AWS API Gateway, Nginx

### Event Sourcing
Store state changes as events:
- Complete audit trail
- Time travel (replay events)
- **Tools**: EventStore, Kafka

## Resources for Learning More

### Books
- "Building Microservices" by Sam Newman
- "Microservices Patterns" by Chris Richardson
- "The Phoenix Project" by Gene Kim

### Online Resources
- [Microservices.io](https://microservices.io/) - Pattern catalog
- [Martin Fowler's Microservices Guide](https://martinfowler.com/microservices/)
- [CNCF Landscape](https://landscape.cncf.io/) - Tools ecosystem

### Technologies to Explore
- **Containers**: Docker, containerd
- **Orchestration**: Kubernetes, Docker Swarm
- **Service Mesh**: Istio, Linkerd
- **Message Queues**: RabbitMQ, Apache Kafka
- **API Gateway**: Kong, Tyk, AWS API Gateway
- **Monitoring**: Prometheus, Grafana, ELK Stack
- **Tracing**: Jaeger, Zipkin, OpenTelemetry

## Contributing

To add new services:

1. Create a new directory under `services/`
2. Follow the same structure as existing services
3. Update this README with service description
4. Document inter-service dependencies

## License

This is an educational example. Use freely for learning purposes.

---

**Remember**: Microservices are a tool, not a goal. Start with a monolith and split into microservices when you have clear boundaries and organizational need. Premature distribution adds complexity without benefits.
