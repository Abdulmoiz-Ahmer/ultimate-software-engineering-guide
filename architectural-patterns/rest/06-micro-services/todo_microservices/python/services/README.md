# Todo Microservices - Python Implementation

## Table of Contents

- [What Are Microservices?](#what-are-microservices)
- [Microservices Architecture Fundamentals](#microservices-architecture-fundamentals)
- [Pros and Cons](#pros-and-cons)
- [When to Use Microservices](#when-to-use-microservices)
- [When NOT to Use Microservices](#when-not-to-use-microservices)
- [About This Example](#about-this-example)
- [Getting Started](#getting-started)
- [Key Patterns Demonstrated](#key-patterns-demonstrated)
- [Best Practices](#best-practices)
- [Evolution Path](#evolution-path)
- [Resources](#resources)

---

## What Are Microservices?

**Microservices** is an architectural pattern where an application is decomposed into a collection of small, autonomous services. Each service:

- **Focuses on a single business capability** (e.g., user management, payment processing, notifications)
- **Runs in its own process** with independent deployment lifecycle
- **Communicates via well-defined APIs** (REST, gRPC, message queues)
- **Owns its own data** (database per service)
- **Can be developed, deployed, and scaled independently**
- **May use different technology stacks** (polyglot architecture)

### Microservices vs Monolithic Architecture

| Aspect                 | Monolithic                                       | Microservices                                      |
| ---------------------- | ------------------------------------------------ | -------------------------------------------------- |
| **Structure**          | Single unified codebase                          | Collection of independent services                 |
| **Deployment**         | Deploy entire application as one unit            | Deploy services independently                      |
| **Scaling**            | Scale entire application vertically/horizontally | Scale individual services based on demand          |
| **Technology**         | Single technology stack                          | Polyglot (mix of languages, databases, frameworks) |
| **Development**        | Single or coordinated teams                      | Autonomous teams per service                       |
| **Failure Impact**     | Single point of failure affects entire app       | Failures isolated to individual services           |
| **Testing**            | Simpler integration testing                      | Complex distributed testing                        |
| **Data Management**    | Single shared database                           | Database per service                               |
| **Deployment Speed**   | Slower (entire app must be deployed)             | Faster (only changed services deployed)            |
| **Initial Complexity** | Lower                                            | Higher (distributed system overhead)               |

---

## Microservices Architecture Fundamentals

### Core Principles

1. **Single Responsibility Principle**
   - Each service does one thing and does it well
   - Clear boundaries aligned with business capabilities

2. **Autonomy**
   - Services are loosely coupled
   - Can be changed, deployed, and scaled independently
   - Teams have full ownership (code to production)

3. **Decentralized Data Management**
   - Each service owns its data store
   - No direct database sharing between services
   - Data consistency via eventual consistency patterns

4. **Resilience by Design**
   - Services must handle failures gracefully
   - Circuit breakers, timeouts, and retries
   - System degrades gracefully, not catastrophically

5. **API-First Design**
   - Services communicate only through well-defined contracts
   - Versioned APIs for backward compatibility
   - Documentation as a first-class artifact

### Communication Patterns

**Synchronous Communication:**

- REST APIs over HTTP/HTTPS
- gRPC for high-performance scenarios
- GraphQL for flexible querying

**Asynchronous Communication:**

- Message queues (RabbitMQ, Amazon SQS)
- Event streaming (Apache Kafka, AWS Kinesis)
- Pub/Sub patterns for loose coupling

---

## Pros and Cons

### Advantages

#### 1. **Independent Deployment and Scaling**

- Deploy individual services without affecting others
- Scale only the services that need more resources
- Faster release cycles (deploy daily or hourly)
- **Example**: Scale the payment service 10x during Black Friday while keeping other services unchanged

#### 2. **Technology Flexibility**

- Choose the best tool for each job
- Experiment with new technologies in isolated services
- Gradually migrate from legacy tech stack
- **Example**: Use Python for data processing, Go for high-performance APIs, Node.js for real-time features

#### 3. **Team Autonomy and Productivity**

- Small, focused teams own complete services
- Parallel development without coordination overhead
- Clear ownership and accountability
- Faster onboarding (smaller codebases)

#### 4. **Fault Isolation and Resilience**

- Failures contained to individual services
- System remains partially operational during failures
- Easier to implement fault tolerance patterns
- **Example**: If the recommendation service fails, users can still browse and purchase

#### 5. **Better Alignment with Business**

- Services map to business capabilities
- Easier to understand and modify business logic
- Domain experts can work with specific services
- Clear cost attribution per business capability

#### 6. **Optimized Resource Usage**

- Run services on hardware suited to their needs
- Scale expensive operations independently
- Turn off unused services in development/testing

### Disadvantages

#### 1. **Increased Operational Complexity**

- Managing dozens or hundreds of services
- Need for sophisticated deployment pipelines
- Monitoring and logging across distributed system
- **Mitigation**: Kubernetes, service mesh, centralized observability

#### 2. **Network Latency and Reliability**

- Inter-service communication over network (slower than in-process calls)
- Network failures become application failures
- Need for timeout, retry, and circuit breaker patterns
- **Impact**: 5-10ms per network hop adds up quickly

#### 3. **Data Consistency Challenges**

- No distributed ACID transactions across services
- Eventual consistency requires careful design
- Complex queries spanning multiple services
- **Mitigation**: Saga pattern, event sourcing, CQRS

#### 4. **Testing Complexity**

- Integration testing requires running multiple services
- End-to-end testing is complex and slow
- Need for contract testing and service mocking
- **Overhead**: Test environments require significant infrastructure

#### 5. **Debugging and Troubleshooting Difficulty**

- Errors span multiple services and logs
- Request tracing across services is essential
- Root cause analysis more complex
- **Mitigation**: Distributed tracing (Jaeger, Zipkin), correlation IDs

#### 6. **Deployment Overhead**

- More moving parts to deploy and manage
- Versioning and compatibility management
- Database schema migrations per service
- **Mitigation**: GitOps, infrastructure as code, automated CI/CD

#### 7. **Initial Development Slowdown**

- Setting up infrastructure takes time
- Boilerplate code for each service
- More upfront architectural decisions
- **Reality Check**: First feature may take 2-3x longer than in a monolith

#### 8. **Organizational Prerequisites**

- Requires DevOps culture and automation
- Need for skilled developers comfortable with distributed systems
- Strong communication and documentation practices
- Cross-functional teams (dev, ops, security)

---

## When to Use Microservices

### Strong Indicators for Microservices

#### 1. **Large, Complex Applications**

- Application has multiple distinct business domains
- Codebase is large (>100K lines of code)
- Many teams working on the same application
- **Example**: E-commerce platform with catalog, cart, payment, shipping, inventory

#### 2. **Different Scalability Requirements**

- Some features need to scale independently
- Clear hot spots in the application
- Cost optimization is important
- **Example**: Search service needs 20 instances, admin panel needs 1

#### 3. **Polyglot Requirements**

- Different problems benefit from different technologies
- Need to leverage specialized tools or libraries
- Legacy systems integration
- **Example**: ML recommendations in Python, real-time chat in Go, admin in Java

#### 4. **Mature DevOps Organization**

- Strong CI/CD pipelines in place
- Infrastructure automation (Terraform, CloudFormation)
- Comprehensive monitoring and alerting
- Team comfortable with distributed systems

#### 5. **Clear Team Boundaries**

- Multiple autonomous teams (>3-4 teams)
- Teams aligned with business capabilities
- Clear ownership model
- Minimal coordination needed for releases

#### 6. **Frequent, Independent Deployments**

- Need to deploy multiple times per day
- Different features have different release cycles
- Rollback needs to be surgical, not all-or-nothing

#### 7. **Regulatory or Security Isolation**

- Need to isolate PCI-compliant payment processing
- Separate security boundaries required
- Data residency requirements
- **Example**: Healthcare application with HIPAA-compliant patient data service

---

## When NOT to Use Microservices

### Red Flags Against Microservices

#### 1. **Startups and MVPs**

- **Why**: Need to move fast and iterate
- **Reality**: Domain boundaries are unclear early on
- **Better**: Start with a well-structured monolith
- **Migrate**: Split when you have clear business domains and scaling needs

#### 2. **Small Teams (<10 developers)**

- **Why**: Operational overhead outweighs benefits
- **Reality**: Team will spend more time on infrastructure than features
- **Better**: Modular monolith with clear boundaries
- **Rule of Thumb**: You need at least 2-3 people to operate a microservices architecture

#### 3. **Simple, Small Applications**

- **Why**: Overhead doesn't justify complexity
- **Examples**: Internal tools, simple CRUD apps, marketing websites
- **Better**: Monolith, serverless functions, or low-code platforms

#### 4. **Unclear Domain Boundaries**

- **Why**: Wrong service boundaries lead to distributed monolith
- **Reality**: Constantly changing service boundaries is expensive
- **Better**: Use monolith to understand domain, then extract services
- **Warning**: Premature decomposition is worse than a monolith

#### 5. **Tight Data Coupling**

- **Why**: If services need frequent joins, they're not independent
- **Reality**: Network overhead kills performance
- **Better**: Keep tightly coupled data in same service/database
- **Example**: Order and OrderLine items should be together

#### 6. **No DevOps Culture or Infrastructure**

- **Why**: Manual deployments don't scale to many services
- **Required**: CI/CD, containerization, orchestration, monitoring
- **Better**: Build DevOps capabilities first with monolith
- **Reality**: Without automation, you'll drown in operational work

#### 7. **Limited Budget or Resources**

- **Why**: Infrastructure costs multiply with services
- **Reality**: Need for load balancers, service mesh, monitoring tools
- **Better**: Use simpler architectures until revenue supports investment

#### 8. **Real-Time Transactional Consistency Required**

- **Why**: Distributed transactions are complex and slow
- **Examples**: Banking transfers, inventory reservation, seat booking
- **Better**: Keep strongly consistent operations in same service
- **Alternative**: If splitting, use Saga pattern with compensation

---

## About This Example

This repository demonstrates a simple microservices architecture with two services that work together to provide a complete todo management system with audit logging.

### Architecture Overview

```
┌──────────────┐         ┌──────────────────┐
│              │  HTTP   │                  │
│   Client     │────────▶│  Todo Service    │
│              │         │  (Port 8000)     │
└──────────────┘         │                  │
                         │  - Create todos  │
                         │  - Delete todos  │
                         │  - Own database  │
                         └────────┬─────────┘
                                  │
                                  │ HTTP POST
                                  │ /audit/events
                                  │
                                  ▼
                         ┌────────────────────┐
                         │                    │
                         │  Audit Service     │
                         │  (Port 8001)       │
                         │                    │
                         │  - Log all events  │
                         │  - Query history   │
                         │  - Own database    │
                         └────────────────────┘

Data Isolation:
├── Todo Service   → todos.db  (SQLite)
└── Audit Service  → audit.db  (SQLite)
```

### Services Description

#### 1. Todo Service (Port 8000)

**Business Capability**: Manage todo items

**Responsibilities:**

- Create new todo items
- Delete todo items
- Publish audit events to Audit Service

**Data Owned:**

- Todo items (id, title, description, created_at)

**Dependencies:**

- Audit Service (for logging events)

#### 2. Audit Service (Port 8001)

**Business Capability**: Centralized audit logging

**Responsibilities:**

- Receive audit events from all services
- Store audit trail with timestamps
- Provide audit history query API

**Data Owned:**

- Audit logs (id, action, entity_type, entity_id, timestamp, metadata)

**Dependencies:**

- None (leaf service)

### Communication Flow Example

```
1. User creates a todo
   ├─▶ POST /todos/ → Todo Service
   │   ├─▶ Save to todos.db
   │   └─▶ POST /audit/events → Audit Service
   │       └─▶ Save to audit.db
   └─▶ Return todo to user

2. User deletes a todo
   ├─▶ DELETE /todos/{id} → Todo Service
   │   ├─▶ Delete from todos.db
   │   └─▶ POST /audit/events → Audit Service
   │       └─▶ Save to audit.db
   └─▶ Return success to user

3. User views audit trail
   └─▶ GET /audit/ → Audit Service
       └─▶ Return all audit logs
```

---

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

Both services should start successfully. You'll see:

- Audit Service: `Uvicorn running on http://127.0.0.1:8001`
- Todo Service: `Uvicorn running on http://127.0.0.1:8000`

### Testing the System

```bash
# 1. Create a todo (automatically creates audit log)
curl -X POST http://localhost:8000/todos/ \
  -H "Content-Type: application/json" \
  -d '{"title":"Buy groceries","description":"Milk, eggs, bread"}'

# Response: {"id":"123e4567-...","title":"Buy groceries",...}
# Copy the returned ID for next step

# 2. View all todos
curl http://localhost:8000/todos/

# 3. View audit logs (should show "todo_created" event)
curl http://localhost:8001/audit/

# 4. Delete the todo (automatically creates audit log)
curl -X DELETE http://localhost:8000/todos/{todo-id-here}

# 5. View audit logs again (should show both "todo_created" and "todo_deleted")
curl http://localhost:8001/audit/
```

### Interactive API Documentation

Both services provide interactive Swagger UI:

- Todo Service: http://localhost:8000/docs
- Audit Service: http://localhost:8001/docs

---

## Key Patterns Demonstrated

### 1. Service Independence

Each service is completely self-contained:

- Own codebase and directory structure
- Own database (no sharing)
- Own API endpoints and version
- Own dependencies (pyproject.toml)
- Can be deployed independently

### 2. Database Per Service

**Pattern**: Each microservice owns its data and database schema

**Implementation:**

- Todo Service: `todos.db` (SQLite)
- Audit Service: `audit.db` (SQLite)

**Benefits:**

- Services can't accidentally corrupt each other's data
- Schema changes are isolated
- Can choose different database types per service

**Tradeoff:**

- No cross-service SQL joins
- Need API calls to fetch related data

### 3. Synchronous HTTP Communication

**Pattern**: Services communicate via REST APIs

**Implementation:**

- Todo Service calls Audit Service via HTTP POST
- Uses `audit_client.py` to encapsulate communication

**Benefits:**

- Simple and widely understood
- Request-response semantics
- Easy to debug with HTTP tools

**Tradeoffs:**

- Creates temporal coupling (caller waits for response)
- Network failures affect functionality
- Slower than in-process calls

### 4. Graceful Degradation

**Pattern**: Core functionality works even if dependencies fail

**Implementation:**

```python
try:
    # Try to send audit event
    await audit_client.send_audit_event(...)
except Exception as e:
    # Log error but don't fail the todo operation
    logger.warning(f"Failed to send audit event: {e}")
```

**Benefits:**

- Todo operations succeed even if Audit Service is down
- System remains partially available
- Better user experience

### 5. Single Responsibility

**Pattern**: Each service has one clear business purpose

**Implementation:**

- Todo Service: Manages todos (ONLY)
- Audit Service: Logs events (ONLY)

**Benefits:**

- Easy to understand and modify
- Clear ownership boundaries
- Reduced coupling

### 6. API Contracts with Schemas

**Pattern**: Strongly typed request/response models

**Implementation:**

- Pydantic schemas in `schemas.py`
- Automatic validation
- Generated API documentation

**Benefits:**

- Prevents invalid data
- Self-documenting APIs
- Contract testing is easier

---

## Project Structure

```
services/
├── README.md                       # This file
│
├── todo_service/                   # Todo management microservice
│   ├── .venv/                      # Virtual environment
│   ├── alembic/                    # Database migrations
│   │   ├── versions/               # Migration scripts
│   │   └── env.py                  # Alembic configuration
│   ├── app/
│   │   ├── clients/
│   │   │   └── audit_client.py     # HTTP client for Audit service
│   │   ├── database.py             # SQLAlchemy setup
│   │   ├── models.py               # ORM models (Todo table)
│   │   ├── router.py               # FastAPI endpoints
│   │   ├── schemas.py              # Pydantic request/response models
│   │   └── service.py              # Business logic layer
│   ├── main.py                     # FastAPI app entry point
│   ├── pyproject.toml              # Python dependencies (uv format)
│   ├── alembic.ini                 # Alembic configuration
│   ├── todos.db                    # SQLite database (created on first run)
│   └── README.md                   # Service-specific documentation
│
└── audit_service/                  # Audit logging microservice
    ├── .venv/                      # Virtual environment
    ├── alembic/                    # Database migrations
    │   ├── versions/               # Migration scripts
    │   └── env.py                  # Alembic configuration
    ├── app/
    │   ├── database.py             # SQLAlchemy setup
    │   ├── models.py               # ORM models (AuditLog table)
    │   ├── router.py               # FastAPI endpoints
    │   ├── schemas.py              # Pydantic request/response models
    │   └── service.py              # Business logic layer
    ├── main.py                     # FastAPI app entry point
    ├── pyproject.toml              # Python dependencies (uv format)
    ├── alembic.ini                 # Alembic configuration
    ├── audit.db                    # SQLite database (created on first run)
    └── README.md                   # Service-specific documentation
```

---

## Best Practices

### 1. **Start with a Monolith**

- Build a well-structured monolith first
- Identify service boundaries through usage patterns
- Extract services when you have clear business reasons
- **Quote**: "Don't even consider microservices unless you have a system that's too complex to manage as a monolith" - Martin Fowler

### 2. **Design for Failure**

- Always expect network failures
- Implement timeouts on all external calls
- Use circuit breakers to prevent cascade failures
- Have fallback mechanisms

### 3. **Observability is Not Optional**

- Centralized logging (ELK, CloudWatch)
- Distributed tracing (Jaeger, Zipkin)
- Metrics and monitoring (Prometheus, Grafana)
- Correlation IDs across all requests

### 4. **API Versioning from Day One**

- Use version prefixes: `/v1/todos`, `/v2/todos`
- Maintain backward compatibility
- Deprecate old versions gradually
- Document breaking changes clearly

### 5. **Automate Everything**

- Automated testing (unit, integration, contract)
- CI/CD pipelines for each service
- Infrastructure as code (Terraform, CloudFormation)
- Automated rollbacks

### 6. **Data Management Strategy**

- One database per service (no sharing)
- Use events for data synchronization
- Accept eventual consistency
- Implement saga pattern for distributed transactions

### 7. **Security in Depth**

- Service-to-service authentication (mutual TLS)
- API Gateway for external traffic
- Secrets management (Vault, AWS Secrets Manager)
- Network policies and segmentation

### 8. **Clear Service Boundaries**

- Align with business capabilities, not technical layers
- Minimize inter-service dependencies
- Avoid circular dependencies
- Document service contracts

---

## Evolution Path

### Phase 1: Current Implementation ✅

- [x] Two services with clear responsibilities
- [x] HTTP/REST communication
- [x] Database per service pattern
- [x] Graceful degradation
- [x] SQLite for simplicity

### Phase 2: Production Ready

- [ ] **API Gateway**: Add Kong or Nginx as single entry point
- [ ] **Authentication**: Implement JWT-based auth
- [ ] **PostgreSQL**: Replace SQLite with production database
- [ ] **Health Checks**: Add `/health` and `/ready` endpoints
- [ ] **Logging**: Structured JSON logging with correlation IDs
- [ ] **Monitoring**: Add Prometheus metrics
- [ ] **Docker**: Containerize both services
- [ ] **Environment Config**: Separate dev/staging/prod configs

### Phase 3: Advanced Patterns

- [ ] **Async Messaging**: Replace some HTTP calls with RabbitMQ/Kafka
- [ ] **Event Sourcing**: Implement for audit service
- [ ] **Circuit Breaker**: Add Hystrix or resilience4j
- [ ] **Service Mesh**: Implement Istio or Linkerd
- [ ] **Distributed Tracing**: Add Jaeger with OpenTelemetry
- [ ] **Rate Limiting**: Per-service and per-client limits
- [ ] **Caching**: Add Redis for performance

### Phase 4: Cloud Native

- [ ] **Kubernetes**: Deploy to K8s cluster
- [ ] **Auto-scaling**: HPA based on CPU/memory/custom metrics
- [ ] **GitOps**: Implement ArgoCD or Flux
- [ ] **Multi-region**: Active-active deployment
- [ ] **Disaster Recovery**: Backup and restore procedures
- [ ] **Chaos Engineering**: Intentional failure testing
- [ ] **Cost Optimization**: Right-sizing and spot instances

---

## Related Patterns and Technologies

### Architectural Patterns

#### API Gateway

**Purpose**: Single entry point for all client requests

**Responsibilities:**

- Request routing to appropriate services
- Authentication and authorization
- Rate limiting and throttling
- Request/response transformation
- SSL termination

**Tools**: Kong, AWS API Gateway, Azure API Management, Nginx

#### Service Mesh

**Purpose**: Infrastructure layer for service-to-service communication

**Responsibilities:**

- Traffic management and load balancing
- Security (mutual TLS, encryption)
- Observability (metrics, tracing, logging)
- Resilience (retries, timeouts, circuit breakers)

**Tools**: Istio, Linkerd, Consul Connect

#### Circuit Breaker

**Purpose**: Prevent cascading failures

**How it works:**

1. **Closed**: Requests flow normally
2. **Open**: Fast fail after threshold of failures
3. **Half-Open**: Test if service recovered

**Tools**: Hystrix (deprecated but influential), resilience4j, Polly

#### Event Sourcing

**Purpose**: Store all state changes as events

**Benefits:**

- Complete audit trail
- Time travel (replay events)
- Event-driven architecture

**Tools**: EventStore, Kafka, AWS EventBridge

#### Saga Pattern

**Purpose**: Manage distributed transactions

**Types:**

- **Choreography**: Services publish events (decentralized)
- **Orchestration**: Central coordinator (centralized)

**Use case**: Multi-service transactions like order processing

#### CQRS (Command Query Responsibility Segregation)

**Purpose**: Separate read and write models

**Benefits:**

- Optimize reads and writes independently
- Scale reads separately from writes
- Works well with event sourcing

### Complementary Technologies

#### Containers

- **Docker**: Package services with dependencies
- **containerd**: Container runtime
- **Podman**: Daemon-less alternative to Docker

#### Orchestration

- **Kubernetes**: Industry standard for container orchestration
- **Docker Swarm**: Simpler alternative
- **AWS ECS/EKS**: Managed container services
- **Google GKE**: Managed Kubernetes

#### Message Queues

- **RabbitMQ**: AMQP-based message broker
- **Apache Kafka**: Distributed event streaming
- **AWS SQS**: Managed message queue
- **Google Pub/Sub**: Global message service

#### Monitoring & Observability

- **Prometheus**: Metrics collection and alerting
- **Grafana**: Metrics visualization
- **ELK Stack**: Elasticsearch, Logstash, Kibana for logs
- **Jaeger/Zipkin**: Distributed tracing
- **OpenTelemetry**: Unified observability standard
- **Datadog/New Relic**: All-in-one commercial solutions

#### Service Discovery

- **Consul**: Service mesh and discovery
- **Eureka**: Netflix's service registry
- **etcd**: Distributed key-value store
- **Kubernetes DNS**: Built-in service discovery

---

## Resources

### Books

- **"Building Microservices" by Sam Newman** (2nd Edition, 2021)  
  Comprehensive guide to microservices architecture

- **"Microservices Patterns" by Chris Richardson** (2018)  
  Pattern catalog for microservices development

- **"Release It!" by Michael Nygard** (2nd Edition, 2018)  
  Design and deploy production-ready software

- **"The Phoenix Project" by Gene Kim** (2013)  
  DevOps and organizational transformation

- **"Domain-Driven Design" by Eric Evans** (2003)  
  Foundational for understanding service boundaries

### Online Resources

- **[Microservices.io](https://microservices.io/)** - Pattern catalog by Chris Richardson
- **[Martin Fowler's Microservices Guide](https://martinfowler.com/microservices/)** - Foundational articles
- **[CNCF Landscape](https://landscape.cncf.io/)** - Cloud native tools ecosystem
- **[12-Factor App](https://12factor.net/)** - Methodology for modern applications
- **[AWS Microservices](https://aws.amazon.com/microservices/)** - Cloud provider perspective

### Video Courses

- **Microservices Architecture** - Pluralsight, Udemy, LinkedIn Learning
- **Kubernetes for Developers** - Linux Foundation (LFD459)
- **Docker Mastery** - Docker official training

### Communities

- **CNCF Slack** - Cloud Native Computing Foundation
- **Kubernetes Slack** - K8s community
- **Reddit** - r/microservices, r/devops, r/kubernetes

---

## Troubleshooting

### Services won't start

```bash
# Check if ports are already in use
lsof -i :8000
lsof -i :8001

# Kill processes if needed
kill -9 <PID>
```

### Audit service unreachable

- Verify Audit Service is running on port 8001
- Check `AUDIT_SERVICE_URL` in Todo Service configuration
- Review network/firewall rules

### Database errors

```bash
# Reset databases (CAUTION: deletes all data)
cd todo_service && rm todos.db && cd ..
cd audit_service && rm audit.db && cd ..

# Re-run migrations
cd todo_service && uv run alembic upgrade head && cd ..
cd audit_service && uv run alembic upgrade head && cd ..
```

---

## Contributing

To add new services to this example:

1. **Create service directory** under `services/`
2. **Follow existing structure** (app/, alembic/, main.py, etc.)
3. **Update this README** with service description and communication flows
4. **Document dependencies** and environment variables
5. **Add health check endpoint**

---

## License

This is an educational example for learning microservices architecture.  
Use freely for educational and reference purposes.

---

## Final Thoughts

> **"Microservices are not a free lunch."** - Martin Fowler

Microservices solve specific organizational and technical problems at the cost of increased complexity. They are a tool, not a goal.

**Start Simple:**

- Begin with a well-structured monolith
- Use clear module boundaries (future service boundaries)
- Invest in DevOps capabilities and automation

**Split When:**

- You have clear business domain boundaries
- Teams are large enough to own services
- You need independent scaling
- The benefits outweigh the operational costs

**Remember:**

- Most successful companies started with monoliths
- A distributed monolith is worse than a modular monolith
- Operational excellence is a prerequisite, not an afterthought
- Culture and organization matter more than technology

**The goal is not to have microservices. The goal is to build systems that serve your users and business effectively.**
