# Message Hub Implementation Guide

## Overview

The Message Hub is a central service that manages all inter-service communication in the D&D Character Creator system. It provides reliable message routing, implements circuit breakers and retries, manages transactions, and ensures consistent communication patterns across services.

## Tech Stack

- **Core Framework**: FastAPI for async API development
- **Database**: PostgreSQL with SQLAlchemy for message persistence
- **Queue**: RabbitMQ for message queuing
- **Cache**: Redis for circuit breaker state
- **API Documentation**: OpenAPI/Swagger UI
- **Testing**: pytest with async support
- **Data Validation**: Pydantic
- **Database Migrations**: Alembic
- **Authentication**: JWT via shared auth system
- **Metrics**: Prometheus/Grafana

## Project Structure

```
message_hub/
├── src/
│   ├── api/                      # API routes and controllers
│   │   ├── __init__.py
│   │   ├── routes.py            # Message routing endpoints
│   │   └── service_registry.py  # Service management endpoints
│   ├── core/                     # Core business logic
│   │   ├── __init__.py
│   │   ├── router.py           # Message routing logic
│   │   ├── circuit_breaker.py  # Circuit breaker implementation
│   │   └── transaction.py      # Transaction management
│   ├── db/                      # Database models and operations
│   │   ├── __init__.py
│   │   ├── models.py           # SQLAlchemy models
│   │   └── repositories.py     # Database access layer
│   ├── queue/                   # Queue management
│   │   ├── __init__.py
│   │   ├── producer.py         # Message producer
│   │   └── consumer.py         # Message consumer
│   ├── schemas/                 # Pydantic models
│   │   ├── __init__.py
│   │   ├── message.py          # Message schemas
│   │   └── service.py          # Service schemas
│   └── services/               # Service management
│       ├── __init__.py
│       ├── registry.py         # Service registry
│       └── health.py          # Health checking
├── tests/                      # Test suites
│   ├── __init__.py
│   ├── conftest.py            # Test configuration
│   ├── test_api/             # API tests
│   ├── test_core/            # Core logic tests
│   └── test_queue/           # Queue tests
├── alembic/                   # Database migrations
│   ├── versions/
│   └── env.py
├── scripts/                  # Deployment and maintenance scripts
│   ├── start.sh             # Service startup
│   └── setup_queues.sh     # Queue initialization
├── Dockerfile               # Container definition
├── pyproject.toml           # Python dependencies
└── alembic.ini             # Alembic configuration
```

## Core Components

### 1. Message Routing

The routing system handles:
- Message routing between services
- Circuit breaker management
- Retry policies
- Error handling

Key interfaces:
```python
class MessageRouter:
    async def route_message(self, message: Message) -> MessageResponse
    async def route_batch(self, messages: List[Message]) -> List[MessageResponse]
    async def get_routes(self, service_name: str) -> List[Route]

class MessageValidator:
    async def validate_message(self, message: Message) -> bool
    async def validate_route(self, route: Route) -> bool
    async def get_validation_errors(self) -> List[str]
```

### 2. Circuit Breaker

The circuit breaker system manages:
- Service health tracking
- Failure detection
- Recovery management
- State transitions

Key interfaces:
```python
class CircuitBreaker:
    async def check_state(self, service: str) -> CircuitState
    async def record_success(self, service: str) -> None
    async def record_failure(self, service: str) -> None
    async def reset(self, service: str) -> None

class CircuitBreakerRegistry:
    async def get_breaker(self, service: str) -> CircuitBreaker
    async def list_breakers(self) -> List[CircuitBreakerStatus]
    async def update_config(self, config: CircuitBreakerConfig) -> None
```

### 3. Transaction Management

The transaction system manages:
- Distributed transactions
- Two-phase commit
- Rollback operations
- Transaction state

Key interfaces:
```python
class TransactionCoordinator:
    async def begin_transaction(self) -> Transaction
    async def prepare(self, transaction_id: str) -> bool
    async def commit(self, transaction_id: str) -> bool
    async def rollback(self, transaction_id: str) -> bool

class TransactionRegistry:
    async def register_participant(self, transaction_id: str, service: str) -> None
    async def get_transaction(self, transaction_id: str) -> Transaction
    async def list_active_transactions(self) -> List[Transaction]
```

## Database Schema

### Messages Table
```sql
CREATE TABLE messages (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    sender_service VARCHAR(100) NOT NULL,
    target_service VARCHAR(100) NOT NULL,
    message_type VARCHAR(100) NOT NULL,
    content JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    processed_at TIMESTAMP WITH TIME ZONE,
    status VARCHAR(50) DEFAULT 'pending',
    retry_count INTEGER DEFAULT 0,
    error_message TEXT,
    metadata JSONB DEFAULT '{}'::jsonb
);
```

### Circuit Breaker State Table
```sql
CREATE TABLE circuit_breaker_state (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    service_name VARCHAR(100) NOT NULL UNIQUE,
    state VARCHAR(50) NOT NULL DEFAULT 'closed',
    failure_count INTEGER DEFAULT 0,
    last_failure_time TIMESTAMP WITH TIME ZONE,
    last_success_time TIMESTAMP WITH TIME ZONE,
    reset_timeout INTEGER DEFAULT 60,
    failure_threshold INTEGER DEFAULT 5,
    metadata JSONB DEFAULT '{}'::jsonb
);
```

### Transaction State Table
```sql
CREATE TABLE transactions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    status VARCHAR(50) NOT NULL DEFAULT 'pending',
    participants JSONB NOT NULL DEFAULT '[]'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    timeout_at TIMESTAMP WITH TIME ZONE,
    metadata JSONB DEFAULT '{}'::jsonb
);
```

## API Endpoints

### Message Routing Endpoints
- `POST /api/v1/messages` - Send message
- `POST /api/v1/messages/batch` - Send batch of messages
- `GET /api/v1/messages/{message_id}` - Get message status
- `DELETE /api/v1/messages/{message_id}` - Cancel message

### Circuit Breaker Endpoints
- `GET /api/v1/circuit-breakers` - List circuit breaker states
- `GET /api/v1/circuit-breakers/{service}` - Get service breaker state
- `POST /api/v1/circuit-breakers/{service}/reset` - Reset circuit breaker

### Transaction Endpoints
- `POST /api/v1/transactions` - Begin transaction
- `POST /api/v1/transactions/{id}/prepare` - Prepare transaction
- `POST /api/v1/transactions/{id}/commit` - Commit transaction
- `POST /api/v1/transactions/{id}/rollback` - Rollback transaction

## Service Registry Integration

### Service Registration
```python
@app.post("/api/v1/services/register")
async def register_service(service: ServiceRegistration) -> ServiceInfo:
    """Register a new service with the message hub."""

@app.delete("/api/v1/services/{service_name}")
async def deregister_service(service_name: str) -> None:
    """Deregister a service from the message hub."""
```

### Health Checking
```python
@app.get("/api/v1/services/{service_name}/health")
async def check_service_health(service_name: str) -> HealthStatus:
    """Check the health status of a registered service."""

@app.get("/api/v1/services/health")
async def check_all_services_health() -> List[HealthStatus]:
    """Check health status of all registered services."""
```

## Setup and Development

### Local Development Setup

1. Set up Python virtual environment:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. Start dependencies:
```bash
# Start PostgreSQL
podman run -d \
  --name message-db \
  -e POSTGRES_PASSWORD=mysecretpassword \
  -p 5432:5432 \
  postgres:13

# Start Redis
podman run -d \
  --name message-cache \
  -p 6379:6379 \
  redis:6

# Start RabbitMQ
podman run -d \
  --name message-queue \
  -p 5672:5672 \
  -p 15672:15672 \
  rabbitmq:3-management
```

3. Initialize services:
```bash
./scripts/setup_queues.sh
alembic upgrade head
```

4. Start development server:
```bash
uvicorn src.main:app --reload --port 8200
```

### Environment Variables

Required environment variables:
- `DATABASE_URL` - PostgreSQL connection string
- `REDIS_URL` - Redis connection string
- `RABBITMQ_URL` - RabbitMQ connection string
- `SECRET_KEY` - JWT secret key
- `LOG_LEVEL` - Logging level (default: INFO)

Optional environment variables:
- `CIRCUIT_BREAKER_TIMEOUT` - Circuit breaker reset timeout
- `CIRCUIT_BREAKER_THRESHOLD` - Circuit breaker failure threshold
- `TRANSACTION_TIMEOUT` - Transaction timeout in seconds
- `MAX_RETRIES` - Maximum message retry attempts
- `QUEUE_PREFIX` - RabbitMQ queue name prefix

### Running Tests

Run the test suite:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=src tests/
```

## Development Guidelines

### Code Organization
1. Follow Clean Architecture principles
2. Keep business logic in core/ directory
3. Use dependency injection for service integration
4. Maintain clear separation of concerns

### API Development
1. Use FastAPI dependency injection
2. Document all endpoints with OpenAPI
3. Validate requests with Pydantic models
4. Follow REST best practices

### Testing Strategy
1. Write unit tests for core logic
2. Write integration tests for API endpoints
3. Test message routing patterns
4. Test circuit breaker behavior
5. Validate transaction management

### Queue Management
1. Handle connection failures
2. Implement proper error handling
3. Monitor queue depths
4. Manage message persistence
5. Implement dead letter queues

## Deployment

### Container Deployment

Build the container:
```bash
podman build -t message-hub .
```

Run the container:
```bash
podman run -d \
  --name message-hub \
  -p 8200:8000 \
  -e DATABASE_URL=postgresql://user:pass@db:5432/db \
  -e REDIS_URL=redis://cache:6379 \
  -e RABBITMQ_URL=amqp://user:pass@queue:5672 \
  -e SECRET_KEY=your-secret-key \
  message-hub
```

### Health Checks

The service provides:
- `/health` - Basic health check
- `/metrics` - Prometheus metrics
- `/docs` - API documentation

### Monitoring

Monitor service health with:
1. Prometheus metrics for:
   - Message routing rates
   - Circuit breaker states
   - Queue depths
   - Transaction states
2. Queue metrics:
   - Consumer status
   - Message rates
   - Error rates
3. System metrics:
   - Memory usage
   - CPU utilization
   - Network bandwidth

## Troubleshooting

### Common Issues

1. Queue Issues
   - Check RabbitMQ connectivity
   - Verify queue existence
   - Monitor queue depth
   - Check consumer status

2. Circuit Breaker Issues
   - Review failure thresholds
   - Check state transitions
   - Verify recovery behavior
   - Monitor service health

3. Transaction Issues
   - Check transaction timeouts
   - Review participant status
   - Monitor prepare/commit phases
   - Verify rollback behavior

### Debugging

1. Enable debug logging:
```bash
export LOG_LEVEL=DEBUG
```

2. Check service logs:
```bash
podman logs message-hub
```

3. Monitor RabbitMQ:
```bash
# Access RabbitMQ management UI at http://localhost:15672
```

4. Check Redis state:
```bash
redis-cli monitor
```

## Future Improvements

1. Performance Optimizations
   - Message batching
   - Queue optimization
   - Connection pooling
   - Cache optimization

2. Feature Enhancements
   - Advanced routing patterns
   - Priority queues
   - Dead letter handling
   - Service discovery

3. Technical Improvements
   - Enhanced monitoring
   - Automated failover
   - Dynamic configuration
   - Advanced transaction patterns