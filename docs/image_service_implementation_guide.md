# Image Service Implementation Guide

## Overview

The Image Service is responsible for generating character portraits, campaign maps, and other visual assets for the D&D Character Creator system. It manages image generation, storage, and retrieval, integrating with AI image generation models for content creation.

## Tech Stack

- **Core Framework**: FastAPI for async API development
- **Database**: PostgreSQL with SQLAlchemy for image metadata
- **Storage**: MinIO (S3-compatible) for image files
- **Image Generation**: Stable Diffusion with SDXL models
- **API Documentation**: OpenAPI/Swagger UI
- **Testing**: pytest with async support
- **Service Communication**: HTTP via Message Hub
- **Data Validation**: Pydantic
- **Database Migrations**: Alembic
- **Authentication**: JWT via shared auth system
- **Metrics**: Prometheus/Grafana

## Project Structure

```
image_service/
├── src/
│   ├── api/                    # API routes and controllers
│   │   ├── __init__.py
│   │   ├── characters.py       # Character portrait endpoints
│   │   ├── maps.py            # Map generation endpoints
│   │   └── tokens.py          # Token generation endpoints
│   ├── core/                   # Core business logic
│   │   ├── __init__.py
│   │   ├── generation.py       # Image generation logic
│   │   ├── storage.py         # Storage management
│   │   └── processing.py      # Image processing utilities
│   ├── db/                     # Database models and operations
│   │   ├── __init__.py
│   │   ├── models.py          # SQLAlchemy models
│   │   └── repositories.py     # Database access layer
│   ├── schemas/               # Pydantic models
│   │   ├── __init__.py
│   │   ├── generation.py      # Generation request/response models
│   │   └── image.py          # Image metadata models
│   └── services/              # External service integration
│       ├── __init__.py
│       ├── stable_diffusion.py # Stable Diffusion client
│       └── message_hub.py     # Message hub client
├── tests/                     # Test suites
│   ├── __init__.py
│   ├── conftest.py           # Test configuration
│   ├── test_api/            # API tests
│   ├── test_core/           # Core logic tests
│   └── test_services/       # Service integration tests
├── alembic/                  # Database migrations
│   ├── versions/
│   └── env.py
├── scripts/                 # Deployment and maintenance scripts
│   ├── start.sh            # Service startup
│   └── init_storage.sh     # Storage initialization
├── Dockerfile              # Container definition
├── pyproject.toml          # Python dependencies
└── alembic.ini            # Alembic configuration
```

## Core Components

### 1. Image Generation

The image generation system handles:
- Portrait generation for characters
- Map generation for campaigns
- Token generation for characters and NPCs
- Style and theme consistency

Key interfaces:
```python
class ImageGenerationService:
    async def generate_portrait(self, description: str, style: dict) -> Image
    async def generate_map(self, description: str, dimensions: Tuple[int, int]) -> Image
    async def generate_token(self, character_id: str, style: dict) -> Image
    async def apply_style(self, image: Image, style: dict) -> Image

class StableDiffusionClient:
    async def generate(self, prompt: str, params: dict) -> Image
    async def inpaint(self, image: Image, mask: Image, prompt: str) -> Image
    async def upscale(self, image: Image) -> Image
```

### 2. Storage Management

The storage system manages:
- Image file storage and retrieval
- Metadata management
- Cache management
- Storage cleanup

Key interfaces:
```python
class StorageService:
    async def store_image(self, image: Image, metadata: dict) -> str
    async def get_image(self, image_id: str) -> Image
    async def delete_image(self, image_id: str) -> bool
    async def update_metadata(self, image_id: str, metadata: dict) -> bool

class CacheService:
    async def cache_image(self, image_id: str, image: Image) -> None
    async def get_cached(self, image_id: str) -> Optional[Image]
    async def clear_cache(self, pattern: str = None) -> None
```

### 3. Service Integration

Integration with other services through the Message Hub:

```python
class ImageIntegrationService:
    async def get_character_details(self, character_id: str) -> CharacterDetails
    async def notify_image_ready(self, image_id: str, target_service: str) -> None
    async def process_generation_request(self, request: ImageRequest) -> ImageResponse
```

## Database Schema

### Image Metadata Table
```sql
CREATE TABLE images (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    storage_path VARCHAR(255) NOT NULL,
    content_type VARCHAR(50) NOT NULL,
    size_bytes INTEGER NOT NULL,
    width INTEGER NOT NULL,
    height INTEGER NOT NULL,
    format VARCHAR(10) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    metadata JSONB DEFAULT '{}'::jsonb,
    status VARCHAR(50) DEFAULT 'active',
    tags TEXT[] DEFAULT ARRAY[]::TEXT[]
);
```

### Generation Jobs Table
```sql
CREATE TABLE generation_jobs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    prompt TEXT NOT NULL,
    parameters JSONB NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE,
    result_image_id UUID REFERENCES images(id),
    error_message TEXT,
    metadata JSONB DEFAULT '{}'::jsonb
);
```

## API Endpoints

### Portrait Generation Endpoints
- `POST /api/v1/portraits` - Generate character portrait
- `GET /api/v1/portraits/{image_id}` - Get generated portrait
- `POST /api/v1/portraits/{image_id}/regenerate` - Regenerate portrait
- `DELETE /api/v1/portraits/{image_id}` - Delete portrait

### Map Generation Endpoints
- `POST /api/v1/maps` - Generate campaign map
- `GET /api/v1/maps/{image_id}` - Get generated map
- `PUT /api/v1/maps/{image_id}` - Update map details
- `DELETE /api/v1/maps/{image_id}` - Delete map

### Token Generation Endpoints
- `POST /api/v1/tokens` - Generate character token
- `GET /api/v1/tokens/{image_id}` - Get generated token
- `POST /api/v1/tokens/batch` - Batch generate tokens
- `DELETE /api/v1/tokens/{image_id}` - Delete token

## Message Hub Integration

### Subscribed Events
- `character.created` - New character creation
- `character.updated` - Character updates
- `campaign.location_added` - New campaign location
- `generation.requested` - Image generation requests

### Published Events
- `image.generated` - Image generation completed
- `image.failed` - Generation failure notification
- `image.updated` - Image metadata updates
- `image.deleted` - Image deletion notification

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
  --name image-db \
  -e POSTGRES_PASSWORD=mysecretpassword \
  -p 5432:5432 \
  postgres:13

# Start MinIO
podman run -d \
  --name image-storage \
  -e MINIO_ROOT_USER=minioadmin \
  -e MINIO_ROOT_PASSWORD=minioadmin \
  -p 9000:9000 \
  -p 9001:9001 \
  minio/minio server /data --console-address ":9001"

# Start Stable Diffusion (optional for development)
podman run -d \
  --name stable-diffusion \
  -p 7860:7860 \
  --gpus all \
  stabilityai/stable-diffusion-sdxl
```

3. Initialize storage and database:
```bash
./scripts/init_storage.sh
alembic upgrade head
```

4. Start development server:
```bash
uvicorn src.main:app --reload --port 8002
```

### Environment Variables

Required environment variables:
- `DATABASE_URL` - PostgreSQL connection string
- `STORAGE_URL` - MinIO/S3 connection string
- `MESSAGE_HUB_URL` - Message Hub service URL
- `SECRET_KEY` - JWT secret key
- `LOG_LEVEL` - Logging level (default: INFO)

Optional environment variables:
- `STABLE_DIFFUSION_URL` - Stable Diffusion API URL
- `CACHE_URL` - Redis cache URL
- `MAX_IMAGE_SIZE` - Maximum image size in bytes
- `STORAGE_BUCKET` - MinIO/S3 bucket name

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
4. Test image generation parameters
5. Validate storage operations

### Image Processing
1. Validate input images and parameters
2. Handle errors gracefully
3. Implement proper cleanup
4. Optimize for performance
5. Monitor resource usage

## Deployment

### Container Deployment

Build the container:
```bash
podman build -t image-service .
```

Run the container:
```bash
podman run -d \
  --name image-service \
  -p 8002:8000 \
  -e DATABASE_URL=postgresql://user:pass@db:5432/db \
  -e STORAGE_URL=s3://minioadmin:minioadmin@storage:9000 \
  -e MESSAGE_HUB_URL=http://message-hub:8200 \
  -e SECRET_KEY=your-secret-key \
  image-service
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
   - Storage operations
   - Processing times
   - Resource usage
2. Storage metrics:
   - Space usage
   - Operation latency
   - Error rates
3. System metrics:
   - GPU usage (if applicable)
   - Memory usage
   - Network bandwidth

## Troubleshooting

### Common Issues

1. Image Generation Issues
   - Check Stable Diffusion service health
   - Verify GPU availability
   - Review generation parameters
   - Check resource limits

2. Storage Issues
   - Verify MinIO/S3 connectivity
   - Check storage permissions
   - Monitor storage capacity
   - Validate file integrity

3. Performance Issues
   - Monitor queue length
   - Check resource utilization
   - Review caching effectiveness
   - Optimize generation parameters

### Debugging

1. Enable debug logging:
```bash
export LOG_LEVEL=DEBUG
```

2. Check service logs:
```bash
podman logs image-service
```

3. Monitor storage operations:
```bash
mc admin trace minio
```

4. Check Stable Diffusion logs:
```bash
podman logs stable-diffusion
```

## Future Improvements

1. Performance Optimizations
   - Implement batch processing
   - Enhance caching strategy
   - Optimize storage operations
   - Add request queuing

2. Feature Enhancements
   - Support more image types
   - Add image editing capabilities
   - Implement style transfer
   - Add batch operations

3. Technical Improvements
   - Add WebSocket support
   - Implement progressive loading
   - Add image transformation pipeline
   - Enhance error recovery