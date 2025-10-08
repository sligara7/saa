#!/bin/bash
set -e

# Helper function to update a single service
update_service() {
    local service=$1
    local service_name=$(echo $service | tr '_' '-')
    echo "Updating $service..."

    # Stop the service
    podman-compose stop $service_name

    # Rebuild the container
    podman-compose build $service_name

    # Run migrations if needed
    if [ -d "$service/alembic" ]; then
        echo "Running migrations for $service..."
        podman-compose run --rm $service_name alembic upgrade head
    fi

    # Start the service
    podman-compose up -d $service_name

    # Wait for service to be healthy
    echo "Waiting for $service_name to be healthy..."
    timeout 30 bash -c "until curl -s http://localhost:$(grep -A 1 \"$service_name\" docker-compose.yml | grep ports | cut -d':' -f2 | tr -d ' ')/health > /dev/null; do echo \"Service $service_name is unavailable - sleeping\"; sleep 1; done"
}

# Update specific service if provided, otherwise update all
if [ "$1" ]; then
    if [ -d "$1" ]; then
        update_service $1
    else
        echo "Service directory $1 not found!"
        exit 1
    fi
else
    # Update all services in dependency order
    services=(
        "message_hub"
        "character_service"
        "campaign_service"
        "image_service"
        "llm_service"
    )
    
    for service in "${services[@]}"; do
        if [ -d "$service" ]; then
            update_service $service
        fi
    done
fi

echo "Service update complete!"