#!/bin/bash
set -e

# Create development environment file if not exists
if [ ! -f .env ]; then
    echo "Creating .env file from example..."
    cp .env.example .env
    # Generate random secret key
    SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_hex(32))')
    sed -i "s/your-64-character-secret-key/$SECRET_KEY/" .env
fi

# Create necessary directories
echo "Creating service directories..."
mkdir -p ./data/postgres ./data/minio ./data/redis ./data/rabbitmq

# Start all services in development mode
echo "Starting services..."
podman-compose up -d

# Wait for databases to be ready
echo "Waiting for databases to be ready..."
for service in character campaign image llm message-hub; do
    echo "Waiting for $service database..."
    until podman exec ${service}-db pg_isready; do
        echo "Database $service is unavailable - sleeping"
        sleep 1
    done
done

# Run database migrations
echo "Running database migrations..."
for service in character_service campaign_service image_service llm_service message_hub; do
    echo "Running migrations for $service..."
    podman exec $(echo $service | tr '_' '-') alembic upgrade head
done

# Initialize MinIO buckets
echo "Initializing MinIO buckets..."
podman exec image-service /app/scripts/init_storage.sh

# Download required models
echo "Downloading required models..."
# Download Stable Diffusion model for image service
podman exec image-service python3 -c "
import os
from huggingface_hub import snapshot_download
model_id = 'stabilityai/stable-diffusion-xl-base-1.0'
if not os.path.exists('/app/models/sdxl'):
    print(f'Downloading {model_id}...')
    snapshot_download(repo_id=model_id, local_dir='/app/models/sdxl', local_dir_use_symlinks=False)
"

# Check all services are healthy
echo "Checking service health..."
for service in character campaign image llm message-hub; do
    echo "Checking $service service..."
    timeout 30 bash -c "until curl -s http://localhost:$(grep -A 1 \"$service\" docker-compose.yml | grep ports | cut -d':' -f2 | tr -d ' ')/health > /dev/null; do echo \"Service $service is unavailable - sleeping\"; sleep 1; done"
done

echo "Development environment setup complete!"
echo "Services running at:"
echo "- Character Service: http://localhost:8000"
echo "- Campaign Service: http://localhost:8001"
echo "- Image Service:    http://localhost:8002"
echo "- LLM Service:      http://localhost:8100"
echo "- Message Hub:      http://localhost:8200"
echo "- API Gateway:      http://localhost:80"
echo "- API Dashboard:    http://localhost:8080"
echo "- MinIO Console:    http://localhost:9001"
echo "- RabbitMQ Admin:   http://localhost:15672"