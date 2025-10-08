# Campaign Service Implementation Guide

## Overview

The Campaign Service is responsible for creating, managing, and evolving D&D campaigns. It handles campaign generation, chapter management, story progression, and integrates with other services to provide a comprehensive campaign management system.

## Tech Stack

- **Core Framework**: FastAPI for async API development
- **Database**: PostgreSQL with SQLAlchemy for async ORM
- **API Documentation**: OpenAPI/Swagger UI
- **Testing**: pytest with async support
- **Service Communication**: HTTP via Message Hub
- **Data Validation**: Pydantic
- **Database Migrations**: Alembic
- **Authentication**: JWT via shared auth system
- **Metrics**: Prometheus/Grafana

## Project Structure

```
campaign_service/
├── src/
│   ├── api/                 # API routes and controllers
│   │   ├── __init__.py
│   │   ├── campaigns.py     # Campaign CRUD operations
│   │   ├── chapters.py      # Chapter management
│   │   └── themes.py        # Theme system endpoints
│   ├── core/                # Core business logic
│   │   ├── __init__.py
│   │   ├── campaign.py      # Campaign generation/management
│   │   ├── chapter.py       # Chapter operations
│   │   └── theme.py         # Theme system logic
│   ├── db/                  # Database models and operations
│   │   ├── __init__.py
│   │   ├── models.py        # SQLAlchemy models
│   │   └── repositories.py  # Database access layer
│   ├── schemas/            # Pydantic models
│   │   ├── __init__.py
│   │   ├── campaign.py     # Campaign-related schemas
│   │   └── chapter.py      # Chapter-related schemas
│   └── services/           # External service integration
│       ├── __init__.py
│       ├── character.py    # Character service client
│       ├── llm.py         # LLM service client
│       └── message_hub.py  # Message hub client
├── tests/                  # Test suites
│   ├── __init__.py
│   ├── conftest.py        # Test configuration
│   ├── test_api/         # API tests
│   ├── test_core/        # Core logic tests
│   └── test_services/    # Service integration tests
├── alembic/               # Database migrations
│   ├── versions/
│   └── env.py
├── scripts/              # Deployment and maintenance scripts
│   ├── start.sh         # Service startup
│   └── init_db.sh       # Database initialization
├── Dockerfile           # Container definition
├── pyproject.toml       # Python dependencies
└── alembic.ini         # Alembic configuration
```

## Core Components

### 1. Campaign Management

The campaign management system handles:
- Campaign creation and generation
- Campaign state tracking
- Theme management
- Chapter organization
- Story progression
- Campaign versioning

Key interfaces:
```python
class CampaignService:
    async def create_campaign(self, concept: str, theme: str) -> Campaign
    async def generate_chapters(self, campaign_id: str) -> List[Chapter]
    async def evolve_campaign(self, campaign_id: str, events: List[Event]) -> Campaign
    async def version_campaign(self, campaign_id: str) -> CampaignVersion

class ChapterService:
    async def create_chapter(self, campaign_id: str, outline: str) -> Chapter
    async def generate_content(self, chapter_id: str) -> ChapterContent
    async def update_chapter(self, chapter_id: str, content: ChapterContent) -> Chapter
```

### 2. Theme System

The theme system manages:
- Campaign theme application
- Setting themes
- Theme transitions
- Theme-based content generation

Key interfaces:
```python
class ThemeService:
    async def apply_theme(self, campaign_id: str, theme: str) -> Campaign
    async def transition_theme(self, campaign_id: str, new_theme: str) -> Campaign
    async def validate_theme(self, content: Any, theme: str) -> bool
```

### 3. Service Integration

Integration with other services through the Message Hub:

```python
class CampaignIntegrationService:
    async def get_character_data(self, character_id: str) -> CharacterData
    async def generate_campaign_content(self, prompt: str) -> CampaignContent
    async def generate_chapter_image(self, description: str) -> ImageData
```

## Database Schema

### Campaign Table
```sql
CREATE TABLE campaigns (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    concept TEXT NOT NULL,
    theme VARCHAR(100) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    version INTEGER DEFAULT 1,
    status VARCHAR(50) DEFAULT 'draft',
    metadata JSONB DEFAULT '{}'::jsonb
);
```

### Chapter Table
```sql
CREATE TABLE chapters (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    campaign_id UUID REFERENCES campaigns(id),
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    sequence_number INTEGER NOT NULL,
    theme VARCHAR(100) NOT NULL,
    status VARCHAR(50) DEFAULT 'draft',
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

## API Endpoints

### Campaign Endpoints
- `POST /api/v1/campaigns` - Create new campaign
- `GET /api/v1/campaigns` - List campaigns
- `GET /api/v1/campaigns/{campaign_id}` - Get campaign details
- `PUT /api/v1/campaigns/{campaign_id}` - Update campaign
- `DELETE /api/v1/campaigns/{campaign_id}` - Delete campaign

### Chapter Endpoints
- `POST /api/v1/campaigns/{campaign_id}/chapters` - Create chapter
- `GET /api/v1/campaigns/{campaign_id}/chapters` - List chapters
- `GET /api/v1/chapters/{chapter_id}` - Get chapter details
- `PUT /api/v1/chapters/{chapter_id}` - Update chapter
- `DELETE /api/v1/chapters/{chapter_id}` - Delete chapter

### Theme Endpoints
- `POST /api/v1/campaigns/{campaign_id}/theme` - Set campaign theme
- `GET /api/v1/themes` - List available themes
- `POST /api/v1/campaigns/{campaign_id}/theme/transition` - Transition theme

## Message Hub Integration

### Subscribed Events
- `character.updated` - Character updates from Character Service
- `content.generated` - Content generation results from LLM Service
- `image.generated` - Image generation results from Image Service

### Published Events
- `campaign.created` - New campaign creation
- `campaign.updated` - Campaign updates
- `chapter.created` - New chapter creation
- `chapter.updated` - Chapter updates

## Setup and Development

### Local Development Setup

1. Set up Python virtual environment:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. Start PostgreSQL database:
```bash
podman run -d \
  --name campaign-db \
  -e POSTGRES_PASSWORD=mysecretpassword \
  -p 5432:5432 \
  postgres:13
```

3. Run database migrations:
```bash
alembic upgrade head
```

4. Start development server:
```bash
uvicorn src.main:app --reload --port 8001
```

### Environment Variables

Required environment variables:
- `DATABASE_URL` - PostgreSQL connection string
- `MESSAGE_HUB_URL` - Message Hub service URL
- `SECRET_KEY` - JWT secret key
- `LOG_LEVEL` - Logging level (default: INFO)

Optional environment variables:
- `CHARACTER_SERVICE_URL` - Character service URL
- `LLM_SERVICE_URL` - LLM service URL
- `IMAGE_SERVICE_URL` - Image service URL

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
3. Mock external service calls in tests
4. Maintain high test coverage

### Database Operations
1. Use SQLAlchemy for database operations
2. Create migrations for schema changes
3. Use repositories for data access
4. Handle transactions properly

## Deployment

### Container Deployment

Build the container:
```bash
podman build -t campaign-service .
```

Run the container:
```bash
podman run -d \
  --name campaign-service \
  -p 8001:8000 \
  -e DATABASE_URL=postgresql://user:pass@db:5432/db \
  -e MESSAGE_HUB_URL=http://message-hub:8200 \
  -e SECRET_KEY=your-secret-key \
  campaign-service
```

### Health Checks

The service provides:
- `/health` - Basic health check
- `/metrics` - Prometheus metrics
- `/docs` - API documentation

### Monitoring

Monitor service health with:
1. Prometheus metrics
2. PostgreSQL query metrics
3. API response times
4. Error rates and types

## Troubleshooting

### Common Issues

1. Database Connection Issues
   - Check DATABASE_URL environment variable
   - Verify database is running
   - Check network connectivity

2. Message Hub Communication
   - Verify MESSAGE_HUB_URL is correct
   - Check Message Hub health
   - Review connection logs

3. Performance Issues
   - Monitor database query performance
   - Check connection pool settings
   - Review API response times

### Debugging

1. Enable debug logging:
```bash
export LOG_LEVEL=DEBUG
```

2. Check service logs:
```bash
podman logs campaign-service
```

3. Review metrics dashboard for issues

## Future Improvements

1. Performance Optimizations
   - Query optimization
   - Caching layer
   - Batch processing

2. Feature Enhancements
   - Advanced theme system
   - Campaign templates
   - Enhanced versioning

3. Technical Improvements
   - GraphQL API
   - Real-time updates
   - Enhanced monitoring