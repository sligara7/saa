# LLM Service Implementation Guide

## Overview

The LLM Service is a centralized service that handles all AI-driven text and content generation for the D&D Character Creator system. It manages interactions with language models, provides caching and rate limiting, and ensures consistent AI responses across all services.

## Tech Stack

- **Core Framework**: FastAPI for async API development
- **Database**: PostgreSQL with SQLAlchemy for request/response caching
- **Cache**: Redis for response caching and rate limiting
- **LLM Integration**: 
  - OpenAI API (GPT-4)
  - Anthropic (Claude)
  - Local models via Ollama
- **API Documentation**: OpenAPI/Swagger UI
- **Testing**: pytest with async support
- **Service Communication**: HTTP via Message Hub
- **Data Validation**: Pydantic
- **Database Migrations**: Alembic
- **Authentication**: JWT via shared auth system
- **Metrics**: Prometheus/Grafana

## Project Structure

```
llm_service/
├── src/
│   ├── api/                 # API routes and controllers
│   │   ├── __init__.py
│   │   ├── generation.py   # Generation endpoints
│   │   └── models.py       # Model management endpoints
│   ├── core/               # Core business logic
│   │   ├── __init__.py
│   │   ├── generation.py   # Generation orchestration
│   │   ├── prompts.py     # Prompt management
│   │   └── validation.py  # Response validation
│   ├── db/                 # Database models and operations
│   │   ├── __init__.py
│   │   ├── models.py      # SQLAlchemy models
│   │   └── repositories.py # Database access layer
│   ├── llm/               # LLM provider integrations
│   │   ├── __init__.py
│   │   ├── openai.py     # OpenAI integration
│   │   ├── anthropic.py  # Anthropic integration
│   │   └── ollama.py     # Ollama integration
│   ├── schemas/           # Pydantic models
│   │   ├── __init__.py
│   │   ├── requests.py   # Request models
│   │   └── responses.py  # Response models
│   └── services/          # External service integration
│       ├── __init__.py
│       ├── cache.py      # Caching service
│       └── message_hub.py # Message hub client
├── tests/                 # Test suites
│   ├── __init__.py
│   ├── conftest.py       # Test configuration
│   ├── test_api/        # API tests
│   ├── test_core/       # Core logic tests
│   └── test_llm/        # LLM integration tests
├── alembic/              # Database migrations
│   ├── versions/
│   └── env.py
├── prompts/             # Prompt templates
│   ├── character/
│   ├── campaign/
│   └── common/
├── scripts/             # Deployment and maintenance scripts
│   ├── start.sh        # Service startup
│   └── init_cache.sh   # Cache initialization
├── Dockerfile          # Container definition
├── pyproject.toml      # Python dependencies
└── alembic.ini        # Alembic configuration
```

## Core Components

### 1. Generation Management

The generation system handles:
- Text generation requests
- Prompt management
- Response validation
- Fallback strategies

Key interfaces:
```python
class GenerationService:
    async def generate_text(
        self, 
        prompt: str, 
        context: dict,
        model: str = "gpt-4"
    ) -> TextResponse
    
    async def stream_text(
        self, 
        prompt: str, 
        context: dict,
        model: str = "gpt-4"
    ) -> AsyncIterator[str]
    
    async def batch_generate(
        self,
        requests: List[GenerationRequest]
    ) -> List[TextResponse]

class PromptService:
    async def get_prompt_template(self, template_id: str) -> str
    async def render_prompt(self, template_id: str, params: dict) -> str
    async def validate_prompt(self, prompt: str) -> bool
```

### 2. LLM Provider Management

The provider system manages:
- Multiple LLM providers
- Model selection
- Rate limiting
- Error handling

Key interfaces:
```python
class LLMProviderManager:
    async def select_provider(self, requirements: dict) -> LLMProvider
    async def get_model_config(self, model: str) -> ModelConfig
    async def list_available_models(self) -> List[ModelInfo]

class BaseProvider:
    async def generate(self, prompt: str, params: dict) -> str
    async def stream(self, prompt: str, params: dict) -> AsyncIterator[str]
    async def validate_response(self, response: str) -> bool
```

### 3. Caching and Rate Limiting

The caching system manages:
- Response caching
- Rate limit tracking
- Token usage monitoring
- Cache invalidation

Key interfaces:
```python
class CacheService:
    async def get_cached_response(self, key: str) -> Optional[str]
    async def cache_response(self, key: str, response: str) -> None
    async def clear_cache(self, pattern: str = None) -> None

class RateLimitService:
    async def check_rate_limit(self, user_id: str) -> bool
    async def track_request(self, user_id: str, tokens: int) -> None
    async def get_usage_stats(self, user_id: str) -> UsageStats
```

## Database Schema

### Generation Requests Table
```sql
CREATE TABLE generation_requests (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    prompt TEXT NOT NULL,
    context JSONB DEFAULT '{}'::jsonb,
    model VARCHAR(50) NOT NULL,
    user_id UUID NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE,
    tokens_used INTEGER,
    status VARCHAR(50) DEFAULT 'pending',
    error_message TEXT,
    metadata JSONB DEFAULT '{}'::jsonb
);
```

### Response Cache Table
```sql
CREATE TABLE response_cache (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    cache_key VARCHAR(255) NOT NULL UNIQUE,
    response TEXT NOT NULL,
    prompt TEXT NOT NULL,
    model VARCHAR(50) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    expires_at TIMESTAMP WITH TIME ZONE,
    metadata JSONB DEFAULT '{}'::jsonb
);
```

## API Endpoints

### Generation Endpoints
- `POST /api/v1/generate` - Generate text response
- `POST /api/v1/generate/stream` - Stream text response
- `POST /api/v1/generate/batch` - Batch generate responses
- `GET /api/v1/generate/{request_id}` - Get generation result

### Model Management Endpoints
- `GET /api/v1/models` - List available models
- `GET /api/v1/models/{model_id}` - Get model details
- `POST /api/v1/models/select` - Select optimal model

### Usage Management Endpoints
- `GET /api/v1/usage` - Get usage statistics
- `GET /api/v1/usage/{user_id}` - Get user usage stats
- `GET /api/v1/rate_limits` - Get rate limit status

## Message Hub Integration

### Subscribed Events
- `generation.requested` - Generation requests from services
- `model.updated` - Model configuration updates
- `cache.invalidate` - Cache invalidation requests

### Published Events
- `generation.completed` - Generation completion
- `generation.failed` - Generation failures
- `usage.updated` - Usage statistics updates

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
  --name llm-db \
  -e POSTGRES_PASSWORD=mysecretpassword \
  -p 5432:5432 \
  postgres:13

# Start Redis
podman run -d \
  --name llm-cache \
  -p 6379:6379 \
  redis:6

# Start Ollama (optional for local LLM)
podman run -d \
  --name ollama \
  -p 11434:11434 \
  ollama/ollama
```

3. Initialize services:
```bash
./scripts/init_cache.sh
alembic upgrade head
```

4. Start development server:
```bash
uvicorn src.main:app --reload --port 8100
```

### Environment Variables

Required environment variables:
- `DATABASE_URL` - PostgreSQL connection string
- `REDIS_URL` - Redis connection string
- `MESSAGE_HUB_URL` - Message Hub service URL
- `SECRET_KEY` - JWT secret key
- `LOG_LEVEL` - Logging level (default: INFO)

Optional environment variables:
- `OPENAI_API_KEY` - OpenAI API key
- `ANTHROPIC_API_KEY` - Anthropic API key
- `OLLAMA_URL` - Ollama API URL
- `DEFAULT_MODEL` - Default model to use
- `CACHE_TTL` - Cache time-to-live in seconds
- `RATE_LIMIT_RPM` - Rate limit requests per minute

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
3. Mock external LLM providers in tests
4. Test caching and rate limiting
5. Validate prompt templates

### LLM Integration
1. Handle provider errors gracefully
2. Implement proper fallback strategies
3. Validate responses thoroughly
4. Monitor token usage
5. Optimize prompt efficiency

## Deployment

### Container Deployment

Build the container:
```bash
podman build -t llm-service .
```

Run the container:
```bash
podman run -d \
  --name llm-service \
  -p 8100:8000 \
  -e DATABASE_URL=postgresql://user:pass@db:5432/db \
  -e REDIS_URL=redis://cache:6379 \
  -e MESSAGE_HUB_URL=http://message-hub:8200 \
  -e OPENAI_API_KEY=your-api-key \
  -e SECRET_KEY=your-secret-key \
  llm-service
```

### Health Checks

The service provides:
- `/health` - Basic health check
- `/metrics` - Prometheus metrics
- `/docs` - API documentation

### Monitoring

Monitor service health with:
1. Prometheus metrics for:
   - Generation requests and success rates
   - Token usage
   - Response times
   - Cache hit rates
   - Rate limit status
2. Provider metrics:
   - API latency
   - Error rates
   - Cost tracking
3. System metrics:
   - Memory usage
   - CPU utilization
   - Network bandwidth

## Troubleshooting

### Common Issues

1. LLM Provider Issues
   - Check API keys and quotas
   - Verify provider status
   - Review error responses
   - Check rate limits

2. Cache Issues
   - Verify Redis connectivity
   - Check cache size
   - Monitor hit rates
   - Review invalidation logs

3. Performance Issues
   - Check request queues
   - Monitor token usage
   - Review response times
   - Optimize prompts

### Debugging

1. Enable debug logging:
```bash
export LOG_LEVEL=DEBUG
```

2. Check service logs:
```bash
podman logs llm-service
```

3. Monitor Redis:
```bash
redis-cli monitor
```

4. Check provider status:
```bash
curl https://api.openai.com/v1/health
```

## Future Improvements

1. Performance Optimizations
   - Enhanced caching strategies
   - Prompt optimization
   - Request batching
   - Response streaming

2. Feature Enhancements
   - More LLM providers
   - Advanced prompt management
   - Response quality metrics
   - Cost optimization

3. Technical Improvements
   - WebSocket support
   - Enhanced monitoring
   - Automated testing
   - Provider failover